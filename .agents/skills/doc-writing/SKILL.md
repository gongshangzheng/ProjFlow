---
name: doc-writing
description: |
  文档写作的流程门禁：写任何文档正文之前，先判断是否结构级变更、开 OpenSpec change、在 design.md 写清结构与目标读者、经用户审核后才动笔。
  触发场景：(1) 要写/新增一篇文档，(2) 文档大改或结构调整，(3) 不确定某次文档改动是否需要开 change，(4) 需要文档落点与登记规则。
  注：文档**内容怎么写**（结构模板、链接、图片、公式、Mermaid、风格）见 documentation skill。
---

# 文档写作流程门禁

本 skill 只回答一件事：**什么时候可以开始写、动笔前必须产出什么。**

内容规范（章节模板、内部链接、图片与图题、LaTeX 公式、Mermaid、写作风格、会议纪要格式）见 `.agents/skills/documentation/SKILL.md`。

## 先判定：这次改动要不要开 change

**判断标准（唯一）**：读者是否需要**重新理解文档结构**？

| 情形 | 处理 |
|------|------|
| 章节增删 / 移动 / 重编号 / 内容定位变化 / 新增一篇 / 废弃一篇 | **结构级** → 必须先开 change |
| 错字、更新一个数字、补一小段论证、修一处链接、换一张图 | **内容级小修** → 直接改 |

结构级不写 design 直接动笔，是返工成本最高的一种错。

## 结构级变更的四步

1. **开 change**
   - wiki 文档：`docs-<slug>`（如 `docs-api-design-conventions`）
   - 其它文档：change 名体现主题（如 `research-core-docs`）
   - 建 change：`openspec new change <name>`
2. **在 `design.md` 写清五件事**（缺一不可）
   - 目标读者（自己回顾 / 团队协作 / 外部评审）
   - 完整章节结构，到二级标题
   - 每一节要表达什么、论证什么、下什么结论
   - 与其它文档的引用关系（谁引用谁、边界在哪）
   - 需要外部调研的知识点（列出来，不许凭空写）
3. **等用户审核通过**该 design
4. **之后才动笔写正文**，并按 `tasks.md` 勾进度；大改完成后通读全文 + grep 悬空引用

## 落点与登记

| 文档类型 | 落点 | 是否登记 |
|---|---|---|
| wiki 文档 | `management/docs/<slug>.md` + 同名 `<slug>.json` sidecar | **必须先改 `openspec/registry.md`**（加/改一行），再动正文 |
| 其它说明性文档 | 相应子路径（如 `papers/docs/`、`evaluation/docs/`） | 不需登记 |
| 任何情况 | **仓库根目录不设 `docs/`** | — |

- 登记表 `openspec/registry.md` 是「新增 / 废弃 / 职责归属」的唯一权威；增删改一行**不需要**开 change，直接编辑即可。
- wiki 文档元数据（`changelog` / `progress` / `appendix` / `related`）写在 sidecar json，**不写进正文**。

## 不要做的事

- ❌ 不写 design 直接改正文（结构级）
- ❌ 凭记忆改局部 —— 动手前必须通读目标文档全文
- ❌ 改编号却不级联重映射引用（改完做「引用 → 标题存在」核对，悬空必须为 0）
- ❌ 正文里写「术语修正」「之前写错了」这类历史信息（演进记录归 sidecar）
- ❌ 编造领域背景/文献；需要调研的写在 design 的调研清单里

## 与其它 skill 的分工

| skill | 管什么 |
|---|---|
| **doc-writing**（本 skill） | 什么时候可以动笔、动笔前必须产出什么、文档放哪、要不要登记 |
| `documentation` | 内容怎么写：结构模板、内部链接、图片与图题、LaTeX 公式、Mermaid、写作风格、会议纪要格式 |
| `management` | 文档的 CRUD 脚本（`create_doc.py` / `update_doc.py` 等） |
