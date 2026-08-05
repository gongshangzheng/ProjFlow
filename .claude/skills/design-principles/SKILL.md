---
name: design-principles
description: |
  UI/UX 设计原则与公约。用于新建页面、列表页、结果展示等场景时遵循统一的设计规范。
  触发场景：(1) 创建新的列表/结果页，(2) 设计分页逻辑，(3) 选择组件布局方案，(4) review UI 改动，
  (5) 视频封面图/缩略图展示，(6) 结果画廊（如 Speed Run），(7) 数据集浏览/资产管理页面
---

# UI/UX 设计原则

本 skill 记录 ProjFlow 项目的设计公约，确保不同页面、不同开发者产出的 UI 风格一致。

**渐进式披露**：本文件只放核心规则（每条 1-3 行）。做具体设计时按需读 `references/` 分块文件，不要一次性全读。

| 主题 | 何时读 | 文件 |
|------|--------|------|
| 分页 | 设计列表/结果页、写分页 API | `references/pagination.md` |
| 视频封面图/缩略图 | 视频卡片、结果画廊、媒体网格 | `references/media-covers.md` |
| 数据集管理界面 | 数据集浏览、资产画廊、文件网格 | `references/dataset-page.md` |

`scripts/extract_covers.py` — 批量提取视频封面（cv2 中间帧，`--src 视频目录 --out 封面目录`，幂等）。

## 1. 列表/结果页必须分页

多项结果（论文、图片、视频、任务等）**必须分页**，不要一次渲染全部。客户端 slice vs 服务端分页的选型、API 契约、页型策略表、重字段剥离、轮询与缓存 → **`references/pagination.md`**。

例外：数据量固定 < 10 条；树形结构（天然折叠）。

## 2. 视频封面图

列表/卡片层不放 `<video>`，用封面图（cv2 中间帧 JPEG q80）+ 点击弹 VideoModal 播放。固定高 thumb 盒 + `object-fit: cover` + `loading="lazy"` + 图标 fallback → **`references/media-covers.md`**。

## 3. 数据集/资产页面

三层渐进披露：数据集卡片 → 目录浏览（面包屑 + 服务端分页）→ 预览 modal。布局尺寸、软链标记、多模态 tabs 扩展 → **`references/dataset-page.md`**。

## 4. 状态色统一

- 进行中/active → 绿 `#22c55e` · 待开始/planned → 蓝 `#3b82f6` · 已完成/completed → 灰 `#71717a` · 暂停/paused → 黄 `#eab308` · 阻塞/blocked → 红 `#ef4444`
- 状态用圆点（`.status-dot`）+ 文字标签，不用彩色大色块。
- 结果角标（正确/错误/未知）：`#22c55e` / `#ef4444` / `#71717a`，左上角 22px 圆形。

## 5. 空状态不报错

数据为空时用共享组件 `EmptyState.vue`（包装 `n-empty`），一句话说明"为什么空 + 怎么让它有数据"：

```vue
<EmptyState description="暂无数据集。将数据集目录（或软链）放入 datasets/ 即可显示。" />
```

## 6. 悬浮卡 vs 详情页

悬浮卡 = 轻量预览（3-5 个关键字段）；超过 5 个字段或需要滚动 → 做详情页。

## 7. 表单验证

必填字段 `*` 标注；错误提示贴输入框下方（toast 留给成功/系统级错误）；用 `n-form` + `rules`。

## 8. 响应式断点

桌面端优先（最小 1024px）。卡片网格用 `n-grid cols="3 600:2 900:3 1200:4" responsive="screen"` 或 CSS `repeat(auto-fill, minmax(Npx, 1fr))` 自适应。

## 9. 加载状态

< 500ms 不显示加载态（避免闪烁）；> 500ms 用骨架屏或"加载中…"；用 `v-if="loading"` 而非 disabled 按钮。

## 10. 错误处理

网络/500 → 全局 toast；业务错误 → 页面内错误卡片；不在控制台打印敏感信息。轮询 handler 用 `try {} catch {}` 包裹，瞬时失败不中断。

## 11. 加载性能

- 路由懒加载；`<img loading="lazy">`；骨架屏优先
- 搜索/筛选大数据走后端；巨量列表用虚拟滚动
- 缩略图 < 100KB/张，原图只在详情层；视频 `preload="none"`（详见 `references/media-covers.md`）
- 并发请求 `Promise.all`；列表页 `keep-alive` 缓存；搜索框 debounce 300ms
