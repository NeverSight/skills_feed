---
name: listenhub
description: |
  Explain anything — turn ideas into podcasts, explainer videos, or voice narration.
  Use when the user wants to "make a podcast", "create an explainer video",
  "read this aloud", "generate an image", or share knowledge in audio/visual form.
  Supports: topic descriptions, YouTube links, article URLs, plain text, and image prompts.
---

<purpose>
**The Hook**: Paste content, get audio/video/image. That simple.

Four modes, one entry point:
- **Podcast** — Two-person dialogue, ideal for deep discussions
- **Explain** — Single narrator + AI visuals, ideal for product intros
- **TTS/Flow Speech** — Pure voice reading, ideal for articles
- **Image Generation** — AI image creation, ideal for creative visualization

Users don't need to remember APIs, modes, or parameters. Just say what you want.
</purpose>

<instructions>

## ⛔ Hard Constraints (Inviolable)

**The scripts are the ONLY interface. Period.**

```
┌─────────────────────────────────────────────────────────┐
│  AI Agent  ──▶  ./scripts/*.sh  ──▶  ListenHub API     │
│                      ▲                                  │
│                      │                                  │
│            This is the ONLY path.                       │
│            Direct API calls are FORBIDDEN.              │
└─────────────────────────────────────────────────────────┘
```

**MUST**:
- Execute functionality ONLY through provided scripts in `**/skills/listenhub/scripts/`
- Pass user intent as script arguments exactly as documented
- Trust script outputs; do not second-guess internal logic

**MUST NOT**:
- Write curl commands to ListenHub/Marswave API directly
- Construct JSON bodies for API calls manually
- Guess or fabricate speakerIds, endpoints, or API parameters
- Assume API structure based on patterns or web searches
- Hallucinate features not exposed by existing scripts

**Why**: The API is proprietary. Endpoints, parameters, and speakerIds are NOT publicly documented. Web searches will NOT find this information. Any attempt to bypass scripts will produce incorrect, non-functional code.

## Script Location

Scripts are located at `**/skills/listenhub/scripts/` relative to your working context.

Different AI clients use different dot-directories:
- Claude Code: `.claude/skills/listenhub/scripts/`
- Other clients: may vary (`.cursor/`, `.windsurf/`, etc.)

**Resolution**: Use glob pattern `**/skills/listenhub/scripts/*.sh` to locate scripts reliably, or resolve from the SKILL.md file's own path.

## Private Data (Cannot Be Searched)

The following are **internal implementation details** that AI cannot reliably know:

| Category | Examples | How to Obtain |
|----------|----------|---------------|
| API Base URL | `api.marswave.ai/...` | ✗ Cannot — internal to scripts |
| Endpoints | `podcast/episodes`, etc. | ✗ Cannot — internal to scripts |
| Speaker IDs | `cozy-man-english`, etc. | ✓ Call `get-speakers.sh` |
| Request schemas | JSON body structure | ✗ Cannot — internal to scripts |
| Response formats | Episode ID, status codes | ✓ Documented per script |

**Rule**: If information is not in this SKILL.md or retrievable via a script (like `get-speakers.sh`), assume you don't know it.

## Design Philosophy

**Hide complexity, reveal magic.**

Users don't need to know: Episode IDs, API structure, polling mechanisms, credits, endpoint differences.
Users only need: Say idea → wait a moment → get the link.

## Environment

### ListenHub API Key

API key stored in `$LISTENHUB_API_KEY`. Check on first use:

```bash
source ~/.zshrc 2>/dev/null; [ -n "$LISTENHUB_API_KEY" ] && echo "ready" || echo "need_setup"
```

If setup needed, guide user:
1. Visit https://listenhub.ai/zh/settings/api-keys
2. Paste key (only the `lh_sk_...` part)
3. Auto-save to ~/.zshrc

### Labnana API Key (for Image Generation)

API key stored in `$LABNANA_API_KEY`, output path in `$LABNANA_OUTPUT_DIR`.

On first image generation, the script auto-guides configuration:
1. Visit https://labnana.com/api-keys (requires subscription)
2. Paste API key
3. Configure output path (default: ~/Downloads)
4. Auto-save to shell rc file

**Security**: Never expose full API keys in output.

## Mode Detection

Auto-detect mode from user input:

**→ Podcast (Two-person dialogue)**
- Keywords: "podcast", "chat about", "discuss", "debate", "dialogue"
- Use case: Topic exploration, opinion exchange, deep analysis
- Feature: Two voices, interactive feel

**→ Explain (Explainer video)**
- Keywords: "explain", "introduce", "video", "explainer", "tutorial"
- Use case: Product intro, concept explanation, tutorials
- Feature: Single narrator + AI-generated visuals, can export video

**→ TTS (Text-to-speech)**
- Keywords: "read aloud", "convert to speech", "tts", "voice"
- Use case: Article to audio, note review, document narration
- Feature: Fastest (1-2 min), pure audio

**→ Image Generation**
- Keywords: "generate image", "draw", "create picture", "visualize"
- Use case: Creative visualization, concept art, illustrations
- Feature: AI image generation via Labnana API, multiple resolutions and aspect ratios

**Default**: If unclear, ask user which format they prefer.

**Explicit override**: User can say "make it a podcast" / "I want explainer video" / "just voice" / "generate image" to override auto-detection.

## Interaction Flow

### Step 1: Receive input + detect mode

```
→ Got it! Preparing...
  Mode: Two-person podcast
  Topic: Latest developments in Manus AI
```

For URLs, identify type:
- `youtu.be/XXX` → convert to `https://www.youtube.com/watch?v=XXX`
- Other URLs → use directly

### Step 2: Submit generation

```
→ Generation submitted

  Estimated time:
  • Podcast: 2-3 minutes
  • Explain: 3-5 minutes
  • TTS: 1-2 minutes

  You can:
  • Wait and ask "done yet?"
  • Check listenhub.ai/zh/app/library
  • Do other things, ask later
```

Internally remember Episode ID for status queries.

### Step 3: Query status

When user says "done yet?" / "ready?" / "check status":

- **Success**: Show result + next options
- **Processing**: "Still generating, wait another minute?"
- **Failed**: "Generation failed, content might be unparseable. Try another?"

### Step 4: Show results

**Podcast result**:
```
✓ Podcast generated!

  "{title}"

  Listen: https://listenhub.ai/zh/app/library

  Duration: ~{duration} minutes

  Need to download? Just say so.
```

**Explain result**:
```
✓ Explainer video generated!

  "{title}"

  Watch: https://listenhub.ai/zh/app/explainer-video/slides/{episodeId}

  Duration: ~{duration} minutes

  Need to download audio? Just say so.
```

**Image result**:
```
✓ Image generated!

  ~/Downloads/labnana-{timestamp}.jpg
```

**Important**: Prioritize web experience. Only provide download URLs when user explicitly requests.

## Script Reference

All scripts are curl-based (no extra dependencies). Locate via `**/skills/listenhub/scripts/*.sh`.

**⚠️ Long-running Tasks**: Generation may take 1-5 minutes. Use your CLI client's native background execution feature:

- **Claude Code**: set `run_in_background: true` in Bash tool
- **Other CLIs**: use built-in async/background job management if available

**Invocation pattern**: `$SCRIPTS/script-name.sh [args]`

Where `$SCRIPTS` = resolved path to `**/skills/listenhub/scripts/`

### Podcast (One-Stage)
```bash
$SCRIPTS/create-podcast.sh "query" [mode] [source_url]
# mode: quick (default) | deep | debate
# source_url: optional URL for content analysis

# Example:
$SCRIPTS/create-podcast.sh "The future of AI development" deep
$SCRIPTS/create-podcast.sh "Analyze this article" deep "https://example.com/article"
```

### Podcast (Two-Stage: Text → Audio)
For advanced workflows requiring script editing between generation:

```bash
# Stage 1: Generate text content
$SCRIPTS/create-podcast-text.sh "query" [mode] [source_url]
# Returns: episode_id + scripts array

# Stage 2: Generate audio from text
$SCRIPTS/create-podcast-audio.sh "<episode-id>" [modified_scripts.json]
# Without scripts file: uses original scripts
# With scripts file: uses modified scripts
```

### Speech (Multi-Speaker)
```bash
$SCRIPTS/create-speech.sh <scripts_json_file>
# Or pipe: echo '{"scripts":[...]}' | $SCRIPTS/create-speech.sh -

# scripts.json format:
# {
#   "scripts": [
#     {"content": "Script content here", "speakerId": "speaker-id"},
#     ...
#   ]
# }
```

### Get Available Speakers
```bash
$SCRIPTS/get-speakers.sh [language]
# language: zh (default) | en
```

**Response structure** (for AI parsing):
```json
{
  "code": 0,
  "data": {
    "items": [
      {
        "name": "Yuanye",
        "speakerId": "cozy-man-english",
        "gender": "male",
        "language": "zh"
      }
    ]
  }
}
```

**Usage**: When user requests specific voice characteristics (gender, style), call this script first to discover available `speakerId` values. NEVER hardcode or assume speakerIds.

### Explain
```bash
$SCRIPTS/create-explainer.sh "<topic>" [mode]
# mode: info (default) | story

# Generate video file (optional)
$SCRIPTS/generate-video.sh "<episode-id>"
```

### TTS
```bash
$SCRIPTS/create-tts.sh "<text>" [mode]
# mode: smart (default) | direct
```

### Image Generation
```bash
$SCRIPTS/generate-image.sh "<prompt>" [size] [ratio] [reference_images]
# size: 1K | 2K | 4K (default: 2K)
# ratio: 16:9 | 1:1 | 9:16 | 2:3 | 3:2 | 3:4 | 4:3 | 21:9 (default: 16:9)
# reference_images: comma-separated URLs (max 14), e.g. "url1,url2"
#   - Provides visual guidance for style, composition, or content
#   - Supports jpg, png, gif, webp, bmp formats
#   - URLs must be publicly accessible
```

### Check Status
```bash
$SCRIPTS/check-status.sh "<episode-id>" <type>
# type: podcast | explainer | tts
```

## Language Adaptation

**Automatic Language Detection**: Adapt output language based on user input and context.

**Detection Rules**:
1. **User Input Language**: If user writes in Chinese, respond in Chinese. If user writes in English, respond in English.
2. **Context Consistency**: Maintain the same language throughout the interaction unless user explicitly switches.
3. **CLAUDE.md Override**: If project-level CLAUDE.md specifies a default language, respect it unless user input indicates otherwise.
4. **Mixed Input**: If user mixes languages, prioritize the dominant language (>50% of content).

**Application**:
- Status messages: "→ Got it! Preparing..." (English) vs "→ 收到！准备中..." (Chinese)
- Error messages: Match user's language
- Result summaries: Match user's language
- Script outputs: Pass through as-is (scripts handle their own language)

**Example**:
```
User (Chinese): "生成一个关于 AI 的播客"
AI (Chinese): "→ 收到！准备双人播客..."

User (English): "Make a podcast about AI"
AI (English): "→ Got it! Preparing two-person podcast..."
```

**Principle**: Language is interface, not barrier. Adapt seamlessly to user's natural expression.

## AI Responsibilities

### Black Box Principle

**You are a dispatcher, not an implementer.**

Your job is to:
1. Understand user intent (what do they want to create?)
2. Select the correct script (which tool fits?)
3. Format arguments correctly (what parameters?)
4. Execute and relay results (what happened?)

Your job is NOT to:
- Understand or modify script internals
- Construct API calls directly
- Guess parameters not documented here
- Invent features that scripts don't expose

### Mode-Specific Behavior

**ListenHub modes (passthrough)**:
- Podcast/Explain/TTS/Speech → pass user input directly
- Server has full AI capability to process content
- If user needs specific speakers → call `get-speakers.sh` first to list options

**Labnana mode (enhance)**:
- Image Generation → client-side AI optimizes prompt
- Thin forwarding layer, needs client intelligence enhancement

## Prompt Optimization (Image Generation)

When generating images, optimize user prompts by adding:

**Style Enhancement**:
- "cyberpunk" → add "neon lights, futuristic, dystopian"
- "ink painting" → add "Chinese ink painting, traditional art style"
- "photorealistic" → add "highly detailed, 8K quality"

**Scene Details**:
- Time: at night / at sunset / in the morning
- Lighting: dramatic lighting / soft lighting / neon glow
- Weather: rainy / foggy / clear sky

**Composition Quality**:
- Composition: cinematic composition / wide-angle / close-up
- Quality: highly detailed / 8K quality / professional photography

**DO**:
- Understand user intent, add missing details
- Use English keywords (models trained on English)
- Add quality descriptors
- Keep user's core intent unchanged
- Show optimized prompt transparently

**DON'T**:
- Drastically change user's original meaning
- Add elements user explicitly doesn't want
- Over-stack complex terminology
- If user wants "simple", don't add "highly detailed"

</instructions>

<examples>

<example name="podcast-request">
<user>Make a podcast about the latest AI developments</user>
<response>
→ Got it! Preparing two-person podcast...
  Topic: Latest AI developments

→ Generation submitted, about 2-3 minutes

  You can:
  • Wait and ask "done yet?"
  • Check listenhub.ai/zh/app/library
</response>
</example>

<example name="explainer-request">
<user>Create an explainer video introducing Claude Code</user>
<response>
→ Got it! Preparing explainer video...
  Topic: Claude Code introduction

→ Generation submitted, explainer videos take 3-5 minutes

  Includes: Script + narration + AI visuals
</response>
</example>

<example name="tts-request">
<user>Convert this article to speech https://blog.example.com/article</user>
<response>
→ Got it! Parsing article...

→ TTS submitted, about 1-2 minutes

  Wait a moment, or ask "done yet?" to check
</response>
</example>

<example name="image-generation">
<user>Generate an image: cyberpunk city at night</user>
<response>
→ Generating image...

  Original: cyberpunk city at night

  Optimized prompt:
  "Cyberpunk city at night, neon lights reflecting on wet streets,
   towering skyscrapers with holographic ads, flying vehicles,
   cinematic composition, highly detailed, 8K quality"

  Resolution: 4K (16:9)

✓ Image generated!
  ~/Downloads/labnana-20260121-143145.jpg
</response>
</example>

<example name="image-with-reference">
<user>Generate an image in this style: https://example.com/style-ref.jpg, prompt: "a futuristic car"</user>
<response>
→ Generating image with reference...

  Prompt: a futuristic car
  Reference images: 1
  Resolution: 2K (16:9)

✓ Image generated!
  ~/Downloads/labnana-20260122-154230.jpg
</response>
</example>

<example name="status-check">
<user>Done yet?</user>
<response>
✓ Podcast generated!

  "AI Revolution: From GPT to AGI"

  Listen: https://listenhub.ai/zh/app/library

  Duration: ~8 minutes

  Need to download? Just say so.
</response>
</example>

</examples>
