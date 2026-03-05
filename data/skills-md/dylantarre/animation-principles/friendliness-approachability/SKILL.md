---
name: friendliness-approachability
description: Use when creating animations that feel warm, welcoming, and make users feel comfortable engaging.
---

# Friendliness & Approachability Animation

Create animations that welcome users and make interfaces feel warm and inviting.

## Emotional Goal

Friendliness comes from gentle, welcoming motion that doesn't intimidate. Approachability means animations that invite interaction and make users feel comfortable.

## Disney Principles for Friendliness

### Squash & Stretch
Moderate, soft deformation (10-20%). Enough to feel alive without being cartoonish. Like a friendly handshake—warm but appropriate.

### Anticipation
Gentle preparation (100-150ms). Friendly motion telegraphs intention without startling. A small "hello" before action.

### Staging
Open, inviting compositions. Elements arranged to welcome, not confront. Clear pathways into the interface.

### Straight Ahead Action
Light spontaneity for personality. Subtle variations that feel human and approachable rather than mechanical.

### Follow Through & Overlapping Action
Soft, natural settling. A gentle bounce or two. Like a friend sitting down beside you—relaxed, not rigid.

### Slow In & Slow Out
Smooth, approachable curves. No sharp accelerations. `ease-out` for welcoming entrances that arrive gently.

### Arc
Natural, relaxed curves. Motion that feels human—not robotic straight lines, not exaggerated bounces.

### Secondary Action
Warm supporting gestures. A subtle wave, a gentle nod. Elements acknowledge user presence.

### Timing
Moderate, comfortable (200-350ms). Not rushed, not sluggish. Conversational pacing that feels natural.

### Exaggeration
Mild (10-20%). Enough personality to feel warm without being overwhelming. Relatable, not theatrical.

### Solid Drawing
Soft, rounded forms. Approachable proportions. Nothing sharp or intimidating.

### Appeal
Warm colors, rounded corners. Friendly faces when appropriate. Inviting, accessible aesthetics.

## Timing Recommendations

| Element | Duration | Easing |
|---------|----------|--------|
| Welcome fade | 250-350ms | `ease-out` |
| Slide in | 300-400ms | `ease-out` |
| Hover response | 150-200ms | `ease-out` |
| Expand/reveal | 250-350ms | `ease-in-out` |

## CSS Easing

```css
--friendly-ease: cubic-bezier(0.25, 0.1, 0.25, 1);
--friendly-enter: cubic-bezier(0.0, 0, 0.2, 1);
--friendly-bounce: cubic-bezier(0.34, 1.3, 0.64, 1);
```

## Welcoming Patterns

```css
@keyframes friendly-wave {
  0%, 100% { transform: rotate(0deg); }
  20% { transform: rotate(14deg); }
  40% { transform: rotate(-8deg); }
  60% { transform: rotate(10deg); }
  80% { transform: rotate(-4deg); }
}

@keyframes friendly-appear {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(8px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}
```

## Approachability Cues

- Respond to hover with gentle acknowledgment
- Animate toward the user, not away
- Use soft shadows, not hard edges
- Elements should feel reachable
- Avoid overwhelming or confrontational motion

## When to Use

- Customer support interfaces
- Onboarding flows
- Community platforms
- Healthcare portals
- Educational apps
- Small business websites
- Personal portfolios
- Chatbots and assistants
