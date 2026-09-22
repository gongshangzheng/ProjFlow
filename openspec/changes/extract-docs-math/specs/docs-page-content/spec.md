## REMOVED Requirements

### Requirement: 文档正文支持 LaTeX 数学公式
**Reason**: 数学渲染是一块独立的能力面（定界符规则、失败降级、Mermaid 图内公式），混在「文档页内容契约」里既难检索也难演进；`openspec/specs/` 下查不到任何 `latex`/`math` 字样，容易被误判为「没有记录」。
**Migration**: 该要求及其 3 个 Scenario 原样迁到新能力 `docs-math`，行为不变；读者此后到 `openspec/specs/docs-math/spec.md` 查阅。

### Requirement: 公式解析失败可降级
**Reason**: 同属数学渲染能力，见上。
**Migration**: 迁到 `docs-math`，行为不变。

### Requirement: 不误吞普通美元符号
**Reason**: 同属数学渲染能力，见上。
**Migration**: 迁到 `docs-math`，行为不变。

### Requirement: Mermaid 图中的公式正确显示
**Reason**: 同属数学渲染能力，见上。
**Migration**: 迁到 `docs-math`，行为不变。
