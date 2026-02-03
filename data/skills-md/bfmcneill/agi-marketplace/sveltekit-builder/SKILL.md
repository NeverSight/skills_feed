---
name: sveltekit-builder
description: Use when building SvelteKit apps with Svelte 5. Covers runes, SSR, forms, and stack patterns (Kysely, Better Auth, shadcn-svelte).
license: MIT
metadata:
  author: rosa
  version: "1.0"
---

# SvelteKit Builder

Expert guidance for building production-ready SvelteKit applications with Svelte 5 runes, remote functions, and modern best practices.

## When to Use This Skill

Use this skill when:
- **Scaffolding new SvelteKit projects** with Svelte 5
- **Migrating from Svelte 4 to Svelte 5** (reactivity model changed fundamentally)
- **Implementing remote functions** (SvelteKit's type-safe server functions)
- **Optimizing performance** (bundle size, SSR, hydration, rendering)
- **Applying security patterns** (XSS prevention, input validation, secret management)
- **Integrating recommended stack** (Kysely, Better Auth, shadcn-svelte, Lucide, AI SDK)
- **Code reviews** where Svelte/SvelteKit patterns need validation
- **Debugging reactivity issues** or SSR hydration mismatches

## Knowledge Base Structure

This skill contains **105+ best practice rules** organized by impact and category:

### Svelte 5 Specific (`svelte5/`) - 66 rules

**CRITICAL Impact:**
- **Reactivity** (`reactivity-*`): $state, $derived, $effect - The foundation changed completely from Svelte 4
- **Remote Functions** (`remote-*`): Type-safe server functions in .remote.ts files
- **Security** (`template-html-*`): XSS prevention with {@html}
- **Async & Data Fetching** (`async-*`): Waterfalls, {#await}, svelte:boundary

**HIGH Impact:**
- **Component Patterns** (`component-*`): $props, callbacks, snippets (not slots anymore)
- **SSR & Hydration** (`ssr-*`): Server rendering, hydration mismatches
- **SvelteKit Patterns** (`sveltekit-*`): Load functions, form actions, error handling
- **Actions** (`actions-*`): Reusable DOM behavior
- **Accessibility** (`a11y-*`): Compiler warnings

**MEDIUM Impact:**
- **State Management** (`state-*`): Shared state, context, stores vs runes
- **Rendering Optimization** (`rendering-*`): Keyed {#each}, unnecessary reactivity
- **CSS & Styling** (`css-*`): Scoped styles, theming
- **Forms** (`forms-*`): Form handling patterns
- **Transitions & Animation** (`transitions-*`): Smooth animations
- **Events** (`events-*`): onclick vs on:click
- **Special Elements** (`elements-*`): svelte:head, svelte:window, svelte:body
- **Template Patterns** (`template-*`): {@const}, {#key}, {#if}

**LOWER Impact:**
- **TypeScript** (`typescript-*`): Props interfaces, generics with snippets

### Framework-Agnostic (`general/`) - 15 rules

**HIGH Impact:**
- **Bundle Optimization** (`bundle-*`): Dynamic imports, tree-shaking, lazy loading
- **Security** (`security-*`): Input sanitization
- **Rendering Performance** (`rendering-*`): content-visibility, layout thrashing

**LOWER Impact:**
- **JavaScript Performance** (`js-*`): Promise.all, Set/Map, debouncing

### Third-Party Stack (`third-party/`) - 24+ rules

Opinionated patterns for the recommended SvelteKit stack:

- **Kysely** (`kysely/*`): Type-safe SQL, connection pooling, transactions
- **Better Auth** (`better-auth/*`): Session management, route protection, OAuth
- **shadcn-svelte** (`shadcn-svelte/*`): Accessible components, dark mode, Superforms
- **Lucide Svelte** (`lucide-svelte/*`): Tree-shakeable icons
- **AI SDK** (`ai-sdk/*`): Streaming, tool validation, API key management

## How to Use This Skill

### 1. Start with Critical Rules

When working on SvelteKit projects, **always check CRITICAL impact rules first**:

```bash
references/svelte5/reactivity-use-state-explicit.md
references/svelte5/remote-separate-files.md
references/svelte5/remote-validate-inputs.md
references/svelte5/template-html-xss.md
references/svelte5/sveltekit-parallel-load.md
```

These prevent silent bugs, security vulnerabilities, and performance issues.

### 2. Reference Rules by Category

When implementing specific features, consult the relevant category:

- **Building a form?** → Check `forms-*` and `remote-*` (form actions)
- **Data fetching?** → Check `async-*` and `sveltekit-*` (load functions)
- **Component communication?** → Check `component-*` ($props, callbacks, snippets)
- **Performance issues?** → Check `bundle-*`, `rendering-*`, and `async-parallel-fetching`
- **Hydration errors?** → Check `ssr-*` rules

### 3. Use the Sections Guide

Refer to `references/_sections.md` for:
- Complete category breakdown
- Impact levels for each prefix
- Rule counts per category
- Comparison with React patterns (for developers migrating)

### 4. Follow Rule Format

Each rule file contains:
- **Impact level** and description
- **Explanation** of why it matters
- **Incorrect example** showing the anti-pattern
- **Correct example** showing the best practice
- **Reference links** to official documentation

## Key Principles

### Svelte 5 Migration Critical Points

**Reactivity is no longer automatic:**
- Svelte 4: `let count = 0;` was reactive
- Svelte 5: Must use `let count = $state(0);` explicitly

**No more createEventDispatcher:**
- Svelte 4: `dispatch('change', value)`
- Svelte 5: Pass callbacks as props

**Slots are now snippets:**
- Svelte 4: `<slot name="header" />`
- Svelte 5: `{@render header()}`

**Effects need cleanup:**
- Always return cleanup functions from `$effect` to prevent memory leaks

### Remote Functions (SvelteKit's Server Functions)

Remote functions are SvelteKit's type-safe server functions (similar to React Server Actions):

1. **Always use `.remote.ts` files** - Never colocate with client code
2. **Validate inputs with Zod** - Prevent injection attacks
3. **Use `query()` for reads** - Automatically cached
4. **Use `form()` for mutations** - Progressive enhancement with `use:enhance`
5. **Batch queries** - Avoid N+1 problems

### Performance Priorities

1. **Bundle size** - Dynamic imports, tree-shaking (HIGH impact on TTI)
2. **Parallel data fetching** - Use Promise.all in load functions (CRITICAL)
3. **SSR optimization** - Avoid hydration mismatches, use hydratable()
4. **Strategic boundaries** - Place {#await} and svelte:boundary wisely

## Common Patterns

### Data Fetching Pattern
```svelte
<script lang="ts">
  import { getUsers, createUser } from './users.remote.ts';
  
  // query() returns a promise - use with {#await}
  const users = getUsers();
</script>

{#await users}
  <p>Loading...</p>
{:then items}
  {#each items as user (user.id)}
    <p>{user.name}</p>
  {/each}
{:catch error}
  <p>Error: {error.message}</p>
{/await}
```

### Form with Progressive Enhancement
```svelte
<script lang="ts">
  import { createUser } from './users.remote.ts';
</script>

<form {...createUser}>
  <input name="name" required />
  <input name="email" type="email" required />
  <button>Create User</button>
</form>
```

### Component with Props
```svelte
<script lang="ts">
  interface Props {
    title: string;
    count?: number;
    onUpdate?: (value: number) => void;
  }
  
  let { title, count = 0, onUpdate }: Props = $props();
  let localCount = $state(count);
  
  function increment() {
    localCount++;
    onUpdate?.(localCount);
  }
</script>

<h2>{title}</h2>
<button onclick={increment}>Count: {localCount}</button>
```

## Reference Files

All rules are in the `references/` directory:

- `references/_sections.md` - Complete category breakdown and comparison tables
- `references/_template.md` - Template for creating new rules
- `references/svelte5/*.md` - 66 Svelte 5 and SvelteKit rules
- `references/general/*.md` - 15 framework-agnostic rules
- `references/third-party/*/` - 24+ rules for Kysely, Better Auth, shadcn-svelte, Lucide, AI SDK

## When NOT to Use Stores

Svelte 5 runes (`$state`, `$derived`, `$effect`) should be preferred over stores for most use cases:

**Use runes when:**
- Component-local state
- Derived computations
- Simple shared state in `.svelte.js` files

**Use stores when:**
- Interoperating with Svelte 4 libraries
- Need subscribe/unsubscribe lifecycle
- Complex pub/sub patterns

See `references/svelte5/state-stores-vs-runes.md` for details.

## Integration with Third-Party Libraries

This skill includes opinionated guidance for the recommended SvelteKit stack. When using these libraries, consult the relevant third-party rules:

- **Database queries** → `references/third-party/kysely/`
- **Authentication** → `references/third-party/better-auth/`
- **UI components** → `references/third-party/shadcn-svelte/`
- **Icons** → `references/third-party/lucide-svelte/`
- **AI/LLM features** → `references/third-party/ai-sdk/`

## Progressive Disclosure

This SKILL.md provides high-level guidance. Reference individual rule files for:
- Detailed explanations
- Code examples (Incorrect vs Correct)
- Impact descriptions
- Official documentation links

Agents should load reference files on-demand based on the specific task at hand, keeping context efficient.
