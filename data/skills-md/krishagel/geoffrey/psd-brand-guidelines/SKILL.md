---
name: psd-brand-guidelines
description: Apply Peninsula School District official brand colors, typography, and logos to artifacts
triggers:
  - "psd brand"
  - "district branding"
  - "psd colors"
  - "psd logo"
  - "peninsula school district style"
  - "brand guide"
  - "on-brand"
allowed-tools: Read, Write, Edit, Bash
version: 0.2.0
---

# PSD Brand Guidelines Skill

This skill applies Peninsula School District's official brand identity to artifacts including presentations, documents, graphics, and other materials.

## CRITICAL: Enforcement Rules

### NEVER Generate

**NEVER** use image-gen or any AI tool to generate:
- District logos or emblems
- "Peninsula School District" in stylized/logo text
- Bridge/landscape imagery meant to represent the district logo
- Any official-looking district branding elements
- District seals or official marks

**Why?** AI-generated logos are inconsistent and may hallucinate incorrect details (wrong colors, wrong name, made-up imagery). Always use actual logo files.

### ALWAYS Use Actual Files

For any branded materials:
1. Use logo files from `assets/` directory
2. Use colors from `brand-config.json`
3. Use `brand.py` utilities to select the right assets

### Programmatic Access

**Machine-readable brand data:** `brand-config.json`
**Python utilities:** `brand.py`

```bash
# Get colors
uv run brand.py colors

# Get appropriate logo path
uv run brand.py logo light wide
uv run brand.py logo dark small

# Validate prompt before image generation
uv run brand.py validate "create an infographic about enrollment"
```

### Image Generation with Brand

When generating images for PSD materials, always use the `--brand` flag:

```bash
# This validates the prompt and blocks logo generation attempts
uv run generate.py "school campus scene" campus.png --brand psd
```

## Purpose

Ensure professional and consistent use of the Peninsula School District brand across all communications. The brand reflects the stunning beauty of the Pacific Northwest and the Puget Sound region.

## Typography

### Headings & Logo Text: Josefin Sans

Modern geometric, elegant font with a vintage 1920s feel. Use **Bold** weight for district name and all headings.

- **Font:** Josefin Sans Bold
- **Source:** https://fonts.google.com/specimen/Josefin+Sans
- **Fallback:** Arial, sans-serif

### Body Text: Josefin Slab

Perfect pairing to Josefin Sans, highly legible at smaller sizes due to slab serif and typewriter-style attributes.

- **Font:** Josefin Slab
- **Source:** https://fonts.google.com/specimen/Josefin+Slab
- **Fallback:** Georgia, serif

## Color Palette

### Logo Colors (Primary)

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **Sea Glass** | #6CA18A | rgb(108, 161, 138) | Primary green, landscape elements |
| **Pacific** | #25424C | rgb(37, 66, 76) | Primary dark blue, text, headers |
| **Driftwood** | #D7CDBE | rgb(215, 205, 190) | Neutral tan, backgrounds |

### Supporting Brand Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **Cedar** | #466857 | rgb(70, 104, 87) | Dark green accent |
| **Whulge** | #346780 | rgb(52, 103, 128) | Medium blue (Coast Salish word for sound of waves) |
| **Sea Foam** | #EEEBE4 | rgb(238, 235, 228) | Light background |
| **Meadow** | #5D9068 | rgb(93, 144, 104) | Green accent |
| **Ocean** | #7396A9 | rgb(115, 150, 169) | Light blue accent |
| **Skylight** | #FFFAEC | rgb(255, 250, 236) | Off-white/cream background |

### Color Selection Guidelines

- **Light backgrounds:** Use Pacific (#25424C) or 2-color logo
- **Dark backgrounds:** Use Sea Glass (#6CA18A) or white logo
- **Neutral backgrounds:** Choose based on contrast needs
- When adding colors, choose natural, complementary colors that reflect Pacific Northwest landscape tones

## Logo Options

### Available Formats

1. **Full Landscape** - Bridge connecting peninsula landscape, district name contained within
2. **Horizontal** - For when name/tagline would be too small
3. **Emblem** - Round versions, perfect for square spaces or tight fits
4. **Stacked** - Vertical layout with name separated from brandmark

### Color Variants

- **2-color** - Sea Glass + Pacific (primary use)
- **1-color Pacific Blue** - For light backgrounds
- **1-color Sea Glass** - For medium backgrounds
- **White** - For dark backgrounds

### File Types

| Format | Use Cases |
|--------|-----------|
| **EPS (Vector)** | Professional printing, large scaling, Adobe programs |
| **PNG (Raster)** | Microsoft Office, websites, social media, email signatures |

### Logo Location

**Local assets folder:** `skills/psd-brand-guidelines/assets/`

**PNG files (19)** - for web, Office, email:
- `psd_logo-2color-{emblem,fulllandscape,stacked,horizontal,square}.png`
- `psd_logo-1color-blue-{emblem,fulllandscape,stacked,horizontal,square}.png`
- `psd_logo-1color-green-{emblem,fulllandscape,stacked,horizontal,square}.png`
- `psd_logo-white-{emblem,stacked,horizontal,square}.png`

**EPS files (19)** - for professional printing, Adobe programs:
- Same variants as PNG, with `.eps` extension

**Reference:**
- `PSD_Branding_Guide.pdf` - full brand guide document

**Google Drive source:**
- **Logos Folder ID:** `1YhjxX_pOwZJppZebIIC7QW_UHF4bvo79`
- **Brand Guide Folder:** `1ufOB6rrKDbAaH7HapdLadJzWy8ho5hTb`

## Logo Usage Rules

### Do's

- Maintain original proportions
- Ensure sufficient contrast with background
- Use appropriate color variant for background
- Use emblem/stacked logo for small sizes

### Don'ts

- Don't shrink full landscape logo below 1.5" wide (print) or 300px (web)
- Don't rotate the logo
- Don't apply effects (drop shadows, mirroring, etc.)
- Don't stretch or squish
- Don't use non-brand fonts with logo
- Don't place on backgrounds with insufficient contrast

## Applying Brand to Artifacts

### Presentations

```css
/* Title slides */
background-color: #25424C;  /* Pacific */
color: #FFFAEC;             /* Skylight */
font-family: 'Josefin Sans', Arial, sans-serif;

/* Content slides */
background-color: #EEEBE4;  /* Sea Foam */
color: #25424C;             /* Pacific */
font-family: 'Josefin Slab', Georgia, serif;

/* Accent elements */
border-color: #6CA18A;      /* Sea Glass */
```

### Documents

- **Headings:** Josefin Sans Bold, Pacific (#25424C)
- **Body:** Josefin Slab, Pacific (#25424C)
- **Links/Highlights:** Whulge (#346780)
- **Backgrounds:** Sea Foam (#EEEBE4) or Skylight (#FFFAEC)

### Digital/Web

- Primary buttons: Sea Glass (#6CA18A)
- Secondary buttons: Whulge (#346780)
- Text on light: Pacific (#25424C)
- Text on dark: Skylight (#FFFAEC)

## Brand Contact

For questions or special needs:
- **Danielle Chastaine**, Digital Media Coordinator
- chastained@psd401.net

## Quick Reference

### Programmatic API (Python)

```python
from brand import get_logo_path, get_colors, validate_prompt, get_color

# Get all colors as hex dict
colors = get_colors()  # {'seaGlass': '#6CA18A', 'pacific': '#25424C', ...}

# Get single color with metadata
color = get_color('pacific')  # {'hex': '#25424C', 'rgb': [37, 66, 76], 'usage': '...'}

# Get logo path based on context
logo = get_logo_path(background='dark', space='wide')   # Returns white-horizontal path
logo = get_logo_path(background='light', space='small')  # Returns 2color-emblem path

# Validate prompt before image generation
valid, errors = validate_prompt("create a school event banner")
if not valid:
    print(errors)  # Lists violations and suggestions
```

### Machine-Readable Config

All brand data is available in `brand-config.json`:
- Colors with hex, RGB, and usage notes
- Typography specifications
- Logo paths with selection rules
- Forbidden generation patterns
- Application guidelines per context

### Legacy Quick Reference

```javascript
const PSD_BRAND = {
  colors: {
    // Logo colors
    seaGlass: '#6CA18A',
    pacific: '#25424C',
    driftwood: '#D7CDBE',
    // Supporting colors
    cedar: '#466857',
    whulge: '#346780',
    seaFoam: '#EEEBE4',
    meadow: '#5D9068',
    ocean: '#7396A9',
    skylight: '#FFFAEC'
  },
  fonts: {
    heading: "'Josefin Sans', Arial, sans-serif",
    body: "'Josefin Slab', Georgia, serif"
  },
  logos: {
    localPath: 'skills/psd-brand-guidelines/assets/',
    driveFolder: '1YhjxX_pOwZJppZebIIC7QW_UHF4bvo79'
  }
};
```

---

*Last updated: January 14, 2025*
*Source: PSD Branding Guide 06.14.2024.pdf, brand-config.json*
