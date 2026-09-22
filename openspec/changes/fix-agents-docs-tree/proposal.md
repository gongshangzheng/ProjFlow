# fix-agents-docs-tree

## Why

`AGENTS.md` 的目录树里仍列着仓库根目录 `docs/`（第 118 行 `└── docs/  # 其他文档`），但该目录早已被删除（`83c78fb chore: 删除项目根目录空 docs/，文档统一放 management/docs/`）。这行过时描述已实际误导下游：`digital-human` / `children-face` 派生后照抄该树，在根目录重新建出了 `docs/`，与上游既定约定相悖。

## What Changes

- 删除 `AGENTS.md` 目录树中过时的 `└── docs/  # 其他文档` 行。
- 在同一处补充一句明确约定：仓库文档统一置于 `management/docs/`，根目录不设 `docs/`。
- 将「文档根目录唯一」写入 `documentation` capability，防止再次回潮。

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

- `documentation`: 新增一条 requirement，明确仓库文档的根目录唯一性（`management/docs/`），根目录 MUST NOT 存在 `docs/`。

## Impact

- 文档：`AGENTS.md`（目录树块，约 1 行替换为 1 行）。
- 规范：`openspec/specs/documentation/spec.md`（新增 1 条 requirement + scenario）。
- 下游：本 change 以 `[shared]` 提交，供 `digital-human` / `children-face` 等下游 cherry-pick，纠正各自 `AGENTS.md` 的同名过时行。
- 不涉及运行时代码、API、端口与业务数据。
