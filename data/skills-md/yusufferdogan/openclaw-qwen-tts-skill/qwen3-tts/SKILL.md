---
name: qwen3-tts
description: Generate multilingual CustomVoice samples and one-off voice replies with Qwen3‑TTS (no Remotion). Includes local setup (Conda Py3.12) and simple CLI scripts.
---

# Qwen3‑TTS Skill (TTS‑only)

This skill provides:
- Python 3.12 Conda env + qwen-tts install
- Batch audio generation from sample text
- One-off voice replies from arbitrary text (returns WAV path)
- Toggle for auto voice replies

No Remotion/video rendering is included in this skill.

## Prereqs
- macOS with Homebrew
- Conda/Miniforge (auto-installed if missing)
- FFmpeg (system)

## Quick Start
```bash
# 1) Prepare env (Conda + Python 3.12)
bash scripts/setup-python.sh

# 2) Generate audio samples
TEXT="This is a voice test." bash scripts/generate-audio.sh

# Outputs WAV files under clawd/tmp/qwen_samples/
```

## One-off voice reply
```bash
TEXT="Your message here" SPEAKER=Ryan LANG=English bash scripts/voice-reply.sh
# -> prints /Users/yusuf/clawd/tmp/qwen_voice/voice-<ts>.wav
```

Toggle auto-voice replies:
```bash
bash scripts/enable-voice-replies.sh
bash scripts/disable-voice-replies.sh
# Wrapper respecting the toggle:
bash scripts/reply-or-voice.sh "Your message" Ryan English
```

## Notes
- For higher quality or cloning, switch models in scripts/generate-audio.py
- CPU works but GPU is faster
