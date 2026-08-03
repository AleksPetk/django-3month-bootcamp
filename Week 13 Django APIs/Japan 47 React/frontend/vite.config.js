import { writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

const publicRoutes = ['', 'regions', 'prefectures', 'places', 'search', 'privacy', 'terms']

// Static crawl files are generated from the deployment URL, avoiding a domain
// hardcode while still producing valid absolute sitemap locations.
function seoFiles(publicUrl) {
  const origin = publicUrl.replace(/\/$/, '')
  return {
    name: 'japan47-seo-files',
    transformIndexHtml(html) {
      return html.replaceAll('https://example.com/', `${origin}/`)
    },
    closeBundle() {
      const urls = publicRoutes.map((route) => `  <url><loc>${origin}/${route}</loc></url>`).join('\n')
      writeFileSync(resolve('dist/sitemap.xml'), `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n</urlset>\n`)
      writeFileSync(resolve('dist/robots.txt'), `User-agent: *\nAllow: /\nDisallow: /profile/\nDisallow: /my-travel\nDisallow: /login\nDisallow: /register\nSitemap: ${origin}/sitemap.xml\n`)
    },
  }
}

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, '.', '')
  return {
  plugins: [react(), seoFiles(env.VITE_PUBLIC_URL || 'http://localhost:5173')],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8000',
      '/media': 'http://localhost:8000',
      '/static': 'http://localhost:8000',
    },
  },
  test: {
    environment: 'jsdom',
    setupFiles: './src/testSetup.js',
  },
}})
