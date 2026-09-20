# Tasks: move-skills-to-agents

## 1. 目录交换

- [x] 1.1 删除 `.agents` 符号链接（`git rm .agents`），建真实目录 `.agents/`
- [x] 1.2 `git mv .claude/skills .agents/skills`（10 个 skill 真实文件迁移，保留 git 血缘）
- [x] 1.3 建反向符号链接 `ln -s ../.agents/skills .claude/skills` 并 `git add`
- [x] 1.4 验证双向可达：`.agents/skills/upstream-sync/SKILL.md` 与 `.claude/skills/upstream-sync/SKILL.md` 均能读到；`git ls-files -s .claude/skills` 显示符号链接、`.agents/skills/*` 显示真实文件

## 2. 引用适配

- [x] 2.1 替换 `.claude/skills/...` → `.agents/skills/...`：`.agents/skills/documentation/SKILL.md`（2 处）、`.agents/skills/management/SKILL.md`（5 处，含 `SD=` 变量）、`.agents/skills/management/scripts/mgmt_io.py`（2 处注释/文档串）
- [x] 2.2 更新 `.claude/agents/README.md` 目录约定图（反映 `.agents/skills` 真实 + `.claude/skills` 符号链接 + `.claude/agents` 真实）
- [x] 2.3 全仓核对：`git grep "\.claude/skills"` 残留为 0（`.claude/agents` 引用保留属正常）

## 3. 验证与提交

- [x] 3.1 验证 `mgmt_io.py` 的 `REPO_ROOT = parents[4]` 仍指向仓库根（跑一个只读脚本，如 `list_tasks.py --help` 或直接 python 断言）
- [x] 3.2 确认 pi 项目级路径生效：`.agents/skills/` 下各 skill 的 SKILL.md 存在且可读（本会话已加载 upstream-sync，路径即 `.agents/skills/...`）
- [x] 3.3 提交：`refactor: skill 真实目录迁至 .agents/skills，.claude/skills 改为兼容符号链接`
