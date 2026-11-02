# Proposal: add-experiment-report（实验报告功能）

## Why

ProjFlow 的评测模块（`evaluation/`）能跑评测、存结果（`evaluation/results/` 的 metrics JSON）、前端对比数值，但实验结束后的结论没有可审阅的载体：数字散在 results JSON 里，结论留在对话或代码注释里，事后无法回答「这个实验证明了什么、上界在哪、案例长什么样」。姊妹库 CyberVerse 刚落地一套成熟的实验报告体系（`management/experiments/<topic>/<slug>/` + 报告查看页 + 生成脚本 + skill 门禁，commit `373ccc8`、change `2026-11-01-experiment-report-viewer`），经过一篇真实报告验收。本 change 把那套体系移植到 ProjFlow，去掉 GPU/远程机器/持久媒体目录等本项目不涉及的部分。

## What Changes

- **报告目录约定** `management/experiments/<topic>/<slug>/`（slug = `<YYYYMMDD>-<runid>`）：`report.md`（frontmatter `title/date/change/run_id/status/verdict/summary/source` + 8 个固定章节）、`metrics.json`（`series` 折线 + `tables` 指标表）、`manifest.json`（`evidence` 六项 + `metrics` 数组 + `cases` 数组）、`assets/`（案例图片）；目录级 `management/experiments/README.md` 说明约定
- **新 skill** `.agents/skills/experiment/`：**模块无关**的实验方法论与报告流程（面向报告规划、证据标准、对照设计、样本量门槛、incomplete 语义、报告生成），覆盖训练实验、消融、A/B 对比、bug 复现等一切假设驱动的工作；评测 run（`evaluation` 模块）只是证据来源之一，不是唯一形态。与 `evaluation` skill 的边界：evaluation 只负责「用评测模块做标准化验证」的模块操作（模型/数据集/配置 CRUD、跑评测、看结果），不含实验方法论；两者互链不合并。内容从 CyberVerse `experiment` skill 裁剪——保留方法论骨架，去掉 GPU 占用检查、resource guard、remote-ops、TRT/数字人领域案例
- **报告生成脚本** `.agents/skills/experiment/scripts/build_report.py`：作者清单驱动（input JSON 提供 report 文字 / evidence / metrics / cases），校验 frontmatter 与章节完整性、案例文件存在性，图片复制进 `assets/`，推导 incomplete 并写 diagnostics；不覆盖已有报告
- **后端只读路由**（`server/routers/management.py`）：`GET /api/management/experiments`（列表，含 topic/slug/status/verdict/incomplete + invalid 项）、`GET /api/management/experiments/{topic}/{slug}`（详情：frontmatter + 正文 + metrics.json + manifest.json + problems）；报告资产复用 docs-assets 静态挂载思路，新增 `management/experiments` 资产服务
- **前端查看页** `web/src/views/management/ExperimentsPage.vue`：左列表（topic 分组 + status/verdict 筛选）右详情（元信息条、`MarkdownRenderer` 正文、指标表、趋势内联 SVG、案例图集并排/交替 A/B 对比、原始像素不缩放），路由 `/management/experiments`，侧边栏菜单入口
- 用一篇现有评测结果生成首篇真实报告（`evaluation/results/` 数据 + `SpeedRun` 产物）作为验收

## 与 CyberVerse 原版的差异（有意裁剪）

| 裁掉 | 理由 |
|------|------|
| 离线单文件 HTML 导出（`--html` / `render_report.cjs`） | 依赖 Node 渲染链与前端 node_modules；ProjFlow demo 无离线分发需求 |
| 持久媒体目录（`CYBERVERSE_EXPERIMENT_MEDIA_ROOT`、音视频 sha256 登记、受限媒体接口） | ProjFlow 评测产物是指标 JSON + 少量对比图；图片统一进 `assets/` 随仓库走 |
| 环境段 11 字段强制校验（commit/torch/gpu_driver…） | 无 GPU/远程实验；环境段保留但按评测模块实际字段（模型/数据集/配置版本、时间戳） |
| 报告 frontmatter 的 `change` 字段强绑定 openspec change | ProjFlow 评测多为轻量对比；`change` 保留为可选引用字段 |

## Capabilities

### New Capabilities

- `experiment-reports`: 实验报告的目录约定、生成流程、只读 API 与前端审阅页

### Modified Capabilities

（无——评测模块 `evaluation` 既有行为不变；`menu-visibility` 如需注册新菜单项则按既有 `HIDDEN_KEYS` 机制加默认可见项，属配置补充）

## Impact

- 新增：`management/experiments/**`、`.agents/skills/experiment/**`、`web/src/views/management/ExperimentsPage.vue`、`web/src/api/experiments.js`（或并入 management.js）
- 修改：`server/routers/management.py`（+2 只读路由 + 资产服务）、`web/src/router/index.js`、`web/src/layouts/MainLayout.vue`（菜单）
- 不影响：`evaluation/` 模块数据与路由、既有 wiki 文档、论文模块
- 归属：报告目录约定与 skill 属共享脚手架层（上下游可继承）；后端/前端代码随本库
