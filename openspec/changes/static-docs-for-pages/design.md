## Context

- `web/src/router/index.js` 用 `createWebHistory(import.meta.env.BASE_URL)`（history 模式）。
- 文档读取链：`DocPage.vue` → `api/management.js` 的 `getDocList()` / `getDocDetail(slug)` → axios → `/api/management/docs[/{slug}]`。
- 后端返回结构（`server/routers/management.py`）：
  - 列表项：`slug / title / author / date / tags / summary / id / order`
  - 详情项：上述 + `content`（去 frontmatter 的正文）+ `sidecar`
  - 排序（`_doc_sort_key`）：文件夹优先级（`server/config.py` 的 `DOCS_FOLDER_ORDER`）→ `order` → `id` → `date` 降序 → `slug` 字典序；`order`/`id` 缺失或非数字 → `inf`
  - 扫描时 `dirs[:] = [d for d in dirs if not d.startswith('_')]`，`_assets/` 不入列表
- `web/node_modules` 无 `yaml` / `js-yaml`。
- 下游 `pet-action-recognition` 已按同一思路落地（文档静态化 + `404.html`）并线上验证通过；本 change 是把它收归上游，使机制可被各下游复用。
- 本仓库**尚未启用 GitHub Pages**，也没有 `.github/workflows`。

## Goals / Non-Goals

**Goals:**

- 上游提供一套与后端**逐字段、逐顺序一致**的文档静态化机制，任何下游取走即可用。
- 本地开发行为零变化（仍走 FastAPI）。
- 深链接回退机制随构建自动产出。

**Non-Goals:**

- 不开启 Pages、不加 `.github/workflows/deploy.yml`、不改 `vite base`（见 D5）。
- 不处理文档图片（`_assets` → 静态托管）——需另开 change。
- 不静态化其它管理模块（团队/报告/项目树/会议/里程碑/评测），它们在静态托管上仍依赖后端。
- 不引入 `yaml` 依赖、不改后端。

## Decisions

### D1: 用 `import.meta.env.PROD` 切换来源，不新增环境变量

开发 → API；生产构建 → 静态数据。理由：部署侧无需注入任何 `VITE_*`；本地 `npm run build && npm run preview` 即可复现静态托管行为，便于验证。

- 备选：`VITE_DOCS_STATIC=1` 手工开关 —— 需要改 workflow 且易出现「构建了但忘开开关」的静默失效，不采用。

### D2: 生成到 `web/public/docs-data.json`，运行时 fetch（不 import 进 bundle）

- 理由 1：开发模式**完全不依赖生成物**，不跑 `prebuild` 也能 dev。
- 理由 2：文档正文体积可观，不进主 bundle；只在进入文档页时拉取。
- 代价：多一次请求（与原先调 API 等价）；必须经 `npm run build`（钩子）而非直接 `vite build`，否则产物缺文件 → 文档页空态（不白屏）。
- 备选：`import data from '../generated/docs-data.json'` —— 开发也依赖生成物、正文进 bundle，不采用。

### D3: 排序链在 JS 里逐级复刻 `_doc_sort_key`

```js
cmp(folderRank(a), folderRank(b))        // DOCS_FOLDER_ORDER 优先级（未列出的排最后）
  || cmp(num(a.order), num(b.order))     // 缺失/非数字 → Infinity
  || cmp(num(a.id), num(b.id))
  || cmp(dateOrd(b.date), dateOrd(a.date))  // 降序
  || cmp(a.slug, b.slug)                 // 字典序兜底
```

- `num`：数字或数字字符串 → Number；否则 `Infinity`。
- `dateOrd`：取前 10 字符按 ISO 解析为时间戳；非法/缺失 → `0`。
- 比较用显式 `cmp(a, b)`（`a === b ? 0 : a < b ? -1 : 1`），**不能**用 `a - b` 的真假判断 —— `Infinity - Infinity = NaN`，NaN 的真假会误判。

### D4: `DOCS_FOLDER_ORDER` 从 `server/config.py` 解析，不硬编码

上游该常量为空数组，下游会覆盖（如 digital-human 用 `['实习复盘','论文笔记','knowledge']`）。脚本用正则读取 `server/config.py` 里 `DOCS_FOLDER_ORDER = [...]` 的字面量；读不到则报错退出。

- 理由：排序必须与后端一致，硬编码会在下游改配置后静默漂移。
- 备选：把该常量搬到 JSON 供 Python 与 Node 共读 —— 需要改后端，收益不足，不采用。

### D5: 部署脚手架（Pages 开关、`base`、workflow）不在本 change

`vite base` 一旦改为 `/ProjFlow/`，本地开发 URL 会从 `localhost:3210/` 变成 `localhost:3210/ProjFlow/`，属于会影响日常使用的变更；且本仓库尚未启用 Pages，贸然加 `deploy.yml` 会让每次 push 触发一个必失败的 job（`configure-pages` 在未启用 Pages 时报错）。

- 因此本 change 只落**机制**；开启 Pages / 设 base / 加 workflow 由用户决策后另开 change。
- 下游（如 pet）已有自己的 `base` 与 `deploy.yml`，取走本机制即可直接生效。

### D6: 自写最小 frontmatter 解析子集，遇不支持写法显式失败

支持：单行 `key: value`、内联数组 `[a, b, c]`、数字字面量、去成对引号、`#` 注释行。遇到缩进（多行）或无法识别的行 → 打印 `文件:行号 + 原文` 并退出非零。

- 理由：为数篇 frontmatter 引入 `yaml` devDependency 收益低；显式失败保证「要么正确、要么报错」。
- 正文切法与后端一致：`content.indexOf('---', 3)` 之后 `.slice(end + 3).trim()`。

## Risks / Trade-offs

- [直接在 `vite build`（绕过 npm 钩子）导致产物无 `docs-data.json`] → 文档页空态 + 控制台报错，不白屏；构建说明强调用 `npm run build`。
- [frontmatter 出现多行/嵌套 YAML] → 脚本显式报错，构建失败而非发布错数据。
- [`DOCS_FOLDER_ORDER` 解析失败（下游改了 config 写法）] → 脚本报错退出；若下游确实改了结构，取机制时需同步调整。
- [静态托管上文内图片 404] → 已列为 Non-Goal，需另开 change（把 `_assets` 复制到 `public/` 并改写 URL）；当前上游文档 0 张图，暂无实际影响。
- [下游 `main.py`/`MarkdownRenderer.vue` 已分叉，取机制时冲突] → 本 change 不触碰这些文件，只新增独立文件 + 改 `DocPage.vue` 一行 import，冲突面极小。

## Migration Plan

1. 新增脚本与 `api/docs.js`，改 `DocPage.vue` 的 import，加 `package.json` 钩子，改 `.gitignore`。
2. 本地验证：`npm run build` 产物含 `docs-data.json` 与 `404.html`；静态数据与 `GET /api/management/docs` 顺序/字段一致；`npm run preview` 下文档页可读；dev 仍走后端。
3. 以 `[shared]` 提交并 push（下游可 `git checkout upstream/main -- web/scripts web/src/api/docs.js` 取用）。
4. 回滚：revert 提交；生成物未入库故无残留状态。
