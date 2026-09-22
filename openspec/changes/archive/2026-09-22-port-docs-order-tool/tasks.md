## 1. 移植工具

- [x] 1.1 新增 `.agents/skills/documentation/scripts/docs_order.py`（取自 digital-human）
- [x] 1.2 `--author` 改为必填（去掉默认人名）
- [x] 1.3 docstring / `--help` 示例路径改为上游语境（`management/docs/<目录>`），去掉领域子目录名
- [x] 1.4 确认脚本只用 Python 标准库、无新增依赖；`--help` 正常

## 2. 技能文档补约定

- [x] 2.1 新增「文档顺序工具」一节（放在 §2 之后、§3 Mermaid 之前）：三条命令示例、默认 dry-run、`--apply` 才写盘、`order` 空档策略、与后端排序链同源的说明、**仅写文档时手工调用**
- [x] 2.2 §2.1 文件规范：补 `order` 用 10/20/30 空档的约定
- [x] 2.3 sidecar 相关处：补 `related` 项必须是含 `slug` 与 `title` 的对象，不能是字符串
- [x] 2.4 文末新增「交付检查」清单（含论文笔记跑 `validate-note.py`）

## 3. 验证

- [x] 3.1 `python3 .agents/skills/documentation/scripts/docs_order.py --help` 退 0
- [x] 3.2 本仓库 `list management/docs` 输出 → `order` 与后端一致（`GET /api/management/docs` 同序）
- [x] 3.3 临时目录（复制 `management/docs/`）跑 `insert --create --apply`：新文件生成、顺序正确
- [x] 3.4 临时目录构造重复 `order` → `list` 返 2 并打印 DUPLICATE；`renumber --apply` **拒绝**（返 2，不改文件）；`renumber --force --apply` 才按当前阅读顺序规范化为 10/20/30…
- [x] 3.5 临时目录构造「两个 `order:` 行」→ 工具拒绝（非 0 退出），文件未被改写
- [x] 3.6 本仓库 `management/docs/` **零改动**（`git status` 不含它）
- [x] 3.7 `openspec validate --all --strict` 通过

## 4. 收尾

- [x] 4.1 提交（`[shared]`）并 push
- [x] 4.2 归档
