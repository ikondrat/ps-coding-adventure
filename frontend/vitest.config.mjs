import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import path from 'path'

export default defineConfig({
  plugins: [svelte()],
  esbuild: {
    // Transpile all files with ESBuild to remove comments from code coverage.
    // Required for `test.coverage.ignoreEmptyLines` to work:
    include: ['**/*.js', '**/*.jsx', '**/*.mjs', '**/*.ts', '**/*.tsx']
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['src/setupTest.ts'],
    coverage: {
      provider: 'v8',
      ignoreEmptyLines: true
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src/renderer/src')
    }
  }
})
