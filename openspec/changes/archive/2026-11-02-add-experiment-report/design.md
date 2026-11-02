# Design: add-experiment-report

> 移植自 CyberVerse `2026-11-01-experiment-report-viewer`（commit `373ccc8`），按 ProjFlow 的技术栈（FastAPI + Vue3 + Naive UI + 既有 MarkdownRenderer）与评测模块形态裁剪。

## Context

- management 是**只读**模块：FastAPI 后端从 `management/` 目录读取，所有写入走脚本（`server/routers/management.py`）。新报告区沿用这个边界，不新增写接口。
- 前端已有 `web/src/components/common/MarkdownRenderer.vue`（markdown-it + katex + mermaid + 任务清单），相对资源路径约定 `/api/management/docs-assets/...`；wiki 文档页（DocPage）已验证这条渲染链。
- 评测模块是实验的对应物：`evaluation/results/` 存 run 结果（`config_id × model_id × dataset_id` + metrics + timestamp），`evaluation/outputs/` 存输出媒体，前端已有 EvalResults / EvalOutputs / SpeedRun 页面。但结论没有沉淀载体。
- 用户已选定：目录落 `management/experiments/`（镜像 CyberVerse 路径）；全栈（skill + 脚本 + 后端 + 前端）一次做完；新建独立 `experiment` skill。
- 概念裁定（用户）：**experiment ≠ evaluation**——训练也是实验，评测只是验证手段之一。experiment 是模块无关的方法论；evaluation 是评测模块的操作指南。两者交叉不包含，不合并。

## Goals / Non-Goals

**Goals:**

- 每个 topic 一个目录，同一 topic 下每篇报告一个子目录；报告由 topic + slug 共同标识，能在前端按 status / verdict / incomplete 筛选浏览。
- 详情页能完成「审阅一篇实验」：看结论上界（evidence）、看指标表与趋势、看案例 A/B 对比（原始像素）。
- 报告由脚本从作者清单 + 既有 run 产物生成，避免手抄数字；执行失败也保留草稿并如实标记。
- 复用既有 markdown 渲染与静态资产服务，不引入图表库（趋势用内联 SVG）。

**Non-Goals:**

- 不做在线编辑、reviewer 打分写回（审阅走人工，结论用 `verdict` 字段表达）。
- 不做跨报告聚合仪表盘。
- 不做离线 HTML 导出、持久媒体目录（见 proposal 差异表）。
- 不改评测模块（`evaluation/`）的运行、结果存储与既有页面行为。

## Decisions

### D1：报告按 topic 分组存放（同 CyberVerse D1）

`management/experiments/<topic>/<YYYYMMDD>-<runid>/`，含 `report.md`、`metrics.json`、`manifest.json`、`assets/`。以 topic + slug 组合唯一定位；扫描两级目录并校验两个路径段。跨模块引用（评测产物在 `evaluation/`、报告在 `management/`）通过 frontmatter `source` 字段（run 产物相对路径）与 manifest 的 `source`/`source_run` 记录追溯，生成脚本不复制大产物。

### D2：后端只加两个只读路由 + 一个资产目录服务

`GET /api/management/experiments`（列表 + invalid）与 `GET /api/management/experiments/{topic}/{slug}`（详情）。实现放 `server/routers/management.py`，解析逻辑独立成 `server/parsers/experiments_parser.py`（与 team/report 等 parser 同级）。

资产服务：`management/experiments/` 下的 `assets/` 图片经 `GET /api/management/experiments/{topic}/{slug}/assets/{file}` 提供（safe_resolve 防穿越，扩展名白名单 png/jpg/jpeg/gif/webp/svg）。不复用 docs-assets 全目录挂载——报告资产需按报告粒度隔离，且未来可能有条件访问；按路由显式服务更清晰。

`incomplete` 由后端推导（不写进 frontmatter）：检查 frontmatter 必填字段、8 个章节标题齐全、manifest 的 evidence 六项 + 每条 metric 的必填子字段、每个 case 的文件存在与 `sha256` 匹配。推导规则与生成脚本一致（同一套常量）。

### D3：A/B 对比组件复用「原始像素不缩放」原则

ProjFlow 评测案例图（对比帧、曲线截图）数量少、以静态图为主，不移植 CyberVerse 的 `CompareViewer.vue` 全量交互（四边裁图 tab、缩放平移）；实现一个轻量版：`CaseGallery` 组件，并排 + 同位置交替切换两种模式，`image-rendering: pixelated`、容器滚动不缩放。后续有逐像素审阅需求时再升级。

### D4：趋势图用仓内已有的 echarts（修订：原定内联 SVG）

原设计照搬 CyberVerse「不引入图表库、手写内联 SVG」，但具前提是 CyberVerse 无图表依赖；ProjFlow 已依赖 `echarts + vue-echarts`（EvalResults 在用）。改为直接用 echarts 折线图渲染 `series`，与仓内既有模式一致，无新增依赖。`metrics.json` 结构不变（`{"series": [...], "tables": [...]}`），tables 仍渲染为 Naive 表格。

### D5：生成脚本放在 skill 私有目录

`.agents/skills/experiment/scripts/build_report.py`（纯标准库）。理由：它只被 experiment skill 的流程使用，还没有被 AGENTS.md 或其他 skill 引用（CyberVerse skill 的「配套脚本放哪里」判据：谁依赖它）。若日后项目规则要引用它，再迁到仓库 `scripts/`。

作者清单（input JSON）格式沿用 CyberVerse：`report`（summary/question/limitations/conclusion，作者文字优先于 run 摘要）、`evidence`（六项）、`metrics`（name/unit/baseline/result/delta/sample_size/source/limitation）、`cases`（id/kind/src/source_run/input/selection_reason）。kind 仅支持 `image`（裁掉 video/audio）。`src` 相对 run 目录或直接给仓库相对路径；脚本复制图片进 `assets/` 并算 sha256。

### D6：status / verdict 枚举 + incomplete 推导（同 CyberVerse D6）

`status`: `complete|partial|failed`（执行状态）；`verdict`: `improved|no-gain|worse|inconclusive`（结论方向）；`incomplete` 派生（报告完整度）。三者独立：失败的 run 也可以有完整的报告。

### D7：报告标题与正文模板（参照 CyberVerse 124a697：读者导向文章模板）

标题「实验主题：对照方案与评估目标」。正文采用读者导向文章五章：背景与目标 / 当前问题 / 实验设计 / 结果与分析 / 结论与下一步，加附录「附录：配置与完整数据」（网页默认折叠）。写作骨架与叙述字段（background/problem/design/analysis/conclusion + 可选 limitations/summary）见 `.agents/skills/experiment/references/report-template.md`。缺失或不适用的内容必须说明原因，不得用占位文字冒充实测结果。

正文只保留能帮助判断的数值、图表和媒体并就近说明含义与限制；完整指标、精确配置、版本、权重、哈希、命令与原始来源放入附录。不得把原始 metrics.md 直接拼进正文，也不得自动铺满指标卡片。核查数据齐全不等于文章清楚，两项均须审阅。

**向后兼容**：后端与生成脚本同时接受新文章模板或旧八章机器校验式模板（旧报告不清空），旧模板标记 legacy 仍完整校验。缺背景、设计或解释时保留明确草稿提示，不从目录名猜造内容。

### D8：skill 边界与裁剪范围

**experiment 是模块无关的方法论 skill**：实验 = 假设驱动的任何实证工作（训练实验、消融、A/B 对比、bug 复现、用评测 run 回答问题）。评测只是其中一种执行底座。

| skill | 管什么 | 不管什么 |
|---|---|---|
| `experiment` | 方法论（假设、baseline、对照、证据标准、样本量、失败边界、即时留痕）、报告生成与审阅（`management/experiments/`） | 评测模块的文件格式与 CRUD 操作 |
| `evaluation` | 评测模块操作（模型/数据集/配置管理、跑评测、结果对比） | 实验设计方法论、实验报告 |

评测 run 作为实验证据时：报告 frontmatter `source` 与 manifest `source_run`/`source` 指向 `evaluation/results|outputs/` 下的产物，experiment skill 引用 evaluation skill 获取数据，不复制其操作指南。训练等其他实验的产物路径由该实验自定，`source` 如实记录（仓库相对路径）。

skill 内容从 CyberVerse 裁剪——保留：核心流程（面向报告规划 → baseline → 对照 → 执行记录 → 报告）、三类实验证据标准（性能效率 / 感知质量 / 正确性一致性，ProjFlow 语境举例：API 延迟、回复质量盲评、指标核算闭环）、可辨识性检查、样本量门槛、一次只改一个变量、反事实差值、自证循环防护、失败边界、evidence 段骨架、反模式表。去掉：GPU 占用检查（0.3）、resource guard（0.3.1）、并行会话协调（0.4）、remote-ops env_check（0.5，换成轻量环境记录要求）、fix-patterns 领域案例、`results/` 产物目录树。

触发词：实验报告、设计对比实验、训练实验、消融、A/B 对比、写实验报告；与 evaluation 触发词（添加模型/数据集、跑评测）无重叠。

### D9：菜单与路由

路由 `/management/experiments`（列表+详情同页，模式同 DocPage/MeetingList）。菜单挂「评测」组（实验报告与评测模块强关联，虽然目录在 management 下）——不对，遵循 management 菜单结构按数据目录组织的现状，挂「项目管理」组的文档附近；最终以 MainLayout 现有分组代码为准，实施时选择语义最贴近的分组（倾向「项目管理」组、Wiki 文档之后）。`HIDDEN_KEYS` 机制登记 key，默认可见。

## 验收

1. `build_report.py` 对一篇真实评测 run 生成报告，缺省清单时产 incomplete 草稿（diagnostics 说明缺什么）；补全后产 complete 报告。
2. `GET /api/management/experiments` 返回该报告（complete）与一个故意破坏的目录（invalid/missing 字段可见）。
3. 前端页面：列表筛选（topic/status/verdict）→ 详情渲染 markdown 正文、指标表、趋势 SVG、案例图 A/B 交替；窄屏与深色模式可用（遵循 design-principles 与 web-a11y change 的既有标准）。
4. experiment skill 触发词覆盖「实验报告 / 设计对比实验 / 训练实验 / 消融 / A/B」等场景，与 evaluation skill 触发词（模块 CRUD、跑评测）无职责重叠。

## 风险

- **两套常量漂移**（脚本 vs 后端的章节/字段校验）：把章节名、必填 frontmatter、evidence 六项定义为两处共享的单一来源不可行（Python 前后端同语言可行——脚本与后端都是 Python，可让脚本 import 后端 parser 的常量；但 skill 脚本 self-locating 要求纯标准库且不依赖 server 包）。取舍：两边常量显式注释「与 X 保持同步」，并在 change tasks 里放一条对拍测试（后端 pytest 用生成脚本产出物断言解析结果）。
- **菜单归属歧义**（数据在 management、语义在 evaluation）：实施时按 MainLayout 实际分组代码定，不新增分组。
- **首页/深链**：报告详情用页内状态而非独立路由段，深链用 query（`?topic=&slug=`）承载，成本低于嵌套路由。
