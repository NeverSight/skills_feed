---
name: nextjs-tinacms
description: Build Next.js 16 + React 19 + TinaCMS sites with visual editing, blocks-based page builder, and complete SEO. Use this skill whenever the user mentions TinaCMS, Tina CMS, Next.js with a CMS, visual editing with Next.js, click-to-edit, content-managed Next.js site, blocks pattern page builder, or migrating to Next.js + TinaCMS. Also trigger for TinaCMS schema design, self-hosted TinaCMS, TinaCMS media configuration, or any TinaCMS troubleshooting. Covers Day 0-2 setup from scaffolding through production deployment on Vercel.
---

# Next.js 16 + React 19 + TinaCMS Skill

Two primary workflows:
1. **New Project**: Scaffold Next.js 16 + TinaCMS with blocks page builder, visual editing, complete SEO, Tailwind CSS 4, shadcn/ui
2. **Add CMS**: Integrate TinaCMS into an existing Next.js 15/16 project

## Why This Stack

- **Next.js 16** — Turbopack default, `"use cache"` directive, `proxy.ts` replaces middleware, async params required, React 19.2
- **TinaCMS 3.x** — Git-backed headless CMS, visual click-to-edit, GraphQL API from code-first schema, admin UI at `/admin`
- **React 19.2** — Server Components stable, Actions, `use()` hook, View Transitions, React Compiler (opt-in)
- **Tailwind CSS 4** — CSS-first config, `@import "tailwindcss"`, no `tailwind.config.js` needed
- **shadcn/ui** — Copy-paste components, works with Tailwind, not a versioned package

## Critical Knowledge

1. **Server-Client split is mandatory.** `useTina()` requires `"use client"`. Every editable page needs a Server Component (data fetcher) and a Client Component (visual editing wrapper). No global `TinaProvider` needed in TinaCMS v2+.
2. **Build order matters.** Always `"build": "tinacms build && next build"`. Running `next build` first → `Cannot find module '../tina/__generated__/client'`.
3. **Pin exact TinaCMS versions.** No caret ranges. UI assets partially served from CDN and drift from local CLI. Keep all `tinacms` and `@tinacms/*` synced via RenovateBot grouping.
4. **`tina/__generated__/` MUST be committed.** Files `_graphql.json`, `_lookup.json`, `_schema.json`, and `tina-lock.json` are needed for production builds.
5. **Async params in Next.js 16.** Every `page.tsx`, `layout.tsx`, `route.ts` must `await params` — sync access fully removed.
6. **`proxy.ts` replaces `middleware.ts` in Next.js 16.** Auth, redirects, and request manipulation move to `app/proxy.ts` running on Node.js runtime.
7. **Node.js ≥ 20.9.0 required.** Next.js 16 dropped Node 18.
8. **Field names: alphanumeric + underscores only.** Hyphens/spaces in schema field names cause build errors.
9. **pnpm required for TinaCMS ≥ 2.7.3.** npm/yarn may have module resolution issues.
10. **Dev command is `tinacms dev -c "next dev"`.** Never `next dev` alone — the local GraphQL server won't run.
11. **Self-hosted TinaCMS does NOT work in Edge Runtime** (Cloudflare Workers, Vercel Edge Functions). Marked wontfix.
12. **`useTina()` returns props.data unchanged in production** — zero overhead. Only subscribes to live updates in edit mode.

## Version Floors

Before scaffolding, look up current stable versions (`npm view <pkg> version`). Minimum floors:

| Package | Minimum | Why |
|---------|---------|-----|
| `next` | ≥ 16.0.10 | Security patches |
| `tinacms` | ≥ 3.3.x | Visual selector, current schema API |
| `@tinacms/cli` | ≥ 2.1.x | Current build toolchain |
| `react` / `react-dom` | ≥ 19.2.x | View Transitions, useEffectEvent |
| `tailwindcss` | ≥ 4.x | CSS-first config (v3.4.x also acceptable) |
| Node.js | ≥ 20.9.0 | Next.js 16 requirement |
| TypeScript | ≥ 5.1.0 | Required for Next.js 16 types |

## Workflow: New Project

Follow the **247-task checklist** in `references/day0-2-checklist.md` task-by-task. The sections below summarize the architecture — the checklist has the exhaustive implementation details.

### Step 1: Scaffold & Install

```bash
npx create-next-app@latest my-site --typescript --tailwind --app --src-dir --turbopack
cd my-site
npx @tinacms/cli@latest init
```

Verify: `tinacms dev` → confirm `/admin` loads at `http://localhost:3000/admin/index.html`.

### Step 2: Configure Package Management

Pin exact TinaCMS versions. Add `renovate.json` — see `references/day0-2-checklist.md § Stack Versions` for config.

### Step 3: Schema Design in `tina/config.ts`

Read `references/nextjs16-react19-tinacms-reference.md § Schema Design Patterns` for full examples. Use `templates/tina-config-starter.ts` as starting point.

**Required collections:**

| Collection | Type | Purpose |
|-----------|------|---------|
| `pages` | Folder + blocks | Dynamic pages with visual page builder |
| `posts` | Folder | Blog/articles with structured fields |
| `authors` | Folder | Referenced by posts |
| `global` | Single doc | Site-wide settings, SEO defaults, social links |
| `navigation` | Single doc | Editable nav structure |
| `footer` | Single doc | Footer content and link groups |
| `notFound` | Single doc | Customizable 404 page content |

**Singleton pattern:**
```typescript
ui: { global: true, allowedActions: { create: false, delete: false } }
```

**Blocks pattern:**
```typescript
{
  type: 'object', list: true, name: 'blocks', label: 'Page Sections',
  ui: { visualSelector: true },
  templates: [heroBlock, featuresBlock, contentBlock, ctaBlock, faqBlock],
}
```

Every block template needs: `ui.previewSrc`, `ui.defaultItem`, section style group (layout/background/height/textColor as enums mapped to Tailwind classes).

**Field quality — enforce on every field:**
- `isTitle: true` on title fields, `required: true` on mandatory fields
- `ui.validate` for character limits, format validation
- `ui.description` for editorial guidance
- `ui.itemProps` on **every** list field with meaningful labels
- `ui.component: 'textarea'` on multi-line strings, `'group'` for collapsible groups

**Reusable field groups** — extract as shared variables: `seoFields`, `ctaFields`, `linkFields`, `responsiveImageFields`, `sectionStyleFields`.

**Content hooks:**
```typescript
ui: {
  beforeSubmit: async ({ values }) => ({
    ...values,
    slug: values.title.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, ''),
    modifiedDate: new Date().toISOString(),
  }),
}
```

### Step 4: Server-Client Page Pattern

See `templates/page-server-client.tsx` for the complete pattern.

```typescript
// app/[...slug]/page.tsx — Server Component
import client from '@/tina/__generated__/client'
import PageClient from './client-page'

export default async function Page({ params }: { params: Promise<{ slug: string[] }> }) {
  const { slug } = await params
  const relativePath = `${slug.join('/')}.md`
  const { data, query, variables } = await client.queries.page({ relativePath })
  return <PageClient data={data} query={query} variables={variables} />
}

export async function generateStaticParams() {
  const pages = await client.queries.pageConnection()
  return pages.data.pageConnection.edges?.map((edge) => ({
    slug: edge?.node?._sys.breadcrumbs,
  })) ?? []
}
```

```typescript
// app/[...slug]/client-page.tsx — Client Component
'use client'
import { useTina, tinaField } from 'tinacms/dist/react'
import { Blocks } from '@/components/blocks'

export default function PageClient(props: { data: any; query: string; variables: any }) {
  const { data } = useTina(props)
  return (
    <main data-tina-field={tinaField(data.page, 'blocks')}>
      <Blocks blocks={data.page.blocks} />
    </main>
  )
}
```

### Step 5: Visual Editing & Draft Mode

**Draft Mode API route** (`app/api/preview/route.ts`):
```typescript
import { draftMode } from 'next/headers'
import { redirect } from 'next/navigation'

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const slug = searchParams.get('slug') || '/'
  ;(await draftMode()).enable()
  redirect(slug)
}
```

**Visual editing debug checklist** — if click-to-edit doesn't work:
1. Draft mode enabled? (`/api/preview`)
2. Component is `"use client"`?
3. `useTina()` called with correct `{ data, query, variables }` props?
4. `data-tina-field={tinaField(data.page, 'fieldName')}` on DOM elements (not wrapper components)?
5. Tina dev server running? (`tinacms dev`)
6. Types generated and current? (`tina/__generated__/`)

**`ui.router` on every content collection** for contextual editing preview:
```typescript
ui: { router: ({ document }) => `/blog/${document._sys.filename}` }
```

### Step 6: Complete SEO Implementation

Read `references/day0-2-checklist.md` — Day 1 tasks 1.16–1.98 for the exhaustive 80+ SEO field specs covering global settings singleton, per-page SEO object, article fields, JSON-LD schemas, OG tags, Twitter cards, discovery files.

**Key patterns:**

**SEO description waterfall:**
1. `metaDescription` (explicit) → 2. `excerpt` → 3. Auto-truncated content → 4. `siteDescription` (global)

**`generateMetadata()` in every page:**
```typescript
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params
  const { data } = await client.queries.page({ relativePath: `${slug}.md` })
  const seo = data.page.seo
  const global = await client.queries.global({ relativePath: 'settings.json' })
  return {
    title: seo?.metaTitle || data.page.title,
    description: resolveDescription(seo, data.page, global.data.global),
    openGraph: {
      images: resolveOgImage(seo, global.data.global),
      type: 'website',
      siteName: global.data.global.siteName,
    },
    robots: { index: !seo?.noIndex, follow: !seo?.noFollow },
    alternates: { canonical: seo?.canonical || `${global.data.global.siteUrl}/${slug}` },
  }
}
```

**JSON-LD** — on every page: `Organization`, `WebSite` (homepage), `WebPage`, `Article`/`BlogPosting` (posts), `BreadcrumbList`, `FAQPage` (FAQ blocks).

**Discovery files:**
- `app/sitemap.ts` — dynamic from all collections, respects `noIndex`/`draft`
- `app/robots.ts` — disallows `/admin`, `/api/preview`
- `app/feed.xml/route.ts` — RSS for blog

### Step 7: Caching Strategy

```typescript
async function getPage(slug: string) {
  'use cache'
  cacheLife({ stale: 300, revalidate: 60, expire: 3600 })
  const { data } = await client.queries.page({ relativePath: `${slug}.md` })
  return data
}
```

Draft mode bypasses all caches (confirmed after Next.js PR #77141). Next.js 15+ changed `fetch()` default to `no-store` — explicitly opt into caching.

### Step 8: Media Management

| Provider | Best For | Setup |
|----------|----------|-------|
| Repo-based (`tina: { mediaRoot, publicFolder }`) | Small sites, blogs | 2 lines in config |
| Cloudinary (`next-tinacms-cloudinary`) | Media-heavy | Package + API route + 3 env vars |
| S3/R2 (`next-tinacms-s3`) | Enterprise | Package + IAM + bucket config |

All providers integrate with `next/image` — add `images.remotePatterns` in `next.config.js`.

### Step 9: Build & Deploy

```json
{
  "scripts": {
    "dev": "tinacms dev -c \"next dev\"",
    "build": "tinacms build && next build",
    "start": "next start"
  }
}
```

**Vercel env vars for Tina Cloud:**
```
NEXT_PUBLIC_TINA_CLIENT_ID=<from app.tina.io>
TINA_TOKEN=<read-only token>
NEXT_PUBLIC_TINA_BRANCH=main
```

**Vercel env vars for self-hosted:**
```
TINA_PUBLIC_IS_LOCAL=false
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxx
NEXTAUTH_SECRET=<random-secret>
KV_REST_API_URL=https://xxx.kv.vercel-storage.com
KV_REST_API_TOKEN=xxx
```

## Workflow: Self-Hosted TinaCMS

Three pluggable components: **database adapter** (Vercel KV / MongoDB / custom), **git provider** (GitHub), **auth provider** (AuthJS/Clerk).

Read `references/nextjs16-react19-tinacms-reference.md § Self-Hosted TinaCMS` for `database.ts` configuration.

**Choose self-hosting** for: full control, cost sensitivity, open-source purity.
**Choose Tina Cloud** for: quick setup, non-technical teams, built-in editorial workflow ($29-599/mo).

## Common Gotchas

| Problem | Cause | Fix |
|---------|-------|-----|
| `Cannot find module '../tina/__generated__/client'` | Wrong build order | `tinacms build && next build` |
| `Schema Not Successfully Built` | Frontend imports in `tina/config.ts` | Keep imports minimal |
| `Field name contains invalid characters` | Hyphens/spaces | Alphanumeric + underscores only |
| `GetCollection failed: template name not provided` | Missing `_template` in frontmatter | Add when using `templates` array |
| Visual editing not working | Multiple causes | Run debug checklist (Step 5) |
| `Expected workUnitAsyncStorage` | Turbopack prerendering bug | `--webpack` fallback |
| List items show "Item 0" | Missing `ui.itemProps` | Add meaningful label function |
| Reference dropdown slow/503 | Large collections | Custom field with pagination |
| SCSS modules broken | TinaCMS esbuild issue | CSS modules or Tailwind |
| Mismatched package versions | Tina packages out of sync | Pin exact, RenovateBot grouping |
| Content stale after Git push | Database index not updated | Re-index from dashboard |
| iOS share sheet broken (iMessage, AirDrop) | `manifest.json` with `display: "standalone"` | Use `"display": "browser"` or omit manifest; `<meta name="theme-color">` handles tinting |

## Anti-Patterns

| Don't | Do Instead |
|-------|-----------|
| Single rich-text for page body | Blocks list with templates |
| Expose CSS values in schema | Enums mapped to Tailwind classes |
| Generic wrapper components | Purpose-built components accepting Tina types |
| `useTina` in Server Components | Client Component wrapper |
| Dependabot for Tina packages | RenovateBot with grouping |
| Inline media (base64) | External media provider |
| No block fallback | Default case in renderer |
| Hardcoded SEO | SEO object in schema with waterfall |
| Missing `ui.itemProps` on lists | Meaningful label functions |
| Sync `params` access | `await params` everywhere |
| Manifest `display: "standalone"` on non-PWA sites | `"display": "browser"` or omit; use `<meta name="theme-color">` for tinting |

## Reference Files

| File | Purpose |
|------|---------|
| `references/day0-2-checklist.md` | **247-task checklist** — follow task-by-task for complete setup |
| `references/nextjs16-react19-tinacms-reference.md` | Deep technical reference: schema patterns, field types, blocks, SEO, React 19, caching, self-hosting, custom components, deployment |
| `templates/tina-config-starter.ts` | Production `tina/config.ts` with reusable SEO fields, 5 block templates, 7 collections |
| `templates/page-server-client.tsx` | Complete server-client page pattern with metadata, static params, block renderer |
