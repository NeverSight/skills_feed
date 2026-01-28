---
name: manim-scroll
description: Build and integrate scroll-driven Manim animations with pre-rendered assets, manifest generation, and the web runtime. Use when users ask about Manim scroll playback, render pipelines, native text animation, or integrating the runtime.
globs:
  - "**/*.tsx"
  - "**/*.ts"
  - "**/*.jsx"
  - "**/*.js"
  - "**/next.config.*"
alwaysApply: false
---

# Manim Scroll

Scroll-driven Manim animations for the web. Pre-render mathematical animations with Manim and play them back smoothly as users scroll.

## Quick Start (Next.js)

The recommended approach uses the Next.js plugin for automatic build-time rendering.

1. Install the unified package:

```bash
npm install @mihirsarya/manim-scroll
```

2. Configure `next.config.js`:

```js
const { withManimScroll } = require("@mihirsarya/manim-scroll/next");

module.exports = withManimScroll({
  manimScroll: {
    pythonPath: "python3",
    quality: "h",
    fps: 30,
    resolution: "1920x1080",
  },
});
```

3. Use the component:

```tsx
import { ManimScroll } from "@mihirsarya/manim-scroll";

export default function Page() {
  return (
    <ManimScroll
      scene="TextScene"
      fontSize={72}
      color="#ffffff"
      scrollRange="viewport"
      style={{ height: "100vh", background: "#111" }}
    >
      Welcome to my site
    </ManimScroll>
  );
}
```

The plugin automatically extracts props, renders animations, and caches them.

## Native Mode (No Pre-rendered Assets)

For text animations without pre-rendered video/frames, use native mode. This renders text directly in the browser using SVG, replicating Manim's Write/DrawBorderThenFill animation.

```tsx
<ManimScroll
  mode="native"
  fontSize={48}
  color="#ffffff"
  scrollRange="viewport"
  style={{ height: "100vh", background: "#111" }}
>
  Currently building
</ManimScroll>
```

### Native Mode Benefits

- **No build step required** - works immediately without Python/Manim
- **Perfect sizing** - text renders at exact pixel size (no scaling artifacts)
- **Smaller bundle** - no video/frame assets to download
- **Authentic Manim animation** - replicates Write/DrawBorderThenFill exactly:
  - Uses Manim's exact `lag_ratio = min(4.0 / length, 0.2)` formula
  - Two-phase animation: stroke drawing (0-50%) and fill transition (50-100%)
  - Progressive contour drawing across all characters
  - Matches Manim's `linear` rate function for Write animation
- **Scroll-driven** - same scroll progress behavior as pre-rendered mode

### Custom Fonts in Native Mode

For authentic Manim typography, provide a font URL (woff, woff2, ttf, otf):

```tsx
<ManimScroll
  mode="native"
  fontSize={48}
  color="#ffffff"
  fontUrl="/fonts/CMUSerif-Roman.woff2"
>
  Mathematical text
</ManimScroll>
```

## Progress-Based Animation (No Scroll)

Animate text programmatically via progress value or duration instead of scroll.

### Controlled Progress Mode

Pass `progress` prop (0-1) to render at exact animation state:

```tsx
const [progress, setProgress] = useState(0);

<ManimScroll mode="native" progress={progress}>
  Hello World
</ManimScroll>

<input 
  type="range" 
  value={progress} 
  onChange={(e) => setProgress(+e.target.value)} 
  min={0} max={1} step={0.01} 
/>
```

### Imperative Playback with Hook

Use `useNativeAnimation` for programmatic control:

```tsx
import { useRef, useEffect } from "react";
import { useNativeAnimation } from "@mihirsarya/manim-scroll";

function AutoPlayDemo() {
  const containerRef = useRef<HTMLDivElement>(null);
  
  const { isReady, play, seek, setProgress, isPlaying } = useNativeAnimation({
    ref: containerRef,
    text: "Hello World",
    fontSize: 72,
    color: "#ffffff",
  });

  // Auto-play on mount
  useEffect(() => {
    if (isReady) {
      play(2000); // Play over 2 seconds
    }
  }, [isReady, play]);

  return (
    <div ref={containerRef}>
      <button onClick={() => play(1000)}>Play</button>
      <button onClick={() => seek(0.5)}>Jump to 50%</button>
      <button onClick={() => setProgress(0)}>Reset</button>
    </div>
  );
}
```

### Playback Options

The `play()` method accepts options for fine-grained control:

```tsx
play({
  duration: 2000,           // Animation duration in ms
  delay: 500,               // Delay before starting
  easing: "ease-in-out",    // Easing: "linear" | "ease-in" | "ease-out" | "ease-in-out" | "smooth"
  loop: true,               // Loop animation
  direction: -1,            // Reverse playback
  onComplete: () => {},     // Callback when done
});
```

### useNativeAnimation Hook

Full programmatic control:

```tsx
import { useRef } from "react";
import { useNativeAnimation } from "@mihirsarya/manim-scroll";

function NativeDemo() {
  const containerRef = useRef<HTMLDivElement>(null);
  
  const { progress, isReady, pause, resume, play, seek, setProgress, isPlaying } = useNativeAnimation({
    ref: containerRef,
    text: "Hello World",
    fontSize: 72,
    color: "#ffffff",
    scrollRange: "viewport", // Ignored when using play()/setProgress()
  });

  return (
    <div ref={containerRef} style={{ height: "100vh" }}>
      {!isReady && <div>Loading...</div>}
    </div>
  );
}
```

## Inline Mode

For animations that flow with surrounding text (like within a paragraph):

```tsx
<p>
  I'm building{" "}
  <ManimScroll
    scene="TextScene"
    fontSize={24}
    color="#667eea"
    inline
    style={{ width: "150px", height: "30px" }}
  >
    the future
  </ManimScroll>{" "}
  today.
</p>
```

Inline mode:
- Renders with a **transparent background**
- Uses `display: inline-block` for flow with text
- Adjusts the Manim camera to fit text tightly with minimal padding
- Outputs WebM with alpha channel (for video mode) or transparent PNGs (for frames mode)

## Scroll Range Configuration

Control when the animation plays relative to scroll position.

### Presets (Recommended)

```tsx
<ManimScroll scrollRange="viewport">...</ManimScroll>  // Default: plays as element crosses viewport
<ManimScroll scrollRange="element">...</ManimScroll>   // Tied to element's own scroll position
<ManimScroll scrollRange="full">...</ManimScroll>      // Spans entire document scroll
```

### Relative Units

```tsx
<ManimScroll scrollRange={["100vh", "-50%"]}>...</ManimScroll>
<ManimScroll scrollRange={["80vh", "-100%"]}>...</ManimScroll>
```

Supported units:
- `vh` - viewport height percentage
- `%` - element height percentage
- `px` - pixels
- Plain numbers - treated as pixels

### Pixel Values (Legacy)

```tsx
<ManimScroll scrollRange={{ start: 800, end: -400 }}>...</ManimScroll>
<ManimScroll scrollRange={[800, -400]}>...</ManimScroll>
```

## useManimScroll Hook

For advanced use cases requiring custom control:

```tsx
import { useRef } from "react";
import { useManimScroll } from "@mihirsarya/manim-scroll";

function CustomAnimation() {
  const containerRef = useRef<HTMLDivElement>(null);

  const { progress, isReady, error, pause, resume, seek, isPaused } = useManimScroll({
    ref: containerRef,
    manifestUrl: "/assets/scene/manifest.json",
    scrollRange: "viewport",
  });

  return (
    <div ref={containerRef} style={{ height: "100vh" }}>
      {!isReady && <div>Loading...</div>}
      <div>Progress: {Math.round(progress * 100)}%</div>
      <button onClick={pause}>Pause</button>
      <button onClick={resume}>Resume</button>
    </div>
  );
}
```

### Auto-Resolution Mode

When using with the Next.js plugin, you can let the hook resolve the manifest automatically:

```tsx
const { progress, isReady } = useManimScroll({
  ref: containerRef,
  scene: "TextScene",
  animationProps: { text: "Hello", fontSize: 72, color: "#fff" },
});
```

## Vanilla JS Usage

### Pre-rendered Animations

```ts
import { registerScrollAnimation } from "@mihirsarya/manim-scroll-runtime";

const container = document.querySelector("#hero") as HTMLElement;

registerScrollAnimation({
  container,
  manifestUrl: "/dist/scene/manifest.json",
  mode: "auto",
  scrollRange: "viewport",
  onReady: () => console.log("ready"),
  onProgress: (progress) => console.log(progress),
});
```

### Native Text Animations

```ts
import { registerNativeAnimation } from "@mihirsarya/manim-scroll-runtime";

const container = document.querySelector("#hero") as HTMLElement;

registerNativeAnimation({
  container,
  text: "Animate this",
  fontSize: 72,
  color: "#ffffff",
  scrollRange: "viewport",
  onReady: () => console.log("ready"),
});
```

## Manual Rendering (Non-Next.js)

For custom workflows, use the Python CLI directly:

```bash
python render/cli.py \
  --scene-file path/to/scene.py \
  --scene-name MyScene \
  --output-dir ./dist/scene \
  --format both \
  --fps 30 \
  --resolution 1920x1080 \
  --quality k
```

### Render Text with Props

```bash
echo '{"text": "Hello World", "fontSize": 72, "color": "#ffffff"}' > props.json

python render/cli.py \
  --scene-file render/templates/text_scene.py \
  --scene-name TextScene \
  --props props.json \
  --output-dir ./dist/scene \
  --format both
```

### CLI Options

| Option | Default | Description |
|--------|---------|-------------|
| `--scene-file` | (required) | Path to the Manim scene file |
| `--scene-name` | (required) | Scene class name to render |
| `--output-dir` | (required) | Directory for render outputs |
| `--format` | `both` | Output format: `frames`, `video`, or `both` |
| `--fps` | `30` | Frames per second |
| `--resolution` | `1920x1080` | Resolution as WxH |
| `--quality` | `k` | Manim quality: `l`, `m`, `h`, `k` |
| `--props` | - | Path to JSON props file |
| `--transparent` | `false` | Render with transparent background |

## Package Structure

| Package | npm | Description |
|---------|-----|-------------|
| `packages/manim-scroll/` | `@mihirsarya/manim-scroll` | Unified package (recommended) |
| `react/` | `@mihirsarya/manim-scroll-react` | React component and hooks |
| `next/` | `@mihirsarya/manim-scroll-next` | Next.js build plugin |
| `runtime/` | `@mihirsarya/manim-scroll-runtime` | Core scroll runtime |
| `render/` | - | Python CLI for Manim rendering |

## Next.js Plugin Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `pythonPath` | `"python3"` | Path to Python executable |
| `quality` | `"h"` | Manim quality preset (l, m, h, k) |
| `fps` | `30` | Frames per second |
| `resolution` | `"1920x1080"` | Output resolution |
| `format` | `"both"` | Output format (frames, video, both) |
| `concurrency` | CPU count - 1 | Max parallel renders |
| `verbose` | `false` | Enable verbose logging |
| `cleanOrphans` | `true` | Remove unused cached assets |

## Component Props Reference

| Prop | Type | Description |
|------|------|-------------|
| `scene` | `string` | Scene name (default: `"TextScene"`) |
| `fontSize` | `number` | Font size for text animations |
| `color` | `string` | Color as hex string (e.g., `"#ffffff"`) |
| `font` | `string` | Font family for text |
| `inline` | `boolean` | Enable inline mode with transparent background |
| `padding` | `number` | Padding around text in inline mode (Manim units, default: `0.2`) |
| `manifestUrl` | `string` | Explicit manifest URL (overrides auto-resolution) |
| `mode` | `"auto" \| "video" \| "frames" \| "native"` | Playback mode |
| `fontUrl` | `string` | URL to font file for native mode |
| `strokeWidth` | `number` | Stroke width for native mode (default: `2`) |
| `scrollRange` | `ScrollRangeValue` | Scroll range: preset, tuple, or object |
| `onReady` | `() => void` | Called when animation is loaded |
| `onProgress` | `(progress: number) => void` | Called on scroll progress |
| `className` | `string` | CSS class for the container |
| `style` | `CSSProperties` | Inline styles for the container |
| `children` | `ReactNode` | Text content (becomes `text` prop) |

## Requirements

- Python 3.8+ with [Manim](https://www.manim.community/) installed (for pre-rendered mode)
- Node.js 18+
- Next.js 13+ (for the plugin)

## Additional Resources

- See `references/ARCHITECTURE.md` for package internals and diagrams
- See `references/API.md` for complete type definitions
- See `references/CUSTOM_SCENES.md` for creating custom Manim scenes
- See `references/TROUBLESHOOTING.md` for common issues and solutions
