## Purpose

区分全局的共享机运行能力与项目自身的远程运行手册，使技能发现不会遮蔽全局入口，并让已有项目自动化继续使用原先的脚本路径。

## ADDED Requirements

### Requirement: Project runtime documentation does not shadow global remote operations

ProjFlow SHALL register its project runtime documentation as `remote-runtime` and SHALL NOT register a project skill named `remote-ops`. Existing runtime script paths and behavior SHALL remain unchanged.

#### Scenario: Discovering remote skills in ProjFlow

- **WHEN** a session discovers project and global skills in ProjFlow
- **THEN** `remote-runtime` names the project handbook and `remote-ops` remains available from the global installation without a project candidate

#### Scenario: Existing callers still use the old script directory

- **WHEN** an existing caller uses a runtime script under the existing `remote-ops/scripts/` path
- **THEN** the script remains present with the same content and contract
