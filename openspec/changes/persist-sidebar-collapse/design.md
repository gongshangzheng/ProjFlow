## Context

- `MainLayout.vue:88` 是 `const collapsed = ref(false)`，`@collapse` / `@expand` 只改内存 ref，无任何持久化。
- `DocPage.vue` 已有一套同类实现可参照：

```js
const SIDEBAR_COLLAPSED_KEY = 'doc-page.sidebar-collapsed'
function readStoredBool(key) {
  try { return localStorage.getItem(key) === '1' } catch { return false }
}
function writeStoredBool(key, value) {
  try { localStorage.setItem(key, value ? '1' : '0') } catch { /* ignore */ }
}
```

- 本仓库已有的「下游可覆盖配置」惯例：`web/src/config/hidden.js`（`HIDDEN_KEYS`）、`server/config.py`（`OUTPUTS_DIR` 等）。
- `web/layouts/MainLayout.vue` 属共享脚手架层（上游所有），改动以 `[shared]` 提交。

## Goals / Non-Goals

**Goals:**

- 主侧边栏折叠状态跨刷新保留。
- 首次访问默认折叠，且默认值可配置、与组件逻辑分离。
- 存储不可用时静默降级。

**Non-Goals:**

- 不改文档页两侧面板（`DocPage.vue`）的折叠逻辑与默认值——它们已持久化，且默认展开是刻意的（文档阅读需要目录）。
- 不改 `n-layout-sider` 的宽度、触发器样式或折叠动画。
- 不改菜单内容与 `HIDDEN_KEYS` 过滤逻辑。

## Decisions

### D1: 存储键命名 `app.sidebar-collapsed`，值用 `'1'` / `'0'`

沿用 `DocPage.vue` 的 `doc-page.sidebar-collapsed` 命名与取值风格，形成「`<域>.<控件>-collapsed`」的一致约定。

- 理由：与既有 key 同构，便于排查与文档化；用 `'1'`/`'0'` 而非 JSON 字符串，避免解析分支。
- 备选：存 JSON / Pinia persistedstate —— 为一个布尔引入序列化层，过重，不采用。

### D2: 默认值放独立配置模块 `web/src/config/layout.js`

```js
export const SIDEBAR_DEFAULT_COLLAPSED = true
```

- 理由：默认折叠是**产品决策**而非组件内部细节；上游组件逻辑保持通用，下游可一行覆盖。与 `hidden.js` / `config.py` 的既有惯例一致。
- 备选：直接写死在 `MainLayout.vue` 的常量里 —— 下游想改默认值就得改组件文件，与上游产生无谓分叉，不采用。
- 备选：放进 `hidden.js` —— 那是「菜单/功能隐藏」的语义，塞布局默认值会污染职责，不采用。

### D3: 读取用 `try/catch` 兜底，写入用 `watch`

读取：`localStorage.getItem` 可能因隐私模式抛异常 → `try/catch` 返回默认值。

写入：用 `watch(collapsed, ...)` 而不是在 `@collapse`/`@expand` 里写 —— 后者只在通过 UI 触发时生效，若将来新增其它改变折叠状态的入口会漏写。

- `watch` 不设 `immediate`，避免初始化时把默认值写进存储（否则用户永远无法通过「删除 key」回到默认）。

### D4: `[shared]` 提交，下游默认值需自行覆盖

上游默认设为折叠（`true`）满足本仓库诉求；下游若希望展开为默认，改 `SIDEBAR_DEFAULT_COLLAPSED` 即可。

- 理由：持久化是通用能力；默认值是各库自己的产品选择。

## Risks / Trade-offs

- [首次访问即折叠，演示时显得"缺了导航"] → 折叠态仍保留图标 + 触发器，且用户展开一次后即持久化；如需展开为默认，改配置一行。
- [下游不知有该配置，继承到不想要的默认值] → 在 `layout.js` 写清注释「仅在无本地偏好时生效，下游可覆盖」，并在本 change 的 Impact 中声明。
- [与 `DocPage` 的 key 冲突] → key 明确分域（`app.` / `doc-page.`），spec 中有互不影响 Scenario。

## Migration Plan

纯前端，无数据迁移。回滚 = revert 提交；已写入的 localStorage key 残留无害（下次访问按默认值即可，或手动清除）。
