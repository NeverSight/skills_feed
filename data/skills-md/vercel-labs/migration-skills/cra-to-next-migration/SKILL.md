---
name: cra-to-next-migration
description: Comprehensive guide for migrating Create React App (CRA) projects to Next.js. Use when migrating a CRA app, converting React Router to file-based routing, or adopting Next.js patterns like Server Components, App Router, or image optimization.
license: MIT
metadata:
  author: community
  version: "1.0.0"
---

# CRA to Next.js Migration Guide

Comprehensive migration guide for converting Create React App projects to Next.js, covering routing, data fetching, components, styling, and deployment. Contains 148 rules across 17 categories, prioritized by migration impact. After a successful migration the application should work the same as it did before the migration.

## When to Apply

Reference these guidelines when:

- Migrating an existing CRA application to Next.js
- Converting React Router routes to file-based routing
- Adopting Server Components in a client-heavy app
- Moving from client-side rendering to SSR/SSG
- Updating environment variables for Next.js
- Optimizing images and fonts with Next.js built-ins

## Version Policy

**Use Next.js 16.x or later. Do NOT use Next.js 14.x or 15.x.**

Before starting migration, check the current latest version:

```bash
npm info next version
```

Use the latest version in your package.json with a caret for minor/patch updates. The minimum supported version for this migration guide is `^16.0.0`.

## Rule Categories by Priority

| Priority | Category              | Impact   | Prefix          | Rules |
| -------- | --------------------- | -------- | --------------- | ----- |
| 1        | Project Setup         | CRITICAL | `setup-`        | 6     |
| 2        | Dependencies          | CRITICAL | `deps-`         | 1     |
| 3        | Routing               | CRITICAL | `routing-`      | 17    |
| 4        | Data Fetching         | CRITICAL | `data-`         | 11    |
| 5        | Components            | HIGH     | `components-`   | 9     |
| 6        | Environment Variables | HIGH     | `env-`          | 6     |
| 7        | Styling               | HIGH     | `styling-`      | 12    |
| 8        | Public Assets         | MEDIUM   | `assets-`       | 5     |
| 9        | Images                | MEDIUM   | `images-`       | 8     |
| 10       | Fonts                 | MEDIUM   | `fonts-`        | 6     |
| 11       | SEO & Metadata        | MEDIUM   | `seo-`          | 9     |
| 12       | API Routes            | MEDIUM   | `api-`          | 9     |
| 13       | State Management      | MEDIUM   | `state-`        | 8     |
| 14       | Integrations          | MEDIUM   | `integrations-` | 1     |
| 15       | Testing               | LOW      | `testing-`      | 9     |
| 16       | Build & Deploy        | LOW      | `build-`        | 7     |
| 17       | Common Gotchas        | HIGH     | `gotchas-`      | 24    |

## Quick Reference

### 1. Project Setup (CRITICAL)

- `setup-initial-structure` - Convert CRA folder structure to Next.js App Router
- `setup-package-json` - Update dependencies and scripts
- `setup-next-config` - Create and configure next.config.js
- `setup-typescript` - Migrate TypeScript configuration
- `setup-eslint` - Update ESLint for Next.js
- `setup-gitignore` - Update .gitignore for Next.js

### 2. Dependencies (CRITICAL)

- `deps-react19-compatibility` - Upgrade dependencies for React 19 compatibility

### 3. Routing (CRITICAL)

- `routing-basic-pages` - Convert components to file-based routes
- `routing-dynamic-routes` - Use [param] syntax for dynamic segments
- `routing-catch-all-routes` - Use [...slug] for catch-all routes
- `routing-optional-catch-all` - Use [[...slug]] for optional catch-all
- `routing-route-groups` - Use (group) folders for organization
- `routing-parallel-routes` - Use @slot for parallel routes
- `routing-intercepting-routes` - Use (..) for intercepting routes
- `routing-link-component` - Replace react-router Link with next/link
- `routing-programmatic-navigation` - Replace useNavigate with useRouter
- `routing-use-params` - Replace useParams with Next.js params
- `routing-use-search-params` - Replace useSearchParams properly
- `routing-nested-layouts` - Convert nested routes to layouts
- `routing-loading-states` - Add loading.tsx for suspense
- `routing-error-boundaries` - Add error.tsx for error handling
- `routing-not-found` - Add not-found.tsx for 404 pages
- `routing-hash-based` - Handle hash-based routing for client-only apps
- `routing-protected-routes` - Implement protected route patterns

### 4. Data Fetching (CRITICAL)

- `data-useeffect-to-rsc` - Convert useEffect fetches to Server Components
- `data-useeffect-to-ssr` - Convert useEffect to getServerSideProps
- `data-useeffect-to-ssg` - Convert useEffect to getStaticProps
- `data-client-fetch` - Keep client fetches with proper patterns
- `data-server-actions` - Use Server Actions for mutations
- `data-revalidation` - Configure data revalidation strategies
- `data-streaming` - Use Suspense for streaming data
- `data-parallel-fetching` - Fetch data in parallel on server
- `data-sequential-fetching` - Handle sequential data dependencies
- `data-caching` - Configure fetch caching behavior
- `data-client-library-init` - Initialize client-only libraries in useEffect

### 5. Components (HIGH)

- `components-use-client` - Add 'use client' directive for client components
- `components-server-default` - Understand server components are default
- `components-boundary-placement` - Place client boundaries strategically
- `components-composition` - Use composition to minimize client JS
- `components-interleaving` - Interleave server and client components
- `components-props-serialization` - Ensure props are serializable
- `components-children-pattern` - Pass server components as children
- `components-context-providers` - Handle Context providers properly
- `components-third-party` - Wrap third-party client components

### 6. Environment Variables (HIGH)

- `env-prefix-change` - Change REACT*APP* to NEXT*PUBLIC*
- `env-server-only` - Use non-prefixed vars for server-only
- `env-runtime-config` - Use runtime configuration when needed
- `env-local-files` - Understand .env file loading order
- `env-build-time` - Understand build-time vs runtime env vars
- `env-validation` - Validate required environment variables

### 7. Styling (HIGH)

- `styling-global-css` - Move global CSS to app/layout.tsx
- `styling-css-modules` - CSS Modules work with minor changes
- `styling-sass` - Configure Sass support
- `styling-tailwind` - Configure Tailwind CSS
- `styling-css-in-js` - Handle CSS-in-JS libraries
- `styling-styled-components` - Configure styled-components for SSR
- `styling-emotion` - Configure Emotion for SSR
- `styling-component-styles` - Import component styles properly
- `styling-postcss` - Configure PostCSS
- `styling-scss-global-syntax` - Use :global only in CSS Modules
- `styling-css-import-order` - Control CSS import order in layouts
- `styling-dark-mode-hydration` - Handle dark mode without hydration mismatch

### 8. Public Assets (MEDIUM)

- `assets-public-folder` - Public folder works the same way
- `assets-static-imports` - Use static imports for assets
- `assets-absolute-urls` - Reference assets without public prefix
- `assets-favicon` - Place favicon in app directory
- `assets-manifest` - Configure web app manifest

### 9. Images (MEDIUM)

- `images-next-image` - Replace img with next/image
- `images-required-dimensions` - Provide width and height
- `images-fill-prop` - Use fill for responsive images
- `images-priority` - Use priority for LCP images
- `images-placeholder` - Configure blur placeholders
- `images-remote-patterns` - Configure remote image domains
- `images-loader` - Configure custom image loaders
- `images-optimization` - Understand automatic optimization

### 10. Fonts (MEDIUM)

- `fonts-next-font` - Use next/font for optimization
- `fonts-google-fonts` - Load Google Fonts properly
- `fonts-local-fonts` - Load local font files
- `fonts-variable-fonts` - Configure variable fonts
- `fonts-font-display` - Configure font-display strategy
- `fonts-preload` - Understand automatic font preloading

### 11. SEO & Metadata (MEDIUM)

- `seo-metadata-api` - Use Metadata API instead of react-helmet
- `seo-dynamic-metadata` - Generate dynamic metadata
- `seo-opengraph` - Configure Open Graph metadata
- `seo-twitter-cards` - Configure Twitter Card metadata
- `seo-json-ld` - Add structured data (JSON-LD)
- `seo-canonical` - Set canonical URLs
- `seo-robots` - Configure robots meta tags
- `seo-sitemap` - Generate sitemap.xml
- `seo-head-component` - Migrate from next/head to Metadata

### 12. API Routes (MEDIUM)

- `api-route-handlers` - Create Route Handlers in app/api
- `api-http-methods` - Export named functions for HTTP methods
- `api-request-body` - Parse request body properly
- `api-query-params` - Access query parameters
- `api-headers-cookies` - Access headers and cookies
- `api-response-types` - Return proper response types
- `api-middleware` - Implement middleware patterns
- `api-cors` - Configure CORS properly
- `api-rate-limiting` - Implement rate limiting

### 13. State Management (MEDIUM)

- `state-context-client` - Context requires 'use client'
- `state-zustand` - Zustand works with hydration care
- `state-redux` - Configure Redux with Next.js
- `state-jotai` - Configure Jotai properly
- `state-recoil` - Configure Recoil properly
- `state-url-state` - Use URL for shareable state
- `state-server-state` - Minimize client state with RSC
- `state-persistence` - Handle state persistence

### 14. Integrations (MEDIUM)

- `integrations-sentry` - Migrate Sentry error monitoring

### 15. Testing (LOW)

- `testing-jest-config` - Update Jest configuration
- `testing-react-testing-library` - RTL works the same
- `testing-server-components` - Test Server Components
- `testing-client-components` - Test Client Components
- `testing-async-components` - Test async components
- `testing-mocking` - Mock Next.js modules
- `testing-e2e-cypress` - Configure Cypress for Next.js
- `testing-e2e-playwright` - Configure Playwright for Next.js
- `testing-api-routes` - Test API Route Handlers

### 16. Build & Deployment (LOW)

- `build-scripts` - Update build scripts
- `build-output` - Understand build output
- `build-standalone` - Configure standalone output
- `build-static-export` - Configure static export
- `build-bundle-analysis` - Analyze bundle size
- `build-vercel` - Deploy to Vercel
- `build-docker` - Configure Docker deployment

### 17. Common Gotchas (HIGH)

- `gotchas-window-undefined` - Handle window/document in SSR
- `gotchas-hydration-mismatch` - Fix hydration mismatches
- `gotchas-use-effect-timing` - Understand useEffect in Next.js
- `gotchas-router-ready` - Check router.isReady for query params
- `gotchas-dynamic-imports` - Use next/dynamic properly
- `gotchas-api-routes-edge` - Edge vs Node.js runtime
- `gotchas-middleware` - Middleware runs on edge
- `gotchas-static-generation` - Static vs dynamic rendering
- `gotchas-redirect` - Handle redirects properly
- `gotchas-headers` - Set response headers
- `gotchas-cookies` - Handle cookies in RSC
- `gotchas-turbopack` - Handle Turbopack compatibility issues
- `gotchas-empty-modules` - Fix empty module exports for isolatedModules
- `gotchas-nullish-coalescing` - Fix nullish coalescing runtime errors
- `gotchas-react19-class-components` - Fix React 19 class component this binding
- `gotchas-react19-ref-prop` - Handle React 19 ref prop changes
- `gotchas-websocket-optional-deps` - Handle WebSocket native dependency bundling
- `gotchas-auth-race-conditions` - Guard against auth/API race conditions
- `gotchas-auth-state-gating` - Wait for auth state before checking roles
- `gotchas-configuration-idempotency` - Ensure configuration idempotency with useRef
- `gotchas-hydration-nested-interactive` - Avoid nested interactive elements
- `gotchas-router-push-timing` - Never call router.push during render
- `gotchas-infinite-rerender` - Prevent infinite re-render loops
- `gotchas-provider-hierarchy` - Configure provider hierarchy correctly

## Pre-Migration Checklist

Before starting migration, scan the codebase for patterns that need special handling:

```bash
# Check for WebSocket libraries (needs webpack fallback config)
grep -E "(socket\.io|\"ws\")" package.json

# Check for SCSS :export syntax (may need --webpack flag)
grep -r ":export" --include="*.scss" src/

# Check for SVG ReactComponent imports (needs SVGR config)
grep -r "ReactComponent" --include="*.ts" --include="*.tsx" src/

# List all REACT_APP_ environment variables
grep -roh "REACT_APP_[A-Z_]*" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" src/ | sort -u

# Check for Redux extraReducers using object notation (must convert to builder pattern for RTK v2)
grep -r "extraReducers:" --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx" src/

# Check for /app/ paths that need updating if using (app) route group
grep -rE "(href|to|push|replace|redirect).*['\"]\/app\/" --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx" src/
```

**Scan Results to Rule Mapping:**

| Scan Result                     | Rules to Read                                          |
| ------------------------------- | ------------------------------------------------------ |
| socket.io or ws in package.json | `gotchas-websocket-optional-deps`, `setup-next-config` |
| `:export` in SCSS files         | `gotchas-turbopack`                                    |
| `ReactComponent` SVG imports    | `assets-static-imports`                                |
| `REACT_APP_` variables found    | `env-prefix-change`                                    |
| `extraReducers:` found          | `state-redux` (RTK v2 builder callback required)       |
| `/app/` paths in navigation     | `routing-route-groups` (update paths for route groups) |

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/setup-initial-structure.md
rules/routing-basic-pages.md
rules/data-useeffect-to-rsc.md
```

Each rule file contains:

- Brief explanation of the migration step
- CRA "before" code example
- Next.js "after" code example
- Additional context and gotchas

## Migration Order

For best results, migrate in this order:

1. **Setup** - Initialize Next.js project structure
2. **Routing** - Convert React Router to file-based routing
3. **Environment Variables** - Update env var prefixes
4. **Components** - Add 'use client' directives where needed
5. **Data Fetching** - Convert useEffect to server patterns
6. **Styling** - Move global CSS, configure CSS-in-JS
7. **Images & Fonts** - Adopt Next.js optimizations
8. **SEO** - Migrate to Metadata API
9. **API Routes** - Create Route Handlers
10. **Testing** - Update test configuration

## Post-Migration Verification Checklist

After migration, verify the application works correctly:

**Core Functionality:**

- [ ] `npm run dev` starts Next.js dev server without errors
- [ ] `npm run build` completes successfully
- [ ] `npm start` runs the production build
- [ ] Main application renders correctly
- [ ] All routes are accessible

**Client-Side Features:**

- [ ] localStorage/sessionStorage persistence works
- [ ] Dark mode or theme toggles work and persist
- [ ] Client-side interactivity (forms, buttons, modals) works
- [ ] Browser back/forward navigation works correctly

**Routing (if applicable):**

- [ ] Hash-based routing works (e.g., `#room=abc,key=xyz`)
- [ ] Query parameters are read correctly
- [ ] Dynamic routes render with correct params
- [ ] 404 pages show for invalid routes

**Real-Time Features (if applicable):**

- [ ] WebSocket connections establish successfully
- [ ] Real-time collaboration or updates work
- [ ] Reconnection after disconnect works

**Integrations (if applicable):**

- [ ] Error monitoring (Sentry) captures errors
- [ ] Analytics tracking fires correctly
- [ ] Third-party auth (OAuth, Firebase) works
- [ ] File uploads work

**PWA (if applicable):**

- [ ] Service worker registers (production build)
- [ ] App is installable
- [ ] Offline functionality works as expected

**Performance:**

- [ ] No hydration mismatch warnings in console
- [ ] Images load and are optimized
- [ ] Fonts load without FOUT/FOIT issues
- [ ] No unexpected console errors or warnings
