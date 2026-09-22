# extract-docs-math

## Why

`add-latex-math` 把数学渲染的 4 条要求加进了**已有的** `docs-page-content`（文档页内容契约）。结果是：

- `openspec/specs/` 下**查不到任何** `latex` / `math` 字样——它只是 `docs-page-content` 里的四节；
- 同样地，也只有熟悉那次 change 的人才找得到「公式渲染契约写在哪」；
- 我在本会话中就因此被质疑过一次「引入 LaTeX 没有 OpenSpec 记录」。

数学渲染本身是一块**独立能力面**（定界符规则、失败降级、不误吞美元符号、Mermaid 图内公式），与「文档页内容契约」的其余部分（锚点、排序、文件夹顺序）没有耦合，混在一起既难检索也难演进。

## What Changes

- 新建 capability `docs-math`，承载原本的 4 条要求（内容原样搬迁，行为不变）：
  - 文档正文支持 LaTeX 数学公式
  - 公式解析失败可降级
  - 不误吞普通美元符号
  - Mermaid 图中的公式正确显示
- `docs-page-content` 中这 4 条以 `REMOVED Requirements` 声明移除，附 **Reason** 与 **Migration**（指向 `docs-math`）。

## Capabilities

### New Capabilities

- `docs-math`: 文档正文与 Mermaid 图中 LaTeX 数学公式的渲染契约（支持的定界符、渲染结果、失败降级、美元符号边界）。

### Modified Capabilities

- `docs-page-content`: 移除 4 条数学相关要求（迁往 `docs-math`），其余要求（锚点接管、链接行为、`order`、排序链、文件夹顺序）保持不变。

## Impact

- 规范：新增 `openspec/specs/docs-math/`；`openspec/specs/docs-page-content/spec.md` 变短。
- 代码、行为、API：**完全不动**（纯规范重划，`MarkdownRenderer` 的实现在 `add-latex-math` 已完成并验证）。
- 引用：`.agents/skills/documentation/SKILL.md` 的公式节曾注明「契约见 `docs-page-content`」，需改为 `docs-math`。
- 说明：**不**改 `openspec/registry.md` —— 那是 wiki **文档**的登记表，不登记 capability；我此前口头提到「加两行到 registry.md」是口误，本次不做。
