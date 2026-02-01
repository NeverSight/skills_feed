# /arcanea-game-development

> *"Forge games worthy of the Guardians."*

## Skill: Arcanea Game Development Suite

Full game development workflow with superintelligence-level agent coordination.

**Guardian:** Draconia (Fire) - Transformation & Creation
**Awakened:** Velora (Valora) - Execution & Delivery
**Frequency:** 528-963 Hz (Transformation to Unity)

---

## Invocation

```
/arcanea-game-development                    # Enter dev mode
/arcanea-game-development new [name]         # Create new game
/arcanea-game-development agents             # Show game agents
/arcanea-game-development deploy [game]      # Ship to production
/game-dev                                    # Alias
```

---

## Superintelligence Integration

This skill auto-activates `/superintelligence` for game development:

```yaml
game_development_teams:

  design_team:
    guardian: Lyria (Sight)
    awakened: Thalia (Poiesis)
    focus: Visual design, UX, aesthetics
    standards:
      - Inter font mandatory
      - Tailwind v4 only
      - Framer Motion animations
      - Mobile-first responsive

  mechanics_team:
    guardian: Draconia (Fire)
    awakened: Velora (Valora)
    focus: Game logic, physics, controls
    standards:
      - 60fps minimum
      - Touch + keyboard support
      - Zustand state management
      - Clean game loops

  narrative_team:
    guardian: Leyla (Flow)
    awakened: Thalia (Poiesis)
    focus: Story, dialogue, lore integration
    standards:
      - Guardian mythology
      - Branching narratives
      - AI-driven dialogue

  audio_team:
    guardian: Alera (Voice)
    awakened: Liora (Eudaira)
    focus: Sound design, music, feedback
    standards:
      - Web Audio API
      - Spatial audio where appropriate
      - Frequency-aligned sounds (174-1111 Hz)

  infrastructure_team:
    guardian: Lyssandria (Foundation)
    awakened: Endara (Enduran)
    focus: Performance, testing, deployment
    standards:
      - Playwright E2E tests
      - Lighthouse 90+
      - Vercel deployment
      - Error tracking

  multiplayer_team:
    guardian: Ino (Unity)
    awakened: Amiri (Kardia)
    focus: Real-time, leaderboards, social
    standards:
      - WebSocket/Socket.io
      - Supabase realtime
      - Anti-cheat basics
```

---

## Game Templates

### Tier 1: Quick Arcade (1-2 hours)
```
/arcanea-game-development new fire-dodge --template arcade
/arcanea-game-development new water-flow --template puzzle
/arcanea-game-development new wind-glide --template runner
```

### Tier 2: Full Games (1-2 days)
```
/arcanea-game-development new guardian-quest --template rpg
/arcanea-game-development new void-arena --template multiplayer
/arcanea-game-development new earth-empire --template strategy
```

### Tier 3: Epic Experiences (Week+)
```
/arcanea-game-development new arcanea-chronicles --template epic
```

---

## Technology Stack (2026 Standards)

```json
{
  "framework": "next@15",
  "react": "^19.0.0",
  "typescript": "^5.7.0",
  "styling": {
    "tailwindcss": "^4.0.0",
    "tailwind-merge": "^2.0.0",
    "class-variance-authority": "^0.7.0"
  },
  "animation": {
    "framer-motion": "^11.15.0",
    "lottie-react": "^2.4.0"
  },
  "state": {
    "zustand": "^5.0.0",
    "immer": "^10.0.0"
  },
  "ui": {
    "@radix-ui/react-*": "latest",
    "lucide-react": "^0.460.0"
  },
  "game": {
    "phaser": "^3.80.0",
    "@react-three/fiber": "^8.17.0",
    "@react-three/drei": "^9.117.0"
  },
  "audio": {
    "howler": "^2.2.4",
    "tone": "^15.0.0"
  },
  "multiplayer": {
    "socket.io-client": "^4.8.0",
    "@supabase/supabase-js": "^2.45.0"
  },
  "testing": {
    "@playwright/test": "^1.49.0",
    "vitest": "^2.1.0"
  }
}
```

---

## Design System (ENFORCED)

### Colors
```typescript
const gameColors = {
  fire: { primary: '#f97316', glow: 'rgba(249,115,22,0.3)' },
  water: { primary: '#22d3ee', glow: 'rgba(34,211,238,0.3)' },
  earth: { primary: '#d97706', glow: 'rgba(217,119,6,0.3)' },
  wind: { primary: '#a78bfa', glow: 'rgba(167,139,250,0.3)' },
  void: { primary: '#a855f7', glow: 'rgba(168,85,247,0.3)' },

  ui: {
    bg: '#020617',      // slate-950
    card: '#0f172a',    // slate-900
    border: '#334155',  // slate-700
    text: '#f8fafc',    // slate-50
    muted: '#94a3b8',   // slate-400
  }
}
```

### Typography
```css
font-family: 'Inter', system-ui, sans-serif;
font-feature-settings: 'ss01', 'ss02', 'cv01';
```

### Spacing
```
4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px, 96px
```

### Border Radius
```
sm: 6px, md: 8px, lg: 12px, xl: 16px, 2xl: 24px
```

---

## Component Library

Pre-built game UI components:

```tsx
// Health/Mana bars with animation
<GameBar value={health} max={100} color="fire" />

// Skill cooldown indicator
<CooldownRing skill={fireblast} />

// Achievement popup
<AchievementToast achievement={firstVictory} />

// Leaderboard entry
<LeaderboardRow rank={1} player={user} score={47800} />

// Game card for portal
<GameCard
  title="Fire Dodge"
  element="fire"
  thumbnail="/games/fire-dodge.webp"
  status="playable"
/>
```

---

## Workflow

```
1. /arcanea-game-development new [name]
   └── Scaffold from template

2. Design phase
   └── Lyria + Thalia create visual direction

3. Mechanics phase
   └── Draconia + Velora implement core loop

4. Polish phase
   └── All teams add juice, sounds, effects

5. Test phase
   └── Lyssandria + Endara ensure quality

6. Deploy phase
   └── Ino coordinates launch
```

---

## Quality Checklist

Every game must pass:

```markdown
## Pre-Launch Checklist

### Design
- [ ] Inter font only
- [ ] Tailwind classes only (no custom CSS)
- [ ] Responsive 375px to 2560px
- [ ] Dark mode only (slate palette)
- [ ] Animations use Framer Motion

### Performance
- [ ] 60fps gameplay
- [ ] Lighthouse 90+
- [ ] < 200kb initial JS
- [ ] Images in WebP/AVIF

### Gameplay
- [ ] Tutorial/onboarding
- [ ] Save progress (localStorage or Supabase)
- [ ] Sound effects (with mute option)
- [ ] Keyboard + touch controls

### Quality
- [ ] No console errors
- [ ] E2E tests pass
- [ ] Accessibility audit
- [ ] Works offline (PWA)
```

---

## Example: Fire Dodge Game

```bash
/arcanea-game-development new fire-dodge --template arcade --element fire
```

Creates:
- Next.js 15 project
- Tailwind v4 configured
- Framer Motion animations
- Zustand game state
- Phaser 3 canvas
- Sound effects (Howler)
- Leaderboard (Supabase)
- E2E tests (Playwright)
- Vercel deployment config

---

*"Build games that honor the Guardians."*
