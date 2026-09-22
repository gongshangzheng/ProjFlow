## Context

- `documentation` spec 的「唯一权威」要求现在指向一张**只存在于归档 change** 的表（`openspec/changes/archive/2026-09-20-docs-system/design.md`）。
- `docs-system` 已归档 → 它的「体系级总 Change」角色事实上失效，新文档无处登记。
- 实测漏登记一行：`add-article-note-skill` 设计要求的 `notes/*` 类目行未加（该 change 的另一项 `.gitignore` 改动已落地）。
- 现有 wiki 文档：`management/docs/api-design-conventions.md`、`management/docs/git-workflow.md`（各有 sidecar json）。`management/docs/_assets/` 为图片资产目录（不参与文档扫描）。
- `notes/*` 由 `article-note` skill 产出（`management/docs/notes/<slug>.md`），目前尚未有笔记落地，属**前向声明行**。

## Goals / Non-Goals

**Goals:**

- 登记表有耐久、可稳定引用的位置。
- 补上 `notes/*` 行，使 `article-note` 的产出在体系中有归属。
- 让 AI/人都能一处找到「新增文档该登记到哪」。

**Non-Goals:**

- 不改编号体系（1、2、3…）与「笔记类不逐篇编号」的既有决策。
- 不改 `management/docs/` 的扫描、sidecar、渲染行为。
- 不重写已归档 change 的历史内容（只在原表处加一行指针）。
- 不引入新的校验脚本（登记表与实际是否一致，暂以人工/评审保证；spec 里已有对应 Scenario）。

## Decisions

### D1: 落点选 `openspec/registry.md`，而不是 `management/docs/` 下的 wiki 文档

- 理由 1：登记表是**决策系统的治理件**（它裁定「哪篇文档管什么」并绑定「单篇 Change」），与 `specs/`、`changes/` 同属一层，放在 `openspec/` 下语义正确。
- 理由 2：放进 `management/docs/` 会变成一篇**被服务的 wiki 文档**，需要给自己再登记一行（自指），并与产品文档混在文档列表里。
- 理由 3：不改 `management/docs/` 的目录即不改任何运行时行为。
- 备选：`openspec/specs/documentation/registry.md` —— `specs/<cap>/` 下混入非 `spec.md` 文件可能被 CLI 当作待校验 spec，风险高，不采用。
- 备选：`docs/`（仓库根）—— 本仓库 `documentation` spec 明确「根目录不设 `docs/`」，且 `openspec/` 才承载治理件，不采用。

### D2: 登记动作从「总 Change」改为「登记表」本身

原流程「先在总 Change `docs-system` 登记」在 `docs-system` 归档后不可执行。改为：**登记动作 = 直接编辑 `openspec/registry.md`**；涉及编号体系/职责边界规则本身的变更，仍走一个体系级 change。

- 理由：登记表就是权威，编辑权威本身不需要再开 change；否则又回到「登记表要登记自己」的循环。
- spec 的 `MODIFIED` requirement 明确写出这一点，避免下一个人再去找总 Change。

### D3: 归档 design 只加指针，不删原表

在 `docs-system/design.md` 的原表上方加一行：

```text
> 登记表已迁移到 `openspec/registry.md`（耐久位置），以那里为准；下表为 2026-09-20 归档时的快照。
```

- 理由：归档是历史记录，删内容会破坏可追溯性；加指针足以防止误用旧表。

### D4: 补 `notes/*` 行，并明确它是前向声明

| 编号 | slug | 标题 | 职责边界 | 单篇 Change |
|---|---|---|---|---|
| — | `notes/*` | 论文精读笔记 | 单篇论文的深度精读笔记（不在 wiki 编号体系内） | `docs-notes-<slug>` |

- 目前 `management/docs/notes/` 尚未创建（第一篇笔记落地时由 `article-note` 创建）。与 `papers/docs/*`、`evaluation/docs/*` 两个类目行同为「整类不编号」的处理方式。
- 因此 spec 的「表与仓库实际一致」Scenario 里把 `*` 结尾的类目行列为豁免。

### D5: `AGENTS.md` 顺带补「push 即部署」的时效说明

现有部署小节写了链路，但没写「文档是构建期编译的，改 md 也要 push 才生效」。这是容易踩的坑，一并写清。

## Risks / Trade-offs

- [登记表与磁盘文档漂移（新增 md 忘了登记）] → spec 的 Scenario 要求核对；本 change 不引入自动校验（值得，但属另一件工具活），在 `registry.md` 的登记规则里写明。
- [`openspec/registry.md` 被 CLI 误判] → 实施后跑 `openspec validate --all --strict` 确认 13 个 spec + 未归档 change 全部通过；若 CLI 报错则改放 `openspec/specs/` 之外的其他耐久位置并记录。
- [把登记动作从 change 移到文件，可能被理解为「降低门槛」] → `registry.md` 的登记规则保留「先登记、再开单篇 change、design 审核后才动笔」的完整流程，只是入口换了地方。

## Migration Plan

1. 新增 `openspec/registry.md`（表 + 登记规则 + 与 change 的关系）。
2. 改 `openspec/specs/documentation/spec.md`（MODIFIED requirement）。
3. `docs-system/design.md` 加迁移指针。
4. `AGENTS.md` 补登记表位置与「push 即部署」说明。
5. 验证：`openspec validate --all --strict`；登记表列出的 slug 与 `management/docs/` 逐一对照。
6. 归档本 change。
