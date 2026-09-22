# pages-deploy Specification

## Purpose
定义仓库的 GitHub Pages 部署通道：触发条件与构建步骤、部署基路径的处理方式，以及对静态产物的要求，使上游仓库自身可作为静态站点发布。
## Requirements
### Requirement: 推送 main 自动部署到 GitHub Pages

仓库 SHALL 提供 GitHub Actions 工作流，在 `main` 分支收到推送（或手动触发）时构建前端并把产物发布到 GitHub Pages；构建步骤 SHALL 在 `web/` 目录下执行安装与构建，产物目录 SHALL 为 `web/dist`。

#### Scenario: 推送触发部署
- **WHEN** 向 `main` 推送提交
- **THEN** 工作流被触发，完成构建并发布到 GitHub Pages，且一次只有一个部署在进行（并发组生效）

#### Scenario: 手动触发
- **WHEN** 通过 `workflow_dispatch` 手动触发
- **THEN** 同样完成构建与发布

#### Scenario: 构建命令走 npm 脚本
- **WHEN** 工作流执行构建
- **THEN** 使用 `npm run build`，从而自动串联 `prebuild`（生成文档静态数据与资产）与 `postbuild`（产出 `404.html`）

### Requirement: 部署基路径与开发路径分离

构建产物的基路径 SHALL 与部署子路径一致（`/<仓库名>/`），而本地开发 SHALL 继续以 `/` 为基路径，使日常开发 URL 不因引入 Pages 而改变。

#### Scenario: 本地开发地址不变
- **WHEN** 开发者运行 `npm run dev`
- **THEN** 站点仍可通过 `http://localhost:<端口>/` 直接访问，无需附加子路径

#### Scenario: 构建产物使用子路径
- **WHEN** 执行 `npm run build` 并部署到 GitHub Pages
- **THEN** 产物的资源引用与路由基路径均为 `/<仓库名>/`，页面在 `https://<user>.github.io/<仓库名>/` 下正常加载

#### Scenario: 路由基路径随场景一致
- **WHEN** 应用初始化路由
- **THEN** 使用的基路径与当前的构建/开发场景一致，深链接在两种场景下都能正确解析

### Requirement: 部署产物包含静态文档能力

发布到 Pages 的产物 SHALL 包含文档静态数据、文档图片资产与 `404.html`，使文档页与深链接在无后端环境下可用。

#### Scenario: 文档页可在线上浏览
- **WHEN** 打开 `https://<user>.github.io/<仓库名>/management/docs/<slug>`
- **THEN** 文档列表与正文正常渲染，无需后端

#### Scenario: 深链接可直接访问与刷新
- **WHEN** 直接在地址栏打开或刷新某个文档深链接
- **THEN** SPA 接管并渲染该文档，不出现平台 404 页面

#### Scenario: 正文配图可加载
- **WHEN** 文档正文包含按约定引用的图片
- **THEN** 图片从部署基路径下的静态资产加载成功

