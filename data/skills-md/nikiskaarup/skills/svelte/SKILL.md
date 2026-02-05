---
name: svelte
description: Guide Svelte 5 component development with runes, props, and performance-aware patterns.
---

# Svelte 5

## Purpose
Guide responses for Svelte 5 component authoring, reactivity, and TypeScript usage based on official docs, assuming the project already uses Svelte 5.

## Scope
- Included: runes ($state, $derived, $effect), props, events, snippets, reactivity, effects, TypeScript usage.
- Excluded: SvelteKit topics unless required by user context, and Svelte 4 legacy patterns.

## When to Use
- You are building or maintaining Svelte 5 components.
- You need guidance on runes, props, events, snippets, or reactivity in Svelte 5.

## Response Guidance
- Prefer runes ($state, $derived, $effect) over legacy $: and implicit reactivity.
- Use $props() destructuring for props; avoid export let unless handling legacy code.
- Use DOM event attributes (onclick, oninput) and component callback props instead of createEventDispatcher.
- Favor snippets (children + {@render ...}) over slots.
- Use $bindable for two-way bindings and avoid mutating non-owned state.

## Performance Gotchas
- Deep $state proxies can be expensive for large objects/arrays; use $state.raw when you don’t need deep reactivity.
- Avoid $effect for simple derived values; use $derived/$derived.by to keep updates precise.
- Be mindful of heavy work in $derived expressions; keep them side-effect free and cheap.
- Async work inside $effect does not track dependencies after await; read dependencies synchronously.
- Avoid recreating objects/functions in templates that cause reactive churn.
- Use $state.snapshot when passing state to non-reactive libraries that expect plain objects.

## TypeScript Guidance
- Prefer explicit prop interfaces with $props() destructuring:

```ts
interface Props {
  class?: ClassValue;
  text: string;
}

let { class: className, text }: Props = $props();
```

- If using snippet props, type them with Snippet:

```ts
import type { Snippet } from 'svelte';

interface Props {
  children?: Snippet;
}
```

- Use .svelte.ts and .svelte.js for shared reactive logic; do not export reassigned $state directly.
- For wrapper component typing, use DOM types from svelte/elements when needed.
- Recommend the Svelte VS Code extension and the TypeScript plugin for best editor support.

## References
- https://svelte.dev/docs/svelte/llms.txt
