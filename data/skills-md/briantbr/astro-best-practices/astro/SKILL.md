---
name: astro
description: >
  Astro framework patterns for Islands Architecture, client directives (client:load, client:visible, client:idle, client:only, client:media), integrations (MDX, Tailwind, React/Vue/Svelte), View Transitions API, and deployment strategies.
  Use when building content-focused sites, implementing partial hydration with islands, setting up multi-framework projects, optimizing performance with zero-JS by default, or deploying static/SSR sites.
---

# Astro Framework

Astro 5.x framework for building fast, content-focused websites with Islands Architecture and zero JavaScript by default.

## Core Concepts

### Zero JavaScript by Default

Astro ships ZERO JavaScript unless you explicitly add a client directive.

```astro
<!-- Static HTML (no JS) -->
<Header />
<Footer />

<!-- Interactive island (JS loaded) -->
<Counter client:idle />
```

**Rule**: Only use client directives when components need hooks, state, or browser APIs.

### Client Directives Quick Reference

| Directive | When to Use | Behavior |
|-----------|-------------|----------|
| `client:load` | Critical interaction needed immediately | Hydrates on page load |
| `client:idle` | Non-critical interactivity | Hydrates when browser idle |
| `client:visible` | Below the fold content | Hydrates when scrolled into view |
| `client:media="(query)"` | Responsive components | Hydrates when media query matches |
| `client:only="framework"` | Breaks during SSR | Skips SSR, client-only render |

**Decision Tree**:
```
Needs immediate interaction?        → client:load
Non-critical interactivity?         → client:idle
Below the fold?                     → client:visible
Only on mobile/desktop?             → client:media="(query)"
Breaks during SSR?                  → client:only="framework"
No interactivity at all?            → No directive (static HTML)
```

### Islands Architecture

Static shell + interactive islands hydrate independently:

```astro
---
import Header from '../components/Header.astro';       // Static
import Counter from '../components/Counter.jsx';       // Interactive
import Newsletter from '../components/Newsletter.vue'; // Interactive
---
<html>
  <body>
    <Header />                          <!-- Static HTML -->
    <Counter client:visible />          <!-- JS when visible -->
    <Newsletter client:idle />          <!-- JS after page load -->
  </body>
</html>
```

### Multi-Framework Support

Mix React, Vue, Svelte in the same project:

```bash
npx astro add react
npx astro add vue
npx astro add svelte
```

```astro
---
import ReactForm from './Form.jsx';
import VueChart from './Chart.vue';
import SvelteCounter from './Counter.svelte';
---
<ReactForm client:idle />
<VueChart client:visible />
<SvelteCounter client:load />
```

## Quick Start

```bash
npm create astro@latest my-project
cd my-project
npx astro add tailwind
npx astro add react
npm run dev
```

## Project Structure

```
src/
├── components/       # .astro, .jsx, .vue, .svelte
├── layouts/          # Page layouts
├── pages/            # File-based routing
│   └── blog/[slug].astro
├── content/          # Content Collections (Markdown/MDX)
│   └── config.ts     # Schema definitions
└── styles/           # Global CSS
```

## Configuration

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import react from '@astrojs/react';

export default defineConfig({
  site: 'https://example.com',
  output: 'static',  // or 'server' or 'hybrid'
  integrations: [tailwind(), react()],
});
```

## Output Modes

| Mode | Use Case | Command |
|------|----------|---------|
| `static` | Blog, docs, marketing | Default |
| `server` | Auth, dynamic data | `npx astro add vercel` |
| `hybrid` | Mostly static + some SSR | Mix of both |

## View Transitions

Enable SPA-like navigation:

```astro
---
import { ViewTransitions } from 'astro:transitions';
---
<html>
  <head>
    <ViewTransitions />
  </head>
  <body><slot /></body>
</html>
```

## Content Collections

Type-safe CMS for Markdown/MDX:

```typescript
// src/content/config.ts
import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  schema: z.object({
    title: z.string(),
    publishDate: z.date(),
    tags: z.array(z.string()),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };
```

```astro
---
import { getCollection } from 'astro:content';
const posts = await getCollection('blog', ({ data }) => !data.draft);
---
```

## Commands

```bash
npm run dev              # Start dev server (localhost:4321)
npm run build            # Build for production
npm run preview          # Preview production build
npx astro check          # TypeScript checks
```

## References

- **Advanced patterns** (SSR, middleware, image optimization, API endpoints): See [references/advanced.md](references/advanced.md)
- **Real-world examples** (blog, forms, auth, i18n, SEO): See [references/examples.md](references/examples.md)

## External Resources

- Official Documentation: https://docs.astro.build
- Islands Architecture: https://docs.astro.build/en/concepts/islands/
- Client Directives: https://docs.astro.build/en/reference/directives-reference/#client-directives
- Content Collections: https://docs.astro.build/en/guides/content-collections/
- View Transitions: https://docs.astro.build/en/guides/view-transitions/
