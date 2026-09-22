## 1. 新增主色派生令牌

- [x] 1.1 `config/theme.js`：`accentFor()` 增加 `borderAlpha`（light `0.27` / dark `0.30`）
- [x] 1.2 `stores/theme.js` `applyAccent()`：写入 `--color-primary-border` = `toRgba(primary, borderAlpha)`
- [x] 1.3 `styles/index.scss` `:root` 兜底：加 `--color-primary-border: rgba(74, 79, 87, 0.27)`
- [x] 1.4 `styles/index.scss` `:root[data-theme='dark']` 兜底：加 `--color-primary-border: rgba(168, 174, 182, 0.30)`

## 2. 替换残留硬编码主色

- [x] 2.1 `PaperList.vue` `.stat-num` color → `var(--color-primary)`
- [x] 2.2 `PaperList.vue` 卡片 `:hover` border-color → `var(--color-primary-border)`
- [x] 2.3 `PaperList.vue` `&.pinned` 左边条 → `var(--color-primary)`，底色 `#fafaff` → `var(--color-primary-soft)`
- [x] 2.4 `PaperList.vue` `.paper-link` 边框色/文字色/hover 背景与边框 → `var(--color-primary)`（`.blog` 的 amber 保留）
- [x] 2.5 `Home.vue` `&.management .module-icon` → `var(--color-primary)`（papers/evaluation 分类色不动）
- [x] 2.6 `TeamDetail.vue` 头像 `backgroundColor` → `var(--color-primary)`

## 3. 死文件清理

- [x] 3.1 删除 `web/public/icons.svg`（全仓已确认无引用）
- [x] 3.2 复核 `web/public/` 剩余文件均有来源（`favicon.svg` 被 index.html 引用；`docs-data.json` 由构建产出）

## 4. 验证

- [x] 4.1 切换强调色（枪灰/青色/玫红）后，论文列表统计数字、卡片 hover 边框、pinned 边条、链接胶囊、首页项目管理图标、成员头像**全部随之变化**
- [x] 4.2 深色模式下 pinned 卡片底色不再是浅色块
- [x] 4.3 明暗切换后上述元素取对应模式色值
- [x] 4.4 `grep -rn "4f46e5\|6366f1\|4338ca\|818cf8" web/src` 仅命中 `config/theme.js` 的 indigo 预设定义
- [x] 4.5 `npm run build` 通过
- [x] 4.6 `openspec validate cleanup-stale-accent` 通过

## 5. 收尾

- [x] 5.1 以 `[shared]` 前缀提交
