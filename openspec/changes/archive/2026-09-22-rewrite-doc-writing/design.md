## Context

- 现有两个文档相关 skill：
  - `documentation`（312 行）：内容规范全量（OpenSpec 双层流程、wiki 文件规范、标准结构、内部链接、图片与图题、公式、Mermaid、风格、会议纪要、模板 + `references/mermaid-cheatsheet.md`）。
  - `doc-writing`（40 行）：只有「OpenSpec 先行」+ 医学领域表述 + 错误路径 `docs/`。
- `documentation` 的 description 触发场景含「创建/修改 Wiki 文档」；`doc-writing` 触发词含「写文档 / 创建文档」→ **同一请求会命中两个 skill**。
- `documentation` §1.1 引用的「总 Change `docs-system`」已归档；登记表现位于 `openspec/registry.md`（`promote-docs-registry`）。
- `documentation/SKILL.md`（1.5 公式节）与 `doc-writing` 都属共享脚手架技能。

## Goals / Non-Goals

**Goals:**

- `doc-writing` 成为本库**可用的流程门禁**：无领域错位、路径正确、与仓库既有机制（登记表、单篇 change 命名、sidecar）一致。
- 两个 skill 的**触发边界不重叠**，任一请求只会命中一个。
- 修掉 `documentation` 里过期的「总 Change」表述。

**Non-Goals:**

- 不合并两个 skill（是否需要合并是用户的决策，见 proposal 的「遗留待决」）。
- 不改 `documentation` 的内容规范本身（除 §1.1 过期表述与 description/分工说明）。
- 不改 `management` skill 的 CRUD 脚本。
- 不改任何代码。

## Decisions

### D1: `doc-writing` = 流程门禁；`documentation` = 内容规范

| 维度 | `doc-writing` | `documentation` |
|------|---------------|-----------------|
| 回答的问题 | **什么时候可以动笔、动笔前必须产出什么** | **内容怎么写**（结构/链接/图片/公式/Mermaid/风格） |
| 形态 | 短小、判定条件与禁止项 | 全量速查与模板 |
| 触发词 | 写文档 / 新增文档 / 文档大改 / 结构变更前置 | 内容规范 / 结构模板 / Mermaid / 内部链接 / 图片图题 / 公式 / 风格 |

- 理由：两个 skill 若都讲「怎么写」，必然漂移；按「流程 vs 内容」切分后，各自只需维护自己的权威内容，并互相指路。
- 备选：把门禁并入 `documentation` 并删除 `doc-writing` —— 触发重叠消失，但用户明确要求保留并重写 `doc-writing`；本 change 按用户要求做，合并作为遗留选项上报。

### D2: `doc-writing` 不重复抄写细则，改为指路

门禁四步在本 skill 里是**判定清单**；章节结构模板、图片规范、公式写法等一律不在本 skill 复制，而是指向 `documentation` 的对应小节。

- 理由：细则重复 = 两处维护 = 必然不一致（本次要修的正是这种病）。
- 例外：**落点与登记**这一张表在本 skill 内写全（`management/docs/` + `openspec/registry.md` + 根目录不设 `docs/`），因为它是「动笔前必须确认」的事项，属门禁范畴。

### D3: 保留「豁免」清单，并给出可判定的标准

沿用原 skill 的豁免思路，但把判断标准写成可操作的一句话：**读者是否需要重新理解文档结构？** 需要 → 走 change；不需要 → 直接改但要写清 commit message。

- 理由：没有明确标准时，作者会以「这是小修」绕过流程。

### D4: 修正 `documentation` 的两个点，且最小改动

1. §1.1 表格：`docs-system` → `openspec/registry.md`（`docs-system` 已归档；登记动作 = 直接编辑登记表；体系级规则变更才开 change）。
2. 顶部补一行分工说明 + description 触发词收窄。

- 理由：这两处是**事实性错误/职责冲突**，不修会让门禁指错地方；其余内容保持不动以控制改动面。

## Risks / Trade-offs

- [重写后 `doc-writing` 与 `documentation` 仍可能被同时加载] → 靠 description 触发词收窄 + 各自身份说明降低歧义；彻底消除需合并（遗留项）。
- [删掉原 skill 的全部旧文本，可能丢掉有用的东西] → 原 40 行里的「OpenSpec 先行」思路保留并强化；医学/临床内容与 `docs/` 路径是明确的错误，删除即是修复；重写内容以仓库既有机制（`registry.md`、`docs-<slug>`、sidecar）为准。
- [`documentation` §1.1 改动牵涉它的示例与模板] → 只改表格那一行与顶部说明，不动 §1.2/§1.3 的流程细则（那些仍有效）。

## Migration Plan

1. 重写 `.agents/skills/doc-writing/SKILL.md`。
2. 修订 `.agents/skills/documentation/SKILL.md`（§1.1 一行 + 顶部一行 + description）。
3. 验证：两文件 description 触发词无交集；`grep -rn "clinical\|临床\|医学\|docs/research" .agents/skills/` 无命中；`.claude/skills` 读到的内容与 `.agents/skills` 一致；`openspec validate --all --strict` 通过。
4. 提交（`[shared]`）并归档。
