---
name: joelclaw-web
displayName: Joelclaw Web
description: "Update and maintain joelclaw.com — the Next.js web app at apps/web/. Use when writing blog posts, editing pages, updating the network page, changing layout/header/footer, adding components, or fixing anything on the site. Hard content triggers: 'write article about X' (draft in Convex), 'publish article <slug>' (set draft=false + revalidate tags/paths). Also triggers on: 'update the site', 'write a post', 'fix the blog', 'joelclaw.com', 'update network page', 'add a page', 'change the header', or any task involving the public-facing web app."
version: 1.2.0
author: Joel Hooks
tags: [joelclaw, web, nextjs, content, site]
---

# joelclaw.com Web App

Next.js app at `apps/web/` in the joelclaw monorepo (`~/Code/joelhooks/joelclaw/`).
Deployed to Vercel on push to `main`. Dark theme, minimal, system-y aesthetic.

## OPSEC Rules

**Never expose real infrastructure details on public pages.**

- **Node/host names**: Use Stephen King universe aliases, never real tailnet hostnames
- **Ports**: Do not publish port numbers for any service
- **Usernames**: Strip `com.joel.` or similar prefixes from service identifiers
- **IPs/subnets**: Never show real IP addresses or CIDR ranges
- **Brands/models of network gear**: Generalize (e.g. "NAS" not "Synology DS1821+")
- **Tailscale**: OK to mention as the mesh VPN product, but no tailnet name or node IPs

Current King universe mapping (network page):
| Role | Alias | Source |
|------|-------|--------|
| Mac Mini (control plane) | Overlook | The Shining |
| NAS (archive) | Derry | IT |
| Laptop (dev machine) | Flagg | The Dark Tower |
| Linux server | Blaine | The Dark Tower |
| Router (exit node) | Todash | The Dark Tower |

## Content Model (Convex-first)

Canonical runtime content lives in Convex `contentResources`:
- `article:<slug>` (`type = article`)
- `adr:<slug>` (`type = adr`)
- `discovery:<slug>` (`type = discovery`)

Filesystem content under `apps/web/content/` is seed/backfill material, not runtime source.

Runtime read policy:
- `apps/web/lib/posts.ts` → Convex-first articles (`article:*`)
- `apps/web/lib/adrs.ts` → Convex-first ADRs (`adr:*`)
- `apps/web/lib/discoveries.ts` → Convex-first discoveries (`discovery:*`)
- Optional local escape hatches (non-production only):
  - `JOELCLAW_ALLOW_FILESYSTEM_POSTS_FALLBACK=1` (articles)
  - `JOELCLAW_ALLOW_FILESYSTEM_CONTENT_FALLBACK=1` (ADRs/discoveries)

Article fields still mirror MDX frontmatter shape:

```yaml
---
title: "Post Title"
type: "article" | "essay" | "note" | "tutorial"
date: "2026-02-19T11:00:00"        # ISO datetime, NOT just date
updated: "2026-02-19T14:30:00"     # optional, bumps sort position
description: "One-liner for cards and meta"
tags: ["tag1", "tag2"]
draft: true                         # optional, hides from prod
source: "https://..."               # optional, for video-notes
channel: "Channel Name"             # optional, for video-notes
duration: "00:42:02"                # optional, for video-notes
---
```

**Sorting**: Posts sort by `updated ?? date` descending. Use full ISO datetimes (not bare dates) for deterministic ordering. Setting `updated` bumps a post to the top without changing its original publish date.

**Slugs**: Derived from `fields.slug` in Convex (`resourceId = article:<slug>`).

## Hard Trigger Workflow

### `write article about X`

1. Generate slug from title/topic.
2. Upsert `contentResources` with `resourceId = article:<slug>`, `type = "article"`, full MDX body in `fields.content`, and `fields.draft = true`.
3. Set `fields.date` to current ISO timestamp.
4. Return slug + draft preview link (`/<slug>` if draft-visible in dev).

### `publish article <slug>`

1. Read `article:<slug>` from Convex.
2. Patch/upsert with `fields.draft = false` and `fields.updated = now`.
3. Revalidate all affected surfaces via `POST /api/revalidate` with:
   - tags: `post:<slug>`, `article:<slug>`, `articles`
   - paths: `/`, `/<slug>`, `/feed.xml`
4. Verify `/`, `/<slug>`, and `/feed.xml` include the published post.

## Media Embeds

**Always embed YouTube videos** in `/cool` discoveries and articles when they add context. Use the `<YouTube id="VIDEO_ID" />` MDX component (available in both `.mdx` articles and `.md` discoveries). Extract the video ID from the URL (`youtube.com/watch?v=VIDEO_ID`). Place embeds near the top of the relevant section, before the prose discussion.

## Writing Voice

Use the `joel-writing-style` skill for prose. Key traits: direct, first-person, strategic profanity, short paragraphs, bold emphasis, conversational but technical. Never corporate-speak.

## Design System

- **Theme**: Dark (`bg-[#0a0a0a]`), neutral grays, `--color-claw: #ff1493` (hot pink accent)
- **Fonts**: Geist Sans (body), Geist Mono (code/data), Dank Mono (code blocks with ligatures)
- **Content width**: `max-w-2xl` (672px) — intentionally narrow for reading
- **Header**: Single row — claw icon + "JoelClaw" left, nav links + search right. No tagline in header.
- **Nav items**: Writing (`/`), Cool (`/cool`), ADRs (`/adrs`), Network (`/network`)
- **Active nav**: White text vs neutral-500 for inactive, detected via `usePathname()`
- **Search**: ⌘K dialog using pagefind, type-based icons/badges
- **Mobile**: Full-screen overlay nav via `MobileNav` component
- **Code blocks**: Catppuccin Macchiato theme, rehype-pretty-code
- **Sidenotes**: Tufte-style CSS sidenotes (pure CSS, no JS)

## Key Files

| File | Purpose |
|------|---------|
| `app/layout.tsx` | Root layout, fonts, metadata, footer |
| `app/page.tsx` | Home page (post list) |
| `app/[slug]/page.tsx` | Post detail pages |
| `app/adrs/page.tsx` | ADR list |
| `app/adrs/[slug]/page.tsx` | ADR detail (strips H1 to avoid duplicate title) |
| `app/cool/page.tsx` | Cool/discoveries list |
| `app/network/page.tsx` | Infrastructure status page |
| `components/site-header.tsx` | Header with active nav (client component) |
| `components/mobile-nav.tsx` | Mobile overlay nav |
| `components/search-dialog.tsx` | ⌘K search |
| `lib/posts.ts` | Article loading from Convex (`article:*`) |
| `lib/adrs.ts` | ADR loading from Convex (`adr:*`) |
| `lib/discoveries.ts` | Discovery loading from Convex (`discovery:*`) |
| `lib/constants.ts` | Site name, URL, tagline |
| `lib/claw.ts` | SVG path for claw icon |

## ADR Display Rules

- ADR runtime source is Convex (`contentResources` with `resourceId = adr:<slug>`)
- Vault sync still updates repo snapshots under `apps/web/content/adrs/`
- Project snapshots into Convex with: `bun scripts/seed-adrs-discoveries.ts`
- The detail page (`app/adrs/[slug]/page.tsx`) strips the H1 from markdown content because the page already renders the title with ADR number prefix
- Regex: `content.replace(/^#\s+(?:ADR-\d+:\s*)?.*$/m, "").trim()`

## Adding a New Post

1. Draft in Convex (`contentResources.upsert`, `resourceId = article:<slug>`, `draft: true`).
2. Use ISO datetime in `date` field.
3. Add images to `apps/web/public/images/<slug>/` if needed and reference `/images/<slug>/...` in MDX.
4. Publish by setting `draft: false`, then revalidate tags + paths (`post:<slug>`, `article:<slug>`, `articles`, `/`, `/<slug>`, `/feed.xml`).
5. Verify route + homepage + feed consistency.

Backfill scripts:
- `scripts/seed-articles.ts` for article resources
- `scripts/seed-adrs-discoveries.ts` for ADR + discovery resources

## Network Page

The network page (`app/network/page.tsx`) shows real infrastructure with aliased names. When updating:

1. Check actual system state (`kubectl get pods`, `tailscale status`, `launchctl print`, etc.)
2. Apply OPSEC rules — alias all hostnames, strip ports/IPs/usernames
3. Keep data arrays at top of file for easy updates
4. Status dots: green (Online) with ping animation, yellow (Idle), gray (Offline)
