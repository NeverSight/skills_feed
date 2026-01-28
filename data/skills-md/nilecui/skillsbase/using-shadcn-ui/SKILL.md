---
name: using-shadcn-ui
description: Use when building React UI components, implementing design systems, or needing pre-built accessible components - leverages shadcn/ui primitives and shadcnblocks.com (829 production-ready blocks) for rapid interface development
---

# Using shadcn/ui

## Overview

shadcn/ui is a collection of re-usable, accessible React components built on Radix UI and Tailwind CSS. Unlike traditional component libraries, shadcn/ui copies components directly into your project, giving you full ownership and customization control.

**Core principle:** Components live in your codebase. You own the code. No package.json dependency.

## When to Use

**Use shadcn/ui when:**
- Building React applications with Tailwind CSS
- Need accessible, customizable UI components
- Want pre-built patterns without library lock-in
- Implementing common UI patterns (forms, dialogs, dropdowns, etc.)
- Starting new projects that need design system foundation
- Need production-ready blocks for hero sections, pricing, testimonials, etc.

**shadcnblocks.com integration:**
- 829 blocks across 42 categories
- Production-ready sections (Hero, Navbar, Footer, Pricing, Testimonials, etc.)
- Copy-paste directly into your project
- Built with same shadcn/ui primitives

**Don't use for:**
- Non-React projects
- Projects without Tailwind CSS
- When you need a locked, versioned component library
- Simple HTML/CSS projects

## Installation Workflow

### 1. Initialize shadcn/ui

```bash
npx shadcn@latest init
```

**Configuration prompts:**
- Style: Default or New York
- Color: Slate, Gray, Zinc, etc.
- CSS variables: Yes (recommended)
- Tailwind config: Use CSS variables for colors

### 2. Add Components

```bash
# Add specific components
npx shadcn@latest add button
npx shadcn@latest add dialog
npx shadcn@latest add form

# Add multiple at once
npx shadcn@latest add button card dialog dropdown-menu
```

**Components install to:** `components/ui/`

### 3. Using shadcnblocks.com

**Visit:** https://www.shadcnblocks.com/blocks

**Workflow:**
1. Browse category (Hero, Pricing, Testimonial, etc.)
2. Find desired block
3. Click "Copy Code"
4. Paste into your component file
5. Install any missing shadcn/ui dependencies
6. Customize colors, text, and layout

## Component Categories Reference

| Category | Common Use Cases | Example Components |
|----------|------------------|-------------------|
| **Forms** | User input, validation | Input, Textarea, Select, Checkbox, Radio Group |
| **Overlays** | Modals, popovers | Dialog, Popover, Tooltip, Sheet |
| **Navigation** | Menus, dropdowns | Dropdown Menu, Navigation Menu, Tabs |
| **Feedback** | User notifications | Alert, Toast, Progress, Skeleton |
| **Data Display** | Tables, cards, badges | Table, Card, Badge, Avatar |
| **Layout** | Containers, separators | Separator, Aspect Ratio, Scroll Area |

## shadcnblocks.com Categories (829 blocks)

### Layout & Navigation (200 blocks)
- **Hero** (162 blocks): Landing page headers with CTAs
- **Navbar** (13 blocks): Navigation headers
- **Footer** (18 blocks): Page footers
- **Banner** (7 blocks): Announcement bars

### Content Sections (367 blocks)
- **Feature** (266 blocks): Product feature showcases
- **Blog** (22 blocks): Blog layouts and cards
- **Gallery** (47 blocks): Image galleries
- **Timeline** (14 blocks): Event timelines
- **Team** (10 blocks): Team member profiles
- **About** (10 blocks): About us sections

### Business Components (116 blocks)
- **Pricing** (35 blocks): Pricing tables and cards
- **Testimonial** (28 blocks): Customer testimonials
- **Case Studies** (9 blocks): Success stories
- **Integration** (16 blocks): Integration showcases
- **Service/Services** (21 blocks): Service offerings
- **Stats** (17 blocks): Statistics displays

### User Engagement (64 blocks)
- **CTA** (25 blocks): Call-to-action sections
- **Contact** (13 blocks): Contact forms
- **Signup/Login** (17 blocks): Authentication forms
- **Waitlist** (2 blocks): Email capture
- **Community** (7 blocks): Community features

### Information Display (82 blocks)
- **FAQ** (15 blocks): Frequently asked questions
- **Comparison** (10 blocks): Feature comparisons
- **Logos** (11 blocks): Logo grids
- **Resources** (4 blocks): Resource libraries
- **Download** (12 blocks): Download sections
- **Changelog** (7 blocks): Update logs
- **Careers** (9 blocks): Job listings
- **Compliance** (3 blocks): Legal/privacy sections

## Quick Start Example

```typescript
// 1. Add button component
// $ npx shadcn@latest add button

// 2. Import and use
import { Button } from "@/components/ui/button"

export function MyComponent() {
  return (
    <div>
      <Button variant="default">Click me</Button>
      <Button variant="destructive">Delete</Button>
      <Button variant="outline">Cancel</Button>
      <Button variant="ghost">Subtle</Button>
    </div>
  )
}
```

## Form Pattern with shadcn/ui

```typescript
// Install: npx shadcn@latest add form input button

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"

const formSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(8, "Password must be at least 8 characters"),
})

export function LoginForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  })

  function onSubmit(values: z.infer<typeof formSchema>) {
    console.log(values)
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input placeholder="you@example.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="password"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Password</FormLabel>
              <FormControl>
                <Input type="password" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Sign In</Button>
      </form>
    </Form>
  )
}
```

## Dialog/Modal Pattern

```typescript
// Install: npx shadcn@latest add dialog button

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"

export function ConfirmDialog() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="destructive">Delete Account</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Are you absolutely sure?</DialogTitle>
          <DialogDescription>
            This action cannot be undone. This will permanently delete your
            account and remove your data from our servers.
          </DialogDescription>
        </DialogHeader>
        <div className="flex justify-end gap-3">
          <Button variant="outline">Cancel</Button>
          <Button variant="destructive">Delete</Button>
        </div>
      </DialogContent>
    </Dialog>
  )
}
```

## Using Blocks from shadcnblocks.com

### Example: Adding a Hero Section

**1. Visit:** https://www.shadcnblocks.com/blocks
**2. Navigate to:** Hero category
**3. Select a design**
**4. Click "Copy Code"**
**5. Create component:**

```typescript
// app/components/hero.tsx
// (Paste copied code from shadcnblocks.com)

import { Button } from "@/components/ui/button"

export function Hero() {
  return (
    <section className="container flex flex-col items-center gap-8 pt-20 pb-12">
      <h1 className="text-6xl font-bold text-center">
        Build amazing products
      </h1>
      <p className="text-xl text-muted-foreground text-center max-w-2xl">
        Get started with production-ready components built with shadcn/ui
      </p>
      <div className="flex gap-4">
        <Button size="lg">Get Started</Button>
        <Button size="lg" variant="outline">Learn More</Button>
      </div>
    </section>
  )
}
```

**6. Install missing components:**
```bash
npx shadcn@latest add button
```

**7. Import and use:**
```typescript
import { Hero } from "@/components/hero"

export default function Home() {
  return <Hero />
}
```

### Example: Adding a Pricing Section

```typescript
// Install: npx shadcn@latest add card button badge

import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

export function Pricing() {
  return (
    <section className="container py-20">
      <h2 className="text-4xl font-bold text-center mb-12">
        Simple, transparent pricing
      </h2>
      <div className="grid md:grid-cols-3 gap-8">
        <Card>
          <CardHeader>
            <CardTitle>Starter</CardTitle>
            <CardDescription>Perfect for trying out</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold mb-2">$9</div>
            <p className="text-sm text-muted-foreground">per month</p>
          </CardContent>
          <CardFooter>
            <Button className="w-full">Get Started</Button>
          </CardFooter>
        </Card>

        <Card className="border-primary">
          <CardHeader>
            <Badge className="w-fit mb-2">Most Popular</Badge>
            <CardTitle>Pro</CardTitle>
            <CardDescription>For growing businesses</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold mb-2">$29</div>
            <p className="text-sm text-muted-foreground">per month</p>
          </CardContent>
          <CardFooter>
            <Button className="w-full">Get Started</Button>
          </CardFooter>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Enterprise</CardTitle>
            <CardDescription>For large organizations</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold mb-2">Custom</div>
            <p className="text-sm text-muted-foreground">contact us</p>
          </CardContent>
          <CardFooter>
            <Button className="w-full" variant="outline">Contact Sales</Button>
          </CardFooter>
        </Card>
      </div>
    </section>
  )
}
```

## Customization

### Theme Colors

Edit `app/globals.css` or `styles/globals.css`:

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    --primary-foreground: 210 40% 98%;
    /* ... more CSS variables */
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    /* ... dark mode colors */
  }
}
```

### Component Variants

Components use `class-variance-authority` for variants:

```typescript
import { Button } from "@/components/ui/button"

// Available variants:
<Button variant="default">Default</Button>
<Button variant="destructive">Destructive</Button>
<Button variant="outline">Outline</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="link">Link</Button>

// Available sizes:
<Button size="default">Default</Button>
<Button size="sm">Small</Button>
<Button size="lg">Large</Button>
<Button size="icon">Icon</Button>
```

### Extending Components

Edit the component file directly in `components/ui/`:

```typescript
// components/ui/button.tsx
const buttonVariants = cva(
  "inline-flex items-center justify-center...",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground...",
        destructive: "bg-destructive text-destructive-foreground...",
        // Add custom variant:
        success: "bg-green-600 text-white hover:bg-green-700",
      },
      // ... rest of variants
    }
  }
)
```

## Common Patterns

### Loading States

```typescript
import { Button } from "@/components/ui/button"
import { Loader2 } from "lucide-react"

export function LoadingButton() {
  const [isLoading, setIsLoading] = useState(false)

  return (
    <Button disabled={isLoading}>
      {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
      {isLoading ? "Loading..." : "Submit"}
    </Button>
  )
}
```

### Toast Notifications

```typescript
// Install: npx shadcn@latest add toast

import { useToast } from "@/hooks/use-toast"
import { Button } from "@/components/ui/button"

export function ToastExample() {
  const { toast } = useToast()

  return (
    <Button
      onClick={() => {
        toast({
          title: "Success!",
          description: "Your changes have been saved.",
        })
      }}
    >
      Show Toast
    </Button>
  )
}
```

### Data Tables

```typescript
// Install: npx shadcn@latest add table

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

const invoices = [
  { invoice: "INV001", status: "Paid", amount: "$250.00" },
  { invoice: "INV002", status: "Pending", amount: "$150.00" },
]

export function InvoiceTable() {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Invoice</TableHead>
          <TableHead>Status</TableHead>
          <TableHead>Amount</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {invoices.map((invoice) => (
          <TableRow key={invoice.invoice}>
            <TableCell>{invoice.invoice}</TableCell>
            <TableCell>{invoice.status}</TableCell>
            <TableCell>{invoice.amount}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Installing as npm package | shadcn/ui copies code. Run `npx shadcn@latest add [component]` |
| Importing from `shadcn` | Import from `@/components/ui/[component]` |
| Not installing dependencies | Each component may need additional packages (listed in CLI) |
| Modifying in node_modules | Components live in your `components/ui/` - edit directly |
| Forgetting Tailwind config | Run `npx shadcn@latest init` to configure properly |
| Skipping shadcnblocks.com | Don't build common sections from scratch - use 829 ready blocks |

## Workflow Summary

**Starting new project:**
1. `npx shadcn@latest init`
2. Add needed components: `npx shadcn@latest add button card dialog`
3. Browse shadcnblocks.com for section blocks
4. Copy blocks, install dependencies, customize

**Adding new feature:**
1. Identify needed components (form, dialog, etc.)
2. `npx shadcn@latest add [components]`
3. Check shadcnblocks.com for similar patterns
4. Build or adapt from block
5. Customize colors and content

**Customizing:**
1. Edit component files in `components/ui/` directly
2. Modify `globals.css` for theme colors
3. Add variants using `class-variance-authority` patterns

## Resources

- **Official Docs:** https://ui.shadcn.com
- **shadcnblocks.com:** https://www.shadcnblocks.com/blocks (829 blocks)
- **Components:** https://ui.shadcn.com/docs/components
- **Themes:** https://ui.shadcn.com/themes
- **Examples:** https://ui.shadcn.com/examples

## Integration with Other Tools

**Works seamlessly with:**
- Next.js (App Router or Pages)
- Remix
- Astro
- Vite + React
- React Hook Form
- Zod validation
- Tailwind CSS
- Radix UI (under the hood)
