---
name: creative-direction
description: Image prompt templates, model selection guidance, and anti-generic patterns for generating visual assets. Use when the user needs AI-generated images for landing pages, marketing, or products. Covers hero images, feature illustrations, OG cards, icons, and backgrounds.
---

# Creative Direction

Image prompt templates, model selection guidance, and anti-generic patterns for generating visual assets. Covers hero images, feature illustrations, testimonial photos, OG images, and more.

## When to Use

- User needs images for a landing page, app, or marketing site
- User asks for "hero image", "feature illustration", or "OG image"
- User wants AI-generated visuals that don't look like stock photos
- User is choosing between image generation models
- User's current AI images look generic and need direction

## Core Philosophy

- **Generic is the enemy.** "A person using a laptop" produces forgettable images. Specificity creates memorability.
- **Every image has a job.** Hero = emotion + aspiration. Feature = clarity. Testimonial = trust. Know the job before prompting.
- **Model matters.** Different models excel at different things. Pick the right tool.
- **Consistency beats quality.** A cohesive set of 7/10 images beats one 10/10 with six mismatches.

---

## Model Selection Guide

### When to Use Each Model

| Model | Best For | Weaknesses | Cost |
|-------|---------|------------|------|
| **GPT-4o / DALL-E 3** | Text in images, diagrams, infographics, precise compositions | Can feel "illustrated", less photorealistic | API credits |
| **Gemini Imagen** | Photorealism, natural scenes, product shots | Less control over composition, text rendering varies | API credits |
| **Midjourney** | Artistic quality, mood, cinematic shots, brand imagery | No API (Discord-only), inconsistent with specific details | Subscription |
| **Flux (via Replicate)** | Photorealism, faces, flexible styles | Requires Replicate account | Per-image |
| **Unsplash / Pexels** | Real photography, when AI looks too AI | Limited to what exists, generic poses | Free |

### Decision Tree

```
Need text in the image? → DALL-E 3 / GPT-4o
Need photorealistic people? → Flux or Gemini
Need artistic/cinematic mood? → Midjourney
Need a specific real-world scene? → Unsplash/Pexels
Need consistency across many images? → Pick ONE model, same style prompt prefix
Need diagrams/UI mockups? → DALL-E 3 / GPT-4o
```

---

## Prompt Templates by Asset Type

### Hero Image

**Job:** Create an emotional first impression. Communicate the product's vibe in 2 seconds.

**Template:**
```
[Art style], [subject doing something specific and aspirational],
[environment with mood-setting details], [lighting description],
[color palette constraint], [composition note]
```

**Example — SaaS Product:**
```
Cinematic photograph, a product designer reviewing a clean dashboard
on a large monitor in a sunlit corner office, morning golden hour
light casting long shadows, muted blue and warm cream color palette,
shot from over the shoulder with shallow depth of field, 35mm lens feel
```

**Anti-generic patterns:**
- ❌ "A person using a computer" → ✅ "A designer reviewing analytics on a ultrawide monitor, sticky notes scattered on the desk"
- ❌ "Happy team working" → ✅ "Three engineers around a whiteboard, one mid-laugh, marker in hand, late afternoon light"
- ❌ "Technology abstract" → ✅ "Closeup of hands arranging physical cards on a table, each card showing a tiny wireframe sketch"

### Feature/Product Illustration

**Job:** Explain what a feature does. Clarity > beauty.

**Template:**
```
[Clean/minimal style], [the feature's core concept as a visual metaphor],
[simple background], [brand colors], [no text unless needed]
```

**Example — Analytics Feature:**
```
Minimal 3D illustration, a translucent glass cube containing floating
data points that form a rising trend line, soft gradient background
from white to light blue, subtle shadows, isometric perspective
```

**Tips:**
- Use visual metaphors, not literal screenshots
- Keep backgrounds simple — the illustration should work on any page section
- Maintain consistent style across all feature illustrations (same rendering style, same perspective, same color treatment)

### Testimonial / Social Proof

**Job:** Build trust. Make real people feel real.

**Approach:** Use real photos when possible (with permission). If generating:

```
Professional headshot, [specific person description with age/style details],
[neutral or office background], [natural lighting], [warm but professional mood],
shot at eye level, slight smile, [avoid uncanny valley — add imperfections]
```

**Tips:**
- Diversity matters — vary age, ethnicity, style
- Avoid the "corporate headshot" look — slightly candid feels more trustworthy
- ⚠️ AI-generated faces for testimonials is ethically questionable. Prefer real photos. If generating, be transparent about it.

### Open Graph (OG) / Social Card

**Job:** Get clicks in a feed. Must work at small sizes.

**Template:**
```
[Bold, high contrast], [simple central element],
[large readable text area (left or center)],
[brand color background or gradient], [16:9 aspect ratio],
minimal detail — this will be viewed at 600×315px
```

**Key constraints:**
- Must be readable at thumbnail size
- Text should be generated separately and composited (AI text rendering is unreliable)
- High contrast between background and text area
- Simple shapes > complex scenes

### Icon / Logo Concept

**Job:** Convey brand identity in a tiny space.

```
Minimal vector icon, [object/symbol], [single or two-color],
clean lines, works at 32px, [style: geometric/rounded/sharp],
white background, no gradients, no shadows
```

**Tips:**
- Generate concepts, then recreate in Figma/SVG for production
- AI-generated logos are starting points, not finals
- Test at small sizes — if it doesn't read at 32px, simplify

### Background / Texture

**Job:** Add depth without competing with content.

```
Abstract [texture type], [color palette], subtle variation,
tileable/seamless, low contrast, [usage: dark background with light text / light background with dark text]
```

**Texture types:** gradient mesh, noise grain, geometric pattern, organic shapes, topographic lines, dot grid

---

## Style Consistency Framework

When generating multiple images for a project, create a **style prefix** and prepend it to every prompt:

```
STYLE PREFIX: "Minimal 3D illustration, soft matte materials, isometric perspective,
pastel color palette with [brand blue] accents, subtle ambient occlusion shadows,
white background —"
```

Then each prompt becomes:
```
[STYLE PREFIX] a shield icon representing security features
[STYLE PREFIX] a speedometer showing performance optimization
[STYLE PREFIX] a connected graph showing team collaboration
```

### Consistency Checklist

- [ ] Same art style (3D, flat, photographic, etc.)
- [ ] Same color palette (or subset of it)
- [ ] Same perspective (isometric, front-facing, etc.)
- [ ] Same lighting direction
- [ ] Same level of detail/complexity
- [ ] Same background treatment

---

## Anti-Generic Playbook

### The Specificity Ladder

Each level adds memorability:

1. **Generic:** "A workspace" ❌
2. **Specific:** "A designer's workspace with a drawing tablet" ⬆️
3. **Atmospheric:** "A designer's workspace at golden hour, warm light on a Wacom tablet" ⬆️
4. **Story:** "A designer's workspace at golden hour, a half-finished illustration on the tablet, coffee cup with a lipstick mark, headphones draped over the monitor" ✅

Always aim for level 3–4.

### Overused AI Image Tropes to Avoid

| ❌ Cliché | ✅ Alternative |
|-----------|---------------|
| Glowing orbs / particles | Physical textures, natural materials |
| Floating holographic UI | Real devices, paper prototypes |
| Purple/blue gradient everything | Earth tones, brand-specific palettes |
| Isometric city blocks | Focused single-object compositions |
| Perfect symmetry | Intentional asymmetry, rule of thirds |
| Hyper-saturated colors | Muted, desaturated palette with one accent |
| "AI art style" shininess | Matte materials, film grain, imperfection |

### Adding Realism to AI Images

Include in prompts:
- **Film grain:** "slight film grain, shot on 35mm"
- **Imperfection:** "slightly worn edges", "coffee stain on the desk"
- **Natural lighting:** "overcast diffused light" instead of "bright studio lighting"
- **Depth of field:** "shallow depth of field, f/1.8" for focus
- **Texture:** "matte finish", "linen texture", "concrete surface"

---

## Output Format

When providing creative direction, output:

```
### Creative Direction: [Asset Type]

**Purpose:** What this image needs to communicate
**Model recommendation:** [Model] — [Why]
**Style:** [Art direction notes]

**Prompt:**
[Full prompt ready to paste]

**Variations to try:**
1. [Alternative angle/mood]
2. [Alternative style]

**Post-processing notes:**
- [Any needed adjustments — cropping, overlay, text addition]
```

---

## Examples

### Example 1: "I need a hero image for a project management SaaS"

**Purpose:** Communicate clarity and control over complex projects
**Model:** Midjourney (cinematic quality) or DALL-E 3 (if text needed)

**Prompt:**
```
Cinematic overhead photograph of a large wooden desk with neatly organized
project cards, color-coded sticky notes in a kanban layout, a MacBook
showing a clean dashboard, a ceramic mug, natural window light from the left,
shallow depth of field focusing on the cards, muted warm palette with
one accent color (brand blue), 35mm film aesthetic with slight grain
```

### Example 2: "Generate feature illustrations for our 4 main features"

**Style prefix:**
```
Minimal 3D illustration, soft matte clay-like materials, front-facing
perspective, brand indigo (#6366F1) as accent, light gray (#F9FAFB)
background, gentle directional shadow to the bottom-right —
```

**Prompts:**
1. `[prefix] a magnifying glass hovering over a organized grid of documents`
2. `[prefix] two puzzle pieces connecting, with a small spark at the join`
3. `[prefix] a clock face with segments in different colors showing time allocation`
4. `[prefix] a shield with a small checkmark, slightly tilted`

### Example 3: "Our AI images look too generic, help"

Audit current images against the anti-generic playbook. Common fixes:
1. Add specificity (level 3–4 on the ladder)
2. Replace cliché tropes (glowing orbs → physical textures)
3. Add film grain / imperfection to prompts
4. Constrain the color palette
5. Use consistent style prefix across all images
