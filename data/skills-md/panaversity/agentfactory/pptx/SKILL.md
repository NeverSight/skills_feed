---
name: pptx
description: "Presentation creation, editing, and analysis. When Claude needs to work with presentations (.pptx files) for: (1) Creating new presentations, (2) Modifying or editing content, (3) Working with layouts, (4) Adding comments or speaker notes, or any other presentation tasks"
license: Proprietary. LICENSE.txt has complete terms
---

# PPTX creation, editing, and analysis

## Operating Contract (Read First — Non-Negotiables)

This skill must produce a **coherent story** and **faithful coverage** before it produces beautiful slides. If there is any conflict between sections of this SKILL.md, the rules in this section win.

### 1. Fidelity: No Invented Facts

- **No metrics, stats, ARR, pricing, or adoption numbers** unless they appear verbatim in source material
- If you need a number for illustration, mark it explicitly: "Example: ~$X (placeholder)" in speaker notes
- **If unsure whether a fact is in the source: omit it**

### 2. Scope Lock: Stay Inside the Chapter

The deck must cover the chapter's learning goals—nothing more.

**Forbidden topics** (unless explicitly in the chapter content):
- Business models, pricing strategies
- ARR, MAU, revenue projections
- "Sell today", "monetize", market sizing
- "Digital FTE economics" calculations
- Competitive landscape analysis

**If a slide drifts into forbidden territory: delete or rewrite it.**

### 3. One Narrative Spine (No Topic Whiplash)

Pick ONE spine and stick to it throughout:

| Spine Type | Flow |
|------------|------|
| **Teaching spine** | Problem → Concept → Mechanism → Workflow → Examples → Pitfalls → Summary → Next steps |
| **Chapter spine** | Hook → Learning objectives → Lesson-by-lesson (Concept → Example → Try) → Summary → CTA |

**Rules**:
- Every slide must map to exactly one spine step
- No A→B→A jumps (if you covered topic A, don't return to it later)
- If a slide doesn't fit the spine: **remove it or split into appropriate steps**

### 4. Coverage Requirement

**Required artifacts** before generating any PPTX file:

| Artifact | Purpose |
|----------|---------|
| `workspace/content-audit.md` | Research notes per lesson (existing) |
| `workspace/slide-outline.md` | Storyboard with titles as conclusions (existing) |
| `workspace/coverage-matrix.md` | Maps every lesson/objective to ≥1 slide |
| `workspace/semantic-qa.md` | Final coherence checklist |

**Coverage rules**:
- Every lesson must appear in at least one slide
- Every learning objective must be addressed
- If you can't cover everything: **add more slides**—don't shrink content
- Omissions must be explicitly justified in coverage-matrix.md

### 5. Semantic QA Gate (Must Pass Before Delivery)

Before generating the final presentation, complete `workspace/semantic-qa.md` with this checklist:

- [ ] Slide order follows chosen spine (no A→B→A jumps)
- [ ] Every slide has ONE clear takeaway matching the outline
- [ ] No new topics introduced that aren't in the approved outline
- [ ] All terminology is introduced before use
- [ ] No invented facts, metrics, or claims
- [ ] No forbidden topics (see Section 2)
- [ ] Coverage-matrix shows 100% lesson coverage

**If ANY check fails: revise and regenerate. Do NOT ship a failing presentation.**

### 6. Conflict Resolution Policy

When content doesn't fit a slide:

1. **Split into more slides** (preferred)
2. Move detail to speaker notes
3. Replace text with diagram/visual
4. Only then compress wording
5. **NEVER** shrink text below MIT typography minimums (24pt body, 40pt titles)

### 7. Standalone Framing (Default)

Unless explicitly requested otherwise, presentations should be **standalone**:

- ❌ **Wrong**: "Chapter 5: Claude Code Features" (assumes book context)
- ✅ **Correct**: "Claude Code: Your General Agent" (works for any audience)

**Rules**:
- No chapter/section/lesson numbers in titles
- No "as we discussed in Lesson X" references
- Presentation should work for someone who never read the source material
- If user wants educational context markers, they must explicitly request it

### 8. Approachable Language

Use language that invites rather than intimidates:

| ❌ Avoid | ✅ Use Instead |
|----------|---------------|
| "What You'll Master" | "By the End of This Session" |
| "Prerequisites you must know" | "What helps to know first" |
| "Advanced concepts" | "Deeper patterns" |
| "Expert techniques" | "Pro tips" |

**Tone**: Confident but welcoming. Never condescending, never gatekeeping.

### 9. Lead with Hook, Not Objectives

The first content slide must create curiosity, not list deliverables.

**Slide order**:
1. Title slide (compelling value proposition)
2. Hook slide (paradigm shift, provocative question, or "what if")
3. THEN learning objectives

❌ **Wrong opening**: Slide 2 = "What You'll Learn: 1. Install... 2. Configure..."
✅ **Correct opening**: Slide 2 = "What if one General Agent could build all your Custom Agents?"

---

## Overview

A user may ask you to create, edit, or analyze the contents of a .pptx file. A .pptx file is essentially a ZIP archive containing XML files and other resources that you can read or edit. You have different tools and workflows available for different tasks.

## Reading and analyzing content

### Text extraction
If you just need to read the text contents of a presentation, you should convert the document to markdown:

```bash
# Convert document to markdown
python -m markitdown path-to-file.pptx
```

### Raw XML access
You need raw XML access for: comments, speaker notes, slide layouts, animations, design elements, and complex formatting. For any of these features, you'll need to unpack a presentation and read its raw XML contents.

#### Unpacking a file
`python ooxml/scripts/unpack.py <office_file> <output_dir>`

**Note**: The unpack.py script is located at `skills/pptx/ooxml/scripts/unpack.py` relative to the project root. If the script doesn't exist at this path, use `find . -name "unpack.py"` to locate it.

#### Key file structures
* `ppt/presentation.xml` - Main presentation metadata and slide references
* `ppt/slides/slide{N}.xml` - Individual slide contents (slide1.xml, slide2.xml, etc.)
* `ppt/notesSlides/notesSlide{N}.xml` - Speaker notes for each slide
* `ppt/comments/modernComment_*.xml` - Comments for specific slides
* `ppt/slideLayouts/` - Layout templates for slides
* `ppt/slideMasters/` - Master slide templates
* `ppt/theme/` - Theme and styling information
* `ppt/media/` - Images and other media files

#### Typography and color extraction
**When given an example design to emulate**: Always analyze the presentation's typography and colors first using the methods below:
1. **Read theme file**: Check `ppt/theme/theme1.xml` for colors (`<a:clrScheme>`) and fonts (`<a:fontScheme>`)
2. **Sample slide content**: Examine `ppt/slides/slide1.xml` for actual font usage (`<a:rPr>`) and colors
3. **Search for patterns**: Use grep to find color (`<a:solidFill>`, `<a:srgbClr>`) and font references across all XML files

## Creating a new PowerPoint presentation **without a template**

When creating a new PowerPoint presentation from scratch, use the **html2pptx** workflow to convert HTML slides to PowerPoint with accurate positioning.

### Design Principles

**CRITICAL**: Before creating any presentation, analyze the content and choose appropriate design elements:
1. **Consider the subject matter**: What is this presentation about? What tone, industry, or mood does it suggest?
2. **Check for branding**: If the user mentions a company/organization, consider their brand colors and identity
3. **Match palette to content**: Select colors that reflect the subject
4. **State your approach**: Explain your design choices before writing code

**Requirements**:
- ✅ State your content-informed design approach BEFORE writing code
- ✅ Use web-safe fonts only: Arial, Helvetica, Times New Roman, Georgia, Courier New, Verdana, Tahoma, Trebuchet MS, Impact
- ✅ Create clear visual hierarchy through size, weight, and color
- ✅ Ensure readability: strong contrast, appropriately sized text, clean alignment
- ✅ Be consistent: repeat patterns, spacing, and visual language across slides

#### MANDATORY Design Declaration

Before writing ANY code, you MUST output a design declaration like this:

```
## Design Approach

**Content analysis**: This presentation covers [topic]. The content suggests [mood/tone/energy].

**Color palette**: [Palette name] because [reason tied to content]
- Primary: #XXXXXX — [purpose, e.g., "titles, key statements"]
- Accent 1: #XXXXXX — [purpose, e.g., "highlights, CTAs"]
- Accent 2: #XXXXXX — [purpose, e.g., "secondary elements"]
- Background: #XXXXXX — light for projection

**Visual approach**: [e.g., "Accent bars on left edge, colored by topic"]
```

❌ **NEVER skip this declaration** — jumping straight to code caused bland, forgettable presentations.

#### Color Anti-Patterns (NEVER DO)

| ❌ Anti-Pattern | Why It's Wrong | ✅ Do Instead |
|----------------|----------------|---------------|
| Navy (#1a1a2e) + Gray (#666) | "Corporate safe" = forgettable | Vibrant palette matching content |
| Default blue (#0066cc) | Looks like template placeholder | Intentional color with meaning |
| All black text on white | Zero visual energy | Colored titles, accent elements |
| Skipping declaration | Leads to autopilot choices | Always state approach first |

#### Color Palette Selection

**Choosing colors creatively**:
- **Think beyond defaults**: What colors genuinely match this specific topic? Avoid autopilot choices.
- **Consider multiple angles**: Topic, industry, mood, energy level, target audience, brand identity (if mentioned)
- **Be adventurous**: Try unexpected combinations - a healthcare presentation doesn't have to be green, finance doesn't have to be navy
- **Build your palette**: Pick 3-5 colors that work together (dominant colors + supporting tones + accent)
- **Ensure contrast**: Text must be clearly readable on backgrounds

**Example color palettes** (use these to spark creativity - choose one, adapt it, or create your own):

1. **Classic Blue**: Deep navy (#1C2833), slate gray (#2E4053), silver (#AAB7B8), off-white (#F4F6F6)
2. **Teal & Coral**: Teal (#5EA8A7), deep teal (#277884), coral (#FE4447), white (#FFFFFF)
3. **Bold Red**: Red (#C0392B), bright red (#E74C3C), orange (#F39C12), yellow (#F1C40F), green (#2ECC71)
4. **Warm Blush**: Mauve (#A49393), blush (#EED6D3), rose (#E8B4B8), cream (#FAF7F2)
5. **Burgundy Luxury**: Burgundy (#5D1D2E), crimson (#951233), rust (#C15937), gold (#997929)
6. **Deep Purple & Emerald**: Purple (#B165FB), dark blue (#181B24), emerald (#40695B), white (#FFFFFF)
7. **Cream & Forest Green**: Cream (#FFE1C7), forest green (#40695B), white (#FCFCFC)
8. **Pink & Purple**: Pink (#F8275B), coral (#FF574A), rose (#FF737D), purple (#3D2F68)
9. **Lime & Plum**: Lime (#C5DE82), plum (#7C3A5F), coral (#FD8C6E), blue-gray (#98ACB5)
10. **Black & Gold**: Gold (#BF9A4A), black (#000000), cream (#F4F6F6)
11. **Sage & Terracotta**: Sage (#87A96B), terracotta (#E07A5F), cream (#F4F1DE), charcoal (#2C2C2C)
12. **Charcoal & Red**: Charcoal (#292929), red (#E33737), light gray (#CCCBCB)
13. **Vibrant Orange**: Orange (#F96D00), light gray (#F2F2F2), charcoal (#222831)
14. **Forest Green**: Black (#191A19), green (#4E9F3D), dark green (#1E5128), white (#FFFFFF)
15. **Retro Rainbow**: Purple (#722880), pink (#D72D51), orange (#EB5C18), amber (#F08800), gold (#DEB600)
16. **Vintage Earthy**: Mustard (#E3B448), sage (#CBD18F), forest green (#3A6B35), cream (#F4F1DE)
17. **Coastal Rose**: Old rose (#AD7670), beaver (#B49886), eggshell (#F3ECDC), ash gray (#BFD5BE)
18. **Orange & Turquoise**: Light orange (#FC993E), grayish turquoise (#667C6F), white (#FCFCFC)

#### Visual Details Options

**Geometric Patterns**:
- Diagonal section dividers instead of horizontal
- Asymmetric column widths (30/70, 40/60, 25/75)
- Rotated text headers at 90° or 270°
- Circular/hexagonal frames for images
- Triangular accent shapes in corners
- Overlapping shapes for depth

**Border & Frame Treatments**:
- Thick single-color borders (10-20pt) on one side only
- Double-line borders with contrasting colors
- Corner brackets instead of full frames
- L-shaped borders (top+left or bottom+right)
- Underline accents beneath headers (3-5pt thick)

**Typography Treatments**:
- Extreme size contrast (72pt headlines vs 11pt body)
- All-caps headers with wide letter spacing
- Numbered sections in oversized display type
- Monospace (Courier New) for data/stats/technical content
- Condensed fonts (Arial Narrow) for dense information
- Outlined text for emphasis

**Chart & Data Styling**:
- Monochrome charts with single accent color for key data
- Horizontal bar charts instead of vertical
- Dot plots instead of bar charts
- Minimal gridlines or none at all
- Data labels directly on elements (no legends)
- Oversized numbers for key metrics

**Layout Innovations**:
- Full-bleed images with text overlays
- Sidebar column (20-30% width) for navigation/context
- Modular grid systems (3×3, 4×4 blocks)
- Z-pattern or F-pattern content flow
- Floating text boxes over colored shapes
- Magazine-style multi-column layouts

**Background Treatments**:
- Solid color blocks occupying 40-60% of slide
- Gradient fills (vertical or diagonal only)
- Split backgrounds (two colors, diagonal or vertical)
- Edge-to-edge color bands
- Negative space as a design element

### MIT-Standard Typography Requirements

**MANDATORY for all presentations. These are non-negotiable quality gates.**

#### Font Size Rules

| Element | Minimum | Recommended | Rationale |
|---------|---------|-------------|-----------|
| Slide titles | 40pt | 44pt | Visible from rear of large auditorium |
| Body text | 24pt | 28pt | MIT minimum for professional settings |
| Bullet text | 24pt | 28pt | Same as body—no smaller bullets |
| Code blocks | 18pt | 20pt | Monospace acceptable slightly smaller |
| Captions/footnotes | 16pt | 18pt | Only for non-critical details |

**Enforcement**: Before finalizing any slide, verify ALL text meets these minimums. If any text is below 24pt (except captions), increase it.

#### Content Density Rules

1. **ONE idea per slide** — Each slide has a single takeaway
2. **Max 4 bullets** — Stricter than MIT's 6 for impact
3. **Max 6 words per bullet** — Forces concision
4. **Max 50 words per slide** — Slides are visual aids, not documents
5. **Title as conclusion** — "Data proves X" not "Data Analysis"

#### Visual Hierarchy Principles

- **Size communicates importance**: Largest element = primary focus
- **Color restraint**: 3 colors maximum (plus black/white)
- **Strategic whitespace**: 20%+ padding creates breathing room
- **Light backgrounds**: Critical for projection (dark modes project poorly)
- **Consistent alignment**: Grid-based, predictable patterns

#### Self-Validation Checklist

Before delivering ANY presentation, verify:

- [ ] All titles are actionable conclusions (not labels)
- [ ] No text below 24pt (except captions)
- [ ] No slide has more than 4 bullets
- [ ] No bullet has more than 6 words
- [ ] At least 30% of slides have visual elements
- [ ] Color palette limited to 3 colors + black/white
- [ ] Light backgrounds throughout
- [ ] Code examples use syntax highlighting

### Creating "Spirited" Presentations

The difference between mechanical and engaging slides:

**Mechanical (avoid)**:
- Generic titles: "Introduction", "Overview", "Summary"
- Bullet dumps: 8+ items in a list
- Text-only: No diagrams or visual elements
- Uniform density: Every slide has same amount of content
- Default colors: Basic blue/gray without intention

**Spirited (target)**:
- Actionable titles: "Skills Reduce Output Drift by 80%"
- Focused content: 1 idea, 3-4 supporting points max
- Visual storytelling: Diagrams, flowcharts, comparisons
- Adaptive density: More slides for complex topics
- Intentional colors: Match layer/topic/mood

#### The "Spirit" Test

Before finalizing, ask:
1. Could someone understand the key message from titles alone?
2. Does each slide have a clear visual focal point?
3. Would this look professional at a KubeCon/Strange Loop talk?
4. Is there breathing room (whitespace) on every slide?

### Layout Tips
**When creating slides with charts or tables:**
- **Two-column layout (PREFERRED)**: Use a header spanning the full width, then two columns below - text/bullets in one column and the featured content in the other. This provides better balance and makes charts/tables more readable. Use flexbox with unequal column widths (e.g., 40%/60% split) to optimize space for each content type.
- **Full-slide layout**: Let the featured content (chart/table) take up the entire slide for maximum impact and readability
- **NEVER vertically stack**: Do not place charts/tables below text in a single column - this causes poor readability and layout issues

### Workflow
1. **MANDATORY - READ ENTIRE FILE**: Read [`html2pptx.md`](html2pptx.md) completely from start to finish. **NEVER set any range limits when reading this file.** Read the full file content for detailed syntax, critical formatting rules, and best practices before proceeding with presentation creation.
2. Create an HTML file for each slide with proper dimensions (e.g., 720pt × 405pt for 16:9)
   - Use `<p>`, `<h1>`-`<h6>`, `<ul>`, `<ol>` for all text content
   - Use `class="placeholder"` for areas where charts/tables will be added (render with gray background for visibility)
   - **CRITICAL**: Rasterize gradients and icons as PNG images FIRST using Sharp, then reference in HTML
   - **LAYOUT**: For slides with charts/tables/images, use either full-slide layout or two-column layout for better readability
3. Create and run a JavaScript file using the [`html2pptx.js`](scripts/html2pptx.js) library to convert HTML slides to PowerPoint and save the presentation
   - Use the `html2pptx()` function to process each HTML file
   - Add charts and tables to placeholder areas using PptxGenJS API
   - Save the presentation using `pptx.writeFile()`
4. **Visual validation**: Generate thumbnails and inspect for layout issues
   - Create thumbnail grid: `python scripts/thumbnail.py output.pptx workspace/thumbnails --cols 4`
   - Read and carefully examine the thumbnail image for:
     - **Text cutoff**: Text being cut off by header bars, shapes, or slide edges
     - **Text overlap**: Text overlapping with other text or shapes
     - **Positioning issues**: Content too close to slide boundaries or other elements
     - **Contrast issues**: Insufficient contrast between text and backgrounds
   - If issues found, adjust HTML margins/spacing/colors and regenerate the presentation
   - Repeat until all slides are visually correct

## Editing an existing PowerPoint presentation

When edit slides in an existing PowerPoint presentation, you need to work with the raw Office Open XML (OOXML) format. This involves unpacking the .pptx file, editing the XML content, and repacking it.

### Workflow
1. **MANDATORY - READ ENTIRE FILE**: Read [`ooxml.md`](ooxml.md) (~500 lines) completely from start to finish.  **NEVER set any range limits when reading this file.**  Read the full file content for detailed guidance on OOXML structure and editing workflows before any presentation editing.
2. Unpack the presentation: `python ooxml/scripts/unpack.py <office_file> <output_dir>`
3. Edit the XML files (primarily `ppt/slides/slide{N}.xml` and related files)
4. **CRITICAL**: Validate immediately after each edit and fix any validation errors before proceeding: `python ooxml/scripts/validate.py <dir> --original <file>`
5. Pack the final presentation: `python ooxml/scripts/pack.py <input_directory> <office_file>`

## Creating a new PowerPoint presentation **using a template**

When you need to create a presentation that follows an existing template's design, you'll need to duplicate and re-arrange template slides before then replacing placeholder context.

### Workflow
1. **Extract template text AND create visual thumbnail grid**:
   * Extract text: `python -m markitdown template.pptx > template-content.md`
   * Read `template-content.md`: Read the entire file to understand the contents of the template presentation. **NEVER set any range limits when reading this file.**
   * Create thumbnail grids: `python scripts/thumbnail.py template.pptx`
   * See [Creating Thumbnail Grids](#creating-thumbnail-grids) section for more details

2. **Analyze template and save inventory to a file**:
   * **Visual Analysis**: Review thumbnail grid(s) to understand slide layouts, design patterns, and visual structure
   * Create and save a template inventory file at `template-inventory.md` containing:
     ```markdown
     # Template Inventory Analysis
     **Total Slides: [count]**
     **IMPORTANT: Slides are 0-indexed (first slide = 0, last slide = count-1)**

     ## [Category Name]
     - Slide 0: [Layout code if available] - Description/purpose
     - Slide 1: [Layout code] - Description/purpose
     - Slide 2: [Layout code] - Description/purpose
     [... EVERY slide must be listed individually with its index ...]
     ```
   * **Using the thumbnail grid**: Reference the visual thumbnails to identify:
     - Layout patterns (title slides, content layouts, section dividers)
     - Image placeholder locations and counts
     - Design consistency across slide groups
     - Visual hierarchy and structure
   * This inventory file is REQUIRED for selecting appropriate templates in the next step

3. **Create presentation outline based on template inventory**:
   * Review available templates from step 2.
   * Choose an intro or title template for the first slide. This should be one of the first templates.
   * Choose safe, text-based layouts for the other slides.
   * **CRITICAL: Match layout structure to actual content**:
     - Single-column layouts: Use for unified narrative or single topic
     - Two-column layouts: Use ONLY when you have exactly 2 distinct items/concepts
     - Three-column layouts: Use ONLY when you have exactly 3 distinct items/concepts
     - Image + text layouts: Use ONLY when you have actual images to insert
     - Quote layouts: Use ONLY for actual quotes from people (with attribution), never for emphasis
     - Never use layouts with more placeholders than you have content
     - If you have 2 items, don't force them into a 3-column layout
     - If you have 4+ items, consider breaking into multiple slides or using a list format
   * Count your actual content pieces BEFORE selecting the layout
   * Verify each placeholder in the chosen layout will be filled with meaningful content
   * Select one option representing the **best** layout for each content section.
   * Save `outline.md` with content AND template mapping that leverages available designs
   * Example template mapping:
      ```
      # Template slides to use (0-based indexing)
      # WARNING: Verify indices are within range! Template with 73 slides has indices 0-72
      # Mapping: slide numbers from outline -> template slide indices
      template_mapping = [
          0,   # Use slide 0 (Title/Cover)
          34,  # Use slide 34 (B1: Title and body)
          34,  # Use slide 34 again (duplicate for second B1)
          50,  # Use slide 50 (E1: Quote)
          54,  # Use slide 54 (F2: Closing + Text)
      ]
      ```

4. **Duplicate, reorder, and delete slides using `rearrange.py`**:
   * Use the `scripts/rearrange.py` script to create a new presentation with slides in the desired order:
     ```bash
     python scripts/rearrange.py template.pptx working.pptx 0,34,34,50,52
     ```
   * The script handles duplicating repeated slides, deleting unused slides, and reordering automatically
   * Slide indices are 0-based (first slide is 0, second is 1, etc.)
   * The same slide index can appear multiple times to duplicate that slide

5. **Extract ALL text using the `inventory.py` script**:
   * **Run inventory extraction**:
     ```bash
     python scripts/inventory.py working.pptx text-inventory.json
     ```
   * **Read text-inventory.json**: Read the entire text-inventory.json file to understand all shapes and their properties. **NEVER set any range limits when reading this file.**

   * The inventory JSON structure:
      ```json
        {
          "slide-0": {
            "shape-0": {
              "placeholder_type": "TITLE",  // or null for non-placeholders
              "left": 1.5,                  // position in inches
              "top": 2.0,
              "width": 7.5,
              "height": 1.2,
              "paragraphs": [
                {
                  "text": "Paragraph text",
                  // Optional properties (only included when non-default):
                  "bullet": true,           // explicit bullet detected
                  "level": 0,               // only included when bullet is true
                  "alignment": "CENTER",    // CENTER, RIGHT (not LEFT)
                  "space_before": 10.0,     // space before paragraph in points
                  "space_after": 6.0,       // space after paragraph in points
                  "line_spacing": 22.4,     // line spacing in points
                  "font_name": "Arial",     // from first run
                  "font_size": 14.0,        // in points
                  "bold": true,
                  "italic": false,
                  "underline": false,
                  "color": "FF0000"         // RGB color
                }
              ]
            }
          }
        }
      ```

   * Key features:
     - **Slides**: Named as "slide-0", "slide-1", etc.
     - **Shapes**: Ordered by visual position (top-to-bottom, left-to-right) as "shape-0", "shape-1", etc.
     - **Placeholder types**: TITLE, CENTER_TITLE, SUBTITLE, BODY, OBJECT, or null
     - **Default font size**: `default_font_size` in points extracted from layout placeholders (when available)
     - **Slide numbers are filtered**: Shapes with SLIDE_NUMBER placeholder type are automatically excluded from inventory
     - **Bullets**: When `bullet: true`, `level` is always included (even if 0)
     - **Spacing**: `space_before`, `space_after`, and `line_spacing` in points (only included when set)
     - **Colors**: `color` for RGB (e.g., "FF0000"), `theme_color` for theme colors (e.g., "DARK_1")
     - **Properties**: Only non-default values are included in the output

6. **Generate replacement text and save the data to a JSON file**
   Based on the text inventory from the previous step:
   - **CRITICAL**: First verify which shapes exist in the inventory - only reference shapes that are actually present
   - **VALIDATION**: The replace.py script will validate that all shapes in your replacement JSON exist in the inventory
     - If you reference a non-existent shape, you'll get an error showing available shapes
     - If you reference a non-existent slide, you'll get an error indicating the slide doesn't exist
     - All validation errors are shown at once before the script exits
   - **IMPORTANT**: The replace.py script uses inventory.py internally to identify ALL text shapes
   - **AUTOMATIC CLEARING**: ALL text shapes from the inventory will be cleared unless you provide "paragraphs" for them
   - Add a "paragraphs" field to shapes that need content (not "replacement_paragraphs")
   - Shapes without "paragraphs" in the replacement JSON will have their text cleared automatically
   - Paragraphs with bullets will be automatically left aligned. Don't set the `alignment` property on when `"bullet": true`
   - Generate appropriate replacement content for placeholder text
   - Use shape size to determine appropriate content length
   - **CRITICAL**: Include paragraph properties from the original inventory - don't just provide text
   - **IMPORTANT**: When bullet: true, do NOT include bullet symbols (•, -, *) in text - they're added automatically
   - **ESSENTIAL FORMATTING RULES**:
     - Headers/titles should typically have `"bold": true`
     - List items should have `"bullet": true, "level": 0` (level is required when bullet is true)
     - Preserve any alignment properties (e.g., `"alignment": "CENTER"` for centered text)
     - Include font properties when different from default (e.g., `"font_size": 14.0`, `"font_name": "Lora"`)
     - Colors: Use `"color": "FF0000"` for RGB or `"theme_color": "DARK_1"` for theme colors
     - The replacement script expects **properly formatted paragraphs**, not just text strings
     - **Overlapping shapes**: Prefer shapes with larger default_font_size or more appropriate placeholder_type
   - Save the updated inventory with replacements to `replacement-text.json`
   - **WARNING**: Different template layouts have different shape counts - always check the actual inventory before creating replacements

   Example paragraphs field showing proper formatting:
   ```json
   "paragraphs": [
     {
       "text": "New presentation title text",
       "alignment": "CENTER",
       "bold": true
     },
     {
       "text": "Section Header",
       "bold": true
     },
     {
       "text": "First bullet point without bullet symbol",
       "bullet": true,
       "level": 0
     },
     {
       "text": "Red colored text",
       "color": "FF0000"
     },
     {
       "text": "Theme colored text",
       "theme_color": "DARK_1"
     },
     {
       "text": "Regular paragraph text without special formatting"
     }
   ]
   ```

   **Shapes not listed in the replacement JSON are automatically cleared**:
   ```json
   {
     "slide-0": {
       "shape-0": {
         "paragraphs": [...] // This shape gets new text
       }
       // shape-1 and shape-2 from inventory will be cleared automatically
     }
   }
   ```

   **Common formatting patterns for presentations**:
   - Title slides: Bold text, sometimes centered
   - Section headers within slides: Bold text
   - Bullet lists: Each item needs `"bullet": true, "level": 0`
   - Body text: Usually no special properties needed
   - Quotes: May have special alignment or font properties

7. **Apply replacements using the `replace.py` script**
   ```bash
   python scripts/replace.py working.pptx replacement-text.json output.pptx
   ```

   The script will:
   - First extract the inventory of ALL text shapes using functions from inventory.py
   - Validate that all shapes in the replacement JSON exist in the inventory
   - Clear text from ALL shapes identified in the inventory
   - Apply new text only to shapes with "paragraphs" defined in the replacement JSON
   - Preserve formatting by applying paragraph properties from the JSON
   - Handle bullets, alignment, font properties, and colors automatically
   - Save the updated presentation

   Example validation errors:
   ```
   ERROR: Invalid shapes in replacement JSON:
     - Shape 'shape-99' not found on 'slide-0'. Available shapes: shape-0, shape-1, shape-4
     - Slide 'slide-999' not found in inventory
   ```

   ```
   ERROR: Replacement text made overflow worse in these shapes:
     - slide-0/shape-2: overflow worsened by 1.25" (was 0.00", now 1.25")
   ```

## Creating Thumbnail Grids

To create visual thumbnail grids of PowerPoint slides for quick analysis and reference:

```bash
python scripts/thumbnail.py template.pptx [output_prefix]
```

**Features**:
- Creates: `thumbnails.jpg` (or `thumbnails-1.jpg`, `thumbnails-2.jpg`, etc. for large decks)
- Default: 5 columns, max 30 slides per grid (5×6)
- Custom prefix: `python scripts/thumbnail.py template.pptx my-grid`
  - Note: The output prefix should include the path if you want output in a specific directory (e.g., `workspace/my-grid`)
- Adjust columns: `--cols 4` (range: 3-6, affects slides per grid)
- Grid limits: 3 cols = 12 slides/grid, 4 cols = 20, 5 cols = 30, 6 cols = 42
- Slides are zero-indexed (Slide 0, Slide 1, etc.)

**Use cases**:
- Template analysis: Quickly understand slide layouts and design patterns
- Content review: Visual overview of entire presentation
- Navigation reference: Find specific slides by their visual appearance
- Quality check: Verify all slides are properly formatted

**Examples**:
```bash
# Basic usage
python scripts/thumbnail.py presentation.pptx

# Combine options: custom name, columns
python scripts/thumbnail.py template.pptx analysis --cols 4
```

## Creating Presentations from Educational Chapters

When asked to create slides for a chapter (e.g., "make slides for Chapter 5"):

### Workspace Structure

All working files go in a `workspace/` directory (created in project root or specified location):

```
workspace/
├── content-audit.md      ← Phase 1: Research notes
├── slide-outline.md      ← Phase 2: Storyboard (user approves)
├── draft-v1.pptx         ← Phase 4: First draft
├── draft-v2.pptx         ← Phase 5: After fixes
├── review/               ← Phase 5: Thumbnail grids
│   └── thumbnails.jpg
└── [chapter]-slides.pptx ← Phase 6: Final delivery
```

### Phase 0: Resolve Chapter Path

**CRITICAL**: Follow the CHAPTER/PART RESOLUTION PROTOCOL from CLAUDE.md.

1. **Parse input**: `ch X` = Chapter X, `part X` = Part X, bare `X` = ASK USER
2. **Discover path via filesystem** (source of truth):
   ```bash
   # For chapter:
   ls -d apps/learn-app/docs/*/05-*/   # Chapter 5

   # For part:
   ls -d apps/learn-app/docs/05-*/     # Part 5
   ```
3. **Count content**:
   ```bash
   ls apps/learn-app/docs/02-AI-Tool-Landscape/05-*/*.md | wc -l
   ```
4. **Create workspace**: `mkdir -p workspace`
5. **Confirm with user** before proceeding

**Example**: "ch 5" → `ls -d apps/learn-app/docs/*/05-*/` → `02-AI-Tool-Landscape/05-claude-code-features-and-workflows/`

### Phase 1: Research & Discovery

**Goal**: Deeply understand content before any slide planning.

**Output**: Save to `workspace/content-audit.md`

1. **Read the chapter README** for learning objectives and scope
2. **Read each lesson completely** and take structured notes:
   ```markdown
   # Content Audit: [Chapter Name]

   **Chapter path**: [discovered path]
   **Total lessons**: [N]
   **Pedagogical layer**: [L1/L2/L3/L4]

   ---

   ## Lesson 1: [Title]
   - **Core concept**: [One sentence]
   - **Key takeaways**: [3-5 bullets]
   - **Needs diagram**: [Yes/No - what kind?]
   - **Memorable quote/example**: [If any]
   - **Word count**: [X words]

   ## Lesson 2: [Title]
   ...

   ---

   ## Narrative Arc
   - **Problem this chapter solves**: [...]
   - **The "aha moment"**: [...]
   - **What to remember a week later**: [...]
   ```
3. **Identify the narrative arc**:
   - What problem does this chapter solve?
   - What's the "aha moment"?
   - What should someone remember a week later?
4. **Note pedagogical layer** (L1-L4) from frontmatter

### Phase 2: Storyboard & Plan

**Goal**: Create a complete slide outline BEFORE generating any slides.

**Output**: Save to `workspace/slide-outline.md`

#### Step 2a: Determine Slide Budget

| Content Type | Slides per 1000 words | Character |
|--------------|----------------------|-----------|
| Conceptual (L1) | 6-8 | More diagrams, analogies |
| Procedural (L2) | 8-10 | Step-by-step visuals |
| Technical (L3-L4) | 5-7 | Code examples, architecture |

#### Step 2b: Draft Slide-by-Slide Outline

Create a detailed storyboard in `workspace/slide-outline.md`:

```markdown
# Chapter X Presentation Outline

**Total slides**: [N]
**Estimated duration**: [N slides × 1-2 min = X minutes]
**Primary color**: [Layer color]

## Opening (Slides 1-3)
1. **Title**: "[Chapter Title]" — [Type: Title]
2. **Hook**: "[Provocative question or problem statement]" — [Type: Hook]
3. **Roadmap**: "What you'll learn" — [Type: Concept, 3 bullets max]

## Lesson 1: [Title] (Slides 4-8)
4. **[Slide title as conclusion]** — [Type: Concept]
   - Key point 1
   - Key point 2
   - Visual: [diagram description]
5. **[Next conclusion]** — [Type: Comparison]
   - Left: [Option A]
   - Right: [Option B]
...

## Closing (Slides N-2 to N)
- **Summary**: "3 Things to Remember" — [Type: Summary]
- **Call to Action**: "[What to do next]" — [Type: Title]
```

#### Step 2c: Apply the "So What?" Test

For each slide in outline, ask:
- **What's the ONE takeaway?** (If unclear, split or cut)
- **Why does the audience care?** (Connect to their goals)
- **Could this be a visual instead?** (Prefer diagrams over bullets)

#### Step 2d: Get User Approval

**STOP and present the outline to the user:**
- Total slide count
- Narrative flow summary
- Any content you're omitting (and why)
- Questions about emphasis or audience

**Do NOT proceed to generation until user approves the outline.**

#### Step 2e: Create Coverage Matrix

After user approval, create `workspace/coverage-matrix.md` to verify complete coverage:

```markdown
# Coverage Matrix: [Chapter Name]

**Chosen spine**: [Teaching / Chapter]

| # | Lesson Title | Key Concepts | Slide(s) | Status |
|---|--------------|--------------|----------|--------|
| 1 | [Lesson 1 title] | [Main concepts] | 4, 5 | ✓ Covered |
| 2 | [Lesson 2 title] | [Main concepts] | 6, 7, 8 | ✓ Covered |
| ... | ... | ... | ... | ... |

## Learning Objectives Coverage

| Objective | Slide(s) | Status |
|-----------|----------|--------|
| [Objective 1] | 3 | ✓ |
| [Objective 2] | 5, 6 | ✓ |

## Omissions (must justify)

- None / [Reason for any excluded content]
```

**Rules**:
- Every lesson must have ≥1 slide
- Every learning objective must appear
- Omissions must be explicitly justified
- If coverage is incomplete: **add slides, don't compress**

### Phase 3: Apply Design System

#### Pedagogical Layer Colors

| Layer | Primary | Accent | Use For |
|-------|---------|--------|---------|
| L1 | #4472C4 (Blue) | #2E5C9A | Foundations, first exposure |
| L2 | #70AD47 (Green) | #548235 | AI collaboration |
| L3 | #9B59B6 (Purple) | #7D3C98 | Skills, MCP, automation |
| L4 | #ED7D31 (Orange) | #C65911 | Capstone, production code |

#### Slide Type Patterns

| Type | Use When | Visual Treatment |
|------|----------|-----------------|
| Title | Opening slide | Large centered text, layer color |
| Hook | Narrative opening | Quote or provocative question |
| Concept | Definition/framework | Diagram + 2-3 bullets max |
| Comparison | Contrasting options | Side-by-side table |
| Process | Step-by-step | Numbered path/flowchart |
| Example | Code/demo | Dark code block with output |
| Try-With-AI | Interactive prompt | Styled as chat/terminal card |
| Summary | Key takeaways | 3 numbered conclusions |

### Phase 4: Generate Draft

**Output**: Save to `workspace/draft-v1.pptx`

1. Generate slides following the approved outline
2. Apply MIT typography rules (24pt minimum, 4 bullets max)
3. Save as `workspace/draft-v1.pptx`

### Phase 5: Verification Loop (TWO-LAYER)

**This phase has TWO layers. Layer 1 (semantic) MUST pass before Layer 2 (visual).**

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│  Draft → Semantic QA → Pass? ─No─→ Revise outline/content            │
│              │                           │                           │
│             Yes                          │                           │
│              ↓                           │                           │
│        Thumbnails → Visual QA → Pass? ─No─→ Fix layout/typography    │
│              │                       │                               │
│             Yes                      │                               │
│              ↓                       │                               │
│            Done ←────────────────────┘                               │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

#### LAYER 1: Semantic Verification (Do This FIRST)

**Before generating thumbnails**, verify the presentation tells a coherent story.

##### Step 5a: Create Semantic QA Checklist

Create `workspace/semantic-qa.md`:

```markdown
# Semantic QA: [Chapter Name] Presentation

**Chosen spine**: [Teaching / Chapter]
**Date**: [YYYY-MM-DD]

## Checklist

| Check | Pass? | Issue (if any) |
|-------|-------|----------------|
| Slides follow chosen spine (no A→B→A jumps) | | |
| Each slide has ONE clear takeaway | | |
| No topics introduced outside approved outline | | |
| All terminology introduced before use | | |
| No invented facts, metrics, or claims | | |
| No forbidden topics (pricing, revenue, market size) | | |
| Coverage-matrix shows 100% lesson coverage | | |

## Slide-by-Slide Review

| Slide | Title | Spine Role | Takeaway | Issues |
|-------|-------|------------|----------|--------|
| 1 | | Title | | |
| 2 | | Hook | | |
| 3 | | Roadmap | | |
| ... | | | | |

## Flagged Issues

1. [Issue description and which slide]
2. ...

## Decision

- [ ] **PASS** — Ready for visual QA (Layer 2)
- [ ] **FAIL** — Must revise (see flagged issues above)
```

##### Step 5b: Evaluate Against Semantic Criteria

For each slide, verify:
1. **Spine alignment**: Does this slide belong in the narrative flow?
2. **Single takeaway**: Can you state the ONE point in one sentence?
3. **Source fidelity**: Is every fact traceable to chapter content?
4. **Scope compliance**: No forbidden topics (pricing, revenue, etc.)?

##### Step 5c: Fix Semantic Violations

If ANY semantic check fails:
1. Identify which slides violate which rules
2. Revise the outline if needed
3. Regenerate affected slides
4. Re-run Layer 1 until all checks pass

**Do NOT proceed to Layer 2 until Layer 1 passes.**

---

#### LAYER 2: Visual Verification

**Only after Layer 1 passes**, verify visual quality.

##### Step 5d: Generate Thumbnail Grid
```bash
python scripts/thumbnail.py workspace/draft-v1.pptx workspace/review --cols 4
```

##### Step 5e: Visual Inspection Checklist

Review each thumbnail and check:

| Check | Pass? | Fix Required |
|-------|-------|--------------|
| All titles are conclusions (not labels) | | |
| No text appears smaller than body text | | |
| No slide has more than 4 bullets | | |
| No bullet wraps to 2+ lines (too long) | | |
| Every slide has clear visual hierarchy | | |
| Light backgrounds throughout | | |
| Consistent color palette | | |
| No text cut off or overlapping | | |
| Adequate whitespace (not cramped) | | |

##### Step 5f: Fix Visual Violations

For each failed check:
1. Note the slide number and issue
2. Identify root cause (content too dense? font too small?)
3. Fix in source HTML/code
4. Regenerate affected slides

##### Step 5g: Iterate

Repeat Steps 5d-5f until:
- All visual checklist items pass
- Thumbnail review shows professional quality
- Would pass the "KubeCon talk" test

### Phase 6: Final Delivery

**Output**: Save to `workspace/[chapter-name]-slides.pptx`

1. Rename `workspace/draft-vN.pptx` to `workspace/[chapter-name]-slides.pptx`
2. Generate final thumbnail grid for user review:
   ```bash
   python scripts/thumbnail.py workspace/[chapter-name]-slides.pptx workspace/final --cols 4
   ```
3. Present to user with:
   - Final slide count
   - Any deviations from approved outline (and why)
   - Thumbnail grid image (`workspace/final-thumbnails.jpg`)

### Common Mistakes to Avoid

These mistakes caused real presentation failures. Don't repeat them.

| Mistake | What Happened | Prevention |
|---------|---------------|------------|
| **Skipping design declaration** | Jumped to code → bland navy/gray colors | ALWAYS output design approach FIRST |
| **Using "Chapter X" in title** | Not standalone, assumes book context | Frame for ANY audience unless told otherwise |
| **Opening with objectives** | Dry, no hook, audience disengages | Lead with paradigm shift or provocative question |
| **Academic language** | "Master", "prerequisites" sounds gatekeeping | Use welcoming language: "By the end..." |
| **Default colors** | Navy + gray = corporate template look | Vibrant, intentional palette matching content |
| **Skipping thumbnail review** | Visual issues caught only by user | Generate + inspect thumbnails before delivery |
| **Abbreviated semantic QA** | Missed coverage gaps, spine violations | Complete FULL slide-by-slide audit |
| **Using python-pptx directly** | Manual positioning, harder to iterate | Prefer html2pptx for new presentations |

**Rule**: If user has to correct design/framing issues, the skill failed. These should be right on first delivery.

## Converting Slides to Images

To visually analyze PowerPoint slides, convert them to images using a two-step process:

1. **Convert PPTX to PDF**:
   ```bash
   soffice --headless --convert-to pdf template.pptx
   ```

2. **Convert PDF pages to JPEG images**:
   ```bash
   pdftoppm -jpeg -r 150 template.pdf slide
   ```
   This creates files like `slide-1.jpg`, `slide-2.jpg`, etc.

Options:
- `-r 150`: Sets resolution to 150 DPI (adjust for quality/size balance)
- `-jpeg`: Output JPEG format (use `-png` for PNG if preferred)
- `-f N`: First page to convert (e.g., `-f 2` starts from page 2)
- `-l N`: Last page to convert (e.g., `-l 5` stops at page 5)
- `slide`: Prefix for output files

Example for specific range:
```bash
pdftoppm -jpeg -r 150 -f 2 -l 5 template.pdf slide  # Converts only pages 2-5
```

## Code Style Guidelines
**IMPORTANT**: When generating code for PPTX operations:
- Write concise code
- Avoid verbose variable names and redundant operations
- Avoid unnecessary print statements

## Dependencies

Required dependencies (should already be installed):

- **markitdown**: `pip install "markitdown[pptx]"` (for text extraction from presentations)
- **pptxgenjs**: `npm install -g pptxgenjs` (for creating presentations via html2pptx)
- **playwright**: `npm install -g playwright` (for HTML rendering in html2pptx)
- **react-icons**: `npm install -g react-icons react react-dom` (for icons)
- **sharp**: `npm install -g sharp` (for SVG rasterization and image processing)
- **LibreOffice**: `sudo apt-get install libreoffice` (for PDF conversion)
- **Poppler**: `sudo apt-get install poppler-utils` (for pdftoppm to convert PDF to images)
- **defusedxml**: `pip install defusedxml` (for secure XML parsing)

## Artifact Templates

Copy these templates when creating the required workspace artifacts.

### coverage-matrix.md Template

```markdown
# Coverage Matrix: [Chapter Name]

**Chapter path**: [apps/learn-app/docs/.../XX-chapter-name/]
**Chosen spine**: [Teaching / Chapter]
**Date**: [YYYY-MM-DD]

## Lesson Coverage

| # | Lesson Title | Key Concepts | Slide(s) | Status |
|---|--------------|--------------|----------|--------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| ... | | | | |

## Learning Objectives Coverage

| Objective (from chapter README) | Slide(s) | Status |
|---------------------------------|----------|--------|
| | | |
| | | |

## Omissions

List any content intentionally excluded and justify why:

- **None** — all content covered

OR

- **[Topic]**: [Reason for exclusion]

## Verification

- [ ] Every lesson has ≥1 slide
- [ ] Every learning objective is addressed
- [ ] All omissions are justified above
```

### semantic-qa.md Template

```markdown
# Semantic QA: [Chapter Name] Presentation

**Chosen spine**: [Teaching / Chapter]
**Date**: [YYYY-MM-DD]
**Reviewer**: Claude

## Semantic Checklist

| # | Check | Pass? | Issue (if failed) |
|---|-------|-------|-------------------|
| 1 | Slides follow chosen spine (no A→B→A jumps) | | |
| 2 | Each slide has ONE clear takeaway | | |
| 3 | No topics introduced outside approved outline | | |
| 4 | All terminology introduced before use | | |
| 5 | No invented facts, metrics, or claims | | |
| 6 | No forbidden topics (pricing, revenue, market size) | | |
| 7 | Coverage-matrix shows 100% lesson coverage | | |

## Slide-by-Slide Audit

| Slide | Title | Spine Role | Single Takeaway | Issues |
|-------|-------|------------|-----------------|--------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| ... | | | | |

## Flagged Issues

List all issues found during review:

1. [None found]

OR

1. **Slide X**: [Description of issue]
2. **Slide Y**: [Description of issue]

## Forbidden Topic Scan

Searched for and found:

- [ ] Business models / pricing → **Not found** / Found on slide(s): ___
- [ ] ARR / MAU / revenue → **Not found** / Found on slide(s): ___
- [ ] Market sizing → **Not found** / Found on slide(s): ___
- [ ] "Digital FTE economics" → **Not found** / Found on slide(s): ___

## Final Decision

- [ ] **PASS** — All semantic checks pass. Ready for Layer 2 (visual QA).
- [ ] **FAIL** — Issues found above must be fixed before proceeding.

### If FAIL, action plan:

1. [What needs to change]
2. [Which slides to regenerate]
```