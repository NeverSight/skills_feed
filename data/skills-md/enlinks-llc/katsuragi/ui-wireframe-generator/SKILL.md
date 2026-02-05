---
name: ui-wireframe-generator
description: This skill generates text-based UI wireframes using .kui file syntax. Use when creating wireframes, mockups, or UI layout diagrams. The skill converts .kui files to SVG/PNG images via the katsuragi CLI tool.
---

# Katsuragi UI Wireframe Generator

Generate text-based UI wireframes using `.kui` file syntax. Katsuragi converts simple declarative files into SVG/PNG images, serving as a communication medium for UI discussions.

**GitHub**: https://github.com/enlinks-llc/katsuragi

## Install

```bash
# Install this skill
npx skills add enlinks-llc/katsuragi

# Install katsuragi CLI
npm install -g katsuragi
# or use directly with npx
npx ktr input.kui -o output.png
```

## Why Katsuragi?

- **LLM-friendly**: Text-based format that AI agents can read, write, and iterate on
- **Human-readable**: Simple syntax anyone can understand without design tools
- **Git-friendly**: Version control your wireframes alongside code
- **Zero design skills needed**: Grid-based layout handles positioning automatically
- **Instant output**: Generate PNG/SVG in seconds via CLI

## Use Cases

- **Developer ↔ Stakeholder communication**: Show rough UI ideas without Figma
- **AI-assisted UI development**: Let LLMs propose layouts in `.kui` format
- **Quick prototyping**: Sketch screen layouts before writing any frontend code
- **Documentation**: Embed wireframes in technical specs and PRs
- **Design discussions**: Iterate on layouts through text diffs

## When to Use

- Creating quick UI wireframes or mockups
- Discussing UI layouts with stakeholders
- Generating visual representations of UI designs
- Documenting UI structures in a text-based format

## Quick Start

To generate a wireframe:

```bash
npx ktr input.kui -o output.png  # PNG output
npx ktr input.kui -o output.svg  # SVG output
```

## File Structure

Every `.kui` file follows this structure:

```kui
ratio: 16:9              // Canvas aspect ratio
grid: 4x3                // Grid dimensions (columns x rows)
gap: 8                   // Space between cells (optional)
padding: 16              // Canvas padding (optional)
colors: { name: "#hex" } // Color definitions (optional)

// Cell definitions
A1..B2: { type: component, property: value }
```

## Grid System

Cells use Excel-style notation:
- **Single cell**: `A1` (column A, row 1)
- **Range**: `A1..B2` (merges cells from A1 to B2)
- **Columns**: A, B, C, D... (left to right)
- **Rows**: 1, 2, 3... (top to bottom)

Grid divides canvas equally. A 4x3 grid creates 4 equal columns and 3 equal rows.

## Components

| Type | Purpose | Key Properties |
|------|---------|----------------|
| `txt` | Text label | `value`, `align` |
| `box` | Empty container | `bg`, `border` |
| `btn` | Button | `value`, `bg` |
| `input` | Form input | `label` |
| `img` | Image placeholder | `alt` |

### Common Properties

| Property | Values | Default |
|----------|--------|---------|
| `align` | `left`, `center`, `right` | `left` |
| `bg` | Color (hex, name, or `$ref`) | `#e0e0e0` |
| `border` | Color (hex, name, or `$ref`) | none |
| `padding` | Number (pixels) | `0` |

## Color System

Define reusable colors in the header:

```kui
colors: { primary: "#3B82F6", danger: "#EF4444", accent: "orange" }

// Use with $ prefix
D3: { type: btn, value: "Submit", bg: $primary }
```

Supported formats: `#RGB`, `#RRGGBB`, CSS color names

## Output Specifications

- **Longest edge**: Fixed at 1280px
- **Aspect ratios**: `16:9` → 1280×720, `4:3` → 1280×960, `9:16` → 720×1280

## Syntax Reference

For complete syntax details, see `references/syntax.md`.

## Examples

### Login Form

```kui
ratio: 16:9
grid: 4x3
gap: 8
padding: 16
colors: { primary: "#3B82F6" }

// Header
A1..D1: { type: txt, value: "Login", align: center }

// Form fields
A2..D2: { type: input, label: "Email" }
A3..C3: { type: input, label: "Password" }

// Submit button
D3: { type: btn, value: "Login", bg: $primary }
```

### Dashboard Layout

```kui
ratio: 16:9
grid: 4x3
gap: 8
padding: 16
colors: { secondary: "#f5f5f5", outline: "#333" }

// Navigation
A1: { type: img, alt: "Logo" }
B1..C1: { type: txt, value: "Dashboard", align: center }
D1: { type: btn, value: "Logout", border: $outline }

// Sidebar
A2..A3: { type: box, bg: $secondary }

// Main content area
B2..D2: { type: txt, value: "Welcome back!", align: left }
B3..D3: { type: box, border: $outline }
```

### Mobile Profile (Vertical)

```kui
ratio: 9:16
grid: 3x5
gap: 8
padding: 16
colors: { primary: "#3B82F6", outline: "#333" }

// Header
A1..C1: { type: txt, value: "My App", align: center }

// Profile image
A2..C2: { type: img, alt: "Profile Photo" }

// User info
A3..C3: { type: txt, value: "John Doe", align: center }

// Actions
A4..C4: { type: btn, value: "Edit Profile", bg: $primary }
A5..C5: { type: btn, value: "Settings", border: $outline }
```

## Workflow

1. **Define the canvas** - Set ratio and grid size based on target layout
2. **Plan the grid** - Sketch cell positions mentally or on paper
3. **Write .kui file** - Start with header, then define cells top-to-bottom
4. **Generate output** - Run `npx ktr file.kui -o output.png`
5. **Iterate** - Adjust grid, spacing, or components as needed

## Best Practices

- Use meaningful color names in the `colors` block
- Add comments (`//`) to organize sections
- Start with larger merged cells for main areas, then refine
- Use `gap` for clean separation between elements
- Test with both SVG and PNG to choose the best format
