---
name: google-image-creator
description: "Generate images using Google AI models (Imagen 4 and Gemini). Presents top 3 model options with pricing, generates images via API, tracks token usage and costs. Use when user needs to: (1) Generate images with Google AI, (2) Choose between Google image models, (3) See pricing for Google image generation, (4) Track image generation costs, or (5) Compare Imagen vs Gemini image models. Self-updating with current pricing from https://ai.google.dev/pricing"
---

# Google AI Image Generation

Generate images using Google's Imagen and Gemini models with automatic cost tracking.

## Quick Start

### 1. Present Model Options

When a user wants to generate images, first show them the top 3 options:

```bash
npx tsx .claude/skills/google-image-creator/scripts/list-models.ts
```

This displays:
- **Gemini 2.5 Flash Image** ($0.039/image) - Best value, fastest
- **Imagen 4 Fast** ($0.020/image) - Photorealistic quality
- **Imagen 4 Ultra** ($0.060/image) - Highest quality

Let the user choose, or recommend Gemini 2.5 Flash for most use cases.

### 2. Generate Image

```bash
npx tsx .claude/skills/google-image-creator/scripts/generate-image.ts \
  "prompt here" \
  "model-id" \
  "./output.png"
```

**Example:**
```bash
npx tsx .claude/skills/google-image-creator/scripts/generate-image.ts \
  "sunset over mountains, photorealistic" \
  "gemini-2.5-flash-image" \
  "./sunset.png"
```

### 3. Report Cost

The script automatically reports:
- Images generated
- Model used
- Estimated cost

Example output:
```
✅ Image generated successfully!
   Model: Gemini 2.5 Flash Image (gemini-2.5-flash-image)
   Prompt: "sunset over mountains"
   Saved to: ./sunset.png
   Images: 1
   Cost: $0.0390
```

## Prerequisites

**API Key Required:**

User must have `GOOGLE_API_KEY` or `GEMINI_API_KEY` set:

```bash
export GOOGLE_API_KEY="user-api-key-here"
```

Get key at: https://aistudio.google.com/app/apikey

**Note:** All Google image generation is **paid tier only** (no free quota).

## Workflow

### Standard Workflow

1. **User Request:** "Generate an image of X"

2. **Ask Model Preference:** "Which model would you like to use?" Then run:
   ```bash
   npx tsx .claude/skills/google-image-creator/scripts/list-models.ts
   ```

3. **User Chooses:** User selects model or you recommend based on needs

4. **Generate:** Run generation script with chosen model

5. **Report:** Display cost and save location

### Quick Workflow (Skip Selection)

If user says "use the cheapest" or doesn't specify:
- Default to `gemini-2.5-flash-image`
- Generate immediately
- Report cost afterward

## Model Selection Guide

**Use Gemini 2.5 Flash** when:
- User wants lowest cost
- High volume generation
- Speed is priority
- General-purpose images

**Use Imagen 4 Fast** when:
- User needs photorealism
- Balance of quality and cost
- Simple text-to-image only

**Use Imagen 4 Ultra** when:
- User explicitly requests highest quality
- Client-facing deliverables
- Budget allows premium pricing

## Cost Tracking

Always report costs after generation. For multiple images, sum costs:

```
Image 1: $0.039
Image 2: $0.039
Image 3: $0.039
-----------------
Total: $0.117
```

## Error Handling

**Common Errors:**

| Error | Solution |
|-------|----------|
| "API key not set" | Tell user to set `GOOGLE_API_KEY` |
| "Unknown model" | Run `list-models.ts` to show valid models |
| "API Error 401" | API key invalid - user needs to verify key |
| "API Error 429" | Rate limit - wait and retry |
| "Quota exceeded" | Gemini image generation requires billing-enabled API key (free tier = 0 quota) |
| "Imagen API is only accessible to billed users" | Enable billing on your Google Cloud project |

## Advanced: Multiple Images

For generating multiple images, run script multiple times and sum costs:

```bash
for i in {1..5}; do
  npx tsx .claude/skills/google-image-creator/scripts/generate-image.ts \
    "landscape $i" \
    "gemini-2.5-flash-image" \
    "./landscape_$i.png"
done

echo "Total: 5 images × $0.039 = $0.195"
```

## Updating Model Information

**To update pricing or add new models:**

1. Check official pricing: https://ai.google.dev/pricing
2. Update `references/models.md`
3. Update `scripts/generate-image.ts` MODEL_PRICING
4. Update `scripts/list-models.ts` TOP_3_MODELS
5. Repackage skill

**Files to update:**
- `references/models.md` - Full documentation
- `references/api-guide.md` - API patterns
- `scripts/generate-image.ts` - MODEL_PRICING object
- `scripts/list-models.ts` - TOP_3_MODELS array

## References

**Detailed Documentation:**
- [references/models.md](references/models.md) - All 6 models with full specs
- [references/api-guide.md](references/api-guide.md) - API setup and patterns

**Official Links:**
- Pricing: https://ai.google.dev/pricing
- Imagen Docs: https://ai.google.dev/gemini-api/docs/imagen
- Gemini Image Docs: https://ai.google.dev/gemini-api/docs/image-generation
- Get API Key: https://aistudio.google.com/app/apikey

## Examples

### Example 1: Basic Generation

**User:** "Generate a sunset image"

**You:**
"I'll generate a sunset image. Which model would you like?"
```
npx tsx .claude/skills/google-image-creator/scripts/list-models.ts
```

**User:** "Use the recommended one"

**You:**
```
npx tsx .claude/skills/google-image-creator/scripts/generate-image.ts \
  "beautiful sunset over ocean, warm colors, photorealistic" \
  "gemini-2.5-flash-image" \
  "./sunset.png"
```

"✅ Generated sunset.png using Gemini 2.5 Flash Image. Cost: $0.0390"

---

### Example 2: High-Quality Request

**User:** "Generate a professional product photo, highest quality"

**You:**
"For highest quality, I recommend Imagen 4 Ultra ($0.06/image). Proceed?"

**User:** "Yes"

**You:**
```
npx tsx .claude/skills/google-image-creator/scripts/generate-image.ts \
  "professional product photo of ceramic mug, studio lighting, high detail" \
  "imagen-4.0-ultra-generate-001" \
  "./product.png"
```

"✅ Generated product.png using Imagen 4 Ultra. Cost: $0.0600"

---

### Example 3: Budget-Conscious

**User:** "Generate 10 landscape images, keep it cheap"

**You:**
"I'll use Gemini 2.5 Flash ($0.039/image). Total cost: $0.39 for 10 images."

```
# Generate 10 images
# Sum costs
```

"✅ Generated 10 landscapes. Total cost: $0.3900"

## Tips

**Prompt Engineering:**
- Be specific: "sunset over mountains, warm colors, golden hour"
- Mention style: "photorealistic", "watercolor", "3D render"
- Include lighting: "soft natural light", "studio lighting"
- Specify details: "high resolution", "shallow depth of field"

**Cost Optimization:**
- Use Gemini 2.5 Flash for testing prompts
- Only use Imagen 4 Ultra for final deliverables
- Batch mode available for Gemini models (50% discount)
- Iterate on cheaper models first

**File Management:**
- Always specify output path
- Use descriptive filenames
- Organize by project/date
- Keep generated images for reference
