# Proposal: document-pick-propagation（cherry-pick 双向传播实操方法入 skill）

## Why

今天以 cherry-pick 方式把 pet-action-recognition 的两个共享改进（cb76c36 sidecar、bafbe23 面板收起）port 回上游 ProjFlow，全程实证了一套可复用的操作方法。但 `.agents/skills/upstream-sync/SKILL.md` 只有"上游→下游"方向的 cherry-pick 工作流；"下游→上游 port 回"小节只写了半句且带着未解答的疑问注释（"下游 SHA 在上游重写后可见吗?"）。下次再遇到同类操作（无论哪个方向）都会重新踩坑：本地路径 fetch、混合 commit 的领域数据剔除、untracked 阻塞、import 级最小化、pick 后验证动作。

## What Changes

- **`.agents/skills/upstream-sync/SKILL.md`**：
  - "port 回上游"小节补全为完整实操流程：fetch 下游本地路径 → cherry-pick → 冲突分类解决（共享文件取 theirs / 领域数据 `git rm` / change 勾选文件取 ours）→ import 级最小化 → `[shared]` + 来源 SHA 标注 → 重启后端 → 勾选对应 change tasks → 浏览器验证
  - 以实证结论替换第 84 行疑问注释：嫁接历史下，fetch 之后下游 SHA 在上游直接可见可用（bafbe23 / cb76c36 已验证）
  - 补注意事项：目标库存在 untracked 同名文件会阻塞 cherry-pick（先提交入库）；混合 commit（共享代码 + 下游领域数据 + 下游 openspec 勾选）是常态而非例外
- **`AGENTS.md`**：开发规范/工作流处加一行指回 SKILL.md 的传播方法（不复制正文）
- 不改任何代码

## Capabilities

纯文档变更（agent skill 与说明），无 spec 级行为变更，`.openspec.yaml` 设置 `skip_specs: true`。

### New Capabilities

（无）

### Modified Capabilities

（无）

## Impact

- 修改：`.agents/skills/upstream-sync/SKILL.md`、`AGENTS.md`（各一小节/一行）
- 不影响：代码、openspec specs、其他 skill
- 读者：执行跨库共享改进传播的开发者与 AI Agent
