## Context

- `add-latex-math`（已归档）使 `MarkdownRenderer` 渲染 `$...$` / `$$...$$`，契约写在 `openspec/specs/docs-page-content/spec.md`。
- 该 change 只更新了 `.agents/skills/article-note/`（笔记技能）的 4 个文件。
- `.agents/skills/documentation/SKILL.md` 是「写 wiki 文档」的指南，已按渲染能力分节：`1.4 图片与图题`、`3. Mermaid 图表`；**没有公式节**。
- `.agents/skills/documentation/references/mermaid-cheatsheet.md` 有 8 节（通用规则 / flowchart / sequenceDiagram / graph / gantt / classDiagram / 常用图例 / 调试技巧），无数学内容。
- `.claude/skills` → `../.agents/skills` 符号链接；`.pi/skills` 不存在（AGENTS.md 的约定），故只需改 `.agents/skills/`。
- 实测事实（来自 `add-latex-math` 的验证，作为写作依据）：
  - `$...$` 行内、`$$...$$` 块级、表格单元格内均渲染
  - `\(...\)` / `\[...\]` 不支持（反斜杠被 markdown-it 转义吃掉）
  - 公式内容首尾不能是空白；`$5 到 $10` 保持字面
  - Mermaid 节点标签内 `$$...$$` 渲染为 KaTeX，单 `$` 不渲染

## Goals / Non-Goals

**Goals:**

- 写 wiki 文档的人（含 AI）能在 `documentation` 技能里一处读到公式写法与全部边界。
- Mermaid 速查里能查到图内公式写法。
- 修掉 `doc-writing` 中与 `documentation` spec 冲突的文档落点表述。

**Non-Goals:**

- 不改渲染实现与契约（已由 `add-latex-math` 完成）。
- 不重写 `doc-writing` 的医学/临床领域表述（另议，见 proposal 的 Impact）。
- 不动 `.claude/skills`（符号链接）与 `article-note`（已更新）。

## Decisions

### D1: 在 `documentation/SKILL.md` 新增 `### 1.5 公式（LaTeX）`，位置紧跟 1.4 图片

- 理由：该技能的结构是「按渲染能力分小节」（1.4 图片、§3 Mermaid），公式是同类内容；放在 1.4 之后、`## 3. Mermaid` 之前，读者按顺序浏览渲染能力时不会漏。
- 写法沿用 1.4 的组织：给可复制的 Markdown 片段 → 约束列表 → 安全/边界说明。

### D2: 边界用「不要/会怎样」的句式明确列出

不写「建议」而写「不要 `\(...\)`（反斜杠会被 markdown-it 转义吃掉，渲染成 `(...)`）」——因为这是**已经验证过的错误行为**，写清后果才能防住。

- 覆盖 4 条：不支持的定界符、`\begin{equation}`、内容首尾空白、紧邻数字的 `$`。

### D3: Mermaid 速查补在 `## 1. 通用规则`，不新开一节

图内公式是「通用规则」级的一行知识点（不是某类图的专属语法），且速查已有 8 节，再加节会稀释结构。

- 内容：`$$...$$` 写在节点标签里 → 渲染为 KaTeX；单 `$` 不渲染；样式由本仓库加载的 KaTeX CSS 提供。

### D4: `doc-writing` 只改路径一行，并留痕

`doc-writing/SKILL.md:37` 的 `docs/` 与 `documentation` spec 冲突，改为 `management/docs/` 并补一句「根目录不设 `docs/`」。

- 理由：这是客观冲突，会让 AI 写出错误落点。
- 该文件其余带医学/临床色彩的表述**保持不动**并上报：它疑似从别的项目带入，是否属于本仓库需要用户判断，本 change 不擅自重写。

## Risks / Trade-offs

- [技能文档与实现再次脱节（例如将来改成不渲染 `$...$`）] → 本次把边界逐条写清，并在 `documentation/SKILL.md` 的公式节里注明契约来源（`docs-page-content`）：改实现时容易顺藤改文档。
- [在 skill 里写 `$...$` 示例，可能被误读成需要转义] → 示例放在 fenced markdown 代码块内，与 1.4 图片示例同款处理。
- [改 `doc-writing` 可能触及非本仓库的意图] → 只改客观冲突的路径一行，领域表述原样保留并上报。

## Migration Plan

1. 改 3 个技能文件。
2. 验证：`grep -n "公式" documentation/SKILL.md` 命中新增节；`grep -n "docs/" doc-writing/SKILL.md` 不再出现根目录 `docs/`；`.claude/skills` 符号链接仍指向 `.agents/skills`（读到的内容一致）。
3. 无代码/运行时影响，无需部署验证；提交后 Pages 会照常重建（内容不变）。
4. 回滚：revert 提交。
