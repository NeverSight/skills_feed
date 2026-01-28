---
name: level-design
description: >
  Level design consulting based on "Level Design: Processes and Experiences"
  (CRC Press). Use when helping with spatial game design, environment layout,
  player guidance, pacing, open-world planning, hiding linearity, themed
  environments, procedural vs handmade content, play-personas, or evaluating
  level quality. Covers horror level design, indie game practices, and
  AAA open-world techniques. NOT for coding - focused on design philosophy
  and player spatial experience.
---

# Level Design Skill

A design consulting framework based on "Level Design: Processes and Experiences" edited by Christopher W. Totten (CRC Press, 2017).

## Core Philosophy

Level design is the **thoughtful execution of gameplay into gamespace for players to dwell in**. It sits at the intersection of programming, design, and art—implementing the game design vision while leading players through experiences without revealing the designer's presence.

> "Level designers don't merely create things for players to do. They create situations that invite players to interpret who they are." — Brian Upton

---

## The Designer's Core Tasks

1. **Guide without forcing** — Lead players through intended experiences while maintaining illusion of freedom
2. **Teach through space** — Use environment to communicate mechanics, not tutorials
3. **Control pacing** — Modulate intensity through spatial rhythm and stillness
4. **Support narrative** — Align levels within overall game progression
5. **Create consistency** — Establish and honor environmental rules players can rely on

---

## Quick Reference: Level Types

| Type | Key Considerations |
|------|-------------------|
| **Linear** | Hide linearity through visual choice, narrative lures, environmental storytelling |
| **Open-World** | POI density, anchor locations, subregions, orientation landmarks |
| **Horror** | Anticipatory play, corners, one-way doors, visible-but-blocked escape |
| **Procedural** | Horizontal vs vertical integration of handmade content |
| **Indie/Focused** | Expand single core mechanic through level variation |

---

## Hiding Linearity

Players must feel in control even when following a predetermined path.

### Techniques

| Technique | Description |
|-----------|-------------|
| **Coerced Progression** | Time pressure, pursuing enemies—no time to question the path |
| **Environmental Signage** | In-world signs, color coding (Mirror's Edge red) |
| **NPC Guides** | Companions who lead, escort targets who follow, enemies to chase |
| **Narrative Lures** | Visible objectives, story hooks that pull forward |
| **Forced Choice Illusion** | Block one path as player approaches, making "choice" feel organic |

### What Breaks the Illusion

- Arbitrary locked doors
- Invisible walls
- Flimsy barriers (yellow police tape blocking a superhero)
- Clear artificial constraints without narrative justification

**See**: `references/hiding-linearity.md`

---

## Anticipatory Play & Horror Design

Horror isn't about jump scares—it's about **dread before the corner**.

### The P.T. Framework

- **Corners** — Hide what's ahead; players imagine horrors worse than you could show
- **Ratchet Doors** — One-way progress; can't retreat, must face what's ahead
- **Valve Doors** — Block progress temporarily; visible state reduces uncertainty about *if* blocked
- **Visible Escape** — Show impossible exits to amplify feeling of being trapped

### Key Principle

> "Anticipatory play requires variety—the situation must evolve so players continually reassess. Static horrors become played out."

**See**: `references/anticipatory-play.md`

---

## Open-World Planning (Burgess Method)

Three living documents for large-scale world design:

### 1. The World Map
- Establish setting, scale, subregions
- Plot anchor locations (story-critical, landmarks)
- Include orienting features (visible from anywhere)
- Plan natural boundaries (water, cliffs) over artificial walls

### 2. The Master List (Excel)
- Every location with X/Y coordinates
- Columns for: designer, quest associations, footprint size, difficulty, encounter type
- Scatter graph overlay on map image
- Filter to visualize distribution patterns

### 3. The Directory (Wiki)
- Per-location pages with: status, goals, walkthrough, known issues, to-do
- Category tags for filtering (by designer, by pass, by type)
- Living documentation updated throughout development

### POI Density

The frequency of points of interest defines exploration feel:
- **High density** = Theme park feel (GTA cities)
- **Low density** = Vast, sparse exploration (Just Cause countryside)
- **Non-uniform** = Urban cores dense, rural areas sparse (Fallout 4)

**See**: `references/open-world-planning.md`

---

## Play-Personas

Model player behavior before and after implementation.

### The Process

1. **Analyze mechanics** → Derive high-level behaviors from low-level actions
2. **Create matrix** → Plot all behavioral combinations (2^n personas)
3. **Select cast** → Choose 2-3 personas aligned with design vision
4. **Associate affordances** → Link behaviors to spatial/ludic elements
5. **Orchestrate** — Modulate which personas are viable throughout level
6. **Validate** — Use telemetry to confirm players match expected personas

### Example: Pac-Man

High-level behaviors: Center vs periphery dwelling, early vs late pill eating, linear vs broken paths

→ 8 persona combinations including "Fraidy Cat" (periphery, early pills, linear) and "Risk Taker" (center, late pills, broken)

**See**: `references/play-personas.md`

---

## Themed Level Tropes

Classic environmental themes with established mechanics and expectations:

| Trope | Core Elements | Design Advantages |
|-------|---------------|-------------------|
| **Fire/Ice** | Environmental hazards, timing puzzles | Color variety, physics tweaks |
| **Dungeon/Cavern** | Tileable textures, traps, treasure | Easily repeatable, expected danger |
| **Factory** | Moving platforms, conveyers, gears | Repurposable mechanics, scalable difficulty |
| **Jungle** | Vines, branches, water, wildlife | Fluid movement, colorful outdoor |
| **Spooky** | Atmosphere, surprise, undead | Combines with any theme |
| **Pirate** | Ships, treasure, melee, water | Action-ready, clear rewards |
| **Urban** | Verticality, cover, vehicles | Real-world familiarity |
| **Space Station** | Tech hazards, airlocks, zero-G | Sci-fi dungeon equivalent |
| **Sewer** | Pipes, rats, rising water | Modern dungeon stand-in |

**Mexican Pizza Technique**: Combine two tropes for fresh results (fire + graveyard, jungle + urban ruins)

**See**: `references/themed-environments.md`

---

## Indie Level Design Practices

When working with limited resources:

| Practice | Description |
|----------|-------------|
| **Expand Core Mechanic** | One strong mechanic explored through level variation (VVVVVV) |
| **Iterative Level Design** | Rapid prototyping, playtest early and often |
| **Design Modes Not Levels** | Create systems that generate challenge (endless runners) |
| **Embrace Emergence** | Simple rules, complex interactions |
| **Object-Oriented Design** | Modular elements that combine predictably |

### Qualities of Good Level Design

- Maintain flow: challenge without anxiety or boredom
- Balance freedom with constraints (illusion of control)
- Enable mastery and emergent solutions
- Balance risk and reward proportionally
- Guide without being obvious

**See**: `references/indie-practices.md`

---

## Procedural vs Handmade Integration

Two integration models:

### Vertical Integration
Handmade thread runs through procedural content (FTL quest chains, Spelunky secrets)

**Best for**: Narrative, puzzle sequences, coherent story beats

### Horizontal Integration
Procedural and handmade content interchangeable in same slot (Dungeon Crawl vaults, URR buildings)

**Best for**: Ensuring specific gameplay moments, quality floors

### Key Decision
**Should players see which is which?**
- **Yes** (DCSS): Visual variety, risk/reward clarity
- **No** (URR): Quality perception, seamless experience

**See**: `references/procedural-handmade.md`

---

## Level Evaluation Framework

When evaluating a level design:

1. **Player Guidance**: Can players find their way without obvious signposting?
2. **Pacing**: Does intensity modulate appropriately? Are there moments of stillness?
3. **Teaching**: Does the space teach mechanics before testing them?
4. **Consistency**: Do environmental rules remain predictable?
5. **Persona Fit**: Does the level support intended play styles?
6. **Density**: Is POI distribution appropriate for the experience?
7. **Linearity Illusion**: Do players feel in control of their path?

---

## Common Pitfalls

| Pitfall | Symptom | Solution |
|---------|---------|----------|
| Obvious Rails | Player comments on being "on rails" | Add visual choice, narrative justification |
| Empty Space | Players comment on emptiness | Increase POI density or justify sparseness |
| Lost Players | Players wander aimlessly | Add orientation landmarks, environmental cues |
| Played-Out Scares | Horror stops being scary | Keep threats evolving, limit exposure time |
| Arbitrary Barriers | Players frustrated by blocked paths | Use narrative-justified or natural boundaries |
| Tutorial Overload | Players skip to "real game" | Teach through safe early gameplay |

---

## Key Mantras

- **"Hide the designer's hand."** Players should feel they're discovering, not being led.
- **"Corners are always significant."** Transitions between visible and hidden create anticipation.
- **"POI density defines feel."** Sparse = vast exploration; dense = action-packed.
- **"Static threats become furniture."** Evolve dangers or limit exposure.
- **"The illusion of choice is enough."** Players interpret forced choices as agency.
- **"Mexican pizza your themes."** Combine familiar tropes for fresh experiences.
