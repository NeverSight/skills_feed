---
name: next-project-structure
description: Authoritative guide on Next.js 16+ App Router structure. Use this skill to determine where files should be created, how to name them for routing, and how to organize project architecture.
---

# Next.js Project Structure

## Purpose
This skill defines the folder and file conventions for Next.js App Router applications. Use this to ensure file placement dictates the correct routing behavior and architectural consistency.

## Usage
When creating new features or refactoring, you must first identify the project's **Organization Strategy** (see below) to determine where files belong.

## 1. Top-Level Organization Strategies
Identify which strategy the project is using and strictly adhere to it. Do not mix strategies.

| Strategy | Description | Indicator |
| :--- | :--- | :--- |
| **Store in `src`** | Application code lives in `src/app`. Config files live in root. | `src/app/page.tsx` exists |
| **Root `app`** | Application code lives in `app`. Config files live in root. | `app/page.tsx` exists |
| **Split by Feature** | Global code in `app`; feature code colocated in route segments. | `app/dashboard/_components/` exists |
| **External Projects** | Project files live in `components/` or `lib/` at root, outside `app`. | `components/` exists at root |

## 2. File Conventions (Quick Ref)
Next.js uses file-system based routing. The filename determines the behavior.

* **Routes:** Must be named `page.tsx` or `route.ts`.
* **UI Wrappers:** `layout.tsx` (persistent), `template.tsx` (re-mounted).
* **Data UI:** `loading.tsx` (Suspense), `error.tsx` (Error Boundary).

> For the complete table of supported file names and their hierarchy, read:
> [references/file-conventions.md](references/file-conventions.md)

## 3. Routing & Groups
Do not rely on folder names alone for URL structure.

* **URL Segments:** `app/blog/page.tsx` -> `/blog`
* **Route Groups:** `app/(marketing)/page.tsx` -> `/` (Folder name omitted from URL)
* **Private Folders:** `app/_utils/` -> Not routable.

> For advanced patterns (Dynamic `[id]`, Parallel `@slot`, Intercepting `(.)`), read:
> [references/routing-patterns.md](references/routing-patterns.md)

## Validation Checklist
Before finalizing a file creation:
1.  Does the file name match a reserved Next.js convention (e.g., `page.tsx`)?
2.  Is the file inside the correct Route Group (if applicable)?
3.  Are colocated components properly marked private (in `_folders`) if they shouldn't be routable?