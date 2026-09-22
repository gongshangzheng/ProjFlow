# documentation

## Purpose

定义 ProjFlow wiki 文档体系的权威来源与内容契约：文档登记表作为「新增 / 废弃 / 职责归属」的唯一权威；文档元数据以同名 sidecar json 承载并按固定布局渲染；结构级变更须经单篇 OpenSpec change 且 design 先行；仓库说明性文档统一置于 `management/docs/`。
## Requirements
### Requirement: 文档登记表为唯一权威

系统 SHALL 维护文档登记表（编号 / 标题 / slug / 职责边界 / 单篇 Change），作为文档体系所有「新增 / 废弃 / 职责归属」问题的唯一权威来源。登记表 SHALL 存放于仓库耐久位置 `openspec/registry.md`，MUST NOT 只存在于某个 change 的产物（尤其已归档的 change）中。

#### Scenario: 新增一篇 wiki

- **WHEN** 需要新增一篇 wiki 文档
- **THEN** 先在 `openspec/registry.md` 登记编号与职责边界，再开单篇 Change `docs-<slug>`，design 审核通过后才动笔

#### Scenario: 内容归属有争议

- **WHEN** 一段内容不确定属于哪一篇（职责边界存疑）
- **THEN** 按登记表的职责边界裁定；边界本身要改时先修订登记表（体系级动作），再动正文

#### Scenario: 登记表位置可被稳定引用

- **WHEN** 需要查看或修改登记表
- **THEN** 在 `openspec/registry.md` 找到它，无需翻找任何归档 change

#### Scenario: 表与仓库实际一致

- **WHEN** 检查登记表列出的 slug
- **THEN** `management/docs/` 下存在对应文档（或该行是以 `*` 结尾的类目行，表示整类不在编号体系内）

### Requirement: 章节列表对标题强调符号的处理

文档页右侧章节列表 SHALL 对 Heading 中的 Markdown 强调符号（`**`）做处理——丢弃或渲染为强调；MUST NOT 原样显示符号字符。

#### Scenario: 标题含加粗

- **WHEN** 某标题为 `### §4.2 任务看板：**三段表结构**`
- **THEN** 章节列表显示「§4.2 任务看板：三段表结构」（符号丢弃）或同等强调渲染，且不出现 `**` 字符

### Requirement: 文档元数据存于同名 sidecar json

每篇文档（`<slug>.md`）SHALL 支持同名 sidecar json（`<slug>.json`）承载元数据：`changelog`（演进：日期 + 一句话 + commit）、`progress`（进度）、`appendix`（附录设计说明）、`related`（相关文档）。这些元数据 SHALL NOT 出现在正文章节与章节列表中。

#### Scenario: 更新演进记录

- **WHEN** 某文档发生一次值得记录的演进
- **THEN** 只更新 `<slug>.json` 的 `changelog`（追加：日期 + 一句话 + commit），正文不变、不触发章节重排

### Requirement: 元数据的渲染布局

文档页 SHALL 在**文章顶部**提供按钮展示演进记录与进度（点击弹层）；SHALL 在**文章底部**以独立块渲染相关文档与附录；无对应字段的文档 MUST NOT 渲染空块。

#### Scenario: 打开带完整 sidecar 的文档

- **WHEN** 读者打开某篇配有完整四字段 sidecar json 的文档
- **THEN** 顶部可见「演进记录」「进度」按钮，点击弹层展示；页面底部出现「相关文档」与「附录」独立块；正文与章节列表不含这些内容

#### Scenario: 无 sidecar 的文档

- **WHEN** 某文档没有同名 json 或 json 为空
- **THEN** 不渲染顶部按钮与底部块，页面正常

### Requirement: 结构级变更走单篇 Change 且 design 先行

结构级文档变更（章节增删 / 移动 / 重编号 / 内容定位变化）MUST 走单篇 OpenSpec Change，且 MUST 在 design.md 中写明目标结构（章节清单 / 每章职责 / 细章分解 / 读者动线）并经用户审核后方可动笔。内容级小修（错字 / 数字 / 单段论证 / 链接）直接修改，MUST 在 commit message 中说明。

#### Scenario: 重排章节

- **WHEN** 需要重排一篇文档的章节
- **THEN** 先在单篇 Change 的 design 写明新旧结构与重映射方案，审核通过后实施，并以「引用闭合核对（悬空 = 0）」作为完成标准

### Requirement: 仓库文档根目录唯一

仓库的说明性文档 SHALL 统一置于 `management/docs/` 下；仓库根目录 MUST NOT 存在 `docs/` 目录。`AGENTS.md` 等结构说明文档 MUST 与实际目录保持一致，不得保留已删除目录的条目。

#### Scenario: 检查仓库顶层目录

- **WHEN** 检查仓库根目录
- **THEN** 不存在 `docs/` 目录，说明性文档位于 `management/docs/`

#### Scenario: 结构说明与实现一致

- **WHEN** 目录结构发生变化（新增或删除顶层目录）
- **THEN** `AGENTS.md` 的目录树在同一变更内同步更新，不残留已删除目录的条目

