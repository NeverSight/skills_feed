---
name: sirv-ai-studio
description: Guide for using Sirv AI Studio (www.sirv.studio), an AI-powered image and video processing platform. Use when working with product images, background removal, image upscaling, AI generation, video creation, batch processing, or e-commerce image workflows. Triggers on mentions of Sirv AI Studio, product photography, background removal, image upscaling, AI image generation, batch image processing, or marketplace optimization. IMPORTANT - If sirv-ai MCP tools are available (sirv_remove_background, sirv_upscale, sirv_generate, etc.), USE THEM directly for image processing tasks instead of telling user to visit the website.
---

# Sirv AI Studio

## IMPORTANT: Use MCP Tools When Available

**Before telling users to visit sirv.studio, CHECK if you have access to sirv-ai MCP tools.** If tools like `sirv_remove_background`, `sirv_upscale`, `sirv_generate` are available, USE THEM DIRECTLY to process images.

### MCP Tool Quick Reference

| Task | MCP Tool | Key Parameters |
|------|----------|----------------|
| Remove background | `sirv_remove_background` | `image_url`, `model` |
| Replace background | `sirv_background_replace` | `image_url`, `prompt` |
| Upscale image | `sirv_upscale` | `image_url`, `scale` (2-4) |
| Generate image | `sirv_generate` | `prompt`, `aspect_ratio` |
| Lifestyle scene | `sirv_product_lifestyle` | `image_url`, `scene_description` |
| Virtual try-on | `sirv_virtual_try_on` | `person_image_url`, `garment_image_url` |
| Get alt text | `sirv_alt_text` | `image_url` |
| Batch remove BG | `sirv_batch_remove_background` | `images` array |
| Check credits | `sirv_get_usage` | none |

### If MCP Tools Are NOT Available

Help the user install the Sirv AI MCP server. Add to project `.mcp.json` or `~/.claude.json`:

```json
{
  "mcpServers": {
    "sirv-ai": {
      "command": "npx",
      "args": ["-y", "sirv-ai-mcp-server"],
      "env": {
        "SIRV_AI_BASE_URL": "https://www.sirv.studio"
      }
    }
  }
}
```

Then restart Claude Code. User will need to authorize with their Sirv AI Studio account on first use.

**Only direct users to www.sirv.studio if they don't want to set up MCP.**

---

## Web UI (Fallback)

If MCP tools are not available, users can access Sirv AI Studio at www.sirv.studio:

1. Upload image(s) via drag-drop or URL
2. Select tool from sidebar
3. Configure options
4. Click Process
5. Download or auto-upload to Sirv CDN

## Core Tools

### Background Processing

| Tool | Credits | Use Case |
|------|---------|----------|
| Background Removal | 1-2 | Product cutouts, transparent PNG |
| Background Replace | 3-4 | New backgrounds via prompt or image |
| Object Removal | 3 | Remove unwanted elements with mask |

**Background Removal Models:**
- BiRefNet v1/v2: Fast, multiple presets (Light, Heavy, Portrait, Matting)
- Bria: Premium quality alternative

**Background Replace Models:**
- Bria: Text prompt or reference image
- FLUX Kontext: Advanced with consistency
- Nano Banana: Faster alternative

### Image Enhancement

| Tool | Credits | Use Case |
|------|---------|----------|
| Upscaling | 1-32 | Increase resolution up to 8x |
| FLUX 2 Edit | 3 | Natural language editing |
| Reve Fast Edit | 1 | Quick prompt-based edits |

**Upscaling Models:**
- ESRGAN: Fast, affordable (1-2 credits, up to 8x)
- Clarity: AI-enhanced with prompts (8+ credits)
- Topaz: Premium quality (8-136 credits)

### Image Generation

| Tool | Credits | Use Case |
|------|---------|----------|
| FLUX 2 | 2 | High-quality text-to-image |
| Z-Image | 2 | Affordable alternative |
| Gemini Pro | 15-30 | Advanced generation |
| Seedream | 2 | Creative/artistic styles |

Supports: 1-4 images per generation, multiple aspect ratios, up to 2048x2048

### Product Tools

| Tool | Credits | Use Case |
|------|---------|----------|
| Product Lifestyle | 3-15 | Product in lifestyle scenes |
| Virtual Try-On | 4 | Garment on person |
| Try-On Video | 11 | Animated try-on |
| Color Variants | 2+/color | Product in multiple colors |
| Alt Text | 1 | AI-generated descriptions |
| Product Description | 1 | Marketing copy (12+ languages) |

**Lifestyle Scenes:** 44 presets (kitchen, office, beach, etc.) or custom prompts

### 3D Generation

| Tool | Credits | Use Case |
|------|---------|----------|
| Meshy v6 | 50 | Single image to 3D |
| Meshy v5 Multi | 25 | Multi-angle input |
| Seed3D/Trellis | 25-50 | Alternative models |

**Output formats:** GLB, OBJ, FBX, USDZ, Blend, STL with PBR textures

### Video Tools

| Tool | Credits | Use Case |
|------|---------|----------|
| LTX 2.0 | 6-24/sec | Up to 4K, 6-10 seconds |
| Kling 2.6 | 6-24/sec | 1080p with speech synthesis |
| Veo 3.1 | 6-24/sec | High quality generation |
| Captions | Variable | Multi-language transcription |

### Free Tools

- **Depth Map**: Generate depth data for 3D/AR effects
- **Image Optimizer**: 17 social media presets, resize/crop/convert
- **Smart Crop**: Intelligent cropping for platforms

## Batch Processing

Process multiple images simultaneously:

1. Upload batch via drag-drop or URL import
2. Configure shared settings
3. Preview results before processing
4. Download ZIP or auto-upload to Sirv

**Available batch tools:**
- Batch Background Removal
- Batch Upscale
- Batch Generate
- Batch Product Lifestyle
- Batch Background Replace
- Batch Alt Text
- Batch Image Translation

**Limits by tier:**
- Free: No batch
- Starter: 100 images
- Pro: 500 images
- Business: 1,500 images
- Volume+: Unlimited

## Workflow Builder (Orchestrator)

Visual DAG pipeline builder for multi-step operations:

**Capabilities:**
- Chain tools: Remove BG → Upscale → Lifestyle → Alt Text
- AI routing: Classify images → branch to different pipelines
- Quality loops: Review → Autofix → Final Review
- Multi-source: Combine images from different inputs

**Example workflows:**
- Amazon-Ready: Remove BG → Validate → Autofix → Alt text
- Fashion: Ghost mannequin → Remove BG → Shadow → Bundle
- Color Variants: Remove BG → Generate colors → Review

## Credit System

### Pricing Tiers

| Tier | Price | Credits | Batch | History |
|------|-------|---------|-------|---------|
| Free | $0 | 15 | 0 | 7 days |
| Starter | $9/mo | 150 | 100 | 30 days |
| Pro | $29/mo | 600 | 500 | 90 days |
| Business | $79/mo | 1,800 | 1,500 | Unlimited |
| Volume+ | $199+/mo | 5K-250K | Unlimited | Unlimited |

### Credit Packs (One-time)

- 50 credits: $4.99
- 100 credits: $9.99
- 500 credits: $39.99
- 1,000 credits: $69.99
- 2,500 credits: $149.99

Bonus credits on top-ups: Free 0%, Starter 5%, Pro 10%, Business 15%, Volume+ 20%

## Sirv CDN Integration

Connect Sirv account for:
- Browse Sirv library in app
- Auto-upload processed images
- Per-tool upload destinations (e.g., `/products/cutouts/`)
- Instant global CDN delivery
- Shopify integration sync

**Sirv plan bonuses:**
- Business: +50 credits
- Enterprise: +150 credits

## Integrations

| Platform | Use Case |
|----------|----------|
| Shopify | Browse products, auto-push results |
| Zapier | Trigger processing from workflows |
| n8n | Self-hosted automation |
| Claude/ChatGPT MCP | Natural language image editing |
| REST API | Custom integrations |

## Quality Control

**Image Review Tool (1 credit):**
- Checks against marketplace rules
- Validates: dimensions, background, watermarks, frame fill
- Presets: Amazon, eBay, Shopify, Walmart

**Marketplace Optimizer:**
- Upload → Select marketplaces → Get compliance scorecard
- One-click fixes for all issues

## File Formats

**Input:** JPG, PNG, WebP, GIF, AVIF, HEIF, BMP, TIFF

**Output:** PNG, JPEG, WebP, GIF (images), MP4/WebM (video), GLB/OBJ/FBX/USDZ/STL (3D)

## Tips

- **Eager upload**: Files upload immediately on selection for faster processing
- **Hash caching**: Identical files skip re-upload
- **Soft delete**: Recover deleted assets from trash
- **Mobile**: Long-press for context menu actions
- **Shortcuts**: Use keyboard shortcuts in dashboard for power workflows

## MCP Server Integration

Sirv AI Studio provides an MCP (Model Context Protocol) server for AI assistants like Claude, enabling natural language image processing directly in conversations.

### Available MCP Tools

#### Background Processing

| Tool | Parameters | Cost |
|------|------------|------|
| `sirv_remove_background` | `image_url`, `provider` (birefnet/bria), `model`, `operating_resolution` | 1-2 |
| `sirv_background_replace` | `image_url`, `prompt`, `ref_image_url`, `model` (bria/flux-kontext/nano-banana) | 4 |
| `sirv_object_removal` | `image_url`, `mask_url` | 3 |

**Background Removal Models:**
- `General Use (Light)` - Fast processing
- `General Use (Light 2K)` - Fast, higher resolution
- `General Use (Heavy)` - Best quality (default)
- `Matting` - For hair/fur details
- `Portrait` - Optimized for people
- `General Use (Dynamic)` - Adaptive

**Operating Resolutions:** `1024x1024`, `2048x2048`, `2304x2304`

#### Image Enhancement

| Tool | Parameters | Cost |
|------|------------|------|
| `sirv_upscale` | `image_url`, `scale` (2-4), `model`, `prompt`, `creativity` | 2-3 |
| `sirv_image_to_image` | `image_url`, `prompt`, `strength` (0-1), `model` | 2-3 |

**Upscale Models:**
- `esrgan` - Fast, general purpose (default)
- `clarity` - AI-enhanced with prompt guidance
- `topaz` - Premium quality

**Image-to-Image Models:**
- `reve-fast-edit` - Quick prompt-based edits (default)
- `flux2-lora` - High quality transformations
- `qwen-integrate-product` - Product integration

#### Image Generation

| Tool | Parameters | Cost |
|------|------------|------|
| `sirv_generate` | `prompt`, `model`, `aspect_ratio`, `num_images` (1-4) | 2 |

**Generation Models:** `zimage` (fast), `flux2` (detailed), `gemini` (photorealistic), `seedream` (artistic)

**Aspect Ratios:** `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `21:9`

#### Product & E-commerce

| Tool | Parameters | Cost |
|------|------------|------|
| `sirv_product_lifestyle` | `image_url`, `scene_description`, `ref_image_url`, `placement_type`, `position`, `num_results` | 3-15 |
| `sirv_virtual_try_on` | `person_image_url`, `garment_image_url` | 4 |
| `sirv_alt_text` | `image_url`, `detail_level` | 1 |

**Placement Types:** `original`, `automatic` (default), `manual_placement`, `manual_padding`

**Positions:** `bottom_center`, `bottom_left`, `bottom_right`, `upper_center`, `upper_left`, `upper_right`, `center_vertical`, `center_horizontal`, `left_center`, `right_center`

**Alt Text Detail Levels:** `caption` (brief), `detailed-caption` (standard), `more-detailed-caption` (comprehensive)

#### 3D & Video

| Tool | Parameters | Cost |
|------|------------|------|
| `sirv_image_to_3d` | `image_url`, `model`, `topology`, `target_polycount`, `enable_pbr` | 80 |
| `sirv_video_generation` | `prompt`, `image_url`, `model`, `duration`, `resolution`, `aspect_ratio`, `generate_audio` | Variable |
| `sirv_depth_map` | `image_url` | FREE |

**3D Models:** `meshy` (default), `meshy-multi`, `seed3d`, `trellis`, `trellis2`, `hunyuan3d`

**Video Models:** `veo31` (default), `ltx`, `kling`, `sora`

**Video Resolutions:** `720p`, `1080p`, `1440p`, `2160p`

#### Batch Operations

| Tool | Parameters | Cost |
|------|------------|------|
| `sirv_batch_remove_background` | `images` (array of {id, image_url}), `model` | 1-2/image |
| `sirv_batch_upscale` | `images` (array of {id, image_url}), `scale`, `model` | 2-3/image |

**Batch Limits:** Up to 100 images per request

#### Account

| Tool | Parameters | Returns |
|------|------------|---------|
| `sirv_get_usage` | None | `used`, `remaining`, `total`, `tier` |

### MCP Usage Examples

**Remove background from a product image:**
```
"Remove the background from https://example.com/product.jpg using the Heavy model"
→ sirv_remove_background(image_url, model="General Use (Heavy)")
```

**Create lifestyle scene:**
```
"Place this product on a modern kitchen counter with morning light"
→ sirv_product_lifestyle(image_url, scene_description="Modern kitchen counter with morning light")
```

**Generate product variations:**
```
"Generate 4 images of a minimalist water bottle on white background"
→ sirv_generate(prompt="minimalist water bottle on white background", num_images=4)
```

**Upscale for print:**
```
"Upscale this image 4x using the Topaz model for print quality"
→ sirv_upscale(image_url, scale=4, model="topaz")
```

**Virtual try-on:**
```
"Show this dress on the model photo"
→ sirv_virtual_try_on(person_image_url, garment_image_url)
```

**Batch processing:**
```
"Remove backgrounds from all these product images"
→ sirv_batch_remove_background(images=[{id: "1", image_url: "..."}, ...])
```

**Check credits:**
```
"How many credits do I have left?"
→ sirv_get_usage()
```

### MCP Server Setup

**Claude Code (`.mcp.json` in project or `~/.claude.json` global):**
```json
{
  "mcpServers": {
    "sirv-ai": {
      "command": "npx",
      "args": ["-y", "sirv-ai-mcp-server"],
      "env": {
        "SIRV_AI_BASE_URL": "https://www.sirv.studio"
      }
    }
  }
}
```

Restart Claude Code after adding. Authorize with Sirv AI Studio account on first use.

### Best Practices

1. **Check usage first** - Use `sirv_get_usage` before large batch operations
2. **Use appropriate models** - Choose quality vs speed based on needs
3. **Batch when possible** - Use batch tools for multiple images to reduce overhead
4. **Provide clear prompts** - Detailed descriptions yield better results for generation/lifestyle
5. **Prepare images** - Remove backgrounds before lifestyle shots for best results
6. **Chain operations** - Remove BG → Upscale → Lifestyle for complete product workflows

## REST API Reference

Base URL: `https://www.sirv.studio/api/zapier`

All requests require: `Authorization: Bearer sk_live_YOUR_API_KEY`

### Endpoints

#### Account

```http
GET /me
```
Returns: `{id, email, credits, tier}`
Cost: FREE

#### Background Removal

```http
POST /remove-bg
Content-Type: application/json

{
  "image_url": "https://example.com/product.jpg",
  "model": "birefnet"
}
```
Returns: `{id, image_url, credits_used}`
Cost: 1-2 credits

**Models:** `birefnet` (default), `bria`

#### Image Upscaling

```http
POST /upscale
Content-Type: application/json

{
  "image_url": "https://example.com/image.jpg",
  "scale": 4,
  "model": "clarity"
}
```
Returns: `{id, image_url, credits_used}`
Cost: 1-8 credits

**Models:** `esrgan` (fast), `clarity` (AI-enhanced), `topaz` (premium)
**Scale:** 2, 3, or 4

#### Background Replacement

```http
POST /replace-bg
Content-Type: application/json

{
  "image_url": "https://example.com/product.jpg",
  "prompt": "Modern kitchen counter with marble surface",
  "model": "flux-kontext"
}
```
Cost: 3-15 credits

**Models:** `bria`, `flux-kontext`, `nano-banana`

#### Image-to-Image Transformation

```http
POST /image-to-image
Content-Type: application/json

{
  "image_url": "https://example.com/image.jpg",
  "prompt": "Transform to watercolor painting style",
  "strength": 0.7
}
```
Cost: 1-8 credits

**Strength:** 0-1 (how much to transform)

#### Image Generation

```http
POST /generate
Content-Type: application/json

{
  "prompt": "Professional product photo of wireless headphones",
  "model": "flux-kontext",
  "aspect_ratio": "1:1"
}
```
Returns: `{id, image_url, credits_used}`
Cost: 1-10 credits

**Models:** `flux-kontext`, `nano-banana`, `ideogram`, `zimage`, `gemini`, `seedream`
**Aspect ratios:** `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `21:9`

#### Video Generation

```http
POST /video-generation
Content-Type: application/json

{
  "prompt": "Product rotating on display stand",
  "image_url": "https://example.com/product.jpg",
  "model": "ltx",
  "duration": 5,
  "aspect_ratio": "16:9"
}
```
Cost: 10-80 credits

**Models:** `veo31`, `ltx`, `kling`, `sora`

#### 3D Model Generation

```http
POST /image-to-3d
Content-Type: application/json

{
  "image_url": "https://example.com/product.jpg",
  "model": "meshy",
  "topology": "quad",
  "enable_pbr": true
}
```
Returns: Multiple formats (glb, obj, fbx, usdz)
Cost: 2-50 credits

#### Alt Text Generation

```http
POST /alt-text
Content-Type: application/json

{
  "image_url": "https://example.com/image.jpg"
}
```
Cost: 1 credit

#### File Upload

```http
POST /upload
Content-Type: multipart/form-data

file: [binary data, max 10MB]
```
Cost: FREE

#### Batch Operations

```http
POST /batch/remove-bg
POST /batch/upscale
POST /batch/alt-text
Content-Type: application/json

{
  "images": [
    {"id": "1", "image_url": "https://example.com/img1.jpg"},
    {"id": "2", "image_url": "https://example.com/img2.jpg"}
  ],
  "model": "birefnet"
}
```

Check batch status:
```http
GET /batch/status/{jobId}
```

### Rate Limits

| Tier | Requests/Hour |
|------|---------------|
| Free | 20 |
| Pro | 500 |
| Business | 2,000 |

### Code Examples

#### JavaScript

```javascript
const SIRV_API = 'https://www.sirv.studio/api/zapier';
const API_KEY = 'sk_live_YOUR_API_KEY';

async function removeBackground(imageUrl) {
  const response = await fetch(`${SIRV_API}/remove-bg`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      image_url: imageUrl,
      model: 'birefnet'
    })
  });
  return (await response.json()).image_url;
}

async function generateImage(prompt, aspectRatio = '1:1') {
  const response = await fetch(`${SIRV_API}/generate`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      prompt,
      model: 'flux-kontext',
      aspect_ratio: aspectRatio
    })
  });
  return (await response.json()).image_url;
}
```

#### cURL

```bash
# Remove background
curl -X POST https://www.sirv.studio/api/zapier/remove-bg \
  -H "Authorization: Bearer sk_live_YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"image_url": "https://example.com/product.jpg", "model": "birefnet"}'

# Generate image
curl -X POST https://www.sirv.studio/api/zapier/generate \
  -H "Authorization: Bearer sk_live_YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Product photo of headphones", "model": "flux-kontext", "aspect_ratio": "1:1"}'

# Check credits
curl https://www.sirv.studio/api/zapier/me \
  -H "Authorization: Bearer sk_live_YOUR_API_KEY"
```
