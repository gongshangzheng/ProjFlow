## Context

- 上游排序链实现：`server/config.py:DOCS_FOLDER_ORDER` + `server/routers/management.py:_doc_sort_key`（文件夹优先级 → `order` → `id` → `date` 降序 → `slug`）。
- `web/scripts/build-docs-data.mjs` 复刻了同一条链（静态文档数据用）。因此 `order` 的正确性同时影响**运行时接口**与**GitHub Pages 静态产物**两处排序。
- 现状：`management/docs/` 只有 2 篇文档、均无 `order`；契约有、工具无。
- 来源：下游 `digital-human` 的 `.agents/skills/documentation/scripts/docs_order.py`（该文件在其仓库**未跟踪**，属本地新增）。
- 上游 skill 目录现状：`.agents/skills/documentation/` 下只有 `SKILL.md` 与 `references/mermaid-cheatsheet.md`。
- `.gitignore` 已忽略 `__pycache__/`（脚本运行不会污染仓库）。

## Goals / Non-Goals

**Goals:**

- 上游具备维护 `order` 的安全工具（默认不写盘、写入后校验、可回滚）。
- 把 digital-human 在实践中总结的 `order` 约定与 `related` 约束补进上游 skill。
- 明确的交付检查清单，避免「改完就提交」。

**Non-Goals:**

- 不整体替换上游 `documentation/SKILL.md`（下游版本 83 行，缺上游的会议纪要/模板/风格/正文零历史信息等节）。
- 不把领域专属内容（子目录名、人名默认值、digital-human tag）带进上游。
- 不改后端排序逻辑、不加 spec 要求、不碰 `web/`。
- 不改动下游仓库（digital-human 保留其领域化版本）。

## Decisions

### D1: 工具原样移植，仅做「上游化」的最小改动

保留：dry-run 默认、整数空位优先、`--shift` 语义、`renumber` 步长、重复值拒绝、多条 `order:` 行拒绝、写入后 `_validate_written_frontmatter`、单文件回滚、排序键与后端同源。

改动：

| 项 | 原因 |
|---|---|
| `--author` 由默认 `汤问` 改为**必填** | 上游通用脚手架不得在生成文件时硬编码人名；`author` 是 frontmatter 必填项，工具不应编造 |
| docstring/`--help` 里的示例路径改为上游语境 | 示例带 `数字人概述` 会把领域概念写进共享技能 |
| 新增文件模板里的 `tags: []` 保持 | 原版已是空数组，无领域值 |

- 备选：`--author` 默认空串 —— 会生成 `author:` 为空、违反必填约定且难以察觉；必填更安全，不采用空串方案。
- 备选：不移植、上游手写一个更简单的工具 —— 下游这个已覆盖 `list/insert/renumber` 且带安全网，重写等于放弃已验证的实现，不采用。

### D1b: 保留「重复 `order` 不自动修」的保守行为

实测：目录内存在重复 `order` 时，`list` 返 2 并打印 `DUPLICATE`，`renumber --apply` 也**拒绝执行**（返 2、不改任何文件），必须显式 `--force`。

- 理由：重复值往往是「手工改动出错」的信号，静默重排会掩盖问题并连带改动其它文档的顺序；显式 `--force` 强制操作者先确认。
- 因此实施时**不**把 `renumber` 描述成「自动修复重复」，skill 的示例也照此写。
- 编写 tasks 时我曾把预期写成「规范化成功」，验证后已更正——这条记在案，避免后人误以为工具会自动兜底。

### D2: 只补三条约定 + 交付检查，不搬下游整篇结构

下游 skill 是「门禁 + 落点 + 元数据 + 顺序工具 + 内容约定 + 公式/Mermaid + 交付检查」的紧凑结构；上游 skill 已更细（含会议纪要、模板、风格、正文零历史信息、章节归属）。本次**只新增上游缺的**：

1. `order` 用 10/20/30 空档
2. sidecar `related` 项必须是对象（含 `slug` + `title`）
3. 交付检查清单

- 理由：skill 合并过一次（`merge-doc-writing-into-documentation`）刚消除「同一件事写两处」；现在再按下游结构重排上游，等于引入第二次大改与新的漂移面。
- 放置：`order` 约定进 `§2.1 文件规范`（它讲 frontmatter）；`related` 约束进 sidecar 相关处；工具进新开的一节（放在 `§2` 之后、`§3 Mermaid` 之前）；交付检查放文末。

### D3: 不为「order 唯一」加 spec 要求

工具会拒绝重复 `order`，但**后端并不强制**——它只按值排序，重复值由 `slug` 兜底。把「唯一」写进 `docs-page-content` 会造出一条系统行为无法验证的假契约。

- 决策：唯一性只作为**工具侧输入校验**与写作约定存在，spec 不动。

### D4: 验证在临时目录做写入，不在本仓库 docs 上试写

`insert --apply` / `renumber --apply` 会真实创建/改写文件。验证时把 `management/docs/` 复制到临时目录再跑 `--apply`，本仓库只跑 `list` 与 `insert`（不带 `--apply`）的 dry-run。

- 理由：验证不能污染待提交的工作区；dry-run 与 `--apply` 走的是同一套计划函数，dry-run 覆盖了计划正确性，临时目录覆盖了写盘与回滚。

## Risks / Trade-offs

- [移植的脚本与上游排序链漂移] → 脚本的 `_sort_key` 注释已声明与 `management.py:_doc_sort_key` 同源；在 skill 的工具节里写明「若后端排序链变更，此脚本需同步」，并在验证中实测一次顺序输出与接口一致（本仓库 2 篇文档、均无 order，顺序应与 `GET /api/management/docs` 相同）。
- [`--author` 必填改变了下游的调用方式] → 属预期（下游自行保留其默认值版本或传 `--author`）；proposal 已声明上游化改动。
- [新增脚本被误当运行时依赖] → skill 节里写明「仅写文档时手工调用，服务运行不依赖它」。
- [脚本写入破坏 frontmatter] → 已有写入后校验 + 单文件回滚；沿用不动。

## Migration Plan

1. 复制脚本 → 上游化改动（`--author` 必填、示例路径）。
2. `SKILL.md`：新增「文档顺序工具」节 + `order` 空档约定 + `related` 对象约束 + 交付检查。
3. 验证：`--help` 可用；`list` 输出与后端顺序一致；临时目录跑 `insert --apply` 与 `renumber --apply` 并检查写入/回滚；本仓库 `git status` 干净。
4. 提交（`[shared]`）；归档。
5. 回滚：revert 提交；脚本对文档的写入可用 git 恢复。
