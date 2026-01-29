---
name: vite-react-best-practices
description: Comprehensive React and Vite SPA performance, architecture, and deployment guidelines. Use this skill when building, reviewing, or refactoring React applications built with Vite (SPA). Covers Vite-specific build configurations, static hosting requirements, and core React performance patterns.
license: MIT
metadata:
  author: ant-gravity
  version: "1.1.0"
---

# Vite React Best Practices

A senior-level guide for building production-ready React Single Page Applications (SPAs) with Vite.

## When to Apply

Reference these guidelines when:
- Setting up a new Vite + React project
- Configuring build pipelines and CI/CD for SPAs
- Troubleshooting production build or caching issues
- Refactoring React components for performance

## Rule Categories

### 1. Vite SPA Deployment (CRITICAL)

- [Static Rewrites](rules/vite-spa-rewrites.md) - **Mandatory** for client-side routing.
- [Caching Strategy](rules/vite-caching-strategy.md) - Immutable assets, no-cache index.html.
- [Build Validation](rules/vite-build-validation.md) - Preview before push.
- [Environment Variables](rules/vite-env-vars.md) - `VITE_` prefix and security.

### 2. React Core Performance

- [Route Splitting](rules/react-route-splitting.md) - Lazy load pages.
- [Server State](rules/react-server-state.md) - Use React Query/SWR.
- [Memoization](rules/react-memoization.md) - When to use useMemo/useCallback.
- [Image Optimization](rules/react-image-optimization.md) - CLS prevention.

### 3. Architecture & Cleanup

- [Colocation](rules/react-colocation.md) - Feature-based structure.
- [Anti-Patterns: Import from Dist](rules/anti-import-dist.md) - Avoid bundling twice.
- [Troubleshooting](rules/vite-troubleshooting.md) - Common Vite fixes.

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
