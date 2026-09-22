# Tasks: add-doc-image-assets

## 1. 后端静态服务

- [x] 1.1 `server/main.py`：引入 `StaticFiles`，定义 `DOC_ASSETS_DIR = MANAGEMENT_DIR/docs/_assets`，启动时 `os.makedirs(exist_ok=True)`，挂载到 `/api/management/docs-assets`（`check_dir=False`）
- [x] 1.2 重启 uvicorn，验证：放一张测试 webp 到 `_assets/test/`，`curl -I /api/management/docs-assets/test/fig-1.webp` 返回 200 且 `content-type: image/webp`；不存在的文件返回 404；目录无 index 不列目录
- [x] 1.3 验证不与既有路由冲突：`GET /api/management/docs`、`GET /api/management/docs/git-workflow` 仍正常

## 2. 前端渲染

- [x] 2.1 `MarkdownRenderer.vue`：覆写 markdown-it `image` 规则——有 alt → `<figure><img src alt loading="lazy"><figcaption>{alt}</figcaption></figure>`；无 alt → 裸 `<img>`（保持 `html:false`）
- [x] 2.2 `web/src/styles/index.scss`：`.markdown-body` 下新增 `figure` / `figure img` / `figcaption` 样式（max-width 100%、居中、圆角边框、图题小字弱色）
- [x] 2.3 浏览器验证：临时文档中插入带图题图片与外链图片——图题显示、图片自适应、窄屏（≤700px）不横向溢出；无 alt 图片不产生空图题

## 3. 约定文档化

- [x] 3.1 更新 `.agents/skills/documentation/SKILL.md` §2：新增「图片与图题」小节——存放位置 `management/docs/_assets/<slug>/`、绝对 URL 引用格式、`![图 N · 说明](url)` 图题约定、资源规范（WebP / ≤1600px / ≤500KB）、不可用本地图床

## 4. 验证与提交

- [x] 4.1 回归：既有两篇无图文档（api-design-conventions、git-workflow）渲染与 TOC 正常；文档列表不含 `_assets` 内文件
- [x] 4.2 清理测试图片（`_assets/test/`），确认 `_assets/` 可空目录入库（加 `.gitkeep` 或保留结构说明）
- [x] 4.3 提交：`[shared] feat: wiki 文档图片支持（_assets 静态端点 + figure 渲染 + 图题样式）`
