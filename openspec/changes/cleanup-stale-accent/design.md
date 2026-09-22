## Context

- 强调色链已就位：`config/theme.js`（`ACCENTS` / `accentFor` / `toRgba`）→ `stores/theme.js`（写 `<html>` 的 `--color-primary` / `-soft` / `--color-selected`）→ `App.vue`（Naive `themeOverrides` computed）。
- 遗漏点：一批组件直接写了旧主色 `#4f46e5`（含 `#4f46e544`、`#fafaff`），不参与令牌。
- 现有令牌：`--color-primary`、`--color-primary-soft`（0.12/0.15）、`--color-selected`（0.08/0.12）。缺一个「中透明度」令牌给 hover 边框用。

## Goals / Non-Goals

**Goals:**

- 让残留的主色元素跟随强调色（含明暗两态）。
- 删掉未被引用的 `public/icons.svg`。
- 用 spec 约束防止再次硬编码。

**Non-Goals:**

- 不重构 `PaperList.vue` 自成一套的 slate 色板（`#64748b` / `#f8fafc` / `#1e293b` / `#94a3b8` / `#f1f5f9` 等）——整页接入主题令牌是独立工作。
- 不动 `TeamList.vue` 的 `colors` 多色头像轮换（刻意设计，非主色）。
- 不改 Naive 组件配色（已由 `themeOverrides` 覆盖）。

## Decisions

### D1: 新增 `--color-primary-border` 令牌（alpha 0.27 / 0.30）

`PaperList` 卡片 hover 边框原来写 `#4f46e544`（约 27% alpha）。直接换成 `--color-primary` 会过重、换成 `--color-primary-soft`（12%）又过淡，因此补一个中透明度令牌。

- light alpha `0.27`（对齐原 `44` ≈ 26.7%），dark alpha `0.30`。
- 与既有 `--color-primary-soft` / `--color-selected` 同源：由 `stores/theme.js` 用 `toRgba(primary, alpha)` 写入 `<html>`，`:root` 保留静态兜底。
- 备选：用 `color-mix(in srgb, var(--color-primary) 27%, transparent)` —— 少一个令牌，但需较新浏览器且与既有「JS 写变量」机制不一致，不采用。

### D2: pinned 卡片底用 `--color-primary-soft`

原 `#fafaff` 是「靛蓝极浅底」，在深色模式下是浅色块（与深色卡片冲突）。改用 `--color-primary-soft` 后明暗两态都是「主色的半透明叠加」，自动适配。

- 这是顺带修掉的深色模式缺陷，不只是换色。

### D3: `Home.vue` 只换「项目管理」那一个模块图标

三个模块图标分别是 indigo / sky / amber，是**分类色**；其中 indigo 恰好等于旧的默认主色，所以看起来像「主题色没跟上」。只把 management 换成 `var(--color-primary)`，另两个保持分类色。

- 备选：三个都跟随强调色 → 三个入口长得一样，失去分类识别，不采用。

### D4: 删除 `public/icons.svg` 并把「无死资源」写进 spec

实测 `grep -rn "icons.svg" web/src web/index.html web/vite.config.js` 无命中。该文件是 `159e4aa` 初始化时随某个模板带进来的社交图标 sprite（`bluesky-icon` 等）。

- 在 spec 里加一条「`web/public/` 不留未引用资源」，避免后续再次沉淀。

## Risks / Trade-offs

- [新增令牌后忘记同步 `:root` 兜底] → 同步改 `index.scss` 的 `:root` 与 `:root[data-theme='dark']`，并在验证里检查无 JS 时的兜底值。
- [`PaperList` 深色模式下仍有个别 slate 硬编码导致观感不一致] → 已在 Non-Goals 声明；本 change 只保证「主色元素跟随」。
- [删 `icons.svg` 若有外部引用（如某处 `<use href="/icons.svg#...">`）会 404] → 已全仓 grep 确认无引用；若下游有引用，其自行保留即可（下游可覆盖）。

## Migration Plan

纯前端，无数据迁移。回滚 = revert 提交；`icons.svg` 如需恢复可从 git 历史取回。
