# cleanup-stale-accent

## Why

强调色体系（`theme-accent` capability）落地后，仍有一批**硬编码的旧主色**没跟上，导致切换强调色时这些元素不变化：

| 位置 | 值 | 影响 |
|------|-----|------|
| `PaperList.vue:591` `.stat-num` | `#4f46e5` | 统计数字永远是靛蓝 |
| `PaperList.vue:601` 卡片 hover 边框 | `#4f46e544` | hover 边框永远靛蓝 |
| `PaperList.vue:602` pinned 卡片 | `#4f46e5` + `#fafaff` | 左边条永远靛蓝；`#fafaff` 在深色模式下是浅底 |
| `PaperList.vue:630/632` 链接胶囊 | `#4f46e5` | 文字与 hover 背景永远靛蓝 |
| `Home.vue:147` 项目管理模块图标 | `#4f46e5` | 陈旧 |
| `TeamDetail.vue:8` 头像底色 | `#4f46e5` | 陈旧 |

另外 `web/public/icons.svg`（一套社交图标 sprite）**从未被任何代码引用**，是初始脚手架带进来的死文件。

这违反 `theme-accent` 已写的「切换强调色后全站主色元素同步变化」，属实现缺陷 + 清理。

## What Changes

- 新增运行时令牌 `--color-primary-border`（主色的中透明度变体，用于 hover 边框等），随强调色/明暗模式更新；同步 `:root` 与 dark 的兜底值。
- `PaperList.vue`：`#4f46e5` 系列 → `var(--color-primary)` / `var(--color-primary-border)`；pinned 卡片底 `#fafaff` → `var(--color-primary-soft)`。
- `Home.vue`：项目管理模块图标 `#4f46e5` → `var(--color-primary)`（论文/评测模块保持各自的分类色）。
- `TeamDetail.vue`：头像底色 `#4f46e5` → `var(--color-primary)`。
- 删除死文件 `web/public/icons.svg`。

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

- `theme-accent`: 新增「主色不得硬编码」约束，防止再次出现不跟随强调色的元素。

## Impact

- 前端：`web/src/config/theme.js`、`web/src/stores/theme.js`、`web/src/styles/index.scss`、`web/src/styles/variables.scss`、`web/src/views/papers/PaperList.vue`、`web/src/views/Home.vue`、`web/src/views/management/TeamDetail.vue`；删除 `web/public/icons.svg`。
- 行为变化：上述元素开始跟随强调色；pinned 卡片在深色模式下不再出现浅底。
- **不在范围**：`PaperList.vue` 自成一套的 slate 色板（`#64748b` / `#f8fafc` / `#1e293b` / `#94a3b8` 等）不随主题变化 —— 那是该页尚未接入主题令牌的遗留，整页改造属独立工作。
- `TeamList.vue` 的 `colors` 数组是**刻意**的多色头像轮换，不属主色，保持不动。
- 归属：`web/` 与共享脚手架层 → 提交加 `[shared]` 前缀。
