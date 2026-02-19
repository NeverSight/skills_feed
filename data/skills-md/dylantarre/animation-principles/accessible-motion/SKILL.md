---
name: accessible-motion
description: Use when implementing reduced motion alternatives, vestibular-safe animations, WCAG compliance, or designing for users with motion sensitivity.
---

# Accessible Motion Design

Apply Disney's 12 animation principles while ensuring accessibility for users with vestibular disorders, motion sensitivity, and cognitive disabilities.

## Quick Reference

| Principle | Accessible Implementation |
|-----------|--------------------------|
| Squash & Stretch | Opacity/color change instead |
| Anticipation | State change indication without motion |
| Staging | Focus management, not motion-based |
| Straight Ahead / Pose to Pose | Instant state changes |
| Follow Through / Overlapping | Eliminated or minimal fade |
| Slow In / Slow Out | Instant or very gentle ease |
| Arc | Straight or no movement |
| Secondary Action | Reduced or eliminated |
| Timing | Instant (0ms) or extended duration |
| Exaggeration | Removed entirely |
| Solid Drawing | Static visual clarity |
| Appeal | Clarity over personality |

## Core Principle

Animation should enhance understanding, never hinder it. When motion causes harm, provide alternatives that maintain functionality.

## Respecting User Preferences

### CSS Media Query
```css
/* Default: Full animation */
.element {
    transition: transform 300ms ease-out;
}

/* Reduced motion preference */
@media (prefers-reduced-motion: reduce) {
    .element {
        transition: opacity 200ms ease-out;
        /* Or no transition at all */
        transition: none;
    }
}
```

### JavaScript Detection
```javascript
const prefersReducedMotion = window.matchMedia(
    '(prefers-reduced-motion: reduce)'
).matches;

if (prefersReducedMotion) {
    // Use instant transitions or subtle fades
} else {
    // Use full animations
}
```

## Principle Adaptations

**Squash & Stretch** → Replace with opacity or color changes. A button can darken on press instead of compressing. Loading indicators can pulse opacity instead of bouncing.

**Anticipation** → Use static indicators. Show a loading state immediately rather than animated preparation. Hover states change color instantly rather than scaling.

**Staging** → Use focus management and visual hierarchy. Scroll to content rather than animated reveals. Static highlighting over motion-based attention.

**Motion Types** → Instant state changes replace transitions. Toggle switches snap position. Modals appear instantly. Menus show without animation.

**Follow Through** → Eliminated. Elements reach final state immediately. No settling, bouncing, or overshoot effects.

**Easing** → Either instant (0ms) or very gentle, extended duration (500ms+) with minimal distance. If using motion, slow and subtle.

**Arc/Paths** → Straight movement only if any movement. Prefer opacity transitions over positional. No circular or complex motion paths.

**Secondary Action** → Significantly reduced or eliminated. Single, clear feedback per interaction. No cascading or staggered animations.

**Timing** → Two approaches: instant (0ms) for snappy feedback, or extended (500ms+) for gentle perception. Avoid 150-400ms range—fast enough to notice, slow enough to trigger symptoms.

**Exaggeration** → Removed entirely. Literal, proportional visual feedback only. No overshoots, bounces, or dramatic effects.

**Solid Drawing** → Maintain visual clarity in static states. Design must work without any animation. Strong contrast and clear hierarchy.

**Appeal** → Appeal through clarity, not personality. Clean, predictable interactions. User confidence in interface stability.

## Safe Motion Patterns

### Generally Safe
- Opacity fades (keep subtle)
- Color transitions
- Small scale changes (<5%)
- Very slow movement (500ms+)
- Non-repeating animations

### Potentially Harmful
- Parallax scrolling
- Background movement
- Zoom animations
- Spinning/rotating elements
- Fast repeated animations
- Large moving areas (>1/4 viewport)

### Always Avoid
- Auto-playing video backgrounds
- Infinite animations
- Vestibular-triggering patterns
- Flashing (seizure risk)
- Rapid zoom in/out

## WCAG Guidelines

### WCAG 2.1 Success Criteria

**2.3.3 Animation from Interactions (AAA)**
Motion triggered by interaction can be disabled unless essential.

**2.2.2 Pause, Stop, Hide (A)**
Moving content lasting >5 seconds must be pausable.

**2.3.1 Three Flashes (A)**
No content flashes more than 3 times per second.

## Implementation Checklist

- [ ] `prefers-reduced-motion` respected globally
- [ ] All animations have reduced/no-motion alternative
- [ ] No auto-playing motion over 5 seconds
- [ ] User can pause/stop any animation
- [ ] No content flashes more than 3x/second
- [ ] Essential functionality works without animation
- [ ] Focus states clear without motion
- [ ] Loading states work without animation
- [ ] Error states visible without motion
- [ ] Form validation static-friendly

## Testing

1. Enable reduced motion in OS settings
2. Verify all functionality works
3. Check all states are clearly communicated
4. Ensure no motion remains that should be reduced
5. Test with screen reader users
6. Validate with vestibular disorder users if possible
