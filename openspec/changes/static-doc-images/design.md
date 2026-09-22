## Context

- 已有链：`build-docs-data.mjs` 扫描 `management/docs/` 产出 `web/public/docs-data.json`；`api/docs.js` 在 `PROD` 下 fetch 它。
- 图片约定（`doc-image-assets`）：源文件放 `management/docs/_assets/<slug>/`，正文用**绝对** `/api/management/docs-assets/<slug>/<file>` 引用；后端把它挂成静态目录。
- `article-note` 的 `figures.py publish` 会往 `_assets/` 写图并生成该绝对 URL；`validate-note.py` 会校验正文里的 URL 与磁盘文件对应。
- 上游当前 `management/docs/_assets/` 只有 `.gitkeep`（0 张图），但机制必须补上——否则第一篇带图笔记一上线就是裂图。
- 静态托管的部署基路径由 `import.meta.env.BASE_URL` 给出（当前 ProjFlow 未设 `base`，即 `/`；下游各自不同）。

## Goals / Non-Goals

**Goals:**

- 生产构建下正文图片可用，且 URL 随基路径正确解析。
- 源 Markdown 与本地上游开发路径**零改动**（`article-note` 的发布与校验继续成立）。
- 产物不含已删除的旧图。

**Non-Goals:**

- 不改 `doc-image-assets` 的存储约定与后端端点。
- 不改 `article-note` 的 `figures.py`。
- 不做图片压缩/格式转换（那是 `figures.py` 的职责，在发布前完成）。
- 不处理 `_assets` 之外的静态资源（如 `papers/` 图片）。

## Decisions

### D1: 构建期复制整树，目标先清空

`build-docs-data.mjs` 增加：

```js
rm -rf web/public/docs-assets          // 清空，避免源端已删的图残留
cp -R management/docs/_assets/. web/public/docs-assets/   // 不存在则跳过
```

- 理由：静态托管的产物是「本次构建的完整快照」，残留旧图会让已删除的图仍可访问（隐性问题）。
- 备选：只复制被正文引用的图 —— 需要先解析所有正文、且有 sidecar/appendix 等其它引用面，容易漏；整树复制更简单可靠。
- 备选：用 rsync `--delete` —— macOS/GitHub Actions 都有，但 Node 脚本内用 `fs` 更可移植，不引入外部命令。

### D2: 正文改写放在**读取静态数据时**，不改源 Markdown

`api/docs.js` 在返回静态详情前做一次 `content.replaceAll('/api/management/docs-assets/', `${import.meta.env.BASE_URL}docs-assets/`)`。

- 理由 1：源 Markdown 必须保持 `/api/management/docs-assets/...` —— `doc-image-assets` 的约定、`validate-note.py` 的校验、本地开发的后端端点都建立在它之上。改写源文件会同时打破这三者。
- 理由 2：基路径 `BASE_URL` 只有运行时才知道（构建产物可部署到任意子路径），放在运行时改写比自己解析 `vite.config.js` 更可靠。
- 备选：在生成脚本里把 base 拼进 `docs-data.json` —— 需要脚本反向解析 `vite.config.js`，且产物与部署路径耦合，不采用。
- 备选：让 `MarkdownRenderer` 统一改写 —— 会影响开发模式（把 API 路径也改掉），不采用。

### D3: `docs-data.json` 增加 `assetCount` 便于排错

生成时统计复制的资产文件数，写入顶层。不影响前端（只读 `docs`/`details`）。

## Risks / Trade-offs

- [整树复制让产物变大] → 资产本就应随笔记入库；`article-note` 已约束单图 ≤500KB、单篇 ≤5MB。
- [改写用 `replaceAll` 可能命中正文里「讨论该 URL 的代码示例」] → 影响仅是那处文本里的路径变成静态路径，语义仍正确；且开发模式不改写，不影响本地。
- [`BASE_URL` 为 `/` 时改写结果为 `/docs-assets/...`] → 正确（`import.meta.env.BASE_URL` 始终以 `/` 结尾）。
- [`_assets` 下非图片文件（如 `.gitkeep`）被一起复制] → 无害；`.gitkeep` 是空文件。
- [下游 `base` 与本地上游不同] → 改写在运行时取 `BASE_URL`，下游无需改脚本。

## Migration Plan

1. 改生成脚本（复制 + 计数）与 `api/docs.js`（改写），`.gitignore` 加 `web/public/docs-assets/`。
2. 验证：放一张测试图 + 一篇引用它的临时文档 → 构建 → 检查产物含图、`docs-data.json` 的 `assetCount`、生产预览下图片 200；dev 下仍指向 `/api/...`。验证后清理测试文件。
3. 回滚：revert 提交；生成物未入库。
