---
name: cartographer
description: Maps and documents the codebase. Generates `docs/CODEBASE_MAP.md` with architecture diagrams, module relationships, and data flow. Use when the user asks to "map the code", "explain the architecture", or "update documentation".
---

# Cartographer

## Purpose
To create a living document (`docs/CODEBASE_MAP.md`) that serves as the architectural "Source of Truth" for the project.

## Workflow

### Phase 1: Reconnaissance
1.  **Tree Scan:** Execute a file listing command (e.g., `find . -maxdepth 2 -not -path '*/.*'`) to visualize the high-level structure.
2.  **Config Check:** Read `package.json` and `tsconfig.json` to identify the stack.

### Phase 2: Iterative Analysis
**Exclusion Protocol:** You must strictly ignore:
* Folders in `.gitignore` (specifically `node_modules/`, `.next/`, `dist/`, `build/`).
* Lock files (`package-lock.json`, `yarn.lock`).
* Public assets (`public/images/`).

**Loop:** For each *relevant* major directory (e.g., `app/`, `lib/`, `components/`):
1.  Read the entry point files.
2.  Apply the **Inspection Rubric** (`references/inspection-rubric.md`).
3.  Store findings in memory.

### Phase 3: Synthesis
Create or Overwrite `docs/CODEBASE_MAP.md` using the strict template in `references/map-template.md`.

## Critical Constraints
* **Mermaid Diagrams:** You MUST generate a Mermaid graph for the high-level architecture.
* **No Fluff:** Do not summarize code line-by-line. Focus on *intent*.
* **Linkage:** Every mention of a file in the map must be a clickable relative link.