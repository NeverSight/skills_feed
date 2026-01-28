---
name: vani-spa-app
description:
  Updates Vani SPA app UI in src/spa-app, especially the landing page/homepage and landing examples.
  Use when the user mentions Vani SPA app, src/spa-app, landing page/homepage, or landing examples.
---

# Vani SPA App

## When to Use

- The user asks to update the Vani SPA app under `src/spa-app`
- Requests mention the landing page/homepage or landing examples

## Quick Rules

- SPA app code lives in `src/spa-app`; entry points are `entry-client.ts`, `entry-server.ts`, and
  `root.html`
- UI components live in `src/spa-app/components`
- Import Vani runtime helpers from `@/vani` and `@/vani/html`
- Use `cn()` from `src/spa-app/components/utils` for composing class names
- Favor small composable sections (e.g. `HeroSection`, `FeaturesSection`)

## Workflow Checklist

Use this checklist in responses:

- [ ] Identify the target section/component in `src/spa-app/components`
- [ ] Apply UI/content changes using Vani component patterns (`component`, `h.*`)
- [ ] Keep class names composed with `cn()` and ensure Tailwind utility consistency
- [ ] If the change touches landing examples, update `landing-page-examples.ts`
- [ ] Update `src/spa-app/styles.css` only when global styles are needed
- [ ] Scan for related copy/links in the landing page and update as needed

## Component Pattern

Use Vani components and HTML helpers:

```ts
import { component } from '@/vani'
import * as h from '@/vani/html'
import { cn } from './utils'

export const ExampleSection = component(() => {
  return () =>
    h.section(
      { className: cn('bg-slate-950 py-16 text-white') },
      h.div({ className: cn('mx-auto max-w-6xl px-6') }, 'Content'),
    )
})
```

## Common Targets

- Landing page layout: `src/spa-app/components/landing-page.ts`
- Landing examples: `src/spa-app/components/landing-page-examples.ts`
- App entry: `src/spa-app/app.ts`

## Present Results to User

Return updates as a checklist and include file paths that changed.
