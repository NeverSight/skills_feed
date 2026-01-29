---
name: xiaohongshu-images
description: Transform markdown/HTML into styled 3:4 ratio images for Xiaohongshu
---

# Xiaohongshu Images Skill

This skill transforms markdown, HTML, or text content into beautifully styled HTML pages with AI-generated cover images, then captures them as sequential screenshots at 3:4 ratio for Xiaohongshu posting.

## Overview

The skill performs the following workflow:

1. **Accept Content**: Receives markdown, HTML, or txt format content from the user
2. **Load Prompt Template**: Reads the prompt template from `prompts/default.md` in this skill's directory
3. **Generate Cover Image**: Uses `/baoyu-cover-image` skill to generate a cover image based on the article content
4. **Generate HTML**: Creates a beautifully styled HTML page following the prompt template specifications
5. **Save Output**: Saves the HTML to `~/Dev/obsidian/articles/<date-article-title>/xhs-preview.html`
6. **Capture Screenshots**: Takes sequential 3:4 ratio screenshots of the entire page without cutting text

## Usage

When the user invokes this skill, follow these steps:

### Step 1: Identify the Input

The user will provide one of the following:
- A file path to a markdown, HTML, or txt file (e.g., `/path/to/article.md`)
- Raw content directly in the conversation
- A URL to fetch content from

If the input is unclear, ask the user to provide either a file path, URL, or paste the content directly.

### Step 2: Read the Prompt Template

Read the prompt template from this skill's directory:

```
{{SKILL_DIR}}/prompts/default.md
```

Use the Read tool to get the prompt template content. This template defines the HTML/CSS styling specifications.

### Step 3: Extract Article Title and Date

From the content, extract:
- **Title**: The main heading (h1) or first significant title in the content
- **Date**: Current date in YYYY-MM-DD format

Create the output folder path as: `~/Dev/obsidian/articles/<date>-<sanitized-title>/`
- Replace spaces with hyphens
- Remove special characters
- Keep the title reasonably short (max 50 characters)
- All images go in `_attachments/` subfolder

### Step 4: Generate Cover Image with baoyu-cover-image Skill

**⚠️ COMPLIANCE CHECK**: Before generating, ensure the image concept complies with Xiaohongshu community guidelines (Section 11 of the prompt template). The image must:
- Be age-appropriate with no revealing clothing or suggestive poses
- Avoid political symbols, violence, gambling, smoking, or alcohol abuse
- Convey positive, constructive messages
- Be culturally sensitive and original

Use the `/baoyu-cover-image` skill to generate the cover image:

1. **Invoke the skill** with the article content:

```bash
/baoyu-cover-image ~/Dev/obsidian/articles/<date>-<title>/index.md --style <auto-or-specified> --no-title
```

Or if the content is not yet saved, pass the content directly to the skill.

2. **Style Selection**:
   - Let baoyu-cover-image auto-select based on content signals, OR
   - Specify a style that matches the article tone:
     - `tech` - AI, coding, digital topics
     - `warm` - Personal stories, emotional content
     - `bold` - Controversial, attention-grabbing topics
     - `minimal` - Simple, zen-like content
     - `playful` - Fun, casual, beginner-friendly content
     - `nature` - Wellness, health, organic topics
     - `retro` - History, vintage, traditional topics
     - `elegant` - Business, professional content (default)

   **Special: Mom Reading Club Template**

   When using the `mom-reading-club` template, override the default cover style with **calligraphy & ink-wash illustration (书法水墨风)**:

   ```bash
   /baoyu-cover-image <article> --style minimal --no-title --custom-prompt "Chinese calligraphy and ink-wash illustration style (书法水墨风). Zen-like simplicity with generous white space (留白). Include subtle ink-wash brush strokes as background texture. Minimalist botanical elements (bamboo, plum blossoms, orchids, lotus) when appropriate. Color palette: ink black (#1a1a1a), warm gray (#666666), subtle gold accents (#C9A962), warm off-white background (#F5F3EE). If human figures are included, depict an elegant woman aged 30-45 with a contemplative, refined demeanor. NO TEXT on the cover."
   ```

3. **Use `--no-title` flag** since Xiaohongshu covers typically use visual-only images without embedded text.

4. **Move the generated image** to the correct location:
   - baoyu-cover-image saves to `imgs/cover.png` relative to the article
   - Move/copy to `~/Dev/obsidian/articles/<date>-<title>/_attachments/cover-xhs.png`

```bash
mv ~/Dev/obsidian/articles/<date>-<title>/imgs/cover.png ~/Dev/obsidian/articles/<date>-<title>/_attachments/cover-xhs.png
```

### Step 5: Generate HTML

**⚠️ COMPLIANCE CHECK**: Before generating HTML, review the text content for compliance:
- No absolute/superlative claims (最好、第一、国家级、最高级、全网最低价)
- No exaggerated effect claims (一分钟见效、吃完就变白)
- No false or unverified medical/financial advice
- No defamatory or offensive language
- If health/investment topics are involved, add disclaimer text

Using the prompt template and the user's content:

1. **Parse the content** to identify:
   - Title (h1)
   - Subtitles (h2-h6)
   - Paragraphs
   - Lists
   - Code blocks
   - Links
   - Emphasis/bold text
   - Blockquotes

2. **Generate complete HTML** following the template specifications:
   - Dark gradient background
   - 600px × 800px cream-colored card
   - Proper typography with Google Fonts (Noto Serif SC, Inter, JetBrains Mono)
   - Cover image at the top
   - All specified styling for text, links, lists, code blocks, etc.
   - Responsive design for mobile

3. **Important HTML Structure**:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Article Title</title>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@700&family=Inter:wght@300;400;700;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        /* All CSS styles inline */
    </style>
</head>
<body>
    <div class="container">
        <img src="_attachments/cover-xhs.png" class="cover-image" alt="Cover">
        <div class="content">
            <!-- Article content -->
        </div>
    </div>
</body>
</html>
```

4. **Save the HTML** to `~/Dev/obsidian/articles/<date>-<title>/xhs-preview.html`

### Step 6: Take Screenshots

After generating the HTML, capture sequential screenshots of the `.container` element at **exact 3:4 aspect ratio**:

**Screenshot Specifications:**
- Container viewport: 600px × 800px (3:4 ratio)
- Output resolution: 1200px × 1600px (2x device scale factor)
- Each screenshot captures exactly the `.container` element, not the full page

**Capture Process:**

1. **Open the HTML page** using Playwright browser with viewport larger than container
2. **Configure browser context**:
   - Viewport: 800px × 1000px (larger than container to ensure full visibility)
   - Device scale factor: 2x for high-resolution output
3. **Scroll within the container**:
   - The `.container` element has `overflow-y: auto`, making it internally scrollable
   - Start from `scrollTop = 0` and increment through the content
   - Each scroll position captures one 3:4 ratio screenshot
4. **Smart text boundary detection**:
   - Before each screenshot, analyze visible block elements (p, h1-h6, li, blockquote, pre, img)
   - If an element would be cut at the bottom boundary, end the current screenshot before that element
   - Add whitespace mask to cover partial content, maintaining clean 3:4 frame
   - Next screenshot starts with the cut element at the top
5. **Capture the complete `.container` content**:
   - Use `container.screenshot()` to capture only the container element (excludes page background)
   - Continue until all content is captured (scrollTop reaches scrollHeight - clientHeight)
6. **Save screenshots** to `~/Dev/obsidian/articles/<date>-<title>/_attachments/`:
   - Sequential naming: `xhs-01.png`, `xhs-02.png`, `xhs-03.png`, etc.

**Use the screenshot script:**

```bash
cd {{SKILL_DIR}} && python scripts/screenshot.py ~/Dev/obsidian/articles/<date>-<title>/xhs-preview.html
```

**Script Output:**
- Each screenshot: exactly 1200×1600 pixels (3:4 ratio at 2x scale)
- Only the cream-colored card content is captured
- No text is cut off between screenshots

### Step 7: Report Results

After completion, report to the user:
- HTML file location
- Number of screenshots generated
- Screenshots folder location
- Preview of the first screenshot (if possible)

## Directory Structure

```
{{SKILL_DIR}}/
├── SKILL.md              # This file
├── prompts/
│   └── default.md        # Default HTML/CSS styling prompt
├── scripts/
│   └── screenshot.py     # Screenshot capture script
└── .gitignore

Output directory (outside skill folder):
~/Dev/obsidian/articles/<date>-<title>/
├── xhs-preview.html          # Styled HTML preview page
├── imgs/                     # Created by baoyu-cover-image
│   ├── prompts/
│   │   └── cover.md          # Cover image prompt
│   └── cover.png             # Generated cover (moved to _attachments/)
└── _attachments/             # Obsidian-style attachments folder
    ├── cover-xhs.png         # Cover image (moved from imgs/cover.png)
    ├── xhs-01.png            # Screenshot page 1 (1200×1600)
    ├── xhs-02.png            # Screenshot page 2
    └── ...
```

## Dependencies

This skill depends on:
- `/baoyu-cover-image` skill for cover image generation (must be installed in `~/.claude/skills/`)

## Example Workflow

**User:** Create a styled article page from this markdown:

```markdown
# My Article Title

This is the introduction paragraph...

## Section 1

Content for section 1...
```

**Assistant Actions:**
1. Read prompt template from `prompts/default.md`
2. Extract title: "My Article Title"
3. Create output folder: `~/Dev/obsidian/articles/2024-01-14-my-article-title/`
4. Invoke `/baoyu-cover-image` skill with `--no-title` flag to generate cover image
5. Move generated cover from `imgs/cover.png` to `_attachments/cover-xhs.png`
6. Generate styled HTML following template specifications
7. Save to `~/Dev/obsidian/articles/2024-01-14-my-article-title/xhs-preview.html`
8. Open in browser and take 3:4 ratio screenshots
9. Save screenshots to `~/Dev/obsidian/articles/2024-01-14-my-article-title/_attachments/xhs-01.png`, etc.
10. Report completion with file locations

## Custom Prompt Templates

Users can provide custom prompt templates by:
1. Placing a `.md` file in the `prompts/` directory
2. Specifying the template name when invoking the skill

Example: "Use the `xiaohongshu-style` template for this article"

### Available Templates

| Template | Description | Best For |
|----------|-------------|----------|
| `default` | Standard style with New Yorker-style illustrations | General articles |
| `mom-reading-club` | Calligraphy & ink-wash style with TsangerJinKai02 font | Mom Reading Club (妈妈读书会) brand content |

### Mom Reading Club Template

Use this template for all "Mom Reading Club" branded content:

```
/xiaohongshu-images <article> --template mom-reading-club
```

**Features:**
- **Font**: TsangerJinKai02 (仓耳今楷02) for titles - requires local installation
- **Cover style**: Chinese calligraphy & ink-wash illustration (书法水墨风)
- **Aesthetic**: Zen simplicity, elegant restraint, generous white space
- **Color accent**: Subtle gold (#C9A962)
- **Target audience**: Cultured mothers aged 30-45

## Error Handling

If the `/baoyu-cover-image` skill fails:
1. Display the error message to the user
2. Offer to retry or proceed without cover image
3. If proceeding without image, use a placeholder or omit the cover

If screenshot capture fails:
1. Verify the HTML file exists and is valid
2. Check browser dependencies
3. Report the specific error to the user

## System Requirements

This skill requires:
- Python 3.8+
- Playwright for screenshot capture (installed via pip: `pip install playwright && playwright install chromium`)
- `/baoyu-cover-image` skill installed in `~/.claude/skills/`

Install dependencies:

```bash
pip install playwright
playwright install chromium
```

## Notes

- The skill preserves all original content exactly as provided
- No modifications, simplifications, or deletions to the content
- The cover image is generated based on the article's main theme
- Screenshots are optimized for Xiaohongshu's 3:4 aspect ratio
- Text is never cut off in screenshots - boundaries are adjusted intelligently

## Community Compliance (社区规范合规)

**IMPORTANT**: All generated content must comply with Xiaohongshu community guidelines.

### Quick Reference - Prohibited Content:

| Category | Examples | Action |
|----------|----------|--------|
| Absolute claims | 最好、最佳、第一、国家级 | Remove or rephrase |
| Exaggerated effects | 一分钟见效、立刻瘦10斤 | Remove or add disclaimers |
| Medical/Financial advice | Health tips, investment suggestions | Add disclaimer: "本内容不构成医疗/投资建议" |
| Inappropriate imagery | Nudity, violence, political symbols | Regenerate with appropriate content |
| False information | Pseudoscience, unverified claims | Verify or remove |
| Defamatory content | Attacks on brands/individuals | Remove entirely |

### Official Guidelines:

- 社区规范: https://www.xiaohongshu.com/crown/community/rules
- 社区公约: https://www.xiaohongshu.com/crown/community/agreement

### Compliance Workflow:

1. **Before image generation**: Review theme for appropriateness
2. **Before HTML generation**: Scan text for prohibited phrases
3. **Before final output**: Run through compliance checklist in prompt template (Section 11.5)
