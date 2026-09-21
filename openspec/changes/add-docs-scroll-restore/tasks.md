# Tasks: add-docs-scroll-restore

## 1. 工具函数

- [x] 1.1 新建 `web/src/utils/scrollMemory.js`：`findScrollContainer()`（查 `.app-content .n-scrollbar-container`，回退 `.n-scrollbar-container`）、`saveScrollPosition(key, el)`、`readScrollPosition(key)`、`attachScrollMemory(el, key)`（150ms 节流保存 + 返回解绑函数）、`restoreAfterRender(key, isReady, opts)`（等就绪 → nextTick 恢复 → 150ms 后二次校正；超时/失败静默返回）
- [x] 1.2 sessionStorage 读写包 try/catch（隐私模式/配额异常时静默降级）

## 2. DocPage 接入

- [x] 2.1 `.agents` 之外的实现文件 `web/src/views/management/DocPage.vue`：`onMounted` 后等 `currentDoc` 就绪触发 `restoreAfterRender`；对容器 `attachScrollMemory`；`onBeforeUnmount` 解绑并兜底保存
- [x] 2.2 确保切换文档（`route.params.slug` 变化）时不对新文档做恢复（key 含 path 天然隔离，代码中显式确认）

## 3. 验证

- [x] 3.1 刷新恢复：滚到文档中部（记录 scrollTop）→ 刷新 → 恢复位置（允许小幅偏差，二次校正生效）
- [x] 3.2 跨文档隔离：A 滚中部 → 进 B（应在顶部）→ 回 A（应恢复 A 的位置）
- [x] 3.3 会话语义：同一标签页刷新保留；新标签页打开同一文档从顶部开始
- [x] 3.4 非文档页回归：项目树 / 报告 / 评测页刷新行为与接入前一致；控制台无未捕获异常
- [x] 3.5 降级验证：临时改写选择器使其找不到容器，确认页面正常渲染且无异常抛出

## 4. 提交

- [x] 4.1 提交：`[shared] feat: 文档页刷新恢复滚动位置（scrollMemory 工具 + DocPage 接入）`
