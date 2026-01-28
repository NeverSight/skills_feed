---
name: nuxt-ui-component-finder
description: Find and explore Nuxt UI components with their props, slots, and examples. Use when users ask about available UI components or how to use specific Nuxt UI features.
---

# Nuxt UI Component Finder

Discover and learn about Nuxt UI components, their usage, props, and customization options.

## When to Use

**DO USE** when:
- User asks "What UI components are available?"
- Need component examples or API reference
- Questions about component props, slots, or events
- Comparing different components for a use case
- Need theming or customization examples

**DO NOT USE** when:
- General Nuxt questions (use nuxt-documentation-lookup)
- Installation/setup questions (covered in instructions)
- Already know which component to use (instructions have examples)

## Available Tools

### Component Information
- `mcp_nuxt-ui_list-components` - List all available components by category
- `mcp_nuxt-ui_get-component` - Get detailed component documentation
- `mcp_nuxt-ui_get-component-metadata` - Get component props, slots, events

### Examples
- `mcp_nuxt-ui_list-examples` - Browse component examples
- `mcp_nuxt-ui_get-example` - Get specific example implementation

### Documentation
- `mcp_nuxt-ui_list-documentation-pages` - List all docs pages
- `mcp_nuxt-ui_get-documentation-page` - Get specific docs content

## Process

**For Component Discovery:**
1. Use `mcp_nuxt-ui_list-components` to see all components
2. Components are organized by category:
   - Form (Button, Input, Select, Checkbox, etc.)
   - Layout (Card, Container, Divider, etc.)
   - Navigation (Tabs, Accordion, Breadcrumb, etc.)
   - Overlay (Modal, Popover, Dropdown, Tooltip, etc.)
   - Data (Table, Avatar, Badge, etc.)
   - Feedback (Alert, Progress, Skeleton, etc.)

**For Component Details:**
1. Use `mcp_nuxt-ui_get-component` with component name (e.g., "Button")
2. Returns full documentation with usage examples

**For Props/API Reference:**
1. Use `mcp_nuxt-ui_get-component-metadata` with component name
2. Returns TypeScript props, slots, events definitions

**For Examples:**
1. Use `mcp_nuxt-ui_list-examples` to browse examples
2. Use `mcp_nuxt-ui_get-example` to get specific implementation

## Common Scenarios

### "What form components are available?"
```
1. mcp_nuxt-ui_list-components
2. Filter by category: "Form"
3. Show: Button, Input, Textarea, Select, Checkbox, Radio, Toggle, Form, etc.
```

### "How do I use the Modal component?"
```
1. mcp_nuxt-ui_get-component with "Modal"
2. Show usage example with v-model
3. Explain programmatic usage with useModal()
```

### "What props does Button accept?"
```
1. mcp_nuxt-ui_get-component-metadata with "Button"
2. List all props: color, size, variant, icon, loading, disabled, etc.
3. Show TypeScript types
```

### "Show me table examples"
```
1. mcp_nuxt-ui_list-examples
2. Find Table examples
3. mcp_nuxt-ui_get-example with example name
```

## Component Categories

**Form Components:**
- Button, ButtonGroup
- Input, Textarea
- Select, SelectMenu
- Checkbox, Radio, Toggle
- Form, FormField

**Layout:**
- App (required wrapper)
- Card
- Container
- Divider

**Navigation:**
- Tabs, TabGroup
- Accordion
- Breadcrumb
- Pagination

**Overlays:**
- Modal
- Popover
- Dropdown
- Tooltip
- ContextMenu

**Data Display:**
- Table
- Avatar
- Badge, Chip
- Kbd
- Meter

**Feedback:**
- Alert
- Progress
- Skeleton
- Spinner
- Toast (programmatic)

## Example Usage

**User: "I need a data table with sorting"**
```
1. Get Table component: mcp_nuxt-ui_get-component("Table")
2. Show sortable example
3. Explain sort prop and @sort event
4. Provide implementation code
```

**User: "How do I customize Button colors?"**
```
1. Get Button metadata: mcp_nuxt-ui_get-component-metadata("Button")
2. Explain color prop (primary, secondary, success, etc.)
3. Show ui prop for advanced customization
4. Provide theming examples
```

**User: "Show me all navigation components"**
```
1. List components: mcp_nuxt-ui_list-components
2. Filter category: "Navigation"
3. Summarize: Tabs, Accordion, Breadcrumb, Pagination
4. Offer to get details on any specific component
```

## Tips

- Component names are PascalCase: "Button", "Modal", "FormField"
- All components have `color` and `size` props
- Use `ui` prop for granular customization
- Check metadata for slots and events
- Examples are practical implementation references
