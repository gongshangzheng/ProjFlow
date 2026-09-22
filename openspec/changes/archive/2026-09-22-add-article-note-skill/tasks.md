# Tasks: add-article-note-skill

## 1. skill 骨架与主流程

- [x] 1.1 建 `.agents/skills/article-note/` 目录树（`phases/`、`subagents/`、`references/`、`scripts/`）
- [x] 1.2 写 `SKILL.md`：frontmatter（name/description/触发场景）+ 模式 + Phase 1–6 总览 + 执行规则 + 质量底线 + 故障处理 + Python/依赖说明；明确"素材在前、change 在后、确认才写正文"的顺序（design D1）

## 2. phases/（5 篇，对应 Phase 1–5；Phase 6 撰写由 `5-writing.md` 承载）

- [x] 2.1 `phases/1-extraction.md`：slug 生成规则、工作区初始化（`.cache/article-note/<slug>/`）、三级来源优先级与命令、extraction-log 规范（design D4/D9）
- [x] 2.2 `phases/2-analysis.md`：7 个可选分析 lane 的分工、direct/assisted/deep 模式、按需委派规则、派发 prompt 模板与产出落点约定（design D5）
- [x] 2.3 `phases/3-index.md`：synthesis.md 的四个限定内容 + 「不复制内容」红线 + 长度红线（200–500 字，>1000 字判为失败）
- [x] 2.4 `phases/4-change.md`：单篇 change 生成步骤（`openspec new change docs-notes-<slug>`）+ **design.md 必含 7 字段模板** + 汇报话术 + 门禁（未确认不写正文）（design D6）
- [x] 2.5 `phases/5-writing.md`：按大纲逐节落笔 + markdown 适配细则（公式代码块+符号表 / 图说明块+锚点 / Mermaid / `[[…]]` / h2-h3 层级）+ 自检清单 + 偏离回写流程（design D3/D7/D8）

## 3. subagents/（7 个分析模板）

- [x] 3.1 适配移植 `background.md`、`methodology.md`、`experiment.md`、`terminology.md`、`citation.md`、`code-analysis.md`、`image-collection.md`（改编自 `~/gongshangzheng.github.io/.agents/skills/read-article/subagents/`，去掉站点专属要求，输出改为"事实 + 指针"以服务 synthesis 索引）
- [x] 3.2 每个模板含：frontmatter（name/description）、输入占位符、输出结构、硬性规则、好/坏例子（对齐本库 `.claude/agents/README.md` 的模板约定）
- [x] 3.3 `image-collection.md` 输出候选图清单（编号 / 图题 / 页面锚点 / 文件路径）与每图价值判断，并给"该图对应笔记哪一节"的建议

## 4. references/（3 篇）

- [x] 4.1 `references/note-structure-template.md`：10 节骨架逐节展开（职责 / 必备元素 / 篇幅参考 / 可跳过条件 / 写作节奏）+ 训练配置披露表 10 项必含清单 + 实验配置表列定义（design D7）
- [x] 4.2 `references/paper-section-guide.md`：论文各章节（Abstract/Intro/Related/Method/Experiments/Appendix）在不同分析维度下的利用方式（改编自 read-article 同名 412 行参考）
- [x] 4.3 `references/sidecar-guide.md`：`changelog/progress/appendix/related` 四字段的用途、写法与示例；说明"什么内容进正文、什么进 sidecar"

## 5. scripts/

- [x] 5.1 `scripts/init-workspace.py`：初始化 `.cache/article-note/<slug>/` 固定目录、`workspace.json`、manifest 和日志骨架；默认不覆盖、不删除，支持 `--check` / `--force`
- [x] 5.2 `scripts/fetch-paper.py`：适配 read-article 的 `fetch-arxiv-paper.py`——arXiv source 下载/解压、TeX→Markdown、结构化 JSON、**图文件定位与抽取**、extraction-log；默认只写工作区
- [x] 5.3 `scripts/figures.py`：inspect/convert/publish 子命令；裁剪留白 + 转 WebP（质量 82 / 最长边 ≤1600px）+ 单文件与单篇体积校验；publish 必须显式执行，缺 Pillow/pymupdf 时降级并提示
- [x] 5.4 `scripts/validate-analysis.py`：校验分析 lane、来源指针、文件引用、synthesis 长度、代码分析条件和配图清单，不修改分析文件
- [x] 5.5 `scripts/validate-note.py`：校验 frontmatter、10 节骨架、h2/h3 层级、公式表达、图片 URL/图号/资产、内部链接和 sidecar，不修改笔记
- [x] 5.6 `scripts/check-delivery.py`：汇总 OpenSpec validate、工作区、分析、笔记、图片、sidecar 和 Git 检查，以非零状态码报告失败项
- [x] 5.7 所有脚本支持 `--help`、明确退出码和 dry-run/check 模式；无可选依赖时记录降级原因，不自动写入 notes、不自动提交

## 6. 仓库级改动

- [x] 6.1 `.gitignore` 增加 `.cache/`
- [x] 6.2 在 `docs-system` 已归档的登记表处理方式基础上，把「论文精读笔记」类目行登记到本 change 的 design（含 `— | notes/* | ... | docs-notes-<slug>`），并说明不逐篇编号的理由（design D2）
- [x] 6.3 确认图片基础设施就绪（依赖 `add-doc-image-assets` 已实施）：`/api/management/docs-assets/` 可访问、`![图 N · 说明](url)` 渲染为 figure

## 7. 验证与提交

- [x] 7.1 skill 可被发现：`.agents/skills/article-note/SKILL.md` 存在且 frontmatter 合法（name/description 可解析）
- [x] 7.2 结构自检：SKILL.md 的 Phase 编号与 `phases/` 文件一一对应；references/subagents/scripts 的引用路径全部可达
- [x] 7.3 脚本与流程演练（可选，消耗较大）：运行脚本 `--help`、工作区初始化、分析/笔记校验；任选一篇短论文跑 Phase 1–5，确认生成的 change design 含 design D6 的 7 个字段、且汇报后停下等确认
- [x] 7.4 提交：`[shared] feat: 新增 article-note skill（论文精读笔记流水线，素材→分析→结构审批→markdown 笔记）`
