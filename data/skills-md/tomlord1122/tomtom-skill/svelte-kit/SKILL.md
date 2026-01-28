---
name: svelte-kit
description: Svelte 5 and SvelteKit syntax expert. Use when working with .svelte files, runes syntax ($state, $derived, $effect), SvelteKit routing, SSR, or component design.
---

# Svelte/SvelteKit Expert

Expert assistant for Svelte 5 runes syntax, SvelteKit routing, SSR/SSG strategies, and component design patterns.

## How It Works

1. Analyzes user's Svelte/SvelteKit code or questions
2. Queries Context7 documentation (`/websites/svelte_dev`) for accurate, up-to-date information
3. Provides solutions using Svelte 5 runes syntax (not legacy stores)
4. Explains SSR vs CSR implications when relevant

## Project Setup

**Preferred Package Manager:** bun

```bash
# Create new SvelteKit project
bunx sv create my-app
cd my-app
bun install
bun run dev
```

## Documentation Resources

**Context7 Library ID:** `/websites/svelte_dev` (5523 snippets, Score: 91)

**Official llms.txt Resources:**
- `https://svelte.dev/docs/llms` - Documentation index
- `https://svelte.dev/docs/llms-full.txt` - Complete documentation
- `https://svelte.dev/docs/llms-small.txt` - Compressed (~120KB)

## Quick Reference

### Svelte 5 Runes

```svelte
<script>
  // Reactive state
  let count = $state(0);

  // Derived values (auto-updates when dependencies change)
  let doubled = $derived(count * 2);

  // Side effects
  $effect(() => {
    console.log(`Count is now ${count}`);
  });

  // Props with defaults
  let { name = 'World', onClick } = $props();

  // Bindable props (two-way binding)
  let { value = $bindable() } = $props();
</script>
```

### SvelteKit Routing

```
src/routes/
├── +page.svelte          # /
├── +page.server.ts       # Server load function
├── +layout.svelte        # Root layout
├── about/+page.svelte    # /about
├── blog/
│   ├── +page.svelte      # /blog
│   └── [slug]/
│       ├── +page.svelte  # /blog/:slug
│       └── +page.ts      # Universal load
└── api/posts/+server.ts  # API endpoint
```

### Load Functions

```typescript
// +page.server.ts - Server-only
export async function load({ params, locals, fetch }) {
  const post = await fetch(`/api/posts/${params.slug}`);
  return { post: await post.json() };
}

// +page.ts - Universal (server + client)
export async function load({ params, fetch }) {
  const res = await fetch(`/api/posts/${params.slug}`);
  return { post: await res.json() };
}
```

### Form Actions

```typescript
// +page.server.ts
export const actions = {
  default: async ({ request }) => {
    const data = await request.formData();
    const email = data.get('email');
    return { success: true };
  },
  delete: async ({ params }) => {
    // Handle delete
  }
};
```

## Present Results to User

When answering Svelte/SvelteKit questions:
- Provide complete, runnable code examples
- Use Svelte 5 runes syntax by default
- Explain the difference between server and universal load functions
- Note any breaking changes between SvelteKit versions
- Include TypeScript types when applicable

## Troubleshooting

**"Cannot use $state outside of component"**
- Runes only work inside `.svelte` files or `.svelte.ts` files

**"Hydration mismatch"**
- Ensure server and client render the same content initially
- Check for browser-only code running during SSR

**"Load function not running"**
- Verify file naming: `+page.ts` or `+page.server.ts`
- Check if `load` function is properly exported
