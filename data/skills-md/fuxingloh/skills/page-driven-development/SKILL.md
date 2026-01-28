---
name: page-driven-development
description: Review and write React/Next.js code following Page Driven Development principles. Use when organizing components, making file structure decisions, or asked to "review structure", "organize code", "refactor components", or "follow PDD".
license: MIT
metadata:
  author: fuxingloh
  version: "1.0.0"
---

# Page Driven Development (PDD)

## Core Principle

Code should be organized by **context**, not by technology or false separation of concerns. Components belong near the pages that use them, not in global shared directories.

## Guidelines

### 1. Colocate Components with Pages

Place components in the same directory as the page that uses them:

```
app/
  dashboard/
    page.tsx
    dashboard-header.tsx      # Only used by dashboard
    dashboard-stats.tsx       # Only used by dashboard
  settings/
    page.tsx
    settings-form.tsx         # Only used by settings
```

**NOT** in a global components folder:

```
# Avoid this pattern
components/
  DashboardHeader.tsx
  DashboardStats.tsx
  SettingsForm.tsx
```

### 2. Avoid False Separation of Concerns

Do not abstract components globally just because they "could" be reused. A component used in multiple pages with vastly different contexts creates tangled coupling.

**Ask yourself:**
- Is this component actually used in multiple places right now?
- Do those places share the same context/narrative?
- Will changes to one usage break the other?

If the contexts differ, keep separate implementations.

### 3. Decompose Pages into Manageable Components

PDD does not mean monolithic pages. Decompose naturally:

- More than 10 `useState` calls in a component is a code smell
- Avoid prop-drilling through many layers
- Avoid type assertions that hide complexity
- Create natural hierarchies within the page directory

### 4. Global Components Are Exceptions

Only create truly global components for:
- Primitives with no business logic (Button, Input, Modal shell)
- Layout wrappers used across all pages
- Design system tokens/utilities

### 5. Embrace Duplication Over Wrong Abstraction

It's better to have similar code in two places than a fragile abstraction that serves neither well. Duplication is cheaper than the wrong abstraction.

## When Reviewing Code

Check for:
- [ ] Components are colocated with their pages
- [ ] No unnecessary global component abstractions
- [ ] Page components are decomposed (not monolithic)
- [ ] No prop-drilling or excessive `useState` in page root
- [ ] Shared components truly share context, not just appearance

## When Writing New Code

1. Start in the page directory
2. Extract components only when the page file grows unwieldy
3. Keep extracted components in the same directory
4. Only promote to global when genuinely reused with same context
