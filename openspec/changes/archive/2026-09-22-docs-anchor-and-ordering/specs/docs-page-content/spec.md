## Purpose

定义文档页（`/management/docs`）内容侧的两项契约：正文内锚点链接 `[文字](#slug)` 的点击行为与右侧 TOC 一致且不改 URL；文档列表顺序由显式字段与稳定兜底键决定，不依赖文件系统遍历顺序。

## ADDED Requirements

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
