## Context

主色现在分散在四处且互不关联：

| 位置 | 内容 |
|------|------|
| `App.vue:30` | `themeOverrides.common.{primaryColor,primaryColorHover,primaryColorPressed}` —— Naive UI 组件用 |
| `styles/index.scss` `:root` | `--color-primary` / `--color-primary-soft` / `--color-selected` —— 自定义元素用 |
| `styles/index.scss` `:root[data-theme='dark']` | 同上，dark 变体 |
| `styles/variables.scss` | `$primary-color` 等（编译期常量，供上面引用） |

已有可复用的模式：`stores/theme.js` 用 pinia + localStorage（`projflow-theme`）+ `<html data-theme>` 属性。

## Goals / Non-Goals

**Goals:**

- 预设强调色可切换，且 **Naive UI 组件与自定义 CSS 变量同源**，不再可能不同步。
- 选择持久化；light / dark 各取匹配色值。
- 顶栏调色盘入口，与明暗切换按钮并列。

**Non-Goals:**

- 不做任意取色器（hex 输入框、吸管），只提供预设。
- 不改明暗模式的判定、存储键与切换逻辑。
- 不改 Mermaid / ECharts / 代码高亮的配色。
- 不改 `variables.scss` 的编译期常量（保留为无 JS 时的兜底）。

## Decisions

### D1: 单一数据源 `web/src/config/theme.js`，JS 同时驱动 CSS 变量与 Naive

```js
export const DEFAULT_ACCENT = 'indigo'

export const ACCENTS = [
  { key: 'indigo', label: '靛蓝', light: '#4f46e5', dark: '#818cf8' },
  { key: 'blue',   label: '蓝色', light: '#2563eb', dark: '#60a5fa' },
  { key: 'cyan',   label: '青色', light: '#0891b2', dark: '#22d3ee' },
  { key: 'teal',   label: '青绿', light: '#0d9488', dark: '#2dd4bf' },
  { key: 'green',  label: '绿色', light: '#16a34a', dark: '#4ade80' },
  { key: 'amber',  label: '琥珀', light: '#d97706', dark: '#fbbf24' },
  { key: 'rose',   label: '玫红', light: '#e11d48', dark: '#fb7185' },
  { key: 'violet', label: '紫罗兰', light: '#7c3aed', dark: '#a78bfa' },
]
```

- 理由：两套渲染路径（Naive 主题对象 / CSS 变量）必须取同一个值，否则必然漂移；把色表放在一个模块，两边都从它算。
- 备选：只用 SCSS 定义 `data-accent` 规则 —— Naive UI 读不到，必须再抄一份到 JS，回到双源问题，不采用。

### D2: 预设表每色只给 2 个值，其余派生

- `hover` / `pressed`：由主色 `mix()` 得到（light 模式 hover 提亮 12%、pressed 压暗 12%；dark 模式幅度略小）。
- `--color-primary-soft` / `--color-selected`：由主色 `toRgba()` 得到（沿用现状 alpha：light `0.12` / `0.08`，dark `0.15` / `0.12`）。

理由：若每个色手挑 6 个值（primary/hover/pressed × 明暗），8 色要维护 48 个十六进制，且新加一色成本高；派生保证同色系关系正确。

- 备选：全部手挑 —— 可控但维护成本高、易不一致，不采用。

### D3: 运行时写 `<html>` inline CSS 变量，SCSS 默认值保留为兜底

store 在 accent / mode 变化时：

```js
root.style.setProperty('--color-primary', primary)
root.style.setProperty('--color-primary-soft', toRgba(primary, softAlpha))
root.style.setProperty('--color-selected', toRgba(primary, selectedAlpha))
```

- 理由：inline style 优先级高于样式表里的 `:root`，无需为每个预设写一段 SCSS；SCSS 里现有的 `--color-primary` 保留，作为 JS 未执行（首屏极短窗口）时的兜底，不删。
- 备选：为 8 色 × 2 模式写 16 段 SCSS 规则 —— 与 D1 的双源问题重现，不采用。

### D4: 存储键 `projflow-accent`，与 `projflow-theme` 并列

沿用 `stores/theme.js` 现有 localStorage 读写与 `try/catch` 兜底风格。`toggle()` 只改 mode，`setAccent()` 只改 accent，互不覆盖。

### D5: 入口用 `n-popover` + 色块网格，而不是 `n-dropdown` 菜单

色块网格能直接展示颜色，比文字菜单更符合「调色盘」直觉；当前项用对勾 + 边框标识。

- 按钮图标：`ColorPaletteOutline`（`@vicons/ionicons5` 已确认存在），与现有 `SunnyOutline` / `MoonOutline` 同尺寸同风格。
- 按钮放在 `<span class="header-date">` 与明暗切换 `n-button` 之间。

## Risks / Trade-offs

- [inline 变量覆盖 SCSS，导致某些依赖 SCSS 变量的编译期逻辑失效] → 只覆盖 3 个运行时令牌，`variables.scss` 的编译期常量不动；`$primary-color` 仍用于初始 `:root`。
- [Naive 部分组件用 `primaryColorSuppl`，只改 `primaryColor` 会漏] → `themeOverrides` 一并给出 `primaryColorSuppl`。
- [明暗切换后未重新应用，dark 下仍用 light 色值] → `applyAccent()` 依赖 mode，`watch([accent, mode])` 同时触发。
- [8 个预设色在 dark 下对比度不足] → 每色的 dark 值统一取较亮变体（相对 light 值提亮），并在验证时逐个目视。
- [新加颜色要改多处] → 只需在 `ACCENTS` 数组加一行，CSS 与 Naive 自动跟随。

## Migration Plan

纯前端，无数据迁移。已有用户 localStorage 无 `projflow-accent` → 按默认靛蓝渲染，视觉与改动前一致（`#4f46e5` / `#818cf8` 即现值）。回滚 = revert 提交；残留 key 无害。
