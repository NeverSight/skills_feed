---
name: nano-banana
description: Generate images using Nano Banana Pro (Google Generative AI). Use this skill when the user asks to create, generate, or make images of any kind - illustrations, photos, product mockups, logos, scenes, textures, UI mockups, or any visual content. Handles style selection, prompt building, generation, and preview.
license: MIT
metadata:
  author: CarolMonroe22
  version: "1.0.0"
  tags:
    - ai
    - images
    - google-ai
    - illustrations
    - design
---

# Nano Banana Pro

Generate images using the Nano Banana Pro model via Google Generative AI API. Supports any image type: illustrations, realistic photos, product mockups, logos, scenes, patterns, UI concepts, and more.

## Setup (first time only)

If `GOOGLE_AI_API_KEY` is not set:

1. Go to https://aistudio.google.com/apikey
2. Click "Create API Key" (free, no credit card needed)
3. Add to shell profile:
   ```bash
   echo 'export GOOGLE_AI_API_KEY="your-key-here"' >> ~/.zshrc
   source ~/.zshrc
   ```

## Interactive Workflow

1. **Ask for concept** - What image do you want to create?
2. **Ask for type** - Illustration, photo, mockup, logo, etc.
3. **Ask for model** - Show options with cost (see Models below)
4. **Ask for size** - What dimensions/aspect ratio?
5. **Ask for style** - User describes their aesthetic, colors, or picks a preset
6. **Build prompt** - Combine type + style + concept + size into a generation prompt
7. **Generate** - Run `scripts/generate.py`
8. **Preview** - Open in default viewer

## Models & Cost

Present these options and confirm cost before generating:

| Model | Flag | Cost/image | Best for |
|-------|------|-----------|----------|
| Nano Banana Pro | `-m nano-banana-pro` | ~$0.13 | Best quality, recommended |
| Gemini 2.5 Flash | `-m gemini-2.5-flash` | ~$0.05 | Fast, good quality, budget |
| Gemini 2.0 Flash | `-m gemini-2.0-flash` | ~$0.03 | Fastest, lower quality |

Always confirm: "This will cost approximately $X.XX. Proceed?"

## Sizes

Ask user what size they need. Add the size instruction to the END of the prompt:

| Size | Use case | Prompt suffix |
|------|----------|---------------|
| Square (1:1) | Blog posts, social | `Square 1:1 aspect ratio.` |
| Wide (16:9) | Headers, banners, YouTube | `Wide format 16:9 aspect ratio.` |
| Portrait (9:16) | Stories, mobile | `Portrait 9:16 aspect ratio.` |
| Landscape (3:2) | Photos, cards | `Landscape 3:2 aspect ratio.` |

## Building the Prompt

### If user has brand/style preferences

Ask: "Do you have specific colors, aesthetic, or brand style you'd like?"

Use their answer to build the prompt with this structure:

```
[IMAGE TYPE], [AESTHETIC/STYLE], [COLOR PALETTE].

[CONCEPT DESCRIPTION]

[STYLE CONSTRAINTS]. [ASPECT RATIO]
```

### Image Type Presets

#### Illustrations

**Watercolor** - Soft, whimsical, hand-drawn
```
Whimsical hand-drawn watercolor illustration, soft [USER_COLOR] palette with warm accents.

Simple composition with ONE/TWO main elements:
[CONCEPT]

Style: Simple and clean like Notion illustrations. NOT complex. NOT busy.
NO text. Cream background. Square 1:1.
```

**Monochromatic** - Single color, clean lines
```
MONOCHROMATIC [USER_COLOR] illustration - use ONLY shades of [USER_HEX] throughout. Ultra high quality.

[CONCEPT]

Style: Clean lines, modern like Notion/Slack. NO other colors.
```

**Flat/Editorial** - Detailed, informative
```
Detailed flat illustration in [USER_COLOR] palette, editorial quality.

[CONCEPT]

Style: Clean linework. Modern editorial feel. High detail.
Wide format 16:9.
```

**Minimal line art** - Simple outlines, one accent
```
Minimal line art, thin black outlines with [USER_COLOR] as single accent color.

[CONCEPT]

Style: Minimal, lots of whitespace. NO fills except accent. White background.
```

#### Photos / Realistic

**Product photo** - Clean, studio-style
```
Professional product photography, studio lighting, clean [white/colored] background.

[PRODUCT DESCRIPTION]

Ultra high quality, sharp focus, soft shadows. [ASPECT RATIO]
```

**Lifestyle photo** - Natural, contextual
```
Lifestyle photography, natural lighting, [warm/cool] tones.

[SCENE DESCRIPTION]

Authentic feel, shallow depth of field. [ASPECT RATIO]
```

**Scene / Environment** - Places, spaces
```
[Photorealistic/Cinematic] scene, [LIGHTING DESCRIPTION], [MOOD].

[SCENE DESCRIPTION]

High detail, professional photography quality. [ASPECT RATIO]
```

#### Design & Branding

**Logo concept** - Clean, symbolic
```
Minimalist logo design on white background. Clean vector style.

[BRAND/CONCEPT DESCRIPTION]

Simple, memorable, works at small sizes. NO text. Square 1:1.
```

**UI mockup** - Interface concepts
```
Clean UI design mockup, modern interface, [light/dark] theme.

[SCREEN/COMPONENT DESCRIPTION]

Style: Modern SaaS aesthetic, clean typography, subtle shadows. [ASPECT RATIO]
```

**Pattern / Texture** - Repeating visuals
```
Seamless [PATTERN TYPE] pattern, [USER_COLOR] palette.

[PATTERN DESCRIPTION]

Tileable, consistent spacing, high quality. Square 1:1.
```

## Generation

### Single image

```bash
python3 scripts/generate.py "<full_prompt>" -o ~/Desktop/<filename>.png -m <model> --open
```

- `-m` selects the model (default: `nano-banana-pro`)
- `--open` opens the image in the default viewer after generation
- Use descriptive kebab-case filenames (e.g., `laptop-notifications.png`)
- If user doesn't like the result, tweak the prompt and regenerate

### Batch generation (same style)

When user needs multiple images in a consistent style (e.g., blog series, icon set, product shots):

1. Define the style prompt once (colors, aesthetic, constraints)
2. Ask user for a list of concepts/subjects
3. Generate each image reusing the same style prefix, only changing the concept
4. Save all to the same folder with numbered or descriptive names

Example batch flow:
```bash
# Same style, different concepts
python3 scripts/generate.py "<STYLE PREFIX> A laptop with sparkles. <STYLE SUFFIX>" -o ~/Desktop/batch/01-laptop.png -m nano-banana-pro
python3 scripts/generate.py "<STYLE PREFIX> A rocket launching. <STYLE SUFFIX>" -o ~/Desktop/batch/02-rocket.png -m nano-banana-pro
python3 scripts/generate.py "<STYLE PREFIX> A lightbulb moment. <STYLE SUFFIX>" -o ~/Desktop/batch/03-lightbulb.png -m nano-banana-pro
```

Confirm total cost before starting: "This batch of N images will cost approximately $X.XX total. Proceed?"

## Tips for Better Results

- Keep concepts focused: describe the main subject clearly
- Specify what you DON'T want (no text, no watermarks, no blurry elements)
- Include aspect ratio (1:1 for social, 16:9 for headers, 9:16 for stories)
- Add "Ultra high quality" or "High detail" for sharper output
- For illustrations: reference styles (Notion, Slack, Linear, Dribbble)
- For photos: describe lighting, angle, and mood
- For logos/design: emphasize simplicity and scalability
- If result isn't right, iterate: adjust the prompt and regenerate
