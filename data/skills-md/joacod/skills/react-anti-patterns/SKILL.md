---
name: react-anti-patterns
description: Introduce React anti-patterns and common mistakes into existing React codebases for training, review, or teaching. Use when asked to intentionally degrade React performance or code quality while keeping apps functional, or to generate anti-pattern examples for junior developer education.
user-invocable: true
invocation-phrases:
  - /react-anti-patterns
  - add react anti-patterns
  - inject react mistakes
  - react training exercise
---

# React Anti-Patterns

## Overview

Inject React anti-patterns and performance pitfalls into existing React apps while keeping them functional, so teams can practice identifying and fixing issues.

## Parameters

### Amount (how many modifications)

- **low**: 1-3 subtle changes, app fully functional
- **medium** (default): 5-8 changes, noticeable performance issues
- **high**: 10+ changes, can cause build failures (TypeScript/lint errors allowed)

### Level (experience targeting)

- **junior**: Obvious issues - easy to spot during code review
- **semi-senior**: Moderate complexity - requires React knowledge
- **senior**: Subtle issues - requires profiling or deep knowledge
- **mixed** (default): Combination of all levels

### Flags

- `--comments`: Add inline comments identifying the anti-pattern
- `--comments-hint`: Add comments with a hint on how to fix
- `--comments-fix`: Add comments with full fix explanation
- `--specific <category>`: Target specific category only (e.g., `--specific rerender`)

### Categories

**React**: `rerender`, `state`, `effect`, `list`, `conditional`, `data`

**Next.js**: `waterfall`, `bundle`, `boundary`, `actions`, `rsc`

## Workflow

### 1. Framework Detection

Check if project is Next.js:

- Look for `next.config.js`, `next.config.mjs`, or `next.config.ts`
- Check `package.json` for `next` dependency

If Next.js detected, ask user:

> "This is a Next.js project. Include Next.js-specific anti-patterns in addition to React patterns?"

### 2. Gather Parameters

If not specified in invocation, ask user:

**Amount** (default: medium): "How many anti-patterns should I introduce?"

- low: 1-3 subtle changes
- medium: 5-8 noticeable changes
- high: 10+ changes, may break build

**Level** (default: mixed): "What experience level should patterns target?"

- junior: obvious issues, easy to spot
- semi-senior: moderate complexity, requires React knowledge
- senior: subtle issues, requires profiling
- mixed: combination of all levels

**Comments** (default: none): "Should I add comments explaining the anti-patterns?"

- none: no comments added
- `--comments`: identify only
- `--comments-hint`: with hints
- `--comments-fix`: with full fixes

### 3. Load Patterns

Based on selections, load relevant reference files:

```
references/anti-patterns-index.md     # Always load for pattern selection
references/react/junior.md            # If level includes junior
references/react/semi-senior.md       # If level includes semi-senior
references/react/senior.md            # If level includes senior
references/nextjs/junior.md           # If Next.js + level includes junior
references/nextjs/semi-senior.md      # If Next.js + level includes semi-senior
references/nextjs/senior.md           # If Next.js + level includes senior
```

### 4. Select Patterns

Using the index, select patterns based on:

- Amount determines count
- Level determines which files to pull from
- `--specific` filters by category
- Prioritize variety across categories unless `--specific` is set

**Selection by amount**:

- **low**: 1-3 patterns from selected level(s)
- **medium**: 5-8 patterns, spread across selected level(s)
- **high**: 10+ patterns, include build-error patterns if available

When `level=mixed`: distribute patterns roughly evenly across junior/semi-senior/senior.
When specific level selected: all patterns from that level only.

### 5. Apply Changes

For each selected pattern:

1. Find suitable injection point in codebase
2. Apply the "After" transformation from the pattern definition
3. Add appropriate comment based on flag:
   - `--comments`: `// ANTI-PATTERN: pattern-id`
   - `--comments-hint`: Add the hint comment from pattern
   - `--comments-fix`: Add the fix comment from pattern
4. Verify the change doesn't break the app (unless high amount with build-error pattern)

### 6. Report

After all changes, provide summary:

```
## Anti-Patterns Applied

### Files Modified
- path/to/Component.tsx: 3 patterns
- path/to/hooks/useData.ts: 2 patterns

### Patterns Introduced
| Pattern | Level | Category | File |
|---------|-------|----------|------|
| list-keys-index | junior | list | Component.tsx:45 |
| usememo-inline-defeat | semi-senior | rerender | Component.tsx:23 |
...

### Next Steps
Run the app and use React DevTools Profiler to identify the performance issues,
or review the code to spot the anti-patterns.
```

## Example Invocations

```bash
# Defaults (medium, mixed levels, no comments)
/react-anti-patterns

# Few junior patterns with hints
/react-anti-patterns --comments-hint low junior

# Many senior patterns with full explanations
/react-anti-patterns --comments-fix high senior

# Only waterfall patterns (Next.js)
/react-anti-patterns --specific waterfall

# Medium amount, semi-senior level, identify comments
/react-anti-patterns --comments medium semi-senior
```

## Resources

- Anti-pattern catalog: `references/anti-patterns-index.md`
- React patterns: `references/react/`
- Next.js patterns: `references/nextjs/`
