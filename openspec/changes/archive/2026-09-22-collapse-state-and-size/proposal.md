# collapse-state-and-size

## Why

两件相关的事：

**1. 应用主侧边栏折叠状态不持久化。** `MainLayout.vue` 是 `const collapsed = ref(false)`，无任何存储；用户折叠后一刷新就自动展开。文档页两侧面板（`DocPage.vue`）已有 localStorage 持久化，主侧边栏漏了同一能力。同时希望首次访问默认折叠。

**2. 各类折叠态占位偏宽。**

| 位置 | 现状 | 问题 |
|------|------|------|
| 主侧边栏折叠宽度 | `:collapsed-width="64"` | 只放图标，64px 偏宽 |
| 主侧边栏折叠图标 | `:collapsed-icon-size="22"` | 相对窄条偏大 |
| 文档页左栏折叠条 | `.doc-sidebar.collapsed { width: 28px }` | 加上 24px gap，视觉留白 52px |
| 文档页右栏折叠条 | `.doc-toc.collapsed { width: 28px }` | 同上 |

## What Changes

**折叠状态（原 `persist-sidebar-collapse` 范围）**

- `MainLayout.vue`：折叠状态从 localStorage 读取并写回（key `app.sidebar-collapsed`）。
- 新增 `web/src/config/layout.js`：`SIDEBAR_DEFAULT_COLLAPSED`（本仓库 `true`），仅在无本地偏好时生效；下游可覆盖。
- localStorage 不可用时静默降级。

**折叠尺寸**

- 主侧边栏：折叠宽度 `64 → 56`，折叠态菜单图标 `22 → 18`（`n-menu` 的 `collapsed-width` 同步）；折叠态 logo 字号微调以适配窄条。
- 文档页：左右栏折叠条 `28px → 20px`，竖排标签字号 `11 → 10px`、字距 `2 → 1px`。

## Capabilities

### New Capabilities

- `sidebar-collapse`: 应用主侧边栏折叠状态的持久化、首次默认值与折叠态尺寸。

### Modified Capabilities

- `docs-page-layout`: 新增「折叠态边条宽度最小化」约束（左右栏折叠条 ≤ 20px）。

## Impact

- 前端：`web/src/layouts/MainLayout.vue`、`web/src/views/management/DocPage.vue`、新增 `web/src/config/layout.js`。
- 行为变化：刷新后侧边栏保持折叠/展开；首次访问默认折叠；折叠态占位变窄（主侧边栏 64→56，文档页两栏 28→20）。
- 不影响：文档页两侧面板的默认展开策略（阅读需要目录）、路由与菜单内容、主题偏好。
- 归属：均属共享脚手架/文档体系层 → 提交加 `[shared]` 前缀；下游可通过 `SIDEBAR_DEFAULT_COLLAPSED` 覆盖默认值。
