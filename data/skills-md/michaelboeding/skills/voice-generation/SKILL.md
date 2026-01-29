---
name: voice-generation
description: >
  Use this skill for AI text-to-speech generation. Triggers include:
  "generate voice", "create audio", "text to speech", "TTS", "read this aloud",
  "generate narration", "create voiceover", "synthesize speech", "podcast audio",
  "dialogue audio", "multi-speaker", "audiobook"
  Supports Google Gemini TTS, ElevenLabs, and OpenAI TTS.
---

# Voice Generation Skill

Generate realistic speech using AI (Google Gemini TTS, ElevenLabs, OpenAI TTS).

## Prerequisites

At least one API key is required:

- `GOOGLE_API_KEY` - For Google Gemini TTS (same key as video/image/music) ✅
- `ELEVENLABS_API_KEY` - For ElevenLabs high-quality voice synthesis
- `OPENAI_API_KEY` - For OpenAI TTS voices

## Available APIs

### Google Gemini TTS (Recommended - Same API Key)
- **Best for**: Podcasts, dialogues, audiobooks with style control
- **Voices**: 30 voices with natural language style control
- **Multi-speaker**: Up to 2 speakers for dialogues ✅
- **Languages**: 24 languages (auto-detected)
- **Features**: Control style, accent, pace via prompts
- **Output**: 24kHz WAV
- **API Key**: Same `GOOGLE_API_KEY` as video/image/music ✅

### ElevenLabs (Best Quality)
- **Best for**: Natural-sounding voices, voice cloning, long-form content
- **Voices**: 100+ pre-made voices + custom voice cloning
- **Languages**: 29+ languages
- **Models**: Eleven Multilingual v2, Eleven Turbo v2

### OpenAI TTS (Simplest)
- **Best for**: Quick, reliable text-to-speech with consistent quality
- **Voices**: alloy, echo, fable, onyx, nova, shimmer
- **Models**: tts-1 (fast), tts-1-hd (high quality)
- **Output**: MP3, Opus, AAC, FLAC

## Workflow

### Step 1: Understand the Request

Parse the user's voice request for:
- **Text content**: What should be spoken?
- **Voice type**: Male, female, specific character?
- **Tone**: Professional, casual, dramatic, cheerful?
- **Use case**: Narration, voiceover, audiobook, notification?
- **Language**: English, Spanish, other?
- **Speed**: Normal, slow, fast?

### Step 2: Select Voice and API

Choose based on requirements:

| Use Case | Recommended API | Reason |
|----------|----------------|--------|
| **Default / Same key as video** | Gemini TTS | Same `GOOGLE_API_KEY` ✅ |
| **Multi-speaker dialogue** | Gemini TTS | Up to 2 speakers built-in |
| **Style/accent control** | Gemini TTS | Natural language prompts |
| **Voice cloning** | ElevenLabs | Only API with cloning |
| **100+ voice options** | ElevenLabs | Widest selection |
| **Audiobook/podcast** | ElevenLabs or Gemini | Both excellent for long content |
| **Quick narration** | OpenAI TTS | Fast, reliable |
| **Budget-conscious** | OpenAI TTS | Lower cost |

### Step 3: Prepare the Text

Optimize text for speech:

1. **Add pauses**: Use commas, periods for natural rhythm
2. **Spell out numbers**: "1,234" → "one thousand two hundred thirty-four" (if needed)
3. **Handle acronyms**: "NASA" vs "N.A.S.A." depending on pronunciation
4. **Mark emphasis**: Some APIs support emphasis markers

**Example transformation:**
- Original: "The Q4 2024 results show a 15% YoY increase."
- Optimized: "The Q4 2024 results show a fifteen percent year-over-year increase."

### Step 4: Generate the Audio

Execute the appropriate script from `${CLAUDE_PLUGIN_ROOT}/skills/voice-generation/scripts/`:

**For Google Gemini TTS (single speaker):**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/voice-generation/scripts/gemini_tts.py \
  --text "Welcome to our podcast!" \
  --voice "Charon"
```

**Gemini TTS with style direction:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/voice-generation/scripts/gemini_tts.py \
  --text "Have a wonderful day!" \
  --voice "Puck" \
  --style "Say cheerfully with a British accent:"
```

**Gemini TTS multi-speaker (dialogue):**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/voice-generation/scripts/gemini_tts.py \
  --multi \
  --speaker "Host:Charon" \
  --speaker "Guest:Aoede" \
  --text "Host: Welcome to the show!
Guest: Thanks for having me!"
```

**For ElevenLabs:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/voice-generation/scripts/elevenlabs.py \
  --text "Your text here" \
  --voice "Rachel" \
  --model "eleven_multilingual_v2"
```

**For OpenAI TTS:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/voice-generation/scripts/openai_tts.py \
  --text "Your text here" \
  --voice "nova" \
  --model "tts-1-hd"
```

**List Gemini voices:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/voice-generation/scripts/gemini_tts.py --list-voices
```

### Step 5: Deliver the Result

1. Provide the generated audio file path
2. Mention the voice and settings used
3. Offer to:
   - Try a different voice
   - Adjust speed or tone
   - Use a different API
   - Generate in a different format

## Error Handling

**Missing API key**: Inform the user which key is needed:
- Gemini TTS: Same `GOOGLE_API_KEY` as video/image - https://aistudio.google.com/apikey
- ElevenLabs: https://elevenlabs.io
- OpenAI: https://platform.openai.com/api-keys

**Gemini TTS requires google-genai package**: `pip install google-genai`

**Text too long**: Split into chunks and concatenate, or suggest shorter text.

**Rate limit**: Suggest waiting or trying a different API.

**Unsupported language**: Suggest an alternative API that supports the language.

**Multi-speaker limit**: Gemini TTS supports max 2 speakers. For more, use ElevenLabs with multiple calls.

## Voice Selection Guide

### Google Gemini TTS Voices (30 voices)
| Style | Voices | Best For |
|-------|--------|----------|
| Bright/Upbeat | Zephyr, Puck, Aoede, Laomedeia | Marketing, cheerful content |
| Firm/Informative | Charon, Kore, Orus, Rasalgethi | News, tutorials, professional |
| Soft/Warm | Achernar, Sulafat, Vindemiatrix | Meditation, gentle narration |
| Smooth | Algieba, Despina, Callirrhoe | Audiobooks, storytelling |
| Clear | Erinome, Iapetus, Pulcherrima | Instructions, clarity |
| Character | Fenrir (excitable), Enceladus (breathy), Algenib (gravelly), Gacrux (mature) | Character voices, drama |
| Friendly | Achird, Zubenelgenubi (casual) | Casual, conversational |

**Gemini TTS Style Tips:**
- Use natural language: `--style "Say angrily:"` or `--style "Whisper mysteriously:"`
- Specify accents: `--style "Speak with a British accent from London:"`
- Control pace: `--style "Speak slowly and deliberately:"`
- Combine: `--style "Say excitedly with a Southern US accent:"`

### OpenAI TTS Voices
| Voice | Description | Best For |
|-------|-------------|----------|
| alloy | Neutral, balanced | General purpose |
| echo | Warm, conversational | Podcasts, casual |
| fable | Expressive, British | Storytelling |
| onyx | Deep, authoritative | Narration, professional |
| nova | Friendly, upbeat | Marketing, tutorials |
| shimmer | Soft, gentle | Meditation, ASMR |

### ElevenLabs Popular Voices
| Voice | Description | Best For |
|-------|-------------|----------|
| Rachel | Young female, American | Narration, audiobooks |
| Domi | Young female, energetic | Marketing, ads |
| Bella | Young female, soft | Storytelling |
| Antoni | Young male, well-rounded | Narration |
| Josh | Young male, deep | Audiobooks |
| Arnold | Mature male, authoritative | Documentary |
| Adam | Middle-aged male, deep | Narration |
| Sam | Young male, raspy | Character voices |

## Best Practices

### For Narration
- Use a consistent voice throughout
- Add natural pauses between paragraphs
- Consider pacing for the content type

### For Dialogue
- Use different voices for different characters
- Match voice characteristics to character descriptions
- Adjust speed for emotional scenes

### For Accessibility
- Use clear, well-paced speech
- Avoid overly stylized voices
- Test with screen readers if applicable

## API Comparison

| Feature | Gemini TTS | ElevenLabs | OpenAI TTS |
|---------|------------|------------|------------|
| API Key | `GOOGLE_API_KEY` ✅ | `ELEVENLABS_API_KEY` | `OPENAI_API_KEY` |
| Voice quality | Excellent | Excellent | Very good |
| Voice variety | 30 voices | 100+ voices | 6 voices |
| Multi-speaker | ✅ Up to 2 | ❌ No | ❌ No |
| Style control | ✅ Natural language | Limited | ❌ No |
| Voice cloning | ❌ No | ✅ Yes | ❌ No |
| Languages | 24 | 29+ | 50+ |
| Speed control | Via prompts | Yes | Yes (0.25-4x) |
| Max length | 32k tokens | 5,000 chars | 4,096 chars |
| Output format | WAV (24kHz) | MP3, WAV | MP3, Opus, AAC, FLAC |
| Same key as video/image | ✅ Yes | ❌ No | ❌ No |
