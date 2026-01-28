---
name: nextjs-shadcn-builder
description: Build new Next.js applications or migrate existing frontends (React, Vue, Angular, vanilla JS, etc.) to Next.js + shadcn/ui with systematic analysis and conversion. Enforces shadcn design principles - CSS variables for theming, standard UI components, no hardcoded values, consistent typography/colors. Use for creating Next.js apps, migrating frontends, adopting shadcn/ui, or standardizing component libraries. Includes MCP integration for shadcn documentation and automated codebase analysis.
license: Complete terms in LICENSE.txt
---

# Next.js + shadcn/ui Builder & Migration Tool

Build production-grade Next.js applications or systematically migrate existing frontends to Next.js + shadcn/ui following strict design principles and best practices.

## Overview

This skill handles two primary workflows:

1. **Creating New Next.js Applications** - Initialize projects with Next.js 15+ (App Router), shadcn/ui, and proper design system setup
2. **Migrating Existing Frontends** - Analyze any frontend codebase (React, Vue, Angular, vanilla JS) and systematically convert to Next.js + shadcn/ui

**Core Philosophy**: 100% adherence to shadcn/ui design principles:
- CSS variables for all theming (colors, spacing, typography)
- Standard shadcn/ui components only (no custom UI components)
- No hardcoded values (colors, spacing, fonts)
- Consistent design tokens across the application
- Mobile-first responsive design for all devices (phone, tablet, desktop)
- WCAG 2.1 Level AA accessibility compliance
- Best practices from https://ui.shadcn.com

## Workflow Decision Tree

```
User Request
    ├─ Creating New Next.js App
    │   └─ Follow "Creating New Application" workflow (Phase 3 onwards)
    │
    └─ Migrating Existing Codebase
        ├─ Phase 1: Codebase Analysis
        ├─ Phase 2: Migration Planning
        ├─ Phase 3: Next.js + shadcn Setup
        ├─ Phase 4: Systematic Conversion
        └─ Phase 5: Verification & Cleanup
```

---

## High-Level Workflow for Migration

### Phase 1: Codebase Analysis
Automated analysis of existing frontend to understand scope and complexity.

**Steps:**
1. Framework and version detection
2. Component inventory and categorization
3. Hardcoded value detection (colors, spacing, custom components)
4. Styling approach analysis (CSS, SCSS, CSS-in-JS, Tailwind, etc.)
5. State management and routing pattern identification
6. Generate comprehensive analysis report

**Deliverables:**
- Framework analysis report
- Component inventory (JSON)
- Hardcoded values report
- Complexity assessment

### Phase 2: Migration Planning
Create systematic conversion plan with prioritized batches.

**Steps:**
1. Map existing components to shadcn/ui equivalents
2. Identify components requiring custom development
3. Organize conversion into batches (5-10 components per batch)
4. Assess risk and complexity per batch
5. Create detailed migration plan

**Deliverables:**
- Component mapping table
- Batched conversion plan
- Risk assessment
- Estimated complexity per component

### Phase 3: Next.js + shadcn Setup
Initialize Next.js infrastructure alongside or replacing existing codebase.

**Steps:**
1. Check/install shadcn MCP server for documentation access
2. Initialize Next.js 15+ with App Router and TypeScript
3. Install and configure Tailwind CSS
4. Run shadcn/ui initialization
5. Set up CSS variables and design tokens
6. Configure path aliases (@/)
7. Install essential shadcn components
8. Create design system documentation

**Deliverables:**
- Configured Next.js project
- Design token system (CSS variables)
- Component library setup
- Path aliases configured

### Phase 4: Systematic Conversion
Convert components batch by batch with testing after each batch.

**Steps:**
1. **Batch 1: Layout & Structure** (Header, Footer, Layout wrappers)
2. **Batch 2: Simple UI Components** (Buttons, Cards, Badges, Alerts)
3. **Batch 3: Form Components** (Inputs, Selects, Checkboxes, Forms)
4. **Batch 4: Complex Components** (Tables, Dialogs, Command Menus, Data visualizations)
5. **Batch 5: Styling Standardization** (Remove hardcoded values, apply CSS variables)
6. **Batch 6: Pages & Routes** (Convert pages, set up Next.js routing)

**Per Batch Workflow:**
1. Select 5-10 related components
2. Use MCP to find appropriate shadcn components
3. Convert components following shadcn patterns
4. Replace hardcoded values with CSS variables
5. Test functionality
6. Verify visual consistency
7. Move to next batch

**Deliverables:**
- Migrated components (batch by batch)
- Updated styling with CSS variables
- Next.js App Router pages
- Passing tests per batch

### Phase 5: Verification & Cleanup
Final testing, optimization, and old code removal.

**Steps:**
1. Run full test suite
2. Visual regression testing
3. Responsive design testing (mobile, tablet, desktop)
4. Performance audit
5. Accessibility audit (WCAG 2.1 Level AA compliance)
6. Remove old framework code
7. Documentation updates
8. Generate completion report

**Deliverables:**
- Test results
- Responsive design verification report
- Performance metrics
- Accessibility audit report (WCAG 2.1 AA)
- Clean codebase
- Migration summary

---

## Phase 1: Codebase Analysis (Detailed Instructions)

### 1.1 Framework Detection

Run the automated analysis script:

```bash
python ./scripts/analyze-codebase.py /path/to/existing/codebase
```

This script will:
- Detect framework (React, Vue, Angular, Svelte, vanilla JS, etc.)
- Identify framework version
- Detect build tool (Vite, Webpack, Parcel, etc.)
- Find package.json dependencies
- Map directory structure

**Output:** `codebase-analysis.json` with framework metadata

### 1.2 Component Inventory

The analysis script automatically generates a component inventory including:

- Component name and file path
- Component type (functional, class, Vue SFC, etc.)
- Props/inputs
- State usage
- Child components
- External dependencies

**Output:** `component-inventory.json`

Example structure:
```json
{
  "components": [
    {
      "name": "UserCard",
      "path": "src/components/UserCard.tsx",
      "type": "functional",
      "complexity": "simple",
      "shadcn_equivalent": "Card",
      "hardcoded_values": ["#3b82f6", "16px padding"],
      "dependencies": ["react", "styled-components"]
    }
  ]
}
```

### 1.3 Hardcoded Value Detection

Run the detection script:

```bash
bash ./scripts/detect-hardcoded-values.sh /path/to/existing/codebase
```

This script detects:
- **Hardcoded colors**: `#hex`, `rgb()`, `rgba()`, `hsl()`, color names
- **Inline spacing**: `margin: 20px`, `padding: 1rem`
- **Custom font declarations**: non-standard fonts
- **Magic numbers**: arbitrary values in components
- **Inline styles**: `style={{...}}`
- **Non-standard patterns**: CSS-in-JS, styled-components that should be Tailwind

**Output:** `hardcoded-values-report.md` with violations grouped by category

### 1.4 Generate Analysis Report

Run the report generator:

```bash
python ./scripts/generate-migration-report.py
```

This combines all analysis data into a comprehensive markdown report:

**Output:** `migration-analysis-report.md`

```markdown
# Frontend Migration Analysis Report

## Executive Summary
[One-paragraph overview: framework, size, complexity]

## Current State Analysis
- **Framework**: React 18.2.0
- **Build Tool**: Vite 4.3.0
- **Component Count**: 47 components
- **Styling**: styled-components + custom CSS
- **State Management**: Redux Toolkit
- **Routing**: React Router v6

## Hardcoded Values Detected
- Colors: 142 instances across 34 files
- Spacing: 89 instances across 28 files
- Custom fonts: 3 non-standard fonts
- Inline styles: 67 instances

## Component Categorization
- **Simple (shadcn mapping exists)**: 28 components
- **Moderate (requires adaptation)**: 13 components
- **Complex (custom development needed)**: 6 components

## Recommended Migration Plan
1. Phase 3: Setup Next.js + shadcn infrastructure
2. Phase 4.1: Convert layout components (Header, Footer, Layout)
3. Phase 4.2: Convert simple UI (Button, Card, Badge → shadcn equivalents)
4. Phase 4.3: Convert forms (Input, Select → shadcn/ui Form components)
5. Phase 4.4: Convert complex components (DataTable, Charts)
6. Phase 4.5: Styling standardization (CSS variables)
7. Phase 4.6: Pages and routing
8. Phase 5: Verification and cleanup

## Estimated Effort
- **Total Components**: 47
- **Batches**: 9-10 batches
- **Complexity**: Moderate
```

---

## Phase 2: Migration Planning (Detailed Instructions)

### 2.1 Component Mapping Strategy

Review the `component-inventory.json` and create a mapping table using the shadcn component reference.

**VERY IMPORTANT: Use MCP to discover shadcn components**

Before mapping, check if shadcn MCP server is available:

```bash
# Check if MCP server is available
# Try accessing https://ui.shadcn.com/docs/mcp
```

If MCP is not available, install it:

```bash
npx shadcn@latest mcp init --client claude
```

**Use MCP to query available components:**
- "What shadcn components are available for buttons?"
- "Show me form components in shadcn"
- "What's the shadcn equivalent of a modal/dialog?"
- "Available data display components in shadcn"

**Component Mapping Table Template:**

| Existing Component | shadcn Equivalent | Complexity | Priority | Notes |
|-------------------|-------------------|------------|----------|-------|
| CustomButton | Button | Low | 1 | Props mostly compatible |
| Modal | Dialog | Medium | 2 | Different API, uses Radix |
| DataTable | Table + DataTable | High | 3 | Requires custom hooks |
| Dropdown | DropdownMenu | Low | 1 | Direct mapping |
| DatePicker | Calendar + Popover | Medium | 2 | Composition pattern |

**Load framework-specific migration guide:**

- For React: Read `./references/react-to-nextjs.md`
- For Vue: Read `./references/vue-to-nextjs.md`
- For Angular: Read `./references/angular-to-nextjs.md`
- For styling: Read `./references/styling-migration.md`

### 2.2 Batch Organization

Organize components into batches following these principles:

**Batching Strategy:**
1. **Group by type** (layout, forms, data display, navigation)
2. **Simple to complex** (start with easy wins)
3. **Dependency order** (convert dependencies first)
4. **Batch size**: 5-10 components per batch

**Example Batch Plan:**

**Batch 1: Layout & Structure** (Priority: Critical)
- Header
- Footer
- MainLayout
- Container
- Sidebar

**Batch 2: Simple UI Components** (Priority: High)
- Button → shadcn Button
- Card → shadcn Card
- Badge → shadcn Badge
- Alert → shadcn Alert
- Avatar → shadcn Avatar

**Batch 3: Form Components** (Priority: High)
- Input → shadcn Input
- Select → shadcn Select
- Checkbox → shadcn Checkbox
- RadioGroup → shadcn RadioGroup
- Form validation → shadcn Form + react-hook-form

**Batch 4: Navigation** (Priority: Medium)
- NavBar → shadcn NavigationMenu
- Breadcrumbs → shadcn Breadcrumb
- Tabs → shadcn Tabs
- Pagination → shadcn Pagination

**Batch 5: Data Display** (Priority: Medium)
- Table → shadcn Table
- DataGrid → shadcn DataTable (with sorting, filtering)
- List → shadcn custom composition
- Accordion → shadcn Accordion

**Batch 6: Overlays & Modals** (Priority: Medium)
- Modal → shadcn Dialog
- Tooltip → shadcn Tooltip
- Popover → shadcn Popover
- DropdownMenu → shadcn DropdownMenu

**Batch 7: Complex Components** (Priority: Low)
- Charts → shadcn Charts (Recharts integration)
- Calendar/DatePicker → shadcn Calendar
- CommandPalette → shadcn Command
- DataVisualization → Custom with shadcn primitives

**Batch 8: Styling Standardization** (Priority: Critical)
- Extract all hardcoded colors → CSS variables
- Convert spacing to Tailwind classes
- Standardize typography
- Apply theme system consistently

**Batch 9: Pages & Routing** (Priority: Critical)
- Convert pages to Next.js App Router
- Set up layouts with Next.js layout.tsx
- Implement routing patterns
- Add loading and error states

### 2.3 Risk Assessment

For each batch, identify risks:

- **API Differences**: Components with significantly different APIs
- **Missing Features**: Features in old components not in shadcn
- **State Management**: Complex state that needs refactoring
- **Dependencies**: External libraries that need replacement
- **Custom Logic**: Business logic tightly coupled to UI

**Risk Mitigation:**
- Document API differences before conversion
- Create adapter/wrapper components when needed
- Write tests before migration
- Keep old components temporarily during transition

### 2.4 Create Detailed Migration Plan

Generate a detailed plan document: `migration-plan.md`

```markdown
# Next.js + shadcn Migration Plan

## Project: [Project Name]
## Date: [Current Date]
## Estimated Timeline: [X batches]

## Migration Strategy

### Approach
- Incremental migration with parallel running old and new code
- Batch-based conversion (5-10 components per batch)
- Test after each batch before proceeding
- Feature flag new components during transition

### Success Criteria
- All components use shadcn/ui or shadcn patterns
- Zero hardcoded colors/spacing (CSS variables only)
- 100% TypeScript coverage
- Passing test suite
- Lighthouse score >= 90
- No accessibility violations

## Detailed Batch Plan

[Include all batches from 2.2 with specific components listed]

## Timeline

Batch 1: Layout & Structure (Days 1-2)
Batch 2: Simple UI (Days 3-4)
[etc.]

## Notes and Considerations
[Any special requirements, blockers, or dependencies]
```

---

## Phase 3: Next.js + shadcn Setup (Detailed Instructions)

### 3.1 Check/Install shadcn MCP Server

**CRITICAL: Always use MCP for shadcn component discovery**

1. Check if MCP server is accessible:
   - Try to access documentation at `https://ui.shadcn.com/docs/mcp`
   - Check if you can query shadcn components via MCP

2. If not available, install MCP server:

```bash
npx shadcn@latest mcp init --client claude
```

This enables:
- Real-time shadcn documentation access
- Component discovery and search
- Block and chart template discovery
- Theme and design token reference

**Using MCP during development:**
- "What components are available for [use case]?"
- "Show me the props for shadcn Button"
- "Available chart types in shadcn"
- "How to use shadcn Form with validation"

### 3.2 Initialize Next.js Project

Run the initialization script:

```bash
bash ./scripts/init-nextjs-shadcn.sh [project-name]
```

**Or manually initialize:**

```bash
# Check Node.js version (18+ required)
node -v

# Create Next.js project with App Router
npx create-next-app@latest [project-name] \
  --typescript \
  --tailwind \
  --app \
  --src-dir \
  --import-alias "@/*" \
  --no-turbopack

cd [project-name]
```

### 3.3 Install and Configure shadcn/ui

```bash
# Initialize shadcn/ui
npx shadcn@latest init

# Configuration prompts:
# - TypeScript: Yes
# - Style: Default
# - Base color: Choose from slate/gray/zinc/neutral/stone
# - CSS variables: Yes (CRITICAL - required for theming)
# - Import alias: @/components
```

This creates:
- `components.json` config file
- `lib/utils.ts` with cn() helper
- Updated `tailwind.config.ts` with shadcn theme
- CSS variables in `app/globals.css`

### 3.4 Configure Design Tokens (CSS Variables)

**VERY IMPORTANT: All theming MUST use CSS variables**

**Color Format: OKLCH (Recommended)**

This skill uses **OKLCH** (OKLab Lightness Chroma Hue) color space instead of HSL for better perceptual uniformity and color accuracy.

**OKLCH Benefits:**
- Perceptually uniform (equal changes = equal perceived differences)
- Better gradient interpolation
- More predictable lightness
- Better for accessibility (more accurate contrast ratios)

Edit `app/globals.css` to define your design system:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --radius: 0.65rem;

    /* Background - Pure white */
    --background: 1 0 0;
    --foreground: 0.141 0.005 285.823;

    /* Card */
    --card: 1 0 0;
    --card-foreground: 0.141 0.005 285.823;

    /* Popover */
    --popover: 1 0 0;
    --popover-foreground: 0.141 0.005 285.823;

    /* Primary - Warm orange */
    --primary: 0.646 0.222 41.116;
    --primary-foreground: 0.98 0.016 73.684;

    /* Secondary - Light purple-gray */
    --secondary: 0.967 0.001 286.375;
    --secondary-foreground: 0.21 0.006 285.885;

    /* Muted - Subtle elements */
    --muted: 0.967 0.001 286.375;
    --muted-foreground: 0.552 0.016 285.938;

    /* Accent */
    --accent: 0.967 0.001 286.375;
    --accent-foreground: 0.21 0.006 285.885;

    /* Destructive - Red */
    --destructive: 0.577 0.245 27.325;

    /* Border and Input */
    --border: 0.92 0.004 286.32;
    --input: 0.92 0.004 286.32;

    /* Focus ring */
    --ring: 0.75 0.183 55.934;

    /* Chart colors */
    --chart-1: 0.837 0.128 66.29;
    --chart-2: 0.705 0.213 47.604;
    --chart-3: 0.646 0.222 41.116;
    --chart-4: 0.553 0.195 38.402;
    --chart-5: 0.47 0.157 37.304;
  }

  .dark {
    /* Dark mode backgrounds */
    --background: 0.141 0.005 285.823;
    --foreground: 0.985 0 0;

    /* Dark mode card */
    --card: 0.21 0.006 285.885;
    --card-foreground: 0.985 0 0;

    /* Dark mode popover */
    --popover: 0.21 0.006 285.885;
    --popover-foreground: 0.985 0 0;

    /* Dark mode primary - Brighter for contrast */
    --primary: 0.705 0.213 47.604;
    --primary-foreground: 0.98 0.016 73.684;

    /* Dark mode secondary */
    --secondary: 0.274 0.006 286.033;
    --secondary-foreground: 0.985 0 0;

    /* Dark mode muted */
    --muted: 0.274 0.006 286.033;
    --muted-foreground: 0.705 0.015 286.067;

    /* Dark mode accent */
    --accent: 0.274 0.006 286.033;
    --accent-foreground: 0.985 0 0;

    /* Dark mode destructive */
    --destructive: 0.704 0.191 22.216;

    /* Dark mode borders (with alpha) */
    --border: 1 0 0 / 10%;
    --input: 1 0 0 / 15%;

    /* Dark mode focus ring */
    --ring: 0.408 0.123 38.172;

    /* Chart colors (consistent) */
    --chart-1: 0.837 0.128 66.29;
    --chart-2: 0.705 0.213 47.604;
    --chart-3: 0.646 0.222 41.116;
    --chart-4: 0.553 0.195 38.402;
    --chart-5: 0.47 0.157 37.304;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
```

**Customizing for Migrated Project:**

If migrating an existing app with a design system, extract existing colors and map to CSS variables:

```bash
# Use the detection script to find existing colors
bash ./scripts/detect-hardcoded-values.sh /path/to/old/codebase

# Map old colors to new CSS variables (OKLCH format)
# Use https://oklch.com or https://colorjs.io to convert
# Example:
# Old: #FF6B35 (brand orange) → --primary: 0.646 0.222 41.116
# Old: #3B82F6 (blue) → --primary: 0.630 0.213 255.5
# Old: #10B981 (green) → --success: 0.710 0.180 165.4
```

### 3.5 Install Essential shadcn Components

**Use MCP to discover which components you need!**

Install core components:

```bash
# Layout & Structure
npx shadcn@latest add card
npx shadcn@latest add separator

# Forms
npx shadcn@latest add button
npx shadcn@latest add input
npx shadcn@latest add label
npx shadcn@latest add select
npx shadcn@latest add checkbox
npx shadcn@latest add radio-group
npx shadcn@latest add form

# Navigation
npx shadcn@latest add navigation-menu
npx shadcn@latest add tabs
npx shadcn@latest add breadcrumb

# Feedback
npx shadcn@latest add alert
npx shadcn@latest add toast
npx shadcn@latest add dialog
npx shadcn@latest add tooltip

# Data Display
npx shadcn@latest add table
npx shadcn@latest add badge
npx shadcn@latest add avatar

# Overlays
npx shadcn@latest add popover
npx shadcn@latest add dropdown-menu
npx shadcn@latest add sheet
```

**Query MCP for additional components as needed during development.**

### 3.6 Set Up Theme Provider (Dark Mode Support)

Install next-themes:

```bash
npm install next-themes
```

Create `components/theme-provider.tsx`:

```typescript
"use client"

import * as React from "react"
import { ThemeProvider as NextThemesProvider } from "next-themes"
import { type ThemeProviderProps } from "next-themes/dist/types"

export function ThemeProvider({ children, ...props }: ThemeProviderProps) {
  return <NextThemesProvider {...props}>{children}</NextThemesProvider>
}
```

Update `app/layout.tsx`:

```typescript
import { ThemeProvider } from "@/components/theme-provider"

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
```

### 3.7 Create Example Component

Create `components/example-card.tsx` demonstrating best practices:

```typescript
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

export function ExampleCard() {
  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>shadcn/ui Best Practices</CardTitle>
        <CardDescription>
          This card demonstrates proper shadcn patterns
        </CardDescription>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground">
          Notice: No hardcoded colors, using CSS variables via Tailwind classes,
          standard shadcn components, and proper typography scale.
        </p>
      </CardContent>
      <CardFooter className="flex justify-between">
        <Button variant="outline">Cancel</Button>
        <Button>Continue</Button>
      </CardFooter>
    </Card>
  )
}
```

**Key Patterns Demonstrated:**
- Uses standard shadcn components (Card, Button)
- No hardcoded colors (uses `text-muted-foreground`)
- CSS variables automatically applied via Tailwind
- Semantic variants (`outline`, default)
- Proper component composition

---

## Phase 4: Systematic Conversion (Detailed Instructions)

### 4.1 Component Conversion Workflow

For each batch of 5-10 components:

**Step 1: Review Components in Batch**

Load the component files and understand:
- Current functionality
- Props/API
- Styling approach
- State management
- Event handlers

**Step 2: Query MCP for shadcn Equivalents**

Before converting, use MCP:
- "What's the shadcn component for [component type]?"
- "Show me shadcn [component] props and examples"
- "How to use shadcn [component] with [feature]?"

**Step 3: Convert Component**

Follow this pattern:

```typescript
// OLD: Custom button with hardcoded styles
const CustomButton = ({ children, onClick, variant = 'primary' }) => {
  const styles = {
    primary: {
      backgroundColor: '#3b82f6', // HARDCODED!
      color: '#ffffff',
      padding: '8px 16px', // HARDCODED!
      borderRadius: '6px'
    },
    secondary: {
      backgroundColor: '#6b7280',
      color: '#ffffff',
      padding: '8px 16px',
      borderRadius: '6px'
    }
  }

  return (
    <button style={styles[variant]} onClick={onClick}>
      {children}
    </button>
  )
}

// NEW: shadcn Button with CSS variables
import { Button } from "@/components/ui/button"

const CustomButton = ({ children, onClick, variant = 'default' }) => {
  return (
    <Button variant={variant} onClick={onClick}>
      {children}
    </Button>
  )
}
```

**Conversion Checklist:**
- ✅ Replace with shadcn component
- ✅ Remove all hardcoded colors
- ✅ Remove inline styles
- ✅ Use Tailwind classes only
- ✅ Use semantic variants (default, outline, destructive, etc.)
- ✅ Preserve all functionality
- ✅ TypeScript types properly defined

**Step 4: Replace Hardcoded Values with CSS Variables**

```typescript
// OLD: Hardcoded spacing and colors
<div style={{
  backgroundColor: '#f3f4f6',  // WRONG
  padding: '20px',              // WRONG
  margin: '10px 0'              // WRONG
}}>

// NEW: Tailwind classes using CSS variables
<div className="bg-secondary p-5 my-2.5">

// Or for custom spacing:
<div className="bg-secondary" style={{ padding: 'var(--spacing-5)' }}>
```

**Step 5: Test Functionality**

After converting each component:

```bash
# Run tests
npm test

# Visual testing
npm run dev
# Manually verify component renders correctly
```

**Step 6: Verify No Violations**

Run detection script on new components:

```bash
bash ./scripts/detect-hardcoded-values.sh src/components/[batch-name]
```

Should return 0 violations.

**Step 7: Mark Batch Complete, Move to Next**

Update todo list and migration-plan.md with progress.

### 4.2 Common Component Migrations

**Refer to `./references/shadcn-component-mapping.md` for detailed mappings.**

Quick reference:

| Pattern | Old Approach | shadcn Approach |
|---------|-------------|-----------------|
| Button | Custom styled button | `<Button variant="...">` |
| Modal/Dialog | Custom overlay | `<Dialog>` with `<DialogTrigger>` and `<DialogContent>` |
| Form Input | Custom input with validation | `<Form>` + `<FormField>` + react-hook-form |
| Dropdown | Custom select | `<Select>` or `<DropdownMenu>` |
| Table | Custom table | `<Table>` or DataTable pattern |
| Tooltip | Custom hover component | `<Tooltip>` |
| Toast/Notification | Custom notification | `useToast()` hook + `<Toaster>` |
| Tabs | Custom tab component | `<Tabs>` with `<TabsList>` and `<TabsContent>` |
| Card | Custom card | `<Card>` with subcomponents |
| Badge | Custom badge/pill | `<Badge variant="...">` |

### 4.3 Handling Complex Components

For components without direct shadcn equivalents:

**Option 1: Composition**

Build using shadcn primitives:

```typescript
// Complex dashboard widget using shadcn primitives
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"

export function DashboardWidget({ title, data, onRefresh }) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>{title}</CardTitle>
        <Button variant="outline" size="sm" onClick={onRefresh}>
          Refresh
        </Button>
      </CardHeader>
      <CardContent>
        {data.map(item => (
          <div key={item.id} className="flex items-center justify-between py-2">
            <span className="text-sm">{item.label}</span>
            <Badge variant={item.status === 'success' ? 'default' : 'destructive'}>
              {item.value}
            </Badge>
          </div>
        ))}
      </CardContent>
    </Card>
  )
}
```

**Option 2: Extend shadcn Components**

Create custom components that extend shadcn:

```typescript
// Custom component extending shadcn Button
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

interface IconButtonProps extends React.ComponentProps<typeof Button> {
  icon: React.ReactNode
}

export function IconButton({ icon, children, className, ...props }: IconButtonProps) {
  return (
    <Button className={cn("flex items-center gap-2", className)} {...props}>
      {icon}
      {children}
    </Button>
  )
}
```

**Option 3: Use shadcn Blocks**

Use MCP to discover shadcn blocks (pre-built complex components):

"What blocks are available in shadcn for [use case]?"

Install blocks:

```bash
npx shadcn@latest add [block-name]
```

### 4.4 Page and Route Conversion

Convert pages to Next.js App Router structure:

**Old Structure (React Router):**
```
src/
  pages/
    Home.tsx
    About.tsx
    Dashboard.tsx
    users/
      UserList.tsx
      UserDetail.tsx
```

**New Structure (Next.js App Router):**
```
app/
  page.tsx          # Home
  about/
    page.tsx        # About
  dashboard/
    page.tsx        # Dashboard
    layout.tsx      # Dashboard layout
  users/
    page.tsx        # UserList
    [id]/
      page.tsx      # UserDetail
  layout.tsx        # Root layout
  loading.tsx       # Loading state
  error.tsx         # Error boundary
```

**Example Conversion:**

```typescript
// OLD: React Router page
// src/pages/Dashboard.tsx
import { useNavigate } from 'react-router-dom'

export function Dashboard() {
  const navigate = useNavigate()
  return (
    <div style={{ padding: '20px' }}>
      <h1>Dashboard</h1>
      <button onClick={() => navigate('/users')}>
        View Users
      </button>
    </div>
  )
}

// NEW: Next.js App Router page
// app/dashboard/page.tsx
import Link from 'next/link'
import { Button } from '@/components/ui/button'

export default function DashboardPage() {
  return (
    <div className="container py-6">
      <h1 className="text-3xl font-bold mb-6">Dashboard</h1>
      <Link href="/users">
        <Button>View Users</Button>
      </Link>
    </div>
  )
}
```

**Key Changes:**
- Default export for pages
- Use Next.js `<Link>` instead of router navigation
- Remove hardcoded padding → Tailwind classes
- Use shadcn Button

### 4.5 State Management Migration

**Load reference:** `./references/react-to-nextjs.md` for state management patterns

Common patterns:

**Local State (useState):**
- Remains the same in Next.js App Router
- Mark client components with `"use client"`

**Global State:**
- **Redux → Zustand or React Context**
- **MobX → Zustand**
- **Recoil → Zustand or Jotai**

**Server State:**
- **React Query → TanStack Query (still works in Next.js)**
- **SWR → SWR (Next.js compatible)**
- Or use Next.js Server Components for server data

---

## Phase 5: Verification & Cleanup (Detailed Instructions)

### 5.1 Run Test Suite

```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Ensure 100% of migrated components have passing tests
```

### 5.2 Visual Regression Testing

Manual verification checklist:

- [ ] All pages render correctly
- [ ] All components match design system
- [ ] Dark mode works correctly
- [ ] Responsive design maintained
- [ ] No hardcoded colors visible
- [ ] Consistent spacing throughout
- [ ] Typography follows design system

Optional: Set up automated visual regression testing with Percy, Chromatic, or Playwright.

### 5.3 Responsive Design Testing

**Critical: Test on real devices, not just browser DevTools**

**Refer to:** `./references/responsive-design-patterns.md` for comprehensive responsive testing guidelines.

**Device Testing Checklist:**
- [ ] iPhone SE (320px - smallest modern viewport)
- [ ] iPhone 14 Pro (390px)
- [ ] iPad (768px)
- [ ] iPad Pro (1024px)
- [ ] Desktop (1280px - 1920px)
- [ ] Ultrawide (2560px+)

**Orientation Testing:**
- [ ] Portrait mode on mobile/tablet
- [ ] Landscape mode on mobile/tablet
- [ ] Responsive behavior when rotating device

**Responsive Patterns Verification:**
- [ ] Navigation: Mobile hamburger → tablet sidebar → desktop navbar
- [ ] Data tables: Mobile cards → tablet scrollable → desktop full table
- [ ] Grids: 1 col mobile → 2 cols tablet → 3-4 cols desktop
- [ ] Forms: Single column mobile → multi-column desktop
- [ ] Touch targets: Minimum 44x44px on mobile
- [ ] Typography: Readable at all screen sizes (minimum 16px body text)
- [ ] Images: Responsive sizing with proper aspect ratios

**Breakpoint Verification:**
```bash
# Test all Tailwind breakpoints
# sm: 640px, md: 768px, lg: 1024px, xl: 1280px, 2xl: 1536px

# Verify components respond correctly at each breakpoint
```

**Example Components:**
Review `./assets/component-templates/` for responsive design examples:
- `responsive-navigation.tsx` - Mobile/tablet/desktop navigation patterns
- `responsive-data-table.tsx` - Responsive table with mobile cards
- `responsive-dashboard.tsx` - Responsive grid layouts
- `complex-form.tsx` - Multi-step responsive form

### 5.4 Run Final Hardcoded Values Check

```bash
bash ./scripts/detect-hardcoded-values.sh src/
```

**Expected result:** 0 violations

If violations found, return to Phase 4 and fix.

### 5.5 Accessibility Audit (WCAG 2.1 Level AA)

**Critical: Achieve WCAG 2.1 Level AA compliance**

**Refer to:** `./references/accessibility-best-practices.md` for comprehensive accessibility testing guidelines.

```bash
# Install axe DevTools or use Lighthouse
npm install -D @axe-core/playwright

# Run accessibility tests
npm run test:a11y
```

shadcn/ui components are built with accessibility in mind (using Radix UI primitives), but verify:

**Automated Testing:**
- [ ] Run axe DevTools browser extension on all pages
- [ ] Lighthouse accessibility score >= 90
- [ ] No WCAG violations reported by automated tools
- [ ] eslint-plugin-jsx-a11y passing (if configured)

**Keyboard Navigation (WCAG 2.1.1, 2.1.2):**
- [ ] All interactive elements accessible via Tab
- [ ] Logical tab order (follows visual layout)
- [ ] No keyboard traps (can Tab out of all components)
- [ ] Enter/Space activates buttons/links
- [ ] Escape closes modals/dialogs
- [ ] Arrow keys navigate within components (tabs, menus, radio groups)
- [ ] Focus indicators visible on all interactive elements

**Screen Reader Testing:**
Test with real screen readers:
- **macOS**: VoiceOver (Cmd + F5)
- **Windows**: NVDA (free) or JAWS
- **Mobile**: VoiceOver (iOS) or TalkBack (Android)

**Screen Reader Checklist (WCAG 1.3.1, 4.1.2):**
- [ ] All images have alt text
- [ ] Form inputs have associated labels
- [ ] Buttons have descriptive text or aria-label
- [ ] Headings follow logical hierarchy (h1 → h2 → h3)
- [ ] Landmarks present (header, nav, main, aside, footer)
- [ ] Dynamic content announces via aria-live regions
- [ ] Error messages announced to screen readers

**Color Contrast (WCAG 1.4.3):**
- [ ] Body text: Minimum 4.5:1 contrast ratio
- [ ] Large text (18pt+): Minimum 3:1 contrast ratio
- [ ] UI components: Minimum 3:1 contrast ratio
- [ ] Focus indicators: Minimum 3:1 contrast ratio
- [ ] Test both light and dark modes

**Forms Accessibility (WCAG 3.3.1, 3.3.2):**
- [ ] All inputs have visible labels
- [ ] Required fields clearly indicated
- [ ] Error messages specific and helpful
- [ ] Error messages associated with inputs (aria-describedby)
- [ ] Form validation doesn't rely on color alone

**Touch Targets (WCAG 2.5.5):**
- [ ] Minimum 44x44 CSS pixels for all touch targets on mobile
- [ ] Adequate spacing between touch targets (8px minimum)

**ARIA Usage (WCAG 4.1.2):**
- [ ] ARIA labels for icon-only buttons
- [ ] aria-expanded for collapsible sections
- [ ] aria-selected for tabs
- [ ] aria-hidden for decorative elements
- [ ] role="alert" for error messages
- [ ] role="status" for non-critical updates

**Complete WCAG 2.1 AA Checklist:**
See `./references/accessibility-best-practices.md` for full WCAG 2.1 Level AA checklist.

### 5.6 Performance Audit

```bash
# Build for production
npm run build

# Analyze bundle
npm run analyze  # If you have bundle analyzer configured
```

Run Lighthouse audit:
- Performance >= 90
- Accessibility >= 90
- Best Practices >= 90
- SEO >= 90

**Performance Checklist:**
- [ ] Core Web Vitals meet "Good" thresholds
  - LCP (Largest Contentful Paint) < 2.5s
  - FID (First Input Delay) < 100ms
  - CLS (Cumulative Layout Shift) < 0.1
- [ ] Images optimized (using Next.js Image component)
- [ ] Code splitting implemented for large components
- [ ] Lazy loading below-the-fold content
- [ ] Bundle size reasonable (check with bundle analyzer)

### 5.7 Remove Old Code

Once migration is verified:

```bash
# Remove old framework code
rm -rf src/old-components/  # or whatever old structure was

# Remove old dependencies
npm uninstall [old-framework] [old-ui-library] styled-components emotion ...

# Clean up old config files
rm -f .babelrc webpack.config.js  # etc.
```

### 5.8 Generate Completion Report

Create `migration-complete-report.md`:

```markdown
# Migration Completion Report

## Summary
Successfully migrated [Project Name] from [Old Framework] to Next.js + shadcn/ui.

## Statistics
- **Components Migrated**: 47
- **Lines of Code Changed**: ~5,200
- **Hardcoded Values Removed**: 231
- **CSS Variables Added**: 48
- **shadcn Components Used**: 18

## Test Results
- **Unit Tests**: 142/142 passing
- **Integration Tests**: 23/23 passing
- **Accessibility Score**: 98/100
- **Lighthouse Performance**: 94/100

## Before/After Comparison

### Before
- Framework: React 18 + Vite
- Styling: styled-components + custom CSS
- Hardcoded values: 231 violations
- Bundle size: 523 KB
- Lighthouse: 76

### After
- Framework: Next.js 15 + App Router
- Styling: Tailwind CSS + shadcn/ui
- Hardcoded values: 0 violations
- Bundle size: 398 KB (24% reduction)
- Lighthouse: 94 (23% improvement)

## Design System
All components now use CSS variables defined in globals.css:
- 24 color tokens
- 12 spacing tokens
- 8 typography tokens
- Full dark mode support

## Next Steps
- Deploy to production
- Monitor performance metrics
- Gather user feedback
- Optional: Implement additional shadcn blocks
```

---

## shadcn Design Principles (CRITICAL)

### Core Principles

**1. CSS Variables for All Theming**
- NEVER hardcode colors, spacing, or typography
- Define all design tokens as CSS variables in `globals.css`
- Use Tailwind classes that reference these variables

**2. Standard Components Only**
- Use shadcn/ui components as-is
- Extend via composition, not modification
- If shadcn doesn't have it, build with shadcn primitives

**3. Consistent Design Language**
- Follow shadcn's design patterns
- Use semantic variants (default, outline, destructive, ghost, link, secondary)
- Maintain consistent spacing scale
- Typography hierarchy from shadcn

**4. No Custom UI Components**
- Don't create custom buttons, inputs, cards, etc.
- Use shadcn components or build with shadcn primitives
- Exception: Business logic components (not UI primitives)

**5. Accessibility First**
- shadcn uses Radix UI (accessible by default)
- Don't override accessibility features
- Test with keyboard navigation and screen readers

### Anti-Patterns to Avoid

**NEVER DO THESE:**

❌ **Hardcoded Colors**
```typescript
// WRONG
<div style={{ backgroundColor: '#3b82f6' }}>

// RIGHT
<div className="bg-primary">
```

❌ **Hardcoded Spacing**
```typescript
// WRONG
<div style={{ padding: '20px', margin: '10px' }}>

// RIGHT
<div className="p-5 m-2.5">
```

❌ **Custom Styled Components for UI Primitives**
```typescript
// WRONG
const CustomButton = styled.button`
  background: #3b82f6;
  padding: 8px 16px;
  border-radius: 6px;
`

// RIGHT
import { Button } from '@/components/ui/button'
```

❌ **Inline Styles**
```typescript
// WRONG
<div style={{ color: 'red', fontSize: '14px' }}>

// RIGHT
<div className="text-destructive text-sm">
```

❌ **Hardcoded Fonts**
```typescript
// WRONG
<h1 style={{ fontFamily: 'Montserrat' }}>

// RIGHT
<h1 className="font-sans text-4xl font-bold">
```

❌ **Emoji Icons** (use Lucide React icons instead)
```typescript
// WRONG
<span>❌ Delete</span>

// RIGHT
import { X } from 'lucide-react'
<Button variant="destructive">
  <X className="mr-2 h-4 w-4" />
  Delete
</Button>
```

❌ **Arbitrary CSS Values**
```typescript
// WRONG
<div className="text-[#ff0000]">

// RIGHT
<div className="text-destructive">
```

### Best Practices

✅ **Use Semantic Color Names**
```typescript
// Use semantic CSS variable names
bg-background
text-foreground
bg-primary
text-primary-foreground
bg-secondary
text-muted-foreground
border-border
```

✅ **Use Tailwind Spacing Scale**
```typescript
// Consistent spacing using Tailwind
p-2, p-4, p-6, p-8  // padding
m-2, m-4, m-6, m-8  // margin
gap-2, gap-4        // flex/grid gap
```

✅ **Compose Components**
```typescript
// Build complex UIs by composing shadcn components
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
```

✅ **Use MCP for Discovery**
```typescript
// Before building, ask MCP:
// "What shadcn component should I use for [use case]?"
// "Show me examples of shadcn [component]"
```

✅ **Extend via Composition**
```typescript
// Create higher-level components that compose shadcn
export function FeatureCard({ feature }: { feature: Feature }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{feature.title}</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-muted-foreground">{feature.description}</p>
        <Button className="mt-4">Learn More</Button>
      </CardContent>
    </Card>
  )
}
```

---

## Reference Files

**Framework-Specific Migration:**
- [React to Next.js Migration](./references/react-to-nextjs.md)
- [Vue to Next.js Migration](./references/vue-to-nextjs.md)
- [Angular to Next.js Migration](./references/angular-to-nextjs.md)

**Component & Styling:**
- [shadcn Component Mapping Reference](./references/shadcn-component-mapping.md)
- [Advanced shadcn Components Guide](./references/advanced-shadcn-components.md) ⭐ NEW
- [Styling Migration Guide](./references/styling-migration.md)

**Responsive Design & Accessibility:**
- [Responsive Design Patterns Guide](./references/responsive-design-patterns.md) ⭐ NEW
- [Accessibility Best Practices (WCAG 2.1)](./references/accessibility-best-practices.md) ⭐ NEW

**Example Component Templates:**
- [Responsive Navigation](./assets/component-templates/responsive-navigation.tsx) - Mobile/tablet/desktop navigation patterns ⭐ NEW
- [Responsive Data Table](./assets/component-templates/responsive-data-table.tsx) - Card view on mobile, table on desktop ⭐ NEW
- [Responsive Dashboard](./assets/component-templates/responsive-dashboard.tsx) - Responsive grid layouts with stats and charts ⭐ NEW
- [Complex Multi-Step Form](./assets/component-templates/complex-form.tsx) - Form validation, file uploads, conditional fields ⭐ NEW
- [Feature Card Example](./assets/component-templates/example-feature-card.tsx) - Basic shadcn component composition
- [User Profile Example](./assets/component-templates/example-user-profile.tsx) - Avatar, badges, and layout patterns

**Scripts:**
- `./scripts/analyze-codebase.py` - Automated codebase analysis
- `./scripts/detect-hardcoded-values.sh` - Find anti-patterns
- `./scripts/init-nextjs-shadcn.sh` - Project initialization
- `./scripts/generate-migration-report.py` - Create migration report

**Official Documentation:**
- shadcn/ui: https://ui.shadcn.com
- Next.js: https://nextjs.org/docs
- Tailwind CSS: https://tailwindcss.com/docs
- Radix UI: https://www.radix-ui.com
- WCAG 2.1 Guidelines: https://www.w3.org/WAI/WCAG21/quickref/

---

## Quick Start for New Projects

If creating a new Next.js app (not migrating):

1. **Initialize**
   ```bash
   bash ./scripts/init-nextjs-shadcn.sh my-app
   ```

2. **Check MCP Access**
   ```bash
   npx shadcn@latest mcp init --client claude
   ```

3. **Install Components**
   - Use MCP to discover needed components
   - Install with `npx shadcn@latest add [component]`

4. **Build with Best Practices**
   - Use CSS variables only
   - Compose shadcn components
   - Follow design principles above

---

## Summary

This skill enables systematic frontend migration to Next.js + shadcn/ui with strict adherence to design principles:

- **Automated analysis** of existing codebases
- **Systematic batch conversion** (5-10 components at a time)
- **Zero tolerance for hardcoded values** (CSS variables only)
- **MCP integration** for shadcn component discovery
- **Multi-framework support** (React, Vue, Angular, vanilla JS)
- **Comprehensive verification** (tests, accessibility, performance)

**Result:** Production-grade Next.js applications following shadcn/ui best practices with consistent design systems, full dark mode support, and no anti-patterns.
