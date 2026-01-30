---
name: mapcn-docs
description: Use when building documentation sites with live code previews, component library docs, API reference pages, or interactive code examples using Next.js App Router and shadcn/ui.
---

# mapcn-docs

Build beautiful, interactive documentation sites with live component previews and copy-paste code examples.

## Overview

This skill implements a documentation system featuring:
- **Live previews** with tabbed preview/code views
- **Syntax-highlighted code** using Shiki with light/dark theme support
- **Copy-to-clipboard** functionality for all code examples
- **Responsive sidebar** navigation with mobile support
- **Scroll-tracking TOC** (Table of Contents)
- **Accessible design** using shadcn/ui components

## When to Use

**Use this skill when:**
- Building a docs site for a component library or design system
- Creating API reference pages with interactive examples
- Need tabbed preview/code views like shadcn/ui docs
- Want copy-paste ready code examples with syntax highlighting

**Do NOT use when:**
- Simple static documentation (use MDX or plain markdown)
- No need for live component previews
- Not using Next.js App Router or React

**Prerequisites:**
- Next.js 13+ with App Router (`app/` directory)
- Tailwind CSS configured
- shadcn/ui initialized (`npx shadcn@latest init`)

## Quick Start

### 1. Directory Structure

```
src/app/docs/
├── layout.tsx                    # Root docs layout
├── page.tsx                      # Introduction page
├── _components/
│   ├── docs.tsx                  # Core UI components
│   ├── docs-sidebar.tsx          # Navigation sidebar
│   ├── docs-toc.tsx              # Table of contents
│   ├── component-preview.tsx     # Server-side preview wrapper
│   ├── component-preview-client.tsx  # Client-side preview tabs
│   ├── code-block.tsx            # Code display
│   ├── copy-button.tsx           # Clipboard utility
│   └── examples/                 # Live example components
└── [route]/page.tsx              # Documentation pages
```

### 2. Install Dependencies

```bash
npm install shiki
npx shadcn@latest add sidebar table card tabs
```

### 3. Create Core Components

See [references/COMPONENTS.md](references/COMPONENTS.md) for complete component implementations.

## Page Structure Pattern

Every documentation page follows this structure:

```tsx
import { Metadata } from "next";
import { DocsLayout, DocsSection, DocsPropTable } from "../_components/docs";
import { ComponentPreview } from "../_components/component-preview";
import { getExampleSource } from "@/lib/get-example-source";
import { MyExample } from "../_components/examples/my-example";

export const metadata: Metadata = { title: "Page Title" };

export default function PageName() {
  const exampleSource = getExampleSource("my-example.tsx");

  return (
    <DocsLayout
      title="Page Title"
      description="Brief description of this page"
      prev={{ title: "Previous", href: "/docs/previous" }}
      next={{ title: "Next", href: "/docs/next" }}
      toc={[
        { title: "Overview", slug: "overview" },
        { title: "Usage", slug: "usage" },
        { title: "API Reference", slug: "api-reference" },
      ]}
    >
      <DocsSection>
        <p>Introduction paragraph.</p>
      </DocsSection>

      <DocsSection title="Overview">
        <p>Section content here.</p>
      </DocsSection>

      <DocsSection title="Usage">
        <ComponentPreview code={exampleSource}>
          <MyExample />
        </ComponentPreview>
      </DocsSection>

      <DocsSection title="API Reference">
        <DocsPropTable
          props={[
            {
              name: "propName",
              type: "string",
              default: "undefined",
              description: "Description of the prop",
            },
          ]}
        />
      </DocsSection>
    </DocsLayout>
  );
}
```

## Example Component Pattern

Create example components in `_components/examples/`:

```tsx
// Client-side example (with state)
"use client";

import { useState } from "react";
import { MyComponent } from "@/registry/my-component";

export function InteractiveExample() {
  const [value, setValue] = useState("initial");

  return (
    <div className="h-[400px] w-full">
      <MyComponent value={value} onChange={setValue} />
    </div>
  );
}
```

```tsx
// Server-side example (no state)
import { MyComponent } from "@/registry/my-component";

export function SimpleExample() {
  return (
    <div className="h-[400px] w-full">
      <MyComponent />
    </div>
  );
}
```

**Key pattern**: Always wrap examples in a fixed-height container (`h-[400px]`) for consistent preview rendering.

## Navigation Configuration

Define navigation in `docs-navigation.ts`:

```tsx
import { BookOpen, Code, Settings } from "lucide-react";

export const docsNavigation = {
  groups: [
    {
      title: "Getting Started",
      items: [
        { title: "Introduction", href: "/docs", icon: BookOpen },
        { title: "Installation", href: "/docs/installation", icon: Code },
      ],
    },
    {
      title: "Components",
      items: [
        { title: "Button", href: "/docs/button", icon: Settings },
        // Add more components...
      ],
    },
  ],
};
```

## Code Highlighting Setup

Create `lib/highlight.ts`:

```tsx
import { codeToHtml } from "shiki";

export async function highlightCode(code: string, lang = "tsx") {
  return codeToHtml(code, {
    lang,
    themes: {
      light: "github-light",
      dark: "github-dark",
    },
  });
}
```

Create `lib/get-example-source.ts`:

```tsx
import fs from "fs";
import path from "path";

export function getExampleSource(filename: string): string {
  const filePath = path.join(
    process.cwd(),
    "src/app/docs/_components/examples",
    filename
  );

  let content = fs.readFileSync(filePath, "utf-8");

  // Transform import paths for user copy-paste
  content = content.replace(
    /@\/registry\//g,
    "@/components/ui/"
  );

  return content;
}
```

## UI Components

The docs system uses these core components:

| Component | Purpose |
|-----------|---------|
| `DocsLayout` | Page wrapper with prev/next nav and TOC |
| `DocsSection` | Content section with auto-generated slug IDs |
| `DocsHeader` | Page title and description |
| `DocsNote` | Highlighted callout boxes |
| `DocsCode` | Inline code styling |
| `DocsLink` | Styled links with external support |
| `DocsPropTable` | API reference tables |
| `ComponentPreview` | Live preview with code tab |
| `CodeBlock` | Standalone code display |

## Preview System Architecture

```
┌─────────────────────────────────────────────┐
│ ComponentPreview (Server Component)          │
│ - Receives code string                       │
│ - Calls highlightCode() with Shiki           │
│ - Passes highlighted HTML to client          │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│ ComponentPreviewClient (Client Component)    │
│ - Renders tabs: Preview | Code               │
│ - Preview tab: renders children              │
│ - Code tab: shows highlighted code           │
│ - Copy button for code                       │
└─────────────────────────────────────────────┘
```

## Adding a New Documentation Page

1. Create route directory: `src/app/docs/[page-name]/page.tsx`
2. Create example component if needed: `_components/examples/[name]-example.tsx`
3. Add to navigation in `docs-navigation.ts`
4. Update prev/next links on adjacent pages

## Best Practices

1. **Keep examples focused** - One concept per example
2. **Use fixed heights** - `h-[400px]` for consistent previews
3. **Transform imports** - Change internal paths for user copy-paste
4. **Include API tables** - Document all props with types and defaults
5. **Add TOC items** - List all major sections for scroll tracking
6. **Mobile-first** - Test sidebar collapse and responsive layouts

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Calling `highlightCode` in Client Component | Move to Server Component - Shiki requires server-side execution |
| Missing fixed height on examples | Add `h-[400px]` wrapper for consistent preview rendering |
| Using internal import paths in examples | Use `getExampleSource()` to transform `@/registry/` to `@/components/ui/` |
| Forgetting to update navigation | Always add new pages to `docs-navigation.ts` |
| Not updating prev/next links | Check adjacent pages when adding/removing docs |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| shadcn/ui not installed | Run `npx shadcn@latest init` first, then add components |
| Shiki SSR errors | Ensure `highlightCode` is only called in Server Components |
| Dark mode not working | Add `defaultColor: false` to Shiki config and use CSS `[data-theme]` selectors |
| Preview height inconsistent | Always use fixed height (`h-[400px]`) on example wrappers |
| Copy button not working | Ensure HTTPS or localhost (clipboard API requirement) |

## Prerequisites Check

Before using this skill, verify:
1. Next.js 13+ with App Router (`app/` directory)
2. Tailwind CSS configured
3. `cn()` utility from shadcn/ui (`lib/utils.ts`)

If missing shadcn/ui:
```bash
npx shadcn@latest init
```

## File Reference

- [references/COMPONENTS.md](references/COMPONENTS.md) - Complete component implementations
- [references/LAYOUT.md](references/LAYOUT.md) - Layout and sidebar setup
- [scripts/create-doc-page.sh](scripts/create-doc-page.sh) - Generate new doc pages
