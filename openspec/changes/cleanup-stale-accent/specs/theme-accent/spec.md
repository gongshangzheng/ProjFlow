## ADDED Requirements

### Requirement: 主色不得硬编码

全站主色 SHALL 只通过运行时令牌（`--color-primary` 及其派生令牌）表达；组件样式 MUST NOT 硬编码某个强调色的具体色值，否则切换强调色时会出现不跟随的元素。

#### Scenario: 切换强调色后无残留主色元素

- **WHEN** 依次切换若干强调色并检查包含主色元素的页面（首页模块入口、论文列表统计与卡片、成员详情头像等）
- **THEN** 这些元素的主色全部随之变化，不存在固定为某一具体色值的元素

#### Scenario: 主色的派生态同样走令牌

- **WHEN** 需要主色的半透明变体（如卡片 hover 边框、选中底色）
- **THEN** 使用主色派生令牌（`--color-primary-soft` / `--color-primary-border` / `--color-selected`）而非硬编码 rgba/hex

### Requirement: 未使用的静态资源不得留在 public

仓库 SHALL NOT 在 `web/public/` 保留未被任何代码或页面引用的静态资源文件。

#### Scenario: 死资源清理

- **WHEN** 检查 `web/public/` 下的文件
- **THEN** 每个文件都能被追溯到某处引用（`index.html`、源码 import、或构建脚本产出）
