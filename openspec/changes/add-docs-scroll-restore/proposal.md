# Proposal: add-docs-scroll-restore（文档页刷新恢复滚动位置）

## Why

文档页是长文精读场景，正文在主内容容器内滚动。浏览器刷新（F5）后容器滚动位置归零，用户每次都要重新翻回原处——精读对照、改文档时反复刷新，体验损耗明显。滚动位置属于用户的阅读上下文，应随刷新保留。

## What Changes

- 文档页记住主内容容器（`.app-content` 内的 `.n-scrollbar-container`）的滚动位置，按文档路由分键存入 `sessionStorage`
- 页面刷新后：等文档内容渲染完成，恢复到刷新前的滚动位置（并做一次延迟校正，吸收图片/Mermaid 加载引起的高度变化）
- 切换到另一篇文档：从顶部开始（各文档位置相互独立）
- 非文档页不受影响；不改 MainLayout 布局内部实现，封装成可复用工具供后续页面按需接入

## Capabilities

### New Capabilities
- `docs-page-scroll-restore`: 文档页主内容滚动位置的记忆与刷新恢复

### Modified Capabilities

（无——`docs-page-layout` 管左右栏收起行为，与滚动位置记忆是不同关注点，不修改其既有需求）

## Impact

- 修改：`web/src/views/management/DocPage.vue`（接入）
- 新增：`web/src/utils/scrollMemory.js`（容器查找 + 节流保存 + 渲染后恢复，供其它长文页复用）
- 不影响：`MainLayout.vue`、后端、其它页面行为；`.agents/skills/**`
- 归属：共享脚手架层（`web/src/`），实施时 commit 加 `[shared]` 前缀
