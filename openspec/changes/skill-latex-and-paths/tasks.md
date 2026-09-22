## 1. documentation 技能补公式节

- [x] 1.1 `documentation/SKILL.md`：在 `### 1.4 图片与图题` 之后、`## 3. Mermaid 图表` 之前插入 `### 1.5 公式（LaTeX）`
- [x] 1.2 内容包含：可复制的行内/块级示例、必须配符号表与中文解释、不支持的定界符（`\(...\)` / `\[...\]` / `\begin{equation}`）及后果、内容首尾空白与紧邻数字的 `$` 边界、Mermaid 内需用 `$$`
- [x] 1.3 节内注明契约来源（`openspec/specs/docs-page-content/spec.md`），便于将来同步

## 2. Mermaid 速查补图内公式

- [x] 2.1 `documentation/references/mermaid-cheatsheet.md`：在 `## 1. 通用规则` 增加图内公式写法（`$$...$$` 渲染为 KaTeX、单 `$` 不渲染、样式由本仓库的 KaTeX CSS 提供）

## 3. doc-writing 路径修正

- [x] 3.1 `doc-writing/SKILL.md`：文档落点 `docs/` → `management/docs/`，并注明「根目录不设 `docs/`」
- [x] 3.2 保留其余（医学/临床）表述不动，并在回报中说明该技能疑似来自其它项目

## 4. 验证

- [x] 4.1 `grep -n "公式" .agents/skills/documentation/SKILL.md` 命中新增节，且四个边界条目齐全
- [x] 4.2 `grep -rn "docs/research\|文档放 \`docs/\`" .agents/skills/` 无命中
- [x] 4.3 `.claude/skills` 仍为符号链接，读到的 `documentation/SKILL.md` 与 `.agents/skills/` 一致
- [x] 4.4 `openspec validate skill-latex-and-paths` 通过
- [x] 4.5 工作区无其它意外改动

## 5. 收尾

- [x] 5.1 提交并 push（`[shared]`；技能属共享脚手架）
- [x] 5.2 归档
