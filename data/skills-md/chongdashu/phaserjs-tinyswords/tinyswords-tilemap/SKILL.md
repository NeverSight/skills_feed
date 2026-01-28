---
name: tinyswords-tilemap
description: >
  Build tilemaps using Tiny Swords asset pack. Handles 64x64 tile grid, elevation layers,
  water foam animation, shadow positioning, and terrain color variants. Use when creating
  game maps, level editors, or rendering terrain with the Tiny Swords tileset.
---

# Tiny Swords Tilemap

Create beautiful, layered tilemaps using the Tiny Swords asset pack with proper elevation, shadows, and animated water effects.

## Philosophy: Elevation as Visual Storytelling

Tilemaps are not just grids of images—they are **layered compositions that create depth and dimensionality**. The Tiny Swords tileset uses a clever layering system where shadows and elevation work together to create the illusion of 3D terrain on a 2D plane.

**Before placing tiles, ask**:
- What elevation levels does this area need?
- Where will the player's eye be drawn?
- How do shadows reinforce the sense of height?
- Does the water feel alive with staggered foam animations?

**Core principles**:

1. **Layers create depth**: Every elevation level adds Shadow + Elevated Ground layers. The stack builds visual height.
2. **Shadows anchor elevation**: A shadow one tile below the walkable surface makes cliffs feel real.
3. **Animation breaks uniformity**: Water foam sprites starting at different frames prevent the "wallpaper effect."
4. **Color distinguishes levels**: Using different terrain colors for each elevation helps players parse the map instantly.

## Tile Specifications

| Element | Size | Notes |
|---------|------|-------|
| Standard tile | 64x64 px | Base grid unit for all terrain |
| Shadow sprite | 128x128 px | Placed on 64x64 grid, overlaps adjacent tiles |
| Animation frame | 64x64 px | Water foam frames in sprite sheets |

## The Six Terrain Components

1. **BG Color** - Water background fill (bottommost layer)
2. **Water Foam** - Animated waves where terrain meets water
3. **Flat Ground** - Lowest walkable terrain adjacent to water
4. **Shadows** - Depth sprites placed below elevated areas
5. **Elevated Ground** - Raised terrain with cliff edges
6. **Stairs** - Connectors between elevation levels

## Layer Ordering (Bottom to Top)

```
┌─────────────────────────────────────────┐
│  Elevated Ground (Level N)              │  ← Repeat for each
│  Shadow (Level N)                       │    elevation level
├─────────────────────────────────────────┤
│  Elevated Ground (Level 2)              │
│  Shadow (Level 2)                       │
├─────────────────────────────────────────┤
│  Elevated Ground (Level 1)              │
│  Shadow (Level 1)                       │
├─────────────────────────────────────────┤
│  Flat Ground                            │
│  Water Foam (animated)                  │
│  BG Color (water background)            │
└─────────────────────────────────────────┘
```

## Shadow Positioning

Shadows create the illusion of height. Position each shadow sprite **one 64x64 tile below** the walkable elevated ground it belongs to.

```
Grid visualization:
    ┌────┬────┬────┐
    │    │WALK│    │  ← Elevated walkable area
    ├────┼────┼────┤
    │    │SHAD│    │  ← Shadow positioned here (one tile down)
    └────┴────┴────┘
```

The 128x128 shadow sprite is placed on the 64x64 grid, allowing it to overlap and create soft depth transitions.

## Water Foam Animation

Water foam is animated and requires **staggered frame starts** to look natural.

**Implementation pattern**:
```javascript
// Each foam sprite instance starts at a random/offset frame
foamSprites.forEach((sprite, index) => {
  sprite.animationOffset = index % totalFrames;
  // OR
  sprite.animationOffset = Math.floor(Math.random() * totalFrames);
});
```

This prevents the synchronized "breathing" effect where all water animates in lockstep.

## Stair Configurations

Stairs connect elevation levels with two configurations based on adjacent terrain:

| Adjacent Terrain | Stair Pieces | Description |
|------------------|--------------|-------------|
| Walkable ground | Single center piece | Minimal connection |
| Cliff edges | Two pieces (top + bottom) | Full stair with cliff transitions |

## Terrain Color Variants

Five terrain colors are available (`Tilemap_color1.png` through `Tilemap_color5.png`). Use different colors for different elevation levels to enhance visual distinction:

```
Level 3: color5 (purple/dark)
Level 2: color3 (brown)
Level 1: color1 (green)
Flat:    color2 (sand/beach)
```

Mix colors intentionally—there's no required order, but contrast between adjacent levels improves readability.

## Anti-Patterns to Avoid

**Flat layering**: Placing all terrain on a single layer
- Why bad: Loses depth, looks like a flat texture
- Better: Use the full layer stack with shadows

**Synchronized water animation**: All foam sprites on the same frame
- Why bad: Creates artificial "pulsing" effect
- Better: Stagger animation start frames

**Shadow misalignment**: Shadows directly under or beside elevated ground
- Why bad: Breaks the height illusion
- Better: Shadow exactly one tile below walkable surface

**Monotone elevation**: Same terrain color for all levels
- Why bad: Hard to visually parse map depth
- Better: Distinct colors per elevation level

**Ignoring cliff types**: Using wrong cliff edge for context
- Why bad: Visual discontinuity at terrain boundaries
- Better: Use water-facing cliffs near water, terrain-facing cliffs near lower ground

## Variation Guidance

**Maps should vary based on context**:
- Island maps: More water foam, fewer elevation levels
- Mountain maps: Multiple elevation levels, less water
- Mixed terrain: Blend all elements with color variety

**Avoid converging on**:
- Always using color1 for everything
- Exactly 2 elevation levels every time
- Identical stair placement patterns
- Uniform shadow density

## Asset Paths Reference

See references/asset-paths.md for complete file paths in this project.

## Remember

The Tiny Swords tileset is designed for **layered depth**. Every shadow, every foam animation offset, every color choice contributes to a map that feels alive and dimensional. Trust the layer system—it's engineered to create beautiful results when used correctly.
