## ADDED Requirements

### Requirement: 仓库文档根目录唯一

仓库的说明性文档 SHALL 统一置于 `management/docs/` 下；仓库根目录 MUST NOT 存在 `docs/` 目录。`AGENTS.md` 等结构说明文档 MUST 与实际目录保持一致，不得保留已删除目录的条目。

#### Scenario: 检查仓库顶层目录

- **WHEN** 检查仓库根目录
- **THEN** 不存在 `docs/` 目录，说明性文档位于 `management/docs/`

#### Scenario: 结构说明与实现一致

- **WHEN** 目录结构发生变化（新增或删除顶层目录）
- **THEN** `AGENTS.md` 的目录树在同一变更内同步更新，不残留已删除目录的条目
