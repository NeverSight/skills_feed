---
name: video-generation
description: >
  Use this skill for AI video generation. Triggers include:
  "generate video", "create video", "make video", "animate", "text to video", "video from image", "video of",
  "animate image", "bring to life", "make it move", "add motion", "video with audio", "video with dialogue"
  Supports text-to-video, image-to-video, video with dialogue/audio using Google Veo 3.1 (default) or OpenAI Sora.
---

# Video Generation Skill

Generate videos using AI (Google Veo 3.1, OpenAI Sora).

**Capabilities:**
- 🎬 **Text-to-Video**: Create videos from text descriptions
- 🖼️ **Image-to-Video**: Animate images as the first frame
- 🔊 **Audio Generation**: Dialogue, sound effects, ambient sounds (Veo 3+)
- 🎭 **Reference Images**: Guide video content with up to 3 reference images (Veo 3.1)

## Prerequisites

### Default: Vertex AI (10 requests/minute) ⭐

Vertex AI is the default backend with 1400x higher rate limits:

```bash
# 1. Set your project
export GOOGLE_CLOUD_PROJECT=your-project-id

# 2. Authenticate (opens browser)
gcloud auth application-default login

# 3. Enable the API (one-time)
gcloud services enable aiplatform.googleapis.com
```

Add to your `.env` file:
```
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

### Fallback: AI Studio (10 requests/day)

Only use if you don't have a GCP project:

- `GOOGLE_API_KEY` - Get from https://aistudio.google.com/apikey

### For Sora (OpenAI)

- `OPENAI_API_KEY` - For OpenAI Sora

## Available Models

### Google Veo Models

| Model | Description | Best For |
|-------|-------------|----------|
| `veo-3.1` | Highest quality (default) | Professional videos, dialogue, reference images |
| `veo-3.1-fast` | Faster processing | Quick iterations, batch generation |

**Both models include:**
- 720p/1080p resolution
- 4, 6, or 8 second duration
- Native audio (dialogue, SFX, ambient)
- Image-to-video (animate images)
- Reference images (up to 3)
- Video extension
- Batch/parallel generation

### OpenAI Sora
- **Best for**: Creative videos, cinematic quality, complex motion
- **Resolutions**: 480p, 720p, 1080p
- **Durations**: 5s, 10s, 15s, 20s
- **Features**: Text-to-video, image-to-video

## Workflow

### Step 1: Gather Requirements (REQUIRED)

⚠️ **Use interactive questioning — ask ONE question at a time.**

#### Question Flow

⚠️ **Use the `AskUserQuestion` tool for each question below.** Do not just print questions in your response — use the tool to create interactive prompts with the options shown.

**Q1: Image**
> "I'll generate that video for you! First — **do you have an image to animate?**
> 
> - Yes (provide path — I'll use it as the first frame)
> - No, generate from scratch"

*Wait for response.*

**Q2: Audio**
> "What **audio preference**?
> 
> - With audio (default) — Veo 3.1 generates dialogue, SFX, ambient
> - Silent video — no audio"

*Wait for response.*

**Q3: Model**
> "Which **model** would you like?
> 
> - `veo-3.1` — Latest, highest quality with audio (default)
> - `veo-3.1-fast` — Faster processing with audio
> - `veo-3` / `veo-3-fast` — Previous generation with audio
> - `sora` — OpenAI, up to 20 seconds, no audio"

*Wait for response.*

**Q4: Duration**
> "What **duration**?
> 
> - 4 seconds
> - 6 seconds
> - 8 seconds (default)"

*Wait for response.*

**Q5: Format**
> "What **aspect ratio and resolution**?
> 
> - 16:9 landscape, 720p
> - 16:9 landscape, 1080p
> - 9:16 portrait, 720p
> - 9:16 portrait, 1080p
> - Or specify"

*Wait for response.*

#### Quick Reference

| Question | Determines |
|----------|------------|
| Image | Image-to-video vs text-to-video |
| Audio | With/without audio generation |
| Model | Quality and speed tradeoff |
| Duration | Clip length |
| Format | Aspect ratio and resolution |

---

### Step 2: Craft the Prompt

Transform the user request into an effective video prompt:

1. **Describe the scene**: Set the visual context
2. **Specify action**: What moves, changes, happens
3. **Include camera work**: "slow pan", "tracking shot", "dolly shot"
4. **Add audio cues** (Veo 3+): Use quotes for dialogue, describe sounds
5. **Set the mood**: Lighting, atmosphere, time of day

**Example with dialogue (Veo 3.1):**
- User: "a person discovering treasure"
- Enhanced: "Close-up of a treasure hunter's face as torchlight flickers. He murmurs 'This must be it...' while brushing dust off an ancient chest. Sound of creaking hinges as he opens it, revealing golden light on his awestruck face. Cinematic, dramatic shadows."

**Example without dialogue:**
- User: "a dog running on a beach"
- Enhanced: "Cinematic slow-motion shot of a golden retriever running joyfully along a beach at sunset, waves lapping, warm golden hour lighting, shallow depth of field"

### Step 3: Select the Model

**Default: veo-3.1** (highest quality, with audio)

| Use Case | Recommended Model | Reason |
|----------|------------------|--------|
| Best quality | veo-3.1 (default) | Highest quality, audio |
| Quick iteration | veo-3.1-fast | Faster processing |
| Batch generation | veo-3.1-fast | Speed matters for multiple clips |
| Longer videos (>8s) | sora | Supports up to 20s |

### Step 4: Generate the Video

Execute the appropriate script from `${CLAUDE_PLUGIN_ROOT}/skills/video-generation/scripts/`:

**For Google Veo 3.1 (default, with audio):**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-generation/scripts/veo.py \
  --prompt "your enhanced prompt with 'dialogue in quotes'" \
  --model "veo-3.1" \
  --duration 8 \
  --aspect-ratio "16:9" \
  --resolution "720p"
```

**For Google Veo 3.1 with image input:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-generation/scripts/veo.py \
  --prompt "The cat slowly opens its eyes and yawns" \
  --image "/path/to/cat.jpg" \
  --model "veo-3.1" \
  --duration 8
```

**For faster generation:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-generation/scripts/veo.py \
  --prompt "your prompt" \
  --model "veo-3.1-fast"
```

**For OpenAI Sora (longer videos):**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-generation/scripts/sora.py \
  --prompt "your enhanced prompt" \
  --duration 20 \
  --resolution "1080p"
```

**List available models:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-generation/scripts/veo.py --list-models
```

## Video Extension (For Long-Form Continuity)

**The `--extend` flag creates TRUE visual continuity** by continuing from where a previous Veo video ended. This is the best approach for long-form videos.

**Basic extension:**
```bash
# First, generate initial clip
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-generation/scripts/veo.py \
  --prompt "A person walks through a forest at sunrise" \
  --duration 8

# Extend it with new content (adds ~7 seconds)
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-generation/scripts/veo.py \
  --extend veo_veo-3.1_20260104_120000.mp4 \
  --prompt "Continue walking, discover a hidden stream"
```

**Multiple extensions (for longer videos):**
```bash
# Extend 5 times (adds ~35 seconds of continuation)
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-generation/scripts/veo.py \
  --extend initial_clip.mp4 \
  --prompt "Keep exploring the forest, encounter wildlife" \
  --extend-times 5
```

**Extension vs Stitching:**

| Approach | Result | Use Case |
|----------|--------|----------|
| **Extension** | True continuity, same characters/scene | Long continuous shots |
| **Stitching** | Separate clips with transitions | Scene changes, montages |

**Extension Limits:**
- Input video must be Veo-generated (max 141 seconds)
- Each extension adds ~7 seconds
- Maximum 20 extensions total (~2.5 minutes)
- Output resolution is 720p

## Batch Generation (Parallel)

**Generate multiple videos simultaneously** for faster multi-scene workflows. Instead of waiting 15+ minutes for 5 sequential videos, generate them all in parallel (~3 minutes total).

### Create a scenes.json file:

```json
[
  {"prompt": "Scene 1: Cinematic hero shot of wireless earbuds on dark surface", "duration": 6, "output": "scene1_hero.mp4"},
  {"prompt": "Scene 2: Sound waves visualization, person enjoying music", "duration": 8, "output": "scene2_sound.mp4"},
  {"prompt": "Scene 3: Close-up of earbud in ear, person exercising", "duration": 8, "output": "scene3_comfort.mp4"},
  {"prompt": "Scene 4: Lifestyle montage, various settings", "duration": 8, "output": "scene4_lifestyle.mp4"},
  {"prompt": "Scene 5: Product with logo on clean background", "duration": 4, "output": "scene5_cta.mp4"}
]
```

### Generate all scenes in parallel:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-generation/scripts/veo.py \
  --batch scenes.json
```

### With custom worker count:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-generation/scripts/veo.py \
  --batch scenes.json \
  --max-workers 3
```

### Batch config options per video:

| Option | Description | Default |
|--------|-------------|---------|
| `prompt` | Video description (required) | - |
| `model` | veo-3.1, veo-3.1-fast, etc. | veo-3.1 |
| `duration` | 4, 6, or 8 seconds | 8 |
| `aspect_ratio` | "16:9" or "9:16" | "16:9" |
| `resolution` | "720p" or "1080p" | "720p" |
| `image` | Path to image for image-to-video | - |
| `negative_prompt` | What to avoid | - |
| `output` | Custom output filename | auto-generated |

### Speed comparison:

| Scenes | Sequential | Parallel (5 workers) | Speedup |
|--------|------------|---------------------|---------|
| 3 | ~9 min | ~3 min | 3x |
| 5 | ~15 min | ~3 min | 5x |
| 10 | ~30 min | ~6 min | 5x |

### Step 5: Deliver the Result

1. Provide the generated video file/URL
2. Share the enhanced prompt used
3. Mention generation settings (duration, resolution)
4. Offer to:
   - Generate variations
   - Try different style/duration
   - Use a different API
   - Extend the video

## Error Handling

**Missing API key**: Inform the user which key is needed:
- OpenAI: https://platform.openai.com/api-keys
- Google: https://aistudio.google.com/apikey

**Content policy violation**: Rephrase the prompt appropriately.

**Generation failed**: Retry with simplified prompt or different API.

**Quota exceeded**: Suggest waiting or trying the other provider.

## Prompt Engineering Tips

### For Audio (Veo 3.1)
- **Dialogue**: Use quotes for speech: `"Hello!" she said excitedly`
- **Sound effects**: Describe explicitly: `tires screeching, engine roaring`
- **Ambient**: Describe the soundscape: `birds chirping, distant traffic`
- **Example**: `A man whispers "Did you hear that?" as footsteps echo in the dark hallway`

### For Cinematic Quality
- Include camera directions: "slow dolly", "tracking shot", "crane shot"
- Specify lighting: "golden hour", "dramatic shadows", "soft diffused light"
- Add film references: "Blade Runner style", "Wes Anderson aesthetic"

### For Realistic Motion
- Describe physics: "natural movement", "realistic physics"
- Include environmental details: "wind in hair", "leaves rustling"
- Specify speed: "slow motion", "real-time", "time-lapse"

### For Image-to-Video
- Describe what should change/move from the starting image
- Be specific about the action: "the cat slowly opens its eyes"
- Include environmental motion: "leaves blow past"

### Negative Prompts
- Describe what NOT to include: `--negative-prompt "cartoon, low quality, blurry"`
- Don't use "no" or "don't" - just describe the unwanted elements

## API Comparison

| Feature | Veo 3.1 (Default) | Veo 3.1 Fast | Sora |
|---------|-------------------|--------------|------|
| Provider | Google | Google | OpenAI |
| API Key | `GOOGLE_API_KEY` | `GOOGLE_API_KEY` | `OPENAI_API_KEY` |
| Max duration | 8 seconds | 8 seconds | 20 seconds |
| Resolution | 720p, 1080p | 720p, 1080p | Up to 1080p |
| Aspect ratios | 16:9, 9:16 | 16:9, 9:16 | 16:9, 9:16, 1:1 |
| Audio (dialogue, SFX) | ✅ Yes | ✅ Yes | ❌ No |
| Image-to-video | ✅ Yes | ✅ Yes | ✅ Yes |
| Reference images | ✅ Up to 3 | ✅ Up to 3 | ❌ No |
| Video extension | ✅ Yes | ✅ Yes | ❌ No |
| Batch generation | ✅ Yes | ✅ Yes | ❌ No |
| Speed | Best quality | ~2x faster | Slower |
| Best for | Professional | Batch workflows | Longer videos |
