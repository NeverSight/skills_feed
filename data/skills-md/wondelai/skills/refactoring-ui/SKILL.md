---
name: refactoring-ui
description: Practical UI design system based on Refactoring UI (Wathan & Schoger). Use when creating or improving user interfaces, web components, dashboards, landing pages, or any visual design work. Applies to HTML/CSS, React, Tailwind, or any frontend output. Triggers on requests for UI design, styling, layout, color schemes, typography, visual hierarchy, or making interfaces "look better."
---

# Refactoring UI Design System

A practical, opinionated approach to UI design. Apply these principles when generating frontend code, reviewing designs, or advising on visual improvements.

## Core Philosophy

**Design in grayscale first.** Add color last. This forces proper hierarchy through spacing, contrast, and typography before relying on color as a crutch.

**Start with too much white space, then remove.** Dense interfaces feel overwhelming. Generous spacing feels premium.

**Details come later.** Don't obsess over icons, shadows, or micro-interactions until the layout and hierarchy work.

## Visual Hierarchy

Not everything can be important. Create hierarchy through three levers:

| Lever | Primary | Secondary | Tertiary |
|-------|---------|-----------|----------|
| **Size** | Large | Base | Small |
| **Weight** | Bold (600-700) | Medium (500) | Normal (400) |
| **Color** | Dark gray (#111) | Medium gray (#666) | Light gray (#999) |

**Combine levers, don't multiply.** Primary text = large OR bold OR dark, not all three. Save "all three" for the single most important element.

### Labels Are Secondary

Form labels, table headers, metadata labels → these support the data, not compete with it. Make labels smaller, lighter, or uppercase-small.

```
❌ Name: John Smith     (label and value same weight)
✅ NAME                  (de-emphasized label)
   John Smith           (emphasized value)
```

### Semantic Color ≠ Visual Weight

Don't make every destructive button bright red. A muted red secondary button often works better than screaming danger for routine actions.

## Spacing System

Use a **constrained spacing scale**, not arbitrary values:

```
4px  → tight coupling (icon + label)
8px  → related elements
16px → standard gap
24px → section separation  
32px → major sections
48px → page sections
64px → hero spacing
```

**Spacing defines relationships.** Elements closer together = more related. Don't use the same spacing everywhere.

### Container Width

- **Text blocks:** 45-75 characters (use `max-w-prose` or ~65ch)
- **Forms:** 300-500px max width
- **Cards:** Size to content, not viewport
- **Full-width is almost never right** for content

## Typography

### Font Size Scale

Use a modular scale. Example (1.25 ratio):

```
12px → fine print, captions
14px → secondary text, labels  
16px → body text (base)
20px → subheadings
24px → section titles
30px → page titles
36px → hero headlines
```

### Line Height Rules

- **Headings:** 1.0 - 1.25 (tight)
- **Body text:** 1.5 - 1.75 (relaxed)
- **Wider text = more line height** needed

### Font Weight Strategy

Avoid font weights below 400 for body text—they become unreadable. Use bold (600-700) for emphasis, not for everything.

Two fonts maximum: one for headings, one for body. Or use one font family with weight variation.

## Color

### Build a Palette, Not Random Colors

Each color needs **5-9 shades** from near-white to near-black:

```
Gray:    50, 100, 200, 300, 400, 500, 600, 700, 800, 900
Primary: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900
```

**The darkest shade isn't black.** Use 900-level dark grays (e.g., `#111827`) instead of pure `#000000`.

### Grays Need Saturation

Pure gray (`#808080`) looks lifeless. Add subtle saturation:
- Cool UI: Slight blue tint (`#64748b`)
- Warm UI: Slight yellow/brown tint (`#78716c`)

### HSL Adjustments

When deriving shades:
- Lighter = higher lightness, lower saturation, shift hue toward 60° (yellow)
- Darker = lower lightness, higher saturation, shift hue toward 0°/240° (red/blue)

### Accessible Contrast

- Body text: minimum 4.5:1 contrast ratio
- Large text (18px+): minimum 3:1
- Use `#374151` (gray-700) on white, not lighter grays

## Depth & Shadows

### Shadow Scale

Small shadows = raised slightly (buttons, cards)
Large shadows = floating (modals, dropdowns)

```css
--shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
--shadow-md: 0 4px 6px rgba(0,0,0,0.1);
--shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
--shadow-xl: 0 20px 25px rgba(0,0,0,0.15);
```

**Shadows have two parts:** A tight, dark shadow for crispness + a larger, softer shadow for atmosphere.

### Creating Depth Without Shadows

- Lighter top border, darker bottom border
- Subtle gradient backgrounds (lighter at top)
- Overlapping elements with offset

## Layout Patterns

### Don't Center Everything

Left-aligned text is easier to read. Center only:
- Short headlines
- Hero sections
- Single-action CTAs
- Empty states

### Break Out of the Box

Cards don't need to contain everything. Let images bleed to edges, overlap containers, or extend beyond their bounds.

### Alternate Emphasis

In lists/feeds, vary the visual treatment. Not every card needs the same layout—feature some, minimize others.

## Practical Checklist

Before considering UI "done":

- [ ] Squint test: Does hierarchy still read when blurred?
- [ ] Grayscale test: Does it work without color?
- [ ] Is there enough white space? (Probably not)
- [ ] Are labels de-emphasized vs. their values?
- [ ] Does spacing follow a consistent scale?
- [ ] Is text width constrained for readability?
- [ ] Do colors have sufficient contrast?
- [ ] Are shadows appropriate for elevation level?

## Quick Fixes for Common Problems

| Problem | Fix |
|---------|-----|
| "Looks amateur" | Add more white space, constrain widths |
| "Feels flat" | Add subtle shadows, border-bottom on sections |
| "Text is hard to read" | Increase line-height, constrain width, boost contrast |
| "Everything looks the same" | Vary size/weight/color between primary and secondary elements |
| "Feels cluttered" | Group related items, increase spacing between groups |
| "Colors clash" | Reduce saturation, use more grays, limit palette |
| "Buttons don't pop" | Increase contrast with surroundings, add shadow |

## Tailwind Quick Reference

For Tailwind CSS implementations:

```
Spacing:    p-1(4px) p-2(8px) p-4(16px) p-6(24px) p-8(32px)
Text size:  text-xs(12) text-sm(14) text-base(16) text-lg(18) text-xl(20)
Font weight: font-normal(400) font-medium(500) font-semibold(600) font-bold(700)  
Text color: text-gray-900(dark) text-gray-600(medium) text-gray-400(light)
Max width:  max-w-prose(65ch) max-w-md(28rem) max-w-lg(32rem) max-w-xl(36rem)
Shadow:     shadow-sm shadow-md shadow-lg shadow-xl
```

## Advanced Topics

For deeper guidance on specific patterns, see [references/advanced-patterns.md](references/advanced-patterns.md):
- Empty states design
- Form design & input states
- Image treatment & overlays
- Icon sizing & usage
- Interaction states (hover, focus, active)
- Color psychology
- Border radius systems
- Text truncation
- Responsive breakpoints
