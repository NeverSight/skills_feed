---
name: shadcn-best-practices
description: Best practices for working with shadcn/ui components, imports, theming, and forms. Use when building UI with shadcn, adding components, configuring theming, or creating forms.
version: 1.0.0
---

# shadcn/ui Best Practices

This skill covers best practices for working with shadcn/ui — component imports, className utilities, form building, theming, and data tables.

## Use-When

This skill activates when:
- Agent works with shadcn/ui components
- Agent adds or imports shadcn components
- Agent builds forms with validation
- Agent configures theming or dark mode
- Agent creates data tables

## Core Rules

- ALWAYS import shadcn components from `@/components/ui/{component-name}`
- ALWAYS use the `cn()` utility for className merging
- ALWAYS use Zod + React Hook Form for form validation
- ALWAYS use CSS variables for theming (not hardcoded colors)
- ALWAYS use TanStack Table for data tables
- ALWAYS check components.json to identify the primitive library (Radix vs Base UI)
- ALWAYS use migration commands when upgrading between styles (`migrate radix`, `migrate rtl`)

## Common Agent Mistakes

- Using relative paths instead of alias paths
- Forgetting to import `cn()` utility
- Hardcoding colors instead of using CSS variables
- Building table logic manually instead of using TanStack Table
- Assuming all shadcn projects use Radix UI (Base UI is now available)
- Using Radix-specific imports in Base UI projects (or vice versa)

## Examples

### ✅ Correct

```tsx
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { cn } from "@/lib/utils"

function MyComponent({ className }) {
  return (
    <Button className={cn("base-class", className)}>
      <Input placeholder="Enter email" />
    </Button>
  )
}
```

### ❌ Wrong

```tsx
// Using relative paths
import { Button } from "../../components/ui/button"

// Hardcoding colors
<Button className="bg-blue-500 text-white" />

// Building table manually
data.map(item => <tr><td>{item.name}</td></tr>)

// Assuming Radix - wrong for Base UI projects
import * as DialogPrimitive from "@radix-ui/react-dialog"
```

### Identifying Primitive Library

```tsx
// Check components.json to determine which library the project uses
// Look for "style" field:
// - "base-*" styles use @base-ui/react
// - Other styles use @radix-ui/react-* or radix-ui

// Example: reading the config
// import fs from "fs"
// const config = JSON.parse(fs.readFileSync("components.json", "utf-8"))
// config.style === "base-vega" // true = Base UI, false = Radix

// The API is identical regardless of library
import { Dialog, DialogContent } from "@/components/ui/dialog"
// Works the same for both Radix and Base UI projects
```

## References

- [shadcn Components](https://ui.shadcn.com/docs/components)
- [shadcn Installation](https://ui.shadcn.com/docs/installation)
- [shadcn Theming](https://ui.shadcn.com/docs/theming)
- [shadcn CLI](https://ui.shadcn.com/docs/cli)
- [components.json Schema](https://ui.shadcn.com/schema.json)
- [TanStack Table](https://tanstack.com/table)
