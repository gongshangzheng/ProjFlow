## Context

- `MarkdownRenderer.vue` 已实现 `$...$` / `$$...$$` → KaTeX（`add-latex-math`，已归档），契约落在 `docs-page-content` 的 4 条要求上（该 spec 第 66 行起）。
- `docs-page-content` 的其余 5 条要求（文内锚点、链接行为、`order` 字段、排序链兜底、文件夹顺序）与数学无关。
- `.agents/skills/documentation/SKILL.md` 的「1.5 公式（LaTeX）」节写有「契约见 `openspec/specs/docs-page-content/spec.md`」，迁移后需同步。
- `openspec/registry.md` 是 **wiki 文档**的登记表（编号/标题/slug/职责边界/单篇 Change），不含 capability，故本 change 不动它。

## Goals / Non-Goals

**Goals:**

- 数学渲染契约可被检索（`grep -r latex openspec/specs/` 应命中）。
- 迁移**零行为变化**：要求文本与 Scenario 逐条原样搬运。
- 修正技能里指向契约的路径。

**Non-Goals:**

- 不改 `MarkdownRenderer` 实现、不加新能力（公式编号、`\label`/`\ref`、`\(...\)` 支持等都不在本次）。
- 不拆 `docs-page-content` 的其它要求。
- 不把 capability 写进 `registry.md`（职责不同）。

## Decisions

### D1: 用 `REMOVED Requirements` + 新 capability 的 `ADDED Requirements`，而不是「就地改名」

OpenSpec 的 spec delta 语义里：把要求从 A 能力移到 B 能力，应按「A 移除 + B 新增」表达，removal 必须给出 Reason 与 Migration，归档时才会正确地从 A 的主 spec 删除、向 B 的主 spec 写入。

- 理由：直接编辑两个主 spec 会绕过 delta 记录，后人查不到「为什么迁移、迁到哪」。
- 备选：保留在 `docs-page-content` 只加索引注释 —— 检索问题依旧（`specs/` 下仍无 `math` 字样），不采用。

### D2: 新能力命名 `docs-math`（而非 `latex` / `docs-latex`）

- 理由：契约描述的是**数学渲染**（KaTeX 是把实现细节；将来若换渲染器，要求不变）；且与既有命名风格一致（`docs-page-content`、`docs-static-build`、`doc-image-assets` 都是「域 + 内容」）。
- 备选：`latex` —— 把实现技术写进能力名，不采用。

### D3: 迁移文本逐字照搬，只加一句来源说明

`docs-math` 的 Purpose 里注明「原为 `docs-page-content` 的一部分，由 `extract-docs-math` 拆出」，便于从主 spec 追溯。

- 理由：**重构不应夹带行为修改**，否则验证无意义；本次验证因此聚焦于「文本一致 + 检索命中 + 技能路径修正」。

## Risks / Trade-offs

- [归档时 REMOVED 与 ADDED 若文本不完全一致，会导致新 spec 内容与旧要求漂移] → 用脚本从 `docs-page-content` 主 spec **直接切片**生成 `docs-math` 的 ADDED 块（本次实施就是这么做的），并逐条核对数量与标题。
- [技能里的契约路径漏改，读者按旧路径找不到] → 列入验证：`grep -rn "docs-page-content" .agents/skills/` 应只剩与「文档页内容契约」本身相关的引用，公式节指向 `docs-math`。
- [有人以为迁移顺带改了行为] → proposal/design 均明确「零行为变化」，且不触碰代码。

## Migration Plan

1. 建 `docs-math`（ADDED 4 条，文本取自现主 spec）。
2. `docs-page-content` 声明 REMOVED 4 条（Reason + Migration）。
3. 改 `.agents/skills/documentation/SKILL.md` 公式节的契约路径。
4. 验证：`openspec validate --all --strict`；`grep -rl latex openspec/specs/` 命中 `docs-math`；两条主 spec 的要求标题集合 = 迁移前集合（仅归属变化）。
5. 归档 `extract-docs-math`（归档时 OpenSpec 会自动重建两条主 spec）。
6. 回滚：revert 提交；主 spec 由归档步骤重建，故需一并回滚归档提交。
