---
name: frontend-performance
version: 1.0.0
description: This skill should be used when the user wants to optimize Next.js frontend performance using Lighthouse, bundle analysis, and animation best practices. Use when diagnosing slow pages, optimizing bundle size, or improving Core Web Vitals (LCP, TBT, CLS).
---

# Frontend Performance Optimization

Diagnose and fix performance issues in Next.js applications.

## Quick Diagnostics

### Run Lighthouse CLI

```bash
# Performance audit (headless)
npx lighthouse http://localhost:3000 --output=json --output-path=./lighthouse.json --chrome-flags="--headless" --only-categories=performance

# Parse key metrics
cat lighthouse.json | jq '{
  score: .categories.performance.score,
  FCP: .audits["first-contentful-paint"].displayValue,
  LCP: .audits["largest-contentful-paint"].displayValue,
  TBT: .audits["total-blocking-time"].displayValue,
  CLS: .audits["cumulative-layout-shift"].displayValue
}'

# Find slow scripts
cat lighthouse.json | jq '.audits["bootup-time"].details.items | .[0:8]'

# Main thread breakdown
cat lighthouse.json | jq '.audits["mainthread-work-breakdown"].details.items'
```

**Important**: Always test production builds (`next build && next start`), not dev mode. Dev mode has 2-10x overhead from HMR, source maps, and no optimizations.

### Bundle Analysis

```bash
# Install
bun add -d @next/bundle-analyzer

# Run analysis
ANALYZE=true bun run build
```

Configure in `next.config.js`:
```js
import bundleAnalyzer from '@next/bundle-analyzer'

const withBundleAnalyzer = bundleAnalyzer({
  enabled: process.env.ANALYZE === 'true',
})

export default withBundleAnalyzer(nextConfig)
```

## Common Fixes

### 1. optimizePackageImports

For libraries with many exports (icons, utilities, animation libraries):

```js
// next.config.js
const nextConfig = {
  experimental: {
    optimizePackageImports: [
      'framer-motion',
      'lucide-react',
      '@phosphor-icons/react',
      'lodash',
      'date-fns',
      '@heroicons/react',
    ],
  },
}
```

This ensures tree-shaking works correctly - only imports you use get bundled.

### 2. Framer Motion - Variants Pattern

**WRONG - Creates N animation controllers:**
```tsx
// Each element has its own animation state - expensive!
{items.map((item, i) => (
  <motion.div
    key={i}
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ delay: i * 0.05 }}  // Individual delays
  >
    {item}
  </motion.div>
))}
```

**RIGHT - Single controller with staggerChildren:**
```tsx
// Parent controls all children - efficient!
const containerVariants = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.05,
    },
  },
}

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { type: 'spring' as const, damping: 15 }
  },
}

<motion.div
  variants={containerVariants}
  initial="hidden"
  animate="visible"
>
  {items.map((item, i) => (
    <motion.div key={i} variants={itemVariants}>
      {item}
    </motion.div>
  ))}
</motion.div>
```

**Also avoid:**
- `filter: blur()` in animations - very expensive
- Too many infinite animations (reduce or use CSS)
- Individual `transition` props on children when using variants

### 3. Move Heavy Computation Server-Side

Keep these out of client bundles:
- Syntax highlighting: use `shiki` server-side, not `prism-react-renderer`
- Markdown parsing: render on server
- Date formatting libraries: consider `Intl.DateTimeFormat`
- Large data transformations: API routes or server components

### 4. Image Optimization

```tsx
// Always use next/image
import Image from 'next/image'

<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority  // For LCP images
  placeholder="blur"  // Reduces CLS
/>
```

### 5. Font Optimization

```tsx
// app/layout.tsx
import { Inter } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',  // Prevents FOIT
  preload: true,
})
```

### 6. External Packages (Server Only)

Prevent server-only packages from being bundled:

```js
// next.config.js
const nextConfig = {
  serverExternalPackages: ['sharp', 'canvas'],
}
```

## Performance Targets

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP | ≤2.5s | 2.5-4s | >4s |
| FCP | ≤1.8s | 1.8-3s | >3s |
| TBT | ≤200ms | 200-600ms | >600ms |
| CLS | ≤0.1 | 0.1-0.25 | >0.25 |

## Debugging Workflow

1. **Run production Lighthouse** - Get baseline metrics
2. **Check bootup-time audit** - Find slow scripts
3. **Run bundle analyzer** - Identify large chunks
4. **Fix largest issues first** - Usually 1-2 packages cause most problems
5. **Re-test** - Verify improvements

## Quick Wins Checklist

- [ ] Test production build, not dev
- [ ] Add `optimizePackageImports` for icon/utility libraries
- [ ] Use Framer Motion variants pattern
- [ ] Remove `filter: blur()` from animations
- [ ] Add `priority` to LCP images
- [ ] Use `next/font` with `display: swap`
- [ ] Move heavy libraries to server components
