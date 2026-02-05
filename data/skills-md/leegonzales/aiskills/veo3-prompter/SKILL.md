---
name: veo3-prompter
description: Craft professional video prompts for Google Veo 3.1 using cinematic techniques, audio direction, and timestamp choreography. Use when generating AI videos, creating video prompts, or working with Veo 3.
---

# Veo 3.1 Video Prompter

Transform ideas into professional Veo 3.1 prompts using cinematic structure, audio direction, and multi-shot choreography.

## When to Use

Invoke when user:
- Says "create a video prompt" or "generate a Veo prompt"
- Wants to "make a video of..." or "animate this..."
- Asks for help with "video generation" or "AI video"
- Needs "Veo 3" or "Veo 3.1" prompt assistance
- Wants to create "multi-shot" or "cinematic" video sequences

## Core Prompt Formula

**[Cinematography] + [Subject] + [Action] + [Context] + [Style & Audio]**

Every prompt should address these five elements for maximum control.

## Prompt Density: Finding the Sweet Spot

Prompts fail in two directions:
- **Too sparse:** Model fills gaps unpredictably, you lose creative control
- **Too dense:** Model can't execute all instructions, produces confused output

### The Priority Framework

**Tier 1 - MUST INCLUDE (model needs these):**
- Shot size (wide/medium/close-up)
- Subject identity (who/what is in frame)
- Primary action (what happens)
- One dominant mood/style word

**Tier 2 - SHOULD INCLUDE (significant impact):**
- Camera movement OR angle (pick one, not both)
- Lighting quality (natural/dramatic/soft)
- One audio layer (dialogue OR SFX OR ambient)
- Setting/environment

**Tier 3 - NICE TO HAVE (diminishing returns):**
- Secondary audio layers
- Specific lens type
- Color palette details
- Film stock/grain texture
- Background action

**Rule of thumb:** Include all Tier 1, most of Tier 2, and 1-2 from Tier 3.

### Density Comparison

**TOO SPARSE (model guesses too much):**
> "A professor talking about philosophy"

**TOO DENSE (model overloaded):**
> "Medium close-up shot at eye level with a 50mm lens at f/1.8 creating shallow depth of field with bokeh highlights, of a 52-year-old female professor with silver-streaked auburn hair pulled back in a loose bun, wearing an olive tweed jacket with leather elbow patches over a cream silk blouse with a small pearl brooch, standing in a contemporary lecture hall with tiered mahogany seating and brass fixtures visible in the soft background, natural diffused daylight streaming through floor-to-ceiling windows on the left side creating soft rembrandt lighting on her face with a gentle fill from reflected light on the right..."

**OPTIMAL (directed but breathable):**
> "Medium close-up of a professor in her 50s, tweed jacket, standing in a university lecture hall. She gestures while speaking: 'Kant asked one question: could everyone do this?' Warm natural window light from left, soft academic atmosphere. SFX: marker on whiteboard."

### Calibration Signals

**Signs your prompt is too sparse:**
- Results vary wildly between generations
- Key elements missing or wrong
- Mood/tone inconsistent with intent

**Signs your prompt is too dense:**
- Model ignores some instructions entirely
- Unnatural or frozen-looking motion
- Conflicting elements appear (e.g., both day and night)
- Audio doesn't match visual action

### Iteration Strategy

1. **Start with Tier 1 only** - generate test
2. **Add Tier 2 elements** that matter most to your vision
3. **Add ONE Tier 3 detail** if something specific is missing
4. **Remove any element the model consistently ignores**

See `references/prompt-calibration.md` for detailed examples and troubleshooting.

## Cinematography Elements

### Shot Composition
- Wide shot, medium shot, close-up, extreme close-up
- Single shot, two shot, over-the-shoulder shot
- High angle, low angle, eye level, worm's eye, bird's eye

### Camera Movement
- Dolly (in/out), tracking shot, crane shot
- Pan (left/right), tilt (up/down), zoom
- Steadicam, handheld, aerial, POV

### Lens & Focus
- Shallow depth of field, deep focus
- Wide-angle lens, telephoto, macro lens
- Soft focus, rack focus, bokeh

## Audio Direction

Veo 3.1 generates synchronized sound. Direct it explicitly:

**Dialogue** (use quotes):
> "A man says, 'The storm is coming.'"

**Sound Effects** (label with SFX):
> "SFX: Thunder rumbles in the distance, rain patters on glass"

**Ambient Noise**:
> "Ambient noise: busy café chatter, clinking cups, soft jazz"

**Music**:
> "A swelling orchestral score begins to play"

## Timestamp Prompting

For multi-shot sequences within one generation (max 8 seconds):

```
[00:00-00:02] Medium shot of a detective at his desk, lighting a cigarette.
SFX: Match strike, paper rustling.

[00:02-00:04] Close-up of his eyes narrowing as he reads a letter.
Ambient: Rain against the window.

[00:04-00:06] Reverse shot of a shadowy figure in the doorway.
A woman's voice: "You shouldn't have looked."

[00:06-00:08] Wide shot as the detective stands, reaching for his gun.
SFX: Chair scraping, thunder crack.
```

## Style Keywords

**Visual Aesthetic:**
- Photorealistic, cinematic, documentary, animation
- Retro (sepia, grainy film, 1980s vaporwave)
- Noir, epic fantasy, sci-fi, romantic, horror

**Mood & Lighting:**
- Warm golden hour, cool blue tones, moody shadows
- Harsh fluorescent, soft morning light, dramatic chiaroscuro
- Neon-lit, candlelit, overcast diffused

**Film Grain Tip:**
> Add "slightly grainy, film-like" to avoid overly clean AI look

## Output Formats

**Quick Prompt:** Single sentence for simple shots
**Structured Prompt:** Multi-line with all five elements
**Timestamp Sequence:** Choreographed multi-shot within 8s
**Storyboard Mode:** Multiple prompts for full narrative

## Example Prompts

**Action Shot:**
> "Tracking shot following a parkour athlete sprinting across rooftops at sunset, warm orange light, urban cityscape background, cinematic, shallow depth of field. SFX: footsteps on concrete, wind rushing past."

**Dialogue Scene:**
> "Medium two-shot in a dimly lit bar, a woman in red leans toward a man in a suit. She says quietly, 'I know what you did.' Ambient: jazz music, glasses clinking. Moody noir aesthetic, warm tungsten lighting."

**Nature Documentary:**
> "Slow-motion close-up of a hummingbird drinking from a flower, macro lens with shallow focus, lush green garden background, soft morning light. SFX: gentle buzzing, birdsong."

## Technical Specs

- **Duration:** 4, 6, or 8 seconds
- **Resolution:** 720p or 1080p
- **Aspect Ratio:** 16:9 (landscape) or 9:16 (portrait)
- **Frame Rate:** Configurable (default: 24 FPS)

## Advanced API Options

When using Veo through API (not Flow), these additional parameters are available:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `negativePrompt` | Elements to exclude from the video | - |
| `seed` | RNG seed for reproducible results (same prompt + seed = same video) | Random |
| `enhancePrompt` | Let the model rewrite your prompt for better results | false |
| `generateAudio` | Generate synchronized audio | true |
| `personGeneration` | Control person generation: `dont_allow` or `allow_adult` | - |
| `referenceImages` | Up to 3 asset images OR 1 style image for consistency | - |

### Negative Prompts

Explicitly exclude unwanted elements:
> "A forest at sunset" + negativePrompt: "people, animals, buildings"

### Seed for Consistency

Use the same seed to reproduce similar results:
> First generation: seed=12345 → video A
> Same prompt + seed=12345 → nearly identical video

Useful for:
- Iterating on a specific "look"
- Creating variations with controlled changes
- A/B testing different prompts

### Reference Images

Maintain visual consistency across shots using reference images:

**Asset References (up to 3):**
- Character appearances
- Locations/settings
- Props or products

**Style References (1):**
- Overall aesthetic
- Color palette
- Visual treatment

## References

- `references/prompt-calibration.md` - Finding the right detail level
- `references/cinematography-glossary.md` - Full camera terms
- `references/prompt-examples.md` - 20+ categorized examples
- `references/advanced-workflows.md` - Image-to-video, first/last frame
