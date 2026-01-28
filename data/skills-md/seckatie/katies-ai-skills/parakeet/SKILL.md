---
name: parakeet
description: Convert audio files to text using parakeet-mlx, NVIDIA's Parakeet automatic speech recognition model optimized for Apple's MLX framework. Run via uvx for on-device speech-to-text processing with high-quality timestamped transcriptions. Ideal for podcasts, interviews, meetings, and other audio content. This skill is triggered when the user says things like "transcribe this audio", "convert audio to text", "transcribe this podcast", "get text from this recording", "speech to text", or "transcribe this wav/mp3/m4a file".
---

# Parakeet-MLX Audio Transcription

This skill provides instructions for using parakeet-mlx to convert audio files to text using NVIDIA's Parakeet automatic speech recognition model optimized for Apple's MLX framework.

## Overview

Parakeet-MLX brings NVIDIA's Parakeet ASR model to Apple Silicon, enabling fast, high-quality on-device speech-to-text conversion similar to Whisper but optimized for Apple's MLX framework.

**Key Features:**
- High-quality transcription with timestamps
- Fast processing (e.g., 1+ hour audio in ~53 seconds)
- On-device processing (no cloud API required)
- Output in SRT subtitle format
- No installation required - run directly with `uvx`

## Basic Usage

### Transcribe an Audio File

The simplest way to transcribe an audio file is:

```bash
uvx parakeet-mlx /path/to/audio/file.mp3
```

This will:
1. Download the model on first run (~2.5GB)
2. Process the audio file
3. Generate an SRT subtitle file with timestamped transcription

**Example:**

```bash
# Transcribe a podcast episode
uvx parakeet-mlx podcast_episode.mp3

# Transcribe an interview
uvx parakeet-mlx interview.wav

# Transcribe a meeting recording
uvx parakeet-mlx meeting_recording.m4a
```

## Important Notes

### First Run

**The first time you run parakeet-mlx, it will download a ~2.5GB model file.** This may take several minutes depending on your internet connection. Subsequent runs will use the cached model and start immediately.

### Performance

Parakeet-MLX is optimized for Apple Silicon and provides excellent performance:
- A 65MB, 1 hour 1 minute 28 second podcast was transcribed in 53 seconds
- Performance scales with audio duration, not file size
- Processing happens entirely on-device

### Output Format

The tool generates an **SRT (SubRip Subtitle)** file with the same name as your input file:

**Input:** `podcast.mp3`
**Output:** `podcast.srt`

The SRT format includes:
- Sequential subtitle numbers
- Timestamp ranges (start --> end)
- Transcribed text for each segment

**Example SRT output:**
```
1
00:00:00,000 --> 00:00:03,500
Welcome to the podcast. Today we're discussing...

2
00:00:03,500 --> 00:00:08,200
The latest developments in machine learning...
```

### Supported Audio Formats

While the documentation explicitly mentions MP3, parakeet-mlx likely supports common audio formats including:
- MP3
- WAV
- M4A
- FLAC
- OGG

If you encounter format issues, consider converting your audio file to MP3 or WAV first using tools like `ffmpeg`.

## Working with Output

### View the Transcription

```bash
# View the entire transcription
cat output.srt

# View just the text (remove timestamps)
grep -v "^[0-9]*$" output.srt | grep -v "^[0-9][0-9]:[0-9][0-9]:[0-9][0-9]"
```

### Convert SRT to Plain Text

If you need plain text without timestamps:

```bash
# Extract only dialogue lines (skip numbers and timestamps)
awk 'NF && !/^[0-9]+$/ && !/^[0-9]{2}:[0-9]{2}:[0-9]{2}/' output.srt > transcript.txt
```

### Use with Other Tools

The SRT format is widely supported and can be:
- Imported into video editing software
- Used with subtitle players
- Converted to other formats (VTT, ASS, etc.)
- Processed with text analysis tools

## Common Workflows

### Transcribe Multiple Files

```bash
# Process all MP3 files in a directory
for file in *.mp3; do
    echo "Processing $file..."
    uvx parakeet-mlx "$file"
done
```

### Transcribe and Extract Text

```bash
# Transcribe and immediately extract plain text
uvx parakeet-mlx audio.mp3
awk 'NF && !/^[0-9]+$/ && !/^[0-9]{2}:[0-9]{2}:[0-9]{2}/' audio.srt > audio.txt
```

### Check Transcription Quality

After transcription, review the SRT file to verify:
- Proper segmentation of speech
- Accurate timestamps
- Text quality and accuracy

## Troubleshooting

### Model Download Issues

If the model download fails or is interrupted:
1. Check your internet connection
2. Ensure you have ~2.5GB of free disk space
3. Try running the command again (it may resume download)

### Performance Issues

If transcription is slow:
- Ensure you're running on Apple Silicon (M1/M2/M3)
- Close other resource-intensive applications
- For very long files, consider splitting them into smaller segments

### Audio Format Not Supported

If you get an error about unsupported format:

```bash
# Convert to MP3 using ffmpeg
ffmpeg -i input.m4a -acodec libmp3lame -ab 192k output.mp3
uvx parakeet-mlx output.mp3
```

## Use Cases

Parakeet-MLX is ideal for:
- **Podcast transcription** - Generate searchable text from episodes
- **Interview documentation** - Convert recorded interviews to text
- **Meeting notes** - Transcribe meeting recordings for reference
- **Content creation** - Generate captions or show notes
- **Accessibility** - Create subtitles for audio/video content
- **Research** - Analyze spoken content at scale

## Advantages Over Other Tools

**vs. Whisper:**
- Optimized specifically for Apple MLX framework
- Potentially faster on Apple Silicon
- Similar quality output

**vs. Cloud APIs:**
- No API costs
- Complete privacy (on-device processing)
- No internet required after model download
- No file size limits

**vs. Manual Transcription:**
- Dramatically faster (hours to minutes)
- Consistent quality
- Includes precise timestamps

## Tips for Best Results

1. **Audio Quality Matters**: Clear audio with minimal background noise produces better results
2. **Speaker Clarity**: Single speaker or well-separated multi-speaker audio works best
3. **Review Output**: Always review the transcription for accuracy, especially for technical terms or names
4. **Use Timestamps**: The SRT format's timestamps are valuable for referencing specific moments
5. **Batch Processing**: Process multiple files in sequence for efficiency

## References

- [Simon Willison's parakeet-mlx article](https://simonwillison.net/2025/Nov/14/parakeet-mlx/)
- Run `uvx parakeet-mlx --help` for command-line options (if available)

## Notes

- Parakeet-MLX runs entirely on-device, ensuring privacy
- The tool is designed for Apple Silicon; performance on Intel Macs may vary
- First run requires internet for model download
- Output quality is reported as "very high" for clear audio
- The tool is optimized for speech recognition, not music or other audio types
