# AGENTS.md — ProjFlow 项目管理平台

> 本文件供 AI Agent（如 Qoder、Cursor 等）阅读，用于理解项目架构、开发规范和工作流程。

> **功能状态（2026-10-16）**：仅项目树暂时停用（菜单隐藏、旧页面跳转任务看板、专用 `/api/management/projects/{slug}*` 路由不挂载，保留看板所需的项目列表接口）。新增工作通过 OpenSpec 跟踪，不主动维护项目树或运行其 CRUD；历史数据及实现保留。任务看板、团队、报表、里程碑、会议和 Wiki 继续使用；management skill 仅停用项目树相关操作。

## 项目概述

ProjFlow 是一个通用的项目管理 demo 平台，包含三大模块：**项目管理**（团队、日报/周报/月报、任务看板、里程碑、会议纪要）、**论文搜集**（多源聚合、智能分类、精读笔记）、**评测体系**（模型管理、评测运行、结果对比）。前后端分离架构，后端读写本地 Markdown 文件和 SQLite 数据库。

## 技术栈

| 层 | 技术 | 端口 |
|----|------|------|
| 前端 | Vue 3 + Vite + Naive UI + Vue Router | 3210 |
| 后端 | FastAPI (Python) | 8809 |

### 服务架构

```
浏览器 → Vite (3210) → FastAPI (8809) → management/ 目录（Markdown 文件）
                                      → data/papers.db（SQLite 论文数据库）
                                      → evaluation/ 目录（模型/数据集/结果 JSON）
```

- **前端**：Vue 3 SPA，通过 Vite dev server 代理 `/api` 到后端
- **后端**：FastAPI，三大模块各自有独立路由和数据源
- **数据源**：管理模块读写 Markdown 文件，论文模块使用 SQLite，评测模块使用 JSON 文件

## 启动服务

```bash
# 一键启动（后端 8809 + 前端 3210）
bash start_services.sh

# 或手动启动：
# 1. 后端
cd ProjFlow
nohup python3 -m uvicorn server.main:app --host 0.0.0.0 --port 8809 </dev/null > /tmp/backend.log 2>&1 & disown

# 2. 前端
cd ProjFlow/web
nohup npx vite --port 3210 --strict-port </dev/null > /tmp/frontend.log 2>&1 & disown
```

> ⚠️ **从本项目初始化新项目时必须替换端口**
>
> 前端 3210 / 后端 8809 是 ProjFlow 的固定端口。若以本仓库为脚手架克隆出新项目（如 ai-api-research），
> 必须全局替换为一组新端口，否则两个项目无法同时运行（启动脚本会检测到端口冲突直接退出）。
>
> 需要同步修改的位置共 3 处：
> 1. `start_services.sh` — 后端 8809、前端 3210（含端口冲突检查逻辑）
> 2. `web/vite.config.js` — `server.port`（3210）和 `/api` 代理 target（8809）
> 3. `server/config.py` — `CORS_ORIGINS` 中的 3210
>
> 建议：新项目选定端口后先 `lsof -i :<新端口>` 确认空闲，再全局搜索替换旧端口号。
>
## 部署（GitHub Pages）

线上站点：<https://gongshangzheng.github.io/ProjFlow/>

```text
push main → .github/workflows/deploy.yml
  → web/ 下 npm install + npm run build
      prebuild  build-docs-data.mjs  management/docs/ → web/public/docs-data.json（含 _assets 复制）
      vite build
      postbuild copy-404.mjs         dist/index.html → dist/404.html
  → 上传 web/dist 到 GitHub Pages
```

关键约定：

1. **基路径条件式**：`web/vite.config.js` 里 `base` 在 `build` 时为 `/ProjFlow/`、开发时为 `/`。
   因此**本地开发地址仍是 `http://localhost:3210/`**，不会被改成子路径。改仓库名时同步改这一处。
2. **构建只走 `npm run build`**：直接用 `vite build` 会跳过 pre/post 钩子 → 产物缺 `docs-data.json`/`404.html`。
3. **文档页在线上读静态数据**（`api/docs.js` 按 `import.meta.env.PROD` 切换）；开发模式仍走 FastAPI。
   源 Markdown 保持 `/api/management/docs-assets/...` 绝对路径，静态分支在读取时改写到 `/<base>/docs-assets/`。
4. **线上只有文档页可用**：无后端，论文/评测/项目树等页面显示空态；`404.html` 负责把深链接交给 SPA。
5. **改了文档要 push 才生效**：`management/docs/*.md` 是**构建期**编译进 `web/public/docs-data.json` 的，
   线上不实时读仓库。所以「改 md → 本地看效果」走 dev（FastAPI 实时读），
   「改 md → 线上更新」必须 `git push`（并等 CI 跑完，约 1–2 分钟）。

> 📋 **从本库初始化新库后的第一件事**：在新库内执行 openspec change `fork-init-guide`
> （走 `openspec-apply-change` 流程；tasks 即完整适配清单：端口 / OpenSpec 目录 / 命名 / 数据 / 依赖 / 功能隐藏 / 自检）。
> 完成后 `openspec archive fork-init-guide`。

## 目录结构

```
ProjFlow/
├── AGENTS.md                # 本文件
├── .gitignore
├── start_services.sh        # 一键启动脚本
├── server/                  # FastAPI 后端
│   ├── config.py            # 配置（端口、CORS、各模块路径）
│   ├── main.py              # 入口（注册 management/papers/evaluation 路由）
│   ├── db.py                # SQLite 数据库操作（论文模块）
│   ├── routers/
│   │   ├── management.py    # 管理路由（读写 Markdown 文件）
│   │   ├── papers.py        # 论文路由（读写 SQLite）
│   │   └── evaluation.py    # 评测路由（读写 JSON）
│   ├── parsers/             # Markdown 解析器
│   │   ├── markdown_table.py    # 通用表格解析
│   │   ├── team_parser.py       # 团队成员解析
│   │   ├── report_parser.py     # 日报/周报/月报解析
│   │   ├── tasks_parser.py      # 任务看板解析
│   │   └── milestones_parser.py # 里程碑解析
│   ├── utils/
│   │   └── file_utils.py   # 文件操作工具
│   └── requirements.txt
├── web/                     # Vue 3 前端
│   ├── vite.config.js       # Vite 配置（端口 3210，代理 /api → 8809）
│   ├── src/
│   │   ├── api/             # API 请求封装（management.js, papers.js, evaluation.js）
│   │   ├── layouts/         # 布局组件
│   │   ├── router/          # 路由配置
│   │   ├── views/
│   │   │   ├── management/  # 团队、日报、周报、月报、任务看板、里程碑、会议纪要
│   │   │   ├── papers/      # 论文列表、论文详情、数据源配置
│   │   │   └── evaluation/  # 评测运行、评测结果、模型管理、数据集管理
│   │   └── components/      # 通用组件
│   └── package.json
├── management/              # 项目管理 Markdown 文件
│   ├── team/                # 团队成员档案
│   ├── daily/               # 日报
│   ├── weekly/              # 周报
│   ├── monthly/             # 月报
│   ├── experiments/         # 实验报告（experiment skill 生成，只读 API 暴露）
│   └── docs/                # 任务、里程碑、会议纪要
├── papers/                  # 论文模块
│   ├── config/              # 数据源配置
│   ├── data/                # 论文数据（.gitignore）
│   ├── cache/               # 缓存（.gitignore）
│   ├── docs/                # 文档
│   └── scripts/             # 脚本
├── evaluation/              # 评测模块
│   ├── models/              # 模型定义 JSON
│   ├── datasets/            # 数据集定义 JSON
│   ├── configs/             # 评测配置 JSON
│   ├── scripts/             # 评测脚本
│   └── results/             # 评测结果 JSON（.gitignore）
├── data/                    # 通用应用数据，例如论文 SQLite 数据库（.gitignore）
├── datasets/                # 数据集资产，例如 demo/images 样本
├── results/                 # 训练、评测等运行生成的结果
├── lib/                     # 有跨流程复用需要时放置实现代码
└── scripts/                 # 长期维护的项目工具入口
    ├── import_papers.py     # 从 data/extracted_papers.json 导入论文
    ├── tmp/                 # 本地临时脚本，Git 忽略
    └── archive/             # 仅供历史参考的归档脚本
```

> 说明性文档（含 wiki）统一置于 `management/docs/`；仓库根目录不设 `docs/`。

## 三大模块架构

### 1. 项目管理模块

**数据流**：
```
management/ 目录（Markdown 文件）
  ↓ FastAPI (port 8809, server/routers/management.py → server/parsers/)
前端 Vue 组件 (port 3210)
```

**关键设计**：
- **团队成员**：从 `management/team/README.md` 解析成员列表表格，从 `management/team/{姓名}.md` 解析成员详情（含技能特长/技术栈）
- **日报/周报/月报**：按目录结构扫描 Markdown 文件，从文件名解析日期和作者
- **任务看板**：解析 `management/docs/tasks.md` 中的三个表格（进行中、待开始、已完成）
- **里程碑**：解析 `management/docs/milestones.md` 中的表格
- **会议纪要**：扫描 `management/docs/meetings/` 目录下的 Markdown 文件

### 2. 论文搜集模块

**数据流**：
```
data/papers.db（SQLite 数据库）
  ↓ FastAPI (port 8809, server/routers/papers.py → server/db.py)
前端 Vue 组件 (port 3210)
```

**关键设计**：
- **论文存储**：SQLite 数据库 `data/papers.db`，表结构含标题、作者、摘要、来源、分类等
- **数据导入**：长期论文导入入口为 `scripts/import_papers.py`，输入文件默认是 `data/extracted_papers.json`。这与 `.agents/skills/papers/scripts/import_papers.py` 的按路径导入工具用途不同。
- **API 端点**：论文列表（分页/筛选）、详情、统计摘要、数据源配置

### 3. 评测体系模块

**数据流**：
```
evaluation/ 目录（JSON 文件）
  ↓ FastAPI (port 8809, server/routers/evaluation.py)
前端 Vue 组件 (port 3210)
```

**关键设计**：
- **模型管理**：`evaluation/models/` 下的 JSON 文件定义模型信息
- **数据集管理**：`evaluation/datasets/` 下的 JSON 文件定义数据集信息
- **评测配置**：`evaluation/configs/` 下的 JSON 文件定义评测参数
- **评测结果**：`evaluation/results/` 下的 JSON 文件存储评测结果
- **空数据策略**：当目录为空时返回空列表（DEFAULT_MODELS 和 DEFAULT_DATASETS 均为空）

### 文件命名规范

| 类型 | 路径格式 | 示例 |
|------|----------|------|
| 日报 | `daily/YYYY/MM/DD-姓名.md` | `daily/2026/07/09-张三.md` |
| 周报 | `weekly/YYYY/WXX-姓名.md` | `weekly/2026/W28-张三.md` |
| 月报 | `monthly/YYYY/MM-姓名.md` | `monthly/2026/07-张三.md` |
| 会议 | `docs/meetings/YYYY-MM-DD.md` | `docs/meetings/2026-07-09.md` |

### 脚本与库目录约定

**落点按归属自上而下选择第一档**：

1. **skill 拥有**：只服务某个 skill 工作流、离开它没有意义的脚本，放进 `.agents/skills/<skill>/scripts/`。
2. **仓库级工具**：跨 skill/模块复用，或由人直接对仓库运行的脚本，放进 `scripts/<area>/`，由该目录 README 说明用法。
3. **临时**：只服务当前一次任务的脚本，放进已忽略的临时目录，任务结束时删除或归档。
4. **归档**：已被取代但仍有参考价值的脚本，放进 `scripts/archive/<area>/`。

归属发生变化时脚本可跨档移动，移动沿用归档已有的引用检查与敏感内容检查。

**`scripts/<area>/` 何时可以提升为 skill**：四条同时满足才提，并且先向用户提出、获准后建。

- 有独立触发场景，不是被人顺手调用。
- 自带一套步骤规范，而不是若干互不相关的独立命令。
- 脚本之间共享判据或状态。
- Agent 需要反复按流程执行，而不是人偶尔跑一次。

只是碰巧放在同一目录的独立一次性脚本（例如按实验分组的校验脚本）不满足上述条件，继续留在 `scripts/<area>/`。提出提及时需写明目标 skill 名、将吸收的脚本与维护成本。

**已记录落点**：`scripts/import_papers.py` 保留在 `scripts/`。它读取 `data/extracted_papers.json`、经 arXiv API 补全、清空论文表后导入，依赖 `server.db` 而非 `papers` skill 的工作流；该 skill 另有按路径导入的脚本，把两者归到同一 skill 会让服务端依赖进入 skill 包，并混入两种用途的导入器。

- 根目录 `scripts/` 存放长期维护、可由开发者直接运行的项目级工具。稳定的重复能力按用途放在具体子目录，运行方式由该目录的 README 说明。
- 临时脚本放在 `scripts/tmp/`。使用前确认当前仓库的忽略规则实际匹配（`git check-ignore -v scripts/tmp/<file>`），并确认 `git ls-files scripts/tmp` 没有已跟踪文件；任一检查不通过时先停下处理，不在该目录创建临时脚本。
- 临时脚本使用后，先检查脚本内容及相关调用上下文中的凭据、令牌、私有端点、用户路径等敏感信息。只有确认适合入库且有历史参考价值时，才检查代码和文档引用并移至 `scripts/archive/`，同时说明保留理由。发现敏感内容或无法判定时，不得自动归档进 Git，先向用户报告并确认处理方式。
- 已确认无用但有历史参考价值的脚本也归档，不凭猜测删除。一次性且无保留价值的内容仅在用途和归属明确、且任务授权清理时删除。不要把 `tmp/` 中已有脚本或数据未经确认就整体移动。
- `scripts/archive/` 保存不属于常规支持流程、但确认适合入库且有保留价值的历史脚本；归档不等于认定脚本无用。
- `.agents/skills/<skill>/scripts/` 存放只服务于对应 skill 工作流的工具；`web/scripts/` 存放前端构建钩子；模块内的 `evaluation/scripts/` 等目录属于模块自身。不要仅因文件类型相同就把这些脚本搬到根目录。
- `lib/` 用于具体项目流程所需的可导入实现代码，不放命令入口或临时脚本。实现只被单一模块使用时，优先放在该模块内部；只有存在跨流程复用需求时，才使用根目录 `lib/`。
- `data/` 存放通用应用数据。本仓库的论文 SQLite 数据库位于 `data/papers.db`。
- `datasets/` 存放数据集资产；仓库当前包含 `datasets/demo/images/` 样本。模块目录如 `evaluation/datasets/` 可以只存定义 JSON，不应假定它包含原始数据。
- `results/` 存放训练、评测等运行产物；大体积或运行期文件按各模块的忽略规则处理。
- 需要多个临时脚本解决相近且重复的问题时，先列出候选能力、输入输出、替代方案和维护成本，再请用户选择是否固化。未获选择前，不新增长期通用工具。

## 开发规范

### Git 工作流

1. **每次功能变更都应提交**，不要积累大量未提交变更
2. **提交信息格式**：`<type>: <描述>`，如 `feat: 添加任务筛选`、`fix: 修复分页问题`
3. **type 取值**：feat（新功能）、fix（修复）、refactor（重构）、style（样式）、docs（文档）、chore（杂项）
4. **禁止提交**：`node_modules/`、`__pycache__/`、`.venv/`、`.env`、`*.db`、`papers/data/`、`papers/cache/`
5. **跨库传播**：共享脚手架改进在上/下游间的 cherry-pick 双向操作与冲突分类解法，见 `.agents/skills/upstream-sync/SKILL.md`（含实证命令序列）

### 文档（wiki）变更

- **登记表是唯一权威**：`openspec/registry.md`（编号 / slug / 标题 / 职责边界 / 单篇 Change）。
  新增或废弃一篇文档 → **先改这张表**，再开单篇 Change `docs-<slug>`，design 审核通过后才动笔。
- **正文位置**：`management/docs/<slug>.md`，元数据在同名 `<slug>.json`（`changelog` / `progress` / `appendix` / `related`）。
- **结构级变更**（章节增删 / 移动 / 重编号）必须走单篇 change 且 design 先行；
  **内容级小修**（错字 / 数字 / 单段论证 / 链接）直接改，commit message 说明即可。
- 详细契约见 `openspec/specs/documentation/spec.md`。

### 前端开发

- 框架：Vue 3 `<script setup>` + Naive UI 组件库
- 样式：SCSS，组件内 `<style scoped>`
- API 请求：通过 `web/src/api/` 封装，统一使用 `request.js` 中的 axios 实例
- 路由：`web/src/router/index.js`
- 布局：`web/src/layouts/MainLayout.vue`（侧边栏 + 内容区，`native-scrollbar=false`）

### 后端开发

- 框架：FastAPI，路由在 `server/routers/`
- 配置：`server/config.py`（端口、CORS、各模块路径）
- Markdown 解析：`server/parsers/` 目录下的解析器
- 数据库操作：`server/db.py`（论文模块 SQLite CRUD）
- Python 版本：3.9（不支持 `str | None` 语法，需用 `Optional[str]`）
- 管理路由直接读写 Markdown 文件，论文路由操作 SQLite，评测路由读写 JSON

### macOS 后台进程

```bash
# 启动后台进程（必须用 </dev/null 防止挂起）
nohup cmd </dev/null > /tmp/log 2>&1 & disown

# 检查进程
ps aux | grep <keyword> | grep -v grep

# 检查端口
lsof -i :<port>
```

## 常见问题

### 前端启动后立即挂起（进程状态为 T）
macOS 上 nohup 进程需要 `</dev/null` 重定向 stdin，否则终端关闭时进程收到 SIGHUP 挂起。

### Vite 端口被占用
使用 `--strict-port` 避免自动 fallback 到其他端口。如果 3210 被占，先 `lsof -i :3210` 找到并杀掉旧进程。

### 管理页面数据为空
检查后端（port 8809）是否在运行，`management/` 目录下是否有对应的数据文件。

### 论文页面数据为空
论文数据库位于 `data/papers.db`。根目录的 `scripts/import_papers.py` 会读取 `data/extracted_papers.json`，并清空现有论文表后导入，因此运行前须确认输入文件和数据库内容可替换。按任意 JSON 文件导入请使用 `.agents/skills/papers/scripts/import_papers.py <json-path>`。

### 评测页面数据为空
在 `evaluation/models/`、`evaluation/datasets/` 等目录下放置 JSON 文件即可显示数据。
