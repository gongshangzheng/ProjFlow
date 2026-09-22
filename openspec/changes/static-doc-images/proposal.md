# static-doc-images

## Why

文档静态化（`docs-static-build`）让正文在静态托管上能读，但**图片仍会 404**：正文按约定写的是绝对路径 `/api/management/docs-assets/<slug>/<file>`，而静态托管上没有后端，该端点不存在。

上游已有两条依赖图片的能力：

- `doc-image-assets`：约定图片放 `management/docs/_assets/<slug>/`，用 `/api/management/docs-assets/...` 引用；
- `article-note`：`figures.py publish` 把插图发布到 `_assets/`，并写入该绝对 URL。

也就是说，只要用 `article-note` 写过一篇带图的笔记，它在静态托管上就会满屏裂图。本 change 把这条链补完。

## What Changes

- `web/scripts/build-docs-data.mjs`：构建期把 `management/docs/_assets/` 整树复制到 `web/public/docs-assets/`（复制前清空目标，避免已删除的图残留）。
- `web/src/api/docs.js`：在生产构建读取静态数据时，把正文里的 `/api/management/docs-assets/` 前缀改写为 `${import.meta.env.BASE_URL}docs-assets/`，使 URL 随部署基路径正确解析。
- `.gitignore`：忽略生成物 `web/public/docs-assets/`。
- 生成物 `docs-data.json` 记录 `assetCount`，便于排错。

关键约束：**源 Markdown 不改写** —— 它必须继续用 `/api/management/docs-assets/...`（`doc-image-assets` 的约定），改写只发生在读取静态数据时。这样 `article-note` 的 `validate-note.py`（校验该绝对 URL）与后端本地开发路径都不受影响。

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

- `docs-static-build`: 新增「文档图片随构建静态化并在正文中正确解析」的要求。

## Impact

- 前端：`web/scripts/build-docs-data.mjs`、`web/src/api/docs.js`、`.gitignore`。
- 后端：**不动**。
- 行为变化：生产构建的正文图片改从 `/<base>/docs-assets/...` 加载；开发模式仍走 `/api/management/docs-assets/...`。
- 不影响：`doc-image-assets` 的存储约定与端点、`article-note` 的 `figures.py publish` 与 `validate-note.py`、源 Markdown 内容。
- 归属：共享脚手架层 → 提交加 `[shared]` 前缀。
