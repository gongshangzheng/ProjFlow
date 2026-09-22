## MODIFIED Requirements

### Requirement: 公式的表达约束

本库 MarkdownRenderer 支持 LaTeX 数学公式（`$...$` 行内、`$$...$$` 块级），skill SHALL 直接使用 LaTeX 书写核心公式，并 SHALL 为公式配套符号表与中文解释；MUST NOT 再要求把公式写成代码块。

#### Scenario: 表达核心公式
- **WHEN** 笔记需要呈现论文核心公式
- **THEN** 公式以 LaTeX 给出（行内 `$...$` / 块级 `$$...$$`），并配套符号表（符号/含义/取值）与自然语言解释

#### Scenario: 公式与符号表对应
- **WHEN** 正文给出一个多符号公式
- **THEN** 紧随其后提供符号表，逐个说明式中符号的含义

#### Scenario: 保留原式作为备查
- **WHEN** 公式在源论文中有特定记号或排版细节需要保真
- **THEN** 可在渲染公式之外附带代码块保留原式，作为可复制的备查形式（可选，不再强制）
