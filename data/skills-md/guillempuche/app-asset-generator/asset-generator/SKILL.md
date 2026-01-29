---
name: asset-generator
description: Generate app icons, splash screens, and adaptive icons for iOS, Android, and Web. Use when creating or updating visual assets.
---

# Asset Generator Skill

Generate complete app asset sets from a single design configuration.

## Quick Commands

| Task | Command |
|------|---------|
| Show help | `bun run dev generate --help` |
| Launch TUI | `bun run tui` |
| List Google Fonts | `bun run dev list-fonts` |
| Show platforms | `bun run dev list-platforms` |
| Dry run | `bun run dev generate --dry-run` |

## Common Tasks

### Text-based Icon

```bash
bun run dev generate \
  --fg-text "X" \
  --fg-font "Inter" \
  --fg-color "#FFFFFF" \
  --bg-color "#000000"
```

### Gradient Background

```bash
bun run dev generate \
  --bg-type gradient \
  --bg-gradient-colors "#B3D9E8,#004C6E" \
  --bg-gradient-type linear \
  --bg-gradient-angle 180 \
  --fg-text "A" \
  --fg-font "Playfair Display"
```

### Custom Scale

```bash
bun run dev generate \
  --icon-scale 0.8 \
  --splash-scale 0.3 \
  --fg-text "M"
```

### Dark Mode Variants

```bash
bun run dev generate \
  --dark-mode \
  --dark-bg-color "#1A1A1A" \
  --fg-text "D" \
  --fg-color "#FFFFFF"
```

### Specific Platforms

```bash
bun run dev generate \
  --platforms "ios,android" \
  --types "icon,adaptive" \
  --fg-text "P"
```

### JSON Output (for automation)

```bash
bun run dev generate --format json --quiet
```

## Output Structure

Assets are saved to `./assets/generated-{timestamp}/`:

- `ios/` - App icons and splash screens
- `android/` - Launcher icons, adaptive icons, splash screens
- `web/` - PWA icons and favicons
- `INSTRUCTIONS.md` - Integration guide

## Scale Guidelines

| Option | Range | Default | Best For |
|--------|-------|---------|----------|
| `--icon-scale` | 0.2-1.0 | 0.7 | 0.6-0.7 standard, 0.8-0.9 bold |
| `--splash-scale` | 0.1-0.5 | 0.25 | 0.2-0.3 standard, 0.15-0.2 minimal |
