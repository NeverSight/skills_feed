---
name: component-library
description: Comprehensive React component library with 30+ production-ready components using shadcn/ui architecture, CVA variants, Radix UI primitives, and Tailwind CSS. Use when users need to (1) Create React UI components with modern patterns, (2) Build complete component systems with consistent design, (3) Implement accessible, responsive, dark-mode-ready components, (4) Generate form components with React Hook Form integration, (5) Create data display components like tables, cards, charts, or (6) Build navigation, layout, or feedback components. Provides instant generation of customizable components that would otherwise take 20-45 minutes each to hand-code.
---

# Component Library - shadcn/ui Architecture

Generate production-ready React components with shadcn/ui patterns, saving 8-10 hours per project.

## Quick Start

When generating components:
1. Create `/components/ui/` directory structure
2. Generate `lib/utils.ts` with cn() helper first
3. Create requested components with full TypeScript, variants, and accessibility
4. Include example usage for each component

## Core Setup Files

### Always generate these first:

**lib/utils.ts** - Essential cn() helper:
```typescript
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

**components.json** - Component registry:
```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "default",
  "rsc": false,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.js",
    "css": "app/globals.css",
    "baseColor": "slate",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils"
  }
}
```

## Component Categories

### Form Components
- **Input** - Text input with variants (default, ghost, underline)
- **Select** - Custom dropdown with search, multi-select options  
- **Checkbox** - With indeterminate state support
- **Radio** - Radio groups with custom styling
- **Switch** - Toggle switches with labels
- **Textarea** - Auto-resize, character count variants
- **DatePicker** - Calendar integration, range selection
- **FileUpload** - Drag & drop, preview, progress
- **Slider** - Range input with marks, tooltips
- **Form** - React Hook Form wrapper with validation

### Display Components  
- **Card** - Container with header/footer slots
- **Table** - Sortable, filterable, pagination
- **Badge** - Status indicators with variants
- **Avatar** - Image/initials with fallback
- **Progress** - Linear and circular variants
- **Skeleton** - Loading states
- **Separator** - Visual dividers
- **ScrollArea** - Custom scrollbars

### Feedback Components
- **Alert** - Info/warning/error/success states
- **Toast** - Notifications with actions
- **Dialog/Modal** - Accessible overlays
- **Tooltip** - Hover information
- **Popover** - Positioned content
- **AlertDialog** - Confirmation dialogs

### Navigation Components
- **Navigation** - Responsive nav with mobile menu
- **Tabs** - Tab panels with keyboard nav
- **Breadcrumb** - Path navigation
- **Pagination** - Page controls
- **CommandMenu** - Command palette (⌘K)
- **ContextMenu** - Right-click menus
- **DropdownMenu** - Action menus

### Layout Components
- **Accordion** - Collapsible sections
- **Collapsible** - Show/hide content
- **ResizablePanels** - Draggable split panes
- **Sheet** - Slide-out panels
- **AspectRatio** - Maintain ratios

## Component Implementation Patterns

### Use CVA for all variants:
```typescript
import { cva, type VariantProps } from "class-variance-authority"

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)
```

### Accessibility Requirements:
- ARIA labels and roles on all interactive elements
- Keyboard navigation (Tab, Arrow keys, Enter, Escape)
- Focus management and trapping for modals
- Screen reader announcements
- Semantic HTML elements

### Dark Mode Support:
- Use Tailwind dark: modifier
- CSS variables for theme colors
- Smooth transitions between modes

### Responsive Design:
- Mobile-first approach
- Container queries where appropriate
- Touch-friendly tap targets (min 44x44px)
- Responsive typography scale

## Dependencies

Include in package.json:
```json
{
  "dependencies": {
    "@radix-ui/react-accordion": "^1.1.2",
    "@radix-ui/react-alert-dialog": "^1.0.5",
    "@radix-ui/react-avatar": "^1.0.4",
    "@radix-ui/react-checkbox": "^1.0.4",
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-dropdown-menu": "^2.0.6",
    "@radix-ui/react-label": "^2.0.2",
    "@radix-ui/react-popover": "^1.0.7",
    "@radix-ui/react-progress": "^1.0.3",
    "@radix-ui/react-radio-group": "^1.1.3",
    "@radix-ui/react-select": "^2.0.0",
    "@radix-ui/react-separator": "^1.0.3",
    "@radix-ui/react-slider": "^1.1.2",
    "@radix-ui/react-switch": "^1.0.3",
    "@radix-ui/react-tabs": "^1.0.4",
    "@radix-ui/react-toast": "^1.1.5",
    "@radix-ui/react-tooltip": "^1.0.7",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.0.0",
    "cmdk": "^0.2.0",
    "date-fns": "^2.30.0",
    "lucide-react": "^0.263.1",
    "react-day-picker": "^8.8.0",
    "react-hook-form": "^7.45.4",
    "tailwind-merge": "^1.14.0",
    "tailwindcss-animate": "^1.0.7"
  }
}
```

## Implementation Workflow

1. **Assess Requirements**: Identify which components are needed
2. **Generate Base Files**: Create utils.ts and components.json
3. **Create Components**: Generate requested components with all features
4. **Provide Examples**: Include usage examples for each component
5. **Document Props**: Add TypeScript interfaces with JSDoc comments

## Advanced Patterns

For complex requirements, see:
- **references/form-patterns.md** - Advanced form handling
- **references/data-tables.md** - Complex table implementations  
- **references/animation-patterns.md** - Framer Motion integration
- **references/testing-setup.md** - Component testing patterns

## Performance Optimization

- Use React.memo for expensive components
- Implement virtual scrolling for long lists
- Lazy load heavy components
- Optimize bundle size with tree shaking
- Use CSS containment for layout stability

## Component Generation Tips

When generating components:
- Include all variant combinations
- Add proper TypeScript types
- Implement keyboard shortcuts
- Include loading and error states
- Provide Storybook stories structure
- Add comprehensive prop documentation
- Include accessibility attributes
- Test with screen readers
