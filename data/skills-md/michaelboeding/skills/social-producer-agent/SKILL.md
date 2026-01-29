---
name: social-producer-agent
description: >
  Use this skill to create multiple social media assets as a coordinated pack.
  Triggers: "social media content", "content pack", "social assets", "campaign assets",
  "instagram content", "tiktok content", "launch kit", "marketing kit", "content series",
  "social media kit", "multiple posts", "content calendar", "batch content"
  Orchestrates: multiple images, short videos, and audio for social platforms.
---

# Social Producer

Create coordinated social media content packs with multiple assets.

**This is an orchestrator skill** that combines:
- Image generation (Gemini Image)
- Short video generation (Veo 3.1)
- Audio/music (Lyria, Gemini TTS)
- Asset assembly and formatting

## What You Can Create

| Type | Example |
|------|---------|
| Launch kit | Hero video + carousel images + short clips |
| Content pack | 5 posts for a week (mix of images/videos) |
| Campaign assets | Multiple formats for one campaign |
| Social series | Episodic content (tips, facts, stories) |
| Platform kit | Same content in multiple aspect ratios |

## Prerequisites

- `GOOGLE_API_KEY` - For Gemini (images), Veo (video), Lyria (music), TTS
- FFmpeg installed: `brew install ffmpeg`

## Workflow

### Step 1: Gather Requirements (REQUIRED)

⚠️ **DO NOT skip this step. Use interactive questioning — ask ONE question at a time.**

#### Question Flow

⚠️ **Use the `AskUserQuestion` tool for each question below.** Do not just print questions in your response — use the tool to create interactive prompts with the options shown.

**Q1: Platform**
> "I'll create your social media content pack! First — **which platform(s)?**
> 
> - Instagram
> - TikTok
> - YouTube
> - LinkedIn
> - All of the above
> - Or specify"

*Wait for response.*

**Q2: Quantity**
> "**How many pieces** of content?
> 
> *(e.g., 5 posts, 10 assets, a week's worth)*"

*Wait for response.*

**Q3: Types**
> "What **content types**?
> 
> - Images only
> - Videos/Reels only
> - Mix of both
> - Or specify"

*Wait for response.*

**Q4: Theme**
> "What's the **theme or campaign**?
> 
> - Product launch
> - Tips/educational series
> - Brand awareness
> - Promotional/sale
> - Or describe your own"

*Wait for response.*

**Q5: Assets**
> "Do you have **existing assets** to use?
> 
> - Product photos (provide paths)
> - Logo/brand assets
> - Brand colors/guidelines
> - No, generate everything"

*Wait for response.*

#### Quick Reference

| Question | Determines |
|----------|------------|
| Platform | Aspect ratios and format requirements |
| Quantity | Number of assets to generate |
| Types | Image vs video generation |
| Theme | Content direction and messaging |
| Assets | Whether to use existing or generate |

---

### Step 2: Plan the Content Pack

Create a manifest of assets to generate:

**Example: Product Launch Kit**

```
SOCIAL CONTENT PACK: New Headphones Launch

PLATFORMS: Instagram, TikTok, LinkedIn

ASSETS TO CREATE:

1. Hero Video (Reel/TikTok)
   - Format: 9:16 vertical, 15-30s
   - Content: Product reveal + features
   - Audio: Trending-style music + text overlays
   
2. Carousel Images (Instagram)
   - Format: 1:1 square, 5 images
   - Content: Feature breakdown, specs, lifestyle
   
3. Product Shots (All platforms)
   - Format: 1:1 square, 16:9 landscape
   - Content: Clean product images, different angles
   
4. Short Clips (Stories/TikTok)
   - Format: 9:16 vertical, 5-8s each
   - Content: Quick feature highlights
   
5. LinkedIn Banner
   - Format: 1200x627
   - Content: Professional product showcase
```

---

### Step 3: Generate Assets by Type

#### Images (Gemini)

**Product shots:**
```bash
# Square format
python3 ${CLAUDE_PLUGIN_ROOT}/skills/image-generation/scripts/gemini.py \
  --prompt "Premium wireless headphones, product photography, clean white background, professional lighting, 3/4 angle" \
  --aspect-ratio "1:1" \
  --resolution "2K"

# Lifestyle shot
python3 ${CLAUDE_PLUGIN_ROOT}/skills/image-generation/scripts/gemini.py \
  --prompt "Person wearing premium headphones, urban setting, modern lifestyle, candid moment, warm lighting" \
  --aspect-ratio "4:5" \
  --resolution "2K"
```

**Carousel frames:**
```bash
# Feature 1
python3 ${CLAUDE_PLUGIN_ROOT}/skills/image-generation/scripts/gemini.py \
  --prompt "Infographic style: Wireless headphones with '40hr battery' text overlay, clean modern design, brand colors blue and white" \
  --aspect-ratio "1:1"

# Feature 2
python3 ${CLAUDE_PLUGIN_ROOT}/skills/image-generation/scripts/gemini.py \
  --prompt "Infographic style: Headphones with 'Active Noise Cancelling' visual representation, sound waves, modern design" \
  --aspect-ratio "1:1"
```

**With user's product image as reference:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/image-generation/scripts/gemini.py \
  --prompt "Product in lifestyle setting, coffee shop, warm lighting" \
  --reference "/path/to/product.jpg" \
  --aspect-ratio "4:5"
```

---

#### Short Videos (Veo)

**Vertical reel (9:16):**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-generation/scripts/veo.py \
  --prompt "Quick product reveal, headphones emerging from shadow, dynamic camera movement, trendy social media style" \
  --model veo-3.1 \
  --duration 8 \
  --aspect-ratio "9:16"
```

**Feature highlight clip:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-generation/scripts/veo.py \
  --prompt "Close-up of headphone ear cup, finger tapping to skip song, satisfying gesture, clean aesthetic" \
  --model veo-3.1-fast \
  --duration 6 \
  --aspect-ratio "9:16"
```

---

#### Audio for Videos (Lyria)

**Trending-style background music:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/music-generation/scripts/lyria.py \
  --prompt "trending social media music, upbeat, modern, catchy, TikTok style" \
  --duration 20 \
  --bpm 120
```

---

#### Assemble Video with Audio

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/media-utils/scripts/video_audio_merge.py \
  --video product_reveal.mp4 \
  --music trending_music.wav \
  -o reel_final.mp4
```

---

### Step 4: Format for Platforms

**Common aspect ratios:**

| Platform | Format | Aspect Ratio | Resolution |
|----------|--------|--------------|------------|
| Instagram Feed | Square | 1:1 | 1080x1080 |
| Instagram Feed | Portrait | 4:5 | 1080x1350 |
| Instagram Reels | Vertical | 9:16 | 1080x1920 |
| Instagram Stories | Vertical | 9:16 | 1080x1920 |
| TikTok | Vertical | 9:16 | 1080x1920 |
| YouTube Shorts | Vertical | 9:16 | 1080x1920 |
| LinkedIn | Landscape | 1.91:1 | 1200x627 |
| Twitter/X | Landscape | 16:9 | 1200x675 |
| Facebook | Multiple | 1:1, 16:9 | 1200x1200 |

**To resize video for different platforms:**
```bash
# Instagram Reel to YouTube Short (same ratio, just re-export)
cp reel.mp4 youtube_short.mp4

# Square to landscape (may crop)
ffmpeg -i square.mp4 -vf "crop=ih*16/9:ih" landscape.mp4
```

---

### Step 5: Deliver the Content Pack

**Organize output:**
```
social_pack_headphones_launch/
├── instagram/
│   ├── reel_product_reveal.mp4
│   ├── carousel_1_battery.png
│   ├── carousel_2_anc.png
│   ├── carousel_3_comfort.png
│   ├── carousel_4_lifestyle.png
│   ├── carousel_5_cta.png
│   └── story_feature_1.mp4
├── tiktok/
│   ├── reveal_video.mp4
│   └── feature_clips/
│       ├── tap_controls.mp4
│       └── battery_life.mp4
├── linkedin/
│   └── banner_professional.png
└── shared/
    ├── product_shot_square.png
    ├── product_shot_landscape.png
    └── background_music.mp3
```

**Delivery message:**

"✅ Your social content pack is ready!

**Created 12 assets:**

📱 **Instagram (6 assets)**
- 1 Reel (15s product reveal)
- 5 Carousel images (feature breakdown)

📱 **TikTok (3 assets)**
- 1 Main video (15s)
- 2 Feature clips (8s each)

💼 **LinkedIn (1 asset)**
- Professional banner image

📦 **Shared assets (2)**
- Product shot (square + landscape)
- Background music track

**All files organized in:** `social_pack_headphones_launch/`

**Want me to:**
- Create more variations?
- Adjust any specific asset?
- Add captions/copy for posts?
- Create a posting schedule?"

---

## Content Ideas by Type

### Product Launch
| Asset | Content |
|-------|---------|
| Reel | Dramatic reveal, unboxing feel |
| Carousel | Feature breakdown (5 slides) |
| Stories | Behind-the-scenes, teasers |
| Static | Hero shot, lifestyle shots |

### Tips/Educational Series
| Asset | Content |
|-------|---------|
| Carousel | Step-by-step how-to |
| Reels | Quick tip videos |
| Static | Quote graphics, stats |

### Brand Awareness
| Asset | Content |
|-------|---------|
| Video | Brand story, values |
| Images | Team, culture, BTS |
| Carousel | Mission, vision, impact |

### Sale/Promotion
| Asset | Content |
|-------|---------|
| Reel | Eye-catching promo |
| Stories | Countdown, urgency |
| Static | Clear offer + CTA |

---

## Batch Generation Tips

**For consistency across assets:**
1. Use the same reference images
2. Keep music style consistent
3. Use same voice for any narration
4. Maintain color palette in prompts

**For efficiency:**
1. Generate music once, reuse across videos
2. Generate base images, create variations
3. Plan all prompts before generating

---

## Limitations

- **Veo max duration**: 8s per clip (concat for longer)
- **Generation time**: Videos take 1-3 min each
- **Text in images**: May need post-processing for perfect text
- **Exact brand colors**: Describe in prompts, results vary

## Example Prompts

**Launch kit:**
> "Create a social media launch kit for our new wireless earbuds. I need: 1 Instagram Reel, 5 carousel images showing features, 3 TikTok clips. Modern, premium feel."

**Weekly content:**
> "Create 5 social media posts for this week. Mix of images and short videos. Topic: productivity tips for remote workers. Professional but friendly tone."

**Campaign:**
> "Create social assets for our Black Friday sale. Need eye-catching visuals with '50% OFF' messaging. Instagram + TikTok formats. Urgent, exciting energy."

**With brand assets:**
> "Using these product photos, create a content pack: 3 lifestyle images, 2 short videos, 1 carousel. Our brand colors are navy and gold."
