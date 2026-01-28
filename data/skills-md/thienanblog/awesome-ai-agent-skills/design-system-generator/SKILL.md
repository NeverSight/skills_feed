---
name: design-system-generator
description: Generate a project-specific DESIGN_SYSTEM.md that enforces consistent UI/UX across SPAs, traditional server-rendered sites, and hybrid systems. Includes tokens, component rules, accessibility gates, and production asset/manifest guidance.
author: Official
---

# Design System Generator

## Overview

This skill generates a project-specific **`DESIGN_SYSTEM.md`** that enforces consistent UI/UX across:
- SPAs (React/Vue/Svelte/Angular)
- Traditional server-rendered sites (Laravel, Rails, Django, WordPress, etc.)
- Hybrid systems (admin + marketing + docs)

The design system must be **component-based**, portable, and practical for real implementation.

**When to use this skill:**
- Setting up UI consistency rules for a new project
- Standardizing component patterns across teams
- Establishing design tokens (colors, typography, spacing)
- Defining accessibility and performance requirements

## Interactive Workflow

### Required Questions

Ask these questions before generating the document:

```
1. Project type: SPA / Traditional / Hybrid

2. Primary framework(s): React/Vue/Svelte/Angular/None + backend/framework

3. Existing UI/template/design system already in use? (yes/no)

4. CSS approach preference:
   a) Tailwind/utility-first
   b) SCSS/SASS
   c) CSS Modules
   d) styled-components/emotion
   e) Component library (MUI/Ant/etc.)

5. Do you need light mode only, light+dark, or multi-theme?

6. Accessibility target (recommend WCAG AA) and keyboard support expectations

7. Browser/device support constraints

8. i18n/RTL requirements (if any)

9. Do you want design tokens exported? (CSS vars / JSON / both)

Reply examples:
- Short: `1a 2b 3no 4a 5b 6aa 7modern 8no 9both`
- Detailed: `SPA with Vue 3, no existing design system, using Tailwind, light+dark theme, WCAG AA, modern browsers only, no RTL, export both CSS vars and JSON`
```

### Optional Questions (ask only if relevant)

- Figma link or brand guide?
- Multi-tenant theming?
- Mobile app alignment?

## Decision Policy

### Rule 1: Prefer existing stack
If the project already uses a template or styling system, adapt to it.

### Rule 2: Choose one best-fit direction
Do not provide 3-5 "options" unless the user requests comparison. Pick one approach and commit.

### Safe Defaults

- **React SPA**: TailwindCSS + shadcn/ui (Radix primitives) + CSS variables tokens
- **Vue SPA**: TailwindCSS + headless components + CSS variables tokens
- **Angular**: Angular Material OR Tailwind + CDK (based on preference)
- **Traditional**: SCSS or PostCSS layered architecture (tokens/base/components/utilities), optional bundler

## Output Files

### Primary
- `DESIGN_SYSTEM.md`

### Optional (only if user wants)
- `design-tokens.json`
- `tokens.css`
- Sample component snippets

## Non-Negotiables (must appear in DESIGN_SYSTEM.md)

### Accessibility
- Visible focus states
- Keyboard navigation for interactive elements
- Contrast targets (WCAG AA recommended)
- Reduced motion support
- Semantic HTML first; ARIA only when necessary

### Performance / Production
- Hashed asset filenames + manifest mapping (cache busting)
- Minify CSS/JS for production
- Image optimization pipeline (including SVG optimization)
- Font loading strategy (`font-display: swap`, limit weights)

## Document Style

`DESIGN_SYSTEM.md` is a **team artifact**:
- Do not mention "AI", "assistant", "model", or "prompt"
- Use clear "Do/Don't" guidance
- Keep readable in ~10-15 minutes

## DESIGN_SYSTEM.md Required Structure

Generate a tailored document using this structure:

1. **Scope**
2. **Design principles** (3-5 bullet max)
3. **Supported platforms & constraints**
4. **Design tokens**
   - Color system
   - Typography
   - Spacing/layout
   - Radius/borders/shadows
   - Motion
5. **UI foundations**
   - Base styles/reset
   - Focus/interaction states
   - Iconography
6. **Component architecture**
   - Portability across SPA + Traditional
   - Naming + folder conventions
   - Required states (hover/focus/disabled/loading/error)
7. **Component inventory** (minimum viable list)
8. **CSS strategy & tooling**
   - SPA path vs Traditional path
9. **Production build & asset strategy**
   - dist structure
   - Manifest requirement
   - Optimization checklist
10. **Accessibility checklist** (ship gate)
11. **Examples** (token usage + one component example)

## SPA vs Traditional Guidance

### SPA guidance must include:
- Recommended bundler (Vite/Webpack/Rollup) aligned with stack
- CSS strategy (Tailwind/CSS Modules/SCSS)
- Component library decision (if any)
- Theming mechanism (CSS variables recommended)

### Traditional guidance must include:
- SCSS/PostCSS architecture:
  - tokens layer
  - base layer
  - components layer
  - utilities layer
- Recommendation for bundling (optional but encouraged)
- Manifest strategy so server templates reference hashed assets

## Required Manifest Guidance (Cache Busting)

Include an explicit section stating:
- Build output must produce a manifest mapping logical asset names to hashed filenames
- Server must read manifest to include assets
- Avoid stale browser caches in production

## Agent-Doc Patch Snippet (Required Output)

After generating `DESIGN_SYSTEM.md`, also output a short patch snippet to add to `AGENTS.md` and/or `CLAUDE.md`:

```markdown
## Design System
All UI components and pages must follow `DESIGN_SYSTEM.md`:
- Use design tokens (no hardcoded colors/sizes).
- Implement component states (hover/focus/disabled/loading/error).
- Meet accessibility and performance requirements.
```

## Reference Files

Before generating `DESIGN_SYSTEM.md`, read these reference files:

- **Template**: `TEMPLATE_DESIGN_SYSTEM.md` - Use this as the base structure for generation
- **Example CSS tokens**: `examples/tokens.css` - Reference for CSS variable token format
- **Example JSON tokens**: `examples/design-tokens.json` - Reference for JSON token export format
- **Example manifest**: `examples/manifest.example.json` - Reference for asset manifest structure
- **AGENTS.md patch**: `examples/AGENTS.patch.md` - The exact snippet to add to AGENTS.md/CLAUDE.md

## Acceptance Criteria

- `DESIGN_SYSTEM.md` is tailored to the user's stack and constraints
- Contains token rules, component state rules, accessibility gates, and production/manifest rules
- Avoids "AI" language entirely in the generated docs
- Recommends a single coherent approach (unless user asked for alternatives)
- Includes an `AGENTS.md` / `CLAUDE.md` patch snippet referencing `DESIGN_SYSTEM.md`

---

*This skill is part of the awesome-ai-agent-skills community library.*
