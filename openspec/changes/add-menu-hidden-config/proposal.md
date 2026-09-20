# Proposal: add-menu-hidden-config（菜单/功能隐藏配置）

## Why

ProjFlow 侧边栏菜单硬编码在 `web/src/layouts/MainLayout.vue`（项目管理：项目树/团队成员/报告/任务看板/里程碑/会议纪要/文档；另有论文/数据集/训练/评测分组）。下游库从本库初始化时不需要全部功能，目前只能改代码裁剪——不可逆、易破坏共享脚手架、后续同步上游改进会冲突。需要一个配置化的 hidden 列表：菜单不显示、路由保留可直达、随时可逆。此外「报告」页面内部还有日报/周报/月报 type tabs，也需要能按类型单独隐藏。

## What Changes

- 新增 `web/src/config/hidden.js`：导出 `HIDDEN_KEYS` 常量数组（默认空 = 全部显示），注释内列出全部可用 key
- 修改 `web/src/layouts/MainLayout.vue`：构建菜单后按 `HIDDEN_KEYS` 过滤——
  - 叶子级：按路由 path 匹配（如 `/management/reports` 隐藏整个「报告」菜单项）
  - 分组级：按分组 key 匹配（如 `evaluation` 隐藏整个「评测体系」）；组内叶子全部隐藏时分组自动隐藏
- 修改 `web/src/views/management/ReportPage.vue`：type tabs 按 `reports:daily` / `reports:weekly` / `reports:monthly` 过滤；当前激活类型被隐藏时自动切到第一个可见类型
- 路由（`router/index.js`）**不动**：被隐藏功能 URL 直达永远可用，删掉 key 即恢复——完全可逆
- 归属：`MainLayout.vue` 属共享脚手架层，实施时 commit 加 `[shared]` 前缀

## Capabilities

### New Capabilities
- `menu-visibility`: 通过集中配置的 hidden key 列表控制侧边栏菜单与报告类型 tab 的可见性；隐藏不删路由，配置可逆

### Modified Capabilities

（无——`openspec/specs/` 当前为空，无既有 capability 受影响）

## Impact

- 新增：`web/src/config/hidden.js`
- 修改：`web/src/layouts/MainLayout.vue`（菜单过滤）、`web/src/views/management/ReportPage.vue`（tab 过滤 + 激活类型兜底）
- 不影响：`router/index.js`、后端、其他页面；`HIDDEN_KEYS` 为空时行为与现状完全一致
- 关联 change：`add-fork-init-guide`（初始化指南第 7 节将以本功能为默认裁剪手段）
