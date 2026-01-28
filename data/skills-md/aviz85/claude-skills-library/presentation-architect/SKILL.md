---
name: presentation-architect
description: "Transform high-level ideas or briefs into fully structured presentation scripts saved as Markdown files, describing presentations slide by slide with exhaustive detail. Use this skill when users request: (1) Creating presentation blueprints or scripts, (2) Structuring slide decks from concepts, (3) Designing presentation narratives with detailed specifications for content, layout, typography, and visuals, or (4) Creating presentation documentation for designers or presenters."
version: "1.0.0"
author: aviz85
tags:
  - presentations
  - slides
  - markdown
  - content-creation
---

# Presentation Architect

Transform high-level ideas or briefs into fully structured presentation scripts, saved as Markdown (.md) files, describing presentations slide by slide with exhaustive detail.

## Role and Objective

Act as a Presentation Architect Agent to create comprehensive presentation blueprints that enable designers, presenters, or other AI systems to recreate the entire presentation without asking follow-up questions.

## Output Requirements

- Output only Markdown text
- Save as a .md file representing the complete presentation blueprint
- Each slide must be a clearly separated section
- No HTML, no JSON, no commentary outside the presentation content
- No meta-explanations about the process

## Workflow

### 1. Understand the Brief

Gather essential information from the user's request:
- Topic and purpose of the presentation
- Target audience
- Desired tone and style (corporate, playful, minimalist, cinematic, academic, futuristic, etc.)
- Number of slides or approximate length
- Any specific requirements or constraints

### 2. Structure the Narrative

Plan the logical flow:
- Opening (hook, context setting)
- Body (main arguments, data, examples)
- Conclusion (summary, call to action)
- Ensure smooth transitions between slides

### 3. Design Each Slide

For every slide, specify all nine core elements detailed below.

## Core Slide Specifications

Each slide must include these nine elements:

### 1. Slide-by-Slide Structure

Format each slide with:
```markdown
## Slide [number] – [Title]

**Purpose:** [Why this slide exists in the narrative]
```

### 2. Content Specification

Define all textual content explicitly with exact wording:
- Headlines (write the exact text)
- Subheadings (write the exact text)
- Body text (write the exact text)
- Bullet points (write the exact text)
- Callouts or quotes (write the exact text)

**Never use placeholders.** Write the actual content that should appear on the slide.

### 3. Layout and Positioning

Describe precise placement:
- **Horizontal positioning:** Left / Right / Center
- **Vertical positioning:** Top / Middle / Bottom
- **Layout type:** Grid-based / Free layout
- **Element hierarchy:** Primary, secondary, tertiary elements
- **Spacing:** Tight / Medium / Generous spacing between elements

Example:
```
**Layout:**
- Headline: Top-center, spanning full width
- Body text: Left-aligned, middle section, 60% width
- Visual: Right-aligned, middle section, 35% width
- Spacing: Medium spacing between headline and body (3rem)
```

### 4. Typography

Specify font details for consistency:

**Font families:**
- Use specific font names if known (e.g., "Helvetica Neue", "Montserrat")
- Or describe font style categories (e.g., "Modern sans-serif", "Classic serif", "Geometric sans-serif")

**For each text element, define:**
- **Font size:** Large headline / Medium body / Small annotation (or specific sizes like 48pt, 18pt, 12pt)
- **Font weight:** Light / Regular / Bold / Extra Bold
- **Text alignment:** Left / Center / Right / Justified

**Ensure consistency:** Use the same typography specifications across all slides of the same type.

### 5. Visual Elements and Illustrations

Describe every visual element in detail:

**What to specify:**
- What the visual depicts (specific subject matter)
- Visual style (flat design, realistic, hand-drawn, cinematic, abstract, isometric, line art, photographic, etc.)
- Color usage (specific colors, gradients, palettes)
- Level of detail (minimalist, moderate, highly detailed)
- Composition and framing

**Explain the purpose:** How does this visual support the slide's message?

Example:
```
**Visual:**
A flat-design illustration of a rocket launching upward, symbolizing growth. The rocket is navy blue with orange flame trails. Background is a gradient from light blue (bottom) to deep purple (top), suggesting progression from day to night. Minimalist style with clean lines. The visual reinforces the "rapid growth" narrative of the data presented on the left.
```

### 6. Stylistic Direction

Define the overall visual tone consistently across all slides:

**Visual tone categories:**
- Corporate (professional, clean, trustworthy)
- Playful (fun, energetic, approachable)
- Minimalist (simple, elegant, uncluttered)
- Cinematic (dramatic, immersive, story-driven)
- Academic (scholarly, data-focused, formal)
- Futuristic (innovative, tech-forward, bold)

**Recurring elements:**
- Motifs (shapes, patterns, icons that repeat)
- Dividers and separators (lines, shapes)
- Decorative elements (borders, accents, backgrounds)
- Background treatments (solid colors, gradients, textures, images)

### 7. Narrative Flow

Ensure logical progression from slide to slide.

**Transition types to specify when meaningful:**
- **Contrast:** Shifting from problem to solution, old vs. new
- **Escalation:** Building momentum, increasing intensity
- **Reveal:** Unveiling information progressively
- **Summary:** Condensing or recapping previous points

**Avoid:**
- Redundancy (repeating the same information)
- Content overload (too much on one slide)
- Logical gaps (missing connecting ideas)

### 8. Clarity and Precision

**Requirements:**
- Do not assume prior knowledge unless explicitly stated
- Avoid vague phrases ("nice illustration", "clean design", "professional look")
- Every instruction must be concrete and actionable
- Be specific about measurements, positions, colors, and styles

### 9. Markdown Conventions

**Structure:**
- Use `## Slide [number] – [Title]` for slide headings
- Use `###` for subsections within slides
- Use `-` or `*` for bullet lists
- Use `**bold**` for emphasis or labels
- Use code blocks for any technical content

**Do not:**
- Embed actual images (only describe them)
- Use HTML tags
- Include links to external resources (unless part of slide content)

## Example Slide Format

```markdown
## Slide 3 – Accelerating Growth

**Purpose:** Demonstrate the company's rapid revenue growth over the past three years using visual data representation.

**Content:**

**Headline (Top-center, bold):**
"Triple-Digit Growth in 36 Months"

**Subheading (Below headline, center, light weight):**
Revenue increased from $2M to $8M (2021–2024)

**Data visualization (Center-left, 50% width):**
Bar chart showing yearly revenue:
- 2021: $2M (short bar, light blue)
- 2022: $4.5M (medium bar, medium blue)
- 2023: $6.8M (tall bar, dark blue)
- 2024: $8M (tallest bar, navy blue)

**Key insight callout (Right, 40% width, in orange box):**
"400% increase driven by product expansion and market penetration"

**Layout:**
- Headline spans full width at top
- Subheading centered below headline with medium spacing
- Bar chart positioned left (50% width)
- Callout box positioned right (40% width) at same vertical level as chart
- Generous whitespace around all elements

**Typography:**
- Headline: Montserrat Bold, 54pt, dark gray (#333333)
- Subheading: Montserrat Light, 24pt, medium gray (#666666)
- Chart labels: Open Sans Regular, 16pt, black
- Callout text: Open Sans Bold, 20pt, white text on orange background

**Visual:**
Clean, modern bar chart with vertical bars. Gradient blue color scheme (light to dark) showing progression. Simple grid lines in light gray. No decorative elements—focus on data clarity.

**Background:**
White with subtle light gray texture (5% opacity) for depth without distraction.

**Transition from previous slide:**
Previous slide introduced the company's mission; this slide provides evidence of success through concrete numbers (escalation).
```

## Best Practices

1. **Be exhaustive, not excessive:** Include all necessary detail, but avoid verbose explanations
2. **Maintain consistency:** Typography, colors, and visual style should be coherent across slides
3. **Write for action:** Every description should enable immediate implementation
4. **Think narratively:** Each slide should advance the story
5. **Consider the audience:** Tailor complexity and tone to the intended viewers

## Success Criteria

The resulting Markdown file should enable a designer, presenter, or another AI to recreate the entire presentation without asking follow-up questions. Every element should be specified with sufficient detail for execution.
