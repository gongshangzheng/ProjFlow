# 数据集管理界面设计规范

> 所属 skill：design-principles。做数据集浏览、资产画廊、文件网格类页面时读本文件。

## 1. 渐进式披露（三层，同一路由内完成）

数据集页面必须分层展示，不要一屏塞满所有信息：

```
L1 数据集卡片列表  →  L2 目录浏览网格（面包屑 + 分页）  →  L3 预览 modal
   （是什么）           （里面有什么）                     （单个样本长什么样）
```

- 层间切换用组件内状态（`currentDataset` ref 切换两个 `n-card`），不新开路由
- 每层只加载该层需要的数据：L1 浅层统计、L2 当前页目录项、L3 单个文件
- 参考实现：`web/src/views/datasets/DatasetBrowser.vue`；对照 pet `DatasetBrowser.vue`、digital_human `AssetGallery.vue`

## 2. L1 数据集卡片

- 网格：`grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 12px`
- 卡片内容：文件夹图标 + 名称 + 元信息行 `N 子目录 · N 文件`（后端**浅层**统计，不递归）
- **软链标记**：数据集常以符号链接挂进来，`is_symlink` 时显示斜体 `→ 软链`
- 空状态：说明把目录放哪就能显示（"将数据集目录（或软链）放入 datasets/ 即可显示"）

## 3. L2 目录浏览

- 网格：`repeat(auto-fill, minmax(140px, 1fr))`；目录在前、文件在后，各自按名称排序
- **面包屑**：`数据集 / {name} / sub / sub`，每段可点击回退（截断 path 重新 fetch）；当前段加粗不可点
- header-extra 放 `共 N 项` + 刷新按钮
- **服务端分页**（目录可能上千文件）：契约与代码片段见 `references/pagination.md` §2
- 每项 = 缩略图盒（100px）+ 文件名（单行省略 + title 提示）+ 大小（`formatSize`）
- 缩略图四分支：目录→文件夹图标 / 图片→原图 / 视频→thumb 端点 + ▶ overlay / 其他→文档图标（见 `references/media-covers.md` §3-4）
- 后端扫描跳过点文件（`.thumbs` 缓存目录因此不会出现在列表里）

## 4. L3 预览 modal

- `n-modal preset="card"`，max-width 800px，标题 = 文件名
- 图片：`<img>` `max-width: 100%; max-height: 70vh`
- 视频：`<video controls preload="none" playsinline>`（缩略图承担视觉，字节只在点播后请求）
- 不支持的类型给一句话说明，不要空白

## 5. 大规模资产的扩展模式（参考 digital_human AssetGallery）

当单个"数据集"内部还有多模态分类（图片/视频/3D/音频）时：

- 左侧窄栏（240px）subject 列表 + 客户端搜索框；每行带**按类型计数徽章**（不同颜色）
- 右侧 `n-tabs` 按类型分栏，tab 标签带计数（`图片 (12)`），自动选中首个非空 tab
- 原始元数据（manifest JSON）放**折叠的** `n-collapse-item` 里（`<pre>` + max-height 滚动）——渐进披露原始数据
- 每个 tab 单独空状态

## 6. 安全公约（后端）

- 所有 path 参数必须防路径穿越：realpath 后校验 `startswith(root + os.sep)`
- 数据集根允许是符号链接（realpath 解析到链接目标后再做包含校验）
- dataset_id 拒绝含 `/` 或以 `.` 开头
