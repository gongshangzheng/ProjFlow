# Proposal: add-doc-image-assets（wiki 文档图片支持）

## Why

本库 wiki（`management/docs/`）当前**无法显示任何图片**：`server/main.py` 没有挂载任何静态资源目录，Markdown 里写本地图片路径必然 404；`MarkdownRenderer` 也无图相关样式与语义包装。这挡住了所有需要配图的文档形态——尤其论文精读笔记（架构图、实验结果曲线是核心内容）、架构文档（模块图、时序图）。本 change 补上"存图 + 供图 + 渲染成 figure"的基础设施，让 wiki 文档可安全引用图片。

## What Changes

- **存储约定**：文档图片存 `management/docs/_assets/<slug>/<name>.webp`（下划线前缀表明"非文档"；文档列表只扫 `*.md`，不受影响）
- **静态服务**：`server/main.py` 挂载 `StaticFiles(directory=management/docs/_assets)` 到 `/api/management/docs-assets`；启动时若目录不存在则创建（`check_dir=False` 避免启动报错）；Vite 已把 `/api` 代理到后端，前端无需额外配置
- **引用约定**：正文使用**绝对 URL** `/api/management/docs-assets/<slug>/<file>`（相对路径在 SPA 下会基于 `/management/docs/<slug>` 解析，必然错）
- **渲染**：`MarkdownRenderer.vue` 覆写 markdown-it 的 image 规则，把 `![图题](src)` 渲染为语义化 `<figure><img loading="lazy"><figcaption>图题</figcaption></figure>`（不引入新依赖；alt 兼作图题）
- **样式**：`.markdown-body` 增加 `figure` / `img` / `figcaption` 规则（自适应宽度、居中、圆角、图题小字灰）
- **资源规范**：WebP、最长边 ≤1600px、质量 82、单文件 ≤500KB、单篇 ≤5MB；图片属内容，随笔记入库

## Capabilities

### New Capabilities
- `doc-image-assets`: wiki 文档图片的存储约定、静态服务端点、markdown 引用与 figure 渲染规范

### Modified Capabilities

（无——`documentation` 的文档规范不因此变更需求，本 change 只新增图片能力）

## Impact

- 修改：`server/main.py`（挂载静态目录）、`web/src/components/common/MarkdownRenderer.vue`（image 规则 + 样式）、`web/src/styles/index.scss`（figure/img 样式）
- 新增：`management/docs/_assets/`（目录约定，初始为空）
- 不影响：既有文档（原本无图）、`GET /api/management/docs`（只扫 `*.md`）、其它路由与页面
- 依赖方向：`add-article-note-skill`（论文精读笔记落图）依赖本 change
- 归属：`server/`、`web/src/` 属共享脚手架层 → 实施提交加 `[shared]` 前缀
