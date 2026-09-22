## 1. 修正 AGENTS.md 目录树

- [x] 1.1 删除 `AGENTS.md` 目录树末尾的 `└── docs/  # 其他文档` 行
- [x] 1.2 在 `management/docs/` 树行补注「文档统一在此，根目录不设 docs/」
- [x] 1.3 通读目录树，确认其余条目与磁盘实际结构一致

## 2. 校验与提交

- [x] 2.1 `openspec validate fix-agents-docs-tree` 通过
- [x] 2.2 确认仓库根目录无 `docs/`（`test ! -d docs`）
- [x] 2.3 以 `[shared]` 前缀提交，供下游 cherry-pick
