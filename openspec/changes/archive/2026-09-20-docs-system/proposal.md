# Proposal: docs-system（文档体系总 Change）

## Why

ProjFlow wiki（`management/docs/`）现有 api-design-conventions、git-workflow 两篇，后续会持续增长。姊妹库 pet-action-recognition 的 wiki 已在增长中踩过坑：职责边界漂移、同一主题两篇重复、编号引用失真、元数据（演进/进度/附录/相关）塞进正文导致结构混乱、TOC 显示原始 Markdown 符号。其解决方案已在该库落地并验证（change `docs-system`，commits fc2110d → cb76c36）。本 Change 将其中**通用机制**移植到 ProjFlow，防患于未然。

## What Changes

- 建立**文档登记表**（本 Change design 内，唯一权威）：每篇文档的编号 / 标题 / slug / 职责边界 / 相互关系 / 对应单篇 Change
- 确立**双层流程**：总 Change（本 Change）管体系；单篇 Change（`docs-<slug>`）管一篇——规则写入 `.agents/skills/documentation/SKILL.md` §0
- 跨文档引用规范：`[N 号《标题》](./<slug>.md)`；引用必须指向真实存在的标题锚
- **文档系统功能（前端 / 渲染层）**，与四库共享脚手架同构：
  - **TOC 强调符号处理**：文档页右侧章节列表不渲染 Markdown 加粗符号，但 Heading 中常含 `**` → 展示时须**丢弃或渲染**，不得原样显示符号
  - **sidecar json**：每篇 md 配同名 `<slug>.json`，承载 `changelog`（演进）/ `progress`（进度）/ `appendix`（附录设计说明）/ `related`（相关文档）；后端 `get_doc_detail` 一并读取返回，**演进/进度等元数据不再进正文章节**
  - **渲染布局**：**顶部按钮**（演进、进度，弹层）+ **底部独立块**（相关文档、附录）；无字段不渲染空块

## Capabilities

### documentation
- 文档登记表 SHALL 为文档体系的唯一权威
- 新增 / 废弃一篇文档 MUST 在本 Change 登记（或开新的体系级 Change）
- 结构级文档变更 MUST 走单篇 Change，且 design 先行

## Impact

- affected: `management/docs/**`、`.agents/skills/documentation/SKILL.md`、`server/routers/management.py`、`web/src/utils/markdown.js`、`web/src/views/management/DocPage.vue`、`openspec/changes/docs-*`
- 归属说明：`server/routers/management.py`、`web/src/views/management/DocPage.vue`、`web/src/utils/markdown.js` 属共享脚手架层；实施后按 upstream-sync 铁律 `[shared]` port 回上游，再传播到其他下游库
- 不影响：papers / evaluation 路由与页面
