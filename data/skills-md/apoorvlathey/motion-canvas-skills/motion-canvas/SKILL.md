---
name: motion-canvas
description: Create programmatic vector animations with TypeScript using the Motion Canvas library. Use when building animated explainer videos, tutorials, data visualizations, or presentations with synchronized audio. Triggers on tasks involving motion graphics, animation scenes, code-based video creation, or requests to animate shapes/text/images with precise timing control.
---

# Motion Canvas

TypeScript library for creating animated videos programmatically using generator functions.

## Project Setup

```bash
npm init @motion-canvas@latest    # Create new project
npm install && npm start          # Run dev server at localhost:9000
```

**Project structure:**
```
my-project/
├── src/
│   ├── project.ts         # Main project config
│   └── scenes/            # Animation scenes
├── vite.config.ts
└── package.json
```

## Core Concepts

### 1. Project Configuration

```ts
// src/project.ts
import {makeProject} from '@motion-canvas/core';
import scene1 from './scenes/scene1?scene';  // Note: ?scene suffix required

export default makeProject({
  scenes: [scene1],
  // audio: audioFile,  // Optional: sync animations to voiceover
});
```

### 2. Scenes

Scenes use generator functions - `yield*` pauses to render frames:

```tsx
import {makeScene2D, Circle, Rect, Txt} from '@motion-canvas/2d';
import {createRef, all, waitFor, waitUntil} from '@motion-canvas/core';

export default makeScene2D(function* (view) {
  const circle = createRef<Circle>();

  view.add(<Circle ref={circle} size={100} fill="#e13238" />);

  yield* circle().position.x(300, 1);  // Move right over 1 second
  yield* waitFor(0.5);                  // Pause 0.5 seconds
  yield* circle().position.x(0, 1);    // Move back
});
```

### 3. Nodes (Visual Elements)

```tsx
// Shapes
<Circle size={100} fill="#e13238" />
<Rect width={200} height={100} fill="blue" radius={10} />
<Line points={[[0,0], [100,100]]} stroke="white" lineWidth={4} />

// Text
<Txt text="Hello" fontSize={48} fill="white" fontFamily="Arial" />

// Media
<Img src={imagePath} width={400} />
<Video ref={videoRef} src={videoPath} />

// Code blocks with syntax highlighting
<Code code={`const x = 1;`} fontSize={24} />
```

### 4. References

Store node references for animation:

```tsx
const circle = createRef<Circle>();
view.add(<Circle ref={circle} />);
yield* circle().scale(2, 1);  // Call with () to access node
```

### 5. Signals (Reactive Values)

```ts
const radius = createSignal(3);
const area = createSignal(() => Math.PI * radius() * radius());  // Computed

// Animate signal
yield* radius(5, 2);  // Change from 3 to 5 over 2 seconds
// area() automatically updates
```

### 6. Animation Patterns

**Sequential:**
```ts
yield* animation1();
yield* animation2();
```

**Parallel:**
```ts
yield* all(
  circle().position(100, 1),
  circle().fill('red', 1),
);
```

**Staggered:**
```ts
yield* sequence(0.1, anim1(), anim2(), anim3());  // 0.1s delay between each
```

**Looping:**
```ts
yield* loop(5, i => circle().rotation(360, 1));
```

### 7. Time Events (Audio Sync)

```ts
yield* waitUntil('intro-end');     // Pause until marker in editor timeline
yield* circle().scale(2, useDuration('grow'));  // Duration from timeline
```

### 8. Layouts (Flexbox)

```tsx
<Layout layout direction="row" gap={20} alignItems="center">
  <Circle size={50} />
  <Rect width={100} height={50} />
</Layout>
```

### 9. Scene Transitions

```ts
yield* slideTransition(Direction.Left);
yield* fadeTransition(0.5);
yield* zoomInTransition();
```

### 10. Code Animations

```tsx
const codeRef = createRef<Code>();
view.add(<Code ref={codeRef} code={initialCode} />);

yield* codeRef().code('new code', 1);                    // Replace all
yield* codeRef().code.replace(range, 'replacement', 1); // Replace range
yield* codeRef().selection(codeRef().findFirstRange('text'), 0.5);  // Highlight
```

## Common Easing Functions

```ts
import {easeInOutCubic, easeOutBack, linear} from '@motion-canvas/core';
yield* node().scale(2, 1, easeOutBack);  // Overshoot effect
```

## Rendering

Click **RENDER** in editor UI. Configure in Video Settings tab:
- Resolution, frame rate, background color
- Frame range, color space
- FFmpeg plugin for video output

## References

- [API Reference](references/api-reference.md) - Comprehensive API documentation
- [Patterns](references/patterns.md) - Common animation patterns and examples
