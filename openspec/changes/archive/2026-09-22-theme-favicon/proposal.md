# theme-favicon

## Why

站点图标（浏览器标签页 favicon）目前是 `web/public/favicon.svg` —— 随初始脚手架一起进来的一个**紫色生成器产物**（`#863bff` / `#7e14ff`，48×46，1 条路径 + 15 个 `filter` + 15 个 `ellipse` 做玻璃质感）。

问题是它和刚建立的主题色体系**完全脱节**：

- 它永远是紫色，无论用户把强调色切成枪灰、青色还是玫红；
- 明暗模式切换也不影响它；
- 用户无法更换图标形状。

浏览器标签页图标无法读取 CSS 变量，因此需要由 JS 生成 SVG 并写入 `<link rel="icon">`。

## What Changes

- 新增 `web/src/config/favicon.js`：6 个自绘的简单图标形状（闪电 / 脉冲 / 网格 / 层级 / 六边形 / 星芒），以及 `faviconSvg(key, bg)` —— 圆角方块底色 = 当前强调色，前景按底色亮度自动取深/浅以保证对比。
- `web/src/stores/theme.js`：新增 `favicon` 状态与 `setFavicon()`；`applyFavicon()` 在 accent / mode 变化时重新生成并写入 `<link rel="icon">` 的 data URL；持久化到 `projflow-favicon`。
- `web/src/layouts/MainLayout.vue`：顶栏调色盘弹层扩展为「主题」面板，含 **主题色**（原 9 色色块）与 **图标**（6 个图标预览）两节。
- `web/public/favicon.svg`：重写为默认图标（闪电）× 默认强调色（枪灰）的静态兜底，替换掉过时的紫色版本。

## Capabilities

### New Capabilities

- `theme-favicon`: 站点图标（favicon）的形状集合、跟随强调色/明暗模式、选择持久化与无 JS 兜底。

### Modified Capabilities

（无）

## Impact

- 前端：新增 `web/src/config/favicon.js`；修改 `web/src/stores/theme.js`、`web/src/layouts/MainLayout.vue`；重写 `web/public/favicon.svg`。
- 行为变化：标签页图标随强调色与明暗模式变化；用户可从 6 个形状中选择并跨会话保留；初始紫色图标被替换。
- 不影响：`index.html` 的 `<link rel="icon">`（仍指向 `/favicon.svg` 作为无 JS 兜底，JS 生效后改写为 data URL）、`projflow-theme` / `projflow-accent` 存储键、主题色体系。
- 归属：共享脚手架层 → 提交加 `[shared]` 前缀。
