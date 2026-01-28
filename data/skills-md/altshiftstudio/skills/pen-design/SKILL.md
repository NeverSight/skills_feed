---
name: pen-design
description: Guide for working with Pencil (.pen) design files. Use this skill for reading, creating, or modifying UI layouts, typography, or styling in .pen design files.
---

# PEN Design Format

Work with .pen design files efficiently.

## Quick Reference

### Root Structure
```json
{
  "version": "2.6",
  "children": [...],     // Design elements
  "themes": {...},       // Theme definitions (e.g., Light/Dark)
  "variables": {...}     // Design tokens
}
```

### Element Types

| Type | Purpose | Key Properties |
|------|---------|----------------|
| `frame` | Container/layout | `layout`, `children`, `gap`, `padding`, `reusable` |
| `text` | Typography | `content`, `fontFamily`, `fontSize`, `fontWeight` |
| `rectangle` | Basic shape | `width`, `height`, `fill`, `cornerRadius` |
| `path` | Vector graphics | `geometry` (SVG path data) |
| `image` | Raster graphics | `url`, `mode` |
| `ref` | Component instance | `ref` (source ID), `descendants` (overrides) |
| `icon_font` | Icon | `iconFontName`, `iconFontFamily` (e.g., "lucide") |
| `prompt` | AI generation | `model`, `content` |

### Token System

Tokens use `$--` prefix:
- **Colors**: `$--primary`, `$--foreground`, `$--background`, `$--border`
- **Semantic**: `$--color-success`, `$--color-warning`, `$--color-error`
- **Fonts**: `$--font-primary`, `$--font-secondary`
- **Radii**: `$--radius-none`, `$--radius-m`, `$--radius-pill`

### Layout

| Property | Values |
|----------|--------|
| `layout` | `"none"` (absolute), `"horizontal"`, `"vertical"` |
| `justifyContent` | `start`, `center`, `end`, `space_between` |
| `alignItems` | `start`, `center`, `end`, `stretch` |

### Sizing
- Fixed: `360`
- Flex: `"fill_container"` or `"fill_container(360)"`
- Fit: `"fit_content"` or `"fit_content(717)"`

## Common Patterns

### For detailed patterns and examples
See [references/patterns.md](references/patterns.md)

### For complete JSON schema
See [references/schema.json](references/schema.json)

## Manipulation Guidelines

1. **Generate unique IDs** - 5 alphanumeric chars (e.g., `"xCEfn"`)
2. **Use tokens** - Prefer `$--primary` over hardcoded colors
3. **Component naming** - `Category/Variant` (e.g., `"Button/Large/Primary"`)
4. **Reusable components** - Add `"reusable": true` to source, use `ref` for instances
5. **Override properties** - Use `descendants` object keyed by child ID
