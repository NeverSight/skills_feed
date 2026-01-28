---
name: micro-landing-builder
description: Scaffold, clone, and deploy config-driven NextJS landing pages that use a shared UI components package. Use this skill when creating single or multiple startup landing pages with email capture, analytics, and modern design. Supports batch creation from templates or CSV/JSON files, and automatic Vercel deployment with custom domains. Each landing is a standalone NextJS app driven by an app.json config file.
---

# Micro Landing Builder

Create config-driven NextJS landing pages for startups.

## Concept

Each landing page is a standalone NextJS app where:

- Content is defined in `app.json` config file
- UI comes from `@agenticindiedev/ui`
- Deploy independently to any domain via Vercel

## Prerequisites

You need a published landing UI components package. The skill expects:

- Package name (default: `@agenticindiedev/ui`)
- Components: Hero, Features, Pricing, FAQ, CTA, Testimonials, Stats, EmailCapture, Header, Footer

## Usage

```bash
# Show help
python3 ~/.claude/skills/micro-landing-builder/scripts/scaffold.py --help

# Create a new landing
python3 ~/.claude/skills/micro-landing-builder/scripts/scaffold.py \
  --slug mystartup \
  --name "My Startup" \
  --domain "mystartup.com" \
  --concept "AI-powered analytics"

# With custom UI package
python3 ~/.claude/skills/micro-landing-builder/scripts/scaffold.py \
  --slug mystartup \
  --name "My Startup" \
  --ui-package "@myorg/landing-kit"

# Allow outside current directory
python3 ~/.claude/skills/micro-landing-builder/scripts/scaffold.py \
  --root ~/www/landings \
  --slug mystartup \
  --allow-outside
```

## Generated Structure

```
mystartup/
├── app.json              # All content/config here
├── package.json          # Depends on UI package
├── next.config.ts
├── tailwind.config.ts
├── tsconfig.json
├── vercel.json           # Vercel deployment config
├── public/
│   └── (images go here)
└── app/
    ├── layout.tsx
    ├── page.tsx          # Renders sections from app.json
    └── globals.css
```

## app.json Config

The landing is entirely driven by `app.json`. See `references/config-schema.md` for full schema.

```json
{
  "name": "My Startup",
  "slug": "mystartup",
  "domain": "mystartup.com",
  "meta": {
    "title": "My Startup - Tagline",
    "description": "SEO description"
  },
  "theme": {
    "primary": "#6366f1",
    "accent": "#f59e0b"
  },
  "analytics": {
    "plausible": "mystartup.com"
  },
  "sections": [
    { "type": "hero", "headline": "...", "subheadline": "..." },
    { "type": "features", "items": [...] },
    { "type": "pricing", "plans": [...] },
    { "type": "faq", "items": [...] },
    { "type": "cta", "emailCapture": { "enabled": true } }
  ]
}
```

## Section Types

- `hero` - Main hero with headline, CTA buttons
- `stats` - Key metrics/numbers
- `features` - Feature grid with icons
- `pricing` - Pricing plans
- `testimonials` - Customer quotes
- `faq` - Accordion FAQ
- `cta` - Call to action with email capture

## Batch Creation

Create multiple landing pages from a template or CSV/JSON file:

```bash
# From CSV file
python3 ~/.claude/skills/micro-landing-builder/scripts/batch_create.py \
  --root ~/www/landings \
  --csv projects.csv \
  --allow-outside

# From JSON file
python3 ~/.claude/skills/micro-landing-builder/scripts/batch_create.py \
  --root ~/www/landings \
  --json projects.json \
  --allow-outside

# Clone from existing template
python3 ~/.claude/skills/micro-landing-builder/scripts/batch_create.py \
  --root ~/www/landings \
  --template ~/www/landings/template-landing \
  --json projects.json \
  --allow-outside
```

### CSV Format

```csv
slug,name,domain,concept
project1,Project One,project1.com,AI-powered analytics
project2,Project Two,project2.com,Cloud infrastructure
```

### JSON Format

```json
[
  {
    "slug": "project1",
    "name": "Project One",
    "domain": "project1.com",
    "concept": "AI-powered analytics"
  },
  {
    "slug": "project2",
    "name": "Project Two",
    "domain": "project2.com",
    "concept": "Cloud infrastructure"
  }
]
```

## Deployment

### Single Project

```bash
cd mystartup
vercel
```

### Batch Deployment with Domains

Deploy multiple projects to Vercel with custom domains:

```bash
# Deploy with domain mapping
python3 ~/.claude/skills/micro-landing-builder/scripts/deploy_vercel.py \
  ~/www/landings/project1 \
  ~/www/landings/project2 \
  --domains-json domains.json \
  --prod \
  --yes

# Single domain
python3 ~/.claude/skills/micro-landing-builder/scripts/deploy_vercel.py \
  ~/www/landings/project1 \
  --domain project1.com \
  --prod \
  --yes
```

### Domain Mapping JSON

```json
{
  "project1": "project1.com",
  "project2": "project2.com"
}
```

**Note:** Domains must be configured in your DNS before adding to Vercel. Vercel will provide DNS records to add.

## Workflow

### Single Landing Page

1. Run scaffold to create landing structure
2. Edit `app.json` with your content
3. Add images to `public/`
4. Deploy with `vercel` or use `deploy_vercel.py`

### Multiple Landing Pages

1. Create CSV/JSON file with project definitions
2. Run `batch_create.py` to generate all landing pages
3. Customize each `app.json` as needed
4. Run `deploy_vercel.py` to deploy all with domains

## Customization

To add custom sections or override components:

1. Add component to `app/components/`
2. Import in `app/page.tsx`
3. Add to section renderer

## References

- `references/config-schema.md` - Full JSON schema
- `references/sections-reference.md` - Section types and props
