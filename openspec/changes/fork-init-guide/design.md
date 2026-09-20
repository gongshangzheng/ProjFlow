# Design: fork-init-guide（新库初始化适配 change）

## Context

见 proposal.md — Why。事实约束：本库 = 四库拓扑的上游；新库通过嫁接上游 root 初始化，**会完整带走 `openspec/` 目录**（含上游的 config.yaml context、docs-system 等在途 change、archive 历史）；`add-menu-hidden-config`（`ff49e31`）已提供 `HIDDEN_KEYS` 部署级裁剪能力。

## Goals / Non-Goals

**Goals:**

- 新库初始化后"第一件事执行什么"有唯一权威答案：执行本 change
- 清单每项可执行、可验收、按依赖排序，agent 在新库可直接跑完
- 上游维护成本趋近于零：常驻模板，不需要随上游演进而重写（除非适配点本身变化）

**Non-Goals:**

- 不覆盖 git 嫁接操作本身（upstream-sync SKILL.md 已有，任务引用）
- 不做交互式初始化脚本/CLI（checklist + agent 已够）
- 不含 rsync 到 pet 服务器等个人部署流程

## Decisions

### D1: change-as-guide，而非静态参考文档

- 备选：`references/fork-init.md` 静态文档（此前方案）。放弃原因：文档无进度语义、无 openspec validate 约束、会与实际适配点漂移
- change 的 tasks.md 自带 checkbox 进度、按序执行、`openspec status` 可见；对 agent 而言"执行一个 change"是已有肌肉记忆（`openspec-apply-change`），零新概念

### D2: 常驻模板机制——上游永不执行，新库执行后归档

- 本 change 在上游永远 0/N 任务；任务 0（上游侧准备）单独成节并在上游勾选完成，与新库任务隔离
- **发现机制**（两层）：
  1. `AGENTS.md`（新库必然携带）初始化说明：发现未执行的 `fork-init-guide` → 立即执行
  2. `.agents/skills/upstream-sync/SKILL.md` 触发场景加"从上游初始化新库"
- 新库执行完毕 → `openspec archive fork-init-guide`（change 完成使命，退出 changes 目录），上游副本不受影响
- 不需要 openspec 原生"模板 change"特性——目录常驻 + 约定即可

### D3: 新库要清理上游遗留的 OpenSpec 内容

- 嫁接带走上游全部 changes（在途的 docs-system、已完成的 add-menu-hidden-config、archive/）与 config.yaml 的 ProjFlow context
- 任务 2 写死两条：① 重写 config.yaml `context`；② `openspec/changes/` 下**除本 change 外全部删除**（含 archive——上游历史随时可回上游仓库查）。"除本 change 外全删"的写法天然覆盖上游后续新增的 change，无需维护清单

### D4: 任务设计原则

- 每个任务 = 一个动作 + 一行验收（做什么才算完）
- 排序即依赖：端口 → OpenSpec → 命名 → 数据 → 依赖安装 → 功能隐藏 → 自检 → 归档
- 功能隐藏引用 `HIDDEN_KEYS`（`web/src/config/hidden.js`，可用 key 注释齐全），不重复列 key 表
- 危险操作（数据删除）限定路径白名单，避免误删共享脚手架文件

### D5: 上游侧入口不写入本 change 任务

- 入口指引（`AGENTS.md` 一行 + `SKILL.md` 触发场景/指引行）属上游日常文档维护，**直接提交**；本 change 的 tasks 只含新库执行内容，避免 change 在上游出现「部分完成」的歧义态
- `AGENTS.md`：启动服务一节的端口适配提示处追加一行「从本库初始化新库后，第一件事：在新库执行 openspec change `fork-init-guide`」
- `upstream-sync/SKILL.md`：frontmatter 触发场景 + 拓扑节末尾一行指引
- 两处均为纯指引文本

## Risks / Trade-offs

- [上游演进后清单过期（如新增第 4 处端口位置）] → 兜底：任务含"全局搜索旧端口/旧命名"步骤，漏项可被搜索法捕获；本 change 属共享脚手架层，适配点变更时应同步更新它（commit 加 `[shared]`）
- [新库 agent 忽略发现机制直接开发] → AGENTS.md 挂在端口提示旁（新库初始化最容易先撞到的问题），命中率高
- [用户在新库想保留上游某在途 change] → 任务 2 允许人工判断保留，但默认全删（YAGNI）

## Migration Plan

上游落地 = 本 change artifacts + AGENTS.md/SKILL.md 两行指引，一次 commit。无行为变更、无迁移、可 revert。

## Open Questions

（无）
