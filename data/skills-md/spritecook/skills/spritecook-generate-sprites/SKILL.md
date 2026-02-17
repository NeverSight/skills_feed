---
name: spritecook-generate-sprites
description: Generate sprites and game assets using the SpriteCook MCP tools. Use when building games and the user needs sprites, pixel art, detailed art, characters, items, tilesets, textures, icons, or UI elements. Also use when asked to create, generate, or make game art assets.
---

# SpriteCook - AI Game Asset Generator

Use SpriteCook MCP tools when the user needs pixel art, detailed/HD sprites, game assets, icons, tilesets, textures, or UI elements for a game project. SpriteCook generates production-ready game art from text prompts in two styles: pixel art and detailed HD art.

**Requires:** SpriteCook MCP server connected to your editor. Set up with `npx spritecook-mcp setup` or see [spritecook.ai](https://spritecook.ai).

## When to Use

- User asks to generate, create, or make sprites, pixel art, detailed art, game assets, or icons
- User is building a game and needs visual assets (characters, items, environments, UI)
- User references sprites, pixel art, HD art, or game art in their request
- A game project needs consistent visual assets across multiple types

## Available Tools

### generate_game_art

Generate game art assets from a text prompt. Supports both pixel art and detailed/HD styles. Waits up to 90s for result, returns download URLs.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string (required) | - | What to generate. Be specific: subject, pose, view angle |
| `width` | int | 64 | Width in pixels (16-512) |
| `height` | int | 64 | Height in pixels (16-512) |
| `variations` | int | 1 | Number of variations (1-4) |
| `pixel` | bool | true | True for pixel art, false for detailed/HD art |
| `bg_mode` | string | "transparent" | "transparent", "white", or "include" |
| `theme` | string | null | Art theme context, e.g. "dark fantasy medieval" |
| `style` | string | null | Style direction, e.g. "16-bit SNES style" |
| `aspect_ratio` | string | "1:1" | "1:1", "16:9", or "9:16" |
| `smart_crop` | bool | true | Auto-crop to content bounds (see note below) |
| `smart_crop_mode` | string | "tightest" | "tightest" (smallest fit) or "power_of_2" (32, 64, 128...) |
| `model` | string | null | "gemini-2.5-flash-image" (default) or "gemini-3-pro-image-preview" (higher quality, 2x credit cost) |
| `mode` | string | "assets" | "assets", "texture", or "ui" |
| `resolution` | string | "1K" | "1K", "2K", or "4K" |
| `colors` | string[] | null | Hex color palette, max 8 (e.g. ["#2D1B2E", "#FF6B35"]) |
| `reference_asset_id` | string | null | Asset ID from a previous generation to use as style reference |
| `edit_asset_id` | string | null | Asset ID to edit/modify with the new prompt |

`reference_asset_id` and `edit_asset_id` are mutually exclusive. The referenced asset must belong to your account. Use `reference_asset_id` to maintain visual consistency across assets.

**Note on output dimensions:** When `pixel=true`, pixel-perfect grid alignment is applied automatically for clean pixel art. The final sprite content may not fill the exact requested canvas size. When `smart_crop` is enabled, the output is trimmed to fit the content. In `"tightest"` mode (default), a 64x64 request might return a 54x54 image. In `"power_of_2"` mode, it snaps to the nearest power of 2 (32, 64, 128...), so 64x64 stays 64x64.

## Pixel Art vs Detailed Art

SpriteCook supports two art styles controlled by the `pixel` parameter:

**Pixel art** (`pixel: true`, default):
- Crisp hard edges, no anti-aliasing, visible pixel grid
- Automatic pixel-perfect post-processing for clean grid alignment
- Best for: retro games, indie games, 8-bit/16-bit style projects
- Typical sizes: 16-128px for sprites, up to 256px for tilesets

**Detailed/HD art** (`pixel: false`):
- Smooth gradients, fine detail, anti-aliased edges
- Higher fidelity output without pixel grid constraints
- Best for: HD 2D games, concept art, marketing assets, higher-resolution projects
- Typical sizes: 128-512px for sprites, larger for backgrounds

Choose based on the game's art direction. When the user doesn't specify, default to pixel art. If they mention "HD", "detailed", "high-res", "realistic", or "smooth", use `pixel: false`.

## Model Selection

Both pixel art and detailed mode default to `gemini-2.5-flash-image` (fast, good quality). You can optionally set the `model` parameter:

- **`gemini-2.5-flash-image`** (default): Fast generation, good quality, standard credit cost.
- **`gemini-3-pro-image-preview`**: Higher quality results with more detail and consistency, but costs 2x credits. Use when the user wants the best possible output or when standard results aren't meeting expectations.

### check_job_status

Check progress and get results of a generation job by `job_id`. Returns asset download URLs when complete.

### get_credit_balance

Check remaining credits, subscription tier, and concurrent job limit on the connected account. Use this before batch generating to know how many credits you have and how many jobs you can run at once.

## Downloading Assets

Each generated asset in the response includes a `pixel_url` (direct download link). Use this URL to download and save the PNG file into your project.

**PowerShell:**
```powershell
Invoke-WebRequest -Uri $pixel_url -OutFile "assets/sprite.png"
```

**Bash / macOS:**
```bash
curl -sL -o "assets/sprite.png" "$pixel_url"
```

Use the asset's `display_name` or `id` to create a meaningful filename. The URLs are temporary (expire after ~1 hour), so download promptly after generation.

## Autonomous Workflow

When a user is building a game, proactively identify and generate needed assets. Follow this pattern:

1. **Check credits** with `get_credit_balance` before generating. Note the `concurrent_jobs` field - this is how many jobs you can run at the same time. Generate assets sequentially (one at a time) unless your limit allows parallel generation.
2. **Identify required assets** from the game description (characters, items, tiles, UI, icons)
3. **Decide pixel vs detailed** based on the game's art style or the user's preference
4. **Generate a hero asset first** (e.g. the main character) to establish the art style
5. **Use `reference_asset_id`** with the hero asset's ID for subsequent generations to maintain visual consistency
6. **Download the assets** from the `pixel_url` in each result and save the PNG files into the project's asset directory
7. **Reference the saved files** in the game code

Example: User says "make a fishing game" -> check credits -> generate the player character first -> use that asset ID as `reference_asset_id` for fish, rod, boat, etc. -> all assets share the same art style -> download and place in project.

Use `edit_asset_id` when the user wants to iterate on a specific asset (e.g. "make the sword larger" or "change the color of the helmet").

If you receive a 429 error (concurrent job limit), wait for the active job to complete before submitting the next one.

## Asset Type Tips

| Asset Type | Recommended Settings |
|------------|---------------------|
| Pixel Characters | width: 64-128, bg_mode: "transparent", pixel: true |
| Pixel Items/Icons | width: 32-64, bg_mode: "transparent", pixel: true |
| Pixel Tilesets | width: 128-256, mode: "texture", bg_mode: "include", pixel: true |
| HD Characters | width: 256-512, bg_mode: "transparent", pixel: false |
| HD Items/Icons | width: 128-256, bg_mode: "transparent", pixel: false |
| HD Backgrounds | width: 512, aspect_ratio: "16:9", bg_mode: "include", pixel: false |
| UI Elements | width: 64-256, mode: "ui", bg_mode: "transparent" |
| Backgrounds | width: 256-512, aspect_ratio: "16:9", bg_mode: "include" |

- Be specific in prompts: "a red dragon breathing fire, side view, single sprite" beats "dragon"
- Use `reference_asset_id` to keep consistent art style across all assets in a project
- Use `theme` and `colors` for additional style and palette consistency
- Set `variations: 2-3` when you want options to pick from
- Use `edit_asset_id` to refine or modify existing assets
