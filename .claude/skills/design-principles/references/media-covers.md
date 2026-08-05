# 视频封面图 / 缩略图设计规范

> 所属 skill：design-principles。做视频卡片、结果画廊、媒体网格时读本文件。

## 1. 生成策略（两种，按场景选）

| 场景 | 策略 | 存放 | 参考实现 |
|------|------|------|---------|
| 跑批产物（数量已知，随批生成） | **批量预生成**：跑批脚本在产出视频的同时提取封面 | `outputs/covers/{video_stem}.jpg` | pet `scripts/speedrun.py` |
| 浏览任意目录（数量未知，按需） | **请求时生成 + 磁盘缓存**：thumb 端点缓存 miss 时提取 | `.thumbs/{md5(abs_path)[:16]}.jpg`（点目录，浏览列表跳过） | `server/routers/datasets.py` |

统一提取方法——**cv2 中间帧 + JPEG q80**（不依赖 ffmpeg CLI）：

```python
import cv2
cap = cv2.VideoCapture(video_path)
total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
if total > 2:
    cap.set(cv2.CAP_PROP_POS_FRAMES, total // 2)   # 中间帧比首帧更有代表性
ok, frame = cap.read()
cap.release()
if ok and frame is not None:
    cv2.imwrite(cover_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
```

要点：

- **封面共享**：N 视频 × M 模型的跑批，封面按源视频生成一次、所有模型共用（N 张而非 N×M 张）
- **幂等**：`if not os.path.isfile(cover_path)` skip-if-exists，重跑不重复提取
- **cv2 惰性 import**：只在缓存 miss 时 import；未安装时优雅降级（404 + 前端图标 fallback），不能拖垮整个路由
- 体积预算：缩略图 < 100KB/张，原图只在详情/预览层加载
- 批量生成用本 skill 的 `scripts/extract_covers.py`

## 2. 服务端点

单一 catch-all 静态端点同时服务视频与图片，按扩展名给 MIME：

```python
@router.get("/outputs/{file_path:path}")
async def serve_output(file_path: str):
    safe = safe_resolve(OUTPUTS_DIR, file_path)   # 防路径穿越，必须
    ext = os.path.splitext(safe)[1].lower()
    media = VIDEO_MIME.get(ext) or IMAGE_MIME.get(ext) or "application/octet-stream"
    return FileResponse(safe, media_type=media, filename=os.path.basename(safe))
```

## 3. 前端展示（卡片 thumb 公约）

固定高度盒 + `object-fit: cover`，**不是** aspect-ratio 盒；`loading="lazy"`；无封面时用图标 fallback（`v-if/v-else` 分支，不靠 `@error`）：

```vue
<div class="thumb">
  <img v-if="r.cover_image" :src="coverUrl(r.cover_image)" class="cover-img" loading="lazy" />
  <n-icon v-else size="36"><play-circle-outline /></n-icon>
  <span class="play-overlay">▶</span>
  <span v-if="r.correct === true" class="badge correct">✓</span>
</div>
```

```scss
.thumb {
  position: relative; height: 120px;              // 画廊 120px / 目录浏览 100px
  display: flex; align-items: center; justify-content: center;
  background: #000; overflow: hidden;
  .cover-img { width: 100%; height: 100%; object-fit: cover; }
  .play-overlay {
    position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
    font-size: 28px; color: rgba(255,255,255,.8);
    text-shadow: 0 2px 8px rgba(0,0,0,.6); pointer-events: none;
  }
  .badge {                                         // 状态角标：左上角圆形
    position: absolute; top: 6px; left: 8px;
    width: 22px; height: 22px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center; color: #fff;
    &.correct { background: #22c55e; }
    &.wrong { background: #ef4444; }
    &.na { background: #71717a; }
  }
}
```

## 4. 视频本体加载

- 列表/卡片层**永远不放 `<video>`**，封面图承担视觉；点击后弹 `VideoModal` 播放
- 弹窗内 `<video controls preload="none" playsinline>` —— 只有用户点播放才请求字节
- 弹窗 `v-if="show"` 控制挂载，关闭即卸载，避免后台继续缓冲
- 文件类型分支：目录→文件夹图标、图片→原图直显（`/file`）、视频→缩略图（`/thumb`）+ ▶ overlay、其他→文档图标
