---
name: react-hook
description: Use when passing callbacks to custom hooks, fixing react-hooks/exhaustive-deps warnings, or debugging unexpected re-renders in React components.
---

# React Hook Patterns

## Overview

**Core principles:**
- Callbacks passed to hooks must be wrapped in `useCallback`
- One hook per file, organized by feature domain
- Only abstract when logic is reused or complex

## Custom Hook Rules

| Rule | Why |
|------|-----|
| Must start with `use` | React's hook detection |
| One hook per file | Maintainability |
| Never call conditionally | Breaks hook order |
| Never return side effects | Unpredictable behavior |
| Type inputs and outputs | Clarity and safety |
| Test in isolation | Reliability |

**On memoization:** Only use `useMemo`/`useCallback` when logic is computationally heavy. Otherwise they degrade readability without meaningful benefit. Exception: callbacks passed TO hooks (see stability section below).

## When to Use

- Passing a callback to a custom hook
- Fixing `react-hooks/exhaustive-deps` ESLint warnings
- Debugging "why is this re-rendering every keystroke?"
- Seeing errors like `addRange(): The given range isn't in document`

## The Problem

```
Inline callback → Hook depends on it → Hook's output in useMemo → Cascade of re-renders
```

When you fix an ESLint `exhaustive-deps` warning by adding a dependency, check if that dependency is STABLE. If not, you've created a re-render loop.

## Core Pattern

```tsx
// ❌ BAD - inline function recreated every render
const { handler } = useCustomHook({
  onComplete: (result) => doSomething(result)
});

// ✅ GOOD - stable reference
const onComplete = useCallback((result) => doSomething(result), []);
const { handler } = useCustomHook({ onComplete });
```

## Quick Reference

| Situation | Action |
|-----------|--------|
| Passing callback to hook | Wrap in `useCallback` |
| ESLint says add dependency | Check if dependency is stable first |
| Hook output changes every render | Trace dependency chain backwards |
| Component re-renders on every keystroke | Check for inline callbacks in hook calls |

## Red Flags - STOP and Check

If you're about to:
- Pass an inline arrow function to a custom hook
- Add a callback to `useMemo`/`useCallback` deps without checking stability
- "Fix" exhaustive-deps by just adding the missing dep

**STOP. Trace the dependency chain. Is everything stable?**

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| "ESLint said add it, so I did" | Check if the dep is stable BEFORE adding |
| "It's just a small callback" | Size doesn't matter, stability does |
| "The hook should handle this" | Caller is responsible for stable refs |

## Dependency Chain Debugging

When something re-renders unexpectedly:

1. Find the `useMemo`/`useCallback` that's recreating
2. Check each dependency - which one changed?
3. Trace that dependency back - why did IT change?
4. Keep tracing until you find the unstable root
5. Wrap the root in `useCallback` with stable deps

## Real-World Impact

**The bug:** Quill editor threw `addRange(): The given range isn't in document` on every keystroke.

**Root cause:**
1. ESLint fix changed `useMemo` deps from `[toast]` to `[imageHandler]`
2. `imageHandler` depended on `insertImage` via `useCallback`
3. `insertImage` was inline (new function every render)
4. Chain: `insertImage` ↻ `imageHandler` ↻ `modules` ↻ ReactQuill re-init

**Fix:** Wrap `insertImage` in `useCallback` with `[]` deps.

**Time saved by knowing pattern:** 2+ hours of debugging → 5 minutes.
