---
name: yt-transcript
description: Format YouTube transcripts into markdown artifacts using yt-dlp with author chapters and resilient fallback providers
---

You are using the **YouTube Transcript (yt-dlp) Formatting** skill.

Goal: produce a clean markdown transcript artifact in the established `youtube-transcripts` format.

## When To Use This Skill

Invoke this skill when the user requests:
- `/yt-transcript <URL>`
- `/yt-transcript <URL> output to <directory>`
- `/yt-transcript <URL> --no-chapters`
- Any request to generate or update a YouTube transcript artifact

## Core Contract

The script is the deterministic engine. The agent orchestrates:
- path selection
- explicit filename override requests (only when user asks)
- user confirmation
- result communication

The script handles extraction, fallback logic, formatting, and file writes.
The script also auto-generates canonical filenames when given a directory target.

## Runtime Requirements

Install dependencies into the same Python interpreter used to run the script.
Python 3.10+ is required.

- macOS/Linux:
```bash
python -m pip install "yt-dlp[default]"
```
- Windows:
```bash
py -m pip install "yt-dlp[default]"
```

Optional fallback dependencies:
- `youtube-transcript-api`
- `openai-whisper`
- `ffmpeg`

Example install:
```bash
python -m pip install youtube-transcript-api openai-whisper
```

If your default `python` is older, create a venv with Python 3.10+ first:
```bash
/opt/homebrew/bin/python3.13 -m venv .venv
.venv/bin/python -m pip install "yt-dlp[default]" youtube-transcript-api
```

## Workflow

### Step 1: Determine Output Path

- Parse the user request for output directory or filename hints.
- If no directory is specified, propose a `youtube-transcripts/` directory in the current workspace context.
- Build an absolute output path.

### Step 2: Let Script Generate Filename

Default behavior: pass an output directory and let the script generate:
`YYYY-MM-DD_identifier_topic-keywords.md`

Only pass an explicit `.md` file path when the user explicitly requests a custom filename.

### Step 3: Decide Extraction Flags

Default invocation is English subtitle-first.

Available flags:
- `--no-chapters`: force flat transcript body
- `--lang <code>`: preferred subtitle language (default `en`)
- `--proxy <url>`: global proxy for yt-dlp requests
- `--http-proxy <url>`: HTTP proxy override for transcript API fallback
- `--https-proxy <url>`: HTTPS proxy override for transcript API fallback
- `--cookies <file>`: Netscape-format cookie file for yt-dlp
- `--cookies-from-browser <spec>`: browser cookie import for yt-dlp
- `--yt-impersonate <client[:os]>`: yt-dlp impersonation target
- `--asr-fallback`: use Whisper fallback if subtitle providers fail
- `--asr-model <name>`: Whisper model (default `small`)
- `--no-artifact-on-failure`: fail hard instead of writing fallback artifact

### Step 4: Preview + Confirm

Before execution, show:
- output directory or explicit file path
- URL
- whether chapters are expected
- whether fallback flags will be used

Wait for user confirmation.

### Step 5: Invoke Script

Use absolute paths and quote arguments.

Linux/macOS example:
```bash
python "/full/path/to/yt-transcript/script" "https://www.youtube.com/watch?v=VIDEO_ID" "/full/path/to/youtube-transcripts"
```

Windows example:
```bash
py "C:\path\to\yt-transcript\script" "https://www.youtube.com/watch?v=VIDEO_ID" "C:\path\to\youtube-transcripts"
```

With fallbacks:
```bash
python "/full/path/to/yt-transcript/script" "URL" "/full/path/to/youtube-transcripts" --cookies-from-browser "chrome" --proxy "socks5://127.0.0.1:1080" --asr-fallback
```

### Step 6: Report Outcome

On success:
- confirm output path
- summarize whether transcript came from subtitles or fallback path

If fallback artifact was written (extraction failed but file created):
- tell user artifact exists
- summarize embedded extraction failure note
- suggest rerun flags if needed

## Output Format Expectations

The generated markdown artifact should follow this shape:
- `# <title>`
- `**Source:** ...`
- `**Speaker/Channel:** ...`
- `**Published:** ...`
- `**Duration:** ...`
- `**Type:** Video Transcript`
- `**Summary:** ...`
- `**Topics:** ...`
- optional `**Chapters:**` list
- `---`
- transcript body (chaptered when available unless `--no-chapters`)

## Error Handling Guidance

Common failures and responses:
- `yt-dlp` missing in active interpreter -> provide interpreter-specific install command
- JS runtime / `yt-dlp-ejs` messages -> recommend `yt-dlp[default]` + runtime install
- missing preferred language subtitles -> ensure `youtube-transcript-api` is installed, then rerun
- no subtitles from provider fallbacks -> rerun with `--asr-fallback`
- blocked/rate-limited requests -> rerun with proxy flags (`--proxy`, `--http-proxy`, `--https-proxy`)
- gated/auth-required access -> rerun with `--cookies` or `--cookies-from-browser`
- invalid URL -> ask user to verify URL format

## Important Notes

- Use the script as the source of truth for extraction and rendering.
- Do not manually parse VTT in the agent response flow.
- Always use absolute paths for invocation.
- Confirm with the user before running when path/flags are ambiguous.
