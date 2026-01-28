---
name: metronic-module
description: Create new modules for the Providr Provider Portal using Metronic Tailwind React theme, Shadcn UI, and KeenIcons. Use when building new features, pages, or modules that follow the established patterns, or when the user asks to create a module using Metronic conventions.
---

# Metronic Provider Portal Module Creator

This skill helps you create production-ready modules for the Providr Provider Portal using the **Metronic Tailwind React theme** with established patterns and conventions.

## Quick Start

When creating a new module, you will:
1. Follow the established file structure patterns
2. Use Metronic theme components and layouts
3. Integrate with Shadcn UI component library
4. Apply consistent naming conventions
5. Implement responsive design with dark mode support

## Documentation Structure

This skill is organized into focused reference documents:

### 📁 [Patterns & Structure](./patterns.md)
- File structure patterns
- Directory organization
- Naming conventions
- Barrel exports
- Module creation checklist

### 🎨 [Components & UI](./components.md)
- Layout components (Container, Toolbar, etc.)
- Common component patterns (Cards, Buttons, Badges)
- Data tables with DataGrid
- Forms with Formik + Yup validation
- Dialogs and modals
- Dropdown menus
- KeenIcons usage

### 🎨 [Styling Conventions](./styling.md)
- Tailwind CSS patterns
- Metronic-specific classes
- Dark mode implementation
- Responsive design breakpoints
- Color system and theming

### 🔌 [API Integration](./api-integration.md)
- React Query patterns
- Data layer components
- Error handling
- Loading states

### 🛣️ [Routing & Menu](./routing-menu.md)
- Route configuration
- Protected routes
- Sidebar menu setup
- Permission-based access

### 📦 [Templates](./templates/)
Ready-to-use component templates:
- `page-template.tsx` - Main page component
- `content-template.tsx` - Content wrapper
- `form-template.tsx` - Form with validation
- `table-template.tsx` - Data table component

### 📚 [Examples](./examples/)
Complete working examples:
- Full module implementation
- Real-world use cases

## Tech Stack

### Core Technologies
- **Theme**: Metronic (Tailwind CSS version)
- **CSS Framework**: Tailwind CSS v3.4.14
- **Component Library**: Shadcn UI (Radix UI primitives)
- **Icons**: KeenIcons (ki-filled, ki-outline, ki-duotone, ki-solid)
- **Layout**: Demo1 (sidebar + fixed header)
- **TypeScript**: Fully typed components

### Libraries & Tools
- **UI Components**: Shadcn UI in `src/components/ui/`
- **Charts**: ApexCharts
- **Forms**: Formik + Yup validation
- **Notifications**: Sonner + Notistack
- **Data Tables**: TanStack React Table (DataGrid)
- **State Management**: React Query (server state) + Context API (UI state)

## Best Practices

1. **TypeScript First** - Always use TypeScript with proper type definitions
2. **Component Reuse** - Use existing Shadcn UI components, don't create custom ones
3. **Follow Patterns** - Reference similar modules (incidents, service-offerings) in the codebase
4. **Dark Mode** - Always implement dark mode with Tailwind `dark:` classes
5. **Responsive Design** - Test on mobile, tablet, and desktop viewports
6. **Loading & Error States** - Handle all data states properly
7. **Accessibility** - Use semantic HTML and ARIA attributes
8. **Icons** - Use only KeenIcons, not other icon libraries
9. **Absolute Imports** - Use `@/` for project-relative imports
10. **Permissions** - Implement role-based access control where needed

## Quick Reference: Component Imports

```tsx
// Layout
import { Container } from '@/components/Container';
import { Toolbar, ToolbarHeading, ToolbarActions } from '@/layouts/demo1';

// UI Components
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardBody } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Dialog, DialogContent } from '@/components/ui/dialog';

// Icons
import { KeenIcon } from '@/components/keenicons';

// Data & Forms
import { DataGrid } from '@/components/data-grid';
import { Formik, Form, Field } from 'formik';
import { useQuery, useMutation } from '@tanstack/react-query';
```

## Workflow

When asked to create a new module:

1. **Understand Requirements**
   - What is the module's purpose?
   - What data does it handle?
   - What permissions are needed?

2. **Review Patterns**
   - Check [patterns.md](./patterns.md) for structure
   - Look at existing similar modules in the codebase

3. **Build Components**
   - Use templates from [templates/](./templates/)
   - Follow examples in [components.md](./components.md)
   - Apply styling from [styling.md](./styling.md)

4. **Add Integration**
   - Implement data layer per [api-integration.md](./api-integration.md)
   - Configure routes per [routing-menu.md](./routing-menu.md)

5. **Finalize**
   - Test responsive design
   - Verify dark mode
   - Check permissions
   - Add to navigation menu

## Getting Help

- For file structure questions → See [patterns.md](./patterns.md)
- For UI component usage → See [components.md](./components.md)
- For styling help → See [styling.md](./styling.md)
- For data fetching → See [api-integration.md](./api-integration.md)
- For routing setup → See [routing-menu.md](./routing-menu.md)
- For ready-to-use code → See [templates/](./templates/)
- For complete examples → See [examples/](./examples/)

---

**Remember**: Always check existing modules in the codebase for real-world reference implementations before creating new patterns.
