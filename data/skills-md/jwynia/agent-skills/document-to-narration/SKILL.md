---
name: document-to-narration
description: "Convert written documents to narrated video scripts with TTS audio and word-level timing. Use when preparing essays, blog posts, or articles for video narration. Outputs scene files, audio, and VTT with precise word timestamps. Keywords: narration, voiceover, TTS, scenes, audio, timing, video script, spoken."
license: MIT
compatibility: Requires Deno, Python 3.12 with venv, ffmpeg, whisper-cpp
metadata:
  author: jwynia
  version: "1.0"
  domain: video-production
  type: generator
  mode: generative
---

# Document to Narration

Convert written documents into narrated video scripts with precise word-level timing.

## Core Principle

**The agent interprets; the document guides.** Rather than rigid template-based splits, this skill uses agent judgment to find where the content naturally breathes, argues, and transitions. The document's argument flow determines scene breaks, not a predetermined structure.

## When to Use This Skill

Use this skill when:
- Converting a blog post or essay to video narration
- Preparing content for TTS audio generation
- Breaking long-form content into digestible scenes
- Creating word-level synchronized captions for video

Do NOT use this skill when:
- The content is already in scene/script format
- You need real-time voice synthesis (this is batch processing)
- Working with dialogue or multi-speaker content (single voice only)

## Prerequisites

- **Deno** installed (https://deno.land/)
- **Python 3.12** with venv support
- **ffmpeg** for audio conversion
- **whisper-cpp** (installed via @remotion/install-whisper-cpp)
- **TTS model** at `tts/model/` (not in git due to size - see Model Setup below)

## Complete Pipeline

There are two approaches: **per-scene** (legacy) and **full narration** (recommended).

### Full Narration Pipeline (Recommended)

Generates a single audio file for consistent volume and pacing:

```
Document (.md)
    ↓ [agent interprets scene breaks]
Scene .txt files (01-scene-name.txt, 02-scene-name.txt, ...)
    ↓ [TTS via narrate-full.py - SINGLE PASS]
full-narration.wav (one consistent audio file)
    ↓ [Whisper via transcribe-full.py]
full-narration.json + full-narration.vtt (word-level timing)
    ↓ [extract-scene-boundaries.py]
Scene timing boundaries for video composition
```

### Per-Scene Pipeline (Legacy)

Generates separate audio per scene - **can cause volume inconsistencies**:

```
Scene .txt files
    ↓ [TTS via narrate-scenes.py - MULTIPLE PASSES]
Scene .wav files (volume may vary between scenes)
    ↓ [concatenate]
Combined audio (may have clipping at boundaries)
```

> **Warning:** Per-scene TTS generates audio with different volume levels and pacing. When concatenated, this causes audible jumps and clipping. Use the full narration pipeline instead.

## Quick Start

### Full Narration Pipeline (Recommended)

```bash
cd .claude/skills/document-to-narration
source tts/.venv/bin/activate

# 1. Split document into scenes (manual or scripted)
deno run --allow-read --allow-write scripts/split-to-scenes.ts input.md --output ./output/

# 2. Generate single audio file
python scripts/narrate-full.py ./output/scenes/

# 3. Transcribe with word-level timestamps
python scripts/transcribe-full.py ./output/full-narration.wav

# 4. Extract scene boundaries for video timing
python scripts/extract-scene-boundaries.py ./output/scenes/ ./output/full-narration.json --typescript
```

### Legacy Per-Scene Pipeline

```bash
# 1. Split document into scenes
deno run --allow-read --allow-write scripts/split-to-scenes.ts input.md --output ./output/

# 2. Generate audio per scene (may have volume inconsistencies)
source tts/.venv/bin/activate
python scripts/narrate-scenes.py ./output/scenes/

# 3. Transcribe (DEPRECATED: transcribe-scenes.ts requires whisper-cpp)
# Use transcribe-full.py instead after concatenating audio
```

## Instructions

### Step 1: Setup (First Time Only)

#### Create Python Virtual Environment

```bash
cd .claude/skills/document-to-narration/tts
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### TTS Model Setup

The fine-tuned voice model (~7.8GB) is not included in git due to size.
Place your Qwen3-TTS model files in `tts/model/`:

```
tts/model/
├── config.json
├── generation_config.json
├── model.safetensors      # Main model weights
├── tokenizer_config.json
├── vocab.json
├── merges.txt
└── speech_tokenizer/
    └── ...
```

#### Install Whisper (if not already installed)

The @remotion/install-whisper-cpp package handles this:
```typescript
import { installWhisperCpp, downloadWhisperModel } from '@remotion/install-whisper-cpp';

await installWhisperCpp({ to: './whisper-cpp', version: '1.5.5' });
await downloadWhisperModel({ model: 'medium', folder: './whisper-cpp' });
```

### Step 2: Prepare Your Document

The skill works best with:
- Markdown documents with clear heading structure (H1, H2)
- Well-structured arguments with distinct sections
- Content that reads naturally aloud

### Step 3: Run the Pipeline

```bash
deno run -A scripts/full-pipeline.ts /path/to/essay.md --output ./output/essay-name/
```

### Step 4: Review Output

```
output/essay-name/
├── scenes/
│   ├── 01-opening-hook.txt      # Scene script
│   ├── 01-opening-hook.wav      # Generated audio
│   ├── 01-opening-hook.vtt      # Word-level captions
│   ├── 02-core-argument.txt
│   ├── 02-core-argument.wav
│   ├── 02-core-argument.vtt
│   └── ...
└── manifest.json                # Complete timing data
```

## Scene Boundary Heuristics

The agent identifies scene breaks using these heuristics:

### Strong Boundaries (Almost Always Break)
- H2 heading changes
- "Here's the thing" / "The point is" pivot statements
- Major metaphor introduction
- Explicit enumeration ("First...", "Second...")
- Significant perspective shifts

### Moderate Boundaries (Consider Breaking)
- Long paragraph after short ones (or vice versa)
- Example-to-principle transitions
- "But" / "However" / "Meanwhile" at paragraph start
- Question-then-answer patterns

### Weak Boundaries (Usually Keep Together)
- Paragraph-to-paragraph within same example
- Sequential evidence for same point
- Build-up to a punchline/reveal

### Scene Length Guidance
- **Target**: 100-300 words per scene (30-90 seconds of audio)
- **Minimum**: 50 words (avoid micro-scenes)
- **Maximum**: 500 words (avoid cognitive overload)

## Anti-Patterns

### The Paragraph Slicer
**Pattern:** Breaking at every paragraph or heading mechanically.
**Problem:** Ignores argument flow. Scenes feel choppy and disconnected.
**Fix:** Look for rhetorical units, not structural units. Multiple paragraphs often form one scene.

### The Wall of Text
**Pattern:** Keeping entire sections as single scenes.
**Problem:** Creates TTS audio that's too long. Loses natural breathing room.
**Fix:** Target 100-300 words. Find the natural pause point within sections.

### The Verbatim Transcriber
**Pattern:** Copying written text exactly without spoken adaptation.
**Problem:** Written conventions don't work when spoken. Parentheticals, complex punctuation, and nested clauses confuse TTS and listeners.
**Fix:** Apply adaptation rules. Read it aloud mentally.

### The Over-Adapter
**Pattern:** Rewriting content so heavily it loses the author's voice.
**Problem:** The result doesn't sound like the original author.
**Fix:** Preserve voice, adjust mechanics. If the author uses rhetorical questions, keep them.

## Available Scripts

### scripts/split-to-scenes.ts

Parse a markdown document and output scene text files.

```bash
deno run --allow-read --allow-write scripts/split-to-scenes.ts input.md --output ./output/
deno run --allow-read --allow-write scripts/split-to-scenes.ts input.md --output ./output/ --adapt
deno run --allow-read scripts/split-to-scenes.ts input.md --dry-run
```

**Options:**
- `--output` - Directory for scene files (created if doesn't exist)
- `--adapt` - Apply spoken adaptation rules
- `--dry-run` - Preview scene breaks without writing files

**Output:** Numbered `.txt` files and initial `manifest.json`

### scripts/narrate-full.py (Recommended)

Generate a single TTS audio file from all scene files. Produces consistent volume and pacing.

```bash
python scripts/narrate-full.py ./output/scenes/
python scripts/narrate-full.py ./output/scenes/ --force
python scripts/narrate-full.py ./output/scenes/ --speaker jwynia
python scripts/narrate-full.py ./output/scenes/ --output ./custom/path/audio.wav
```

**Options:**
- `--force` - Regenerate even if output exists
- `--speaker` - Speaker name (default: jwynia)
- `--output` - Custom output path (default: `../full-narration.wav`)

**Output:** Single `full-narration.wav` in parent directory of scenes

### scripts/narrate-scenes.py (Legacy)

Generate TTS audio for each scene file separately. **Not recommended** - can cause volume inconsistencies when concatenated.

```bash
python scripts/narrate-scenes.py ./output/scenes/
python scripts/narrate-scenes.py ./output/scenes/ --force
python scripts/narrate-scenes.py ./output/scenes/ --speaker jwynia
```

**Options:**
- `--force` - Regenerate even if output exists
- `--speaker` - Speaker name (default: jwynia)

**Output:** `.wav` files alongside each `.txt` file

### scripts/transcribe-full.py (Recommended)

Transcribe audio with word-level timestamps using Python's openai-whisper.

```bash
python scripts/transcribe-full.py ./output/full-narration.wav
python scripts/transcribe-full.py ./output/full-narration.wav --model large-v3
python scripts/transcribe-full.py ./output/full-narration.wav --output-dir ./captions/
```

**Options:**
- `--model` - Whisper model: tiny, base, small, medium, large, large-v2, large-v3 (default: medium)
- `--output-dir` - Output directory (default: same as audio file)

**Output:**
- `.vtt` file with word-level timestamps
- `.json` file with captions array for Remotion

**Dependencies:** Requires `openai-whisper` in Python environment:
```bash
pip install openai-whisper
```

### scripts/extract-scene-boundaries.py

Extract scene timing boundaries from transcript by matching scene opening phrases.

```bash
# Human-readable table
python scripts/extract-scene-boundaries.py ./output/scenes/ ./output/full-narration.json

# JSON output
python scripts/extract-scene-boundaries.py ./output/scenes/ ./output/full-narration.json --json

# TypeScript for Video.tsx
python scripts/extract-scene-boundaries.py ./output/scenes/ ./output/full-narration.json --typescript
```

**Options:**
- `--json` - Output as JSON array
- `--typescript` - Output as TypeScript code for Video.tsx scenes array

**Output:** Scene numbers, slugs, start times, and durations

### scripts/transcribe-scenes.ts (Deprecated)

> **Deprecated:** Requires whisper-cpp binary which may not be installed. Use `transcribe-full.py` instead.

Transcribe per-scene audio files using whisper-cpp.

```bash
deno run --allow-read --allow-write --allow-run scripts/transcribe-scenes.ts ./output/scenes/
```

**Output:** `.vtt` files with word-level timestamps

### scripts/full-pipeline.ts

Orchestrate the complete pipeline.

```bash
deno run -A scripts/full-pipeline.ts input.md --output ./output/project-name/
```

**Options:**
- `--output` - Output directory (required)
- `--adapt` - Apply spoken adaptation
- `--skip-tts` - Skip audio generation (text only)
- `--skip-transcribe` - Skip Whisper transcription

## Output Format

### manifest.json

```json
{
  "source": "appliance-vs-trade-tool-draft.md",
  "created_at": "2024-01-15T10:30:00Z",
  "total_scenes": 9,
  "total_duration_seconds": 420,
  "scenes": [
    {
      "number": 1,
      "slug": "popcorn-opening",
      "word_count": 185,
      "audio_duration_seconds": 55.2,
      "files": {
        "text": "scenes/01-popcorn-opening.txt",
        "audio": "scenes/01-popcorn-opening.wav",
        "captions": "scenes/01-popcorn-opening.vtt"
      },
      "captions": [
        { "text": "Two", "startMs": 0, "endMs": 180, "confidence": 0.98 },
        { "text": "people", "startMs": 180, "endMs": 450, "confidence": 0.97 }
      ]
    }
  ]
}
```

### VTT Format

```vtt
WEBVTT

00:00.000 --> 00:00.180
Two

00:00.180 --> 00:00.450
people

00:00.450 --> 00:00.720
walk

00:00.720 --> 00:01.100
into
```

## Spoken Adaptation

When `--adapt` is enabled, the skill transforms written conventions to spoken equivalents:

| Written | Spoken |
|---------|--------|
| Parenthetical asides | Em-dash or separate sentence |
| "e.g." | "for example" |
| "i.e." | "that is" |
| Long nested clauses | Split into multiple sentences |
| Semicolons | Periods |
| `*emphasis*` | Context-appropriate stress |

**Preserve:**
- Author's voice and tone
- Rhetorical questions
- Deliberate repetition
- Key phrases and memorable formulations

## Integration

### With remotion-designer
- Pass manifest scene list to remotion-designer
- Each scene becomes a visual design unit
- Word-level timing drives text animation

### With Remotion Compositions
```tsx
import { Audio, useCurrentFrame, Sequence } from 'remotion';
import manifest from './output/manifest.json';

// Use scene durations for Sequence timing
{manifest.scenes.map((scene, i) => (
  <Sequence
    from={accumulatedFrames}
    durationInFrames={scene.audio_duration_seconds * fps}
  >
    <Audio src={staticFile(scene.files.audio)} />
    <CaptionRenderer captions={scene.captions} />
  </Sequence>
))}
```

## Technical Notes

### WAV Format Conversion
Whisper requires 16kHz mono WAV. The pipeline handles conversion automatically:
```bash
ffmpeg -i input.wav -ar 16000 -ac 1 output_16khz.wav
```

### TTS Model
The fine-tuned voice model (~7.8GB) is bundled at `tts/model/`. Uses Qwen3-TTS with custom speaker embedding.

### Performance
- TTS: ~5-30 seconds per sentence (Apple Silicon MPS or NVIDIA CUDA)
- Whisper: ~0.5-2x realtime depending on model size
- Full essay (~2000 words): ~10-20 minutes total processing

## What This Skill Does NOT Do

- Generate video visuals (use remotion-designer)
- Real-time voice synthesis
- Multi-speaker dialogue
- Edit or improve the content's argument
- Make editorial changes beyond mechanical spoken adaptation
