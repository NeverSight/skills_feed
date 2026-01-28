---
name: nextra-writer
description: Expert in creating clear, comprehensive technical documentation with Nextra (Next.js-based docs framework), MDX, and modern documentation patterns. Use for documentation sites that need Next.js integration.
version: 1.0.0
tags:
  - documentation
  - nextra
  - nextjs
  - mdx
  - technical-writing
  - api-docs
  - react
  - typescript
auto_activate: true
---

# Nextra Technical Writer

Expert technical writer for creating documentation using Nextra, the Next.js-based documentation framework.

**Why Nextra:** Next.js integration, fast builds, automatic routing, full-text search, dark mode, and MDX support out of the box.

## When This Activates

- Creating or updating Nextra documentation (.md, .mdx)
- Configuring Nextra settings (next.config.mjs, theme.config.tsx)
- Writing API documentation
- Organizing documentation structure and navigation
- Setting up documentation search and navigation

## Tech Stack

| Technology | Version |
|------------|---------|
| Nextra | 3.x |
| Next.js | 14.x / 15.x |
| React | 18.x / 19.x |
| TypeScript | 5.x |
| MDX | 3.x |

## Quick Start

```bash
# Create new Nextra docs
bun create next-app docs --example nextra-docs-template

# Or add to existing Next.js project
bun add nextra nextra-theme-docs
```

## Project Structure

```
docs/
├── pages/
│   ├── _meta.json          # Navigation config
│   ├── index.mdx           # Home page
│   ├── getting-started.mdx
│   └── api/
│       ├── _meta.json
│       └── endpoints.mdx
├── theme.config.tsx        # Theme configuration
├── next.config.mjs         # Next.js + Nextra config
└── package.json
```

## Navigation

Configure via `_meta.json`:

```json
{
  "index": "Introduction",
  "getting-started": "Getting Started",
  "---": {
    "type": "separator"
  },
  "api": "API Reference"
}
```

## Key Features

| Feature | Pattern |
|---------|---------|
| Callouts | `<Callout type="info">` |
| Tabs | `<Tabs items={['npm', 'yarn']}>` |
| Cards | `<Cards>` component |
| Steps | `<Steps>` component |
| File Tree | `<FileTree>` component |

## Documentation Hierarchy

1. Quick Start (5-10 min)
2. Core Concepts
3. Feature Documentation
4. Guides & Tutorials
5. API Reference
6. Advanced Topics

## Integration

| Skill | When to Use |
|-------|-------------|
| `docs` | General technical writing |
| `api-design-expert` | API documentation structure |
| `frontend-design` | Custom documentation UI |

---

**For detailed configuration, MDX patterns, and component examples:** `references/full-guide.md`
