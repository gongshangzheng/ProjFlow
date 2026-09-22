# static-docs-for-pages

## Why

前端部署到静态托管（GitHub Pages 等）时**没有 FastAPI 后端**，`DocPage.vue` 调 `/api/management/docs` 必然失败，文档页只能显示空态。同时 history 路由在纯静态托管下，直接访问/刷新深链接会被平台判 404（磁盘上没有该路径）。

本仓库的 `web/` 是**共享脚手架**（下游 `pet-action-recognition` 已按同一思路落地并验证），因此机制应落在上游：上游定义一次，下游 `git checkout upstream/main -- <path>` 即可获得，避免各库各写一份。

## What Changes

**1. 文档静态化（机制）**

- 新增 `web/scripts/build-docs-data.mjs`：扫描 `management/docs/` 下的 `.md` 与同名 sidecar `.json`，产出 `web/public/docs-data.json`；字段与排序**逐项复刻后端** `GET /api/management/docs`、`GET /api/management/docs/{slug}`，含上游特有的排序链（文件夹优先级 → `order` → `id` → `date` 降序 → `slug`）与 `_` 前缀目录跳过。
- 新增 `web/src/api/docs.js`：文档取数的**来源切换层** —— 开发（`import.meta.env.DEV`）走 FastAPI，生产构建读静态数据。
- `web/src/views/management/DocPage.vue`：改从 `api/docs` 导入（一行）。
- `web/package.json`：增加 `prebuild` / `postbuild` 钩子。
- `.gitignore`：忽略生成物 `web/public/docs-data.json`。

**2. 深链接回退（机制）**

- 新增 `web/scripts/copy-404.mjs`：把 `web/dist/index.html` 复制为 `web/dist/404.html`，由 `postbuild` 钩子驱动。

## Capabilities

### New Capabilities

- `docs-static-build`: 文档在构建期静态化、开发/生产的数据来源切换，以及 SPA 深链接的静态托管回退。

### Modified Capabilities

（无）

## Impact

- 前端：新增 `web/scripts/build-docs-data.mjs`、`web/scripts/copy-404.mjs`、`web/src/api/docs.js`；修改 `web/src/views/management/DocPage.vue`、`web/package.json`；`.gitignore` 增一行。
- 后端：**不动**（继续提供本地开发的实时文档接口）。
- 下游：可用 `git checkout upstream/main -- web/scripts web/src/api/docs.js` 取机制，再按各自 base/工作流适配。
- 行为变化：生产构建的文档页数据来自静态 JSON；开发模式行为不变。
- **不在本 change 范围**：开启 Pages、设置 `vite base`、新增 `.github/workflows/deploy.yml` —— 本仓库尚未启用 Pages，且 `base` 会改变本地开发 URL（`localhost:3210/` → `localhost:3210/ProjFlow/`），需单独决策。
- 已知边界：静态托管上文档里的图片引用（`/api/management/docs-assets/...`）不会存在，需另开 change 处理；当前文档 0 张图。
