# port-docs-order-tool

## Why

上游有文档排序契约、却没有维护它的工具：

- `docs-page-content` 的「用 `order` 字段显式表达阅读顺序」要求文档支持 `order`，并规定排序链为 `文件夹优先级 → order → id → date 降序 → slug`；
- 但 `management/docs/` 下**没有**任何脚本或约定去维护 `order`——只能手改 frontmatter，容易写出重复值、把顺序改乱，也无从知道「两个值之间还有没有整数空位」。

下游 `digital-human` 已把这个问题解决并实际使用：`.agents/skills/documentation/scripts/docs_order.py`
（`list` 只读查看顺序/空位/重复、`insert` 默认 dry-run 且优先占用整数空位、`renumber` 规范化 10/20/30；
拒绝重复值与多条 `order:` 行、写入后校验并单文件回滚）。

按 `upstream-sync` 铁律「下游改了共享脚手架必须先 port 回上游」，本 change 把它收归上游（并去掉领域专属部分）。

## What Changes

**新增工具** `.agents/skills/documentation/scripts/docs_order.py`（取自 digital-human，做两处上游化调整）：

1. **`--author` 改为必填**：原版默认 `汤问`（作者本人）。上游是通用脚手架，不能在生成文件时硬编码某个人名；frontmatter 的 `author` 是必填项，工具不替你编造。
2. **文档串与示例路径改为上游语境**（`management/docs/<目录>`，去掉 `数字人概述` 等示例）。
   其余逻辑原样保留：排序键与 `server/routers/management.py:_doc_sort_key` 同源、默认 dry-run、写入后结构校验 + 单文件回滚、重复 `order` 拒绝（除非 `--force`）。

**技能文档补三条通用约定**（同样来自 digital-human，去掉领域专属部分）：

1. `order` 建议用 **10、20、30** 空档，便于日后在中间插入而不改他人；
2. sidecar `related` 的每一项必须是**含 `slug` 与 `title` 的对象**，不能写成字符串（与 `docs-system` 的 schema 一致，此前 Skill 未写明）；
3. 新增「交付检查」清单：章节与已审 design 一致、事实可追溯、链接/图片目标存在、sidecar JSON 合法、Mermaid 可渲染、公式用受支持定界符、`openspec validate --strict` 通过；论文笔记另跑 `article-note/scripts/validate-note.py`。

**明确不取**（领域专属）：`数字人概述/`、`技术介绍/`、`论文笔记/`、`knowledge/` 等子目录名；`tags: [digital-human]`；`--author` 的人名默认值；该 skill 重写版中「取代旧 doc-writing」的表述（上游已完成同样的合并）。

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

（无）

> `order` 的排序语义早已由 `docs-page-content` 定义；本 change 只加**维护工具**与**写作约定**，不改变任何可观察行为。
> 因此设 `skip_specs: true`。特别地：**不**为「`order` 必须唯一」加 spec 要求——后端排序并不强制唯一性，那是工具侧的输入校验，写进 spec 会造出无法被系统行为验证的假契约。

## Impact

- 技能：新增 `.agents/skills/documentation/scripts/docs_order.py`；`.agents/skills/documentation/SKILL.md` 增一节 + 两条约定 + 交付检查。
- 代码/运行时/后端：**不动**（工具只在写文档时手工调用）。
- `.claude/skills` 为符号链接，自动同步。
- 依赖：脚本只用 Python 标准库，无新依赖。
- 不写下游：本 change 只在当前仓库（ProjFlow）落地；digital-human 侧保持其自有的领域化版本。
