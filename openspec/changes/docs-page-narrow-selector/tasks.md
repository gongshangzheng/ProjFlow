# Tasks: docs-page-narrow-selector

- [x] 1.1 `DocPage.vue` 根容器改为窄屏 `column` / 宽屏 `row`（断点 1024px），窄屏 `gap: 12px`、`padding: 16px`。
- [x] 1.2 `.doc-mobile-select` 窄屏 `width: 100%`、去掉 `margin-bottom`；`n-select` 加 `:consistent-menu-width="false"`。
- [x] 1.3 正文卡片内边距窄屏收紧（<640px 时 16px），保证正文字宽优先。
- [x] 1.4 `cd web && npm run build` 通过；构建产物包含新断点规则。
- [x] 1.5 反哺来源：本改动先在 pet-action-recognition（下游）发现并验证，按 upstream-sync 铁律回填上游。
