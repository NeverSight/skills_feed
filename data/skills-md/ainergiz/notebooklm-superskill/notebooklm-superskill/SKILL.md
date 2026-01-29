---
name: notebooklm-superskill
description: Generate slide decks, audio podcasts, infographics, and video overviews from NotebookLM notebooks. Customizable by audience, format, language (80+), orientation, and visual themes. Use when asked to generate slides, create podcast, make infographic, video overview, or automate NotebookLM content creation.
allowed-tools: Bash, Read, Glob, Grep
---

# NotebookLM SuperSkill

Generate professional content from NotebookLM notebooks: slides, podcasts, infographics, and videos.

## When to Use This Skill

Use this skill when the user wants to:
- Generate slide decks for different audiences (technical, investor, customer, executive, beginner)
- Create AI podcast-style audio overviews
- Make visual infographics from research
- Generate video overviews/explainers
- Automate NotebookLM content creation

## Critical: Always Use run.py Wrapper

All scripts MUST be run through `run.py` to ensure proper virtual environment setup:

```bash
python scripts/run.py <script_name> [args...]
```

## Authentication (One-Time Setup)

Before first use, authenticate with Google:

```bash
# Interactive login (browser opens)
python scripts/run.py auth_manager.py setup

# Check status
python scripts/run.py auth_manager.py status

# Validate credentials work
python scripts/run.py auth_manager.py validate
```

## Quick Reference

### 1. Slide Decks

Generate presentation slides with audience-specific customization.

```bash
# Single slide deck
python scripts/run.py generate_slides.py \
  --notebook-url "https://notebooklm.google.com/notebook/..." \
  --audience technical \
  --format detailed \
  --length default

# Multiple audiences at once
python scripts/run.py generate_slides.py \
  --notebook-url URL \
  --audiences technical,investor,customer
```

**Options:**
| Option | Values | Description |
|--------|--------|-------------|
| `--audience` | technical, investor, customer, executive, beginner | Target audience |
| `--audiences` | comma-separated | Generate multiple decks |
| `--format` | detailed, presenter | Slide format |
| `--length` | short, default, long | Slide count |
| `--source` | path | Upload source file first |
| `--prompt` | text | Custom prompt (overrides audience) |

### 2. Audio Overviews (Podcasts)

Generate AI podcast-style deep dive discussions.

```bash
python scripts/run.py generate_audio.py \
  --notebook-url URL \
  --format deep-dive \
  --language en-US
```

**Options:**
| Option | Values | Description |
|--------|--------|-------------|
| `--format` | deep-dive, brief, critique, debate | Podcast style |
| `--language` | en-US, es-ES, fr-FR, de-DE, ja-JP, etc. | 80+ languages |
| `--prompt` | text | Custom instructions |

**Note:** Audio generation takes 5-10 minutes.

### 3. Infographics

Generate visual infographics for different platforms.

```bash
python scripts/run.py generate_infographic.py \
  --notebook-url URL \
  --orientation landscape \
  --detail standard
```

**Options:**
| Option | Values | Description |
|--------|--------|-------------|
| `--orientation` | square, portrait, landscape | Aspect ratio |
| `--detail` | concise, standard, detailed | Information density |
| `--prompt` | text | Custom instructions |

**Orientations:**
- `square` - 1:1 for social media posts
- `portrait` - 9:16 for Instagram Stories, TikTok
- `landscape` - 16:9 for LinkedIn, presentations

### 4. Video Overviews

Generate video explainers with visual themes.

```bash
python scripts/run.py generate_video.py \
  --notebook-url URL \
  --format explainer \
  --theme futuristic
```

**Options:**
| Option | Values | Description |
|--------|--------|-------------|
| `--format` | brief, explainer | Video length |
| `--theme` | retro-90s, futuristic, corporate, minimal | Visual style |
| `--custom-theme` | text | Custom theme description |
| `--prompt` | text | Custom instructions |

**Note:** Video generation takes 10-15 minutes.

## Decision Flow

1. **User wants slides?** → Use `generate_slides.py`
   - Multiple audiences? Use `--audiences` flag
   - Single audience? Use `--audience` flag

2. **User wants podcast/audio?** → Use `generate_audio.py`
   - Non-English? Specify `--language`
   - Quick summary? Use `--format brief`

3. **User wants visual summary?** → Use `generate_infographic.py`
   - Social media? Consider `--orientation portrait`
   - Presentation? Use `--orientation landscape`

4. **User wants video?** → Use `generate_video.py`
   - Quick overview? Use `--format brief`
   - Training material? Use `--format explainer`

## Common Options

All scripts support:
- `--output DIR` - Output directory (default: current)
- `--headless` - Run without visible browser
- `--help` - Show detailed help

## Example Workflows

### Investor Pitch Materials
```bash
# Generate investor slides
python scripts/run.py generate_slides.py --notebook-url URL --audience investor

# Create brief overview podcast
python scripts/run.py generate_audio.py --notebook-url URL --format brief

# Make landscape infographic for deck
python scripts/run.py generate_infographic.py --notebook-url URL --orientation landscape
```

### Training Content
```bash
# Beginner-friendly slides
python scripts/run.py generate_slides.py --notebook-url URL --audience beginner --length long

# Deep dive podcast
python scripts/run.py generate_audio.py --notebook-url URL --format deep-dive

# Explainer video
python scripts/run.py generate_video.py --notebook-url URL --format explainer
```

### Social Media Content
```bash
# Portrait infographic for stories
python scripts/run.py generate_infographic.py --notebook-url URL --orientation portrait --detail concise

# Brief video with trendy theme
python scripts/run.py generate_video.py --notebook-url URL --format brief --theme retro-90s
```

## Troubleshooting

**Authentication issues:**
```bash
python scripts/run.py auth_manager.py reauth
```

**Script not found:**
- Ensure you're in the skill directory
- Use full path: `python /path/to/scripts/run.py ...`

**Timeout errors:**
- Audio/video generation takes time (5-15 min)
- Use `--headless` for faster execution
- Check notebook has sufficient source content

## Additional Resources

For detailed guides on each feature, see:
- [references/slides_guide.md](references/slides_guide.md)
- [references/audio_guide.md](references/audio_guide.md)
- [references/infographic_guide.md](references/infographic_guide.md)
- [references/video_guide.md](references/video_guide.md)
