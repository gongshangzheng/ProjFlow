# skill-latex-and-paths

## Why

`add-latex-math` 让文档正文支持 LaTeX 后，只更新了 `article-note`（写**笔记**的技能）。但**写 wiki 文档**的技能没跟上：

- `.agents/skills/documentation/SKILL.md` 专门记录渲染约定——已有「1.4 图片与图题」「3. Mermaid 图表」两节，**却完全没有公式/LaTeX 内容**（`grep 公式` 零命中）。按它现在的指引写文档，作者不知道公式该怎么写、也不知道 `\(...\)` 是不支持的。
- `.agents/skills/documentation/references/mermaid-cheatsheet.md` 是 Mermaid 速查，但**没有提**「节点标签里可以用 `$$...$$` 写公式」——而这是刚验证过的可用能力（且依赖我们引入的 KaTeX 样式）。

顺带发现一处与仓库契约直接冲突的表述：

- `.agents/skills/doc-writing/SKILL.md:37` 写「文档放 `docs/` 对应子目录（科研文档 `docs/research/`）」，而 `documentation` spec 明确「仓库说明性文档统一置于 `management/docs/`；仓库根目录 MUST NOT 存在 `docs/`」。

## What Changes

- `documentation/SKILL.md`：新增 `### 1.5 公式（LaTeX）`，与 1.4 图片同风格，写清：写法（`$...$` / `$$...$$`）、必须配符号表与中文解释、不支持的写法（`\(...\)`、`\[...\]`、`\begin{equation}`）、空白与美元符号边界、Mermaid 内需用 `$$`。
- `documentation/references/mermaid-cheatsheet.md`：在「1. 通用规则」补一条图内公式写法（`$$...$$`，单 `$` 不渲染）。
- `doc-writing/SKILL.md`：把文档落点由 `docs/` 改为 `management/docs/`，并注明根目录不设 `docs/`。

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

（无）

> 本 change 只改技能文档的**内容表述**，不改变任何行为契约——LaTeX 渲染契约已由 `add-latex-math` 写入 `docs-page-content`。
> 因此设 `skip_specs: true`。

## Impact

- 技能文档：`.agents/skills/documentation/SKILL.md`、`.agents/skills/documentation/references/mermaid-cheatsheet.md`、`.agents/skills/doc-writing/SKILL.md`。
- 代码与运行时：**不动**。
- `.claude/skills` 是指向 `.agents/skills` 的符号链接，自动同步，无需改动。
- **不在范围**：`doc-writing/SKILL.md` 里带有医学/临床领域的表述（「医学背景、文献」「临床合作者」），与 ProjFlow 无关——疑似从别的项目带入的技能。本 change 只修其中与仓库契约冲突的**路径**表述，是否重写该技能由用户决定。
