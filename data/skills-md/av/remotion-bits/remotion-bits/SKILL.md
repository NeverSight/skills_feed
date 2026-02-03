---
name: remotion-bits
description: Animation components and utilities for Remotion video projects. Use when building Remotion compositions with text animations, gradient transitions, particle effects, 3D scenes, or staggered motion effects. Provides example bits (complete compositions) and reusable components that can be installed via jsrepo.
---

# Remotion Bits

Remotion Bits provides animation components and complete example compositions (bits) for building Remotion videos. The workflow is: discover bits that match your needs, install them, customize, and compose into sequences.

## Installation

```bash
# Initialize jsrepo registry
npx jsrepo init https://unpkg.com/remotion-bits/registry.json

# Install components (reusable building blocks)
npx jsrepo add animated-text particle-system scene-3d

# Install bits (complete example compositions)
npx jsrepo add bit-3d-basic

# Or install from npm (library usage without customization)
npm install remotion-bits
```

Components install to `src/components/`, utilities to `src/utils/`, bits to `src/compositions/`.

## Core Concepts

### 1. Bits vs Components
- **Bits**: Complete, ready-to-use Remotion compositions demonstrating specific patterns (e.g., `bit-3d-basic`, `bit-particles-snow`)
- **Components**: Reusable building blocks used inside bits and custom compositions (e.g., `AnimatedText`, `Particles`, `Scene3D`)

Install bits as starting points for your video. Install components when building custom compositions.

### 2. AnimatedValue Pattern
Most components accept `AnimatedValue` for animated properties:
```tsx
opacity: 1              // Static value
opacity: [0, 1]         // Animate from 0 to 1
opacity: [0, 1, 0.5, 0] // Keyframes over duration
```

### 3. Responsive Sizing
Never hardcode pixel values. Use `useViewportRect()` for responsive scaling:
```tsx
const rect = useViewportRect(); // { width, height, vmin, vmax, vw, vh, cx, cy }
<div style={{ fontSize: rect.vmin * 5 }}>Scales with viewport</div>
```

### 4. Component Categories
- **Text**: `AnimatedText` - character/word/line animations; `TypeWriter` - typewriter effect with cursor/typos; `CodeBlock` - syntax highlighting with line reveals
- **Numbers**: `AnimatedCounter` - interpolate numbers with prefix/postfix
- **Motion**: `StaggeredMotion` - animate multiple elements with timing offsets
- **Visual**: `GradientTransition` - smooth gradient morphing
- **Particles**: `Particles`, `Spawner`, `Behavior` - declarative particle systems
- **3D**: `Scene3D`, `Step`, `Element3D` - camera-based 3D presentations

## Discovering Bits

Bits are complete composition examples that demonstrate component usage. The registry includes bits alongside components and utilities.

To discover available bits:
```bash
# List all bits
jq 'if type == "object" then .items else . end | .[] | select(.type == "bit") | {name, title, description}' registry.json

# Get full details for a specific bit
jq 'if type == "object" then .items else . end | .[] | select(.name == "bit-3d-basic")' registry.json

# Filter by registry dependencies (e.g., bits using scene-3d)
jq 'if type == "object" then .items else . end | .[] | select(.type == "bit" and (.registryDependencies | contains(["scene-3d"])))' registry.json
```

After discovering a bit in the registry, read its source file to understand implementation details.

## Using Bits and Components

### Installing from Registry

```bash
# Install a bit (copies source to src/compositions/)
npx jsrepo add bit-3d-basic

# Install a component (copies source to src/components/)
npx jsrepo add animated-text

# Dependencies are auto-installed via registryDependencies
```

### Customizing Installed Bits

Bits are **starting points**, not rigid templates:
1. Read the bit source in `src/compositions/` after installing
2. Modify timing, styling, content, and animations as needed
3. The source is yours to customize freely

### Assembling Compositions

Use Remotion's `<Sequence>` to combine bits and custom scenes:

```tsx
import { AbsoluteFill, Sequence } from "remotion";
import { Bit3DBasic } from "./compositions/3DBasic";
import { CustomScene } from "./CustomScene";

export const FinalVideo = () => (
  <AbsoluteFill>
    <Sequence from={0} durationInFrames={150}>
      <Bit3DBasic />
    </Sequence>
    <Sequence from={150} durationInFrames={180}>
      <CustomScene />
    </Sequence>
  </AbsoluteFill>
);
```

### Building Custom Compositions

When bits don't fit, build with components directly:

```tsx
import { AnimatedText, useViewportRect } from "remotion-bits";

export const CustomTitle = () => {
  const rect = useViewportRect();

  return (
    <AnimatedText
      transition={{
        split: "character",
        splitStagger: 2,
        opacity: [0, 1],
        y: [rect.vmin * 10, 0],
        duration: 30,
        easing: "easeOutCubic"
      }}
      style={{ fontSize: rect.vmin * 8 }}
    >
      Your Title
    </AnimatedText>
  );
};
```

## Finding Examples

- **Installed bits**: `src/compositions/` - Full working compositions
- **Bit source files**: Query registry for `files[].relativePath` to locate originals
- **Reference patterns**: [references/patterns.md](references/patterns.md) - Common recipes
- **Component APIs**: [references/components.md](references/components.md) - Props and usage

## Reference Files

For detailed API documentation:
- [references/components.md](references/components.md) - Full component props reference
- [references/utilities.md](references/utilities.md) - Utility functions reference
- [references/patterns.md](references/patterns.md) - Common animation patterns
and Using Bits

### Finding Bits

Bits are discoverable via the jsrepo registry. Use `jq` to query `registry.json`:

```bash
# List all available bits
jq 'if type == "object" then .items else . end | .[] | select(.type == "bit") | {name, title, description}' registry.json

# Find bits using specific components (e.g., Scene3D)
jq 'if type == "object" then .items else . end | .[] | select(.type == "bit" and (.registryDependencies | contains(["scene-3d"])))' registry.json

# Get installation details for a specific bit
jq 'if type == "object" then .items else . end | .[] | select(.name == "bit-3d-basic")' registry.json
```

After finding a bit in the registry, **read its source file** to understand the implementation before installing.

### Installing Bits

```bash
# Install a bit (copies source to src/compositions/)
npx jsrepo add bit-3d-basic

# Dependencies are auto-installed (e.g., scene-3d component)
```

### Customizing Bits

Bits are **starting points for customization**, not rigid templates:

1. Read the bit source file to understand its structure
2. Install the bit via jsrepo (copies source code to your project)
3. Modify the composition in `src/compositions/` to fit your needs
4. Adjust timing, styling, content, animations as needed

### Common Bit Patterns

When reviewing bit source files, look for:
- **`metadata.registry.registryDependencies`**: Which components the bit uses
- **`useViewportRect()`**: How it handles responsive sizing
- **Timing**: `duration`, `transitionDuration`, stagger values
- **Animation patterns**: How `AnimatedValue` arrays create motion
- **Component composition**: How multiple components work together

## Assembling Remotion Videos

### Sequencing with Remotion

Use `<Sequence>` to combine bits and custom scenes:

```tsx
import { AbsoluteFill, Sequence } from "remotion";
import { Bit3DBasic } from "./compositions/3DBasic";
import { BitParticlesSnow } from "./compositions/ParticlesSnow";

export const FinalVideo = () => (
  <AbsoluteFill>
    <Sequence from={0} durationInFrames={150}>
      <Bit3DBasic />
    </Sequence>
    <Sequence from={150} durationInFrames={180}>
      <BitParticlesSnow />
    </Sequence>
  </AbsoluteFill>
);
```

### Building Custom Compositions

When bits don't fit your needs, build custom compositions with components:

```tsx
import { AnimatedText, useViewportRect } from "remotion-bits";
import { useCurrentFrame } from "remotion";

export const CustomTitle = () => {
  const rect = useViewportRect();

  return (
    <AnimatedText
      transition={{
        split: "character",
        splitStagger: 2,
        opacity: [0, 1],
        y: [rect.vmin * 10, 0],
        duration: 30,
        easing: "easeOutCubic"
      }}
      style={{ fontSize: rect.vmin * 8 }}
    >
      Your Title Here
    </AnimatedText>
  );
};
```

## Key Components Overview

For detailed API documentation, see reference files below. Quick reference:

- **AnimatedText**: Text with character/word/line splitting, stagger, and transitions
- **TypeWriter**: Classic typewriter effect with cursor blinking, typos simulation, and variable speeds
- **CodeBlock**: Syntax highlighted code with line-by-line reveal, highlighting, and focus regions
- **AnimatedCounter**: Number interpolation with transition support
- **StaggeredMotion**: Animate child elements with stagger and directional timing
- **GradientTransition**: Smooth gradient morphing with Oklch interpolation
- **Particles + Spawner + Behavior**: Declarative particle systems with physics
- **Scene3D + Step + Element3D**: Camera-based 3D presentations (impress.js style)

Import from `remotion-bits` or from installed component files in `src/components/`.

## Reference Documentation

For comprehensive API details:
- [references/components.md](references/components.md) - Complete component props and examples
- [references/utilities.md](references/utilities.md) - Utility functions (interpolate, color, geometry)
- [references/patterns.md](references/patterns.md) - Common animation patterns and recipe