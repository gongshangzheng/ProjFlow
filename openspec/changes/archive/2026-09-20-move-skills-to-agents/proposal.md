# Proposal: move-skills-to-agents（skill 真实目录迁到 .agents）

## Why

pi 的项目级 skill 位置是 `.pi/skills/` 与 `.agents/skills/`；`.claude/skills/` 是 Claude Code 约定，pi 要显式配置才读。当前 ProjFlow 的 skill 真实文件在 `.claude/skills/`（38 个已入库文件），靠 `.agents → .claude` 符号链接"借壳"被 pi 发现——隐式、易被误删、与 pi 文档的原生约定不符。应把真实目录放到多 harness 通用的 `.agents/skills/`，让 Claude Code 走兼容符号链接。

## What Changes

- `.agents` 由符号链接变为**真实目录**，skill 真实文件迁至 `.agents/skills/`（10 个 skill）
- `.claude/skills` 变为指向 `../.agents/skills` 的**符号链接**（Claude Code 仍按 `.claude/skills/...` 正常读取）
- `.claude/agents/`（Claude 专用 subagent 提示词）保持真实目录不动
- 同步更新引用：`.claude/skills/...` → `.agents/skills/...`（4 个文件；`.claude/agents/...` 的引用保持不变）
- 更新 `.claude/agents/README.md` 的目录约定图，反映新布局

## Capabilities

纯仓库结构/引用调整，无 spec 级行为变更，`.openspec.yaml` 设置 `skip_specs: true`。

### New Capabilities

（无）

### Modified Capabilities

（无）

## Impact

- 结构：`.agents`（符号链接 → 真实目录）、`.claude/skills`（真实目录 → 符号链接）
- 引用更新：`.agents/skills/documentation/SKILL.md`、`.agents/skills/management/SKILL.md`、`.agents/skills/management/scripts/mgmt_io.py`、`.claude/agents/README.md`
- 不影响：skill 内容与行为、`server/`、`web/`、openspec changes
- 注意：`mgmt_io.py` 用 `parents[4]` 推导仓库根，路径深度不变（`.agents/skills/<skill>/scripts/X.py` 与原 `.claude/skills/...` 同级）
