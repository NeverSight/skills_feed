---
name: shadcn-ui-expert
description: Develop high-quality, accessible React components using shadcn-ui, Tailwind CSS, and Radix UI. Use when building forms, layouts, dialogs, tables, or any UI components. Supports Next.js, Vite, Remix, Astro, and more. Integrates with shadcn MCP server for component discovery and installation.
allowed-tools: Read, Grep, Glob, Write, Shell
---

# shadcn-ui Expert

shadcn-ui is a collection of beautifully-designed, accessible React components built with TypeScript, Tailwind CSS, and Radix UI primitives. This skill guides you through component selection, implementation, customization, and best practices.

## Quick Start

### Installation

First, initialize shadcn-ui in your project:

```bash
npx shadcn-ui@latest init
```

This creates a `components.json` file for configuration. Choose your framework:
- **Next.js** (App Router recommended)
- **Vite**
- **Remix**
- **Astro**
- **Laravel**
- **Gatsby**
- **React Router**
- **TanStack Router/Start**

### Installing Components

Use the CLI to install individual components:

```bash
# Install a button component
npx shadcn-ui@latest add button

# Install form components
npx shadcn-ui@latest add form input select checkbox

# Install a data table
npx shadcn-ui@latest add data-table
```

Or ask me directly to "add a login form" - I can use the MCP server to handle installation with natural language.

## Component Categories

### Form & Input Components
**Use for**: Data collection, user input, validation
- `form` - Complex forms with React Hook Form
- `input` - Text fields
- `textarea` - Multi-line text
- `select` - Dropdown selections
- `checkbox` - Boolean inputs
- `radio-group` - Single selection from options
- `switch` - Toggle boolean states
- `date-picker` - Date selection
- `combobox` - Searchable select with autocomplete

### Layout & Navigation
**Use for**: App structure, navigation flows, content organization
- `sidebar` - Collapsible side navigation
- `tabs` - Tabbed content
- `accordion` - Collapsible sections
- `breadcrumb` - Navigation path
- `navigation-menu` - Dropdown menus
- `scroll-area` - Custom scrollable regions

### Overlays & Dialogs
**Use for**: Modals, confirmations, floating content
- `dialog` - Modal dialogs
- `alert-dialog` - Confirmation prompts
- `drawer` - Mobile-friendly side panels
- `popover` - Floating popovers
- `tooltip` - Hover information
- `dropdown-menu` - Menu dropdowns
- `context-menu` - Right-click menus

### Data Display
**Use for**: Showing structured data
- `table` - Basic HTML tables
- `data-table` - Advanced tables with sorting/filtering/pagination
- `avatar` - User profile images
- `badge` - Status labels
- `card` - Content containers

### Feedback & Status
**Use for**: User feedback, loading states, alerts
- `alert` - Alert messages
- `toast` - Notifications
- `progress` - Progress bars
- `skeleton` - Loading placeholders
- `spinner` - Loading indicators

## Component Selection Guide

Ask yourself these questions to choose the right component:

1. **What is the user interacting with?**
   - Text input → use `input`
   - Choosing from options → use `select` or `combobox`
   - Yes/no decision → use `checkbox` or `switch`
   - Multiple fields → use `form`

2. **How should it be displayed?**
   - Inline with other content → `input`, `select`
   - Centered on screen → `dialog`
   - Slide from side → `drawer`
   - Information tooltip → `tooltip`

3. **What's the context?**
   - Inside a form → use `field` component with `form`
   - Standalone button → use `button`
   - Inside a table → use table row cell or `data-table`

4. **Does it need validation?**
   - Yes → combine `form` + `field` + React Hook Form
   - No → use simple components (`input`, `select`)

## Common Implementation Patterns

### Basic Form with Validation

```tsx
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { Button } from "@/components/ui/button"
import { Form, FormField, FormItem, FormLabel, FormControl } from "@/components/ui/form"
import { Input } from "@/components/ui/input"

const formSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})

export function LoginForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
  })

  function onSubmit(values: z.infer<typeof formSchema>) {
    console.log(values)
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input placeholder="you@example.com" {...field} />
              </FormControl>
            </FormItem>
          )}
        />
        <Button type="submit">Submit</Button>
      </form>
    </Form>
  )
}
```

### Dialog Pattern

```tsx
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"

export function DeleteDialog() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="destructive">Delete</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Are you sure?</DialogTitle>
          <DialogDescription>
            This action cannot be undone.
          </DialogDescription>
        </DialogHeader>
        <div className="flex gap-3 justify-end">
          <Button variant="outline">Cancel</Button>
          <Button variant="destructive">Delete</Button>
        </div>
      </DialogContent>
    </Dialog>
  )
}
```

## Styling & Customization

All components use **Tailwind CSS** for styling. Customize appearance through:

### 1. Tailwind Classes
Add classes directly to components:
```tsx
<Button className="w-full text-lg">Full Width</Button>
<Input className="rounded-lg border-2" />
```

### 2. CSS Variables (Theme Colors)
shadcn/ui uses CSS variables for theming. Edit `app/globals.css`:
```css
@layer base {
  :root {
    --primary: 222.2 47.4% 11.2%;
    --secondary: 210 40% 96%;
  }
}
```

### 3. Dark Mode
Enable dark mode in your framework:
- **Next.js**: Configure in `next.config.js`
- **Vite**: Add dark class detection in `tailwind.config.js`
- Components automatically respond to `dark` class

### 4. Component Variants
Many components have built-in variants:
```tsx
<Button variant="outline" />
<Button variant="ghost" />
<Button variant="destructive" />
<Badge variant="secondary" />
```

## Composition & Best Practices

### 1. Composition Over Customization
Combine small components rather than modifying large ones:
```tsx
// ✅ Good: Compose components
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
  </CardHeader>
  <CardContent>
    <Form>...</Form>
  </CardContent>
</Card>

// ❌ Avoid: Over-modifying single component
<CustomDialog withHeader={true} withForm={true} />
```

### 2. Use Type Safety
Leverage TypeScript for prop safety:
```tsx
import { Button } from "@/components/ui/button"
import type { ButtonProps } from "@/components/ui/button"

type CustomButtonProps = ButtonProps & {
  label: string
}
```

### 3. Accessibility Built-in
shadcn/ui uses Radix UI primitives with accessibility built-in:
- Keyboard navigation
- ARIA attributes
- Screen reader support
- Focus management

Just use components correctly; accessibility comes free.

### 4. Performance
- Components are small and modular
- Tree-shakeable
- No runtime overhead beyond Radix UI
- Use `React.memo` for frequently-rerendered components if needed

## Framework-Specific Notes

### Next.js
- Use `shadcn-ui@latest add form` for React Hook Form integration
- Combine with Server Actions for form submissions
- Dark mode works via `next-themes`

### Vite
- Ensure `tailwind.config.js` includes component paths
- Use Vite's HMR for fast development

### Remix
- Forms work with `remix` form actions
- Use route transitions for optimistic updates

## Common Customization Tasks

### Changing Primary Color
Edit `components.json` during init or manually update CSS variables in `globals.css`.

### Adding Custom Components
Create your own components in `components/ui/` following shadcn/ui patterns:
```tsx
// components/ui/my-component.tsx
import * as React from "react"

export interface MyComponentProps
  extends React.HTMLAttributes<HTMLDivElement> {}

const MyComponent = React.forwardRef<HTMLDivElement, MyComponentProps>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={className}
      {...props}
    />
  )
)
MyComponent.displayName = "MyComponent"

export { MyComponent }
```

### Theming for Multiple Brands
Use CSS variable layers:
```css
.brand-a {
  --primary: 220 90% 56%;
  --secondary: 0 0% 100%;
}

.brand-b {
  --primary: 0 100% 50%;
  --secondary: 200 100% 50%;
}
```

## Validation & Forms

### With React Hook Form + Zod
Best practice for complex forms with client-side validation:
```bash
npm install react-hook-form zod @hookform/resolvers
```

### With TanStack Form
Alternative for advanced form requirements:
```bash
npm install @tanstack/react-form
```

Ask me for specific form patterns (login, signup, multi-step, etc.)

## Troubleshooting

### Components Not Styling Correctly
- ✅ Verify Tailwind is configured in `tailwind.config.js`
- ✅ Check `components.json` has correct `path` setting
- ✅ Run `npm install` after adding components

### TypeScript Errors
- ✅ Ensure components are imported from `/components/ui/name`
- ✅ Components have proper TypeScript support built-in

### Form Validation Not Working
- ✅ Install `zod` and `@hookform/resolvers`
- ✅ Use `zodResolver` with `useForm`

## Next Steps

For detailed guidance on specific tasks:
- **[COMPONENT_GUIDE.md](COMPONENT_GUIDE.md)** - Deep dive into each component
- **[FORMS_GUIDE.md](FORMS_GUIDE.md)** - Building complex forms
- **[PATTERNS.md](PATTERNS.md)** - Common UI patterns and combinations
- **[CUSTOMIZATION.md](CUSTOMIZATION.md)** - Theming and styling guide

## Resources

- [shadcn/ui Documentation](https://ui.shadcn.com)
- [Radix UI Primitives](https://www.radix-ui.com)
- [Tailwind CSS](https://tailwindcss.com)
- [React Hook Form](https://react-hook-form.com)
- [Zod Validation](https://zod.dev)