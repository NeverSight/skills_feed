---
name: video-producer-agent
description: >
  Use this skill to create complete videos with voiceover and music.
  Triggers: "create video", "product video", "explainer video", "promo video", "demo video",
  "training video", "ad video", "commercial", "marketing video", "video with voiceover",
  "video with music", "brand video", "testimonial video"
  Orchestrates: script, voiceover, background music, video clips/images, and final assembly.
---

# Video Producer

Create complete videos with voiceover, music, and visuals.

**This is an orchestrator skill** that combines:
- Script/storyboard generation (Claude)
- Voiceover synthesis (Gemini TTS)
- Background music (Lyria)
- Video clip generation (Veo 3.1) or image animation
- Final assembly (FFmpeg via media-utils)

## Workflow

### Step 1: Gather Requirements (REQUIRED)

⚠️ **DO NOT skip this step. DO NOT run init_project.py until you have ALL answers.**

**Use interactive questioning** — ask ONE question at a time, wait for the response, then ask the next. This creates a collaborative spec-driven process.

#### Question Flow

⚠️ **Use the `AskUserQuestion` tool for each question below.** Do not just print questions in your response — use the tool to create interactive prompts with the options shown.

**Q1: Subject**
> "I'll create that video! First — **what's it about?**
> 
> *(e.g., product launch, brand story, tutorial, explainer — or describe your own)*"

*Wait for response.*

**Q2: Duration**
> "How long should the video be?
> 
> - 15 seconds *(quick hook)*
> - 30 seconds *(standard ad)*
> - 60 seconds *(explainer)*
> - 2+ minutes *(detailed)*
> - Or specify your own duration"

*Wait for response.*

**Q3: Style**
> "What visual style?
> 
> - Premium/luxury
> - Fun/playful
> - Corporate/professional
> - Dramatic/cinematic
> - Minimal/clean
> - Or describe your own style"

*Wait for response.*

**Q4: Assets**
> "Do you have existing images or video clips to use?
> 
> - No, generate everything
> - Yes, I have images *(provide paths)*
> - Yes, I have video clips *(provide paths)*"

*Wait for response.*

**Q5: Audio Strategy**
> "How should we handle audio?
> 
> - **Custom** — I generate voiceover + background music
> - **Veo native** — Use Veo's built-in dialogue/SFX/ambient
> - **Silent** — No audio, add later"

*Wait for response.*

**Q6: Voice** *(if custom audio)*
> "What voice tone for the voiceover?
> 
> - Professional
> - Friendly/warm
> - Energetic
> - Calm/soothing
> - Dramatic
> - Or describe your own tone"

*Wait for response.*

**Q7: Music** *(if custom audio)*
> "What music vibe?
> 
> - Modern electronic
> - Cinematic/epic
> - Upbeat pop
> - Ambient/chill
> - Corporate
> - Or describe your own style"

*Wait for response.*

**Q8: Format**
> "What **aspect ratio**?
> 
> - 16:9 (YouTube, web)
> - 9:16 (TikTok, Reels, Shorts)
> - 1:1 (Instagram feed)"

*Wait for response.*

**Q9: Resolution**
> "What **resolution**?
> 
> - 720p (faster generation)
> - 1080p (standard HD)"

*Wait for response.*

**Q10: Model**
> "Which **Veo model**?
> 
> - `veo-3.1` — Latest, highest quality (default)
> - `veo-3.1-fast` — Faster generation, slightly lower quality
> - `veo-3` — Previous generation
> - `veo-3-fast` — Previous gen, faster"

*Wait for response.*

#### Quick Reference

| Question | Determines |
|----------|------------|
| Subject | Scene content and prompts |
| Duration | Scene count (Veo clips must be 4, 6, or 8 seconds) |
| Style | Visual prompts and music selection |
| Assets | Generate vs use existing |
| Audio | custom, veo_audio, or silent |
| Voice | TTS voice selection |
| Music | Lyria prompt |
| Format | Aspect ratio for Veo |
| Resolution | 720p or 1080p output quality |
| Model | veo-3.1, veo-3.1-fast, veo-3, veo-3-fast |

---

### Step 2: Initialize Project

Once you have the user's answers, initialize the project with their preferences:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-producer-agent/scripts/init_project.py \
  --name "Product Launch Video" \
  --duration 30 \
  --aspect-ratio 16:9 \
  --audio-strategy custom \
  --scenes 5
```

### Step 3: Configure project.json

Edit `project.json` with scene prompts, voiceover text, and music style based on user's answers.

### Step 4: Assemble the Video

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-producer-agent/scripts/assemble.py \
  --project ~/my_video_project/
```

---

## Project Structure

When you initialize a project, this folder structure is created:

```
my_project/
├── project.json          # Configuration: scenes, voiceover, music, settings
├── storyboard.md         # Planning document for the video
├── scenes/               # Generated video clips from Veo
│   ├── scene1_intro.mp4
│   ├── scene2_features.mp4
│   └── scene3_cta.mp4
├── audio/                # Audio assets
│   ├── voiceover.wav     # Generated voiceover
│   ├── background_music.wav  # Generated music
│   └── final_mix.mp3     # Mixed audio track
├── work/                 # Intermediate files (auto-generated)
│   ├── silent_scene1.mp4
│   ├── video_concatenated.mp4
│   └── ...
└── output/               # Final deliverables
    └── product_launch_video_final.mp4
```

---

## Scripts

### init_project.py

Initialize a new video project with folder structure and templates.

```bash
# Basic project
python3 init_project.py --name "My Video" --duration 30

# Create in specific directory
python3 init_project.py --name "Demo Video" --output ~/Videos/

# Vertical video for social
python3 init_project.py --name "Instagram Reel" --aspect-ratio 9:16 --duration 15

# Use Veo's native audio (no custom voiceover/music)
python3 init_project.py --name "Cinematic Scene" --audio-strategy veo_audio

# More scenes
python3 init_project.py --name "Long Video" --duration 60 --scenes 5
```

**Options:**
| Option | Default | Description |
|--------|---------|-------------|
| `--name` | required | Project name |
| `--output` | current dir | Parent directory |
| `--duration` | 30 | Target duration in seconds |
| `--aspect-ratio` | 16:9 | 16:9, 9:16, 1:1, 4:3 |
| `--audio-strategy` | custom | custom, veo_audio, silent |
| `--scenes` | 3 | Number of scene placeholders |

### assemble.py

Orchestrate the full video assembly pipeline.

```bash
# Full pipeline (generate everything + assemble)
python3 assemble.py --project ~/my_project/

# Skip generation (use existing scene/audio files)
python3 assemble.py --project ~/my_project/ --skip-generation

# Dry run (show what would be done)
python3 assemble.py --project ~/my_project/ --dry-run
```

**Pipeline steps:**
1. Generate video scenes (Veo 3.1)
2. Strip audio from scenes (if custom audio)
3. Generate voiceover (Gemini TTS)
4. Generate background music (Lyria)
5. Mix voiceover + music
6. Concatenate video clips
7. Merge audio with video
8. Output final video

---

## project.json Configuration

```json
{
  "name": "Product Launch Video",
  "duration_target": 30,
  "aspect_ratio": "16:9",
  "resolution": "720p",
  "audio_strategy": "custom",
  
  "scenes": [
    {
      "id": 1,
      "name": "scene1_hero",
      "prompt": "Cinematic slow zoom on premium product, dramatic lighting, high-end commercial style",
      "duration": 6,
      "notes": "Music only, no voiceover"
    },
    {
      "id": 2,
      "name": "scene2_features",
      "prompt": "Product features demonstration, sleek animations, modern tech aesthetic",
      "duration": 8,
      "notes": "Voiceover starts here"
    },
    {
      "id": 3,
      "name": "scene3_cta",
      "prompt": "Product with logo on clean background, call to action moment",
      "duration": 6,
      "notes": "Music swells, voiceover ends"
    }
  ],
  
  "voiceover": {
    "enabled": true,
    "text": "Introducing the future of audio. Crystal clear sound. All-day comfort. Experience the difference.",
    "voice": "Charon",
    "style": "Professional, confident, premium brand voice"
  },
  
  "music": {
    "enabled": true,
    "prompt": "modern electronic, premium, sleek, product showcase, subtle bass",
    "duration": 35,
    "bpm": 100,
    "brightness": 0.6
  },
  
  "assembly": {
    "transition": "fade",
    "transition_duration": 0.5,
    "music_volume": 0.3,
    "fade_in": 1.0,
    "fade_out": 2.0
  }
}
```

---

## Audio Strategies

| Strategy | Description | Use When |
|----------|-------------|----------|
| `custom` | Strip Veo audio, add custom voiceover + music | Most videos |
| `veo_audio` | Keep Veo's generated audio (dialogue, SFX) | Cinematic scenes, dialogues |
| `silent` | Strip audio, output silent video | Adding audio later |

---

## Workflow: Creating a Video

### Step 1: Initialize Project

```bash
python3 init_project.py --name "Wireless Earbuds Promo" --duration 30
```

### Step 2: Plan the Storyboard

Edit `storyboard.md` to plan your video structure:

```markdown
## Scene 1: Hero Reveal (0-5s)
- Visual: Earbuds emerging from shadow, premium lighting
- Audio: Music only (dramatic intro)

## Scene 2: Sound Quality (5-12s)
- Visual: Sound waves, person enjoying music
- Audio: Voiceover: "Crystal clear sound. Immersive bass."

## Scene 3: Comfort (12-20s)
- Visual: Close-up of fit, person running
- Audio: Voiceover: "All-day comfort. Secure fit."

## Scene 4: CTA (20-30s)
- Visual: Product + logo
- Audio: Voiceover: "Experience the difference." + music swell
```

### Step 3: Configure project.json

Fill in the scene prompts, voiceover text, and music style based on your storyboard.

### Step 4: Assemble

```bash
python3 assemble.py --project ~/wireless_earbuds_promo/
```

### Step 5: Review and Iterate

Check the output in `output/`. If adjustments needed:

```bash
# Re-run with existing scenes (just re-mix audio)
python3 assemble.py --project ~/wireless_earbuds_promo/ --skip-generation
```

---

## What You Can Create

| Type | Example |
|------|---------|
| Product video | 30s hero video showcasing a product |
| Explainer video | How-to or feature explanation |
| Promo/ad video | Marketing advertisement |
| Demo video | Product demonstration |
| Training video | Internal training content |
| Testimonial | Customer quote style video |
| Brand video | Company/brand story |

---

## Prerequisites

- `GOOGLE_API_KEY` - For Veo (video), Gemini TTS (voice), Lyria (music)
- FFmpeg installed: `brew install ffmpeg`

---

## Video Styles & Music Pairings

| Style | Music Prompt | Voice |
|-------|--------------|-------|
| Premium/Luxury | "elegant, minimal, ambient, sophisticated" | Charon (informative) |
| Tech/Modern | "electronic, futuristic, clean, innovative" | Kore (firm) |
| Fun/Playful | "upbeat, cheerful, acoustic, positive" | Puck (upbeat) |
| Corporate | "professional, inspiring, orchestral lite" | Orus (firm) |
| Lifestyle | "chill, aspirational, indie, warm" | Aoede (breezy) |
| Dramatic/Cinematic | "epic, orchestral, emotional, building" | Gacrux (mature) |

---

## Common Video Structures

### Product Video (30s)
```
0-5s:   Hero shot (music only)
5-15s:  Features (voiceover + music)
15-25s: Lifestyle/use case (voiceover + music)
25-30s: Logo + CTA (music fade)
```

### Explainer Video (60s)
```
0-5s:   Hook/problem statement
5-20s:  Solution introduction
20-45s: How it works (3 steps)
45-55s: Benefits summary
55-60s: CTA
```

### Testimonial Video (45s)
```
0-5s:   Intro/name card
5-35s:  Testimonial quote (multiple scenes)
35-45s: Product shot + logo
```

---

## Manual Workflow (Without Scripts)

If you prefer to run each step manually:

**Generate scenes:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-generation/scripts/veo.py \
  --batch scenes.json
```

**Generate voiceover:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/voice-generation/scripts/gemini_tts.py \
  --text "Your voiceover text..." \
  --voice Charon \
  --style "Professional, warm"
```

**Generate music:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/music-generation/scripts/lyria.py \
  --prompt "modern electronic, premium" \
  --duration 35
```

**Strip audio from clips:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/media-utils/scripts/video_strip_audio.py \
  -i scene*.mp4
```

**Concatenate videos:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/media-utils/scripts/video_concat.py \
  -i silent_*.mp4 --transition fade -o video.mp4
```

**Mix audio:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/media-utils/scripts/audio_mix.py \
  --voice voiceover.wav --music music.wav -o audio.mp3
```

**Merge audio + video:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/media-utils/scripts/video_audio_merge.py \
  --video video.mp4 --audio audio.mp3 -o final.mp4
```

---

## Input Files You Can Provide

| File Type | How It's Used |
|-----------|---------------|
| Product images | Animate with Veo as first frame |
| Logo (PNG) | Overlay on final scene |
| Existing voiceover | Place in `audio/voiceover.wav` |
| Brand music | Place in `audio/background_music.wav` |
| Video clips | Place in `scenes/` folder |
| Script/copy | Use for voiceover text |

---

## Limitations

- **Veo video duration**: Max 8 seconds per clip (concatenate for longer)
- **Veo 3.1 includes audio**: All clips have generated audio (strip if using custom)
- **Processing time**: Video generation takes 1-3 minutes per clip
- **Resolution**: Currently 720p or 1080p (1080p for 8s only)

---

## Error Handling

| Error | Solution |
|-------|----------|
| "GOOGLE_API_KEY not set" | Set up API key per README |
| "FFmpeg not found" | Install: `brew install ffmpeg` |
| "project.json not found" | Run init_project.py first |
| Video generation timeout | Retry, or use shorter duration |
| Audio/video sync issues | Adjust scene durations |

---

## Example Prompts

**Simple:**
> "Create a 30-second product video for my new coffee maker"

**Detailed:**
> "Create a 45-second product video for our new wireless earbuds. Premium, luxury feel. I have product photos attached. Professional male voiceover. Modern electronic music. 16:9 for YouTube."

**With project:**
> "Initialize a video project called 'App Demo' with 5 scenes, 60 seconds total, vertical format for TikTok"
