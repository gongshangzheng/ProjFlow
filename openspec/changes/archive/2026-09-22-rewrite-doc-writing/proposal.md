# rewrite-doc-writing

## Why

`.agents/skills/doc-writing/SKILL.md` 内容与这个仓库**不匹配**：

| 问题 | 证据 |
|------|------|
| 领域错位 | 写着「医学背景、文献」「导师或临床合作者」——ProjFlow 是项目管理平台，与临床无关，该文件疑似从别的项目带入 |
| 路径错误 | 「文档放 `docs/` 对应子目录（科研文档 `docs/research/`）」——`documentation` spec 明确「说明性文档统一置于 `management/docs/`；根目录 MUST NOT 存在 `docs/`」 |
| 与 `documentation` 职责重叠、触发词撞车 | 两者都讲「写文档要先走 OpenSpec」；`documentation` 的 description 是「创建/修改 Wiki 文档」，本 skill 的触发词是「写文档」——同一个请求会命中两个 skill，路由不确定 |
| 未反映仓库既有机制 | 不提 `openspec/registry.md` 登记表、不提 `docs-<slug>` 单篇 change 命名、不提 sidecar |

同时 `documentation/SKILL.md` 里有一处**过期**：`§1.1` 的表格把「总 Change」写成 `docs-system`，而该 change 已归档、登记表已迁到 `openspec/registry.md`（`promote-docs-registry`）。

## What Changes

**重写 `doc-writing/SKILL.md`**（本库的文档写作流程门禁）：

- 去掉全部领域（医学/临床）内容与错误路径。
- 明确**适用范围**与**豁免**：结构级变更走 change；错字/数字/单段论证/链接属内容级小修可直接改（commit 说明）。
- 固化**门禁四步**：判断是否结构级 → 建 change → 在 `design.md` 写清目标读者/章节结构/每节要表达什么/引用关系/待调研内容 → 用户审核通过后才动笔。
- 写清**落点与登记**：wiki `management/docs/<slug>.md` + 同名 `.json` sidecar，且**先登记 `openspec/registry.md`**；其它文档放相应子路径（仓库根目录不设 `docs/`）。
- 写清**与其它 skill 的分工**：`documentation` 管「内容怎么写」，`management` 管 CRUD 脚本，本 skill 管「什么时候可以动笔、动笔前必须产出什么」。
- 收窄 description/触发词，与 `documentation` 不重叠。

**修订 `documentation/SKILL.md`**：

- `§1.1` 的「总 Change `docs-system`」→ 改为「登记表 `openspec/registry.md`（登记动作直接编辑它；只有体系级规则变更才开 change）」。
- 顶部补一行与 `doc-writing` 的分工说明。
- description 触发词收窄为「内容规范」类，不再与「写文档」撞车。

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

（无）

> 纯技能文档重写，不涉及行为契约（LaTeX 等渲染契约已分别落在 `docs-math` / `docs-page-content`），故设 `skip_specs: true`。

## Impact

- 技能：`.agents/skills/doc-writing/SKILL.md`（重写）、`.agents/skills/documentation/SKILL.md`（两处修订 + description）。
- `.claude/skills` 为符号链接，自动同步。
- 代码/运行时：**不动**。
- **遗留待决**：本库现有两个文档相关 skill，边界靠本次分工表述维持。若希望只保留一个（把 `documentation` 的内容规范并入 `doc-writing`，或反之），属独立决策，不在本 change 内擅自合并。
