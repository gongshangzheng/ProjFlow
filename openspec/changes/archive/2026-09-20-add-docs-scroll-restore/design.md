# Design: add-docs-scroll-restore

## Context

见 proposal.md — Why。实测事实（1600×900，`/management/docs/git-workflow`）：窗口本身不滚动（`documentElement.scrollHeight 725 ≈ clientHeight 720`）；真正的滚动容器是 MainLayout `app-content`（naive-ui `n-layout-content` `:native-scrollbar="false"`）内部的 `.n-scrollbar-container`（scrollHeight 998 / clientHeight 664）。DocPage 内已有的 `scrollToHeading()` 用 `scrollIntoView` 定位，说明滚动由该容器承载。

## Goals / Non-Goals

**Goals:**

- 刷新后回到原阅读位置，长文精读不丢上下文
- 各文档位置独立、会话级隔离（sessionStorage）
- 不改 MainLayout，不动 naive-ui 组件配置；工具函数可复用

**Non-Goals:**

- 不做跨会话（localStorage）位置记忆——过期位置会误导
- 不做"阅读进度条""上次读到此处"提示等附加 UI
- 不改其它页面（列在后续可选，工具已就绪）
- 不改变 TOC 平滑滚动与面板收起逻辑

## Decisions

### D1: 存储用 sessionStorage，键含路由 path

- 键：`doc-scroll:${route.path}`；值：整数 scrollTop
- 选 sessionStorage：滚动位置属"瞬时上下文"，同一标签页刷新保留即可；新标签页从顶部更符合预期。面板收起偏好用 localStorage（长期偏好），二者语义不同，故不复用其存储
- 备选：localStorage → 隔天再打开会跳到中间，反直觉；URL hash → 会污染链接、且刷新本就可保留 hash，属另一机制

### D2: 容器定位放在工具函数里，不改布局

- `web/src/utils/scrollMemory.js` 暴露：
  - `findScrollContainer()`：查 `.app-content .n-scrollbar-container`（回退 `.n-scrollbar-container`）
  - `saveScrollPosition(key, el)` / `readScrollPosition(key)`
  - `restoreAfterRender(key, isReady)`：等待 `isReady()` 为真（或最多重试 N 次/超时）→ `nextTick` 后写入 scrollTop，再延迟 ~150ms 二次校正
- 理由：MainLayout 是共享脚手架核心文件，改它风险面大（影响全部页面）；选择器容错式读取实现同样的能力

### D3: 时机——保存节流 + 卸载兜底，恢复等渲染完成

- 保存：滚动事件节流 150ms 写入 sessionStorage；`onBeforeUnmount` 再兜底写一次（防止快速离页丢失最后位置）
- 恢复：等 `currentDoc` 就绪（`detailLoading` 结束且 `currentDoc` 有值）→ 恢复；再延迟 150ms 校正一次，吸收 Markdown 内图片/Mermaid 异步渲染引起的高度变化
- 明确不在"容器高度不足"时恢复（即内容未渲染完就写 scrollTop 会被浏览器截断到 0）

### D4: 分工——DocPage 只管接线

- DocPage 侧：`onMounted`/`watch(currentDoc)` 触发恢复；滚动监听挂在容器上；`onBeforeUnmount` 保存
- 切换文档：key 含 path，天然隔离；不做主动清除，返回旧文档时恢复其位置（与浏览器前进/后退直觉一致）

### D5: 静默降级

容器找不到、sessionStorage 不可用（隐私模式/配额）时不抛错：工具函数内部 try/catch + 直接 return，页面照常渲染（spec 已定义该行为）。

## Risks / Trade-offs

- [naive-ui 内部类名 `.n-scrollbar-container` 随版本变化] → 选择器集中在工具函数一处，便于随版本调整；找不到时静默降级不报错
- [恢复位置因图片/Mermaid 高度变化而偏移] → 二次延迟校正；仍可能小幅偏移（spec 已明确允许）
- [滚动监听带来额外开销] → 150ms 节流 + 组件卸载时移除监听
- [侧栏/TOC 内部也有滚动（sticky 自身滚动）] → 只挂主容器，避免误记侧栏位置

## Migration Plan

纯前端新增文件 + DocPage 接入，无迁移。回滚 = revert 该提交。

## Open Questions

（无）
