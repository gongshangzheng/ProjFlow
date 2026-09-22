# Design: add-doc-image-assets

## Context

见 proposal.md — Why。已核实事实：

- `server/main.py` 只 `include_router` 各模块路由，**无任何 `StaticFiles` 挂载**
- `management.router` 前缀 `/api/management`，已有 `GET /docs` 与 `GET /docs/{slug:path}`（路径段是 `docs`，与拟挂的 `docs-assets` 不冲突）
- `GET /api/management/docs` 用 `os.walk` 且**仅收 `*.md`** → `_assets/` 下的图片不会被当成文档
- `MarkdownRenderer.vue`：markdown-it `html:false` + `linkify` + `typographer` + `breaks` + `markdown-it-task-checkbox` + mermaid；**无 image 相关处理，无样式**
- `web/vite.config.js` 已把 `/api` 代理到 `http://localhost:8809` → 新端点自动可用，无需改 Vite
- `server/requirements.txt`：`fastapi==0.115.0`（Starlette StaticFiles 无需额外依赖）

## Goals / Non-Goals

**Goals:**

- 文档能可靠嵌入并显示图片，且引用方式在 SPA 路由下不会解析错
- 图片语义化（`figure`/`figcaption`），图题可读、可样式化、对 SEO/a11y 友好
- 零新增依赖（后端与前端都不加包）
- 既有无图文档零影响

**Non-Goals:**

- 不做图片上传 UI（本 change 只提供"放置 + 服务 + 引用"能力，素材由 skill/人工落盘）
- 不做图床/对象存储/CDN
- 不引入 markdown-it 插件（`markdown-it-image-figures` 等），避免新增依赖与 lock 变更
- 不做图片压缩服务端转码（规范约束在产出侧，见 D6）

## Decisions

### D1: 存储位置 `management/docs/_assets/<slug>/`

- 下划线前缀表达"非文档资产"，与文档 slug 命名空间天然隔离；`<slug>` 与文档 slug 对齐，便于"这篇文档的图"一眼可查
- **配套加固**：`get_docs()` 的 `os.walk` 过滤掉下划线前缀目录（`dirs[:] = [d for d in dirs if not d.startswith('_')]`）。实测发现：仅靠"只收 `.md`"不够——放在 `_assets/` 下的 `README.md` 会被当成 wiki 文档出现在列表里；过滤后连误放的 `.md` 也不会入库（非下划线子目录如 `notes/` 不受影响）
- 备选：`management/assets/`（全局）→ 与文档的对应关系变弱；`papers/cache/`（已 gitignore）→ 图片属内容不可忽略
- 该目录随 git 入库（图片是文档内容的一部分）；空目录用 `.gitkeep` 保留

### D2: 服务端点 `/api/management/docs-assets`

```python
from fastapi.staticfiles import StaticFiles
import os
from server.config import MANAGEMENT_DIR

DOC_ASSETS_DIR = os.path.join(MANAGEMENT_DIR, 'docs', '_assets')
os.makedirs(DOC_ASSETS_DIR, exist_ok=True)
app.mount('/api/management/docs-assets', StaticFiles(directory=DOC_ASSETS_DIR, check_dir=False), name='doc-assets')
```

- 保持 `/api` 前缀：走既有 Vite 代理与 CORS，前端与生产反代都无需新规则
- `check_dir=False` + 启动时 `makedirs`：空仓库也能启动
- 与 `/api/management/docs/{slug:path}` 不冲突（字面段 `docs-assets` ≠ `docs`）；挂载顺序放在 include_router 之后也安全，因为路径首段不同

### D3: 正文用绝对 URL 引用

- 约定：`![图 1 · MaskGIT 整体架构](/api/management/docs-assets/maskgit-2022/fig-1.webp)`
- 理由：文档页面 URL 是 `/management/docs/notes/<slug>`，相对路径 `_assets/x.png` 会被解析成 `/management/docs/notes/_assets/x.png` → 404。绝对 `/api/...` 在任何层级都正确
- 备选：渲染时按 slug 重写相对路径 → 需 renderer 知道当前文档 slug 并改 MarkdownRenderer 接口，复杂度不值当

### D4: 渲染为 `<figure>`，覆写 image 规则（不加依赖）

在 `MarkdownRenderer.vue` 里覆写 markdown-it 的 `image` 渲染规则：

- 输出 `<figure><img src loading="lazy" alt><figcaption>{alt}</figcaption></figure>`（alt 为空时退化输出裸 `<img>`）
- `alt` 兼作图题 → 无额外语法（不引入 `图:` 之类的自定义标记）
- 保持 `html: false`（不放开原始 HTML，安全面不变）
- 影响面：全站 `![]()` 行为统一变化；现有文档无图片，属零破坏

### D5: 样式

`.markdown-body` 内新增：

```scss
figure { margin: 16px 0; text-align: center; }
figure img { max-width: 100%; height: auto; border-radius: 8px; border: 1px solid var(--color-border); }
figcaption { margin-top: 6px; font-size: 12px; color: var(--color-text-dim); line-height: 1.5; }
```

- 自适应容器宽度，窄屏自动缩放；图题小字灰，与正文区分

### D6: 资源规范（产出侧约束）

| 项 | 规范 | 理由 |
|---|---|---|
| 格式 | WebP（源为 PNG/JPG 时转） | 同画质体积约为 PNG 的 1/3–1/5 |
| 尺寸 | 最长边 ≤1600px | 正文渲染宽度通常 ≤1000px，2x 屏足够 |
| 质量 | 82 | 文字/曲线清晰度与体积的平衡点 |
| 单文件 | ≤500KB | 避免单图拖慢文档加载 |
| 单篇 | ≤5MB | 控制仓库与页面加载成本 |
| 命名 | `fig-<序号>-<简短语义>.webp` | 排序稳定、可读 |

- 违规时（如原图无法压缩）允许保留原格式，但须在 sidecar 或 change 中说明

### D7: 安全

- `StaticFiles` 只读挂载固定目录，路径穿越由 Starlette 自身防护（`follow_symlink=False` 默认）
- 不暴露目录列表（StaticFiles 默认行为：无 index 时不列目录）
- 不放开 markdown 原始 HTML，图片仅经 `![]()` 进入渲染

## Risks / Trade-offs

- [仓库体积随图片增长] → D6 规范约束单文件/单篇上限；后续可选加 `git-lfs` 或分离 assets 仓库（独立 change）
- [WebP 转换需要工具] → Pillow 可用则转；不可用则保留原格式（PNG/JPG 浏览器同样能显示），降级不影响功能
- [全站 image 规则变化可能影响未来引入的图片用法] → 语义化 figure 是通用良好实践；如需内联小图标（行内 img）可在 alt 为空时退化为裸 `<img>`（已按此设计）
- [静态目录与 API 同源，将来若加鉴权需一并覆盖] → 本库无鉴权；记录为后续注意点

## Migration Plan

后端改动需重启 uvicorn 生效；前端改动走 Vite HMR。回滚 = revert 提交（`_assets/` 中已放图片会保留但不再可访问，不影响其它功能）。

## Open Questions

（无）
