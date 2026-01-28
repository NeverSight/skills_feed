---
name: zustand-expert
id: zustand-expert
version: 1.2.0
description: "Senior State Architect for React 19 and Next.js 16.1+ applications. Specialist in Zustand v5, SSR-safe stores, and slices pattern for large-scale state management."
---

# 🧠 Skill: zustand-expert

## Description
Senior state architect specializing in Zustand v5 for modern React applications. Expert in solving hydration mismatches, preventing state leakage in SSR (Next.js), and implementing scalable architectures using the Slices Pattern and advanced middleware (Persist, Immer).

## Core Priorities
1.  **SSR Safety (Anti-Singleton)**: Preventing shared state between requests in Next.js by using per-request stores via React Context.
2.  **Hydration Integrity**: Managing persistence and asynchronous rehydration to ensure sub-100ms LCP without flickering.
3.  **Modular Scalability**: Enforcing the Slices Pattern for complex domain state.
4.  **Performance Optimization**: Strategic use of selectors and `useSyncExternalStore` (Zustand v5 native).

## 🏆 Top 5 Gains in Zustand v5 (2026)

1.  **Native `useSyncExternalStore`**: Full support for React 18/19 concurrent rendering with zero "tearing" issues.
2.  **Smaller Footprint**: Dropped legacy support, leading to a leaner, faster bundle.
3.  **Improved Type Safety**: Native TypeScript support for combined stores and middleware.
4.  **Context-Store Pattern**: Official standard for SSR to avoid user-data leakage.
5.  **Manual Rehydration Control**: `skipHydration: true` for fine-grained control over when persisted state hits the UI.

## Table of Contents & Detailed Guides

### 1. [SSR & Next.js 16 Pattern](./references/1-ssr-nextjs.md) — **CRITICAL**
- The Provider Pattern (Ref-based store creation)
- Preventing Singleton data leaks
- Initializing state from Server Props

### 2. [The Slices Pattern](./references/2-slices-pattern.md) — **HIGH**
- Modularizing large stores
- Type-safe combined states
- Sharing state between slices

### 3. [Persistence & Hydration](./references/3-persistence.md) — **HIGH**
- `persist` middleware with `skipHydration`
- Migration strategies for schema changes
- Handling Hydration Mismatch in Next.js

### 4. [Middleware & Immutability](./references/4-middleware.md) — **MEDIUM**
- `immer` for complex nested state
- Custom middleware for logging/analytics
- Testing stores with Vitest/Jest

## Quick Reference: The "Do's" and "Don'ts"

| **Don't** | **Do** |
| :--- | :--- |
| `export const useStore = create(...)` | Use `StoreContext` for SSR |
| Monolithic store file | Use Slices Pattern |
| `useStore(state => state)` (Full object) | Use Atomic Selectors (`state.id`) |
| Direct Mutation | Use `immer` middleware or functional updates |
| `useEffect` for hydration sync | Use `persist` with `skipHydration` |
| Store read in RSC | Use Props to pass data to Client Components |

---
*Optimized for Zustand v5 and React 19.2+.*
*Updated: January 22, 2026 - 15:03*
