import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig(({ command, isPreview }) => ({
  // 构建产物部署在 GitHub Pages 子路径下（https://<user>.github.io/ProjFlow/）。
  // 只在「开发服务器」用根路径，避免把日常访问地址改成 http://localhost:3210/ProjFlow/；
  // 构建与 `vite preview` 都用子路径 —— preview 的 command 也是 'serve'，
  // 若不算进来，预览会以 / 为基路径，而产物引用的是 /ProjFlow/... 导致资源 404。
  base: command === 'build' || isPreview ? '/ProjFlow/' : '/',
  plugins: [vue()],
  server: {
    port: 3210,
    proxy: {
      '/api': {
        target: 'http://localhost:8809',
        changeOrigin: true,
      },
    },
  },
}))
