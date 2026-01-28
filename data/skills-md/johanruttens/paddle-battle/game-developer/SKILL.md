---
name: game-developer
description: Expert game development and design skill for building complete, polished games. Use when creating games, game prototypes, or interactive entertainment experiences across platforms (React Native, web, Unity concepts, Godot). Covers game mechanics, physics, AI opponents, level design, progression systems, visual effects, sound integration, and player experience. Triggers on requests to build games, create game mechanics, design levels, implement game AI, add game audio, or develop interactive entertainment.
---

# Game Developer & Designer Skill

Build complete, polished games with professional-grade mechanics, visuals, and player experience.

## Core Workflow

1. **Analyze** — Understand game type, platform, core loop, target audience
2. **Design** — Define mechanics, progression, visual style, audio needs
3. **Architect** — Plan component structure, state management, game loop
4. **Implement** — Build iteratively: core → polish → juice
5. **Playtest** — Test feel, balance, edge cases

## Game Design Fundamentals

### The Core Loop
Every game needs a satisfying core loop. Define it explicitly:
```
Action → Challenge → Reward → Progression → (repeat)
```

Example (Pong-style): Hit ball → Keep rally → Score point → Level up → Harder AI

### Player Experience Pillars
- **Agency**: Player actions feel meaningful and responsive
- **Challenge**: Difficulty matches skill, with room to grow  
- **Reward**: Clear feedback for success (visual, audio, progression)
- **Flow**: Minimize friction between player intent and game response

## Platform-Specific Guidance

**React Native Games**: See [references/react-native-games.md](references/react-native-games.md)
**Web/HTML5 Games**: See [references/web-games.md](references/web-games.md)
**Game Math & Physics**: See [references/game-physics.md](references/game-physics.md)

## Implementation Patterns

### Game Loop Architecture
```javascript
// Core game loop pattern
const useGameLoop = (updateFn, isRunning) => {
  const frameRef = useRef();
  const lastTimeRef = useRef(0);
  
  useEffect(() => {
    if (!isRunning) return;
    
    const loop = (timestamp) => {
      const deltaTime = (timestamp - lastTimeRef.current) / 1000;
      lastTimeRef.current = timestamp;
      updateFn(deltaTime);
      frameRef.current = requestAnimationFrame(loop);
    };
    
    frameRef.current = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(frameRef.current);
  }, [isRunning, updateFn]);
};
```

### State Management
Separate concerns clearly:
- **Game State**: Positions, scores, level, entities
- **UI State**: Menus, modals, settings
- **Input State**: Current touches, gestures, keys
- **Audio State**: What's playing, volume levels

### Collision Detection
Start simple, optimize only if needed:
```javascript
// AABB collision (rectangles)
const checkCollision = (a, b) => (
  a.x < b.x + b.width &&
  a.x + a.width > b.x &&
  a.y < b.y + b.height &&
  a.y + a.height > b.y
);

// Circle collision
const circleCollision = (a, b) => {
  const dx = a.x - b.x;
  const dy = a.y - b.y;
  const distance = Math.sqrt(dx * dx + dy * dy);
  return distance < a.radius + b.radius;
};
```

## Game Feel ("Juice")

Good games feel responsive and alive. Add juice through:

### Visual Feedback
- **Screen shake** on impacts (subtle: 2-5px, dramatic: 10-15px)
- **Particle effects** for collisions, explosions, trails
- **Squash/stretch** on bounces and impacts
- **Flash effects** on damage or scoring
- **Trails** behind fast-moving objects

### Audio Feedback
- Vary pitch slightly on repeated sounds (±10%)
- Layer sounds for impact (hit + whoosh + bass)
- Use rising tones for positive events, falling for negative
- Add subtle ambient soundscape

### Timing & Easing
- Use easing functions, never linear motion
- Add anticipation before actions (wind-up)
- Add follow-through after actions (settle)
- Hit-stop/freeze frames on important impacts (16-50ms)

## AI Opponent Design

### Difficulty Scaling
```javascript
const AI_CONFIGS = {
  easy: {
    reactionDelay: 200,    // ms before responding
    predictionError: 0.3,  // randomness in targeting
    speedMultiplier: 0.7,  // movement speed
    mistakeChance: 0.15    // chance to miss intentionally
  },
  medium: {
    reactionDelay: 100,
    predictionError: 0.15,
    speedMultiplier: 0.9,
    mistakeChance: 0.05
  },
  hard: {
    reactionDelay: 50,
    predictionError: 0.05,
    speedMultiplier: 1.0,
    mistakeChance: 0.01
  }
};
```

### AI Behavior Patterns
- **Reactive**: Respond to current ball position
- **Predictive**: Calculate where ball will arrive
- **Adaptive**: Adjust strategy based on player patterns
- **Personality**: Add quirks (aggressive, defensive, erratic)

## Level Design & Progression

### Difficulty Curve
```
Levels 1-10:   Tutorial zone — Teach mechanics gently
Levels 11-25:  Learning zone — Introduce variations
Levels 26-50:  Challenge zone — Test mastery
Levels 51-75:  Expert zone — Combine mechanics
Levels 76-100: Mastery zone — Peak difficulty
```

### Progression Systems
- **Unlocks**: New content as reward for progress
- **Upgrades**: Permanent improvements
- **Achievements**: Recognition for skill/exploration
- **Leaderboards**: Social competition

### Level Variation Techniques
- Modify parameters (speed, size, count)
- Add/remove elements
- Change layouts
- Introduce new mechanics
- Combine existing mechanics

## Visual Style Guidelines

### Retro/Arcade (80s)
- Neon colors: `#ff00ff`, `#00ffff`, `#39ff14`, `#ff6b35`
- Scanline/CRT effects
- Pixel fonts or bold geometric sans-serif
- Grid backgrounds, glow effects
- High contrast, dark backgrounds

### Modern Minimal
- Limited color palette (2-3 colors)
- Clean geometric shapes
- Generous whitespace
- Subtle shadows and depth
- Smooth animations

### Pixel Art
- Consistent pixel scale (don't mix sizes)
- Limited palette per sprite
- Clear silhouettes
- Animation principles still apply

## Sound Design Checklist

Essential sounds for most games:
- [ ] Menu navigation (select, confirm, back)
- [ ] Core action sounds (hit, collect, shoot)
- [ ] Feedback sounds (success, failure, damage)
- [ ] Ambient/background music
- [ ] Transition sounds (level start, game over)

Implementation tips:
- Preload all sounds before gameplay
- Use audio sprites for web
- Implement volume controls (music/SFX separate)
- Support mute toggle
- Vary sounds slightly to avoid repetition fatigue

## Performance Optimization

### Critical for Games
- Target 60 FPS consistently
- Minimize garbage collection (object pooling)
- Use `useMemo`/`useCallback` for expensive calculations
- Batch state updates
- Profile before optimizing

### React Native Specific
- Use `react-native-reanimated` for animations
- Avoid JS thread blocking during gameplay
- Use native driver for animations when possible
- Consider `react-native-game-engine` for complex games

## Project Structure Template

```
game-name/
├── src/
│   ├── components/
│   │   ├── game/          # Game entities (Player, Ball, Enemy)
│   │   ├── ui/            # UI components (Button, Modal, Score)
│   │   └── effects/       # Visual effects (Particles, Glow)
│   ├── screens/           # Full screens (Menu, Game, Settings)
│   ├── hooks/             # Custom hooks (useGameLoop, useSound)
│   ├── context/           # State management
│   ├── utils/             # Helpers (physics, math, collision)
│   ├── config/            # Constants, level data, settings
│   ├── assets/
│   │   ├── sounds/
│   │   ├── images/
│   │   └── fonts/
│   └── types/             # TypeScript definitions
├── App.tsx
└── package.json
```

## Quality Checklist

Before considering a game complete:

### Gameplay
- [ ] Core loop is satisfying
- [ ] Controls feel responsive (<100ms latency)
- [ ] Difficulty curve is smooth
- [ ] Edge cases handled (pause, background, resume)

### Polish
- [ ] Visual feedback for all actions
- [ ] Sound effects for key events
- [ ] Smooth transitions between states
- [ ] Loading states where needed

### UX
- [ ] Clear how to play (tutorial or intuitive)
- [ ] Progress is saved
- [ ] Settings are accessible
- [ ] Pause functionality works

### Technical
- [ ] Consistent 60 FPS
- [ ] No memory leaks
- [ ] Handles interruptions gracefully
- [ ] Works on target devices/browsers