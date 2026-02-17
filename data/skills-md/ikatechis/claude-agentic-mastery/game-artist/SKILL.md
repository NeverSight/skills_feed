---
name: game-artist
description: Manage game assets with Kenney-ONLY approach. Search 36,000+ Kenney CC0 assets. If asset not found, ask user to find/generate manually. Ensure style consistency with flat/vector Kenney aesthetic. Auto-triggers on asset requests.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Game Artist Skill

Intelligent game asset management with **Kenney-first** workflow.

## When This Skill Activates

This skill automatically triggers when you:
- Request a game asset ("find a health icon", "need a tree sprite")
- Ask about visual elements ("what would work for power-ups?")
- Want to add new sprites/graphics
- Need asset recommendations

## Core Principle: Kenney ONLY

**Don't generate - use what exists!**

The project has access to Kenney's All-in-1 collection (~36,000 assets, all CC0):
- 150+ 2D asset packs
- Characters, tiles, props, UI, effects
- All in consistent flat/vector style
- Free for any use

**Workflow:**
1. 🔍 **Search** Kenney collection thoroughly
2. ✅ **Use** existing asset if good match
3. ❓ **Ask user** to find/generate manually if not found
4. ✔️ **Verify** style matches flat/vector aesthetic

## Step-by-Step Workflow

### Step 1: Understand the Request

**Questions to answer:**
- What type of asset? (character, item, prop, UI, effect)
- What size? (based on game world scale - see STYLE_GUIDE.md)
- What purpose? (collectible, decoration, functional)
- What colors? (check STYLE_GUIDE.md palette)
- Style requirements? (must match flat/vector style)

**Example:**
```
Request: "Need a health power-up sprite"
→ Type: Item/collectible
→ Size: 48x48 or 64x64 (smaller than character)
→ Purpose: Collectible power-up
→ Colors: Red/green (health colors)
→ Style: Flat/vector, must match player sprite
```

### Step 2: Search Kenney Collection

**Use KENNEY_CATALOG.md to find relevant packs:**

1. **Check catalog** - Review pack index for likely candidates
2. **Browse spritesheets** - Use `spritesheet*.png` files for visual overview
3. **Browse Preview.png** - Alternative visual inspection
4. **Navigate to assets** - Find individual sprites in PNG/ folders

**Visual Browsing Strategy:**

**Method 1: Spritesheets (Recommended)**
```bash
# Find all spritesheets in a pack
find "/path/to/Kenney/2D assets/[Pack Name]" -name "spritesheet*.png"

# Example for Puzzle Assets:
find "/path/to/Kenney/2D assets/Puzzle Assets" -name "spritesheet*.png"
```

Then use **Read tool with visual inspection** to see all sprites in one image:
```python
Read("/path/to/spritesheet_items.png")
# Claude Vision can see all sprites at once!
```

**Method 2: Preview.png**
```bash
# Single preview image showing asset samples
ls "/path/to/Kenney/2D assets/[Pack Name]/Preview.png"
```

**Method 3: Individual PNGs** (when needed)
```bash
# Browse individual sprites
ls "/path/to/Kenney/2D assets/[Pack Name]/PNG/"
```

**Search locations by asset type:**

| Asset Type | Primary Packs | Browse Method |
|------------|---------------|---------------|
| Characters | Topdown Shooter | Spritesheet in `Spritesheet/` folder |
| Items/Collectibles | Generic Items, Puzzle Assets | Spritesheet or Preview.png |
| Power-ups | Space Shooter Redux, Puzzle Assets | Check spritesheet_items.png |
| UI Elements | Game Icons, UI Pack | Preview.png (no spritesheets) |
| Props/Environment | Topdown Shooter, Generic Items | Spritesheet in pack |
| Effects | Explosion Pack, Particle Pack | Spritesheet for each effect type |

**Spritesheet File Patterns:**
```
spritesheet_complete.png    - All assets in pack
spritesheet_items.png        - Just items
spritesheet_characters.png   - Just characters
spritesheet_tiles.png        - Just tiles
spritesheet_enemies.png      - Just enemies
```

**Quick search workflow:**
```bash
# 1. Find relevant pack
ls "/path/to/Kenney/2D assets/" | grep -i "puzzle"

# 2. Check for spritesheets
find "/path/to/Kenney/2D assets/Puzzle Assets" -name "spritesheet*.png"

# 3. Visual inspect with Read tool
Read("/path/to/Kenney/2D assets/Puzzle Assets/Spritesheet/spritesheet_items.png")

# 4. If found what you need, navigate to individual PNG
ls "/path/to/Kenney/2D assets/Puzzle Assets/PNG/"
```

### Step 3: Evaluate Candidates

**For each candidate asset:**

✅ **Style Match:**
- Flat/vector (NOT pixel art)?
- Smooth rounded shapes?
- Thin dark outline?
- Simple geometric forms?

✅ **Color Match:**
- Uses game palette?
- Can be easily recolored if needed?
- Fits visual theme?

✅ **Size Match:**
- Appropriate game world scale?
- Can be resized to tile multiples (64, 96, 128, 192, 256)?
- Maintains quality at target size?

✅ **Purpose Match:**
- Communicates intended meaning?
- Clear silhouette/icon?
- Works in gameplay context?

**Decision tree:**
```
Found perfect match → Use it (Step 4)
Found close match  → Use and modify colors if needed (Step 4)
No good match      → Ask user to provide asset (Step 5)
```

### Step 4: Use Kenney Asset

If suitable asset found:

1. **Identify exact sprite** from spritesheet visual inspection

2. **Navigate to individual PNG:**
   ```bash
   ls "/path/to/Kenney/[Pack]/PNG/[Category]/"
   # Find the specific sprite file
   ```

3. **Copy asset** from Kenney folder to project:
   ```bash
   cp "Kenney/path/to/sprite.png" "assets/sprites/sprite_name.png"
   ```

4. **Resize if needed** (maintain aspect ratio):
   ```bash
   # Use ImageMagick or similar
   magick sprite.png -resize 64x64 output.png
   ```

5. **Verify transparency** - Check alpha channel present

6. **Test in-game** - Place alongside existing sprites

7. **Document source** - Note which Kenney pack it came from

**Output to user:**
```
✅ Found Kenney asset: [Asset Name]
📁 Source: [Pack Name]
📏 Size: [Original] → [Scaled to]
🎨 Colors: [Matches palette]
💾 Saved to: assets/sprites/[filename]
```

### Step 5: Ask User to Provide Asset

Only if no suitable Kenney asset exists:

1. **Report search results** - Explain what was searched and why nothing matched

2. **Ask user to provide asset:**

   **Output to user:**
   ```
   ❌ No suitable Kenney asset found for: [asset description]

   📁 Searched packs:
   - [Pack 1] - [why didn't match]
   - [Pack 2] - [why didn't match]

   🎨 Style requirements for manual creation:
   - Flat/vector style (NOT pixel art)
   - Smooth rounded shapes with thin dark outline
   - Simple geometric forms, clear silhouette
   - Transparent background (PNG with alpha)
   - Size: [recommended dimensions]
   - Colors: [recommended from palette]

   ✅ Options:
   1. Find similar Kenney asset from different pack
   2. Generate manually with AI tool of your choice
   3. Create/edit sprite with image editor
   4. Use placeholder colored circle for now

   📥 Once created, save to: assets/sprites/[filename]
   ```

3. **Suggest placeholder** - Offer to use colored circle fallback

4. **Wait for user** - Don't proceed until asset is provided

### Step 6: Quality Verification

**⚠️ CRITICAL REQUIREMENT: Always use Read tool with Claude Vision to visually inspect sprites!**

Never assume a sprite matches requirements without visual confirmation. AI generators can produce unexpected results.

**Visual verification checklist:**

1. **VERIFY ACTUAL CONTENT** - Does the image show what it's supposed to? (e.g., lightning bolt vs pentagon star)
2. **Compare to references** - Side-by-side with player/zombie sprite
3. **Check style** - Flat/vector vs pixel art
4. **Verify transparency** - Alpha channel present? (look for gray checkerboard pattern)
5. **Inspect edges** - Smooth anti-aliased edges?
6. **Check colors** - Within palette?
7. **Test readability** - Clear at target size?

**Style consistency checklist:**
- [ ] Smooth rounded shapes (not pixelated)
- [ ] Thin dark outline
- [ ] Flat colors with subtle gradients
- [ ] Simple geometric forms
- [ ] Transparent background
- [ ] Matches player/zombie style
- [ ] Appropriate scale
- [ ] Clear silhouette

**If quality issues found:**
```
For Kenney assets:
→ Try different asset from same pack
→ Try similar pack with better style match

For user-provided assets:
→ Give feedback on style mismatch
→ Reference STYLE_GUIDE.md for requirements
→ Suggest specific improvements needed
```

## Advanced Features

### Batch Asset Requests

For multiple related assets:

1. **Group by type** - Characters, items, props, etc.
2. **Check spritesheet** - Visual overview of entire pack
3. **Extract all at once** - Batch copy from same pack
4. **Maintain consistency** - Same pack = same style

**When to use subagent instead:**
- Need 10+ assets from exploration
- Creating complete themed collection
- Batch generation with variations
- Complex multi-step asset pipeline

### Color Variations

If Kenney asset has wrong color:

1. **Load original** with image manipulation
2. **Hue shift** to target color
3. **Verify contrast** - Maintain readability
4. **Save variant** with descriptive name

```bash
# Example: shift green gem to blue
magick green_gem.png -modulate 100,100,180 blue_gem.png
```

### Style Transfer (Future)

When Layer.ai API becomes available:
- Upload Kenney reference
- Generate matching style assets
- Batch process for consistency

## Templates and Resources

Quick references:

- **KENNEY_CATALOG.md** - Asset pack index and search tips
- **STYLE_GUIDE.md** - Visual style specifications
- **EXAMPLES.md** - Real workflow walkthroughs
- **templates/pollinations_prompts.md** - Generation templates
- **templates/midjourney_prompts.md** - Moodboard prompts
- **templates/quality_checklist.md** - Verification criteria

## Common Scenarios

### Scenario 1: Power-Up Sprites

**Request:** "Need health, speed, shield power-up sprites"

**Workflow:**
1. Check KENNEY_CATALOG.md → "Puzzle Assets has colored gems!"
2. Find spritesheet: `find "Puzzle Assets" -name "spritesheet*.png"`
3. Visual inspect spritesheet with Read tool → See all gems at once
4. Navigate to PNG folder, copy: green gem, blue gem, gold gem
5. Resize all to 64x64
6. Test in-game alongside player sprite
7. ✅ Done - all from Kenney, no generation needed

### Scenario 2: Custom Enemy Character

**Request:** "Need a flying zombie enemy sprite"

**Workflow:**
1. Check Topdown Shooter spritesheet → Has zombies, but no flying variant
2. Check Space Shooter Redux spritesheet → Has flying enemies, but wrong theme
3. **Decision:** Asset not found in Kenney
4. Report to user:
   ```
   ❌ No flying zombie found in Kenney collection

   📁 Searched: Topdown Shooter (has zombies), Space Shooter Redux (has flying)

   ✅ Options:
   1. Use regular zombie sprite as placeholder
   2. Modify existing zombie sprite with wings manually
   3. Generate externally with: "flying zombie, top-down view, Kenney flat vector style"

   📥 Save to: assets/sprites/flying_zombie.png
   ```
5. Wait for user to provide asset
6. Once provided, visually inspect with Read tool
7. Verify style matches existing zombie

### Scenario 3: Environment Props

**Request:** "Need trees, bushes, rocks for environment"

**Workflow:**
1. Check Kenney catalog → Multiple options
2. Visual inspect `Topdown Shooter/Spritesheet/` spritesheets
3. Check `Foliage Pack/Spritesheet/` spritesheets
4. Extract several options from PNG folders
5. Resize to appropriate scale (trees 64x128, bushes 64x64)
6. Test variety in-game
7. ✅ Multiple Kenney assets, instant variety

## Error Handling

### Common Issues

**No suitable Kenney asset found:**
→ Search related packs (check KENNEY_CATALOG.md)
→ Try similar assets that can be modified
→ Ask user to provide custom asset

**User-provided asset doesn't match style:**
→ Give clear feedback on what's wrong
→ Reference STYLE_GUIDE.md requirements
→ Provide example Kenney asset for comparison
→ Suggest specific style adjustments needed

**Kenney asset wrong size:**
→ Resize maintaining aspect ratio
→ Use multiples of 16px (64, 96, 128, 192, 256)
→ Verify quality after resize

**Colors don't match palette:**
→ Hue shift existing asset
→ Find alternative in same pack
→ Generate with specific color hex codes

## Tips for Success

✅ **Always check Kenney exhaustively** - 90% of needs covered
✅ **Use spritesheet files** - See entire pack at once with visual inspection
✅ **Use Preview.png files** - Alternative quick browse method
✅ **Search multiple related packs** - Don't give up after one pack
✅ **Maintain style consistency** - Flat/vector throughout
✅ **Verify in-game** - Test alongside existing sprites
✅ **Document sources** - Track which pack assets came from
✅ **Keep aspect ratios** - Don't stretch/squash
✅ **Use tile-based sizing** - Multiples of 64px base unit

❌ **Don't mix styles** - No pixel art with vector art
❌ **Don't give up too quickly** - Search thoroughly before asking user
❌ **Don't ignore scale** - Size relative to characters matters
❌ **Don't forget transparency** - All sprites need alpha channel
❌ **Don't generate with tokens** - Save tokens, use Kenney only

## Output Format

When completing an asset request:

```markdown
## Asset Request: [Asset Name]

**Source:** [Kenney Pack Name] OR [User Provided]
**File Path:** assets/sprites/[filename]
**Size:** [dimensions] ([X tiles])
**Style Match:** ✅ Verified / ⚠️ Needs review
**Notes:** [Any special considerations]

[Visual preview if using Read tool]
```

## When to Recommend Subagent Instead

Suggest using a subagent for:
- **Batch exploration:** "Catalog all enemy sprites in Kenney packs"
- **Complex generation:** "Create 8-frame walk animation for new character"
- **Style redesign:** "Redesign all UI in cyberpunk theme"
- **Asset pipeline:** "Generate 20 weapon variations with stats"

**How to suggest:**
```
For this complex task, I recommend using a subagent:
- Run: `Task tool with subagent_type=Explore` for thorough pack search
- OR: Create custom subagent for batch generation workflow
This allows autonomous exploration and decision-making.
```

## Remember

**Kenney ONLY - no token-expensive generation!**

The goal is to maximize use of professional CC0 assets while maintaining visual consistency. If Kenney doesn't have it, ask the user to provide it manually to save tokens.
