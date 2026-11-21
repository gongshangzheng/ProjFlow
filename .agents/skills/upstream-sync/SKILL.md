---
name: upstream-sync
description: |
  ProjFlow 家族的上游／下游职责与同步指南。用于确认 Git 或脚手架关系、归属共享改进、把已验证的共享改动传播到适用下游。
---

# 上游 / 下游拓扑与责任分工

## 拓扑与同步依据

- **ProjFlow** 维护共享脚手架；`pet-action-recognition` 与 `children-face` 和它共享 Git 祖先 `159e4aa`。pet 还有自身的历史；各库同步前都应核对实际 `upstream` 与 merge-base，不以历史示例替代现状。
- **investement**、**digital-human** 和 **live2d-avatar** 的项目文档确认它们由 ProjFlow 脚手架派生，但它们有独立的 Git 根。不要假定它们配置了同一个 `upstream` 或者能直接合并。
- **CyberVerse** 不属于这个家族。退役项目名称只保留在历史记录中，不作为同步目标。

向下游传播共享改动时，只迁移适用职责和约定；保留各库的端口、路径、数据、技能定制与 Git 发布策略。若没有可用远端，维持本地改动，不替项目新建远端。

> 初始化新库时，参考上游 `openspec/changes/fork-init-guide` 的适配清单；在目标仓核对当前变更位置、适用的审批和归档流程。

## 责任分工（决定一个改动该落在哪）

| 范围 | 归属 | 典型路径 |
|------|------|----------|
| 共享全栈脚手架 | **上游** | `server/main.py`(app+CORS+router 挂载)、`server/config.py`(路径常量模式)、`server/utils/file_utils.py`、`server/parsers/markdown_table.py`(含空表修复)、`server/parsers/tasks_parser.py`(看板=项目树同源派生)、parser 模式、`web/` 脚手架(vite.config/api/request.js/layouts/MainLayout.vue/router/index.js/styles/)、`start_services.sh`、`AGENTS.md` 结构、management/papers/evaluation **模块结构**、`.github/workflows` |
| 共享 skills | **上游** | ProjFlow 家族复用的项目 skill（项目管理、Web 实现、本 upstream-sync 等）；全局通用工具不在家族仓库复制维护 |
| 宠物动作识别领域 | **pet-action-recognition（下游）** | `evaluation/`、宠物专属 router/views、pet-action-recognition-* skills |
| 领域数据 | **各下游自管，永不进上游** | `management/`(team/daily/...)、`papers/` 数据、`data/*.db`、`datasets/` |

**铁律**：
1. 下游改了**共享脚手架**（修 parser、改 MainLayout 等）→ **必须先 port 回上游**（上游提交），再由上游传播到兄弟库；下游**不直接**互相传共享改动。
2. **领域代码 / 领域数据永不进上游**——`benchmark/`、`evaluation/`、`datasets/`、`data/*.db`、`management/` 数据各库自管。
3. 共享改进的 commit message 加 `[shared]` 前缀，便于识别与 cherry-pick。

## 传播工作流

### 下游同步上游的共享改进（推荐 cherry-pick，精准）

```bash
# 在下游库（已 add upstream remote）
git fetch upstream                       # 拉上游最新
git log upstream/main --oneline          # 找 [shared] 改进 commit
git cherry-pick <SHA>                   # 精准搬一个共享改进
# 例: git cherry-pick abc1234
```

> 不要默认合并 `upstream/main`。共享祖先的下游也可能已大幅分叉；优先挑选具体的 `[shared]` 提交。只有脚手架关系、没有共同历史的库，应按目标基线移植并验证。

### 取上游的「部分文件」到下游（共享件，保留 git 血缘）

当上游的一个 `[shared]` commit 里**只有一部分**是下游要的（例如 evaluation 模块：上游有通用后端 + 共享前端视图，下游只取前端视图、后端要自己定制），**不要用 `cp`**——会丢 git 血缘，下游看不出文件源自上游。用 `git checkout upstream/main -- <path>` 取：

```bash
git fetch upstream
# 只取共享的前端视图/组件（带血缘 stage 进下游），后端 evaluation.py 下游自己写
git checkout upstream/main -- web/src/views/evaluation/ web/src/components/common/VideoModal.vue web/src/api/evaluation.js
# 下游定制的后端/配置：直接在下游写，不 checkout（会被上游通用版覆盖）
#   server/routers/evaluation.py  -> 下游接领域数据源(codecs/序列/results.json)
#   server/config.py 的 OUTPUTS_DIR -> 下游指 results/video/ 而非 evaluation/outputs/
```

**判别规则**：文件内容跨库**通用**（视图/组件/api 客户端/数据模板）→ `git checkout upstream/main -- <path>` 取；文件**绑定领域数据源**（router 读 results.json、列 codecs）→ 下游自己写。`cp` 只在「两库该文件已分叉、想手动合并」时用，且务必 commit message 注明源自上游哪个 commit。

> 注意：`git checkout upstream/main -- <path>` 取回的文件会**覆盖**工作区同名文件（用上游版本替换），所以只对「下游该文件应等于上游」的路径用；对已定制分叉的路径别用，否则丢下游定制。

### 下游改了共享脚手架 → port 回上游（上游侧操作）

```bash
# 在下游：先把改动整理成 [shared] commit（纯共享内容最好；混入领域数据也能处理，见下表）
git commit -m "[shared] fix: ..."

# 在上游：直接 fetch 下游仓库（本地路径即可，无需配 remote）
cd <上游工作树>
git fetch ~/pet-action-recognition main        # 或其他下游库路径
git cherry-pick <下游的 [shared] commit SHA>   # fetch 后对象与 SHA 直接可用
git commit --amend -m "[shared] <原信息>（pick 自 pet <SHA>）"  # 标注来源
```

嫁接只重写了下游自身的 commit SHA，不影响上游 pick：fetch 之后对象就在本地，cherry-pick 零障碍（实证：pet cb76c36 / bafbe23 → 上游 bd91ac2 / aacb342，2026-09-20）。旧方案（下游 `format-patch` → 上游 `git am`）仍可用，但已无必要。

**混合 commit 的冲突按文件归属分类解决**（下游 commit 混着领域数据是常态，不是例外）：

| 文件类型 | 解法 |
|---------|------|
| 共享脚手架（`server/`、`web/src/`、`start_services.sh`、共享 skill） | 取 theirs（无冲突则自动套上） |
| 下游领域数据（`management/` 数据、领域 docs、`results/`、`*.db`） | `git rm`，永不进上游 |
| 下游的 openspec change 勾选（tasks.md） | 取 ours（`git checkout --ours`），事后在本库对应 change 手动勾选并注明 pick 来源 |
| 冲突的 import 块 | 只留下游新代码实际用到的 import，弃下游特有残留（例：只取 `import json`，弃 datetime/hashlib/subprocess） |

**注意事项**：
- 上游存在 **untracked 同名文件会直接阻塞 cherry-pick**（报 "would be overwritten by merge"）——先把本库未入库文件 commit 掉再 pick。
- pick 含后端改动的 commit 后需**重启 uvicorn** 才生效；改完勾选本库对应 change 的 tasks 并浏览器实测。
- 多个 commit 有依赖（如面板收起叠在 sidecar 底座上）时，**按拓扑序连着 pick**，后面的才能干净套上。

上游落地后，再由各兄弟下游 `git fetch upstream && git cherry-pick <上游SHA>` 取回——形成"下游发现 → port 回上游 → 传播到所有下游"的闭环。

### 判断改动归属的快速决策

- 改的是 `server/main.py` / `config.py` / `file_utils.py` / `markdown_table.py` / `web/layouts/MainLayout.vue` / `start_services.sh` / 通用 skill？→ **上游**。
- 改的是 `benchmark/` / `evaluation/` / 领域 router/view / 领域 skill？→ **对应下游**。
- 改的是 `management/` 数据 / `papers/` / `data/*.db` / `datasets/`？→ **下游本地，不进任何远程共享**。

## 禁忌

- ❌ 下游间直接 cherry-pick 共享改动（绕过上游）。
- ❌ 把领域代码/数据推到上游（上游只放共享脚手架 + 共享 skill）。
- ❌ 在下游改共享脚手架后不 port 回上游（会导致兄弟库拿不到、长期分叉）。
- ❌ `git merge upstream/main` 不带审查（重叠文件冲突，易吞掉下游定制）。

## 经验沉淀（架构决策，供后人参考）

- **任务数据单源（2026-07-15）**：任务看板与项目树曾用两份冗余文件——`management/docs/tasks.md`（全局看板，3 段 markdown 表）+ `management/docs/projects/{slug}/tasks.json`（项目树，层级 JSON），schema 各异、手动双写易分叉。已合并为**单源 = per-project `tasks.json`**：看板（`server/parsers/tasks_parser.parse_tasks(slug)`）递归展平树 + 按 status 映射成 3 桶（completed→completed / active→in_progress / planned·paused·blocked→pending）；`tasks.md` 删除。改一处、看板与项目树同步。脚手架改动按铁律先在上游落地 `[shared]` commit，再同步到下游。管理 skill 脚本（`add/update/delete/list_task.py`）改操作 `tasks.json`（`--slug --id`），成员/报表/会议/里程碑仍是 markdown（`mgmt_io` markdown helpers 保留）。
- **训练界面上游/下游边界**：上游训练 UI 是上游契约（`/run` 是 stub，models/datasets 空，待下游覆盖）。（历史注：infraredComp 的训练 UX——localStorage F5 持久化、config preset 回填、3s 实时轮询曲线、auto-select-latest、withSelected 下拉稳定——已回移植到上游作为通用范本，当时丢弃了红外特异设计；该库已退役。）判断标准：上游表单只放通用超参（epochs/lr/batch/optimizer/device/extra_args），领域超参由下游加。

## 备份与历史

历史嫁接操作前曾为当时参与的仓库做 bundle 备份（`~/backups/pregraft-<date>/`），可 `git clone <bundle> <dir>` 完整恢复旧历史。嫁接后的提交 SHA 与旧历史不同；恢复备份与改写远端历史是两回事，本指南不授权改写远端历史。
