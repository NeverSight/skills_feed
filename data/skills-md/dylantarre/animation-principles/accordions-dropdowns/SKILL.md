---
name: accordions-dropdowns
description: Use when animating accordions, collapsibles, dropdowns, or expand/collapse elements for smooth reveal transitions
---

# Accordion & Dropdown Animation Principles

Apply Disney's 12 principles to expand/collapse elements for smooth, informative reveals.

## Principles Applied to Accordions

### 1. Squash & Stretch
Content can slightly compress as it collapses, stretch as it expands. Trigger header can squash on click feedback.

### 2. Anticipation
Before expanding, header briefly depresses. Chevron starts rotation before content reveals. Builds expectation.

### 3. Staging
Expanded section should be clearly visible. Consider dimming other accordion items. Active header stays highlighted.

### 4. Straight Ahead & Pose to Pose
Define clear states: collapsed, expanding, expanded, collapsing. Pose-to-pose for controlled, reversible animations.

### 5. Follow Through & Overlapping Action
Container expands first, content fades in 50-100ms later. Chevron rotation can overshoot and settle. Creates depth.

### 6. Ease In & Ease Out
Expand: `ease-out` (fast start, smooth finish). Collapse: `ease-in` (slow start, fast finish). `cubic-bezier(0.4, 0, 0.2, 1)` works well.

### 7. Arcs
Chevron rotation should ease through the arc. Content items can enter with slight arc paths rather than straight down.

### 8. Secondary Action
While content reveals (primary), chevron rotates (secondary), sibling accordions may collapse (tertiary).

### 9. Timing
- Expand/collapse: 250-350ms
- Chevron rotation: 200-250ms
- Content fade: 150-200ms
- Stagger internal items: 30-50ms
- Click feedback: 50ms

### 10. Exaggeration
Important reveals can use more dramatic timing. FAQ accordions can have snappier animations. Match content importance.

### 11. Solid Drawing
Maintain consistent header heights. Content should not jitter during height animation. Use proper height techniques.

### 12. Appeal
Smooth accordions feel polished. Janky height animations feel broken. Proper expand/collapse is worth the technical investment.

## CSS Implementation

```css
.accordion-content {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 300ms ease-out;
}

.accordion-content.open {
  grid-template-rows: 1fr;
}

.accordion-inner {
  overflow: hidden;
}

.accordion-chevron {
  transition: transform 250ms ease-out;
}

.accordion-header[aria-expanded="true"] .accordion-chevron {
  transform: rotate(180deg);
}

/* Alternative: animate max-height */
.dropdown-content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 300ms ease-out;
}

.dropdown-content.open {
  max-height: 500px; /* larger than content */
}
```

## Key Properties
- `grid-template-rows`: smooth height
- `max-height`: simpler but less precise
- `transform`: rotate chevrons
- `opacity`: content fade
- `overflow`: hidden during transition
