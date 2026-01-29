---
name: audio-producer-agent
description: >
  Use this skill to create single-voice audio content like audiobooks, voiceovers, narrations, jingles, and audio ads.
  Triggers: "create audiobook", "generate voiceover", "narration", "audio ad", "radio ad",
  "jingle", "brand audio", "sonic logo", "text to audio", "read this aloud", "audio guide",
  "meditation audio", "soundscape"
  Orchestrates: narration/TTS, background music, and audio assembly.
  NOTE: For conversations/dialogues, use podcast-producer instead.
---

# Audio Producer

Create single-speaker audio content: audiobooks, voiceovers, narrations, jingles, and more.

**This is an orchestrator skill** that combines:
- Text-to-speech / narration (Gemini TTS, ElevenLabs, or OpenAI TTS)
- Background music / ambient audio (Lyria)
- Audio assembly (FFmpeg via media-utils)

**For dialogues and conversations**, use `podcast-producer` instead.

## What You Can Create

| Type | Example |
|------|---------|
| Audiobook | Long-form narration of text/chapters |
| Voiceover | Narration for video, presentation, or slideshow |
| Audio ad | Radio or podcast advertisement |
| Jingle | Short brand music with optional tagline |
| Sonic logo | Audio brand identifier (few seconds) |
| Audio guide | Museum/tour style narration |
| Meditation | Guided relaxation with ambient audio |
| Soundscape | Ambient audio environment |

## Prerequisites

- `GOOGLE_API_KEY` - For Gemini TTS (voice) and Lyria (music)
- FFmpeg installed: `brew install ffmpeg`

## Workflow

### Step 1: Gather Requirements (REQUIRED)

⚠️ **DO NOT skip this step. Use interactive questioning — ask ONE question at a time.**

#### Question Flow

⚠️ **Use the `AskUserQuestion` tool for each question below.** Do not just print questions in your response — use the tool to create interactive prompts with the options shown.

**Q1: Type**
> "I'll create that audio for you! First — **what type of audio?**
> 
> - Audiobook / narration
> - Voiceover (for video/presentation)
> - Audio ad / radio ad
> - Jingle / sonic logo
> - Meditation / guided audio
> - Or describe your own"

*Wait for response.*

**Q2: Content**
> "What's the **text/content** to speak?
> 
> - Paste the text here
> - Or describe what you need and I'll write it"

*Wait for response.*

**Q3: Voice**
> "What **voice style**?
> 
> - Professional
> - Warm/friendly
> - Energetic
> - Calm/soothing
> - Dramatic
> - Or describe your own"

*Wait for response.*

**Q4: Music**
> "Do you want **background music**?
> 
> - Yes — describe the style (ambient, upbeat, cinematic, etc.)
> - No — voice only"

*Wait for response.*

**Q5: Duration**
> "What's the **target duration**?
> 
> - Let it be natural length
> - Or specify (e.g., 30 seconds, 2 minutes)"

*Wait for response.*

#### Quick Reference

| Question | Determines |
|----------|------------|
| Type | Processing approach and output format |
| Content | TTS input text |
| Voice | Voice selection and style parameters |
| Music | Whether to generate and mix music |
| Duration | Pacing and content length |

---

### Step 2: Prepare the Content

**For narration/voiceover:**
- Optimize text for speech (spell out numbers if needed)
- Add natural pause points (commas, periods)
- Break long content into chunks if > 32k tokens

**For jingles/audio ads:**
- Write the tagline/copy
- Determine music style
- Plan structure: music intro → voice → music outro

**For audiobooks:**
- Split into chapters
- Consider different voice styles for different sections
- Plan ambient music (subtle, low volume)

---

### Step 3: Generate Assets

#### Type: Voiceover / Narration

**Generate narration (Gemini TTS):**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/voice-generation/scripts/gemini_tts.py \
  --text "Your narration text here..." \
  --voice Charon \
  --style "Professional, measured pace, warm and authoritative"
```

**Generate background music if needed (Lyria):**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/music-generation/scripts/lyria.py \
  --prompt "subtle ambient, corporate, unobtrusive, background" \
  --duration 120 \
  --density 0.2 \
  --brightness 0.4
```

**Mix voice with music:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/media-utils/scripts/audio_mix.py \
  --voice narration.wav \
  --music background.wav \
  --music-volume 0.15 \
  --fade-in 2 \
  --fade-out 3 \
  -o final_voiceover.mp3
```

---

#### Type: Audio Ad / Radio Spot

**Structure: 30-second radio ad**
```
0-3s:   Music hook (attention grabber)
3-25s:  Voice with music bed underneath
25-30s: Music + tagline + CTA
```

**Generate energetic music:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/music-generation/scripts/lyria.py \
  --prompt "upbeat, energetic, advertising, catchy, radio jingle" \
  --duration 35 \
  --bpm 120
```

**Generate voice with style:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/voice-generation/scripts/gemini_tts.py \
  --text "Tired of ordinary coffee? Wake up to extraordinary! Premium beans, perfect roast, delivered fresh. Visit BestCoffee.com today and get 20% off your first order!" \
  --voice Puck \
  --style "Energetic, radio announcer style, enthusiastic, clear call to action"
```

**Mix and assemble:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/media-utils/scripts/audio_mix.py \
  --voice ad_voice.wav \
  --music ad_music.wav \
  --music-volume 0.35 \
  --fade-in 1 \
  --fade-out 2 \
  -o radio_ad.mp3
```

---

#### Type: Jingle / Sonic Logo

**For jingle with tagline:**

**Generate catchy music:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/music-generation/scripts/lyria.py \
  --prompt "catchy jingle, memorable, brand audio, upbeat, major key" \
  --duration 10 \
  --bpm 110 \
  --scale C
```

**Generate tagline:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/voice-generation/scripts/gemini_tts.py \
  --text "TechCorp. Innovation for tomorrow." \
  --voice Kore \
  --style "Confident, aspirational, slight pause between company name and tagline"
```

**Mix tagline over music:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/media-utils/scripts/audio_mix.py \
  --voice tagline.wav \
  --music jingle.wav \
  --music-volume 0.5 \
  -o brand_jingle.mp3
```

**For sonic logo (music only):**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/music-generation/scripts/lyria.py \
  --prompt "sonic logo, 3 seconds, memorable, brand identifier, simple, distinctive" \
  --duration 5 \
  --bpm 100
```

---

#### Type: Audiobook

**Process chapters:**

```bash
# Chapter 1
python3 ${CLAUDE_PLUGIN_ROOT}/skills/voice-generation/scripts/gemini_tts.py \
  --text-file chapter1.txt \
  --voice Algieba \
  --style "Audiobook narrator, measured pace, engaging storytelling" \
  -o chapter1.wav

# Chapter 2
python3 ${CLAUDE_PLUGIN_ROOT}/skills/voice-generation/scripts/gemini_tts.py \
  --text-file chapter2.txt \
  --voice Algieba \
  -o chapter2.wav
```

**Optional: Add subtle ambient music:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/music-generation/scripts/lyria.py \
  --prompt "ambient, subtle, reading music, calm, unobtrusive, soft piano" \
  --duration 600 \
  --density 0.1 \
  --brightness 0.3
```

**Concatenate chapters:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/media-utils/scripts/audio_concat.py \
  -i chapter1.wav chapter2.wav chapter3.wav \
  --crossfade 0.5 \
  -o audiobook.mp3
```

---

#### Type: Meditation / Relaxation Audio

**Generate calming narration:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/voice-generation/scripts/gemini_tts.py \
  --text "Close your eyes. Take a deep breath in... and slowly release..." \
  --voice Achernar \
  --style "Calm, soothing, slow pace, relaxing, gentle, meditation guide"
```

**Generate ambient soundscape:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/music-generation/scripts/lyria.py \
  --prompt "ambient, meditation, peaceful, nature sounds, gentle, calming" \
  --duration 300 \
  --density 0.1 \
  --brightness 0.6
```

**Mix with high ambient volume:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/media-utils/scripts/audio_mix.py \
  --voice meditation_guide.wav \
  --music ambient.wav \
  --music-volume 0.5 \
  -o meditation_session.mp3
```

---

### Step 4: Deliver the Result

**Example delivery:**

"✅ Your audio ad is ready!

**File:** `coffee_radio_ad.mp3` (30s)

**What I created:**
- Energetic voiceover (Puck voice, radio announcer style)
- Upbeat background music (120 BPM)
- Music ducks under voice, fades out at end

**Structure:**
- 0-3s: Music hook
- 3-25s: Voice + music bed
- 25-30s: Music swell + tagline

**Want me to:**
- Try a different voice?
- Change the music energy?
- Adjust timing?"

---

## Voice Recommendations by Type

| Audio Type | Recommended Voices | Style Direction |
|------------|-------------------|-----------------|
| Corporate voiceover | Charon, Orus | Professional, measured |
| Audiobook | Algieba, Despina | Smooth, engaging |
| Radio ad | Puck, Laomedeia | Energetic, upbeat |
| Meditation | Achernar, Sulafat | Calm, soothing |
| Jingle tagline | Kore, Alnilam | Confident, memorable |
| Documentary | Gacrux, Rasalgethi | Mature, authoritative |
| Tutorial | Achird, Charon | Friendly, clear |

## Music Recommendations by Type

| Audio Type | Lyria Prompt | Settings |
|------------|--------------|----------|
| Corporate VO | "subtle, professional, ambient" | density: 0.2, brightness: 0.4 |
| Radio ad | "upbeat, energetic, catchy" | bpm: 120, density: 0.6 |
| Audiobook | "soft, ambient, unobtrusive" | density: 0.1, brightness: 0.3 |
| Meditation | "peaceful, ambient, nature" | density: 0.1, brightness: 0.6 |
| Jingle | "catchy, memorable, brand" | bpm: 110, density: 0.5 |

---

## Limitations

- **Gemini TTS max**: 32k tokens per request (split longer content)
- **Lyria instrumental only**: No vocals in background music
- **Processing time**: Long audiobooks take time to generate

## Example Prompts

**Voiceover:**
> "Create a professional voiceover for this script: '...' Add subtle corporate background music."

**Audio ad:**
> "Create a 30-second radio ad for our coffee brand. Energetic, memorable, with catchy music. End with 'Visit BestCoffee.com'"

**Jingle:**
> "Create a 5-second jingle for TechCorp. Modern, memorable, with the tagline 'Innovation for tomorrow'"

**Audiobook:**
> "Convert this text into an audiobook chapter. Use a warm, engaging narrator voice. Add subtle ambient music."

**Meditation:**
> "Create a 5-minute guided meditation. Calm, soothing voice with peaceful ambient background."
