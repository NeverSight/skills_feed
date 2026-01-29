---
name: music-generation
description: >
  Use this skill for AI music generation. Triggers include:
  "generate music", "create a song", "make music", "compose", "create a beat", 
  "generate audio", "make a soundtrack", "create a jingle", "instrumental music",
  "background music", "lo-fi beats", "electronic music"
  Supports vocals (Suno/Udio) and instrumental-only (Google Lyria).
---

# Music Generation Skill

Generate music, songs, and audio using AI (Suno, Udio, Google Lyria).

## Prerequisites

At least one API key is required:

- `GOOGLE_API_KEY` - For Google Lyria (same key as video/image) ✅
- `SUNO_API_KEY` - For Suno music generation
- `UDIO_API_KEY` - For Udio music generation

## Available APIs

### Google Lyria (Instrumental Only)
- **Best for**: Background music, beats, soundtracks, game audio
- **Duration**: Any length (streams in real-time)
- **Features**: BPM control, key/scale, brightness, density
- **Output**: 48kHz stereo WAV
- **API Key**: Same `GOOGLE_API_KEY` as video/image generation ✅
- **⚠️ INSTRUMENTAL ONLY** - Cannot generate vocals

### Suno (Recommended for Songs with Vocals)
- **Best for**: Full songs with vocals, catchy melodies, various genres
- **Duration**: Up to 4 minutes
- **Features**: Lyrics generation, instrumental mode, style tags
- **Genres**: Pop, rock, jazz, electronic, classical, hip-hop, and more

### Udio
- **Best for**: High-fidelity audio, experimental styles, remixes
- **Duration**: Up to 2 minutes per generation
- **Features**: Style control, audio quality options
- **Genres**: Wide variety with strong electronic/experimental support

## Workflow

### Step 1: Ask Key Question - Vocals or Instrumental?

**This determines which API to use:**

| Need | API | Why |
|------|-----|-----|
| **Vocals/Lyrics** | Suno or Udio | Lyria cannot generate vocals |
| **Instrumental only** | Lyria (preferred) | Same API key as video/image, real-time control |
| **Background music** | Lyria | Best for soundtracks, game audio |
| **Full songs** | Suno | Best vocal quality |

**Example prompt to user:**

"I'll generate that music! Quick question:

1. **Do you need vocals/lyrics?**
   - Yes → I'll use Suno (best for songs)
   - No, instrumental only → I'll use Lyria (same key as video/image)

2. **What genre/mood?** (e.g., chill lo-fi, epic orchestral, upbeat pop)

3. **How long?** (Lyria: any length, Suno: up to 4 min)

4. **Any BPM preference?** (e.g., 90 for chill, 128 for dance)"

---

### Step 2: Understand the Request

Parse the user's music request for:
- **Genre/style**: Pop, rock, jazz, electronic, classical, etc.
- **Mood**: Happy, sad, energetic, calm, dramatic
- **Tempo**: Fast, slow, medium, specific BPM
- **Vocals**: With vocals → Suno/Udio, Instrumental → Lyria
- **Purpose**: Background music, song, jingle, soundtrack
- **Duration**: How long should it be?

### Step 2: Craft the Prompt

Transform the user request into an effective music generation prompt:

1. **Specify genre**: Be specific about the style
2. **Describe mood**: Emotional tone and energy level
3. **Include instruments**: What should be prominent
4. **Add production style**: Lo-fi, polished, vintage, modern
5. **Set tempo**: BPM or descriptive (upbeat, slow)

**Example transformation:**
- User: "happy summer song"
- Enhanced: "Upbeat indie pop song with bright acoustic guitar, cheerful ukulele, and sunny vibes. Feel-good summer anthem with catchy hooks and positive energy. Male vocals, 120 BPM, radio-friendly production"

### Step 3: Handle Lyrics (If Needed)

For songs with vocals:
- **User provides lyrics**: Use them directly
- **Generate lyrics**: Ask Suno/Udio to generate, or use Claude to write them first
- **Instrumental**: Specify "instrumental" to skip vocals

Lyrics format for Suno:
```
[Verse 1]
Your lyrics here

[Chorus]
Catchy chorus lyrics

[Verse 2]
More lyrics
```

### Step 4: Select the API

Choose based on requirements:

| Use Case | Recommended API | Reason |
|----------|----------------|--------|
| **Instrumental/background** | Lyria | Same API key, any duration, real-time control |
| **Full songs with vocals** | Suno | Best vocal quality |
| **Lo-fi beats** | Lyria | Great for ambient/chill |
| **Experimental/electronic** | Udio | Strong in these genres |
| **Specific lyrics needed** | Suno | Lyrics input support |
| **Game/video soundtrack** | Lyria | Precise BPM/key control |

### Step 5: Generate the Music

Execute the appropriate script from `${CLAUDE_PLUGIN_ROOT}/skills/music-generation/scripts/`:

**For Google Lyria (Instrumental):**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/music-generation/scripts/lyria.py \
  --prompt "chill lo-fi hip hop, jazzy piano, vinyl crackle" \
  --duration 60 \
  --bpm 85
```

**Lyria with key/scale:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/music-generation/scripts/lyria.py \
  --prompt "ambient, ethereal synths, dreamy" \
  --duration 120 \
  --scale "C" \
  --brightness 0.7
```

**Lyria with multiple prompts (blended):**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/music-generation/scripts/lyria.py \
  --prompt "minimal techno" \
  --prompt "deep bass, 808" \
  --bpm 128 \
  --duration 90
```

**For Suno (with vocals):**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/music-generation/scripts/suno.py \
  --prompt "upbeat indie pop, summer vibes, acoustic guitar" \
  --title "Summer Days"
```

**For Udio:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/music-generation/scripts/udio.py \
  --prompt "cinematic orchestral, epic trailer music" \
  --duration 120
```

### Step 6: Deliver the Result

1. Provide the generated audio file path
2. Share the prompt and settings used
3. Mention the duration and format
4. Offer to:
   - Generate variations
   - Try different style/genre
   - Adjust tempo or mood
   - Extend the track
   - Add or remove vocals

## Error Handling

**Missing API key**: Inform the user which key is needed:
- Lyria: Same `GOOGLE_API_KEY` as video/image - https://aistudio.google.com/apikey
- Suno: https://suno.com/api (or app.suno.ai)
- Udio: https://udio.com/api

**Lyria requires google-genai package**: `pip install google-genai`

**User wants vocals but only has GOOGLE_API_KEY**: Explain Lyria is instrumental-only, suggest Suno/Udio.

**Content policy violation**: Rephrase lyrics or prompt.

**Generation failed**: Retry with simplified prompt.

**Quota exceeded**: Suggest waiting or trying other provider.

## Prompt Engineering Tips

### Genre Tags (Suno Style)
Include specific genre tags for best results:
- `[pop, upbeat, female vocals, 128 BPM]`
- `[jazz, smooth, saxophone, laid-back]`
- `[electronic, synthwave, 80s, driving]`
- `[classical, orchestral, emotional, strings]`

### Mood Descriptors
- **Energetic**: upbeat, driving, powerful, intense
- **Calm**: relaxing, ambient, peaceful, gentle
- **Happy**: cheerful, bright, sunny, joyful
- **Sad**: melancholic, emotional, heartfelt, somber
- **Epic**: cinematic, dramatic, sweeping, grand

### Production Style
- **Lo-fi**: warm, vintage, tape hiss, nostalgic
- **Polished**: crisp, modern, radio-ready, professional
- **Raw**: garage, live, organic, unpolished
- **Electronic**: synthesizers, digital, processed

## API Comparison

| Feature | Lyria | Suno | Udio |
|---------|-------|------|------|
| API Key | `GOOGLE_API_KEY` ✅ | `SUNO_API_KEY` | `UDIO_API_KEY` |
| Max duration | **Unlimited** | 4 minutes | 2 minutes |
| Vocals | ❌ **No** | ✅ Excellent | ✅ Good |
| Instrumentals | ✅ Excellent | ✅ Great | ✅ Excellent |
| BPM control | ✅ 60-200 | ❌ No | ❌ No |
| Key/Scale control | ✅ Yes | ❌ No | ❌ No |
| Audio quality | 48kHz WAV | Very good | Excellent |
| Lyrics input | ❌ No | ✅ Yes | ✅ Yes |
| Real-time steering | ✅ Yes | ❌ No | ❌ No |
| Best for | Beats, soundtracks | Songs | Experimental |

## Example Prompts

### Pop Song
```
Catchy pop song with female vocals, bright synths, and an anthemic chorus. 
Feel-good energy, summer vibes, 120 BPM, radio-friendly production.
```

### Cinematic Score
```
Epic orchestral trailer music with building tension. Powerful brass, 
sweeping strings, thundering percussion. Dramatic and emotional.
```

### Lo-fi Beat
```
Chill lo-fi hip hop beat, jazzy piano samples, vinyl crackle, 
relaxed drums, perfect for studying. 85 BPM, nostalgic mood.
```

### Electronic Dance
```
High-energy EDM track with massive drops, pulsing synths, 
four-on-the-floor beat. Festival-ready, 128 BPM.
```

## Lyria-Specific Examples

### Lo-fi Study Beats
```bash
python3 lyria.py -p "lo-fi hip hop, jazzy piano, vinyl crackle, chill" \
  --duration 300 --bpm 85 --brightness 0.3
```

### Techno/Dance
```bash
python3 lyria.py -p "minimal techno, deep bass, 808 drums" \
  --duration 120 --bpm 128 --density 0.7
```

### Ambient/Meditation
```bash
python3 lyria.py -p "ambient, ethereal, soft pads, dreamy" \
  --duration 180 --brightness 0.8 --density 0.2
```

### Game Soundtrack
```bash
python3 lyria.py -p "epic orchestral, cinematic, dramatic strings" \
  --duration 90 --scale "D" --mode quality
```

### Lyria Prompt Tips
- **Instruments**: piano, guitar, synth, drums, bass, strings, 808, Rhodes, Moog
- **Genres**: lo-fi hip hop, minimal techno, ambient, jazz fusion, synthwave, chillout
- **Moods**: chill, energetic, dreamy, dark, upbeat, melancholic, epic
- **Combine prompts**: Use multiple `-p` flags to blend styles
