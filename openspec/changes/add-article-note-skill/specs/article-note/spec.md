# article-note（论文精读笔记）

## Purpose

把单篇论文/技术长文转成本库 wiki 格式的精读笔记：抓素材 → 并行深读 → 生成带详细结构大纲的 OpenSpec change → 用户确认 → 撰写 markdown 正文并登记。素材留在 gitignored 工作区，只有笔记进 wiki。

## ADDED Requirements

### Requirement: 素材抓取与来源优先级

skill SHALL 按 `arXiv source tarball → arXiv/会议 HTML → PDF` 的优先级抓取正文、结构（表格/公式/caption）与元信息，并 SHALL 把每次来源尝试的成功/失败与回源指针写入工作区 `sources/extraction-log.md`。

#### Scenario: source 可用时走首选路径
- **WHEN** 目标论文在 arXiv 且有 e-print source
- **THEN** 使用 source 提取正文与图表 caption，extraction-log 记录 source 成功、未触发降级路径

#### Scenario: 全部来源失败
- **WHEN** source、HTML、PDF 三条路径均失败
- **THEN** 中止流程并报告失败原因与已尝试的来源，不得凭标题臆造论文内容

### Requirement: 主 agent 优先、按需委派分析

skill SHALL 默认由主 agent 完成素材分析；对于相对独立且耗 token 的工作，MAY 按需委派 7 个分析 lane（背景 / 方法 / 实验与数据 / 术语与符号 / 引用链 / 代码分析 / 配图采集）中的一个或多个。委派结果 SHALL 写入工作区 `analysis/`，并包含事实、来源指针和不确定性。主 agent SHALL 综合结果并处理冲突，不得机械复制 subagent 正文。

#### Scenario: 简单论文直接分析
- **WHEN** 论文较短、素材完整且问题边界清晰
- **THEN** 主 agent 使用 direct 模式，不要求启动 subagent，仍生成可追溯的 synthesis 或分析索引

#### Scenario: 独立工作并行委派
- **WHEN** 论文方法、实验和配图分析相互独立且耗费较多上下文
- **THEN** 主 agent 可并行委派对应 lane，以减少主流程 token 消耗；各 lane 不得写最终笔记或 OpenSpec change

#### Scenario: 有代码仓库
- **WHEN** 论文附带 GitHub 仓库且任务需要复现或实现核对
- **THEN** 启用 `code-analysis` lane，产出仓库结构、关键实现与论文的一致性/偏差

#### Scenario: 无代码仓库
- **WHEN** 论文无公开代码
- **THEN** 不启用 `code-analysis` lane，并在 synthesis 中标注该维度缺失

### Requirement: 确定性流程脚本

skill SHALL 提供脚本处理工作区初始化、来源抓取、图片转换与发布、分析产物校验、笔记校验和交付检查；脚本 SHALL 不负责论文理解、结构决策、正文生成或用户确认。

#### Scenario: 初始化工作区
- **WHEN** 主 agent 开始处理新论文
- **THEN** 可运行 `init-workspace.py` 创建 `.cache/article-note/<slug>/` 的固定目录、manifest 和日志骨架，默认不覆盖已有文件

#### Scenario: 校验分析与笔记
- **WHEN** subagent 分析或主 agent 笔记完成一个阶段
- **THEN** 可运行 `validate-analysis.py` 或 `validate-note.py` 检查来源指针、结构、frontmatter、图片 URL、标题层级、内部链接和 sidecar，而不修改正文

#### Scenario: 发布图片
- **WHEN** 主 agent 明确选择候选图片进入笔记
- **THEN** 显式运行 `figures.py publish` 将合格图片写入 `management/docs/_assets/<slug>/`；脚本校验尺寸和体积，不自动选择图片或写笔记正文

#### Scenario: 交付检查
- **WHEN** 用户确认结构且正文、图片和 sidecar 均准备完成
- **THEN** 可运行 `check-delivery.py` 汇总 OpenSpec、素材、笔记、资产和 Git 检查，并以非零状态码报告失败项

### Requirement: 导航索引不等于再总结

skill SHALL 生成 `synthesis.md`，内容限定为：事实位置索引、跨文件交叉引用、矛盾标注、写作分配建议；SHALL NOT 复制或压缩 `analysis/` 的正文内容。

#### Scenario: 索引保持简短
- **WHEN** 6 份分析产出齐备
- **THEN** `synthesis.md` 通常 200–500 字；若超过 1000 字视为在复制内容，需重写为指针式索引

### Requirement: 先生成 change 并汇报结构，确认后方可撰写

skill SHALL 在分析完成后、撰写正文前生成单篇 change `docs-notes-<slug>`，其 `design.md` SHALL 包含：论文速览、一句话价值主张、逐节笔记结构大纲（含每节要点、素材来源、必备元素、字数参考、缺料与替代）、口径与取舍、图表公式清单、引用关系计划、风险与待确认项。skill SHALL 向用户汇报该结构并等待**明确确认**；未获确认 SHALL NOT 在 `management/docs/notes/` 下写入任何文件。

#### Scenario: 结构未确认
- **WHEN** change 已生成并向用户展示了结构大纲，用户尚未确认
- **THEN** 不创建或修改 `management/docs/notes/**` 下的任何文件

#### Scenario: 用户明确确认
- **WHEN** 用户确认结构（或明确要求直接撰写）
- **THEN** 按已确认大纲撰写正文

### Requirement: 正文结构遵循标准骨架

笔记正文 SHALL 采用标准 10 节骨架（论文信息 / 一句话总结 / 问题与动机 / 方法精析 / 训练与实现细节 / 推理与系统链路 / 相关工作与定位 / 局限与启发 / 术语与符号表 / 相关文档），并按各节声明的可跳过条件裁剪；标题层级 SHALL 只用 `##` 与 `###`。

#### Scenario: 纯理论论文缺训练细节
- **WHEN** 论文无训练环节（如纯理论分析）
- **THEN** 省略「训练与实现细节」节，并在 change design 的「口径与取舍」中记录该裁剪

#### Scenario: 层级规范
- **WHEN** 撰写笔记正文标题
- **THEN** 顶层用 `##`、次级用 `###`，不出现 `####` 及更深层级

### Requirement: 笔记格式与本库 wiki 约定一致

笔记 SHALL 落于 `management/docs/notes/{slug}.md`，frontmatter 只含后端支持的 `title/author/date/tags/summary`（可选 `id`）；论文元信息（arXiv id / venue / 代码仓库 / 原文链接）SHALL 以正文「论文信息」表格呈现；内部链接 SHALL 使用 `[[slug]]` / `[[slug|label]]` 语法；演进、进度、附录、相关文档 SHALL 写入同名 sidecar json 而非正文。

#### Scenario: 元信息落位
- **WHEN** 撰写笔记 frontmatter 与开头
- **THEN** frontmatter 不含 `paper_*` 等后端不支持的字段，论文元信息出现在正文表格中

### Requirement: 配图流水线与落图规范

skill SHALL 采集论文原图并落入 `management/docs/_assets/<slug>/`，正文以 `![图 N · 说明](/api/management/docs-assets/<slug>/<file>)` 引用；图片 SHALL 满足 WebP 格式、最长边 ≤1600px、单文件 ≤500KB、单篇 ≤5MB；常规论文 SHALL ≥ 3 张图且每图在正文中有对应解读。

#### Scenario: 从 source 抽取原图
- **WHEN** arXiv source tarball 内含 figure 图片文件
- **THEN** 抽取并挑选支撑结论的图，转 WebP 落入 `_assets/<slug>/`，正文以绝对 URL + 图题引用

#### Scenario: 无法获取原图
- **WHEN** source、HTML、用户截图三路均取不到某关键图
- **THEN** 改用表格重排或文字描述 + 原文锚点链接，并在交付说明中标注缺图；不得自行编造或改画数据

#### Scenario: 转换依赖缺失
- **WHEN** 环境无 Pillow 无法转 WebP
- **THEN** 保留原格式（PNG/JPG）落盘并打印提示，不中断流程

### Requirement: 公式的表达约束

因本库 MarkdownRenderer 不渲染 LaTeX，skill SHALL 把公式写成代码块保留原式，并配套符号表与中文解释。

#### Scenario: 表达核心公式
- **WHEN** 笔记需要呈现论文核心公式
- **THEN** 公式以代码块给出，并配套符号表（符号/含义/取值）与自然语言解释，不写期望被渲染的裸 LaTeX

### Requirement: 素材与产物分离

抓取与分析素材 SHALL 存放于 gitignored 工作区 `.cache/article-note/<slug>/`；`management/docs/notes/` 下 SHALL 只含笔记正文与 sidecar。

#### Scenario: 不污染 wiki 目录
- **WHEN** 流程结束
- **THEN** `management/docs/notes/` 下不存在 raw 素材、分析产出或 extraction-log

### Requirement: 结构与大纲偏离须回写 change

撰写过程中若需增删节次或改变叙事顺序，skill SHALL 先通过 `openspec-update-change` 回写 change 的笔记结构大纲，再修改正文；SHALL NOT 静默偏离已确认的大纲。

#### Scenario: 发现大纲缺一节
- **WHEN** 撰写时发现缺少「失败案例」讨论有必要独立成节
- **THEN** 先更新 change 的 design 大纲并经确认，再改正文

### Requirement: 质量底线可核查

skill SHALL 在交付前逐项核对质量底线，至少包含：素材来源可追溯（关键结论指向 raw 位置）、未披露项显式标注「未披露」而非臆测、`[[…]]` 链接指向真实存在的文档或任务、Mermaid 可渲染、篇幅达到各节参考下限或说明原因。

#### Scenario: 论文未披露训练硬件
- **WHEN** 训练配置披露表中某配置项原文未给出
- **THEN** 该项标注「未披露」并说明原文未给出，不填写推测值
