## 1. 建立耐久登记表

- [x] 1.1 新增 `openspec/registry.md`：迁移原表（`api-design-conventions` / `git-workflow` / `papers/docs/*` / `evaluation/docs/*`）并**补 `notes/*` 行**
- [x] 1.2 同文件写明登记规则（先登记 → 再开单篇 `docs-<slug>` → design 审核后才动笔）、编号体系说明、类目行（`*` 结尾）不编号的约定
- [x] 1.3 同文件声明与 OpenSpec 的关系（体系级规则变更走 change；日常登记直接编辑本表）

## 2. 修订契约

- [x] 2.1 `openspec/specs/documentation/spec.md`：MODIFIED「文档登记表为唯一权威」——指明位置 `openspec/registry.md`，登记动作改为编辑登记表，新增「表与仓库实际一致」Scenario
- [x] 2.2 `openspec/changes/archive/2026-09-20-docs-system/design.md`：原表上方加一行迁移指针（声明以 `openspec/registry.md` 为准，下表为归档快照）

## 3. AGENTS.md 补充

- [x] 3.1 登记表位置：说明「新增/调整 wiki 文档先改 `openspec/registry.md`」
- [x] 3.2 部署小节补「push 即部署」：`management/docs/*.md` 是构建期编译进 `docs-data.json` 的，改完必须 push（并等 CI 完成）才会在线上生效；线上只有文档页可用
- [x] 3.3 顺带写明「必须用 `npm run build`（pre/post 钩子）」已在原小节，确认无需重复

## 4. 验证

- [x] 4.1 `openspec validate --all --strict` 通过（确认 `openspec/registry.md` 未被 CLI 误判为 spec/change）
- [x] 4.2 登记表逐行对照磁盘：`api-design-conventions` / `git-workflow` 存在；`papers/docs/*`、`evaluation/docs/*`、`notes/*` 为类目行（豁免存在性）
- [x] 4.3 `grep -rn "docs-system" AGENTS.md`：确认指向登记表的说明可读、无自相矛盾
- [x] 4.4 工作区无意外改动（本次只动 `openspec/`、`AGENTS.md`）

## 5. 收尾

- [x] 5.1 提交并 push（push 会触发 Pages 重新部署，属预期）
- [x] 5.2 归档 `promote-docs-registry`
