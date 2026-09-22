# add-latex-math

## Why

文档正文**目前完全不支持 LaTeX**（实测）：

| 写法 | 现状 |
|------|------|
| `$E = mc^2$` | 当字面文本原样显示 |
| `\(a^2+b^2=c^2\)` | 反斜杠被 markdown-it 的转义吃掉 → 显示成 `(a^2+b^2=c^2)`（比上一条更容易误读） |
| `$$\frac{...}{...}$$` | 当普通段落文本 |
| 表格内 `$\theta$` | 字面 `$\theta$` |

浏览器侧 `document.querySelector('.katex')` 为 `null`——一个 KaTeX 节点都没有。产物里那个 `katex-*.js` chunk 是 **mermaid 的传递依赖**（mermaid 渲染 `$$` 数学图时才懒加载），容易让人误判为已支持。

后果：论文精读笔记、需要公式的设计文档只能写「代码块 + 符号表」。`article-note` 的 spec 甚至把这条写成了硬约束：

> 因本库 MarkdownRenderer 不渲染 LaTeX，skill SHALL 把公式写成代码块保留原式。

对以公式为核心内容的笔记来说，这个折中损失很大（公式无法阅读、无法引用、无法与符号表视觉对应）。

**Mermaid 侧的情况不同（实测）**：Mermaid 11 自带 KaTeX 渲染通道，图节点标签里的 `$$...$$` **已经**被渲染成 KaTeX 标记
（探针图里出现 `.katex` 节点、`$` 被消费）。但仓库从未引入 KaTeX 的样式表，这些节点**没有配套 CSS**，显示尺寸与间距是错的。
本次引入 KaTeX CSS 后，Mermaid 里的公式会同时显示正常 —— 属顺带修好，但需要显式纳入契约与验证，
否则「看起来支持、实际错位」的状态会再次被误认为已完成。

## What Changes

- 依赖：新增直接依赖 `katex` 与 `@vscode/markdown-it-katex`（`katex` 现已是 mermaid/naive-ui 的传递依赖，此处提为直接依赖以免受其版本与剔除策略牵连）。
- `web/src/components/common/MarkdownRenderer.vue`：注册 math 插件，使 `$...$`（行内）与 `$$...$$`（块级）渲染为 KaTeX；引入 `katex/dist/katex.min.css` —— 该样式表同时修复 **Mermaid 图内公式**的显示。
- 契约：`docs-page-content` 新增两条要求——「文档正文支持 LaTeX 数学公式」（含不支持写法与安全边界）与「Mermaid 图中公式显示正确」（`$$...$$` + KaTeX 样式就绪）。
- 契约：`article-note` 的「公式的表达约束」由「**必须**写成代码块」改为「**可用** LaTeX 渲染」，同时保留符号表要求（渲染出的公式仍需符号表与中文解释）。

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

- `docs-page-content`: 新增「文档正文支持 LaTeX 数学公式」——渲染边界、错误降级与既有行为不受影响。
- `article-note`: 修订「公式的表达约束」——公式改为可直接使用 LaTeX，符号表与中文解释要求保留。

## Impact

- 前端：`web/src/components/common/MarkdownRenderer.vue`、`web/package.json`（+ `package-lock.json`，已入库）。
- 产物：新增 KaTeX 样式与字体文件（woff2），`web/dist` 体积小幅增加。
- 行为变化：`$...$` / `$$...$$` 由字面文本变为排版公式；`\(...\)` 这类反斜杠写法仍按 markdown-it 转义规则处理（建议不使用，登记在 spec 中）。
- 文档约定变化：`article-note` skill 不再强制公式走代码块；需要改动该 skill 的 `SKILL.md` 与 `phases/5-writing.md` 表述。
- 不影响：Markdown 的 `html: false` 约束、图片 figure 包装、`[[slug]]` 链接改写、文内锚点接管、Mermaid 渲染。
