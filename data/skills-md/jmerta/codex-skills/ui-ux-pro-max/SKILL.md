---
name: ui-ux-pro-max
description: "Use when designing, building, or refining frontend UI/UX: layouts, components, visual systems, typography, color, and UX patterns for websites, landing pages, dashboards, and product interfaces. Provides searchable styles, palettes, font pairings, charts, and stack best practices (React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind)."
---

# UI/UX Pro Max - Design Intelligence

Searchable database of UI styles, color palettes, font pairings, chart types, product recommendations, UX guidelines, and stack-specific best practices.

## How to Use This Skill

Run the commands from the skill directory (`$CODEX_HOME/skills/ui-ux-pro-max`) so `scripts/search.py` resolves, or provide an absolute path to the script. If `python` is not available, use `python3`.

When user requests UI/UX work (design, build, create, implement, review, fix, improve), follow this workflow:

### Step 1: Analyze User Requirements

Extract key information from user request:
- **Product type**: SaaS, e-commerce, portfolio, dashboard, landing page, etc.
- **Style keywords**: minimal, playful, professional, elegant, dark mode, etc.
- **Industry**: healthcare, fintech, gaming, education, etc.
- **Stack**: React, Vue, Next.js, or default to `html-tailwind`

### Step 2: Search Relevant Domains

Use `search.py` multiple times to gather comprehensive information. Search until you have enough context.

```bash
python scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

**Recommended search order:**

1. **Product** - Get style recommendations for product type
2. **Style** - Get detailed style guide (colors, effects, frameworks)
3. **Typography** - Get font pairings with Google Fonts imports
4. **Color** - Get color palette (Primary, Secondary, CTA, Background, Text, Border)
5. **Landing** - Get page structure (if landing page)
6. **Chart** - Get chart recommendations (if dashboard/analytics)
7. **UX** - Get best practices and anti-patterns
8. **Stack** - Get stack-specific guidelines (default: html-tailwind)

### Step 3: Stack Guidelines (Default: infer-from-project)

If user doesn't specify a stack, infer it from the project or default to `html-tailwind`.

```bash
python scripts/search.py "<keyword>" --stack html-tailwind
```

Available stacks: `html-tailwind`, `react`, `nextjs`, `vue`, `svelte`, `swiftui`, `react-native`, `flutter`

---

## Search Reference

### Available Domains

| Domain | Use For | Example Keywords |
|--------|---------|------------------|
| `product` | Product type recommendations | SaaS, e-commerce, portfolio, healthcare, beauty, service |
| `style` | UI styles, colors, effects | glassmorphism, minimalism, dark mode, brutalism |
| `typography` | Font pairings, Google Fonts | elegant, playful, professional, modern |
| `color` | Color palettes by product type | saas, ecommerce, healthcare, beauty, fintech, service |
| `landing` | Page structure, CTA strategies | hero, hero-centric, testimonial, pricing, social-proof |
| `chart` | Chart types, library recommendations | trend, comparison, timeline, funnel, pie |
| `ux` | Best practices, anti-patterns | animation, accessibility, z-index, loading |
| `prompt` | AI prompts, CSS keywords | (style name) |

### Available Stacks

| Stack | Focus |
|-------|-------|
| `html-tailwind` | Tailwind utilities, responsive, a11y (DEFAULT) |
| `react` | State, hooks, performance, patterns |
| `nextjs` | SSR, routing, images, API routes |
| `vue` | Composition API, Pinia, Vue Router |
| `svelte` | Runes, stores, SvelteKit |
| `swiftui` | Views, State, Navigation, Animation |
| `react-native` | Components, Navigation, Lists |
| `flutter` | Widgets, State, Layout, Theming |

---

## Example Workflow

**User request:** "Làm landing page cho dịch vụ chăm sóc da chuyên nghiệp"

**AI should:**

```bash
# 1. Search product type
python scripts/search.py "beauty spa wellness service" --domain product

# 2. Search style (based on industry: beauty, elegant)
python scripts/search.py "elegant minimal soft" --domain style

# 3. Search typography
python scripts/search.py "elegant luxury" --domain typography

# 4. Search color palette
python scripts/search.py "beauty spa wellness" --domain color

# 5. Search landing page structure
python scripts/search.py "hero-centric social-proof" --domain landing

# 6. Search UX guidelines
python scripts/search.py "animation" --domain ux
python scripts/search.py "accessibility" --domain ux

# 7. Search stack guidelines (default: html-tailwind)
python scripts/search.py "layout responsive" --stack html-tailwind
```

**Then:** Synthesize all search results and implement the design.

---

## Tips for Better Results

1. **Be specific with keywords** - "healthcare SaaS dashboard" > "app"
2. **Search multiple times** - Different keywords reveal different insights
3. **Combine domains** - Style + Typography + Color = Complete design system
4. **Always check UX** - Search "animation", "z-index", "accessibility" for common issues
5. **Use stack flag** - Get implementation-specific best practices
6. **Iterate** - If first search doesn't match, try different keywords

---

## Common Rules for Professional UI

These are frequently overlooked issues that make UI look unprofessional:

### Icons & Visual Elements

| Rule | Enforce |
|------|---------|
| **SVG icon sets** | Use SVG icons from a single set (Heroicons, Lucide, Simple Icons) for UI controls; reserve emojis for content only. |
| **Stable hover states** | Use color/opacity transitions on hover; keep layout dimensions fixed to prevent shift. |
| **Correct brand logos** | Pull official SVGs from Simple Icons or brand sites; verify the latest mark before use. |
| **Consistent icon sizing** | Standardize viewBox (24x24) and apply w-6 h-6 (or equivalent) across the set. |

### Interaction & Cursor

| Rule | Enforce |
|------|---------|
| **Pointer cues** | Add `cursor-pointer` to all clickable/hoverable cards and elements. |
| **Hover feedback** | Provide clear visual feedback (color, shadow, border) on hover and focus. |
| **Smooth transitions** | Use 150-300ms transitions (colors, opacity, shadow) to keep changes fluid. |

### Light/Dark Mode Contrast

| Rule | Enforce |
|------|---------|
| **Glass card light mode** | Use `bg-white/80` or higher opacity for glass surfaces. |
| **Light text contrast** | Use `#0F172A` (slate-900) or darker for body text to meet 4.5:1 contrast. |
| **Muted text light** | Use `#475569` (slate-600) or darker for secondary text. |
| **Border visibility** | Use `border-gray-200` or higher in light mode so edges remain visible. |

### Layout & Spacing

| Rule | Enforce |
|------|---------|
| **Floating navbar spacing** | Add `top-4 left-4 right-4` (or equivalent) margin for floating navbars. |
| **Content clearance** | Add top padding equal to the fixed navbar height to keep content visible. |
| **Consistent max-width** | Use a single container width (e.g., `max-w-6xl` or `max-w-7xl`) across sections. |

---

## Pre-Delivery Checklist

Before delivering UI code, verify these items:

### Visual Quality
- [ ] No emojis used as icons (use SVG instead)
- [ ] All icons from consistent icon set (Heroicons/Lucide)
- [ ] Brand logos are correct (verified from Simple Icons)
- [ ] Hover states don't cause layout shift
- [ ] Use theme colors directly (bg-primary) not var() wrapper

### Interaction
- [ ] All clickable elements have `cursor-pointer`
- [ ] Hover states provide clear visual feedback
- [ ] Transitions are smooth (150-300ms)
- [ ] Focus states visible for keyboard navigation

### Light/Dark Mode
- [ ] Light mode text has sufficient contrast (4.5:1 minimum)
- [ ] Glass/transparent elements visible in light mode
- [ ] Borders visible in both modes
- [ ] Test both modes before delivery

### Layout
- [ ] Floating elements have proper spacing from edges
- [ ] No content hidden behind fixed navbars
- [ ] Responsive at 320px, 768px, 1024px, 1440px
- [ ] No horizontal scroll on mobile

### Accessibility
- [ ] All images have alt text
- [ ] Form inputs have labels
- [ ] Color is not the only indicator
- [ ] `prefers-reduced-motion` respected
