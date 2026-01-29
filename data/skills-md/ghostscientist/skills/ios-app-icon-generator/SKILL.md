---
name: ios-app-icon-generator
description: Generates a complete iOS app icon set with all required sizes. Use when asked to create an app icon, design an iOS icon, generate app store artwork, or make an icon for an iPhone/iPad app. Follows a philosophy-first approach - first defining the visual identity and concept, then producing production-ready icons.
---

# iOS App Icon Generator

Create beautiful, production-ready iOS app icons through a two-phase creative process.

## Phase 1: Visual Philosophy

Before drawing anything, develop a 2-3 paragraph **Icon Philosophy** that articulates:

- **Core concept**: What single idea or feeling should the icon convey?
- **Visual metaphor**: What shape, object, or abstraction represents the app's purpose?
- **Color psychology**: What palette evokes the right emotional response?
- **Silhouette test**: Will it be recognizable as a tiny black shape?

Write this philosophy out. It guides every design decision.

### Design Principles

Icons that work follow these rules:

- **Simplicity**: One focal element. No more than 2-3 colors. No text (illegible at small sizes).
- **Distinctiveness**: Must stand out in a grid of 30 other icons. Avoid generic symbols (gears, checkmarks, clouds).
- **Scalability**: The 16x16 notification icon must read as clearly as the 1024x1024 App Store version.
- **No photography**: Apple's guidelines discourage photos. Use illustration, geometry, or abstract forms.
- **Optical balance**: Center of visual weight, not geometric center. Curves feel heavier than straight lines.

## Phase 2: Icon Generation

Generate the icon as a **self-contained HTML file** with embedded SVG that:

1. Renders the icon design at 1024x1024 (the master size)
2. Includes iOS-style rounded corners (superellipse, not CSS border-radius)
3. Shows a preview grid of all sizes to verify readability
4. Provides a download mechanism for each size

### Required Sizes

Generate all iOS app icon sizes:

| Size | Purpose |
|------|---------|
| 1024x1024 | App Store |
| 180x180 | iPhone (@3x) |
| 167x167 | iPad Pro (@2x) |
| 152x152 | iPad (@2x) |
| 120x120 | iPhone (@2x) |
| 87x87 | Spotlight (@3x) |
| 80x80 | Spotlight (@2x) |
| 76x76 | iPad (@1x) |
| 60x60 | iPhone (@1x) |
| 58x58 | Settings (@2x) |
| 40x40 | Spotlight (@1x) |
| 29x29 | Settings (@1x) |
| 20x20 | Notification (@1x) |

### HTML Artifact Structure

```html
<!DOCTYPE html>
<html>
<head>
  <title>App Icon: [Name]</title>
  <style>
    /* Dark interface, icon grid layout, download buttons */
  </style>
</head>
<body>
  <!-- Philosophy statement -->
  <!-- Master SVG at 1024x1024 -->
  <!-- Preview grid showing all sizes -->
  <!-- Download buttons (use canvas to convert SVG → PNG) -->
  <script>
    // SVG → Canvas → PNG download logic
  </script>
</body>
</html>
```

### SVG Guidelines

- Use `viewBox="0 0 1024 1024"` for the master
- Apply the iOS squircle mask (superellipse with n≈5)
- Use gradients sparingly but effectively
- Ensure googd stroke widths scale proportionally
- Test: zoom browser to 25% - is the icon still clear?

### iOS Squircle Mask

The iOS icon shape is NOT a rounded rectangle. Use this superellipse path or approximate with:

```svg
<clipPath id="ios-squircle">
  <path d="M512,1024 C252,1024 0,772 0,512 C0,252 252,0 512,0 C772,0 1024,252 1024,512 C1024,772 772,1024 512,1024 Z" />
</clipPath>
```

Or generate programmatically with the superellipse formula: `|x/a|^n + |y/b|^n = 1` where n ≈ 5.

## Process

1. Ask about the app's purpose, name, and any existing brand colors
2. Write the Icon Philosophy
3. Describe 2-3 concept directions with rationale
4. Get user approval on a direction
5. Generate the HTML artifact with full icon set
6. Iterate based on feedback

## Quality Bar

The output should look like it belongs on a top-10 App Store chart. Every icon in that grid was crafted by a professional designer - yours should be indistinguishable from theirs.

Avoid:
- Glossy/skeuomorphic styles (outdated since iOS 7)
- Thin hairline details (disappear at small sizes)
- Overly complex illustrations
- Generic clip-art aesthetics
- Centered-circle-on-gradient laziness
