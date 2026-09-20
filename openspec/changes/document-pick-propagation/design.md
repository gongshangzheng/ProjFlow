# Design: document-pick-propagation

## Context

见 proposal.md — Why。实证来源：2026-09-20 会话（ProjFlow 上游 pick pet 下游 cb76c36 + bafbe23，commits bd91ac2 / aacb342）。SKILL.md 现有结构：拓扑 → 责任分工铁律 → 传播工作流（下游同步上游 / 部分文件 / port 回上游）→ 反模式。

## Goals / Non-Goals

**Goals:**

- 双向传播都有可直接照抄的命令级流程；"下游→上游"从半句话变完整小节
- 把今天踩过的 4 个坑固化成注意事项，不依赖记忆

**Non-Goals:**

- 不写成脚本/CLI（路径、SHA、冲突因次而异，流程文档足够）
- 不覆盖 fork 初始化流程（那是 `fork-init-guide` change 的事）
- 不改 AGENTS.md 正文结构（只加一行指向）

## Decisions

### D1: 更新位置——扩写 SKILL.md 现有「port 回上游」小节，不新增章节

该小节已存在且方向正确，只是不完整；同位置扩写保持单一权威。命令块 + 冲突分类表 + 注意事项三段式。

### D2: 冲突/文件按"归属"分类处理，写入速查表

| 文件类型 | 解法 | 今日实例 |
|---------|------|---------|
| 共享脚手架文件 | 取 theirs（无冲突则自动套上） | `DocPage.vue`、`markdown.js` |
| 领域数据（下游的 docs/data/results） | `git rm`，不进上游 | `architecture.md/.json` |
| 下游的 openspec change 勾选 | 取 ours，事后在本库对应 change 里手动勾选并注明 pick 来源 | `docs-system/tasks.md` |
| 冲突的 import 块 | 只留下游代码实际用到的 import | 只取 `import json`，弃 datetime/hashlib/subprocess |

### D3: 疑问注释改为实证结论

第 84 行 `# 下游 SHA 在上游重写后可见吗?——` → 改为：可见可用。嫁接重写的是下游自身的 commit SHA；在上游 `git fetch <下游路径> main` 后对象与 SHA 直接可用（实证：bafbe23、cb76c36 零障碍 pick）。

### D4: AGENTS.md 只加一行

开发规范 Git 工作流小节末尾加："跨库共享改进传播（cherry-pick 双向操作与冲突分类）见 `.agents/skills/upstream-sync/SKILL.md`"。

## Risks / Trade-offs

- [skill 与实际操作漂移] → 小节末尾注明实证 commit（bd91ac2/aacb342）与日期，后续操作后顺手核对
- [skill 会镜像到下游，下游视角读起来方向反了] → 小节标题明确"上游侧操作"，下游视角沿用既有"下游同步上游"小节

## Migration Plan

纯文档，落地即生效，可 revert。

## Open Questions

（无）
