## 1. 色表与工具

- [x] 1.1 新增 `web/src/config/theme.js`：`DEFAULT_ACCENT` + `ACCENTS`（8 色，每色 light/dark 两值）
- [x] 1.2 同文件提供 `mix(hex, target, ratio)`（派生 hover/pressed）与 `toRgba(hex, alpha)`（派生 soft/selected），并导出 `accentFor(key, isDark)`
- [x] 1.3 同文件导出 `accentThemeOverrides(key, isDark)`，返回 Naive `common` 覆盖对象（primary/hover/pressed/suppl）

## 2. 状态与注入

- [x] 2.1 `stores/theme.js`：新增 `accent` 状态（初值读 `projflow-accent`，缺失用 `DEFAULT_ACCENT`）
- [x] 2.2 `stores/theme.js`：新增 `setAccent(key)`——写入 state + localStorage + 应用 CSS 变量
- [x] 2.3 `stores/theme.js`：抽出 `applyAccent()`，写 `<html>` 的 `--color-primary` / `--color-primary-soft` / `--color-selected`；`init()` 与 `toggle()` 后均调用
- [x] 2.4 `App.vue`：`themeOverrides` 改为 `computed(() => ({ common: { ...accentThemeOverrides(accent, isDark), borderRadius: '8px' } }))`；删除写死的 `#4f46e5` 等三行

## 3. 顶栏入口

- [x] 3.1 `MainLayout.vue`：`header-right` 在明暗按钮旁加调色盘按钮（`ColorPaletteOutline`，`quaternary circle`，与现有按钮同款）
- [x] 3.2 用 `n-popover` 展开色板：网格列出 `ACCENTS` 的色块 + 名称，当前项加对勾，点击调用 `themeStore.setAccent(key)` 并关闭
- [x] 3.3 色板样式（布局在 MainLayout 的 `<style scoped>` 或 `styles/index.scss`）：色块圆形、hover 描边、选中描边 + 对勾
- [x] 3.4 按钮加 `title="主题色"`，与现有按钮的可访问性一致

## 4. 验证

- [x] 4.1 切换任一强调色：顶栏按钮、菜单选中态、标签、文档页选中项同时变色（Naive 与自定义元素一致）
- [x] 4.2 刷新后仍为所选色；清除 `projflow-accent` 后回到靛蓝
- [x] 4.3 明暗模式切换：强调色保持所选，色值切换到对应变体
- [x] 4.4 `projflow-theme` 与 `projflow-accent` 互不覆盖
- [x] 4.5 逐个目视 8 色在 light / dark 下的对比度，无明显不可读
- [x] 4.6 `npm run build` 通过

## 5. 收尾

- [x] 5.1 `openspec validate add-accent-color-picker` 通过
- [x] 5.2 以 `[shared]` 前缀提交
