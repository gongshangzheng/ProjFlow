## Why

ProjFlow 的本地 `report-figures` 遮蔽了全局同名入口。两套工具的绘图实现相同；项目只需维护图源、图片和报告资产的落点。

## What Changes

- 把项目资产规则迁入 `documentation`，将制图指引明确指向全局 `report-figures`。
- 删除本地 `report-figures` 技能副本与其中的示例、工具和测试；保留项目图源、生成件和报告。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `doc-image-assets`：区分项目资产存放规则与通用制图入口；终止本地同名注册。

## Impact

影响 ProjFlow 的两个项目技能目录；不改绘图实现、服务端、图表或报告，也不触碰未发布的本地提交。
