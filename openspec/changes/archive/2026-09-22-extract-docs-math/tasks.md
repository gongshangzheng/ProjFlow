## 1. 建立 docs-math capability

- [x] 1.1 从 `openspec/specs/docs-page-content/spec.md` 切片生成 `specs/docs-math/spec.md`（Purpose + 4 条 ADDED，文本逐字一致）
- [x] 1.2 Purpose 注明来源（`add-latex-math` 引入、`extract-docs-math` 拆出）

## 2. 从 docs-page-content 移除

- [x] 2.1 `specs/docs-page-content/spec.md` 写 `REMOVED Requirements`：4 条各附 Reason 与 Migration
- [x] 2.2 确认 docs-page-content 其余 5 条要求未出现在 delta 中（保持不动）

## 3. 技能里的契约路径

- [x] 3.1 `.agents/skills/documentation/SKILL.md` 公式节：`docs-page-content` → `docs-math`

## 4. 验证

- [x] 4.1 `openspec validate extract-docs-math` 通过
- [x] 4.2 `grep -rl "LaTeX\|KaTeX" openspec/specs/` 命中 `docs-math`（迁移后主 spec）
- [x] 4.3 两条主 spec 的要求标题集合与迁移前一致（只有归属变化，无内容增删）
- [x] 4.4 `grep -rn "docs-page-content" .agents/skills/` 中公式相关引用已改指 `docs-math`
- [x] 4.5 代码零改动：`git status` 不含 `web/`、`server/`

## 5. 收尾

- [x] 5.1 提交
- [x] 5.2 归档（OpenSpec 重建两条主 spec）并复核
