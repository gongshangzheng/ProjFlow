## 1. 新增灰色预设

- [x] 1.1 `web/src/config/theme.js`：`ACCENTS` 末尾追加 `{ key: 'gray', label: '枪灰', light: '#4a4f57', dark: '#a8aeb6' }`

## 2. 默认色与兜底

- [x] 2.1 `web/src/config/theme.js`：`DEFAULT_ACCENT` `'indigo' → 'gray'`
- [x] 2.2 `web/src/styles/variables.scss`：`$primary-color/-light/-dark` → `#4a4f57 / #60646b / #41464d`
- [x] 2.3 `web/src/styles/index.scss` `:root`：`--color-primary-soft` / `--color-selected` 改为枪灰 rgba
- [x] 2.4 `web/src/styles/index.scss` `:root[data-theme='dark']`：`--color-primary` → `#a8aeb6`，soft/selected 同步
- [x] 2.5 `web/src/styles/index.scss` blockquote 的 `border-left`：`$primary-color` → `var(--color-primary)`

## 3. 验证

- [x] 2.1 调色盘出现 9 个色块，末尾为「枪灰」
- [x] 2.2 浅色模式选枪灰：`--color-primary` = `#4a4f57`，Naive `--n-item-text-color-active` 同值
- [x] 2.3 深色模式选枪灰：`--color-primary` = `#a8aeb6`，Naive 变量同值
- [x] 2.4 刷新后仍为枪灰；`readAccent()` 对未知 key 的回落仍正常
- [x] 2.5 `npm run build` 通过

## 4. 收尾

- [x] 3.1 `openspec validate add-gray-accent` 通过
- [x] 3.2 以 `[shared]` 前缀提交
