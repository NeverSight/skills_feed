---
name: video-tool
description: |
  Video processing toolkit. Use when user wants to:
  - Download videos from YouTube or other sites
  - Remove silence from videos
  - Trim, cut, or extract segments from videos
  - Extract audio from video files
  - Enhance or denoise audio
  - Replace audio track in a video
  - Change video playback speed
  - Concatenate multiple videos
  - Generate transcripts/captions (VTT)
  - Generate video descriptions, timestamps, or context cards
  - Upload videos to YouTube or Bunny.net CDN
  - Get video metadata (duration, resolution, codec)
allowed-tools: Bash(which:*), Bash(curl:*), Bash(uv:*), Bash(video-tool:*), AskUserQuestion(*)
---

# Video Tool CLI

AI-powered video processing toolkit with ffmpeg operations, Whisper transcription, and content generation.

## Installation Status

video-tool: !`which video-tool > /dev/null && echo "INSTALLED" || echo "NOT INSTALLED - run installation below"`
uv: !`which uv > /dev/null && echo "INSTALLED" || echo "NOT INSTALLED"`

If video-tool is not installed, run the installation commands below before proceeding.

## Installation

```bash
# Install uv first (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install video-tool
uv tool install git+https://github.com/alejandro-ao/video-tool-cli.git
```

### Dependencies
- **ffmpeg**: Required for all video operations (`brew install ffmpeg` on macOS)
- **yt-dlp**: Required for video downloads (`brew install yt-dlp` on macOS)

### API Keys Setup

Configure API keys (choose one method):

**Option 1: Non-interactive (recommended for Claude Code)**
```bash
video-tool config keys --set groq_api_key=YOUR_KEY
video-tool config keys --set openai_api_key=YOUR_KEY
# Multiple at once:
video-tool config keys --set groq_api_key=xxx --set openai_api_key=yyy
```

**Option 2: Edit credentials file directly**
If users prefer not to share keys with Claude Code, they can edit directly:
```bash
# File: ~/.config/video-tool/credentials.yaml
openai_api_key: sk-xxx
groq_api_key: gsk_xxx
bunny_library_id: xxx
bunny_access_key: xxx
replicate_api_token: xxx
```

**Option 3: Interactive setup**
```bash
video-tool config keys
```

Required keys:
- **groq_api_key** - Transcription (Whisper)
- **openai_api_key** - Content generation (descriptions, timestamps)

Optional keys:
- **bunny_library_id**, **bunny_access_key** - Bunny.net CDN uploads
- **replicate_api_token** - Audio enhancement

```bash
video-tool config keys --show   # View configured keys (masked)
video-tool config keys --reset  # Clear all credentials
```

## IMPORTANT: Handling Authentication Errors

**When a command fails with "AUTHENTICATION REQUIRED" or "API key not configured":**

1. **DO NOT** try to work around the issue by writing custom scripts
2. **DO NOT** try to call APIs directly
3. **INSTEAD**, offer the user two options using AskUserQuestion:

**Option A: Provide key to Claude (convenient)**
- User gives you the API key directly
- You run: `video-tool config keys --set KEY_NAME=VALUE`
- Faster, but the key is visible in the conversation

**Option B: User configures privately (more secure)**
- User runs the command themselves or edits the file directly
- Key never appears in the conversation with Claude
- Tell user to run: `video-tool config keys` (interactive)
- Or edit: `~/.config/video-tool/credentials.yaml`

**Example AskUserQuestion prompt:**
"This command requires a [Groq/OpenAI] API key. How would you like to configure it?"
- Option 1: "I'll provide the key" - convenient but key visible to Claude
- Option 2: "I'll configure it myself" - more private, key stays hidden from Claude

After user configures (either way), retry the original command.

**Commands that require API keys:**
- `video-tool generate transcript` → Requires **Groq API key**
- `video-tool video timestamps -m transcript` → Requires **OpenAI API key** (structured output)
- `video-tool upload bunny-*` → Requires **Bunny.net credentials**
- `video-tool video enhance-audio` → Requires **Replicate API token**

---

## Content Generation: CLI Commands vs Direct Generation

Some CLI commands use OpenAI to generate content. When Claude runs this skill, it's often better for Claude to generate content directly instead of calling another LLM.

### Use CLI command (requires OpenAI API key):
- `video timestamps -m transcript` - Uses structured output for precise JSON

### Generate directly as Claude (no OpenAI needed):
For these tasks, read the transcript/timestamps and generate content using the linked templates:

- **Description**: See [templates/description.md](templates/description.md)
- **SEO Keywords**: See [templates/seo-keywords.md](templates/seo-keywords.md)
- **LinkedIn/Twitter Posts**: See [templates/social-posts.md](templates/social-posts.md)
- **Context Cards**: See [templates/context-cards.md](templates/context-cards.md)

### Note on CLI commands
The CLI has commands like `generate description`, `generate context-cards` that use OpenAI. These exist for manual CLI usage. If user explicitly requests a CLI command, honor the request (it may require OpenAI key). Otherwise, generate content directly.

---

## Output Location

Before generating files (transcripts, descriptions, timestamps, etc.), if not especified before, ask the user where to save them using AskUserQuestion.

**Example prompt:**
"Where should I save the output files?"
- Option 1: "Current directory" - save in `.` or `./output/`
- Option 2: "Same folder as video" - save alongside the source video
- Option 3: "I'll specify a path" - user provides custom location

**Default behavior if user doesn't specify:** Ask rather than assuming temp directory.

---

### YouTube Authentication

For YouTube uploads, run OAuth2 setup:
```bash
video-tool config youtube-auth
```

---

## Command Reference

### Video Processing

#### Download Video
Download from YouTube or other supported sites.
```bash
video-tool video download -u "URL" -o ./output -n "filename"
```
| Option | Description |
|--------|-------------|
| `-u, --url` | Video URL |
| `-o, --output-dir` | Output directory |
| `-n, --name` | Output filename (without extension) |

#### Get Video Info
Get metadata: duration, resolution, codec, bitrate.
```bash
video-tool video info -i video.mp4
```

#### Remove Silence
Remove silent segments from video.
```bash
video-tool video silence-removal -i input.mp4 -o output.mp4 -t 1.0
```
| Option | Description |
|--------|-------------|
| `-i, --input` | Input video |
| `-o, --output-path` | Output path |
| `-t, --threshold` | Min silence duration to remove (default: 1.0s) |

#### Trim Video
Cut from start and/or end of video.
```bash
video-tool video trim -i input.mp4 -o output.mp4 -s 00:00:10 -e 00:05:00
```
| Option | Description |
|--------|-------------|
| `-s, --start` | Start timestamp (HH:MM:SS, MM:SS, or seconds) |
| `-e, --end` | End timestamp |
| `-g, --gpu` | Use GPU acceleration |

#### Extract Segment
Keep only a specific portion of video.
```bash
video-tool video extract-segment -i input.mp4 -o output.mp4 -s 00:01:00 -e 00:02:30
```

#### Cut Segment
Remove a middle portion from video.
```bash
video-tool video cut -i input.mp4 -o output.mp4 -f 00:01:00 -t 00:02:00
```
| Option | Description |
|--------|-------------|
| `-f, --from` | Start of segment to remove |
| `-t, --to` | End of segment to remove |

#### Change Speed
Speed up or slow down video.
```bash
video-tool video speed -i input.mp4 -o output.mp4 -f 1.5
```
| Option | Description |
|--------|-------------|
| `-f, --factor` | Speed factor (0.25-4.0). 2.0=double, 0.5=half |
| `-p, --preserve-pitch` | Keep original audio pitch (default: yes) |

#### Concatenate Videos
Join multiple videos into one.
```bash
video-tool video concat -i ./clips/ -o ./output/final.mp4 -f
```
| Option | Description |
|--------|-------------|
| `-i, --input-dir` | Directory containing videos |
| `-o, --output-path` | Output file path |
| `-f, --fast-concat` | Skip re-encoding (faster, requires same codec) |

### Audio Operations

#### Extract Audio
Extract audio track to MP3.
```bash
video-tool video extract-audio -i video.mp4 -o audio.mp3
```

#### Enhance Audio
Improve audio quality using Resemble AI (requires Replicate API token).
```bash
video-tool video enhance-audio -i input.mp4 -o enhanced.mp4
video-tool video enhance-audio -i input.mp4 -o denoised.mp4 -d  # denoise only
```

#### Replace Audio
Swap audio track in a video.
```bash
video-tool video replace-audio -v video.mp4 -a new_audio.mp3 -o output.mp4
```

### Transcription & Timestamps

#### Generate Transcript
Create VTT captions using Groq Whisper (requires Groq API key).
```bash
video-tool generate transcript -i video.mp4 -o transcript.vtt
```

#### Generate Timestamps
Create chapter markers (requires OpenAI API key for transcript mode).
```bash
# From video clips directory
video-tool video timestamps -m clips -i ./clips/ -o timestamps.json

# From transcript
video-tool video timestamps -m transcript -i transcript.vtt -o timestamps.json -g medium
```
| Option | Description |
|--------|-------------|
| `-m, --mode` | `clips` or `transcript` |
| `-g, --granularity` | `low`, `medium`, `high` (transcript mode) |
| `-n, --notes` | Additional instructions for LLM |

### Uploads

#### YouTube Upload
Upload video as draft (requires OAuth2 auth via `video-tool config youtube-auth`).
```bash
video-tool upload youtube-video -i video.mp4 -t "Title" -d "Description" -p private
video-tool upload youtube-video -i video.mp4 --metadata-path metadata.json
```
| Option | Description |
|--------|-------------|
| `-t, --title` | Video title |
| `-d, --description` | Description text |
| `--description-file` | Read description from file |
| `--tags` | Comma-separated tags |
| `--tags-file` | Tags from file (one per line) |
| `-c, --category` | YouTube category ID (default: 27 Education) |
| `-p, --privacy` | `private` (draft) or `unlisted` only |
| `--thumbnail` | Thumbnail image path |

#### YouTube Metadata Update
Update existing video metadata.
```bash
video-tool upload youtube-metadata -v VIDEO_ID --description-file description.md
```

#### YouTube Transcript Upload
Add captions to YouTube video.
```bash
video-tool upload youtube-transcript -v VIDEO_ID -t transcript.vtt -l en
```

#### Bunny.net Uploads
Upload to Bunny.net CDN (requires Bunny credentials via `config keys`).
```bash
video-tool upload bunny-video -v video.mp4
video-tool upload bunny-transcript -v VIDEO_ID -t transcript.vtt
video-tool upload bunny-chapters -v VIDEO_ID -c timestamps.json
```

### Full Pipeline

Run complete workflow: concat → timestamps → transcript → content → optional upload.
```bash
video-tool pipeline -i ./clips/ -o ./output/ -t "Video Title" -y
```
| Option | Description |
|--------|-------------|
| `-f, --fast-concat` | Fast concatenation |
| `--timestamps-from-clips` | Generate timestamps from clip names |
| `-g, --granularity` | Timestamp detail level |
| `--upload-bunny` | Upload to Bunny.net after processing |
| `-y, --yes` | Non-interactive mode |

### Configuration

```bash
video-tool config keys                        # Configure API keys (interactive)
video-tool config keys --set KEY=VALUE        # Set key non-interactively
video-tool config keys --show                 # View configured keys
video-tool config llm                         # Configure LLM settings and persistent links
video-tool config youtube-auth                # Set up YouTube OAuth2
video-tool config youtube-status              # Check YouTube credentials
```

---

## Command Templates for Skills

Common tasks that other skills can reference by name.

### Transcribe Video
Generate VTT transcript from video/audio file.
```bash
video-tool generate transcript -i <INPUT_FILE> -o <OUTPUT_FILE>
```
**Inputs:**
- `<INPUT_FILE>`: Path to video or audio file
- `<OUTPUT_FILE>`: Path to output VTT file

**Requirements:** Groq API key

---

### Concatenate Videos
Join multiple video clips into single file.
```bash
video-tool video concat -i <INPUT_DIR> -o <OUTPUT_FILE> --fast-concat
```
**Inputs:**
- `<INPUT_DIR>`: Directory with numbered clips (01-*.mp4, 02-*.mp4, etc.)
- `<OUTPUT_FILE>`: Path to output video file
- `--fast-concat`: Skip reprocessing (optional, recommended for speed)

**Note:** Clips must be named with numeric prefixes for correct ordering.

---

### Generate Timestamps from Clips
Create chapter timestamps from clip filenames.
```bash
video-tool video timestamps --mode clips -i <INPUT_DIR> -o <OUTPUT_FILE>
```
**Inputs:**
- `<INPUT_DIR>`: Directory with numbered clips
- `<OUTPUT_FILE>`: Path to output JSON file

**Output Format:**
```json
{
  "timestamps": [
    {"time": "00:00:00", "title": "Introduction"},
    {"time": "00:05:30", "title": "Main Content"}
  ]
}
```

---

### Upload to YouTube
Upload video with metadata to YouTube.
```bash
video-tool upload youtube-video \
  -i <VIDEO_FILE> \
  -t "<TITLE>" \
  --description-file <DESCRIPTION_FILE> \
  --tags-file <TAGS_FILE> \
  --privacy <PRIVACY>
```
**Inputs:**
- `<VIDEO_FILE>`: Path to video file
- `<TITLE>`: Video title (quoted)
- `<DESCRIPTION_FILE>`: Path to markdown description file
- `<TAGS_FILE>`: Path to text file with tags (one per line)
- `<PRIVACY>`: `private`, `unlisted`, or `public`

**Requirements:** YouTube OAuth2 authentication (`video-tool config youtube-auth`)

**Output:** JSON with video_id and url (save to youtube-upload.json for publish skill)

---

## Common Workflows

See [workflows.md](workflows.md) for detailed examples.
