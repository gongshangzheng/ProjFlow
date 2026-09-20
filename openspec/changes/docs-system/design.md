# Design: docs-system

> 来源：移植自姊妹库 pet-action-recognition 的同名 change（commits fc2110d / 2bda2fa–ded3e31 / 070ed58 / cb76c36），机制通用，登记表内容按 ProjFlow 实际重写。

## 文档登记表（唯一权威）

| 编号 | slug | 标题 | 职责边界（只管什么） | 单篇 Change |
|---|---|---|---|---|
| 1 | api-design-conventions | API 设计约定 | server/ 各路由的 API 设计规范（路径 / 响应结构 / 错误处理） | — |
| 2 | git-workflow | Git 工作流 | 分支模型 / commit 规范 / 提交流程 | — |
| — | papers/docs/* | 论文模块文档 | 论文模块专属说明（不在 wiki 编号体系内） | — |
| — | evaluation/docs/* | 评测模块文档 | 评测模块专属说明（不在 wiki 编号体系内） | — |

**登记规则**：
- 新增 / 废弃一篇 wiki → 先在本表登记编号与职责边界，再开单篇 Change `docs-<slug>`
- 职责争议按「职责边界」列裁定；边界要改 → 先改本表（体系级动作），再动正文

## 跨文档引用规范

- 格式：`[N 号《标题》](./<slug>.md)`；带节号时 `[N 号 §X.Y](./<slug>.md)`
- **引用必须闭合**：指向的标题必须真实存在；编号重映射后全仓核对（悬空引用必须为 0）
- 正文中引用决策用「名字（Cxx）」，不裸用编号

## 文档系统功能范围（渲染层 / 前端）

| 功能 | 说明 | 涉及 |
|---|---|---|
| TOC 强调符号处理 | 章节列表对标题中的 `**` 丢弃（或渲染为强调），不显示符号字符 | `web/src/utils/markdown.js`（extractToc / slugify）|
| **sidecar json** | 每篇 `management/docs/<slug>.md` 配同名 `<slug>.json`：`changelog`（演进：date + note + commit 数组）/ `progress`（roadmap + gates）/ `appendix`（title + body，markdown 字符串）/ `related`（title + slug + desc 数组）| `server/routers/management.py`（get_doc_detail 读取同名 json 一并返回；解析失败降级为空对象）|
| 渲染布局 | **顶部按钮**：演进记录、进度（点击弹层）；**底部独立块**：相关文档、附录；无 sidecar 或字段为空不渲染 | `web/src/views/management/DocPage.vue` + 弹层 / 底部块组件 |

**sidecar 字段 schema**（与 pet 库一致，保证四库可交换）：

```json
{
  "changelog": [{ "date": "YYYY-MM-DD", "note": "一句话", "commit": "<sha>" }],
  "progress": { "roadmap": ["..."], "gates": ["..."] },
  "appendix": { "title": "...", "body": "markdown 字符串" },
  "related": [{ "title": "...", "slug": "...", "desc": "..." }]
}
```

## 与上游 / 下游的关系

- 本 Change 实施的是**共享脚手架层**功能（management 路由 / DocPage / markdown 工具），非 ProjFlow 领域数据
- 按 upstream-sync 铁律：实施完成后整理 `[shared]` commit port 回上游，由上游传播到 infraredComp / DigitalTeacher
- 来源血缘：pet-action-recognition `docs-system`（cb76c36 等搬运时该改进尚未经上游传播，属下游直引，port 上游时须注明）

## 与其他 Change 的关系

- 领域功能 change（papers / evaluation / management 业务）不在本 Change 登记
- 文档类 change（`docs-<slug>` 单篇）登记在本 Change 的 tasks 与登记表
