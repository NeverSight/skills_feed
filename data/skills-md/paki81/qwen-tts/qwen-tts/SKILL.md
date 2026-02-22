---
name: qwen-tts
description: Local text-to-speech using Qwen3-TTS-12Hz-1.7B-CustomVoice. Use when generating audio from text, creating voice messages, or when TTS is requested. Supports 10 languages including Italian, 9 premium speaker voices, and instruction-based voice control (emotion, tone, style). Alternative to cloud-based TTS services like ElevenLabs. Runs entirely offline after initial model download.
---

# Qwen TTS

Local text-to-speech using Hugging Face's Qwen3-TTS-12Hz-1.7B-CustomVoice model.

## Quick Start

Generate speech from text:

```bash
scripts/tts.py "Ciao, come va?" -l Italian -o output.wav
```

With voice instruction (emotion/style):

```bash
scripts/tts.py "Sono felice!" -i "Parla con entusiasmo" -l Italian -o happy.wav
```

Different speaker:

```bash
scripts/tts.py "Hello world" -s Ryan -l English -o hello.wav
```

## Installation

**First-time setup** (one-time):

```bash
cd skills/public/qwen-tts
bash scripts/setup.sh
```

This creates a local virtual environment and installs `qwen-tts` package (~500MB).

**Note:** First synthesis downloads ~1.7GB model from Hugging Face automatically.

## Usage

```bash
scripts/tts.py [options] "Text to speak"
```

### Options

- `-o, --output PATH` - Output file path (default: qwen_output.wav)
- `-s, --speaker NAME` - Speaker voice (default: Vivian)
- `-l, --language LANG` - Language (default: Auto)
- `-i, --instruct TEXT` - Voice instruction (emotion, style, tone)
- `--list-speakers` - Show available speakers
- `--model NAME` - Model name (default: CustomVoice 1.7B)

### Examples

**Basic Italian speech:**
```bash
scripts/tts.py "Benvenuto nel futuro del text-to-speech" -l Italian -o welcome.wav
```

**With emotion/instruction:**
```bash
scripts/tts.py "Sono molto felice di vederti!" -i "Parla con entusiasmo e gioia" -l Italian -o happy.wav
```

**Different speaker:**
```bash
scripts/tts.py "Hello, nice to meet you" -s Ryan -l English -o ryan.wav
```

**List available speakers:**
```bash
scripts/tts.py --list-speakers
```

## Available Speakers

The CustomVoice model includes 9 premium voices:

| Speaker | Language | Description |
|---------|----------|-------------|
| Vivian | Chinese | Bright, slightly edgy young female |
| Serena | Chinese | Warm, gentle young female |
| Uncle_Fu | Chinese | Seasoned male, low mellow timbre |
| Dylan | Chinese (Beijing) | Youthful Beijing male, clear |
| Eric | Chinese (Sichuan) | Lively Chengdu male, husky |
| Ryan | English | Dynamic male, rhythmic |
| Aiden | English | Sunny American male |
| Ono_Anna | Japanese | Playful female, light nimble |
| Sohee | Korean | Warm female, rich emotion |

**Recommendation:** Use each speaker's native language for best quality, though all speakers support all 10 languages (Chinese, English, Japanese, Korean, German, French, Russian, Portuguese, Spanish, Italian).

## Voice Instructions

Use `-i, --instruct` to control emotion, tone, and style:

**Italian examples:**
- `"Parla con entusiasmo"`
- `"Tono serio e professionale"`
- `"Voce calma e rilassante"`
- `"Leggi come un narratore"`

**English examples:**
- `"Speak with excitement"`
- `"Very happy and energetic"`
- `"Calm and soothing voice"`
- `"Read like a narrator"`

## Integration with OpenClaw

The script outputs the audio file path to stdout (last line), making it compatible with OpenClaw's TTS workflow:

```bash
# OpenClaw captures the output path
cd skills/public/qwen-tts
OUTPUT=$(scripts/tts.py "Ciao" -s Vivian -l Italian -o /tmp/audio.wav 2>/dev/null)
# OUTPUT = /tmp/audio.wav
```

## Performance

- **GPU (CUDA):** ~1-3 seconds for short phrases
- **CPU:** ~10-30 seconds for short phrases  
- **Model size:** ~1.7GB (auto-downloads on first run)
- **Venv size:** ~500MB (installed dependencies)

## Troubleshooting

**Setup fails:**
```bash
# Ensure Python 3.10-3.12 is available
python3.12 --version

# Re-run setup
cd skills/public/qwen-tts
rm -rf venv
bash scripts/setup.sh
```

**Model download slow/fails:**
```bash
# Use mirror (China mainland)
export HF_ENDPOINT=https://hf-mirror.com
scripts/tts.py "Test" -o test.wav
```

**Out of memory (GPU):**
The model automatically falls back to CPU if GPU memory insufficient.

**Audio quality issues:**
- Try different speaker: `--list-speakers`
- Add instruction: `-i "Speak clearly and slowly"`
- Check language matches text: `-l Italian` for Italian text

## Model Details

- **Model:** Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice
- **Source:** Hugging Face (https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice)
- **License:** Check model card for current license terms
- **Sample Rate:** 16kHz
- **Output Format:** WAV (uncompressed)
