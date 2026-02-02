---
name: arch-nuxt-lite
description: Vitesse Lite — lightweight Vite + Vue 3 SPA with file-based routing, UnoCSS, VueUse, Vitest. Use when scaffolding or maintaining a simple Vue SPA with this stack.
metadata:
  author: hairy
  version: "2026.1.30"
  source: Generated from https://github.com/antfu-collective/vitesse-lite, scripts located at https://github.com/antfu/skills
---

arch-nuxt-lite (Vitesse Lite) is the **lightweight Vite + Vue 3 SPA** starter: file-based routing via unplugin-vue-router, components and composables auto-import, UnoCSS, VueUse, and Vitest. No SSR, i18n, layouts, SSG, PWA, or Markdown. Prefer it for simple client-only apps; use arch-nuxt or Nuxt for SSR.

> The skill is based on vitesse-lite (arch-nuxt-lite source), generated at 2026-01-30.

**Recommended practices:**
- Prefer Vite + unplugin-vue-router for file-based routing; keep routes in `src/pages`
- Use `~/` alias for `src/` in imports
- Use VueUse (useDark, useToggle, useCounter, etc.) and composables in `src/composables`; all auto-imported

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Overview | Project purpose, structure, stack, when to use | [core-overview](references/core-overview.md) |
| App structure | Entry, RouterView, path alias, App.vue | [core-app-structure](references/core-app-structure.md) |
| Vite config | defineConfig, plugins, alias, Vitest | [core-vite-config](references/core-vite-config.md) |
| Scripts | build, dev, lint, typecheck, preview, test | [core-scripts](references/core-scripts.md) |
| CI | GitHub Actions — build, test, lint, typecheck matrix | [core-ci](references/core-ci.md) |
| ESLint | @antfu/eslint-config, unocss, formatters, pnpm | [core-eslint](references/core-eslint.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Routing | unplugin-vue-router, file-based routes, useRoute/useRouter, typed params | [features-routing](references/features-routing.md) |
| Components | unplugin-vue-components, auto-import, UnoCSS icons | [features-components](references/features-components.md) |
| Composables | unplugin-auto-import, composables dir, dark mode (useDark, useToggle) | [features-composables](references/features-composables.md) |
| UnoCSS | uno.config.ts, shortcuts, presets, icons, web fonts | [features-unocss](references/features-unocss.md) |
| Testing | Vitest, jsdom, component tests with @vue/test-utils | [features-testing](references/features-testing.md) |
| Deploy | Netlify, netlify.toml, SPA redirect | [features-deploy](references/features-deploy.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Routing | File-based routing patterns, dynamic/catch-all routes | [best-practices-routing](references/best-practices-routing.md) |
