---
name: visual-keywords
description: "Generate keyword-rich strings for visual references to optimize for fuzzy search and recall. Focuses on searchability and keyword matching rather than prose or alt text."
metadata:
  author: nweii
  version: "1.0.0"
---

# Visual Keywords

Analyze the provided visual content and generate a dense string of searchable keywords. This is intended to make images and media easier to fuzzy search during recall, not to act as alt text or prose description. Specify the type:

- **Aesthetic/Image keywords** — For design work, photos, illustrations, UI screenshots
- **Font keywords** — For typeface specimens, font families, typography examples

## For Aesthetic/Image Keywords

Analyze and extract keywords for visual elements, style, composition, and emotional impact.

### Analysis Framework

- **Subjects/Motifs**: Main elements, objects, themes (portrait, landscape, geometric shapes, etc.)
- **Mood/Adjectives**: Emotions and aesthetics evoked (cheerful, gloomy, elegant, grungy, etc.)
- **Medium/Context**: Type of visual (photo, illustration, 3D render, graphic design, UI, etc.)
- **Style/Genre**: Artistic influences, design paradigms (Art Nouveau, brutalist, steampunk, etc.)
- **Color Palette**: Dominant colors and schemes (pastels, neon, earth tones, monochrome, etc.)
- **Composition**: Layout, perspective, symmetry, visual flow (closeup, isometric, minimalist, etc.)
- **Emotional Impact**: Intended feelings (awe, mystery, calm, nostalgia, unease, etc.)
- **Details**: Settings, techniques, textures, lighting, time period

### Output Format

Synthesize into a dense string of keywords using concise, shorthand style. Omit articles, prepositions, and grammatical connectors. Avoid prose or alt-text style descriptions. Focus entirely on maximizing keyword matching for fuzzy search. ~100-150 words per image in a code block.

**Example:**

```
majestic dragon craggy cliffside wings outspread tail coiled glowing crystal orb fantasy concept art intricate scales spines horns luminous full moon starry night sky deep blues purples orange accents dramatic cinematic composition close-up head distant body background polished painterly aesthetic atmospheric haze lighting effects highly detailed digital illustration awe power magic wonder adventure
```

## For Font Keywords

Analyze typeface characteristics, stylistic influences, emotional impact, and usage contexts for keyword extraction.

### Analysis Framework

- **Category**: Primary classification (serif, sans-serif, display, script, monospace)
- **Weights/Proportions**: Range shown (thin to heavy, compressed to wide)
- **Distinctive Features**: Unique letter shapes, strokes, terminals, details
- **Similar Fonts**: Comparable well-known typefaces for reference
- **Mood/Personality**: Emotions evoked; how it changes across weights
- **Era/Influences**: Time periods, design movements, cultural traditions
- **Formality/Aesthetics**: Overall character (playful, mechanical, organic, sophisticated, etc.)
- **Expressive Genres**: Fiction/story vibes this font suits (cyberpunk, horror, coming-of-age, etc.)
- **Non-Fiction Uses**: Academic fields, journalistic beats, professional contexts
- **Medium Suitability**: Publications, products, design projects (billboards, textbooks, etc.)
- **Use Cases & Pairings**: Specific contexts; complementary visual treatments

### Output Format

Synthesize into information-dense keyword strings. Omit sentences and conversational filler. The goal is searchability and recall. ~150-300 words in a code block.

**Example:**

```
hand-brushed sans-serif 2 weights italics energetic uneven strokes ragged edges wobbly baseline similar Architype Van Doesburg Boisterous Inline exuberant spontaneous unfiltered manic raw impulsive intensity graffiti guerrilla postering untamed creative outpouring playful unhinged era influences Futurist anti-art abstract expressionism punk DIY aesthetic genres psychedelic thrillers transgressive fiction introspective autobiographies underground comics beat poetry indie films lo-fi zines edgy fashion progressive activism unmediated transmission thoughts page unapologetic statement identity visceral urgency display sizes electric dynamism smaller sizes pairings xerox-distressed photos low-res bitmaps anarchic collages fluorescent colors brash auteur-driven designs fringe publications experimental music street art youth-oriented brands
```

---

Provide the visual content and specify which type of keywords you need.
