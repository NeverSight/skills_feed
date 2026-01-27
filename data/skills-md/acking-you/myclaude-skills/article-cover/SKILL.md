---
name: article-cover
description: Generate professional article cover images as SVG files. Use when user wants to create cover/banner images for blog posts, technical articles, or documentation. Creates visually appealing covers with titles, diagrams, and tech-themed graphics.
---

# Article Cover SVG Generation

Generate professional, visually striking article cover images in SVG format for technical blogs, documentation, and articles.

## Critical Rules

1. **ViewBox Standard**: Use `viewBox="0 0 1200 630"` (social media friendly 1.91:1 ratio)

2. **Text Readability (MUST follow)**:
   - Main title: 44-48px, bold, high contrast
   - Subtitle: 28-32px, white or light color
   - Labels/tags: 14-16px
   - Never use fonts smaller than 11px

3. **Background Design**:
   - Always use gradient backgrounds (avoid flat solid colors)
   - Dark tech themes: `#0d1117` → `#161b22` (GitHub dark style)
   - Add subtle grid patterns or decorative elements for depth

4. **Visual Hierarchy**:
   - Title area: bottom 1/3 of the image (y: 420-540)
   - Diagram/illustration area: top 2/3 (y: 80-400)
   - Tags/labels: bottom edge (y: 550-600)

5. **Color Contrast**: Ensure text is readable against backgrounds
   - Light text on dark backgrounds
   - Use gradients for emphasis (orange/yellow for tech, blue/cyan for data)

## Design Patterns

### Tech Article Cover (Comparison Layout)
Best for: Performance comparisons, version upgrades, before/after scenarios

```
┌─────────────────────────────────────────────────┐
│  [Logo]                           [Badge: 100x+]│
│                                                 │
│  ┌─────────┐    VS    ┌─────────┐    ┌────────┐│
│  │ Before  │  ────►   │ Middle  │ ►  │ After  ││
│  │  ❌     │          │   ⚠     │    │   ✓    ││
│  └─────────┘          └─────────┘    └────────┘│
│                                                 │
│         Main Title (Large, Gradient)            │
│           Subtitle (Medium, White)              │
│                                                 │
│    [Tag1]  [Tag2]  [Tag3]  [Tag4]  [Tag5]      │
└─────────────────────────────────────────────────┘
```

### Tech Article Cover (Flow Layout)
Best for: Process explanations, architecture overviews

```
┌─────────────────────────────────────────────────┐
│  [Logo]                                         │
│                                                 │
│  [Input] ──► [Process Box] ──► [Output]         │
│     │            │                │             │
│     └────────────┴────────────────┘             │
│                                                 │
│         Main Title (Large, Gradient)            │
│           Subtitle (Medium, White)              │
│                                                 │
│    [Tag1]  [Tag2]  [Tag3]  [Tag4]              │
└─────────────────────────────────────────────────┘
```

## Color System

| Purpose | Background | Stroke/Text | Use Case |
|---------|------------|-------------|----------|
| Negative/Before | `#1c2128` | `#dc3545` | Problems, old version |
| Warning/Transition | `#1c2128` | `#ffcc02` | Partial solution, v1 |
| Positive/After | `#1c2128` | `#00f2fe` | Solution, new version |
| Success | `#22863a` | `#22863a` | Checkmarks, improvements |
| Accent | `#ff6b35` → `#ffcc02` | gradient | Titles, highlights |

## SVG Template

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630">
  <defs>
    <!-- Background gradient -->
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0d1117"/>
      <stop offset="100%" style="stop-color:#161b22"/>
    </linearGradient>
    <!-- Title gradient (orange/yellow for tech) -->
    <linearGradient id="titleGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#ff6b35"/>
      <stop offset="100%" style="stop-color:#ffcc02"/>
    </linearGradient>
    <!-- Glow effect for emphasis -->
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="1200" height="630" fill="url(#bgGradient)"/>

  <!-- Top accent bar -->
  <rect x="0" y="0" width="1200" height="5" fill="url(#titleGradient)"/>

  <!-- Logo area (top-left) -->
  <g transform="translate(50, 30)">
    <!-- Logo elements here -->
  </g>

  <!-- Main illustration area (center) -->
  <g transform="translate(600, 220)">
    <!-- Diagram/comparison elements here -->
  </g>

  <!-- Main title -->
  <text x="600" y="450" fill="url(#titleGradient)"
        font-family="Arial, sans-serif" font-size="46"
        text-anchor="middle" font-weight="bold">
    Article Title Here
  </text>

  <!-- Subtitle -->
  <text x="600" y="510" fill="#fff"
        font-family="Arial, sans-serif" font-size="28"
        text-anchor="middle">
    Subtitle or Description
  </text>

  <!-- Bottom tags -->
  <g transform="translate(600, 580)">
    <!-- Tag pills here -->
  </g>
</svg>
```

## Element Templates

### Comparison Box (with status icon)
```svg
<g transform="translate(X, Y)">
  <rect x="0" y="0" width="300" height="180" rx="10"
        fill="#1c2128" stroke="#COLOR" stroke-width="2"/>
  <text x="150" y="30" fill="#COLOR" font-size="17"
        text-anchor="middle" font-weight="bold">ICON Title</text>
  <!-- Content here -->
</g>
```

Status icons: `❌` (negative), `⚠` (warning), `✓` (positive)

### Performance Badge
```svg
<g transform="translate(X, Y)">
  <rect x="-60" y="-25" width="140" height="50" rx="25"
        fill="#00f2fe" opacity="0.15" stroke="#00f2fe" stroke-width="2"/>
  <text x="10" y="8" fill="#00f2fe" font-size="28"
        text-anchor="middle" font-weight="bold">100x+</text>
</g>
```

### Tag Pill
```svg
<rect x="X" y="-22" width="100" height="36" rx="18"
      fill="transparent" stroke="#COLOR" stroke-width="2"/>
<text x="X+50" y="4" fill="#COLOR" font-size="14"
      text-anchor="middle" font-weight="bold">TagName</text>
```

### Arrow (with label)
```svg
<g transform="translate(X, Y)">
  <path d="M 0 0 L 35 0" stroke="#COLOR" stroke-width="3" fill="none"/>
  <polygon points="35,0 25,-6 25,6" fill="#COLOR"/>
</g>
```

### Data Bar (for showing proportions)
```svg
<rect x="X" y="Y" width="WIDTH" height="12" rx="2"
      fill="#COLOR" opacity="0.8"/>
```

## Workflow

1. **Understand the article**: What's the main topic? Is it a comparison, tutorial, or overview?

2. **Choose layout pattern**:
   - Comparison → Use 2-3 column comparison layout
   - Process/Flow → Use flow diagram layout
   - Single concept → Use centered illustration

3. **Extract key elements**:
   - Main title (keep concise, 10-15 Chinese chars or 5-8 English words)
   - Subtitle (descriptive, can be longer)
   - Key metrics (performance numbers, version info)
   - Tags (3-5 relevant keywords)

4. **Design the illustration**:
   - Use simple shapes (rectangles, arrows)
   - Show the core concept visually
   - Use color to differentiate states/versions

5. **Generate SVG**: Follow the template, ensure all text is readable

## Output

- Filename: `{article-slug}-cover.svg`
- Location: Same directory as the article or `assets/` folder
- Tell user: Can be opened in browser, converted to PNG via Inkscape/browser screenshot

## Tips

- **Chinese text**: Use `font-family="Arial, sans-serif"` which has good CJK support
- **Emphasis**: Use `filter="url(#glow)"` sparingly on key elements
- **Spacing**: Keep 20-40px padding around text elements
- **Testing**: Open SVG in browser to verify rendering before finalizing
