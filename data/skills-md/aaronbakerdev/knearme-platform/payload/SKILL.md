---
name: payload
description: Expert guidance for building with Payload CMS - collections, fields, hooks, access control, Local API, authentication, uploads, and admin theming
---

# Payload CMS Skill

> Comprehensive reference for Payload CMS development including data modeling, API usage, and admin customization.

## Overview

Payload is a headless CMS and application framework built on Next.js. This skill covers collections, fields, hooks, access control, Local API operations, authentication, uploads, globals, plugins, and admin panel styling.

## Quick Reference: Which File Do I Need?

| Task | Reference File |
|------|----------------|
| Create/configure a collection | `collections.md` |
| Add fields to a collection | `fields.md` |
| Run code before/after operations | `hooks.md` |
| Control who can read/write data | `access-control.md` |
| Query or mutate data server-side | `local-api.md` |
| Use REST API externally | `rest-api.md` |
| Use GraphQL API | `graphql.md` |
| Set up user login/auth | `authentication.md` |
| Handle file/image uploads | `uploads.md` |
| Organize uploads in folders | `folders.md` |
| Create site-wide settings | `globals.md` |
| Add official plugins (SEO, forms) | `plugins.md` |
| Theme the admin panel | `admin-styling.md` |
| Build custom admin components | `custom-components.md` |
| Configure rich text editor | `rich-text.md` |
| Set up live preview | `live-preview.md` |
| Enable drafts/versions | `versions.md` |
| Configure database/migrations | `database.md` |
| Customize payload.config.ts | `configuration.md` |
| Set up email/notifications | `email.md` |
| Background jobs/scheduling | `jobs-queue.md` |
| Saved list view filters | `query-presets.md` |
| Soft delete/trash | `trash.md` |
| TypeScript type generation | `typescript.md` |
| Deploy to production | `production.md` |

## Reference Files Summary

### Core Data & API
| File | Lines | Description |
|------|-------|-------------|
| `collections.md` | ~200 | Collection config, slugs, admin options |
| `fields.md` | ~220 | All field types, validation, conditional logic |
| `globals.md` | ~50 | Single-document data (settings, nav) |
| `hooks.md` | ~170 | Lifecycle hooks for collections, fields, globals |
| `access-control.md` | ~200 | Permissions, RBAC, query constraints |
| `local-api.md` | ~190 | Server-side find, create, update, delete |
| `rest-api.md` | ~240 | REST endpoints, query params, auth headers |
| `graphql.md` | ~245 | GraphQL queries, mutations, schema |

### Authentication & Users
| File | Lines | Description |
|------|-------|-------------|
| `authentication.md` | ~200 | Auth config, strategies, password reset |
| `email.md` | ~180 | Email adapters (Nodemailer, Resend), templates |

### Content & Media
| File | Lines | Description |
|------|-------|-------------|
| `uploads.md` | ~60 | Media uploads, image sizes, storage adapters |
| `folders.md` | ~120 | Organize uploads in folder hierarchies |
| `rich-text.md` | ~270 | Lexical editor, features, serialization |
| `versions.md` | ~265 | Drafts, publishing, autosave, version history |
| `trash.md` | ~115 | Soft delete, restore, permanent delete |

### Admin Panel
| File | Lines | Description |
|------|-------|-------------|
| `admin-styling.md` | ~180 | CSS variables, BEM classes, theming |
| `custom-components.md` | ~300 | Field/Cell/View components, React hooks |
| `live-preview.md` | ~215 | Real-time content preview in admin |
| `query-presets.md` | ~125 | Saved filters for list views |

### Configuration & Infrastructure
| File | Lines | Description |
|------|-------|-------------|
| `configuration.md` | ~240 | payload.config.ts structure, all options |
| `database.md` | ~200 | MongoDB/Postgres adapters, migrations |
| `plugins.md` | ~60 | Official plugins and installation |
| `typescript.md` | ~220 | Type generation, payload-types.ts |
| `jobs-queue.md` | ~215 | Background tasks, workers, scheduling |
| `production.md` | ~190 | Deployment (Vercel, Docker), env vars |

## Common Workflows

### Creating a New Collection

1. Read `collections.md` for config structure
2. Read `fields.md` to add your data fields
3. Read `access-control.md` to set permissions
4. Optionally read `hooks.md` for lifecycle logic

### Building a Custom API Endpoint

1. Read `local-api.md` for query syntax
2. Read `authentication.md` if auth context needed
3. Read `access-control.md` to understand permissions

### Enabling File Uploads

1. Read `uploads.md` for upload config
2. Read `fields.md` for upload/relationship field linking
3. Read `plugins.md` if using cloud storage (S3, etc.)

### Theming the Admin Panel

1. Read `admin-styling.md` for CSS variables and classes
2. Focus on elevation variables for dark/light mode
3. Use `@layer payload` for overrides

## Quick Lookup Patterns

```bash
# Find hook types
grep -n "beforeChange\|afterChange" references/hooks.md

# Find field types
grep -n "type:" references/fields.md

# Find access control patterns
grep -n "role\|RBAC" references/access-control.md

# Find query operators
grep -n "equals\|contains\|greater" references/local-api.md

# Find CSS variables
grep -n "elevation\|gutter" references/admin-styling.md
```

## Key Patterns

### Getting Payload Instance (Server-Side)

```typescript
import { getPayload } from 'payload'
import config from '@payload-config'

const payload = await getPayload({ config })
```

### Basic Query

```typescript
const posts = await payload.find({
  collection: 'posts',
  where: { status: { equals: 'published' } },
  limit: 10,
})
```

### Access Control Function

```typescript
access: {
  read: () => true, // Public
  create: ({ req }) => !!req.user, // Authenticated
  update: ({ req, id }) => req.user?.id === id, // Owner only
}
```

## Official Documentation

- [Payload Docs](https://payloadcms.com/docs)
- [Collections](https://payloadcms.com/docs/configuration/collections)
- [Fields](https://payloadcms.com/docs/fields/overview)
- [Hooks](https://payloadcms.com/docs/hooks/overview)
- [Access Control](https://payloadcms.com/docs/access-control/overview)
- [Local API](https://payloadcms.com/docs/local-api/overview)
- [Authentication](https://payloadcms.com/docs/authentication/overview)
- [Uploads](https://payloadcms.com/docs/upload/overview)
- [Globals](https://payloadcms.com/docs/configuration/globals)
- [Plugins](https://payloadcms.com/docs/plugins/overview)
- [Customizing CSS](https://payloadcms.com/docs/admin/customizing-css)
