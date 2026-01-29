---
name: text-to-voice
description: Convert text to speech using Kyutai's Pocket TTS. Use when the user asks to "generate speech", "text to speech", "TTS", "convert text to audio", "voice synthesis", "generate voice", "read aloud", or "create audio from text". Supports voice cloning from audio samples and multiple pre-made voices (alba, marius, javert, jean, fantine, cosette, eponine, azelma).
license: MIT
metadata:
  contributor: Aaron Adetunmbi
  thanks: kyutai-labs
---

# Text-to-Voice with Kyutai Pocket TTS

Convert text to natural speech using Kyutai's Pocket TTS - a lightweight 100M parameter model that runs efficiently on CPU.

## Installation

```bash
pip install pocket-tts
# or use uvx to run without installing:
uvx pocket-tts generate
```

Requires Python 3.10+ and PyTorch 2.5+. GPU not required.

## CLI Usage

### Basic Generation

```bash
# Generate with defaults (saves to ./tts_output.wav)
uvx pocket-tts generate

# Specify text
pocket-tts generate --text "Hello, this is my message."

# Specify output file location
pocket-tts generate --text "Hello" --output-path ./audio/greeting.wav

# Full example with all common options
pocket-tts generate \
  --text "Welcome to the demo." \
  --voice alba \
  --output-path ./output/welcome.wav
```

### CLI Options

| Option | Default | Description |
|--------|---------|-------------|
| `--text` | "Hello world..." | Text to convert to speech |
| `--voice` | alba | Voice name, local file path, or HuggingFace URL |
| `--output-path` | `./tts_output.wav` | **Where to save the generated audio file** |
| `--temperature` | 0.7 | Generation temperature (higher = more expressive) |
| `--lsd-decode-steps` | 1 | Quality steps (higher = better quality, slower) |
| `--eos-threshold` | -4.0 | End detection threshold (lower = finish earlier) |
| `--frames-after-eos` | auto | Extra frames after end (each frame = 80ms) |
| `--device` | cpu | Device to use (cpu/cuda) |
| `-q, --quiet` | false | Disable logging output |

### Voice Selection (CLI)

```bash
# Use a pre-made voice by name
pocket-tts generate --voice alba --text "Hello"
pocket-tts generate --voice javert --text "Hello"

# Use a local audio file for voice cloning
pocket-tts generate --voice ./my_voice.wav --text "Hello"

# Use a voice from HuggingFace
pocket-tts generate --voice "hf://kyutai/tts-voices/alba-mackenna/merchant.wav" --text "Hello"
```

### Quality Tuning (CLI)

```bash
# Higher quality (more generation steps)
pocket-tts generate --lsd-decode-steps 5 --temperature 0.5 --output-path high_quality.wav

# More expressive/varied output
pocket-tts generate --temperature 1.0 --output-path expressive.wav

# Shorter output (finishes speaking earlier)
pocket-tts generate --eos-threshold -3.0 --output-path shorter.wav
```

### Local Web Server

For quick iteration with multiple voices/texts:

```bash
uvx pocket-tts serve
# Open http://localhost:8000
```

## Available Voices

Pre-made voices (use name directly with `--voice`):

| Voice | Gender | License | Description |
|-------|--------|---------|-------------|
| `alba` | Female | CC BY 4.0 | Casual voice |
| `marius` | Male | CC0 | Voice donation |
| `javert` | Male | CC0 | Voice donation |
| `jean` | Male | CC-NC | EARS dataset |
| `fantine` | Female | CC BY 4.0 | VCTK dataset |
| `cosette` | Female | CC-NC | Expresso dataset |
| `eponine` | Female | CC BY 4.0 | VCTK dataset |
| `azelma` | Female | CC BY 4.0 | VCTK dataset |

Full voice catalog: https://huggingface.co/kyutai/tts-voices

For detailed voice information, see [references/voices.md](references/voices.md).

## Voice Cloning

Clone any voice from an audio sample. For best results:
- Use clean audio (minimal background noise)
- 10+ seconds recommended
- Consider [Adobe Podcast Enhance](https://podcast.adobe.com/en/enhance) to clean samples

```bash
pocket-tts generate --voice ./my_recording.wav --text "Hello" --output-path cloned.wav
```

## Output Format

- Sample Rate: 24kHz
- Channels: Mono
- Format: 16-bit PCM WAV
- Default location: `./tts_output.wav`

## Python API

For programmatic use:

```python
from pocket_tts import TTSModel
import scipy.io.wavfile

tts_model = TTSModel.load_model()
voice_state = tts_model.get_state_for_audio_prompt("alba")
audio = tts_model.generate_audio(voice_state, "Hello world!")

# Save to specific location
scipy.io.wavfile.write("./audio/output.wav", tts_model.sample_rate, audio.numpy())
```

### TTSModel.load_model()

```python
model = TTSModel.load_model(
    variant="b6369a24",      # Model variant
    temp=0.7,                # Temperature (0.0-1.0)
    lsd_decode_steps=1,      # Generation steps
    noise_clamp=None,        # Max noise value
    eos_threshold=-4.0       # End-of-sequence threshold
)
```

### Voice State

```python
# Pre-made voice
voice_state = model.get_state_for_audio_prompt("alba")

# Local file
voice_state = model.get_state_for_audio_prompt("./my_voice.wav")

# HuggingFace
voice_state = model.get_state_for_audio_prompt("hf://kyutai/tts-voices/alba-mackenna/casual.wav")
```

### Generate Audio

```python
audio = model.generate_audio(voice_state, "Text to speak")
# Returns: torch.Tensor (1D)
```

### Streaming

```python
for chunk in model.generate_audio_stream(voice_state, "Long text..."):
    # Process each chunk as it's generated
    pass
```

### Properties

- `model.sample_rate` - 24000 Hz
- `model.device` - "cpu" or "cuda"

## Performance

- ~200ms latency to first audio chunk
- ~6x real-time on MacBook Air M4 CPU
- Uses only 2 CPU cores

## Limitations

- English only
- No built-in pause/silence control
