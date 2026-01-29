---
name: design
description: >
  Use when building dashboards, admin interfaces, SaaS UIs, or any interface needing
  polished, professional design. Triggers on: "design system", "UI design", "dashboard",
  "admin interface", "make it look like Linear", "clean minimalist", "Stripe-style", "use design mode", 
  "enterprise UI", "SaaS design", "pixel-perfect", "design direction", "spacing system".
  Full access mode - can create/modify UI components and styles.
---

# Design Principles

Enforce precise, crafted design for enterprise software, SaaS dashboards, admin interfaces, and web applications. Philosophy: Jony Ive-level precision with intentional personality—every interface is polished, each designed for its specific context.

## Design Direction (REQUIRED)

Before writing any code, commit to a design direction. Don't default. Think about what this specific product needs to feel like.

### Think About Context

- **What does this product do?** A finance tool needs different energy than a creative tool.
- **Who uses it?** Power users want density. Occasional users want guidance.
- **What's the emotional job?** Trust? Efficiency? Delight? Focus?
- **What would make this memorable?** Every product has a chance to feel distinctive.

### Choose a Personality

Enterprise/SaaS UI has more range than you think:

| Personality                  | Characteristics                                    | Examples                        |
| ---------------------------- | -------------------------------------------------- | ------------------------------- |
| **Precision & Density**      | Tight spacing, monochrome, information-forward     | Linear, Raycast, terminal tools |
| **Warmth & Approachability** | Generous spacing, soft shadows, friendly colors    | Notion, Coda                    |
| **Sophistication & Trust**   | Cool tones, layered depth, financial gravitas      | Stripe, Mercury                 |
| **Boldness & Clarity**       | High contrast, dramatic negative space, confident  | Vercel                          |
| **Utility & Function**       | Muted palette, functional density, clear hierarchy | GitHub, developer tools         |
| **Data & Analysis**          | Chart-optimized, technical but accessible          | Analytics, BI tools             |

Pick one. Or blend two. But commit.

### Choose a Color Foundation

Don't default to warm neutrals. Consider the product:

- **Warm foundations** (creams, warm grays) — approachable, comfortable, human
- **Cool foundations** (slate, blue-gray) — professional, trustworthy, serious
- **Pure neutrals** (true grays, black/white) — minimal, bold, technical
- **Tinted foundations** (slight color cast) — distinctive, memorable, branded

**Light or dark?** Dark feels technical, focused, premium. Light feels open, approachable, clean.

**Accent color** — Pick ONE that means something. Blue for trust. Green for growth. Orange for energy. Violet for creativity.

### Choose a Layout Approach

The content should drive the layout:

- **Dense grids** for information-heavy interfaces where users scan and compare
- **Generous spacing** for focused tasks where users need to concentrate
- **Sidebar navigation** for multi-section apps with many destinations
- **Top navigation** for simpler tools with fewer sections
- **Split panels** for list-detail patterns where context matters

### Choose Typography

- **System fonts** — fast, native, invisible (utility-focused products)
- **Geometric sans** (Geist, Inter) — modern, clean, technical
- **Humanist sans** (SF Pro, Satoshi) — warmer, more approachable
- **Monospace influence** — technical, developer-focused, data-heavy

---

## Core Craft Principles

These apply regardless of design direction. This is the quality floor.

### The 4px Grid

All spacing uses a 4px base grid:

| Value  | Usage                                 |
| ------ | ------------------------------------- |
| `4px`  | Micro spacing (icon gaps)             |
| `8px`  | Tight spacing (within components)     |
| `12px` | Standard spacing (related elements)   |
| `16px` | Comfortable spacing (section padding) |
| `24px` | Generous spacing (between sections)   |
| `32px` | Major separation                      |

### Symmetrical Padding

TLBR must match. If top padding is 16px, left/bottom/right must also be 16px.

```css
/* Good */
padding: 16px;
padding: 12px 16px; /* Only when horizontal needs more room */

/* Bad */
padding: 24px 16px 12px 16px;
```

### Border Radius Consistency

Stick to the 4px grid. Sharper corners feel technical, rounder corners feel friendly:

- **Sharp**: 4px, 6px, 8px
- **Soft**: 8px, 12px
- **Minimal**: 2px, 4px, 6px

Don't mix systems. Consistency creates coherence.

### Depth & Elevation Strategy

Match your depth approach to your design direction. Choose ONE:

**Borders-only (flat)** — Clean, technical, dense. Works for utility-focused tools. Linear, Raycast use almost no shadows—just subtle borders.

**Subtle single shadows** — Soft lift without complexity: `0 1px 3px rgba(0,0,0,0.08)`

**Layered shadows** — Rich, premium, dimensional. Stripe and Mercury use this approach.

**Surface color shifts** — Background tints establish hierarchy without shadows. A card at `#fff` on `#f8fafc` already feels elevated.

```css
/* Borders-only approach */
--border: rgba(0, 0, 0, 0.08);
border: 0.5px solid var(--border);

/* Single shadow approach */
--shadow: 0 1px 3px rgba(0, 0, 0, 0.08);

/* Layered shadow approach */
--shadow-layered:
  0 0 0 0.5px rgba(0, 0, 0, 0.05), 0 1px 2px rgba(0, 0, 0, 0.04),
  0 2px 4px rgba(0, 0, 0, 0.03), 0 4px 8px rgba(0, 0, 0, 0.02);
```

The craft is in the choice, not the complexity.

### Card Layouts

Monotonous card layouts are lazy design. A metric card doesn't have to look like a plan card doesn't have to look like a settings card.

Design each card's internal structure for its specific content—but keep the surface treatment consistent: same border weight, shadow depth, corner radius, padding scale, typography.

### Isolated Controls

UI controls deserve container treatment. Date pickers, filters, dropdowns should feel like crafted objects.

**Never use native form elements for styled UI.** Native `<select>`, `<input type="date">` render OS-native controls that cannot be styled. Build custom components instead.

Custom select triggers must use `display: inline-flex` with `white-space: nowrap` to keep text and chevron icons on the same row.

### Typography Hierarchy

| Element   | Weight  | Tracking        |
| --------- | ------- | --------------- |
| Headlines | 600     | tight (-0.02em) |
| Body      | 400-500 | standard        |
| Labels    | 500     | slight positive |

**Scale**: 11px, 12px, 13px, 14px (base), 16px, 18px, 24px, 32px

### Monospace for Data

Numbers, IDs, codes, timestamps belong in monospace. Use `tabular-nums` for columnar alignment. Mono signals "this is data."

### Iconography

Use **Phosphor Icons** (`@phosphor-icons/react`). Icons clarify, not decorate—if removing an icon loses no meaning, remove it.

Give standalone icons presence with subtle background containers.

### Animation

- 150ms for micro-interactions, 200-250ms for larger transitions
- Easing: `cubic-bezier(0.25, 1, 0.5, 1)`
- No spring/bouncy effects in enterprise UI

### Contrast Hierarchy

Build a four-level system: **foreground** (primary) → **secondary** → **muted** → **faint**. Use all four consistently.

### Color for Meaning Only

Gray builds structure. Color only appears when it communicates: status, action, error, success. Decorative color is noise.

Ask whether each use of color is earning its place. Score bars don't need to be color-coded by performance—a single muted color works.

---

## Navigation Context

Screens need grounding. A data table floating in space feels like a component demo, not a product. Consider including:

- **Navigation** — sidebar or top nav showing where you are in the app
- **Location indicator** — breadcrumbs, page title, or active nav state
- **User context** — who's logged in, what workspace/org

When building sidebars, consider using the same background as the main content area. Tools like Supabase, Linear, and Vercel rely on a subtle border for separation rather than different background colors.

---

## Dark Mode Considerations

**Borders over shadows** — Shadows are less visible on dark backgrounds. Lean more on borders for definition. A border at 10-15% white opacity might look nearly invisible but it's doing its job.

**Adjust semantic colors** — Status colors (success, warning, error) often need to be slightly desaturated for dark backgrounds.

**Same structure, different values** — The hierarchy system (foreground → secondary → muted → faint) still applies, just with inverted values.

---

## Anti-Patterns

### Never Do This

- Dramatic drop shadows (`box-shadow: 0 25px 50px...`)
- Large border radius (16px+) on small elements
- Asymmetric padding without clear reason
- Pure white cards on colored backgrounds
- Thick borders (2px+) for decoration
- Excessive spacing (margins > 48px between sections)
- Spring/bouncy animations
- Gradients for decoration
- Multiple accent colors in one interface

### Always Question

- "Did I think about what this product needs, or did I default?"
- "Does this direction fit the context and users?"
- "Does this element feel crafted?"
- "Is my depth strategy consistent and intentional?"
- "Are all elements on the grid?"

---

## The Standard

Every interface should look designed by a team that obsesses over 1-pixel differences. Not stripped—_crafted_. And designed for its specific context.

Different products want different things. A developer tool wants precision and density. A collaborative product wants warmth and space. A financial product wants trust and sophistication. Let the product context guide the aesthetic.

The goal: **intricate minimalism with appropriate personality**. Same quality bar, context-driven execution.

---

## Pre-Delivery Checklist

Before shipping UI:

### Visual Quality

- [ ] No emojis as icons (use SVG)
- [ ] Consistent icon set throughout
- [ ] Hover states don't cause layout shift
- [ ] All elements on 4px grid
- [ ] Typography hierarchy is consistent
- [ ] Color used for meaning, not decoration

### Interaction

- [ ] Clickable elements have `cursor: pointer`
- [ ] Loading states for async operations
- [ ] Transitions are 150-300ms
- [ ] Error states are clear and actionable
- [ ] Focus states visible for keyboard navigation

### Interaction Feedback

- [ ] Buttons show pressed/active state
- [ ] Forms validate on blur or submit
- [ ] Success feedback for completed actions

### Responsive

- [ ] Works at 375px, 768px, 1024px, 1440px
- [ ] No horizontal scroll on mobile
- [ ] Content not hidden behind fixed elements
- [ ] Touch targets minimum 44px
- [ ] Text readable without zooming

### Accessibility

- [ ] Color contrast meets WCAG AA (4.5:1 for text)
- [ ] Interactive elements are keyboard accessible
- [ ] Form inputs have visible labels
- [ ] Images have alt text where meaningful
