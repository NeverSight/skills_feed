---
name: spline-3d-integration
description: Integrate Spline 3D scenes into React, Next.js, and vanilla web apps with reliable embed patterns, runtime API usage, and performance-safe defaults.
---

# Spline 3D Integration

Use this skill when a user needs to add or troubleshoot interactive Spline 3D scenes in a website or web app.

## When to use this skill

- The user wants to embed a Spline scene in React, Next.js, or vanilla JS.
- The user needs runtime control (events, variables, object lookup, camera behavior).
- The user is seeing poor performance, blank scenes, or loading issues.
- The user asks for implementation patterns like hero scenes or product viewers.

## When not to use this skill

- The user only needs static 3D media (image/video) with no interaction.
- The user is not using Spline assets.

## Outcome expectations

When using this skill, produce:

1. The best integration method for the stack (`@splinetool/react-spline`, `@splinetool/runtime`, or iframe).
2. A minimal working snippet using the user's framework.
3. Performance recommendations (scene optimization + loading strategy).
4. A short troubleshooting checklist for likely failure modes.

## Integration decision tree

```text
Is this React/Next.js?
  Yes -> Use @splinetool/react-spline (see guides/REACT_INTEGRATION.md)
  No -> Need runtime control (events/variables/object APIs)?
          Yes -> Use @splinetool/runtime (see guides/VANILLA_INTEGRATION.md)
          No  -> Use iframe embed
```

## Quick implementation defaults

- Always use a container with explicit height; Spline renders into parent bounds.
- In React/Next.js, lazy-load Spline components.
- Keep one complex scene per page when possible.
- Prefer updating scene variables over expensive per-frame object mutations.
- Provide a loading fallback and optional low-power/mobile fallback.

## Minimal snippets

### React / Next.js

```tsx
import Spline from '@splinetool/react-spline';

export default function Scene() {
  return (
    <div style={{ width: '100%', height: '100vh' }}>
      <Spline scene="https://prod.spline.design/YOUR_SCENE_ID/scene.splinecode" />
    </div>
  );
}
```

### Vanilla runtime

```html
<canvas id="canvas3d" style="width:100%;height:100vh"></canvas>
<script type="module">
  import { Application } from 'https://esm.sh/@splinetool/runtime';

  const app = new Application(document.getElementById('canvas3d'));
  app.load('https://prod.spline.design/YOUR_SCENE_ID/scene.splinecode');
</script>
```

### iframe

```html
<iframe src="https://my.spline.design/YOUR_SCENE_ID/" width="100%" height="600" frameborder="0"></iframe>
```

## Runtime API checklist

- Lookup objects: `findObjectByName`, `findObjectById`, `getAllObjects`.
- Drive interactions: `emitEvent`, `emitEventReverse`, `addEventListener`.
- Sync app state: `getVariable`, `setVariable`.
- Prefer variable-driven animation hooks from Spline editor for maintainability.

## Performance guardrails

- Target less than 150k polys desktop, less than 50k mobile.
- Keep lights low (ideally 1-3).
- Enable compression in Spline export settings.
- Lazy-load below-the-fold scenes.
- Remove hidden/unused objects before export.
- Consider image/video fallback when interaction is unnecessary.

## Troubleshooting order

1. Validate scene URL and accessibility.
2. Confirm container has non-zero height.
3. Ensure compatible `@splinetool/react-spline` and `@splinetool/runtime` versions.
4. Check browser console for CORS/network errors.
5. Test reduced scene complexity if mobile crashes or stutters.

## Repository resources

- `guides/REACT_INTEGRATION.md`
- `guides/VANILLA_INTEGRATION.md`
- `guides/PERFORMANCE.md`
- `examples/react-spline-wrapper.tsx`
- `examples/vanilla-embed.html`
- `examples/interactive-scene.tsx`
