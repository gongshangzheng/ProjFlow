# Tasks: document-pick-propagation

## 1. SKILL.md 扩写

- [x] 1.1 「port 回上游」小节补全：fetch 下游本地路径命令、cherry-pick 序列、按归属分类的冲突解决速查表（design D2）、`[shared]` + 来源 SHA commit message 模板、pick 后收尾（重启 uvicorn / 勾选 change tasks / 浏览器验证）
- [x] 1.2 替换第 84 行疑问注释为实证结论（design D3），小节末注明实证来源 commit（bd91ac2 / aacb342，2026-09-20）
- [x] 1.3 注意事项补充：目标库 untracked 同名文件会阻塞 pick（先入库）；混合 commit 是常态

## 2. AGENTS.md 指向

- [x] 2.1 Git 工作流小节末尾加一行：跨库共享改进传播见 upstream-sync SKILL.md

## 3. 验证与提交

- [x] 3.1 通读更新后的 SKILL.md，确认与既有「下游同步上游」小节方向表述无矛盾；命令可复制执行（路径示例用占位符）
- [x] 3.2 提交：`docs: upstream-sync skill 补全 cherry-pick 双向传播实操方法`
