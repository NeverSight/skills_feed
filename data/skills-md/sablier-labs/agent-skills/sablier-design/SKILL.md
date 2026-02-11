---
name: sablier-design
description: Create distinctive, production-grade React interfaces aligned with Sablier's dark-theme aesthetic. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that leverages the Sablier theme.
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics.
Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context
about the purpose, audience, or technical constraints.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:

- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined,
  playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc.
  There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic
  direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work -
the key is intentionality, not intensity.

Then implement working code in React that is:

- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:

- **Typography**: Use **Urbanist** as the primary font family (already defined in `@shared/theme/sablier.css`).
  **Roboto** works as an alternative. Leverage the theme's font size tokens and letter spacing for consistency.
- **Color & Theme**: Leverage the existing Sablier theme (`@shared/theme/sablier.css`) with its signature
  orange-to-yellow gradient, dark surfaces, and blue/purple accents. Sablier is dark-theme native. Use the theme's color
  tokens for consistency.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion
  library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals
  (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that
  surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous
  negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual
  effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures,
  geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

Avoid generic AI-generated aesthetics like predictable layouts and component patterns, or cookie-cutter design that
lacks context-specific character. Stay true to Sablier's established visual language.

Interpret creatively and make unexpected choices that feel genuinely designed for the context within Sablier's
dark-theme aesthetic. Vary layouts, compositions, and visual treatments—no two designs should feel identical.

Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive
animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing,
typography, and subtle details. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when
thinking outside the box and committing fully to a distinctive vision.
