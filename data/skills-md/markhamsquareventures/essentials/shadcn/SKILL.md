---
name: shadcn
description: How to work effectively with shadcn/ui components, always use when adding UI components
---

# shadcn/ui

## Instructions

This project uses shadcn/ui with the **New York** style variant. Components are built on Radix UI primitives with Tailwind CSS styling.

### Configuration

- Style: `new-york`
- Base color: `neutral`
- Icons: `lucide-react`
- Components location: `resources/js/components/ui/`
- Utils location: `resources/js/lib/utils.ts`

### Adding New Components

Use the shadcn CLI to add components:

```bash
npx shadcn@latest add <component-name>
```

Examples:

```bash
npx shadcn@latest add table
npx shadcn@latest add tabs
npx shadcn@latest add calendar
```

Do NOT manually create shadcn components - always use the CLI to ensure correct styling and dependencies.

### Available Components

Components already installed in this project:

- `alert`
- `alert-dialog`
- `avatar`
- `badge`
- `breadcrumb`
- `button`
- `card`
- `checkbox`
- `collapsible`
- `dialog`
- `dropdown-menu`
- `input`, `input-otp`
- `label`
- `navigation-menu`
- `select`
- `separator`
- `sheet`
- `sidebar`
- `skeleton`
- `sonner` (toast notifications)
- `spinner`
- `toggle`, `toggle-group`
- `tooltip`

### Using Components

Always import from `@/components/ui/`:

<code-snippet name="Importing shadcn Components" lang="tsx">
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from '@/components/ui/card';
</code-snippet>

### Button Variants

<code-snippet name="Button Variants" lang="tsx">
<Button>Default</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="destructive">Destructive</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="link">Link</Button>

{/_ Sizes _/}
<Button size="sm">Small</Button>
<Button size="default">Default</Button>
<Button size="lg">Large</Button>
<Button size="icon"><IconComponent /></Button>
</code-snippet>

### Form Patterns

Use Label + Input together, with proper error styling:

<code-snippet name="Form Field Pattern" lang="tsx">
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';

<div className="space-y-2">
    <Label htmlFor="email">Email</Label>
    <Input
        id="email"
        name="email"
        type="email"
        placeholder="you@example.com"
        aria-invalid={!!errors.email}
    />
    {errors.email && (
        <p className="text-sm text-destructive">{errors.email}</p>
    )}
</div>
</code-snippet>

### Dialog Pattern

<code-snippet name="Dialog Example" lang="tsx">
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from '@/components/ui/dialog';

<Dialog>
    <DialogTrigger asChild>
        <Button>Open Dialog</Button>
    </DialogTrigger>
    <DialogContent>
        <DialogHeader>
            <DialogTitle>Dialog Title</DialogTitle>
            <DialogDescription>
                Description text goes here.
            </DialogDescription>
        </DialogHeader>
        {/* Dialog content */}
    </DialogContent>
</Dialog>
</code-snippet>

### Toast Notifications

Use Sonner for toast notifications:

<code-snippet name="Toast Usage" lang="tsx">
import { toast } from 'sonner';

// Success
toast.success('Changes saved successfully');

// Error
toast.error('Something went wrong');

// With description
toast.success('Project created', {
description: 'Your new project is ready to use.',
});
</code-snippet>

### The cn() Utility

Use `cn()` from `@/lib/utils` to merge Tailwind classes conditionally:

<code-snippet name="cn() Usage" lang="tsx">
import { cn } from '@/lib/utils';

<div className={cn(
    'rounded-lg border p-4',
    isActive && 'border-primary bg-primary/10',
    className
)}>
    {children}
</div>
</code-snippet>

### Icons

Use Lucide React for icons:

<code-snippet name="Icon Usage" lang="tsx">
import { Plus, Trash2, Edit, ChevronRight } from 'lucide-react';

<Button>
    <Plus /> Add Item
</Button>

<Button variant="ghost" size="icon">
    <Trash2 />
</Button>
</code-snippet>
