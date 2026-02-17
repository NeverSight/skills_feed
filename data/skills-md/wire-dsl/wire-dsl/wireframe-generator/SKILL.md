---
name: wireframe-generator
description: Generate Wire DSL code for wireframes and UI prototypes
---

# Wire DSL Code Generator

Generate syntactically correct Wire DSL code for creating wireframes and UI prototypes. Wire DSL is a block-declarative language similar to Mermaid, but specifically designed for UI wireframing.

## What This Skill Does

This skill enables LLMs to generate valid Wire DSL code by providing:
- Complete syntax reference and grammar rules
- Catalog of all 21 available components
- Layout container patterns (Stack, Grid, Split, Panel, Card)
- Best practices for code generation
- Common UI patterns and examples

## When to Use This Skill

Use this skill when you need to:
- Generate `.wire` files for wireframe prototypes
- Create UI mockups using declarative syntax
- Build multi-screen application wireframes
- Design forms, dashboards, product catalogs, or admin interfaces
- Convert UI requirements into Wire DSL code

## Core Concepts

**Structure:** Every Wire DSL file follows this hierarchy:
```
project → theme → screen → layout → components
```

**Syntax Style:** Block-declarative with curly braces, similar to CSS/HCL:
```wire
project "App Name" {
  theme { ... }
  screen ScreenName {
    layout <type> { ... }
  }
}
```

**Key Rules:**
- String values MUST be quoted: `text: "Hello"`
- Numbers, booleans, enums are NOT quoted: `height: 200`, `checked: true`, `variant: primary`
- Property format: `key: value`
- Comments: `//` for line, `/* */` for block

## Instructions for Code Generation

### Step 1: Start with Project Structure

Always begin with the project wrapper and theme configuration:

```wire
project "Project Name" {
  theme {
    density: "normal"
    spacing: "md"
    radius: "md"
    stroke: "normal"
    font: "base"
  }

  // screens go here
}
```

### Step 2: Create Screens

Each screen represents a unique view in the application:

```wire
screen ScreenName {
  layout <type> {
    // content
  }
}
```

**Naming:** Use CamelCase for screen names (e.g., `UsersList`, `ProductDetail`, `Dashboard`)

### Step 3: Choose Layout Container

Select the appropriate layout based on the UI structure:

| Layout | Use Case | Children | Example |
|--------|----------|----------|---------|
| **stack** | Linear arrangement | Multiple | Forms, lists, vertical/horizontal sections |
| **grid** | Multi-column (12-col) | cells | Dashboards, product grids, responsive layouts |
| **split** | Sidebar + main area | Exactly 2 | Admin panels, navigation + content |
| **panel** | Bordered container | Exactly 1 | Highlighted sections, form groups |
| **card** | Content cards | Multiple | Product cards, user profiles, info boxes |

### Step 4: Add Components

Choose from 21 available components organized in categories:

**Text:** Heading, Text, Label
**Input:** Input, Textarea, Select, Checkbox, Radio, Toggle
**Buttons:** Button, IconButton
**Navigation:** Topbar, SidebarMenu, Breadcrumbs, Tabs
**Data:** Table, List
**Media:** Image, Icon
**Display:** Divider, Badge, Link, Alert
**Info:** StatCard, Code, ChartPlaceholder
**Modal:** Modal, Spinner

### Step 5: Validate Syntax

Before outputting, check:
- ✅ All strings are quoted
- ✅ Numbers/booleans/enums are NOT quoted
- ✅ All braces are closed
- ✅ Required properties are present
- ✅ Component names match exactly (case-sensitive)
- ✅ Split has 2 children, Panel has 1 child
- ✅ Grid cells have valid `span` values (1-12)

## Reference Files

| File | Purpose |
|------|---------|
| [core-syntax.md](references/core-syntax.md) | Complete syntax rules, property formats, naming conventions |
| [components-catalog.md](references/components-catalog.md) | All 21 components with properties and examples |
| [layouts-guide.md](references/layouts-guide.md) | Layout containers (Stack, Grid, Split, Panel, Card) with patterns |
| [best-practices.md](references/best-practices.md) | Validation checklist, common mistakes, gotchas |
| [common-patterns.md](references/common-patterns.md) | Reusable patterns for forms, dashboards, navigation, cards |

## Examples

### Example 1: Simple Login Form

```wire
project "Login App" {
  theme {
    density: "normal"
    spacing: "md"
    radius: "md"
    stroke: "normal"
    font: "base"
  }

  screen Login {
    layout stack(direction: vertical, gap: lg, padding: xl) {
      component Heading text: "Sign In"
      component Input label: "Email" placeholder: "your@email.com"
      component Input label: "Password" placeholder: "Enter password"
      component Checkbox label: "Remember me" checked: false
      component Button text: "Sign In" variant: primary
      component Link text: "Forgot password?"
    }
  }
}
```

### Example 2: Dashboard with Sidebar

```wire
project "Admin Dashboard" {
  theme {
    density: "normal"
    spacing: "md"
    radius: "md"
    stroke: "normal"
    font: "base"
  }

  screen Dashboard {
    layout split(sidebar: 260, gap: md) {
      layout stack(direction: vertical, gap: md, padding: md) {
        component Heading text: "Menu"
        component SidebarMenu items: "Dashboard,Users,Settings,Analytics" active: 0
      }

      layout stack(direction: vertical, gap: lg, padding: lg) {
        component Heading text: "Dashboard Overview"

        layout grid(columns: 12, gap: md) {
          cell span: 3 {
            component StatCard title: "Total Users" value: "2,543"
          }
          cell span: 3 {
            component StatCard title: "Revenue" value: "$45,230"
          }
          cell span: 3 {
            component StatCard title: "Growth" value: "+12.5%"
          }
          cell span: 3 {
            component StatCard title: "Active Now" value: "892"
          }
        }

        component ChartPlaceholder type: "line" height: 300
        component Table columns: "User,Email,Status,Role" rows: 8
      }
    }
  }
}
```

### Example 3: Product Grid (E-Commerce)

```wire
project "Product Catalog" {
  theme {
    density: "comfortable"
    spacing: "lg"
    radius: "lg"
    stroke: "thin"
    font: "base"
  }

  screen Products {
    layout stack(direction: vertical, gap: xl, padding: xl) {
      layout grid(columns: 12, gap: md) {
        cell span: 8 {
          component Heading text: "Featured Products"
        }
        cell span: 4 align: end {
          component Button text: "View All" variant: primary
        }
      }

      layout grid(columns: 12, gap: lg) {
        cell span: 4 {
          layout card(padding: md, gap: md, radius: lg, border: true) {
            component Image placeholder: "square" height: 220
            component Heading text: "Wireless Headphones"
            component Text content: "Premium sound quality"
            component Badge text: "New" variant: primary
            layout stack(direction: horizontal, gap: sm) {
              component Text content: "$129.99"
              component Button text: "Add to Cart" variant: primary
            }
          }
        }

        cell span: 4 {
          layout card(padding: md, gap: md, radius: lg, border: true) {
            component Image placeholder: "square" height: 220
            component Heading text: "Smart Watch"
            component Text content: "Track your fitness"
            component Badge text: "Sale" variant: success
            layout stack(direction: horizontal, gap: sm) {
              component Text content: "$199.99"
              component Button text: "Add to Cart" variant: primary
            }
          }
        }

        cell span: 4 {
          layout card(padding: md, gap: md, radius: lg, border: true) {
            component Image placeholder: "square" height: 220
            component Heading text: "Laptop Stand"
            component Text content: "Ergonomic design"
            component Badge text: "Popular" variant: info
            layout stack(direction: horizontal, gap: sm) {
              component Text content: "$49.99"
              component Button text: "Add to Cart" variant: primary
            }
          }
        }
      }
    }
  }
}
```

## Quick Tips

**Spacing:** Use `gap` and `padding` with tokens: `xs`, `sm`, `md`, `lg`, `xl`
**Padding Default:** Layouts have 0px padding by default - always specify when needed
**Grid System:** 12-column grid, cells can span 1-12 columns
**Icons:** Use Feather Icons names: `search`, `settings`, `menu`, `user`, `star`, `heart`, etc.
**CSV Lists:** Comma-separated strings for items: `items: "Home,About,Contact"`
**Variants:** Components support: `primary`, `secondary`, `ghost`, `success`, `warning`, `error`, `info`

## Common Mistakes to Avoid

❌ Forgetting quotes on strings: `text: Hello` → ✅ `text: "Hello"`
❌ Adding quotes to numbers: `height: "200"` → ✅ `height: 200`
❌ Wrong component case: `button` → ✅ `Button`
❌ Using kebab-case for screens: `user-list` → ✅ `UserList`
❌ Forgetting padding: Layouts default to 0px, not theme spacing
❌ Split with 3 children → Must have exactly 2
❌ Panel with multiple children → Must have exactly 1
❌ Invalid grid span: `span: 15` → Must be 1-12

## Output Guidelines

When generating Wire DSL code:

1. **Always validate syntax** before outputting
2. **Include complete, runnable examples** - not partial snippets
3. **Use realistic content** - "John Doe", "john@example.com", actual values
4. **Follow naming conventions** - CamelCase screens, exact component names
5. **Add proper spacing** - Use `gap` and `padding` appropriately
6. **Structure logically** - Group related components, nest layouts properly
7. **Comment when helpful** - Explain complex structures with `//` comments

## Getting Help

For more details, see the reference files in the `references/` folder or consult:
- Project docs: `/home/user/wire-dsl/docs/`
- User docs: `/home/user/wire-dsl/apps/docs/`
- Examples: `/home/user/wire-dsl/examples/`
