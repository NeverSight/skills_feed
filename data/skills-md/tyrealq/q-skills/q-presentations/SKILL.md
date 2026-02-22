---
name: q-presentations
description: Generates professional slide deck images from content with smart logo branding and video-overlay-aware layout selection. Use when user asks to "create slides", "make a presentation", "generate deck", "slide deck", or "PPT".
---

# Q-Presentations

Built on the foundation of [baoyu-slide-deck](https://github.com/nicepkg/baoyu-slide-deck) by baoyu, extended with layout-driven overlay safety and smart logo branding.

## Usage

```bash
/q-presentations path/to/content.md
/q-presentations path/to/content.md --style sketch-notes
/q-presentations path/to/content.md --audience executives
/q-presentations path/to/content.md --lang en
/q-presentations path/to/content.md --slides 10
/q-presentations path/to/content.md --outline-only
/q-presentations  # Then paste content
```

## Script Directory

Agent execution instructions:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`.
2. Script path = `${SKILL_DIR}/scripts/<script-name>`.

| Script | Purpose |
|--------|---------|
| `scripts/gen_slide.py` | Generate slide images via Gemini API |
| `scripts/overlay_logo.py` | Apply Dr. Q logo overlay |
| `scripts/merge-to-pptx.ts` | Merge slides into PowerPoint (Bun/TS) |
| `scripts/merge-to-pdf.ts` | Merge slides into PDF (Bun/TS) |

## Options

| Option | Description |
|--------|-------------|
| `--style <name>` | Visual style: preset name, `custom`, or custom style name |
| `--audience <type>` | Target: beginners, intermediate, experts, executives, general |
| `--lang <code>` | Output language (en, zh, ja, etc.) |
| `--slides <number>` | Target slide count (8-25 recommended, max 30) |
| `--outline-only` | Generate outline only, skip image generation |
| `--prompts-only` | Generate outline + prompts, skip images |
| `--images-only` | Generate images from existing prompts directory |
| `--regenerate <N>` | Regenerate specific slide(s): `--regenerate 3` or `--regenerate 2,5,8` |
| `--logo <position>` | Logo placement: top-right (default), bottom-right, top-left, bottom-left, none |
| `--video-overlay <side>` | Side reserved for video overlay: right (default), left, bottom, none |

## Style System

### Presets

| Preset | Dimensions | Best For |
|--------|------------|----------|
| `blueprint` (Default) | grid + cool + technical + balanced | Architecture, system design |
| `chalkboard` | organic + warm + handwritten + balanced | Education, tutorials |
| `corporate` | clean + professional + geometric + balanced | Investor decks, proposals |
| `minimal` | clean + neutral + geometric + minimal | Executive briefings |
| `sketch-notes` | organic + warm + handwritten + balanced | Educational, tutorials |
| `watercolor` | organic + warm + humanist + minimal | Lifestyle, wellness |
| `dark-atmospheric` | clean + dark + editorial + balanced | Entertainment, gaming |
| `notion` | clean + neutral + geometric + dense | Product demos, SaaS |
| `bold-editorial` | clean + vibrant + editorial + balanced | Product launches, keynotes |
| `editorial-infographic` | clean + cool + editorial + dense | Tech explainers, research |
| `fantasy-animation` | organic + vibrant + handwritten + minimal | Educational storytelling |
| `intuition-machine` | clean + cool + technical + dense | Technical docs, academic |
| `pixel-art` | pixel + vibrant + technical + balanced | Gaming, developer talks |
| `scientific` | clean + cool + technical + dense | Biology, chemistry, medical |
| `vector-illustration` | clean + vibrant + humanist + balanced | Creative, children's content |
| `vintage` | paper + warm + editorial + balanced | Historical, heritage |

Full specs: `references/dimensions/*.md`, `references/dimensions/presets.md`, `references/styles/*.md`.

## Design Philosophy

Decks are designed for reading and sharing, not only live presenting:
- Each slide should be self-explanatory.
- Flow should remain clear in a scroll view.
- Context should be present on each slide.
- Style should remain consistent across the full deck.

See:
- `references/design-guidelines.md` for audience and visual hierarchy.
- `references/layouts.md` for layout selection and overlay-safe rules.

## File Management

### Output Directory

```text
slide-deck/{topic-slug}/
|-- source-{slug}.{ext}
|-- outline.md
|-- prompts/
|   |-- 01-slide-cover.md, 02-slide-{slug}.md, ...
|-- 01-slide-cover.png, 02-slide-{slug}.png, ...
|-- {topic-slug}.pptx
`-- {topic-slug}.pdf
```

## Language Handling

Detection priority:
1. `--lang` flag.
2. EXTEND.md `language`.
3. User conversation language.
4. Source content language.

Rule: all user-facing responses should use the user's preferred language. Technical names remain in English.

## Workflow

```text
Slide Deck Progress:
- [ ] Step 0: Skill announcement (first run only)
- [ ] Step 1: Setup and analyze
- [ ] Step 2: Confirmation
- [ ] Step 3: Generate outline
- [ ] Step 4: Review outline (conditional)
- [ ] Step 5: Generate prompts
- [ ] Step 6: Review prompts (conditional)
- [ ] Step 7: Generate images
- [ ] Step 7.5: Logo overlay
- [ ] Step 8: Merge to PPTX/PDF
- [ ] Step 9: Output summary
```

Flow:
`Announce -> Input -> Preferences -> Analyze -> Confirm -> Outline -> [Review] -> Prompts -> [Review] -> Images -> Logo -> Merge -> Complete`

### Step 0: Skill announcement

```text
q-presentations - slide deck generator
Built on baoyu-slide-deck, extended with layout-driven overlay safety and smart logo branding.
```

### Step 1: Setup and analyze

#### 1.1 Load preferences (EXTEND.md)

Check in this order:
1. `.q-skills/q-presentations/EXTEND.md` (project)
2. `$HOME/.q-skills/q-presentations/EXTEND.md` (user)

When found: parse and summarize.
When missing: collect preferences and proceed with defaults.

Schema: `references/config/preferences-schema.md`

#### 1.2 Analyze content

1. Save source content (if pasted, save as `source.md`).
2. Backup existing source/prompt/image files before overwrite.
3. Follow `references/analysis-framework.md`.
4. Detect language and recommend slide count/style.
5. Generate topic slug.

#### 1.3 Check existing content

If `slide-deck/{topic-slug}` exists, ask user whether to regenerate outline, regenerate images, backup and regenerate, or exit.

### Step 2: Confirmation

Three parts:
1. Round 1 (always): style, audience, slide count, outline review, prompt review.
2. Round 2 (if custom style): texture, mood, typography, density.
3. q-presentations questions (always): video overlay side and logo placement.

Video overlay options:
- right (recommended)
- left
- bottom
- none

Logo options:
- top-right (recommended)
- bottom-right
- top-left
- bottom-left
- none

Store: `video_overlay_side`, `logo_position`, and all style/audience/review preferences.

### Step 3: Generate outline

1. Build STYLE_INSTRUCTIONS from preset/custom dimensions.
2. Apply audience, language, and slide count.
3. Select a `Layout` for every slide using `references/layouts.md`.

Layout selection policy:
1. Infer content-fit candidates.
2. Use `primary_content_bias` and derived safe-side mapping from `layouts.md`.
3. Apply `layouts.md` exceptions table.
4. Keep only layouts compatible with selected `video_overlay_side`.
5. Rank by content fit and diversity.
6. If empty, use fallback layouts from `layouts.md`.

Prompting rule:
- Do not state overlay reservations or empty-zone instructions.
- Only include the chosen layout composition.

Outline metadata should include:
```text
**Video Overlay**: [right/left/bottom/none]
**Logo**: [top-right/bottom-right/top-left/bottom-left/none]
```

Save as `outline.md`.

### Step 4: Review outline (conditional)

Skip when user disabled outline review.
Otherwise show slide-by-slide summary and ask: proceed, edit, regenerate.

### Step 5: Generate prompts

1. Read `references/base-prompt.md`.
2. For each slide, merge:
   - STYLE_INSTRUCTIONS from outline
   - slide content
   - selected layout guidance
3. Save into `prompts/` with backups on overwrite.

### Step 6: Review prompts (conditional)

Skip when user disabled prompt review.
Otherwise ask: proceed, edit, regenerate.

### Step 7: Generate images

Generate sequentially using:

```bash
python ${SKILL_DIR}/scripts/gen_slide.py <prompt-file> <output-png>
```

Rules:
- Backup existing image before overwrite.
- Auto-retry once on failure.
- Report progress in user language.

### Step 7.5: Logo overlay

```bash
python ${SKILL_DIR}/scripts/overlay_logo.py <slide-deck-dir> --position <logo-position> --style <style-name>
```

If logo is `none`, add `--skip`.

### Step 8: Merge to PPTX/PDF

Use Bun/TypeScript tools:
```bash
npx -y bun ${SKILL_DIR}/scripts/merge-to-pptx.ts <slide-deck-dir>
npx -y bun ${SKILL_DIR}/scripts/merge-to-pdf.ts <slide-deck-dir>
```

### Step 9: Output summary

```text
Slide Deck Complete!

Topic: [topic]
Style: [preset or custom dimensions]
Video Overlay Zone: [side]
Logo: [position]
Location: [directory]
Slides: N total

Outline: outline.md
PPTX: {topic-slug}.pptx
PDF: {topic-slug}.pdf
```

## Partial Workflows

| Option | Workflow |
|--------|----------|
| `--outline-only` | Steps 1-3 only |
| `--prompts-only` | Steps 1-5 only |
| `--images-only` | Start from Step 7 (requires prompts/) |
| `--regenerate N` | Regenerate specific slide(s) only |

## References

| File | Content |
|------|---------|
| `references/analysis-framework.md` | Content analysis for presentations |
| `references/outline-template.md` | Outline structure and format |
| `references/modification-guide.md` | Edit, add, delete slide workflows |
| `references/content-rules.md` | Content and style guidelines |
| `references/design-guidelines.md` | Audience, typography, colors, visual elements |
| `references/layouts.md` | Layout catalog, overlay-safe policy, fallback rules |
| `references/base-prompt.md` | Base prompt for image generation |
| `references/dimensions/*.md` | Dimension specifications |
| `references/dimensions/presets.md` | Preset to dimension mapping |
| `references/styles/<style>.md` | Full style specifications |
| `references/config/preferences-schema.md` | EXTEND.md structure |

## Notes

- Image generation usually takes 10-30 seconds per slide.
- Keep `GEMINI_API_KEY` user-configurable through environment variables.
- Never include photorealistic images of prominent individuals.
- Never include placeholder slides for author/date metadata.
