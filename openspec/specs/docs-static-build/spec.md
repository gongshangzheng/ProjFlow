# docs-static-build Specification

## Purpose
定义纯静态托管（无后端）场景下文档页的数据来源：构建期把 `management/docs/` 编译为静态数据，前端在生产构建读取该数据、开发时仍走 FastAPI；并保证 history 路由的深链接可被 SPA 接管。
## Requirements
### Requirement: 构建期生成文档静态数据

构建流程 SHALL 扫描 `management/docs/` 下的 Markdown 与同名 sidecar JSON，产出前端可读取的静态数据文件；其字段 SHALL 与后端文档接口一致（列表项含 `slug/title/author/date/tags/summary/id/order`，详情项额外含 `content` 与 `sidecar`），排序 SHALL 与后端完全一致。扫描 SHALL 跳过下划线前缀目录（与后端一致）。

#### Scenario: 生成列表与详情
- **WHEN** 执行构建
- **THEN** 产出静态数据文件，含全部文档的列表项与按 slug 索引的详情项，详情项的 `content` 为去掉 frontmatter 的正文

#### Scenario: 排序与后端一致
- **WHEN** 比较静态数据列表顺序与 `GET /api/management/docs` 的顺序
- **THEN** 两者一致，即依次按「文件夹优先级（`DOCS_FOLDER_ORDER`）→ `order` → `id` → `date` 降序 → `slug` 字典序」排序，缺失/非数字的 `order` 与 `id` 排最后

#### Scenario: 资产目录不参与
- **WHEN** `management/docs/_assets/` 下存在文件
- **THEN** 静态数据不含该目录下任何内容，与后端文档列表行为一致

#### Scenario: sidecar 元数据保留
- **WHEN** 某文档存在同名 `.json`
- **THEN** 静态详情项包含该 sidecar 内容；无 sidecar 时为空对象

### Requirement: 生产构建读静态数据，开发走 FastAPI

文档取数 SHALL 通过单一来源切换层暴露：开发模式调用后端 API，生产构建读取静态数据。组件 MUST NOT 直接依赖具体来源。

#### Scenario: 本地开发
- **WHEN** 以开发模式运行前端
- **THEN** 文档列表与正文来自后端 API，改动 `management/docs/` 后刷新即可见

#### Scenario: 生产构建
- **WHEN** 以生产构建运行于静态托管
- **THEN** 文档列表与正文来自静态数据，无需后端

#### Scenario: 静态数据中不存在该文档
- **WHEN** 请求一个不在静态数据中的 slug
- **THEN** 取数层以错误结束（与后端 404 行为一致），页面显示空态而非崩溃

### Requirement: 生成失败必须显式失败

当 `management/docs/` 缺失、不含任何 Markdown、或 frontmatter 存在无法解析的内容时，生成步骤 SHALL 以非零退出码结束并打印可定位的错误；MUST NOT 静默产出残缺数据。

#### Scenario: 文档目录缺失
- **WHEN** 构建时仓库内没有 `management/docs/`
- **THEN** 生成步骤报错退出，构建失败

#### Scenario: frontmatter 无法解析
- **WHEN** 某篇文档的 frontmatter 含不支持的写法
- **THEN** 打印文件名与行号并退出非零

### Requirement: SPA 深链接回退

构建完成后 SHALL 提供 `404.html`（内容与 `index.html` 相同），使静态托管在直接访问 history 路由深链接时由 SPA 接管渲染。

#### Scenario: 直接访问文档深链接
- **WHEN** 浏览器直接打开 `/<base>/management/docs/<slug>`
- **THEN** 托管平台返回 `404.html`，SPA 启动后按路由渲染该文档

#### Scenario: 产物一致性
- **WHEN** 构建结束
- **THEN** `dist/404.html` 与 `dist/index.html` 内容一致

### Requirement: 文档图片随构建静态化

构建流程 SHALL 把 `management/docs/_assets/` 整树复制到前端产物的静态资源目录；复制前 SHALL 清空目标目录，避免源端已删除的图片残留在产物中。当 `_assets/` 不存在时构建 SHALL 照常成功。

#### Scenario: 图片进入产物
- **WHEN** `management/docs/_assets/<slug>/fig-1.webp` 存在并执行构建
- **THEN** 产物中存在 `/docs-assets/<slug>/fig-1.webp`，可被静态托管直接访问

#### Scenario: 已删除的图片不残留
- **WHEN** 上次构建后某张图片在 `_assets/` 被删除，再次构建
- **THEN** 产物中不再包含该图片

#### Scenario: 无资产目录
- **WHEN** 仓库中不存在 `management/docs/_assets/`
- **THEN** 构建成功，不报错

### Requirement: 正文图片在生产构建下正确解析

生产构建读取静态数据时，正文中的 `/api/management/docs-assets/` 前缀 SHALL 改写为 `${BASE_URL}docs-assets/`，使图片 URL 随部署基路径正确解析；开发模式 SHALL 保持原样以走后端端点。源 Markdown MUST NOT 被改写。

#### Scenario: 静态托管的子路径部署
- **WHEN** 部署在 `/<repo>/` 基路径下，正文引用 `/api/management/docs-assets/x/fig-1.webp`
- **THEN** 页面加载 `/<repo>/docs-assets/x/fig-1.webp` 并成功显示

#### Scenario: 开发模式仍走后端
- **WHEN** 以开发模式运行并打开同一篇文档
- **THEN** 图片请求指向 `/api/management/docs-assets/...`，由后端静态端点提供

#### Scenario: 源文件不被改写
- **WHEN** 构建完成后检查 `management/docs/` 下的 Markdown
- **THEN** 其中的图片引用仍是 `/api/management/docs-assets/...`，与 `doc-image-assets` 约定一致

