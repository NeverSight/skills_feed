---
name: generate-icon
description: This skill should be used when the user asks to "generate an icon", "create a favicon", "make an app icon", "create iOS icon", "create Android icon", "generate PWA icons", "make desktop app icon", "create Windows icon", "create macOS icon", "app store icon", "Play Store icon", "App Store icon", or needs AI-generated icons with platform-specific sizing.
---

# Generate Icon Skill

Generate professional icons for any platform using Gemini AI with automatic background removal, cropping, and multi-size export.

## Quick Start

```bash
# Favicon for website
bun run icon "modern tech startup logo letter S" --preset favicon --output ./icons/favicon

# iOS App Store icons
bun run icon "meditation app lotus flower" --preset apple-app-icon --output ./icons/ios

# Android Play Store + adaptive icons
bun run icon "fitness tracker flame icon" --preset android-app-icon --output ./icons/android

# PWA manifest icons
bun run icon "productivity app checkmark" --preset pwa --output ./icons/pwa

# macOS desktop app
bun run icon "code editor brackets symbol" --preset macos-icns --output ./icons/macos

# Windows desktop app
bun run icon "music player note icon" --preset windows-ico --output ./icons/windows

# General UI icons
bun run icon "settings gear" --preset ui-icons --output ./icons/ui
```

## Presets

| Preset | Description | Sizes | Bundle |
|--------|-------------|-------|--------|
| `apple-app-icon` | iOS/iPadOS App Store | 18 sizes (1024-20px) | No |
| `android-app-icon` | Google Play + adaptive layers | 11 sizes + foreground | No |
| `favicon` | Browser tab icons | 8 sizes + ICO | Yes (.ico) |
| `pwa` | Progressive Web App | 11 sizes + maskable | No |
| `macos-icns` | macOS desktop | 10 sizes | Yes (.icns) |
| `windows-ico` | Windows desktop | 7 sizes | Yes (.ico) |
| `ui-icons` | In-app icons | 9 sizes (512-16px) | No |

## Pipeline

1. **Generate** - Creates master icon at high resolution via Gemini
2. **Remove Background** - Uses Replicate rembg for clean edges
3. **Crop & Center** - Trims whitespace, centers on square canvas with 5% padding
4. **Resize** - Exports all preset sizes with lanczos3 interpolation
5. **Bundle** - Creates ICO/ICNS bundles where needed

## Options

```
bun run icon "prompt" --preset <name> --output <dir> [options]

Required:
  --preset <name>       Platform preset (see table above)
  --output <dir>        Output directory

Optional:
  --input <image>       Reference image for style guidance
  --master-image <path> Use existing master instead of generating
  --skip-generate       Skip AI generation (requires --master-image)
  --skip-remove-bg      Skip background removal
  --bg-color <hex>      Background color for non-transparent presets
```

## Examples

### Using a reference image
```bash
bun run icon "clean app icon version" --preset pwa --input ./existing-logo.png --output ./icons
```

### Using an existing master
```bash
bun run icon "" --preset ui-icons --master-image ./my-icon.png --skip-generate --output ./icons
```

### iOS with custom background color
```bash
bun run icon "weather app sun" --preset apple-app-icon --bg-color "#0066CC" --output ./icons/ios
```

## Icon Design Tips

**DO:**
- Simple, bold, recognizable silhouette
- Single focal point
- High contrast
- Clean edges
- Works at 16x16px

**DON'T:**
- Fine details that disappear at small sizes
- Text (unreadable at icon sizes)
- Complex gradients (banding issues)
- Multiple competing elements
- Photos or realistic images

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes | Google AI Studio API key |
| `REPLICATE_API_TOKEN` | Yes | Replicate API token for background removal |

## Output Structure

```
output/
├── master-raw.png        # Original generated image
├── master-nobg.png       # Background removed
├── master-cropped.png    # Cropped and centered
├── master-final.png      # With background (iOS only)
├── favicon.ico           # ICO bundle (favicon preset)
├── AppIcon.icns          # ICNS bundle (macos preset)
├── icon-512.png          # Size variants...
├── icon-256.png
└── ...
```

## Context Discipline

**Do not read generated icon images back into context.** The script outputs file paths for all generated sizes. Ask the user to visually inspect the results. Icon sets produce many files across multiple sizes - reading them back would quickly exhaust the context window.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "GEMINI_API_KEY not set" | Export your API key: `export GEMINI_API_KEY=your-key` |
| "REPLICATE_API_TOKEN not set" | Export your token: `export REPLICATE_API_TOKEN=your-token` |
| ICO not generated | Install ImageMagick: `brew install imagemagick` |
| ICNS not generated | Only works on macOS (requires iconutil) |
| Background not removed cleanly | Try a simpler prompt with solid background |
| Icon too complex | Simplify prompt, avoid "detailed" or "realistic" |
