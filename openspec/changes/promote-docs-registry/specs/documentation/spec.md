## MODIFIED Requirements

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
