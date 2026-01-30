---
name: realistic-ugc-video
description: Create realistic long-form AI talking head/UGC videos that don't look AI-generated. Use when user wants to make "realistic AI video", "UGC video", "talking head video", "AI spokesperson", "AI ad content", "video that looks real", "human-looking AI video". Orchestrates Nano Banana for base images and Kling AI for video generation with natural pacing.
allowed-tools: Read, Bash, Task
---

# Realistic UGC Video Production

Create long-form AI videos that look and sound authentically human. This skill orchestrates a multi-step workflow using Nano Banana for realistic base images and Kling AI for video generation, with specific techniques to avoid the "AI look".

## Why Videos Look AI (And How to Fix It)

| Problem | Solution |
|---------|----------|
| Too perfect/clean skin | Add imperfections: micro-pores, natural oils, fine lines |
| Studio lighting | Use available/natural light, mixed color temps |
| Character too still | Add micro-movements, head tilts, natural sway |
| Inconsistent pacing | Use 55-60 syllables per clip |
| Robotic voice | Process through Adobe Podcast or Resemble AI |
| Obvious jump cuts | Cover with B-roll or animations |
| **Weird AI hands** | **Crop hands out of frame or keep completely static** |

## Known Limitation: Hands

AI video models (Kling, Veo, etc.) struggle with realistic hand movement. Fingers morph, gestures look unnatural, and hands are often the biggest tell.

**Best practice: Keep hands OUT of frame or completely static.**

Options:
1. **Head/shoulders framing** - Crop base image to exclude hands entirely
2. **Arms crossed** - Static pose, no finger movement needed
3. **Hands below frame** - Desk edge cuts off at wrists
4. **Cover with B-roll** - Cut away during any hand weirdness in post

## Complete Workflow

### Phase 1: Collect Requirements

Before starting, gather from the user:

1. **Character description** - Age, ethnicity, features, clothing
2. **Setting/background** - Office, home, studio, outdoor
3. **Script** - The full text the character will speak
4. **Tone** - Conversational, urgent, professional, friendly
5. **Video length target** - This determines how many clips needed

### Phase 2: Generate Base Image (Nano Banana)

Use the Nano Banana skill to generate the character image. **Critical:** Apply the imperfection techniques from [CHARACTER-PROMPTING.md](CHARACTER-PROMPTING.md).

**Key elements for realistic UGC:**
- iPhone capture aesthetic (26mm equivalent lens)
- Available/mixed lighting (NOT studio)
- Visible skin texture (pores, oils, fine lines)
- Minor imperfections (stubble, dark circles)
- Computational depth artifacts
- ISO noise (500-900 range)

**Command:**
```bash
~/.claude/skills/nano-banana/scripts/generate.sh "[enhanced prompt]" --aspect 9:16 --size 2K
```

Then optionally upscale through Enhancor AI for additional texture.

### Phase 3: Chunk the Script (Critical for Pacing)

This is the **most important step** for natural pacing. See [SCRIPT-CHUNKING.md](SCRIPT-CHUNKING.md).

**The 55-60 Syllable Rule:**
- Count syllables, not words
- Each video generation = 55-60 syllables
- Never cut mid-sentence
- Add filler sentences to reach target if needed

**Example chunking:**
```
Chunk 1 (58 syllables):
"Hey everyone, I wanted to share something that completely changed how I think about productivity. It's not another app or system."

Chunk 2 (56 syllables):
"It's actually about understanding your own energy patterns throughout the day. Once I figured this out, everything clicked into place."
```

### Phase 4: Generate Video Clips (Kling AI)

For each script chunk, generate a 10-second video clip. Use the Kling AI skill with **movement prompts** from [MOVEMENT-PROMPTING.md](MOVEMENT-PROMPTING.md).

**Key elements:**
- Hand "Home Base" Protocol
- Timestamped movement clusters
- Natural blinks, head tilts, micro-sways
- Consistent base image reference

**Spawn background agent for each clip:**
```
Task tool:
- subagent_type: "general-purpose"
- run_in_background: true
- prompt: [Include image URL, script chunk, movement prompt, output path]
```

### Phase 5: Post-Production

See [POST-PRODUCTION.md](POST-PRODUCTION.md) for detailed guidance.

1. **Assemble clips** in CapCut or similar editor
2. **Fix audio** with Adobe Podcast (minimum) or Resemble AI (for voice swap)
3. **Cover jump cuts** with B-roll or animations
4. **Remove filler sentences** if they feel awkward
5. **Export** in final resolution

## Quick Start: Single Clip Test

Before generating full video, test the workflow with one clip:

1. Generate base image with full imperfections
2. Create 10-second test video with first script chunk
3. Evaluate pacing and movement
4. Adjust prompts if needed
5. Proceed with full production

## Example Full Prompt for Base Image

```
A vertical 9:16 UGC-style video frame captured on an iPhone 11 resting on a tripod.
Medium-wide portrait at true eye-level with slightly forward-leaning posture.

[CHARACTER]: A [age] [gender] with [ethnicity] complexion, [eye color] eyes beneath
[eyebrow description], [nose description]. [Jawline/facial hair]. [Hair description].
Expression is [emotion]—[specific expression details].

[CLOTHING]: [Fitted/casual garment], [collar detail].

[SKIN TEXTURE]: Visible pores across T-zone, faint smile lines, natural oils catching
light on forehead and nose. [Age-appropriate details]. No filter, no foundation.

[FOREGROUND]: Hands rest naturally on [surface], fingers relaxed, visible veins and
knuckle texture. Nearby: [everyday objects like water bottle, phone, notebook].

[CAMERA]: Native iPhone 11 lens (26mm equivalent), slightly wide perspective, mild
barrel softness at edges. Only tiny pockets of neural blur around hair edges.

[LIGHTING]: Available light mix—cool overcast daylight from window left, warm tungsten
from desk lamp right. Soft asymmetric shadows, natural falloff. ISO noise 500-900.

[BACKGROUND]: [Realistic home/office elements]—bookshelf, [furniture], clearly visible
not heavily blurred.

[REALITY DETAILS]: Gentle 35mm film grain, light fingerprint smudge on lens, tiny dust
haze in air. No cinematic bloom, no studio finish.

Styling: raw UGC realism, available indoor light, mixed color temperature, minimal
depth blur, visible ISO noise, emphasis on authenticity.
```

## Example Movement Prompt for Video

```
Hand "Home Base" Protocol: Hands default to Active Idle. Fingers shift, thumbs rub,
wrists rotate slightly while anchored. Gestures only for key emphasis.

[0.0s-0.5s] Pre-roll: Sharp inhale, eyes lock to lens, head still
[0.5s-3.0s] Hands in Active Idle (fingers interlocked), head tilts slightly right,
           brows furrow in seriousness
[3.0s-6.0s] Hands break clasp for quick open-palm rotation then return, head drifts
           forward, natural blink
[6.0s-8.0s] Hands return to Active Idle (loose clasp, thumbs tapping), head nods
           encouragingly, cheeks lift in natural smile
[8.0s-10.0s] Hands anchored (wrist shifts), chin lifts in quick final nod, natural blink

[Script]: "[CHUNK TEXT HERE]"
[Tone]: [Urgent/Conversational/Professional/etc.]
[Pacing]: Rapid fire delivery, high energy, viral UGC style, confident, 2x speed
```

## Reference Files

- **[CHARACTER-PROMPTING.md](CHARACTER-PROMPTING.md)** - Imperfection techniques for realistic characters
- **[SCRIPT-CHUNKING.md](SCRIPT-CHUNKING.md)** - The syllable method for consistent pacing
- **[MOVEMENT-PROMPTING.md](MOVEMENT-PROMPTING.md)** - Natural movement choreography
- **[POST-PRODUCTION.md](POST-PRODUCTION.md)** - Audio fixing and editing tips

## Alternative: InfiniteTalk

For simpler long-form videos, consider InfiniteTalk (infinitetalk.ai).

**Pros:** Single generation for longer videos
**Cons:** Less control over pacing (no timer/duration control), charged by output length

Use the syllable method above when precise pacing control is needed.

## Checklist Before Generating

- [ ] Character prompt includes skin imperfections
- [ ] Lighting is available/natural, NOT studio
- [ ] Script chunked into 55-60 syllable segments
- [ ] Each chunk is complete sentences
- [ ] Movement prompt includes hand base, head movements, blinks
- [ ] Post-production plan for audio and jump cuts
