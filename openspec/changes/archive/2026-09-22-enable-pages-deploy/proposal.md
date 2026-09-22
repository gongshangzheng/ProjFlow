# enable-pages-deploy

## Why

前面两个 change 已让静态托管可用：`docs-static-build`（文档静态化 + `404.html`）与 `static-doc-images`（正文配图静态化）。但本仓库**还没有部署通道** —— 没有 `.github/workflows`，也没启用 Pages，也没有为子路径部署设置 `base`。下游 `pet-action-recognition` 已用同一套模式跑通线上（<https://gongshangzheng.github.io/pet-action-recognition/>）。

本 change 把「部署通道」这条上游缺的短板补上，使上游自身可发布，也让后续新下游有可照抄的基线。

## What Changes

- 新增 `.github/workflows/deploy.yml`：push `main`（或手动触发）时在 `web/` 下 `npm install` + `npm run build`，把 `web/dist` 发布到 GitHub Pages。
- `web/vite.config.js`：base 改为**条件式** —— 构建时 `/<仓库名>/`（Pages 子路径），开发时 `/`（**不改变本地开发 URL**）。
- 启用仓库 Pages（`build_type: workflow`）。
- `AGENTS.md` / `README.md`：补充 Pages 部署说明、线上地址，以及「开发 URL 不变、构建才走子路径」的说明。

## Capabilities

### New Capabilities

- `pages-deploy`: 仓库的 GitHub Pages 部署通道（触发条件、构建步骤、基路径处理与产物要求）。

### Modified Capabilities

（无）

## Impact

- 基础设施：新增 `.github/workflows/deploy.yml`；`web/vite.config.js` 的 `base`。
- 仓库设置：启用 Pages（`build_type: workflow`）。
- 文档：`AGENTS.md`、`README.md`。
- 行为变化：push `main` 后自动构建并发布到 `https://gongshangzheng.github.io/ProjFlow/`；本地开发 URL 保持 `http://localhost:3210/` 不变。
- 依赖：`docs-static-build` 与 `static-doc-images` 提供的静态数据 / 资产 / `404.html` 是部署产物的一部分。
- 已知边界：Pages 上**只有文档页可用**；依赖后端的页面（论文列表/评测/项目树等）会显示空态。原因同 `static-docs-for-pages`：无后端、无数据库。
