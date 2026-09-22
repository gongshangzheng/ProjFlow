## 1. 静态数据生成脚本（上游排序链版）

- [x] 1.1 新增 `web/scripts/build-docs-data.mjs`：定位仓库根，校验 `management/docs/` 存在且含 ≥1 篇 `.md`，否则非零退出
- [x] 1.2 从 `server/config.py` 解析 `DOCS_FOLDER_ORDER`（正则读字面量；读不到则报错退出）
- [x] 1.3 扫描时跳过 `_` 前缀目录（与后端 `dirs[:] = [d for d in dirs if not d.startswith('_')]` 一致）
- [x] 1.4 最小 frontmatter 解析（单行 `key: value`、内联数组、数字、去引号、`#` 注释）；不支持的行打印 `文件:行号` 并退出
- [x] 1.5 生成列表项（`slug/title/author/date/tags/summary/id/order`）与详情项（+ `content`/`sidecar`）
- [x] 1.6 复刻 `_doc_sort_key`：文件夹优先级 → `order` → `id` → `date` 降序 → `slug`；用显式 `cmp` 避免 `Infinity - Infinity = NaN` 误判
- [x] 1.7 写出 `web/public/docs-data.json`（含 `generatedAt`/`docs`/`details`），打印条数与路径

## 2. 前端来源切换层

- [x] 2.1 新增 `web/src/api/docs.js`：`getDocList()` / `getDocDetail(slug)`；`import.meta.env.PROD` 时 fetch `${import.meta.env.BASE_URL}docs-data.json`，否则调 `api/management.js`
- [x] 2.2 静态分支：只拉一次并缓存；slug 不存在时抛错（与后端 404 一致）
- [x] 2.3 `DocPage.vue`：import 由 `api/management` 改为 `api/docs`（其余逻辑不动）

## 3. 深链接回退

- [x] 3.1 新增 `web/scripts/copy-404.mjs`：`dist/index.html` → `dist/404.html`（缺 index.html 时报错退出）
- [x] 3.2 `web/package.json`：加 `prebuild`（生成数据）与 `postbuild`（复制 404）钩子
- [x] 3.3 `.gitignore`：忽略 `web/public/docs-data.json`

## 4. 验证

- [x] 4.1 `npm run build` 成功，产物含 `web/dist/docs-data.json` 与 `web/dist/404.html`（后者与 `index.html` 逐字节一致）
- [x] 4.2 静态数据与后端 `GET /api/management/docs` 的**顺序与全部字段**一致（含 `order`），`_assets` 未混入
- [x] 4.3 `npm run preview` 下文档页可见列表 + 正文 + sidecar 区块，深链接直接打开可渲染
- [x] 4.4 开发模式（`npm run dev`）文档页仍走后端 API
- [x] 4.5 负向：frontmatter 多行写法 / `management/docs` 缺失 → 均非零退出且信息可定位
- [x] 4.6 `openspec validate static-docs-for-pages` 通过

## 5. 收尾

- [x] 5.1 以 `[shared]` 前缀提交并 push（供下游取用）
- [x] 5.2 说明「开启 Pages / base / workflow」与「文档图片静态化」为后续 change
