import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite';
import Components from 'unplugin-vue-components/vite';
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(),
        AutoImport({
            resolvers: [ElementPlusResolver()],
        }),
        Components({
            resolvers: [ElementPlusResolver()],
        }),],
    css: {
        preprocessorOptions: {
            scss: {
                additionalData: '@import "./src/style/main.scss";',
            },
        },
    },
    server: {
        proxy: {
            /*
      代理所有以/api开头的请求，将其转发给后端，后端路径不携带/api的，自动去掉
      */
            '/api': {
                target: 'http://127.0.0.1:5000', //要跨域的路径，实际访问的地址
                changeOrigin: true, //是否跨域
                rewrite: (path) => path.replace(/^\/api/, ''),
            },
        },
    },
})
