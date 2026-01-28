---
name: motion-designer
description: Advanced motion designer with decades of After Effects and motion graphics experience, specialized in creating engaging video specifications for Remotion. Use when creating video specs, planning motion graphics, designing animations, or when asked to "create a video", "design motion graphics", "plan video content", or "spec out a video". Produces detailed scene-by-scene specifications with timing, audio, sound effects, and animation descriptions.
---

# Motion Designer

Expert motion design guidance for creating compelling, engaging videos. This skill provides decades of After Effects and motion graphics knowledge applied to Remotion video specifications.

## Philosophy

Great motion design combines three elements:

1. **Visual storytelling** — Every frame serves the narrative
2. **Rhythmic timing** — Motion follows natural rhythms and music beats
3. **Emotional resonance** — Design choices evoke intended feelings

## How This Skill Works

When invoked, this skill guides you through creating detailed video specifications that include:

- **Scene-by-scene breakdowns** — Complete description of every visual element
- **Timing and pacing** — Precise frame timing for all animations and transitions
- **Audio strategy** — Background music recommendations with mood and energy level
- **Sound effect placement** — Specific SFX with exact timing and purpose
- **Transition design** — How scenes connect and flow
- **Visual hierarchy** — What viewers should focus on at each moment

The output is a comprehensive specification document that works seamlessly with `/remotion-best-practices` for implementation.

## Core Frameworks

### The 12 Principles of Animation (Disney)

1. **Squash and Stretch** — Gives weight and flexibility
2. **Anticipation** — Prepares the audience for action
3. **Staging** — Directs attention to most important elements
4. **Straight Ahead vs Pose-to-Pose** — Two animation approaches
5. **Follow Through and Overlapping Action** — Natural motion continues
6. **Slow In and Slow Out** — Easing creates realistic movement
7. **Arcs** — Natural movement follows curved paths
8. **Secondary Action** — Supporting details add life
9. **Timing** — Speed creates personality and mood
10. **Exaggeration** — Pushes reality for impact
11. **Solid Drawing** — Three-dimensional forms
12. **Appeal** — Design is engaging and pleasing

### Motion Design Arc

Every engaging video follows an emotional arc:

```
Hook (0-5s)     → Grab attention immediately
Build (5-30s)   → Establish context and build interest
Peak (30-70s)   → Deliver main message with maximum impact
Resolve (70-90s) → Satisfying conclusion and call-to-action
```

### Audio Design Layers

Professional motion graphics use layered audio:

1. **Background Music** — Sets mood and energy (40-60% volume)
2. **Sound Effects** — Emphasizes actions and transitions (60-80% volume)
3. **Ambient Texture** — Subtle background presence (20-30% volume)
4. **Voiceover/Dialog** — If applicable (80-100% volume)

### Timing Theory

Motion graphics timing follows natural rhythms:

- **24-30 FPS** — Standard video frame rates
- **2-frame rule** — Minimum duration for something to register
- **0.3s (9 frames)** — Minimum for comfortable reading
- **0.5s (15 frames)** — Sweet spot for UI micro-interactions
- **1-2s** — Comfortable transition duration
- **3-5s** — Scene duration for complex information
- **8-12s** — Maximum attention span without change

## Video Specification Format

When creating a video spec, use this structure:

### 1. Overview
- **Title** — Clear, descriptive name
- **Duration** — Total length in seconds
- **Dimensions** — Width x height (typically 1920x1080)
- **Frame Rate** — 30 fps (standard)
- **Style** — Visual aesthetic description
- **Mood** — Emotional tone

### 2. Audio Strategy
- **Background Music**
  - Style/genre
  - Mood and energy level
  - Key moments to sync with
  - Volume envelope (fades, ducks)
- **Sound Effects**
  - List of all SFX needed
  - Timing for each (in seconds)
  - Purpose of each effect

### 3. Scene Breakdown

For each scene, specify:

```markdown
## Scene N: [Name] (Xs - Ys, Duration: Zs)

**Visual Description:**
[Detailed description of every element, position, color, size, typography]

**Animation Details:**
- Element 1: [entrance/behavior] from Xs to Ys
- Element 2: [movement/transform] from Xs to Ys
- Element 3: [exit/transition] from Xs to Ys

**Timing:**
- Frame 0-30: [what happens]
- Frame 30-60: [what happens]
- Frame 60-90: [what happens]

**Audio:**
- Background music: [volume level, mood]
- SFX at Xs: [effect description]
- SFX at Ys: [effect description]

**Transitions:**
[How this scene transitions to the next]

**Focus Points:**
[What should draw viewer attention]
```

### 4. Technical Specifications

Include Remotion-specific guidance:

- Composition dimensions and FPS
- Color palette (hex codes)
- Typography (fonts, sizes, weights)
- Animation types (spring, interpolate, easing)
- Spring configurations for different effects
- Asset requirements (images, icons, etc.)

## Integration with Remotion Best Practices

This skill produces specifications that map directly to Remotion implementation:

- **Scene descriptions** → Remotion `<Sequence>` components
- **Timing details** → Frame-based animation with `useCurrentFrame()`
- **Animation details** → `spring()` and `interpolate()` configurations
- **Audio placements** → `<Audio>` components with timing
- **Transitions** → Transition patterns from remotion-best-practices

After creating a spec with this skill, use `/remotion-best-practices` to implement it.

## Common Video Types

| Type | Duration | Structure | Key Elements |
|------|----------|-----------|--------------|
| **Micro-interaction** | 1-3s | Single action | Fast, snappy, clear feedback |
| **Explainer intro** | 5-10s | Hook + tease | Bold text, simple concept |
| **Product demo** | 15-30s | Problem → Solution | Show, don't tell |
| **Feature showcase** | 30-60s | Build → Peak → CTA | Multiple scenes, transitions |
| **Brand story** | 60-120s | Arc structure | Emotional journey |
| **Tutorial** | 2-5min | Step-by-step | Clear progression, pauses |

## Sound Effect Categories

### UI/Interaction
- **Whoosh** — Transitions, reveals
- **Pop** — Buttons, checkmarks, success
- **Click** — Selections, interactions
- **Swoosh** — Fast movements, swipes

### Emphasis
- **Impact** — Important moments, reveals
- **Boom** — Big reveals, launches
- **Ding** — Achievements, completions
- **Chime** — Notifications, alerts

### Ambient
- **Hum** — Background technology feel
- **Texture** — Subtle atmosphere
- **Riser** — Building anticipation
- **Reverb tail** — Spacious, dramatic

## Anti-Patterns

- **Random easing** — Every animation should have intentional timing
- **Over-animation** — Not everything needs to bounce
- **Unclear hierarchy** — Viewer shouldn't guess where to look
- **Mismatched audio** — Sound must reinforce visuals
- **No breathing room** — Scenes need space to land
- **Inconsistent style** — Visual language should be coherent
- **Ignoring story arc** — Even abstract videos need flow

## Quality Checklist

Before finalizing a video spec:

- [ ] Clear visual hierarchy in every scene
- [ ] Timing follows natural rhythms
- [ ] Audio supports and enhances visuals
- [ ] Sound effects emphasize key moments
- [ ] Transitions feel smooth and purposeful
- [ ] Story arc is clear (hook → build → peak → resolve)
- [ ] Technical specs are complete for implementation
- [ ] Every element serves the narrative
- [ ] Pacing matches content complexity
- [ ] Ending has satisfying resolution

## Expert Tips

### Timing
- Action should land on music beats when possible
- Use the "rule of thirds" for timing: 1/3 anticipation, 1/3 action, 1/3 follow-through
- Vary timing to create rhythm (avoid mechanical repetition)

### Visual Design
- Use contrast to guide attention (color, size, motion)
- Limit palette to 3-5 colors for cohesion
- Typography hierarchy: headline → subhead → body
- White space is a design element, not empty space

### Audio Design
- Duck background music when SFX play (-6dB to -12dB)
- Layer 2-3 SFX for rich, full sound
- Use silence strategically for impact
- Fade in/out music, don't hard cut

### Animation
- Spring animations feel natural (damping: 200 for smooth, 20 for bouncy)
- Use easing for mechanical UI elements
- Group animations: stagger by 5-10 frames for flow
- Exit animations should be faster than entrances (3:2 ratio)

## When to Consult Rules

For detailed guidance on specific aspects:

- [rules/scene-composition.md](rules/scene-composition.md) — Visual hierarchy and staging
- [rules/timing-pacing.md](rules/timing-pacing.md) — Frame timing and rhythm
- [rules/audio-design.md](rules/audio-design.md) — Music and audio strategy
- [rules/sound-effects.md](rules/sound-effects.md) — SFX selection and placement
- [rules/transitions.md](rules/transitions.md) — Scene transitions and flow
- [rules/visual-hierarchy.md](rules/visual-hierarchy.md) — Directing attention
- [rules/storytelling-flow.md](rules/storytelling-flow.md) — Narrative structure
- [rules/camera-movement.md](rules/camera-movement.md) — Virtual camera techniques
