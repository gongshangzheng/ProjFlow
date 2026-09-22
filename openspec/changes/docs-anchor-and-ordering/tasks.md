## 1. 后端：文档列表排序链

- [x] 1.1 `server/config.py` 新增 `DOCS_FOLDER_ORDER = []`（含「上游默认空，下游按需覆盖」注释）
- [x] 1.2 `server/routers/management.py` 从 config 导入 `DOCS_FOLDER_ORDER`
- [x] 1.3 新增 `_doc_number` / `_doc_date_ordinal` / `_doc_sort_key` 三个辅助函数
- [x] 1.4 `get_docs()` 输出新增 `order` 字段；末尾两趟 `sort` 改为 `docs.sort(key=_doc_sort_key)`
- [x] 1.5 确认保留 `_assets` 等下划线目录跳过逻辑（`add-doc-image-assets` 的改动不回退）

## 2. 前端：文内锚点接管

- [x] 2.1 `MarkdownRenderer.vue` 的 `handleClick`：`href` 空值早返回 + `#` 分支（`preventDefault` + `scrollIntoView({behavior:'smooth'})`）
- [x] 2.2 确认 `/management/` 路由跳转、`[[slug]]` 改写与图片渲染分支不受影响

## 3. 验证

- [x] 3.1 重启后端，`GET /api/management/docs` 连续请求返回顺序完全一致（消除文件系统序）
- [x] 3.2 造一篇带 `order` 的文档，确认 `order` 优先级高于 `id`；移除后回到 `id` 序
- [x] 3.3 浏览器验证：点文内锚点平滑滚动且 URL 不变；跨文档链接与右侧 TOC 行为不变
- [x] 3.4 `cd web && npm run build` 通过

## 4. 收尾

- [x] 4.1 `openspec validate docs-anchor-and-ordering` 通过
- [x] 4.2 以 `[shared]` 前缀提交，供下游 cherry-pick
