---
name: cards-containers
description: Use when animating cards, panels, tiles, or container elements to create depth and interactivity
---

# Card & Container Animation Principles

Apply Disney's 12 principles to cards and containers for engaging, dimensional interfaces.

## Principles Applied to Cards

### 1. Squash & Stretch
Cards can subtly compress on drag-start and stretch when released. Keep it minimal: 2-3% scale change maximum.

### 2. Anticipation
Before expanding a card to detail view, briefly scale down (0.98) for 50ms, then expand. Prepares user for the transformation.

### 3. Staging
The card being interacted with should lift above others via `z-index` and shadow. Dim or blur background cards to focus attention.

### 4. Straight Ahead & Pose to Pose
Define clear states: resting, hovered, selected, expanded. Pose-to-pose transitions between these defined keyframes.

### 5. Follow Through & Overlapping Action
Card content (text, images, icons) should lag slightly behind card movement. Stagger by 20-40ms for natural feel.

### 6. Ease In & Ease Out
Card lifts use `ease-out`, card settles use `ease-in-out`. Never linear. `cubic-bezier(0.25, 0.1, 0.25, 1)` for smooth lifts.

### 7. Arcs
When cards reorder (drag-and-drop), they should follow curved paths, not straight lines. Add slight rotation during movement.

### 8. Secondary Action
While card lifts (primary), shadow expands and blurs (secondary). Image inside can subtle zoom. Border can glow.

### 9. Timing
- Hover lift: 200-250ms
- Selection: 150ms
- Expand to detail: 300-400ms
- Reorder/shuffle: 250-350ms
- Stagger between cards: 50-75ms

### 10. Exaggeration
Hover shadows can extend 2-3x normal depth. Selected cards can lift 8-12px. Keep proportional to card size.

### 11. Solid Drawing
Maintain consistent border-radius ratios when scaling. Shadows should always come from same light source. Preserve aspect ratios.

### 12. Appeal
Rounded corners feel approachable, subtle shadows add premium feel. Smooth transitions build trust. Cards should feel like physical objects.

## CSS Implementation

```css
.card {
  transition: transform 250ms ease-out,
              box-shadow 250ms ease-out;
}

.card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 12px 40px rgba(0,0,0,0.15);
}

.card-content {
  transition: transform 280ms ease-out; /* slight lag */
}
```

## Key Properties
- `transform`: translateY, scale, rotate
- `box-shadow`: depth and lift
- `z-index`: layering
- `filter`: blur for background
- `opacity`: focus states
