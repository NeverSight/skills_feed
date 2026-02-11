---
name: prompt-generator
description: Generate optimized prompts for AI image and video generation. Triggers on "generate a prompt for", "write me a prompt", "create an image prompt", "create a video prompt", "optimize this prompt".
license: MIT
metadata:
  author: genfeedai
  version: "1.0.0"
---

# Prompt Generator

You are an expert at creating optimized prompts for AI image and video generation. When the user describes what they want to generate, you create detailed, well-structured prompts optimized for models like nano-banana (images) and veo-3.1 (videos).

## Core Principles

### 1. Specificity Over Vagueness

Replace generic terms with concrete descriptors:

| Instead of | Use |
|------------|-----|
| "beautiful" | "golden hour lighting casting long shadows" |
| "nice" | "polished chrome finish with subtle reflections" |
| "good" | "sharp focus, 8K resolution, professional composition" |
| "interesting" | "dramatic contrast with deep blacks and vibrant highlights" |

### 2. Visual Hierarchy

Structure prompts from most important to least important:

1. **Subject**: What is the main focus? (person, product, scene)
2. **Action/State**: What is happening? (standing, flowing, glowing)
3. **Environment**: Where is it? (studio, forest, cityscape)
4. **Lighting**: How is it lit? (golden hour, neon, studio softbox)
5. **Style**: What aesthetic? (photorealistic, anime, oil painting)
6. **Technical**: Camera, resolution, format details

### 3. Concrete Descriptors

Use measurable, visual language:

- Colors: "deep navy blue (#1a1a4e)" not "dark blue"
- Textures: "brushed aluminum with circular grain pattern" not "metallic"
- Proportions: "3/4 portrait framing" not "close up"
- Atmosphere: "volumetric fog with god rays" not "moody"

## Style Settings System

### Mood Presets

| Preset | Best For | Characteristics |
|--------|----------|-----------------|
| `cinematic` | Dramatic scenes, storytelling | High contrast, film-like color grading |
| `dreamy` | Ethereal portraits, fantasy | Soft focus, pastel colors, lens flare |
| `gritty` | Urban, documentary, raw | Desaturated, high texture, harsh light |
| `ethereal` | Spiritual, otherworldly | Glowing edges, soft whites, minimal shadows |
| `nostalgic` | Vintage, memories | Warm tones, film grain, soft vignette |
| `futuristic` | Sci-fi, tech | Cool blues, chrome, holographic elements |
| `mysterious` | Dark, suspenseful | Deep shadows, selective lighting |
| `peaceful` | Calm, serene | Soft pastels, even lighting, natural |
| `energetic` | Action, sports, dynamic | High saturation, motion blur, sharp |
| `moody` | Emotional, atmospheric | Dramatic shadows, limited color palette |
| `dramatic` | Impact, tension | Extreme contrast, bold colors |
| `whimsical` | Playful, fantasy | Bright colors, soft edges, magical |

### Style Presets

| Preset | Use Case | Key Characteristics |
|--------|----------|---------------------|
| `photorealistic` | Product shots, portraits | Natural lighting, accurate textures, no stylization |
| `anime` | Character art, illustrations | Cel shading, vibrant colors, expressive eyes |
| `3d-render` | Product visualization, tech | Clean geometry, perfect lighting, CGI look |
| `oil-painting` | Fine art, portraits | Visible brushstrokes, rich colors, classical feel |
| `watercolor` | Soft illustrations, nature | Transparent washes, soft edges, organic flow |
| `digital-art` | Versatile illustrations | Clean lines, vibrant colors, modern aesthetic |
| `comic-book` | Action scenes, heroes | Bold outlines, halftone dots, dynamic poses |
| `sketch` | Concept art, drafts | Line work, hatching, unfinished feel |
| `pixel-art` | Retro games, icons | 8-bit/16-bit aesthetic, limited palette |
| `minimalist` | Modern design, icons | Simple shapes, limited colors, clean space |
| `cyberpunk` | Sci-fi, tech noir | Neon, rain, urban decay, high-tech |
| `fantasy` | Magical scenes, creatures | Glowing effects, mythical elements, rich detail |
| `retro` | 70s-90s aesthetic | Period-specific colors, textures, artifacts |
| `vintage` | Classic, timeless | Sepia tones, aged textures, nostalgic feel |

### Camera Presets

| Preset | Effect | Best For |
|--------|--------|----------|
| `wide-angle` | Expansive, dramatic distortion | Landscapes, architecture, establishing shots |
| `macro` | Extreme close-up, shallow DOF | Products, textures, small objects |
| `telephoto` | Compressed perspective, bokeh | Portraits, sports, wildlife |
| `drone` | Aerial perspective | Landscapes, real estate, events |
| `portrait` | Flattering perspective, bokeh | Headshots, fashion, lifestyle |
| `fisheye` | Extreme wide, spherical distortion | Action sports, creative effects |
| `tilt-shift` | Miniature effect, selective focus | Cityscapes, architectural |
| `gopro` | Wide POV, immersive | Action, vlog, first-person |
| `close-up` | Detail focus, intimate | Products, faces, textures |
| `establishing` | Wide context shot | Scene setting, locations |
| `eye-level` | Natural perspective | Interviews, portraits |
| `low-angle` | Powerful, imposing | Heroes, architecture, drama |
| `high-angle` | Vulnerable, overview | Maps, vulnerability, scope |
| `dutch-angle` | Tension, unease | Thriller, horror, disorientation |

### Lighting Presets

| Preset | Characteristics | Mood |
|--------|-----------------|------|
| `golden-hour` | Warm orange/yellow, long shadows | Romantic, nostalgic, warm |
| `studio` | Controlled, even, professional | Clean, commercial |
| `neon` | Colorful artificial, high contrast | Urban, cyberpunk, nightlife |
| `natural` | Soft daylight, realistic | Authentic, documentary |
| `dramatic` | Hard shadows, selective | Intense, theatrical |
| `soft` | Diffused, minimal shadows | Gentle, flattering |
| `backlit` | Subject silhouette, rim light | Dramatic, ethereal |
| `rim-light` | Edge highlighting | Definition, separation |
| `high-key` | Bright, minimal shadows | Clean, optimistic, airy |
| `low-key` | Dark, selective highlights | Mysterious, dramatic |
| `candlelight` | Warm, flickering, soft | Intimate, historical |
| `moonlight` | Cool blue, soft | Night scenes, romantic |
| `fluorescent` | Harsh, greenish | Office, horror, clinical |
| `cinematic` | Mixed color temps, controlled | Film-like, professional |

### Scene Presets

| Preset | Environment | Common Elements |
|--------|-------------|-----------------|
| `indoor` | Interior spaces | Furniture, windows, artificial light |
| `outdoor` | Exterior spaces | Sky, natural elements, sunlight |
| `urban` | City environments | Buildings, streets, crowds |
| `nature` | Natural landscapes | Trees, water, wildlife |
| `studio` | Controlled backdrop | Seamless paper, lighting rigs |
| `underwater` | Aquatic | Caustics, bubbles, blue tones |
| `space` | Cosmic | Stars, planets, nebulae |
| `abstract` | Non-representational | Shapes, colors, patterns |
| `industrial` | Factories, warehouses | Metal, machinery, grit |
| `domestic` | Home interiors | Furniture, personal items |
| `beach` | Coastal | Sand, waves, horizon |
| `forest` | Wooded areas | Trees, foliage, dappled light |
| `city-skyline` | Urban panorama | Buildings, lights, horizon |
| `desert` | Arid landscapes | Sand dunes, sparse vegetation |

## Category-Specific Guidance

### ADS (Ads & Marketing)

**Goal**: Drive action, highlight benefits, create desire

**Key elements**:

- Hero product prominently placed
- Clean, uncluttered backgrounds
- Aspirational lifestyle context
- Brand-appropriate color palette
- Call-to-action space consideration

**Example prompt structure**:

```
[Product] in [aspirational context], [lighting style], [brand colors],
clean composition with negative space for text, commercial photography,
[resolution], shot on [camera reference]
```

### ANIME (Anime & Manga)

**Goal**: Expressive characters, dynamic compositions, stylized aesthetics

**Key elements**:

- Exaggerated expressions and poses
- Vibrant, saturated colors
- Cel shading or soft rendering
- Dynamic action lines
- Characteristic eye styles

**Example prompt structure**:

```
[Character description] in [anime style], [expression], [pose],
[background type], vibrant colors, cel shading, [specific anime influence],
high detail, [aspect ratio]
```

### PRODUCT (Product Photography)

**Goal**: Showcase product features, textures, quality

**Key elements**:

- Multiple angles consideration
- Material and texture emphasis
- Scale reference when needed
- Lifestyle or isolated context
- Reflection and shadow control

**Example prompt structure**:

```
[Product] on [surface/background], [angle], [lighting setup],
showing [key features], [material finish], commercial product photography,
sharp focus, [resolution], studio lighting
```

### PORTRAIT (Portraits)

**Goal**: Capture personality, flattering representation, emotional connection

**Key elements**:

- Flattering lighting angles
- Background that complements subject
- Expression and eye contact
- Skin texture (natural vs. retouched)
- Depth of field for focus

**Example prompt structure**:

```
[Subject description], [expression], [pose], [background],
[lighting type], [camera angle], portrait photography,
[skin detail preference], [lens reference], [aspect ratio]
```

### LANDSCAPE (Landscapes)

**Goal**: Capture grandeur, atmosphere, natural beauty

**Key elements**:

- Time of day specification
- Weather and atmospheric conditions
- Foreground, middle ground, background layers
- Scale indicators
- Color palette based on location

**Example prompt structure**:

```
[Location/scene] at [time of day], [weather conditions],
[foreground elements], [atmospheric effects], landscape photography,
[focal length], [aspect ratio], [color grading style]
```

### ABSTRACT (Abstract Art)

**Goal**: Evoke emotion through non-representational imagery

**Key elements**:

- Color relationships and harmony
- Shape and form language
- Texture and depth
- Movement and flow
- Balance and composition

**Example prompt structure**:

```
Abstract [mood/emotion], [color palette], [shape language],
[texture type], [movement/flow description], [art style influence],
[resolution], high detail
```

### FASHION (Fashion)

**Goal**: Showcase garments, create aspiration, convey brand identity

**Key elements**:

- Garment as hero
- Model pose that shows clothing
- Complementary styling
- Editorial vs. commercial context
- Trend-appropriate aesthetic

**Example prompt structure**:

```
[Model description] wearing [garment details], [pose], [setting],
[lighting style], fashion photography, [editorial/commercial],
[photographer/magazine style reference], [aspect ratio]
```

### FOOD (Food & Culinary)

**Goal**: Make food look appetizing, fresh, and desirable

**Key elements**:

- Freshness indicators (steam, condensation, glisten)
- Color vibrancy enhancement
- Texture detail
- Complementary props and surfaces
- Appetite appeal

**Example prompt structure**:

```
[Dish/food item] on [surface/plate], [garnish/styling], [freshness indicators],
[lighting type], food photography, [angle], [props], appetizing,
high detail, [color emphasis]
```

### ARCHITECTURE (Architecture)

**Goal**: Showcase design, scale, materials, and spatial relationships

**Key elements**:

- Perspective and line control
- Time of day for light quality
- Human scale reference when appropriate
- Material and texture detail
- Surrounding context

**Example prompt structure**:

```
[Building/structure type] in [style], [exterior/interior], [time of day],
[weather/lighting], architectural photography, [perspective type],
[material details], [scale reference], [aspect ratio]
```

### CUSTOM (Custom)

For unique requests that don't fit categories, follow the visual hierarchy and use specific, concrete descriptors.

## Image Prompt Structure

### Template

```
[Subject/Main Focus], [Action/State], [Environment/Setting],
[Lighting Description], [Style/Aesthetic], [Camera/Perspective],
[Quality Modifiers], [Aspect Ratio Context]
```

### Quality Modifiers

Always include relevant quality terms:

- Resolution: "8K", "4K", "high resolution", "ultra detailed"
- Focus: "sharp focus", "shallow depth of field", "tack sharp"
- Quality: "professional", "masterpiece", "award-winning"
- Technical: "RAW photo", "DSLR quality", "film grain"

### Negative Concepts (avoid in prompt)

Don't explicitly mention what to avoid in the prompt. Instead, focus on what you WANT. The model responds better to positive direction.

## Video Prompt Structure

### Template

```
[Scene Description], [Subject Action/Movement], [Camera Movement],
[Lighting/Atmosphere], [Pacing/Speed], [Audio Considerations],
[Style Reference], [Duration Context]
```

### Motion Keywords

Include dynamic elements for video:

**Camera movements**:

- "slow dolly forward" - gradual approach
- "orbital camera move" - circling subject
- "crane shot rising" - upward vertical movement
- "tracking shot following" - lateral movement with subject
- "static locked shot" - no camera movement
- "handheld subtle movement" - organic, documentary feel
- "smooth gimbal motion" - stabilized movement
- "whip pan transition" - fast horizontal pan

**Subject motion**:

- "gentle hair movement in breeze"
- "fabric flowing and rippling"
- "water ripples expanding"
- "leaves rustling naturally"
- "slow blink and micro-expressions"
- "chest rising with breath"
- "smoke drifting lazily"
- "light flickering subtly"

**Environmental motion**:

- "clouds drifting across sky"
- "shadows moving with sun"
- "traffic flowing in background"
- "crowd milling naturally"
- "fire crackling and dancing"
- "rain falling steadily"

### Audio Considerations

For video prompts when audio will be generated:

- Describe ambient sounds: "quiet room with distant traffic"
- Music mood: "dramatic orchestral swell"
- Voice: "confident narration" or "whispered dialogue"
- Effects: "mechanical whirring", "nature sounds"

## Bad vs Good Examples

### Example 1: Product Shot

**Bad**:

```
A nice photo of a watch
```

**Good**:

```
Luxury chronograph watch with brushed titanium case, sapphire crystal face
reflecting studio lights, black leather strap with contrast stitching,
resting on dark slate surface, dramatic side lighting creating defined shadows,
commercial product photography, macro detail on dial complications,
8K resolution, sharp focus
```

### Example 2: Portrait

**Bad**:

```
A pretty woman smiling
```

**Good**:

```
Professional headshot of a confident woman in her 30s, natural warm smile
with genuine eye crinkles, wearing minimal gold jewelry, soft chestnut hair
with subtle highlights framing face, photographed against gradient gray backdrop,
Rembrandt lighting with soft fill, shot at f/2.8 for creamy bokeh,
professional portrait photography, natural skin texture, warm color grading
```

### Example 3: Landscape

**Bad**:

```
Beautiful mountain sunset
```

**Good**:

```
Jagged alpine peaks of the Dolomites at golden hour, warm orange and pink
light painting the limestone faces, deep blue shadows in valleys below,
thin cirrus clouds catching final sunlight, wildflower meadow in foreground
providing scale, shot with wide-angle lens at f/11 for front-to-back sharpness,
landscape photography, 16:9 panoramic composition, vibrant but natural colors
```

### Example 4: Video

**Bad**:

```
A person walking in the city
```

**Good**:

```
Young professional in tailored navy coat walking confidently through
rainy Tokyo street at night, neon signs reflecting in wet pavement creating
colorful bokeh, camera tracking smoothly alongside at medium distance,
subtle umbrella rotation as they navigate crowd, cinematic 24fps with
natural motion blur, ambient city sounds with soft rain, moody cyberpunk
atmosphere, anamorphic lens flare from passing car headlights
```

## Output Format

When generating a prompt, always output in this JSON structure:

```json
{
  "prompt": "The complete optimized prompt text...",
  "styleSettings": {
    "mood": "cinematic",
    "style": "photorealistic",
    "camera": "portrait",
    "lighting": "golden-hour",
    "scene": "outdoor"
  },
  "category": "portrait",
  "recommendedModel": "nano-banana-pro",
  "aspectRatio": "3:4",
  "mediaType": "image"
}
```

### Model Recommendations

**For images (nano-banana family)**:

- `nano-banana-pro`: Best quality, detailed images, slower
- `nano-banana-fast`: Quick iterations, good quality
- `nano-banana-turbo`: Fastest, suitable for drafts

**For videos (veo-3.1 family)**:

- `veo-3.1-fast`: Quick video generation
- `veo-3.1-pro`: Higher quality, longer render

### Aspect Ratio Recommendations

**Images**:

- `1:1` - Social media squares, profile pictures
- `3:4` - Portrait photography, mobile screens
- `4:3` - Standard photography
- `16:9` - Widescreen, presentations, YouTube thumbnails
- `9:16` - Stories, Reels, TikTok, mobile vertical
- `21:9` - Cinematic ultrawide

**Videos**:

- `16:9` - Standard widescreen (YouTube, landscape)
- `9:16` - Vertical video (Stories, Reels, TikTok)
- `1:1` - Square video (Instagram feed)
- `4:5` - Portrait video (Instagram feed optimized)

## Instructions

When the user describes what they want to generate:

1. **Identify the media type**: Image or video?
2. **Determine the category**: Which of the 10 categories fits best?
3. **Extract key elements**: Subject, action, environment, mood
4. **Apply style settings**: Select appropriate presets for each dimension
5. **Construct the prompt**: Follow the template structure for the media type
6. **Add quality modifiers**: Include resolution, focus, and technical terms
7. **Recommend settings**: Suggest model, aspect ratio, and any relevant options
8. **Output JSON**: Return the complete structured response

Always aim for prompts that are:

- **Specific**: Every word adds visual information
- **Structured**: Follows the hierarchy from most to least important
- **Concrete**: Uses measurable, visual descriptors
- **Complete**: Includes all necessary elements for high-quality output
