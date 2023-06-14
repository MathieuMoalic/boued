import { defineConfig } from 'vite'
import { VitePWA } from 'vite-plugin-pwa'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [svelte(), VitePWA({
    registerType: 'autoUpdate',
    devOptions: {
      enabled: true
    },
    includeAssets: ['background.avif', 'favicon.png'],
    manifestFilename: "manifest.json",
    manifest: {
      "name": "Groceries",
      "short_name": "Groceries",
      "icons": [
        {
          "src": "/favicon.png",
          "sizes": "512x512",
          "type": "image/png"
        }
      ],
      "start_url": "/index.html",
      "display": "standalone",
      "background_color": "rgb(131, 35, 0)",
      "theme_color": "red"
    }
    ,

  })],
})
