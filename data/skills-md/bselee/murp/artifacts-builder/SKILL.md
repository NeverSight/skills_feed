---
name: artifacts-builder
description: Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui). Use for complex artifacts requiring state management, routing, or shadcn/ui components - not for simple single-file HTML/JSX artifacts.
allowed-tools: Bash, Read, Write, Edit, Glob
license: Complete terms in LICENSE.txt
---

# Artifacts Builder

To build powerful frontend claude.ai artifacts, follow these steps:
1. Initialize the frontend repo using `scripts/init-artifact.sh`
2. Develop your artifact by editing the generated code
3. Bundle all code into a single HTML file using `scripts/bundle-artifact.sh`
4. Display artifact to user
5. (Optional) Test the artifact

**Stack**: React 18 + TypeScript + Vite + Parcel (bundling) + Tailwind CSS + shadcn/ui

## Design & Style Guidelines

VERY IMPORTANT: To avoid what is often referred to as "AI slop", avoid using excessive centered layouts, purple gradients, uniform rounded corners, and Inter font.

## Quick Start

### Step 1: Initialize Project

Run the initialization script to create a new React project:
```bash
bash .claude/skills/artifacts-builder/scripts/init-artifact.sh <project-name>
cd <project-name>
```

This creates a fully configured project with:
- React + TypeScript (via Vite)
- Tailwind CSS 3.4.1 with shadcn/ui theming system
- Path aliases (`@/`) configured
- 40+ shadcn/ui components pre-installed
- All Radix UI dependencies included
- Parcel configured for bundling (via .parcelrc)
- Node 18+ compatibility (auto-detects and pins Vite version)

### Step 2: Develop Your Artifact

To build the artifact, edit the generated files. See **Common Development Tasks** below for guidance.

### Step 3: Bundle to Single HTML File

To bundle the React app into a single HTML artifact:
```bash
bash .claude/skills/artifacts-builder/scripts/bundle-artifact.sh
```

This creates `bundle.html` - a self-contained artifact with all JavaScript, CSS, and dependencies inlined. This file can be directly shared in Claude conversations as an artifact.

**Requirements**: Your project must have an `index.html` in the root directory.

**What the script does**:
- Installs bundling dependencies (parcel, @parcel/config-default, parcel-resolver-tspaths, html-inline)
- Creates `.parcelrc` config with path alias support
- Builds with Parcel (no source maps)
- Inlines all assets into single HTML using html-inline

### Step 4: Share Artifact with User

Finally, share the bundled HTML file in conversation with the user so they can view it as an artifact.

### Step 5: Testing/Visualizing the Artifact (Optional)

Note: This is a completely optional step. Only perform if necessary or requested.

To test/visualize the artifact, use available tools (including other Skills or built-in tools like Playwright or Puppeteer). In general, avoid testing the artifact upfront as it adds latency between the request and when the finished artifact can be seen. Test later, after presenting the artifact, if requested or if issues arise.

## Common Development Tasks

### Adding a New Component

Create components in `src/components/`:
```tsx
// src/components/MyComponent.tsx
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export function MyComponent() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>My Component</CardTitle>
      </CardHeader>
      <CardContent>
        <Button>Click me</Button>
      </CardContent>
    </Card>
  )
}
```

### Using shadcn/ui Components

All 40+ shadcn/ui components are pre-installed. Import from `@/components/ui/`:

```tsx
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
```

### State Management

Use React hooks for state:

```tsx
import { useState, useEffect } from 'react'

function MyComponent() {
  const [data, setData] = useState<string[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Fetch data or perform side effects
  }, [])

  return <div>{/* render */}</div>
}
```

### Styling with Tailwind CSS

Use Tailwind utility classes directly:

```tsx
<div className="flex flex-col gap-4 p-6 bg-slate-50 dark:bg-slate-900">
  <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
    Title
  </h1>
  <p className="text-slate-600 dark:text-slate-400">
    Description text
  </p>
</div>
```

## Project Structure

After initialization, your project structure:

```
<project-name>/
├── index.html          # Entry point
├── src/
│   ├── main.tsx        # React entry
│   ├── App.tsx         # Main component
│   ├── index.css       # Tailwind imports + shadcn theme
│   ├── lib/
│   │   └── utils.ts    # cn() utility for class merging
│   └── components/
│       └── ui/         # shadcn/ui components (40+)
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── postcss.config.js
└── vite.config.ts
```

## Available shadcn/ui Components

Pre-installed components (import from `@/components/ui/<name>`):

- **Layout**: card, separator, scroll-area, resizable
- **Forms**: button, input, textarea, select, checkbox, radio-group, switch, slider, form, label
- **Data Display**: table, avatar, badge, progress
- **Feedback**: alert, alert-dialog, toast, sonner
- **Overlay**: dialog, drawer, popover, tooltip, hover-card, sheet
- **Navigation**: tabs, navigation-menu, menubar, dropdown-menu, context-menu, command, breadcrumb
- **Data Input**: calendar, date-picker, combobox, toggle, toggle-group
- **Misc**: accordion, collapsible, aspect-ratio, carousel, skeleton

## Reference

- **shadcn/ui components**: https://ui.shadcn.com/docs/components
- **Tailwind CSS**: https://tailwindcss.com/docs
- **Radix UI Primitives**: https://www.radix-ui.com/primitives/docs
