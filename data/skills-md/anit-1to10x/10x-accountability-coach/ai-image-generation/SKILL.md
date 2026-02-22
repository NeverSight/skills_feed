---
name: ai-image-generation
description: "Execute AI image generation with optimal quality. Use when you need to generate images via Replicate API. Triggers on: generate image, create visual, product shot. Outputs generated images for feedback and iteration."
---

# AI Image Generation

This is the core execution skill for AI image generation. It handles the actual generation work — model selection, prompt construction, API calls, iteration, and quality verification.

**Use this skill when:** You need to generate any image and want optimal quality.
**Route here from:** ai-creative-workflow, ai-creative-strategist, or direct requests.

---

## Why This Skill Exists

**The problem:** Most people waste time and money on AI image generation because they:
1. Use the wrong model for the job
2. Write vague prompts that produce generic results
3. Generate once and hope for the best
4. Don't know how to iterate effectively

**The solution:** A systematic approach that:
- Uses the right model (Nano Banana Pro via Glif for speed + quality)
- Constructs prompts with proven structure
- Builds in iteration as the default workflow
- Knows when to stop and when to keep refining

---

## Model Selection

### Primary: Nano Banana Pro via Glif (DEFAULT)

**Why:** Fastest high-quality generation available. ~20 seconds vs ~3 minutes for comparable quality.

| Model | Glif ID | Speed | Quality |
|-------|---------|-------|---------|
| **🍌 Nano Banana Pro Text 2 Image** | `cmi7ne4p40000kz04yup2nxgh` | ~20sec | Excellent |

**Use the `run_glif` MCP tool:**
```
Glif: 🍌 Nano Banana Pro Text 2 Image
ID: cmi7ne4p40000kz04yup2nxgh
Inputs: ["Your prompt here"]
```

**Do NOT use:** imagen-3, DALL-E, Flux, or direct Replicate API calls unless specifically requested.

---

### When to Use Alternatives

```
IF user specifically requests a different model:
    use requested model

ELIF need text rendering (logos, quotes, announcements):
    use Recraft v3 or Ideogram v3 (route to ai-typography)

ELIF need image-to-video:
    generate image first, then route to ai-video-generation

ELIF need people/lifestyle imagery:
    still use Nano Banana Pro (handles people well)

ELSE:
    Nano Banana Pro via Glif  // DEFAULT
```

---

## Prompt Construction

### The Formula

```
[SUBJECT] + [SETTING/CONTEXT] + [STYLE] + [LIGHTING] + [QUALITY BOOSTERS]
```

Each element serves a purpose:
- **SUBJECT** — What you're generating (be specific)
- **SETTING** — Where/context (grounds the image)
- **STYLE** — Visual aesthetic (photography, illustration, etc.)
- **LIGHTING** — Mood and dimension (often overlooked, always important)
- **QUALITY BOOSTERS** — Technical terms that elevate output

---

### Subject Specificity

**Bad:** "A coffee cup"
**Good:** "Artisan ceramic coffee cup with latte art, steam rising"

**Bad:** "A laptop"
**Good:** "Silver MacBook Pro on oak desk, screen showing code editor"

**Bad:** "A person working"
**Good:** "Woman in her 30s, focused expression, typing on laptop in bright modern office"

The more specific your subject, the less the model has to guess.

---

### Setting/Context Options

**Studio/Clean:**
```
on pure white background
against dark charcoal gradient
floating in negative space
on seamless backdrop
```

**Environmental:**
```
in modern minimalist office
on rustic wooden table
in cozy coffee shop
against urban cityscape
```

**Abstract:**
```
with geometric patterns
surrounded by abstract shapes
with dynamic particle effects
in surreal dreamscape
```

---

### Style Presets

**Photography Styles:**
```
professional product photography
lifestyle photography
editorial fashion photography
documentary photography style
portrait photography
macro photography
aerial/drone photography
```

**Illustration Styles:**
```
digital illustration
watercolor illustration
vector art style
hand-drawn sketch style
3D rendered
isometric illustration
flat design
```

**Artistic Styles:**
```
cinematic
surrealist
minimalist
maximalist
retro/vintage
futuristic
organic/natural
```

---

### Lighting Presets

Lighting is the most underused prompt element. It dramatically affects mood and quality.

**Studio Lighting:**
```
professional studio lighting
three-point lighting setup
single dramatic spotlight
soft diffused lighting
rim lighting
```

**Natural Lighting:**
```
soft natural daylight
golden hour light
overcast diffused light
harsh midday sun
blue hour
```

**Dramatic Lighting:**
```
high contrast dramatic lighting
moody low-key lighting
backlit silhouette
chiaroscuro lighting
neon accent lighting
```

**Specific Directions:**
```
key light from upper left
side lighting from right
overhead soft box
underlighting (dramatic)
```

---

### Quality Boosters

Add these to elevate output quality:

**Technical Quality:**
```
ultra-detailed
high resolution
sharp focus
professional quality
8k resolution
```

**Professional Context:**
```
commercial photography
award-winning
magazine quality
advertising campaign
editorial quality
```

**Specific Techniques:**
```
shallow depth of field
bokeh background
lens flare
motion blur
long exposure
```

---

## Complete Prompt Examples

### Product Hero Shot
```
Premium wireless headphones floating against dark charcoal gradient,
professional product photography, single dramatic spotlight from upper left,
subtle rim lighting on edges, metallic surface reflections,
ultra-detailed, commercial advertising quality, negative space on right for text
```

### Lifestyle Scene
```
Young professional woman enjoying morning coffee in bright modern apartment,
natural window light streaming in, cozy weekend aesthetic,
lifestyle photography, warm tones, genuine relaxed expression,
shallow depth of field, editorial quality
```

### Food Photography
```
Gourmet burger with melted cheese and fresh vegetables on rustic wooden board,
professional food photography, soft diffused overhead lighting,
steam rising, appetizing presentation, shallow depth of field,
restaurant menu quality, warm inviting tones
```

### Tech/SaaS
```
Modern dashboard interface on large monitor in minimalist home office,
clean UI design visible on screen, soft ambient lighting,
tech product photography, contemporary workspace aesthetic,
shallow depth of field on screen, professional quality
```

### Abstract/Conceptual
```
Abstract representation of data flow and connectivity,
glowing particles forming network patterns against deep blue gradient,
futuristic technology aesthetic, dynamic motion blur,
cinematic quality, vibrant cyan and purple accent colors
```

---

## Aspect Ratio Guide

| Use Case | Ratio | Pixels | Notes |
|----------|-------|--------|-------|
| Square (Instagram, LinkedIn) | 1:1 | 1024×1024 | Most versatile |
| Landscape (Hero banners, YouTube) | 16:9 | 1280×720 | Web standard |
| Portrait tall (Instagram feed) | 4:5 | 1024×1280 | Better feed presence |
| Stories/TikTok | 9:16 | 1080×1920 | Vertical mobile |
| Pinterest | 2:3 | 1000×1500 | Optimal for pins |
| Wide cinematic | 21:9 | 2560×1080 | Dramatic headers |

**Default:** 1:1 unless platform-specific requirement is known.

---

## Execution Workflow

### Step 1: Clarify Requirements

Before generating, know:
```
□ What is the subject? (be specific)
□ What style/aesthetic?
□ What platform/use case?
□ What aspect ratio?
□ Any must-have elements?
□ Any must-avoid elements?
```

### Step 2: Construct Prompt

Use the formula:
```
[SUBJECT] + [SETTING] + [STYLE] + [LIGHTING] + [QUALITY BOOSTERS]
```

### Step 3: Generate First Draft

```
Glif: 🍌 Nano Banana Pro Text 2 Image
ID: cmi7ne4p40000kz04yup2nxgh
Inputs: ["[constructed prompt]"]
```

### Step 4: Present for Feedback

```markdown
## Image Generated

**Prompt:** [prompt used]
**Aspect Ratio:** [ratio]

**Image URL:** [URL]

**Quick Assessment:**
- Subject accuracy: ✓/✗
- Style match: ✓/✗
- Composition: ✓/✗
- Quality: ✓/✗

**Feedback?**
- What works?
- What should change?
- Ready to approve or iterate?
```

### Step 5: Iterate Based on Feedback

Common iteration patterns:
```
"Too dark" → Add "bright" "well-lit" "high key lighting"
"Too busy" → Add "minimal" "clean" "simple composition"
"Wrong style" → Be more explicit about style reference
"Missing element" → Add specific element to prompt
"Wrong mood" → Adjust lighting and color descriptors
```

### Step 6: Approve or Continue

- If approved → Deliver final image
- If needs changes → Return to Step 5
- If fundamentally wrong → Return to Step 2 with new prompt approach

---

## Iteration Strategies

### When It's Close But Not Right

**Problem:** Almost right but something's off
**Strategy:** Make targeted prompt adjustments

```
Original: "Coffee cup on table"
Iteration 1: "Coffee cup on table, warmer tones" (if too cool)
Iteration 2: "Coffee cup on table, warmer tones, more steam" (if missing element)
```

### When It's Completely Wrong

**Problem:** Output doesn't match intent at all
**Strategy:** Rewrite prompt from scratch with more specificity

Don't iterate on a bad foundation. Start fresh with better prompt construction.

### When Quality Is Low

**Problem:** Image looks AI-generated or low quality
**Strategy:** Add quality boosters and professional context

```
Add: "ultra-detailed, professional photography, commercial quality"
Add: "8k resolution, sharp focus, magazine quality"
```

### When Composition Is Wrong

**Problem:** Elements in wrong places, bad framing
**Strategy:** Be explicit about composition

```
Add: "subject centered in frame"
Add: "negative space on left for text"
Add: "rule of thirds composition"
Add: "close-up shot" or "wide establishing shot"
```

---

## Quality Checklist

Before delivering, verify:

### Technical Quality
- [ ] Resolution is sufficient for intended use
- [ ] No obvious AI artifacts (weird fingers, melted text, etc.)
- [ ] Sharp focus on main subject
- [ ] Appropriate for intended platform

### Compositional Quality
- [ ] Subject is clear and prominent
- [ ] Composition supports intended use (text space if needed)
- [ ] Lighting creates appropriate mood
- [ ] Colors are cohesive

### Brief Alignment
- [ ] Matches requested subject
- [ ] Matches requested style
- [ ] Matches requested mood/tone
- [ ] Usable for intended platform

---

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Generic/stock photo feel | Vague prompt | Add specific details, unique elements |
| Wrong style | Style not specified | Be explicit: "product photography style" not just "photo" |
| Poor lighting | No lighting direction | Add specific lighting: "dramatic spotlight from upper left" |
| Cluttered composition | Too many elements | Add "minimal" "clean" "simple composition" |
| AI artifacts | Model limitations | Regenerate, or note area to avoid |
| Wrong aspect ratio | Default used | Specify ratio in request |
| Doesn't match brand | No style reference | Add brand color/style keywords |
| Text rendering issues | Wrong model | Route to ai-typography for text-heavy graphics |

---

## Output Format

### Standard Output
```markdown
## Image Generated

**Subject:** [what was generated]
**Style:** [style used]
**Aspect Ratio:** [ratio]

**Image URL:** [URL]

**Prompt Used:**
> [full prompt for reference]

**Quality Check:**
- ✓ Subject accurate
- ✓ Style matches
- ✓ Composition works
- ✓ Quality sufficient

**Options:**
- [ ] Approve and use
- [ ] Iterate (specify changes)
- [ ] Generate variant
- [ ] Try different approach
```

### With Iteration Context
```markdown
## Image Generated (Iteration 2)

**Changes from v1:** [what changed]
**Image URL:** [URL]

**Comparison:**
- v1: [issue]
- v2: [improvement]

**Feedback needed?**
```

---

## Handoff Protocols

### Receiving from ai-creative-workflow
```yaml
Receive:
  subject: "[what to generate]"
  style: "[aesthetic direction]"
  platform: "[intended use]"
  aspect_ratio: "[ratio]"
  constraints: "[any limitations]"
```

### Returning to Workflow
```yaml
Return:
  status: "complete" | "needs_iteration" | "needs_different_approach"
  deliverables:
    - url: "[image URL]"
      aspect_ratio: "[ratio]"
      prompt_used: "[prompt]"
  feedback_needed: "[any questions]"
```

### Routing to Video
```yaml
Route to ai-video-generation:
  image_url: "[approved image URL]"
  aspect_ratio: "[ratio]"
  animation_intent: "[what motion is needed]"
```

---

## Integration with Creative Pipeline

```
IMAGE GENERATION PIPELINE

┌─────────────────────────────────────────┐
│  Request arrives (direct or routed)     │
│  → Clarify requirements                 │
│  → Construct prompt                     │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│  ai-image-generation (THIS SKILL)       │
│  → Generate with Nano Banana Pro/Glif   │
│  → Present for feedback                 │
│  → Iterate as needed                    │
│  → Quality check                        │
└─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
┌──────────────────┐   ┌──────────────────┐
│  Static Delivery │   │  Route to Video  │
│  → Final image   │   │  → ai-video-     │
│    delivered     │   │    generation    │
└──────────────────┘   └──────────────────┘
```

---

## Speed vs Quality Decision

```
QUICK DRAFT (concept testing):
    → Nano Banana Pro via Glif (~20 sec)
    → Good enough to evaluate concept
    → Iterate quickly

PRODUCTION QUALITY (final delivery):
    → Nano Banana Pro via Glif (~20 sec)
    → Already production quality
    → Most cases don't need more

MAXIMUM QUALITY (premium needs):
    → Direct Replicate API call to specialized model
    → Only if Glif output insufficient
    → Rare — Nano Banana Pro handles most needs
```

**Default to Glif.** It's fast AND high quality. Only go elsewhere if specific need arises.

---

## Tips from Experience

### What Works

1. **Specificity beats creativity** — "Red 2024 Tesla Model 3" beats "cool car"
2. **Lighting is underrated** — Always specify lighting direction/type
3. **Negative space matters** — Mention if you need room for text
4. **Iterate fast** — Don't overthink first prompt, generate and refine
5. **Quality boosters work** — "Professional photography, ultra-detailed" actually helps

### What Doesn't Work

1. **Vague prompts** — "Something cool" produces nothing useful
2. **Too many elements** — Keep focused, don't cram everything in
3. **Ignoring aspect ratio** — Always match to intended platform
4. **Single generation** — Plan for iteration, don't expect perfection first try
5. **Wrong model for text** — Nano Banana Pro struggles with text rendering

### The 80/20

80% of good results come from:
1. Specific subject description
2. Clear style direction
3. Explicit lighting
4. Appropriate aspect ratio

Get these four right, and you'll get good results.
