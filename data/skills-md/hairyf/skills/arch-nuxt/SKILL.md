---
name: arch-nuxt
description: Vitesse-style Nuxt 4 starter with Vite, UnoCSS, Pinia, VueUse, PWA. Use when scaffolding or maintaining a Nuxt app with this stack.
metadata:
  author: hairy
  version: "2026.1.30"
  source: Generated from https://github.com/antfu/vitesse-nuxt, scripts located at https://github.com/antfu/skills
---

arch-nuxt is the **Vitesse-style starter for Nuxt 4**: SSR, file-based routing, auto-imports, and an opinionated stack (Vite, UnoCSS, Pinia, VueUse, ColorMode, VitePWA). It provides a minimal, production-ready setup: `app/` structure, layouts, composables, Pinia store with HMR, server API, PWA config, and UnoCSS. Prefer Vite-powered Nuxt; do not consider webpack or other bundlers.

> The skill is based on vitesse-nuxt (arch-nuxt source), generated at 2026-01-30.

**Recommended practices:**
- Prefer Vite-powered Nuxt; skip webpack and other bundlers
- Use Pinia for global/client state; use `useState` for SSR-shared state when appropriate
- Keep PWA config in `app/config/pwa.ts` and spread it in `nuxt.config.ts`

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Overview | Project purpose, structure, stack, when to use | [core-overview](references/core-overview.md) |
| Nuxt config | defineNuxtConfig, modules, app head, nitro, experimental | [core-nuxt-config](references/core-nuxt-config.md) |
| App structure | app/, app.vue, NuxtLayout, NuxtPage | [core-app-structure](references/core-app-structure.md) |
| Scripts | build, dev, generate, preview, typecheck, dev:pwa | [core-scripts](references/core-scripts.md) |
| Constants | app/constants, appName, appDescription | [core-constants](references/core-constants.md) |
| ESLint | @antfu/eslint-config, Nuxt append | [core-eslint](references/core-eslint.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Layouts | Layout system, definePageMeta layout | [features-layouts](references/features-layouts.md) |
| Composables | useCount, useState, auto-import | [features-composables](references/features-composables.md) |
| Pinia state | useUserStore, defineStore, HMR | [features-pinia-state](references/features-pinia-state.md) |
| Server API | defineEventHandler, server/api | [features-server-api](references/features-server-api.md) |
| PWA | VitePWA config, manifest, workbox, dev PWA | [features-pwa](references/features-pwa.md) |
| UnoCSS | uno.config.ts, shortcuts, presets, icons | [features-unocss](references/features-unocss.md) |
| ColorMode | useColorMode, DarkToggle, theme-color meta | [features-color-mode](references/features-color-mode.md) |
| Components | Auto-import, Counter, Footer, NuxtLink | [features-components](references/features-components.md) |
| Client-only | ClientOnly, Suspense, useOnline, fallback | [features-client-only](references/features-client-only.md) |
| Data fetching | useFetch, useTimeAgo, async component data | [features-data-fetching](references/features-data-fetching.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Routing | File-based routing, dynamic/catch-all routes | [best-practices-routing](references/best-practices-routing.md) |
| Page meta | definePageMeta, layout selection | [best-practices-page-meta](references/best-practices-page-meta.md) |
