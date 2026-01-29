---
name: og-card
description: |
  Generate deterministic, template-based Open Graph cards with Satori.
  Use when: creating OG images for blog posts, product pages, changelogs,
  or comparison pages. Complements /og-hero-image (AI creative) with
  consistent, branded templates. Keywords: og image, open graph, satori,
  social card, meta image, twitter card.
argument-hint: "[template: blog, product, changelog] [title]"
---

# /og-card

## vs /og-hero-image
- /og-hero-image: AI creative via Gemini. Use for one-off hero art.
- /og-card: consistent templates via Satori. Use for branded systems.

## Templates
- blog: title + author + date + brand colors
- product: logo + tagline + screenshot
- changelog: version + highlights
- comparison: product vs competitor

## Process
1. Read `brand-profile.yaml` for colors/fonts when present.
2. Select a template and pass required fields.
3. Render via `skills/og-card/scripts/generate-card.ts`.
4. Emit a 1200x630 PNG.

## Prerequisites
`pnpm add @vercel/og satori sharp`

## Usage
`/og-card blog "Title" by Author`
`/og-card product for heartbeat`

## Output
`og-[template]-[slug].png` at 1200x630
