---
name: fractal-tree-file-structure
description: "Guides file and folder organization using fractal tree structure: self-similar directories, encapsulation, shared/ folders, mini-library pattern, and kebab-case naming. Use when creating, moving, or renaming files, extracting modules into subdirectories, deciding where shared code belongs, or checking import boundaries."
license: MIT
metadata:
  author: kachkaev
  version: "1.0.0"
---

# Fractal tree file structure

This project follows a **fractal tree** approach to file organization, where the structure of any part mirrors the whole.
This self-similar organization allows confident navigation without needing to understand the entire codebase.

## Core principles

- **Recursive structure**: Every directory follows the same organizational patterns, creating predictable navigation at any depth.  
  Developers should not need to learn the entire codebase structure to contribute meaningfully to any section.

- **No circular dependencies**: Imports must form a directed acyclic graph.
  Circular import chains turn the fractal tree into a generic graph, breaking the tree's integrity and causing runtime issues.

- **Organic growth**: Start with a single file; extract to subdirectories only when complexity demands it.
  No boilerplate structure upfront.
  Group resources by functional purpose, never by file "shape" (no project-wide `components/`, `hooks/`, or `utils/` folders).

- **Encapsulation**: Resources in a subdirectory are internal to the parent file unless explicitly re-exported.
  A `shapes/` directory is "owned" by `shapes.ts`.
  Direct imports from nested levels are prohibited—each sub-tree exports resources that can only be imported on the next level up.

- **Contextual sharing**: Common logic lives at the closest common ancestor ("fork" in the tree).
  The `shared/` directory exists at the `src/` level because multiple entrypoints need it.
  Place shared logic as deep in the tree as possible while still serving all dependents.

- **Present-state focus**: Structure reflects current reality, not anticipated future needs.
  Refactor freely as usage patterns evolve.
  This eliminates over-engineering and enables formal linting enforcement.

## Practical rules

### Naming

All files and folders use **kebab-case** for cross-platform compatibility with case-sensitive filesystems.
Enforced via `unicorn/filename-case`.

### No index files

Avoid `index.ts` files that enable implicit folder imports.
They cause path ambiguity where `./foo` could resolve to both `foo.ts` and `foo/index.ts`, and they hurt ESM compatibility.

### Files as mini-libraries

Each file acts as a self-contained "mini-library" with cohesive exports serving a common semantic purpose.
If a file contains only one export, name the file after that export.
Avoid default exports unless externally required.

### Outgrown files become sub-trees

When a file grows unwieldy, extract logic into a sibling subdirectory bearing the original filename:

```text
my-app.ts → my-app.ts (keeps public API)
          → my-app/
              ├── config.ts
              ├── lifecycle.ts
              ├── lifecycle/
              │   ├── something.ts
              │   └── something-else.ts
              └── helpers.ts
```

Only `my-app.ts` imports from the `my-app/` directory, and only `lifecycle.ts` imports from the `lifecycle/` directory – each file owns its namespace.
If `my-app.ts` becomes unused, delete it together with its internal folder safely.

### Relative paths within workspaces

All imports within a workspace use relative paths.
Avoid mixing path alias systems (e.g. `@/foo`) with relative imports, as this creates inconsistency.
(This project uses `@/` aliases for the `src/` root as a convention.)

### `shared/` folder convention

Shared resources between sub-trees go into `path/to/common-parent/shared/`.
Think of `shared/` folders as lightweight `node_modules/`.
Contents of parent-level `shared/` folders remain accessible, but sub-tree `shared/` folders are internal to that sub-tree.

### Multiple entry points

Projects may have several entry points (pages, API handlers, scripts, tests).
Keep their names distinct from mini-libraries using suffixes: `do-something.script.ts`, `xyz.test.tsx`.
Entry points access shared resources but remain outside core logic.

### Colocate unit tests

Place unit tests beside the files they cover: `foo.ts` pairs with `foo.test.ts`.
Integration and end-to-end tests live in separate directories outside the source tree root.

### Exceptions are permitted

Partial adoption works.
Gradually migrate from leaves toward the root.
Imperfect implementation still provides benefits by clarifying dependencies in sections of larger codebases.

## Scoped directories with `@` prefix

Directories prefixed with `@` group related utilities under a namespace, similar to npm scoped packages:

```text
src/shared/
├── @foo/
|  ├── a.ts
|  └── b.ts
├── @bar/
|  ├── m.ts
|  └── n.ts
├── x.ts
└── y.ts
```

This prevents naming collisions and clearly signals "this is a utility namespace, not a feature."

## Import rules

As a consequence of encapsulation, imports should only target "public" resources:

```typescript
// ✓ Correct: import from the mini-library entry point
import { something } from "../../../shared/foo.ts";
import { other } from "../../../shared/@scope/bar.ts";

// ✗ Incorrect: import from internal files (owned by their parent)
import { internal } from "../../../shared/foo/helpers.ts";
import { deep } from "../../../shared/@scope/bar/internal.ts";

// ✗ Incorrect: import from a scope directly (like npm, scopes aren't packages)
import { wrong } from "../../../shared/@scope";
```

## Organic growth example

A real project evolves step by step.
Starting with a single file:

```text
example.ts
```

Extract when necessary:

```text
example.ts
example/
├── do-x.ts
└── do-x.test.ts
```

Add shared logic between extracted modules:

```text
example.ts
example/
├── shared/
│   └── do-common-thing.ts
├── do-x.ts
└── do-y.ts
```

When a second entry point (`example-2.ts`) needs something previously nested, promote it to the closest common ancestor:

```text
shared/
└── bar.ts
example.ts
example/
├── shared/
│   └── do-common-thing.ts
├── do-x.ts
└── do-y.ts
example-2.ts
```

Each step reflects actual code relationships without predicting future needs.

## Anti-patterns

- Do not group files by type/shape rather than function (`components/`, `hooks/`, `utils/`)
- Do not use `index.ts` files enabling implicit folder resolution and path synonyms
- Avoid default exports unless required by third-party
- Do not over-engineer structures for hypothetical future needs
- Do not prematurely split files before maintenance issues emerge (they may not)
- Do not import from a sub-tree's internal files (bypassing encapsulation)
