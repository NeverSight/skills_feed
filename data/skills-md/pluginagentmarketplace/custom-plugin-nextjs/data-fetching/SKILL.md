---
name: data-fetching
description: "Next.js data fetching - Server actions, caching, revalidation"
sasmp_version: "1.3.0"
bonded_agent: nextjs-expert
bond_type: PRIMARY_BOND
---

# Data Fetching Skill

## Overview

Modern data fetching in Next.js with server actions, caching strategies, and revalidation.

## Capabilities

- **Server Actions**: 'use server' for mutations
- **Caching**: Automatic request memoization
- **Revalidation**: Time-based and on-demand
- **Streaming**: Progressive rendering
- **Parallel Fetching**: Promise.all patterns

## Examples

```tsx
// Server Action
'use server'

export async function createPost(formData: FormData) {
  const title = formData.get('title')
  await db.posts.create({ title })
  revalidatePath('/posts')
}

// Data fetching with caching
async function getData() {
  const res = await fetch('https://api.example.com/data', {
    next: { revalidate: 3600 } // Revalidate every hour
  })
  return res.json()
}
```

## Caching Options

- `cache: 'force-cache'` - Default, cached
- `cache: 'no-store'` - No caching
- `next: { revalidate: N }` - Revalidate after N seconds

