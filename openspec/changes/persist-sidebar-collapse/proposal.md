# persist-sidebar-collapse

## Why

应用主侧边栏（`MainLayout.vue` 的 `n-layout-sider`）的折叠状态**没有任何持久化**：

```js
const collapsed = ref(false)   // 刷新即回到展开
```

后果：用户把侧边栏折叠后，一刷新就自动展开，需要反复手动折叠。文档页两侧面板（`DocPage.vue`）已有 localStorage 持久化，主侧边栏漏了同一能力。

同时希望**首次访问默认折叠**，把横向空间让给正文。

## What Changes

- `web/src/layouts/MainLayout.vue`：侧边栏折叠状态改为从 localStorage 读取，并在状态变化时写回（key `app.sidebar-collapsed`，沿用 `doc-page.*` 命名惯例）。
- 新增 `web/src/config/layout.js`：导出 `SIDEBAR_DEFAULT_COLLAPSED`（本仓库设为 `true`），只在该 key 无本地偏好时生效；下游可覆盖。
- localStorage 不可用（隐私模式等）时静默降级为默认值，不报错。

## Capabilities

### New Capabilities

- `sidebar-collapse`: 应用主侧边栏折叠状态的持久化与首次默认值。

### Modified Capabilities

（无）

## Impact

- 前端：`web/src/layouts/MainLayout.vue`、新增 `web/src/config/layout.js`。
- 行为变化：刷新后侧边栏保持折叠/展开状态；首次访问（无本地偏好）默认折叠。
- 不影响：文档页两侧面板（各自独立 key）、路由与菜单内容、主题偏好。
- 归属：`web/layouts/MainLayout.vue` 属共享脚手架层 → 提交加 `[shared]` 前缀；下游通过 `SIDEBAR_DEFAULT_COLLAPSED` 覆盖默认值。
