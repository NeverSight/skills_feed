---
name: text2speech
description: "Generate text-to-speech audio using Qwen3-TTS. Supports preset speakers, voice design from descriptions, voice cloning from audio/timbre, batch processing, and audio tokenization."
homepage: https://github.com/CatfishW/TTSAgentSkill
metadata:
  {
    "claude-code":
      {
        "emoji": "🔊",
        "requires": { "bins": ["python3"], "python_packages": ["requests"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "package": "text2speech-skill",
              "bins": ["text2speech", "t2s"],
              "label": "Install via npm",
            },
            {
              "id": "pip",
              "kind": "pip",
              "package": "text2speech-skill",
              "bins": ["text2speech", "t2s"],
              "label": "Install via pip",
            },
          ],
      },
  }
---

# Text2Speech Skill

Generate high-quality text-to-speech audio using Qwen3-TTS models.

## Prerequisites

- Python 3.8+
- `requests` package
- Access to TTSWeb API (https://mc.agaii.org/TTS)

## Installation

### Via npm (Node.js)

```bash
npm install -g @catfishw/text2speech-skill
```

### Via pip (Python)

```bash
pip install git+https://github.com/CatfishW/TTSAgentSkill.git
```

### Direct Usage

```bash
python3 -m text2speech_skill.cli --help
```

## Quick Start

### Speak with Preset Speaker

```bash
text2speech speak "Hello world" -s vivian -o hello.wav
```

### Design Custom Voice

```bash
text2speech design "Welcome to the future" \
  -d "futuristic female AI assistant, clear and professional" \
  -o welcome.wav
```

### Clone Voice from Audio

```bash
text2speech clone "This is my cloned voice speaking" \
  -a reference.wav \
  -r "original transcript of reference audio" \
  -o cloned.wav
```

### Clone with Preset Timbre

```bash
text2speech clone "Hello" -t ryan -o output.wav
```

## Commands

### speak

Text-to-speech with preset speaker voices.

```bash
text2speech speak <text> [options]

Options:
  -s, --speaker     Speaker name (default: vivian)
  -l, --language    Language code (default: Auto)
  -i, --instruct    Style instruction (e.g., "speak cheerfully")
  -o, --output      Output audio file (required)
```

**Speakers:** vivian, ryan, aiden, dylan, eric, ono_anna, serena, sohee, uncle_fu

**Examples:**
```bash
text2speech speak "Hello" -s vivian -o hello.wav
text2speech speak "Bonjour" -s serena -l French -o bonjour.wav
text2speech speak "Hi" -s ryan -i "speak like a news anchor" -o hi.wav
```

### design

Create voice from natural language description.

```bash
text2speech design <text> -d <description> [options]

Options:
  -d, --description  Voice description (required)
  -l, --language     Language code
  -o, --output       Output audio file (required)
```

**Examples:**
```bash
text2speech design "Hello" -d "old man with raspy voice" -o oldman.wav
text2speech design "Welcome" -d "young energetic female, enthusiastic" -o welcome.wav
```

### clone

Clone voice from reference audio or preset timbre.

```bash
text2speech clone <text> [options]

Options:
  -a, --audio           Reference audio file
  -t, --timbre          Preset timbre speaker (alternative to audio)
  -r, --ref-text        Reference transcript (for ICL mode)
  -x, --x-vector-only   Use x-vector only mode
  -i, --instruct        Style instruction
  -l, --language        Language code
  -o, --output          Output audio file (required)
```

**Examples:**
```bash
# Clone from audio with transcript (ICL mode)
text2speech clone "Hello" -a ref.wav -r "original text" -o out.wav

# Clone from audio (x-vector only, faster)
text2speech clone "Hello" -a ref.wav -x -o out.wav

# Clone using preset timbre
text2speech clone "Hello" -t ryan -o out.wav
```

### batch-speak

Batch process multiple text files.

```bash
text2speech batch-speak <input_dir> <output_dir> [options]

Options:
  -s, --speaker   Speaker name (default: vivian)
  -l, --language  Language code
  -i, --instruct  Style instruction
```

**Input:** Directory containing `.txt` files
**Output:** Audio files + `batch_report.json`

**Example:**
```bash
mkdir -p texts output
echo "Hello" > texts/1.txt
echo "World" > texts/2.txt
text2speech batch-speak texts/ output/ -s vivian
```

### batch-clone

Batch clone voice for multiple texts.

```bash
text2speech batch-clone <input_dir> <output_dir> -a <audio> [options]

Options:
  -a, --audio     Reference audio (required)
  -r, --ref-text  Reference transcript
  -l, --language  Language code
```

**Example:**
```bash
text2speech batch-clone texts/ output/ -a reference.wav -r "transcript"
```

### encode

Encode audio to tokens (tokenizer).

```bash
text2speech encode <audio> [-o output.json]
```

**Example:**
```bash
text2speech encode audio.wav -o tokens.json
cat tokens.json | jq '.count'
```

### decode

Decode tokens to audio.

```bash
text2speech decode <tokens_file> -o <output>
```

**Example:**
```bash
text2speech decode tokens.json -o output.wav
```

### status

Check service status.

```bash
text2speech status
```

Shows:
- API health
- GPU availability
- Loaded models
- Speaker count

### speakers

List available preset speakers.

```bash
text2speech speakers
```

### languages

List supported languages.

```bash
text2speech languages
```

## API Configuration

Default API: `https://mc.agaii.org/TTS/api/v1`

To use local backend, modify `text2speech_skill/cli.py`:
```python
API_BASE = "http://localhost:24536/api/v1"
```

## Voice Cloning Modes

### ICL Mode (In-Context Learning)
- Requires reference transcript (`--ref-text`)
- Higher quality, follows reference prosody
- Default mode when transcript provided

### X-Vector Mode
- Use `--x-vector-only` flag
- Faster, only speaker characteristics
- No transcript needed

## Tips

- Use `@file.txt` syntax to read text from file: `text2speech speak @input.txt -o out.wav`
- Reference audio should be clear and 5-30 seconds for best cloning
- ICL mode produces better results than x-vector when transcript is accurate
- Batch operations save a `batch_report.json` with results

## Troubleshooting

**Job fails with "ref_text required"**
→ Add `--ref-text` with transcript or use `--x-vector-only`

**Audio quality is poor**
→ Use clearer reference audio, or try different speaker/timbre

**Timeout on long text**
→ Break into smaller chunks, or use batch mode
