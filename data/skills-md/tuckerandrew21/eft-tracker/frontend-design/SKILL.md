---
name: frontend-design
description: Frontend UI/UX design for websites and web apps. Handles page layouts, component design, responsive design, animations, and accessibility. Uses RazorVision brand guidelines by default (Light Blue #43B6E7, Dark Grey #393939, Raleway font). Activates when user mentions: design, redesign, UI, UX, layout, styling, CSS, visual improvements, responsive, mobile design, component styling, or brand alignment.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, mcp__playwright__browser_navigate, mcp__playwright__browser_take_screenshot, mcp__playwright__browser_snapshot, mcp__playwright__browser_close, mcp__playwright__browser_click
---

# Frontend Design Skill

## Capabilities

This skill handles:

- **Page Design** - Layouts, hero sections, navigation, footers
- **Component Design** - Buttons, cards, modals, forms, tables
- **Responsive Design** - Mobile-first, breakpoints, fluid layouts
- **Animations** - Transitions, micro-interactions, loading states
- **Accessibility** - WCAG compliance, keyboard navigation, screen readers
- **Brand Alignment** - Color systems, typography, visual consistency

## Activation Triggers

- "Design a new page/component"
- "Update the UI/UX"
- "Make this responsive"
- "Improve the visual design"
- "Add animations/transitions"
- "Fix the mobile layout"
- "Style this component"
- "Match our brand guidelines"

## Process

### 1. Discovery

- Identify what needs designing (page, component, feature)
- Take screenshot of current state (if updating existing)
- Ask clarifying questions about requirements
- Check for existing design patterns in the project

### 2. Design Planning

- Reference brand guidelines: `~/.claude/RAZORVISION_DOCS.md`
- **Run through Design Checklist below**
- Propose design approach with rationale
- Consider responsive breakpoints
- Plan accessibility requirements
- Get user approval before implementing

## Design Checklist (Safe Rules)

Based on [Anthony Hobday's Visual Design Rules](https://anthonyhobday.com/sideprojects/saferules/).

### Colors

- [ ] **Near-black/near-white** - No pure `#000000` or `#ffffff`. Use `#0a0a0a` and `#f5f5f5` or similar
- [ ] **Saturate neutrals** - Add slight color tint (<5% saturation) to greys for cohesion
- [ ] **Distinct brightness levels** - Each color in palette should have noticeably different brightness
- [ ] **Warm OR cool** - Pick one temperature for neutrals, don't mix

### Contrast & Hierarchy

- [ ] **High contrast for important elements** - Buttons, CTAs, key content stand out
- [ ] **Lower icon contrast** - Icons paired with text should be slightly dimmer (0.8 opacity)
- [ ] **Border contrast** - Borders must contrast with BOTH container and background
- [ ] **Container brightness** - Keep within 12% of background (dark UI) or 7% (light UI)

### Spacing & Layout

- [ ] **8px spacing scale** - Use multiples: 8, 16, 24, 32, 48, 64, 96
- [ ] **Outer padding >= inner padding** - Container edges need equal or more space than interior gaps
- [ ] **Optical alignment** - Align visually, not mathematically (especially icons, shapes)
- [ ] **12-column grid** - Flexible for 1, 2, 3, 4-column layouts

### Typography

- [ ] **Max 2 typefaces** - One for headings, one for body
- [ ] **16px minimum body text** - Never smaller for readability
- [ ] **~70 character line length** - Use max-width to constrain (60-80 chars ideal)
- [ ] **Adjust letter-spacing** - Tighter for large text, looser for small text

### Buttons & Components

- [ ] **Button padding 2:1** - Horizontal padding should be double vertical
- [ ] **Nested corner radius** - Inner radius = outer radius - gap distance

### Dark UI Specific

- [ ] **No shadows** - Use borders instead; shadows don't make sense in dark UIs
- [ ] **Closer = lighter** - Elements appearing nearer should have lighter values
- [ ] **Consistent depth technique** - Pick one approach (borders, subtle bg changes) and stick with it

### Avoid

- [ ] **No adjacent hard divides** - Don't place multiple edges/borders directly next to each other
- [ ] **No complex on complex** - Simple elements on complex backgrounds, or vice versa

### 3. Implementation

**Default Brand Standards (RazorVision):**

- Colors: Light Blue (#43B6E7), Dark Grey (#393939), Light Grey (#F5F5F5)
- Typography: Raleway (Bold headings, Regular body)
- Principles: Clean, professional, generous whitespace

**CSS Approach:**

- Use CSS variables for theming
- Mobile-first responsive design
- Prefer Tailwind classes if project uses Tailwind
- Fallback to CSS modules or styled-components

**Accessibility Checklist:**

- Semantic HTML elements
- ARIA labels where needed
- Keyboard navigable
- Sufficient color contrast (4.5:1 minimum)
- Focus states visible

### 4. Verification

- Take after screenshot
- Test responsive at: 320px, 768px, 1024px, 1440px
- Verify accessibility with browser tools
- Check animations don't cause motion sickness (prefers-reduced-motion)
- Compare against design requirements

## Reference Files

- Brand guide: `~/.claude/RAZORVISION_DOCS.md`
- Logo assets: `~/.claude/rv-assets/`

## Common Patterns

### Responsive Breakpoints

```css
/* Mobile first */
@media (min-width: 640px) { /* sm */ }
@media (min-width: 768px) { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }
```

### CSS Variables Setup

```css
:root {
  --color-primary: #43B6E7;
  --color-text: #393939;
  --color-bg: #F5F5F5;
  --font-family: 'Raleway', sans-serif;
}
```

### Animation Best Practices

```css
.element {
  transition: transform 0.2s ease, opacity 0.2s ease;
}
@media (prefers-reduced-motion: reduce) {
  .element { transition: none; }
}
```
