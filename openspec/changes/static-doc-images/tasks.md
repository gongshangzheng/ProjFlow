## 1. 构建期复制资产

- [x] 1.1 `web/scripts/build-docs-data.mjs`：新增 `syncAssets()` —— 目标 `web/public/docs-assets/` 先清空（`fs.rmSync(..., {recursive:true, force:true})`），再把 `management/docs/_assets/` 整树复制过去
- [x] 1.2 `management/docs/_assets/` 不存在时跳过且不报错
- [x] 1.3 统计复制的文件数，写入 `docs-data.json` 顶层 `assetCount`
- [x] 1.4 构建日志打印资产数量

## 2. 正文 URL 改写（仅静态分支）

- [x] 2.1 `web/src/api/docs.js`：`getDocDetail()` 静态分支返回前，把 `content` 里的 `/api/management/docs-assets/` 替换为 `${import.meta.env.BASE_URL}docs-assets/`
- [x] 2.2 开发分支（走 API）与源 Markdown 均不改写

## 3. 忽略生成物

- [x] 3.1 `.gitignore` 增加 `web/public/docs-assets/`

## 4. 验证

- [x] 4.1 造测试数据：`management/docs/_assets/__probe/fig-1.webp`（1×1 png 改名或最小 webp）+ 引用它的临时文档 `__probe.md`
- [x] 4.2 `npm run build` 后产物含 `dist/docs-assets/__probe/fig-1.webp`，`docs-data.json` 的 `assetCount` ≥ 1
- [x] 4.3 `npm run preview` 下打开该文档，图片请求返回 200 且来自 `/docs-assets/...`
- [x] 4.4 开发模式（3210）下同一文档的图片请求指向 `/api/management/docs-assets/...`
- [x] 4.5 删除测试图后再次构建，产物中不再包含该图（清空逻辑生效）
- [x] 4.6 源 Markdown 未被改写：`grep -c "/api/management/docs-assets/" management/docs/__probe.md` 仍为 1
- [x] 4.7 `npm run build` 与 `openspec validate static-doc-images` 通过
- [x] 4.8 清理全部测试文件并复核工作区干净

## 5. 收尾

- [x] 5.1 以 `[shared]` 前缀提交
