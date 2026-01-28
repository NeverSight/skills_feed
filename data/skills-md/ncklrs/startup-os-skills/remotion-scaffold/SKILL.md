---
name: remotion-scaffold
description: Scaffolds Remotion project folder structure, base configuration files, and file organization. Focuses ONLY on directory creation, empty file templates, and Remotion configuration. Use when starting a new video project or when asked to "scaffold Remotion project", "create project structure", "setup Remotion folders".
---

# Remotion Scaffold

Creates the foundational folder structure, configuration files, and organizational framework for Remotion video projects. This skill focuses exclusively on project setup and does NOT generate animation logic or component implementation.

## What This Skill Does

Generates project scaffolding for:

1. **Directory structure** — Organized folder layout for compositions, scenes, assets
2. **Configuration files** — Base constants.ts, types.ts with empty templates
3. **Empty scene templates** — Placeholder scene components with TODO markers
4. **Asset directories** — Organized folders for images, audio, fonts
5. **Registration setup** — Composition registration in Root.tsx

## Scope Boundaries

**IN SCOPE:**
- Creating folder structure
- Writing empty file templates
- Setting up configuration skeleton
- Directory organization patterns

**OUT OF SCOPE:**
- Animation implementation (use `/remotion-animation`)
- Scene component logic (use `/remotion-component-gen`)
- Sequence composition (use `/remotion-composition`)
- Component generation (use `/remotion-component-gen`)

## Input/Output Formats

### Input Format: Project Requirements

Accepts project setup requirements:

**Natural Language:**
```
Create a new Remotion project scaffold for a 30-second video with 4 scenes.
```

**Structured Format:**
```markdown
## Project Requirements

**Project Name:** ProductDemo
**Duration:** 30 seconds
**Frame Rate:** 30 fps
**Dimensions:** 1920x1080 (16:9)
**Number of Scenes:** 4 (Intro, Features, Demo, CTA)
**Asset Types:** Images, Audio (music + SFX)
```

### Output Format: SCAFFOLD_MANIFEST.md

Generates a manifest documenting created structure:

```markdown
# Scaffold Manifest: ProductDemo

## Status
✅ Directory structure created
✅ Configuration files generated
✅ Scene templates created (empty)
⏳ Ready for implementation

## Generated Structure

```
src/remotion/compositions/ProductDemo/
├── index.tsx                 # ✅ Created - Main composition (empty)
├── constants.ts              # ✅ Created - Constants template
├── types.ts                  # ✅ Created - Type definitions
└── scenes/
    ├── Scene1Intro.tsx       # ✅ Created - Empty template
    ├── Scene2Features.tsx    # ✅ Created - Empty template
    ├── Scene3Demo.tsx        # ✅ Created - Empty template
    └── Scene4CTA.tsx         # ✅ Created - Empty template

public/
├── images/                   # ✅ Created - Empty directory
├── audio/
│   ├── music/                # ✅ Created - Empty directory
│   └── sfx/                  # ✅ Created - Empty directory
└── fonts/                    # ✅ Created - Empty directory
```

## File Templates Created

### Main Composition: `index.tsx`
```typescript
import { AbsoluteFill, Sequence } from "remotion";
import { SCENE_TIMING } from "./constants";
import { Scene1Intro } from "./scenes/Scene1Intro";
import { Scene2Features } from "./scenes/Scene2Features";
import { Scene3Demo } from "./scenes/Scene3Demo";
import { Scene4CTA } from "./scenes/Scene4CTA";
import type { ProductDemoProps } from "./types";

export function ProductDemo({}: ProductDemoProps) {
  return (
    <AbsoluteFill>
      {/* TODO: Add composition layout via /remotion-composition */}
      <Sequence
        from={SCENE_TIMING.intro.start}
        durationInFrames={SCENE_TIMING.intro.duration}
      >
        <Scene1Intro />
      </Sequence>

      {/* Additional scenes... */}
    </AbsoluteFill>
  );
}
```

### Constants: `constants.ts`
```typescript
// TODO: Define color palette
export const COLORS = {
  // Add colors here
} as const;

// TODO: Configure spring animations via /remotion-animation
export const SPRING_CONFIGS = {
  // Add spring configs here
} as const;

// Scene timing (30fps, 30 seconds total = 900 frames)
const FPS = 30;

export const SCENE_TIMING = {
  intro: { start: 0, duration: 5 * FPS },
  features: { start: 5 * FPS, duration: 10 * FPS },
  demo: { start: 15 * FPS, duration: 10 * FPS },
  cta: { start: 25 * FPS, duration: 5 * FPS },
} as const;
```

### Types: `types.ts`
```typescript
export interface ProductDemoProps {
  // Add custom props here
}

export interface SceneProps {
  // Common scene props
}
```

### Scene Template: `scenes/Scene1Intro.tsx`
```typescript
import { AbsoluteFill } from "remotion";

export function Scene1Intro() {
  return (
    <AbsoluteFill>
      {/* TODO: Implement scene via /remotion-component-gen */}
    </AbsoluteFill>
  );
}
```

## Next Steps

1. **Define animations** → Run `/remotion-animation` to generate animation configs
2. **Build composition** → Run `/remotion-composition` to structure Sequence layout
3. **Implement scenes** → Run `/remotion-component-gen` for each scene
4. **Configure render** → Run `/remotion-render-config` for output settings
5. **Add assets** → Run `/remotion-asset-coordinator` for asset preparation

## Configuration Summary

| Setting | Value |
|---------|-------|
| **Composition ID** | ProductDemo |
| **Duration** | 30 seconds (900 frames) |
| **Frame Rate** | 30 fps |
| **Dimensions** | 1920x1080 (16:9) |
| **Scenes** | 4 (Intro, Features, Demo, CTA) |
| **Status** | Scaffold complete, ready for implementation |

## File Locations

All files created in:
- **Composition:** `/path/to/project/src/remotion/compositions/ProductDemo/`
- **Assets:** `/path/to/project/public/`

## Scaffold Checklist

Creation checklist:
- [x] Create composition folder structure
- [x] Generate main composition file (`index.tsx`) with TODO markers
- [x] Generate constants file (`constants.ts`) as template
- [x] Generate types file (`types.ts`)
- [x] Create empty scene component files
- [x] Create asset directories (`public/images/`, `public/audio/`)
- [x] Add composition registration skeleton
- [ ] Animation implementation (next: `/remotion-animation`)
- [ ] Composition logic (next: `/remotion-composition`)
- [ ] Scene implementation (next: `/remotion-component-gen`)
```

## Directory Structure Patterns

### Pattern 1: Simple Project (1-2 scenes)

```
src/remotion/compositions/VideoName/
├── index.tsx          # Main composition
├── constants.ts       # Configuration constants
└── types.ts           # TypeScript types
```

### Pattern 2: Multi-Scene Project (3+ scenes)

```
src/remotion/compositions/VideoName/
├── index.tsx           # Main composition
├── constants.ts        # Shared constants
├── types.ts            # Type definitions
└── scenes/
    ├── Scene1.tsx
    ├── Scene2.tsx
    └── Scene3.tsx
```

### Pattern 3: Complex Project (with audio)

```
src/remotion/compositions/VideoName/
├── index.tsx           # Main composition
├── constants.ts        # Configuration
├── types.ts            # Types
├── audio.ts            # Audio configuration
└── scenes/
    └── ...
```

### Pattern 4: Component Library Project

```
src/remotion/
├── components/
│   ├── particles/
│   ├── text/
│   ├── progress/
│   └── transitions/
├── compositions/
│   └── VideoName/
└── utils/
    ├── seededRandom.ts
    └── timing.ts
```

## File Templates

### Empty Main Composition

```typescript
import { AbsoluteFill } from "remotion";
import type { VideoNameProps } from "./types";

export function VideoName({}: VideoNameProps) {
  return (
    <AbsoluteFill>
      {/* TODO: Add composition structure via /remotion-composition */}
    </AbsoluteFill>
  );
}
```

### Empty Constants Template

```typescript
// TODO: Define via /remotion-animation
export const COLORS = {} as const;
export const SPRING_CONFIGS = {} as const;
export const SCENE_TIMING = {} as const;
```

### Empty Types Template

```typescript
export interface VideoNameProps {
  // Add props here
}
```

### Empty Scene Template

```typescript
import { AbsoluteFill } from "remotion";

export function Scene1() {
  return (
    <AbsoluteFill>
      {/* TODO: Implement via /remotion-component-gen */}
    </AbsoluteFill>
  );
}
```

## Registration Template

Add to `src/remotion/Root.tsx`:

```typescript
import { Composition } from "remotion";
import { VideoName } from "./compositions/VideoName";

// Add to RemotionRoot component:
<Composition
  id="VideoName"
  component={VideoName}
  durationInFrames={900}  // TODO: Calculate based on requirements
  fps={30}
  width={1920}
  height={1080}
  defaultProps={{}}
/>
```

## Video Format Presets

Quick reference for common video formats:

```typescript
// YouTube (16:9)
{ width: 1920, height: 1080, fps: 30 }

// Instagram Reels / TikTok (9:16)
{ width: 1080, height: 1920, fps: 30 }

// Twitter/X (16:9)
{ width: 1920, height: 1080, fps: 30 }

// Square (1:1)
{ width: 1080, height: 1080, fps: 30 }
```

## Asset Directory Organization

Standard asset directory structure:

```
public/
├── images/
│   ├── logos/
│   ├── backgrounds/
│   └── icons/
├── audio/
│   ├── music/
│   └── sfx/
└── fonts/
    └── [custom-fonts].woff2
```

## Scaffold Workflow

1. **Parse requirements** → Extract project name, duration, scenes, format
2. **Create directories** → Generate folder structure
3. **Write empty templates** → Create files with TODO markers
4. **Setup registration** → Add composition to Root.tsx
5. **Generate manifest** → Document created structure in SCAFFOLD_MANIFEST.md
6. **Hand off** → Direct to specialized skills for implementation

## Integration with Other Skills

This skill is the FIRST STEP in the pipeline:

```
remotion-scaffold (this skill)
    ↓ outputs: SCAFFOLD_MANIFEST.md
remotion-animation
    ↓ outputs: ANIMATION_CONFIG.md
remotion-composition
    ↓ outputs: COMPOSITION_STRUCTURE.md
remotion-component-gen (per scene)
    ↓ outputs: SCENE_COMPONENT.md
remotion-render-config
    ↓ outputs: RENDER_CONFIG.md
```

**Works with:**
- `/motion-designer` — Project requirements may come from design specs
- `/remotion-animation` — Next step for animation configuration
- `/remotion-composition` — Next step for composition structure
- `/remotion-component-gen` — Next step for scene implementation
- `/remotion-render-config` — Final step for render settings

---

This skill provides clean, minimal project scaffolding that serves as the foundation for the Remotion implementation pipeline.
