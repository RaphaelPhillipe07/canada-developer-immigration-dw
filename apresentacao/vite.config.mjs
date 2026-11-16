import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({ base: './', plugins: [tailwindcss()], esbuild: { jsx: 'automatic' }, build: {rollupOptions: {output: {manualChunks(id) {if (id.includes('node_modules/recharts') || id.includes('node_modules/d3-')) return 'charts'; if (id.includes('node_modules/motion') || id.includes('node_modules/framer-motion')) return 'motion'}}}} })
