# ProjFlow

通用项目管理 demo 平台——项目管理、论文搜集、评测体系三大模块。

## 项目背景

ProjFlow 是一个轻量级项目管理平台 demo，适用于小型团队的日常协作管理。基于 Markdown 文件和 SQLite 存储数据，开箱即用。

核心功能：
- **项目管理**：成员档案、技能特长、日报/周报/月报、任务看板、里程碑、会议纪要
- **论文搜集**：多源聚合、智能分类、精读笔记
- **评测体系**：模型管理、数据集管理、评测运行、结果对比

## 项目结构

```
ProjFlow/
├── management/      # 项目管理体系
│   ├── team/        # 团队成员档案
│   ├── daily/       # 日报
│   ├── weekly/      # 周报
│   ├── monthly/     # 月报
│   └── docs/        # 任务、里程碑、会议纪要
├── papers/          # 论文搜集模块
│   ├── config/      # 数据源配置
│   ├── data/        # 论文数据
│   ├── cache/       # 缓存
│   └── scripts/     # 脚本
├── evaluation/      # 评测体系模块
│   ├── models/      # 模型定义
│   ├── datasets/    # 数据集定义
│   ├── configs/     # 评测配置
│   └── results/     # 评测结果
├── data/            # 数据目录（papers.db）
├── scripts/         # 工具脚本
├── server/          # FastAPI 后端
│   ├── routers/     # API 路由
│   ├── parsers/     # Markdown 解析器
│   └── utils/       # 工具函数
├── web/             # Vue 3 前端
│   └── src/
│       ├── api/     # API 请求封装
│       ├── views/   # 页面组件
│       ├── layouts/ # 布局组件
│       └── router/  # 路由配置
├── docs/            # 其他文档
├── AGENTS.md        # AI Agent 指南
└── start_services.sh # 一键启动脚本
```

## 快速开始

```bash
# 一键启动（后端 8809 + 前端 3210）
bash start_services.sh

# 或手动启动：
# 1. 后端
cd ProjFlow
python3 -m uvicorn server.main:app --host 0.0.0.0 --port 8809

# 2. 前端
cd ProjFlow/web
npx vite --port 3210
```

启动后访问 http://localhost:3210（开发基路径为 `/`，不需要子路径前缀）

## GitHub Pages

线上站点：<https://gongshangzheng.github.io/ProjFlow/>

- push `main` 后由 `.github/workflows/deploy.yml` 自动构建 `web/` 并发布 `web/dist`。
- `npm run build` 会自动串联 `prebuild`（生成文档静态数据 `docs-data.json` 与图片资产）与 `postbuild`（产出 `404.html`）。
- **开发与构建的基路径不同**：`vite.config.js` 里构建时用 `/ProjFlow/`、开发时用 `/`，因此本地开发地址不受影响。
- **Pages 上只有文档页可用**（无后端）：论文列表 / 评测 / 项目树等依赖 FastAPI 的页面会显示空态。
  文档正文里的图片走静态资产，可正常显示。

## 技术栈

| 层 | 技术 | 端口 |
|----|------|------|
| 前端 | Vue 3 + Vite + Naive UI + Vue Router | 3210 |
| 后端 | FastAPI (Python) | 8809 |
| 数据源 | Markdown 文件 + SQLite | — |

## License

MIT
