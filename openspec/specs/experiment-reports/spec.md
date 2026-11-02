# experiment-reports Specification

## Purpose
TBD - created by archiving change add-experiment-report. Update Purpose after archive.
## Requirements
### Requirement: 报告目录约定

实验报告 SHALL 存放于 `management/experiments/<topic>/<slug>/`（slug 形如 `<YYYYMMDD>-<runid>`），每个报告目录 SHALL 包含 `report.md`，并 MAY 包含 `metrics.json`、`manifest.json` 与 `assets/`。报告 SHALL 由 topic 与 slug 组合唯一定位。

#### Scenario: 合法目录被收录
- **WHEN** `management/experiments/` 下存在合法 topic 与 slug 两级目录且含 `report.md`
- **THEN** 该报告出现在实验报告列表中，带 topic、slug 与 frontmatter 元信息

#### Scenario: 非法目录单列
- **WHEN** 某目录缺 `report.md`、frontmatter 缺必填字段或路径段非法
- **THEN** 该目录不出现在报告列表，而出现在 `invalid` 列表并说明缺失项

### Requirement: frontmatter 与章节完整性

`report.md` 的 frontmatter SHALL 提供 `title`、`date`、`run_id`、`status`、`verdict`、`summary`、`source`（`change` 为可选引用）；`status` SHALL 取 `complete|partial|failed`，`verdict` SHALL 取 `improved|no-gain|worse|inconclusive`。正文 SHALL 含八个规定章节：结论摘要、实验问题与假设、实验设置与环境、指标结果、案例展示、失败案例与限制、结论与建议、产物来源；不适用的章节 SHALL 说明原因而非省略。

#### Scenario: 枚举校验
- **WHEN** frontmatter 的 `status` 或 `verdict` 取枚举外值
- **THEN** 报告被标记不完整并列出该字段问题

#### Scenario: 缺章节
- **WHEN** 正文缺少任一规定章节标题
- **THEN** 报告被标记不完整并指出缺失章节

### Requirement: incomplete 由内容推导

报告完整度（incomplete）SHALL 由后端依据 frontmatter 完整性、章节齐全性、manifest 证据字段与案例可访问性推导，MUST NOT 由作者自填字段决定。

#### Scenario: 案例文件缺失
- **WHEN** manifest 声明的案例在 `assets/` 中不存在或 sha256 不匹配
- **THEN** 报告标记为 incomplete，详情页展示缺失原因

#### Scenario: 完整报告
- **WHEN** 所有必填字段、章节、evidence 六项与案例均有效
- **THEN** 报告不被标记 incomplete

### Requirement: 机器可读指标与案例清单

`metrics.json` SHALL 为 `{"series": [{name, x_label, y_label, points: [{x, y}]}], "tables": [{title, columns, rows}]}` 结构；`manifest.json` SHALL 提供 `evidence` 对象（实验类型、baseline 数值来源、可辨识性、样本量、失败边界、结论上界六项）、`metrics` 数组（每条含 name/unit/baseline/result/delta/sample_size/source/limitation）与 `cases` 数组（每条含 id/kind/src/source_run/input/selection_reason/sha256）。案例 MUST 由作者显式选择，生成器 MUST NOT 自动把扫描到的文件当作代表性案例。

#### Scenario: 指标结构校验
- **WHEN** `metrics.json` 缺 `series` 或 `tables` 键，或 series 的点缺 x/y
- **THEN** 详情接口返回结构问题，前端指标区显示缺失提示

### Requirement: 只读 API 与资产服务

后端 SHALL 提供实验报告列表与详情两个只读接口，以及按报告粒度服务 `assets/` 图片的资产接口；资产路径 SHALL 经防穿越校验且扩展名限于图片白名单。写入 SHALL 仅经由脚本完成，后端 MUST NOT 提供报告写接口。

#### Scenario: 路径穿越被拒
- **WHEN** 资产请求路径含 `..` 或白名单外扩展名
- **THEN** 请求被拒绝，不返回文件系统其它内容

### Requirement: 前端审阅页

前端 SHALL 提供实验报告审阅页：列表支持 topic 分组与 status/verdict/完整度筛选；详情展示元信息、Markdown 正文、指标表、趋势图与案例对比；案例图对比 SHALL 保持原始像素（不缩放），提供并排与交替两种查看模式。

#### Scenario: 筛选与深链
- **WHEN** 用户按 verdict=inconclusive 筛选并打开一篇报告后刷新
- **THEN** 详情经 query 参数恢复，正文与案例完整渲染

### Requirement: experiment skill 职责边界

experiment skill SHALL 覆盖模块无关的实验方法论（假设、baseline、对照、证据标准、样本量、失败边界、即时留痕）与报告生成流程；评测模块的文件格式与操作 SHALL 归属 evaluation skill，两者 MUST NOT 互相复制对方内容。

#### Scenario: 评测 run 作为证据
- **WHEN** 实验报告以评测 run 为证据来源
- **THEN** 报告 source 指向 `evaluation/` 下产物路径，正文不复制 evaluation skill 的操作指南

