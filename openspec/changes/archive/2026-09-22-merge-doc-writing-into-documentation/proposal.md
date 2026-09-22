# merge-doc-writing-into-documentation

## Why

本库有**两个**文档写作 skill，靠「分工表述 + 触发词收窄」勉强不打架：

| skill | 行数 | 定位 |
|---|---|---|
| `documentation` | 315（+ `references/mermaid-cheatsheet.md`） | 内容规范（结构模板 / 链接 / 图片 / 公式 / Mermaid / 风格 / 会议纪要） |
| `doc-writing` | 76 | 流程门禁（何时可动笔、动笔前产出什么） |

并存的代价在本会话中已经反复显现：

1. **表述漂移**——`documentation` 的 §1.1 把「总 Change」写成已归档的 `docs-system`；`doc-writing` 则带着医学领域表述与错误的 `docs/` 路径（与 `documentation` spec 直接冲突）。
2. **触发撞车**——同一句「帮我写一篇文档」会命中两者，路由不确定；只能靠描述里互相指路缓解。
3. **职责本就重叠**——`documentation` 的 §1「文档变更的 OpenSpec 双层流程」已经把门禁讲了一大半；`doc-writing` 只多出「design 五要素」与「落点与登记」。

也就是说：**同一件事写在两处**。合并为一个 skill 才能根治。

## What Changes

- 把 `doc-writing` 的独有内容并入 `documentation`（§1 门禁相关小节）：
  - §1.2 的 design 要素补全为五要素（目标读者 / 章节结构 / 每节表达什么 / 与其它文档的引用关系 / 待调研知识点）
  - §1.3 补两条纪律：不编造领域背景（需调研的写进 design）；wiki 文档**先登记 `openspec/registry.md` 再动笔**
  - §2.1 文件规范补：**仓库根目录不设 `docs/`**，wiki 文档必须落 `management/docs/`
- `documentation` 的 description 合并两者的触发面（写文档 / 结构调整 / 内容规范 / 模板格式），并删除全部指向 `doc-writing` 的说明。
- 删除 `.agents/skills/doc-writing/`（内容已无独有部分）。
- `management/SKILL.md` 已指向 `documentation`，无需改动（本次确认）。

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

（无）

> 纯技能文档的合并与删除，不涉及行为契约，故 `skip_specs: true`。

## Impact

- 技能：`.agents/skills/documentation/SKILL.md`（合并门禁内容 + description + 去除交叉引用）；**删除** `.agents/skills/doc-writing/`。
- `.claude/skills` 为符号链接到 `.agents/skills`，自动同步（`doc-writing` 随之消失，无需单独处理）。
- 代码/运行时：**不动**。
- 迁移：`doc-writing` 的触发词（写文档 / 新增文档 / 文档大改 / 落点与登记）全部并入 `documentation` 的 description，功能不丢。
- 注意：删除 skill 是**不可逆的可见变化**（用户若习惯 `/doc-writing`，需改用它名）；因此 description 里把两类触发词都写全，保证按任一说法都能命中。
