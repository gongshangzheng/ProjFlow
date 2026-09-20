# Design: add-menu-hidden-config（菜单/功能隐藏配置）

## Context

见 proposal.md — Why。现状：`web/src/layouts/MainLayout.vue` 内 `menuOptions` 硬编码 5 个分组 + 首页；`ReportPage.vue` 内 `REPORT_TYPES = [daily, weekly, monthly]` 硬编码 type tabs。路由集中在 `web/src/router/index.js`。

## Goals / Non-Goals

**Goals:**

- 单一配置点（一个常量数组）控制两级粒度：菜单项（含分组）与报告类型
- 完全可逆：路由不动、URL 直达始终可用、删 key 即恢复
- `HIDDEN_KEYS = []` 时行为与现状逐像素一致（下游同步零风险）

**Non-Goals:**

- 不做运行时/后端动态配置（无需求，静态数组 + git 即可逆）
- 不做用户级权限（hidden 是部署级裁剪，不是访问控制）
- 不隐藏路由（router/index.js 不动，隐藏 ≠ 禁访）
- 不做拖拽排序、图标配置等菜单编辑能力

## Decisions

### D1: 配置形态——前端常量文件 `web/src/config/hidden.js`

- 导出 `HIDDEN_KEYS: string[]`，文件头注释列出全部可用 key（分组/叶子/报告类型三段），供人直接照抄取消注释
- 备选：① 后端配置 API——过度设计，初始化裁剪是静态决策；② `.env` / vite define——藏在构建配置里，可读性与 git 可逆性都差；③ 直接在 MainLayout.vue 顶部放数组——单文件自包含，但"配置"和"实现"耦合，后续 ReportPage 也要读它，必须独立模块
- 常量文件是纯 ESM，无构建步骤、无运行时开销、diff 一目了然

### D2: key 命名——三级命名空间

| 层级 | key 形态 | 示例 |
|------|---------|------|
| 分组 | 裸分组 key（与 menuOptions 的 key 一致） | `management` `papers` `training` `evaluation` |
| 菜单项（叶子） | 完整路由 path | `/management/reports` `/evaluation/models` |
| 报告类型 | `reports:<type>` | `reports:daily` `reports:weekly` `reports:monthly` |

- 叶子直接复用 path：零映射表、与 `handleMenuSelect` 的 key 语义天然一致
- 报告类型不是路由，用 `reports:` 前缀命名空间隔离，避免与 `/management/reports` 混淆（后者是菜单项级、前者是 tab 级，可独立使用）
- 顶层直达项（首页 `/`、数据集 `/datasets`）用 path 规则天然覆盖，无需特判

### D3: 过滤实现——构建后过滤，不污染 menuOptions 定义

- MainLayout.vue：`menuOptions` 定义保持原样；新增 `computed visibleMenuOptions`，在 computed 内过滤后交给 `<n-menu>`。规则：叶子命中 path → 摘除；分组 key 命中 → 摘整组；分组未命中但过滤后 children 为空 → 摘整组
- ReportPage.vue：`REPORT_TYPES` 保持原样；新增 computed `visibleTypes`（按 `reports:<type>` 过滤）；`activeType` 的取值逻辑增加兜底——当前值不在 `visibleTypes` 时回落到 `visibleTypes[0]`；`visibleTypes` 为空时渲染空态提示（spec 已定义该边界）
- 过滤逻辑收敛为一个纯函数 `filterHidden(items, hiddenKeys)`（放 `hidden.js` 内导出），MainLayout 复用；ReportPage 的 tab 过滤单独三行，不复用（结构不同：无嵌套）

### D4: 不动路由——可逆性来源

- `router/index.js` 零改动：被隐藏页面 URL 直达、面包屑、`route.meta` 全部照常
- 恢复 = 从数组删 key + 刷新，无缓存无迁移

## Risks / Trade-offs

- [隐藏项仍可通过 URL 访问，可能被误认为权限控制] → spec 明确"隐藏 ≠ 禁访"；文档（fork-init-guide）中注明用途边界
- [hidden.js 注释里的 key 清单与菜单定义漂移] → key 清单注释标注"与 MainLayout.vue menuOptions 同步维护"；tasks 含核对步骤；菜单本身低频变更
- [空 visibleTypes 边界（三类型全隐藏）] → spec 定义空态提示而非崩溃；属配置错误场景，加 console.warn 提示
- [共享脚手架层变更需传播下游] → commit 加 `[shared]` 前缀，下游按 upstream-sync cherry-pick；`HIDDEN_KEYS=[]` 默认值保证下游不 cherry-pick 也无行为差异

## Migration Plan

默认空数组上线，无行为变化，无迁移。回滚 = revert 单个 commit。

## Open Questions

（无）
