---
name: react-vite-best-practices
description: React and Vite performance optimization guidelines. Use when writing, reviewing, or optimizing React components built with Vite. Triggers on tasks involving Vite configuration, build optimization, code splitting, lazy loading, HMR, bundle size, or React performance.
license: MIT
metadata:
  author: agent-skills
  version: "1.0.0"
---

# React + Vite Best Practices

Comprehensive performance optimization guide for React applications built with Vite. Contains 40+ rules across 8 categories, prioritized by impact to guide code generation and refactoring.

## When to Apply

Reference these guidelines when:
- Configuring Vite for React projects
- Implementing code splitting and lazy loading
- Optimizing build output and bundle size
- Setting up development environment
- Reviewing code for performance issues

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Build Optimization | CRITICAL | `build-` |
| 2 | Code Splitting | CRITICAL | `split-` |
| 3 | Development Performance | HIGH | `dev-` |
| 4 | Asset Handling | HIGH | `asset-` |
| 5 | Environment Config | MEDIUM | `env-` |
| 6 | HMR Optimization | MEDIUM | `hmr-` |
| 7 | Bundle Analysis | LOW-MEDIUM | `bundle-` |
| 8 | Advanced Patterns | LOW | `advanced-` |

## Quick Reference

### 1. Build Optimization (CRITICAL)

- `build-manual-chunks` - Configure manual chunks for vendor separation
- `build-minify-terser` - Use Terser for production minification
- `build-target-modern` - Target modern browsers for smaller bundles
- `build-sourcemap-production` - Configure sourcemaps appropriately
- `build-output-structure` - Organize output directory structure
- `build-chunk-size-limit` - Set appropriate chunk size warnings

### 2. Code Splitting (CRITICAL)

- `split-route-lazy` - Use React.lazy() for route-based splitting
- `split-suspense-boundaries` - Wrap lazy components with Suspense
- `split-dynamic-imports` - Use dynamic imports for heavy components
- `split-preload-critical` - Preload critical chunks on interaction
- `split-named-chunks` - Use named chunks for better caching
- `split-vendor-separation` - Separate vendor from application code

### 3. Development Performance (HIGH)

- `dev-dependency-prebundling` - Configure dependency pre-bundling
- `dev-exclude-large-deps` - Exclude large deps from optimization
- `dev-warmup-frequent` - Warmup frequently used modules
- `dev-server-config` - Optimize dev server configuration
- `dev-hmr-overlay` - Configure HMR error overlay

### 4. Asset Handling (HIGH)

- `asset-inline-limit` - Set appropriate asset inline limit
- `asset-public-dir` - Configure public directory correctly
- `asset-import-syntax` - Use correct asset import syntax
- `asset-svg-components` - Handle SVGs as React components
- `asset-image-optimization` - Optimize image loading
- `asset-font-loading` - Optimize font loading strategy

### 5. Environment Configuration (MEDIUM)

- `env-vite-prefix` - Use VITE_ prefix for client variables
- `env-type-definitions` - Type environment variables
- `env-mode-specific` - Use mode-specific env files
- `env-sensitive-data` - Never expose sensitive data
- `env-build-time` - Understand build-time replacement

### 6. HMR Optimization (MEDIUM)

- `hmr-fast-refresh` - Ensure Fast Refresh works correctly
- `hmr-preserve-state` - Preserve component state during HMR
- `hmr-boundary-setup` - Set up proper HMR boundaries
- `hmr-custom-handlers` - Implement custom HMR handlers

### 7. Bundle Analysis (LOW-MEDIUM)

- `bundle-visualizer` - Use rollup-plugin-visualizer
- `bundle-analyze-deps` - Analyze dependency sizes
- `bundle-tree-shaking` - Ensure proper tree shaking
- `bundle-dead-code` - Eliminate dead code
- `bundle-css-splitting` - Configure CSS code splitting

### 8. Advanced Patterns (LOW)

- `advanced-ssr-config` - Configure for SSR if needed
- `advanced-library-mode` - Build as library
- `advanced-multi-page` - Multi-page application setup
- `advanced-worker-threads` - Web Worker integration
- `advanced-wasm` - WebAssembly integration

## Essential Configurations

### Recommended vite.config.ts

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],

  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },

  build: {
    target: 'esnext',
    minify: 'terser',
    sourcemap: false,
    chunkSizeWarningLimit: 500,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom'],
        },
      },
    },
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
      },
    },
  },

  optimizeDeps: {
    include: ['react', 'react-dom'],
  },

  server: {
    port: 3000,
    open: true,
    hmr: {
      overlay: true,
    },
  },
})
```

### Route-Based Code Splitting

```typescript
import { lazy, Suspense } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'

// Lazy load route components
const Home = lazy(() => import('./pages/Home'))
const Dashboard = lazy(() => import('./pages/Dashboard'))
const Settings = lazy(() => import('./pages/Settings'))

// Named chunks for better debugging
const Profile = lazy(() =>
  import(/* webpackChunkName: "profile" */ './pages/Profile')
)

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<LoadingSpinner />}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/profile" element={<Profile />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  )
}
```

### Environment Variables

```typescript
// src/vite-env.d.ts
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL: string
  readonly VITE_APP_TITLE: string
  readonly VITE_ENABLE_ANALYTICS: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
```

```typescript
// Usage
const apiUrl = import.meta.env.VITE_API_URL
const isDev = import.meta.env.DEV
const isProd = import.meta.env.PROD
```

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/build-manual-chunks.md
rules/split-route-lazy.md
rules/_sections.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references
