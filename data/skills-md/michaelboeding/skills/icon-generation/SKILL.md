---
name: icon-generation
description: >
  Generate app icons with transparent backgrounds. Triggers include:
  "generate icon", "create icon", "make icon", "app icon", "favicon",
  "icon for", "logo icon", "icon set", "icon pack", "transparent icon"
  Creates square PNG icons with transparent backgrounds suitable for app icons, favicons, and UI elements.
---

# Icon Generation Skill

Generate professional app icons with transparent backgrounds using AI (Google Gemini).

**Output:** Square PNG with transparent background - ready for app stores, favicons, or UI.

## Quick Examples

| User Says | What Happens |
|-----------|--------------|
| "Create an icon for a music app" | Generates square PNG with transparent background |
| "Make a settings gear icon, flat style" | Flat design icon with clean lines |
| "Generate a 3D shopping cart icon" | 3D-style icon with depth and shadows |
| "I need a favicon for my blog" | Small icon optimized for web |
| "Create icon set: home, search, profile" | Batch generates multiple icons |
| "Make icons matching this style" + image | Uses reference image to match style |
| "Generate more icons like this one" | Creates consistent icon set from reference |

## Prerequisites

- `GOOGLE_API_KEY` - Required for Google Gemini image generation
  - Get your key at: https://aistudio.google.com/apikey

## Icon Styles

| Style | Description | Best For |
|-------|-------------|----------|
| **flat** | Modern flat design, solid colors, minimal shadows | iOS, Material Design, web |
| **3d** | Depth, gradients, realistic shadows | macOS, premium apps |
| **line** | Outline only, thin strokes | Minimalist UI, toolbars |
| **glyph** | Solid filled shape, single color | System icons, tab bars |
| **gradient** | Smooth color transitions | Modern app icons |
| **minimal** | Ultra-simple, essential shapes only | Professional, clean UI |

## Workflow

### Step 1: Gather Requirements (REQUIRED)

Use the `AskUserQuestion` tool for each question. Ask ONE question at a time.

**Q1: Icon Concept**
> "What should this icon represent?
>
> Examples: settings gear, shopping cart, user profile, home, music note, camera"

*Wait for response.*

**Q2: Style**
> "What **style**?
>
> - Flat (modern, solid colors)
> - 3D (depth, shadows)
> - Line (outline only)
> - Glyph (solid filled shape)
> - Gradient (color transitions)
> - Minimal (ultra-simple)"

*Wait for response.*

**Q3: Size**
> "What **size**? (can generate multiple)
>
> - 1024px (App Store, high-res)
> - 512px (Android, web)
> - 256px (desktop apps)
> - 128px (favicons, small UI)
> - All common sizes"

*Wait for response.*

**Q4: Reference Image (Optional but important for icon sets)**
> "Do you have a **reference image** to match the style?
>
> - Yes, I have an existing icon to match
> - No, generate fresh style"

*If yes, ask for the image path. Wait for response.*

**Q5: Colors (Optional)**
> "Any **color preferences**?
>
> - Let AI choose based on concept
> - Specific colors (e.g., blue and white)
> - Monochrome (single color + transparency)
> - Match brand colors"

*Wait for response.*

**Q6: Output Format**
> "What **file format**?
>
> - PNG (transparency, recommended)
> - JPEG (smaller file, no transparency)
> - WebP (modern format, good compression)"

*Wait for response.*

**Q7: Background Removal Method (for PNG/WebP)**
> "How should we remove the background?
>
> - Built-in (fast, may have minor artifacts)
> - Rembg (AI-based, high quality, runs locally)
> - None (keep white background from generation)"

*Wait for response.*

### Step 2: Craft the Prompt

Transform user request into an icon-specific prompt:

**Template:**
```
A [STYLE] style icon of [CONCEPT] on a transparent background.
Square format, centered, clean edges, suitable for app icon.
[COLOR PREFERENCES]. Simple, recognizable, professional.
```

**Example transformations:**
- User: "music app icon"
- Enhanced: "A flat style icon of a musical note on a transparent background. Square format, centered, clean edges, suitable for app icon. Vibrant purple and pink gradient. Simple, recognizable, professional design with modern aesthetic."

- User: "settings gear, minimal"
- Enhanced: "A minimal style icon of a settings gear on a transparent background. Square format, centered, clean edges. Monochrome gray. Ultra-simple design, essential shapes only, no extra details."

### Step 3: Generate the Icon

Execute the script:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/icon-generation/scripts/icon_generator.py \
  --prompt "your enhanced prompt" \
  --style "flat" \
  --size 1024 \
  --output "/path/to/icon.png"
```

**With multiple sizes:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/icon-generation/scripts/icon_generator.py \
  --prompt "your enhanced prompt" \
  --style "flat" \
  --size 1024 512 256 128 \
  --output "/path/to/icon"
```
This generates: `icon_1024.png`, `icon_512.png`, `icon_256.png`, `icon_128.png`

**Batch generation (multiple icons):**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/icon-generation/scripts/icon_generator.py \
  --batch '["home", "search", "profile", "settings"]' \
  --style "flat" \
  --size 512 \
  --output "/path/to/icons"
```
This generates: `home_512.png`, `search_512.png`, `profile_512.png`, `settings_512.png`

### Step 4: Deliver the Result

1. Show the generated icon(s) to the user
2. Provide the prompt used
3. Offer to:
   - Generate different sizes
   - Try a different style
   - Create variations
   - Generate as ICO (favicon format)

## Script Parameters

| Parameter | Short | Description | Default |
|-----------|-------|-------------|---------|
| `--prompt` | `-p` | Icon description | Required |
| `--style` | `-s` | Icon style preset | flat |
| `--size` | `-z` | Size(s) in pixels | 512 (or auto from reference) |
| `--format` | `-f` | Output format (png, jpeg, webp) | png |
| `--bg-removal` | `--bg` | Background removal method (builtin, rembg, none) | builtin |
| `--output` | `-o` | Output path | auto-generated |
| `--batch` | `-b` | JSON array of concepts | None |
| `--colors` | `-c` | Color preferences | AI choice |
| `--reference` | `-r` | Reference image(s) for style matching | None |

## Background Removal Methods

This skill uses the **background-remove** skill for transparent background generation.

| Method | Description | Best For |
|--------|-------------|----------|
| **builtin** | Fast white-to-transparent conversion | Quick iterations, most icons |
| **rembg** | AI-based removal using U2-Net model | High-quality results, complex backgrounds |
| **none** | Keeps the white background as-is | JPEG output, manual post-processing |

### Requirements

See the [background-remove skill](../background-remove/SKILL.md) for installation instructions.

```bash
# Install rembg for AI-based background removal
pip install rembg

# Or with GPU acceleration (requires CUDA)
pip install rembg[gpu]
```

## Style Prompt Modifiers

The script automatically adds these style-specific prompt modifiers:

| Style | Modifier Added |
|-------|----------------|
| flat | "flat design, solid colors, no gradients, minimal shadows, clean vector style" |
| 3d | "3D style, depth, soft shadows, subtle gradients, professional rendering" |
| line | "line art, outline only, thin consistent strokes, no fill, minimalist" |
| glyph | "solid filled shape, single color, bold silhouette, high contrast" |
| gradient | "smooth gradient colors, modern vibrant transitions, glossy finish" |
| minimal | "ultra-minimal, essential shapes only, maximum simplicity, geometric" |

## Common Icon Sizes

| Size | Use Case |
|------|----------|
| 1024px | iOS App Store, high-resolution displays |
| 512px | Android Play Store, macOS apps |
| 256px | Windows apps, desktop shortcuts |
| 192px | Android launcher icons |
| 180px | iOS home screen |
| 128px | Favicons (high-res), small UI |
| 64px | Toolbar icons |
| 32px | Standard favicon |
| 16px | Smallest favicon |

## Error Handling

**Missing API key:**
```
Error: GOOGLE_API_KEY not set. Get your key at https://aistudio.google.com/apikey
```

**Generation failed:**
- Retry with simpler prompt
- Check if concept is clear and recognizable
- Ensure style is appropriate for the concept

**Non-transparent output:**
- The script explicitly requests transparent background
- If still not transparent, try adding "isolated on transparent" to prompt
- For complex concepts, results may vary

## Reference Image Support

Use reference images to create consistent icon sets. When you provide a reference, the AI will match:
- Visual style and design language
- Line weight and stroke thickness
- Color palette and shading
- Level of detail and complexity
- Overall proportions and spacing

### When to Use Reference Images

| Scenario | Use Reference? |
|----------|----------------|
| Creating multiple icons for same app | Yes - ensures consistency |
| Matching existing brand icons | Yes - maintains brand identity |
| Adding to existing icon set | Yes - blends seamlessly |
| Single standalone icon | Optional - fresh style is fine |
| Exploring different styles | No - let AI be creative |

### Reference Image Examples

**Single icon matching existing style:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/icon-generation/scripts/icon_generator.py \
  -p "settings gear" \
  -r /path/to/existing_icon.png \
  -z 512
```

**Icon set with consistent style:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/icon-generation/scripts/icon_generator.py \
  -b '["home", "search", "profile", "settings", "notifications"]' \
  -r /path/to/brand_icon.png \
  -z 512 \
  -o "app_icons"
```

**Multiple reference images (up to 14):**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/icon-generation/scripts/icon_generator.py \
  -p "calendar" \
  -r /path/to/icon1.png \
  -r /path/to/icon2.png \
  -z 512
```

## Tips for Best Results

1. **Be specific about the concept**: "shopping cart" is better than "e-commerce"
2. **Match style to platform**: Flat for iOS/Android, 3D for macOS
3. **Keep it simple**: Icons should be recognizable at small sizes
4. **Test at small sizes**: Generate 32px to ensure readability
5. **Use consistent style**: For icon sets, use same style for all icons
6. **Use reference images**: For icon sets, always use a reference to ensure consistency

## Examples

### App Icon
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/icon-generation/scripts/icon_generator.py \
  -p "camera with colorful lens" \
  -s gradient \
  -z 1024 512 256 \
  -o "camera_icon"
```

### Favicon
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/icon-generation/scripts/icon_generator.py \
  -p "letter B for blog" \
  -s minimal \
  -z 128 32 16 \
  -o "favicon"
```

### Icon Set
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/icon-generation/scripts/icon_generator.py \
  -b '["home", "search", "notifications", "profile", "settings"]' \
  -s flat \
  -z 512 \
  -o "app_icons"
```

### High-Quality Background Removal (Rembg)
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/icon-generation/scripts/icon_generator.py \
  -p "detailed gear with shadows" \
  -s 3d \
  -z 512 \
  --bg rembg \
  -o "gear_icon"
```

### WebP Format with Built-in Background Removal
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/icon-generation/scripts/icon_generator.py \
  -p "lightning bolt" \
  -s gradient \
  -z 512 \
  -f webp \
  -o "bolt_icon"
```
