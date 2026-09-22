## 1. 依赖

- [x] 1.1 `web` 下安装直接依赖 `katex` 与 `@vscode/markdown-it-katex`（`npm install --save`，更新 `package.json` + `package-lock.json`）
- [x] 1.2 确认 `package.json` 的 `dependencies` 里两者都在（`katex` 不能再只作为传递依赖）

## 2. 渲染接入

- [x] 2.1 `web/src/components/common/MarkdownRenderer.vue`：`import 'katex/dist/katex.min.css'`
- [x] 2.2 同文件：注册 math 插件（`md.use(katex)`），确认不改变 `html: false` / `linkify` / `typographer` 既有配置
- [x] 2.3 确认块级公式不会被 `paragraph_open/close` 的 figure 包装误包
- [x] 2.4 确认 `mermaid.initialize` 配置未被改动（Mermaid 图内公式靠同一份 KaTeX CSS 生效，不接管其解析）
- [x] 2.5 对 CJS 插件的默认导出做归一化（dev 预打包给命名空间对象、build 给函数），并**在 dev 与 preview 两侧都验证**

## 3. 契约与 skill 同步

- [x] 3.1 `openspec/specs/article-note/spec.md`：由本 change 的 MODIFIED delta 覆盖「公式的表达约束」（归档时生效）
- [x] 3.2 `.agents/skills/article-note/SKILL.md`：删除「不写裸 LaTeX 期待渲染」，改为「公式用 `$...$` / `$$...$$`，并配符号表」
- [x] 3.3 `.agents/skills/article-note/phases/5-writing.md`：同步「公式放 fenced code block」的表述
- [x] 3.4 检查 `references/note-structure-template.md` 等处是否仍暗示「必须代码块」

## 4. 验证（造探针文档，测完删除）

- [x] 4.1 行内 `$E = mc^2$` → 出现 `.katex` 节点，不显示 `$`
- [x] 4.2 块级 `$$ ... $$` → 出现 `.katex-display`，居中成块，且未被包进 `<figure>`
- [x] 4.3 表格单元格内 `$\theta$` → 行内公式，表格结构正常
- [x] 4.4 金额文本 `价格从 $5 到 $10 不等` → **不被吞**（若被吞则加守卫后复测）
- [x] 4.5 代码块内含 `$` 或 `$$` → 原样保留
- [x] 4.6 非法公式 `$\frac{1}{$` → 不整页崩，其余内容正常
- [x] 4.7 回归：图片 figure + 图题、Mermaid、文内锚点、`[[slug]]` 链接改写均正常
- [x] 4.8 含 `--` / `*` / `_` 的公式不被 typographer 破坏
- [x] 4.9 Mermaid 图内 `$$...$$` → 图内出现 `.katex` 节点，且其计算字体族为 KaTeX 自带字体（证明 CSS 已加载）
- [x] 4.10 Mermaid 图内单 `$` → 不渲染为公式（已知边界，按 Mermaid 规则处理）
- [x] 4.11 `npm run build` 通过；确认产物无重复 katex（必要时 `resolve.dedupe`）
- [x] 4.12 清理探针文件，工作区干净

## 5. 收尾

- [x] 5.1 `openspec validate add-latex-math` 通过
- [x] 5.2 以 `[shared]` 前缀提交并 push
- [x] 5.3 归档
