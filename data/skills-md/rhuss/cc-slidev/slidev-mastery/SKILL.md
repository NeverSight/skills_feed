---
name: Slidev Mastery
description: This skill should be used when the user asks to "create slides with Slidev", "use Slidev syntax", "add Slidev components", "configure Slidev theme", "export Slidev presentation", or mentions Slidev-specific features like layouts, animations, Monaco editor, or code highlighting. Provides comprehensive Slidev expertise for markdown-based presentations.
version: 0.2.0
---

# Slidev Mastery

Slidev is a presentation framework for developers that uses markdown with Vue components. Create beautiful, interactive slides using familiar syntax with powerful features like live coding, diagrams, and animations.

**Evidence-based design**: This skill incorporates research-based best practices for accessible, effective presentations. See `references/presentation-best-practices.md` for full guidelines.

## Core Concepts

### Slide Separation

Separate slides with `---` on its own line:

```markdown
# First Slide

Content here

---

# Second Slide

More content
```

### Importing Slides from External Files

You can split your presentation into multiple markdown files using the `src` frontmatter option. This allows for better organization and reusability:

```markdown
# Normal slide

---
src: ./slides/introduction.md
---

---
# Another normal slide

---
src: ./slides/conclusion.md
---
```

**Benefits of modular slide structure:**
- **Stable identity:** Use meaningful filenames (e.g., `microservices-benefits.md`) instead of numbers
- **Easy reordering:** Move `src` includes in master file without renaming files
- **Independent editing:** Edit individual slide files separately
- **Better collaboration:** Team members can work on different slides simultaneously
- **Version control:** Meaningful file names in git diffs

**Example structure:**
```
presentation/
├── slides.md                      # Master file with includes
├── slides/
│   ├── 01-title.md                # Slide 1: Title
│   ├── 02-hook.md                 # Slide 2: Opening hook
│   ├── 03-problem-statement.md    # Slide 3: Problem introduction
│   ├── 04-architecture-overview.md # Slide 4: Architecture slide
│   ├── 18-conclusion.md           # Conclusion
│   └── 19-questions.md            # Q&A
└── public/images/
```

**File naming:** Individual slides use numeric prefix (01-, 02-, etc.) plus descriptive name for easy ordering in directory listings while maintaining meaningful names.

**Master file example with slide number comments:**
```markdown
---
theme: default
title: My Presentation
---

---
src: ./slides/01-title.md
---
<!-- Slide 1: Title -->

---
src: ./slides/02-hook.md
---
<!-- Slide 2: Opening Hook -->

---
src: ./slides/03-problem-statement.md
---
<!-- Slide 3: Problem Statement -->
```

**Note:** Comments must come AFTER the closing `---` (not inside frontmatter block) per Slidev specs.

**Frontmatter merging:** You can override frontmatter from external files:
```markdown
---
src: ./slides/content.md
layout: two-cols  # Overrides layout in content.md
---
```

### Frontmatter Configuration

Configure presentation globally in frontmatter at the top of `slides.md`:

```yaml
---
theme: default
background: https://source.unsplash.com/collection/94734566/1920x1080
class: text-center
highlighter: shiki
lineNumbers: false
drawings:
  persist: false
transition: slide-left
title: Welcome to Slidev
---
```

**Key frontmatter fields:**
- `theme`: Visual theme (default, seriph, apple-basic, etc.)
- `background`: Global background image or color
- `highlighter`: Code highlighting engine (shiki or prism)
- `lineNumbers`: Show line numbers in code blocks
- `transition`: Slide transition effect
- `title`: Presentation title for metadata

### Per-Slide Frontmatter

Configure individual slides with frontmatter after `---`:

```markdown
---
layout: center
background: './images/background.jpg'
class: 'text-white'
---

# Centered Slide

With custom background
```

## Layouts

Slidev provides built-in layouts for different slide types:

### Common Layouts

**`default`** - Standard layout with title and content:
```markdown
# Title

Content here
```

**`center`** - Centered content:
```markdown
---
layout: center
---

# Centered Title
```

**`cover`** - Cover slide for presentation start:
```markdown
---
layout: cover
background: './bg.jpg'
---

# Presentation Title

Subtitle or author
```

**`intro`** - Introduction slide:
```markdown
---
layout: intro
---

# Topic

Brief description
```

**`image-right`** - Content on left, image on right:
```markdown
---
layout: image-right
image: './diagram.png'
---

# Content

Text goes here
```

**`image-left`** - Image on left, content on right:
```markdown
---
layout: image-left
image: './photo.jpg'
---

# Content

Text goes here
```

**`two-cols`** - Two column layout:
```markdown
---
layout: two-cols
---

# Left Column

Content for left

::right::

# Right Column

Content for right
```

**`quote`** - Large quote display:
```markdown
---
layout: quote
---

# "Innovation distinguishes between a leader and a follower."

Steve Jobs
```

**`fact`** - Emphasize key fact or statistic:
```markdown
---
layout: fact
---

# 95%

User satisfaction rate
```

## Code Highlighting

### Basic Code Blocks

```markdown
\```python
def hello():
    print("Hello, World!")
\```
```

### Line Highlighting

Highlight specific lines with `{line-numbers}`:

```markdown
\```python {2-3}
def process():
    important_line()
    another_important()
    return result
\```
```

### Line Numbers

Enable line numbers for a code block:

```markdown
\```python {1|2|3} {lines:true}
first_line()
second_line()
third_line()
\```
```

### Monaco Editor

Enable live code editing with Monaco:

```markdown
\```python {monaco}
def editable():
    return "Users can edit this code"
\```
```

## Animations and Clicks

### Click Animations

Reveal content incrementally with `v-click`:

```markdown
- First point
- <v-click>Second point (appears on click)</v-click>
- <v-click>Third point (appears on next click)</v-click>
```

### After Clicks

Show content after specific click:

```markdown
<div v-after="2">
  Appears after 2 clicks
</div>
```

### Click Counting

Use click counters for complex animations:

```markdown
<div v-click="1">First</div>
<div v-click="2">Second</div>
<div v-click="3">Third</div>
```

## Mermaid Diagrams

Embed mermaid diagrams directly:

```markdown
\```mermaid
graph LR
    A[Start] --> B[Process]
    B --> C[End]
\```
```

**Supported diagram types:**
- Flowchart: `graph LR`, `graph TD`
- Sequence: `sequenceDiagram`
- Class: `classDiagram`
- State: `stateDiagram-v2`
- ER: `erDiagram`
- Gantt: `gantt`

### Custom Theme

Apply custom colors to mermaid diagrams:

```markdown
\```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#3b82f6'}}}%%
graph TD
    A[Blue themed]
\```
```

## Images and Media

### Images

```markdown
![Alt text](./path/to/image.jpg)
```

With custom size:

```markdown
<img src="./image.jpg" class="w-50 mx-auto" />
```

### Background Images

Per-slide background:

```markdown
---
background: './images/slide-bg.jpg'
---
```

## Presenter Notes

Add notes visible only in presenter mode:

```markdown
# Slide Title

Content visible to audience

<!--
These are presenter notes
Only visible in presenter mode
Press 'p' to toggle presenter view
-->
```

## Components

### Built-in Components

**Arrows**:
```markdown
<Arrow x1="100" y1="100" x2="200" y2="200" />
```

**YouTube**:
```markdown
<Youtube id="video-id" width="500" height="300" />
```

**Tweet**:
```markdown
<Tweet id="tweet-id" />
```

### Custom Components

Create reusable Vue components in `components/` directory:

```vue
<!-- components/CustomButton.vue -->
<template>
  <button class="custom-btn">
    <slot />
  </button>
</template>

<style scoped>
.custom-btn {
  background: #3b82f6;
  color: white;
  padding: 1rem 2rem;
  border-radius: 0.5rem;
}
</style>
```

Use in slides:

```markdown
<CustomButton>Click me</CustomButton>
```

## Themes

### Using Themes

Set in frontmatter:

```yaml
---
theme: seriph
---
```

**Popular themes:**
- `default` - Clean, minimal
- `seriph` - Elegant serif fonts
- `apple-basic` - Apple keynote style
- `shibainu` - Playful, colorful
- `bricks` - Modern, structured

### Custom Styling

Add custom CSS in frontmatter or separate `style.css`:

```markdown
---
---

<style>
h1 {
  color: #3b82f6;
}

.custom-class {
  background: linear-gradient(45deg, #3b82f6, #8b5cf6);
}
</style>
```

## Exporting

### PDF Export

```bash
slidev export slides.md --output presentation.pdf
```

### PPTX Export

```bash
slidev export slides.md --format pptx
```

### PNG Export (slides as images)

```bash
slidev export slides.md --format png --output slides/
```

## Development Workflow

### Start Dev Server

```bash
slidev slides.md
```

Opens at `http://localhost:3030` with hot reload.

### Build for Production

```bash
slidev build slides.md
```

Generates static HTML in `dist/` directory.

### Presenter Mode

Press `p` during presentation to enter presenter mode with notes and preview.

## Best Practices (Evidence-Based)

### Slide Content

**One idea per slide** (Critical):
- Each slide communicates exactly one central finding
- If explaining takes >2 minutes → split into multiple slides
- Slide title should state the one clear point

**Meaningful titles** (Critical):
- Use assertions, not labels: "API handles 10K req/sec" not "Performance"
- Format: subject + verb + finding
- Reading titles in sequence should tell the story

**Minimal text** (Critical):
- <50 words per slide (excluding title)
- Use keywords and phrases, not full sentences
- Put detailed explanations in presenter notes (not on slide)
- Remember: Audience cannot read and listen simultaneously

**Visual over text**:
- Almost never have text-only slides
- Use diagrams, charts, images, code
- Text-only acceptable only for: quotes, definitions, bold statements

**Cognitive load management**:
- Max 6 distinct elements per slide (bullets, images, diagrams, charts)
- If >6 needed, use progressive disclosure with `v-click`
- Example of elements: title + 1 diagram + 3 bullets = 5 ✓

**Progressive disclosure** - Use `v-click` for complex ideas:
```markdown
- Key point 1
- <v-click>Key point 2 (reveals on click)</v-click>
- <v-click>Key point 3 (reveals next)</v-click>
```
Prevents audience from reading ahead while you explain

### File Organization

```
presentation/
├── slides.md           # Main presentation
├── public/             # Static assets
│   └── images/
├── components/         # Custom Vue components
└── styles/            # Custom CSS
```

### Performance

- **Optimize images** - Compress before using
- **Lazy load** - Use v-after for heavy content
- **Limit animations** - Don't overuse transitions
- **Test export** - Verify PDF/PPTX render correctly

### Accessibility (Required)

**Font requirements** (from research):
- **Body text**: Minimum 18pt, ideally 18-24pt
- **Headings**: Minimum 24pt or larger
- **Font family**: Sans-serif for body (Arial, Helvetica, Verdana)
- **AVOID**: Italics, underlines, ALL CAPS in body text (reduces readability)

Configure in frontmatter or custom CSS:
```yaml
---
theme: default
---

<style>
/* Accessibility-focused defaults */
h1 { font-size: 3rem; }      /* ~48pt */
h2 { font-size: 2rem; }      /* ~32pt */
h3 { font-size: 1.5rem; }    /* ~24pt */
p, li { font-size: 1.25rem; } /* ~20pt */

body {
  font-family: 'Helvetica Neue', Arial, sans-serif;
}
</style>
```

**Color requirements**:
- **Contrast ratio**: Minimum 4.5:1 for normal text, 3:1 for large text (>24pt)
- **Colorblind-safe**: Use tools like ColorBrewer to verify palettes
- **Don't rely on color alone**: Add patterns, labels, or shapes
  - Example: In charts, use both color AND patterns/icons
- **Core scheme**: 2 main colors (one light, one dark), 1-2 accents

Test contrast:
```bash
# Online tools
# - WebAIM Contrast Checker
# - Colorblind Web Page Filter
```

**Layout requirements**:
- Adequate margins and white space
- Consistent layout across slides
- Clear section demarcation
- Alt text for all images (in presenter notes)

**Keyboard navigation**:
- Test presentation without mouse
- Arrow keys, space bar should work
- Presenter mode accessible via 'p' key

**Recommended accessible theme:**
```yaml
---
theme: default  # Good contrast, clean design
# OR create custom theme with accessibility defaults
---
```

## Common Patterns

### Title Slide

```markdown
---
layout: cover
background: './background.jpg'
---

# Presentation Title

## Subtitle

Author Name · Date
```

### Agenda Slide

```markdown
# Agenda

- <v-click>Introduction</v-click>
- <v-click>Main Topics</v-click>
- <v-click>Conclusion</v-click>
- <v-click>Q&A</v-click>
```

### Code Comparison

```markdown
---
layout: two-cols
---

# Before

\```python
old_code()
\```

::right::

# After

\```python
improved_code()
\```
```

### Diagram with Explanation

```markdown
---
layout: image-right
---

# Architecture

\```mermaid
graph TD
    A[Client]
    B[Server]
    A --> B
\```

::right::

Key points:
- Client initiates
- Server responds
- Simple flow
```

## Troubleshooting

### Slides not rendering

- Check markdown syntax (especially `---` separators)
- Verify frontmatter YAML is valid
- Ensure images paths are correct

### Code highlighting not working

- Verify highlighter is set (`shiki` or `prism`)
- Check language identifier in code block
- Ensure code block syntax is correct

### Export fails

- Install playwright browsers: `npx playwright install`
- Check for syntax errors in slides
- Verify all image paths are accessible

### Theme not applying

- Ensure theme is installed: `npm install slidev-theme-name`
- Check theme name spelling in frontmatter
- Restart dev server after theme installation

---

For more advanced features and detailed API documentation, consult Slidev official documentation at https://sli.dev
