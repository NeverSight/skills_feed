---
name: ts-morph-analyzer
description: Use when debugging TypeScript/JavaScript bugs by tracing call chains, understanding unfamiliar codebases quickly, making architectural decisions, or reviewing code quality. Extract function signatures and JSDoc without full file reads, trace call hierarchies up/down, detect code smells, and follow data flow. Triggers on debugging, understanding codebase, architectural analysis, signature extraction, call tracing.
---

# TypeScript Codebase Analyzer

## Overview

Lightweight codebase analysis using ts-morph. Extract signatures, JSDoc, and call chains without flooding context with full file reads.

**Core principle:** Get maximum architectural insight with minimum token usage.

## When to Use

| Situation | Script to Use |
|-----------|---------------|
| Understand a codebase's public API quickly | `extract-signatures.ts` |
| Trace a bug through function calls | `trace-calls.ts` |
| Map what a module exports | `analyze-exports.ts` |
| Detect architectural issues before diving in | `code-smells.ts` |
| Understand import/dependency structure | `analyze-exports.ts --deps` |

## Setup

```bash
# In the skill directory
cd ~/.claude/skills/ts-morph-analyzer
npm install
```

Or run the setup script:
```bash
~/.claude/skills/ts-morph-analyzer/setup.sh
```

## Quick Reference

### Extract Signatures (Most Common)

Get function/method signatures + JSDoc without reading full files:

```bash
# All signatures in a file
npx ts-node scripts/extract-signatures.ts src/api/users.ts

# All signatures in a directory (recursive)
npx ts-node scripts/extract-signatures.ts src/

# Filter to exported only
npx ts-node scripts/extract-signatures.ts src/ --exported

# Include types and interfaces
npx ts-node scripts/extract-signatures.ts src/ --types

# Output as JSON for further processing
npx ts-node scripts/extract-signatures.ts src/ --json
```

**Output example:**
```
// src/api/users.ts

/**
 * Fetches user by ID from the database
 * @param id - User's unique identifier
 * @returns User object or null if not found
 */
export async function getUser(id: string): Promise<User | null>

/**
 * Creates a new user account
 * @throws ValidationError if email is invalid
 */
export async function createUser(data: CreateUserInput): Promise<User>
```

### Trace Call Hierarchy

Follow function calls up (who calls this?) or down (what does this call?):

```bash
# Who calls this function?
npx ts-node scripts/trace-calls.ts src/api/users.ts:getUser --up

# What does this function call?
npx ts-node scripts/trace-calls.ts src/api/users.ts:getUser --down

# Full call chain (both directions, limited depth)
npx ts-node scripts/trace-calls.ts src/api/users.ts:getUser --depth 3

# Output as tree
npx ts-node scripts/trace-calls.ts src/api/users.ts:getUser --tree
```

**Output example (--up):**
```
getUser (src/api/users.ts:15)
├── called by: handleGetUser (src/routes/users.ts:23)
│   └── called by: router.get('/users/:id') (src/routes/users.ts:8)
├── called by: validateSession (src/middleware/auth.ts:45)
└── called by: getUserProfile (src/services/profile.ts:12)
```

### Analyze Exports

Map a module's public API surface:

```bash
# What does this module export?
npx ts-node scripts/analyze-exports.ts src/api/

# Include re-exports
npx ts-node scripts/analyze-exports.ts src/ --follow-reexports

# Show dependency graph
npx ts-node scripts/analyze-exports.ts src/ --deps
```

### Detect Code Smells

Quick architectural assessment:

```bash
# Full analysis
npx ts-node scripts/code-smells.ts src/

# Specific checks
npx ts-node scripts/code-smells.ts src/ --check circular-deps
npx ts-node scripts/code-smells.ts src/ --check large-functions
npx ts-node scripts/code-smells.ts src/ --check missing-jsdoc
npx ts-node scripts/code-smells.ts src/ --check many-params
```

## Architectural Assessment Patterns

When analyzing a new codebase for potential issues:

### 1. Public API Surface First
```bash
# Get the big picture: what's exported?
npx ts-node scripts/extract-signatures.ts src/ --exported --json > api-surface.json
```
Look for: Overly complex interfaces, inconsistent naming, missing JSDoc on public APIs

### 2. Dependency Structure
```bash
# Map imports - circular deps are red flags
npx ts-node scripts/code-smells.ts src/ --check circular-deps
```
Look for: Circular dependencies, deep import chains, unclear module boundaries

### 3. Function Complexity
```bash
# Find complex functions that may need refactoring
npx ts-node scripts/code-smells.ts src/ --check large-functions --check many-params
```
Look for: Functions >50 lines, >5 parameters, deep nesting

### 4. Documentation Coverage
```bash
# Public APIs should be documented
npx ts-node scripts/code-smells.ts src/ --check missing-jsdoc --exported
```

## Following the Data Trail

When debugging, trace data flow without reading full files:

### Pattern: "Where does this value come from?"

```bash
# 1. Find who calls the function with the bad value
npx ts-node scripts/trace-calls.ts src/service.ts:processData --up --depth 5

# 2. Get signatures of callers to understand parameter flow
npx ts-node scripts/extract-signatures.ts src/caller.ts
```

### Pattern: "Where does this return value go?"

```bash
# 1. Find what uses this function's return
npx ts-node scripts/trace-calls.ts src/api.ts:fetchUser --down

# 2. Check how return values are consumed
npx ts-node scripts/trace-calls.ts src/api.ts:fetchUser --down --show-usage
```

### Pattern: "Full call chain for a bug"

```bash
# Get complete path from entry point to problem area
npx ts-node scripts/trace-calls.ts src/broken.ts:problematicFn --up --tree
```

## Script Locations

All scripts in: `~/.claude/skills/ts-morph-analyzer/scripts/`

| Script | Purpose |
|--------|---------|
| `extract-signatures.ts` | Extract function/method/class signatures with JSDoc |
| `trace-calls.ts` | Trace call hierarchies up/down |
| `analyze-exports.ts` | Map module exports and dependencies |
| `code-smells.ts` | Detect architectural issues |

## Common Issues

| Problem | Solution |
|---------|----------|
| "Cannot find module 'ts-morph'" | Run `npm install` in skill directory |
| Slow on large codebases | Add `--include "src/**/*.ts"` to limit scope |
| Missing type info | Ensure tsconfig.json is in project root |
| Memory issues | Use `--exclude "node_modules"` (default) |
