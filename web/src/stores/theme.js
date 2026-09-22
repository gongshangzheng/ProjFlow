import { defineStore } from 'pinia'
import { ACCENTS, DEFAULT_ACCENT, accentFor, toRgba } from '../config/theme'

const STORAGE_KEY = 'projflow-theme'
const ACCENT_KEY = 'projflow-accent'

function detectInitial() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved === 'light' || saved === 'dark') return saved
  } catch { /* ignore */ }
  // 默认跟随系统偏好
  if (window.matchMedia?.('(prefers-color-scheme: dark)').matches) return 'dark'
  return 'light'
}

function readAccent() {
  try {
    const saved = localStorage.getItem(ACCENT_KEY)
    if (ACCENTS.some((a) => a.key === saved)) return saved
  } catch { /* ignore */ }
  return DEFAULT_ACCENT
}

function apply(mode) {
  document.documentElement.setAttribute('data-theme', mode)
}

/** 把强调色写入 <html> 的 CSS 变量（inline 优先级高于样式表里的 :root 默认值）。 */
function applyAccent(accent, mode) {
  const a = accentFor(accent, mode === 'dark')
  const root = document.documentElement
  root.style.setProperty('--color-primary', a.primary)
  root.style.setProperty('--color-primary-soft', toRgba(a.primary, a.softAlpha))
  root.style.setProperty('--color-selected', toRgba(a.primary, a.selectedAlpha))
  root.setAttribute('data-accent', a.key)
}

export const useThemeStore = defineStore('theme', {
  state: () => ({
    mode: detectInitial(),
    accent: readAccent(),
  }),
  getters: {
    isDark: (state) => state.mode === 'dark',
  },
  actions: {
    init() {
      apply(this.mode)
      applyAccent(this.accent, this.mode)
    },
    toggle() {
      this.mode = this.mode === 'dark' ? 'light' : 'dark'
      try { localStorage.setItem(STORAGE_KEY, this.mode) } catch { /* ignore */ }
      apply(this.mode)
      // 明暗切换后强调色需换用对应模式色值
      applyAccent(this.accent, this.mode)
    },
    setAccent(key) {
      if (!ACCENTS.some((a) => a.key === key)) return
      this.accent = key
      try { localStorage.setItem(ACCENT_KEY, key) } catch { /* ignore */ }
      applyAccent(key, this.mode)
    },
  },
})
