---
name: omnicaptions-translate
description: Use when translating captions/captions to another language. Supports bilingual output and context-aware translation. Default uses Claude native, Gemini API optional.
allowed-tools: Bash(omnicaptions:*), Read, Write, Glob
---

# Caption Translation

**Default: Claude native translation** (no API key needed)

Use Gemini API only when user explicitly requests it.

## Default Workflow (Claude)

1. Read the caption file
2. Translate using Claude's native ability
3. Write output with `_Claude_{lang}` suffix

## Gemini API (Optional)

Use CLI when user requests Gemini:

```bash
omnicaptions translate input.srt -l zh --bilingual
```

Output: `input_Gemini_zh.srt`

## When to Use

- Translate SRT/VTT/ASS to another language
- Generate bilingual captions (original + translation)
- Translate YouTube video transcripts
- Need context-aware translation (not line-by-line)

## When NOT to Use

- Need transcription (use `/omnicaptions:transcribe`)
- Just format conversion without translation (use `/omnicaptions:convert`)

## Setup

```bash
pip install https://github.com/lattifai/omni-captions-skills/raw/main/packages/lattifai_captions-0.1.0.tar.gz
pip install https://github.com/lattifai/omni-captions-skills/raw/main/packages/omnicaptions-0.1.0.tar.gz
```

## API Key

Priority: `GEMINI_API_KEY` env → `.env` file → `~/.config/omnicaptions/config.json`

If not set, ask user: `Please enter your Gemini API key (get from https://aistudio.google.com/apikey):`

Then run with `-k <key>`. Key will be saved to config file automatically.

## Context-Aware Translation

LLM-based translation is superior to traditional machine translation because it understands context across multiple lines:

### Why Context Matters

| Approach | Problem | Result |
|----------|---------|--------|
| Line-by-line | No context | Robotic, disconnected translations |
| **Batch + Context** | Sees surrounding lines | Natural, coherent dialogue |

### How It Works

```
┌─────────────────────────────────────────┐
│  Batch size: 30 lines                   │
│  Context: 5 lines before/after          │
├─────────────────────────────────────────┤
│  [5 previous lines] → context           │
│  [30 current lines] → translate         │
│  [5 next lines]     → preview           │
└─────────────────────────────────────────┘
```

Benefits:
- **Speaker continuity** - maintains character voice
- **Split sentences** - handles dialogue spanning multiple lines
- **Idioms & culture** - adapts cultural references naturally
- **Pronoun resolution** - correct he/she/they based on context

## Advanced Features

### Bilingual Output

```bash
# Original + Translation (for language learning)
omnicaptions translate input.srt -l zh --bilingual
```

Output example:
```srt
1
00:00:01,000 --> 00:00:03,500
Welcome to the show.
欢迎来到节目。

2
00:00:03,500 --> 00:00:06,000
Thank you for having me.
感谢邀请我。
```

### Custom Glossary (Coming Soon)

For domain-specific or branded content:

```bash
# Use glossary for consistent terminology
omnicaptions translate input.srt -l zh --glossary terms.json
```

Glossary format:
```json
{
  "API": "接口",
  "Token": "令牌",
  "Machine Learning": "机器学习"
}
```

Benefits:
- **Terminology consistency** - "one term, one translation"
- **Brand compliance** - use official product names
- **Domain accuracy** - medical, legal, technical terms

## Best Practices

### 1. Provide Context for Better Quality

For specialized content, use custom prompts:

```python
from omnicaptions import GeminiCaption

gc = GeminiCaption()
gc._translation_prompt = """
You are translating captions for a medical documentary.
Use formal Chinese medical terminology.
Glossary: {glossary}
"""
gc.translate("input.srt", "output.srt", "zh")
```

### 2. Choose the Right Model

| Model | Best For |
|-------|----------|
| `gemini-3-flash-preview` | Fast, everyday content |
| `gemini-3-pro-preview` | Complex, nuanced content |

### 3. Review Bilingual Output

Bilingual captions let viewers verify translation quality - ideal for:
- Language learners
- Quality assurance
- Accessibility

## CLI Usage

```bash
# Translate (auto-output to same directory)
omnicaptions translate input.srt -l zh         # → ./input_Gemini_zh.srt

# Specify output file or directory
omnicaptions translate input.srt -o output/ -l zh   # → output/input_Gemini_zh.srt
omnicaptions translate input.srt -o zh.srt -l zh    # → zh.srt

# Bilingual output (original + translation)
omnicaptions translate input.srt -l zh --bilingual

# Specify model
omnicaptions translate input.vtt -l ja -m gemini-3-pro-preview
```

| Option | Description |
|--------|-------------|
| `-k, --api-key` | Gemini API key (auto-prompted if missing) |
| `-o, --output` | Output file or directory (default: same dir as input) |
| `-l, --language` | Target language code (required) |
| `--bilingual` | Output both original and translation |
| `-m, --model` | Model name (default: gemini-3-flash-preview) |
| `-v, --verbose` | Verbose output |

## Language Codes

| Language | Code |
|----------|------|
| Chinese (Simplified) | `zh` |
| Chinese (Traditional) | `zh-TW` |
| Japanese | `ja` |
| Korean | `ko` |
| English | `en` |
| Spanish | `es` |
| French | `fr` |
| German | `de` |

## Supported Formats

All formats from `lattifai-captions`: SRT, VTT, ASS, TTML, JSON, Gemini MD, etc.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| No API key | Use `-k YOUR_KEY` or follow the prompt |
| Wrong language code | Use ISO codes: zh, ja, en, etc. |
| Lost formatting | ASS styles preserved; SRT basic only |
| Inconsistent terms | Use glossary for technical content |

## References

- [Caption LLM Translator](https://github.com/yigitkonur/caption-llm-translator) - Context window approach
- [Caption Translator](https://github.com/rockbenben/caption-translator) - Batch processing
- [Captions.Translate.Agent](https://github.com/captionsdog/Captions.Translate.Agent) - Multi-agent workflow

## Related Skills

| Skill | Use When |
|-------|----------|
| `/omnicaptions:transcribe` | Need transcript first |
| `/omnicaptions:LaiCut` | Align timing before translation |
| `/omnicaptions:convert` | Convert format after translation |
| `/omnicaptions:download` | Download captions to translate |

### Workflow Examples

**Important**: Generate bilingual captions AFTER LaiCut alignment.

**File naming convention** - preserve language tag and processing chain:
```
video.en.vtt → video.en_LaiCut.json → video.en_LaiCut.srt → video.en_LaiCut_Claude_zh.srt → video.en_LaiCut_Claude_zh_Color.ass
```

| 翻译方式 | 后缀 | 示例 |
|----------|------|------|
| Claude (默认) | `_Claude_zh` | `video.en_LaiCut_Claude_zh.srt` |
| Gemini API | `_Gemini_zh` | `video.en_LaiCut_Gemini_zh.srt` |

```bash
# 1. LaiCut 对齐 (保留词级时间)
omnicaptions LaiCut video.mp4 video.en.vtt
# → video.en_LaiCut.json

# 2. 转换为 SRT (翻译用，文件小)
omnicaptions convert video.en_LaiCut.json -o video.en_LaiCut.srt

# 3a. Claude 翻译 (默认)
# → video.en_LaiCut_Claude_zh.srt

# 3b. 或 Gemini 翻译
omnicaptions translate video.en_LaiCut.srt -l zh --bilingual
# → video.en_LaiCut_Gemini_zh.srt

# 4. 转换为带颜色的 ASS
omnicaptions convert video.en_LaiCut_Claude_zh.srt -o video.en_LaiCut_Claude_zh_Color.ass \
  --line1-color "#00FF00" --line2-color "#FFFF00"
```

### Large JSON Files

LaiCut outputs JSON with word-level timing. **For translation, convert to SRT first** (much smaller):

```bash
# JSON (word-level, ~150KB) → SRT (segment-level, ~15KB)
omnicaptions convert video.en_LaiCut.json -o video.en_LaiCut.srt
```

Why? JSON preserves word timing for karaoke, but translation only needs segment text. SRT is 10-20x smaller.

## Claude Translation Rules (Default)

1. **Preserve format exactly** - Keep all timing codes, formatting tags, style definitions
2. **Context-aware** - Consider surrounding lines for coherent dialogue
3. **Speaker consistency** - Maintain character voice and tone
4. **Cultural adaptation** - Adapt idioms and references naturally
5. **Large files** - Process in batches of 100 lines to maintain quality

## Claude vs Gemini

| Feature | Claude (Default) | Gemini API |
|---------|------------------|------------|
| API Key | None needed | Required |
| Invocation | Skill (Read/Write) | CLI command |
| Output suffix | `_Claude_{lang}` | `_Gemini_{lang}` |
| Best for | Most tasks | Large files, automation |
