---
name: robis-design-best-practice
description: Apply Robi's UI design principles for beautiful, accessible interfaces. Use when building UI components, reviewing designs, choosing colors, setting spacing, or implementing animations. Covers color theory (HSL, WCAG, halation), spacing (4px system), icons, shadows, and micro-interactions.
---

# Robi's Design Best Practice

## Quick Reference Checklist

When designing or reviewing UI components:

- [ ] Colors are low saturation (avoid "vibe code" oversaturated colors)
- [ ] Dark mode colors are desaturated or lightened appropriately
- [ ] Text contrast meets WCAG AAA standards
- [ ] No pure black (#000000) or pure white (#FFFFFF) - use tinted variations
- [ ] All spacing uses 4px multiples
- [ ] Nested border radii follow: `inner_radius = outer_radius - padding`
- [ ] Icons use consistent weight and style throughout
- [ ] Shadows avoided in dark mode (use borders/color instead)
- [ ] Animations use smooth easings (not linear)
- [ ] Micro-interactions added for premium feel

## Color Guidelines

### Avoid Oversaturated Colors

The "purple internet theory" - AI and many modern sites overuse vibrant, saturated colors. This causes user eye strain and reduces time spent on your site.

**HSL Basics:**
- **Hue**: Position on color wheel (0-360°)
- **Saturation**: How much color is present (0-100%)
- **Lightness**: How light/dark the color is (0-100%)

**Rule**: Aim for **low saturation** unless doing neo-brutalism design.

Example:
```
Bad:  hsl(280, 100%, 60%) - Too vibrant purple
Good: hsl(280, 30%, 60%)  - Muted, easier on eyes
```

### Dark Mode Color Adjustments

Colors appear brighter on black backgrounds. Compensate by:
- **Desaturating colors** (reduce saturation 10-20%)
- **Increasing lightness** slightly

```
Light mode: hsl(220, 40%, 50%)
Dark mode:  hsl(220, 25%, 65%)  // Less saturated, lighter
```

### WCAG Contrast Standards

**Always aim for AAA rating** for text on backgrounds.

- AAA: 7:1 contrast ratio minimum
- AA: 4.5:1 contrast ratio minimum (acceptable fallback)

Use tools like WebAIM Contrast Checker or built-in browser devtools.

### Prevent Halation

Pure black on white or pure white on black creates a "blurry halo" effect called halation.

**Solution**: Use slightly tinted variations.

```css
/* Instead of pure values */
/* Bad */ background: #000000;
/* Bad */ color: #FFFFFF;

/* Use tinted variations */
/* Good */ background: #0a0a0a;  /* Slightly lighter black */
/* Good */ color: #fafafa;       /* Slightly darker white */

/* Or with slight color tints */
/* Good */ background: hsl(220, 5%, 5%);   /* Dark with blue tint */
/* Good */ color: hsl(40, 5%, 98%);        /* Off-white with warm tint */
```

## Spacing System

**All spacing must be multiples of 4px.**

This creates visual consistency and alignment across your UI.

### Tailwind/Shadcn Scale

```
p-1  = 4px     gap-1  = 4px
p-2  = 8px     gap-2  = 8px
p-3  = 12px    gap-3  = 12px
p-4  = 16px    gap-4  = 16px
p-6  = 24px    gap-6  = 24px
p-8  = 32px    gap-8  = 32px
```

Use consistent spacing values throughout your design:
- Small gaps: 4px, 8px
- Medium gaps: 12px, 16px
- Large gaps: 24px, 32px, 48px

## Border Radius Stacking

When nesting elements with border radius, add the padding value to maintain concentric appearance.

**Formula**: `inner_radius = outer_radius - padding`

```css
/* Parent container */
.outer {
  border-radius: 16px;
  padding: 12px;
}

/* Child element */
.inner {
  border-radius: 4px;  /* 16px - 12px = 4px */
}
```

Tailwind example:
```jsx
<div className="rounded-2xl p-3">  {/* 16px radius, 12px padding */}
  <div className="rounded">         {/* 4px radius */}
    Content
  </div>
</div>
```

## Icon Consistency

### Never Mix Icon Styles

**Don't mix**: duotone, fill, regular, thin, light weights in the same UI.

```
Bad: Using filled home icon + regular settings icon + thin user icon
Good: All icons use regular weight and same size
```

### Show Active/Selected State

**Exception to mixing rule**: You can use a filled version of the same icon to indicate active/selected state.

```jsx
/* Navigation example */
<Icon 
  icon={isActive ? "home-filled" : "home-regular"} 
  weight="regular"
  size={24}
/>
```

### Consistency Rules
- Use same weight across all icons (e.g., all "regular")
- Use same size across context (e.g., all nav icons 24px)
- Give focused/active icons different stroke color OR filled variant
- Avoid mixing families (don't mix Phosphor with Heroicons)

## Shadows and Dark Mode

### Dark Mode Strategy

In dark mode, **avoid using shadows** for elevation. Instead use:
- Borders with subtle color
- Background color variations
- Slight lightness adjustments

```css
/* Light mode */
.card-light {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Dark mode - use border instead */
.card-dark {
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: hsl(220, 10%, 12%);
}
```

### Neumorphic Design Caution

Neumorphic design relies heavily on shadows to create depth and realistic feeling. This works well in light mode but can be problematic in dark mode. Use sparingly.

## Animation and Easings

### Avoid Linear Easings

Linear motion (y=x) feels robotic and unnatural.

**Use smooth easing functions:**

```css
/* CSS */
/* Bad */  transition: all 0.3s linear;
/* Good */ transition: all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);

/* Common easings */
ease-out:     cubic-bezier(0.0, 0.0, 0.2, 1)    /* Decelerating */
ease-in-out:  cubic-bezier(0.4, 0.0, 0.2, 1)    /* Smooth both ends */
spring:       Custom spring physics              /* Bouncy, natural */
```

### Framer Motion Example

```jsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ 
    duration: 0.4,
    ease: [0.4, 0.0, 0.2, 1]  // Custom cubic-bezier
  }}
>
  Content
</motion.div>
```

## Micro-Interactions

Add small interactive details that give premium feel. Companies like Linear, Notion, and Supabase excel at this.

### Examples of Micro-Interactions
- Button hover states with smooth color transitions
- Subtle scale on click (scale: 0.98)
- Loading skeleton animations
- Toast notifications with slide-in animations
- Checkbox animations when checked
- Input focus states with border color transitions
- Hover tooltips with delay and fade-in

```jsx
/* Button with micro-interaction */
<button className="
  px-4 py-2 rounded-lg
  bg-blue-600 hover:bg-blue-700
  transform transition-all duration-200
  hover:scale-[1.02] active:scale-[0.98]
">
  Click me
</button>
```

## Layout Alternatives

**Not every data display needs to be a table or card.**

Explore alternative layouts:
- Kanban boards for task management
- Timeline views for chronological data
- Bento grid layouts for dashboards
- List groups with dividers
- Tree views for hierarchical data
- Gallery/masonry grids for media
- Accordion/collapsible sections

Break out of the table/card pattern to create more engaging interfaces.

## Design Inspiration

### Browse and Learn

Develop your design taste by studying great work:

**Platforms to explore:**
- **Pinterest** - UI design patterns and inspiration
- **Twitter** - Design threads and tips from experts
- **cosmos.so** - Component and pattern library
- **Behance** - Professional design portfolios
- **Dribbble** - UI design shots and concepts

### Steal and Mimic

"There is always someone better than you that did something amazing - try to learn from it."

**Process:**
1. Find designs you admire
2. Analyze what makes them work
3. Recreate elements to learn the technique
4. Adapt and curate to your own style

This is how taste develops - through exposure to quality work and deliberate practice.

## Additional Resources

For code examples and implementation details, see [examples.md](examples.md).

Reference: kigen.design/color for HSL color tools.
