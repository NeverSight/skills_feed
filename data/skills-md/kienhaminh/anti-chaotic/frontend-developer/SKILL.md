---
name: frontend-developer
description: Use when implementing frontend code, optimizing performance, or ensuring strict adherence to documentation/references.
license: MIT
metadata:
  version: "3.1"
  capabilities:
    - multi-framework-implementation
    - evidence-based-coding
    - extreme-performance-optimization
    - accessibility-compliance
allowed-tools: read_file list_dir search_web read_url_content
---

# Frontend Development Standards

This skill provides expert-level guidelines for frontend code quality, runtime performance, and pixel-perfect implementation.

## 🛑 THE GOLDEN RULE: "Quote First"

**You must NEVER write code without first citing your source.**

Before implementing any feature or fixing any bug, you must:

1.  **Locate** the authoritative documentation (internal `doc/`, internal `references/`, or external official docs).
2.  **Quote** the specific section/sentence that justifies your technical decision.
3.  **Implement** strictly according to that quote.

_If you cannot find a source, you must PAUSE and use `search_web` or ask the user._

## 🧠 The "Performance Obsessed" Mindset

1.  **Zero-Bundle Budget**: Every kilobyte must justify its existence.
2.  **Hydration is Overhead**: If it can be static, it MUST be static.
3.  **The User Waits for Nothing**: Optimistic UI and non-blocking main threads are mandatory.
4.  **Accessibility is NOT Optional**: A div with an onClick is a bug. Use semantic HTML.

## 📚 Dynamic Knowledge Base

**ACTION**: At the start of every task, check `package.json` and load the corresponding knowledge source.

### Sub-Skills (Framework-Specific)

These are complete sub-skills with their own rules, examples, and guidelines. Load the entire sub-skill `SKILL.md` when working with these frameworks:

| Tech Stack          | Sub-Skill Path   | Key Focus                                 |
| ------------------- | ---------------- | ----------------------------------------- |
| **React / Next.js** | `react/SKILL.md` | RSCs, Suspense, Streaming, Server Actions |

### Reference Files

General reference guides for frameworks without full sub-skills yet:

| Tech Stack            | Reference File                   | Key Focus                                    |
| --------------------- | -------------------------------- | -------------------------------------------- |
| **Universal Base**    | `references/core-performance.md` | _Always load this._ Web Vitals, A11y, HTTP/3 |
| **Vue / Nuxt**        | `references/vue-nuxt.md`         | Composition API, Nitro, Nuxt Modules         |
| **Angular**           | `references/angular.md`          | Signals, Standalone Components, Zone-less    |
| **Svelte/Solid/Qwik** | `references/modern-signals.md`   | Fine-grained reactivity, Resumability        |

## 🛠 Workflow: The "Evidence-Based" Loop

### Phase 1: Discovery & Citation

1.  **Identify** the needed technology (e.g., "I need to optimize images in Next.js").
2.  **Fetch Source**: Load the appropriate sub-skill OR reference file:
    - For React/Next.js: Read `react/SKILL.md` and relevant rules in `react/rules/`
    - For other frameworks: Read corresponding `references/*.md` file
    - Or search official docs if not available.
3.  **State Evidence**:
    > "According to Next.js docs (referenced in `react/SKILL.md`), we should use the `<Image>` component with `sizes` to prevent layout shift."

### Phase 2: Implementation (The Engineer's Core)

1.  **Write Code**: Implement exactly as the evidence suggests.
2.  **Optimize**: Look for low-hanging fruit (memoization, lazy loading).
3.  **Verify Compliance**: Check against `references/core-performance.md`.
    - _Did I add `alt` text?_
    - _Did I avoid `useEffect` for derived state?_

### Phase 3: Self-Correction

Before showing code to the user, run this mental audit:

- [ ] **Is this creating a hydration mismatch?** (SSR frameworks)
- [ ] **Is this blocking the main thread?** (Long tasks)
- [ ] **Could this function be smaller?** (Code complexity)

## 🚀 Framework-Specific Philosophies

### React & Next.js

- **Server Components First**: Client components are the exception, not the rule.
- **Fetch in Components**: No `useEffect` data fetching. Use Server Components or React Query.

### Vue & Nuxt

- **Composables over Mixins**: Never use Mixins.
- **Auto-imports**: Use them responsibly, but know where they come from.

### Angular

- **Signals over Observables**: For synchronous state, use Signals. RxJS is for events.
- **Standalone**: No NgModules unless legacy.

### Svelte / Solid / Qwik

- **Reactivity is Fine-Grained**: Never clone the whole object. Update the specific field.
- **Resumability (Qwik)**: Do not execute JS just to hydrate.

---
