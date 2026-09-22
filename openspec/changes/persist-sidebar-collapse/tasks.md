## 1. 配置与持久化

- [x] 1.1 新增 `web/src/config/layout.js`：导出 `SIDEBAR_DEFAULT_COLLAPSED = true`（含「仅在无本地偏好时生效，下游可覆盖」注释）
- [x] 1.2 `MainLayout.vue`：新增 `SIDEBAR_COLLAPSED_KEY = 'app.sidebar-collapsed'` 及 `readCollapsed()` / `writeCollapsed()`
- [x] 1.3 `MainLayout.vue`：`collapsed` 初值改为 `readCollapsed()`；加 `watch(collapsed, writeCollapsed)`（不设 immediate）

## 2. 验证

- [x] 2.1 首次访问（清 localStorage）：侧边栏为折叠态
- [x] 2.2 展开后刷新：仍为展开；折叠后刷新：仍为折叠
- [x] 2.3 删除 `app.sidebar-collapsed` 后刷新：回到默认折叠
- [x] 2.4 文档页两侧面板与主题偏好不受影响（key 互不覆盖）
- [x] 2.5 菜单点击、路由跳转、面包屑正常；`npm run build` 通过

## 3. 收尾

- [x] 3.1 `openspec validate persist-sidebar-collapse` 通过
- [x] 3.2 以 `[shared]` 前缀提交
