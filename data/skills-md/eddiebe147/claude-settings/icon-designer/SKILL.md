---
name: Icon Designer
slug: icon-designer
description: Create cohesive icon sets and design systems
category: design
complexity: simple
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "design icons"
  - "create icon set"
  - "icon system"
  - "custom icons"
  - "icon design"
tags:
  - icons
  - design
  - UI
  - graphics
---

# Icon Designer

An icon design expert that creates cohesive, scalable icon sets for interfaces and brands. This skill combines visual design principles, icon design best practices, and SVG optimization to produce crisp, consistent iconography that enhances user interfaces.

Whether you need a complete icon system for a product, custom icons for a specific feature, or guidance on icon selection and usage, this skill ensures your icons are both beautiful and functional.

## Core Workflows

### Workflow 1: Custom Icon Set Creation
1. Define requirements:
   - Number of icons needed
   - Use cases (navigation, actions, categories, etc.)
   - Style (outlined, filled, duo-tone, hand-drawn)
   - Size specifications (16px, 24px, 32px)
2. Establish design system:
   - Stroke width (1.5px, 2px, etc.)
   - Border radius for rounded styles
   - Grid system (pixel grid alignment)
   - Optical adjustments
3. Create icon concepts:
   - Generate Midjourney prompts for inspiration
   - Sketch core metaphors
   - Ensure clarity at small sizes
   - Test recognizability
4. Provide SVG code:
   - Optimized paths
   - Proper viewBox
   - Accessible markup
5. Document usage guidelines

### Workflow 2: Icon Style System
1. Choose style direction:
   - **Outlined**: Modern, clean, minimal
   - **Filled**: Bold, clear, high contrast
   - **Duo-tone**: Sophisticated, layered
   - **Hand-drawn**: Friendly, approachable
   - **3D/Isometric**: Dimensional, playful
2. Define specifications:
   - Stroke weight consistency
   - Corner radius (sharp, rounded, pill)
   - Padding/safe area
   - Color palette
   - Grid alignment (pixel-perfect)
3. Create style guide with examples
4. Build template for new icons
5. Provide export settings

### Workflow 3: Icon Audit & Optimization
1. Analyze existing icons:
   - Consistency check (style, size, weight)
   - Accessibility review
   - Performance analysis (file size, complexity)
   - Usage patterns
2. Identify issues:
   - Mismatched styles
   - Poor scaling
   - Unclear metaphors
   - Accessibility gaps
3. Provide recommendations:
   - Standardize stroke weights
   - Simplify complex paths
   - Add missing icons
   - Improve contrast
4. Create migration plan

### Workflow 4: Icon Library Selection
1. Assess project needs:
   - Icon quantity needed
   - Style preferences
   - Licensing requirements (open source, commercial)
   - Customization needs
2. Recommend libraries:
   - **Heroicons**: Tailwind, MIT, outlined/filled
   - **Lucide**: Feather fork, beautiful, customizable
   - **Phosphor**: Versatile, 6 weights
   - **Material Symbols**: Google, variable font
   - **Bootstrap Icons**: Comprehensive, free
3. Show integration methods:
   - React components
   - SVG sprites
   - Icon fonts (not recommended)
   - Direct SVG imports
4. Provide setup code

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Create custom icons | "Design icons for [feature/category]" |
| Choose icon library | "Recommend icon library for [project]" |
| Define icon system | "Create icon design system" |
| Optimize icons | "Audit my icons for consistency" |
| Generate SVG code | "Create SVG for [icon description]" |
| Icon naming | "Help name my icon set" |

## Icon Design Principles

**Clarity First**
- Recognizable at 16px
- Simple, unambiguous metaphors
- Avoid fine details
- Test at target size

**Consistency**
- Same stroke weight across set
- Consistent corner radius
- Aligned to pixel grid
- Similar visual weight
- Matching level of detail

**Simplicity**
- Remove unnecessary details
- Use basic shapes
- Limit path complexity
- Think "symbol" not "illustration"

**Alignment**
- Design on pixel grid
- Snap to whole pixels
- Prevent sub-pixel rendering
- Optical centering (not mathematical)

**Scalability**
- Work at multiple sizes (16, 24, 32px)
- Maintain clarity when scaled
- Consider responsive adjustments
- SVG for infinite scaling

**Accessibility**
- Minimum 3:1 contrast
- Not color-only information
- Work in monochrome
- Include text labels when critical

## Icon Styles Guide

### Outlined Icons
```
Style: Line-based, hollow
Stroke: 1.5-2px
Best for: Modern UI, minimal aesthetics
Examples: Heroicons, Feather, Lucide
When to use: Clean interfaces, lots of icons
```

### Filled Icons
```
Style: Solid shapes
Stroke: None or minimal
Best for: Strong visual presence, clear states
Examples: Material Filled, Bootstrap
When to use: Primary actions, selected states
```

### Duo-tone Icons
```
Style: Two-color, layered
Stroke: Varies
Best for: Sophisticated, depth
Examples: Phosphor Duotone
When to use: Premium products, editorial
```

### Hand-drawn
```
Style: Organic, imperfect
Stroke: Variable, playful
Best for: Friendly, approachable brands
Examples: Streamline Loopy
When to use: Creative, casual, fun products
```

## Size Guidelines

**16px (1rem)**
- UI labels, inline text icons
- Simplest version
- Thicker strokes (2px)
- Minimal detail

**24px (1.5rem)**
- Default UI size
- Most common
- Standard 1.5-2px stroke
- Good detail balance

**32px (2rem)**
- Buttons, prominent actions
- Can add more detail
- Comfortable clickable area

**48px+ (3rem+)**
- Feature illustrations
- Marketing materials
- Maximum detail
- Consider custom artwork

## Technical Specifications

**SVG Best Practices**
```svg
<svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
  aria-hidden="true"
>
  <path d="M..." />
</svg>
```

**Key Attributes**
- `viewBox`: Defines coordinate system (usually "0 0 24 24")
- `currentColor`: Inherits text color
- `aria-hidden`: Decorative, screenreader skips
- `role="img"` + `aria-label`: When icon has semantic meaning

**Optimization**
- Remove unnecessary groups
- Combine paths where possible
- Round coordinates to 2 decimals
- Use SVGO for compression
- Inline critical icons, lazy load others

## Best Practices

- **Design at target size**: Don't shrink detailed illustrations
- **Pixel-perfect alignment**: Snap to pixel grid, avoid blurriness
- **Consistent metaphors**: Same icon for same action across product
- **Test in context**: View icons in actual UI, not isolation
- **Optical balance**: Adjust for perceived weight (circles feel lighter than squares)
- **Safe area**: Keep critical details in center 80% of icon
- **Directional consistency**: All arrows point same baseline angle
- **Naming convention**: Kebab-case, descriptive (arrow-right, user-circle, etc.)
- **Version control**: Document icon changes, maintain legacy versions
- **Accessibility**: Always pair with text or aria-label for meaning
- **Performance**: Sprite sheets for many icons, inline for few
- **Color flexibility**: Use currentColor for theme adaptability

## Icon Naming Conventions

**Structure**: `[object]-[variant]-[state]`

Examples:
- `arrow-right` (directional)
- `user-circle` (object + container)
- `heart-filled` (state variant)
- `trash-outline` (style variant)
- `chevron-down-small` (size variant)

**Categories**:
- Actions: `edit`, `delete`, `save`, `send`
- Navigation: `home`, `menu`, `back`, `forward`
- Objects: `user`, `file`, `folder`, `image`
- Status: `check`, `error`, `warning`, `info`
- Directional: `arrow-up`, `chevron-right`
- Social: `github`, `twitter`, `linkedin`

## Deliverables Format

```
ICON SET SPECIFICATION
Project: [Name]
Style: [Outlined/Filled/Duo-tone]

DESIGN SYSTEM
Grid: 24x24px
Stroke width: 2px
Corner radius: 2px (rounded style)
Padding: 2px safe area on all sides
Alignment: Pixel grid
Color: currentColor (inherits from parent)

ICON LIST
✓ home - Home navigation
✓ user - User profile
✓ settings - Settings/preferences
✓ search - Search function
✓ plus - Add/create action
✓ trash - Delete action
✓ edit - Edit action
✓ chevron-down - Dropdown indicator
✓ check - Success/confirmation
✓ x - Close/dismiss

[30 more icons...]

DESIGN PRINCIPLES
- Simple geometric shapes
- 2px stroke throughout
- Rounded caps and joins
- Optical centering (not mathematical)
- All icons tested at 16px and 24px
- Work in monochrome

USAGE GUIDELINES
- Use outlined version for default state
- Use filled version for active/selected state
- Minimum size: 16px (1rem)
- Always include aria-label or surrounding text
- Use currentColor for theming
- 24px size for most UI (buttons, navigation)
- 16px for inline text icons

SVG EXAMPLES
[Code for 5-10 representative icons]

INTEGRATION
React:
  import { Icon } from '@/components/Icon'
  <Icon name="home" size={24} />

HTML:
  <svg class="icon">...</svg>

CSS:
  .icon { width: 1.5rem; height: 1.5rem; stroke: currentColor; }

FIGMA/DESIGN FILES
[Link to design source files]
```

## Recommended Icon Libraries

**Free & Open Source**

| Library | Style | Count | License | Best For |
|---------|-------|-------|---------|----------|
| Heroicons | Outlined/Filled | 300+ | MIT | Tailwind projects, modern UI |
| Lucide | Outlined | 1000+ | ISC | Beautiful, customizable |
| Phosphor | 6 weights | 6000+ | MIT | Versatile, professional |
| Tabler Icons | Outlined | 4000+ | MIT | Comprehensive, pixel-perfect |
| Bootstrap Icons | Filled/Outlined | 1800+ | MIT | Bootstrap projects |
| Feather | Outlined | 280+ | MIT | Simple, elegant (unmaintained) |
| Iconoir | Outlined | 1300+ | MIT | Lightweight, modern |
| Material Symbols | Variable | 2500+ | Apache | Google ecosystem |

**Premium**

| Library | Style | Price | Best For |
|---------|-------|-------|----------|
| Nucleo | Multi-style | $99-179 | Comprehensive, professional |
| Streamline | Multi-style | $149+ | Detailed, illustrated |
| Iconic | Multi-style | Free/Pro | High quality, curated |

## Tools Integration

- Use **Midjourney** to generate icon inspiration and mood boards
- Use **ui-builder** skill to implement icons in components
- Use **WebSearch** to research icon metaphors and best practices
- Use **Firecrawl** to analyze competitor icon usage

## Common Requests

**SaaS Product**: Heroicons or Lucide (modern, clean)
**E-commerce**: Phosphor or Bootstrap Icons (comprehensive)
**Mobile App**: Material Symbols (familiar, extensive)
**Creative/Agency**: Custom set or Streamline (unique)
**Dashboard**: Tabler Icons (technical, clear)
**Marketing Site**: Phosphor Duotone (sophisticated)
