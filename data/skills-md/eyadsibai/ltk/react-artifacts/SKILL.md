---
name: react-artifacts
description: Use when "building React artifacts", "creating HTML artifacts", "bundling React apps", "single HTML file", or asking about "artifact builder", "shadcn components", "Tailwind artifacts"
version: 1.0.0
---

<!-- Adapted from: awesome-claude-skills/artifacts-builder -->

# React Artifacts Builder

Create elaborate, multi-component claude.ai HTML artifacts using React, Tailwind CSS, and shadcn/ui.

## When to Use

- Building complex React artifacts for claude.ai
- Creating interactive demos needing state management
- Using shadcn/ui components in artifacts
- Bundling React apps into single HTML files
- NOT for simple single-file HTML/JSX artifacts

## Stack

- React 18 + TypeScript + Vite
- Parcel (bundling)
- Tailwind CSS
- shadcn/ui (40+ pre-installed components)

## Workflow

1. **Initialize** - Create project with init script
2. **Develop** - Build your artifact
3. **Bundle** - Convert to single HTML file
4. **Share** - Display artifact to user

## Project Initialization

```bash
# Create new artifact project
bash scripts/init-artifact.sh <project-name>
cd <project-name>
```

Creates project with:

- React + TypeScript via Vite
- Tailwind CSS with shadcn theming
- Path aliases (@/) configured
- 40+ shadcn/ui components pre-installed
- All Radix UI dependencies
- Parcel configured for bundling

## Bundling to Single HTML

```bash
# Bundle entire React app to one HTML file
bash scripts/bundle-artifact.sh
```

Creates `bundle.html` - self-contained artifact with all JS, CSS, and dependencies inlined.

## Design Guidelines

**Avoid "AI slop"**:

- No excessive centered layouts
- No purple gradients
- No uniform rounded corners
- Vary from Inter font

**Best Practices**:

- Match content to subject
- Clear visual hierarchy
- Consistent patterns
- Accessible design

## shadcn/ui Components

Reference: <https://ui.shadcn.com/docs/components>

Pre-installed components include:

- Button, Card, Dialog, Drawer
- Form, Input, Select, Checkbox
- Table, Tabs, Toast
- And many more...

## Example Structure

```tsx
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export default function App() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>My Artifact</CardTitle>
      </CardHeader>
      <CardContent>
        <Button>Click me</Button>
      </CardContent>
    </Card>
  )
}
```

## Tips

- Develop normally, bundle at the end
- Test in browser before bundling
- Keep bundle size reasonable
- Use Tailwind for responsive design
