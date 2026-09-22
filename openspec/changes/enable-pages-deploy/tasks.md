## 1. 构建基路径

- [x] 1.1 `web/vite.config.js`：改为 `defineConfig(({ command }) => ({ base: command === 'build' ? '/ProjFlow/' : '/', ... }))`，并写明理由注释
- [x] 1.2 确认 `server.port` 与 `/api` 代理保持原样（不被本次改动带偏）
- [x] 1.3 `web/src/router/index.js`：`createWebHistory()` → `createWebHistory(import.meta.env.BASE_URL)`（否则子路径下路由全不匹配、白屏）
- [x] 1.4 `vite.config.js` 的 base 判断须包含 `isPreview`（preview 的 command 也是 serve），否则本地预览资源 404

## 2. 部署工作流

- [x] 2.1 新增 `.github/workflows/deploy.yml`：push main + workflow_dispatch；concurrency group `pages`；permissions `contents:read` / `pages:write` / `id-token:write`
- [x] 2.2 build job：checkout → setup-node 22 → `working-directory: web` 下 `npm install --no-audit --no-fund` + `npm run build` → `configure-pages@v5` → `upload-pages-artifact@v3`（`path: web/dist`）
- [x] 2.3 deploy job：`needs: build`、environment `github-pages`、`deploy-pages@v4`
- [x] 2.4 不在 workflow 里手工 `cp` 404.html（由 postbuild 钩子负责）

## 3. 启用 Pages 与文档同步

- [x] 3.1 启用仓库 Pages，部署源设为 GitHub Actions（`build_type: workflow`）；失败则暂停本 change 并回报
- [x] 3.2 `AGENTS.md`：补充线上地址、条件 base 说明、Pages 上仅文档页可用的边界
- [x] 3.3 `README.md`：补充线上地址与部署说明

## 4. 验证

- [x] 4.1 `npm run dev` 下 `http://localhost:3210/` 直接可用（不需要 `/ProjFlow/` 前缀）
- [x] 4.2 `npm run build` 产物中 `index.html` 的资源引用前缀为 `/ProjFlow/`
- [x] 4.3 `npm run preview` 下 `/ProjFlow/` 可打开首页与 `/ProjFlow/management/docs/<slug>` 深链接
- [x] 4.4 push 后首次工作流成功（`conclusion: success`）
- [x] 4.5 线上 `https://gongshangzheng.github.io/ProjFlow/` 首页 200；`/management/docs/<slug>` 深链接由 SPA 渲染；`/ProjFlow/docs-data.json` 200
- [x] 4.6 `openspec validate enable-pages-deploy` 通过

## 5. 收尾

- [x] 5.1 提交（`[shared]` 前缀；workflow 属共享脚手架）
