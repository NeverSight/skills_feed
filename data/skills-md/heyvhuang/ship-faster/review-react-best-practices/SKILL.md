---
name: review-react-best-practices
description: "Review or refactor React / Next.js code for performance and reliability using a prioritized rule library (waterfalls, bundle size, server/client data fetching, re-renders, rendering). Use when writing React components, Next.js pages (App Router), optimizing bundle size, improving performance, or doing a React/Next.js performance review."
---

# React Best Practices Review (Performance-First)

Use this skill to turn “React feels slow / Next.js page is heavy / too many requests” into a **repeatable, prioritized review**.

This skill is intentionally built like a rule library:

- `SKILL.md`: how to review + how to search rules
- `references/rules/*`: one rule per file (taggable, sortable, easy to evolve)

## When to apply

Use when:

- Building or refactoring React components
- Working in Next.js (App Router) on RSC boundaries, Server Actions, data fetching
- Reviewing PRs for performance regressions
- Bundle size increases / slow HMR / cold start issues
- UI jank / unnecessary re-renders / hydration issues

## Review method (prioritized)

1. **Start with CRITICAL** rules first (waterfalls + bundle).
2. Only then go to **HIGH** (server patterns + serialization).
3. Then **MEDIUM** (re-render + rendering).
4. Then **LOW-MEDIUM** micro-optimizations (JS hot paths).

Section ordering lives in: [`references/rules/_sections.md`](references/rules/_sections.md)

## How to use the rules efficiently

### Search by keyword

```bash
rg -n "waterfall|Promise\\.all|defer await" references/rules
rg -n "barrel|optimizePackageImports|dynamic" references/rules
rg -n "cache\\(|React\\.cache|serialization|RSC" references/rules
rg -n "memo\\(|useMemo|useCallback|dependencies" references/rules
```

### Search by tag

Each rule has `tags:` in YAML frontmatter.

```bash
rg -n "tags:.*bundle" references/rules
rg -n "tags:.*rerender" references/rules
```

## Output format (recommended)

When reviewing code, output:

1. **Summary** (1 paragraph)
2. **Critical fixes** (must-fix, biggest wins)
3. **High impact** (should-fix)
4. **Medium / Low** (nice-to-have)

For each issue include:

- Rule name (and file under `references/rules/`)
- Location (`path:line`)
- Why it matters (latency / bundle / CPU / UX)
- Minimal fix direction (prefer small diffs)

If running in a Ship Faster run directory, persist the report to:

- `run_dir/evidence/react-best-practices-review.md`

## Rule library

Rules live in:

- [`references/rules/`](references/rules/)
- Rule template: [`references/rules/_template.md`](references/rules/_template.md)
