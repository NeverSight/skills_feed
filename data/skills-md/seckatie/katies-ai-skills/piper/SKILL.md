---
name: piper
description: Convert text to speech using Piper TTS. This skill is triggered when the user says things like "convert text to speech", "text to audio", "read this aloud", "create audio from text", "generate speech from text", "make an audio file from this text", or "use piper TTS".
---

# Piper Text-to-Speech Workflow

Convert text or markdown files to natural-sounding speech audio.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `input` | string | Yes | - | Path to input file (.md or .txt) or literal text |
| `output` | string | Yes | - | Path to output .wav file |
| `voice` | string | No | `en_US-amy-medium` | Voice model name (see Available Voices) |
| `speed` | float | No | `0.67` | Speech speed (0.5=slow, 0.67=1.5x, 1.0=normal, 1.5=fast) |
| `sentence_silence` | float | No | `0.3` | Seconds of silence between sentences |
| `volume` | float | No | `1.0` | Volume multiplier |

## Available Voices

Models are stored in `~/piper-voices/`. Each voice requires two files: `.onnx` and `.onnx.json`.

| Voice | Description |
|-------|-------------|
| `en_US-amy-medium` | US English female (installed) |

Download additional voices from: https://huggingface.co/rhasspy/piper-voices

## Workflow

### Step 1: Validate Input

Determine input type and validate:

```bash
# Check if input is a file
if [[ -f "$input" ]]; then
  input_type="file"
  extension="${input##*.}"
else
  input_type="text"
fi
```

**Constraints:**
- If file: must exist and be readable
- If markdown (.md): proceed to Step 2
- If text file (.txt) or literal text: skip to Step 3

### Step 2: Clean Markdown (if applicable)

For markdown files, clean formatting for TTS:

```bash
python3 /Users/katiemulliken/Documents/Projects/kmtools/piper/clean_obsidian_for_tts.py "$input" -o "${input%.md}_clean.txt" --stats
```

**Removes:**
- YAML frontmatter
- Markdown formatting (headers, bold, italic, links)
- Code blocks and inline code
- HTML tags and comments
- Emojis and special Unicode
- URLs

**Output:** Cleaned text file for Step 3

### Step 3: Generate Audio

Convert text to speech using Piper:

```bash
# From cleaned/text file
/Users/katiemulliken/.local/bin/piper \
  -m ~/piper-voices/${voice}.onnx \
  -i "$cleaned_input" \
  -f "$output" \
  --length-scale $speed \
  --sentence-silence $sentence_silence \
  --volume $volume

# From literal text
echo "$text" | /Users/katiemulliken/.local/bin/piper \
  -m ~/piper-voices/${voice}.onnx \
  -f "$output" \
  --length-scale $speed \
  --sentence-silence $sentence_silence \
  --volume $volume
```

### Step 4: Verify Output

Confirm successful generation:

```bash
# Check file exists and has content
if [[ -f "$output" && -s "$output" ]]; then
  echo "Audio generated: $output"
  # Get duration using ffprobe if available
  ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$output" 2>/dev/null
fi
```

### Step 5: Link Audio to Original

You should link the audio to the original input using the following syntax

```markdown
![[The Converted Audio File.wav]]
```

## Complete Examples

### Markdown to Audio (Default Settings)

```bash
# Step 1-2: Clean markdown
python3 /Users/katiemulliken/Documents/Projects/kmtools/piper/clean_obsidian_for_tts.py "article.md" -o "article_clean.txt" --stats

# Step 3: Generate audio
/Users/katiemulliken/.local/bin/piper \
  -m ~/piper-voices/en_US-amy-medium.onnx \
  -i "article_clean.txt" \
  -f "article.wav" \
  --length-scale 0.67 \
  --sentence-silence 0.3
```

### Text to Audio (One-liner)

```bash
echo "Hello, this is a test." | /Users/katiemulliken/.local/bin/piper \
  -m ~/piper-voices/en_US-amy-medium.onnx \
  -f "output.wav"
```

### Batch Process Directory

```bash
for file in *.md; do
  python3 /Users/katiemulliken/Documents/Projects/kmtools/piper/clean_obsidian_for_tts.py "$file" | \
    /Users/katiemulliken/.local/bin/piper \
      -m ~/piper-voices/en_US-amy-medium.onnx \
      -f "${file%.md}.wav" \
      --length-scale 0.67 \
      --sentence-silence 0.3
done
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `command not found: piper` | piper not in PATH | Use full path: `/Users/katiemulliken/.local/bin/piper` |
| `Model file not found` | Missing .onnx file | Verify voice exists in `~/piper-voices/` |
| `Config file not found` | Missing .onnx.json | Download matching config file |
| `Input file not found` | Invalid input path | Check file path exists |

## Adding Voices

```bash
cd ~/piper-voices
# Download model and config (example: lessac voice)
curl -L "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx" -o en_US-lessac-medium.onnx
curl -L "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json" -o en_US-lessac-medium.onnx.json
```

Preview voices: https://rhasspy.github.io/piper-samples/
