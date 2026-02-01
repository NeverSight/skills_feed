---
name: react-use-client-boundary
description:
  Guides proper usage of "use client" directive in React/Next.js. Use this skill
  when adding client components, troubleshooting Server Component errors, or
  deciding where to place the client boundary.
---

# React "use client" Directive & Client Boundaries

Understanding when to use (and when NOT to use) the "use client" directive in React Server Components architecture.

## Core Concept: The Boundary

`"use client"` marks a **boundary** between server and client components - not a label for individual components.

**Critical Rule:** Once inside a client boundary, ALL imported components are automatically client components. You should NOT add `"use client"` to child components that are already imported by a parent client component.

## Mental Model: The Fence

Think of `"use client"` as a **fence** or **gate**:

```
┌─────────────────────────────────────────────────────┐
│  SERVER TERRITORY                                   │
│  ┌─────────────┐                                    │
│  │ page.tsx    │  (Server Component - default)      │
│  │             │                                    │
│  │  <Header /> │───────────────────────┐            │
│  └─────────────┘                       │            │
│                                        ▼            │
│  ════════════════ "use client" FENCE ════════════   │
│                                        │            │
│  ┌─────────────────────────────────────┼──────────┐ │
│  │ CLIENT TERRITORY                    ▼          │ │
│  │  ┌─────────────┐    ┌─────────────┐            │ │
│  │  │ Header.tsx  │───▶│ NavMenu.tsx │            │ │
│  │  │"use client" │    │ (no directive│            │ │
│  │  │             │    │  needed!)    │            │ │
│  │  └─────────────┘    └─────────────┘            │ │
│  │                                                 │ │
│  │  You're already inside - no more fences needed │ │
│  └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

## When to Use "use client"

Add the directive when ALL of these are true:

1. **The component is imported by a Server Component** (directly or as a page entry)
2. **AND** the component needs client-side features:
   - React hooks (`useState`, `useEffect`, `useContext`, etc.)
   - Event handlers (`onClick`, `onChange`, `onSubmit`, etc.)
   - Browser APIs (`window`, `document`, `localStorage`, etc.)
   - Third-party libraries that use any of the above

## When NOT to Use "use client"

1. **Already inside a client boundary** - parent component has `"use client"`
2. **Component is pure presentation** - just renders props, no interactivity
3. **"Just to be safe"** - this creates confusion and unnecessary boundaries
4. **Every component that uses props** - props work fine in server components

## Common Mistake: Redundant Directives

```tsx
// ❌ WRONG: Unnecessary "use client" in child

// components/form.tsx
"use client"
import { Input } from "./input"
import { Button } from "./button"

export function Form() {
  const [value, setValue] = useState("")
  return (
    <form>
      <Input value={value} onChange={setValue} />
      <Button type="submit">Send</Button>
    </form>
  )
}

// components/input.tsx
"use client"  // ❌ WRONG - already a client component!
export function Input({ value, onChange }) {
  return <input value={value} onChange={e => onChange(e.target.value)} />
}

// components/button.tsx
"use client"  // ❌ WRONG - already a client component!
export function Button({ children, type }) {
  return <button type={type}>{children}</button>
}
```

## Correct Approach: Single Boundary

```tsx
// ✅ CORRECT: Only the entry point has "use client"

// components/form.tsx
"use client"
import { Input } from "./input"
import { Button } from "./button"

export function Form() {
  const [value, setValue] = useState("")
  return (
    <form>
      <Input value={value} onChange={setValue} />
      <Button type="submit">Send</Button>
    </form>
  )
}

// components/input.tsx
// ✅ No directive - imported by client component
export function Input({ value, onChange }) {
  return <input value={value} onChange={e => onChange(e.target.value)} />
}

// components/button.tsx
// ✅ No directive - imported by client component
export function Button({ children, type }) {
  return <button type={type}>{children}</button>
}
```

## Decision Flowchart

```
Is this component imported by a Server Component?
│
├─ NO ──▶ Is its parent/importer a Client Component?
│         │
│         ├─ YES ──▶ ❌ Don't add "use client" (already in boundary)
│         │
│         └─ NO ───▶ Check the import chain upward
│
└─ YES ─▶ Does this component need client features?
          │
          ├─ NO ──▶ ❌ Don't add "use client" (keep it server)
          │
          └─ YES ─▶ ✅ Add "use client" (create boundary here)
```

## Real-World Example: Page with Interactive Section

```tsx
// app/products/page.tsx (Server Component - no directive)
import { ProductList } from "@/components/product-list"
import { SearchFilters } from "@/components/search-filters"
import { getProducts } from "@/lib/api"

export default async function ProductsPage() {
  const products = await getProducts()  // Server-side data fetching
  
  return (
    <main>
      <h1>Products</h1>
      <SearchFilters />           {/* Client boundary starts here */}
      <ProductList data={products} />  {/* Server component */}
    </main>
  )
}

// components/search-filters.tsx
"use client"  // ✅ Boundary: imported by server, needs state
import { FilterDropdown } from "./filter-dropdown"
import { PriceSlider } from "./price-slider"

export function SearchFilters() {
  const [filters, setFilters] = useState({})
  
  return (
    <div>
      <FilterDropdown onSelect={...} />  {/* No directive needed */}
      <PriceSlider onChange={...} />      {/* No directive needed */}
    </div>
  )
}

// components/filter-dropdown.tsx
// ✅ No "use client" - already inside client boundary
export function FilterDropdown({ onSelect }) {
  return <select onChange={e => onSelect(e.target.value)}>...</select>
}

// components/price-slider.tsx
// ✅ No "use client" - already inside client boundary
export function PriceSlider({ onChange }) {
  return <input type="range" onChange={e => onChange(e.target.value)} />
}
```

## Edge Case: Shared Components

When a component is used by BOTH server and client components:

```tsx
// components/card.tsx
// No directive - works in both contexts if it's pure presentation
export function Card({ title, children }) {
  return (
    <div className="card">
      <h2>{title}</h2>
      {children}
    </div>
  )
}

// app/page.tsx (Server Component)
import { Card } from "@/components/card"
// Card renders as server component here

// components/modal.tsx
"use client"
import { Card } from "@/components/card"
// Card renders as client component here (inside boundary)
```

## Troubleshooting Common Errors

### Error: "useState only works in Client Components"

**Cause:** Using hooks in a component without `"use client"` that's imported by a server component.

**Fix:** Add `"use client"` to the component using the hook, OR move the hook usage to a parent client component.

### Error: "Event handlers cannot be passed to Client Components from Server Components"

**Cause:** Trying to pass a function from server to client component.

**Fix:** Move the event handler logic to the client component, or restructure the boundary.

### Error: "async/await is not yet supported in Client Components"

**Cause:** Using async component syntax inside a client boundary.

**Fix:** Keep data fetching in server components, pass data as props to client components.

## Best Practices Summary

| Do | Don't |
|---|---|
| Place `"use client"` at the highest necessary point | Sprinkle `"use client"` on every component |
| Keep the client boundary as small as possible | Make entire pages client components |
| Let child components inherit client context | Add redundant `"use client"` to children |
| Use server components for data fetching | Fetch data in client components when avoidable |

## References

- [React Docs: "use client"](https://react.dev/reference/rsc/use-client)
- [Next.js Discussion: Client Component Boundaries](https://github.com/vercel/next.js/discussions/46795)
