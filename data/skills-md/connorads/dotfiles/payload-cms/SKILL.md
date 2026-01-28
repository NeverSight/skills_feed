---
name: payload-cms
description: >
  Use when working with Payload CMS projects (payload.config.ts, collections, fields, hooks, access control, Payload API).
  Triggers on tasks involving: collection definitions, field configurations, hooks, access control, database queries,
  custom endpoints, authentication, file uploads, drafts/versions, live preview, or plugin development.
  Also use when debugging validation errors, security issues, relationship queries, transactions, or hook behavior.
author: payloadcms
version: 1.0.0
---

# Payload CMS Development

Payload is a Next.js native CMS with TypeScript-first architecture. This skill transfers expert knowledge for building collections, hooks, access control, and queries the right way.

## Mental Model

Think of Payload as **three interconnected layers**:

1. **Config Layer** → Collections, globals, fields define your schema
2. **Hook Layer** → Lifecycle events transform and validate data
3. **Access Layer** → Functions control who can do what

Every operation flows through: `Config → Access Check → Hook Chain → Database → Response Hooks`

## Quick Reference

| Task | Solution | Details |
|------|----------|---------|
| Auto-generate slugs | `slugField()` or beforeChange hook | [references/fields.md#slug-field] |
| Restrict by user | Access control with query constraint | [references/access-control.md] |
| Local API with auth | `user` + `overrideAccess: false` | [references/queries.md#local-api] |
| Draft/publish | `versions: { drafts: true }` | [references/collections.md#drafts] |
| Computed fields | `virtual: true` with afterRead hook | [references/fields.md#virtual] |
| Conditional fields | `admin.condition` | [references/fields.md#conditional] |
| Filter relationships | `filterOptions` on field | [references/fields.md#relationship] |
| Prevent hook loops | `req.context` flag | [references/hooks.md#context] |
| Transactions | Pass `req` to all operations | [references/hooks.md#transactions] |
| Background jobs | Jobs queue with tasks | [references/advanced.md#jobs] |

## Quick Start

```bash
npx create-payload-app@latest my-app
cd my-app
pnpm dev
```

### Minimal Config

```ts
import { buildConfig } from 'payload'
import { mongooseAdapter } from '@payloadcms/db-mongodb'
import { lexicalEditor } from '@payloadcms/richtext-lexical'

export default buildConfig({
  admin: { user: 'users' },
  collections: [Users, Media, Posts],
  editor: lexicalEditor(),
  secret: process.env.PAYLOAD_SECRET,
  typescript: { outputFile: 'payload-types.ts' },
  db: mongooseAdapter({ url: process.env.DATABASE_URL }),
})
```

## Core Patterns

### Collection Definition

```ts
import type { CollectionConfig } from 'payload'

export const Posts: CollectionConfig = {
  slug: 'posts',
  admin: {
    useAsTitle: 'title',
    defaultColumns: ['title', 'author', 'status', 'createdAt'],
  },
  fields: [
    { name: 'title', type: 'text', required: true },
    { name: 'slug', type: 'text', unique: true, index: true },
    { name: 'content', type: 'richText' },
    { name: 'author', type: 'relationship', relationTo: 'users' },
    { name: 'status', type: 'select', options: ['draft', 'published'], defaultValue: 'draft' },
  ],
  timestamps: true,
}
```

### Hook Pattern (Auto-slug)

```ts
export const Posts: CollectionConfig = {
  slug: 'posts',
  hooks: {
    beforeChange: [
      async ({ data, operation }) => {
        if (operation === 'create' && data.title) {
          data.slug = data.title.toLowerCase().replace(/\s+/g, '-')
        }
        return data
      },
    ],
  },
  fields: [{ name: 'title', type: 'text', required: true }],
}
```

### Access Control Pattern

```ts
import type { Access } from 'payload'

// Type-safe: admin-only access
export const adminOnly: Access = ({ req }) => {
  return req.user?.roles?.includes('admin') ?? false
}

// Row-level: users see only their own posts
export const ownPostsOnly: Access = ({ req }) => {
  if (!req.user) return false
  if (req.user.roles?.includes('admin')) return true
  return { author: { equals: req.user.id } }
}
```

### Query Pattern

```ts
// Local API with access control
const posts = await payload.find({
  collection: 'posts',
  where: {
    status: { equals: 'published' },
    'author.name': { contains: 'john' },
  },
  depth: 2,
  limit: 10,
  sort: '-createdAt',
  user: req.user,
  overrideAccess: false, // CRITICAL: enforce permissions
})
```

## Critical Security Rules

### 1. Local API Access Control

**Default behavior bypasses ALL access control.** This is the #1 security mistake.

```ts
// ❌ SECURITY BUG: Access control bypassed even with user
await payload.find({ collection: 'posts', user: someUser })

// ✅ SECURE: Explicitly enforce permissions
await payload.find({
  collection: 'posts',
  user: someUser,
  overrideAccess: false, // REQUIRED
})
```

**Rule:** Use `overrideAccess: false` for any operation acting on behalf of a user.

### 2. Transaction Integrity

**Operations without `req` run in separate transactions.**

```ts
// ❌ DATA CORRUPTION: Separate transaction
hooks: {
  afterChange: [async ({ doc, req }) => {
    await req.payload.create({
      collection: 'audit-log',
      data: { docId: doc.id },
      // Missing req - breaks atomicity!
    })
  }]
}

// ✅ ATOMIC: Same transaction
hooks: {
  afterChange: [async ({ doc, req }) => {
    await req.payload.create({
      collection: 'audit-log',
      data: { docId: doc.id },
      req, // Maintains transaction
    })
  }]
}
```

**Rule:** Always pass `req` to nested operations in hooks.

### 3. Infinite Hook Loops

**Hooks triggering themselves create infinite loops.**

```ts
// ❌ INFINITE LOOP
hooks: {
  afterChange: [async ({ doc, req }) => {
    await req.payload.update({
      collection: 'posts',
      id: doc.id,
      data: { views: doc.views + 1 },
      req,
    }) // Triggers afterChange again!
  }]
}

// ✅ SAFE: Context flag breaks the loop
hooks: {
  afterChange: [async ({ doc, req, context }) => {
    if (context.skipViewUpdate) return
    await req.payload.update({
      collection: 'posts',
      id: doc.id,
      data: { views: doc.views + 1 },
      req,
      context: { skipViewUpdate: true },
    })
  }]
}
```

## Project Structure

```
src/
├── app/
│   ├── (frontend)/page.tsx
│   └── (payload)/admin/[[...segments]]/page.tsx
├── collections/
│   ├── Posts.ts
│   ├── Media.ts
│   └── Users.ts
├── globals/Header.ts
├── hooks/slugify.ts
└── payload.config.ts
```

## Type Generation

Generate types after schema changes:

```ts
// payload.config.ts
export default buildConfig({
  typescript: { outputFile: 'payload-types.ts' },
})

// Usage
import type { Post, User } from '@/payload-types'
```

## Getting Payload Instance

```ts
// In API routes
import { getPayload } from 'payload'
import config from '@payload-config'

export async function GET() {
  const payload = await getPayload({ config })
  const posts = await payload.find({ collection: 'posts' })
  return Response.json(posts)
}

// In Server Components
export default async function Page() {
  const payload = await getPayload({ config })
  const { docs } = await payload.find({ collection: 'posts' })
  return <div>{docs.map(p => <h1 key={p.id}>{p.title}</h1>)}</div>
}
```

## Common Field Types

```ts
// Text
{ name: 'title', type: 'text', required: true }

// Relationship
{ name: 'author', type: 'relationship', relationTo: 'users' }

// Rich text
{ name: 'content', type: 'richText' }

// Select
{ name: 'status', type: 'select', options: ['draft', 'published'] }

// Upload
{ name: 'image', type: 'upload', relationTo: 'media' }

// Array
{
  name: 'tags',
  type: 'array',
  fields: [{ name: 'tag', type: 'text' }],
}

// Blocks (polymorphic content)
{
  name: 'layout',
  type: 'blocks',
  blocks: [HeroBlock, ContentBlock, CTABlock],
}
```

## Decision Framework

**When choosing between approaches:**

| Scenario | Approach |
|----------|----------|
| Data transformation before save | `beforeChange` hook |
| Data transformation after read | `afterRead` hook |
| Enforce business rules | Access control function |
| Complex validation | `validate` function on field |
| Computed display value | Virtual field with `afterRead` |
| Related docs list | `join` field type |
| Side effects (email, webhook) | `afterChange` hook with context guard |
| Database-level constraint | Field with `unique: true` or `index: true` |

## Quality Checks

Good Payload code:
- [ ] All Local API calls with user context use `overrideAccess: false`
- [ ] All hook operations pass `req` for transaction integrity
- [ ] Recursive hooks use `context` flags
- [ ] Types generated and imported from `payload-types.ts`
- [ ] Access control functions are typed with `Access` type
- [ ] Collections have meaningful `admin.useAsTitle` set

## Reference Documentation

For detailed patterns, see:
- **[references/fields.md](references/fields.md)** - All field types, validation, conditional logic
- **[references/collections.md](references/collections.md)** - Auth, uploads, drafts, live preview
- **[references/hooks.md](references/hooks.md)** - Hook lifecycle, context, patterns
- **[references/access-control.md](references/access-control.md)** - RBAC, row-level, field-level
- **[references/queries.md](references/queries.md)** - Operators, Local/REST/GraphQL APIs
- **[references/advanced.md](references/advanced.md)** - Jobs, plugins, localization

## Resources

- Docs: https://payloadcms.com/docs
- LLM Context: https://payloadcms.com/llms-full.txt
- GitHub: https://github.com/payloadcms/payload
- Templates: https://github.com/payloadcms/payload/tree/main/templates
