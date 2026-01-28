---
name: auto-animate
description: |
  Zero-config animations for React, Vue, Solid, Svelte, Preact with @formkit/auto-animate (3.28kb).
  Prevents 10+ documented errors: SSR/Next.js imports, conditional parents, missing keys, flexbox width,
  table display, Jest/esbuild config, CSS position conflicts, Vue/Nuxt registration, Angular ESM.

  Use when: animating lists/accordions/toasts/forms, troubleshooting SSR animation errors, need
  accessible animations (auto prefers-reduced-motion), or want drop-in transitions without Motion overhead.
license: MIT
metadata:
  version: 1.1.0
  last_verified: 2025-11-22
  package_version: 0.9.0
  framework_support: React, Vue, Solid, Svelte, Preact
  keywords:
    - auto-animate
    - "@formkit/auto-animate"
    - formkit
    - zero-config-animation
    - solid support
    - preact support
    - ssr animation errors
    - conditional parent error
    - missing keys animation
    - flexbox width animation
    - table row animation
    - jest auto-animate
    - esbuild auto-animate
    - vue nuxt auto-animate
    - angular esm auto-animate
    - prefers-reduced-motion
    - accessible-animations
    - cloudflare-workers-animation
    - nextjs-animation-ssr
---

# AutoAnimate - Error Prevention Guide

**Package**: @formkit/auto-animate@0.9.0 (Sept 2025)
**Frameworks**: React, Vue, Solid, Svelte, Preact
**Last Updated**: 2025-11-22

---

## SSR-Safe Pattern (Critical for Cloudflare Workers/Next.js)

```tsx
// Use client-only import to prevent SSR errors
import { useState, useEffect } from "react";

export function useAutoAnimateSafe<T extends HTMLElement>() {
  const [parent, setParent] = useState<T | null>(null);

  useEffect(() => {
    if (typeof window !== "undefined" && parent) {
      import("@formkit/auto-animate").then(({ default: autoAnimate }) => {
        autoAnimate(parent);
      });
    }
  }, [parent]);

  return [parent, setParent] as const;
}
```

**Why this matters**: Prevents Issue #1 (SSR/Next.js import errors). AutoAnimate uses DOM APIs not available on server.

---

## Known Issues Prevention (10 Documented Errors)

This skill prevents **10+** documented issues:

### Issue #1: SSR/Next.js Import Errors
**Error**: "Can't import the named export 'useEffect' from non EcmaScript module"
**Source**: https://github.com/formkit/auto-animate/issues/55
**Why It Happens**: AutoAnimate uses DOM APIs not available on server
**Prevention**: Use dynamic imports (see `templates/vite-ssr-safe.tsx`)

### Issue #2: Conditional Parent Rendering
**Error**: Animations don't work when parent is conditional
**Source**: https://github.com/formkit/auto-animate/issues/8
**Why It Happens**: Ref can't attach to non-existent element
**Prevention**:
```tsx
// ❌ Wrong
{showList && <ul ref={parent}>...</ul>}

// ✅ Correct
<ul ref={parent}>{showList && items.map(...)}</ul>
```

### Issue #3: Missing Unique Keys
**Error**: Items don't animate correctly or flash
**Source**: Official docs
**Why It Happens**: React can't track which items changed
**Prevention**: Always use unique, stable keys (`key={item.id}`)

### Issue #4: Flexbox Width Issues
**Error**: Elements snap to width instead of animating smoothly
**Source**: Official docs
**Why It Happens**: `flex-grow: 1` waits for surrounding content
**Prevention**: Use explicit width instead of flex-grow for animated elements

### Issue #5: Table Row Display Issues
**Error**: Table structure breaks when removing rows
**Source**: https://github.com/formkit/auto-animate/issues/7
**Why It Happens**: Display: table-row conflicts with animations
**Prevention**: Apply to `<tbody>` instead of individual rows, or use div-based layouts

### Issue #6: Jest Testing Errors
**Error**: "Cannot find module '@formkit/auto-animate/react'"
**Source**: https://github.com/formkit/auto-animate/issues/29
**Why It Happens**: Jest doesn't resolve ESM exports correctly
**Prevention**: Configure `moduleNameMapper` in jest.config.js

### Issue #7: esbuild Compatibility
**Error**: "Path '.' not exported by package"
**Source**: https://github.com/formkit/auto-animate/issues/36
**Why It Happens**: ESM/CommonJS condition mismatch
**Prevention**: Configure esbuild to handle ESM modules properly

### Issue #8: CSS Position Side Effects
**Error**: Layout breaks after adding AutoAnimate
**Source**: Official docs
**Why It Happens**: Parent automatically gets `position: relative`
**Prevention**: Account for position change in CSS or set explicitly

### Issue #9: Vue/Nuxt Registration Errors
**Error**: "Failed to resolve directive: auto-animate"
**Source**: https://github.com/formkit/auto-animate/issues/43
**Why It Happens**: Plugin not registered correctly
**Prevention**: Proper plugin setup in Vue/Nuxt config (see references/)

### Issue #10: Angular ESM Issues
**Error**: Build fails with "ESM-only package"
**Source**: https://github.com/formkit/auto-animate/issues/72
**Why It Happens**: CommonJS build environment
**Prevention**: Configure ng-packagr for Angular Package Format

---

## Critical Rules (Error Prevention)

### Always Do

✅ **Use unique, stable keys** - `key={item.id}` not `key={index}`
✅ **Keep parent in DOM** - Parent ref element always rendered
✅ **Client-only for SSR** - Dynamic import for server environments
✅ **Respect accessibility** - Keep `disrespectUserMotionPreference: false`
✅ **Test with motion disabled** - Verify UI works without animations
✅ **Use explicit width** - Avoid flex-grow on animated elements
✅ **Apply to tbody for tables** - Not individual rows

### Never Do

❌ **Conditional parent** - `{show && <ul ref={parent}>}`
❌ **Index as key** - `key={index}` breaks animations
❌ **Ignore SSR** - Will break in Cloudflare Workers/Next.js
❌ **Force animations** - `disrespectUserMotionPreference: true` breaks accessibility
❌ **Animate tables directly** - Use tbody or div-based layout
❌ **Skip unique keys** - Required for proper animation
❌ **Complex animations** - Use Motion instead

**Note**: AutoAnimate respects `prefers-reduced-motion` automatically (never disable this).

---

## Package Versions

**Latest**: @formkit/auto-animate@0.9.0 (Sept 5, 2025)

```json
{
  "dependencies": {
    "@formkit/auto-animate": "^0.9.0"
  }
}
```

**Framework Compatibility**: React 18+, Vue 3+, Solid, Svelte, Preact

---

## Official Documentation

- **Official Site**: https://auto-animate.formkit.com
- **GitHub**: https://github.com/formkit/auto-animate
- **npm**: https://www.npmjs.com/package/@formkit/auto-animate
- **React Docs**: https://auto-animate.formkit.com/react

---

## Templates & References

See bundled resources:
- `templates/` - Copy-paste examples (SSR-safe, accordion, toast, forms)
- `references/` - CSS conflicts, SSR patterns, library comparisons
