# add-accent-color-picker

## Why

当前全站只有一个紫色/靛蓝主色，且**写死在两处**、彼此无关联：

```js
// App.vue:30 —— Naive UI 组件色（静态常量）
const themeOverrides = { common: { primaryColor: '#4f46e5', primaryColorHover: '#6366f1', primaryColorPressed: '#4338ca' } }
```

```scss
// styles/index.scss —— 自定义元素的 CSS 变量
:root                 { --color-primary: #4f46e5; --color-primary-soft: rgba(79,70,229,.12); }
:root[data-theme=dark]{ --color-primary: #818cf8; --color-primary-soft: rgba(129,140,248,.15); }
```

用户无法更换主色，且这两处一旦不同步就会出现「Naive 组件一个色、自定义元素另一个色」。本次提供**强调色（主题色）切换**：顶栏明暗切换按钮旁加一个调色盘，可从预设色中选，选择持久化，明暗两套模式下自动取对应色值。

## What Changes

- 新增 `web/src/config/theme.js`：预设强调色表（每色含 light / dark 两个主色值）+ 默认项 + 颜色工具（`mix` 派生 hover/pressed、`toRgba` 派生生 soft/selected）。
- `web/src/stores/theme.js`：新增 `accent` 状态与 `setAccent()`，持久化到 `projflow-accent`，并在明暗模式或强调色变化时把值写入 `<html>` 的 CSS 变量（`--color-primary` / `--color-primary-soft` / `--color-selected`）。
- `web/src/App.vue`：`themeOverrides` 由静态常量改为 `computed`，随 accent + mode 变化重算（Naive UI 组件与 CSS 变量**同源**，不再可能不同步）。
- `web/src/layouts/MainLayout.vue`：顶栏 `header-right` 在明暗切换按钮旁新增调色盘按钮（`ColorPaletteOutline`），点击弹出预设色板，当前色带选中标记。

## Capabilities

### New Capabilities

- `theme-accent`: 全站强调色（主色）的预设集合、切换入口、持久化与明暗适配。

### Modified Capabilities

（无）

## Impact

- 前端：新增 `web/src/config/theme.js`；修改 `web/src/stores/theme.js`、`web/src/App.vue`、`web/src/layouts/MainLayout.vue`、`web/src/styles/index.scss`。
- 行为变化：主色可切换并跨会话保留；明暗模式各取匹配色值；Naive UI 组件与自定义元素主色保持同源。
- 不影响：明暗模式切换逻辑与存储键、路由、菜单内容、业务数据。
- 归属：均属共享脚手架层 → 提交加 `[shared]` 前缀。
