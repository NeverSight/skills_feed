---
name: achra-guidelines
description: Achra Platform guidelines, business rules, architecture, and engineering patterns. Use when writing or refactoring Achra code, adding modules or components, creating or updating skeleton loaders, loading placeholders, Suspense fallbacks, or Next.js loading.tsx, answering questions about Achra architecture or business domains, deciding when to use feature flags, applying Achra naming and placement conventions, or answering which technologies and libraries the project uses.
---

# Achra Guidelines

## Overview

Achra platform guidelines for architecture, conventions, business domains, and technical patterns. This skill covers where code lives, how to name and structure it, when to use feature flags, and how domains and routes map.

**WIP:** These guidelines are a draft. When a task is not covered here or in linked references, prefer consistency with existing Achra code and patterns.

## When to Apply

Reference these guidelines when:
- Writing new code in the Achra codebase (components, pages, services, hooks, providers, etc)
- Creating skeleton loaders, loading placeholders, Suspense fallbacks, or Next.js loading.tsx
- Refactoring or reviewing code for Achra consistency
- Adding a new module, feature, or route
- Answering questions about Achra architecture, business domains, or conventions
- Deciding where to place a component or whether to add a feature flag
- Answering questions about Achra's tech stack or choosing libraries/tools

## Quick Reference

| Topic | Rule | Details |
|-------|------|---------|
| **Module placement** | Shared vs domain, promotion rules | Used in 2+ modules or app root → check [Promotion rules](references/architecture.md#promotion-rules); single domain → `modules/{domain}/`. See [architecture.md](references/architecture.md). |
| **Naming** | kebab-case | Files and directories: `component-name.tsx`, `use-hook-name.ts`. See [conventions.md](references/conventions.md). |
| **Components** | Directory + index | One dir per component; **one component per file** (subcomponents in separate files). Helpers in **lib/utils**, not in component files. Named function, named export. See [conventions.md](references/conventions.md). |
| **Feature flags** | Shared, env-specific | `modules/shared/lib/feature-flags/`. Use for gating domains/sections (workstreams, finances, roadmaps). See [feature-flags-and-env.md](references/feature-flags-and-env.md). |
| **Data / GraphQL** | Domain graphql, generated | Queries in `modules/<domain>/graphql/*.graphql`; generated in `modules/__generated__/graphql/`. See [data-and-graphql.md](references/data-and-graphql.md). |
| **Types** | Props in file; reusable at module root | [conventions.md](references/conventions.md) |
| **Tech stack** | Next 16, React 19, TS, Tailwind 4, shadcn, GraphQL + TanStack Query | Framework, UI, data, forms, and tooling. See [tech-stack.md](references/tech-stack.md). |
| **Skeleton loading** | Mirror layout with Skeleton | Use `Skeleton` from `@/shared/components/ui/skeleton`; place `*-skeleton.tsx` next to source component. See [skeleton-loading.md](references/skeleton-loading.md). |
| **Server actions** | actions/, one per file, suffix action | In `modules/<module>/actions/`; file and function names end with `action`. See [architecture.md](references/architecture.md). |

## Skeleton loading

Skeleton loading is an Achra pattern for loading states. Use it for route loading (`loading.tsx`), Suspense fallbacks, or any placeholder that should match the final layout to avoid shift.

**Workflow:** Locate the target UI → create a sibling `{component-name}-skeleton.tsx` → mirror structure and replace content with `Skeleton` elements sized to match → remove interactivity and data logic → validate layout parity and contrast.

**Quick checklist:**
- Mirror layout containers and responsive classes (`sm:`, `md:`, etc.).
- Replace text with `Skeleton` using line-height-derived heights; for multi-line with `gap-1`, subtract 2px per line to prevent layout shift.
- Remove buttons, links, state, effects, and data fetching.
- Use `bg-border` on skeletons inside `bg-accent`, `bg-muted`, or `bg-secondary`.
- Reuse existing skeleton subcomponents when available.

**Required import:** `import { Skeleton } from '@/shared/components/ui/skeleton'`

Full rules, sizing, contrast, and accessibility: [skeleton-loading.md](references/skeleton-loading.md). Patterns and examples: [skeleton-loading-examples.md](references/skeleton-loading-examples.md).

## References

Full documentation:

- [achra-overview.md](references/achra-overview.md) — Business and product context; main domains and where they live
- [architecture.md](references/architecture.md) — Module layout, shared vs domain, promotion rules, placement decision tree, imports
- [conventions.md](references/conventions.md) — Naming, component directories, exports
- [feature-flags-and-env.md](references/feature-flags-and-env.md) — When and where to use feature flags; env behavior
- [data-and-graphql.md](references/data-and-graphql.md) — GraphQL and services location; generated code
- [tech-stack.md](references/tech-stack.md) — Framework, UI, data, forms, and tooling used in the project
- [skeleton-loading.md](references/skeleton-loading.md) — Skeleton loaders: layout mirroring, sizing, contrast, cleanup, validation
- [skeleton-loading-examples.md](references/skeleton-loading-examples.md) — Skeleton patterns and code examples
- [achra-guidelines.md](references/achra-guidelines.md) — Human-facing index with table of contents and links
- [rules/](references/rules/) — Granular rules (arch-, conv-, ff-, data-)
