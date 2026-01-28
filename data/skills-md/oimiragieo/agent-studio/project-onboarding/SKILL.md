---
name: project-onboarding
description: Guided project onboarding for new codebases. Helps agents understand project structure, build systems, test commands, and development workflows by creating persistent knowledge memories.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Glob, Grep, Bash, Write]
best_practices:
  - Perform onboarding before starting any substantial work on unfamiliar projects
  - Create structured memories for reuse across sessions
  - Focus on actionable information (build commands, test commands, key directories)
  - Validate discovered information by running commands when safe
  - Keep memories concise and well-organized
error_handling: graceful
streaming: supported
---

<identity>
Project Onboarding Specialist - Guided codebase exploration and knowledge capture for rapid project understanding.
</identity>

<capabilities>
- Discovering project structure and organization patterns
- Identifying build systems and package managers
- Finding test commands and coverage configuration
- Mapping key directories and entry points
- Creating persistent memories for future sessions
- Generating project overview documentation
- Identifying development workflows and conventions
</capabilities>

<instructions>

## When to Use

Invoke this skill when:

- Starting work on an unfamiliar codebase
- After context is lost (new session)
- When `check_onboarding_performed` indicates no memories exist
- When user asks to "learn about this project" or "understand this codebase"

## Onboarding Workflow

### Step 1: Check Existing Knowledge

First, check if onboarding was already performed:

```
List files in: .claude/context/memory/
Look for: project-structure.md, build-commands.md, test-commands.md
```

If memories exist, read them and skip to Step 6 (Validation).

### Step 2: Project Discovery

**First, classify the project:**

#### Greenfield vs Brownfield Detection

| Indicator                                                   | Present?      | Classification         |
| ----------------------------------------------------------- | ------------- | ---------------------- |
| `.git` directory with history                               | Yes           | Brownfield             |
| Package manifest (`package.json`, `requirements.txt`, etc.) | Yes           | Brownfield             |
| Source directories (`src/`, `app/`, `lib/`) with code       | Yes           | Brownfield             |
| Dirty git status (uncommitted changes)                      | Yes           | Brownfield (warn user) |
| Empty or only README.md                                     | None of above | Greenfield             |

**For Brownfield Projects:**

1. **Respect Ignore Files**: Check `.gitignore` and `.claudeignore` BEFORE scanning
2. **Efficient File Triage**:
   - Use `git ls-files` to list tracked files (respects .gitignore)
   - For large files (>1MB): Read only head/tail (first and last 20 lines)
   - Skip binary files, node_modules, build artifacts
3. **Infer Tech Stack**: Analyze manifests before asking questions
4. **Context-Aware Questions**: Base questions on discovered patterns

```bash
# Efficient file listing (respects .gitignore)
git ls-files --exclude-standard -co | head -100

# For non-git projects with manual ignores
find . -type f \
  -not -path '*/node_modules/*' \
  -not -path '*/.git/*' \
  -not -path '*/dist/*' \
  -not -path '*/build/*' \
  | head -100
```

**For Greenfield Projects:**

- Create fresh context artifacts
- Use interactive-requirements-gathering skill for setup

Analyze the project root to identify:

1. **Package Manager & Language**:
   - `package.json` - Node.js/JavaScript/TypeScript
   - `pyproject.toml`, `requirements.txt` - Python
   - `Cargo.toml` - Rust
   - `go.mod` - Go
   - `pom.xml`, `build.gradle` - Java
   - `composer.json` - PHP

2. **Project Type**:
   - Frontend, Backend, Fullstack, Library, CLI, Mobile, Monorepo

3. **Framework Detection**:
   - Parse dependencies for frameworks (React, Next.js, FastAPI, etc.)

### Step 3: Build System Analysis

Identify how to build/run the project:

1. **Check package.json scripts** (Node.js):

   ```json
   {
     "scripts": {
       "dev": "...",
       "build": "...",
       "start": "...",
       "test": "..."
     }
   }
   ```

2. **Check Makefiles** (Python, Go, Rust):

   ```makefile
   build:
   test:
   lint:
   ```

3. **Check pyproject.toml** (Python):

   ```toml
   [tool.poetry.scripts]
   [tool.poe.tasks]
   ```

4. **Document discovered commands**:
   - Development: `npm run dev`, `uv run dev`
   - Build: `npm run build`, `cargo build`
   - Test: `npm test`, `pytest`
   - Lint: `npm run lint`, `ruff check`

### Step 4: Directory Structure Mapping

Map key directories:

| Directory                       | Purpose             |
| ------------------------------- | ------------------- |
| `src/`                          | Source code         |
| `lib/`                          | Library code        |
| `test/`, `tests/`, `__tests__/` | Test files          |
| `docs/`                         | Documentation       |
| `scripts/`                      | Utility scripts     |
| `config/`                       | Configuration files |

Identify:

- Entry points (`index.ts`, `main.py`, `app.py`)
- Component directories
- API routes
- Database models

### Step 5: Create Onboarding Memories

Save discovered information to persistent memories:

**Memory: project-structure.md**

```markdown
# Project Structure

## Overview

- Project Type: [fullstack/backend/frontend/library]
- Primary Language: [TypeScript/Python/Go/Rust]
- Framework: [Next.js/FastAPI/Express/etc.]

## Key Directories

- Source: `src/`
- Tests: `test/`
- Config: `.claude/`

## Entry Points

- Main: `src/index.ts`
- API: `src/api/`

## Important Files

- Configuration: `package.json`, `tsconfig.json`
- Environment: `.env.example`
```

**Memory: build-commands.md**

```markdown
# Build Commands

## Development

- Start dev server: `npm run dev`
- Watch mode: `npm run watch`

## Build

- Production build: `npm run build`
- Type check: `npm run typecheck`

## Clean

- Clean build: `npm run clean`
```

**Memory: test-commands.md**

```markdown
# Test Commands

## Unit Tests

- Run all: `npm test`
- Watch mode: `npm test -- --watch`
- Coverage: `npm test -- --coverage`

## E2E Tests

- Run: `npm run test:e2e`

## Linting

- Lint: `npm run lint`
- Fix: `npm run lint:fix`
```

### Step 6: Validation

Validate discovered information:

1. **Test Commands** (if safe):
   - Run `npm --version` or equivalent to verify package manager
   - Run `npm run --silent` to list available scripts
   - Do NOT run build or test without user permission

2. **Verify Paths**:
   - Confirm key directories exist
   - Verify entry points are correct

### Step 7: Report Summary

Output a concise summary:

```
## Onboarding Complete

**Project**: [name]
**Type**: [fullstack/backend/etc.]
**Framework**: [Next.js/FastAPI/etc.]

**Quick Commands**:
- Dev: `npm run dev`
- Test: `npm test`
- Build: `npm run build`

**Key Locations**:
- Source: `src/`
- Tests: `test/`
- API: `src/api/`

**Memories Created**:
- .claude/context/memory/project-structure.md
- .claude/context/memory/build-commands.md
- .claude/context/memory/test-commands.md
```

</instructions>

<examples>
<usage_example>
**User Request**: "I need to understand this codebase"

**Agent Actions**:

1. Check for existing memories in `.claude/context/memory/`
2. If no memories, run project discovery
3. Analyze package.json, directory structure
4. Create memory files
5. Report summary

**Output**:

```
## Onboarding Complete

**Project**: agent-studio
**Type**: Multi-agent orchestration framework
**Framework**: Claude Code + Custom agents

**Quick Commands**:
- Validate: `node .claude/tools/validate-agents.mjs`
- Test hooks: `node .claude/hooks/routing/router-enforcer.cjs`

**Key Locations**:
- Agents: `.claude/agents/`
- Skills: `.claude/skills/`
- Memory: `.claude/context/memory/`

**Memories Created**: 3 files
```

</usage_example>
</examples>

<integration>
**Related Skills**:
- `project-analyzer` - Deep automated analysis (complements onboarding)
- `repo-rag` - Semantic search for patterns
- `session-handoff` - Prepare context for new sessions
</integration>

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern discovered -> `.claude/context/memory/learnings.md`
- Issue encountered -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
