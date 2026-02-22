---
name: spline-3d-integration
description: "Use when adding interactive 3D scenes from Spline.design to web projects. Covers embedding methods (React, Next.js, vanilla JS), the @splinetool/runtime API for programmatic control (events, variables, animations, camera), performance optimization, and common integration patterns like hero sections, product viewers, and scroll-driven 3D."
---

# Spline 3D Integration

Master guide for embedding interactive 3D scenes from [Spline.design](https://spline.design) into web projects.

---

## What Is Spline?

Spline is a **browser-based 3D design tool** — think of it as Figma, but for 3D. Designers create interactive 3D scenes (objects, materials, animations, physics, events) in the Spline editor, then export them for the web.

- **Free tier** available (with watermark)
- Scenes are hosted by Spline and loaded at runtime
- Supports mouse, scroll, keyboard, and touch interactions
- Built on WebGL — works in all modern browsers

---

## Integration Methods

There are **3 ways** to embed a Spline scene. Choose based on your stack:

| Method | Best For | Package |
|--------|----------|---------|
| **React Component** | React / Next.js apps | `@splinetool/react-spline` |
| **Vanilla JS Runtime** | Plain HTML/JS, Webflow, any framework | `@splinetool/runtime` |
| **iframe Embed** | Quick embeds, no-code sites, CMS | None (just a URL) |

### Decision Guide

```
Is this a React or Next.js project?
  → YES: Use @splinetool/react-spline (see REACT_INTEGRATION.md)
  → NO:
      Do you need programmatic control (events, variables, animations)?
        → YES: Use @splinetool/runtime (see VANILLA_INTEGRATION.md)
        → NO: Use iframe embed (simplest option)
```

---

## Quick Start

### Getting the Scene URL

1. Open your scene in the **Spline editor**
2. Click **Export** (top-right)
3. Select **Code**
4. Choose **React** or **Vanilla JS**
5. Copy the scene URL — it looks like:
   ```
   https://prod.spline.design/aBcDeFgHiJkLmNoP/scene.splinecode
   ```

> **Important:** The URL contains a unique scene ID. Each time you re-export, Spline generates a new URL. Use the latest one.

### React (10 lines)

```bash
npm install @splinetool/react-spline @splinetool/runtime
```

```tsx
import Spline from '@splinetool/react-spline';

export default function MyScene() {
  return (
    <div style={{ width: '100%', height: '100vh' }}>
      <Spline scene="https://prod.spline.design/YOUR_SCENE_ID/scene.splinecode" />
    </div>
  );
}
```

### Vanilla JS (10 lines)

```html
<canvas id="canvas3d" style="width: 100%; height: 100vh;"></canvas>
<script type="module">
  import { Application } from 'https://esm.sh/@splinetool/runtime';

  const canvas = document.getElementById('canvas3d');
  const spline = new Application(canvas);
  spline.load('https://prod.spline.design/YOUR_SCENE_ID/scene.splinecode')
    .then(() => console.log('Scene loaded!'));
</script>
```

### iframe (1 line)

```html
<iframe src="https://my.spline.design/YOUR_SCENE_ID/" width="100%" height="600" frameborder="0"></iframe>
```

---

## Runtime API — Key Methods

Once a scene is loaded, you can interact with it programmatically. These methods work in **both** React (via `onLoad` callback) and vanilla JS (via the `Application` instance).

### Getting a Reference

**React:**
```tsx
function handleLoad(splineApp) {
  // splineApp is your runtime reference
  const cube = splineApp.findObjectByName('Cube');
}

<Spline scene="..." onLoad={handleLoad} />
```

**Vanilla JS:**
```js
spline.load('...').then(() => {
  const cube = spline.findObjectByName('Cube');
});
```

### Object Queries

| Method | What It Does |
|--------|-------------|
| `findObjectByName('name')` | Find an object by its name in the Spline editor |
| `findObjectById('uuid')` | Find an object by its unique ID |
| `getAllObjects()` | Get an array of all objects in the scene |

### Triggering Events

You can trigger events that are **already defined in the Spline editor**:

```js
// Trigger a mouseDown event on an object by name
splineApp.emitEvent('mouseDown', 'Cube');

// Trigger by object ID
splineApp.emitEventReverse('mouseDown', 'object-uuid');
```

**Supported event types:** `mouseDown`, `mouseUp`, `mouseHover`, `keyDown`, `keyUp`, `start`, `lookAt`, `follow`

### Listening to Events

```js
splineApp.addEventListener('mouseDown', (e) => {
  console.log('Clicked:', e.target.name);
  console.log('Position:', e.target.position);
});

splineApp.addEventListener('mouseHover', (e) => {
  document.body.style.cursor = 'pointer';
});
```

### Variables

Spline scenes can have **variables** (defined in the editor). You can read and write them from code:

```js
// Read
const score = splineApp.getVariable('score');

// Write — this updates the scene in real-time
splineApp.setVariable('score', 42);
splineApp.setVariable('isActive', true);
splineApp.setVariable('userName', 'Visitor');
```

> **Use case:** Drive 3D animations from your app data. For example, set a `progress` variable that controls a loading bar animation inside the Spline scene.

### Object Properties (Direct Manipulation)

Once you have an object reference, you can modify it directly:

```js
const cube = splineApp.findObjectByName('Cube');

// Position
cube.position.x = 2;
cube.position.y = 0;
cube.position.z = -1;

// Rotation (radians)
cube.rotation.y = Math.PI / 4;

// Scale
cube.scale.x = 1.5;
cube.scale.y = 1.5;
cube.scale.z = 1.5;
```

---

## Common Patterns

### 1. Hero Section with 3D Scene

The most popular pattern — a split layout with text on one side and a 3D scene on the other. See `examples/react-spline-wrapper.tsx` for the recommended lazy-loaded component.

```tsx
<div className="hero">
  <div className="hero-text">
    <h1>Welcome</h1>
    <p>Some subtitle text</p>
  </div>
  <div className="hero-3d">
    <SplineScene scene="https://prod.spline.design/.../scene.splinecode" />
  </div>
</div>
```

**Key tips:**
- Always lazy-load the Spline component (it's a heavy library)
- Show a loading spinner/skeleton while the scene loads
- Use `flex` or `grid` for the split layout
- On mobile, stack vertically or consider hiding the 3D scene entirely

### 2. Interactive Product Viewer

Let users rotate, zoom, and interact with a 3D product:

```tsx
function ProductViewer({ sceneUrl }) {
  const handleLoad = (app) => {
    // Listen for clicks on hotspots
    app.addEventListener('mouseDown', (e) => {
      if (e.target.name === 'Hotspot_1') {
        showProductDetail('screen');
      }
    });
  };

  return <Spline scene={sceneUrl} onLoad={handleLoad} />;
}
```

### 3. Scroll-Driven 3D

Connect scroll position to a Spline variable to create scroll-triggered 3D animations:

```js
const splineApp = /* your loaded app */;

window.addEventListener('scroll', () => {
  const scrollPercent = window.scrollY / (document.body.scrollHeight - window.innerHeight);
  splineApp.setVariable('scrollProgress', scrollPercent);
});
```

Then in the Spline editor, use the `scrollProgress` variable to drive animations (0 to 1).

### 4. Data-Driven 3D Dashboard

Update 3D visualizations from live data:

```js
async function updateDashboard() {
  const data = await fetch('/api/metrics').then(r => r.json());

  splineApp.setVariable('revenue', data.revenue);
  splineApp.setVariable('users', data.activeUsers);
  splineApp.setVariable('status', data.systemStatus);
}

// Update every 5 seconds
setInterval(updateDashboard, 5000);
```

---

## Performance Best Practices

This is the **#1 issue** people hit with Spline. Follow these rules:

### The Big 8

| # | Rule | Why |
|---|------|-----|
| 1 | **Max 150k polygons** per scene | More polygons = more GPU work = slower rendering |
| 2 | **≤ 3 lights** per scene | Each light multiplies rendering calculations |
| 3 | **Enable geometry compression** on export | Reduces file size by 50-80% |
| 4 | **Lazy-load scenes below the fold** | Don't load what the user can't see yet |
| 5 | **One complex scene per page** max | Multiple scenes compete for GPU resources |
| 6 | **Delete hidden/unused objects** | They still get loaded and processed |
| 7 | **Use Matcap materials** over complex lighting | Fakes realistic shading without GPU cost |
| 8 | **Consider image/video fallback** for simple scenes | If the scene doesn't need interaction, export as image/video instead |

### Lazy Loading Pattern (React)

**Always** lazy-load the Spline component. The `@splinetool/runtime` package is ~500KB+.

```tsx
import { Suspense, lazy } from 'react';

const Spline = lazy(() => import('@splinetool/react-spline'));

export function SplineScene({ scene, className }) {
  return (
    <Suspense
      fallback={
        <div className="spline-loader">
          <div className="spinner" />
        </div>
      }
    >
      <Spline scene={scene} className={className} />
    </Suspense>
  );
}
```

### Spline Editor Optimization Checklist

Before exporting, run through this in the Spline editor:

1. Open the **Performance panel** (View → Performance)
2. Check polygon count — aim for under 150k
3. Remove any hidden or off-screen objects
4. Reduce segments on smooth objects (spheres, cylinders)
5. Under Export settings:
   - Set **Geometry Quality** to "Performance"
   - Enable **Image Compression**
6. Test on mobile — if it's slow, simplify further

---

## Gotchas & Troubleshooting

### CORS Issues
**Problem:** Scene won't load, browser console shows CORS errors.
**Solution:** Download the `.splinecode` file from Spline's export panel and self-host it. Serve it from your own domain or a CDN.

```tsx
// Instead of Spline's URL
<Spline scene="https://prod.spline.design/abc123/scene.splinecode" />

// Self-hosted
<Spline scene="/assets/scene.splinecode" />
```

### Version Mismatches
**Problem:** `TypeError` or blank screen after install.
**Solution:** Make sure `@splinetool/react-spline` and `@splinetool/runtime` versions are compatible. Install them together:

```bash
npm install @splinetool/react-spline@latest @splinetool/runtime@latest
```

### Scene Loads but Shows Blank White
**Problem:** Container has `0` height.
**Solution:** The Spline component fills its parent. Make sure the parent has explicit dimensions:

```css
.spline-container {
  width: 100%;
  height: 100vh; /* or any fixed/relative height */
  position: relative;
}
```

### Mobile Performance
**Problem:** Scene is laggy or crashes on phones.
**Solutions:**
- Reduce polygon count significantly (under 50k for mobile)
- Use fewer lights (1-2 max)
- Consider showing a static image on mobile instead:

```tsx
function ResponsiveScene({ scene, fallbackImage }) {
  const isMobile = window.innerWidth < 768;

  if (isMobile) {
    return <img src={fallbackImage} alt="3D scene" />;
  }

  return <SplineScene scene={scene} />;
}
```

### Loading UX
**Problem:** Users see a blank space for 2-5 seconds while the scene loads.
**Solution:** Always show a loader. Use the `onLoad` callback to hide it:

```tsx
function SceneWithLoader({ scene }) {
  const [loaded, setLoaded] = useState(false);

  return (
    <div className="scene-container">
      {!loaded && <div className="spinner" />}
      <Spline
        scene={scene}
        onLoad={() => setLoaded(true)}
        style={{ opacity: loaded ? 1 : 0, transition: 'opacity 0.5s' }}
      />
    </div>
  );
}
```

---

## Detailed Guides

- **[React & Next.js Integration](guides/REACT_INTEGRATION.md)** — Lazy loading, wrapper components, Next.js specifics, TypeScript
- **[Vanilla JS Integration](guides/VANILLA_INTEGRATION.md)** — Canvas setup, CDN usage, event handling, animation loops
- **[Performance Optimization](guides/PERFORMANCE.md)** — Deep dive on scene optimization, export settings, mobile strategies

## Examples

- **[react-spline-wrapper.tsx](examples/react-spline-wrapper.tsx)** — Production-ready lazy-loaded React wrapper
- **[vanilla-embed.html](examples/vanilla-embed.html)** — Minimal vanilla JS embed
- **[interactive-scene.tsx](examples/interactive-scene.tsx)** — Full interactive example with events, variables, and camera
