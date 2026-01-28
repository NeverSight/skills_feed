---
name: gemini-image-prompting
description: Patterns for prompting Gemini to generate conceptual images for game development. Use when creating concept art, UI mockups, character designs, environment sketches, or visual references.
allowed-tools: Read, Write, Edit
---

# Gemini Image Prompting for Game Dev

---

## Quick Reference

**Gemini Models for Image Generation:**
- **Gemini 2.0 Flash** - Fast, good for iteration
- **Imagen 3** - Higher quality, more detailed

**Key Principle:** Be specific about style, composition, and game context.

---

## Prompt Structure Template

```
[STYLE] [SUBJECT] [ACTION/POSE] [ENVIRONMENT] [LIGHTING] [CAMERA] [GAME CONTEXT]
```

### Example:
```
Low-poly stylized 3D render of a treasure chest, slightly open with gold coins spilling out,
on a stone dungeon floor, warm torchlight from the left, isometric view,
Roblox pet simulator style, clean edges, vibrant colors
```

---

## Style Modifiers by Game Type

### Roblox/Blocky Style
```
- "low-poly blocky style"
- "Roblox-inspired aesthetic"
- "cubic voxel art"
- "smooth plastic material"
- "vibrant saturated colors"
- "clean geometric shapes"
- "chunky proportions"
```

### Anime/Stylized
```
- "anime cel-shaded"
- "Genshin Impact style"
- "soft gradient shading"
- "expressive eyes, simplified features"
- "dynamic action pose"
- "speed lines, motion blur"
```

### Realistic/Semi-Realistic
```
- "semi-realistic 3D render"
- "PBR materials"
- "subsurface scattering on skin"
- "realistic lighting with ray tracing"
- "detailed textures"
```

### Pixel Art
```
- "16-bit pixel art"
- "limited color palette (16 colors)"
- "clean pixel edges, no anti-aliasing"
- "retro SNES style"
```

---

## Subject Categories

### Character Concepts

**Template:**
```
[Style] character concept art of [description], [pose], [outfit details],
[expression], [accessories], front and side view, game-ready design,
[game reference style]
```

**Example - Pet Simulator Pet:**
```
Cute low-poly 3D render of a baby dragon pet, sitting pose,
bright purple scales with golden belly, big sparkly eyes, tiny wings folded,
happy expression, Roblox pet simulator style, clean topology,
vibrant colors on white background
```

**Example - Fighter Character:**
```
Anime cel-shaded character concept of a martial arts master,
dynamic fighting stance, flowing white gi with red trim,
determined expression, bandaged fists,
Street Fighter inspired style, front view with action pose variation
```

### Environment/Map Concepts

**Template:**
```
[Style] environment concept art, [biome/location type], [key landmarks],
[atmosphere], [time of day], [weather], bird's eye view / establishing shot,
game level design reference
```

**Example - Tycoon Hub:**
```
Isometric low-poly 3D render of a colorful tycoon game hub area,
central fountain plaza, surrounding shop stalls with striped awnings,
winding paths connecting areas, bright daylight, cheerful atmosphere,
Roblox simulator map style, vibrant greens and warm oranges
```

**Example - Obby Stage:**
```
Side-scrolling platformer level concept, floating islands in a candy sky,
rainbow bridges, bouncy mushroom platforms, checkpoint flags,
cotton candy clouds, magical sparkles, whimsical game art style
```

### UI/HUD Concepts

**Template:**
```
Game UI mockup, [UI element type], [game genre], [color scheme],
[key information displayed], clean vector style, [screen position],
mobile-friendly / desktop layout
```

**Example - Shop UI:**
```
Game UI mockup of a pet shop interface, 4x3 grid of pet cards,
each card showing pet icon, name, rarity stars, and price,
purchase button at bottom, currency display top-right,
purple and gold color scheme, clean flat design, Roblox style
```

**Example - HUD:**
```
Game HUD overlay design, top-left health bar (red gradient),
top-right coin counter with icon, bottom-center hotbar with 5 slots,
minimap top-right corner, semi-transparent dark panels,
modern flat UI style, 16:9 aspect ratio
```

### VFX/Particle Concepts

**Template:**
```
[Style] visual effect concept, [effect type], [color palette],
[particle behavior description], [context/trigger],
game VFX reference sheet, transparent background
```

**Example - Hit Effect:**
```
Anime-style impact VFX concept sheet, punch hit effect,
white starburst with yellow energy rings expanding outward,
small debris particles, speed lines radiating from center,
4-frame animation sequence, transparent background
```

**Example - Magic Spell:**
```
Fantasy magic spell VFX concept, ice nova explosion,
crystalline shards bursting outward, swirling snowflakes,
blue-white-cyan color palette, frost mist at base,
top-down view for game implementation reference
```

### Item/Prop Concepts

**Template:**
```
[Style] game prop concept, [item name], [material/texture],
[special features], [size reference], multiple angles,
inventory icon and 3D model reference
```

**Example - Weapon:**
```
Low-poly stylized sword concept, legendary fire blade,
black steel with glowing orange runes, flame particles along edge,
ornate golden crossguard, 3/4 view and top-down icon,
RPG game item style, clean geometry for 3D modeling
```

---

## Lighting Keywords

| Mood | Keywords |
|------|----------|
| **Cheerful** | bright daylight, warm sunlight, soft shadows, vibrant |
| **Mysterious** | dim ambient, purple haze, rim lighting, foggy |
| **Dramatic** | harsh shadows, single spotlight, high contrast |
| **Cozy** | warm indoor lighting, fireplace glow, soft orange |
| **Spooky** | green/purple underlighting, long shadows, moonlight |
| **Epic** | golden hour, god rays, dramatic clouds |

---

## Camera/Composition Keywords

| View | Use For |
|------|---------|
| **Isometric** | Tycoon maps, base builders, strategy games |
| **Front view** | Character sheets, shop items |
| **3/4 view** | Props, buildings, general purpose |
| **Bird's eye** | Map overviews, level layouts |
| **Dynamic angle** | Action shots, combat, promotional art |
| **Side view** | Platformer levels, 2D game assets |

---

## Quality Boosters

Add these to improve output:
```
- "high detail"
- "professional game art"
- "clean lines"
- "game-ready design"
- "concept art quality"
- "artstation trending" (use sparingly)
- "vibrant colors"
- "clear silhouette"
```

---

## Negative Prompt Guidance

Tell Gemini what to avoid:
```
- "no text, no watermarks"
- "no realistic human faces" (for stylized)
- "no cluttered background"
- "avoid dark muddy colors"
- "no blurry edges"
```

---

## Iteration Workflow

1. **First Pass - Broad Concept:**
   ```
   Low-poly pet concept, cute dragon, purple, Roblox style
   ```

2. **Refine - Add Details:**
   ```
   Low-poly 3D pet concept, baby dragon, sitting pose, purple scales
   with gold accents, big sparkly eyes, tiny wings, Roblox simulator style
   ```

3. **Final - Full Specification:**
   ```
   Cute low-poly 3D render of a baby dragon pet for Roblox simulator game,
   sitting pose looking upward, bright purple scales with metallic gold belly,
   oversized sparkly cyan eyes, tiny folded wings, happy open-mouth smile,
   clean geometric topology, vibrant saturated colors, white background,
   game-ready character design, front and 3/4 view
   ```

---

## Game-Specific Prompt Examples

### Pet Simulator Map Overview
```
Isometric bird's eye view of a pet simulator game hub map,
hexagonal layout with central spawn plaza,
6 themed zones radiating outward (forest, ocean, desert, snow, volcano, candy),
winding paths connecting zones, small shop buildings with colorful awnings,
bright cheerful lighting, Roblox low-poly style,
vibrant greens, blues, and warm accent colors
```

### Tycoon Dropper Machine
```
Low-poly 3D render of a tycoon game dropper machine,
industrial factory style, conveyor belt base,
hopper at top dropping golden coins,
pipes and gears decoration, steam particles,
grey metal with orange safety stripes,
isometric view, Roblox tycoon style
```

### Obby Checkpoint
```
Low-poly 3D checkpoint platform for obby game,
glowing green circular pad, particle ring effect,
floating crystal above, "Stage 5" text hologram,
clean geometric design, bright friendly colors,
front 3/4 view, Roblox obby style
```

### Fighting Game Character Select
```
Game UI mockup of fighting game character select screen,
3x4 grid of character portrait frames,
selected character highlighted with golden border,
large character preview on right side in fighting pose,
player name and stats below preview,
dark purple gradient background with energy particles,
anime fighting game style, 16:9 layout
```

---

## 3D Model Reference Sheets (For Roblox Building)

Use these prompts to generate multi-view concept art that you can then build programmatically in Roblox using Parts.

### Why Multi-View Sheets?

When building 3D models from Parts in Roblox, you need to know:
- **Proportions** from multiple angles
- **Part breakdown** - which boxes/shapes make up the model
- **Colors** for each section
- **Size ratios** between components

A 3x3 or orthographic grid gives you all the reference you need.

---

### Template: 3x3 Model Reference Grid

```
Create a 3x3 grid reference sheet for a [SUBJECT] in classic Roblox stud style.

Grid layout:
- Top row: Front view | Side view | Back view
- Middle row: 3/4 front-left | Top-down view | 3/4 front-right
- Bottom row: Close-up detail | Full model with scale reference | Color palette

Style requirements:
- Blocky low-poly shapes (build from rectangular boxes)
- Classic Roblox stud texture on surfaces
- Vibrant solid colors (no gradients)
- Clean edges, no bevels or smooth curves
- Show part seams/divisions where pieces connect
- White or light gray background
- Each view clearly labeled

Subject: [DESCRIPTION]
Colors: [COLOR REQUIREMENTS]
Scale: [SIZE REFERENCE - e.g., "human character is 5 studs tall"]
```

---

### Example: Dragon Model Reference

```
Create a 3x3 grid reference sheet for a dragon in classic Roblox stud style.

Grid layout:
- Top row: Front view | Side view | Back view
- Middle row: 3/4 front-left | Top-down view | 3/4 front-right
- Bottom row: Head close-up | Full model with Roblox character for scale | Color/part breakdown

Style requirements:
- Blocky low-poly shapes (build from rectangular boxes only)
- Classic Roblox stud texture on all surfaces
- Vibrant solid colors, no gradients
- Clean edges, chunky proportions
- Show clear part divisions (body, head, neck, tail segments, wings, legs)
- White background
- Each view labeled

Subject: Fierce dragon with wings spread, sitting pose
Colors: Bright red body, orange belly, yellow eyes, dark grey claws
Scale: Dragon body is 10 studs long, 6 studs tall (without wings)
```

---

### Example: Treasure Chest Model Reference

```
Create a 3x3 grid reference sheet for a treasure chest in classic Roblox stud style.

Grid layout:
- Top row: Front (closed) | Side view | Back view
- Middle row: Front (open) | Top-down (open) | 3/4 view (open)
- Bottom row: Lid detail | Treasure contents | Part breakdown with measurements

Style requirements:
- Blocky rectangular shapes only
- Classic Roblox stud texture
- Show hinges and metal bands as separate parts
- Clear color separation between wood and metal parts
- White background, labeled views

Subject: Pirate treasure chest, slightly open showing gold coins
Colors: Reddish brown wood, dark stone grey metal bands, bright yellow gold
Scale: Chest is 4 studs wide, 3 studs deep, 3 studs tall
```

---

### Example: Vehicle Model Reference

```
Create a 3x3 grid reference sheet for a race car in classic Roblox stud style.

Grid layout:
- Top row: Front view | Side view | Rear view
- Middle row: 3/4 front | Top-down | 3/4 rear
- Bottom row: Wheel detail | Interior/cockpit | Exploded part diagram

Style requirements:
- Blocky low-poly shapes, NO smooth curves
- Classic Roblox stud texture on body panels
- Show clear part divisions (body, hood, wheels, spoiler, windows)
- Wheels are cylinders, body is boxes
- White background, labeled views

Subject: Sporty race car with rear spoiler
Colors: Bright red body, black wheels, white racing stripes, light blue windows
Scale: Car is 12 studs long, 5 studs wide, 3 studs tall
```

---

### Example: Building/Structure Reference

```
Create a 3x3 grid reference sheet for a medieval tower in classic Roblox stud style.

Grid layout:
- Top row: Front view | Side view | Back view
- Middle row: 3/4 view | Top-down (roof removed) | Cross-section interior
- Bottom row: Door detail | Window detail | Part breakdown by floor

Style requirements:
- Blocky stone brick construction
- Classic Roblox stud texture
- Crenellations on top (battlement pattern)
- Show floor divisions, wall thickness
- White background, labeled views

Subject: Three-story castle tower with pointed roof
Colors: Medium stone grey walls, dark stone grey trim, bright red roof, reddish brown door
Scale: Tower is 20 studs tall, 10 studs wide base
```

---

### Example: Character/Creature Reference

```
Create a 3x3 grid reference sheet for a robot character in classic Roblox stud style.

Grid layout:
- Top row: Front view | Side view | Back view
- Middle row: 3/4 view | Top-down | Action pose
- Bottom row: Head detail | Hand/arm detail | Part breakdown (body segments)

Style requirements:
- Blocky rectangular robot parts
- Classic Roblox stud texture on metal surfaces
- Clear joint divisions (head, torso, arms, legs as separate parts)
- Visible seams between body segments
- White background, labeled views

Subject: Friendly helper robot with antenna and claw hands
Colors: Bright blue body, medium stone grey joints, bright yellow eyes, black accents
Scale: Robot is 6 studs tall (same as Roblox character)
```

---

### Example: Pet/Creature Reference

```
Create a 3x3 grid reference sheet for a slime pet in classic Roblox stud style.

Grid layout:
- Top row: Front view | Side view | Back view
- Middle row: 3/4 happy | Top-down | 3/4 bouncing pose
- Bottom row: Face expressions (happy/sad/angry) | Size variations (S/M/L) | Color variations

Style requirements:
- Blocky/chunky blob shape (NOT smooth - use stacked boxes)
- Classic Roblox stud texture
- Simple dot eyes and smile
- Show how to build rounded shape from rectangular parts
- White background, labeled views

Subject: Cute bouncy slime pet
Colors: Lime green body, white eyes, pink cheeks (optional)
Scale: Small = 2 studs, Medium = 3 studs, Large = 5 studs
```

---

### Orthographic View Template (Technical)

For more precise building reference:

```
Create an orthographic projection reference sheet for [SUBJECT] in Roblox stud style.

Layout (2x3 grid):
- Top row: TOP view | FRONT view | RIGHT SIDE view
- Bottom row: BOTTOM view | BACK view | LEFT SIDE view

Requirements:
- Pure orthographic projection (no perspective distortion)
- Grid overlay showing stud measurements
- Each view same scale
- Part outlines showing where to divide model
- Dimension labels in studs
- Classic Roblox stud texture
- Flat lighting, no dramatic shadows

Subject: [DESCRIPTION]
Measurements: Include stud dimensions for key parts
```

---

### Part Breakdown Prompt

When you need to see how to construct a model from Parts:

```
Create an exploded view diagram of [SUBJECT] showing all individual parts separated.

Requirements:
- Roblox stud style (blocky, rectangular parts only)
- Each part pulled apart to show assembly
- Parts numbered and labeled
- Arrows showing how pieces connect
- Color-coded by section (body=red, limbs=blue, details=yellow)
- Include a "assembled" thumbnail in corner
- White background

Show part list:
- Part name
- Approximate size in studs (LxWxH)
- BrickColor name

Subject: [DESCRIPTION]
```

---

### Quick Reference: View Types

| View | Best For |
|------|----------|
| **Front** | Face, main features, symmetry check |
| **Side** | Profile, depth, limb positions |
| **Back** | Tail, back details, symmetry |
| **Top-down** | Footprint, wing span, overall shape |
| **3/4** | Most natural view, shows depth |
| **Exploded** | Understanding part assembly |
| **Cross-section** | Interior details, wall thickness |

---

### Stud Style Keywords

Always include these for Roblox-buildable concepts:
```
- "classic Roblox stud texture"
- "blocky low-poly"
- "rectangular box shapes only"
- "no smooth curves or bevels"
- "visible part seams"
- "chunky proportions"
- "vibrant solid BrickColors"
- "clean geometric construction"
```

---

## Map Layout Concept Prompts (Detailed)

Use this format for generating detailed top-down 2D concept map layouts with labeled zones, connections, and clear structure.

### Template Structure:
```
Create a top-down 2D concept map layout for a [GAME TYPE] game. The map should show:

[ZONE TYPE 1] ([quantity/location]):
- [Feature 1]
- [Feature 2]
- [Feature 3]

[ZONE TYPE 2] ([location]):
- [Feature 1]
- [Feature 2]

[SPECIAL AREAS]:
- [Area 1]: [description]
- [Area 2]: [description]

CONNECTIONS:
- [How zones connect]
- [Pathways and travel methods]
- [Gates/requirements]

MAP BORDERS:
- [Natural border types by direction]

STYLE:
- [Art style]
- [Perspective]
- [Labels and legend requirements]
```

---

### Example: Tycoon-Simulator Hybrid Map

```
Create a top-down 2D concept map layout for a Roblox tycoon-simulator hybrid game. The map should show:

PERSONAL TYCOON PLOTS (grid of 12-16 plots around the map edges):
- Individual player bases (square plots)
- Each plot has: Dropper → Conveyor → Processor → Collection bin
- Upgrade pads inside each plot
- Plot expansion areas (locked sections)

CENTRAL SHARED HUB (large area in center):
- Main spawn point
- Sell station (where players sell collected items)
- Shop building (buy droppers, conveyors, upgrades)
- Rebirth shrine (prestige system)
- Global leaderboard display
- Daily rewards chest
- Codes redemption NPC

SHARED FARMING/GRINDING ZONES (between hub and plots):
- Zone A (Starter Field): Basic collectibles, anyone can farm
- Zone B (Premium Grove): Better drops, requires rebirth 1+
- Zone C (Elite Quarry): Rare materials, requires rebirth 5+
- Zone D (Legendary Void): End-game drops, requires rebirth 10+

SPECIAL AREAS:
- Pet sanctuary (hatch/equip pets that boost earnings)
- Trading plaza (player-to-player trading)
- VIP lounge (gamepass exclusive zone with 2x multiplier)
- Event stage (seasonal/limited time events)
- Minigame arena (quick games for bonus cash)

CONNECTIONS:
- Main road from hub to each zone
- Pathways between tycoon plots
- Teleport pads for quick travel
- Gates with level/rebirth requirements between zones

MAP BORDERS:
- Mountains on north and east edges
- Ocean/water on south and west edges
- Dense forest clusters along all borders
- Natural, not walls

STYLE:
- Clean, colorful, cartoon/low-poly Roblox aesthetic
- Bird's eye view / top-down perspective
- Clear labels for each area
- Show plot grid layout clearly
- Include a simple legend/key
- Size indicators (small/medium/large areas)
```

---

### Example: Pet Simulator World Map

```
Create a top-down 2D concept map layout for a Roblox pet simulator game. The map should show:

SPAWN HUB (center of map):
- Central plaza with fountain
- Pet equip/unequip station
- Shop building with striped awning
- Egg hatching area (3 egg pedestals)
- Inventory/storage NPC
- Daily spin wheel

THEMED WORLDS (radiating from hub, unlocked progressively):
- World 1 (Starter Meadow): Green grass, basic pets, free access
- World 2 (Beach Paradise): Sandy shores, water pets, 1K coins to unlock
- World 3 (Haunted Forest): Spooky trees, shadow pets, 10K coins
- World 4 (Candy Kingdom): Sweet terrain, rare candy pets, 100K coins
- World 5 (Volcano Island): Lava pools, fire pets, 1M coins
- World 6 (Space Station): Cosmic theme, legendary pets, 10M coins

EACH WORLD CONTAINS:
- Coin spawns (scattered collectibles)
- Treasure chests (random loot)
- World-specific egg for hatching
- Mini-boss area (defeat for bonus rewards)
- Secret area (hidden behind obstacles)

SPECIAL ZONES:
- Trading hub (dedicated trading area between worlds)
- VIP cloud (floating island, gamepass only)
- Enchant temple (upgrade pet stats)
- Rebirth altar (prestige for multipliers)
- Event portal (seasonal limited areas)

CONNECTIONS:
- Portal gates between each world (show unlock cost)
- Rainbow bridge connecting VIP area
- Paths within each world connecting sub-areas
- Teleport pads at world entrances

MAP BORDERS:
- Clouds and sky on all edges (floating island aesthetic)
- Waterfalls dropping into void
- Magical barrier shimmer effect

STYLE:
- Bright, vibrant, cute cartoon style
- Top-down bird's eye view
- Each world clearly color-coded
- Numbered world progression (1→2→3→4→5→6)
- Icons for key locations (egg=oval, shop=building, boss=skull)
- Legend showing unlock costs
```

---

### Example: Obby Tower Map

```
Create a top-down 2D concept map layout for a Roblox tower obby game. The map should show:

GROUND FLOOR (spawn area):
- Main lobby with spawn points
- Stage select portals (skip to unlocked stages)
- Shop (buy skips, speed boosts, checkpoints)
- Leaderboard (fastest times, highest stage reached)
- Tutorial area (basic jump practice)

TOWER STRUCTURE (vertical progression, show as spiral or sectioned):
- Stages 1-10 (Easy): Green platforms, simple jumps
- Stages 11-25 (Medium): Yellow platforms, moving obstacles
- Stages 26-40 (Hard): Orange platforms, disappearing blocks
- Stages 41-55 (Extreme): Red platforms, lava, kill parts
- Stages 56-70 (Nightmare): Purple platforms, invisible sections
- Stages 71-99 (Impossible): Black platforms, everything combined
- Stage 100 (Final): Rainbow boss stage

EACH STAGE SECTION HAS:
- Checkpoint at start
- 3-5 obstacle types
- Secret badge location (hidden)
- Skip pad (costs robux/coins)

SPECIAL FLOORS (between sections):
- Rest areas with mini-games
- Bonus coin collection rooms
- Race challenge rooms (compete with others)
- Parkour puzzle rooms

WINNER AREA (top of tower):
- Victory platform with fireworks
- Trophy display
- Winner-only shop (exclusive trails, effects)
- Hall of fame (player names)
- Teleport back to lobby

CONNECTIONS:
- Ladders/stairs between stages (one-way up)
- Checkpoint teleports (two-way to unlocked)
- Fall zones (reset to last checkpoint)
- Shortcut tubes (VIP only)

MAP BORDERS:
- Sky/clouds surrounding tower
- Birds flying at different heights
- Sun/moon indicating progress (higher = night sky)

STYLE:
- Side-view cross-section of tower (show all floors)
- Color gradient from green (bottom) to rainbow (top)
- Stage numbers clearly labeled
- Difficulty indicators (stars or skulls)
- Height markers (floor 1, floor 25, etc.)
- Show approximate player count at each section
```

---

### Example: Fighting Game Arena Map

```
Create a top-down 2D concept map layout for a Roblox anime fighting game. The map should show:

MAIN LOBBY (central safe zone):
- Spawn area (no PvP)
- Character select pedestals
- Skill tree/upgrade station
- Quest board NPC
- Leaderboard (wins, kills, rank)
- Shop (skins, effects, weapons)

BATTLE ARENAS (surrounding lobby):
- Arena 1 (Training Grounds): 1v1, no rank loss, practice
- Arena 2 (Ranked Colosseum): 1v1 competitive, ELO system
- Arena 3 (Team Stadium): 3v3 team battles
- Arena 4 (Battle Royale Zone): 20 player FFA, shrinking zone
- Arena 5 (Boss Arena): PvE, fight waves of enemies

THEMED FIGHTING ZONES (open world PvP):
- Zone A (Ninja Village): Rooftops, trees, stealth combat
- Zone B (Samurai Castle): Bridges, towers, sword focus
- Zone C (Demon Realm): Lava, darkness, curse effects
- Zone D (Heaven's Gate): Clouds, holy light, aerial combat

SPECIAL AREAS:
- Clan base plots (group territories)
- Tournament stage (scheduled events)
- Spectator stands (watch fights)
- Training dummies (test combos)
- Meditation shrine (passive XP gain)

CONNECTIONS:
- Portals from lobby to each arena
- Open pathways between PvP zones
- Safe corridors (no combat) between areas
- Respawn points in each zone

MAP BORDERS:
- Energy barriers (visible dome)
- Out of bounds = teleport to spawn
- Spectator-only outer ring

STYLE:
- Anime/manga aesthetic
- Top-down with zone labels
- PvP zones marked with crossed swords icon
- Safe zones marked with shield icon
- Rank requirements shown for each arena
- Player capacity per zone
- Color-coded by danger level
```

---

## Workflow: Simple Props vs Complex Models

When generating Roblox model reference sheets, use different approaches based on complexity:

### Complex Models (Individual Reference Sheets)
Use the full 8-view grid (or 3x3 with details) for:
- **Characters/Creatures**: Dragon, Horse, Robot, Zombie, Ghost, Skeleton
- **Buildings**: Houses, Towers, Churches, Castles, Windmills
- **Vehicles**: Cars, Tanks, Mechs, Boats
- **Large Props**: Treasure Chests (with interior), Furniture with details

Why: These need multiple angles to understand proportions, part breakdown, and construction details.

### Simple Props (Pack Reference Sheets)
Generate multiple items in a single image for:
- **Small Props**: Torches, Barrels, Crates, Buckets, Sacks
- **Decor Items**: Candles, Rope coils, Shields, Lanterns
- **Food Items**: Apples, Bread, Cheese, Meat
- **Nature Items**: Rocks, Bushes, Flowers, Logs

**Pack Template:**
```
Create a props reference sheet showing 6-8 simple items in Roblox stud style.

Layout: 2 rows of items, each shown in 3/4 view

Items:
1. [Item 1] - [brief description]
2. [Item 2] - [brief description]
3. [Item 3] - [brief description]
4. [Item 4] - [brief description]
5. [Item 5] - [brief description]
6. [Item 6] - [brief description]

Style requirements:
- Blocky low-poly shapes (rectangular boxes only)
- Classic Roblox stud texture on surfaces
- Vibrant solid colors
- White background
- Each item labeled with name
- Show relative size between items

Theme: [THEME NAME]
Colors: [COLOR PALETTE]
```

**Example Pack Prompt (Medieval Props):**
```
Create a props reference sheet showing 8 medieval items in Roblox stud style.

Layout: 2 rows of 4 items, each shown in 3/4 view

Items:
1. Wall Torch - wooden handle, orange flame
2. Wooden Barrel - brown with dark bands
3. Crate - light wood, nailed shut
4. Grain Sack - tan/beige, tied top
5. Water Bucket - grey metal, wooden handle
6. Candle - white wax, yellow flame, puddle base
7. Rope Coil - tan/brown, coiled on ground
8. Wooden Shield - round, metal boss center

Style requirements:
- Blocky low-poly shapes (rectangular boxes only)
- Classic Roblox stud texture on surfaces
- Vibrant solid colors (browns, greys, warm accents)
- White background
- Each item labeled with name
- Show relative size between items

Theme: Medieval/Fantasy Village
Colors: Reddish brown wood, dark stone grey metal, warm orange flames
```

### Workflow Summary
| Complexity | Reference Type | Items per Image |
|------------|---------------|-----------------|
| Complex (dragon, building) | 8-view grid | 1 model |
| Simple (torch, barrel) | Props pack sheet | 6-8 items |

---

## Checklist Before Prompting

- [ ] Defined art style (low-poly, anime, realistic, pixel)?
- [ ] Specified game type/reference (Roblox, fighting game, RPG)?
- [ ] Included camera angle/view?
- [ ] Described lighting/mood?
- [ ] Added color palette guidance?
- [ ] Mentioned what to avoid (negative guidance)?
- [ ] Requested multiple views if needed?
