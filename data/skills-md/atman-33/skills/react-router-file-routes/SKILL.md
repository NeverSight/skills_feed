---
name: react-router-file-routes
description: Reference guide for React Router v7 file-based routing conventions. Use when creating or organizing routes in React Router v7 projects, naming route files, or working with dynamic segments, nested routes, pathless layouts, optional segments, splat routes, and special characters in file-based routing.
---

# React Router File Routes

Complete reference for React Router v7 file-based routing conventions and file naming patterns.

## Core Concepts

React Router v7 uses file-based routing where file names in `app/routes/` directory automatically become routes. Special characters in file names create specific routing behaviors.

## File Naming Conventions

### Basic Routes

| File Name | URL Path | Description |
|-----------|----------|-------------|
| `_index.tsx` | `/` | Index route at the root or parent path |
| `about.tsx` | `/about` | Simple static route |
| `contact.tsx` | `/contact` | Another static route |

### Nested Routes with Dots

Dots (`.`) create nested URL paths and establish parent-child relationships.

| File Name | URL Path | Parent Layout |
|-----------|----------|---------------|
| `concerts.tsx` | `/concerts` | `root.tsx` |
| `concerts._index.tsx` | `/concerts` | `concerts.tsx` |
| `concerts.trending.tsx` | `/concerts/trending` | `concerts.tsx` |
| `concerts.$city.tsx` | `/concerts/:city` | `concerts.tsx` |
| `settings.profile.tsx` | `/settings/profile` | `root.tsx` |
| `settings.profile.edit.tsx` | `/settings/profile/edit` | `root.tsx` |

**Example structure:**
```
app/
├── routes/
│   ├── _index.tsx
│   ├── concerts.tsx              # Layout for /concerts/*
│   ├── concerts._index.tsx       # Renders at /concerts
│   ├── concerts.trending.tsx     # Renders at /concerts/trending
│   └── concerts.$city.tsx        # Renders at /concerts/:city
└── root.tsx
```

### Dynamic Segments

Prefix with `$` to create URL parameters.

| File Name | URL Path | Params |
|-----------|----------|--------|
| `blog.$slug.tsx` | `/blog/:slug` | `{ slug: string }` |
| `users.$userId.tsx` | `/users/:userId` | `{ userId: string }` |
| `teams.$teamId.projects.$projectId.tsx` | `/teams/:teamId/projects/:projectId` | `{ teamId: string, projectId: string }` |

**Access params in component:**
```typescript
import type { Route } from "./+types/blog.$slug";

export async function loader({ params }: Route.LoaderArgs) {
  // params.slug is available here
}

export default function Component({ params }: Route.ComponentProps) {
  return <div>Post: {params.slug}</div>;
}
```

### Optional Segments

Append `?` to make a segment optional (works with both static and dynamic segments).

| File Name | URL Path | Matches |
|-----------|----------|---------|
| `$lang.categories.tsx` | `/:lang?/categories` | `/categories` and `/en/categories` |
| `users.$userId.edit.tsx` | `/users/:userId/edit?` | `/users/123` and `/users/123/edit` |

### Pathless Layout Routes

Prefix with `_` (underscore) to create layouts that don't affect the URL structure.

| File Name | URL Path | Layout Parent |
|-----------|----------|---------------|
| `_auth.tsx` | N/A (pathless) | `root.tsx` |
| `_auth.login.tsx` | `/login` | `_auth.tsx` |
| `_auth.register.tsx` | `/register` | `_auth.tsx` |

**Example structure:**
```
app/
├── routes/
│   ├── _auth.tsx                 # Pathless layout
│   ├── _auth.login.tsx          # URL: /login (wrapped in _auth layout)
│   ├── _auth.register.tsx       # URL: /register (wrapped in _auth layout)
│   └── dashboard.tsx            # URL: /dashboard (not wrapped in _auth)
└── root.tsx
```

### Escaping Layouts with Trailing Underscore

Suffix with `_` to create a nested URL without inheriting parent layout.

| File Name | URL Path | Layout Parent |
|-----------|----------|---------------|
| `concerts.tsx` | `/concerts` | `root.tsx` |
| `concerts.trending.tsx` | `/concerts/trending` | `concerts.tsx` |
| `concerts_.mine.tsx` | `/concerts/mine` | `root.tsx` (skips concerts.tsx) |

### Splat Routes (Catch-All)

Use `$` to create catch-all routes that match remaining URL segments.

| File Name | URL Path | Params |
|-----------|----------|--------|
| `files.$.tsx` | `/files/*` | `{ "*": string }` |
| `$.tsx` | `/*` | `{ "*": string }` (404 catch-all) |

**Access splat params:**
```typescript
export async function loader({ params }: Route.LoaderArgs) {
  const filePath = params["*"]; // Everything after /files/
  return getFileInfo(filePath);
}
```

### Escaping Special Characters

Use `[]` brackets to escape special characters and include them literally in URLs.

| File Name | URL Path | Purpose |
|-----------|----------|---------|
| `sitemap[.]xml.tsx` | `/sitemap.xml` | Resource route with extension |
| `blog[$slug].tsx` | `/blog/$slug` | Literal `$slug` in URL (not a param) |
| `about[.].tsx` | `/about.` | Literal dot in URL |

## Complete File Structure Examples

### Standard Nested Routes
```
app/
├── routes/
│   ├── _index.tsx           # /
│   ├── about.tsx            # /about
│   ├── concerts.tsx         # /concerts layout
│   ├── concerts._index.tsx  # /concerts
│   ├── concerts.$city.tsx   # /concerts/:city
│   └── concerts.trending.tsx # /concerts/trending
└── root.tsx
```

### Pathless Layout Routes
```
app/
├── routes/
│   ├── _auth.tsx            # Pathless layout
│   ├── _auth.login.tsx      # /login
│   ├── _auth.register.tsx   # /register
│   └── dashboard.tsx        # /dashboard
└── root.tsx
```

### Mixed Layouts
```
app/
├── routes/
│   ├── _index.tsx              # /
│   ├── concerts.tsx            # /concerts layout
│   ├── concerts._index.tsx     # /concerts
│   ├── concerts.trending.tsx   # /concerts/trending
│   └── concerts_.mine.tsx      # /concerts/mine (skips layout)
└── root.tsx
```

## Quick Reference

| Pattern | File Example | URL Result | Notes |
|---------|-------------|------------|-------|
| Simple route | `about.tsx` | `/about` | Static route |
| Nested path | `a.b.c.tsx` | `/a/b/c` | Dots create slashes |
| Index route | `concerts._index.tsx` | `/concerts` | Default child route |
| Dynamic segment | `blog.$slug.tsx` | `/blog/:slug` | Creates param |
| Multiple params | `$a.$b.tsx` | `/:a/:b` | Multiple dynamic segments |
| Optional segment | `$lang?.about.tsx` | `/about` or `/:lang/about` | Optional param |
| Pathless layout | `_auth.login.tsx` | `/login` | Uses `_auth.tsx` layout |
| Escape layout | `parent_.child.tsx` | `/parent/child` | Skips `parent.tsx` layout |
| Splat route | `files.$.tsx` | `/files/*` | Catches all after `/files/` |
| Escape chars | `api[.]json.tsx` | `/api.json` | Literal `.` in URL |

## Common Patterns

### Authentication Routes
```
_auth.tsx              # Shared auth layout
_auth.login.tsx       # /login
_auth.register.tsx    # /register
_auth.forgot.tsx      # /forgot
```

### Admin Dashboard
```
_admin.tsx                    # Admin layout
_admin._index.tsx            # /admin
_admin.users.tsx             # /admin/users
_admin.users.$userId.tsx     # /admin/users/:userId
```

### Blog with Categories
```
blog.tsx                     # Blog layout
blog._index.tsx             # /blog
blog.$slug.tsx              # /blog/:slug
blog.category.$cat.tsx      # /blog/category/:cat
```

### Resource Routes
```
api.json.tsx                # /api/json
sitemap[.]xml.tsx          # /sitemap.xml
robots[.]txt.tsx           # /robots.txt
```

### scripts/
Executable code (Python/Bash/etc.) that can be run directly to perform specific operations.

**Examples from other skills:**
- PDF skill: `fill_fillable_fields.py`, `extract_form_field_info.py` - utilities for PDF manipulation
- DOCX skill: `document.py`, `utilities.py` - Python modules for document processing

**Appropriate for:** Python scripts, shell scripts, or any executable code that performs automation, data processing, or specific operations.

**Note:** Scripts may be executed without loading into context, but can still be read by Codex for patching or environment adjustments.

### references/
Documentation and reference material intended to be loaded into context to inform Codex's process and thinking.

**Examples from other skills:**
- Product management: `communication.md`, `context_building.md` - detailed workflow guides
- BigQuery: API reference documentation and query examples
- Finance: Schema documentation, company policies

**Appropriate for:** In-depth documentation, API references, database schemas, comprehensive guides, or any detailed information that Codex should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Codex produces.

**Examples from other skills:**
- Brand styling: PowerPoint template files (.pptx), logo files
- Frontend builder: HTML/React boilerplate project directories
- Typography: Font files (.ttf, .woff2)

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Not every skill requires all three types of resources.**
