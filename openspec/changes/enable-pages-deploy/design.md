## Context

- 现状：ProjFlow **无** `.github/workflows`、**未启用** Pages、`web/vite.config.js` 未设 `base`（即 `/`）。
- 下游 `pet-action-recognition` 已跑通：`.github/workflows/deploy.yml`（`configure-pages` + `upload-pages-artifact` + `deploy-pages`）、`base: '/pet-action-recognition/'`、线上 <https://gongshangzheng.github.io/pet-action-recognition/>。
- `web/src/api/request.js` 用绝对 `baseURL: '/api'`，**不受 `base` 影响**（代理与后端调用不受本 change 干扰）。
- `web/src/router/index.js` 原本是 **`createWebHistory()` 无参**（base 锁死 `/`）—— 一旦以子路径部署，路由路径会带上 `/ProjFlow/` 前缀而全部匹配失败、页面白屏。本 change 必须一并把它改为 `createWebHistory(import.meta.env.BASE_URL)`。
- 前置能力已就绪：`build-docs-data.mjs`（含资产复制）、`copy-404.mjs`、`api/docs.js` 的来源切换。

## Goals / Non-Goals

**Goals:**

- push `main` 即自动发布到 Pages。
- **不改变本地开发 URL**（`http://localhost:3210/` 仍是 `http://localhost:3210/`）。
- 线上文档页、深链接、正文配图三者在无后端下都可用。

**Non-Goals:**

- 不做后端部署（Pages 只有静态文件），不做无后端页面的降级改造。
- 不静态化论文/评测/项目树等模块（另议）。
- 不改端口分配（8809/3210）与 `start_services.sh`。
- 不为下游强制统一 base 写法（下游可继续用常设 base）。

## Decisions

### D1: `base` 条件式 —— 构建 `/<仓库名>/`，开发 `/`

```js
export default defineConfig(({ command }) => ({
  // 构建产物部署在 Pages 子路径下；开发仍用根路径，避免日常访问地址被改成 /ProjFlow/
  base: command === 'build' ? '/ProjFlow/' : '/',
  ...
}))
```

- 理由 1：常设 `base: '/ProjFlow/'` 会把开发地址变成 `http://localhost:3210/ProjFlow/`，属对日常使用的破坏性变更，且需要改 `start_services.sh` 注释、README、AGENTS、以及用户书签。
- 理由 2：`request.js` 用绝对 `/api`，与 base 无关；`router` 用 `BASE_URL`，条件式 base 下两种场景各自正确。
- 备选：常设 `base`（与 pet 一致，配置更"直白"）—— 代价是改变开发地址，不采用。
- 备选：`vite build --base=/ProjFlow/`（只在 workflow 里传）—— 本地 `npm run build` 会产出 base `/` 的站点，导致「本地构建能看、线上错位」，不采用。

### D1b: `vite preview` 也必须算作「子路径」场景

`vite preview` 的 `command` 同样是 `'serve'`。若只判断 `command === 'build'`，preview 会以 `/` 为基路径，而产物引用的是 `/ProjFlow/assets/...` → 资源全部 404、页面白屏（本地无法自测线上形态）。

- 因此判断条件为 `command === 'build' || isPreview`（Vite 的 `ConfigEnv.isPreview`）。
- 实测教训：修之前 `GET /ProjFlow/assets/index-*.js` 返回 `404 text/html`。

### D2: 工作流照抄 pet 的成熟结构，只改 `working-directory`

`actions/checkout@v4` → `setup-node@v4`（node 22）→ 在 `web/` 下 `npm install --no-audit --no-fund` + `npm run build` → `configure-pages@v5` → `upload-pages-artifact@v3`（`path: web/dist`）→ `deploy-pages@v4`；`permissions: pages/id-token/contents`；`concurrency: group pages`。

- 理由：该结构已在下游验证可用；上游直接复用可避免踩坑。
- 注意：**不要**在 workflow 里另外 `cp` 出 `404.html` —— 已由 `postbuild` 钩子自动完成（`npm run build` 触发）。

### D3: 由本 change 启用 Pages（`build_type: workflow`）

`configure-pages` 在 Pages 未启用时会失败，导致每次 push 红叉。因此在实施阶段直接启用 Pages（部署源为 GitHub Actions），让工作流第一次运行即成功。

- 备选：让用户去网页设置里开 —— 多一步人工操作且首跑会失败，不采用。
- 若启用失败（权限/组织策略），则本 change 暂停并交回用户，不留下一个必失败的 workflow。

### D4: 文档同步更新

`AGENTS.md` / `README.md` 增补：线上地址、`base` 的处理方式（开发不受影响）、以及「Pages 上仅文档页可用」的边界。

## Risks / Trade-offs

- [首次部署后非文档页在线上空白] → 已在 proposal 声明边界；属无后端场景的预期，不是缺陷。
- [条件式 base 让「开发/构建」行为不同，后来者可能困惑] → 在 `vite.config.js` 处写明注释，并在 AGENTS.md 记录理由。
- [子路径写死仓库名，仓库改名后失效] → 与 pet 同款处理；仓库改名属罕见事件，届时同步改一处即可。
- [`concurrency.cancel-in-progress` 取消正在进行中的部署] → 期望行为，避免旧提交覆盖新提交。
- [Pages 缓存旧产物] → 每次部署整站替换；如遇缓存，`404.html` 与 `index.html` 同源一致故无差异表现。

## Migration Plan

1. 改 `vite.config.js`（条件 base），新增 `.github/workflows/deploy.yml`，更新 AGENTS.md / README.md。
2. 本地验证：`npm run dev` 仍为 `http://localhost:3210/`；`npm run build` 产物资源前缀为 `/ProjFlow/`；`npm run preview` 在 `/ProjFlow/` 下能打开文档页与深链接。
3. 启用 Pages → 提交并 push → 观察首次工作流成功 → 打开线上地址验证文档页/深链接/配图。
4. 回滚：删除 workflow 并还原 base；Pages 可在仓库设置里关闭。
