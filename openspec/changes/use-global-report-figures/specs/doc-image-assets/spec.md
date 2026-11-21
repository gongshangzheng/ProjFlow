## ADDED Requirements

### Requirement: 图件工作流不遮蔽全局技能

ProjFlow SHALL 通过项目 `documentation` 说明项目图件落点，并将通用图件生成和编辑交给全局 `report-figures`。项目 SHALL NOT 注册同名技能。现有项目图源、生成件及图片访问路径 SHALL 保持不变。

#### Scenario: 在 ProjFlow 选择制图工具

- **WHEN** 用户需要为文档或实验报告制作图件
- **THEN** `documentation` 说明项目资产位置，全局 `report-figures` 提供制图工作流，项目不遮蔽其名称
