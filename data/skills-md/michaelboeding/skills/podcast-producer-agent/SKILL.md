---
name: podcast-producer-agent
description: >
  Use this skill to create podcast episodes, interviews, dialogues, and conversation-style audio.
  Triggers: "create podcast", "podcast episode", "interview audio", "dialogue", "conversation",
  "two hosts discussing", "audio show", "radio show", "audio drama"
  Orchestrates: script generation, multi-speaker TTS, intro/outro music, and audio assembly.
---

# Podcast Producer

Create complete podcast episodes, interviews, and conversation-style audio content.

**This is an orchestrator skill** that combines:
- Script/dialogue generation (Claude)
- Multi-speaker voice synthesis (Gemini TTS)
- Intro/outro music (Lyria)
- Audio assembly (FFmpeg via media-utils)

## What You Can Create

| Type | Example |
|------|---------|
| Podcast episode | Two hosts discussing a topic |
| Interview | Q&A format with host and guest |
| Dialogue | Scripted conversation between characters |
| Audio drama | Story with multiple characters |
| Radio show | Formatted audio program with segments |

## Prerequisites

- `GOOGLE_API_KEY` - For Gemini TTS (voices) and Lyria (music)
- FFmpeg installed: `brew install ffmpeg` (macOS) or `apt install ffmpeg` (Linux)

## Workflow

### Step 1: Gather Requirements (REQUIRED)

⚠️ **DO NOT skip this step. Use interactive questioning — ask ONE question at a time.**

#### Question Flow

⚠️ **Use the `AskUserQuestion` tool for each question below.** Do not just print questions in your response — use the tool to create interactive prompts with the options shown.

**Q1: Topic**
> "I'll create that podcast episode! First — **what's the topic?**
> 
> *(What should the hosts discuss?)*"

*Wait for response.*

**Q2: Hosts**
> "Who are the **hosts/speakers**?
> 
> *(Names and brief personality — e.g., 'Sarah, enthusiastic tech expert' — max 2 for TTS)*"

*Wait for response.*

**Q3: Duration**
> "How **long** should the episode be?
> 
> - 5 minutes
> - 10 minutes
> - 15 minutes
> - Or specify your own"

*Wait for response.*

**Q4: Tone**
> "What **tone**?
> 
> - Professional
> - Casual/conversational
> - Funny/entertaining
> - Serious/educational
> - Or describe your own"

*Wait for response.*

**Q5: Music**
> "What **music style** for intro/outro?
> 
> - Upbeat pop
> - Chill lo-fi
> - Corporate/professional
> - Electronic
> - Or describe your own"

*Wait for response.*

#### Quick Reference

| Question | Determines |
|----------|------------|
| Topic | Script content and discussion points |
| Hosts | Voice selection and script style |
| Duration | Script length |
| Tone | Writing style and energy |
| Music | Lyria prompt for intro/outro |

---

### Step 2: Generate the Script

Use Claude to create the dialogue script with speaker labels:

```
[INTRO MUSIC: 10 seconds, upbeat tech podcast vibe]

Sarah: Welcome back to Tech Talk! I'm Sarah, and today we have something exciting.

Mike: Hey everyone! I'm Mike, and yes - we're diving into AI in healthcare.

Sarah: So Mike, what's the biggest change you've seen this year?

Mike: Great question! The use of AI for diagnostic imaging has exploded...

[Continue dialogue...]

[OUTRO MUSIC: Fade under last lines, 5 seconds after]

Sarah: Thanks for listening! Follow us for more episodes.

Mike: See you next time!
```

**Script Guidelines:**
- Use speaker names exactly as they'll be configured in TTS
- Include music cues in brackets: `[INTRO MUSIC: description]`
- Natural conversation flow with back-and-forth
- Aim for ~150 words per minute of audio

---

### Step 3: Plan Asset Generation

Create a manifest of what needs to be generated:

```json
{
  "project": "tech_talk_ai_healthcare",
  "duration_target": "5 minutes",
  "speakers": [
    {"name": "Sarah", "voice": "Kore", "style": "Enthusiastic, upbeat"},
    {"name": "Mike", "voice": "Puck", "style": "Friendly, knowledgeable"}
  ],
  "assets": [
    {
      "type": "music",
      "name": "intro_music",
      "prompt": "upbeat tech podcast, electronic, modern",
      "duration": 15,
      "script": "lyria"
    },
    {
      "type": "dialogue", 
      "name": "main_content",
      "speakers": ["Sarah", "Mike"],
      "text": "[the dialogue script]",
      "script": "gemini_tts"
    },
    {
      "type": "music",
      "name": "outro_music",
      "prompt": "same as intro, fade out",
      "duration": 10,
      "script": "lyria"
    }
  ],
  "assembly": [
    {"action": "mix", "voice": "intro_with_music", "music": "intro_music", "music_volume": 0.8},
    {"action": "concat", "files": ["intro_with_music", "main_content"]},
    {"action": "mix", "voice": "main_content_end", "music": "outro_music", "fade_out": 5}
  ]
}
```

---

### Step 4: Generate Assets

Execute each generation step:

**Generate intro music (Lyria):**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/music-generation/scripts/lyria.py \
  --prompt "upbeat tech podcast, electronic, modern, positive energy" \
  --duration 15 \
  --bpm 120
```

**Generate dialogue (Gemini TTS multi-speaker):**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/voice-generation/scripts/gemini_tts.py \
  --multi \
  --speaker "Sarah:Kore" \
  --speaker "Mike:Puck" \
  --text "[dialogue script from Step 2]" \
  --style "Make Sarah sound enthusiastic and upbeat. Mike sounds friendly and knowledgeable."
```

**Generate outro music (same as intro or variation):**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/music-generation/scripts/lyria.py \
  --prompt "upbeat tech podcast, electronic, fade out feel" \
  --duration 10 \
  --bpm 120
```

---

### Step 5: Assemble the Podcast

Use media-utils to stitch everything together:

**Mix intro music with beginning of dialogue:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/media-utils/scripts/audio_mix.py \
  --voice dialogue.wav \
  --music intro_music.wav \
  --music-volume 0.4 \
  --fade-out 3 \
  -o intro_mixed.wav
```

**Concatenate all segments:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/media-utils/scripts/audio_concat.py \
  -i intro_mixed.wav main_dialogue.wav outro_mixed.wav \
  --crossfade 1.0 \
  -o final_podcast.mp3
```

---

### Step 6: Deliver the Result

Provide:
1. The final audio file
2. Summary of what was created
3. Offer adjustments

**Example delivery:**

"✅ Your podcast episode is ready!

**File:** `tech_talk_ai_healthcare.mp3` (5:23)

**What I created:**
- Dialogue between Sarah (Kore voice) and Mike (Puck voice)
- 15s upbeat electronic intro music
- 10s outro music fade

**Want me to:**
- Adjust the voices or tone?
- Change the music style?
- Extend or shorten any section?
- Add more topics to the discussion?"

---

## Voice Pairing Suggestions

| Host Type | Suggested Voice | Description |
|-----------|-----------------|-------------|
| Main host (energetic) | Kore, Puck, Laomedeia | Firm, upbeat |
| Co-host (calm) | Charon, Algieba | Informative, smooth |
| Guest (expert) | Rasalgethi, Gacrux | Knowledgeable, mature |
| Interviewer | Achird | Friendly |
| Narrator | Charon, Orus | Informative, clear |

## Music Style Suggestions

| Podcast Type | Music Prompt |
|--------------|--------------|
| Tech/Business | "upbeat electronic, modern, corporate, positive" |
| Casual/Comedy | "fun, playful, acoustic guitar, lighthearted" |
| News/Serious | "subtle, professional, ambient, understated" |
| Storytelling | "cinematic, emotional, orchestral, atmospheric" |
| Health/Wellness | "calm, peaceful, ambient, gentle piano" |
| True Crime | "dark, suspenseful, minimal, tension" |

## Limitations

- **Max 2 speakers** per Gemini TTS call (for more, generate separate files and concatenate)
- **Lyria is instrumental only** - no vocals in music
- **Duration estimates** may vary - dialogue length depends on speaking pace
- **Music loops** if shorter than dialogue

## Error Handling

| Error | Solution |
|-------|----------|
| "GOOGLE_API_KEY not set" | Set up API key per README |
| "FFmpeg not found" | Install: `brew install ffmpeg` |
| "google-genai not installed" | Run: `pip install google-genai` |
| TTS too long | Split script into segments, generate separately, concat |

## Example Prompts

**Simple:**
> "Create a 3-minute podcast episode about remote work tips with two hosts"

**Detailed:**
> "Create a 5-minute tech podcast episode. Hosts: Alex (enthusiastic, tech-savvy) and Jordan (skeptical, asks good questions). Topic: The future of AI assistants. Include upbeat electronic intro/outro music. Casual but informative tone."

**With provided script:**
> "Turn this dialogue into a podcast episode with intro/outro music:
> Alex: Hey everyone, welcome back!
> Jordan: Today we're talking about..."
