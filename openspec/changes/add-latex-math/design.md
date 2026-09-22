## Context

- `web/src/components/common/MarkdownRenderer.vue` 用 markdown-it（`html: false`、`linkify`、`typographer`），已自定义：`heading_open`（生成 id）、`fence`（mermaid / 代码块）、`image` + `paragraph_open/close`（figure 包装）、以及渲染前的 `[[proj#task]]` / `[[slug]]` 链接改写。
- 无任何 math 插件。`katex@0.16.47` 已在 `node_modules`（mermaid / naive-ui 的传递依赖），但源码零引用。
- `web/package-lock.json` **已入库**，因此新增依赖会带来 lockfile 变更（正常）。
- npm registry 为 `registry.npmmirror.com`，可访问；`@vscode/markdown-it-katex@1.1.2` 可用。
- 既有约定：`openspec/specs/article-note/spec.md` 的「公式的表达约束」要求公式走代码块。
- **Mermaid**：`MarkdownRenderer` 用 `mermaid.initialize({ theme, securityLevel: 'loose', ... })` 后 `mermaid.run()`；Mermaid 11 自带 KaTeX 通道。实测图内 `$$...$$` 已产出 `.katex` 节点，但仓库未加载 KaTeX CSS → 显示错位。

### D6: Mermaid 图内公式靠同一份 KaTeX CSS 修好，不额外改 Mermaid 配置

实测结论：

| 写法 | Mermaid 11 现状 |
|------|-----------------|
| `$$x_t$$` | 已渲染为 KaTeX 标记（`.katex` 节点存在，`$` 被消费） |
| `$\hat{y}$`（单 `$`） | 不渲染为数学（Mermaid 自身规则如此） |

因此**不改 `mermaid.initialize` 的任何配置**，也不自己接管图内公式；只需加载 `katex/dist/katex.min.css`，
图内公式即从「标记正确、样式缺失」变为显示正确。

- 理由：Mermaid 的数学解析在它内部，从外部接管既无必要也会与它的版本演进打架。
- 备选：关掉 Mermaid 的数学、自己在源码里预渲染 —— 会把公式渲染耦合到 Mermaid 版本，不采用。
- 边界：图内**只支持 `$$...$$`**（单 `$` 不支持），已写进 spec 的已知边界 Scenario。

## Goals / Non-Goals

**Goals:**

- `$...$` / `$$...$$` 渲染为 KaTeX，且不破坏既有渲染链（figure、mermaid、锚点、链接改写、`html: false`）。
- 公式非法时降级，不整页崩。
- 不误吞普通 `$`（如金额）。
- 同步改掉「公式必须写代码块」的契约与 skill 表述。

**Non-Goals:**

- 不支持 `\(...\)` / `\[...\]` 这两种反斜杠定界符（见 D3）。
- 不做公式编号 / 交叉引用（`\label` / `\ref` / 自动编号）。
- 不改 Mermaid 内部对 `$$` 的处理。
- 不引入服务端渲染（KaTeX 在前端渲染）。

## Decisions

### D1: 用 `@vscode/markdown-it-katex`，而不是自写 rule 或 `markdown-it-texmath`

- 理由：它是 `markdown-it-katex` 的维护版，直接产出 KaTeX HTML，含 `throwOnError: false` 的降级路径；自写 rule 要正确处理定界符转义、嵌套、`$$` 跨段落等边界，收益不抵风险。
- 依赖：同时把 `katex` 提为**直接依赖**——否则一旦 mermaid 改版/换实现，`katex` 会从依赖树消失，文档公式跟着崩。两者都要显式声明。
- 备选：`markdown-it-texmath`（支持多引擎）—— 功能过剩且 API 更绕，不采用。
- 备选：自写 rule + 直接调 `katex.renderToString` —— 边界处理成本高，不采用。

### D2: 只开 `$...$` 与 `$$...$$`，并显式验证不误吞金额

`@vscode/markdown-it-katex` 的行内规则本身带保护（开定界符后不能紧跟空白、闭定界符前不能是空白等），但仍需**实测** `价格从 $5 到 $10 不等` 这类文本不被吞。若被吞，则按仓库既有做法收窄：只在 `inline.math_inline` 前置一个「开闭 `$` 两侧非数字/非空白」的自定义守卫。

- 该实验写进验证任务，结论若为「被吞」则在实施时补守卫并在 spec 的 Scenario 中保持同一期望。

### D3: 不支持 `\(...\)` / `\[...\]`，并在 spec 中写明

`\(` 在 markdown-it 里本就是「转义左括号」，会被吃成 `(`。要支持得先绕过转义链，容易与其它规则打架（且现状下写这两种定界符的文档本来就已经渲染错误）。

- 决策：不引入、不支持；在 `docs-page-content` 的能力说明里说明「建议使用 `$...$`」。这样不会给出「看起来支持其实错」的错觉。
- 备选：同时支持 —— 需处理 `md.escape` 链与插件冲突，收益低，不采用。

### D4: KaTeX 样式在 `MarkdownRenderer.vue` 内引

`import 'katex/dist/katex.min.css'`。理由：只有用到该渲染器的页面需要它；Vite 会把这部分 CSS 关联到该组件的 chunk。字体（woff2）随之进入产物，属可接受成本。

### D5: 与既有自定义规则共存时的注意点

- `paragraph_open/close` 的 figure 包装只在「整段仅一张带 alt 的图」时生效，纯公式段落不满足该条件 → 不受影响；但需实测块级公式（KaTeX 会输出 `<span class="katex-display">`）不会被包进 `<figure>`。
- `fence` 覆写负责 mermaid 与代码块，math 不走 fence → 代码块里的 `$` 保持原样（spec 有对应 Scenario）。
- 链接改写发生在 `md.render` **之前**（正则替换），公式里含 `[[` 的极端情况不在承诺范围。

### D7: 针对 CJS 插件的默认导出做归一化（dev/build 互操作不同）

实施时踩到的真实坑：`@vscode/markdown-it-katex` 是 CJS（`exports.default = fn`），
两侧打包器的默认导出形态**不一致**：

| 环境 | `import` 拿到的默认导出 |
|------|------------------------|
| dev（esbuild 预打包） | 命名空间对象 `{ default: fn, __esModule: true }` |
| build（Rollup） | 函数本身 |

dev 下 `md.use(对象)` 会抛错，而 `<script setup>` 的顶层代码就在 setup 里执行 →
Vue 只报「Unhandled error during execution of setup function」，**正文整块不渲染**（页面看似只剩空态，排错成本高）。

处理：把导入改成 `import * as m`，再 `m.default?.default ?? m.default` 归一化；拿到非函数时 `console.error` 并跳过注册
（宁可公式按原文显示，也不要整块正文消失）。生产构建实测正常，说明归一化在两侧都成立。

## Risks / Trade-offs

- [金额等普通 `$` 被误吞] → 实测 + 必要时加守卫（D2）。
- [KaTeX CSS/字体进入产物，dist 变大] → 可接受；如需可后续按路由懒加载。
- [与 mermaid 各自带的 katex 版本不一致] → 提为直接依赖后由本仓库锁定版本；如出现重复打包，必要时在 Vite 里做 `resolve.dedupe: ['katex']`。
- [`\\(...\\)` 旧文档写法仍不可用] → 本就不支持且当前渲染结果是错的（反斜杠被转义），无回归；在 spec 中写明建议写法。
- [公式里的内容被 `typographer`/`linkify` 干扰（如 `--` 变连字符）] → 实测一个含 `--`、`*`、`_` 的公式；若被干扰，考虑对 `math_inline`/`math_block` 内容不做 typographer 处理（插件通常已隔离）。

## Migration Plan

1. `web` 下安装 `katex` 与 `@vscode/markdown-it-katex`（更新 `package.json` + `package-lock.json`）。
2. `MarkdownRenderer.vue`：引 CSS + `md.use(katexPlugin)`。
3. 造探针文档验证：行内 / 块级 / 表格内 / 非法公式 / 金额文本 / 代码块内 `$` / figure 与 mermaid 不回归；测完删除探针。
4. 更新 `article-note` 的 `SKILL.md` 与 `phases/5-writing.md` 表述，去掉「不写裸 LaTeX」。
5. 提交（`[shared]`，因 `MarkdownRenderer.vue` 属共享脚手架）。
6. 回滚：revert 提交并 `npm install` 回到旧 lockfile。
