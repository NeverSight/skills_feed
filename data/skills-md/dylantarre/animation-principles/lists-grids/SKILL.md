---
name: lists-grids
description: Use when animating lists, grids, tables, or collections of items to create smooth ordering, filtering, and loading states
---

# List & Grid Animation Principles

Apply Disney's 12 principles to lists and grids for smooth, organized motion.

## Principles Applied to Lists & Grids

### 1. Squash & Stretch
List items compress slightly when grabbed for reorder. Grid items can stretch when expanding to fill space on filter.

### 2. Anticipation
Before list reorders, items briefly compress. Before filter removes items, they can shrink slightly. Prepares for change.

### 3. Staging
Item being dragged lifts above others (z-index + shadow). Filtered results highlight while others fade. Guide eye to relevant items.

### 4. Straight Ahead & Pose to Pose
Define states: entering, resting, reordering, exiting. Use pose-to-pose for predictable, controllable list animations.

### 5. Follow Through & Overlapping Action
Stagger item entrance: first item leads, others follow (30-50ms delay). Content within items lags behind item container.

### 6. Ease In & Ease Out
Item enter: `ease-out`. Item exit: `ease-in`. Reorder: `ease-in-out`. Stagger easing should feel like a wave, not mechanical.

### 7. Arcs
Reordering items should follow curved paths, not straight lines. Adds personality and organic feel to grid shuffles.

### 8. Secondary Action
While item moves (primary), placeholder appears (secondary), other items shift (tertiary). Coordinate the ensemble.

### 9. Timing
- Stagger delay: 30-75ms per item
- Item enter: 200-300ms
- Item exit: 150-200ms
- Reorder: 250-350ms
- Filter shuffle: 300-400ms
- Max total stagger: 500-800ms

### 10. Exaggeration
Dramatic filter transitions can scale items to 0 before removing. New items can overshoot position slightly. Make sorting visible.

### 11. Solid Drawing
Maintain consistent spacing during animations. Grid gaps should stay uniform. Item proportions should remain stable during transforms.

### 12. Appeal
Smooth list animations feel premium. Jarring reorders feel broken. Staggered entrances guide attention naturally. Users notice quality.

## CSS Implementation

```css
.list-item {
  animation: itemEnter 250ms ease-out backwards;
}

.list-item:nth-child(1) { animation-delay: 0ms; }
.list-item:nth-child(2) { animation-delay: 50ms; }
.list-item:nth-child(3) { animation-delay: 100ms; }
/* continue pattern */

@keyframes itemEnter {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.grid-item {
  transition: transform 300ms ease-in-out,
              opacity 200ms ease-out;
}
```

## Key Properties
- `transform`: translate, scale
- `opacity`: enter/exit
- `animation-delay`: stagger
- `grid-template`: layout shifts
- `order`: reordering
