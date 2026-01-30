---
name: aesthetic
description: Create aesthetically beautiful interfaces following proven design principles. Use when building UI/UX, analyzing designs from inspiration sites, generating design images, implementing visual hierarchy and color theory, adding micro-interactions, or creating design documentation. Integrate localized specialized skills (chrome-devtools, ImageMagick) with native vision intelligence to achieve premium aesthetic standards.
---

# Aesthetic

Create aesthetically beautiful interfaces by following proven design principles and systematic workflows.

## When to Use This Skill

Use when:

- Building or designing user interfaces
- Analyzing designs from inspiration websites (Dribbble, Mobbin, Behance)
- Generating design images and evaluating aesthetic quality using vision intelligence
- Implementing visual hierarchy, typography, color theory
- Adding micro-interactions and animations
- Creating design documentation and style guides
- Need guidance on accessibility and design systems

## Core Framework: Four-Stage Approach

### 1. BEAUTIFUL: Understanding Aesthetics

Study existing designs, identify patterns, extract principles. AI lacks innate aesthetic sense—standards must come from analyzing high-quality examples and aligning with market tastes.

**Reference**: [`references/design-principles.md`](references/design-principles.md) - Visual hierarchy, typography, color theory, white space principles.

### 2. RIGHT: Ensuring Functionality

Beautiful designs lacking usability are worthless. Study design systems, component architecture, accessibility requirements.

**Reference**: [`references/design-principles.md`](references/design-principles.md) - Design systems, component libraries, WCAG accessibility standards.

### 3. SATISFYING: Micro-Interactions

Incorporate subtle animations with appropriate timing (150-300ms), easing curves (ease-out for entry, ease-in for exit), sequential delays.

**Reference**: [`references/micro-interactions.md`](references/micro-interactions.md) - Duration guidelines, easing curves, performance optimization.

### 4. PEAK: Storytelling Through Design

Elevate with narrative elements—parallax effects, particle systems, thematic consistency. Use restraint: "too much of anything isn't good."

**Reference**: [`references/storytelling-design.md`](references/storytelling-design.md) - Narrative elements, scroll-based storytelling, interactive techniques.

## Workflows

### Workflow 1: Capture & Analyze Inspiration

**Purpose**: Extract design guidelines from inspiration websites.

**Steps**:

1. Browse inspiration sites (Dribbble, Mobbin, Behance, Awwwards)
2. Use the **chrome-devtools** skill to capture full-screen screenshots
3. Use your **native vision capabilities** to analyze the results, prioritizing skill-based insights to extract:
   - Design style (Minimalism, Glassmorphism, Neo-brutalism, etc.)
   - Layout structure & grid systems
   - Typography system & hierarchy
     **IMPORTANT:** Try to predict the font name (Google Fonts) and font size in the given screenshot, don't just use Inter or Poppins.
   - Color palette with hex codes
   - Visual hierarchy techniques
   - Component patterns & styling
   - Micro-interactions
   - Accessibility considerations
   - Overall aesthetic quality rating (1-10)
4. Document findings in project design guidelines using templates

### Workflow 2: Generate & Iterate Design Images

**Purpose**: Create aesthetically pleasing design images through iteration.

**Steps**:

1. Define design prompt with: style, colors, typography, audience, animation specs
2. Use available **image generation tools** (e.g., `generate_image`) to generate design images.
3. Use your **native vision capabilities** to analyze output images and evaluate aesthetic quality.
4. If score < 7/10 or fails professional standards:
   - Identify specific weaknesses (color, typography, layout, spacing, hierarchy)
   - Refine prompt with improvements
   - Regenerate using available tools or use the `ImageMagick` skill to refine outputs (resize, crop, filters, composition).
5. Repeat until aesthetic standards met (score ≥ 7/10)
6. Document final design decisions using templates

## Design Documentation

### Create Design Guidelines

Use [`assets/design-guideline-template.md`](assets/design-guideline-template.md) to document:

- Color patterns & psychology
- Typography system & hierarchy
- Layout principles & spacing
- Component styling standards
- Accessibility considerations
- Design highlights & rationale

Save in project `./docs/design-guideline.md`.

### Create Design Story

Use [`assets/design-story-template.md`](assets/design-story-template.md) to document:

- Narrative elements & themes
- Emotional journey
- User journey & peak moments
- Design decision rationale

Save in project `./docs/design-story.md`.

## Resources & Integration

### Related Skills

- **Multimodal Intelligence**: Analyze documents, screenshots & videos, generate design images, and evaluate aesthetic quality.
- **chrome-devtools**: Capture high-quality screenshots from inspiration websites for analysis.
- **media-processing**: Refine generated images using specialized skills (FFmpeg for video, ImageMagick for images).
- **ui-styling**: Implement designs with semantic HTML/CSS or framework components.
- **web-frameworks**: Build with modern frameworks (Next.js, Vite, etc.).

### Reference Documentation

**References**: [`references/design-resources.md`](references/design-resources.md) - Inspiration platforms, design systems, AI tools, and development strategies.

## Key Principles

1. Aesthetic standards come from humans, not AI—study quality examples
2. Iterate based on analysis—never settle for first output
3. Balance beauty with functionality and accessibility
4. Document decisions for consistency across development
5. Use progressive disclosure in design—reveal complexity gradually
6. Always evaluate aesthetic quality objectively (score ≥ 7/10)
