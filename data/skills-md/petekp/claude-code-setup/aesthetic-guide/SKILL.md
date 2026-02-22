---
name: aesthetic-guide
description: Research a UI design aesthetic and produce exhaustive, implementation-ready design guidelines for coding agents. Use when the user names an aesthetic (brutalist, glassmorphism, retro-futuristic, Swiss modernist, Apple HIG, neumorphism, minimalism, cyberpunk, Material Design, art deco, vaporwave, etc.) and wants a complete style guide with exact CSS values, color palettes, component states, animations, and typography — detailed enough for a coding agent to faithfully implement the aesthetic with zero ambiguity.
---

# Aesthetic Guide

Produce exhaustive, implementation-ready design system documentation for a named UI aesthetic. The output is a reference guide detailed enough that a coding agent can faithfully implement the aesthetic with minimal room for interpretation.

## Workflow

1. **Identify the aesthetic** from the user's request
2. **Check the catalog** — read [references/aesthetic-catalog.md](references/aesthetic-catalog.md) to see if pre-researched data exists for this aesthetic
3. **Research if needed** — if the aesthetic is not in the catalog or the user wants a custom variant, conduct web research to gather implementation-level specifics (exact CSS values, fonts, colors, timing functions)
4. **Load the output schema** — read [references/output-schema.md](references/output-schema.md) for the required structure
5. **Generate the guide** — fill every section of the output schema with concrete, copy-pasteable values. No hand-waving, no "choose an appropriate value" — every property must have an exact value or a constrained range with rationale.
6. **Deliver as a markdown file** — write the completed guide to the project (default: `.claude/docs/{aesthetic-name}-design-system.md`)

## Research Protocol

When researching an aesthetic not in the catalog:

- Search for "{aesthetic} CSS", "{aesthetic} UI design system", "{aesthetic} web design examples"
- Look for open-source implementations, CodePen examples, design system documentation
- Extract concrete values: hex codes, font names, px/rem values, cubic-bezier curves, shadow syntax
- Cross-reference multiple sources to identify the consensus properties that define the aesthetic
- Distinguish between **essential** properties (without these, it's not the aesthetic) and **characteristic** properties (common but optional)

## Output Requirements

- Every color must be a hex or HSL value, never a name like "dark blue"
- Every font must be a specific family with fallback stack
- Every spacing value must be in px or rem
- Every transition must have duration + timing function
- Every interactive state (hover, active, focus, disabled) must have explicit CSS
- Every component must have all pseudo-states defined
- Include both CSS custom properties (variables) and Tailwind equivalents where applicable

## Customization

The user may request:
- **A specific framework** (Tailwind, vanilla CSS, CSS-in-JS) — adjust output format
- **A hybrid** ("brutalist with soft shadows") — blend aesthetics, noting which properties come from which
- **A variant** ("dark mode cyberpunk" vs "light mode cyberpunk") — generate the specific variant
- **Partial guide** (just colors, just typography) — generate only the requested sections
