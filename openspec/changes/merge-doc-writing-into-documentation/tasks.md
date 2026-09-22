## 1. 合并门禁内容到 documentation

- [x] 1.1 description：合并两类触发词（写/新增文档、结构调整、是否需开 change｜内容规范、模板格式、Mermaid、链接/图片/公式、风格），删除「见 doc-writing skill」指路句
- [x] 1.2 §1.2：把 design 要求补全为五要素（目标读者 / 完整章节结构 / 每节表达什么 / 与其它文档的引用关系 / 待调研知识点）
- [x] 1.3 §1.3：追加两条纪律——不编造领域背景（需调研的写进 design）；wiki 文档**先登记 `openspec/registry.md` 再动笔**
- [x] 1.4 §2.1 文件规范：追加「仓库根目录不设 `docs/`，wiki 文档必须落 `management/docs/`」
- [x] 1.5 顶部：删除「与 doc-writing skill 的分工」说明

## 2. 删除 doc-writing

- [x] 2.1 删除 `.agents/skills/doc-writing/`（内容已无独有部分）
- [x] 2.2 确认 `.claude/skills/doc-writing` 不存在（符号链接自动消失）；若为实体目录则一并删除
- [x] 2.3 核对 `management/SKILL.md` 的引用仍指向 `documentation`（无需改动）

## 3. 逐条核对合并清单（doc-writing 的 5 类内容都要有落点）

- [x] 3.1 范围与豁免（结构级 vs 内容级小修 + 唯一判据）→ 在 §1.1/§1.2 可见
- [x] 3.2 门禁四步（建 change → design → 审核 → 动笔）→ 在 §1.1/§1.2 可见
- [x] 3.3 design 五要素 → §1.2
- [x] 3.4 落点与登记 → §2.1（落点）+ §1.3（登记）
- [x] 3.5 不要做的事（5 条）→ §1.3/§1.4 覆盖（不写 design、凭记忆、改编号、正文写历史、编造背景）

## 4. 验证

- [x] 4.1 `grep -rn "doc-writing" .agents/ AGENTS.md README.md openspec/` 无命中
- [x] 4.2 `documentation` 的 description 同时含「写文档/新增文档」与「内容规范/模板格式」类触发词
- [x] 4.3 `ls .agents/skills/` 无 `doc-writing`；`test ! -e .claude/skills/doc-writing`
- [x] 4.4 行数对比：`documentation/SKILL.md` 行数不减少（除删除的 2 处指路句）
- [x] 4.5 `openspec validate --all --strict` 通过
- [x] 4.6 代码零改动（`git status` 不含 `web/`、`server/`）

## 5. 收尾

- [x] 5.1 提交（`[shared]`）
- [x] 5.2 归档
