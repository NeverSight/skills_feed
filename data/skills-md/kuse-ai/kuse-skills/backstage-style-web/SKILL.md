---
name: backstage-style-web
description: Generate enterprise-grade web applications using Backstage Design System. Create admin dashboards, developer tools, and internal applications with modern React components, dark/light themes, and responsive design patterns based on Radix UI and Tailwind CSS.
---

# Backstage Style Web Generator

## Overview

Create professional, enterprise-grade web applications using the Backstage Design System. This skill generates modern React applications with TypeScript, featuring comprehensive UI components, dark/light theme support, responsive design, and accessibility-first patterns. Perfect for building admin dashboards, developer tools, internal applications, and data management interfaces.

# Backstage Design System Implementation Guide

## Core Architecture Overview

The Backstage Design System is built on modern React patterns and industry-standard libraries:

### Technology Stack
- **React 18+** with TypeScript
- **Radix UI Primitives** for accessible, headless components
- **Tailwind CSS** for utility-first styling
- **Class Variance Authority (CVA)** for type-safe component variants
- **React Hook Form** with Zod validation
- **Lucide React** for consistent iconography

### Key Design Principles

1. **Accessibility First**: Built on Radix UI primitives with ARIA support
2. **Type Safety**: Full TypeScript coverage with strict typing
3. **Composability**: Components designed for flexible composition
4. **Consistency**: Unified design tokens and patterns
5. **Performance**: Optimized for bundle size and runtime performance

## Component Architecture Patterns

### 1. Compound Components
Components are designed with multiple sub-components for maximum flexibility:

```typescript
// Card component structure
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Description</CardDescription>
    <CardAction>Action buttons</CardAction>
  </CardHeader>
  <CardContent>
    Main content
  </CardContent>
  <CardFooter>
    Footer content
  </CardFooter>
</Card>
```

### 2. Variant-Based Styling
Using CVA for type-safe, predictable component variants:

```typescript
const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent",
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
);
```

### 3. Data Attributes for Styling
Consistent use of data attributes for component identification and styling:

```typescript
<div
  data-slot="card"
  className="bg-card text-card-foreground rounded-lg border"
>
  <div data-slot="card-header">
    {/* Header content */}
  </div>
</div>
```

## Theme System Implementation

### 1. Color Architecture

#### Brand Colors (11-step scale)
```css
:root {
  --brand-050: #F5F1F0;  /* 最浅背景色 */
  --brand-100: #E9DDDB;  /* Hover background / light tint */
  --brand-200: #D6BEBB;  /* Soft background */
  --brand-300: #B78F8A;  /* Subtle brand tint */
  --brand-400: #94635E;  /* Hover / outline */
  --brand-500: #6A4040;  /* Primary brand color */
  --brand-600: #5B3535;  /* Active / pressed */
  --brand-700: #4C2D2D;  /* Stronger contrast */
  --brand-800: #3E2525;  /* Deep background */
  --brand-900: #2E1C1C;  /* Text on light */
  --brand-950: #1C1010;  /* Text on dark / darkest tone */
}
```

#### Semantic Color Tokens
```css

:root {
  /* === Light Mode === */
  --background: hsl(48, 33%, 98%);
  --foreground: hsl(0, 25%, 33%);
  --card: hsl(48, 33%, 98%);
  --card-foreground: hsl(0, 25%, 33%);
  --popover: hsl(48, 33%, 98%);
  --popover-foreground: hsl(0, 25%, 33%);
  --primary: hsl(222, 28%, 14%);
  --primary-foreground: hsl(48, 33%, 98%);
  --secondary: hsl(210, 25%, 96%);
  --secondary-foreground: hsl(0, 25%, 33%);
  --muted: hsl(210, 25%, 96%);
  --muted-foreground: hsl(215, 9%, 46%);
  --accent: hsl(210, 25%, 96%);
  --accent-foreground: hsl(0, 25%, 33%);
  --destructive: hsl(0, 82%, 67%);
  --destructive-foreground: hsl(48, 33%, 98%);
  --border: hsl(0, 14%, 94%);
  --input: hsl(214, 27%, 91%);
  --ring: hsl(0, 25%, 33%);
}

[data-theme='dark'] {
  /* === Dark Mode === */
  --background: hsl(0, 25%, 6%);
  --foreground: hsl(48, 33%, 98%);
  --card: hsl(0, 25%, 6%);
  --card-foreground: hsl(48, 33%, 98%);
  --popover: hsl(0, 25%, 6%);
  --popover-foreground: hsl(48, 33%, 98%);
  --primary: hsl(48, 33%, 98%);
  --primary-foreground: hsl(0, 25%, 33%);
  --secondary: hsl(0, 22%, 14%);
  --secondary-foreground: hsl(48, 33%, 98%);
  --muted: hsl(0, 22%, 14%);
  --muted-foreground: hsl(0, 20%, 75%);
  --accent: hsl(0, 22%, 14%);
  --accent-foreground: hsl(48, 33%, 98%);
  --destructive: hsl(0, 82%, 67%);
  --destructive-foreground: hsl(48, 33%, 98%);
  --border: hsl(0, 22%, 14%);
  --input: hsl(0, 22%, 14%);
  --ring: hsl(0, 25%, 33%);
}


```

### 2. Font Families
```css
/* Import custom fonts */
@font-face {
  font-family: 'Instrument Serif';
  src: url('./references/InstrumentSerif-Regular.ttf') format('truetype');
  font-weight: 400;
  font-style: normal;
}

@font-face {
  font-family: 'Instrument Serif';
  src: url('./references/InstrumentSerif-Italic.ttf') format('truetype');
  font-weight: 400;
  font-style: italic;
}

/* Typography Rules */
/* Paragraph and text content */
p, .text-body, .text-content {
  font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* Headings */
h1, h2, h3, h4, h5, h6,
.heading-1, .heading-2, .heading-3, .heading-4, .heading-5, .heading-6 {
  font-family: 'Instrument Serif', Georgia, 'Times New Roman', serif;
  font-weight: 400;
}

/* Prepositions in headings should use italic */
h1 .preposition, h2 .preposition, h3 .preposition,
h4 .preposition, h5 .preposition, h6 .preposition,
.heading-1 .preposition, .heading-2 .preposition, .heading-3 .preposition,
.heading-4 .preposition, .heading-5 .preposition, .heading-6 .preposition {
  font-style: italic;
}
```

### 3. Typography Scale
```css
.text-xxs { font-size: 8px; }   /* Micro text */
.text-xs  { font-size: 10px; }  /* Caption */
.text-sm  { font-size: 12px; }  /* Secondary text */
.text-base { font-size: 14px; } /* Default body */
.text-lg  { font-size: 16px; }  /* Paragraph */
.display-xl { font-size: 60px; } /* Hero headings */
```

### 4. Spacing System (4px base unit)
```css
.space-1 { margin: 4px; }   /* XS */
.space-2 { margin: 8px; }   /* SM */
.space-3 { margin: 12px; }  /* MD */
.space-4 { margin: 16px; }  /* LG - Component spacing */
.space-6 { margin: 24px; }  /* Standard spacing */
.space-8 { margin: 32px; }  /* Section padding */
.space-16 { margin: 64px; } /* Large sections */
```

## Responsive Design Strategy

### 1. Breakpoint System
```css
/* Mobile-first approach */
sm: '640px',   /* Small devices */
md: '768px',   /* Tablets */
lg: '1024px',  /* Laptops */
xl: '1280px',  /* Desktops */
2xl: '1536px'  /* Large screens */
```

### 2. Component Responsiveness
```typescript
// Example: Responsive grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Cards automatically adapt */}
</div>

// Custom mobile hook
const isMobile = useIsMobile(); // 768px breakpoint
```

### 3. Sidebar Adaptation
```typescript
// Desktop: Collapsible sidebar
// Mobile: Transforms to sheet/drawer
{isMobile ? (
  <Sheet open={openMobile} onOpenChange={setOpenMobile}>
    <SheetContent side="left" className="p-0">
      <SidebarContent />
    </SheetContent>
  </Sheet>
) : (
  <Sidebar className={cn(
    "transition-all duration-300",
    state === "collapsed" ? "w-[48px]" : "w-[256px]"
  )}>
    <SidebarContent />
  </Sidebar>
)}
```

## Accessibility Implementation

### 1. ARIA Patterns
```typescript
// Proper ARIA labeling
<button
  aria-label="Close dialog"
  aria-expanded={isOpen}
  aria-controls="dialog-content"
>
  <X className="h-4 w-4" />
</button>

// Form accessibility
<label htmlFor="email" className="sr-only">
  Email address
</label>
<input
  id="email"
  type="email"
  aria-describedby="email-description"
  aria-invalid={hasError}
/>
<div id="email-description" className="text-sm text-muted-foreground">
  We'll never share your email
</div>
```

### 2. Keyboard Navigation
```typescript
// Custom keyboard event handling
useEffect(() => {
  const handleKeyDown = (event: KeyboardEvent) => {
    if (event.key === 'Escape') {
      onClose();
    }
    if (event.key === 'Enter' || event.key === ' ') {
      onActivate();
    }
  };

  document.addEventListener('keydown', handleKeyDown);
  return () => document.removeEventListener('keydown', handleKeyDown);
}, [onClose, onActivate]);
```

### 3. Focus Management
```typescript
// Focus trap for modals
import { FocusTrap } from '@radix-ui/react-focus-trap';

<FocusTrap asChild>
  <div className="modal-content">
    {/* Modal content with proper focus order */}
  </div>
</FocusTrap>
```

## Form Architecture

### 1. React Hook Form Integration
```typescript
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";

const formSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(8, "Password must be at least 8 characters"),
});

type FormData = z.infer<typeof formSchema>;

const form = useForm<FormData>({
  resolver: zodResolver(formSchema),
  defaultValues: {
    email: "",
    password: "",
  },
});
```

### 2. Form Field Component Pattern
```typescript
<FormField
  control={form.control}
  name="email"
  render={({ field }) => (
    <FormItem>
      <FormLabel>Email</FormLabel>
      <FormControl>
        <Input placeholder="Enter your email" {...field} />
      </FormControl>
      <FormDescription>
        We'll use this to send you updates
      </FormDescription>
      <FormMessage />
    </FormItem>
  )}
/>
```

## State Management Patterns

### 1. Component State
```typescript
// Local state for UI interactions
const [isOpen, setIsOpen] = useState(false);
const [selectedItems, setSelectedItems] = useState<string[]>([]);

// Derived state
const hasSelection = selectedItems.length > 0;
const allSelected = selectedItems.length === items.length;
```

### 2. Context for Shared State
```typescript
// Theme context
const ThemeContext = createContext<{
  theme: Theme;
  setTheme: (theme: Theme) => void;
} | null>(null);

// Sidebar context
const SidebarContext = createContext<{
  state: "expanded" | "collapsed";
  open: boolean;
  setOpen: (open: boolean) => void;
  isMobile: boolean;
} | null>(null);
```

### 3. URL State Management
```typescript
// For filters, search, pagination
const [searchParams, setSearchParams] = useSearchParams();

const currentPage = Number(searchParams.get('page')) || 1;
const searchQuery = searchParams.get('q') || '';

const updateFilters = (filters: Record<string, string>) => {
  const newParams = new URLSearchParams(searchParams);
  Object.entries(filters).forEach(([key, value]) => {
    if (value) {
      newParams.set(key, value);
    } else {
      newParams.delete(key);
    }
  });
  setSearchParams(newParams);
};
```

## Performance Optimization

### 1. Code Splitting
```typescript
// Lazy loading for routes
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

// Wrap in Suspense
<Suspense fallback={<LoadingSpinner />}>
  <Routes>
    <Route path="/dashboard" element={<Dashboard />} />
    <Route path="/settings" element={<Settings />} />
  </Routes>
</Suspense>
```

### 2. Memoization
```typescript
// Expensive calculations
const processedData = useMemo(() => {
  return data.map(item => ({
    ...item,
    computed: expensiveComputation(item)
  }));
}, [data]);

// Callback memoization
const handleItemClick = useCallback((id: string) => {
  setSelectedItems(prev =>
    prev.includes(id)
      ? prev.filter(item => item !== id)
      : [...prev, id]
  );
}, []);

// Component memoization
const MemoizedTableRow = memo(TableRow);
```

### 3. Virtual Scrolling (for large lists)
```typescript
import { FixedSizeList as List } from 'react-window';

const VirtualizedTable = ({ items }: { items: any[] }) => {
  const Row = ({ index, style }: { index: number; style: React.CSSProperties }) => (
    <div style={style}>
      <TableRow data={items[index]} />
    </div>
  );

  return (
    <List
      height={600}
      itemCount={items.length}
      itemSize={50}
      width="100%"
    >
      {Row}
    </List>
  );
};
```

## Testing Patterns

### 1. Component Testing
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './button';

describe('Button', () => {
  it('renders with correct variant styles', () => {
    render(<Button variant="destructive">Delete</Button>);
    const button = screen.getByRole('button');
    expect(button).toHaveClass('bg-destructive');
  });

  it('handles click events', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

### 2. Accessibility Testing
```typescript
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

it('should not have accessibility violations', async () => {
  const { container } = render(<MyComponent />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

This implementation guide provides the foundation for building consistent, accessible, and performant applications using the Backstage Design System.
