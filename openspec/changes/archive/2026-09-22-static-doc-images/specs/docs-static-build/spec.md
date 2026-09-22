## ADDED Requirements

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
