---
name: frontend-design
description: Create bold, high-end, production-grade frontend interfaces with the mindset of a professional UI/UX designer and frontend engineer.
  This skill is used when the user asks to design or redesign web interfaces
  (components, pages, dashboards, or applications) that must feel intentional,
  distinctive, and non-generic.

  The model should actively draw inspiration from a wide range of real-world design
  references (e.g. modern product interfaces, editorial layouts, design systems,
  experimental web design, trends seen on platforms like Pinterest, Awwwards, Dribbble),
  without copying any single source.

  The output must be real, implementation-ready code, but should avoid rigid,
  template-like, or overly symmetric “AI-looking” components. Layouts, spacing,
  typography, hierarchy, and interaction patterns should feel designed, not generated.

  Preference is given to strong visual direction, thoughtful UX decisions, and
  controlled experimentation over safe or conventional UI patterns.
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:

- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick a clear extreme: brutally minimal, maximalist chaos, luxury/refined, brutalist/raw, retro-futuristic, organic/soft, etc.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:

- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:

- **Typography**: Choose distinctive fonts. Avoid Arial/Inter/Roboto. Pair a bold display font with refined body font.
- **Color & Theme**: Commit to cohesive aesthetic. Use CSS variables. Dominant colors with sharp accents outperform timid palettes.
- **Motion**: High-impact animations for page load with staggered reveals. Use CSS @keyframes for HTML, Framer Motion for React.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements.
- **Backgrounds & Visual Details**: Create atmosphere with gradient meshes, noise textures, patterns, layered transparencies, shadows.

NEVER use generic AI aesthetics: Inter/Roboto/Arial fonts, purple gradients on white, predictable layouts, cookie-cutter design lacking context-specific character. No design should be the same. NEVER converge on common choices (Space Grotesk, etc.).

**IMPORTANT**: Match code complexity to vision. Maximalist = elaborate animations. Minimalist = restraint and precision.

## Design Process

**Discovery** → Understand requirements, audience, constraints → Define 3 key visual principles
**Concept** → Choose aesthetic direction → Select fonts (1-2), colors (3-5), spacing scale
**Implement** → Design tokens → Semantic HTML → Visuals → Motion → Polish
**Verify** → Accessibility, responsiveness, performance

## Design Token Detection

Before implementing, check if user's project has existing design tokens:

**Check**: `tailwind.config.js`, CSS `:root` variables, `theme.js`, `styles/variables.css`, styled-components themes

**If found**: Extract and use existing colors/typography/spacing. Follow naming conventions. Only add new tokens for gaps.
**If not found**: Use `templates/design-tokens-template.css` or create inline matching chosen aesthetic.

## Accessibility (Non-Negotiable)

WCAG 2.1 AA required. Creative freedom in aesthetics, NOT accessibility.

- **Contrast**: 4.5:1 text, 3:1 UI
- **Keyboard**: Tab/Enter/Escape work, visible focus, no traps
- **Semantic HTML**: h1-h6 hierarchy, landmarks, alt text
- **Motion**: `@media (prefers-reduced-motion: reduce)` for all animations
- **Forms**: Labels for all inputs, clear error messages

Rule: Accessibility wins. External ref: https://www.w3.org/WAI/WCAG21/quickref/

## Responsive Design

Mobile-first. Breakpoints: 640px (sm), 768px (md), 1024px (lg), 1280px (xl).

- Fluid typography: `clamp(1rem, 0.5rem + 2vw, 2rem)`
- CSS Grid/Flexbox over fixed widths
- Touch targets: 44x44px minimum
- Test on real devices

## Technical Patterns

**Design Tokens**: Follow this structure: fonts, colors, spacing, radius, shadows, animation timings (see `templates/design-tokens-template.css` for reference)

**Animations**:

- HTML/CSS: @keyframes with animation-delay for staggered effects
- React: Framer Motion for complex, CSS for simple
- Only animate transform/opacity

**Code Quality**:

- Semantic HTML (header, nav, main, article, section)
- BEM or Tailwind utilities
- Mobile-first CSS, no !important
- Performance: <50kb CSS, <3.5s TTI

**Delivery Checklist**: ✓ All states (hover/focus/loading/error) ✓ Responsive ✓ Accessible ✓ No console errors
