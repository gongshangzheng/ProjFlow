# Tasks: docs-system

## 1. 体系治理

- [x] 1.1 文档登记表落库（本 design）
- [x] 1.2 双层流程写入 `.agents/skills/documentation/SKILL.md` §0（总 Change + 单篇 Change、design 先行、豁免标准、结构变更纪律）
- [x] 1.3 各篇补齐单篇 Change（按需触发：当前两篇均无结构级变更需求，待首次单篇重构时开 docs-<slug>；依据为 2026-09-20 引用核对时两篇内容稳定）

## 2. 引用健康

- [x] 2.1 api-design-conventions、git-workflow 引用闭合核对（悬空 = 0）

## 3. 文档系统功能（前端 / 渲染层）

- [x] 3.1 TOC 强调符号处理：`extractToc` 丢弃（或渲染）标题中的 `**`，不显示符号字符（`web/src/utils/markdown.js`）
- [x] 3.2 **sidecar json 约定**：字段 schema（changelog / progress / appendix / related）+ 后端 `get_doc_detail` 读取同名 `<slug>.json` 一并返回，解析失败降级为空对象（`server/routers/management.py`）
- [x] 3.3 **渲染**：DocPage 顶部按钮（演进记录 / 进度，n-modal 弹层）+ 底部独立块（相关文档 / 附录）；无字段不渲染空块（`web/src/views/management/DocPage.vue`）
- [x] 3.4 共享脚手架 port 回上游：以 cherry-pick 方式完成（bd91ac2 剔除 pet 领域文档、fe046fe），源自 pet-action-recognition cb76c36
