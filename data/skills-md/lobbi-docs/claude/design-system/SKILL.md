---
name: design-system
description: Apply and manage the AI-powered design system with 50+ curated styles
triggers:
  - 'apply * style'
  - 'design system'
  - 'style tokens'
  - 'make it look *'
  - 'blend * with *'
  - 'generate * component'
  - 'create styled *'
---

# AI Design System Skill

You have access to an AI-powered design system with 50+ professionally curated visual styles. This skill enables you to apply cohesive, distinctive aesthetics to components and interfaces while avoiding generic "AI slop" patterns.

## Core Capabilities

### 1. Style Application

Apply any of 50+ curated styles to components:

```
"apply art-deco style"
"use brutalist aesthetic"
"make it look cyberpunk"
```

### 2. Style Blending

Combine multiple styles with weighted blending:

```
"blend japandi with scandinavian 80/20"
"mix brutalist with glassmorphism 60/40"
"combine art-deco with cyberpunk 50/50"
```

### 3. Component Generation

Generate styled components with current active style:

```
"create button with current style"
"generate card component in art-deco style"
"build navigation bar using brutalist tokens"
```

### 4. Token Management

Access and apply design tokens:

```
"show available tokens for art-deco"
"list all minimalist styles"
"what colors are in cyberpunk theme?"
```

## Style Categories (50+ Styles)

### 1. Minimalist & Modern (5 styles)

- **minimalist**: Pure simplicity, maximum white space, subtle interactions
- **brutalist**: Raw HTML aesthetic, stark typography, intentional "broken" design
- **scandinavian**: Light woods, soft colors, cozy functionality
- **japandi**: Japanese minimalism meets Scandinavian warmth
- **swiss**: Grid-based, sans-serif typography, asymmetric layouts

### 2. Historical & Classical (5 styles)

- **art-deco**: Geometric patterns, gold accents, luxury materials
- **art-nouveau**: Organic curves, nature motifs, ornamental typography
- **baroque**: Ornate details, dramatic contrasts, rich embellishments
- **victorian**: Decorative borders, serif typography, vintage colors
- **renaissance**: Classical proportions, balanced compositions, refined details

### 3. Retro & Nostalgic (5 styles)

- **retro-80s**: Neon colors, geometric shapes, synthwave vibes
- **retro-90s**: Bold gradients, CD-ROM aesthetics, early web nostalgia
- **vaporwave**: Pastel pinks/blues, glitch effects, surreal imagery
- **y2k**: Metallic finishes, bubble letters, early 2000s tech aesthetic
- **mid-century**: Atomic age design, bold colors, organic shapes

### 4. Digital UI (5 styles)

- **glassmorphism**: Frosted glass effects, backdrop blur, transparency layers
- **neumorphism**: Soft shadows, subtle depth, tactile surfaces
- **material-design**: Elevation system, bold colors, motion principles
- **fluent-design**: Acrylic materials, depth layers, light/shadow
- **skeuomorphic**: Real-world textures, dimensional shadows, tactile metaphors

### 5. Futuristic & Sci-Fi (5 styles)

- **cyberpunk**: Neon against dark, tech grunge, high contrast
- **cybernetic**: Chrome finishes, holographic elements, tech interfaces
- **space-age**: Cosmic colors, star fields, futuristic typography
- **dystopian**: Industrial grays, worn textures, utilitarian design
- **solarpunk**: Eco-futurism, green technology, optimistic sustainability

### 6. Nature-Inspired (5 styles)

- **organic**: Natural forms, earth tones, flowing shapes
- **botanical**: Plant motifs, green palettes, growth patterns
- **coastal**: Ocean blues, sandy neutrals, weathered textures
- **desert**: Warm sands, terracotta, minimalist landscapes
- **forest**: Deep greens, wood textures, layered canopy effects

### 7. Bold & Expressive (5 styles)

- **maximalist**: Pattern overload, color clashing, intentional chaos
- **pop-art**: Bold colors, halftone patterns, comic book aesthetics
- **psychedelic**: Swirling patterns, kaleidoscopic colors, optical effects
- **graffiti**: Urban textures, spray paint effects, street art energy
- **punk**: DIY aesthetic, collage style, rebellious typography

### 8. Illustration & Artistic (5 styles)

- **hand-drawn**: Sketchy lines, imperfect shapes, human touch
- **watercolor**: Soft washes, color bleeding, organic textures
- **flat-illustration**: Vector art, solid colors, simplified shapes
- **isometric**: 3D perspective, technical illustration, game-like views
- **line-art**: Minimal strokes, monochrome, elegant simplicity

### 9. Cultural & Regional (5 styles)

- **mediterranean**: Warm blues, terracotta, sun-bleached aesthetics
- **nordic**: Cool tones, minimalist patterns, functional beauty
- **asian-zen**: Balance, negative space, natural materials
- **tribal**: Geometric patterns, earth pigments, cultural motifs
- **moroccan**: Rich colors, intricate patterns, ornamental details

### 10. Special Purpose & Emerging (5 styles)

- **dark-mode**: True blacks, OLED optimization, reduced eye strain
- **high-contrast**: WCAG AAA compliance, accessibility-first, clear hierarchy
- **print-inspired**: Newspaper layouts, editorial typography, ink textures
- **terminal**: Monospace fonts, CLI aesthetics, hacker green or amber
- **low-fi**: Intentional degradation, pixel art, retro computing

## Token Reference Structure

Design tokens are organized hierarchically:

```
src/design-system/
  tokens/
    styles/
      {style-name}.json          # Complete style definition
    core/
      colors.json                # Base color palette
      typography.json            # Font definitions
      spacing.json               # Spacing scale
      shadows.json               # Shadow tokens
      animations.json            # Motion tokens
```

Each style token file includes:

- **colors**: Primary, secondary, accent, surface, text
- **typography**: Font families, sizes, weights, line heights
- **spacing**: Margin, padding, gap scales
- **borders**: Radius, width, styles
- **shadows**: Elevation levels, focus states
- **animations**: Transitions, durations, easings

## Usage Guidelines

### Anti-AI-Slop Principles

**NEVER use these generic patterns:**

- Inter, Roboto, Arial, or Helvetica as primary fonts
- Purple/blue gradients on white backgrounds (#667eea → #764ba2)
- Generic rounded corners (border-radius: 8px everywhere)
- Cookie-cutter card layouts with drop shadows
- Overused emoji in UI (🚀 ✨ 🎉)
- Generic "modern" spacing (gap: 1rem)

**ALWAYS follow these rules:**

1. **Commit fully** to a chosen aesthetic - no half measures
2. **Use design tokens** for ALL values - no magic numbers
3. **Define hover states** - every interactive element needs feedback
4. **Consider dark mode** - design for both light and dark from the start
5. **Test accessibility** - maintain WCAG AA contrast minimum
6. **Use distinctive fonts** - choose typefaces that match the style
7. **Add personality** - each style should feel unique and intentional

### Style Application Workflow

1. **Select Style**: Choose from 50+ styles or blend multiple
2. **Load Tokens**: Reference token files for the selected style(s)
3. **Apply Systematically**: Use tokens for colors, typography, spacing
4. **Add Interactions**: Define hover, focus, active, disabled states
5. **Test Cohesion**: Ensure all components feel unified
6. **Document Usage**: Note which styles are applied where

### Component Generation Best Practices

When generating components:

1. Start with semantic HTML structure
2. Apply style tokens, not hardcoded values
3. Include all interactive states (hover, focus, active, disabled)
4. Add ARIA attributes for accessibility
5. Provide variants (sizes, colors, states)
6. Include usage examples and documentation

### Blending Formula

When blending styles with ratios (e.g., 80/20):

- **Dominant style (80%)**: Core colors, primary typography, main spacing
- **Accent style (20%)**: Secondary colors, accent fonts, decorative elements

Example blend:

```
"blend art-deco with cyberpunk 70/30"
→ Art-deco base with cyberpunk accent colors and occasional neon highlights
```

## Integration with Development Workflow

### With Coder Agent

```
"Hey coder, apply brutalist style to the dashboard components"
→ Coder applies brutalist tokens systematically
```

### With Reviewer Agent

```
"Reviewer, check if components follow art-deco style guide"
→ Reviewer validates token usage and style consistency
```

### With Planner Agent

```
"Planner, create a style migration plan from material to glassmorphism"
→ Planner breaks down token replacement strategy
```

## Quick Reference Commands

### Inspect Styles

- `"list all available styles"` - Show all 50+ styles
- `"describe {style-name}"` - Get detailed style info
- `"show {style-name} tokens"` - Display token values

### Apply Styles

- `"apply {style-name}"` - Set active style
- `"use {style-name} for {component}"` - Style specific component
- `"restyle {component} as {style-name}"` - Convert existing component

### Blend Styles

- `"blend {style-a} with {style-b}"` - 50/50 blend
- `"blend {style-a} with {style-b} {ratio}"` - Custom ratio
- `"what would {style-a} + {style-b} look like?"` - Preview blend

### Generate Components

- `"create {component} in {style-name}"` - New styled component
- `"generate {component-set} using current style"` - Multiple components
- `"build {layout} with {style-name} tokens"` - Complex layouts

## Tips for Success

1. **Be Specific**: "Apply art-deco style" is better than "make it fancy"
2. **Stay Consistent**: Use one style (or blend) per project section
3. **Trust the Tokens**: Don't override token values without good reason
4. **Test Early**: Apply styles early in development, not as afterthought
5. **Document Choices**: Note which styles and why in commit messages
6. **Embrace Constraints**: Limitations drive better design decisions

## Resources

- **Style Guide**: `@references/style-guide.md` - Detailed aesthetic rules
- **Prompt Templates**: `@references/prompt-templates.md` - Ready-to-use prompts
- **Token Schema**: `@references/token-schema.md` - Token structure reference

---

_Last Updated: 2025-12-03_
_Version: 1.0.0_
_Styles Available: 50+_
