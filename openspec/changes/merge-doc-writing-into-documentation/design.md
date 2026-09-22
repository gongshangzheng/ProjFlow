## Context

- `documentation/SKILL.md`（315 行）结构：`§1 文档变更的 OpenSpec 双层流程`（1.1 双层 Change 结构 / 1.2 写正文前的硬性顺序 / 1.3 结构变更纪律 / 1.4 正文零历史信息 / 1.5 章节归属）、`§2 Wiki 文档`（1.1 文件规范 / 1.2 标准结构 / 1.3 内部链接 / 1.4 图片与图题 / 1.5 公式）、`§3 Mermaid`、`§4 写作风格`、`§5 会议纪要`、`§6 模板`，另有 `references/mermaid-cheatsheet.md`。
- `doc-writing/SKILL.md`（76 行，本会话刚重写）结构：适用范围与豁免 / 门禁四步 / 落点与登记 / 不要做的事 / 与其它 skill 的分工。
- 外部引用：`management/SKILL.md:324` 已指向 `documentation`；没有任何外部文件引用 `doc-writing`（只有两个 skill 互相指）。
- `documentation` §1.1 的表格已在 `rewrite-doc-writing` 中改为「登记表 `openspec/registry.md`」。
- 该 skill 内部的编号本来就重复（`§1` 下有 1.1–1.5，`§2` 下又有一套 1.1–1.5），本次**不顺手重排编号**（避免无关 churn 与引用风险）。

## Goals / Non-Goals

**Goals:**

- 只保留一个文档写作 skill，触发面覆盖两者的全部说法。
- 门禁的**独有**内容（design 五要素、落点与登记表）不丢。
- 消除「同一件事写在两处」的漂移源。

**Non-Goals:**

- 不重排 `documentation` 的既有编号体系（另有独立价值，但属风险不等的改动）。
- 不改代码、不改 spec、不改 `management` skill。
- 不重写 `documentation` 的既有内容规范（除合并门禁所必需的增补）。

## Decisions

### D1: 保留 `documentation`，删除 `doc-writing`

依据：

1. `management/SKILL.md` 已引用 `documentation`；删除它需要改更多引用。
2. `references/mermaid-cheatsheet.md` 挂在 `documentation` 下；保留它则无需搬目录。
3. 内容体量在 `documentation`（315 vs 76），合并是「把小并进大」。

- 备选：保留 `doc-writing` 名字、把 `documentation` 内容搬过去 —— 需要改 `management` 的引用 + 移动 `references/`，收益只是名字更好听；且用户先前误以为 `doc-writing` 是唯一 skill，正说明该名字的认知负担，不采用。

### D2: 门禁内容并入 `§1`，而不是新开一节

`§1` 已经是「文档变更的 OpenSpec 双层流程」——门禁与它是同一件事。补进 1.2（design 五要素）与 1.3（两条纪律），避免再造一个平行章节。

- 理由：合并的目的是**减少**平行结构；新开一节等于把漂移风险原样搬进来。

### D3: 落点与登记拆两处写，各归其位

- 「**仓库根目录不设 `docs/`**」→ 写进 `§2.1 文件规范`（它就在讲存放位置）。
- 「wiki 文档**先登记 `openspec/registry.md` 再动笔**」→ 写进 `§1.3 结构变更纪律`（它是动笔前的门禁动作）。

- 理由：按「内容规范」与「流程门禁」的归属放置，而不是把一张表整体塞进某一节。

### D4: description 合并两类触发词，且不再互指

新 description 同时覆盖「写/新增文档、结构调整、不确定是否要开 change」与「内容规范、模板格式、Mermaid、链接/图片/公式、风格」，并删掉原先的「见 doc-writing skill」指路句。

- 理由：删掉一个 skill 后，用户按旧说法（「写文档」）也必须能命中；互指句在新结构下已无对象。

### D5: 删除 `doc-writing` 目录，并核对 `.claude/skills`

`.claude/skills` 是符号链接，删除后自动消失；验证时确认没有残留悬空引用（`grep -rn "doc-writing"`）。

## Risks / Trade-offs

- [用户习惯用 `/doc-writing`] → description 写全两类触发词，按「写文档」「新增文档」等说法仍命中 `documentation`；skill 名变化属可接受的可见变化（已在 proposal 声明）。
- [合并时漏掉 `doc-writing` 的某条约束] → 用清单核对：范围与豁免、门禁四步、design 五要素、落点与登记、不要做的事（5 条）——逐条对应到 `documentation` 的目标小节，合并后逐条 grep 确认存在。
- [误删 `documentation` 的既有内容] → 只做**插入与替换**（description、1.2 步骤、1.3 追加两条、2.1 追加一条、删两处交叉引用），不做整段重写；用行数变化核对（应增加而非减少，除删除的两处指路句）。
- [`.claude/skills` 若万一不是符号链接] → 验证步骤里显式检查，若是实体目录则同步删除。

## Migration Plan

1. 改 `documentation/SKILL.md`（description / §1.2 / §1.3 / §2.1 / 删两处交叉引用）。
2. 删除 `.agents/skills/doc-writing/`。
3. 验证：`grep -rn "doc-writing" .agents/skills/ AGENTS.md README.md` 无命中；`documentation` 的 description 含两类触发词；`§1.2/1.3/2.1` 增补内容存在；`.claude/skills/doc-writing` 不存在；`openspec validate --all --strict` 通过。
4. 提交（`[shared]`）并归档。
5. 回滚：revert 提交即可恢复 `doc-writing` 目录与 `documentation` 原文。
