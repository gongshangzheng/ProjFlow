# Tasks: docs-system

## 1. 体系治理

- [x] 1.1 文档登记表落库（本 design）
- [ ] 1.2 双层流程写入 `.agents/skills/documentation/SKILL.md` §0（总 Change + 单篇 Change、design 先行、豁免标准、结构变更纪律）
- [ ] 1.3 各篇补齐单篇 Change（按需，结构级变更时开）

## 2. 引用健康

- [ ] 2.1 api-design-conventions、git-workflow 引用闭合核对（悬空 = 0）

## 3. 文档系统功能（前端 / 渲染层）

- [ ] 3.1 TOC 强调符号处理：`extractToc` 丢弃（或渲染）标题中的 `**`，不显示符号字符（`web/src/utils/markdown.js`）
- [ ] 3.2 **sidecar json 约定**：字段 schema（changelog / progress / appendix / related）+ 后端 `get_doc_detail` 读取同名 `<slug>.json` 一并返回，解析失败降级为空对象（`server/routers/management.py`）
- [ ] 3.3 **渲染**：DocPage 顶部按钮（演进记录 / 进度，n-modal 弹层）+ 底部独立块（相关文档 / 附录）；无字段不渲染空块（`web/src/views/management/DocPage.vue`）
- [ ] 3.4 共享脚手架 port 回上游：整理 `[shared]` commit，format-patch 后在上游 `git am`，注明源自 pet-action-recognition docs-system
