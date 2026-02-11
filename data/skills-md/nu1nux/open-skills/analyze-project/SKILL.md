---
name: analyze-project
description: Analyze a project's features, architecture, and implementation details without modifying any files.
---

# Project Analysis

## Overview

Perform comprehensive project analysis across three dimensions: **Features**, **Architecture**, and **Implementation**. Provide actionable insights with specific file paths and line references.

**Core principle:** Read and understand, never modify. Always provide concrete code references.

**Announce at start:** "I'm analyzing this project's features, architecture, and implementation."

${languageInstruction}

## Critical Constraints

- **READ-ONLY** - Do not edit or create any files
- **NO CODE GENERATION** - Only reference existing code
- **ALWAYS CITE SOURCES** - Include `file:line` references for all code mentions
- **SAVE REPORT** - Save analysis to `docs/analysis/YYYY-MM-DD-<project-name>.md`

## Analysis Process

### Phase 1: Feature Discovery

**Goal:** Identify what the project does.

**Steps:**

1. Parse arguments to determine analysis scope:
   - No args: Analyze entire project
   - Directory path: Focus analysis on that directory
   - `--features` / `--architecture` / `--implementation`: Run only the specified phase(s)
2. Find entry points:
   - Check config files for entry hints: `package.json` (`main`/`bin`/`scripts`), `Cargo.toml` (`[[bin]]`), `setup.py`/`pyproject.toml` (`entry_points`/`scripts`), `go.mod`, `Makefile`, etc.
   - Look for common entry files: `main.*`, `index.*`, `app.*`, `cli.*`, `server.*`
   - Identify CLI commands, API route definitions, exported modules
3. Identify feature modules and their responsibilities
4. List public APIs and interfaces
5. Document configuration options

### Phase 2: Architecture Analysis

**Goal:** Understand how the project is organized.

**Steps:**

1. Identify tech stack (language, runtime, framework, build tools)
2. Analyze key third-party dependencies and their purposes (focus on 5-15 most significant; group by category if many)
3. Map source directory structure with file purposes
4. Identify core components and their relationships
5. Trace data flow (input → processing → output)
6. Identify design patterns used and whether they are applied consistently

### Phase 3: Implementation Deep Dive

**Goal:** Understand how key features are implemented.

**Steps:**

1. Trace code paths for core features
2. Document key algorithms and logic
3. Identify important classes/functions and their roles
4. Find extension points and customization options

## Output Format

```markdown
# Project Analysis: [Project Name]

## Overview

[One paragraph describing what the project does]

## Features

| Feature | Description | Entry Point |
|---------|-------------|-------------|
| [name] | [what it does] | [file:line] |

## Architecture

### Tech Stack

| Category | Technology |
|----------|------------|
| Language | [e.g., Python 3.12, Go 1.22, TypeScript 5.x] |
| Runtime | [e.g., Node.js 20, CPython, JVM 21] |
| Framework | [e.g., Express, Django, Gin] |
| Build Tool | [e.g., Vite, setuptools, cargo] |

### Dependencies (Key)

List direct dependencies critical to understanding the project. Group by category if many.

| Package | Version | Purpose |
|---------|---------|---------|
| [name] | [version] | [what it does] |

### Source Structure

<!-- Adapt tree to actual project structure and language -->
project/
├── src/                # Source code
│   ├── core/           # Core business logic
│   ├── utils/          # Utility functions
│   └── main.*          # Main entry point
├── tests/              # Test files
└── [config files]      # Project configuration

**Key Files:**

| Path | Purpose |
|------|---------|
| [path to main entry] | Main entry, exports public API |
| [path to core module] | Core business logic |

### Core Components

| Component | Location | Responsibility |
|-----------|----------|----------------|
| [name] | [file:line] | [what it does] |

### Data Flow

[Input] → [Processing Stage 1] → [Processing Stage 2] → [Output]

### Design Patterns

| Pattern | Location | Purpose |
|---------|----------|---------|
| [pattern name] | [file:line] | [why it's used] |

## Implementation Details

### [Feature Name]

- **Entry:** `file:line`
- **Code Path:** file1:10 → file2:25 → file3:100
- **Key Logic:** [explanation of algorithm/approach]
- **Extension Points:** [how to customize/extend]
```

## Edge Cases

| Scenario | Action |
| -------- | ------ |
| Empty or near-empty project | Note limited scope, analyze what exists |
| Monorepo with multiple packages | Summarize top-level structure, then analyze each package briefly; ask user if they want a deep dive on a specific package |
| Very large project (>100 source files) | Focus on key entry points and core modules; note areas skipped |
| No recognizable entry point | State this explicitly; analyze based on directory structure and config files |
| Multiple languages | Identify all languages; organize analysis by language or component |
| Generated / vendor / build output files | Skip by default; note as skipped |
| Project has existing documentation (README, docs/) | Cross-reference findings against it; note discrepancies |

## Usage Examples

| Command | Description |
| ------- | ----------- |
| `/analyze-project` | Analyze the current project |
| `/analyze-project src/` | Focus analysis on the src directory |
| `/analyze-project --features` | Only run Feature Discovery phase |
| `/analyze-project --architecture` | Only run Architecture Analysis phase |
| `/analyze-project --implementation` | Only run Implementation Deep Dive phase |

## Guidelines

- Start with the broadest view, then drill into details — don't get lost in implementation before understanding architecture
- Prioritize accuracy over completeness — say "unclear" rather than guess
- Adapt depth to project size: small projects get full analysis, large projects focus on core modules
- When multiple patterns coexist (e.g., both MVC and event-driven), note the inconsistency
- Identify not just what patterns are used, but whether they're applied correctly
- Don't list every file — focus on architecturally significant files
- If the project has documentation, cross-reference your findings against it
- Use tables for structured data, tree diagrams for directories, flow notation (→) for data flow

Arguments: ${args}
