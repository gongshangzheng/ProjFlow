## Context

- 来源：下游 `digital-human` 的两个已归档 change（`docs-inline-anchor-links`、`docs-list-ordering`）在共享脚手架层落地并验证通过。
- 现状（ProjFlow）：
  - `MarkdownRenderer.vue` 的 `handleClick` 只接管 `/management/` 前缀链接；`#` 锚点走浏览器默认行为（改 URL、不接 TOC 平滑滚动）。
  - `get_docs()` 用两趟稳定排序（id 主序 + date 降序），`_assets` 等下划线目录已跳过（`add-doc-image-assets`）。
- 约束：`add-doc-image-assets` 刚落地，回灌时 MUST 保留其 `_assets` 跳过逻辑，避免覆盖。
- 归属：`AGENTS.md` 结构、`server/`、`web/` 脚手架均属上游，按 `upstream-sync` 铁律回灌上游。

## Goals / Non-Goals

**Goals:**

- 把两处通用改进以 `[shared]` 形式落到上游，供所有下游 cherry-pick。
- 排序链保持向后兼容：有 `order`/`id` 时顺序与改动前一致。

**Non-Goals:**

- 不引入任何领域目录名到上游（`DOCS_FOLDER_ORDER` 默认空）。
- 不改前端列表/树组件（顺序完全由服务端返回顺序决定，前端无需改动）。
- 不顺手把 `add-doc-image-assets` 的下发写入本 change（那是下游 cherry-pick 动作，不在上游）。

## Decisions

### D1: 排序键放 `_doc_sort_key`，folder 优先级从 `config.py` 读

`server/config.py` 新增：

```python
# 文档列表中文件夹的先后（上游默认空；下游按需覆盖，未列出的排在已知之后）
DOCS_FOLDER_ORDER = []
```

`get_docs()` 末尾由两趟 `sort` 改为单次 `docs.sort(key=_doc_sort_key)`，键为元组：

```text
(folder_rank, order_num, id_num, -date_ordinal, slug)
```

- 理由：元组比较天然给出全序，最后一级 `slug` 是与文件系统无关的稳定兜底。
- 备选：仍用多趟稳定排序——需要四级排序且易漏兜底，可读性差，不采用。
- 备选：把 `DOCS_FOLDER_ORDER` 硬编码成中文领域目录——污染上游、下游各异，不采用。

### D2: 数字字段统一走 `_doc_number`

`order` / `id` 可能是 int、float、字符串或缺失。统一转为 `float`，缺失/非数字 → `inf`（排最后），与原有 `id` 处理语义一致。`bool` 显式排除（`isinstance(value, bool)`），避免 `True` 被当作 1。

### D3: 日期统一走 `_doc_date_ordinal`

`date` 已由 `_normalize_date` 归一为字符串；排序时再转 `date.fromisoformat(value[:10]).toordinal()`，非法/缺失返回 `0`。取负实现降序，保持「新在前」。

### D4: 锚点接管放在 `handleClick` 最前，`href` 空值早返回

```js
const href = anchor.getAttribute('href')
if (!href) return
if (href.startsWith('#')) { /* preventDefault + scrollIntoView */ return }
if (href.startsWith('/management/')) { /* 原有 router.push */ }
```

- 理由：`#` 分支必须在 `/management/` 之前判定（互斥前缀，顺序无关但需先处理）；`href` 为空时原逻辑会静默跳过，显式早返回更清晰。
- `decodeURIComponent(href.slice(1))`：兼容中文锚点（浏览器会 URL 编码）。

## Risks / Trade-offs

- [回灌覆盖 `add-doc-image-assets` 的改动] → 本 change 保留 `_assets` 跳过与图片渲染代码不动，只替换 `get_docs()` 排序段与 `handleClick`。
- [列表顺序变化影响既有页面观感] → 仅当 `order`/`id`/`date` 全部无法区分时才变化（由不确定→确定）；有 `id` 的文档顺序不变。
- [`DOCS_FOLDER_ORDER` 默认空导致下游以为功能缺失] → 在 `config.py` 注释中说明「下游按需覆盖」，并在本 change 中记录 digital-human 的取值。
