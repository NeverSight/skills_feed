---
name: excalidraw-slides
description: This skill should be used when the user asks to "create slides", "make a PPT", "generate presentation", "create deck", "制作幻灯片", "生成演示文稿". Generates professional 16:9 presentation slides in Excalidraw JSON format.
metadata:
  version: 3.5.0
---

# Excalidraw Slide Generator

Transform text into professional Excalidraw slide decks (16:9 aspect ratio) using a **robotic, resumable 2-phase workflow**.

## Core Philosophy

Act as a **Presentation Designer**. The goal is not just to put text on a canvas, but to **visualize ideas**.
- **Extract Content**: Avoid copy-pasting. Summarize, simplify, and structure text into bullet points or punchy headlines.
- **Visual Hierarchy**: Use size, color, and position to guide the eye.
- **16:9 Canvas**: All work happens in 1600x900 pixel frames.

## Workflow (Resumable & Robust)

Follow this 2-phase process to ensure stability and fault tolerance.

### Phase 1: Planning (Outline)
**Trigger**: When the user provides a topic or content but **NO** project folder exists.

1.  **Read Content**: Analyze the user's input text.
2.  **Load System Prompt**: Read **`resources/prompt.md`** to understand the outlining strategy.
3.  **Create Project Folder**:
    - Generate a **kebab-case folder name** from the topic (2-4 words).
    - Example: "AI Coding Assistant" → `ai-coding-assistant/`
    - Example: "Climate Change Solutions" → `climate-change-solutions/`
    - Create this folder in the root directory.
4.  **Generate Outline**: Create **`slides_list.md`** inside the project folder.
    - This file must be a Markdown checklist (`- [ ]`).
    - Each item represents one slide.
    - Include nested bullets for **Narrative**, **Content**, **Visuals**, and **Layout** for EACH slide.
5.  **Stop**: Notify the user that the outline is ready for review.

### Phase 2: Execution (Generation)
**Trigger**: When `slides_list.md` exists in a project folder (either just created or user provided).

**Execution Strategy**: Use sub-agents for efficiency. You have two options:

#### Option A: Sequential Generation (Default)
- Generate one slide at a time
- Good for: Early validation, user feedback iterations

#### Option B: Batch Generation with Sub-Agent (Recommended for speed)
- Use Task tool to generate 2-3 slides in parallel
- Good for: Finalizing complete decks, faster iteration

**Batch Generation Workflow**:
1. Read next 2-3 unchecked items from `slides_list.md`
2. Call **Task tool** with `subagent_type="general-purpose"`
3. Prompt: "Generate these N slides following the workflow below. For each slide:
   - Read SKILL.md to understand Phase 2 execution steps
   - Generate Excalidraw JSON for each slide
   - Generate SVG illustration for each slide (theme is in the outline)
   - Save each slide file
   - Report back with file paths created"
4. Wait for completion and verify all files exist
5. Mark items as completed in `slides_list.md`

---

### Detailed Steps (for Sequential or Batch):

1.  **Locate Project**: Find the project folder containing `slides_list.md`.
2.  **Read Checklist**: Open `slides_list.md`.
3.  **Find Next Task**: LOCATE the **first unchecked item** (`- [ ]`) OR **next 2-3 unchecked items** (for batch).
    - *If all checked, stop.*
4.  **Generate Slide**:
    - Extract the details (Narrative, Content, Visuals, Layout) for that specific slide.
    - Select the matching layout from **`resources/slide-patterns.md`**.
    - Generate the Excalidraw JSON.

5.  **Generate SVG Illustration** (Always required - theme from outline):
    - Extract **SVG theme** from the "视觉画面" section in `slides_list.md`.
    - Read SVG prompt template from **`resources/svg-prompt.md`**.
    - **Use Task tool to generate SVG code**:
      * Call `Task` tool with `subagent_type="general-purpose"`
      * Prompt: "Read resources/svg-prompt.md. Using that template, generate SVG code for theme: '[EXTRACTED SVG THEME]'. Output ONLY the SVG code, no explanations."
      * Wait for completion and capture the output
      * Verify the output is valid SVG code (starts with `<svg`, contains `</svg>`)
    - Generate unique 32-character hexadecimal file ID (use `openssl rand -hex 16`).
    - Save SVG as **`[folder-name].illustration-[N].svg`** in project folder.
    - **Embed SVG in markdown file**:
      * Add `## Embedded Files` section between `## Text Elements` and `## Drawing`
      * Format: `[fileId]: [[filename.svg]]` (e.g., `e9c970134433484397edf4ca2699fd74355d9c22: [[ai-coding-assistant.illustration-01.svg]]`)
      * Add image element to JSON elements array with `fileId` matching the ID above
      * Keep `files` object as empty `{}`
    - See **examples/svg-embed-example.md** for complete reference

6.  **Save File**: Save as **`[folder-name].Slide-[N].excalidraw.md`** inside the project folder.
    - Example: `ai-coding-assistant/ai-coding-assistant.Slide-01.excalidraw.md`
    - **N** is the slide number (01, 02...).
7.  **Update Checklist**: Edit `slides_list.md` to mark items as **completed** (`- [x]`).
8.  **Loop**: **REPEAT** step 3-7 until you decide to stop for user feedback or finish all slides.

## Output Format (Slide Files)

**Follow this output structure precisely:**
> ⚠️ **CRITICAL: JSON Format Requirements**
> - The JSON output must be **valid JSON** without any comments
> - **DO NOT** use `//` comments inside the JSON block
> - **DO NOT** use trailing commas
> - **DO NOT** use unquoted keys
> - All strings must use double quotes `"` not single quotes `'`
> - **NO nested double quotes** in values: Use single quotes `'` inside text values
>   - ✅ Correct: `"text": "He said 'hello'"`
>   - ❌ Wrong: `"text": "He said \"hello\""` (causes JSON parsing errors)   

```markdown
---
excalidraw-plugin: parsed
tags: [excalidraw]
---
==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠== You can decompress Drawing data with the command palette: 'Decompress current Excalidraw file'. For more info check in plugin settings under 'Saving'

# Excalidraw Data

## Text Elements
%%
## Drawing
\`\`\`json
{JSON 完整数据}
\`\`\`
%%
```

## Coordinate System & Frames

- **Slide Size**: 1600 (width) x 900 (height).
- **Positioning**: Since files are separate, always place the Frame at `x: 0, y: 0`.
- **Frames**: Use Frame elements (`type: "frame"`) for all slides.
    - All elements for a slide must be visually inside the frame's bounds.
    - **Crucial**: element `frameId` must point to the parent frame's `id`.

## Styled Elements

### Typography
- **Font**: Use `fontFamily: 5` (Excalifont) for a hand-drawn look, or `1` (Virgil) if requested.
- **Sizes**:
    - **Title**: 60-80px
    - **Subtitle / Header**: 36-48px
    - **Body**: 20-28px
    - **Small**: 16px

### Colors (Theme) - "Warm Paper & Morandi"
Use this specific palette for all slides.
- **Canvas Background**: `#F0EEE6` (Warm Cream).
- **Text Main**: `#1A1A1A` (Charcoal).
- **Text Secondary**: `#4A4A4A` (Dark Gray).
- **Brand Accent**: `#D97757` (Terracotta) - for Headers, key highlights, buttons.
- **Card/Shape Backgrounds**:
    - *Sand*: `#EBE5D5` (Default for containers)
    - *Sage*: `#D1E0D7`
    - *Lavender*: `#D0D0E3`
    - *Soft Red*: `#E09F87`

## JSON Structure Template

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [
    {
      "id": "slide-frame",
      "type": "frame",
      "x": 0, "y": 0, "width": 1600, "height": 900,
      "name": "01 Title",
      "backgroundColor": "#F0EEE6"
    },
    {
       "id": "title-text",
       "type": "text",
       "x": 800, "y": 450,
       "text": "Presentation Title",
       "textAlign": "center",
       "strokeColor": "#1A1A1A",
       "frameId": "slide-frame"
    }
  ],
  "appState": { "viewBackgroundColor": "#F0EEE6" },
  "files": {}
}
```

## References

### Core Resources
- **[resources/prompt.md](resources/prompt.md)**: System prompt for generating the outline (emphasizes text hierarchy and layout over visuals).
- **[resources/slide-patterns.md](resources/slide-patterns.md)**: Standard layouts (Title, Content, Split, Grid).
- **[resources/excalidraw-schema.md](resources/excalidraw-schema.md)**: JSON element reference (colors, shapes, text).
- **[resources/svg-prompt.md](resources/svg-prompt.md)**: SVG illustration prompt template for Anthropic-style graphics.

### Examples
- **[examples/project-structure.md](examples/project-structure.md)**: Directory structure and file naming conventions.
- **[examples/slides_list.md](examples/slides_list.md)**: Sample outline file structure.
- **[examples/pitch-deck.md](examples/pitch-deck.md)**: Complete JSON example (3 slides).
- **[examples/svg-embed-example.md](examples/svg-embed-example.md)**: SVG embedding guide with file ID generation and positioning.
