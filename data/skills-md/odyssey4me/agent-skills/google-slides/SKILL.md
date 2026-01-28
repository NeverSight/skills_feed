---
name: google-slides
description: Manage Google Slides presentations. Create presentations, add/delete slides, insert text, shapes, and images. Use when working with Google Slides presentation management.
metadata:
  author: odyssey4me
  version: "0.1.0"
license: MIT
---

# Google Slides

Interact with Google Slides for presentation creation, slide management, and content insertion.

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install --user google-auth google-auth-oauthlib google-api-python-client keyring pyyaml
   ```

2. **Download the skill** from [Releases](https://github.com/odyssey4me/agent-skills/releases) or use directly from this repository.

## Setup Verification

After installation, verify the skill is properly configured:

```bash
python scripts/google-slides.py check
```

This will check:
- Python dependencies (google-auth, google-auth-oauthlib, google-api-python-client, keyring, pyyaml)
- Authentication configuration
- Connectivity to Google Slides API

If anything is missing, the check command will provide setup instructions.

## Authentication

Google Slides uses OAuth 2.0 for authentication. For complete setup instructions, see:

1. [GCP Project Setup Guide](../../docs/gcp-project-setup.md) - Create project, enable Slides API
2. [Google OAuth Setup Guide](../../docs/google-oauth-setup.md) - Configure credentials

### Quick Start

1. Create `~/.config/agent-skills/google.yaml`:
   ```yaml
   oauth_client:
     client_id: your-client-id.apps.googleusercontent.com
     client_secret: your-client-secret
   ```

2. Run `python scripts/google-slides.py check` to trigger OAuth flow and verify setup.

### OAuth Scopes

The skill requests granular scopes for different operations:

| Scope | Permission | Used For |
|-------|-----------|----------|
| `presentations.readonly` | Read presentations | Reading presentation metadata and content |
| `presentations` | Full access | Creating and modifying presentations |

### Scope Errors

If you encounter "insufficient scope" errors, revoke your token and re-authenticate:

1. Revoke at https://myaccount.google.com/permissions
2. Clear token: `keyring del agent-skills google-slides-token-json`
3. Re-run: `python scripts/google-slides.py check`

## Commands

### check

Verify configuration and connectivity.

```bash
python scripts/google-slides.py check
```

This validates:
- Python dependencies are installed
- Authentication is configured
- Can connect to Google Slides API
- Creates a test presentation to verify write access

### auth setup

Store OAuth 2.0 client credentials for custom OAuth flow.

```bash
python scripts/google-slides.py auth setup \
  --client-id YOUR_CLIENT_ID \
  --client-secret YOUR_CLIENT_SECRET
```

Credentials are saved to `~/.config/agent-skills/google-slides.yaml`.

**Options:**
- `--client-id` - OAuth 2.0 client ID (required)
- `--client-secret` - OAuth 2.0 client secret (required)

### presentations create

Create a new Google Slides presentation.

```bash
python scripts/google-slides.py presentations create --title "My Presentation"
```

**Options:**
- `--title` - Presentation title (required)
- `--json` - Output as JSON

**Example:**
```bash
python scripts/google-slides.py presentations create --title "Q4 Review"

# Output:
# ✓ Presentation created successfully
# Title: Q4 Review
# Presentation ID: 1abc...xyz
# Slides: 1
# URL: https://docs.google.com/presentation/d/1abc...xyz/edit
```

### presentations get

Get presentation metadata and structure.

```bash
python scripts/google-slides.py presentations get PRESENTATION_ID
```

**Arguments:**
- `presentation_id` - The Google Slides presentation ID

**Options:**
- `--json` - Output full presentation structure as JSON

**Example:**
```bash
python scripts/google-slides.py presentations get 1abc...xyz

# Output:
# Title: Q4 Review
# Presentation ID: 1abc...xyz
# Slides: 5
# URL: https://docs.google.com/presentation/d/1abc...xyz/edit
#
# Slides:
# Slide 1:
#   ID: slide_id_1
#   Layout: TITLE
#   Elements: 2 (2 text, 0 shapes, 0 images, 0 other)
# Slide 2:
#   ID: slide_id_2
#   Layout: TITLE_AND_BODY
#   Elements: 3 (2 text, 1 shapes, 0 images, 0 other)
```

### slides create

Add a new slide to a presentation.

```bash
python scripts/google-slides.py slides create PRESENTATION_ID --layout BLANK
```

**Arguments:**
- `presentation_id` - The Google Slides presentation ID

**Options:**
- `--layout` - Slide layout (default: BLANK)
  - `BLANK` - Empty slide
  - `TITLE` - Title slide
  - `TITLE_AND_BODY` - Title and body text
  - `TITLE_ONLY` - Title only
  - `SECTION_HEADER` - Section header
  - `SECTION_TITLE_AND_DESCRIPTION` - Section with description
  - `ONE_COLUMN_TEXT` - Single column of text
  - `MAIN_POINT` - Large centered text
  - `BIG_NUMBER` - Large number display
- `--index` - Insert at specific position (0-based, optional)
- `--json` - Output API response as JSON

**Example:**
```bash
# Add blank slide at the end
python scripts/google-slides.py slides create 1abc...xyz --layout BLANK

# Add title slide at position 0
python scripts/google-slides.py slides create 1abc...xyz --layout TITLE --index 0

# Output:
# ✓ Slide created successfully
#   Slide ID: slide_abc123
#   Layout: TITLE
```

See [references/layouts-guide.md](references/layouts-guide.md) for layout details.

### slides delete

Delete a slide from a presentation.

```bash
python scripts/google-slides.py slides delete PRESENTATION_ID --slide-id SLIDE_ID
```

**Arguments:**
- `presentation_id` - The Google Slides presentation ID

**Options:**
- `--slide-id` - Slide object ID to delete (required, not the index!)
- `--json` - Output API response as JSON

**Example:**
```bash
# Get slide IDs first
python scripts/google-slides.py presentations get 1abc...xyz --json | jq '.slides[].objectId'

# Delete a slide
python scripts/google-slides.py slides delete 1abc...xyz --slide-id slide_abc123

# Output:
# ✓ Slide deleted successfully
```

**Warning:** Cannot delete the last remaining slide in a presentation.

### text insert

Insert text into a slide.

```bash
python scripts/google-slides.py text insert PRESENTATION_ID \
  --slide-id SLIDE_ID \
  --text "Hello World"
```

**Arguments:**
- `presentation_id` - The Google Slides presentation ID

**Options:**
- `--slide-id` - Slide object ID (required)
- `--text` - Text to insert (required)
- `--x` - X position in points (default: 100)
- `--y` - Y position in points (default: 100)
- `--width` - Text box width in points (default: 400)
- `--height` - Text box height in points (default: 100)
- `--json` - Output API response as JSON

**Example:**
```bash
# Insert text at default position
python scripts/google-slides.py text insert 1abc...xyz \
  --slide-id slide_abc123 \
  --text "Hello World"

# Insert text at custom position
python scripts/google-slides.py text insert 1abc...xyz \
  --slide-id slide_abc123 \
  --text "Q4 Results" \
  --x 50 --y 50 --width 500 --height 80

# Output:
# ✓ Text inserted successfully
#   Text: Q4 Results
#   Position: (50.0, 50.0) points
#   Size: 500.0 x 80.0 points
```

**Note:** Coordinates are in points (1 point = 1/72 inch). Origin (0,0) is top-left.

### shapes create

Create a shape on a slide.

```bash
python scripts/google-slides.py shapes create PRESENTATION_ID \
  --slide-id SLIDE_ID \
  --shape-type RECTANGLE
```

**Arguments:**
- `presentation_id` - The Google Slides presentation ID

**Options:**
- `--slide-id` - Slide object ID (required)
- `--shape-type` - Shape type (required)
  - `RECTANGLE`, `ELLIPSE`, `TRIANGLE`, `PENTAGON`, `HEXAGON`
  - `STAR_5`, `STAR_8`, `STAR_24`, `STAR_32`
  - `CLOUD`, `HEART`, `LIGHTNING_BOLT`, `MOON`, `SUN`
  - `ARROW_NORTH`, `ARROW_EAST`, `ARROW_SOUTH`, `ARROW_WEST`
  - And many more (see [references/shapes-guide.md](references/shapes-guide.md))
- `--x` - X position in points (default: 100)
- `--y` - Y position in points (default: 100)
- `--width` - Shape width in points (default: 200)
- `--height` - Shape height in points (default: 200)
- `--json` - Output API response as JSON

**Example:**
```bash
# Create rectangle
python scripts/google-slides.py shapes create 1abc...xyz \
  --slide-id slide_abc123 \
  --shape-type RECTANGLE

# Create star with custom size
python scripts/google-slides.py shapes create 1abc...xyz \
  --slide-id slide_abc123 \
  --shape-type STAR_5 \
  --x 300 --y 200 --width 150 --height 150

# Output:
# ✓ Shape created successfully
#   Type: STAR_5
#   Position: (300.0, 200.0) points
#   Size: 150.0 x 150.0 points
```

See [references/shapes-guide.md](references/shapes-guide.md) for all shape types.

### images create

Insert an image into a slide.

```bash
python scripts/google-slides.py images create PRESENTATION_ID \
  --slide-id SLIDE_ID \
  --image-url "https://example.com/image.png"
```

**Arguments:**
- `presentation_id` - The Google Slides presentation ID

**Options:**
- `--slide-id` - Slide object ID (required)
- `--image-url` - Image URL (required, must be publicly accessible)
- `--x` - X position in points (default: 100)
- `--y` - Y position in points (default: 100)
- `--width` - Image width in points (default: 300)
- `--height` - Image height in points (default: 200)
- `--json` - Output API response as JSON

**Example:**
```bash
python scripts/google-slides.py images create 1abc...xyz \
  --slide-id slide_abc123 \
  --image-url "https://example.com/chart.png" \
  --x 50 --y 150 --width 400 --height 300

# Output:
# ✓ Image created successfully
#   URL: https://example.com/chart.png
#   Position: (50.0, 150.0) points
#   Size: 400.0 x 300.0 points
```

**Note:** The image URL must be publicly accessible or authenticated with Google.

## Examples

### Create a simple presentation

```bash
# Create presentation
PRES_ID=$(python scripts/google-slides.py presentations create \
  --title "Team Update" --json | jq -r '.presentationId')

# Get the default slide ID
SLIDE_ID=$(python scripts/google-slides.py presentations get $PRES_ID --json | \
  jq -r '.slides[0].objectId')

# Add title text
python scripts/google-slides.py text insert $PRES_ID \
  --slide-id $SLIDE_ID \
  --text "Q4 Team Update" \
  --x 50 --y 50 --width 600 --height 100

# Add subtitle
python scripts/google-slides.py text insert $PRES_ID \
  --slide-id $SLIDE_ID \
  --text "December 2024" \
  --x 50 --y 180 --width 600 --height 50
```

### Build a multi-slide presentation

```bash
#!/bin/bash
PRES_ID="your-presentation-id"

# Add content slide
SLIDE_ID=$(python scripts/google-slides.py slides create $PRES_ID \
  --layout TITLE_AND_BODY --json | jq -r '.replies[0].createSlide.objectId')

# Add title
python scripts/google-slides.py text insert $PRES_ID \
  --slide-id $SLIDE_ID \
  --text "Key Metrics" \
  --x 50 --y 30 --width 600 --height 60

# Add chart image
python scripts/google-slides.py images create $PRES_ID \
  --slide-id $SLIDE_ID \
  --image-url "https://example.com/metrics.png" \
  --x 100 --y 120 --width 500 --height 350

# Add another slide with shapes
SLIDE2_ID=$(python scripts/google-slides.py slides create $PRES_ID \
  --layout BLANK --json | jq -r '.replies[0].createSlide.objectId')

# Add decorative shape
python scripts/google-slides.py shapes create $PRES_ID \
  --slide-id $SLIDE2_ID \
  --shape-type STAR_5 \
  --x 550 --y 30 --width 80 --height 80
```

### Create presentation from data

```bash
#!/bin/bash

# Create presentation
PRES_ID=$(python scripts/google-slides.py presentations create \
  --title "Sales Report" --json | jq -r '.presentationId')

# Add slide for each region
for region in "North" "South" "East" "West"; do
  SLIDE_ID=$(python scripts/google-slides.py slides create $PRES_ID \
    --layout TITLE_AND_BODY --json | jq -r '.replies[0].createSlide.objectId')

  python scripts/google-slides.py text insert $PRES_ID \
    --slide-id $SLIDE_ID \
    --text "$region Region Sales" \
    --x 50 --y 30 --width 600 --height 80
done
```

## Coordinate System

Google Slides uses **points** for positioning and sizing:
- 1 point = 1/72 inch
- 1 inch = 72 points
- Origin (0, 0) is at the top-left corner
- Standard slide size: 720 x 540 points (10 x 7.5 inches)

**Common reference positions:**

```
(0, 0)                                    (720, 0)
  ┌───────────────────────────────────────┐
  │  Title area                           │
  │  (50, 50, 620, 80)                    │
  │                                       │
  │  Content area                         │
  │  (50, 150, 620, 350)                  │
  │                                       │
  │                                       │
  └───────────────────────────────────────┘
(0, 540)                                (720, 540)
```

## Troubleshooting

### "Insufficient scope" errors

You need to revoke and re-authenticate to grant additional permissions:

1. Go to https://myaccount.google.com/permissions
2. Find "Agent Skills" and remove access
3. Delete stored token: `keyring del agent-skills google-slides-token-json`
4. Run `python scripts/google-slides.py check` to re-authenticate

### Cannot find presentation

Make sure you're using the correct presentation ID from the URL:
- URL: `https://docs.google.com/presentation/d/1abc...xyz/edit`
- Presentation ID: `1abc...xyz`

### Cannot find slide ID

Slide IDs are object IDs, not indices. Get them with:

```bash
python scripts/google-slides.py presentations get $PRES_ID --json | \
  jq -r '.slides[] | "\(.objectId) (index \(.slideProperties.slideIndex))"'
```

### Image not appearing

The image URL must be:
- Publicly accessible (no authentication required), OR
- Accessible to the Google account you're using

Test the URL in a browser. If it requires authentication, you'll need to:
1. Upload the image to Google Drive
2. Make it publicly accessible or share it with your Google account
3. Use the Google Drive URL

### Slide position/size issues

Remember:
- Coordinates are in **points**, not pixels
- Standard slide: 720 x 540 points
- Elements outside slide boundaries won't be visible
- Use `--x`, `--y`, `--width`, `--height` to position elements

### Dependencies not found

Install required dependencies:

```bash
pip install --user google-auth google-auth-oauthlib google-api-python-client keyring pyyaml
```

### OAuth flow fails

Ensure your GCP project has:
1. Google Slides API enabled (`slides.googleapis.com`)
2. OAuth 2.0 credentials created
3. OAuth consent screen configured
4. Your email added as a test user (if app is in testing mode)

See [docs/gcp-project-setup.md](../../docs/gcp-project-setup.md) for detailed instructions.

## Related Skills

- [Google Drive](../google-drive/SKILL.md) - File management (Drive manages file metadata, Slides manages content)
- [Google Docs](../google-docs/SKILL.md) - Document creation and editing
- [Google Sheets](../google-sheets/SKILL.md) - Spreadsheet management

## API Reference

For advanced usage, see:
- [Google Slides API Documentation](https://developers.google.com/slides/api)
- [Working with presentations](https://developers.google.com/slides/api/guides/presentations)
- [Layouts guide](references/layouts-guide.md)
- [Shapes guide](references/shapes-guide.md)
