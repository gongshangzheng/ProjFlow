## Context

- `web/src/config/theme.js` 是强调色的唯一数据源：`ACCENTS` 每项含 `key` / `label` / `light` / `dark`，`hover`、`pressed`、`soft`、`selected` 全部由 `mix()` / `toRgba()` 派生。
- 调色盘（`MainLayout.vue`）用 `v-for="a in ACCENTS"` 渲染，`swatchColor()` 按当前模式取 `light` / `dark`。
- 因此新增一个预设**只需在数组加一行**，UI 与注入逻辑自动跟随。

## Goals / Non-Goals

**Goals:**

- 增加一个中性灰强调色，明暗两套模式各取匹配色值。

**Non-Goals:**

- 不改色板网格列数（4 列，9 项呈 4+4+1，可接受）。
- 不改既有 8 个色值。
- 不新增 spec（`theme-accent` 契约已是「≥6 种预设」）。

## Decisions

### D1: 色值取枪灰 —— light `#4a4f57` / dark `#a8aeb6`

- `light #4a4f57`（RGB 74/79/87）：R<G<B，冷调偏蓝绿，比中性灰 `#52525b` 更深、更有「枪械金属」感；白底上作主色与白色文字对比度约 8:1。
- `dark #a8aeb6`（RGB 168/174/182）：沿用同色族提亮思路，在深底 `#18181b` 上对比度约 7.4:1；与既有 dark 变体（`#818cf8`、`#22d3ee` 等偏亮）风格一致。
- 同一色族取深浅两端，明暗切换时色相不跳（都保持 R<G<B 的冷调）。
- 备选：中性灰 `#52525b` / `#a1a1aa`（zinc 系）—— R=G、蓝通道单边高，不算枪灰，已弃用。
- 备选：提供「石墨黑」二分（`light #3f3f46`）—— 用户只要求一个灰色，不采用；后续需要再加行即可。

### D2: 排在数组末尾

`APPEND` 在 `violet` 之后，不改变既有项顺序与默认项（`DEFAULT_ACCENT = 'indigo'`）。

### D3: 默认色改为枪灰 + 同步无 JS 兜底色值

`DEFAULT_ACCENT` 由 `'indigo'` 改为 `'gray'`；同时把样式层的「无 JS 兜底」也换成枪灰：

| 位置 | 改前 | 改后 |
|------|------|------|
| `variables.scss` `$primary-color` | `#4f46e5` | `#4a4f57` |
| `variables.scss` `$primary-light` / `$primary-dark` | `#6366f1` / `#4338ca` | `#60646b` / `#41464d`（按 `mix()` 规则手算） |
| `index.scss` `:root` `--color-primary-soft` / `--color-selected` | 靛蓝 rgba | 枪灰 rgba |
| `index.scss` dark `--color-primary` / soft / selected | `#818cf8` / 靛蓝 / 蓝 | `#a8aeb6` / 中性 / 中性 |

- 理由：`:root` 的变量在 JS store 执行前就已生效（首屏极短窗口），若不同步会出现「枪灰→靛蓝→枪灰」闪色。
- 顺带修正：`index.scss` 的 `blockquote { border-left: 4px solid $primary-color }` 用的是**编译期常量**，改强调色时它不跟随（永远靛蓝）。改为 `var(--color-primary)` 后与其它元素一致。

## Risks / Trade-offs

- [枪灰作主色时选中态不够醒目] → `--color-selected` 用 rgba 叠加，仍有可见底色差；这是「不抢注意力」的预期代价。
- [9 个色块在 4 列网格里最后一行只有 1 个] → 仅视觉排布，不影响功能；若在意可改 3 列（后续一行改动）。

## Migration Plan

纯前端、无迁移。回滚 = revert 提交；已存 `projflow-accent = 'gray'` 的浏览器在回滚后会因校验失败回落到默认靛蓝（`readAccent()` 已做 `ACCENTS.some()` 校验）。
