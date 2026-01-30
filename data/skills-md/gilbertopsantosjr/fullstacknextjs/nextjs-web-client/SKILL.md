---
name: nextjs-web-client
description: Guide for building Next.js 15+ React 19+ frontend components with App Router, Shadcn UI, and React Hook Form. Use when creating UI components, pages, layouts, forms, data tables, or client-side interactivity in a Next.js application.
---

# Next.js Web Client Development

## Server vs Client Components

**Default to Server Components** unless you need:
- Event handlers (onClick, onChange)
- Browser APIs (window, localStorage)
- React hooks (useState, useEffect)

### Component Split Pattern

For components needing server data + client interactivity:

```
components/
├── AccountForm.tsx              # Re-exports server component
├── AccountForm-server.tsx       # Fetches data, passes to client
└── AccountForm-client.tsx       # 'use client', handles interactions
```

```typescript
// AccountForm-server.tsx
import { AccountFormClient } from './AccountForm-client'
export async function AccountForm() {
  const data = await fetchData()
  return <AccountFormClient data={data} />
}

// AccountForm-client.tsx
'use client'
export function AccountFormClient({ data }: Props) {
  const [state, setState] = useState(data)
  return <form>...</form>
}
```

## Shadcn UI

Install components via CLI:
```bash
npx shadcn@latest add button input form dialog table card
```

Components copy to `src/components/ui/` - customize directly.

## Forms with React Hook Form

```typescript
'use client'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { Form, FormField, FormItem, FormLabel, FormControl, FormMessage } from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'

export function CreateForm() {
  const form = useForm<FormInput>({
    resolver: zodResolver(FormSchema),
    defaultValues: { name: '' },
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl><Input {...field} /></FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Submit</Button>
      </form>
    </Form>
  )
}
```

## Dynamic Imports

Use for conditionally rendered components:

```typescript
import dynamic from 'next/dynamic'

const EditDialog = dynamic(() => import('./EditDialog'))
const SettingsTab = dynamic(() => import('./tabs/SettingsTab'))

// Only load when needed
{showEdit && <EditDialog />}
{tab === 'settings' && <SettingsTab />}
```

## Loading & Error States

```typescript
// loading.tsx (in route folder)
export default function Loading() {
  return <Skeleton className="h-[200px]" />
}

// error.tsx (in route folder)
'use client'
export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div>
      <p>Something went wrong</p>
      <Button onClick={reset}>Try again</Button>
    </div>
  )
}

// With Suspense
<Suspense fallback={<LoadingSkeleton />}>
  <AsyncComponent />
</Suspense>
```

## Data Tables

```typescript
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'

export function DataTable({ items }: { items: Item[] }) {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Name</TableHead>
          <TableHead>Status</TableHead>
          <TableHead className="w-[100px]">Actions</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {items.map((item) => (
          <TableRow key={item.id}>
            <TableCell>{item.name}</TableCell>
            <TableCell>{item.status}</TableCell>
            <TableCell><Button size="sm">Edit</Button></TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
```

## Naming Conventions

| Type | Case | Example |
|------|------|---------|
| Components | PascalCase | `AccountCard.tsx` |
| Hooks | use-kebab | `use-account-form.ts` |
| Pages | kebab-case dirs | `app/(dashboard)/accounts/page.tsx` |
| Route groups | (parentheses) | `(auth)`, `(dashboard)` |
