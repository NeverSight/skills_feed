---
name: update-docs
description: Update README.md, architecture documentation (ARCHITECTURE.md, docs/), and plan files (plan/, task_plan.md, progress.md) to reflect current codebase state. Use when the user explicitly asks to "update docs", "update documentation", "update the readme", "update architecture docs", "update plan", "sync docs with code", or similar requests. Discovers project structure, analyzes code changes, and updates documentation with concise technical descriptions and ASCII diagrams.
---

# Update Docs

Update README and architecture documentation to accurately reflect the current state of a codebase.

## Workflow

1. **Discover documentation structure**
2. **Analyze codebase for changes**
3. **Update relevant docs**
4. **Verify accuracy**

## Step 1: Discover Documentation

Find existing documentation files:

```
README.md                    # Root readme
ARCHITECTURE.md              # Root architecture doc
docs/ARCHITECTURE.md         # Docs folder architecture
docs/architecture/           # Architecture subdirectory
docs/*.md                    # Other markdown docs

# Plan files
plan/                        # Plan directory
task_plan.md                 # Task planning doc
progress.md                  # Progress tracking
findings.md                  # Research findings
```

Use Glob to find these patterns. Note which files exist and their current content.

If no architecture doc exists, ask the user where to create one (root or docs/).
If plan files exist, check if they need updates based on completed work.

## Step 2: Analyze Codebase

### Use Git to Identify Changes

Run these commands to understand what changed:

```bash
# See what changed vs main branch
git diff main...HEAD --stat
git diff main...HEAD

# See recent commit history for context
git log main..HEAD --oneline

# See all changed files
git diff main...HEAD --name-only
```

Focus documentation updates on files/components that changed.

### What to Document

1. **For README updates:**
   - Project structure (directories, key files)
   - Installation/setup steps
   - Usage examples
   - Dependencies

2. **For architecture updates:**
   - High-level component overview
   - Data flow between components
   - Key abstractions and interfaces
   - External integrations

3. **For plan file updates:**
   - Mark completed tasks based on commits
   - Update progress based on diff
   - Add findings from implementation

Use these patterns to discover architecture:

```
src/              # Source code root
lib/              # Libraries
packages/         # Monorepo packages
**/index.{ts,js}  # Entry points
**/types.{ts,d.ts} # Type definitions
```

## Step 3: Update Documentation

### README.md Format

```markdown
# Project Name

Brief description (1-2 sentences).

## Quick Start

<installation and basic usage>

## Project Structure

<directory tree with brief explanations>

## Development

<dev commands, testing, etc.>
```

### ARCHITECTURE.md Format

```markdown
# Architecture

## Overview

<1-2 paragraph high-level description>

## Components

<ASCII diagram showing main components>

+------------------+     +------------------+
|   Component A    |---->|   Component B    |
+------------------+     +------------------+
         |
         v
+------------------+
|   Component C    |
+------------------+

### Component A
<brief description, responsibilities>

### Component B
<brief description, responsibilities>

## Data Flow

<describe how data moves through the system>

## Key Decisions

<notable architectural choices and why>
```

### ASCII Diagram Guidelines

Use box-drawing for components:

```
+--------+  Arrow types:
| Box    |  ---> data flow
+--------+  .... optional/async
            <==> bidirectional
```

Keep diagrams under 60 chars wide for terminal readability.

### Plan Files Format

**task_plan.md** - Track implementation tasks:

```markdown
# Task Plan: <feature/project name>

## Objective
<1-2 sentence goal>

## Tasks
- [x] Completed task
- [ ] Pending task
- [ ] Another pending task

## Notes
<decisions, blockers, context>
```

**progress.md** - Track session progress:

```markdown
# Progress

## Completed
- <what was done>

## In Progress
- <current work>

## Next Steps
- <upcoming tasks>
```

**findings.md** - Document research/investigation:

```markdown
# Findings

## Summary
<key takeaways>

## Details
<detailed findings, code references, etc.>
```

When updating plan files:
- Mark completed tasks with `[x]`
- Move completed items to "Completed" section in progress.md
- Add new discoveries to findings.md
- Remove stale/irrelevant items

## Step 4: Verify

After updating:

1. Ensure file paths mentioned in docs exist
2. Verify commands in docs actually work (if testable)
3. Check that component names match actual code

## Style Guidelines

- **Concise**: One sentence per concept where possible
- **Technical**: Assume reader knows programming basics
- **Current**: Only document what exists now, not planned features
- **Accurate**: Every path, command, and name must be verifiable

Avoid:
- Marketing language
- Redundant explanations
- Documenting obvious code
- Future tense ("will be", "planned")
