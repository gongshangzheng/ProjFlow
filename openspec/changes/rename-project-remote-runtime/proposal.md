## Why

ProjFlow 的项目运行手册与全局 `remote-ops` 同名，导致全局能力被遮蔽。上游与下游应使用同一项目手册名，同时保留各项目现有运行契约。

## What Changes

- 将 ProjFlow 手册与语义引用改名为 `remote-runtime`；原有 `remote-ops/scripts/` 兼容路径和实现不变。
- 记录下游采用规则：有项目运行手册才注册 `remote-runtime`；只有过期引用的项目改指实际入口。
- Git 分支只承载本次命名变更，不推当前本地 `main` 的其他提交，不触及部署远端。

## Capabilities

### New Capabilities

- `project-remote-runtime`: 区分项目手册的可发现名称和全局远程能力，并保留旧项目脚本接口。

### Modified Capabilities

无。

## Impact

ProjFlow 项目技能和引用、下游同步说明。无运行时、服务器配置或授权改变。pet 的项目更名由其自身 change 跟踪。
