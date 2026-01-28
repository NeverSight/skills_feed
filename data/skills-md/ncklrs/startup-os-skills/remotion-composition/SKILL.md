---
name: remotion-composition
description: Generates Remotion composition structure focusing ONLY on Sequence ordering, scene transitions, and duration mapping. Input is scene list with durations. Output is COMPOSITION_STRUCTURE.md with Sequence layout and timing calculations. Use when organizing scenes or when asked to "structure composition", "layout scenes", "calculate timing".
---

# Remotion Composition

Generates composition structure documents that define how scenes are ordered, timed, and transitioned in a Remotion video. This skill focuses exclusively on Sequence layout and timing orchestration.

## What This Skill Does

Generates composition structure for:

1. **Sequence layout** — Ordering and positioning of scene Sequences
2. **Timing calculations** — Start frames, end frames, duration for each scene
3. **Scene transitions** — Overlap and crossfade timing between scenes
4. **Duration mapping** — Converting seconds to frames for all scenes
5. **Timing constants** — Structured timing object for constants.ts

## Scope Boundaries

**IN SCOPE:**
- Sequence component organization
- Frame calculations for scene timing
- Scene overlap and transition timing
- Duration constant generation
- Scene ordering logic

**OUT OF SCOPE:**
- Scene component implementation (use `/remotion-component-gen`)
- Animation parameters (use `/remotion-animation`)
- Visual styling (colors, layouts)
- Asset management (use `/remotion-asset-coordinator`)

## Input/Output Formats

### Input Format: Scene List with Durations

Accepts scene timing specifications:

**Natural Language:**
```
Scene 1 (Intro): 0-5 seconds
Scene 2 (Features): 5-15 seconds
Scene 3 (Demo): 15-25 seconds
Scene 4 (CTA): 25-30 seconds
```

**Structured Format:**
```markdown
## Scene Timing

**Total Duration:** 30 seconds
**Frame Rate:** 30 fps
**Total Frames:** 900

**Scenes:**
1. Scene 1 - Intro: 5 seconds (0s - 5s)
2. Scene 2 - Features: 10 seconds (5s - 15s)
3. Scene 3 - Demo: 10 seconds (15s - 25s)
4. Scene 4 - CTA: 5 seconds (25s - 30s)

**Transitions:**
- Fade transition between scenes: 0.5 seconds (15 frames)
```

### Output Format: COMPOSITION_STRUCTURE.md

Generates composition structure document:

```markdown
# Composition Structure: ProductDemo

## Status
✅ Sequence layout defined
✅ Timing calculations complete
⏳ Ready for scene implementation

## Composition Overview

**Total Duration:** 30 seconds (900 frames @ 30fps)
**Scenes:** 4
**Transitions:** Crossfade (15 frames)

## Scene Timing Constants

```typescript
const FPS = 30;

export const SCENE_TIMING = {
  intro: {
    start: 0,
    end: 150,
    duration: 150,
    // 0s - 5s
  },
  features: {
    start: 150,
    end: 450,
    duration: 300,
    // 5s - 15s
  },
  demo: {
    start: 450,
    end: 750,
    duration: 300,
    // 15s - 25s
  },
  cta: {
    start: 750,
    end: 900,
    duration: 150,
    // 25s - 30s
  },
} as const;

// Transition timing
export const TRANSITIONS = {
  crossfadeDuration: 15, // frames (0.5 seconds)
} as const;
```

## Composition Layout

Main composition with Sequence structure:

```typescript
import { AbsoluteFill, Sequence } from "remotion";
import { SCENE_TIMING } from "./constants";
import { Scene1Intro } from "./scenes/Scene1Intro";
import { Scene2Features } from "./scenes/Scene2Features";
import { Scene3Demo } from "./scenes/Scene3Demo";
import { Scene4CTA } from "./scenes/Scene4CTA";

export function ProductDemo() {
  return (
    <AbsoluteFill>
      {/* Scene 1: Intro (0s - 5s) */}
      <Sequence
        from={SCENE_TIMING.intro.start}
        durationInFrames={SCENE_TIMING.intro.duration}
      >
        <Scene1Intro />
      </Sequence>

      {/* Scene 2: Features (5s - 15s) */}
      <Sequence
        from={SCENE_TIMING.features.start}
        durationInFrames={SCENE_TIMING.features.duration}
      >
        <Scene2Features />
      </Sequence>

      {/* Scene 3: Demo (15s - 25s) */}
      <Sequence
        from={SCENE_TIMING.demo.start}
        durationInFrames={SCENE_TIMING.demo.duration}
      >
        <Scene3Demo />
      </Sequence>

      {/* Scene 4: CTA (25s - 30s) */}
      <Sequence
        from={SCENE_TIMING.cta.start}
        durationInFrames={SCENE_TIMING.cta.duration}
      >
        <Scene4CTA />
      </Sequence>
    </AbsoluteFill>
  );
}
```

## Scene Timing Breakdown

| Scene | Name | Duration | Frames | Start Frame | End Frame |
|-------|------|----------|--------|-------------|-----------|
| 1 | Intro | 5s | 150 | 0 | 150 |
| 2 | Features | 10s | 300 | 150 | 450 |
| 3 | Demo | 10s | 300 | 450 | 750 |
| 4 | CTA | 5s | 150 | 750 | 900 |

**Total:** 30 seconds (900 frames)

## Timeline Visualization

```
Frame:     0        150       450       750       900
Time:      0s        5s        15s       25s       30s
           |---------|---------|---------|---------|
Scene:     |  Intro  | Features|   Demo  |   CTA   |
           |---------|---------|---------|---------|
```

## Next Steps

1. **Implement scenes** via `/remotion-component-gen`
2. **Add transitions** if needed (crossfades, wipes)
3. **Integrate constants** into composition constants.ts
4. **Test timing** in Remotion preview
5. **Adjust durations** if scenes feel too fast/slow

## Checklist

- [x] Scene timing calculated
- [x] Sequence layout defined
- [x] Constants generated
- [x] Timing constants structured
- [ ] Scene components implemented (next step)
- [ ] Transitions added (if needed)
- [ ] Timing tested in preview
```

## Composition Patterns

### Pattern 1: Sequential Scenes (No Overlap)

Standard sequential layout where scenes don't overlap:

```typescript
<Sequence from={0} durationInFrames={150}>
  <Scene1 />
</Sequence>

<Sequence from={150} durationInFrames={300}>
  <Scene2 />
</Sequence>

<Sequence from={450} durationInFrames={300}>
  <Scene3 />
</Sequence>
```

### Pattern 2: Overlapping Scenes (Crossfade)

Scenes overlap for smooth transitions:

```typescript
const CROSSFADE = 15; // frames

// Scene 1: Full duration
<Sequence from={0} durationInFrames={150}>
  <Scene1 />
</Sequence>

// Scene 2: Starts before Scene 1 ends
<Sequence from={150 - CROSSFADE} durationInFrames={300 + CROSSFADE}>
  <Scene2 />
</Sequence>

// Scene 3: Starts before Scene 2 ends
<Sequence from={450 - CROSSFADE} durationInFrames={300 + CROSSFADE}>
  <Scene3 />
</Sequence>
```

### Pattern 3: Layered Composition

Background + foreground scenes running simultaneously:

```typescript
{/* Background layer - runs full duration */}
<Sequence from={0} durationInFrames={900}>
  <BackgroundScene />
</Sequence>

{/* Foreground scenes - sequential */}
<Sequence from={0} durationInFrames={150}>
  <Scene1 />
</Sequence>

<Sequence from={150} durationInFrames={300}>
  <Scene2 />
</Sequence>
```

### Pattern 4: Nested Sequences

Sub-scenes within main scenes:

```typescript
<Sequence from={0} durationInFrames={300}>
  <AbsoluteFill>
    {/* Sub-scene 1 */}
    <Sequence from={0} durationInFrames={100}>
      <Intro />
    </Sequence>

    {/* Sub-scene 2 */}
    <Sequence from={100} durationInFrames={200}>
      <MainContent />
    </Sequence>
  </AbsoluteFill>
</Sequence>
```

## Timing Calculation Helpers

Common frame calculations:

```typescript
// Convert seconds to frames
const secondsToFrames = (seconds: number, fps: number = 30): number =>
  Math.round(seconds * fps);

// Calculate scene timing
interface SceneTiming {
  start: number;
  end: number;
  duration: number;
}

const calculateSceneTiming = (
  startSeconds: number,
  durationSeconds: number,
  fps: number = 30
): SceneTiming => {
  const start = secondsToFrames(startSeconds, fps);
  const duration = secondsToFrames(durationSeconds, fps);
  const end = start + duration;

  return { start, end, duration };
};

// Calculate crossfade overlap
const calculateCrossfade = (
  scene1Start: number,
  scene1Duration: number,
  crossfadeDuration: number
) => ({
  scene1: {
    from: scene1Start,
    durationInFrames: scene1Duration,
  },
  scene2: {
    from: scene1Start + scene1Duration - crossfadeDuration,
    durationInFrames: crossfadeDuration, // or more if scene is longer
  },
});

// Validate total duration
const validateDuration = (
  scenes: SceneTiming[],
  expectedTotal: number
): boolean => {
  const lastScene = scenes[scenes.length - 1];
  return lastScene.end === expectedTotal;
};
```

## Scene Timing Generation

Automated timing generation from scene list:

```typescript
interface SceneSpec {
  name: string;
  durationSeconds: number;
}

const generateSceneTiming = (
  scenes: SceneSpec[],
  fps: number = 30
) => {
  let currentFrame = 0;
  const timing: Record<string, SceneTiming> = {};

  for (const scene of scenes) {
    const duration = secondsToFrames(scene.durationSeconds, fps);

    timing[scene.name] = {
      start: currentFrame,
      end: currentFrame + duration,
      duration,
    };

    currentFrame += duration;
  }

  return {
    timing,
    totalFrames: currentFrame,
    totalSeconds: currentFrame / fps,
  };
};

// Usage:
const scenes = [
  { name: 'intro', durationSeconds: 5 },
  { name: 'features', durationSeconds: 10 },
  { name: 'demo', durationSeconds: 10 },
  { name: 'cta', durationSeconds: 5 },
];

const result = generateSceneTiming(scenes, 30);
// Result:
// {
//   timing: {
//     intro: { start: 0, end: 150, duration: 150 },
//     features: { start: 150, end: 450, duration: 300 },
//     ...
//   },
//   totalFrames: 900,
//   totalSeconds: 30,
// }
```

## Transition Patterns

### Crossfade Transition

Smooth opacity crossfade between scenes:

```typescript
const CROSSFADE = 15;

// Scene 1 - fades out at end
<Sequence from={0} durationInFrames={150}>
  <Scene1 crossfadeOut={CROSSFADE} />
</Sequence>

// Scene 2 - fades in at start
<Sequence from={150 - CROSSFADE} durationInFrames={300}>
  <Scene2 crossfadeIn={CROSSFADE} />
</Sequence>

// In Scene component:
function Scene1({ crossfadeOut = 0 }) {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const opacity = crossfadeOut > 0
    ? interpolate(
        frame,
        [durationInFrames - crossfadeOut, durationInFrames],
        [1, 0],
        { extrapolateRight: 'clamp' }
      )
    : 1;

  return <AbsoluteFill style={{ opacity }}>...</AbsoluteFill>;
}
```

### Hard Cut Transition

No transition, instant scene change:

```typescript
<Sequence from={0} durationInFrames={150}>
  <Scene1 />
</Sequence>

<Sequence from={150} durationInFrames={300}>
  <Scene2 />
</Sequence>
```

### Slide Transition

One scene slides out while next slides in:

```typescript
const TRANSITION_DURATION = 20;

<Sequence from={0} durationInFrames={150}>
  <Scene1 slideOut={TRANSITION_DURATION} />
</Sequence>

<Sequence from={150 - TRANSITION_DURATION} durationInFrames={300}>
  <Scene2 slideIn={TRANSITION_DURATION} />
</Sequence>
```

## Duration Validation

Ensuring timing adds up correctly:

```typescript
// Validation helper
const validateCompositionTiming = (
  scenes: Record<string, SceneTiming>,
  expectedDuration: number,
  fps: number
): { valid: boolean; issues: string[] } => {
  const issues: string[] = [];

  // Check for gaps
  const sceneList = Object.entries(scenes).sort((a, b) => a[1].start - b[1].start);

  for (let i = 0; i < sceneList.length - 1; i++) {
    const currentEnd = sceneList[i][1].end;
    const nextStart = sceneList[i + 1][1].start;

    if (nextStart > currentEnd) {
      issues.push(`Gap detected: ${currentEnd} to ${nextStart} (${(nextStart - currentEnd) / fps}s)`);
    }
    if (nextStart < currentEnd) {
      issues.push(`Overlap detected: ${sceneList[i][0]} and ${sceneList[i + 1][0]}`);
    }
  }

  // Check total duration
  const lastScene = sceneList[sceneList.length - 1][1];
  if (lastScene.end !== expectedDuration) {
    issues.push(
      `Total duration mismatch: expected ${expectedDuration}, got ${lastScene.end} (${lastScene.end / fps}s)`
    );
  }

  return {
    valid: issues.length === 0,
    issues,
  };
};
```

## Timeline Visualization Helper

Generate ASCII timeline:

```typescript
const generateTimeline = (
  scenes: Record<string, SceneTiming>,
  fps: number,
  width: number = 60
) => {
  const lastScene = Object.values(scenes).reduce((max, scene) =>
    scene.end > max ? scene.end : max, 0
  );

  const timeline: string[] = [];

  // Frame markers
  const frameMarkers = Array.from({ length: width + 1 }, (_, i) => {
    const frame = Math.round((i / width) * lastScene);
    return frame.toString().padStart(4);
  }).join('');
  timeline.push('Frame: ' + frameMarkers);

  // Time markers
  const timeMarkers = Array.from({ length: width + 1 }, (_, i) => {
    const time = ((i / width) * lastScene) / fps;
    return time.toFixed(1) + 's';
  }).join(' ');
  timeline.push('Time:  ' + timeMarkers);

  // Scene bars
  for (const [name, timing] of Object.entries(scenes)) {
    const startPos = Math.round((timing.start / lastScene) * width);
    const endPos = Math.round((timing.end / lastScene) * width);
    const bar = ' '.repeat(startPos) + '|' + '='.repeat(endPos - startPos - 1) + '|';
    timeline.push(`${name.padEnd(8)}: ${bar}`);
  }

  return timeline.join('\n');
};
```

## Best Practices

### Timing Guidelines

```typescript
// Minimum scene duration for readability
const MIN_SCENE_DURATION = 30; // 1 second at 30fps

// Standard transition duration
const STANDARD_TRANSITION = 15; // 0.5 seconds

// Maximum scene duration before pacing feels slow
const MAX_SCENE_DURATION = 600; // 20 seconds

// Recommended scene duration range
const IDEAL_SCENE_DURATION = {
  min: 60,   // 2 seconds
  max: 300,  // 10 seconds
};
```

### Composition Organization

```typescript
// Group related Sequences
// Good:
<>
  {/* Background layer */}
  <Sequence from={0} durationInFrames={900}>
    <Background />
  </Sequence>

  {/* Content scenes */}
  <Sequence from={0} durationInFrames={150}>
    <Scene1 />
  </Sequence>
  <Sequence from={150} durationInFrames={300}>
    <Scene2 />
  </Sequence>
</>

// Bad: Mixed layers without organization
```

## Integration Workflow

1. **Define scene durations** → Input to this skill
2. **Generate composition structure** → COMPOSITION_STRUCTURE.md
3. **Add to composition file** (index.tsx)
4. **Add timing to constants** (constants.ts)
5. **Implement scenes** via `/remotion-component-gen`
6. **Test timing** in preview
7. **Adjust if needed** and regenerate

## Integration with Other Skills

This skill coordinates with:

```
remotion-composition (this skill)
    ↓ outputs: COMPOSITION_STRUCTURE.md
remotion-component-gen
    ↓ implements scenes with timing awareness
remotion-animation
    ↓ animation timing works within scene durations
```

**Works with:**
- `/motion-designer` — Scene timing from design specs
- `/remotion-scaffold` — Structure added to composition file
- `/remotion-animation` — Timing coordinates with animation configs
- `/remotion-component-gen` — Scenes fit within calculated durations
- `/remotion-spec-translator` — Orchestrates this skill in pipeline

---

This skill provides precise composition structure and timing calculations that ensure smooth, well-paced Remotion videos.
