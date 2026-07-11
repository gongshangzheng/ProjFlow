---
name: projflow-management
description: |
  ProjFlow 项目管理模块操作指南。用于项目树、团队成员管理、日报/周报/月报、任务看板、里程碑、会议纪要等 CRUD 操作。
  触发场景：(1) 添加/编辑团队成员，(2) 创建/查看报表，(3) 管理任务看板，(4) 创建会议纪要，(5) 了解项目结构
---

# ProjFlow 项目管理模块

本 skill 提供 ProjFlow 项目管理模块的完整操作指南。

## 项目结构

```
management/
├── team/           # 团队成员档案
│   ├── README.md   # 成员列表表格
│   └── {姓名}.md   # 个人详情
├── daily/          # 日报 YYYY/MM/DD-姓名.md
├── weekly/         # 周报 YYYY/WXX-姓名.md
├── monthly/        # 月报 YYYY/MM-姓名.md
└── docs/
    ├── tasks.md    # 任务看板
    ├── milestones.md # 里程碑
    ├── projects/   # 项目树 {slug}/README.md + tasks.json + notes/
    └── meetings/   # 会议纪要 YYYY-MM-DD.md
```

## 启动服务

```bash
# 后端 (8090)
python3 -m uvicorn server.main:app --host 0.0.0.0 --port 8090

# 前端 (3002)
cd web && npx vite --port 3002
```

访问 http://localhost:3002

---

## 1. 团队成员管理

### 查看成员列表

```bash
# API
GET /api/management/team

# 直接读取
cat management/team/README.md
```

### 添加新成员

需要两步：

1. **更新成员列表** - 编辑 `management/team/README.md`，在表格中添加新成员：

```markdown
| 姓名 | 英文标识 | 角色 | 入职日期 |
|------|----------|------|----------|
| 张三 | zhangsan | 算法工程师 | 2026-01-15 |
```

2. **创建个人档案** - 创建 `management/team/{姓名}.md`：

```markdown
# 张三

## 基本信息

| 字段 | 内容 |
|------|------|
| 姓名 | 张三 |
| 英文标识 | zhangsan |
| 角色 | 算法工程师 |
| 入职日期 | 2026-01-15 |
| 研究方向 | 大语言模型 |

## 技术栈

- Python
- PyTorch
- Transformers

## 负责模块

- 论文搜集
- 模型评测

## 备注

专注 LLM 研究
```

### 查看成员详情

```bash
# API
GET /api/management/team/{member_id}

# 直接读取
cat management/team/{姓名}.md
```

---

## 2. 报表管理

### 日报

**文件命名**: `daily/YYYY/MM/DD-姓名.md`

```bash
# 查看列表
GET /api/management/daily

# 查看详情
GET /api/management/daily/{date}/{author}

# 示例文件: management/daily/2026/07/10-zhangsan.md
```

**模板**:
```markdown
# 日报 — 张三 — 2026-07-10

## 今日工作

- 完成 XX 功能开发
- 调研 XX 技术方案

## 明日计划

- 继续 XX 开发
- 参加 XX 会议

## 备注

无
```

### 周报

**文件命名**: `weekly/YYYY/WXX-姓名.md`

```bash
GET /api/management/weekly
GET /api/management/weekly/{year}/{week}/{author}

# 示例: management/weekly/2026/W28-zhangsan.md
```

**模板**:
```markdown
# 周报 — 张三 — 2026 第 28 周

## 本周工作

- 完成 XX 模块开发
- 优化了 XX 性能

## 下周计划

- 开展 XX 项目
- 准备 XX 汇报

## 备注

无
```

### 月报

**文件命名**: `monthly/YYYY/MM-姓名.md`

```bash
GET /api/management/monthly
GET /api/management/monthly/{year}/{month}/{author}

# 示例: management/monthly/2026/07-zhangsan.md
```

---

## 3. 任务看板

**文件**: `management/docs/tasks.md`

```bash
GET /api/management/tasks
```

**表格结构**:
```markdown
## 进行中

| 任务 | 负责人 | 优先级 | 截止日期 |
|------|--------|--------|----------|
| XX 开发 | 张三 | P1 | 2026-07-15 |

## 待开始

| 任务 | 负责人 | 优先级 | 截止日期 |
|------|--------|--------|----------|

## 已完成

| 任务 | 负责人 | 完成日期 |
|------|--------|----------|
```

---

## 4. 里程碑

**文件**: `management/docs/milestones.md`

```bash
GET /api/management/milestones
```

**表格结构**:
```markdown
## 里程碑

| 名称 | 目标日期 | 状态 | 备注 |
|------|----------|------|------|
| v1.0 发布 | 2026-08-01 | 进行中 | |
```

---

## 5. 会议纪要

**目录**: `management/docs/meetings/`
**文件命名**: `YYYY-MM-DD.md`

```bash
GET /api/management/meetings
GET /api/management/meetings/{date}
```

**模板**:
```markdown
# 会议纪要 — 2026-07-10

## 基本信息

- 参会人：张三、李四
- 记录人：张三
- 时间：2026-07-10 14:00-15:00

## 议题

1. 项目进度回顾
2. 技术方案讨论

## 讨论内容

### 议题 1
...

### 议题 2
...

## 决议

- 确认 XX 方案
- 继续推进 XX

## 待办

- [ ] 张三：完成 XX
- [ ] 李四：调研 XX
```

---

## 6. 项目树

**目录**: `management/docs/projects/{slug}/`

```bash
GET /api/management/projects
GET /api/management/projects/{slug}
GET /api/management/projects/{slug}/tasks
GET /api/management/projects/{slug}/notes/{note_path}
```

每个项目目录包含：
- `README.md`：项目说明（含 YAML frontmatter）
- `tasks.json`：任务树
- `notes/`：任务笔记 markdown

---

## 常用命令

```bash
# 启动服务
bash start_services.sh

# 查看后端日志
tail -f /tmp/projflow-backend.log

# 查看前端日志
tail -f /tmp/projflow-frontend.log
```
