## Context

- `web/index.html:5` 是 `<link rel="icon" type="image/svg+xml" href="/favicon.svg" />`，即静态文件 `web/public/favicon.svg`（`159e4aa` 初始化时带入的紫色生成器产物）。
- 浏览器标签页图标**无法读取 CSS 变量**，所以「跟随主题」必须由 JS 生成 SVG 并替换 `<link>` 的 href。
- 现有可复用件：`config/theme.js` 的 `ACCENTS` / `accentFor()` / `readableOn()`；`stores/theme.js` 已有 accent + mode 的应用链（`init` / `toggle` / `setAccent`）。

## Goals / Non-Goals

**Goals:**

- 图标形状可选（≥4 个），且**自动**跟随当前强调色与明暗模式。
- 无 JS 时有一致的静态兜底，不再残留紫色。

**Non-Goals:**

- 不做自定义上传图标 / 自定义底色 / 图形编辑器。
- 不改 `index.html` 的 `<link>` 结构（仍以 `/favicon.svg` 为初始兜底）。
- 不清理 `web/public/icons.svg`（未被引用的社交图标 sprite，与本 change 无关）。
- 不改 `PaperList.vue` / `Home.vue` 里仍未跟随强调色的硬编码 `#4f46e5`（另一件事，可用单独 change 处理）。

## Decisions

### D1: 图标 = 「强调色圆角方块 + 白色/深色前景形状」

不用「透明底 + 彩色形状」，因为深色强调色（枪灰 `#4a4f57`）在深色标签栏上几乎不可见。改成 app-icon 式底块后，任何标签栏背景都能看清，且底色直接表达主题色。

- 视角：32×32，圆角 7。
- 前景色由 `readableOn(bg)` 决定（深底→白，浅底→深灰 `#1f2937`），保证枪灰深色模式值 `#a8aeb6` 这类「亮底」也有对比。
- 备选：形状本身取强调色、透明底 —— 深底部不可见，不采用。

### D2: 形状用 JS 字符串模板，不用独立 .svg 文件

`config/favicon.js` 里每个形状是一个 `(color) => string` 的模板函数，`faviconSvg(key, bg)` 拼成完整 SVG。

- 理由：需要把当前强调色注入到 SVG 里，独立文件做不到；字符串模板同时服务于「预览」（`v-html`）与「真图标」（data URL），保证预览即所得。
- 6 个形状：`bolt` 闪电、`flow` 脉冲、`grid` 网格、`layers` 层级、`hex` 六边形、`spark` 星芒 —— 全部为几何路径，16px 下仍可辨识。

### D3: 真图标走 data URL，预览走内联 SVG

```js
link.href = 'data:image/svg+xml,' + encodeURIComponent(faviconSvg(key, bg))
```

- 理由：data URL 无需新增静态路由/后端；`encodeURIComponent` 保证 `#` 等字符不破坏 URL。
- 预览直接 `v-html="faviconSvg(...)"`：内容由本地模板生成、无用户输入，无 XSS 面。

### D4: 存储键 `projflow-favicon`，与 theme/accent 并列，三者在同一 store 内联动

`applyFavicon(key, accent, mode)` 在 `init()` / `toggle()` / `setAccent()` / `setFavicon()` 后调用；读取时用 `FAVICONS.some()` 校验，未知值回落 `DEFAULT_FAVICON = 'bolt'`。

- 理由：图标依赖 accent + mode 两个状态，放在同一 store 才能保证任一变化都触发重算，不会出现「改了主题色但图标没变」。

### D5: 静态兜底 = 默认形状 + 默认强调色，由 JS 覆盖

`web/public/favicon.svg` 重写为 `bolt` + 枪灰 `#4a4f57` + 白色前景（与 `faviconSvg('bolt', '#4a4f57')` 输出一致）。

- 理由：`index.html` 的 `<link>` 在 JS 执行前就已加载，兜底必须与默认值一致，否则首屏闪一个不一致的图标。
- 用 `<img src="/favicon.svg">` 无法验证「数据一致」——验证时用字符串比对。

## Risks / Trade-offs

- [data URL favicon 在部分旧浏览器不生效] → 目标环境为现代浏览器；且 `index.html` 始终保留静态 SVG 兜底，最坏情况退化为静态图标。
- [图标底色用「当前模式」的强调色，可能与品牌预期不符（深色模式下图标变亮）] → 这是「跟随主题」的显式要求；如只想跟 accent 不跟 mode，改 `applyFavicon` 传 `false` 一处即可。
- [形状在 16px 标签页下糊成一团] → 全部使用粗线条/大色块几何形状，避免细线；验证时按 16/32 两档目视。
- [重写 `public/favicon.svg` 后，旧用户缓存仍显示紫色] → 文件名未变可能命中缓存；如出现，可在验证后给 href 加版本查询串（本 change 不做，记为已知现象）。

## Migration Plan

纯前端，无数据迁移。回滚 = revert 提交；残留 `projflow-favicon` key 会被校验回落为默认（`readFavicon()` 已做 `FAVICONS.some()` 检查）。
