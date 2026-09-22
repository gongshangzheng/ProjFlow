# add-gray-accent

## Why

`ACCENTS` 现有 8 个预设全是彩色（靛蓝/蓝/青/青绿/绿/琥珀/玫红/紫罗兰），缺一个**中性灰**。需要灰色的场景很实际：长时间阅读论文笔记时彩色主色会抢注意力；截图、演示、打印时希望主色不干扰内容。色值取**枪灰**（深、冷、微金属感），而非普通中性灰。

## What Changes

- `web/src/config/theme.js` 的 `ACCENTS` 增加一项：

```js
{ key: 'gray', label: '枪灰', light: '#4a4f57', dark: '#a8aeb6' },
```

- 调色盘自动多出一个色块（无需改 `MainLayout.vue` —— 色板由 `ACCENTS` 驱动）。
- **默认强调色改为枪灰**：`DEFAULT_ACCENT` 由 `'indigo'` 改为 `'gray'`。
- **同步无 JS 兜底色值**：`styles/variables.scss` 的 `$primary-*` 与 `styles/index.scss` 的 `:root` / `:root[data-theme='dark']` 三个运行时变量改为枪灰（避免 JS 生效前闪一下靛蓝）；`blockquote` 的 `border-left` 由编译期 `$primary-color` 改为 `var(--color-primary)`，使其真正跟随强调色。

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

- `theme-accent`: 「强调色选择持久化」中的默认色由「靛蓝」改为「枪灰」，并补充「未知 key 回落」场景。

## Impact

- 前端：`web/src/config/theme.js` 一行；调色盘色块从 8 个变 9 个（网格 4 列 → 4+4+1）。
- 行为变化：清除本地偏好后默认主色为枪灰（原为靛蓝）；`blockquote` 左侧竖条开始跟随强调色（原固定靛蓝）。
- 不影响：既有 9 个预设的色值、明暗适配逻辑、`projflow-accent` 存储键、Naive/CSS 同源机制。
- 归属：共享脚手架层 → 提交加 `[shared]` 前缀。
