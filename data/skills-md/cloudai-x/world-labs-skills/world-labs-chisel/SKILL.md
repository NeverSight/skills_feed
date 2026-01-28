---
name: world-labs-chisel
description: Chisel 3D blocking tool for world generation - geometry, walls, and reference models
allowed-tools:
  - Bash
  - WebFetch
---

# World Labs Chisel Tool

Chisel is an AI-native 3D blocking tool that separates **structure** from **style** for world generation. Define room layouts, architectural structures, and scene composition—then let AI fill in the visual details.

## Overview

Chisel decouples geometry from aesthetics:

- **Structure**: You define with 3D blocking (walls, volumes, layouts)
- **Style**: AI generates based on your text prompt

This separation enables rapid iteration—change the prompt to get completely different visual styles while keeping the same spatial layout.

## Accessing Chisel

1. Go to <https://marble.worldlabs.ai>
2. Click the **Omnibox** → Select **3D Input** mode
3. Click **Start** to enter the Chisel Scene
4. Or open existing world → Edit in Chisel

**Documentation**: <https://docs.worldlabs.ai/marble/create/chisel-tools/chisel-basics>

## Core Concepts

### Structure vs Style

```
┌─────────────────────────────────────────────────┐
│         CHISEL (You Define)                     │
│  ┌───────────────────────────────────────────┐  │
│  │  3D Geometry: walls, volumes, layout      │  │
│  │  Reference models: furniture placement    │  │
│  │  Camera position: viewpoint for generation│  │
│  └───────────────────────────────────────────┘  │
│                      +                          │
│         TEXT PROMPT (You Describe)              │
│  ┌───────────────────────────────────────────┐  │
│  │  Style: "modern minimalist" / "rustic"    │  │
│  │  Materials: "marble floors" / "wood"      │  │
│  │  Lighting: "warm sunset" / "neon"         │  │
│  │  Details: paintings, plants, furniture    │  │
│  └───────────────────────────────────────────┘  │
│                      =                          │
│         GENERATED WORLD (AI Creates)            │
│  ┌───────────────────────────────────────────┐  │
│  │  Your layout + AI-generated visuals       │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

## Tools & Keyboard Shortcuts

| Tool         | Key             | Description                   |
| ------------ | --------------- | ----------------------------- |
| Wall Tool    | `X`             | Draw walls by clicking points |
| Extrude Tool | `Z`             | Pull faces to create volumes  |
| Delete       | `Delete`        | Remove selected geometry      |
| Undo         | `⌘Z` / `Ctrl+Z` | Undo last action              |

### Navigation

| Action     | Control              |
| ---------- | -------------------- |
| Orbit View | Middle Mouse         |
| Pan View   | Shift + Middle Mouse |
| Zoom       | Scroll Wheel         |

## Wall Tool (X)

Create walls by clicking to place points:

```
Click sequence:
    1 ──────── 2
              │
              │
    4 ──────── 3

Result: A rectangular room outline
```

### Usage

1. Press `X` to activate
2. Click to place wall start point
3. Click to place subsequent corners
4. Double-click or press `Enter` to finish
5. Adjust wall height using wall handles

### Tips

- Hold `Shift` for straight lines (snaps to angles)
- Walls automatically have height - adjust in properties panel
- Create openings by selecting wall segments and adjusting

## Extrude Tool (Z)

Pull 2D faces into 3D volumes:

```
Before:           After extrude:
┌─────┐           ┌─────┐
│     │           │ ╱   │╲
│     │    →      │╱    │ ╲
└─────┘           └─────┘  │
                   ╲      ╱
                    ╲────╱
```

### Usage

1. Select a face (floor, ceiling, wall)
2. Press `Z` to activate extrude
3. Drag to pull out geometry
4. Click to confirm

### Tips

- Extrude floor to create platforms, steps, raised areas
- Extrude walls to create alcoves, pillars, protrusions
- Negative extrude (push in) for recesses, doorways

## Reference Geometry Import

Upload 3D models as starting points or guides:

### Supported Formats

| Format | Description          | Max Size |
| ------ | -------------------- | -------- |
| GLB    | Recommended, compact | 100 MB   |
| FBX    | Wide compatibility   | 100 MB   |

### How to Use

1. Click "Import Reference" or upload via template
2. Upload your GLB/FBX file
3. Position and scale the reference using handles
4. Use as basis for blocking out geometry
5. The reference defines structure; AI adds style

### Good Reference Models

- Simple architectural blockouts
- Furniture placement guides
- Terrain rough shapes
- Vehicle/prop silhouettes

## Generation Workflow

### Step 1: Block Out Geometry

```
┌────────────────────┐
│    ┌──┐            │
│    │  │  ← pillar  │
│    └──┘            │
│                    │
│ ╔════╗             │
│ ║door║             │
│ ╚════╝             │
└────────────────────┘
```

### Step 2: Position Panorama Camera

- Place camera at desired viewpoint
- Adjust height for perspective
- Rotate to face desired direction

### Step 3: Add Text Prompt

```
"Ancient stone temple interior with torches,
moss-covered walls, dramatic lighting through
cracks in the ceiling"
```

### Step 4: Generate

- Select model: `Marble 0.1-plus` (quality) or `Marble 0.1-mini` (draft)
- Click **Generate**
- AI transforms your blocks into detailed world

### Step 5: Iterate

- Change only the text prompt to explore different styles
- Same structure can become: modern, medieval, sci-fi, etc.

## Best Practices

### DO

✅ **Start simple**: Block major shapes first, add detail later
✅ **Define boundaries**: Clear walls help the model understand space
✅ **Use reference**: Import models for complex shapes
✅ **Consider scale**: Block at realistic proportions
✅ **Leave openings**: Doors, windows, passages for flow
✅ **Iterate on style**: Try different prompts with same geometry

### DON'T

❌ **Over-detail geometry**: Blocks should be rough; AI adds visual detail
❌ **Ignore physics**: Floating geometry may cause issues
❌ **Create impossible spaces**: Non-euclidean geometry confuses the model
❌ **Skip the prompt**: Text is crucial for guiding the style

## Common Patterns

### Interior Room

```
1. Draw outer walls (X)
2. Add interior walls for rooms
3. Cut doorways (negative extrude)
4. Raise platform for level changes
5. Add pillar blocks
6. Prompt: describe style, era, condition
```

### Outdoor Scene

```
1. Create ground plane
2. Extrude terrain features (hills, cliffs)
3. Block building volumes
4. Add path/road depressions
5. Prompt: describe biome, time, weather
```

### Cave/Tunnel

```
1. Create solid block
2. Negative extrude tunnel path
3. Add chamber volumes
4. Create uneven surfaces
5. Prompt: describe rock type, lighting, features
```

## Style Variation Examples

Same geometry, different prompts:

| Prompt                                       | Result              |
| -------------------------------------------- | ------------------- |
| "Modern minimalist gallery with white walls" | Clean, contemporary |
| "Medieval castle great hall with tapestries" | Gothic, historical  |
| "Cyberpunk nightclub with neon lighting"     | Futuristic, vibrant |
| "Abandoned warehouse, overgrown with vines"  | Post-apocalyptic    |

## Note on API Integration

Chisel is primarily a **UI-based tool** within the Marble app. The blocked-out geometry is used during generation within the Marble interface.

For programmatic world generation, use:

- `world-labs-image-prompt` - Single image as input
- `world-labs-multi-image` - Multiple images with direction control
- `world-labs-text-prompt` - Text-only generation

## Related Skills

- `world-labs-api` - API integration
- `world-labs-text-prompt` - Prompting best practices
- `world-labs-studio` - Compose and animate generated worlds
- `world-labs-export` - Export formats
