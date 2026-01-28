---
name: remotion-component-gen
description: Generates individual Remotion scene components from visual direction. Input is visual/animation description for a specific scene. Output is SCENE_COMPONENT.md with complete TSX implementation. Use when implementing scenes or when asked to "create a scene component", "implement scene from spec", "build Scene1Intro".
---

# Remotion Component Gen

Generates production-ready Remotion scene component implementations from visual direction and animation specifications. This skill focuses on creating complete, working scene components.

## What This Skill Does

Generates scene component code for:

1. **Scene components** — Complete TSX implementation for individual scenes
2. **Animation integration** — Applies spring/interpolate from animation configs
3. **Visual layout** — Implements positioning, sizing, layout logic
4. **Asset integration** — StaticFile imports and asset usage
5. **TypeScript types** — Props interfaces for scene components

## Scope Boundaries

**IN SCOPE:**
- Complete scene component TSX code
- Animation implementation (springs, interpolate)
- Layout and visual styling
- Asset imports and usage
- Component-level logic

**OUT OF SCOPE:**
- Animation config definitions (use `/remotion-animation`)
- Composition sequence layout (use `/remotion-composition`)
- Project scaffolding (use `/remotion-scaffold`)
- Asset sourcing (use `/remotion-asset-coordinator`)

## Input/Output Formats

### Input Format: Visual Direction for Scene

Accepts scene description with visual and animation details:

**From Motion Spec:**
```markdown
## Scene 1: Logo Reveal (0s - 5s)

**Visual Description:**
- Centered logo on dark background
- Logo scales from 0.8 to 1.0 with smooth spring
- Subtitle text fades in below logo
- Background: #0A0A0A (Black)
- Logo color: #FF6B35 (Primary)

**Animation Details:**
- Logo entrance: Frames 0-30
  - Spring config: smooth (damping: 200)
  - Scale: 0.8 → 1.0
  - Opacity: 0 → 1
- Subtitle reveal: Frames 20-50
  - Fade in with slight upward movement
  - TranslateY: 20px → 0
  - Opacity: 0 → 1

**Assets:**
- Logo: public/images/logo.svg
```

**From Natural Language:**
```
Create Scene1Intro with centered logo that springs in from 0.8 scale to 1.0.
Add subtitle text below that fades in after logo.
Use smooth spring animation for logo, linear fade for text.
```

### Output Format: SCENE_COMPONENT.md

Generates complete scene component implementation:

```markdown
# Scene Component: Scene1Intro

## Status
✅ Component implementation complete
⏳ Ready for integration into composition

## Component Code

File: `scenes/Scene1Intro.tsx`

```typescript
import {
  AbsoluteFill,
  spring,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
  Img,
  staticFile,
} from "remotion";
import { COLORS, SPRING_CONFIGS } from "../constants";

export function Scene1Intro() {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  // Logo entrance animation (frames 0-30)
  const logoProgress = spring({
    frame,
    fps,
    config: SPRING_CONFIGS.smooth,
  });

  const logoScale = interpolate(logoProgress, [0, 1], [0.8, 1]);
  const logoOpacity = logoProgress;

  // Subtitle reveal animation (frames 20-50)
  const subtitleProgress = interpolate(
    frame,
    [20, 50],
    [0, 1],
    {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    }
  );

  const subtitleTranslateY = interpolate(subtitleProgress, [0, 1], [20, 0]);
  const subtitleOpacity = subtitleProgress;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: COLORS.background,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {/* Logo */}
      <div
        style={{
          transform: `scale(${logoScale})`,
          opacity: logoOpacity,
        }}
      >
        <Img
          src={staticFile("images/logo.svg")}
          style={{
            width: 400,
            height: 400,
          }}
        />
      </div>

      {/* Subtitle */}
      <div
        style={{
          position: "absolute",
          top: height / 2 + 250,
          transform: `translateY(${subtitleTranslateY}px)`,
          opacity: subtitleOpacity,
        }}
      >
        <h2
          style={{
            color: COLORS.text,
            fontSize: 48,
            fontWeight: 600,
            margin: 0,
          }}
        >
          Innovation in Motion
        </h2>
      </div>
    </AbsoluteFill>
  );
}
```

## Component Props (if needed)

```typescript
export interface Scene1IntroProps {
  // Add props here if scene needs customization
}

// Update component:
export function Scene1Intro({}: Scene1IntroProps) {
  // ...
}
```

## Usage in Composition

```typescript
import { Scene1Intro } from "./scenes/Scene1Intro";

// In main composition:
<Sequence
  from={SCENE_TIMING.intro.start}
  durationInFrames={SCENE_TIMING.intro.duration}
>
  <Scene1Intro />
</Sequence>
```

## Assets Required

- [x] Logo image: `public/images/logo.svg` (400x400)

## Animation Summary

- **Logo entrance:** Smooth spring scale + fade (0-30 frames)
- **Subtitle reveal:** Linear fade + slide up (20-50 frames)

## Next Steps

1. **Add logo asset** to public/images/logo.svg
2. **Test in preview** to verify timing and animation feel
3. **Adjust constants** if needed (scale values, timing)
4. **Move to next scene** via another `/remotion-component-gen` call

## Checklist

- [x] Component implemented
- [x] Animation logic integrated
- [x] Asset imports configured
- [x] TypeScript types defined
- [ ] Asset added to project
- [ ] Tested in preview
```

## Component Implementation Patterns

### Pattern 1: Simple Entrance Animation

Basic spring-based entrance with scale and fade:

```typescript
export function Scene() {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame,
    fps,
    config: SPRING_CONFIGS.smooth,
  });

  const scale = interpolate(progress, [0, 1], [0.8, 1]);

  return (
    <AbsoluteFill
      style={{
        transform: `scale(${scale})`,
        opacity: progress,
      }}
    >
      {/* Content */}
    </AbsoluteFill>
  );
}
```

### Pattern 2: Staggered Elements

Multiple elements with delayed animations:

```typescript
export function Scene() {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const items = ['Feature 1', 'Feature 2', 'Feature 3'];
  const STAGGER_DELAY = 10;

  return (
    <AbsoluteFill>
      {items.map((item, index) => {
        const itemProgress = spring({
          frame: frame - (index * STAGGER_DELAY),
          fps,
          config: SPRING_CONFIGS.snappy,
        });

        const translateX = interpolate(itemProgress, [0, 1], [-50, 0]);

        return (
          <div
            key={index}
            style={{
              transform: `translateX(${translateX}px)`,
              opacity: itemProgress,
              marginBottom: 20,
            }}
          >
            <h3>{item}</h3>
          </div>
        );
      })}
    </AbsoluteFill>
  );
}
```

### Pattern 3: Text Reveal

Character-by-character or word-by-word reveal:

```typescript
export function Scene() {
  const frame = useCurrentFrame();
  const text = "Hello World";
  const CHARS_PER_FRAME = 2;

  const charsToShow = Math.min(
    text.length,
    Math.floor(frame / CHARS_PER_FRAME)
  );

  return (
    <AbsoluteFill>
      <h1 style={{ fontSize: 72 }}>
        {text.slice(0, charsToShow)}
        {charsToShow < text.length && (
          <span style={{ opacity: Math.sin(frame * 0.3) * 0.5 + 0.5 }}>
            |
          </span>
        )}
      </h1>
    </AbsoluteFill>
  );
}
```

## Integration Workflow

1. **Receive visual direction** → Input to this skill
2. **Generate scene component** → SCENE_COMPONENT.md
3. **Create scene file** in scenes/ folder
4. **Add assets** as specified
5. **Test in preview**
6. **Adjust timing/styling** if needed
7. **Move to next scene**

## Integration with Other Skills

This skill works within the pipeline:

```
remotion-component-gen (this skill)
    ↓ outputs: SCENE_COMPONENT.md (per scene)
    ↓ uses: ANIMATION_CONFIG.md (from remotion-animation)
    ↓ uses: COMPOSITION_STRUCTURE.md (for timing context)
```

**Works with:**
- `/motion-designer` — Visual direction from design specs
- `/remotion-animation` — Uses spring configs and timing from this skill
- `/remotion-composition` — Scene fits within timing structure from this skill
- `/remotion-scaffold` — Components added to scaffolded project
- `/remotion-asset-coordinator` — Assets sourced and prepared for import
- `/remotion-spec-translator` — Orchestrated by this skill for full translation

---

This skill generates production-ready scene component implementations that bring motion design specs to life in Remotion.
