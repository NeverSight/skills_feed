---
name: app-router
description: "Next.js App Router - Server components, layouts, routing patterns"
sasmp_version: "1.3.0"
bonded_agent: nextjs-expert
bond_type: PRIMARY_BOND
---

# App Router Skill

## Overview

Master Next.js 14+ App Router with server components, layouts, and modern routing patterns.

## Capabilities

- **Layouts**: Root layout, nested layouts, templates
- **Server Components**: Default server rendering
- **Client Components**: Interactive with 'use client'
- **Route Groups**: (folder) for organization
- **Parallel Routes**: @slot for simultaneous rendering
- **Intercepting Routes**: (.) notation patterns

## Examples

```tsx
// app/layout.tsx
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}

// app/dashboard/page.tsx
export default async function DashboardPage() {
  const data = await fetchData() // Server-side
  return <Dashboard data={data} />
}
```

## Best Practices

- Use server components by default
- Add 'use client' only when needed
- Leverage layouts for shared UI
- Use loading.tsx for suspense

