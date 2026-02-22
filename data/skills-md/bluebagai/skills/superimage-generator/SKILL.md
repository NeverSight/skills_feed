---
name: superimage-generator
description: "WHAT: Transforms basic image prompts into model-optimized superprompts for AI image generation. WHEN: generating images, creating AI art, enhancing image prompts, working with Flux, Flux Kontext Max, Nano Banana, Midjourney, Ideogram, Recraft, Luma, Reve, Grok, GPT Image 1.5, or Seedream 4.5. KEYWORDS: superprompt, image prompt, generate image, AI art, enhance prompt, optimize prompt, photorealistic, portrait, product, selfie, photography, image generation."
---

# Superprompt Generator

Transform basic prompts into professional-grade superprompts optimized for specific AI image models.

**Terminology:**

- **prompt** = user's basic input (e.g., "a woman taking a selfie")
- **superprompt** = the enhanced, structured output with detailed specifications

## ⚠️ MANDATORY WORKFLOW - DO NOT SKIP ANY STEPS

This skill has a **sequential, dependency-based workflow**. Each step builds on the previous one. **Skipping steps produces inferior results and failed generations.**

### Critical Enforcement Rules:

- [ ] **Step 1 MUST complete before Step 2** — No model selection without intent clarification
- [ ] **Step 3 MUST check `examples/INDEX.md` before generating** — Read the index, follow its instructions. Do NOT read more than 2 example files.
- [ ] **Step 4 VALIDATION is mandatory — no exceptions** — Run validation script before proceeding
- [ ] **Do NOT flatten (Step 5) until validation returns `✓ VALID`** — Invalid prompts fail on models
- [ ] **Always show user the validation report** — They need to see quality scores and any warnings

**If you are tempted to skip steps: DON'T. The workflow exists for a reason.**

## Contents

- [Quick Start](#quick-start)
- [Workflow Selection](#workflow-selection)
- [Workflow](#workflow)
- [Reference Image Workflow](#reference-image-workflow)
- [Superprompt Playbook](#superprompt-playbook) (see also [playbook.md](playbook.md))
- [Examples](#examples)
- [Model Templates](#model-templates)
- [Validation Scripts](#validation-scripts)
- [Aspect Ratio Reference](#aspect-ratio-reference)

## Quick Start

> [! IMPORTANT]
> Do not act after reading the quick start section alone. Make sure to read [Workflow Selection](#workflow-selection) before commiting to generating an output.

**Input:** `"a woman taking a selfie"`

**Output:** Structured superprompt with `subject`, `wardrobe`, `pose`, `scene`, `lighting`, `camera` blocks containing anatomical precision, fabric details, camera technicals, and negative constraints.

**With Reference Image:** `"gym selfie" + [uploaded face reference]`
→ See [Reference Image Workflow](#reference-image-workflow) below.

## Workflow Selection

**Does the user provide a reference image for face/identity preservation?**

- **YES** → Follow [Reference Image Workflow](#reference-image-workflow)
- **NO** → Follow [Standard Workflow](#workflow) below

---

## Workflow

Copy this checklist and track progress — **each step is mandatory**::

```
Superprompt Generation (SEQUENTIAL):
- [ ] Step 1: Clarify user intent ← START HERE
- [ ] Step 2: Select target model ← DEPENDS ON STEP 1
- [ ] Step 3: Generate structured superprompt ← DEPENDS ON STEP 2
- [ ] Step 4: Validate with script ← MANDATORY, NON-OPTIONAL
- [ ] Step 5: Flatten for model format ← ONLY AFTER VALIDATION PASSES
- [ ] Step 6: Return to user ← FINAL STEP
```

### Step 1: Clarify Intent

**DO NOT skip this step. If unsure about intent, ask the user:**

- Main subject? (person, product, landscape, architecture, food, animal)
- Style? (photorealistic, artistic, illustration)
- Aspect ratio preference? (9:16 mobile, 16:9 landscape, 1:1 square)
- Any other specific mood or setting?

**Document their answers. You need these for Step 2.**

### Step 2: Select Model

**Model selection depends on Step 1 answers. Use the table below:**

**Defaults by subject type:**

- **Person/human subject** → `nano-banana` (anatomical precision, complex poses)
- **Product/object/landscape** → `flux` (general photorealism)

When to use a different model:

- Need text rendering? → `ideogram` or `gpt-image-1.5`
- Need face/identity preservation? → `flux-kontext-max`
- Need artistic/aesthetic style? → `midjourney`
- Need video/motion? → `luma`
- Need iterative editing? → `gpt-image-1.5`

| Model              | Best For                                           | Template                                                 |
| ------------------ | -------------------------------------------------- | -------------------------------------------------------- |
| `nano-banana`      | **Default (people)** - Anatomical precision, poses | [models/nano-banana.md](models/nano-banana.md)           |
| `flux`             | **Default (non-people)** - General photorealism    | [models/flux.md](models/flux.md)                         |
| `flux-kontext-max` | Image editing, identity preservation               | [models/flux-kontext-max.md](models/flux-kontext-max.md) |
| `gpt-image-1.5`    | Reasoning-based, UI mockups, logos                 | [models/gpt-image-1.5.md](models/gpt-image-1.5.md)       |
| `seedream-4.5`     | Natural language, text in images, 4K               | [models/seedream-4.5.md](models/seedream-4.5.md)         |
| `midjourney`       | Aesthetic quality, artistic                        | [models/midjourney.md](models/midjourney.md)             |
| `ideogram`         | Typography, logos                                  | [models/ideogram.md](models/ideogram.md)                 |
| `recraft`          | Illustrations, vectors                             | [models/recraft.md](models/recraft.md)                   |
| `luma`             | Video, 3D, motion                                  | [models/luma.md](models/luma.md)                         |
| `reve`             | Artistic styles                                    | [models/reve.md](models/reve.md)                         |
| `grok-imagine`     | Quick iterations                                   | [models/grok-imagine.md](models/grok-imagine.md)         |

**If uncertain which model to use:** Ask the user about subject type (person vs. object/scene) and desired style, then apply the defaults above.

### Step 3: Generate Superprompt

**Before generating:**

1. Open `examples/INDEX.md`
2. Follow its instructions — read ONE universal example + ONE category match
3. Use as structural reference, do NOT copy verbatim

**Consider perspective:**

- If the user's request implies mood, tension, scale, or narrative — check `resources/perspectives.md` for a perspective that enhances the image
- If the user specifies a camera angle already, respect it
- Default: do NOT force an unusual perspective on every prompt. Standard eye-level is fine when nothing calls for more

**Then** use the schema structure matching your selected model.

> **WARNING -- OUTPUT FORMAT:**
> Your generated JSON must contain ONLY the superprompt fields at the **top level**. Do NOT wrap these in a `superprompt` key. Do NOT include metadata keys like `name`, `description`, `input_prompt`, `target_model`, `model_adaptations`, `flattened_prompt`, `color_palette`, or `playbook_principles_applied`. The example files in the `examples/` directory contain these wrapper fields for documentation purposes only -- the validator checks the superprompt content directly at the top level. If you include wrapper keys, validation WILL fail because the validator will not find the required fields at the root of the JSON.

**Choose `prompt_type` based on subject:**

- `portrait` — people, characters, subjects with identity/expression
- `product` — objects, items, still life, architecture
- `collage` — multi-panel compositions, editorial layouts

**Schema depends on target model:**

- **Nano-banana** → uses its own flat structure (no `prompt_type` field). See nano-banana example below.
- **Luma** → uses its own video-specific structure. See [models/luma.md](models/luma.md).
- **All other models** → use the base schema with `prompt_type` discriminator and `meta.target_model`. See portrait/product examples below.

#### Example: Portrait (base schema — flux, midjourney, ideogram, recraft, gpt-image-1.5, seedream-4.5, etc.)

**Required:** `prompt_type`, `meta`, `subject`, `wardrobe`, `pose_action`, `environment`, `lighting`, `camera_technical`, `realism_anchors`, `negative_prompt`

```json
{
  "prompt_type": "portrait",
  "meta": {
    "quality_tier": "professional",
    "aspect_ratio": "9:16",
    "style": "photorealistic",
    "target_model": "flux"
  },
  "subject": {
    "description": "young woman mid-20s, honey blonde beach waves, confident smile",
    "identity": {
      "age_range": "mid-20s",
      "type": "young woman",
      "distinguishing_features": ["honey blonde beach waves", "confident smile"]
    },
    "physical_details": {
      "skin": { "tone": "light warm", "texture": "visible pores, natural" },
      "hair": {
        "color": "honey blonde",
        "style": "beach waves, past shoulders"
      },
      "face": { "expression": "confident smile", "gaze": "direct at camera" }
    },
    "expression_mood": "confident, relaxed"
  },
  "wardrobe": {
    "clothing": [
      {
        "type": "tank top",
        "material": "cotton",
        "fit": "fitted",
        "color": "white"
      },
      { "type": "denim shorts", "fit": "high-waisted", "details": "frayed hem" }
    ],
    "accessories": ["gold layered necklaces", "small hoop earrings"]
  },
  "pose_action": {
    "position": "mirror selfie, phone at chest level",
    "posture": "slight hip tilt"
  },
  "environment": {
    "location": "modern apartment bedroom",
    "background": ["natural light from window"],
    "atmosphere": "casual, warm"
  },
  "lighting": {
    "type": "natural",
    "quality": "soft diffused",
    "effects": ["window light", "subtle shadows"]
  },
  "camera_technical": {
    "device": "iPhone 15 Pro",
    "lens": "24mm wide",
    "aperture": "f/2.0"
  },
  "realism_anchors": [
    "visible skin pores",
    "fabric texture",
    "natural window light"
  ],
  "negative_prompt": [
    "cartoon",
    "deformed",
    "blurry",
    "airbrushed",
    "watermark",
    "low quality"
  ]
}
```

#### Example: Product (base schema)

**Required:** `prompt_type`, `meta`, `subject`, `environment`, `lighting`, `camera_technical`, `realism_anchors`, `negative_prompt`

```json
{
  "prompt_type": "product",
  "meta": {
    "quality_tier": "professional",
    "aspect_ratio": "1:1",
    "style": "photorealistic",
    "target_model": "flux"
  },
  "subject": {
    "description": "vintage 1970s Polaroid camera, cream and brown body, rainbow stripe",
    "physical_details": {
      "materials": ["plastic body", "metal accents"],
      "finish": "matte with age patina"
    }
  },
  "environment": {
    "location": "weathered wooden table surface",
    "background": ["soft out-of-focus bookshelf", "warm afternoon light"],
    "atmosphere": "nostalgic, cozy"
  },
  "lighting": {
    "type": "golden-hour",
    "direction": "side lighting from window",
    "quality": "soft warm",
    "effects": ["warm highlights", "soft shadows"]
  },
  "camera_technical": { "lens": "50mm macro", "aperture": "f/2.8" },
  "realism_anchors": [
    "surface scratches",
    "dust particles",
    "leather texture",
    "metal patina"
  ],
  "negative_prompt": [
    "blurry",
    "low quality",
    "oversaturated",
    "artificial",
    "floating",
    "watermark"
  ]
}
```

#### Example: Nano-banana model

Nano-banana uses its own flat structure — no `prompt_type` field needed.

**Required:** `subject` (with `body`), `wardrobe`, `scene`, `lighting`, `camera`

```json
{
  "subject": {
    "description": "young woman mid-20s, honey blonde beach waves, confident smile",
    "body": {
      "physique": "natural athletic build, hourglass figure",
      "anatomy": "defined shoulders, narrow waist, curved hips",
      "details": "visible skin pores, natural texture, subtle imperfections"
    }
  },
  "wardrobe": {
    "top": "white cotton tank top, fitted, subtle outline visible",
    "bottom": "high-waisted denim shorts, frayed hem",
    "accessories": ["gold layered necklaces", "small hoop earrings"]
  },
  "pose_action": {
    "description": "mirror selfie, holding smartphone at chest level, slight hip tilt"
  },
  "scene": {
    "environment": "modern apartment bedroom, natural light from window"
  },
  "lighting": {
    "type": "soft natural",
    "effects": ["diffused window light", "subtle shadows"]
  },
  "camera": {
    "technical": "iPhone 15 Pro, 24mm wide, f/2.0",
    "aspect_ratio": "9:16",
    "negative_constraints": "no cartoon, no deformed, no blurry, no airbrushed, no watermark"
  }
}
```

### Step 4: Validate

```bash
# Auto-detects model from meta.target_model (defaults to nano-banana if absent)
node /skills/generating-image-superprompts/scripts/validate-prompt.js --input prompt.json

# Or specify model explicitly
node /skills/generating-image-superprompts/scripts/validate-prompt.js --input prompt.json --model flux
```

Validation checks: required fields per prompt_type and model, conflicts, model-specific requirements, negative coverage.

> **IMPORTANT -- JSON structure for validation:**
> The JSON you pass to the validation script must have the prompt fields (`subject`, `wardrobe`, `scene`, `lighting`, `camera`, etc.) at the **top level** of the object. The example files in the `examples/` directory wrap these fields inside a `superprompt` key alongside documentation metadata (`name`, `description`, `model_adaptations`, etc.), but the validator does NOT expect that wrapper -- it expects fields at root level.
>
> **Common failure:** If validation fails with "Required" errors for `subject`, `wardrobe`, `scene`, `lighting`, or `camera`, you almost certainly wrapped the prompt fields inside a `superprompt` object. Remove the wrapper and put all fields at the root of the JSON.

**If validation fails:**

1. Review the error messages carefully
2. Check whether you accidentally wrapped prompt fields in a `superprompt` key or included metadata keys (`name`, `description`, `model_adaptations`, etc.) -- if so, remove them and put prompt fields at root level
3. Fix the identified issues in your JSON
4. Re-run validation
5. **Only proceed to Step 5 when validation passes**

Repeat this loop until you get `✓ VALID` status.

### Step 5: Flatten for Model

Convert your structured JSON into the model's expected text format. "Flattening" means joining nested values into a comma-separated string.

**Example (Flux):**

Structured JSON:

```json
{
  "quality_prefix": "masterpiece, 8k uhd",
  "subject": "young woman mid-20s, honey blonde beach waves",
  "wardrobe": "white tank top, denim mini skirt",
  "pose": "mirror selfie, back arch",
  "lighting": "hard direct sunlight"
}
```

Flattened prompt (ready for model):

```
masterpiece, 8k uhd, young woman mid-20s, honey blonde beach waves, white tank top, denim mini skirt, mirror selfie, back arch, hard direct sunlight
```

See model templates for model-specific flattening rules (some models like GPT Image 1.5 prefer natural language paragraphs instead of comma-separated tags).

### Step 6: Return to User

**Always provide:**

1. Ready-to-use flattened prompt (copy-paste ready for the model)
2. Recommended model settings (guidance_scale, steps, aspect_ratio)

**Optionally provide:** 3. Structured JSON — include when the user explicitly requests it OR when they need to iterate/edit the prompt later

## Reference Image Workflow

When user provides a reference image for face/identity preservation, you still generate a **complete superprompt** — you just add a `reference` block to preserve identity.

> [! IMPORTANT] >
> This is NOT an alternative to the standard workflow. You follow the standard workflow AND add reference settings.

```
Reference Image Generation:
- [ ] Step 1: Confirm reference image uploaded
- [ ] Step 2: Follow Standard Workflow Steps 1-3 (generate FULL superprompt)
- [ ] Step 3: Add reference block to the superprompt
- [ ] Step 4: Ensure subject.appearance.skin references the image
- [ ] Step 5: Continue with Standard Workflow Steps 4-6 (validate, flatten, return)
```

### What You Generate

You generate a **complete superprompt** with all the usual blocks (`subject`, `wardrobe`, `pose`, `scene`, `lighting`, `camera`) PLUS a `reference` block at the top.

### Reference Block Structure

Add this block to your full superprompt:

```json
{
  "reference": {
    "face_identity": "use uploaded reference image",
    "identity_lock": true,
    "face_accuracy": "100% identical to reference — same facial structure, proportions, skin texture, expression, and details"
  }
}
```

### Complete Example (Reference + Full Superprompt)

```json
{
  "reference": {
    "face_identity": "use uploaded reference image",
    "identity_lock": true,
    "face_accuracy": "100% identical to reference — same facial structure, proportions, skin texture"
  },
  "subject": {
    "description": "young woman mid-20s, athletic build",
    "body": {
      "physique": "toned athletic build",
      "anatomy": "defined shoulders, narrow waist",
      "details": "visible skin pores, natural texture"
    },
    "appearance": {
      "skin": {
        "tone": "same as reference image",
        "texture": "natural, visible pores"
      },
      "expression": "confident smile",
      "gaze": "direct at camera"
    }
  },
  "wardrobe": {
    "top": "black sports bra, fitted",
    "bottom": "high-waisted grey leggings",
    "accessories": "small stud earrings"
  },
  "pose": "gym mirror selfie, phone at chest level, slight hip tilt",
  "scene": {
    "environment": "modern gym, weight racks in background",
    "lighting": { "type": "overhead fluorescent", "quality": "bright, even" }
  },
  "lighting": {
    "type": "gym fluorescent",
    "effects": "even illumination, subtle shadows"
  },
  "camera": {
    "technical": "iPhone 15 Pro, 24mm wide, f/1.8",
    "aspect_ratio": "9:16",
    "negative_constraints": "no cartoon, no deformed, no blurry, no face change, no identity drift"
  }
}
```

### Key Reference Settings

| Setting                          | Purpose                        |
| -------------------------------- | ------------------------------ |
| `identity_lock: true`            | Prevents face drift            |
| `face_accuracy: "100%"`          | Exact facial match             |
| `skin.tone: "same as reference"` | Preserves skin characteristics |

### Reference-Compatible Models

- **Flux IP-Adapter** - Best for face preservation
- **Flux Kontext Max** - Exceptional identity preservation across edits
- **GPT Image 1.5** - Robust facial and identity preservation for iterative edits
- **Seedream 4.5** - Supports up to 14 reference images for character consistency
- **Nano Banana** - Strong identity lock support
- **Midjourney --cref** - Character reference flag

See [examples/reference-image-gym.json](examples/reference-image-gym.json) for complete example.

---

## Superprompt Playbook

Core principles for high-quality prompts. See [playbook.md](playbook.md) for detailed explanations and examples.

**The 7 Principles (quick reference):**

1. **Hierarchical Specificity** — be specific, not vague (`"fitted burgundy velvet midi dress"` not `"wearing a dress"`)
2. **Realism Anchors** — ground in physical reality (`visible pores`, `fabric weave`, `accurate shadows`)
3. **Technical Camera Language** — use photography terms (`85mm lens`, `f/1.8 aperture`)
4. **Negative Prompt Hygiene** — exclude quality issues, anatomy errors, style leaks
5. **Spatial Consistency** — define camera angle and subject positioning clearly
6. **Lighting as Storytelling** — golden hour = warm; hard midday = bold; rim = dramatic
7. **Identity Lock** — for character consistency, lock age, hair, body type

## Examples

Complete examples with input → output transformations. Each includes prompts adapted for multiple models.

### Key Examples by Category

**Reference Image (Start here for identity preservation):**

- [examples/reference-image-gym.json](examples/reference-image-gym.json) - Face/identity preservation workflow with best practices

**Mirror Selfies (Most common use case):**

- [examples/nano-banana-mirror-selfie.json](examples/nano-banana-mirror-selfie.json) - 4 variations, deep anatomical detail
- [examples/elevator-mirror-selfie.json](examples/elevator-mirror-selfie.json) - Multiple reflections, late-night mood
- [examples/lifestyle-selfie.json](examples/lifestyle-selfie.json) - Street shop window reflection

**Outdoor/Lifestyle:**

- [examples/backyard-bikini.json](examples/backyard-bikini.json) - iPhone outdoor realism, gravity physics
- [examples/jet-ski-lookback.json](examples/jet-ski-lookback.json) - Ocean golden hour, torso twist pose
- [examples/tropical-beach-selfie.json](examples/tropical-beach-selfie.json) - Beach selfie POV, straw hat

**Indoor/Casual:**

- [examples/bedroom-prone-selfie.json](examples/bedroom-prone-selfie.json) - Cozy bed selfie, pink loungewear
- [examples/kitchen-candid.json](examples/kitchen-candid.json) - Apartment evening, rainy city, mixed lighting

**Artistic/Stylized:**

- [examples/bw-window-portrait.json](examples/bw-window-portrait.json) - Text-to-structured, B&W cinematic
- [examples/streetwear-editorial-collage.json](examples/streetwear-editorial-collage.json) - Multi-panel poster, analog-digital fusion
- [examples/fashion-studio-collage.json](examples/fashion-studio-collage.json) - Multi-pose collage, same model 6-8 poses

### Additional Examples

Browse the `examples/` directory for 50+ additional examples covering:

- Athletic/gym poses, complex wardrobe, branded items
- Couples, group shots, dual subjects
- Night photography, flash aesthetics, low-light
- Editorial fashion, collages, split layouts
- Character/cosplay, fantasy elements

## Model Templates

Each model has specific prompt formatting requirements:

- [models/flux.md](models/flux.md) - Quality tags first, photography language
- [models/flux-kontext-max.md](models/flux-kontext-max.md) - Natural language editing, preservation clauses, 512 token limit
- [models/gpt-image-1.5.md](models/gpt-image-1.5.md) - Natural language, quality parameter, no quality tags needed
- [models/seedream-4.5.md](models/seedream-4.5.md) - Coherent natural language, concise prompts, text in quotes
- [models/nano-banana.md](models/nano-banana.md) - Deep JSON, anatomical terms, inline negatives
- [models/black-forest-labs.md](models/black-forest-labs.md) - Detailed BFL/Flux guide
- [models/midjourney.md](models/midjourney.md) - Parameters (--ar, --v, --style)
- [models/ideogram.md](models/ideogram.md) - Text in quotes, magic prompt
- [models/recraft.md](models/recraft.md) - Style presets, color palettes
- [models/luma.md](models/luma.md) - Motion descriptions, camera movement
- [models/reve.md](models/reve.md) - Art movement references
- [models/grok-imagine.md](models/grok-imagine.md) - Natural language, social-ready

## Validation Scripts

```bash
# Validate a prompt
node /skills/generating-image-superprompts/scripts/validate-prompt.js --input prompt.json --model nano-banana

# Strict mode (warnings as errors)
node /skills/generating-image-superprompts/scripts/validate-prompt.js --input prompt.json --model nano-banana --strict

# Pipe from stdin
cat prompt.json | node /skills/generating-image-superprompts/scripts/validate-prompt.js --model nano-banana
```

Output includes quality score (0-100) for specificity, realism, technical, and negative coverage.

## Aspect Ratio Reference

| Ratio | Use Case              |
| ----- | --------------------- |
| 9:16  | Mobile/Stories/TikTok |
| 16:9  | Desktop/YouTube       |
| 1:1   | Instagram/Profile     |
| 4:5   | Instagram portrait    |
