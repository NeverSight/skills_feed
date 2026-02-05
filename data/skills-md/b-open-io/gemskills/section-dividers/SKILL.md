---
name: Section Dividers
description: This skill should be used when the user asks to "create section dividers", "make transparent dividers", "generate decorative borders", "create parallax dividers", "design section transitions", "make HR dividers", "crystal dividers", "organic borders", "silhouette borders", or needs transparent PNG dividers for web sections.
---

# Section Dividers

Generate transparent decorative dividers for web page sections.

## CRITICAL RULES - Read Before Generating

### 1. FULL WIDTH Required
- Strip MUST extend from LEFT EDGE to RIGHT EDGE of image
- NO floating islands - content spans entire width
- Add "FULL WIDTH from left edge to right edge" to prompt

### 2. Cross-Section NOT Reflection
- TOP edge: Content pointing UPWARD (houses, trees, rooftops)
- BOTTOM edge: DIFFERENT content pointing DOWNWARD (pipes, caves, roots)
- NOT a mirror/reflection of the same scene
- Add "TOP EDGE has [X] pointing UPWARD. BOTTOM EDGE has [Y] pointing DOWNWARD" - use DIFFERENT X and Y

### 3. SOLID Filled Strip
- Strip must be SOLID between top and bottom edges
- NOT hollow, NOT a cave opening, NOT an arch
- Add "SOLID FILLED strip - not hollow, not a cave"

### 4. Clean Boundary Required
- Sharp, clear edge between silhouette content and background
- High contrast between the two colors
- If edges are fuzzy or blended = generation failed

### 5. Content Must NOT Touch Image Edges
- Content should float in CENTER with background above and below
- If content touches TOP or BOTTOM of image = JUNK, do not process
- Verify raw image BEFORE running bg removal

### 6. Exact Color Matching
- **Background** = EXACT parallax color (use `analyze-bg.ts`)
- **Silhouette** = EXACT section CSS color
- Both colors must be explicitly stated in prompt with hex values

## Background Color Strategy

**Use a HIGH CONTRAST color from the parallax image's own palette.** This ensures:
1. Clean edges when removing background (high contrast = sharp removal)
2. No color fringing or halos (color exists in the parallax)
3. Seamless blending with the actual parallax

### Get the Parallax Color
```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/section-dividers

# Analyze the parallax image to find colors in its palette
bun run scripts/analyze-bg.ts /path/to/parallax.png top   # for top border
bun run scripts/analyze-bg.ts /path/to/parallax.png bottom # for bottom border
```

Choose the color from the parallax palette that provides HIGHEST CONTRAST with your silhouette color. For dark silhouettes, pick the lightest color from the parallax. For light silhouettes, pick the darkest.

### Background Removal
Use `remove-bg.ts` (AI-based) for reliable background removal:
```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/section-dividers && bun run scripts/remove-bg.ts input.png output.png
```

## Generation Workflow

### Step 1: Generate

```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/generate-image
bun run scripts/generate.ts "[PROMPT]" --aspect 21:9 --size 2K --negative "[NEGATIVES]" --output divider-raw.png
```

**Prompt template:**
```
ONE THIN horizontal SOLID terrain strip floating in solid [PARALLAX_COLOR].
FULL WIDTH from left edge to right edge.
The strip is SOLID FILLED - not hollow, not a cave.
TOP EDGE silhouette: [SURFACE_CONTENT] pointing UPWARD.
BOTTOM EDGE silhouette: [UNDERGROUND_CONTENT] pointing DOWNWARD.
SOLID MASS between top and bottom edges - filled with [SECTION_COLOR].
JAGGED organic edges on BOTH top AND bottom.
Strip is 12-15% of image height floating in vertical center.
85% solid [PARALLAX_COLOR] background above and below.
Shadow puppet silhouettes.
```

**Negative prompt:**
```
hollow, cave, empty center, arch, tunnel view, flat edges, reflection, mirror, white, pink, magenta, tall, thick, floating island, not full width
```

### Step 2: Verify Raw Image (CRITICAL)

Before processing, verify:
- [ ] Content spans FULL WIDTH (left to right)
- [ ] TOP content points UP, BOTTOM content points DOWN (not reflection)
- [ ] Strip is SOLID (not hollow/cave)
- [ ] Content does NOT touch top/bottom image edges
- [ ] Clear boundary between content and background

**If ANY check fails = REGENERATE. Do not process junk.**

### Step 3: Remove Background

```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/section-dividers
bun run scripts/remove-bg.ts divider-raw.png divider.png
```

Uses `cjwbw/rembg` model which PRESERVES RESOLUTION.

### Step 4: Verify Final Image

- [ ] Transparency is clean (no artifacts)
- [ ] Full resolution preserved
- [ ] Blends with parallax and section on page

## Scripts

### remove-bg.ts
AI background removal via Replicate (rembg model). Preserves original resolution.
```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/section-dividers && bun run scripts/remove-bg.ts input.png output.png
```

### analyze-bg.ts
Extract dominant color from parallax image.
```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/section-dividers && bun run scripts/analyze-bg.ts parallax.png bottom
```

### colorize.ts
Tint transparent silhouette to match theme.
```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/section-dividers && bun run scripts/colorize.ts input.png output.png "#042f2e"
```

## Fixing Existing Dividers (Color Mismatch)

When an existing divider has wrong colors or semi-transparent edges:

### Step 1: Remove Background
```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/section-dividers
bun run scripts/remove-bg.ts original.png transparent.png
```

### Step 2: Make SOLID with Section Color
The remove-bg output has semi-transparent edges. To make it SOLID and match the section:

```python
from PIL import Image

img = Image.open('transparent.png').convert('RGBA')
pixels = img.load()
width, height = img.size

# Get EXACT section color from CSS/computed style
# Example: oklch(0.12 0.015 260) = RGB(3, 6, 11)
sr, sg, sb = 3, 6, 11

for y in range(height):
    for x in range(width):
        r, g, b, a = pixels[x, y]
        if a > 50:  # Any visible pixel = SOLID section color
            pixels[x, y] = (sr, sg, sb, 255)
        else:  # Transparent stays transparent
            pixels[x, y] = (0, 0, 0, 0)

img.save('final.png')
```

**Key points:**
- Alpha > 50 = make fully opaque (255) with section color
- Alpha <= 50 = make fully transparent (0)
- This eliminates semi-transparent edges from AI removal
- Section color must EXACTLY match the adjacent section's background

### Getting Exact Section Color
```javascript
// In browser console on the page:
const el = document.querySelector('#section-id');
const canvas = document.createElement('canvas');
canvas.width = 1; canvas.height = 1;
const ctx = canvas.getContext('2d');
ctx.fillStyle = getComputedStyle(el).backgroundColor;
ctx.fillRect(0, 0, 1, 1);
const data = ctx.getImageData(0, 0, 1, 1).data;
console.log(`RGB(${data[0]}, ${data[1]}, ${data[2]})`);
```

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Content doesn't span full width | Missing "FULL WIDTH" | Add "FULL WIDTH from left edge to right edge" |
| Bottom is mirror of top | Reflection not cross-section | Use DIFFERENT content for top and bottom |
| Hollow/cave shape | Wrong shape prompt | Add "SOLID FILLED - not hollow, not a cave" |
| Content touches edges | Strip too tall | Add "12-15% height, 85% background above/below" |
| Fuzzy edges after removal | Background color mismatch | Ensure background EXACTLY matches parallax color |
| AI removed too much | Complex edges | Try regenerating with cleaner silhouette shapes |
| Wrong colors | Didn't match exactly | Use exact hex values from analyze-bg and CSS |
| Ghosting/semi-transparent edges | Soft edges in generation | Regenerate with sharper silhouette style |
| Semi-transparent silhouette | AI removal creates soft alpha | Use "Fixing Existing Dividers" workflow above |
| Color doesn't match section | Wrong RGB values | Get exact color from browser computed style |

## CSS Positioning

### Animated vs Static Dividers

**For ANIMATED dividers** (with `.float` or other CSS animations):
- Use fixed pixel values: `top: -20px`
- DO NOT use `translateY(-50%)`

**For STATIC dividers** (no animation):
- `translateY(-50%)` works fine
- Centers element on the seam

### Why Transforms Fail with Animations

When an element has a CSS animation that uses `transform` in its keyframes:
```css
@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}
```

The animation's transform **completely overrides** any inline transform:
- Your `style={{ transform: "translateY(-50%)" }}` gets replaced
- Element renders with animation's `translateY(0px)` instead

Also note: percentage margins (`margin-top: -50%`) are based on parent WIDTH, not height.

### Correct Approach: Simple Negative Top

```css
/* Position divider on seam between sections */
.divider-top {
  position: absolute;
  top: -20px;  /* Adjust until CENTER sits on seam */
  left: 0;
  right: 0;
  z-index: 50;
  pointer-events: none;
}
```

### Layout Structure

```
SECTION (solid background)
    ↓
    SEAM ← divider CENTER should align HERE
    ↓
PARALLAX CONTAINER
  └── DIVIDER (absolute, top: -20px, adjusts per image)
  └── PARALLAX IMAGE
  └── DIVIDER (absolute, bottom: 0, transform for bottom)
    ↓
    SEAM
    ↓
SECTION (solid background)
```

### Implementation Pattern

From `tokenpass-web/src/components/BorderedParallax.tsx`:

```tsx
{/* Top divider - sits on seam above parallax */}
<div
  className="absolute left-0 right-0 z-50 pointer-events-none float"
  style={{ top: "-20px" }}  // Simple fixed value
>
  <img src={borders.top} className="w-full h-auto" />
</div>
```

### Positioning Tips

1. Start with `top: -20px` and adjust visually
2. Goal: CENTER of divider image sits on the SEAM
3. If image has transparent space, account for it
4. Test on both mobile AND desktop
5. Fixed pixel values work consistently across screen sizes
