---
name: nano-banana-prompt
description: Craft highly effective prompts for Nano Banana Pro (Gemini image generation). Use when generating images with Nano Banana Pro for any purpose including photorealistic portraits, product photography, creative experiments, e-commerce mockups, social media content, editorial layouts, 3D renders, era-specific aesthetics (Y2K, 2000s, 1990s), miniature/diorama effects, or any advanced image generation task. Provides proven prompt patterns, technical specifications, JSON structuring, identity preservation techniques, and style-specific templates.
---

# Nano Banana Prompt Engineer

## Core Principles

Nano Banana Pro excels at:
- **Photorealistic rendering** with accurate textures, lighting, and materials
- **Identity preservation** - maintaining facial features across transformations
- **Complex compositions** - multiple subjects, detailed environments, layered effects
- **Technical precision** - specific camera specs, lighting setups, era aesthetics
- **Creative experiments** - surreal compositions, 3D effects, recursive visuals

**Key success factors:**
1. **Specificity over brevity** - Detailed prompts yield better results
2. **Technical language** - Use photography/cinematography terminology
3. **Progressive layering** - Build from overall mood → subject details → technical specs
4. **JSON for complexity** - Use structured JSON for multi-element scenes
5. **Negative prompts** - Explicitly state what to avoid

## Prompt Pattern Selection

Choose your approach based on the task:

### Simple Prompts (Text-Based)
**When to use:** Single subject, straightforward composition, basic style transfer

**Pattern:**
```
[Style/mood] + [Subject description] + [Environment] + [Technical specs] + [Quality markers]
```

**Example:**
```
A professional, high-resolution profile photo, maintaining exact facial features of the uploaded image.
Shot from chest up with ample headroom, looking directly at camera. Smart casual blazer in charcoal gray.
Solid neutral studio background (#562226). Bright airy lighting with catchlights in eyes.
85mm f/1.8 lens, shallow depth of field, crisp focus on eyes, soft bokeh.
Clean cinematic color grading with subtle warmth.
```

### Structured JSON Prompts
**When to use:** Complex scenes, multiple elements, precise control, era-specific aesthetics

**When JSON is essential:**
- Multiple subjects with different styling
- Detailed accessory/wardrobe specifications
- Era-specific aesthetics (Y2K, 2000s) with many characteristic elements
- Scene compositions requiring precise element placement
- Photography setups with specific technical requirements

See [JSON Structure Guide](references/json-structure-guide.md) for templates.

### Hybrid Approach
**When to use:** Moderate complexity, some technical precision needed

Combine narrative description with key technical specs in structured sections.

## Identity Preservation

When maintaining facial features from a reference image:

**Critical phrases:**
- "Keep the facial features of the person in the uploaded image exactly consistent"
- "Preserve original face 100% accurate from reference image"
- "maintain the exact facial structure, identity, and key features"
- "without changing her original face"
- `"face": { "preserve_original": true, "reference_match": true }`

**Additional requirements:**
- Specify what CAN change (outfit, environment, pose, expression)
- Add technical specs to ensure quality (8k, sharp focus, etc.)
- Describe the transformation while emphasizing face preservation

**Example:**
```
Keep the facial features of the person in the uploaded image exactly consistent.
Dress them in a professional navy blue business suit with white shirt.
Background: Clean solid dark gray studio photography backdrop with subtle gradient.
Photography Style: Sony A7III with 85mm f/1.4 lens, flattering portrait compression.
Lighting: Three-point setup with soft key light, subtle rim light.
Render natural skin texture with visible pores. Ultra-realistic 8k professional headshot.
```

## Technical Specifications

Adding precise technical specs dramatically improves output quality.

### Camera & Lens
- **Camera models:** Canon EOS R5, Sony A7III, Hasselblad H6D, iPhone 16, Canon IXUS
- **Lenses:** 85mm f/1.4 (portraits), 35mm f/2.8 (environmental), 12-18mm (fisheye), 50mm f/1.8
- **Settings:** Aperture (f/1.4 - f/5.6), ISO (100-400), shutter speed (1/60s - 1/125s)

### Lighting
- **Studio:** Three-point lighting, soft diffused, ring flash, hard flash
- **Natural:** Golden hour, sunset, harsh midday, window light
- **Cinematic:** Rim light, backlight, volumetric fog, dramatic shadows
- **Flash:** Built-in flash, on-camera flash, blown-out highlights

### Film Stocks & Color
- **Film:** Kodak Portra 400, Kodak Ektar 100, 35mm aesthetic
- **Color grading:** Cinematic, warm nostalgic, high contrast, muted tones
- **Quality:** 8K, 4K, ultra HD, film grain, sharp detail

### Depth of Field & Focus
- Shallow DoF for portraits (f/1.4 - f/2.8)
- Deep DoF for products/architecture (f/5.6 - f/11)
- "Crisp focus on eyes with soft bokeh background"
- "Everything in sharp focus, edge to edge"

## Pattern Categories

### Photorealism & Portraits
Use for: Professional headshots, editorial portraits, realistic scene photography

**Key elements:**
- Identity preservation phrases
- Specific camera/lens combinations
- Detailed lighting setups
- Skin texture rendering ("visible pores," "natural texture")
- Environmental context

See [Photorealism & Portraits Guide](references/photorealism-portraits.md) for:
- Professional headshot templates
- Era-specific aesthetics (2000s mirror selfie, 1990s flash photography)
- Victoria's Secret style shoots
- Business photo transformations
- Film photography aesthetics

### Creative Experiments
Use for: 3D renders, dioramas, isometric views, surreal compositions, miniatures

**Key elements:**
- Rendering engine specs (Cinema 4D, C4D)
- Material descriptions (glossy, matte, PVC-like)
- Perspective types (isometric, orthographic, axonometric)
- Scale relationships (miniature, toy-sized, oversized)
- Surreal physics violations

See [Creative Experiments Guide](references/creative-experiments.md) for:
- 3D chibi/blind box style transformations
- Isometric dioramas and miniature worlds
- Floating island dioramas
- Recursive/Droste effects
- Surreal compositions (ironing wrinkles, trans-dimensional liquid pours)
- Fisheye and wide-angle distortions

### Product & Commercial
Use for: E-commerce shots, product photography, brand imagery, luxury goods

**Key elements:**
- Clean isolation ("pure white background RGB 255,255,255")
- Professional lighting ("soft commercial studio lighting")
- Material emphasis ("fabric texture," "metallic sheen")
- Contact shadows for grounding
- Brand integration

See [Product & Commercial Guide](references/product-commercial.md) for:
- E-commerce product isolation
- Virtual model try-on
- Luxury product photography
- Magazine cover layouts
- 3D brand store visualizations

### Editing & Transformation
Use for: Aspect ratio changes, background removal, style transfer, outpainting

**Key elements:**
- Preservation specifications
- Logical fill instructions
- Consistency requirements
- Seamless blending

See [Editing & Transformation Guide](references/editing-transformation.md) for:
- Smart outpainting (composition rescue)
- Background removal and replacement
- Crowd removal with intelligent fill
- Aspect ratio expansion
- Style transfer while preserving identity

## Quick Reference Templates

### Professional Portrait
```
Keep the facial features exactly as in the uploaded image.
Professional [outfit description].
Background: [solid color/environment].
Photography: [Camera] with [lens], [lighting style].
[Technical details: DoF, skin texture, quality markers].
```

### Era-Specific Aesthetic
Use JSON structure. Include:
- Period-accurate clothing, accessories, makeup
- Era-specific photography style (flash, grain, camera model)
- Environmental elements from the era
- Nostalgic lighting and color palette

See [JSON templates](references/json-structure-guide.md).

### 3D/Miniature Effect
```
Create a [style: isometric/chibi/diorama] 3D render of [subject].
Rendered using [Cinema 4D/C4D], [material specs: glossy/matte/PVC].
[Perspective type: isometric/axonometric].
[Scale: miniature/toy-sized].
Soft studio lighting, [color palette], clean [background color] background.
```

### Product Shot
```
Professional e-commerce product photography of [product].
Pure white background (RGB 255,255,255) with subtle contact shadow.
Soft commercial studio lighting highlighting [texture/material].
Shot on [camera] with [lens], even illumination, no harsh glare.
Sharp, color-corrected, professional retouching. High resolution.
```

## Advanced Techniques

### Multi-Element Scenes
For scenes with multiple subjects or complex interactions, use JSON to specify each element precisely. Structure sections for: subject, accessories, environment, lighting, photography, mood.

### Negative Prompts
Always include negative prompts for complex requests:
```json
{
  "negative": {
    "content": "multiple characters, wrong gender, messy composition, extreme angles, fisheye",
    "style": "no hyper-saturation, no soft focus filters, no heavy vignetting"
  }
}
```

### Text Integration
When including text in images:
- Use HEREDOC format for proper rendering
- Specify font characteristics (serif/sans-serif, bold/light, size)
- Describe text placement and styling
- Include text purpose (magazine title, poster headline, labels)

**Example:**
```
Glossy magazine cover, large bold words "Nano Banana Pro" in serif font, black on white.
Dynamic portrait in front of text. Issue number and date in corner, barcode, price.
```

### Consistency Across Variations
For generating multiple related images:
- Define "Visual Anchors" (3-6 traits that stay constant)
- Specify what changes between shots
- Maintain lighting style and color grade
- Use same technical specs across all images

## Common Patterns by Use Case

**Social Media Content:**
- Viral thumbnail style with exaggerated expressions
- Y2K scrapbook collages with multiple poses
- Mirror selfies with era-specific aesthetics

**Professional/Corporate:**
- Business headshots with studio lighting
- Magazine editorial layouts
- Corporate presentation mockups

**E-commerce:**
- Product isolation on white
- Virtual try-on with identity preservation
- 3D brand store visualizations

**Creative/Artistic:**
- Surreal compositions breaking physics
- Miniature diorama effects
- Recursive/Droste effects
- Era-accurate recreations

## Resources

This skill includes detailed reference guides:

- **[references/photorealism-portraits.md](references/photorealism-portraits.md)** - Professional portraits, era aesthetics, identity preservation techniques
- **[references/creative-experiments.md](references/creative-experiments.md)** - 3D renders, dioramas, isometric views, surreal effects
- **[references/product-commercial.md](references/product-commercial.md)** - Product photography, e-commerce, brand imagery
- **[references/editing-transformation.md](references/editing-transformation.md)** - Outpainting, background removal, style transfer
- **[references/json-structure-guide.md](references/json-structure-guide.md)** - JSON templates for complex prompts

Load these references as needed for detailed templates and examples.
