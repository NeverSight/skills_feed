---
name: next-loading-skeleton
description: When building Next.js App Router pages with data loading, slow fetches, or Suspense, generate loading.tsx using shadcn/ui Skeleton placeholders for instant loading UI. Always install shadcn skeleton component first if not present. Use for dashboards, lists, profiles, forms.
---

## When to Use

Trigger this skill when:
- Creating Next.js App Router pages with data fetching
- User mentions "loading", "skeleton", "placeholder", "Suspense"
- Building dashboards, tables, lists, or profile pages
- Pages with slow API calls or database queries
- Any layout that needs instant visual feedback

## Installation Reminder

**Always install shadcn/ui skeleton first:**
```bash
npx shadcn@latest add skeleton
```

Install additional components as needed:
```bash
npx shadcn@latest add card table avatar badge
```

## Standard Patterns

### Basic Structure
- Create `loading.tsx` in same folder as `page.tsx`
- Export default function `Loading()`
- Import `{ Skeleton }` from "@/components/ui/skeleton"
- Use `animate-pulse` on wrapper elements

### Common Skeleton Patterns
```tsx
// Text line
<Skeleton className="h-4 w-[250px] rounded-full" />

// Card
<Skeleton className="h-[125px] w-full rounded-lg" />

// Avatar
<Skeleton className="h-10 w-10 rounded-full" />

// Table row
<div className="flex gap-4">
  <Skeleton className="h-4 w-[100px]" />
  <Skeleton className="h-4 w-[200px]" />
  <Skeleton className="h-4 w-[150px]" />
</div>
```

## Generation via Script

For complex layouts, use the Python script to save tokens:

```bash
python scripts/generate-loading.py "dashboard with 4 stat cards and recent users table"
```

The script outputs a complete `loading.tsx` string that matches your description.

## Examples

### Simple Card List
```tsx
import { Skeleton } from "@/components/ui/skeleton"

export default function Loading() {
  return (
    <div className="space-y-4 animate-pulse">
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <Skeleton key={i} className="h-[125px] w-full rounded-lg" />
        ))}
      </div>
      <div className="space-y-2">
        {Array.from({ length: 3 }).map((_, i) => (
          <Skeleton key={i} className="h-20 w-full rounded-lg" />
        ))}
      </div>
    </div>
  )
}
```

### Profile Page
```tsx
import { Skeleton } from "@/components/ui/skeleton"

export default function Loading() {
  return (
    <div className="space-y-6 animate-pulse">
      <div className="flex items-center gap-4">
        <Skeleton className="h-20 w-20 rounded-full" />
        <div className="space-y-2">
          <Skeleton className="h-6 w-[200px]" />
          <Skeleton className="h-4 w-[150px]" />
        </div>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        <Skeleton className="h-[200px] w-full rounded-lg" />
        <Skeleton className="h-[200px] w-full rounded-lg" />
      </div>
    </div>
  )
}
```

### Table with Search
```tsx
import { Skeleton } from "@/components/ui/skeleton"

export default function Loading() {
  return (
    <div className="space-y-4 animate-pulse">
      <div className="flex gap-4">
        <Skeleton className="h-10 w-[300px]" />
        <Skeleton className="h-10 w-[100px]" />
      </div>
      <div className="space-y-2">
        {Array.from({ length: 8 }).map((_, i) => (
          <div key={i} className="flex gap-4">
            <Skeleton className="h-4 w-[100px]" />
            <Skeleton className="h-4 w-[200px]" />
            <Skeleton className="h-4 w-[150px]" />
            <Skeleton className="h-4 w-[100px]" />
          </div>
        ))}
      </div>
    </div>
  )
}
```

## Key Principles

1. **Match real layout** - Skeleton should mirror actual page structure
2. **Use animate-pulse** - Add to wrapper containers for smooth animation
3. **Vary skeleton sizes** - Different widths/heights for realistic feel
4. **Keep it simple** - Focus on main content areas, ignore minor details
