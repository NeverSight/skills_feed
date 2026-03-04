---
name: gremlin
displayName: Gremlin Course Platform
description: Work on gremlin — the Convex-powered next-gen course platform. Use when any task mentions gremlin, gremlincms, wizardshit, course platform, badass-courses, or working on the gremlin monorepo. Loads project context, points to config files, ADRs, and related skills.
version: 0.1.0
author: joel
tags:
  - gremlin
  - course-platform
  - convex
  - tanstack
  - nextjs
---

# Gremlin — Course Platform

Gremlin is the next-gen course platform built on Convex, with a provider/adapter pattern supporting multiple frameworks. Namespace: `@gremlincms`.

Accounting and payouts are being developed in `skillrecordings/payout` as a reusable financial core that is a piece of Gremlin’s future platform architecture.

## When to Use

Triggers: `gremlin`, `gremlincms`, `wizardshit`, `course platform`, `badass-courses`, `work on gremlin`, `gremlin repo`, or any task involving the gremlin monorepo.

## Key Paths

| What | Path |
|------|------|
| **Repo root** | `/Users/joel/Code/badass-courses/gremlin` |
| **AGENTS.md** | `/Users/joel/Code/badass-courses/gremlin/AGENTS.md` |
| **ADRs** | `/Users/joel/Code/badass-courses/gremlin/docs/adr/` |
| **ADR index** | `/Users/joel/Code/badass-courses/gremlin/docs/adr/README.md` |
| **GitHub** | `github.com/badass-courses/gremlin` |

### Apps

| App | Path | Framework | Domain |
|-----|------|-----------|--------|
| **wizardshit-ai** | `apps/wizardshit-ai` | Next.js 16 | wizardshit.ai |
| **gremlin-cms** | `apps/gremlin-cms` | TanStack Start | gremlincms.com |

### Packages

| Package | Path | Purpose |
|---------|------|---------|
| `@gremlincms/core` | `packages/core` | Router, schemas, types |
| `@gremlincms/db` | `packages/db` | ContentResourceAdapter interface |

### Planned packages (from ADRs, not yet created)

- `@gremlincms/convex-adapter` → `packages/convex-adapter/`
- `@gremlincms/drizzle-adapter` → `packages/drizzle-adapter/`
- `@gremlincms/next` → `packages/next/`
- `@gremlincms/tanstack` → `packages/tanstack/`

## Architecture Decisions

Read these before making structural changes:

- **ADR-010**: Convex-first provider/adapter pattern — Convex is primary DB, adapters are separate packages
- **ADR-011**: Multi-framework frontend support — Next.js + TanStack Start priority, framework-agnostic core
- **ADR-012**: Reference site architecture — wizardshit-ai (Next.js 16) + gremlin-cms (TanStack Start)

Legacy ADRs (001–009) cover auth, router, content model, tooling, monorepo structure, testing, CI/CD.

## Vercel Deploys

Both sites deploy via **git push** to `main` on `badass-courses/gremlin`. No CLI deploys needed.

- Vercel org: `skillrecordings` (team `team_QwoK7Pe6T0HIuFjig2Pm4qH8`)
- wizardshit-ai: root dir `apps/wizardshit-ai`
- gremlin-cms: root dir `apps/gremlin-cms`

## Related Skills

Load these when working on specific areas:

- **tanstack-start**: TanStack Start patterns, server functions, deployment quirks
- **next-best-practices**: Next.js App Router conventions
- **nextjs-static-shells**: Static-first rendering with dynamic slots
- **next-cache-components**: `'use cache'`, `cacheLife`, `cacheTag`
- **convex**: Convex development patterns (umbrella)
- **convex-schema-validator**: Schema design with Convex
- **favicon**: Emoji favicon generation with emojico
- **frontend-design**: UI/design quality standards
- **skillrecordings-payout**: financial core + payout rules used as Gremlin/platform accounting substrate

## SEO Standards

All gremlin sites follow these SEO practices:
- **Static-first content** — no client-side data fetching for content
- **Full JSON-LD** — `WebSite` schema at minimum, `Course`/`Organization` per page type
- **Dynamic OG images** — `/og` (Next.js) or `/og-image` (TanStack Start) endpoints
- **Canonical URLs**, robots directives, Twitter cards, Open Graph tags
- **Semantic HTML** — proper heading hierarchy, lang attribute, structured content

## Rules

1. **Always read `AGENTS.md`** at `/Users/joel/Code/badass-courses/gremlin/AGENTS.md` before making changes — it has project-specific constraints.
2. **Use pnpm** — never edit `package.json` by hand for deps. Use `pnpm add`.
3. **Namespace is `@gremlincms`** — not `@badass` (legacy packages still use `@badass`, rename deferred).
4. **Adapter packages are separate** — never co-locate Convex and Drizzle adapters.
5. **Check ADRs before structural changes** — if there's no ADR, write one first.
6. **No CLI deploys** — push to git, let Vercel auto-deploy.
7. **TanStack Start needs `nitro()` plugin** — without it, Vercel deploys 404. Already configured in `vite.config.ts`.

## Quick Start

```bash
cd /Users/joel/Code/badass-courses/gremlin

# Install deps
pnpm install

# Dev (both apps)
pnpm dev

# Dev (single app)
pnpm --filter @wizardshit/web dev
pnpm --filter @gremlin/gremlin-cms dev

# Test
pnpm test

# Build
pnpm build
```
