# Proposal: fork-init-guide（新库初始化适配 change）

## Why

ProjFlow（上游）已被多个库当脚手架初始化（infraredComp / pet-action-recognition / DigitalTeacher / ai-api-research），且踩过真实坑：ai-api-research 未替换端口与本库 3210/8809 冲突、`package-lock.json` 内网 registry 导致 `npm install` 反复回滚、本库是 OpenSpec 库而新库若不清理会继承 ProjFlow 的 context 与 changes 历史。这些适配点散落在 AGENTS.md（仅端口）与 upstream-sync SKILL.md（仅拓扑），新库初始化后靠人记必然遗漏。**本 change 本身就是适配指南**：它常驻上游、在上游永不执行；新库从本库初始化后的第一个动作，就是执行这个 change，把全部适配工作走完。

## What Changes

- **tasks.md 即新库适配清单**（本 change 的核心产出）：端口替换 → OpenSpec 目录适配 → 项目身份重命名 → 领域数据清理 → 依赖安装（registry 坑）→ `HIDDEN_KEYS` 功能隐藏（依赖已落地的 `add-menu-hidden-config`，commit `ff49e31`）→ 双服务自检 → 首次 commit → archive 本 change
- **发现机制**（不属本 change 任务，由上游直接维护）：`AGENTS.md` 与 `.agents/skills/upstream-sync/SKILL.md` 各一行入口说明——新库 agent 发现未执行的 `fork-init-guide` 时立即执行（已完成）
- 上游不产出独立参考文档（撤销此前 `references/fork-init.md` 方案——静态文档会过期，change 是带 checkbox 的活清单）

## Capabilities

纯流程模板 change，无 spec 级行为变更，`.openspec.yaml` 已设置 `skip_specs: true`。

### New Capabilities

（无）

### Modified Capabilities

（无）

## Impact

- 上游（ProjFlow）：本 change 常驻 `openspec/changes/fork-init-guide/`（任务 1.x–7.x 永远保持未勾选）；`AGENTS.md`、`.agents/skills/upstream-sync/SKILL.md` 各一行入口
- 新库：执行 tasks 时改动端口（`start_services.sh` / `web/vite.config.js` / `server/config.py`）、命名（`ProjFlow/projflow` 全局出现点）、清理领域数据、配置 `web/src/config/hidden.js`
- 依赖：`add-menu-hidden-config` 必须先在上游落地（已完成）
