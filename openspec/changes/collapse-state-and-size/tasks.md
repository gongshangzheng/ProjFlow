## 1. 配置与持久化

- [x] 1.1 新增 `web/src/config/layout.js`：导出 `SIDEBAR_DEFAULT_COLLAPSED = true`（含「仅在无本地偏好时生效，下游可覆盖」注释）
- [x] 1.2 `MainLayout.vue`：新增 `SIDEBAR_COLLAPSED_KEY = 'app.sidebar-collapsed'` 及 `readCollapsed()` / `writeCollapsed()`
- [x] 1.3 `MainLayout.vue`：`collapsed` 初值改为 `readCollapsed()`；加 `watch(collapsed, writeCollapsed)`（不设 immediate）

## 2. 折叠尺寸收缩

- [x] 2.1 `MainLayout.vue`：`n-layout-sider` 的 `collapsed-width` `64 → 56`
- [x] 2.2 `MainLayout.vue`：`n-menu` 的 `collapsed-width` `64 → 56`、`collapsed-icon-size` `22 → 18`
- [x] 2.3 `MainLayout.vue`：折叠态 logo（`.logo-icon`）字号适配窄条
- [x] 2.4 `DocPage.vue`：`.doc-sidebar.collapsed` 与 `.doc-toc.collapsed` 宽度 `28px → 20px`
- [x] 2.5 `DocPage.vue`：`.panel-strip-label` 字号 `11 → 10px`、字距 `2 → 1px`

## 3. 验证

- [x] 3.1 首次访问（清 localStorage）：侧边栏为折叠态
- [x] 3.2 展开后刷新：仍为展开；折叠后刷新：仍为折叠
- [x] 3.3 删除 `app.sidebar-collapsed` 后刷新：回到默认折叠
- [x] 3.4 文档页两侧面板与主题偏好不受影响（key 互不覆盖）
- [x] 3.5 折叠态实测宽度：主侧边栏 ≈56px、文档页两栏 ≈20px；图标与竖排标签无裁切
- [x] 3.6 展开态回归：主侧边栏 240px、文档页两栏恢复 210px / 180px
- [x] 3.7 菜单多级展开/收起正常，菜单点选与路由跳转正常
- [x] 3.8 `npm run build` 通过

## 4. 收尾

- [x] 4.1 `openspec validate collapse-state-and-size` 通过
- [x] 4.2 以 `[shared]` 前缀提交
