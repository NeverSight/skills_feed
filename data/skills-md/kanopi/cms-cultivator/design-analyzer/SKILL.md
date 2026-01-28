---
name: design-analyzer
description: Automatically extract technical requirements from design references when user mentions Figma, uploads images, or says "implement this design". Analyzes colors, typography, spacing, layout, and maps to WordPress blocks or Drupal paragraph fields. Provides detailed specifications for developers including exact values, responsive behavior, and accessibility requirements.
---

# Design Analyzer Skill

## Purpose
Extract technical requirements from design references (Figma URLs, screenshots, mockups) for CMS component implementation.

## Philosophy

Accurate design-to-code translation requires systematic extraction of technical specifications.

### Core Beliefs

1. **Precision Over Interpretation**: Extract exact values, don't guess or estimate
2. **Accessibility from the Start**: Check contrast and touch targets during analysis
3. **Responsive by Default**: Design for mobile first, enhance for desktop
4. **Document Technical Decisions**: Record exact colors, spacing, typography for reproducibility

### Why Design Analysis Matters

- **Pixel-Perfect Implementation**: Faithful translation of designer intent
- **Consistent Experiences**: Same colors, spacing, typography across components
- **Accessibility Compliance**: Catch contrast and touch target issues early
- **Developer Efficiency**: Clear specs eliminate guesswork

## When This Skill Activates

This skill automatically activates when:
- User mentions **Figma URL** or Figma design
- User **uploads an image** file (.png, .jpg, .jpeg, .webp, .svg)
- User says phrases like:
  - "implement this design"
  - "create a component from this mockup"
  - "build this layout"
  - "convert this design to [WordPress/Drupal]"
- User asks to analyze visual design elements
- User references a "screenshot" or "wireframe"

## Decision Framework

Before analyzing a design, determine:

### What's the Design Source?

1. **Figma URL** → Extract artboard structure, exact values from design tokens
2. **Screenshot/Image** → Visual analysis, estimate values, measure ratios
3. **Wireframe** → Structure only, minimal styling details
4. **Partial mockup** → Analyze what's visible, note missing context

### What's the Target Platform?

**WordPress**:
- Map to **native blocks** (Group, Heading, Paragraph, Buttons, Image, Columns)
- Output: Block pattern PHP file + SCSS
- Focus: Block composition and responsive classes

**Drupal**:
- Map to **paragraph fields** (text, image, link, entity reference)
- Output: Paragraph type YAML + Twig + SCSS
- Focus: Field structure and view modes

### What Components Are Visible?

**Layout patterns**:
- Hero sections → Full-width container with content overlay
- Card grids → Repeating cards with consistent spacing
- Feature lists → Icon + heading + text patterns
- Navigation → Header with menu items

**Interactive elements**:
- Buttons → Identify all button states (default, hover, focus, active)
- Forms → Note input types, labels, validation states
- Links → Check text links vs. button styles

### What Technical Specs Are Needed?

**Always extract**:
- ✅ **Colors** - Hex values, opacity, contrast ratios
- ✅ **Typography** - Font families, sizes, weights, line heights
- ✅ **Spacing** - Margins, padding, gaps (in px or rem)
- ✅ **Layout** - Grid columns, flex direction, alignment

**Check for accessibility**:
- ✅ **Contrast ratios** - Calculate for all text (4.5:1 minimum)
- ✅ **Touch targets** - Verify buttons ≥ 44x44px on mobile
- ✅ **Focus indicators** - Note if visible focus states exist

### What Responsive Behavior?

**Analyze breakpoints**:
- **Mobile (< 768px)** - Stacked layout, larger touch targets
- **Tablet (768-1023px)** - Mixed layout, medium spacing
- **Desktop (1024px+)** - Full layout, smaller relative spacing

**Common responsive patterns**:
- Columns → Stack on mobile, side-by-side on desktop
- Font sizes → Smaller base on mobile, larger on desktop
- Images → Full width on mobile, constrained on desktop

### Decision Tree

```
User provides design reference
    ↓
Identify source type (Figma/image/wireframe)
    ↓
Determine target platform (WordPress/Drupal)
    ↓
Extract visual specs (colors/typography/spacing)
    ↓
Check accessibility (contrast/touch targets)
    ↓
Map to CMS components (blocks/paragraphs)
    ↓
Document responsive behavior
    ↓
Output structured technical spec
```

## Capabilities

### Design Input Processing
- **Figma URLs**: Extract node IDs, artboard names, frame structure
- **Screenshots**: Analyze visual hierarchy, layout patterns, UI components
- **Mockups**: Identify design system elements, spacing, typography
- **Wireframes**: Extract structure and content relationships

### Component Identification
- Recognize common patterns: heroes, CTAs, cards, galleries, slideshows
- Map sections to CMS components (WordPress blocks, Drupal paragraphs)
- Identify reusable patterns vs. unique implementations
- Detect interactive elements requiring JavaScript

### Technical Extraction
- **Colors**: Extract hex codes, identify primary/secondary/accent colors
- **Typography**: Font families, sizes, weights, line-heights
- **Spacing**: Margins, padding, gaps (in px, rem, or relative units)
- **Layout**: Grid systems, flexbox patterns, column structures
- **Breakpoints**: Responsive design requirements
- **Interactions**: Hover states, animations, transitions

## Analysis Process

### 1. Initial Assessment

Ask clarifying questions:
```
What type of component is this?
- WordPress block pattern?
- Drupal paragraph type?
- Custom theme component?

What's the primary purpose?
- Hero section?
- Content display?
- Interactive element?
- Navigation?
```

### 2. Visual Hierarchy Analysis

Examine and document:
```
Layout Structure:
- Sections and their relationships
- Container widths (full-width, contained, etc.)
- Visual hierarchy (what's most prominent)

Content Elements:
- Headings (identify h1, h2, h3 levels)
- Body text and captions
- Images and media placement
- Buttons and CTAs
- Icons and decorative elements
```

### 3. Component Mapping

#### For WordPress:
```
Map to Core Blocks:
- Group: Container/wrapper
- Cover: Full-width sections with background images
- Heading: H1-H6 headings
- Paragraph: Body text
- Buttons/Button: CTAs
- Image: Individual images
- Gallery: Image collections
- Columns/Column: Multi-column layouts
- Spacer: Vertical spacing
- Separator: Dividers
```

#### For Drupal:
```
Map to Paragraph Fields:
- Text (plain): Short text fields
- Text (formatted, long): Body/description fields
- Link: CTA buttons, navigation
- Entity reference (Media): Images, videos
- Boolean: Toggle features
- List (text): Select options
- Entity reference (Taxonomy): Categories/tags
```

### 4. Responsive Behavior Planning

Determine how layout changes:
```
Mobile (320px-767px):
- Single column layouts
- Stacked elements
- Larger touch targets
- Simplified navigation

Tablet (768px-1023px):
- 2-column layouts where appropriate
- Adjusted typography
- Moderate spacing

Desktop (1024px+):
- Multi-column layouts
- Full typography scale
- Maximum spacing
- Hover states prominent
```

### 5. Styling Requirements

Extract specific values:
```
Colors:
  primary: #HEXCODE
  secondary: #HEXCODE
  text: #HEXCODE
  background: #HEXCODE

Typography:
  heading-1: [size]px / [line-height] / [weight]
  heading-2: [size]px / [line-height] / [weight]
  body: [size]px / [line-height] / [weight]

Spacing:
  section-padding: [value]
  element-margin: [value]
  gap: [value]
```

### 6. Accessibility Requirements

Identify needs:
```
Semantic Structure:
- Proper heading hierarchy
- Landmark regions
- Form labels
- Button text

ARIA Needs:
- Labels for icon-only buttons
- Descriptions for complex widgets
- Live regions for dynamic content
- Hidden content for screen readers

Contrast:
- Check all text against backgrounds
- Verify minimum 4.5:1 for body text
- Verify minimum 3:1 for large text/UI
```

### 7. Interactive Elements

Document behavior:
```
For each interactive element:
- What triggers it (click, hover, focus)
- What changes (visual, content, navigation)
- Animation/transition details
- Keyboard interaction requirements
- Accessible alternatives
```

## Output Format

When analysis is complete, provide structured output:

```yaml
component_analysis:
  type: "block_pattern" | "paragraph_type" | "theme_component"
  name: "descriptive-name"
  cms: "wordpress" | "drupal"

structure:
  sections:
    - name: "hero"
      elements:
        - type: "heading"
          level: "h1"
          content: "Main Heading Text"
        - type: "paragraph"
          content: "Supporting text"
        - type: "button"
          style: "primary"
          text: "Call to Action"

wordpress_blocks:
    - "core/cover"
    - "core/heading"
    - "core/paragraph"
    - "core/buttons"

drupal_fields:
    - name: "field_heading"
      type: "string"
      cardinality: 1
    - name: "field_body"
      type: "text_long"
      cardinality: 1
    - name: "field_cta"
      type: "link"
      cardinality: 1

styling:
  colors:
    primary: "#0073aa"
    secondary: "#23282d"
    text: "#1e1e1e"
    background: "#ffffff"

  typography:
    heading_1:
      mobile: "2rem / 1.2 / 700"
      tablet: "2.5rem / 1.2 / 700"
      desktop: "3rem / 1.2 / 700"
    body:
      mobile: "1rem / 1.6 / 400"
      tablet: "1.125rem / 1.6 / 400"
      desktop: "1.25rem / 1.6 / 400"

  spacing:
    section_padding:
      mobile: "2rem"
      tablet: "3rem"
      desktop: "4rem"
    element_gap: "1.5rem"

  layout:
    max_width: "1200px"
    columns:
      mobile: 1
      tablet: 2
      desktop: 3

responsive:
  breakpoints:
    mobile: "320px"
    tablet: "768px"
    desktop: "1024px"
  behavior:
    - "Stack columns on mobile"
    - "Reduce heading sizes"
    - "Adjust padding/margins"

interactions:
  - element: "CTA button"
    trigger: "hover"
    effect: "background color change"
    css: "transition: background-color 0.3s ease"
  - element: "Image"
    trigger: "click"
    effect: "Open lightbox"
    requires: "JavaScript"

accessibility:
  requirements:
    - "Heading hierarchy: h1 → h2"
    - "Alt text for hero image"
    - "Button has descriptive text"
    - "Color contrast: all text 4.5:1 or better"
    - "Focus indicators on interactive elements"

  concerns:
    - "Icon-only button needs aria-label"
    - "Decorative image should have empty alt"

implementation_notes:
  - "Use CSS Grid for desktop 3-column layout"
  - "Background image should be lazy-loaded"
  - "Consider reduced motion preferences"
  - "Test with keyboard navigation"
```

## Integration with Commands

This skill provides critical context for:

### `/design-to-block` Command
Provides:
- WordPress block selections
- Pattern structure
- Styling specifications
- Accessibility requirements

### `/design-to-paragraph` Command
Provides:
- Drupal field types and configuration
- Twig template structure
- CSS requirements
- Interactive behavior specs

### `/design-validate` Command
Provides:
- Design comparison reference
- Expected behavior documentation
- Accessibility requirements to check

## Example Activation

**User uploads image and says:**
> "Create a WordPress block pattern from this hero design"

**Skill Response:**
```
I'll analyze this design for WordPress implementation.

[Performs visual analysis]

Design Analysis Complete:
- Type: Hero section with overlaid text
- WordPress Blocks Needed: Cover, Heading, Paragraph, Buttons
- Layout: Full-width background image with centered content
- Colors: Dark overlay (#000000 40% opacity), white text
- Typography: 3rem heading on desktop, 2rem mobile
- Responsive: Text size reduces, padding adjusts
- Accessibility: Need alt text for background image, ensure text contrast

Ready to generate the block pattern. Shall I proceed?
```

## Best Practices

1. **Ask Before Assuming**: If design intent is unclear, ask the user
2. **Be Specific**: Provide exact values (px, rem, hex codes)
3. **Think Mobile-First**: Always consider mobile layout first
4. **Check Accessibility**: Flag potential issues early
5. **Document Interactions**: Don't overlook hover states and animations
6. **Map to Native Components**: Prefer platform-native solutions

## Common Patterns Recognition

Learn to quickly identify these patterns:

- **Hero**: Full-width section, background image, overlaid text, CTA
- **Card Grid**: Repeating items, image + text, equal heights
- **CTA Banner**: Contrasting background, centered text, prominent button
- **Testimonial**: Quote, author info, possibly image
- **Slideshow**: Multiple items, navigation arrows, pagination dots
- **Feature List**: Icons, headings, descriptions, grid/list layout
- **Team Grid**: Photos, names, titles, bio text

For each pattern, know the typical WordPress blocks or Drupal fields needed.
