# docs-page-content Specification

## Purpose
定义文档页（`/management/docs`）内容侧的两项契约：正文内锚点链接 `[文字](#slug)` 的点击行为与右侧 TOC 一致且不改 URL；文档列表顺序由显式字段与稳定兜底键决定，不依赖文件系统遍历顺序。
## Requirements
### Requirement: 文内锚点链接与 TOC 行为一致

正文里 `href` 以 `#` 开头的链接 SHALL 由前端接管：点击时阻止默认跳转，按锚点 id 找到目标元素并平滑滚动到视口顶部；MUST NOT 修改浏览器 URL（不留 hash）。

#### Scenario: 点击文内锚点
- **WHEN** 文档正文含 `[小节标题](#小节标题)`，读者点击它
- **THEN** 页面平滑滚动到该小节标题处，URL 保持不变

#### Scenario: 锚点指向不存在的 id
- **WHEN** 链接的锚点在当前文档里不存在
- **THEN** 点击无任何副作用（不报错、不改 URL），页面不跳动

### Requirement: 不影响既有链接行为

接管文内锚点 SHALL NOT 影响三类既有链接：跨文档链接（`[[slug|显示名]]` 与 `/management/docs/...`）、外部链接（`https://...`）、以及右侧 TOC 的滚动行为。

#### Scenario: 三类链接照常
- **WHEN** 正文同时含跨文档链接、外部链接与文内锚点链接
- **THEN** 前两类按原行为工作（站内路由跳转 / 新链接触发），文内锚点平滑滚动，右侧 TOC 点击仍平滑滚动

### Requirement: 用 `order` 字段显式表达阅读顺序

文档 frontmatter SHALL 支持 `order` 字段（数字），列表接口 SHALL 一并返回。列表排序中 `order` 的优先级 SHALL 高于 `id`：`order` 越小越靠前。未写 `order` 的文档 SHALL 继续按 `id` 排序，行为与改动前一致。

#### Scenario: 两篇都写了 order
- **WHEN** `A.md` 写 `order: 1`、`B.md` 写 `order: 2`（其余字段相同）
- **THEN** 列表中 A 排在 B 之前

#### Scenario: 未写 order 时不改变现状
- **WHEN** 某文档没有 `order` 字段
- **THEN** 它仍按 `id` 升序参与排序，既有顺序不变

#### Scenario: order 非数字
- **WHEN** `order` 的值不是数字
- **THEN** 该字段被忽略，回退到 `id` → `date` 排序，不报错

### Requirement: 排序链最终必须确定（不得落到文件系统顺序）

当文件夹、`order`、`id`、`date` 都无法区分两篇文档时，系统 SHALL 以稳定且与文件系统无关的附加键（slug 字典序）作为最后一级，保证列表顺序确定、可复现。

#### Scenario: 全部排序键相同
- **WHEN** 两篇文档同 `date`、同 `id`、都无 `order`
- **THEN** 它们的先后由 slug 字典序决定，且重复请求结果一致

### Requirement: 文件夹在列表中的先后可配置

文档在列表中的先后 SHALL 先按文件夹优先级判定，优先级由服务端配置常量 `DOCS_FOLDER_ORDER` 决定；未列入配置的文件夹 SHALL 排在已配置的之后。该常量在上游 SHALL 默认为空列表，不内置任何领域目录名。

#### Scenario: 配置的文件夹优先
- **WHEN** 配置 `DOCS_FOLDER_ORDER = ['a', 'b']`，文档树含 `b/` 与 `a/`
- **THEN** `a/` 下的文档整体排在 `b/` 之前

#### Scenario: 默认空配置不引入优先级
- **WHEN** `DOCS_FOLDER_ORDER` 为默认空列表
- **THEN** 不因文件夹名称产生额外优先级，顺序由 `order` → `id` → `date` → `slug` 决定

#### Scenario: 未配置的文件夹
- **WHEN** 树中出现未列入配置的文件夹
- **THEN** 它排在已配置文件夹之后，不报错

### Requirement: 文档正文支持 LaTeX 数学公式

文档正文 SHALL 支持以 `$...$` 书写的行内公式与 `$$...$$` 书写的块级公式，并渲染为 KaTeX 排版结果；渲染 MUST 保持 Markdown 渲染器的既有安全约束（不放开原始 HTML）。

#### Scenario: 行内公式
- **WHEN** 正文含 `质能关系 $E = mc^2$ 成立`
- **THEN** 该片段渲染为 KaTeX 行内公式（存在 `.katex` 节点），不显示 `$` 字面量

#### Scenario: 块级公式
- **WHEN** 正文含独占一行的 `$$ ... $$` 公式块
- **THEN** 渲染为 KaTeX 块级公式（存在 `.katex-display` 节点），居中成块

#### Scenario: 公式出现在表格中
- **WHEN** 表格单元格内含 `$...$`
- **THEN** 该单元格内渲染为行内公式，表格结构不受破坏

#### Scenario: 不放开原始 HTML
- **WHEN** 正文包含原始 HTML 字符串（如 `<img onerror=...>`）
- **THEN** 仍按文本转义输出，不执行；本能力仅新增数学渲染，不改变 `html: false`

### Requirement: 公式解析失败可降级

当公式语法非法时，渲染 SHALL 不抛异常、不导致整篇文档渲染失败；SHALL 以可辨识的方式呈现原式（如渲染为错误提示或保留原文）。

#### Scenario: 非法公式
- **WHEN** 正文含 `$\frac{1}{$`（括号不闭合）
- **THEN** 页面其余内容正常渲染，该处不出现未捕获异常导致的空白页

### Requirement: 不误吞普通美元符号

数学解析 SHALL NOT 把普通文本中的美元符号误判为公式定界符；一段文本中若 `$` 不构成合法公式（如紧邻数字或空白不符），SHALL 保持字面显示。

#### Scenario: 金额文本
- **WHEN** 正文含 `价格从 $5 到 $10 不等`
- **THEN** 该句按普通文本显示，不渲染为公式

#### Scenario: 代码块内不解析
- **WHEN** 代码块内含 `$` 或 `$$`
- **THEN** 代码块内容原样保留，不做数学解析

### Requirement: Mermaid 图中的公式正确显示

Mermaid 图节点标签中的 `$$...$$` SHALL 渲染为 KaTeX，且 KaTeX 样式表 SHALL 已加载，使公式的尺寸、间距与字体正确（Mermaid 自带 KaTeX 渲染通道，样式由本仓库提供）。

#### Scenario: 图内公式
- **WHEN** Mermaid 图中某节点标签写作 `输入 $$x_t$$`
- **THEN** 该标签渲染出 KaTeX 公式（图内存在 `.katex` 节点），不显示 `$$` 字面量

#### Scenario: 样式已就绪
- **WHEN** 检查图内 `.katex` 节点的计算样式
- **THEN** 字体族为 KaTeX 自带字体（如 `KaTeX_Main`），而非站点的默认字体（后者说明样式表未加载）

#### Scenario: 图内不支持单美元
- **WHEN** 图节点标签写作 `输出 $\hat{y}$`（单个 `$`）
- **THEN** 按 Mermaid 自身规则处理（不渲染为公式），属已知边界，不作为缺陷

