## Context

见[提案](proposal.md)。旧手册与兼容脚本同目录，但脚本路径是既有接口，技能名称不是脚本路径的一部分。

## Goals / Non-Goals

- 全局 `remote-ops` 保留原名；项目运行手册使用 `remote-runtime`。
- 不动脚本内容、现有授权检查、服务器配置或项目数据。此次不合并其他技能迁移。

## Decisions

### 保留旧脚本目录

只将 `.agents/skills/remote-ops/SKILL.md` 移到 `.agents/skills/remote-runtime/SKILL.md`，并修改注册名。`.agents/skills/remote-ops/scripts/` 保持原样。更新 `.agents/skills/experiment/SKILL.md` 的语义引用，在 `.agents/skills/upstream-sync/SKILL.md` 说明下游采用规则。兼容 `.claude/skills` 仍解析到同一目录，不复制实现。

### 发布以目标远端的基线为准

ProjFlow 的发布分支从自身 `origin/main` 建立，确认只含改名补丁；不推本地 `main` 的其他提交。pet 已有独立 change；其本地基线较远端前进较多，须按远端现有的技能和测试结构移植和验证，不能直接发布本地 HEAD。live2d-avatar 只有过期引用，不复制手册；没有项目适配的后代不增同名入口。各仓发布产物互不覆盖，但先定上游约定，再移植下游；本仓验收和发布不并行。

## Risks / Trade-offs

- 旧脚本目录仍叫 `remote-ops`，但无 `SKILL.md`。明确这是兼容路径，避免工具将目录名误当作技能注册名。
- macOS 不覆盖 Linux 守卫的完整契约。此次脚本不变，只检查内容、路径和 Shell 语法，不将完整 Linux 套件作为推送条件。
