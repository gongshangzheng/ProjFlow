# docs-anchor-and-ordering

## Why

下游库 `digital-human` 在共享脚手架层做出两处通用改进，均已在其仓库验证通过，但尚未回灌上游：

1. **文内锚点接管**：正文里 `[文字](#小节)` 目前走浏览器默认跳转，会改 URL 且不与右侧 TOC 行为一致。
2. **文档列表排序链**：`get_docs()` 只有 `id` + `date` 两级排序，`id` 缺失或相同时顺序落到文件系统遍历序（APFS 无序），表现为刷新一次顺序一个样。

按 `upstream-sync` 铁律，下游改了共享脚手架必须先 port 回上游，再由上游传播到各兄弟库。

## What Changes

- `web/src/components/common/MarkdownRenderer.vue`：`handleClick` 增加文内锚点分支——`href` 以 `#` 开头时 `preventDefault`，按 id 平滑滚动到目标，**不修改 URL**。
- `server/routers/management.py`：`get_docs()` 输出新增 `order` 字段，并以统一排序键 `_doc_sort_key` 取代现有两趟 `sort`——排序链为 **文件夹序 → `order` → `id` → `date` 降序 → `slug` 字典序**；新增 `_doc_number` / `_doc_date_ordinal` 辅助函数。
- `server/config.py`：新增 `DOCS_FOLDER_ORDER`（文件夹优先级列表，**上游默认空列表**，下游按需覆盖）。

## Capabilities

### New Capabilities

- `docs-page-content`: 文档页内容契约——正文内锚点链接的点击行为，以及文档列表顺序的确定性规则。

### Modified Capabilities

（无）

## Impact

- 代码：`web/src/components/common/MarkdownRenderer.vue`、`server/routers/management.py`、`server/config.py`。
- 行为变化：
  - 文内锚点不再改 URL（改为平滑滚动），与右侧 TOC 一致；
  - `id` 缺失或相同的文档，列表顺序由「不确定」变为「确定」；有 `order`/`id` 时顺序不变（向后兼容）。
- 以 `[shared]` 提交，供 `digital-human` / `children-face` / pet 等下游 cherry-pick。
- `DOCS_FOLDER_ORDER` 上游默认空，**不内置任何领域目录名**。
