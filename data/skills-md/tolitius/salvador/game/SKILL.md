---
name: game
description: Autonomous browser game agent. Analyzes game concept, implements with KAPLAY.js (2D) or Three.js (3D), playtests in headless browser, critiques gameplay/mechanics, fixes, and launches the result.
---

# Game Agent
Use this skill to create browser-based games using KAPLAY.js (2D) or Three.js (3D) with a focus on **playable mechanics, clear feedback, and polished feel**.

## Workflow
Follow this **strict loop** when asked to create a game:

### Phase 1: Bootstrap
1. **Check Context**: If `package.json` is missing, run `bash .claude/skills/game/scripts/setup.sh`.
2. **Scaffold**: Ensure `index.html` and `src/game.js` exist (or inline in index.html).
3. **Read API Reference**:
   - For 2D games: Read `references/kaplay-ref.md` for KAPLAY API.
   - For 3D games: Read `references/threejs-ref.md` for Three.js API.
   - For FPS games: Read `references/fps-patterns.md` for pointer lock, hit detection, enemy AI.
4. **Read Game Patterns**: Read `references/game-patterns.md` for architecture patterns.
5. **Read Game Systems**: Read `references/game-systems.md` for difficulty scaling, scoring, persistence, and UI patterns.
6. **Read Visual Assets**: Read `references/visual-assets.md` for procedural sprites, palettes, and visual effects.

### Phase 1.5: Game Design Analysis (Before Coding!)

This game needs to be **playable and fun** from the first iteration.
Therefore, define the core loop before writing any code.

Before writing any code, decompose the game:

1. **Identify the Core Mechanic**: What is the ONE thing the player does repeatedly?
   - Strip away everything else first
   - This mechanic must be satisfying on its own
   - Examples: jump, shoot, match, dodge, collect, solve

2. **Define the Challenge**: What makes it difficult?
   - Timing? Precision? Resource management? Puzzle solving?
   - How does difficulty progress?
   - What's the failure state?

3. **Establish the Feedback Loop**:
   - **Input**: What does the player press/click/drag?
   - **Response**: What happens immediately? (must feel < 100ms)
   - **Outcome**: Success or failure indication
   - **Reward/Penalty**: Score change, sound, visual effect

4. **Scope to Minimum Viable Game (MVG)**:
   - ONE level or endless mode
   - ONE enemy type or obstacle  
   - ONE player ability
   - Win AND lose conditions
   - Can be expanded later, but MVG must work first

5. **Research the Domain** (for educational/simulation games):
   - Look up actual facts (angles, counts, formulas, rules)
   - Don't guess scientific/mathematical details
   - See `references/physics-constants.md` for common values

### Phase 1.6: Game Feel Principles

6. **Juice**: The game must feel alive and responsive.
   - **Input Response**: Every input produces immediate visual/audio feedback
   - **Screen Shake**: On impacts, collisions, explosions - use `shake(intensity)`
   - **Flash**: Brief color flash on damage or success - use `flash(color, duration)`
   - **Particles**: On deaths, pickups, actions (spawn small objects with `lifespan`)
   - **Squash & Stretch**: Scale objects on jumps, bounces, movements

7. **Clarity**: The player must always understand:
   - Where they are (player position obvious, distinct color/shape)
   - What they can do (affordances clear)
   - What hurts them (dangers visually distinct - red, spiky, animated)
   - What helps them (pickups/goals highlighted - gold, glowing, animated)
   - Current state (score, lives, progress visible in HUD)

8. **Pacing**: Control the rhythm
   - Moments of tension followed by release
   - Difficulty curves, not walls
   - Rest points between challenges
   - Even endless games need rhythm variation (spawn rate waves)

9. **Polish Details**:
   - Title/start screen with game name and controls
   - Pause functionality (P key or Escape)
   - Restart on game over (R key)
   - Score or progress display (top-left, `fixed()` for HUD)
   - Control hints visible ("Arrow keys: Move | Space: Jump")

### Phase 1.7: Physics & Reachability Validation

**CRITICAL**: Validate that game physics allow the player to accomplish required actions.

16. **Test Core Movement**: Before finalizing level/game design:
    - Can the player reach all required locations?
    - Can the player avoid all avoidable hazards?
    - Does movement feel responsive (not sluggish or twitchy)?
    - Are speeds balanced (player vs enemies vs projectiles)?

17. **Validate With Math**: For physics-based games, calculate limits:
    - Movement range per second = speed × time
    - Jump/launch height = (force)² / (2 × gravity)
    - Projectile range = speed × lifetime
    - **If design requires X, verify physics allow X**

18. **Common Physics Pitfalls**:
    - Targets placed beyond movement range
    - Gaps larger than jump/dash distance
    - Enemies faster than player can react
    - Timers shorter than required actions
    - **Always prototype movement before building levels**

### Phase 1.8: Visual Polish (Before Coding!)

**CRITICAL**: Games must look polished from the first iteration. No "sticks and boxes."

**Quality Bar**: Ask yourself - "Would someone pay $5 for this?" If not, it's not ready.

10. **Choose a Color Palette**: Select from `visual-assets.md` palettes:
    - `PASTEL` - friendly, casual games
    - `PICO8` - retro pixel art feel
    - `ENDESGA` - modern indie aesthetic
    - `NEON` - cyberpunk, arcade style

11. **Generate PREMIUM Procedural Sprites**: Every sprite needs MULTIPLE layers of polish:
    - **Player/Hero**: outer glow + multi-stop gradient + shadow + character details (eyes, expression) + highlights
    - **Collectibles**: glow aura + metallic/shiny gradient + inner detail + shine streak + sparkle accents
    - **Enemies/Hazards**: danger glow + gradient body + expressive features + shadow + distinguishing details
    - **Environment** (platforms, walls, tiles): surface texture + body gradient + edge highlights + shadow + structural details
    - **Projectiles/Effects**: core glow + color gradient + trail suggestion + bright center
    - **NEVER use bare `rect()`, `circle()`, `polygon()` for visible game objects**
    - **"Has a gradient" is NOT enough** - premium sprites have 5+ visual layers
    - See `visual-assets.md` for the universal sprite layer checklist

12. **Create Gradient Background**: Flat backgrounds look cheap.
    - Use `makeGradientBg()` with palette colors
    - Add subtle stars/dots for depth
    - Consider parallax layers for side-scrollers

13. **Add Idle Animations**: Static objects feel dead.
    - Coins: `addFloat()` - gentle bobbing
    - Player: `addBreathing()` - subtle scale pulse
    - Enemies: combine breathing + slight movement
    - Pickups: `addSpin()` or glow pulse

14. **Plan Particle Effects**: Every interaction needs MULTIPLE feedback layers:
    - **Positive events** (collect, score, win): particle burst + floating text (+1, +100) + screen flash + UI reaction + small shake
    - **Negative events** (damage, death, lose): explosion particles + screen shake + color flash + UI feedback
    - **Movement events** (jump, dash, land, turn): directional particles + object deformation (squash/stretch/spin)
    - **Ambient atmosphere**: floating particles + twinkling/pulsing background elements
    - **Projectiles/Actions**: spawn flash + trail particles + impact burst
    - **One effect is NOT enough** - premium feedback stacks 3+ effects per action

15. **Establish Z-Index Hierarchy**: Proper layering adds depth.
    - Background: z(-100)
    - Platforms: z(0)
    - Pickups: z(10)
    - Enemies: z(20)
    - Player: z(30)
    - Particles: z(50)
    - HUD: z(100) + fixed()

### Phase 2: Autonomous Loop (The "Work")
Repeat this cycle until the game is **Playable and Polished**:

1. **Implement/Refine**: Write game code.
   * *Constraint*: Use KAPLAY.js for 2D (default), Three.js only if 3D is explicitly needed.
   * *Constraint*: Single HTML file with CDN imports (no build step for player).
   * *Constraint*: **Color Palette**: Use a predefined palette from `visual-assets.md` (PASTEL, PICO8, ENDESGA, NEON).
   * *Constraint*: **No Bare Primitives**: NEVER use `rect()`, `circle()`, `polygon()` for game objects. Use procedural sprites from `visual-assets.md`.
   * *Constraint*: **Gradient Background**: Always use `makeGradientBg()` instead of flat `background` color.
   * *Constraint*: **Idle Animations**: All game objects must have subtle animations (float, breathe, pulse, spin).
   * *Constraint*: **Particle Effects**: Every collision/pickup must spawn particles using `burstParticles()` or `deathExplosion()`.
   * *Constraint*: **Z-Index Layering**: Use proper z-index hierarchy (BG:-100, platforms:0, pickups:10, enemies:20, player:30, particles:50, HUD:100).
   * *Constraint*: **Game Loop**: Use KAPLAY's `onUpdate()` for continuous logic. Never use `noLoop()`.
   * *Constraint*: **Input Handling**: Use KAPLAY's `onKeyPress`, `onKeyDown`, `isKeyDown`.
   * *Constraint*: **Collision**: Use `area()` component and `onCollide()` for interactions.
   * *Constraint*: **Canvas sizing**: 800x600 or 16:9 aspect ratio.
   * *Constraint*: **State Management**: Use KAPLAY scenes for menu/play/gameover states.
   * *Constraint*: **HUD**: Use `fixed()` and `z(100)` for UI that ignores camera.
   * *Constraint*: **Controls Display**: Show control hints on screen at all times.
   * *Constraint*: **Keyboard Handling**: Use `onKeyPress("space", ...)` not raw DOM events for game input.

2. **Playtest**: Run `node playtest.js`
   - Captures screenshots at t=0, t=2s, t=5s
   - Simulates basic inputs (arrow keys, space, click)
   - Checks console for errors
   - Extracts game state variables if exposed

3. **Critique**:
   * **Logs**: Are there JavaScript errors?
   * **Visual Audit**: Open *all* generated screenshots (`playtest-screenshots/`) and evaluate:
     * **Does it run?**: Is there movement/change between frames?
     * **Input Response**: Did simulated input cause visible change?
     * **Readability**: Is text/HUD legible? Good contrast?
     * **Composition**: Is game area centered? Nothing cut off?
     * **State Changes**: Can you see game progressing (score changing, objects moving)?
   * **Visual Quality Audit** (CRITICAL - no sticks and boxes!):
     * **No bare primitives?**: Are all objects using procedural sprites with gradients/details?
     * **Gradient background?**: Is the background a gradient (not flat color)?
     * **Objects alive?**: Do coins bob, player breathe, objects animate?
     * **Particles present?**: Are there particle effects on interactions?
     * **Color harmony?**: Is a consistent palette used throughout?
     * **Visual depth?**: Are z-indexes creating proper layering?
     * **Glow/highlights?**: Do important objects (coins, player) have visual emphasis?
   * **Gameplay Audit** (mental simulation):
     * Is the core mechanic present and functional?
     * Is there a clear goal?
     * Is there a failure state?
     * Would a player understand what to do without external instructions?

4. **Decide**:
   * *Errors?* → Fix code → **Repeat**.
   * *Static/Frozen?* → Fix game loop, ensure `onUpdate` runs → **Repeat**.
   * *No Input Response?* → Fix input handlers, check key names → **Repeat**.
   * *Missing Feedback?* → Add juice (shake, flash, particles) → **Repeat**.
   * *Unclear Goal?* → Add visual indicators, HUD elements → **Repeat**.
   * *No Win/Lose?* → Implement end conditions → **Repeat**.
   * *Unreadable Text?* → Increase font size, add contrast → **Repeat**.
   * *Bare rectangles/circles?* → Replace with procedural sprites → **Repeat**.
   * *Flat background?* → Add gradient background → **Repeat**.
   * *Static objects?* → Add idle animations (float, breathe) → **Repeat**.
   * *No particles?* → Add burst/explosion effects → **Repeat**.
   * *Playable, Clear, Responsive & Visually Polished?* → **Proceed to Phase 3**.

### Phase 3: Presentation (The "Launch")
Once the loop is complete and the game is polished:
1. **Launch**: Run `npx vite --open`.
2. **Notify**: Tell the user:
   - "Game is ready!"
   - "Controls: [List all controls]"
   - "Goal: [One sentence on how to win/play]"

---

## Technology Selection

| Request Type | Framework | Template |
|-------------|-----------|----------|
| 2D game (default) | KAPLAY.js | `templates/kaplay-2d.html` |
| 3D game (explicit) | Three.js | `templates/threejs-3d.html` |
| FPS / first-person shooter | Three.js | `templates/threejs-fps.html` |
| Ultra-simple (quiz, flashcard) | Vanilla Canvas | `templates/canvas-minimal.html` |

**Decision rule**:
- Use KAPLAY for most 2D games (platformer, top-down, puzzle, etc.)
- Use `threejs-fps.html` for first-person shooters, DOOM-likes, or any game requiring pointer lock + mouse look
- Use `threejs-3d.html` for third-person 3D games, 3D puzzles, or non-shooter 3D experiences
- FPS indicators: "first-person", "FPS", "shooter", "DOOM", "Wolfenstein", "gun", "pointer lock"

---

## File References
- **KAPLAY API**: See `references/kaplay-ref.md` for component list and patterns
- **Visual Assets**: See `references/visual-assets.md` for procedural sprites, color palettes, animations, and particle effects
- **Three.js API**: See `references/threejs-ref.md` for 3D setup
- **FPS Patterns**: See `references/fps-patterns.md` for pointer lock, hit detection, enemy AI, weapon rendering
- **Game Systems**: See `references/game-systems.md` for difficulty scaling, scoring, persistence, UI patterns
- **Game Patterns**: See `references/game-patterns.md` for architecture (state machines, ECS, proc-gen)
- **Physics Constants**: See `references/physics-constants.md` for educational accuracy

---

## Common Pitfalls (Avoid These)

### Gameplay Pitfalls
1. **No game loop**: Forgetting `onUpdate()` results in static screen
2. **Wrong key names**: Use `"space"` not `"Space"`, `"left"` not `"ArrowLeft"` in KAPLAY
3. **Missing `area()`**: Objects won't collide without the `area()` component
4. **Missing `body()`**: Objects won't fall or respond to physics without `body()`
5. **HUD moves with camera**: Use `fixed()` component for UI elements
6. **No scenes**: Putting everything in global scope - use `scene()` for states
7. **Forgetting `go()`**: Must call `go("sceneName")` to start the first scene
8. **Text too small**: Default text size is often too small - use 20+ for HUD
9. **No restart**: Player stuck at game over - always add R to restart
10. **Missing `opacity()` for `lifespan()`**: The `lifespan` component requires `opacity()` to be present on the object
11. **Unreachable goals**: ALWAYS verify physics allow completing required actions. If player must reach X, calculate whether movement/jump/projectile range allows it.
12. **Variable name `rgb` conflicts with KAPLAY**: Never use `const rgb = ...` as it shadows KAPLAY's `rgb()` function. Use `const c = hexToRgb(...)` instead.

### Visual Pitfalls (CRITICAL)
13. **Bare primitives**: Using `rect()`, `circle()`, `polygon()` for game objects looks terrible - use procedural sprites
14. **Flat backgrounds**: `background: [r,g,b]` looks cheap - use `makeGradientBg()` with texture/particles
15. **Static objects**: Game objects sitting motionless feel dead - add idle animations (`addFloat()`, `addBreathing()`, `addSpin()`)
16. **No particles**: Interactions without visual feedback are unsatisfying - add particle bursts on all events
17. **Random colors**: Picking colors without a palette creates visual chaos - use PASTEL, PICO8, ENDESGA, or NEON
18. **No z-index**: Everything at same layer looks flat - use proper z-index hierarchy (-100 to 100)
19. **No glow/outline**: Important objects don't stand out - add glow/aura to key game objects
20. **Bean for everything**: `loadBean()` is a placeholder, not a finished sprite - create proper procedural sprites
21. **"Good enough" sprites**: A sprite with ONE gradient is functional, not premium. Premium = 5+ layers (glow + gradient + highlight + shadow + detail)
22. **Single-effect feedback**: One particle burst is weak. Premium = stacked effects (particles + text + flash + shake + UI reaction)
23. **No movement deformation**: Objects moving without squash/stretch/rotation feel stiff - add deformation on velocity changes
24. **No impact particles**: Collisions and surface contacts without particles lack weight - add particles on all physical interactions
25. **No floating text**: Score changes without visible "+N" text miss dopamine feedback - show value changes visually

### FPS-Specific Pitfalls
26. **Pointer lock not recovering**: After alt-tab or focus loss, pointer lock is lost. ALWAYS re-request on focus/click events.
27. **Enemies shoot through walls**: Must check line of sight (step along ray) before allowing enemy attacks.
28. **Enemies spawn in walls**: Validate spawn positions against collision map; use fallback positions if invalid.
29. **3D hit detection for 2D gameplay**: Classic FPS uses 2D XZ-plane distance with cone-of-fire, ignoring Y axis.
30. **Weapon drawn sideways**: FPS weapons should point forward (barrel vertical), not left-to-right like a side view.
31. **No weapon feedback**: Always add recoil animation (move down/up) and muzzle flash on fire.
32. **Static enemy sprites**: Animate walk (leg movement) and shoot (arms raised) states with canvas texture updates.
33. **AI too aggressive**: Balance detection range, attack rate, and damage. First-time playability > difficulty.
34. **Score counts down during play**: Live score should ONLY increase. Time bonuses calculated at end, only if mission succeeded.
35. **Time bonus on failure**: Speed bonus should only be awarded when the player wins, not on death.
36. **Floating point stat display**: Always use `Math.floor()` for health, armor, score display to avoid "99.7" health.
37. **Modal UI not interactive**: Game over screen must have proper `pointer-events: auto` and exit pointer lock.

---

## Known Warnings (Safe to Ignore)

- **Puppeteer ARM64 warning**: On Apple Silicon Macs, you may see a "Degraded performance warning" about Chrome/Rosetta. This is expected and does not affect playtest functionality.
