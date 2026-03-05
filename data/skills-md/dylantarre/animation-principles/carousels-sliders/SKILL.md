---
name: carousels-sliders
description: Use when animating carousels, sliders, image galleries, or horizontally scrolling content for smooth navigation
---

# Carousel & Slider Animation Principles

Apply Disney's 12 principles to carousels and sliders for smooth, intuitive navigation.

## Principles Applied to Carousels

### 1. Squash & Stretch
Slides can slightly compress in scroll direction during fast swipes. Expands perception of speed and momentum.

### 2. Anticipation
Before slide change, current slide can shift 5-10px in direction of navigation. Button can depress before triggering.

### 3. Staging
Current/active slide should be prominently displayed: larger, centered, more opaque. Adjacent slides can be dimmed or scaled down.

### 4. Straight Ahead & Pose to Pose
Use pose-to-pose: define exact positions for each slide. Snap points should be clear and predictable.

### 5. Follow Through & Overlapping Action
After snap, slide can overshoot slightly and settle back. Content within slide (text, buttons) lags behind container movement.

### 6. Ease In & Ease Out
Swipe release: `ease-out` (momentum slowdown). Button navigation: `ease-in-out`. `cubic-bezier(0.25, 0.1, 0.25, 1)` for smooth slides.

### 7. Arcs
3D carousels should rotate slides along curved paths. Coverflow effects follow arc naturally. Even flat carousels can have subtle Y movement.

### 8. Secondary Action
While slide moves (primary), pagination updates (secondary), adjacent slides scale/fade (tertiary), progress bar moves (quaternary).

### 9. Timing
- Slide transition: 300-500ms
- Swipe momentum: 200-400ms
- Pagination dot: 150ms
- Autoplay interval: 4000-6000ms
- Pause on hover: immediate
- Adjacent slide scale: 250ms

### 10. Exaggeration
Hero carousels can use more dramatic transitions. Product carousels should be smoother, less distracting. Scale to context.

### 11. Solid Drawing
Maintain consistent slide dimensions. Gaps should stay uniform. Aspect ratios must be preserved during any transforms.

### 12. Appeal
Smooth carousels feel premium. Janky sliders feel cheap. Touch response should feel native. Investment here pays dividends.

## CSS Implementation

```css
.carousel-track {
  display: flex;
  transition: transform 400ms cubic-bezier(0.25, 0.1, 0.25, 1);
}

.carousel-slide {
  flex-shrink: 0;
  transition: transform 300ms ease-out,
              opacity 300ms ease-out;
}

.carousel-slide:not(.active) {
  transform: scale(0.9);
  opacity: 0.6;
}

.pagination-dot {
  transition: transform 150ms ease-out,
              background-color 150ms ease-out;
}

.pagination-dot.active {
  transform: scale(1.3);
}

/* CSS scroll snap */
.carousel-container {
  scroll-snap-type: x mandatory;
  scroll-behavior: smooth;
}

.carousel-slide {
  scroll-snap-align: center;
}
```

## Key Properties
- `transform`: translateX, scale
- `opacity`: inactive slides
- `scroll-snap-type`: native snapping
- `scroll-behavior`: smooth scrolling
- `transition`: slide movements
