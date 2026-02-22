---
name: ui-design-pro
description: The definitive UI design skill for building professional, production-grade software. Use this skill when the user wants to create, redesign, polish, or elevate any web application UI — dashboards, SaaS apps, landing pages, billing pages, analytics views, mobile apps, or any "vibecoded" interface. Covers 25+ design laws across color theory (4-layer system, OKLCH, dark mode, HSB palettes), layout, typography, icons, micro-interactions, component design, pricing pages, analytics, cards, spacing, interactive feedback, playful design, presentation techniques, and design thinking. Produces clean, modern, trustworthy software that converts.
license: MIT
---

# UI Design Pro — The Complete System

This skill transforms rough, AI-generated, or amateur UI into polished, professional software. It encodes specific, actionable design principles organized into a layered system that covers everything from color science to micro-interactions to design philosophy.

## When to Use This Skill

- User has an existing UI that looks "AI-generated" or unpolished
- User wants to build a new SaaS dashboard, landing page, or app
- User asks to "make it look professional" or "redesign this"
- User is building any web application and wants it to look production-grade
- User has a vibecoded prototype that needs design elevation
- User wants to add micro-interactions or animations
- User needs a color palette or dark mode
- User wants to make a design more playful or engaging
- User needs to present/showcase their designs

## Core Philosophy

**Design is not art — it is a story.** The goal is not to impress other designers, it is to guide someone to an action. Start with user intent, not aesthetics. Only as user intent expands should functionality expand. Fonts, colors, and icons affect aesthetics but do very little to change functionality. Focus on making things work brilliantly for the user first, then make them beautiful.

**Presentation drives conversion and trust.** AI-generated UIs fail in predictable, fixable ways. The problems are almost always the same: wrong icons, bad colors, redundant information, poor layouts, and missing features. Fixing these specific issues transforms amateur software into professional products.

---

# PART 1: THE 10 FOUNDATION LAWS

These are the core rules for transforming any AI-generated or amateur UI into professional software.

---

### LAW 1: Kill the Emojis — Use Professional Icon Libraries

**The Problem**: AI defaults to emojis. This instantly signals "not professional."

**The Fix**: Replace ALL emojis with icons from professional interface libraries.

**Recommended libraries:**
1. **Lucide** — Clean, consistent. Best default for React/web.
2. **Phosphor Icons** — More personality, multiple weights.
3. **Heroicons** — Tailwind ecosystem, solid and outline variants.
4. **Feather Icons** — Lightweight, good Figma plugin.

**Icon rules:**
- Outline/regular weight for navigation and secondary elements
- Filled/solid weight for active states and primary actions
- Consistent sizes within context (16px inline, 20px nav, 24px feature cards)
- Icons ADD information or aid scanning — never decorative filler
- For the most part, icons need NO color. Reserve color for communicating STATUS.
- It IS okay to have different icon styles in the same design, but ONLY if they are visually separate areas
- Well-known icons (home, bookmark, user) need no label. Ambiguous icons need a tooltip.

---

### LAW 2: Never Let AI Choose Your Colors

**The Problem**: AI gravitates toward bright, saturated colors that clash.

**The Fix**: Use muted, sophisticated palettes. See PART 2 for the complete 4-layer color system.

**Quick rules:**
- Backgrounds: dark, desaturated tones. Never bright colors.
- ONE accent color used sparingly for CTAs and active states.
- Add color THROUGH data visualization (charts, sparklines), not decorative UI.
- The more important a button is, the darker it is (ghost to outlined to filled to black).

---

### LAW 3: Eliminate Redundancy — Show Information Once

Every piece of information appears EXACTLY ONCE in the most appropriate location. If a card or section has no interaction and no unique data, DELETE IT.

---

### LAW 4: KPIs Should Be Rich, Not Repetitive

Elevate KPIs with micro-charts, trends, and contextual data. Each KPI card includes: label (small), primary value (large, tabular-nums), trend indicator (arrow + percentage), micro-chart (sparkline), comparison context. Use donut charts for usage/quota KPIs.

---

### LAW 5: Never Let AI Choose Your Layout

**Sidebar:** Align LEFT, tighten spacing, only relevant nav items, replace gradient profile circles with account card, collapse secondary items to popover.

**Cards:** Collapse actions to triple-dot menu, pattern is [Icon + Title] ... [Key Metric], chips become icons when tight, metrics go far right.

**Pages:** Two-column for settings. Tabs for organization. Full-width tables over card grids. Give charts ROOM.

---

### LAW 6: Modals Over Sparse Forms

If a form has few fields but the page has lots of space, use a MODAL. Collapse advanced options by default. Include fields AI forgot. This is the highest-ROI fix.

---

### LAW 7: Design Billing and Pricing Like a Real SaaS

4 plans max. Show discount clearly (strikethrough + savings %). Plan name SMALL, price LARGE. Show what next plan ADDS (delta, not full list). Highlight recommended plan. Use TABS for billing page (Usage | Billing | Invoices).

---

### LAW 8: Analytics Should Be Rich and Visual

Remove redundant KPIs. Time-series primary chart. Toggle for individual items to compare. Data rows with colored icons. Geographic MAP instead of bar charts. Low-hanging fruit: per-link toggle, comparison mode, geographic heatmap, referrer breakdown with favicons.

---

### LAW 9: Landing Pages Are About Presentation

Product screenshots with perspective transforms create massive credibility. Replace icon grids with actual feature screenshots. CSS perspective(1000px) rotateY(-5deg) instantly elevates. Better presentation equals better conversion.

---

### LAW 10: Sweat the Details

**Spacing:** 4/8/12/16/24/32/48/64px scale. Cards 16-24px padding. Sections 32-48px.
**Typography:** 2-3 sizes per context. Weight over size for hierarchy. Tabular figures for numbers. Large text (70px+) needs -2% to -4% kerning.
**Borders:** 1px only, barely visible. Prefer spacing over dividers. Subtle box-shadow over hard borders.
**Rounded corners:** Inner radius = outer radius minus gap. Enable iOS corner smoothing for subtle tapering.

---

# PART 2: THE 4-LAYER COLOR SYSTEM

A complete, scientific approach to color for product design.

---

## Layer 1: Neutral Foundation

For product design you need: 4 background layers, 2 border colors, 3 text variants, plus hover states.

### Light Mode

**Frame/sidebar:** Slightly darker anchor. Add 2% of brand hue to sidebar. It only needs to be very slightly darker since it is a large element.

**Cards on backgrounds — 3 approaches:**
1. Dark background + lighter cards (Vercel)
2. Light background + darker cards (Notion)
3. Monochromatic layers (Supabase)

Darker cards are often the same color as sidebar. Lighter cards can be pure white, which is why NOT having pure white as main background is smart.

**Borders:** Do not use thin black borders. Use roughly 85% white to define edges without overpowering.

**Button darkness rule:** Ghost (transparent) = least important. Light gray (90-95% white) = multi-purpose. Dark/black with white text = CTA/most important.

**Text:** Headings at 11% white. Body at 15-20%. Subtext at 30-40%. Almost never pure black.

```css
:root {
  --bg-frame: hsl(220, 8%, 96%);
  --bg-page: hsl(0, 0%, 99%);
  --bg-card: hsl(0, 0%, 100%);
  --border-default: hsl(220, 10%, 85%);
  --border-subtle: hsl(220, 8%, 91%);
  --text-primary: hsl(220, 15%, 11%);
  --text-secondary: hsl(220, 8%, 35%);
  --text-tertiary: hsl(220, 6%, 55%);
}
```

### Dark Mode

**Critical:** Dark colors look more similar. They require MORE distance to appear different. Double the distance: light mode has 2% between layers, dark mode needs 4-6%.

**Surfaces always get lighter as they elevate.** No exceptions. Dim text (not pure white for body). Brighten borders. Reserve pure white for headings and key actions only.

```css
:root {
  --bg-frame: hsl(220, 15%, 7%);
  --bg-page: hsl(220, 13%, 11%);
  --bg-card: hsl(220, 11%, 15%);
  --bg-elevated: hsl(220, 10%, 19%);
  --border-default: hsl(220, 10%, 22%);
  --text-primary: hsl(220, 10%, 93%);
  --text-secondary: hsl(220, 8%, 65%);
  --text-tertiary: hsl(220, 6%, 45%);
}
```

### Dark Mode Depth Without Shadows
Take dark background, bump UP brightness by 4-6 in HSB, bump DOWN saturation by 10-20. Repeat for each layer.

### Brand Tint
Add a hint of brand color to neutrals. GitHub uses dark blue instead of pure black. Headspace tints cards with orange.

**Tailwind shortcut:** Light bg = 50 value, accent = 500. Dark bg = 950, accent = 300. Bulletproof for every color.

---

## Layer 2: Functional Accent

Think of color as a SCALE, not a single value. Main color at 500-600. Hover at 700. Link at 400-500. Use uicolors.app for ramp generation.

**Dark mode accent:** Use 300-400 as primary (lighter). Hover at 400-500.

### HSB Palette Generation

For matching palettes that objectively look good:
1. Start with base color in HSB
2. Darker variant: slide Hue toward blue (+20 degrees), Saturation +20, Brightness -10
3. Even darker: repeat same shift
4. Blues/purples are darkest hues; yellows/reds are lightest. Shifting toward blue as you darken mimics natural color.

### Brand Color Adaptation

If brand color fails WCAG with white text: darken it, or choose complementary color across color wheel. Use analogous colors (neighbors) for variety. Mailchimp = yellow + complementary turquoise. Airbnb = bright pink + deeper pink.

---

## Layer 3: Semantic Communication

**Non-negotiable:** Red = destructive/error. Green = success. Yellow = warning. Blue = info. Even if brand is purple, destructive actions MUST be red.

### Charts: OKLCH Palette
Neutral charts are lame. Brand ramp only is too similar. Use OKLCH for perceptually uniform brightness across spectrum:
1. Go to oklch.com
2. Set consistent Lightness and Chroma
3. Increment Hue by 25-30 degrees per color
4. Each color has same perceived brightness

### Element States
- Disabled: desaturate, lighter text
- Hover: slightly lighter/brighter
- Active/pressed: slightly darker
- Mobile: press state only (darker on press for tactile feel)

---

## Layer 4: Theming via OKLCH

Convert any design to themed version:
1. Take every neutral hex, plug into OKLCH
2. Drop Lightness by 0.003, increase Chroma by 0.02
3. Adjust Hue to desired theme
4. Works for any color. Even better for dark mode.

---

# PART 3: MICRO-INTERACTIONS AND ANIMATION

Animations add clarity or functionality. Never just decoration. Buttons should ALWAYS have small animations. Scroll-jacking should be used very sparingly. Load more is better than infinite scroll.

---

## The 11 Essential Micro-Interactions

1. **Button hover text slide** — Mask two text layers, slide on hover. Scale down 0.97 on press.
2. **Toast notifications** — Slide up, loading animation, success with particles, auto-dismiss.
3. **Name tag on hover** — Pop up with spring easing (500ms, stiffness 636, dampening 24).
4. **Shimmer gradient stroke** — Rotating angular gradient masked to outline shape.
5. **Delayed tooltips** — 1000ms delay on mouse enter, instant hide on leave.
6. **Text hover pop-out** — Preview image/card appears on text hover.
7. **Progress bar drawing** — Masked colored rectangle sliding behind stroke path.
8. **Card swipe stack** — Dismiss rotates card out, cards behind scale up and shift to fill gap.
9. **Search bar expansion** — Magnifying glass expands to full search bar on click.
10. **Hover upgrade details** — Slide in next plan benefits on usage limit hover.
11. **Scroll parallax entrances** — Small elements pop in, large fly in then bob. Elements draw attention to center.

## Interactive Feedback (Critical)

- Button click: gray out or show loading
- Save action: fill icon + add badge to save tab
- Destructive: red confirmation
- Loading: spinner or skeleton, never blank
- No feedback = user thinks nothing happened

---

# PART 4: BEGINNER MISTAKES

1. **Missing user flow elements** — Sketch flow on paper first. Catch missing search, skip, save, back, empty states.
2. **Overusing effects** — Harsh shadows, loud gradients, glows. Less noise = better. Change shadow color to light gray with high blur.
3. **Tight spacing** — Use grids, increase vertical spacing, mobile needs MORE space. 4/8px grid. Nudge amount = 8.
4. **Inconsistent components** — One corner radius per size. Identical elements must be identical. Use design tokens.
5. **Bad icons** — One library, one style, one stroke width. SVG downloads.
6. **Redundant elements** — If removing it does not reduce clarity, remove it.
7. **Pretty but unreadable charts** — Clear axes, readable values, logical data mapping.
8. **Pure black/white overuse** — Use near-black and near-white. Comfort with gray = professional.

---

# PART 5: PLAYFUL DESIGN

Modern design has become sterile. Playful elements create delight and memorability.

## Contextual Illustrations
Add elements that give CONTEXT to your product without reading. Maintain spacing around text. Elements draw attention to center. Trail off from center. Do not overdo — one element too many crosses the cluttered line.

## The Vibe Spectrum
Most playful (blobs, cartoons) → Middle (doodles, scribbles) → Most professional (realistic imagery) → Neo-brutalist (bold, raw). Match to audience.

## Text Animations
Animate key words: progress bars, bouncing symbols, dropping text, checkbox animations. Goal is drawing attention through motion, not complexity.

## Friendly Copy
"We sweat the details" over "We take pride in our attention to detail." Natural language over corporate jargon.

## Fun 404 Pages
Interactive games, brand characters, smooth animations, personal text, auto-redirect.

---

# PART 6: CARD LAYOUT DESIGN

1. Remove labels if UI implies them
2. Group by related info
3. Rank by importance (most scannable gets prominence)
4. Stack related fields, right-align secondary
5. Add icons for faster scanning
6. Lose the lines — space items apart instead. Alternating row backgrounds over lines if tight.
7. Fewer elements to make your point = better

---

# PART 7: DESIGN THINKING

1. **Start with user intent** — what are they trying to DO?
2. **Design primary feature first** — only expand as intent expands
3. **Leverage existing layouts** — top-to-bottom, left-to-right, nav at top, CTAs visible
4. **Structure content for edge cases** — truncate long names, ensure icon contrast
5. **Progressive disclosure** — show needed info, reveal more on demand
6. **Design systems** — shared language for teams, know when to bend rules with intention

---

# PART 8: PRESENTING DESIGNS

## Creative/Portfolio
- **Plain background:** Darken and desaturate accent color
- **Dark glow:** Large blurred accent circles behind UI
- **Exploding:** Extend UI elements off screen
- **Skew:** 2 degrees vertical, -14 degrees horizontal. Pop main section out with shadow.
- **Collage:** Offset screens, slight rotation, do not align to grid
- **Dashboard details:** Zoom in to specific section, animate slightly

## Professional/Client
- **Mockups:** Designs on real devices (MacBook, iPad)
- **AI mockups:** Prompt with device + green screen + environment. Punch out green, skew in design.
- **Prototyping:** Do not describe, SHOW. Animate modals, transitions, hidden gestures.

---

# COMPLETE CHECKLIST

```
□ USER FLOW    Sketch flow. Catch missing elements.
□ ICONS        One library, one style. No emojis.
□ COLORS       Layer 1 neutrals → Layer 2 accent → Layer 3 semantic → Layer 4 theme
□ REDUNDANCY   Show each metric once. Delete useless cards.
□ SPACING      4/8px grid. Breathe. More space on mobile.
□ LAYOUT       Tight sidebar. Collapse actions. Two-column settings.
□ CARDS        Group, rank, remove labels, add icons.
□ FORMS        Modals for sparse forms. Add missing fields.
□ KPIs         Sparklines, trends, donut charts.
□ TYPOGRAPHY   Weight over size. Tabular nums. Kern large text.
□ EFFECTS      Remove harsh shadows/gradients.
□ COMPONENTS   Consistent radii, buttons, states.
□ FEEDBACK     Hover, press, loading, success/error.
□ MICRO        Button animations, toasts, tooltips.
□ DARK MODE    Double distance. Dim text. Brighten borders.
□ PRICING      4 tiers max. Large price. Show delta.
□ ANALYTICS    Map, toggle, icon rows.
□ CHARTS       OKLCH palette. Clear axes.
□ LANDING      Screenshots + perspective. Friendly copy.
□ PLAYFUL      Context illustrations. Text animations. Fun 404.
□ PRESENT      Skew, glow, mockups, prototypes.
```

---

# ANTI-PATTERNS REFERENCE

| AI/Beginner Default | Professional Fix |
|---------------------|-----------------|
| Emojis as icons | Lucide / Phosphor |
| Bright saturated backgrounds | Neutral gray / subtle brand tint |
| Pure black text | 11% white headings, 15-20% body |
| Pure white everywhere | 98-99% white for card flexibility |
| Gradient profile circles | Proper account card |
| Same KPI shown 3x | Show once |
| Sparse inline forms | Modals |
| 5+ pricing tiers | Max 4 |
| Small price text | LARGE price, small name |
| Bar charts for geography | Maps |
| Icon grids on landing | Product screenshots + perspective |
| Visible action buttons | Triple-dot overflow |
| Full text badges | Icon-only chips |
| Loose sidebar | Tight, left-aligned |
| Color as decoration | Color through data |
| Useless cards | Delete |
| Harsh shadows | Light gray, high blur, or remove |
| Black borders on cards | 85% white borders |
| Tight spacing | 4/8px grid, breathe |
| Mixed corner radii | One radius per size |
| Mixed icon styles | One library, one width |
| No hover/press states | Feedback on everything |
| Dark = inverted light | Separate palette, double distance |
| Pretty unreadable charts | Axes, readable, logical |
| Corporate jargon | Natural language |
| Static everything | Purposeful micro-interactions |
| Overused scroll animations | Progressive disclosure |
| No interactive feedback | Loading, success, error states |
