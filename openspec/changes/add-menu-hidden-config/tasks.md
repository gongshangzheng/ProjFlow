# Tasks: add-menu-hidden-config

## 1. 配置模块

- [x] 1.1 新建 `web/src/config/hidden.js`：导出 `HIDDEN_KEYS`（默认 `[]`）与纯函数 `filterHidden(items, hiddenKeys)`；文件头注释分三段列出全部可用 key（分组：`management/papers/training/evaluation`；叶子：全部菜单项 path；报告类型：`reports:daily|weekly|monthly`），注明与 MainLayout.vue menuOptions 同步维护

## 2. 菜单过滤（MainLayout.vue）

- [x] 2.1 `web/src/layouts/MainLayout.vue` 引入 `HIDDEN_KEYS` + `filterHidden`，新增 computed `visibleMenuOptions`：叶子按 path 摘除、分组 key 命中摘整组、children 过滤后为空摘整组；`<n-menu>` 改绑 `visibleMenuOptions`
- [x] 2.2 验证：`HIDDEN_KEYS=[]` 时菜单与现状一致；含 `/management/reports` 时「报告」消失且 URL 直达可访问；含 `evaluation` 时整组消失；`/papers/list`+`/papers/config` 同时隐藏时「论文搜集」组消失、仅隐藏其一时组内剩一项

## 3. 报告类型过滤（ReportPage.vue）

- [x] 3.1 `web/src/views/management/ReportPage.vue` 引入 `HIDDEN_KEYS`，新增 computed `visibleTypes`（按 `reports:<type>` 过滤两处 type tabs 模板）；`activeType` 兜底：当前值被隐藏时回落 `visibleTypes[0]`；`visibleTypes` 为空时渲染空态提示 + console.warn
- [x] 3.2 验证：`reports:daily` 隐藏时仅显示周报/月报 tab 且默认周报；停留日报 tab 刷新后自动落周报；日报详情路由直达正常；三类型全隐藏时页面空态不崩溃

## 4. 收尾

- [x] 4.1 全量回归：`HIDDEN_KEYS=[]` 跑通首页/项目树/报告/任务看板/论文/评测各一页；确认 `router/index.js` 零改动
- [x] 4.2 提交：`[shared] feat: 菜单与报告类型可配置隐藏（HIDDEN_KEYS）`
