# /fal-generate

Universal AI media generation - generates images, videos, audio, music, and more.

## Instructions

Analyze the user's request and determine what they want to generate. Claude Code should understand the intent directly and call the appropriate `fal_api.py` command.

### Prerequisites

Before executing any generation, verify the API key is configured:

```bash
if [ ! -f ~/.config/fal-skill/.env ]; then
  echo "❌ API key not configured. Please run /fal-setup first."
  exit 1
fi
```

### Intent Classification

| Intent | Triggers (examples) | Command |
|--------|---------------------|---------|
| **Image Generation** | Default; "画", "生成图片", "create image", "draw" | `generate` |
| **Video Generation** | "视频", "video", "animate", "动画", "clip" | `video` |
| **Image-to-Video** | Has image + "变成视频", "animate this", "make it move" | `video --image-url` |
| **Background Removal** | "去背景", "抠图", "remove bg", "transparent", "cutout" | Use `/fal-remove-bg` |
| **TTS** | "朗读", "说", "speak", "voice", "tts", "read aloud" | `tts` |
| **Music** | "音乐", "music", "歌曲", "song", "bgm", "soundtrack" | `music` |
| **Sound Effects** | "音效", "sound effect", "sfx" | `music` (cassetteai model) |
| **Avatar/Lipsync** | "口型", "avatar", "lipsync", "talking head" | `avatar` |
| **Transcribe** | "转文字", "transcribe", "听写", "speech to text" | `transcribe` |
| **Upscale** | "放大", "upscale", "enhance", "超分", "2x/4x/8x" | `upscale` |
| **Photo Edit** | "调色", "打光", "colorize", "relight", "reseason" | `edit` |

### Intent Priority (Conflict Resolution)

When a request matches multiple intents, use this priority order:

1. **Upscale** - If explicit scale keywords (2x, 4x, 8x, upscale, 放大, 超分)
2. **Background Removal** - If "background", "去背景", "抠图", "transparent"
3. **Transcribe** - If "transcribe", "转文字", "听写" with audio file
4. **Avatar** - If "avatar", "lipsync", "口型" with image+audio
5. **TTS** - If "speak", "朗读", "tts", "voice" (speech output)
6. **Music/SFX** - If "music", "音乐", "sfx", "音效" (no video context)
7. **Video** - If "video", "视频", "animate", "动画"
8. **Photo Edit** - If editing keywords with existing image (colorize, relight, reseason)
9. **Image Generation** - Default fallback for creative prompts

### Ambiguous Cases

| Request | Correct Intent | Reasoning |
|---------|---------------|-----------|
| "remove the person from photo.jpg" | Photo Edit (remove-object) | "remove" + object subject = object removal |
| "remove background from photo.jpg" | Background Removal | "background" keyword = bg removal |
| "make the image larger" | Upscale | "larger" without creative context = upscale |
| "create a larger castle image" | Image Generation | "larger" in creative context = image gen |
| "music video of a band" | Video Generation | "video" takes precedence over "music" |
| "generate music for my video" | Music Generation | "music" is the output, video is context |
| "enhance photo.jpg" | Upscale | "enhance" alone = quality improvement |
| "enhance the colors in photo.jpg" | Photo Edit (colorize) | "colors" specifies editing operation |

### Parameter Extraction

Extract these parameters from the user's request:

**Video parameters:**
- Duration: "短视频" → 5, "长一点" → 10, "10秒/10 seconds" → 10
- Aspect ratio: "手机看/vertical/portrait/tiktok" → 9:16, "横屏/widescreen" → 16:9, "方形/square" → 1:1

**Image parameters:**
- Size: "竖版/portrait" → portrait_16_9, "横版/landscape" → landscape_16_9, default → square_hd
- Quality: "快速/fast" → fewer steps, "精细/detailed" → more steps

**Upscale parameters:**
- Scale: "2倍/2x" → 2, "4倍/4x" → 4, "8倍/8x" → 8 (default: 2)

### Default Models

| Task | Model |
|------|-------|
| Image Generation | `fal-ai/flux.2/dev` |
| Text-to-Video | `fal-ai/kling-video/v2/standard/text-to-video` |
| Image-to-Video | `fal-ai/kling-video/v2/standard/image-to-video` |
| TTS | `fal-ai/kokoro/american-english` |
| Music | `fal-ai/minimax-music/v2` |
| Sound Effects | `cassetteai/sound-effects-generator` |
| Avatar | `fal-ai/kling-video/ai-avatar/v2/standard` |
| Transcribe | `fal-ai/elevenlabs/speech-to-text/scribe-v2` |
| Upscale (Image) | `fal-ai/crystal/upscale` |
| Photo Colorize | `fal-ai/fibo-edit/colorize` |
| Photo Relight | `fal-ai/fibo-edit/relight` |
| Photo Reseason | `fal-ai/fibo-edit/reseason` |
| Photo Restyle | `fal-ai/fibo-edit/restyle` |

### Execution

The skill directory is at: `~/.claude/skills/fal-ai/fal-ai`

Run commands using `uv`:

```bash
cd ~/.claude/skills/fal-ai/fal-ai && uv run python scripts/fal_api.py <command> [options]
```

### File/URL Handling

- If user provides a local file path, first upload it: `uv run python scripts/upload_image.py <path>`
- Use the returned URL as `--image-url`, `--video-url`, or `--audio-url`
- If user says "这张图", "this image", etc., use the most recently generated/mentioned file

## Examples

### Image Generation

User: "帮我画一只猫"
```bash
cd ~/.claude/skills/fal-ai/fal-ai && uv run python scripts/fal_api.py generate \
  --model fal-ai/flux.2/dev \
  --prompt "a cat"
```

User: "a portrait of a warrior in high quality"
```bash
cd ~/.claude/skills/fal-ai/fal-ai && uv run python scripts/fal_api.py generate \
  --model fal-ai/flux.2/dev \
  --prompt "a portrait of a warrior" \
  --size portrait_16_9 \
  --steps 50
```

### Video Generation

User: "生成一个海浪的视频"
```bash
cd ~/.claude/skills/fal-ai/fal-ai && uv run python scripts/fal_api.py video \
  --model fal-ai/kling-video/v2/standard/text-to-video \
  --prompt "ocean waves crashing on beach" \
  --duration 5 \
  --aspect-ratio 16:9
```

User: "适合手机看的短视频，一只猫在跳舞"
```bash
cd ~/.claude/skills/fal-ai/fal-ai && uv run python scripts/fal_api.py video \
  --model fal-ai/kling-video/v2/standard/text-to-video \
  --prompt "a cat dancing" \
  --duration 5 \
  --aspect-ratio 9:16
```

### Image-to-Video

User: "把这张图变成视频 cat.jpg"
```bash
# First upload the image
cd ~/.claude/skills/fal-ai/fal-ai && uv run python scripts/upload_image.py cat.jpg
# Then generate video (use returned URL)
cd ~/.claude/skills/fal-ai/fal-ai && uv run python scripts/fal_api.py video \
  --model fal-ai/kling-video/v2/standard/image-to-video \
  --image-url <uploaded_url> \
  --prompt "the cat starts walking" \
  --duration 5
```

### Text-to-Speech

User: "朗读这段话：今天天气真好"
```bash
cd ~/.claude/skills/fal-ai/fal-ai && uv run python scripts/fal_api.py tts \
  --model fal-ai/kokoro/american-english \
  --text "今天天气真好"
```

User: "speak this in a warm voice: Hello world"
```bash
cd ~/.claude/skills/fal-ai/fal-ai && uv run python scripts/fal_api.py tts \
  --model fal-ai/kokoro/american-english \
  --text "Hello world" \
  --voice af_heart
```

### Music Generation

User: "生成一段轻松的背景音乐"
```bash
cd ~/.claude/skills/fal-ai/fal-ai && uv run python scripts/fal_api.py music \
  --model fal-ai/minimax-music/v2 \
  --prompt "relaxing background music, ambient, calm" \
  --duration 30
```

User: "explosion sound effect"
```bash
cd ~/.claude/skills/fal-ai/fal-ai && uv run python scripts/fal_api.py music \
  --model cassetteai/sound-effects-generator \
  --prompt "explosion, cinematic"
```

### Avatar / Lipsync

User: "用这张照片和音频做口型同步 portrait.jpg audio.mp3"
```bash
# Upload both files first
cd ~/.claude/skills/fal-ai/fal-ai && uv run python scripts/upload_image.py portrait.jpg
cd ~/.claude/skills/fal-ai/fal-ai && uv run python scripts/upload_image.py audio.mp3
# Then create avatar
cd ~/.claude/skills/fal-ai/fal-ai && uv run python scripts/fal_api.py avatar \
  --model fal-ai/kling-video/ai-avatar/v2/standard \
  --image-url <portrait_url> \
  --audio-url <audio_url>
```

### Transcription

User: "把这段音频转成文字 meeting.mp3"
```bash
# Upload audio first
cd ~/.claude/skills/fal-ai/fal-ai && uv run python scripts/upload_image.py meeting.mp3
# Then transcribe
cd ~/.claude/skills/fal-ai/fal-ai && uv run python scripts/fal_api.py transcribe \
  --model fal-ai/elevenlabs/speech-to-text/scribe-v2 \
  --audio-url <uploaded_url>
```

### Upscale

User: "放大这张图4倍 img.png"
```bash
cd ~/.claude/skills/fal-ai/fal-ai && uv run python scripts/upload_image.py img.png
cd ~/.claude/skills/fal-ai/fal-ai && uv run python scripts/fal_api.py upscale \
  --model fal-ai/crystal/upscale \
  --image-url <uploaded_url> \
  --scale 4
```

### Photo Editing

User: "让照片更温暖 photo.jpg"
```bash
cd ~/.claude/skills/fal-ai/fal-ai && uv run python scripts/upload_image.py photo.jpg
cd ~/.claude/skills/fal-ai/fal-ai && uv run python scripts/fal_api.py edit \
  --model fal-ai/fibo-edit/relight \
  --image-url <uploaded_url> \
  --light-type "sunrise light"
```

User: "把这张照片变成冬天的场景 landscape.jpg"
```bash
cd ~/.claude/skills/fal-ai/fal-ai && uv run python scripts/upload_image.py landscape.jpg
cd ~/.claude/skills/fal-ai/fal-ai && uv run python scripts/fal_api.py edit \
  --model fal-ai/fibo-edit/reseason \
  --image-url <uploaded_url> \
  --season winter
```

User: "colorize this old photo vintage.jpg"
```bash
cd ~/.claude/skills/fal-ai/fal-ai && uv run python scripts/upload_image.py vintage.jpg
cd ~/.claude/skills/fal-ai/fal-ai && uv run python scripts/fal_api.py edit \
  --model fal-ai/fibo-edit/colorize \
  --image-url <uploaded_url> \
  --color "contemporary color"
```

## Error Handling

If a command fails:
1. Check if the API key is configured: `~/.config/fal-skill/.env`
2. Check if the file exists and is accessible
3. Report the error message to the user
4. Suggest alternatives or corrections

## Related Skills

- `/fal-remove-bg` - Background removal (specialized)
- `/fal-generate-video` - Video generation (specialized)
- `/fal-setup` - Configure API key
