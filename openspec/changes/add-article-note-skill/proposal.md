# Proposal: add-article-note-skill（论文精读笔记 skill）

## Why

ProjFlow 的 `papers` 模块只做论文**搜集**（列表/分类/搜索），缺"读进去并沉淀"的能力。姊妹项目 `~/gongshangzheng.github.io` 有一套成熟的 `read-article` skill（Phase 1 素材抽取 + Phase 2 并行分析 + Phase 3 导航索引 + 结构大纲 + 撰写 + Review），但它面向该站的 **HTML 博客**形态（7-Part HTML、MathJax、本地配图、发布流水线），与本库的 **markdown wiki**（`management/docs/`）不兼容。本 change 把那套"抓素材 → 并行深读 → 生成结构 → 写正文"的方法论移植过来，去掉博客/发布专属部分，改为：**抓素材 → 分析 → 生成 OpenSpec change（含详细笔记结构大纲）→ 向用户汇报结构 → 用户确认后才写正文**，产出落进本库 wiki。

## What Changes

- 新增 skill `.agents/skills/article-note/`：论文/技术长文精读笔记流水线
  - `SKILL.md`：主流程（Phase 1–6）、模式、执行规则、质量底线、故障处理
  - `phases/`：素材抓取、并行分析、导航索引、**change 生成与结构汇报**、markdown 撰写
  - `subagents/`：7 个分析模板（背景调研 / 方法精析 / 实验与数据 / 术语 / 引用链 / 代码分析 / 配图采集），适配自 read-article 的 14 个
  - `references/`：笔记标准结构模板、论文章节利用指南、sidecar json 使用指南
  - `scripts/fetch-paper.py`：arXiv source（首选）→ HTML → PDF 降级抓取 + 配图抽取（裁剪留白 + WebP 转换）+ extraction-log
- **落图能力**：笔记正文嵌入论文原图 —— 图片落 `management/docs/_assets/<slug>/`，经 `/api/management/docs-assets/` 服务，以 `![图 N · 说明](url)` 渲染为 figure（依赖 `add-doc-image-assets`，本 change 不含后端/前端基础设施改动）
- **流程关键差异（本 skill 的核心特征）**：read-article 是"先建 change（Phase 0 门禁）再抓素材"；本 skill 是**先抓素材与并行分析，再据实际素材生成 change**，change 的 `design.md` 给出**详细笔记结构大纲**，向用户汇报后才写正文——避免"先承诺结构、后缺料"
- 产物落点：笔记 `management/docs/notes/{slug}.md`（+ sidecar `{slug}.json`），配图 `management/docs/_assets/{slug}/`，素材留在 gitignored 工作区 `.cache/article-note/<slug>/`
- `.gitignore` 增加 `.cache/`
- 文档登记表增加"论文精读笔记"类目行（不逐篇编号）

## Capabilities

### New Capabilities
- `article-note`: 论文精读笔记的素材抓取、并行分析、结构大纲生成与用户确认门禁、markdown 笔记产出与登记

### Modified Capabilities

（无——`documentation` 定义 wiki 文档通用规范，本 change 复用而不改其需求）

## Impact

- 新增：`.agents/skills/article-note/**`
- 修改：`.gitignore`（加 `.cache/`）、`openspec/changes/add-article-note-skill/design.md`（登记表类目行登记于本 change design）
- **依赖**：`add-doc-image-assets`（文档图片静态端点 + figure 渲染）——本 change 的落图能力建立在其之上，实施顺序为先基础设施后 skill
- 不影响：`server/`、`web/`（技能自身不改后端/前端代码）、既有 wiki 文档、`papers` 模块
- 归属：skill 属共享脚手架层 → 实施提交加 `[shared]` 前缀
- 环境依赖：arXiv 抓取需网络；配图转 WebP 依赖 Pillow（缺则降级保留原格式）；PDF 降级路径依赖 `pdftotext`（可选）
