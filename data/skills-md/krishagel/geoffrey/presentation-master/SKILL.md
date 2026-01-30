---
name: presentation-master
description: World-class presentation creation embodying principles from Garr Reynolds, Nancy Duarte, Guy Kawasaki, Seth Godin, and TED
triggers:
  - "create presentation"
  - "make presentation"
  - "build presentation"
  - "design deck"
  - "make slides"
  - "create slides"
  - "build deck"
  - "presentation for"
  - "slides for"
allowed-tools: Read, Write, Bash, WebSearch, Skill, AskUserQuestion
version: 1.0.0
---

# Presentation Master

World-class presentation creation skill that embodies best practices from presentation masters and adapts to your needs.

## Philosophy

**Key Innovation**: This isn't just a presentation generator—it's a presentation *coach* that teaches world-class design while creating slides.

Principles from:
- **Garr Reynolds** (Presentation Zen) - Simplicity and visual storytelling
- **Nancy Duarte** (Resonate) - Story structure and audience as hero
- **Guy Kawasaki** - 10/20/30 rule (10 slides, 20 minutes, 30pt fonts)
- **Seth Godin** - 6 words maximum per slide
- **TED** - Visual-first, minimal text, high impact
- **Edward Tufte** - Data integrity and information design
- **Steve Jobs** - Rule of Three and surprise moments

## Workflow: Guided Creation with Checkpoints

### Phase 1: Discovery & Context Analysis

**User provides**: Topic + Audience + Duration

**Skill analyzes**:
- Presentation type (board update, keynote, training, TED-style)
- Audience level (technical, executive, general public)
- Key message and desired transformation
- Story framework recommendation

**Checkpoint 1**: Present 3 structure options with rationale → user approves

### Phase 2: Content Development

**Skill develops**:
- Research topic if needed (web search, Obsidian knowledge)
- Extract maximum 10 core concepts (Kawasaki rule)
- Apply "what is / what could be" alternation (Duarte)
- Draft slide outline with one concept per slide
- Identify slides needing visuals

**Checkpoint 2**: Present outline + visual plan → user approves

### Phase 3: Visual Strategy

**Skill proposes** for each visual slide:
- Image type (infographic, photo, diagram, data visualization)
- Visual concept/metaphor
- Aesthetic direction (colors from brand, style, mood)
- Estimated generation cost ($0.13-$0.24 per image)

**Checkpoint 3**: Present visual strategy → user approves images to generate

### Phase 4: Generation & Validation

**Skill executes**:
1. Generate approved images in parallel using image-gen skill
2. Build slides using selected adapter (PPTX/Google Slides/Canva)
3. Apply design rules automatically:
   - 30pt+ fonts minimum
   - <6 words per slide (Godin standard)
   - High contrast (4.5:1 minimum)
   - No bullet points
   - No paragraphs
4. Run validation scoring (0-100 scale)
5. Generate quality report

**Checkpoint 4**: Present presentation + quality report → user reviews

### Phase 5: Iteration & Refinement (if needed)

**Skill refines**:
- Apply requested changes
- Re-validate quality score
- Save final presentation to Obsidian Research folder
- Document learnings and metadata

## Validation Scoring (0-100)

### CRITICAL Violations (Auto-fail)
- Font size < 30pt
- >10 core concepts
- Bullet points detected
- Paragraphs (>2 consecutive sentences)
- Poor contrast ratio (<4.5:1)
- Default template usage

### WARNING Flags
- >6 words per slide
- >15 slides for 20-min presentation
- No images in presentation
- Text-heavy slides (>3 lines)
- Inconsistent fonts (>2 families)
- Low-resolution images

### Quality Score Breakdown
- **Simplicity** (10pts): Word count, visual clutter
- **Visual Dominance** (10pts): Image quality, text-to-visual ratio
- **Story Structure** (10pts): Narrative arc, emotional beats
- **One Idea/Slide** (10pts): Concept clarity
- **Typography** (8pts): Size, consistency
- **Layout** (7pts): Hierarchy, whitespace, alignment
- **Color/Contrast** (7pts): Readability, brand consistency
- **Media Quality** (8pts): Image resolution, relevance
- **Cognitive Load** (20pts): Mayer's 12 multimedia principles
- **Data Integrity** (10pts): Tufte principles (if data present)

**Target Score**: 85+ for high-quality presentations

## Slide Pattern Library

### Six Core Patterns

1. **Title Slide** - Minimal text, strong visual, sets tone
2. **One Big Idea** - Single word/number/image, max 6 words
3. **Visual + Caption** - Large high-quality image, short caption
4. **Data Visualization** - Charts following Tufte principles (maximize data-ink ratio)
5. **Timeline/Process** - Linear flow, minimal text per step
6. **Transition/Section Break** - Single word or phrase, signals shift

### Adaptive Pattern Selection

**Board/Executive Update**: Patterns 3, 4, 6 (data-focused, professional)
**Keynote/TED-style**: Patterns 1, 2, 3 (story-focused, visual-first)
**Training/Education**: Patterns 4, 5 (process-focused, clarity)
**Pitch/Demo**: Patterns 2, 3, 4 (impact-focused, evidence-based)

## Story Frameworks

### Nancy Duarte's Sparkline
- Alternate "what is" (current reality) with "what could be" (aspiration)
- Build tension through contrast between present and future
- End with transformation and new reality

### The Rule of Three (Steve Jobs)
- Break presentation into 3 main sections
- 3 key features/points per section
- Memorable and dramatic

### TED Structure
- Hook (first 30 seconds) - Grab attention
- Personal connection - Why this matters to you
- Core idea with evidence - The meat
- Call to action - What next
- Strong close - Never end with Q&A

## Output Format Support

### Current: PPTX (Phase 1)
- Uses existing pptx skill
- Direct PptxGenJS API for simple slides
- html2pptx.js for complex layouts
- Saves to Obsidian Research folder
- Generates quality validation report

### Coming: Google Slides (Phase 2)
- Google Slides API v1
- Integrates with google-workspace skill
- Supports all 3 accounts (psd, kh, hrg)
- Returns shareable link

### Future: Canva (Phase 3)
- Canva REST API
- Auto-apply brand kits
- Returns shareable link

## Image Generation Integration

### Intelligent Visual Recommendations

For each slide, analyzes:
- **Numeric data** → Infographic recommendation
- **Abstract concepts** → Conceptual image/metaphor (especially for keynotes)
- **Concrete examples** → Photo/realistic imagery
- **Processes/flows** → Diagram recommendation
- **Trends/comparisons** → Chart/data visualization

### Prompt Generation (6-Step Process)

From image-gen skill:
1. Extract narrative from slide content
2. Choose visual concept/metaphor
3. Apply aesthetic (brand colors, presentation style)
4. Construct detailed prompt
5. Execute generation
6. Validate output

### Cost Management
- Show total estimated cost before generating
- Allow opt-out of specific images
- Cache generated images for reuse
- Track spending in presentation metadata

### Naming Convention
```
{presentation-id}-slide-{number}-{type}.png

Examples:
cybersecurity-2025-slide-02-threat-timeline.png
port-ai-2025-slide-04-breakthroughs.png
```

## Brand Integration

Automatically detects and applies branding:
- **PSD presentations**: Use psd-brand-guidelines skill (Sea Glass, Pacific, etc.)
- **Personal presentations**: Use personal brand (if defined)
- **Client presentations**: Custom brand kit (future)

Applies to:
- Color palettes
- Typography choices
- Logo placement
- Overall aesthetic

## Learning & Metadata Tracking

After each presentation, save metadata to Obsidian:

```json
{
  "presentation_id": "cybersecurity-2025-board",
  "type": "board-update",
  "audience": "school-board",
  "duration": "15min",
  "slides": 10,
  "quality_score": 91,
  "images_generated": 7,
  "generation_cost": 0.94,
  "validation_warnings": 1,
  "user_edits": ["slide-8-wording"],
  "effectiveness": "approved-minor-changes",
  "created": "2025-11-24",
  "tools_used": ["research", "image-gen", "pptx"],
  "learnings": "Board prefers data charts over concept graphics"
}
```

## Integration with Existing Skills

**Dependencies**:
- `image-gen` - Visual content generation
- `pptx` - PowerPoint creation (Phase 1)
- `google-workspace` - Google Slides (Phase 2)
- `psd-brand-guidelines` - Brand colors/logos
- `research` - Content development
- `obsidian-manager` - Knowledge storage

**Coordination Pattern**:
```
presentation-master (orchestrator)
├── calls research for content depth
├── calls image-gen for visuals
├── calls pptx/slides/canva adapter for output
├── calls psd-brand-guidelines for colors/logos
└── calls obsidian-manager to save final + metadata
```

## Usage Examples

### Example 1: Board Update
```
User: "Create presentation on cybersecurity trends for school board, 15 minutes"

Geoffrey: I'll create a board update presentation on cybersecurity trends.

**Context Analysis**
- Type: Board/Executive Update
- Audience: School board (non-technical)
- Duration: 15 minutes
- Purpose: Inform + Recommend action

**Recommended Structures**
1. Problem → Solution → Action (8 slides)
2. Current State → Trends → Implications → Recommendations (10 slides) ⭐
3. Story: Recent incident → Broader context → Our response (7 slides)

Which structure resonates?

[User selects #2]

**Draft Outline** (10 slides, one concept each)
1. Title: Cybersecurity Trends 2025
2. Current Threat Landscape [visual: threat timeline]
3. Trend 1: AI-Powered Attacks [visual: concept illustration]
4. Trend 2: Ransomware Evolution [visual: data chart]
5. Trend 3: Supply Chain Risks [visual: network diagram]
6. Impact on Education Sector [visual: stat infographic]
7. Our Current Posture [visual: assessment chart]
8. Gaps & Vulnerabilities [text-focused, high contrast]
9. Recommended Actions [visual: roadmap]
10. Investment & Timeline [visual: budget chart]

**Visual Strategy**
- 7 images recommended
- Estimated cost: $0.94 (2K resolution)
- Mix: 3 infographics, 2 charts, 1 diagram, 1 illustration

Approve and proceed?

[User approves]

Generating 7 visuals in parallel...
✓ All generated (0.94 total)

Building presentation with PSD brand colors...
Validating against best practices...

**Quality Score: 91/100**
✓ All fonts 36pt+
✓ Avg 4.2 words/slide
✓ High contrast (8.5:1)
✓ Story arc present
✓ Cognitive load optimized
⚠ Slide 8 has 7 words (rec: 6 max)

Created: /Obsidian/Research/cybersecurity-trends-2025-board.pptx
```

### Example 2: Keynote
```
User: "Create keynote on future of education for conference, 30 minutes"

Geoffrey: I'll create a TED-style keynote on the future of education.

**Context Analysis**
- Type: Keynote/TED-style
- Audience: Education professionals + parents
- Duration: 30 minutes
- Purpose: Inspire + Shift perspective

**Recommended Structures** (Nancy Duarte's Sparkline)
1. What education is today → What it could be → Transformation (12 slides) ⭐
2. Steve Jobs Rule of Three: Past → Present → Future (9 slides)
3. Hero's Journey: Problem → Trials → New reality (10 slides)

Which framework?

[Continues with guided creation...]
```

## Quality Checklist

Before presenting to user, verify:

**Content**
- [ ] One main idea per slide
- [ ] Clear story arc (beginning/middle/end)
- [ ] Audience positioned as hero
- [ ] Emotional connection established
- [ ] Maximum 10 core concepts

**Design**
- [ ] All fonts 30pt+ minimum
- [ ] High contrast (4.5:1+)
- [ ] No bullet points
- [ ] No paragraphs
- [ ] Maximum 6 words per slide (or justified exception)
- [ ] All images high-resolution
- [ ] Consistent fonts/colors/alignment
- [ ] No transitions or animations

**Data Visualization** (if applicable)
- [ ] Lie factor 0.95-1.05
- [ ] Maximum data-ink ratio
- [ ] Clear, detailed labeling
- [ ] No chart junk (3D effects, unnecessary borders)

**Structure**
- [ ] Follows chosen framework (Duarte/Jobs/TED)
- [ ] Creates tension and resolution
- [ ] Includes surprise/memorable moments
- [ ] Ends strong (not with Q&A)
- [ ] Appropriate length for time

## Advanced Features

### Context Detection

Automatically infers presentation type from cues:
- "board meeting" → Board update (data-focused)
- "keynote" or "conference" → Keynote (story-focused)
- "training" or "workshop" → Educational (process-focused)
- "pitch" or "investor" → Pitch (evidence-focused)

### Smart Defaults

Based on detected type:
- **Board update**: 10 slides, 8 with visuals, professional tone
- **Keynote**: 12-15 slides, minimal text, emotional arc
- **Training**: 15-20 slides, process diagrams, step-by-step
- **Pitch**: 10 slides (Kawasaki rule), data-driven, ROI focus

### Accessibility

Ensures presentations are accessible:
- High contrast text (4.5:1 minimum, aim for 7:1)
- Large fonts (30pt minimum, 36pt+ preferred)
- Clear hierarchy and flow
- Alt text for images (future enhancement)

## Limitations & Future Enhancements

**Current Limitations**:
- No animation support (by design - Godin principle)
- No video embedding yet (future enhancement)
- No speaker notes generation (Phase 2)
- No slide master editing (uses templates)

**Future Enhancements**:
- Auto-generate speaker notes from slide content
- Suggest rehearsal timing
- A/B test different structures
- Track presentation effectiveness scores
- Build personal pattern library from successful presentations

## References

Full principles documentation in:
- `principles/masters.md` - Expert best practices
- `principles/validation-rules.md` - Quality scoring system
- `principles/slide-patterns.md` - Template library
- `principles/story-frameworks.md` - Narrative structures

Scripts and adapters:
- `scripts/analyze-context.js` - Type detection
- `adapters/pptx-adapter.js` - PowerPoint output
- `adapters/slides-adapter.js` - Google Slides (Phase 2)
- `adapters/canva-adapter.js` - Canva (Phase 3)

---

**Remember**: The best presentations are simple, visual, story-driven, and focused on the audience's transformation—not the speaker's information.
