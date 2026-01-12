import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
// import vueDevTools from 'vite-plugin-vue-devtools'  <-- COMMENT THIS OUT

export default defineConfig({
  plugins: [
    vue(),
  ],

  define: {
    global: 'window',
  },

  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },

  build: {
    target: 'esnext'
  }
})