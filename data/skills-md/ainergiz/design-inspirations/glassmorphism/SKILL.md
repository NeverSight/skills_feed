---
name: glassmorphism
description: Creates frosted glass UI elements with blur, transparency, and subtle borders. Use when building overlays, floating controls, tooltips, or any element that should appear elevated with a translucent background.
---

# Glassmorphism Pattern

Create frosted glass effects for overlays and floating UI elements.

## Core Classes

```tsx
// Standard glassmorphic container
<div className="bg-black/20 backdrop-blur-md border border-white/10">
  ...
</div>
```

## Variations

### Dark Overlay (on images/media)
Best for controls overlaid on images or video.

```tsx
<div className="bg-black/20 backdrop-blur-md border border-white/10 rounded-full px-3 py-2">
  {/* Content */}
</div>
```

### Light Overlay (on dark backgrounds)
```tsx
<div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl px-4 py-3">
  {/* Content */}
</div>
```

### Subtle Glass (minimal effect)
```tsx
<div className="bg-black/10 backdrop-blur-sm border border-white/5 rounded-lg px-3 py-2">
  {/* Content */}
</div>
```

### Strong Glass (prominent effect)
```tsx
<div className="bg-black/40 backdrop-blur-lg border border-white/20 rounded-2xl px-5 py-4">
  {/* Content */}
</div>
```

## Token Reference

| Property | Light Glass | Standard | Strong |
|----------|-------------|----------|--------|
| Background | `bg-black/10` | `bg-black/20` | `bg-black/40` |
| Blur | `backdrop-blur-sm` | `backdrop-blur-md` | `backdrop-blur-lg` |
| Border | `border-white/5` | `border-white/10` | `border-white/20` |

## Common Use Cases

### Carousel Indicators
```tsx
<div className="absolute bottom-3 left-1/2 -translate-x-1/2">
  <div className="flex items-center gap-2 px-3 py-2 rounded-full bg-black/20 backdrop-blur-md border border-white/10">
    {/* Indicator dots */}
  </div>
</div>
```

### Floating Action Button
```tsx
<button className="fixed bottom-6 right-6 p-4 rounded-full bg-black/20 backdrop-blur-md border border-white/10 hover:bg-black/30 transition-colors">
  <Icon className="w-6 h-6 text-white" />
</button>
```

### Tooltip/Popover
```tsx
<div className="absolute top-full mt-2 px-3 py-2 rounded-lg bg-black/30 backdrop-blur-md border border-white/10">
  <span className="text-white text-sm">Tooltip content</span>
</div>
```

### Navigation Bar (over hero)
```tsx
<nav className="fixed top-0 left-0 right-0 z-50 bg-black/10 backdrop-blur-md border-b border-white/10">
  {/* Nav content */}
</nav>
```

## Text Contrast

When using glassmorphism, ensure text has sufficient contrast:

| Background Opacity | Text Color |
|-------------------|------------|
| `bg-black/10` - `bg-black/20` | `text-white` or `text-white/90` |
| `bg-black/30` - `bg-black/40` | `text-white` |
| `bg-white/10` - `bg-white/20` | `text-white` or `text-zinc-100` |

## Performance Note

`backdrop-blur` can impact performance on lower-end devices. Consider:
- Using smaller blur values (`backdrop-blur-sm`) for frequently updated elements
- Avoiding large glassmorphic areas that cover significant viewport
- Testing on mobile devices

## Checklist

- [ ] Background has transparency (e.g., `bg-black/20`)
- [ ] `backdrop-blur-*` applied for frosted effect
- [ ] Subtle border with transparency (`border-white/10`)
- [ ] Text has sufficient contrast
- [ ] Border radius matches design language
- [ ] Tested on lower-end devices for performance
