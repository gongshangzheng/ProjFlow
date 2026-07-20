import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
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
})
