## Context

- 上游 ProjFlow 在 `83c78fb` 删除了空目录 `docs/`，并明确「文档统一放 management/docs/」。
- 但 `AGENTS.md` 的目录树未同步，仍在第 118 行列出 `└── docs/  # 其他文档`。
- 下游库（`digital-human`、`children-face`、`pet-action-recognition` 等）以 `AGENTS.md` 为派生蓝本，已出现照抄该行、并在根目录重建 `docs/` 的实例（`digital-human/docs/external-sources.md`）。
- `AGENTS.md` 结构属上游所有（见 `upstream-sync` 责任分工表），因此修正必须落在上游，再向下游传播。

## Goals / Non-Goals

**Goals:**

- 让 `AGENTS.md` 的目录树与磁盘真实结构一致（根目录无 `docs/`）。
- 用一条 spec requirement 把「文档根目录唯一」固定下来，避免再次回潮。

**Non-Goals:**

- 不触碰 `management/docs/` 内部的文档组织（由 `docs-system` 总 Change 负责）。
- 不处理任何单个下游库的具体清理（各下游自行 cherry-pick 本 `[shared]` 提交）。
- 不修改后端/前端对文档的扫描逻辑（`get_docs()` 行为不变）。

## Decisions

### D1: 只改 `AGENTS.md` 一处，不加过渡说明

删掉 `└── docs/  # 其他文档`，并在 `management/docs/` 那一行补充「文档统一在此」的注释。

- 理由：目录树是结构速查表，过时条目比缺条目更有害（会被下游当作模板照抄）。
- 备选：保留该行并标注「已废弃」——会继续被复制，不采用。

### D2: 写入 spec 而非仅修文档

在 `documentation` capability 下新增 requirement，明确根目录不得有 `docs/`，且结构说明须随结构变更同步。

- 理由：这次问题的根因是「文档与实现脱节且无契约约束」；只改一次文字无法防止下一次。
- 备选：`skip_specs: true` 纯文档修订——无法阻止回潮，不采用。

## Risks / Trade-offs

- [下游 `AGENTS.md` 已分叉，cherry-pick 可能冲突] → 冲突只涉及目录树附近一两行，人工合入即可；`upstream-sync` 已记录该处理方式。
- [本 change 只修上游，不保证下游立刻跟] → 属预期：下游按各自节奏 pick；本 change 在 proposal/Impact 中已声明传播方式。
