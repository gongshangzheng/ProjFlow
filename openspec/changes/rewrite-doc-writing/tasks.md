## 1. 重写 doc-writing

- [x] 1.1 重写 `.agents/skills/doc-writing/SKILL.md`：description/触发词收窄为「流程门禁」类
- [x] 1.2 写入适用范围与豁免（含可判定标准：读者是否需要重新理解文档结构）
- [x] 1.3 写入门禁四步（判断 → 建 change → design 写清五要素 → 审核后动笔）
- [x] 1.4 写入落点与登记表（`management/docs/` + `openspec/registry.md` + 根目录不设 `docs/`）
- [x] 1.5 写入与 `documentation` / `management` 的分工，且不重复细则
- [x] 1.6 删除全部医学/临床表述与 `docs/research` 路径

## 2. 修订 documentation

- [x] 2.1 §1.1 表格：「总 Change `docs-system`」→「登记表 `openspec/registry.md`」并说明登记动作
- [x] 2.2 顶部补一行与 `doc-writing` 的分工（流程 vs 内容）
- [x] 2.3 description 触发词收窄为「内容规范」类，去掉与「写文档」的重叠

## 3. 验证

- [x] 3.1 两个 skill 的 description 触发词无交集（人工比对 + 输出两者 description）
- [x] 3.2 `grep -rn "临床\|医学\|临床合作者\|docs/research" .agents/skills/` 无命中
- [x] 3.3 `doc-writing` 与 `documentation` 互指关系正确（各自提到对方管什么）
- [x] 3.4 `.claude/skills` 读到内容与 `.agents/skills` 一致（符号链接）
- [x] 3.5 `openspec validate --all --strict` 通过
- [x] 3.6 代码零改动（`git status` 不含 `web/`、`server/`）

## 4. 收尾

- [x] 4.1 提交（`[shared]`）
- [x] 4.2 归档
- [x] 4.3 回报「是否需要合并两个 skill」这一遗留项
