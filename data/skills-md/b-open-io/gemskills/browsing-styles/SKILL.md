---
name: Browsing Styles
description: This skill should be used when the user asks to "browse art styles", "preview styles", "list available styles", "search styles", "show style thumbnails", "explore art movements", or needs to see available artistic styles for image generation.
---

# Browsing Styles

Browse and preview 100+ artistic styles for image generation. Launch an interactive grid preview server or list styles from the command line.

## When to Use

This skill should be used when:
- Browsing available art styles for image generation
- Previewing style thumbnails before selecting one
- Searching for a specific style by name or category
- Exploring styles by art movement, technique, or era

## Style Categories

| Category | Count | Examples |
|----------|-------|----------|
| movement | 27 | Impressionism, Cubism, Surrealism |
| cultural | 15 | Ukiyo-e, Persian Miniature, Celtic |
| technique | 20 | Watercolor, Charcoal, Mosaic |
| photography | 10 | Cinematic, Noir, Polaroid |
| digital | 15 | Pixel Art, Cyberpunk, Vaporwave |
| illustration | 13 | Anime, Comic Book, Fantasy Art |

## Quick Reference (Top 20 Styles)

| Short | Name | Category |
|-------|------|----------|
| impr | Impressionism | movement |
| cube | Cubism | movement |
| ukiy | Ukiyo-e | cultural |
| deco | Art Deco | movement |
| wtrc | Watercolor | technique |
| char | Charcoal | technique |
| pixl | Pixel Art | digital |
| cybr | Cyberpunk | digital |
| anim | Anime | illustration |
| barq | Baroque | movement |
| surr | Surrealism | movement |
| minm | Minimalism | movement |
| noir | Film Noir | photography |
| vapr | Vaporwave | digital |
| cine | Cinematic | photography |
| comi | Comic Book | illustration |
| fant | Fantasy Art | illustration |
| stmp | Steampunk | illustration |
| lpol | Low Poly | digital |
| botn | Botanical | illustration |

## Usage

### Launch Preview Server

Start an interactive browser-based style grid:

```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/browsing-styles && bun run scripts/preview_server.ts
```

Opens at `http://localhost:3456` with:
- Thumbnail grid of all styles
- Click to view full size
- Filter by category
- Search by name
- Copy style ID on click

### List Styles (CLI)

Output styles as JSON for scripting:

```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/browsing-styles

# List all styles
bun run scripts/list_styles.ts

# Filter by category
bun run scripts/list_styles.ts --category movement

# Search by name
bun run scripts/list_styles.ts --search "art deco"

# Output specific fields
bun run scripts/list_styles.ts --fields id,shortName,promptHints
```

### Fetch Reference Images

Download reference images from museum APIs:

```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/browsing-styles

# Fetch all styles (creates ~/.cache/gemskills/styles/)
bun run scripts/fetch_styles.ts

# Fetch specific style
bun run scripts/fetch_styles.ts --style impressionism

# Force re-download
bun run scripts/fetch_styles.ts --force
```

## Integration with generate-image

Use styles with the generate-image skill:

```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/generate-image

# Using style ID
bun run scripts/generate.ts "mountain landscape" --style impressionism

# Using short name
bun run scripts/generate.ts "portrait" --style ukiy
```

The style's `promptHints` are prepended to your prompt automatically.

## Style Registry

Styles are defined in `/styles/styles.json` at the plugin root. Each style includes:

```json
{
  "id": "impressionism",
  "shortName": "impr",
  "name": "Impressionism",
  "category": "movement",
  "era": "1860-1890",
  "artists": ["Monet", "Renoir", "Pissarro"],
  "promptHints": "visible brushstrokes, pure unmixed colors...",
  "sources": [
    {"api": "met", "objectId": 437133, "title": "Water Lilies"}
  ]
}
```

## Reference Images

Reference images are fetched from museum APIs with CC0/public domain licenses:

- **Metropolitan Museum of Art** - Primary source, 492K+ images, no auth required
- **Rijksmuseum** - 800K+ images, CC-BY license
- **Art Institute of Chicago** - 50K+ IIIF images

Images are cached locally at `~/.cache/gemskills/styles/<style-id>/`:
- `thumb.jpg` - 256x256 thumbnail for preview grid
- `ref-1.jpg`, `ref-2.jpg` - Full resolution reference images

## Adding Custom Styles

To add a custom style, edit `/styles/styles.json`:

1. Choose a unique `id` (lowercase, hyphens)
2. Assign a 4-character `shortName`
3. Write descriptive `promptHints` (comma-separated descriptors)
4. Optionally add Met Museum `objectId`s for reference images

Then run `bun run scripts/fetch_styles.ts --style <your-style-id>` to download references.

## See Also

- `references/museum-apis.md` - API documentation for image sources
- `references/style-catalog.md` - Full descriptions of all 100+ styles
- `references/prompt-hints.md` - Detailed prompt engineering guidance
