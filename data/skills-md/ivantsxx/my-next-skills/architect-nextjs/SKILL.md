---
name: architect-nextjs
description: Establish the architecture for Next.js 15+ applications using the Scope Rule and Screaming Architecture. Use this skill when (1) Setting up a new project, (2) Deciding component placement (local vs shared), (3) Refactoring codebases, or (4) implementing Server Actions, layouts, and route groups.
---

# Scope Rule Architect (Next.js 15+)

This skill establishes the architectural foundation for scalable Next.js applications by enforcing strict **Scope Rules** and **Screaming Architecture**.

## Core Principles

### 1. The Scope Rule (Absolute Law)

**"Scope determines structure."**

- **Local Scope**: Code used by **1 feature** → MUST stay local (e.g., `(user)/profile/_components`).
- **Shared Scope**: Code used by **2+ features** → MUST go to `src/shared/`.
- **No Exceptions**: Do not pollute `shared` with single-use components.

### 2. Screaming Architecture

Directory structures must immediately declare *what* the application does.

- Use **Route Groups** `(feature)` for top-level modules.
- Avoid generic folders like `containers` or `views` at the top level.

### 3. Next.js 15 Standards

- **App Router Only**: No `pages/` directory.
- **Server-First**: Components are Server Components by default.
- **Data Access**: Fetch directly in Server Components or via Server Actions.

## Decision Framework

When placing files, follow this decision tree:

1. **Count Usage**:
    - **Used by 1 Feature**: Place in `app/(feature)/_components/`.
    - **Used by 2+ Features**: Place in `src/shared/components/`.

2. **Determine Type**:
    - **Server Component**: Default. Used for static content and initial data fetching.
    - **Client Component**: Use ONLY for `useState`, `useEffect`, or event listeners.
    - **Server Action**: Use for mutations and form handling. Place in `_actions/name.ts`.

## Implementation Guides

### Project Structure

For the standard directory layout, reference the [Project Structure Template](references/project_structure.md).  
Use this reference when setting up new folders or verifying where a specific file should reside.

### Component Templates

For code patterns ensuring best practices, reference the [Component Templates](references/component_templates.md).  
This includes:

- **Server Components** with `Suspense` and data fetching.
- **Client Components** isolated for interactivity.
- **Server Actions** properly typed and validated.

## Quality Checklist

Before finalizing a structure or file creation:

1. [ ] **Scope**: Is this used in >1 feature? If no, move to `_components`.
2. [ ] **Server**: Is "use client" absolutely necessary? Can it be pushed down the tree?
3. [ ] **Screaming**: Does the folder name describe *what* it does (e.g., `(invoices)` vs `pages`)?
4. [ ] **Colocation**: Are specific hooks/types/styles next to the consuming component?
