# Design: add-article-note-skill

## Context

**来源**：`~/gongshangzheng.github.io/.agents/skills/read-article/`（SKILL.md 573 行 + phases 3 篇 + subagents 14 个 + references 3 篇 + scripts 1 个）。其 Phase 1 抽取（arXiv source 优先 → HTML → PDF 降级）、Phase 2 四路并行分析、Phase 3 导航索引（索引≠总结）、质量底线（篇幅/表格/公式/超参数硬指标）可直接借鉴。

**本库已核实的约束**（决定适配方案）：

| 约束 | 事实 | 影响 |
|------|------|------|
| 后端 frontmatter schema | `get_doc_detail` 只返回 `title/author/date/tags/summary/id`，其它键被丢弃（`server/routers/management.py`） | 论文元信息不能放 frontmatter，须进正文表格；**不改后端** |
| 公式渲染 | `MarkdownRenderer.vue` 只挂 `markdown-it-task-checkbox` + mermaid，**无 KaTeX/MathJax** | 公式不能写 LaTeX 期待渲染，须代码块 + 符号表 |
| 静态资源 | `server/main.py` 原本无 StaticFiles 挂载 → 由 `add-doc-image-assets` 补上 `/api/management/docs-assets/` 服务 `management/docs/_assets/` | 笔记可落图（本 skill 依赖该 change） |
| 文档目录 | `GET /management/docs` 递归 `os.walk`，支持子目录 slug（如 `architecture/api-design`） | 笔记可放 `management/docs/notes/` 并被列表/TOC 正常识别 |
| 文档体系 | `docs-system`（已归档）确立：文档登记表唯一权威 + 双层流程（体系级总 Change / 单篇 `docs-<slug>`）+ design 先行 | 每篇新笔记 = 一个单篇 change，正文前须过 structure-design 审核 |
| sidecar | `{slug}.json` 承载 `changelog/progress/appendix/related`，`get_doc_detail` 一并返回 | 笔记的演进/进度/参考不进正文 |
| 忽略规则 | `.gitignore` 无 `.cache/` | 需新增，避免素材污染 git |

## Goals / Non-Goals

**Goals:**

- 一条可复用的"论文 → 精读笔记"流水线，产出与本库 wiki 格式**原生兼容**的 markdown
- 笔记能嵌入论文原图（架构图/结果曲线），图题规范、体积受控
- 结构先审后写：change 的 `design.md` 是审批核心，**未确认不得写正文**
- 素材可追溯：每条关键结论能指回 raw 素材位置
- 素材与产物分离：素材留在 gitignored 工作区，只有笔记与配图进 wiki

**Non-Goals:**

- 不做 HTML 博客/发布/邮件/站点 hub/交叉回链（read-article Phase 5–9 的站点专属部分）
- 不引入 KaTeX（公式仍用代码块+符号表）、不改后端 frontmatter schema（均列为后续可选）
- 不自行实现图片基础设施：静态端点与 figure 渲染由 `add-doc-image-assets` 提供，本 change 只用不改
- 不替代 `papers` 模块的搜集/分类职责；本 skill 只处理"已在手上的具体论文"
- 不做多篇综述聚合（`academic-research` 那种批量路线）——v1 只单篇

## Decisions

### D1: 流程顺序反转——素材在前，change 在后

read-article：Phase 0（OpenSpec 门禁，先建 change）→ 抓素材 → … → 按已批准大纲落笔。
本 skill：**Phase 1 抓素材 → Phase 2 并行分析 → Phase 3 导航索引 → Phase 4 建 change（大纲基于真实素材）→ Phase 5 汇报并等确认 → Phase 6 写正文**。

- 理由：大纲的可行性取决于实际抓到的料（论文可能缺训练细节、无代码仓库、图表不可得）。先建 change 会写出"承诺了却没有依据"的节；反过来，则大纲的每一节都能标注具体素材出处
- 代价：若用户最终不认可结构，已消耗抓取成本——用"素材可复用"抵消（同一 slug 二次精读直接复用 raw）

### D2: 笔记落点与登记方式——`notes/` 子目录 + 类目行登记

- 路径：`management/docs/notes/{slug}.md`，sidecar `management/docs/notes/{slug}.json`
- slug 规则沿用 read-article：`<论文关键词>-<年份>`（`maskgit-2022`、`attention-2017`），小写连字符
- 登记表**不逐篇编号**，只加一行类目：`| — | notes/* | 论文精读笔记 | 单篇论文的深度精读笔记（不在 wiki 编号体系内） | docs-notes-<slug> |`
  - 理由：编号体系（1、2、3…）适合少量长期维护的规范文档；论文笔记会持续增长到几十上百篇，逐篇编号会淹没体系、且引用重映射成本高。参照现有 `papers/docs/*`、`evaluation/docs/*` 的"不在编号体系内"处理
- 单篇 change 命名：`docs-notes-<slug>`（如 `docs-notes-maskgit-2022`）

### D3: markdown 适配点（逐条）

| 维度 | read-article（HTML 站） | 本 skill（本库 wiki） |
|------|------------------------|---------------------|
| 元信息 | frontmatter `paper_*` 字段 → 构建系统渲染 info-box | **正文顶部「论文信息」表格**（后端 schema 不含 paper_*，改后端不在本 change 范围） |
| 公式 | MathJax 渲染 LaTeX | **代码块**保留 LaTeX 源码 + **符号表**（符号/含义/取值），正文用自然语言解释公式含义。代码块保留原式便于复查 |
| 图片 | 下载原图 → WebP → 本地 assets | **落图**：抽取/下载原图 → 裁剪留白（可选）→ 压缩转 WebP → `management/docs/_assets/<slug>/` → 正文用 `![图 N · 说明](/api/management/docs-assets/<slug>/fig-N-xxx.webp)`（alt 兼作图题，渲染为 figure）。资源规范：≤1600px / 质量 82 / 单文件 ≤500KB / 单篇 ≤5MB |
| 图表 | HTML table + `.table-wrap` | markdown 表格（本库渲染正常）；宽表拆列或改纵向"项目/值"两列 |
| 流程图 | inline HTML/SVG | **Mermaid**（本库已支持），用于 pipeline / 时序 / 模块关系 |
| 层级 | `.ch` 顶层 + `h3 section-title` | `##` 顶层 + `###` 次级（DocPage TOC 取 h2/h3；避免 h4 以下，TOC 不显示） |
| 内部链接 | 站点路由 + `#key#` 引用 | `[[slug]]` / `[[slug\|label]]`（子目录 slug 可含 `/`）、任务链 `[[proj#tN]]` |
| 元数据落位 | frontmatter + info-box | frontmatter 仅 6 字段；演进/进度/附录/相关 → **sidecar json** |
| 篇幅口径 | 按 HTML 正文总字数 | 同口径按 markdown 正文字数（中文按字符计） |

### D4: 素材工作区（gitignored）

```
.cache/article-note/<slug>/
├── raw/
│   ├── sources/            # <slug>.md（TeX/HTML 转成的正文）、<slug>.json（结构化）、extraction-log.md
│   └── figures/            # 配图工作区：原图 + figures-manifest.md（编号/图题/来源/目标文件名）
├── analysis/               # Phase 2 按需启用的分析产出（background.md / methodology.md / ...）
└── synthesis.md            # Phase 3 导航索引
```

- 配图流转：`raw/figures/`（工作区，可含未采用的候选图）→ 筛选/裁剪/转 WebP → `management/docs/_assets/<slug>/`（交付，随 git 入库）
- `.gitignore` 增 `.cache/`
- 素材**永不**进 `management/docs/`；笔记正文里引用素材时用 `（素材：analysis/methodology.md §3.2）` 这类工作区相对指针，便于回查（不进最终交付内容）

### D5: 主 agent 优先、按需委派 subagent（14 → 7 个分析 lane）

这 7 个文件是**可复用的分析模板**，不是必须全部启动的固定流水线。主 agent 负责完整闭环：判断复杂度、准备素材、选择委派任务、汇总结果、处理冲突、生成 OpenSpec change、等待用户确认并撰写最终笔记。

| Lane | 适用场景 | 输出要点 |
|------|------|---------|
| `background.md` | 需要补领域背景、作者团队或影响时 | 领域脉络、作者/团队来源、社区影响、被引/热度 |
| `methodology.md` | 方法复杂、公式较多或需要独立复核时 | 架构逐模块、关键推导与损失函数、与已有方法的机制区别 |
| `experiment.md` | 实验表格多、数字密集或需要核对结果时 | 实验配置、超参数具体数值、主结果/消融、失败案例、训练成本 |
| `terminology.md` | 术语密集、符号较多或公式容易混淆时 | 术语中英对照 + 符号表 |
| `citation.md` | 需要补充研究脉络和前置工作时 | top 3–5 前置工作、与本文差异、后续影响 |
| `code-analysis.md` | 有代码仓库且用户关心复现时 | 仓库结构、关键实现与论文的一致性/偏差、复现要点 |
| `image-collection.md` | 图片对理解结论有帮助时 | 候选图清单、图题、来源锚点、候选文件、价值判断与笔记节号映射 |

#### 委派模式

- `direct`（默认）：主 agent 独立完成，适合短文、材料完整或问题边界清晰的论文。
- `assisted`：主 agent 委派 1–3 个相对独立且耗 token 的 lane，适合需要局部深挖的论文。
- `deep`：主 agent 并行委派多个互不依赖的 lane，适合长论文、复杂实验、代码复现或配图较多的论文。

委派时应优先选择可独立读取同一份 raw 素材的任务，例如 `methodology`、`experiment`、`terminology`、`image-collection` 可以并行；`code-analysis` 仅在代码仓库存在时启用。主 agent 不应为了凑数启动 lane，也不应让多个 lane 重复总结同一问题。

#### 委派边界

subagent 只能阅读素材、提取事实、标记来源位置、指出矛盾/缺口并提出结构建议；不得创建 OpenSpec change、修改最终笔记、写入 `management/docs/notes/` 或绕过用户确认。所有 subagent 输出统一采用“事实 + 来源指针 + 不确定性”格式，写入 `.cache/article-note/<slug>/analysis/`。主 agent 必须综合而非机械复制；若输出冲突，须回到 raw 素材核查并在 `synthesis.md` 标注。

**不迁移**：`review-html-format.md`（HTML 专属）、`method-writing/experiment-writing/conclusion-writing`（博客分段写作器，本 skill 由主 agent 统一撰写）、`problem-definition/review-fidelity/review-completeness`（并入 methodology / 质量底线检查）。

### D6: change 的 design.md 规范（**审批核心，必须详细**）

Phase 4 生成的 `openspec/changes/docs-notes-<slug>/design.md` 必须含以下**全部**字段，缺项视为未完成：

1. **论文速览**：标题 / 作者与单位 / venue 与年份 / arXiv id / 代码仓库 / 原文链接
2. **一句话价值主张**：这篇论文解决什么、核心手段是什么、结果如何（≤100 字）
3. **笔记结构大纲**（主体，逐节表格）：

   | 节号 | 标题 | 写什么（要点清单） | 素材来源（指向 analysis/raw 文件与行段） | 必备元素（表/公式/图/代码/Mermaid） | 字数参考 | 缺料与替代 |
   |---|---|---|---|---|---|---|

4. **口径与取舍**：哪些节刻意略写/省略及理由（如无代码仓库、论文未披露训练细节）
5. **图表公式清单**：预计的表格（含列定义）、公式（编号 + 符号表）、Mermaid 图、图说明块——**逐项列出**，便于用户直接判断"该讲的有没有讲"
6. **引用关系**：与该论文相关的既有 wiki 文档/笔记的 `[[…]]` 链接计划；sidecar `related` 计划
7. **风险与待确认项**：素材缺口、存疑结论、需要用户裁决的口径问题

Phase 5 汇报格式（固定）：把大纲表格 + 图表公式清单 + 缺料/待确认项贴给用户，明确问一句"结构是否确认？确认后我按此写正文"。**未获明确确认，禁止写 `management/docs/notes/` 下任何文件**（唯一例外：用户明确说"直接写"）。

### D7: 标准笔记结构（Phase 6 的落笔骨架）

adapted 自 read-article 的 7-Part，按笔记形态重排为 10 节；每节的"可跳过"条件必须显式遵守：

| 节 | 标题示例 | 职责 | 必备元素 | 篇幅参考 | 可跳过 |
|---|---|---|---|---|---|
| **0** | 论文信息 | 元信息表（标题/作者/单位/venue/链接/代码） | 表格 | — | 否 |
| **1** | 一句话总结 | 价值主张 + 3–5 条核心贡献 | 列表 | 150–300 字 | 否 |
| **2** | 问题与动机 | 领域背景 → 核心矛盾 → 已有方法为何不行 → 本文 insight（含 motivation 实验数据） | 数据点 + 至少 1 张对比/动机图 | 400–700 字 | 否 |
| **3** | 方法精析 | 整体 pipeline → 逐模块 → 关键推导/损失 → 与已有方法的机制差异 | Mermaid 图 + ≥2 公式（代码块+符号表）+ **≥1 张架构原图** | ≥1000 字 | 否 |
| **4** | 训练与实现细节 | 数据 → 预处理 → 损失 → 优化 → **训练配置披露表（10 项逐项标注"已披露/未披露"）** → 训练成本 | 披露表 | 400–700 字 | 仅纯理论/无训练论文 |
| **5** | 推理与系统链路 | 输入准备 → 生成/解码 → 后处理 → 输出；实时/系统型论文必含 streaming | Mermaid 时序 | 300–600 字 | 非系统型论文 |
| **6** | 实验与结果 | 实验配置表 → 指标与基线 → 主实验 → 消融 → 失败案例 | 配置表 + ≥1 对比表（带数值）+ **≥1 张主结果图** | 600–1000 字 | 否 |
| **7** | 相关工作与定位 | 与 top 3–5 前置工作的差异（表格对比） | 对比表 | 300–500 字 | 否 |
| **8** | 局限与启发 | 作者自述局限 + 我的判断 + 可操作启发 | — | 300–500 字 | 否 |
| **9** | 术语与符号表 | 术语中英对照 + 符号表 | 两张表 | — | 否 |
| **10** | 相关文档 | `[[…]]` 内部链接（既有 wiki/笔记） | 链接列表 | — | 无相关文档时省略 |

写作节奏：2 建立动机 → 3 是核心最重 → 4/5 是工程细节 → 6 用数字说话 → 7/8 收束定位。每张表后必须有一句"这个数字/对比说明什么"。

**配图要求（全篇）**：常规论文 ≥3 张原图（架构 / 主结果 / 消融或可视化），综述/系统型论文 ≥4 张；每图必须配图题（`![图 N · 说明](url)`）并在正文中有对应解读（不能只丢图不说）；图的选择以"能替代一段文字"为标准，避免装饰性配图。

### D11: 落图流水线（Phase 1 采集 → Phase 6 入稿）

1. **采集**（Phase 1，`image-collection` subagent 主导）：按优先级取图——`arXiv source tarball 内嵌图（PDF/EPS/PNG/JPG）` → `arXiv HTML figure URL` → `用户提供的截图`（最高优先，若存在）→ 图表无法取到时，**不改画数据**，改用"表格重排"或"文字描述 + 原文锚点"
2. **筛选**：按"是否支撑结论"选图；候选未采用的图留在 `raw/figures/`，不进交付
3. **加工**：裁剪留白（可选，依赖 Pillow/pymupdf，缺则原图直用）→ 转 WebP（质量 82、最长边 ≤1600px）；Pillow 不可用时保留原格式（PNG/JPG 同样可显示）
4. **入稿**：拷入 `management/docs/_assets/<slug>/fig-<序号>-<语义>.webp`；正文用绝对 URL + alt 图题；核对单文件 ≤500KB、单篇 ≤5MB（超限先降质量/尺寸，仍超则在交付说明中标注）
5. **图题规范**：`图 N · <说明>`（N 按正文出现顺序全局递增）；同一图多子图时用 `图 N(a) · …` 形式，并在正文一次讲清

### D8: 撰写与 Review 门禁

- Phase 6 由主 agent 统一撰写（不再拆 writing subagent），逐节按 design 大纲推进
- 写完的自检（写进 SKILL.md 质量底线）：结构对齐大纲（逐节核对，偏离须先走 `openspec-update-change`）、来源可追溯、未披露项不臆测、`[[…]]` 链接真实存在、无 KaTeX 语法裸奔、Mermaid 可渲染、TOC 层级只用 h2/h3
- 结构与大纲不符时**回写 change** 再改稿，不默默偏离（对齐 docs-system 的双层流程）

### D9: 脚本与依赖

- `scripts/fetch-paper.py` 适配自 read-article 的 `fetch-arxiv-paper.py`，保留：arXiv source tarball 下载解压 → TeX（含 bib/figure caption/table）→ Markdown + 结构化 JSON + **配图抽取（定位 figure 环境与内嵌图片文件）** + `extraction-log.md`；PDF 降级用 `pdftotext -layout`（命令缺失则记录并提示）
- 配图后处理：`scripts/figures.py`（新增）——裁剪留白 + 转 WebP + 尺寸/体积校验；依赖 `Pillow`（可选 `pymupdf` 用于 PDF 取图，`numpy` 用于范围裁剪）；缺依赖时降级保留原图并打印提示，不中断流程
- 环境：Python 3 + `requests`/标准库；可选依赖列在 SKILL.md 的"环境依赖"节；失败一律落 extraction-log 并给出回源指针

### D10: 术语与命名

- skill 名 `article-note`（用户指定），目录 `.agents/skills/article-note/`
- 触发场景：用户给论文链接/PDF/标题并表达"精读/解读/做笔记/整理这篇论文"

### D12: 固定工作交给脚本，理解工作留给 agent

本 skill 增加一组确定性辅助脚本，用于处理目录初始化、素材抓取、图片转换、产物校验和交付检查。脚本不承担论文理解、结构决策、事实综合或用户确认。

#### D12.1 脚本职责

| 脚本 | 职责 | 是否允许写最终笔记 |
|---|---|---|
| `init-workspace.py` | 初始化 `.cache/article-note/<slug>/`、manifest 和日志骨架 | 否 |
| `fetch-paper.py` | 抓取 source/HTML/PDF、提取原始材料、图片与元信息 | 否 |
| `figures.py` | 图片检查、转换、发布到 `_assets/` | 只写图片资产，不写笔记正文 |
| `validate-analysis.py` | 校验分析文件、来源指针、lane 一致性和 synthesis 长度 | 否 |
| `validate-note.py` | 校验 Markdown、frontmatter、图片、链接和 sidecar | 否 |
| `check-delivery.py` | 汇总 OpenSpec、素材、笔记、资产和 Git 检查 | 否 |

#### D12.2 主 agent、subagent 与脚本边界

主 agent 负责选择 `direct / assisted / deep` 模式、判断是否委派、选择进入笔记的图片、综合事实与冲突、生成并解释 OpenSpec design、获取用户确认和撰写最终正文。

subagent 负责相对独立且耗 token 的素材分析：读取素材、提取事实、标记来源位置、指出矛盾/缺口并提出结构建议。subagent 不得创建 OpenSpec change、修改最终笔记、写入 `management/docs/notes/` 或绕过用户确认。

脚本负责可重复的文件操作、来源下载与格式转换、尺寸/体积/命名/路径校验，以及输出供 agent 消费的机器可读报告。脚本不自动决定论文贡献、不拼接正文、不选择全部图片、不补全未披露数据。

#### D12.3 脚本安全门禁

脚本 SHALL：

- 默认不覆盖已有文件、不删除工作区、不写入 `management/docs/notes/`；
- 不自动提交 Git、不自动确认 OpenSpec；
- 对网络失败、依赖缺失和解析失败写入日志并返回明确非零状态码；
- 提供 `--help`，支持 dry-run 或 check 模式；
- 对会写入 `_assets/` 的操作要求显式 `publish` 子命令或等价确认参数。

## Risks / Trade-offs

- [无公式渲染导致笔记表达力受限] → 代码块保留原式 + 符号表 + 自然语言解释；后续可选加 KaTeX（独立 change，须评估对既有文档的影响）
- [配图取不到/质量差（无关论文）] → 三级来源（source 内嵌图 → HTML figure URL → 用户截图）；实在无图时改为表格重排或文字+锚点，**不自行改画数据**，并在交付说明标注
- [仓库体积随配图增长] → 单文件 ≤500KB、单篇 ≤5MB、WebP+尺寸限制；超限降质量优先，仍超则标注（后续可选引入 git-lfs 或分离 assets 仓库，独立 change）
- [图片基础设施尚不存在] → 本 change 显式依赖 `add-doc-image-assets`（静态端点 + figure 渲染），实施顺序：先基础设施、后 skill
- [脚本误写或覆盖用户内容] → 默认只写 `.cache/article-note/`，发布图片必须显式执行 `figures.py publish`，笔记校验脚本只读，所有脚本默认不覆盖、不删除、不提交
- [素材抓取依赖网络/arXiv 可用性] → 三级降级（source → HTML → PDF）+ extraction-log 记录失败原因；全失败则中止并报告，不硬写
- [笔记量大后 wiki 列表变长] → 独立 `notes/` 子目录 + 不逐篇编号；DocPage 侧栏已支持目录树折叠
- [与 `papers` 模块职责重叠] → 明确边界：papers 管"找到并归档元信息"，article-note 管"读进去并沉淀笔记"；笔记可 `related` 指回 papers 条目
- [长流程 token/时间成本] → 默认 direct；对相对独立且耗 token 的分析按需并行委派 subagent；用索引式 synthesis（不复制内容）和确定性校验脚本控制主 agent 上下文，并允许用户只跑到 Phase 5 拿大纲

## Migration Plan

纯新增 skill 文件 + 两行仓库级改动（`.gitignore`、登记表类目行）。落地即生效，无迁移。回滚 = revert 提交（已产出的笔记不受影响）。

## Open Questions

（无——后续可选增强已在 Risks 中标注为独立 change）
