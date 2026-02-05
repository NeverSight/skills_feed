---
name: ui-ux-pro-max
description: "UI/UX design intelligence. 50 styles, 21 palettes, 50 font pairings, 20 charts, 9 stacks (React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui). Actions: plan, build, create, design, implement, review, fix, improve, optimize, enhance, refactor, check UI/UX code. Projects: website, landing page, dashboard, admin panel, e-commerce, SaaS, portfolio, blog, mobile app, .html, .tsx, .vue, .svelte. Elements: button, modal, navbar, sidebar, card, table, form, chart. Styles: glassmorphism, claymorphism, minimalism, brutalism, neumorphism, bento grid, dark mode, responsive, skeuomorphism, flat design. Topics: color palette, accessibility, animation, layout, typography, font pairing, spacing, hover, shadow, gradient. Integrations: shadcn/ui MCP for component search and examples."
---

# UI/UX Pro Max - Design Intelligence

Comprehensive design guide for web and mobile applications. Contains 50+ styles, 97 color palettes, 57 font pairings, 99 UX guidelines, and 25 chart types across 9 technology stacks. Searchable database with priority-based recommendations.

## When to Apply

Reference these guidelines when:
- Designing new UI components or pages
- Choosing color palettes and typography
- Reviewing code for UX issues
- Building landing pages or dashboards
- Implementing data visualizations

## Rule Categories by Priority

1.  **Accessibility (CRITICAL)** - Must be met for compliance and usability
2.  **Touch & Interaction (CRITICAL)** - Essential for functionality
3.  **Performance (HIGH)** - Impacts user retention and SEO
4.  **Layout & Responsive (HIGH)** - Core structural integrity
5.  **Typography & Color (MEDIUM)** - Brand and readability
6.  **Animation (MEDIUM)** - Delight and feedback (progressive enhancement)
7.  **Style Selection (MEDIUM)** - Aesthetic direction
8.  **Charts & Data (LOW)** - Specific visualization needs

---

## Quick Reference

### 1. Accessibility (CRITICAL)
- **Contrast**: Text/Background ratio > 4.5:1 (AA) or 7:1 (AAA).
- **Target Size**: Touch targets > 44x44px (mobile).
- **Alt Text**: All images must have `alt` description.
- **Focus**: Visible focus ring for keyboard users.
- **Labels**: All form inputs must have associated labels.

### 2. Touch & Interaction (CRITICAL)
- **Feedback**: Immediate visual response on active/pressed states.
- **Thumb Zone**: Primary actions in bottom 50% of mobile screen.
- **Hit Area**: Buttons should have padding (min 12px).
- **Gestures**: Support swipe for carousels/drawers.

### 3. Performance (HIGH)
- **Images**: Use WebP/AVIF. Lazy load off-screen images.
- **CLS**: Define width/height for all media elements to prevent shifts.
- **Fonts**: Use `font-display: swap`. limit weights to 2-3.

### 4. Layout & Responsive (HIGH)
- **Mobile First**: Design for 375px width first, then scale up.
- **Grid**: Use 4-column (mobile), 8-column (tablet), 12-column (desktop).
- **Spacing**: Use 4px base scale (4, 8, 12, 16, 24, 32...).

### 5. Typography & Color (MEDIUM)
- **Scale**: Use modular scale (e.g., Major Third 1.250).
- **Line Height**: Variables by usage (Headings: 1.1-1.2, Body: 1.5).
- **Colors**: Limit strict palette to Primary, Secondary, Neural, Danger/Success.
- **Dark Mode**: Avoid pure black (#000000), use dark grey (#121212).

### 6. Animation (MEDIUM)
- **Duration**: Micro-interactions (100-200ms), Transitions (300-500ms).
- **Easing**: Use `ease-out` for entering, `ease-in` for exiting.
- **Purpose**: Only animate to guide attention or show state change.

### 7. Style Selection (MEDIUM)
- **Consistency**: Stick to one distinct style (e.g., Glassmorphism) per app.
- **Brand**: Align style with brand voice (Playful vs. Corporate).

### 8. Charts & Data (LOW)
- **Clarity**: Remove chart junk (borders, heavy grids).
- **Color**: Use distinct colors for categories (accessible for color blind).
- **Legends**: Place legends close to data.

---

## How to Use This Skill

### Step 1: Analyze User Requirements
Identify what the user wants to build and the constraints.
*   **Type**: Web App, Mobile, Dashboard, Landing Page?
*   **Vibe**: Professional, Playful, Futuristic, Minimal?
*   **Tech**: React, Vue, SwiftUI, Tailwind?

### Step 2: Generate Design System (REQUIRED)
**ALWAYS** run the `design_system.py` script to generate a cohesive design system (colors, typography, spacing, radius, shadows) tailored to the requirements.

```bash
python .agent/skills/ui-ux-pro-max/scripts/design_system.py \
  --vibe="[style_name]" \
  --color="[primary_color]" \
  --stack="[technology_stack]"
```

*   `--vibe`: e.g., "modern_clean", "cyberpunk", "luxury", "playful"
*   `--color`: e.g., "blue-500", "#FF5733", "emerald"
*   `--stack`: e.g., "html-tailwind" (default), "react-shadcn", "swiftui"

**Output**: The script will output CSS variables, Tailwind config, or specialized tokens. **Copy this output into your implementation plan or directly into the project configuration.**

### Step 3: Supplement with Detailed Searches (as needed)
If you need specific components or patterns not covered by the high-level system, use `search.py`.

```bash
python .agent/skills/ui-ux-pro-max/scripts/search.py --query "[term]" --category "[category]"
```

*   `--query`: "login form", "bar chart", "pricing card"
*   `--category`: "charts", "colors", "icons", "ui-patterns", "ui-reasoning", "ux-guidelines", "web-interface"

### Step 4: Stack Guidelines (Default: html-tailwind)
If no stack is specified, assume **HTML + Tailwind CSS**.
- Use `flex` and `grid` for layout.
- Use `rem` for sizing.
- Use `lucide-react` or `heroicons` for icons.

---

## Search Reference

### Available Domains
The `search.py` script searches across these CSV data files:
- `charts.csv`: Best practices for data viz (bar, line, pie, etc.)
- `colors.csv`: Curated palettes (light/dark modes)
- `icons.csv`: Icon system recommendations
- `ui-patterns.csv`: Component implementation guides (modals, cards, navs)
- `ui-reasoning.csv`: "Why" behind design decisions (psychology)
- `ux-guidelines.csv`: Usability rules and accessibility checks
- `web-interface.csv`: Layout templates (dashboard, landing page)

### Available Stacks
The `design_system.py` script supports:
- `html-tailwind` (Web Standard) - **DEFAULT**
- `react-shadcn` (Modern Web)
- `react-native` (Mobile)
- `swiftui` (iOS)
- `flutter` (Cross-platform)
- `vue-tailwind`
- `svelte-tailwind`
- `ios-uikit`
- `android-compose`

---

## Example Workflow

**User**: "Build a modern dashboard for a fintech app using React and Tailwind."

### Step 1: Analyze Requirements
- **Type**: Dashboard (High density, charts)
- **Vibe**: Trustworthy, Clean, Modern (Fintech)
- **Tech**: React + Tailwind

### Step 2: Generate Design System (REQUIRED)
```bash
python .agent/skills/ui-ux-pro-max/scripts/design_system.py --vibe="modern_clean" --color="slate" --stack="react-shadcn"
```
*Result*: Returns a `globals.css` with CSS variables for colors, radius, fonts.

### Step 3: Supplement with Detailed Searches (as needed)
I need a chart for revenue:
```bash
python .agent/skills/ui-ux-pro-max/scripts/search.py --query "line chart" --category "charts"
```
*Result*: Returns guidelines: "Use minimal grid lines, distinct colors for datasets, smooth curves (monotone)."

### Step 4: Stack Guidelines
Apply the generated system. Use Shadcn UI components for cards and tables.

---

## Output Formats

The skill provides outputs optimized for:
1.  **Direct Code**: CSS variables, Tailwind configs, simplified component structures.
2.  **Implementation Plans**: Checklist items for accessibility and performance.
3.  **Design Review**: Criteria to critique existing UIs.

## Tips for Better Results
- **Be Specific with "Vibe"**: "Cyberpunk" yields very different results from "Corporate".
- **Don't skip the Design System**: It acts as the "source of truth" to prevent inconsistent UIs.
- **Check Mobile**: The guidelines prioritize mobile-responsiveness.

## Common Rules for Professional UI

### Icons & Visual Elements
| Rule | Do | Don't |
|------|----|----- |
| **Stroke weight** | Match icon stroke to text weight (usually 1.5px or 2px) | Use filled icons next to outlined ones (inconsistent) |
| **Sizing** | Use 4px increments (16, 20, 24, 32) | Arbitrary sizes (17px, 23px) |
| **Alignment** | Optical alignment for play buttons/triangles | Strict geometric center |

### Interaction & Cursor
| Rule | Do | Don't |
|------|----|----- |
| **Clickable** | `cursor: pointer` on EVERYTHING clickable | Leave default arrow cursor on buttons/divs |
| **Disabled** | `cursor: not-allowed` + opacity 0.5 | Hide disabled elements completely (usually) |

### Light/Dark Mode Contrast
| Rule | Do | Don't |
|------|----|----- |
| **Text** | High contrast (Slate-900 / Slate-50) | Pure black on pure white (eye strain) |
| **Borders** | Subtle (Slate-200 / Slate-800) | Thick, dark borders in light mode |

### Layout & Spacing
| Rule | Do | Don't |
|------|----|----- |
| **Floating navbar** | Add `top-4 left-4 right-4` spacing | Stick navbar to `top-0 left-0 right-0` |
| **Content padding** | Account for fixed navbar height | Let content hide behind fixed elements |
| **Consistent max-width** | Use same `max-w-6xl` or `max-w-7xl` | Mix different container widths |

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
- [ ] Responsive at 375px, 768px, 1024px, 1440px
- [ ] No horizontal scroll on mobile

### Accessibility
- [ ] All images have alt text
- [ ] Form inputs have labels
- [ ] Color is not the only indicator
- [ ] `prefers-reduced-motion` respected
