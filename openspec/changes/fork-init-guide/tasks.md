# Tasks: fork-init-guide

> **本 change 是新库初始化适配清单。** 上游（ProjFlow）永不执行任务 1–7；
> 新库从本库初始化后，第一件事就是在**新库内**执行本 change（走 `openspec-apply-change` 流程），
> 全部完成后 `openspec archive fork-init-guide`。

## 0. 上游侧准备（在 ProjFlow 完成，新库勿执行）

- [ ] 0.1 `AGENTS.md` 启动服务一节端口提示后追加一行：从本库初始化新库后，第一件事是在新库执行 openspec change `fork-init-guide`
- [ ] 0.2 `.agents/skills/upstream-sync/SKILL.md` 触发场景加「从上游初始化新库」，拓扑节末尾加一行指引到本 change

## 1. 端口适配（新库执行）

- [ ] 1.1 选定新的前端/后端端口（上游保留 3210/8809，不可复用），`lsof -i :<新端口> -sTCP:LISTEN` 确认空闲
- [ ] 1.2 替换 3 处端口：`start_services.sh`（后端+前端+冲突检查）、`web/vite.config.js`（`server.port` 与 `/api` 代理 target）、`server/config.py`（`CORS_ORIGINS` 中的前端端口）
- [ ] 1.3 验收：全局搜索 `3210`、`8809` 无残留；`bash start_services.sh` 后双端口 health 页面均 200；与上游 ProjFlow 服务可同时运行互不冲突

## 2. OpenSpec 目录适配（新库执行）

- [ ] 2.1 重写 `openspec/config.yaml` 的 `context` 为新项目一句话描述（技术栈+模块+端口），移除全部 ProjFlow 文案
- [ ] 2.2 清理上游遗留：删除 `openspec/changes/` 下**除 `fork-init-guide` 外**的所有 change 目录及 `archive/`（上游历史在上游仓库可随时查阅，新库不携带副本）
- [ ] 2.3 验收：`openspec list` 只剩本 change；`openspec validate` 通过

## 3. 项目身份重命名（新库执行）

- [ ] 3.1 全局搜索 `ProjFlow`/`projflow`（不区分大小写）逐处替换为新项目名，已知出现点：`web/index.html`、`web/package.json` name、`web/src/router/index.js` 页面 title 后缀、`web/src/stores/theme.js`、`web/src/layouts/MainLayout.vue`（侧边栏 logo 文案与缩写）、`server/main.py`、`start_services.sh`、`AGENTS.md`、README、`management/projects/`（项目树数据）
- [ ] 3.2 验收：全局搜索旧名仅剩历史无关命中（如 git 记录）；浏览器标签页标题与侧边栏 logo 显示新名

## 4. 领域数据清理（新库执行）

- [ ] 4.1 清空 ProjFlow 领域数据（只允许动以下路径）：`management/`（team/daily/weekly/monthly/projects/docs/meetings 的内容文件，保留目录结构与空模板）、`management/projects/projflow/`
- [ ] 4.2 删除运行数据：`data/*.db`、`papers/data/`、`papers/cache/`、`evaluation/results/`、`results/`、`datasets/.thumbs/`
- [ ] 4.3 验收：报告/团队/项目树页面显示空态不报错；`git status` 确认未误删 `server/`、`web/src/` 等共享脚手架文件

## 5. 依赖安装（新库执行）

- [ ] 5.1 检查 `web/package-lock.json` 是否含不可达 registry（如 `anpm.alibaba-inc.com`），有则全局替换为 `registry.npmmirror.com`
- [ ] 5.2 `cd web && npm install`；若中途中断留下空壳包目录，先 `find node_modules -maxdepth 3 -type d -empty -delete` 再重装
- [ ] 5.3 验收：`npm ls --depth=0` 无 missing/invalid；`npx vite --port <新前端端口>` 可启动

## 6. 功能隐藏（新库执行）

- [ ] 6.1 编辑 `web/src/config/hidden.js`，把新库不需要的分组 / 菜单项 / 报告类型 key 加入 `HIDDEN_KEYS`（文件头注释含全部可用 key；菜单不显示、路由保留直达、随时可逆）
- [ ] 6.2 验收：被隐藏入口从侧边栏消失；直接输入对应 URL 仍可打开

## 7. 收尾（新库执行）

- [ ] 7.1 双服务自检：`bash start_services.sh`，首页 + 每个未隐藏模块各打开一页确认渲染正常
- [ ] 7.2 首次提交：`chore: 初始化自 ProjFlow 脚手架，完成 fork-init-guide 适配`
- [ ] 7.3 归档本 change：`openspec archive fork-init-guide`——本 change 在新库完成使命
