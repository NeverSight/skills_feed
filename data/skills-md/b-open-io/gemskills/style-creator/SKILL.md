---
name: Style Creator
description: This skill should be used when the user asks to "add a new style", "create a style", "add an art style", "new aesthetic", "custom style", "make a style for", or needs to add a new art style to the gemskills style library. Guides the complete workflow from defining the style to generating and optimizing the reference tile.
---

# Style Creator

Add new art styles to the gemskills style library with properly crafted prompts, reference tiles, and registry entries.

## When to Use

- Adding a new art style to the library
- Creating a regional or cultural aesthetic style
- Defining a custom visual style with a reference tile
- Batch-adding multiple related styles

## Important: Working Directory

All file edits and commands operate relative to the **plugin root** using `${SKILL_BASE_DIR}/..` to reach sibling skills or `${CLAUDE_PLUGIN_ROOT}` for the repo root.

**Sharp may fail in the plugin cache.** If `bun run optimize` fails, the tile generation script auto-optimizes. If both fail, use `sips` as a fallback:
```bash
sips -s format png -s formatOptions best <tile-path> --out <tile-path>
```

## Workflow

Follow these steps in order. Do not skip steps.

### Step 1: Define the Style

Gather from the user:
- **Name**: Human-readable name (e.g. "Miami Aesthetic")
- **ID**: Lowercase with hyphens (e.g. `miami-aesthetic`)
- **Short name**: 3-4 character abbreviation (e.g. `miam`)
- **Category**: One of: `traditional`, `digital`, `illustration`, `photography`, `design`, `retro`, `technique`, `decorative`, `creative`, `cultural`

If the user provides only a name or concept, derive the ID and short name automatically. Choose the category that best fits.

### Step 2: Write promptHints

The `promptHints` field is a comma-separated string of descriptors prepended to user prompts when the style is used. Focus on:

- Color palette keywords
- Texture and material descriptors
- Technique and medium references
- Mood and atmosphere terms
- Compositional patterns

Keep to 8-12 descriptors. These guide the model when generating user images, not the tile itself.

### Step 3: Write the tilePrompt

Apply these principles — do NOT read external reference files, the rules are right here:

**Core principle: Texture vs Object.** The tile must transfer materiality/medium/technique, NOT a scene. A tile showing "a cyberpunk city" will bleed city elements into every user prompt. A tile showing "neon refractions on chrome with film grain" transfers only the visual physics.

**6-part prompt structure:**
1. **Full-bleed anchor**: `Full-bleed [style] filling the entire canvas`
2. **Macro/texture anchor**: `extreme close-up macro texture`, `seamless pattern`, `abstract composition`
3. **Style descriptors**: Specific movements, artists, time periods
4. **Materiality/medium**: What the art is "made of" — `cracked canvas`, `halftone dots`, `VHS static`, `watercolor bleed`
5. **Palette and lighting**: `chiaroscuro`, `pastel gradients`, `neon rim light`, `sepia tones`
6. **Anti-container enforcers**: `Edge to edge, no frame, no border, no [style-specific items]`

**Category tips:**
- **Abstract styles**: Focus on geometry and brushwork, avoid naming objects
- **Figurative styles** (anime, comic): Generate the *ink and paper*, not a character. Use `dense montage` or `extreme macro of brushwork`
- **Photography**: Focus on camera artifacts — grain, light leaks, vignette, bokeh
- **Design movements**: Focus on repeating motifs and materials
- **Regional aesthetics**: Color palette and textures, NOT photos of places. No buildings, streets, or landmarks.

**Anti-container items to add based on style:**
- Paintings: `no canvas, no easel, no gallery, no museum, no wall`
- Crafts: `no hoop, no frame, no desk, no table`
- Photos: `no letterbox, no black bars, no monitor, no screen`
- Textiles: `no cloth edge, no fabric edge, no bed, no furniture`

### Step 4: Add to styles.json

Add the new style entry to the `styles` array in:
```
${SKILL_BASE_DIR}/../browsing-styles/assets/styles.json
```

Entry format:
```json
{
  "id": "style-id",
  "shortName": "shrt",
  "name": "Style Name",
  "category": "category",
  "promptHints": "descriptor1, descriptor2, descriptor3",
  "tilePrompt": "Full-bleed ... Edge to edge, no frame, no border."
}
```

Verify the ID and short name are unique across all existing styles before adding.

### Step 5: Generate the Tile

Generate the reference tile using the tile generation script:

```bash
cd ${SKILL_BASE_DIR}/../browsing-styles && bun run scripts/generate_tiles.ts --style <style-id>
```

This generates a 512x512 PNG tile at `assets/tiles/<style-id>.png` and auto-optimizes it.

If auto-optimization fails, try manually from the plugin root:
```bash
cd ${CLAUDE_PLUGIN_ROOT} && bun run optimize -- --file=skills/browsing-styles/assets/tiles/<style-id>.png
```

If sharp is unavailable, use sips:
```bash
sips -s format png -s formatOptions best ${SKILL_BASE_DIR}/../browsing-styles/assets/tiles/<style-id>.png --out ${SKILL_BASE_DIR}/../browsing-styles/assets/tiles/<style-id>.png
```

If the style benefits from a reference image (e.g. a regional aesthetic), use the generate-image script with `--input`:

```bash
cd ${SKILL_BASE_DIR}/../generate-image && bun run scripts/generate.ts \
  "<tilePrompt text>" \
  --input /path/to/reference.jpg \
  --aspect 1:1 --size 1K \
  --output ${SKILL_BASE_DIR}/../browsing-styles/assets/tiles/<style-id>.png
```

### Step 6: Visual Verification

**Do not read the generated tile back into context.** Ask the user to visually inspect it. Common issues:

- Not full-bleed? (frames, borders, containers, canvas edges)
- Shows a scene instead of the aesthetic?
- Wrong color palette?
- Text, logos, or trademarked content?

If it fails, update the tilePrompt and regenerate.

### Step 7: Update Counts

After adding styles, update the style count in these files:
- `${CLAUDE_PLUGIN_ROOT}/README.md` (style count mentions)
- `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json` (description text and version bump)
- `${SKILL_BASE_DIR}/../browsing-styles/SKILL.md` (count)
- `${SKILL_BASE_DIR}/../team-group-photo/SKILL.md` (count)

Regenerate `STYLES.md` from the plugin root:
```bash
cd ${CLAUDE_PLUGIN_ROOT} && bun -e "
const data = JSON.parse(require('fs').readFileSync('skills/browsing-styles/assets/styles.json', 'utf8'));
const styles = data.styles;
const cats = data.categories;
const grouped = {};
for (const s of styles) { if (!grouped[s.category]) grouped[s.category] = []; grouped[s.category].push(s); }
let md = '# Art Styles Reference\n\n' + styles.length + ' styles across ' + Object.keys(grouped).length + ' categories. Use \\\`--style <id>\\\` or \\\`--style <short>\\\` with any image generation skill.\n\n## Categories\n\n| Category | Count | Description |\n|----------|-------|-------------|\n';
for (const [cat, desc] of Object.entries(cats)) { md += '| ' + cat + ' | ' + (grouped[cat]?.length || 0) + ' | ' + desc + ' |\n'; }
md += '\n';
for (const [cat, desc] of Object.entries(cats)) { const items = grouped[cat] || []; if (!items.length) continue; md += '## ' + cat.charAt(0).toUpperCase() + cat.slice(1) + '\n\n| Tile | ID | Short | Name |\n|------|-----|-------|------|\n'; for (const s of items) { md += '| <img src=\"skills/browsing-styles/assets/tiles/' + s.id + '.png\" width=\"80\" /> | ' + s.id + ' | ' + s.shortName + ' | ' + s.name + ' |\n'; } md += '\n'; }
require('fs').writeFileSync('STYLES.md', md);
console.log('STYLES.md written with ' + styles.length + ' styles');
"
```

### Step 8: Bump Version and Commit

Bump the patch version in `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json` and commit all changes.

## Context Discipline

**Do not read generated tile images back into context.** The scripts output file paths only. Ask the user to visually inspect tiles and provide feedback for iteration.
