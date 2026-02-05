---
name: shadcn-ui
description: Use when building React UIs with component libraries, implementing forms, dialogs, navigation, or data display. Use when user mentions shadcn, Radix UI, Base UI, or asks about accessible React components. Proactively suggest when building UI that would benefit from pre-built accessible components with Tailwind CSS styling.
---

# ShadCN/UI Expert Skill

## Overview

ShadCN/UI is a collection of beautifully-designed, accessible components built with TypeScript, Tailwind CSS, and headless UI primitives (Base UI or Radix UI). Unlike traditional component libraries, ShadCN uses a **copy-paste model** - components are copied into YOUR project, giving you full ownership and customization control.

**Core Principle:** You own the code. Components live in your project (typically `src/components/ui/`), not in node_modules. This fundamentally changes how you think about customization - edit the source directly.

## When to Use

### Choose ShadCN When:
- Building React apps needing accessible, polished components
- You want full control over component code (not locked to library updates)
- Using Tailwind CSS for styling
- Need consistent design system with customization flexibility
- Building forms with validation (React Hook Form + Zod integration)

### Base Library Selection

During project creation (`shadcn create`), choose your base primitives:

| Base Library | Choose When |
|--------------|-------------|
| **Base UI** | Prefer MUI ecosystem, need unstyled primitives with strong React patterns |
| **Radix UI** | Want extensive primitive catalog, strong accessibility defaults |

Example preset with Base UI:
```bash
pnpm dlx shadcn@latest create --preset "https://ui.shadcn.com/init?base=base&style=nova&baseColor=stone" --template vite
```

### Choose Alternatives When:
- **Not using Tailwind** - ShadCN is Tailwind-first
- **Want batteries-included** - Use Chakra UI, Mantine, or MUI
- **Vue/Svelte project** - Use shadcn-vue or shadcn-svelte ports
- **Need zero styling opinions** - Use Base UI or Radix primitives directly

## Component Selection

```
Need user input?
  → Form & Input category (Input, Select, Checkbox, Form)

Need to show/hide content?
  → Triggered by click/hover? → Overlays (Dialog, Popover, Tooltip, Sheet)
  → User-controlled toggle? → Layout (Accordion, Tabs, Collapsible)

Need to display data?
  → Single item → Card
  → Multiple items → Table or Data Table

Need feedback?
  → Temporary → Toast (Sonner)
  → Persistent → Alert
```

Refer to `llms.txt` in this skill directory for the full component index with documentation links.

## Core Patterns

### The "Own Your Code" Model

ShadCN copies components into YOUR project. This means:
- Full customization - edit the source directly
- No version lock-in - you control updates
- Tree-shaking friendly - only what you use
- You maintain the code - breaking changes are your responsibility

### Component Composition

ShadCN components are composable primitives, not monolithic widgets:

```tsx
// Anti-pattern: Expecting a single "FormInput" component
<FormInput label="Email" error={errors.email} />

// ShadCN pattern: Compose primitives
<FormField>
  <FormLabel>Email</FormLabel>
  <FormControl>
    <Input {...field} />
  </FormControl>
  <FormMessage />
</FormField>
```

### Form Pattern (React Hook Form + Zod)

```tsx
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"

const schema = z.object({
  email: z.string().email("Invalid email address"),
  name: z.string().min(2, "Name must be at least 2 characters"),
})

type FormData = z.infer<typeof schema>

function ContactForm() {
  const form = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: { email: "", name: "" },
  })

  const onSubmit = (data: FormData) => {
    console.log(data)
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl>
                <Input placeholder="John Doe" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input placeholder="john@example.com" {...field} />
              </FormControl>
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

### Dialog with Form Pattern

```tsx
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { useState } from "react"

function DialogWithForm() {
  const [open, setOpen] = useState(false)

  const handleSuccess = () => {
    setOpen(false) // Close dialog on successful submit
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>Open Form</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Contact Us</DialogTitle>
          <DialogDescription>
            Fill out the form below and we'll get back to you.
          </DialogDescription>
        </DialogHeader>
        <ContactForm onSuccess={handleSuccess} />
      </DialogContent>
    </Dialog>
  )
}
```

### Toast Notifications (Sonner)

```tsx
import { toast } from "sonner"
import { Button } from "@/components/ui/button"

function ToastExample() {
  return (
    <div className="space-x-2">
      <Button onClick={() => toast("Event created")}>
        Default
      </Button>
      <Button onClick={() => toast.success("Successfully saved!")}>
        Success
      </Button>
      <Button onClick={() => toast.error("Something went wrong")}>
        Error
      </Button>
      <Button
        onClick={() =>
          toast.promise(saveData(), {
            loading: "Saving...",
            success: "Data saved!",
            error: "Could not save",
          })
        }
      >
        With Promise
      </Button>
    </div>
  )
}
```

### Data Table Pattern

```tsx
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

interface User {
  id: string
  name: string
  email: string
  role: string
}

function UsersTable({ users }: { users: User[] }) {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Name</TableHead>
          <TableHead>Email</TableHead>
          <TableHead>Role</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {users.map((user) => (
          <TableRow key={user.id}>
            <TableCell className="font-medium">{user.name}</TableCell>
            <TableCell>{user.email}</TableCell>
            <TableCell>{user.role}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
```

For advanced sorting, filtering, and pagination, use `@tanstack/react-table` with the Data Table component. See: https://ui.shadcn.com/docs/components/data-table

### Command Palette Pattern (⌘K)

```tsx
import {
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command"
import { useEffect, useState } from "react"

function CommandPalette() {
  const [open, setOpen] = useState(false)

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault()
        setOpen((open) => !open)
      }
    }
    document.addEventListener("keydown", down)
    return () => document.removeEventListener("keydown", down)
  }, [])

  return (
    <CommandDialog open={open} onOpenChange={setOpen}>
      <CommandInput placeholder="Type a command or search..." />
      <CommandList>
        <CommandEmpty>No results found.</CommandEmpty>
        <CommandGroup heading="Actions">
          <CommandItem>New File</CommandItem>
          <CommandItem>New Folder</CommandItem>
          <CommandItem>Settings</CommandItem>
        </CommandGroup>
      </CommandList>
    </CommandDialog>
  )
}
```

### Dark Mode Toggle

```tsx
import { Moon, Sun } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useTheme } from "@/components/theme-provider"

function ModeToggle() {
  const { theme, setTheme } = useTheme()

  return (
    <Button
      variant="outline"
      size="icon"
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
    >
      <Sun className="h-4 w-4 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-4 w-4 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
      <span className="sr-only">Toggle theme</span>
    </Button>
  )
}
```

## MCP Server Integration

### Setup (Claude Code)

```bash
npx shadcn@latest mcp init --client claude
```

This creates `.mcp.json`:
```json
{
  "mcpServers": {
    "shadcn": {
      "command": "npx",
      "args": ["shadcn@latest", "mcp"]
    }
  }
}
```

### Other Clients

```bash
npx shadcn@latest mcp init --client cursor   # Cursor
npx shadcn@latest mcp init --client vscode   # VS Code
npx shadcn@latest mcp init --client codex    # Codex
```

### Available Tools

Once configured, MCP tools allow:
- **Browse components** - List all components in configured registries
- **Search components** - Find components by name or functionality
- **Install components** - Add components to the project

### Natural Language Usage

The MCP server understands requests like:
- "Show me all available form components"
- "Add button, dialog, and card to my project"
- "What components are available for data display?"

### Multiple Registries

Configure private/custom registries in `components.json`:
```json
{
  "registries": {
    "@company": "https://registry.company.com/{name}.json"
  }
}
```

### When to Use MCP vs llms.txt

| Need | Use |
|------|-----|
| Browse/install components | MCP tools |
| Understand component API | WebFetch to docs URL from llms.txt |
| Check what's available | MCP browse or llms.txt index |

## Common Mistakes

### Importing from node_modules

```tsx
// Wrong - ShadCN components live in YOUR project
import { Button } from "@shadcn/ui"

// Correct - import from your components directory
import { Button } from "@/components/ui/button"
```

### Over-customizing via props

```tsx
// Wrong - expecting MUI-style prop customization
<Button colorScheme="purple" size="xl" leftIcon={<Icon />}>

// Correct - use Tailwind classes + composition
<Button className="bg-purple-600 text-lg">
  <Icon className="mr-2 h-4 w-4" />
  Click me
</Button>
```

### Forgetting dependencies

Components may require peer dependencies. Common ones:
- Forms: `react-hook-form`, `@hookform/resolvers`, `zod`
- Data Table: `@tanstack/react-table`
- Date Picker: `date-fns`, `react-day-picker`
- Charts: `recharts`
- Toast: `sonner`

### Not initializing first

```bash
# Must run init before adding components
npx shadcn@latest init
npx shadcn@latest add button dialog card
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Components not styled | Ensure Tailwind config includes `./src/components/**/*.{ts,tsx}` in content paths |
| TypeScript errors | Run `npx shadcn@latest init` to generate proper tsconfig paths |
| Dark mode not working | Check `darkMode: "class"` in tailwind.config + wrap app in ThemeProvider |
| Path alias issues (@/) | Verify `baseUrl` and `paths` in tsconfig.json match components.json |
| Component not found | Run `npx shadcn@latest add <component-name>` to install it |

## Quick Reference

### Project Setup (Vite + React)

```bash
# Create new project with preset
pnpm dlx shadcn@latest create --template vite

# Or add to existing project
npx shadcn@latest init
```

### Adding Components

```bash
npx shadcn@latest add button        # Single component
npx shadcn@latest add button card   # Multiple components
npx shadcn@latest add --all         # All components
```

### File Structure

```
src/
  components/
    ui/           # ShadCN components live here
      button.tsx
      card.tsx
      dialog.tsx
      ...
  lib/
    utils.ts      # cn() utility for className merging
```

### The cn() Utility

```tsx
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// Usage - merge classes safely
<Button className={cn("mt-4", isActive && "bg-primary")}>
```

## Resources

- **Documentation:** https://ui.shadcn.com/docs
- **Component Index:** See `llms.txt` in this skill directory
- **Themes:** https://ui.shadcn.com/themes
- **Examples:** https://ui.shadcn.com/examples
- **Blocks (page templates):** https://ui.shadcn.com/blocks
