---
name: midjourney-replicate-flux
description: Generate highly detailed, Midjourney-style image prompts optimized for the FLUX 1.1 Pro model on Replicate. Transform basic user descriptions into rich, cinematic prompts with professional photography qualities, dramatic lighting, and editorial-quality aesthetics. Use when users request image generation, need prompt enhancement, or want Midjourney-quality outputs via FLUX 1.1 Pro.
---

# Midjourney-Style Prompt Generator for FLUX 1.1 Pro

Generate professional, Midjourney-quality image prompts optimized for the `black-forest-labs/flux-1.1-pro` model on Replicate.

## Purpose

Transform basic user image requests into rich, detailed prompts that produce Midjourney-quality results using the FLUX 1.1 Pro model. This skill provides:

- Midjourney aesthetic principles and visual characteristics
- FLUX 1.1 Pro model optimization techniques
- Prompt structure templates and patterns
- Before/after transformation examples
- Direct integration with the Replicate MCP server

## When to Use This Skill

Use this skill when:
- User requests image generation via FLUX or Replicate
- User wants "Midjourney-style" or "cinematic" images
- User provides basic image descriptions that need enhancement
- User asks for prompt optimization or improvement
- User requests professional, editorial, or artistic photography
- User wants to generate high-quality AI images

**Trigger phrases**: "generate an image", "create a photo of", "Midjourney style", "cinematic image", "professional photography", "make me a picture of", "FLUX image generation"

## How to Use This Skill

### Step 1: Understand User Intent

Clarify what the user wants to create. Ask targeted questions if the request is too vague:
- What is the main subject?
- What mood or atmosphere do they want?
- What style or genre (portrait, landscape, product, etc.)?
- Any specific preferences (time of day, colors, composition)?

Keep questions focused and avoid overwhelming the user with too many at once.

### Step 2: Select Appropriate Prompt Pattern

Based on the genre, consult `references/midjourney-style-guide.md` for the relevant prompt pattern:
- **Portrait Photography** - People, characters, headshots
- **Landscape/Environment** - Nature, cityscapes, locations
- **Product Photography** - Objects, commercial shots
- **Architectural** - Buildings, structures, interiors
- **Fashion Editorial** - Models, clothing, styling
- **Conceptual/Artistic** - Abstract, surreal, artistic concepts

Each pattern provides a structured template for building prompts in that genre.

### Step 3: Build Layered Prompt

Construct the prompt following the 5-layer structure from `references/midjourney-style-guide.md`:

**Layer 1: Main Subject & Core Composition** (Required)
```
[Subject] [action/pose/position], [composition placement]
```

**Layer 2: Visual Style & Aesthetic** (Required)
```
[art style/movement], [mood descriptor], [color treatment]
```

**Layer 3: Lighting & Environment** (Highly Recommended)
```
[lighting type], [time of day], [weather/atmosphere]
```

**Layer 4: Technical Details & Quality Enhancers** (Recommended)
```
[camera/lens specs], [depth of field], [quality terms]
```

**Layer 5: Artistic References & Influences** (Optional)
```
[artist name], [art movement], [cultural reference]
```

### Step 4: Apply FLUX Optimizations

Enhance the prompt for FLUX 1.1 Pro by consulting `references/flux-model-optimization.md`:

1. **Add explicit artistic treatment**: FLUX is more literal than Midjourney, so specify "cinematic", "editorial", "artistic photography"

2. **Define color grading clearly**: Don't rely on automatic enhancement; specify exact color treatment

3. **Request composition explicitly**: State framing, perspective, and compositional techniques

4. **Include professional quality markers**: "professional photography", "award-winning", "expert color grading"

5. **Use technical photography anchors**: Camera, lens, aperture specifications ground the image in photographic reality

### Step 5: Verify Quality

Check the enhanced prompt against the quality checklist from `references/midjourney-style-guide.md`:
- [ ] Word count is 40-75 words
- [ ] Main subject is clearly defined
- [ ] Lighting is specified with direction and quality
- [ ] Mood/atmosphere is conveyed
- [ ] Technical photography details are present
- [ ] Color treatment is mentioned
- [ ] Composition guidance is included
- [ ] Quality enhancers are present (2-3 minimum)
- [ ] Prompt flows naturally when read aloud
- [ ] No redundant or contradictory terms

### Step 6: Generate Image via Replicate MCP Server

Use the installed Replicate MCP server to generate the image. Call the `mcp__replicate__create_predictions` tool with these parameters:

```json
{
  "version": "black-forest-labs/flux-1.1-pro",
  "input": {
    "prompt": "[Your enhanced Midjourney-style prompt here]",
    "aspect_ratio": "16:9",
    "output_format": "png"
  }
}
```

**Default configuration for Midjourney-style outputs:**
- **aspect_ratio**: `"16:9"` (widescreen, cinematic format)
- **output_format**: `"png"` (highest quality, lossless)
- **safety_tolerance**: 2 (default, balanced - can increase to 3-4 for artistic content if needed)

**Alternative aspect ratios** (from `references/flux-model-optimization.md`):
- `"1:1"` - Square (social media, portraits)
- `"2:3"` or `"4:5"` - Portrait orientation
- `"3:2"` - Classic photo ratio
- `"21:9"` - Ultra-widescreen (panoramic)

The MCP server will return a prediction object. Monitor the prediction status and provide the user with the output image URL when generation completes.

### Step 7: Offer Variations (When Requested)

If the user requests multiple options or variations, provide 2-3 alternative prompts that emphasize different aspects:
- **Variation 1**: Different lighting (golden hour vs blue hour)
- **Variation 2**: Different composition (wide shot vs close-up)
- **Variation 3**: Different mood (dramatic vs serene)

Each variation should maintain the core subject while exploring different artistic directions.

## Reference Documentation

The skill includes three comprehensive reference files that should be consulted during prompt creation:

### 1. `references/midjourney-style-guide.md`

**When to load**: Always consult when building any Midjourney-style prompt

**Contains**:
- Core Midjourney aesthetic principles
- 5-layer prompt structure template
- Midjourney-quality descriptive vocabulary
- Lighting, composition, mood, color, and technical terms
- Common prompt patterns for each genre
- Artistic movement and style references
- Quality control checklist
- Common mistakes to avoid

**Search patterns** (use for quick access to specific sections):
- "Portrait Photography pattern" - Get portrait template
- "Landscape pattern" - Get landscape template
- "Lighting Terms" - Get lighting vocabulary
- "Color & Tone" - Get color treatment options
- "Quality Enhancers" - Get quality modifiers

### 2. `references/flux-model-optimization.md`

**When to load**: Consult when optimizing prompts for FLUX or troubleshooting results

**Contains**:
- FLUX 1.1 Pro specifications and parameters
- Replicate MCP server usage instructions
- FLUX vs Midjourney adaptation strategies
- Model-specific optimization techniques
- Aspect ratio and output format guide
- Safety tolerance settings
- Prompt engineering strategies for FLUX
- Troubleshooting common issues

**Search patterns**:
- "Aspect Ratios" - Get ratio options
- "FLUX Strengths" - Understand what FLUX does best
- "Adaptation Techniques" - Learn FLUX-specific adjustments
- "Parameter Selection" - Choose optimal parameters
- "Troubleshooting" - Fix common issues

### 3. `references/prompt-examples.md`

**When to load**: When learning prompt transformation or seeking inspiration

**Contains**:
- 16 complete before/after transformation examples
- Examples across all major genres (portrait, landscape, product, etc.)
- Word count verification for each example
- Detailed explanations of why each enhancement works
- Transformation principles summary
- Enhancement formula and process

**Search patterns**:
- "Portrait examples" - See portrait transformations
- "Landscape examples" - See landscape transformations
- "Product Photography examples" - See product transformations
- "Transformation Principles" - Understand the enhancement process

## Practical Workflow

### Example 1: Simple Request Enhancement

**User**: "Create an image of a woman in a garden"

**Process**:
1. Identify genre: Portrait photography in outdoor setting
2. Consult `references/midjourney-style-guide.md` for portrait pattern
3. Build layered prompt:
   - Subject: Woman in garden setting
   - Style: Editorial portrait photography
   - Lighting: Golden hour natural light
   - Technical: Canon R5 85mm f/1.4
   - Quality: Highly detailed, professional
4. Apply FLUX optimizations from `references/flux-model-optimization.md`:
   - Add "cinematic composition"
   - Specify "warm color grading"
   - Include "shallow depth of field"
5. Verify: 52 words ✓

**Enhanced Prompt**:
"Woman in flowing dress standing among blooming roses, garden setting, editorial portrait photography, golden hour sunlight filtering through trees, warm and romantic atmosphere, shot on Canon R5 85mm f/1.4, shallow depth of field with soft bokeh background, warm color grading with rich earth tones, cinematic composition, highly detailed, professional photography"

6. Generate via MCP server with aspect_ratio "16:9", output_format "png"

### Example 2: Genre-Specific Request

**User**: "Generate a photo of a vintage car on a coastal road"

**Process**:
1. Identify genre: Automotive photography with landscape elements
2. Consult automotive pattern from `references/prompt-examples.md`
3. Build prompt emphasizing:
   - Specific car era (1960s convertible)
   - Evocative setting (coastal highway overlook)
   - Nostalgic mood with film grain
4. Apply FLUX techniques:
   - Specify chrome and paint details FLUX excels at
   - Request warm nostalgic color grading explicitly
5. Verify quality checklist

**Enhanced Prompt**:
"1960s vintage convertible parked on coastal highway overlook, sunset ocean view in background, automotive editorial photography, golden hour side lighting, warm nostalgic color grading with slight film grain, shot on Canon R5 50mm f/1.4, shallow depth of field isolating car, emphasize chrome details and period-correct paint, sense of freedom and nostalgia, highly detailed, professional automotive photography"

6. Generate via MCP server

### Example 3: Multiple Variations

**User**: "Create a cityscape image, give me a few options"

**Process**:
1. Create three variations emphasizing different aspects
2. Reference `references/midjourney-style-guide.md` for urban photography vocabulary

**Variation 1 - Blue Hour**:
"Modern city skyline at blue hour twilight, glowing office building windows, cinematic urban photography, dramatic perspective from elevated viewpoint, shot on Sony A7R IV 24mm, deep focus, cool color grading with blue and purple tones, atmospheric haze, highly detailed, 8k resolution"

**Variation 2 - Golden Hour**:
"Urban cityscape bathed in golden hour sunlight, warm light on building facades, cinematic architectural photography, wide angle establishing shot, shot on Canon R5 24-70mm, rich color saturation with warm orange tones, long shadows creating depth, highly detailed, professional photography"

**Variation 3 - Night Scene**:
"City lights at night with light trails from traffic, vibrant urban photography, long exposure creating motion blur, shot on Sony A7R IV 35mm, dynamic composition, neon colors and warm street lights, atmospheric and energetic, highly detailed, 8k resolution"

3. Generate all three via MCP server, present options to user

## Important Notes

### Do Not Create Custom Scripts

**CRITICAL**: The Replicate MCP server is already installed and provides all necessary API integration. Do NOT create Python scripts, Node.js code, or any other custom code for API calls. Always use the `mcp__replicate__create_predictions` tool directly.

### Prompt Length Management

Always aim for 40-75 words:
- **Under 40 words**: Risk losing Midjourney aesthetic richness
- **40-60 words**: Optimal for most prompts
- **60-75 words**: Complex scenes with multiple elements
- **Over 75 words**: Diminishing returns, potential confusion

If a prompt exceeds 75 words, consolidate by removing redundant quality terms while maintaining core elements.

### Quality Over Quantity

Better to have one excellent, well-crafted prompt than multiple mediocre ones. Take time to thoughtfully layer the elements.

### Be Specific, Not Generic

Replace vague terms with specific descriptions:
- ❌ "beautiful lighting" → ✅ "golden hour sunlight from behind creating rim light"
- ❌ "nice colors" → ✅ "warm color grading with rich earth tones and orange highlights"
- ❌ "good quality" → ✅ "shot on Canon R5 85mm f/1.4, professional photography"

### Learn From Examples

The `references/prompt-examples.md` file contains 16 complete transformations. Study these to understand the enhancement process and internalize the patterns.

### Artistic References

Use artistic references when appropriate, but ensure they're relevant:
- Photography: Annie Leibovitz, Peter Lindbergh, Steve McCurry, Ansel Adams
- Cinematography: Blade Runner 2049, The Grand Budapest Hotel, Her
- Art Movements: Impressionism, Surrealism, Minimalism, Art Nouveau

Don't force references if they don't fit the request naturally.

### FLUX-Specific Adaptations

Remember that FLUX 1.1 Pro differs from Midjourney:
- More literal interpretation (less automatic artistic elevation)
- Excels at photorealism and fine detail
- Superior text rendering in images
- More accurate colors (less stylized)
- Needs explicit quality and style instructions

Always compensate by adding clear artistic direction in the prompt.

## Success Criteria

A successful Midjourney-style prompt for FLUX 1.1 Pro should:

1. ✅ Transform generic requests into rich, detailed descriptions
2. ✅ Maintain 40-75 word length for optimal results
3. ✅ Include all core elements: subject, style, lighting, technical specs, color, quality
4. ✅ Read naturally and coherently without contradictions
5. ✅ Leverage FLUX's strengths (photorealism, detail, complex compositions)
6. ✅ Compensate for FLUX's differences from Midjourney (explicit artistic treatment)
7. ✅ Generate images via Replicate MCP server with appropriate parameters
8. ✅ Produce outputs matching Midjourney's distinctive aesthetic quality

When these criteria are met, the resulting images should exhibit:
- Ultra-detailed rendering with sharp focus
- Cinematic composition and dramatic lighting
- Professional color grading with tonal depth
- Editorial quality and artistic refinement
- That distinctive "Midjourney look" of polished, magazine-worthy imagery
