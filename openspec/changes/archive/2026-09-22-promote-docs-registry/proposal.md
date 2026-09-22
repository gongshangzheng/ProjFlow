# promote-docs-registry

## Why

`documentation` spec 声明「文档登记表为**唯一权威**」，但这张表**只存在于归档 change 里**：

```text
openspec/changes/archive/2026-09-20-docs-system/design.md   ← 表的唯一所在
```

而 `docs-system` 是**已归档**的「体系级总 Change」。spec 的流程又要求「新增一篇 wiki 先在总 Change 登记」，于是形成两个问题：

1. **权威来源不可维护**：新增文档要登记时，只能去改归档产物，语义与操作都错位。
2. **有一行漏登记**：`add-article-note-skill` 的设计与 Impact 写明「两行仓库级改动」，其中 `.gitignore` 的 `.cache/` 已落地，但**登记表的 `notes/*` 类目行从未加上**（现表只有 4 行：`api-design-conventions` / `git-workflow` / `papers/docs/*` / `evaluation/docs/*`）。

## What Changes

- 新增 `openspec/registry.md`：文档登记表迁到耐久位置（内容取自 `docs-system` 的 design，按 ProjFlow 现状重写），并补上缺失的 `notes/*` 行。
- `openspec/specs/documentation/spec.md`：修订「文档登记表为唯一权威」，指明登记表位置为 `openspec/registry.md`，并把「先在总 Change 登记」改为「先在登记表登记」。
- `openspec/changes/archive/2026-09-20-docs-system/design.md`：在原表处加一行指针，声明登记表已迁出、以 `openspec/registry.md` 为准（保留历史内容不动）。
- `AGENTS.md`：补两处说明 —— ①登记表位置（AI 改文档时的入口）；②**「push 即部署」**：`management/docs/*.md` 是构建期编译进 `docs-data.json` 的，改完必须 push 才会在线上生效。

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

- `documentation`: 「文档登记表为唯一权威」明确登记表位置，并把登记动作从「总 Change」改为「登记表」——因为总 Change 已归档。

## Impact

- 文档/治理：新增 `openspec/registry.md`；修改 `openspec/specs/documentation/spec.md`、`AGENTS.md`、`docs-system` 归档 design 的一行指针。
- 代码：**不动**（登记表是治理件，不影响运行时代码）。
- 契约变化：登记表的**新增/修改文档登记流程**由「在 docs-system change 里登记」变为「在 `openspec/registry.md` 登记」；`docs-system` 及其它已归档 change 的历史记录保持原样。
- 范围外：不改 wiki 的渲染/接口（`management/docs/` 的扫描与 sidecar 行为不变）、不改编号体系本身。
