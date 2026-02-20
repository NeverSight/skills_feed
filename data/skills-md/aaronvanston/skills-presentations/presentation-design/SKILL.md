---
name: presentation-design
description: Visual design guidance for bold, minimal presentations. Provides layout patterns, typography hierarchy, color specifications, and slide composition rules. Use when asking "how should this slide look?", "design guidance for...", "what layout for this slide?", or when translating content into visual structure for a presentation.
---

# Presentation Design

Visual design guidance for bold, minimal presentations optimized for live presenting.

## Core Style

**Theme:** Dark-first, high contrast, minimal (light mode supported)
**Feel:** Modern, confident, tech-forward

| Element | Specification |
|---------|---------------|
| Background | Black (#000000) or near-black; light mode: #fafafa |
| Primary text | White (#FFFFFF); light mode: #09090b |
| Secondary text | Gray (#9CA3AF) |
| Accents | Section-specific colors (see below) |
| Typography | Sans-serif (e.g. Geist Sans), **light weights** at large sizes |
| Letter spacing | Tight (-0.035em to -0.015em) |

## Typography Hierarchy

Impact comes from **scale, not weight**. Use light/regular weights (400-600) at massive sizes.

```
SECTION LABEL     Small caps, section color, tracked wide
                  Example: "THE PROBLEM" | "WHAT WORKS"

Headline          Massive, primary color, light weight (400-500)
                  Fluid sizing via container queries
                  1-5 words per line typical

Subtitle          Smaller, secondary/muted color, regular weight
                  1-2 lines maximum

Body/Bullets      Medium size, primary or secondary color
                  Bold lead-ins (600 weight) when used
```

### Text Contrast Hierarchy

Use 4 levels of contrast to create depth:

| Level | Purpose | Example |
|-------|---------|---------|
| Primary | Headlines, key content | White / #FFFFFF |
| Secondary | Subtitles, supporting text | Light gray |
| Muted | Labels, metadata | Medium gray |
| Faint | Background elements | Dark gray |

## Section Colors

Each major section of a presentation gets its own accent color. This reinforces structure and helps the audience track where they are.

| Color | Hex (dark) | Typical use |
|-------|------------|-------------|
| Teal | #14b8a6 | Opening, framing, recap |
| Red | #f87171 | Problems, challenges, tension |
| Purple | #a78bfa | Solutions, features, tools |
| Amber | #fbbf24 | Data, reality checks, caveats |
| Green | #34d399 | Best practices, what works |
| Blue | #60a5fa | Technical, implementation |
| Pink | #f472b6 | Highlights, special callouts |

Section colors appear in: section labels, gradient backgrounds, progress bars, and accent elements.

## Layout Patterns

### Full Statement (most common)
```
┌─────────────────────────────────────────┐
│ SECTION LABEL                           │
│                                         │
│ Massive                                 │
│ Headline                                │
│ Here                                    │
│                                         │
│ Subtitle text in muted color            │
│                                 [ref] ↗ │
└─────────────────────────────────────────┘
```

### Big Statement (maximum impact)
```
┌─────────────────────────────────────────┐
│ SECTION LABEL                           │
│                                         │
│                                         │
│       Even Bigger                       │
│       Statement                         │
│                                         │
│                                         │
└─────────────────────────────────────────┘
```

### Split Layout
```
┌─────────────────────────────────────────┐
│ SECTION LABEL                           │
│                                         │
│ Headline        │  • Point one          │
│ Here            │  • Point two          │
│                 │  • Point three        │
│ Subtitle        │  • Point four         │
└─────────────────────────────────────────┘
```

### Section Divider (with gradient)
```
┌────────────────────┬────────────────────┐
│                    │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
│ Section            │▓▓▓ Gradient ▓▓▓▓▓▓▓│
│ Title              │▓▓▓ Background ▓▓▓▓▓│
│                    │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
│ Subtitle           │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
└────────────────────┴────────────────────┘
```

### Code Slide
```
┌─────────────────────────────────────────┐
│ SECTION LABEL                           │
│ Headline                                │
│ Subtitle                                │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ // syntax-highlighted code block    │ │
│ │ const result = await generate()     │ │
│ │                                     │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### Data/Metrics
```
┌─────────────────────────────────────────┐
│        ┌────────┐ ┌────────┐ ┌────────┐ │
│        │  $10M  │ │  ~10%  │ │  NPS   │ │
│        │  ARR   │ │ GROWTH │ │   90   │ │
│        └────────┘ └────────┘ └────────┘ │
│ SECTION LABEL                           │
│ Headline                                │
│ Subtitle                                │
└─────────────────────────────────────────┘
```

### People/Photos Grid
```
┌─────────────────────────────────────────┐
│ Headline                                │
│ Subtitle                                │
│                                         │
│ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐        │
│ │photo│ │photo│ │photo│ │photo│        │
│ │Name │ │Name │ │Name │ │Name │        │
│ │TITLE│ │TITLE│ │TITLE│ │TITLE│        │
│ └─────┘ └─────┘ └─────┘ └─────┘        │
│                                         │
│ Photo style: Rounded, B&W or consistent │
└─────────────────────────────────────────┘
```

## Slide Type → Layout Mapping

| Slide Type | Layout |
|------------|--------|
| Title | Full statement, centered |
| Section divider | Split with gradient, section color |
| Statement | Full statement, left-aligned |
| Big statement | Big statement, maximum scale |
| Question | Full statement, centered |
| Goals/Agenda | Split layout, bullets right |
| Data | Metrics boxes top |
| Code | Headline + syntax-highlighted block |
| Quote | Centered, large quotation marks |
| People | Photos grid |
| Recap | Split layout, labeled bullets |
| Resources | Grouped reference links by section |
| Next steps | Timeline or labeled bullets |

## Embedded Content

Slides can embed rich media alongside headlines:

- **Code blocks** — syntax-highlighted, dark surface background
- **Terminal output** — monospace with ANSI color support
- **Tweet cards** — styled quote cards with avatar and attribution
- **Video previews** — thumbnail with play button
- **Article previews** — link cards with title and description

## Visual Elements

- **Section labels:** Top-left, uppercase, section color
- **Progress bar:** Bottom edge, section color, thin (3px)
- **References:** Bottom footer with clickable URLs
- **Gradients:** Aurora-style background effects using section color
- **Icons:** Simple line icons, white or accent color, used sparingly

## Things to Avoid

- Dense paragraphs of text
- More than 4-5 bullet points
- Clip art or stock imagery
- Heavy font weights for headlines (use scale instead)
- Multiple competing focal points
- Animation for animation's sake
