---
name: baoyu-xhs-images
description: Xiaohongshu (Little Red Book) infographic series generator with multiple style options. Breaks down content into 1-10 cartoon-style infographics. Use when user asks to create "小红书图片", "XHS images", or "RedNote infographics".
---

# Xiaohongshu Infographic Series Generator

Break down complex content into eye-catching infographic series for Xiaohongshu with multiple style options.

## Usage

```bash
# Auto-select style and layout based on content
/baoyu-xhs-images posts/ai-future/article.md

# Specify style
/baoyu-xhs-images posts/ai-future/article.md --style notion

# Specify layout
/baoyu-xhs-images posts/ai-future/article.md --layout dense

# Combine style and layout
/baoyu-xhs-images posts/ai-future/article.md --style tech --layout list

# Direct content input
/baoyu-xhs-images
[paste content]

# Direct input with options
/baoyu-xhs-images --style bold --layout comparison
[paste content]
```

## Options

| Option | Description |
|--------|-------------|
| `--style <name>` | Visual style (see Style Gallery) |
| `--layout <name>` | Information layout (see Layout Gallery) |

## Two Dimensions

| Dimension | Controls | Options |
|-----------|----------|---------|
| **Style** | Visual aesthetics: colors, lines, decorations | cute, fresh, warm, bold, minimal, retro, pop, notion, chalkboard |
| **Layout** | Information structure: density, arrangement | sparse, balanced, dense, list, comparison, flow |

Style × Layout can be freely combined. Example: `--style notion --layout dense` creates an intellectual-looking knowledge card with high information density.

## Style Gallery

| Style | Description |
|-------|-------------|
| `cute` (Default) | Sweet, adorable, girly - classic Xiaohongshu aesthetic |
| `fresh` | Clean, refreshing, natural |
| `warm` | Cozy, friendly, approachable |
| `bold` | High impact, attention-grabbing |
| `minimal` | Ultra-clean, sophisticated |
| `retro` | Vintage, nostalgic, trendy |
| `pop` | Vibrant, energetic, eye-catching |
| `notion` | Minimalist hand-drawn line art, intellectual |
| `chalkboard` | Colorful chalk on black board, educational |

Detailed style definitions: `references/styles/<style>.md`

## Layout Gallery

| Layout | Description |
|--------|-------------|
| `sparse` (Default) | Minimal information, maximum impact (1-2 points) |
| `balanced` | Standard content layout (3-4 points) |
| `dense` | High information density, knowledge card style (5-8 points) |
| `list` | Enumeration and ranking format (4-7 items) |
| `comparison` | Side-by-side contrast layout |
| `flow` | Process and timeline layout (3-6 steps) |

Detailed layout definitions: `references/layouts/<layout>.md`

## Auto Selection

| Content Signals | Style | Layout |
|-----------------|-------|--------|
| Beauty, fashion, cute, girl, pink | `cute` | sparse/balanced |
| Health, nature, clean, fresh, organic | `fresh` | balanced/flow |
| Life, story, emotion, feeling, warm | `warm` | balanced |
| Warning, important, must, critical | `bold` | list/comparison |
| Professional, business, elegant, simple | `minimal` | sparse/balanced |
| Classic, vintage, old, traditional | `retro` | balanced |
| Fun, exciting, wow, amazing | `pop` | sparse/list |
| Knowledge, concept, productivity, SaaS | `notion` | dense/list |
| Education, tutorial, learning, teaching, classroom | `chalkboard` | balanced/dense |

## File Structure

Each session creates an independent directory named by content slug:

```
xhs-images/{topic-slug}/
├── source-{slug}.{ext}             # Source files (text, images, etc.)
├── analysis.md                     # Deep analysis results
├── outline-style-[slug].md         # Variant A (e.g., outline-style-tech.md)
├── outline-style-[slug].md         # Variant B (e.g., outline-style-notion.md)
├── outline-style-[slug].md         # Variant C (e.g., outline-style-minimal.md)
├── outline.md                      # Final selected
├── prompts/
│   ├── 01-cover-[slug].md
│   ├── 02-content-[slug].md
│   └── ...
├── 01-cover-[slug].png
├── 02-content-[slug].png
└── NN-ending-[slug].png
```

**Slug Generation**:
1. Extract main topic from content (2-4 words, kebab-case)
2. Example: "AI工具推荐" → `ai-tools-recommend`

**Conflict Resolution**:
If `xhs-images/{topic-slug}/` already exists:
- Append timestamp: `{topic-slug}-YYYYMMDD-HHMMSS`
- Example: `ai-tools` exists → `ai-tools-20260118-143052`

**Source Files**:
Copy all sources with naming `source-{slug}.{ext}`:
- `source-article.md`, `source-photo.jpg`, etc.
- Multiple sources supported: text, images, files from conversation

## Workflow

### Step 1: Analyze Content → `analysis.md`

Read source content, save it if needed, and perform deep analysis.

**Actions**:
1. **Save source content** (if not already a file):
   - If user provides a file path: use as-is
   - If user pastes content: save to `source.md` in target directory
2. Read source content
3. **Deep analysis** following `references/analysis-framework.md`:
   - Content type classification (种草/干货/测评/教程/避坑...)
   - Hook analysis (爆款标题潜力)
   - Target audience identification
   - Engagement potential (收藏/分享/评论)
   - Visual opportunity mapping
   - Swipe flow design
4. Detect source language
5. Determine recommended image count (2-10)
6. Select 3 style+layout combinations
7. **Save to `analysis.md`**

### Step 2: Generate 3 Outline Variants

Based on analysis, create three distinct style variants.

**For each variant**:
1. **Generate outline** (`outline-style-[slug].md`):
   - YAML front matter with style, layout, image_count
   - Cover design with hook
   - Each image: layout, core message, text content, visual concept
   - **Written in user's preferred language**
   - Reference: `references/outline-template.md`

| Variant | Selection Logic | Example Filename |
|---------|-----------------|------------------|
| A | Primary recommendation | `outline-style-tech.md` |
| B | Alternative style | `outline-style-notion.md` |
| C | Different audience/mood | `outline-style-minimal.md` |

**All variants are preserved after selection for reference.**

### Step 3: User Confirms All Options

**IMPORTANT**: Present ALL options in a single confirmation step using AskUserQuestion. Do NOT interrupt workflow with multiple separate confirmations.

**Determine which questions to ask**:

| Question | When to Ask |
|----------|-------------|
| Style variant | Always (required) |
| Default layout | Only if user might want to override |
| Language | Only if `source_language ≠ user_language` |

**Language handling**:
- If source language = user language: Just inform user (e.g., "Images will be in Chinese")
- If different: Ask which language to use

**AskUserQuestion format**:

```
Question 1 (Style): Which style variant?
- A: tech + dense (Recommended) - 专业科技感，适合干货
- B: notion + list - 清爽知识卡片
- C: minimal + balanced - 简约高端风格
- Custom: 自定义风格描述

Question 2 (Layout) - only if relevant:
- Keep variant default (Recommended)
- sparse / balanced / dense / list / comparison / flow

Question 3 (Language) - only if mismatch:
- 中文 (匹配原文)
- English (your preference)
```

**After confirmation**:
1. Copy selected `outline-style-[slug].md` → `outline.md`
2. Update YAML front matter with confirmed options
3. If custom style: regenerate outline with that style
4. User may edit `outline.md` directly for fine-tuning

### Step 4: Generate Images

With confirmed outline + style + layout:

**For each image (cover + content + ending)**:
1. Save prompt to `prompts/NN-{type}-[slug].md` (in user's preferred language)
2. Generate image using confirmed style and layout
3. Report progress after each generation

**Image Generation Skill Selection**:
- Check available image generation skills
- If multiple skills available, ask user preference

**Session Management**:
If image generation skill supports `--sessionId`:
1. Generate unique session ID: `xhs-{topic-slug}-{timestamp}`
2. Use same session ID for all images
3. Ensures visual consistency across generated images

### Step 5: Completion Report

```
Xiaohongshu Infographic Series Complete!

Topic: [topic]
Style: [style name]
Layout: [layout name or "varies"]
Location: [directory path]
Images: N total

✓ analysis.md
✓ outline-style-tech.md
✓ outline-style-notion.md
✓ outline-style-minimal.md
✓ outline.md (selected: tech + dense)

Files:
- 01-cover-[slug].png ✓ Cover (sparse)
- 02-content-[slug].png ✓ Content (balanced)
- 03-content-[slug].png ✓ Content (dense)
- 04-ending-[slug].png ✓ Ending (sparse)
```

## Image Modification

### Edit Single Image

1. Identify image to edit (e.g., `03-content-chatgpt.png`)
2. Update prompt in `prompts/03-content-chatgpt.md` if needed
3. Regenerate image using same session ID

### Add New Image

1. Specify insertion position (e.g., after image 3)
2. Create new prompt with appropriate slug
3. Generate new image
4. **Renumber files**: All subsequent images increment NN by 1
5. Update `outline.md` with new image entry

### Delete Image

1. Remove image file and prompt file
2. **Renumber files**: All subsequent images decrement NN by 1
3. Update `outline.md` to remove image entry

## Content Breakdown Principles

1. **Cover (Image 1)**: Hook + visual impact → `sparse` layout
2. **Content (Middle)**: Core value per image → `balanced`/`dense`/`list`/`comparison`/`flow`
3. **Ending (Last)**: CTA / summary → `sparse` or `balanced`

**Style × Layout Matrix** (✓✓ = highly recommended, ✓ = works well):

| | sparse | balanced | dense | list | comparison | flow |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| cute | ✓✓ | ✓✓ | ✓ | ✓✓ | ✓ | ✓ |
| fresh | ✓✓ | ✓✓ | ✓ | ✓ | ✓ | ✓✓ |
| warm | ✓✓ | ✓✓ | ✓ | ✓ | ✓✓ | ✓ |
| bold | ✓✓ | ✓ | ✓ | ✓✓ | ✓✓ | ✓ |
| minimal | ✓✓ | ✓✓ | ✓✓ | ✓ | ✓ | ✓ |
| retro | ✓✓ | ✓✓ | ✓ | ✓✓ | ✓ | ✓ |
| pop | ✓✓ | ✓✓ | ✓ | ✓✓ | ✓✓ | ✓ |
| notion | ✓✓ | ✓✓ | ✓✓ | ✓✓ | ✓✓ | ✓✓ |
| chalkboard | ✓✓ | ✓✓ | ✓✓ | ✓✓ | ✓ | ✓✓ |

## References

Detailed templates and guidelines in `references/` directory:
- `analysis-framework.md` - XHS-specific content analysis
- `outline-template.md` - Outline format and examples
- `styles/<style>.md` - Detailed style definitions
- `layouts/<layout>.md` - Detailed layout definitions
- `base-prompt.md` - Base prompt template

## Notes

- Image generation typically takes 10-30 seconds per image
- Auto-retry once on generation failure
- Use cartoon alternatives for sensitive public figures
- All prompts and text use confirmed language preference
- Maintain style consistency across all images in series

## Extension Support

Custom styles and configurations via EXTEND.md.

**Check paths** (priority order):
1. `.baoyu-skills/baoyu-xhs-images/EXTEND.md` (project)
2. `~/.baoyu-skills/baoyu-xhs-images/EXTEND.md` (user)

If found, load before Step 1. Extension content overrides defaults.
