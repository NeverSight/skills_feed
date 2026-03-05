---
name: urgency-action
description: Use when creating animations that prompt immediate user action, highlight time-sensitivity, or drive conversions.
---

# Urgency & Action Animation

Create animations that motivate immediate response and communicate time-sensitivity.

## Emotional Goal

Urgency creates a compelling need to act now. Action-driving animations capture attention, create momentum, and remove hesitation through dynamic, forward-moving motion.

## Disney Principles for Urgency

### Squash & Stretch
Sharp, impactful deformations. Quick squash on landing (15-25%) creates impact. Fast stretch during motion shows speed and force.

### Anticipation
Very short or none (0-50ms). Urgency means no time to prepare. Direct, immediate action. Skip wind-up for instant response.

### Staging
Aggressive focus on call-to-action. High contrast, motion isolation. Everything else should recede. Spotlight the urgent element.

### Straight Ahead Action
Creates unpredictable, attention-grabbing movement. Use for pulsing, shaking, or urgent indicator animations.

### Follow Through & Overlapping Action
Minimal follow-through. Sharp stops communicate decisiveness. No lingering—immediate resolution drives action.

### Slow In & Slow Out
Asymmetric: fast start, abrupt end. `ease-out` with high initial velocity. `cubic-bezier(0.0, 0, 0.2, 1)` for aggressive acceleration.

### Arc
Direct, linear paths for speed. Urgency takes the shortest route. Curved paths feel leisurely—use straight lines.

### Secondary Action
Attention-grabbing pulses, glows, or shakes. Badge counters that bounce. Subtle but persistent motion draws eyes.

### Timing
Fast and punchy (100-200ms). Rapid animations create energy. Pulse intervals: 1-2 seconds to maintain attention without annoyance.

### Exaggeration
Moderate to high (20-40%). Amplified motion captures attention. Oversized bounces on notifications, emphasized shakes on errors.

### Solid Drawing
Strong, bold forms. High-contrast shapes that command attention. No subtlety—clarity is paramount.

### Appeal
Bold colors (red, orange). Strong contrast. Asymmetric, dynamic compositions that feel active, not static.

## Timing Recommendations

| Element | Duration | Easing |
|---------|----------|--------|
| Attention pulse | 150-200ms | `ease-out` |
| CTA bounce | 200-300ms | `ease-out-back` |
| Countdown tick | 100ms | `linear` |
| Error shake | 300-400ms | `ease-in-out` |

## CSS Easing

```css
--urgency-snap: cubic-bezier(0.0, 0, 0.2, 1);
--urgency-punch: cubic-bezier(0.25, 0.46, 0.45, 0.94);
--urgency-bounce: cubic-bezier(0.34, 1.4, 0.64, 1);
```

## Attention Patterns

```css
@keyframes urgent-pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

@keyframes urgent-shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-4px); }
  75% { transform: translateX(4px); }
}
```

## When to Use

- Limited-time offers and sales
- Low stock warnings
- Countdown timers
- Form validation errors
- Notification badges
- Call-to-action buttons
- Checkout urgency

## Ethics Note

Use urgency honestly. Fake scarcity damages trust. Reserve for genuinely time-sensitive situations.
