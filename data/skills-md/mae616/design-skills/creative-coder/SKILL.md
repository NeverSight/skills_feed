---
name: creative-coder
description: Translate motion, interaction, and visual experience into implementable constraints while preserving accessibility and performance. Apply when working on animations, transitions, scroll effects, or micro-UX.
user-invocable: false
metadata:
  tags: animation, interaction, motion, micro-ux, transitions, creative
---

# Creative Coder Skill

## When to Apply

Apply this skill when the request involves:
- Animation, interaction, motion design, transitions, scroll effects, micro-UX, immersive experience
- アニメーション、インタラクション、表現、演出、マイクロUX、没入感、スクロール、トランジション
- Any visual expression or timing-based UI behavior

## Core Principles

- **Experience is state transitions and timing, not just visuals.** Design how things change over time.
- **Constraints first.** Respect accessibility (prefers-reduced-motion) and performance (GPU load, INP/LCP).
- **Start minimal.** Prototype small, keep only animations that add value.

## Design Philosophy (Decision Rules)

1. **Motion is information, but can also be noise.** Articulate the purpose: visual guidance, state change comprehension, or delight.
2. **Don't animate everything.** Only animate important moments (create contrast).
3. **Never break a11y.** Support reduced motion, maintain contrast, preserve focus and operability.
4. **Performance IS the experience.** Avoid layout thrashing; prefer lightweight techniques.
5. **Make it reversible.** Implement animations as toggleable features.

## Initial Questions to Clarify

- What should users understand from this motion? (Purpose)
- What environment is expected? (Mobile / low-spec / slow network)
- What triggers this? (Hover / click / scroll / route change)
- Is reduced motion support required? (If yes, it's mandatory)

## Output Format (Follow This Order)

1. Purpose (what experience goal to achieve)
2. Specification (trigger, states, duration, easing, stop conditions)
3. Implementation approach (start minimal → enhance if needed)
4. Accessibility considerations (reduced motion, focus, operability)
5. Performance considerations (measurement points)
6. Next actions (prototype → integration)

## Checklist

- [ ] Can you explain the motion's purpose? (Not just "looks cool")
- [ ] Does it respect `prefers-reduced-motion`?
- [ ] Are keyboard/focus operations unobstructed?
- [ ] Does it avoid layout recalculations? (Prefer transform/opacity)
- [ ] No negative impact on INP/LCP?

## Common Pitfalls

- Over-animating everything, reducing information density
- Ignoring reduced motion, causing discomfort or danger
- Heavy implementations (scroll handler abuse) degrading INP
