---
name: debug:svelte
description: Debug Svelte application issues systematically. This skill helps diagnose and resolve Svelte-specific problems including reactivity failures, runes issues ($state, $derived, $effect), store subscription memory leaks, SSR hydration mismatches, and compiler warnings. Covers both Svelte 4 legacy patterns and Svelte 5 runes-based reactivity. Provides debugging tools like $inspect(), {@debug} tags, and svelte-check CLI usage.
---

# Svelte Debugging Guide

This guide provides a systematic approach to debugging Svelte applications, with special emphasis on Svelte 5 runes and reactivity patterns.

## Common Error Patterns

### 1. Reactivity Not Triggering

**Symptoms:**
- UI doesn't update when state changes
- Computed values are stale
- Event handlers seem to fire but nothing happens

**Root Causes:**

```svelte
<!-- WRONG: Mutating object properties without reassignment (Svelte 4) -->
<script>
  let user = { name: 'John' };
  function updateName() {
    user.name = 'Jane';  // Won't trigger reactivity in some cases
  }
</script>

<!-- CORRECT: Reassign the entire object -->
<script>
  let user = { name: 'John' };
  function updateName() {
    user = { ...user, name: 'Jane' };  // Triggers reactivity
  }
</script>
```

**Svelte 5 Fix with Runes:**
```svelte
<script>
  let user = $state({ name: 'John' });
  function updateName() {
    user.name = 'Jane';  // Deep reactivity works with $state
  }
</script>
```

### 2. Runes ($state, $derived, $effect) Issues

**Error: "Cannot use runes in .js files"**
```bash
# WRONG: Using runes in regular JS file
# utils.js
export const count = $state(0);  // ERROR!

# CORRECT: Rename to .svelte.js
# utils.svelte.js
export const count = $state(0);  // Works!
```

**Error: "Class properties not reactive"**
```javascript
// WRONG: $state wrapper on class instance has no effect
let instance = $state(new MyClass());  // Properties NOT reactive

// CORRECT: Make class properties reactive internally
class MyClass {
  count = $state(0);
  name = $state('');
}
let instance = new MyClass();  // Properties ARE reactive
```

**Error: "Infinite loop in $derived"**
```svelte
<script>
  let count = $state(0);

  // WRONG: Modifying state inside $derived
  let doubled = $derived(() => {
    count++;  // ERROR: Causes infinite loop!
    return count * 2;
  });

  // CORRECT: Pure computation only
  let doubled = $derived(count * 2);
</script>
```

**Error: "Infinite update loop in $effect"**
```svelte
<script>
  import { untrack } from 'svelte';

  let count = $state(0);
  let log = $state([]);

  // WRONG: Reading and writing same state
  $effect(() => {
    log.push(count);  // Infinite loop!
  });

  // CORRECT: Use untrack() to break dependency
  $effect(() => {
    untrack(() => {
      log.push(count);
    });
  });
</script>
```

**Error: "Cannot export reassigned $state"**
```javascript
// WRONG: Exporting reassigned state
// store.svelte.js
export let count = $state(0);  // ERROR if reassigned

// CORRECT: Wrap in object for mutation
export const state = $state({ count: 0 });
// Or use getter/setter
let _count = $state(0);
export const count = {
  get value() { return _count; },
  set value(v) { _count = v; }
};
```

### 3. Store Subscription Problems (Svelte 4)

**Memory Leak: Forgotten Unsubscribe**
```svelte
<script>
  import { myStore } from './stores';
  import { onDestroy } from 'svelte';

  // WRONG: No cleanup
  myStore.subscribe(value => console.log(value));

  // CORRECT: Clean up subscription
  const unsubscribe = myStore.subscribe(value => console.log(value));
  onDestroy(unsubscribe);

  // BEST: Use auto-subscription
  $: value = $myStore;  // Svelte handles cleanup
</script>
```

**Store Not Updating**
```javascript
// WRONG: Mutating store value
import { writable } from 'svelte/store';
const items = writable([]);
items.update(arr => {
  arr.push('new item');  // Mutation, may not trigger
  return arr;
});

// CORRECT: Return new array
items.update(arr => [...arr, 'new item']);
```

### 4. SSR Hydration Mismatches

**Symptoms:**
- Console warning about hydration mismatch
- Content flickers on page load
- Interactive elements don't work initially

**Common Causes:**
```svelte
<script>
  import { browser } from '$app/environment';

  // WRONG: Different content server vs client
  let date = new Date().toLocaleString();  // Different on each render!

  // CORRECT: Initialize consistently, update on mount
  let date = '';
  import { onMount } from 'svelte';
  onMount(() => {
    date = new Date().toLocaleString();
  });

  // OR: Guard browser-only code
  {#if browser}
    <BrowserOnlyComponent />
  {/if}
</script>
```

**LocalStorage Access**
```svelte
<script>
  import { browser } from '$app/environment';

  // WRONG: Accessing localStorage during SSR
  let theme = localStorage.getItem('theme');  // ERROR on server!

  // CORRECT: Guard with browser check
  let theme = $state('light');
  if (browser) {
    theme = localStorage.getItem('theme') ?? 'light';
  }
</script>
```

### 5. Compiler Errors

**"'foo' is not defined"**
```svelte
<!-- Check for typos in variable names -->
<!-- Check script context vs module context -->
<script context="module">
  // This runs once, not per component
  export const sharedValue = 'shared';
</script>

<script>
  // This runs per component instance
  let instanceValue = 'instance';
</script>
```

**"Cannot bind to property"**
```svelte
<script>
  // WRONG: Binding to non-bindable prop
  let { value } = $props();
</script>
<input bind:value />  <!-- Error if parent doesn't use bind: -->

<!-- CORRECT: Declare as bindable -->
<script>
  let { value = $bindable() } = $props();
</script>
```

## Debugging Tools

### 1. Svelte DevTools Browser Extension

Install from Chrome Web Store or Firefox Add-ons. Provides:
- Component tree visualization
- Props and state inspection
- Store value monitoring
- Event tracking

### 2. The $inspect() Rune (Svelte 5)

```svelte
<script>
  let count = $state(0);
  let user = $state({ name: 'John' });

  // Log when values change
  $inspect(count);  // Logs: "count", 0, then changes

  // Custom effect with .with()
  $inspect(user).with(console.trace);  // Show stack trace

  // Multiple values
  $inspect(count, user);
</script>
```

### 3. The {@debug} Tag

```svelte
<script>
  let items = ['a', 'b', 'c'];
  let filter = '';
</script>

<!-- Pauses execution with devtools open -->
{@debug items, filter}

<!-- Shows in console when values change -->
{#each items as item}
  {@debug item}
  <li>{item}</li>
{/each}
```

### 4. Console Methods

```svelte
<script>
  import { onMount, beforeUpdate, afterUpdate, onDestroy } from 'svelte';

  // Track component lifecycle
  onMount(() => console.log('Component mounted'));
  beforeUpdate(() => console.log('Before update'));
  afterUpdate(() => console.log('After update'));
  onDestroy(() => console.log('Component destroyed'));

  // Reactive statement debugging
  $: console.log('Count changed:', count);

  // Object inspection
  $: console.table(items);
  $: console.dir(complexObject, { depth: null });
</script>
```

### 5. Vite Dev Server

```bash
# Start with verbose logging
npm run dev -- --debug

# Clear cache if issues persist
rm -rf node_modules/.vite
npm run dev
```

### 6. svelte-check CLI

```bash
# Type checking and diagnostics
npx svelte-check

# Watch mode
npx svelte-check --watch

# With specific tsconfig
npx svelte-check --tsconfig ./tsconfig.json

# Output format for CI
npx svelte-check --output human-verbose
```

### 7. VS Code Debugging

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "chrome",
      "request": "launch",
      "name": "Debug Svelte",
      "url": "http://localhost:5173",
      "webRoot": "${workspaceFolder}",
      "sourceMaps": true
    }
  ]
}
```

Enable breakpoints in .svelte files:
1. Open VS Code settings
2. Search for `debug.allowBreakpointsEverywhere`
3. Enable the setting

## The Four Phases (Svelte-specific)

### Phase 1: Gather Information

```bash
# Check Svelte version
npm list svelte

# Check for type errors
npx svelte-check --output human-verbose

# Check browser console for warnings/errors
# Look for:
# - Hydration warnings
# - Reactivity warnings
# - Unhandled promise rejections

# Check component props
$inspect($$props);  # Svelte 5
```

**Questions to Answer:**
- Is this a Svelte 4 or Svelte 5 project?
- Are you using SvelteKit or standalone Svelte?
- Does the issue occur in dev, build, or both?
- Is it SSR-related (works in CSR but not SSR)?

### Phase 2: Isolate the Problem

```svelte
<!-- Create minimal reproduction -->
<script>
  // Strip component to minimum code that reproduces issue
  let count = $state(0);

  // Add debugging
  $inspect(count);

  function handleClick() {
    console.log('Before:', count);
    count++;
    console.log('After:', count);
  }
</script>

<button onclick={handleClick}>
  Count: {count}
</button>
```

**Isolation Strategies:**
1. Comment out unrelated code
2. Remove external dependencies
3. Test in fresh component
4. Check if issue is component-specific or global

### Phase 3: Form Hypothesis and Test

**Common Hypotheses:**

| Symptom | Hypothesis | Test |
|---------|------------|------|
| No reactivity | Missing $state | Add $state wrapper |
| Infinite loop | Circular dependency | Check $derived/$effect |
| SSR error | Browser API in SSR | Add browser guard |
| Props not reactive | Destructured props | Use $props() correctly |
| Store stale | Subscription issue | Use auto-subscription $ |

```svelte
<script>
  // Hypothesis: Props not updating
  // Test 1: Log prop changes
  let { value } = $props();
  $effect(() => {
    console.log('Prop value changed:', value);
  });

  // Test 2: Check if parent is reactive
  // Add $inspect in parent component
</script>
```

### Phase 4: Fix and Verify

**Verification Checklist:**
- [ ] Issue no longer occurs
- [ ] No new console warnings
- [ ] svelte-check passes
- [ ] Works in both dev and build
- [ ] Works in SSR (if applicable)
- [ ] No memory leaks (check DevTools)

```bash
# Full verification
npx svelte-check
npm run build
npm run preview  # Test production build
```

## Quick Reference Commands

### Diagnostic Commands

```bash
# Check Svelte/SvelteKit versions
npm list svelte @sveltejs/kit

# Run type checking
npx svelte-check

# Run type checking with watch
npx svelte-check --watch

# Check for outdated packages
npm outdated

# Clear caches
rm -rf node_modules/.vite .svelte-kit
npm run dev
```

### Common Fixes

```bash
# Reset node_modules
rm -rf node_modules package-lock.json
npm install

# Regenerate SvelteKit types
npx svelte-kit sync

# Update Svelte to latest
npm update svelte @sveltejs/kit

# Check for peer dependency issues
npm ls
```

### Debug Environment Variables

```bash
# Enable Vite debug mode
DEBUG=vite:* npm run dev

# Enable SvelteKit debug mode
DEBUG=kit:* npm run dev

# Both
DEBUG=vite:*,kit:* npm run dev
```

## Svelte 5 Migration Pitfalls

### From let to $state

```svelte
<!-- Svelte 4 -->
<script>
  let count = 0;  // Implicitly reactive at top level
</script>

<!-- Svelte 5 -->
<script>
  let count = $state(0);  // Explicitly reactive
</script>
```

### From $: to $derived/$effect

```svelte
<!-- Svelte 4 -->
<script>
  $: doubled = count * 2;  // Reactive derivation
  $: console.log(count);   // Reactive side effect
</script>

<!-- Svelte 5 -->
<script>
  let doubled = $derived(count * 2);  // Derivation
  $effect(() => {
    console.log(count);  // Side effect
  });
</script>
```

### From export let to $props

```svelte
<!-- Svelte 4 -->
<script>
  export let name = 'default';
  export let value;
</script>

<!-- Svelte 5 -->
<script>
  let { name = 'default', value } = $props();
</script>
```

### From createEventDispatcher to Callback Props

```svelte
<!-- Svelte 4 -->
<script>
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();
  function handleClick() {
    dispatch('click', { data: 'value' });
  }
</script>

<!-- Svelte 5 -->
<script>
  let { onclick } = $props();
  function handleClick() {
    onclick?.({ data: 'value' });
  }
</script>
```

## Reactive Collections (Svelte 5)

```javascript
// Import reactive versions of Map, Set, etc.
import { SvelteMap, SvelteSet, SvelteURL } from 'svelte/reactivity';

// Use instead of native collections
let items = new SvelteMap();
let tags = new SvelteSet();

// These are deeply reactive
items.set('key', { nested: 'value' });
tags.add('new-tag');
```

## Form Handling with tick()

```svelte
<script>
  import { tick } from 'svelte';

  let value = $state('');

  async function submitWithValue(newValue) {
    value = newValue;
    await tick();  // Wait for DOM to update
    form.submit();  // Now form has updated value
  }
</script>
```

## Sources

- [Svelte @debug Documentation](https://svelte.dev/docs/svelte/@debug)
- [SvelteKit Breakpoint Debugging](https://svelte.dev/docs/kit/debugging)
- [Svelte 5 Migration Guide](https://svelte.dev/docs/svelte/v5-migration-guide)
- [Svelte 5 States: Avoiding Common Reactivity Traps](https://jamesy.dev/blog/svelte-5-states-avoiding-common-reactivity-traps)
- [The Guide to Svelte Runes](https://sveltekit.io/blog/runes)
- [Introducing Runes](https://svelte.dev/blog/runes)
- [Exploring the Magic of Runes in Svelte 5](https://blog.logrocket.com/exploring-runes-svelte-5/)
