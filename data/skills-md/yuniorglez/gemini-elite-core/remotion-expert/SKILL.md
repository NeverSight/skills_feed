---
name: remotion-expert
id: remotion-expert
version: 1.0.0
description: "Senior Specialist in Remotion v4.0+, React 19, and Next.js 16. Expert in programmatic video generation, sub-frame animation precision, and AI-driven video workflows for 2026."
---

# Remotion Expert - High-Performance Video Generation

Senior Specialist in Remotion v4.0+, React 19, and Next.js 16. Expert in programmatic video generation, sub-frame animation precision, and AI-driven video workflows for 2026.

## 🧭 Overview
Remotion allows you to create videos programmatically using React. This skill expands the LLM's capabilities to handle complex animations, dynamic data-driven videos, and high-fidelity rendering pipelines.

### Core Capabilities
- **Programmatic Animation**: Frame-perfect control via `useCurrentFrame` and `interpolate`.
- **Dynamic Compositions**: Parameterized videos that adapt to external data.
- **Modern Stack**: Fully optimized for **React 19.3**, **Next.js 16.2**, and **Tailwind CSS 4.0**.
- **AI Orchestration**: Integration with Remotion Skills for instruction-driven video editing.

---

## 🛠️ Table of Contents
1. [Quick Start](#-quick-start)
2. [Mandatory Rules & Anti-Patterns](#-mandatory-rules--anti-patterns)
3. [Core Concepts](#-core-concepts)
4. [Advanced Patterns](#-advanced-patterns)
5. [The "Do Not" List](#-the-do-not-list-common-mistakes)
6. [References](#-references)

---

## ⚡ Quick Start

Scaffold a new project using Bun (recommended for 2026):
```bash
bun create video@latest my-video
cd my-video
bun start
```

### Basic Composition Pattern
```tsx
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';

export const MyVideo = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Animate from 0 to 1 over the first second
  const opacity = interpolate(frame, [0, fps], [0, 1], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{ 
      backgroundColor: 'white', 
      justifyContent: 'center', 
      alignItems: 'center' 
    }}>
      <h1 style={{ opacity, fontSize: 100 }}>Remotion 2026</h1>
    </AbsoluteFill>
  );
};
```

---

## 🛡️ Mandatory Rules & Anti-Patterns

1. **NO CSS ANIMATIONS**: Never use standard CSS `@keyframes` or `transition`. They are not deterministic and will fail during rendering. Use `interpolate()` or `spring()`.
2. **Deterministic Logic**: Ensure all calculations are derived from `frame`. Avoid `Math.random()` or `Date.now()` inside components unless seeded.
3. **Zod Validation**: Always use Zod for `defaultProps` to ensure type safety in parameterized videos.
4. **Asset Preloading**: Use `staticFile()` for local assets and ensure remote assets are reachable during render.

---

## 🧠 Core Concepts

### 1. Frame-Based Animation
Everything is a function of the current frame.
```tsx
const frame = useCurrentFrame();
const scale = interpolate(frame, [0, 20], [0, 1], { easing: Easing.bezier(0.25, 0.1, 0.25, 1) });
```

### 2. Composition Architecture
Compositions are the "entry points". They define the canvas.
```tsx
<Composition
  id="Main"
  component={MyComponent}
  durationInFrames={300}
  fps={60}
  width={1920}
  height={1080}
  defaultProps={{ title: 'Hello' }}
/>
```

---

## 🚀 Advanced Patterns

### AI-Driven Video Modification (2026)
Integration with "Remotion Skills" allows for natural language instructions to modify compositions.
```tsx
// Pattern: Instruction-driven prop updates
export const aiUpdateHandler = async (instruction: string, currentProps: Props) => {
  // Logic to map LLM output to Remotion props
  return updatedProps;
};
```

### Dynamic Metadata Calculation
Fetch data *before* the composition renders to set duration or dimensions.
```tsx
export const calculateMetadata = async ({ props }) => {
  const response = await fetch(`https://api.v2.com/video-data/${props.id}`);
  const data = await response.json();
  return {
    durationInFrames: data.duration * 60,
    props: { ...props, content: data.content }
  };
};
```

---

## 🚫 The "Do Not" List (Common Mistakes)

- **DO NOT** use `setTimeout` or `setInterval`. They do not sync with the renderer.
- **DO NOT** use `npm` for 2026 workflows; prefer `bun` for sub-second install and execution.
- **DO NOT** forget to use `<Sequence>` for delaying elements. Manual frame offsets are error-prone.
- **DO NOT** use Tailwind 3.x patterns; leverage **Tailwind 4.0** native container queries for responsive video layouts.
- **DO NOT** use `useState` for animation progress. Animation state must always be derived from `frame`.
- **DO NOT** perform heavy computations inside the render loop without `useMemo`. Remember that the component renders *every frame*.
- **DO NOT** use external libraries that rely on `window.requestAnimationFrame`. They won't be captured by the Remotion renderer.
- **DO NOT** hardcode frame counts. Always use constants or relative calculations like `2 * fps`.

---

## 📚 References
- [Animations & Timing](./references/animations-timing.md) - Precision interpolation and springs.
- [Compositions & Props](./references/compositions-props.md) - Structuring complex video projects.
- [Media & Assets](./references/media-assets.md) - Handling Video, Audio, and Lottie.
- [Sequencing & Series](./references/sequencing.md) - Timeline orchestration.
- [Next.js Integration](./references/nextjs-integration.md) - SSR and Server Actions for Video.

---

*Updated: January 22, 2026 - 20:00*
