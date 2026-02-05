---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.


## Overview

This skill guides the creation of frontends that go beyond the generic. Use when creating interfaces, HTML/React artifacts, or any visual component.

## Avoid AI Slop

You tend to converge on generic outputs ("on distribution"). This creates the AI ​​slop aesthetic. Avoid:

- Generic fonts: Inter, Roboto, Arial, Open Sans, Lato, system fonts
- Clichéd color schemes: purple gradients on white backgrounds
- Predictable layouts and cookie-cutter patterns
- Always converge to Space Grotesk

Make creative, unexpected choices that fit the context. Vary between light/dark, different fonts, different aesthetics. Think outside the box.

## Typography

Typography instantly signals quality.

**Never use:** Inter, Roboto, Open Sans, Lato, system fonts

**Good choices:**
- Code aesthetic: JetBrains Mono, Fira Code, IBM Plex Mono
- Editorial: Playfair Display, Crimson Pro, Newsreader
- Technical: IBM Plex family, Source Sans 3
- Distinctive: Bricolage Grotesque, DM Sans, Instrument Sans

**Contrast:**
- High contrast pairs work: Display + monospace, serif + geometric sans
- Use weight extremes: 100/200 vs 800/900 (not 400 vs 600)
- Size jumps: 3x or more (not 1.5x)
- A distinctive font used decisively > multiple fonts

Upload from Google Fonts.

## Visual Hierarchy

Create clear hierarchy through scale, weight and contrast:

- **Titles:** large and heavy, dominate the screen
- **Subtitles:** medium, organize the content
- **Body:** small and light, supports information

Use a maximum of 3 hierarchy levels. High contrast for main text, medium contrast for secondary text.

## Spacing & Proximity

Use powers of 2 for spacing: **2, 4, 8, 16, 32, 64, 128**

Each value is double the previous one, creating dramatic progression and natural hierarchy.

**Proximity:**
- **2, 4, 8** → micro-spacing within elements
- **16, 32** → spacing between related elements
- **64, 128** → spacing between different sections

Nearby elements = smaller values. Separate sections = larger values. This creates visual hierarchy throughout the space.

Whitespace is critical. Use generously around important elements.

## Color & Palette

Commit to a cohesive aesthetic:

- Dominant colors with dramatic accents > evenly distributed palettes
- Temperature contrast (hot vs cold) creates visual impact
- Get inspired by IDE themes, cultural aesthetics, color theory
- Avoid multiple colors fighting for attention

Maintain consistency across your chosen palette.

## Motion & Animation

Animations add polish that static designs don't have:

- Prioritize CSS for HTML when possible
- Use motion libraries for React when necessary
- Focus on high-impact moments: orchestrated page loads with staggered reveals (stagger delays) create more delight than random micro-interactions

## Backgrounds

Create atmosphere and depth instead of solid colors:

- Gradient layers
- Subtle geometric patterns
- Contextual effects that match the aesthetics
- Avoid flat and lifeless backgrounds

## When to Apply

Use this skill whenever you create HTML/React artifacts, interface components, landing pages, dashboards, or any visual content that needs impact and personality.
