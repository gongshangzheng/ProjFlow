## 1. 图标形状与生成

- [x] 1.1 新增 `web/src/config/favicon.js`：`DEFAULT_FAVICON = 'bolt'` + `FAVICONS`（6 个形状：bolt / flow / grid / layers / hex / spark，各带中文 label）
- [x] 1.2 同文件：`faviconSvg(key, bgColor)` —— 32×32 圆角方块（底色 `bgColor`）+ 前景（`readableOn(bgColor)`）形状
- [x] 1.3 同文件：`faviconDataUrl(key, bgColor)` = `data:image/svg+xml,` + `encodeURIComponent(...)`

## 2. 状态与注入

- [x] 2.1 `stores/theme.js`：新增 `favicon` 状态（读 `projflow-favicon`，`FAVICONS.some()` 校验，缺失/未知回落 `DEFAULT_FAVICON`）
- [x] 2.2 `stores/theme.js`：`applyFavicon(key, accent, mode)` —— 找到或创建 `<link rel="icon">`，写入 data URL
- [x] 2.3 `stores/theme.js`：`init()` / `toggle()` / `setAccent()` 后调用 `applyFavicon()`；新增 `setFavicon(key)`（写 state + localStorage + apply）
- [x] 2.4 `MainLayout.vue`：计算当前强调色主色（供图标预览用），弹层扩展为「主题色」+「图标」两节

## 3. 静态兜底

- [x] 3.1 重写 `web/public/favicon.svg`：`bolt` 形状 + 枪灰 `#4a4f57` 底 + 白色前景（与 `faviconSvg('bolt','#4a4f57')` 一致）

## 4. 验证

- [x] 4.1 切换强调色：`<link rel="icon">` 的 data URL 内容随底色变化
- [x] 4.2 切换明暗模式：底色取对应模式色值，前景对比仍清晰
- [x] 4.3 面板显示 6 个图标预览，当前项有选中标记；选择后立即生效
- [x] 4.4 刷新后图标形状保持；写入未知 key 后回落 `bolt`
- [x] 4.5 禁用 JS / 清空 `<link>` 时 `/favicon.svg` 返回枪灰闪电（与默认一致）
- [x] 4.6 `npm run build` 通过

## 5. 收尾

- [x] 5.1 `openspec validate theme-favicon` 通过
- [x] 5.2 以 `[shared]` 前缀提交
