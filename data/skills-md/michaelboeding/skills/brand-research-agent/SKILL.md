---
name: brand-research-agent
description: >
  Use this skill to analyze a brand from their website before creating content.
  Triggers: "analyze brand", "research brand", "brand guidelines", "brand profile",
  "understand brand", "brand colors", "brand voice", "before creating content for"
  Extracts: colors, typography, voice/tone, products, audience, competitive positioning.
  Outputs a reusable brand_profile.json that producer skills can use.
---

# Brand Research Skill

Analyze a brand's website to extract brand elements for content creation.

**This skill uses 5 specialized agents** that analyze different brand dimensions in parallel, then synthesizes into a unified brand profile.

## What It Extracts

| Dimension | Elements | Used For |
|-----------|----------|----------|
| **Visual** | Colors, typography, logo, imagery style | Image prompts, video style |
| **Voice** | Tone, messaging, taglines, copy style | Voiceover, scripts |
| **Product** | Offerings, features, USPs, pricing | Content focus |
| **Audience** | Demographics, psychographics, pain points | Tone targeting |
| **Positioning** | Market position, competitors, differentiation | Messaging strategy |

## Prerequisites

- Browser access (uses web scraping)
- No API keys required

## Workflow

### Step 1: Get the Website URL (REQUIRED)

**FIRST, always ask for the website URL.** Do not proceed without it.

**Say this to the user:**

> "I'll analyze that brand for you! 
>
> **What's the website URL?** (e.g., https://nike.com)
>
> Optional: Any specific pages to focus on? Any known competitors?"

**Wait for the user to provide the URL before proceeding.**

If the user just says "analyze Nike's brand", ask:
> "I'll analyze Nike for you. Just to confirm - should I use https://nike.com?"

---

### Step 2: Navigate and Capture Website Data

Use browser tools to navigate the website and capture:

```
1. Homepage - Overall impression, hero messaging, colors
2. About page - Company story, values, team
3. Products/Services page - Offerings, features, pricing
4. Blog/Resources - Voice, content style
5. Footer - Social links, taglines
```

**Capture for each page:**
- Screenshot for visual analysis
- HTML/CSS for colors and fonts
- Text content for voice analysis
- Images for style analysis

---

### Step 3: Run Specialized Agents in Parallel

Deploy 5 agents, each analyzing a different dimension:

#### Agent 1: Visual Analyst
Focus: Colors, typography, logo, imagery style
```
Analyze:
- Primary, secondary, accent colors from CSS/design
- Font families for headings and body
- Logo usage and placement
- Photography/illustration style
- Overall visual mood (minimal, bold, playful, etc.)
```

#### Agent 2: Voice Analyst
Focus: Tone, messaging, taglines, copy style
```
Analyze:
- Headlines and how they're written
- Body copy style (formal vs casual)
- CTAs and their tone
- Taglines and slogans
- Emotional appeals used
```

#### Agent 3: Product Analyst
Focus: Offerings, features, USPs, pricing
```
Analyze:
- What products/services they offer
- Key features highlighted
- Unique selling propositions
- Pricing model and tiers
- Value propositions
```

#### Agent 4: Audience Analyst
Focus: Demographics, psychographics, pain points
```
Analyze:
- Who the messaging targets
- Pain points addressed
- Aspirations appealed to
- Language level and jargon
- Testimonials and case studies
```

#### Agent 5: Competitive Analyst
Focus: Market position, competitors, differentiation
```
Analyze:
- Market/industry category
- Implied competitors
- How they differentiate
- Unique market position
- Competitive advantages claimed
```

---

### Step 4: Synthesize into Brand Profile

Combine all agent outputs into a unified `brand_profile.json`:

```json
{
  "brand": {
    "name": "Company Name",
    "website": "https://example.com",
    "tagline": "Their main tagline",
    "analyzed_date": "2026-01-04"
  },
  "visual": {
    "colors": {
      "primary": "#1E40AF",
      "secondary": "#F59E0B",
      "accent": "#10B981",
      "background": "#FFFFFF",
      "text": "#1F2937"
    },
    "typography": {
      "headings": "Montserrat Bold",
      "body": "Open Sans",
      "style": "Modern, clean"
    },
    "logo": {
      "description": "Abstract geometric mark + wordmark",
      "usage": "Typically on white/dark backgrounds"
    },
    "imagery_style": {
      "type": "Photography",
      "mood": "Professional, aspirational",
      "subjects": "People using product, office settings",
      "treatment": "Bright, high contrast, natural lighting"
    }
  },
  "voice": {
    "tone": ["Confident", "Approachable", "Expert"],
    "personality": "Like a smart friend who knows their stuff",
    "formality": "Professional casual",
    "style_notes": [
      "Short, punchy sentences",
      "Active voice preferred",
      "Benefit-focused over feature-focused",
      "Uses 'you' and 'your' frequently"
    ],
    "example_headlines": [
      "Built for builders",
      "Simple. Powerful. Yours."
    ],
    "words_to_use": ["Simple", "Powerful", "Fast", "Seamless"],
    "words_to_avoid": ["Cheap", "Basic", "Just"]
  },
  "products": {
    "category": "SaaS / Developer Tools",
    "offerings": [
      {
        "name": "Core Platform",
        "description": "Main product offering",
        "key_features": ["Feature 1", "Feature 2", "Feature 3"]
      }
    ],
    "usps": [
      "10x faster than alternatives",
      "No-code setup in 5 minutes",
      "Enterprise-grade security"
    ],
    "pricing_model": "Freemium with usage-based scaling",
    "value_proposition": "Get to market faster without sacrificing quality"
  },
  "audience": {
    "primary": {
      "who": "Technical founders and developers",
      "demographics": "25-45, tech-savvy, startup/scale-up",
      "psychographics": "Move fast, value efficiency, quality-conscious"
    },
    "secondary": {
      "who": "Enterprise DevOps teams",
      "demographics": "Large companies, IT departments"
    },
    "pain_points": [
      "Complex setup processes",
      "Slow iteration cycles",
      "Scaling costs out of control"
    ],
    "aspirations": [
      "Ship faster",
      "Look professional",
      "Scale effortlessly"
    ]
  },
  "positioning": {
    "market": "Developer tools / Infrastructure",
    "competitors": ["Competitor A", "Competitor B", "Competitor C"],
    "differentiation": "Simplicity + Enterprise power in one package",
    "market_position": "Premium but accessible",
    "competitive_advantages": [
      "Easiest setup in category",
      "Best-in-class performance",
      "Loved by developers"
    ]
  },
  "content_guidelines": {
    "for_video_producer": {
      "music_style": "Modern, upbeat, confident but not aggressive",
      "voiceover_tone": "Confident, clear, approachable expert",
      "visual_style": "Clean, minimal, bold accents, professional"
    },
    "for_podcast_producer": {
      "host_personality": "Smart, curious, enthusiastic about tech",
      "conversation_style": "Educational but engaging, not dry"
    },
    "for_audio_producer": {
      "voiceover_direction": "Professional but warm, not corporate robot",
      "music_mood": "Inspiring, forward-moving, modern"
    },
    "for_social_producer": {
      "image_style": "Clean product shots, lifestyle use cases",
      "video_style": "Quick, punchy, value-first",
      "copy_style": "Short, benefit-focused, emoji-light"
    }
  }
}
```

---

### Step 5: Save and Deliver

Save the brand profile:

```bash
# Save to current directory
brand_profile.json

# Or to a specific location
/path/to/project/brand_profile.json
```

**Delivery message:**

"✅ Brand analysis complete!

**Brand Profile saved to:** `brand_profile.json`

**Summary:**
- **Brand:** Acme Corp
- **Colors:** Blue (#1E40AF) + Orange (#F59E0B)
- **Voice:** Confident, approachable, expert
- **Audience:** Technical founders, 25-45
- **Position:** Simplicity + Power

**Use this profile with:**
- `video-producer --brand brand_profile.json`
- `podcast-producer --brand brand_profile.json`
- `social-producer --brand brand_profile.json`

**Want me to:**
- Analyze additional pages?
- Deep dive on any dimension?
- Create content using this profile?"

---

## Using the Brand Profile with Producers

Once you have a `brand_profile.json`, reference it when creating content:

**Example workflow:**

```
USER: "Create a product video using our brand profile"

PRODUCER:
1. Reads brand_profile.json
2. Uses colors for visual prompts: "Color scheme: blue (#1E40AF) and orange (#F59E0B)"
3. Uses voice for TTS: "Tone: Confident, approachable, professional"
4. Uses music style: "Modern, upbeat, confident"
5. Uses imagery style: "Clean, minimal, professional photography"

RESULT: On-brand video that matches company's existing presence
```

---

## Manual Brand Profile

If you can't scrape or prefer manual input, create `brand_profile.yaml`:

```yaml
brand:
  name: "My Company"
  tagline: "Innovation for everyone"

visual:
  colors:
    primary: "#1E40AF"
    secondary: "#F59E0B"
  typography:
    headings: "Montserrat"
    body: "Open Sans"

voice:
  tone: ["Friendly", "Expert", "Approachable"]
  formality: "Professional casual"

audience:
  primary: "Small business owners, 30-50"
  pain_points: ["Too complex", "Too expensive"]

# ... etc
```

---

## Agents

This skill uses 5 specialized agents defined in `agents/`:

| Agent | File | Focus |
|-------|------|-------|
| Visual Analyst | `visual-analyst.md` | Colors, fonts, imagery |
| Voice Analyst | `voice-analyst.md` | Tone, messaging, copy |
| Product Analyst | `product-analyst.md` | Offerings, USPs |
| Audience Analyst | `audience-analyst.md` | Who they target |
| Competitive Analyst | `competitive-analyst.md` | Market position |

---

## Limitations

- **Dynamic content**: May miss JavaScript-rendered content
- **Accuracy**: Analysis is interpretation, not definitive
- **Access**: Some sites may block scraping
- **Currency**: Brands evolve; re-analyze periodically

## Example Prompts

**Basic:**
> "Analyze Nike's brand from their website"

**With specifics:**
> "Research the Apple brand, focusing on their product pages and About section"

**For content creation:**
> "Before creating our marketing video, analyze our competitor's brand: https://competitor.com"

**Update existing:**
> "Re-analyze our brand profile, we've updated our website"
