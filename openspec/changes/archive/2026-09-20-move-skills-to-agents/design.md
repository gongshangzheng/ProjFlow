# Design: move-skills-to-agents

## Context

见 proposal.md — Why。现状：`.agents` 是 git 跟踪的符号链接（mode 120000）→ `.claude`；真实内容 `.claude/skills/`（10 skill）+ `.claude/agents/`（2 文件）。pi 文档规定项目级位置为 `.pi/skills/` 与 `.agents/skills/`。

## Goals / Non-Goals

**Goals:**

- `.agents/skills/` 成为 skill 的真实物理位置，pi 无需配置即原生发现
- Claude Code 兼容性零损失（`.claude/skills/...` 路径照常可读）
- 引用与目录约定文档同步，无悬空路径

**Non-Goals:**

- 不动 `.claude/agents/`（Claude 专用 subagent 提示词，无 pi 对应物）
- 不引入 `.pi/settings.json`（`.agents` 原生路径已足够，少一层配置）
- 不改任何 skill 的内容语义（仅路径字符串）

## Decisions

### D1: 只交换 `skills/` 子目录，不整目录对调

- 备选：`.claude` ↔ `.agents` 整目录交换（`.claude` 变符号链接）。放弃原因：`.claude/agents/` 是 Claude Code 专用资产，被裹进 `.agents/` 后语义混乱（`.agents/agents/`）
- 选定：`.agents/skills/` 真实 + `.claude/skills` → `../.agents/skills` 符号链接，各自保留最合适的物理归属

### D2: 符号链接方向固定为 `.claude` → `.agents`

- 多 harness 通用目录（`.agents`）作为真实源，harness 专属目录（`.claude`）作为兼容入口
- 若将来接入 Codex 等，同样只需其专属目录指向 `.agents/skills`

### D3: 引用更新以 `.claude/skills` 为唯一替换目标

- 替换范围：`.claude/skills/...` → `.agents/skills/...`（4 文件 6 处）
- `.claude/agents/...` 引用**保持**（该目录仍真实存在）
- 顺带更新 `.claude/agents/README.md` 的目录树示意，避免文档与实际布局漂移

### D4: 路径深度不变，`parents[4]` 无需改

`.agents/skills/management/scripts/mgmt_io.py` 与 `.claude/skills/management/scripts/mgmt_io.py` 到仓库根深度相同（scripts → management → skills → .agents → root），故仅注释文案需改，推导逻辑不动。

## Risks / Trade-offs

- [符号链接在 Windows / 部分 CI 检出异常] → 与现状同类风险（原本 `.agents` 就是符号链接），未新增；文档中说明两路径等价
- [引用漏改导致 skill 内路径失效] → tasks 含全仓 grep 核对（`.claude/skills` 残留必须为 0）
- [兄弟库仍用 `.agents → .claude` 旧布局，四库不一致] → 记入 forks；后续可在各下游按同一 change 适配（`move-skills-to-agents` 属共享脚手架层，可 cherry-pick）

## Migration Plan

一次提交内完成：删符号链接 → 建真实目录 → `git mv` skills → 建反向符号链接 → 改引用。回滚 = revert 该提交。无运行时影响（前后端服务不需重启，skill 为 agent 侧资产）。

## Open Questions

（无）
