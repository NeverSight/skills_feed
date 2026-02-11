---
name: bria-ai
description: Use when generating visual assets with Bria.ai - product photos, hero images, icons, backgrounds. Includes batch generation (multiple images concurrently), pipeline workflows (generate → edit → remove background), and parallel API patterns. Use for websites, presentations, e-commerce catalogs, or any task needing multiple AI-generated images.
---

# Bria Visual Asset Generator

Generate production-ready visual assets for websites, presentations, documents, and applications using Bria's commercially-safe AI models.

## When to Use This Skill

- **Website/App Development**: Hero images, product photos, backgrounds, illustrations
- **Presentations**: Slides visuals, diagrams, icons, cover images
- **Documents**: Report graphics, infographics, headers, decorative elements
- **Marketing**: Social media assets, banners, promotional images
- **E-commerce**: Product photography, lifestyle shots, catalog images
- **Batch Generation**: Multiple images with different prompts concurrently
- **Pipeline Workflows**: Chained operations (generate → edit → remove background → lifestyle shot)

## Core Capabilities

| Need | Capability | Use Case |
|------|------------|----------|
| Create new images | FIBO Generate | Hero images, product shots, illustrations |
| Edit by text | FIBO-Edit | Change colors, modify objects, transform scenes |
| Edit with mask | GenFill/Erase | Precise inpainting, add/replace specific regions |
| Add/Replace/Remove objects | Text-based editing | Add vase, replace apple with pear, remove table |
| Transparent backgrounds | RMBG-2.0 | Extract subjects for overlays, logos, cutouts |
| Background operations | Replace/Blur/Erase | Change, blur, or remove backgrounds |
| Expand images | Outpainting | Extend boundaries, change aspect ratios |
| Upscale images | Super Resolution | Increase resolution 2x or 4x |
| Enhance quality | Enhancement | Improve lighting, colors, details |
| Transform style | Restyle | Oil painting, anime, cartoon, 3D render |
| Change lighting | Relight | Golden hour, spotlight, dramatic lighting |
| Change season | Reseason | Spring, summer, autumn, winter |
| Blend/composite | Image Blending | Apply textures, logos, merge images |
| Text replacement | Rewrite | Change text in images |
| Restore photos | Restoration | Fix old/damaged photos |
| Colorize | Colorization | Add color to B&W, or convert to B&W |
| Sketch to photo | Sketch2Image | Convert drawings to realistic photos |
| Product photography | Lifestyle Shot | Place products in scenes |

## Quick Reference

### Generate an Image (FIBO)

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/generate" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "your description",
    "aspect_ratio": "16:9"
  }'
```

**Aspect ratios**: `1:1` (square), `16:9` (hero/banner), `4:3` (presentation), `9:16` (mobile/story), `3:4` (portrait)

> **Advanced**: For precise, deterministic control over generation, use **[VGL structured prompts](../vgl/SKILL.md)** instead of natural language. VGL defines every visual attribute (objects, lighting, composition) as explicit JSON.

### Remove Background (RMBG-2.0)

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/edit/remove_background" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"image": "https://..."}'
```

Returns PNG with transparency.

### Edit Image (FIBO-Edit) - No Mask Required

Edit any image with natural language instructions:

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/edit" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "images": ["https://..."],
    "instruction": "change the mug to red"
  }'
```

**Python example:**
```python
from bria_client import BriaClient
client = BriaClient()
result = client.edit_image(image_url, "change the mug to red")
print(result['result']['image_url'])
```

### Edit Image Region with Mask (FIBO-Edit)

For precise control over which region to edit:

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/edit/gen_fill" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "image": "https://...",
    "mask": "https://...",
    "prompt": "what to generate in masked area"
  }'
```

### Expand Image (Outpainting)

Extend image boundaries to new aspect ratio:

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/edit/expand" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "image": "base64-or-url",
    "aspect_ratio": "16:9",
    "prompt": "coffee shop background, wooden table"
  }'
```

### Upscale Image

Increase image resolution 2x or 4x:

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/edit/increase_resolution" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"image": "https://...", "scale": 2}'
```

### Product Lifestyle Shot

Place a product in a lifestyle scene:

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/edit/lifestyle_shot_by_text" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "image": "https://product-with-transparent-bg.png",
    "prompt": "modern kitchen countertop, natural morning light"
  }'
```

---

## Asset Generation Workflows

### Website Hero Images

Generate wide banner images for landing pages:

```json
{
  "prompt": "Modern tech startup workspace with developers collaborating, bright natural lighting, clean minimal aesthetic",
  "aspect_ratio": "16:9",
  "negative_prompt": "cluttered, dark, low quality"
}
```

**Tips for hero images:**
- Use `16:9` for full-width banners
- Describe lighting and mood explicitly
- Include "professional", "high quality", "commercial" for polished results
- Specify "clean background" or "minimal" for text overlay space

### Product Photography

Generate e-commerce style product shots:

```json
{
  "prompt": "Professional product photo of [item] on white studio background, soft shadows, commercial photography lighting",
  "aspect_ratio": "1:1"
}
```

**Then remove background** for transparent PNG to composite anywhere:

```json
{"image": "generated_image_url"}
```

### Presentation Visuals

Generate slides-ready images:

```json
{
  "prompt": "Abstract visualization of data analytics, blue and purple gradient, modern corporate style, clean composition with space for text",
  "aspect_ratio": "16:9"
}
```

**Common presentation themes:**
- "Abstract technology background" - tech slides
- "Business team collaboration" - culture slides
- "Growth chart visualization" - metrics slides
- "Minimalist geometric patterns" - section dividers

### Document Graphics

Generate report or article images:

```json
{
  "prompt": "Isometric illustration of cloud computing infrastructure, flat design, vibrant colors, white background",
  "aspect_ratio": "4:3"
}
```

### Icons and Illustrations

For icons, generate then remove background:

```json
{
  "prompt": "3D icon of a shield with checkmark, glossy material, soft gradient background, app icon style",
  "aspect_ratio": "1:1"
}
```

Then use RMBG-2.0 to get transparent PNG.

### Social Media Assets

**Instagram post (1:1):**
```json
{
  "prompt": "Lifestyle photo of coffee and laptop on wooden desk, morning light, cozy atmosphere",
  "aspect_ratio": "1:1"
}
```

**Story/Reel (9:16):**
```json
{
  "prompt": "Vertical product showcase of smartphone, floating in gradient background, tech aesthetic",
  "aspect_ratio": "9:16"
}
```

---

## Prompt Engineering Tips

### Be Specific About Style
- "professional product photography" vs "casual snapshot"
- "flat design illustration" vs "3D rendered"
- "corporate modern" vs "playful colorful"

### Specify Technical Details
- Lighting: "soft natural light", "studio lighting", "dramatic shadows"
- Background: "white studio", "gradient", "blurred office", "transparent"
- Composition: "centered", "rule of thirds", "negative space on left for text"

### Quality Keywords
Add these for polished results:
- "high quality", "professional", "commercial grade"
- "4K", "detailed", "sharp focus"
- "award-winning photography" (for photos)

### Negative Prompts
Exclude unwanted elements:
- "blurry, low quality, pixelated"
- "text, watermark, logo"
- "cluttered, busy, messy"

---

## Async Response Handling

All endpoints return async responses:

```json
{
  "request_id": "uuid",
  "status_url": "https://engine.prod.bria-api.com/v2/status/uuid"
}
```

Poll the status_url until `status: "COMPLETED"`, then get `result.image_url`.

```python
import requests, time

def get_result(status_url, api_key):
    while True:
        r = requests.get(status_url, headers={"api_token": api_key})
        data = r.json()
        if data["status"] == "COMPLETED":
            return data["result"]["image_url"]
        if data["status"] == "FAILED":
            raise Exception(data.get("error"))
        time.sleep(2)
```

---

## Batch & Parallel Image Generation

### Generating Multiple Images Concurrently

For generating many images efficiently, launch requests in parallel and poll concurrently:

```python
import asyncio
import aiohttp

async def generate_image(session, api_key, prompt, aspect_ratio="1:1"):
    """Launch a single generation request."""
    async with session.post(
        "https://engine.prod.bria-api.com/v2/image/generate",
        headers={"api_token": api_key, "Content-Type": "application/json"},
        json={"prompt": prompt, "aspect_ratio": aspect_ratio}
    ) as resp:
        return await resp.json()

async def poll_status(session, api_key, status_url, timeout=120):
    """Poll until complete or failed."""
    for _ in range(timeout // 2):
        async with session.get(status_url, headers={"api_token": api_key}) as resp:
            data = await resp.json()
            if data["status"] == "COMPLETED":
                return data["result"]["image_url"]
            if data["status"] == "FAILED":
                raise Exception(data.get("error", "Generation failed"))
        await asyncio.sleep(2)
    raise TimeoutError(f"Timeout polling {status_url}")

async def generate_batch(api_key, prompts, aspect_ratio="1:1", max_concurrent=5):
    """Generate multiple images with different prompts concurrently."""
    semaphore = asyncio.Semaphore(max_concurrent)  # Rate limiting

    async def generate_one(prompt):
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                # Launch request
                result = await generate_image(session, api_key, prompt, aspect_ratio)
                # Poll for completion
                return await poll_status(session, api_key, result["status_url"])

    # Run all concurrently
    results = await asyncio.gather(*[generate_one(p) for p in prompts], return_exceptions=True)
    return results

# Usage
prompts = [
    "Professional photo of running shoes on white background",
    "Professional photo of leather handbag on white background",
    "Professional photo of smartwatch on white background",
    "Professional photo of sunglasses on white background",
]
image_urls = asyncio.run(generate_batch("YOUR_API_KEY", prompts, max_concurrent=3))
```

**Key points:**
- Use `asyncio.Semaphore` to limit concurrent requests (recommended: 3-5)
- `return_exceptions=True` prevents one failure from canceling all requests
- Each result is either a URL string or an Exception object

### TypeScript/Node.js Parallel Generation

```typescript
type AspectRatio = "1:1" | "4:3" | "16:9" | "3:4" | "9:16";

interface BriaResponse {
  request_id: string;
  status_url: string;
}

interface BriaStatusResponse {
  status: "IN_PROGRESS" | "COMPLETED" | "FAILED";
  result?: { image_url: string };
  error?: string;
}

interface GenerateBatchResult {
  prompt: string;
  imageUrl: string | null;
  error: string | null;
}

async function generateBatch(
  apiKey: string,
  prompts: string[],
  aspectRatio: AspectRatio = "1:1",
  maxConcurrent = 5
): Promise<GenerateBatchResult[]> {
  const semaphore = { count: 0, max: maxConcurrent };

  async function withLimit<T>(fn: () => Promise<T>): Promise<T> {
    while (semaphore.count >= semaphore.max) {
      await new Promise(r => setTimeout(r, 100));
    }
    semaphore.count++;
    try {
      return await fn();
    } finally {
      semaphore.count--;
    }
  }

  async function generateOne(prompt: string): Promise<string> {
    return withLimit(async () => {
      // Launch request
      const res = await fetch("https://engine.prod.bria-api.com/v2/image/generate", {
        method: "POST",
        headers: { "api_token": apiKey, "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, aspect_ratio: aspectRatio })
      });
      const { status_url } = (await res.json()) as BriaResponse;

      // Poll for result
      for (let i = 0; i < 60; i++) {
        const statusRes = await fetch(status_url, { headers: { "api_token": apiKey } });
        const data = (await statusRes.json()) as BriaStatusResponse;
        if (data.status === "COMPLETED") return data.result!.image_url;
        if (data.status === "FAILED") throw new Error(data.error || "Generation failed");
        await new Promise(r => setTimeout(r, 2000));
      }
      throw new Error("Timeout waiting for generation");
    });
  }

  const results = await Promise.allSettled(prompts.map(generateOne));

  return results.map((result, i) => ({
    prompt: prompts[i],
    imageUrl: result.status === "fulfilled" ? result.value : null,
    error: result.status === "rejected" ? result.reason.message : null
  }));
}

// Usage
const results = await generateBatch(process.env.BRIA_API_KEY!, [
  "Modern office workspace with natural lighting",
  "Abstract tech background with blue gradient",
  "Professional headshot studio setup"
], "16:9", 3);

results.forEach(r => {
  if (r.imageUrl) console.log(`✓ ${r.prompt}: ${r.imageUrl}`);
  else console.log(`✗ ${r.prompt}: ${r.error}`);
});
```
```

---

## Pipeline Workflows

Chain multiple operations on images (generate → edit → remove background).

### Complete Pipeline Example

```python
async def product_pipeline(api_key, product_descriptions, scene_prompt):
    """
    Pipeline: Generate product → Remove background → Place in lifestyle scene
    """
    async with aiohttp.ClientSession() as session:
        results = []

        for desc in product_descriptions:
            # Step 1: Generate product image
            gen_result = await generate_image(session, api_key,
                f"Professional product photo of {desc} on white background, studio lighting",
                aspect_ratio="1:1")
            product_url = await poll_status(session, api_key, gen_result["status_url"])

            # Step 2: Remove background
            async with session.post(
                "https://engine.prod.bria-api.com/v2/image/edit/remove_background",
                headers={"api_token": api_key, "Content-Type": "application/json"},
                json={"image": product_url}
            ) as resp:
                rmbg_result = await resp.json()
            transparent_url = await poll_status(session, api_key, rmbg_result["status_url"])

            # Step 3: Place in lifestyle scene
            async with session.post(
                "https://engine.prod.bria-api.com/v2/image/edit/lifestyle_shot_by_text",
                headers={"api_token": api_key, "Content-Type": "application/json"},
                json={"image": transparent_url, "prompt": scene_prompt}
            ) as resp:
                lifestyle_result = await resp.json()
            final_url = await poll_status(session, api_key, lifestyle_result["status_url"])

            results.append({
                "product": desc,
                "original": product_url,
                "transparent": transparent_url,
                "lifestyle": final_url
            })

        return results

# Usage
products = ["coffee mug", "water bottle", "notebook"]
scene = "modern minimalist desk, natural morning light, plants in background"
results = asyncio.run(product_pipeline("YOUR_API_KEY", products, scene))
```

### Parallel Pipeline (Advanced)

Process multiple products through the pipeline concurrently:

```python
async def parallel_pipeline(api_key, products, scene_prompt, max_concurrent=3):
    """Run full pipeline for multiple products in parallel."""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def process_one(product):
        async with semaphore:
            return await single_product_pipeline(api_key, product, scene_prompt)

    return await asyncio.gather(*[process_one(p) for p in products], return_exceptions=True)
```

### Common Pipeline Patterns

| Pipeline | Steps | Use Case |
|----------|-------|----------|
| Product → Transparent | generate → remove_background | E-commerce cutouts |
| Product → Lifestyle | generate → remove_background → lifestyle_shot | Marketing photos |
| Edit → Upscale | edit → increase_resolution | High-res edited images |
| Generate → Restyle | generate → restyle | Artistic variations |
| Generate → Variations | generate (num_results=4) | A/B testing options |

---

## Integration Examples

### React/Next.js Component

```jsx
// Generate and display a hero image
const [imageUrl, setImageUrl] = useState(null);

async function generateHero(prompt) {
  const res = await fetch('/api/bria/generate', {
    method: 'POST',
    body: JSON.stringify({ prompt, aspect_ratio: '16:9' })
  });
  const { image_url } = await res.json();
  setImageUrl(image_url);
}
```

### Python Script for Batch Generation

```python
import asyncio

# See "Batch & Parallel Image Generation" section for generate_batch function

async def main():
    api_key = "YOUR_API_KEY"
    products = ["running shoes", "leather bag", "smart watch"]
    prompts = [f"Professional product photo of {p} on white background" for p in products]

    results = await generate_batch(api_key, prompts, aspect_ratio="1:1", max_concurrent=3)

    for product, result in zip(products, results):
        if isinstance(result, Exception):
            print(f"{product}: FAILED - {result}")
        else:
            print(f"{product}: {result}")

asyncio.run(main())
```

---

## API Reference

See `references/api-endpoints.md` for complete endpoint documentation.

### Key Endpoints

**Generation**
| Endpoint | Purpose |
|----------|---------|
| `POST /v2/image/generate` | Generate images from text (FIBO) |

**Edit by Text (No Mask)**
| Endpoint | Purpose |
|----------|---------|
| `POST /v2/image/edit` | Edit image with natural language instruction |
| `POST /v2/image/edit/add_object_by_text` | Add objects to image |
| `POST /v2/image/edit/replace_object_by_text` | Replace objects in image |
| `POST /v2/image/edit/erase_by_text` | Remove objects by name |

**Edit with Mask**
| Endpoint | Purpose |
|----------|---------|
| `POST /v2/image/edit/gen_fill` | Inpaint/generate in masked region |
| `POST /v2/image/edit/erase` | Erase masked region |

**Background Operations**
| Endpoint | Purpose |
|----------|---------|
| `POST /v2/image/edit/remove_background` | Remove background (RMBG-2.0) |
| `POST /v2/image/edit/replace_background` | Replace with AI-generated background |
| `POST /v2/image/edit/blur_background` | Apply blur to background |
| `POST /v2/image/edit/erase_foreground` | Remove foreground, fill background |
| `POST /v2/image/edit/crop_foreground` | Crop tightly around subject |

**Image Transformation**
| Endpoint | Purpose |
|----------|---------|
| `POST /v2/image/edit/expand` | Outpaint to new aspect ratio |
| `POST /v2/image/edit/enhance` | Enhance quality and details |
| `POST /v2/image/edit/increase_resolution` | Upscale 2x or 4x |
| `POST /v2/image/edit/blend` | Blend/merge images or textures |
| `POST /v2/image/edit/reseason` | Change season/weather |
| `POST /v2/image/edit/restyle` | Transform artistic style |
| `POST /v2/image/edit/relight` | Modify lighting |

**Text & Restoration**
| Endpoint | Purpose |
|----------|---------|
| `POST /v2/image/edit/replace_text` | Replace text in image |
| `POST /v2/image/edit/sketch_to_image` | Convert sketch to photo |
| `POST /v2/image/edit/restore` | Restore old/damaged photos |
| `POST /v2/image/edit/colorize` | Colorize B&W or convert to B&W |

**Product Photography**
| Endpoint | Purpose |
|----------|---------|
| `POST /v2/image/edit/lifestyle_shot_by_text` | Place product in scene by text |
| `POST /v2/image/edit/shot_by_image` | Place product on reference background |

**Utilities**
| Endpoint | Purpose |
|----------|---------|
| `POST /v2/structured_instruction/generate` | Generate JSON instruction (no image) |
| `GET /v2/status/{id}` | Check async request status |

### Authentication

All requests need `api_token` header:
```
api_token: YOUR_BRIA_API_KEY
```

---

## Related Skills

- **[vgl](../vgl/SKILL.md)** - Write structured VGL (Visual Generation Language) JSON prompts for precise, deterministic control over FIBO image generation. Use VGL for reproducible outputs with explicit visual attributes.
- **[image-utils](../image-utils/SKILL.md)** - Classic image manipulation (resize, crop, composite, watermarks) for post-processing Bria outputs
