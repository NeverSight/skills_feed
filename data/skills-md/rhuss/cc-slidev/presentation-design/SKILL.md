---
name: Presentation Design
description: This skill should be used when the user asks to "design a presentation", "structure presentation content", "improve presentation flow", "create presentation outline", "make slides more engaging", or needs guidance on storytelling, visual hierarchy, audience engagement, or presentation best practices.
version: 0.2.0
---

# Presentation Design

Effective presentations combine research-backed design principles, storytelling, and audience understanding. Create compelling narratives that engage audiences and communicate ideas clearly.

**Research Basis**: These guidelines are based on cognitive load studies (Miller's Law), TED presentation research, MIT Communication Lab recommendations, and analysis of effective technical conference talks. They prevent common mistakes that make presentations hard to follow. See `references/presentation-best-practices.md` for detailed research citations.

## HARD LIMITS (Never Violate)

These are research-backed **maximum limits** that should NEVER be exceeded. If content exceeds these limits, you MUST split into multiple slides:

🔴 **MAX 6 elements** per slide (bullets + images + diagrams + code blocks combined)
🔴 **MAX 50 words** body text per slide (excluding title)
🔴 **MAX 1-2 code blocks** per slide (8-10 lines each)
🔴 **ONE idea** per slide (if multiple ideas → split slides)

**Why these are hard limits:**
- Cognitive load research: >6 elements exponentially increases audience confusion
- Reading vs listening interference: >50 words means audience stops listening
- Code complexity: >2 code examples creates comparison overhead

**When content doesn't fit:**
- ❌ **NEVER** compress or shrink to fit
- ❌ **NEVER** reduce font size below 18pt
- ✅ **ALWAYS** split into additional slides
- ✅ **ALWAYS** move details to presenter notes or backup slides

## Core Principles

### 1. One Idea Per Slide

**Critical Rule**: Each slide communicates exactly ONE central idea, finding, or question.

**Why this matters:**
- Prevents cognitive overload
- Maintains audience focus
- Enables clear narrative progression

**In practice:**
- If a slide requires >2 minutes to explain → split it
- Each slide title should state one clear point
- No tangential information on slides
- Content supports only the title's assertion

**Example:**
- ❌ Bad: One "Background" slide covering problem + impact + existing solutions
- ✅ Good: Three slides → "Problem X costs $Y annually" → "Existing solutions fail at scale" → "No current approach handles edge case Z"

### 2. Meaningful Titles (Assertions, Not Labels)

**Critical Rule**: Slide titles should state the TAKEAWAY, not just the topic.

**Why this matters:**
- Titles act as "topic sentences" for slides
- Reading titles in sequence tells the story
- Helps distracted audience members catch up
- Prevents speaker from losing train of thought

**Format:** Use complete assertion (subject + verb + finding), not one-word labels

**Examples:**
- ❌ Weak: "Results" / "Background" / "Thermal Images"
- ✅ Strong: "Experiment X demonstrates 2x performance gain" / "Current solutions fail under high-load conditions" / "Thermal images show electronics overheating"

**Validation**: Could audience understand main point from title alone?

### 3. Cognitive Load Management

**Critical Rule**: Limit distinct elements to ~6 items per slide maximum.

**Scientific basis:**
- Working memory: 7±2 items (Miller's Law)
- David JP Phillips research: >6 objects exponentially increases cognitive load

**Elements to count:**
1. Bullet points
2. Images/photos
3. Diagrams
4. Text blocks
5. Charts/graphs
6. Callout boxes

**If >6 elements needed:** Use progressive builds, split across slides, or simplify

### 4. Design for the Distracted Viewer

**Critical Rule**: Each slide must convey its message even if viewer doesn't hear your narration.

**Why this matters:**
- Audience zones out momentarily (long sessions, after lunch)
- Slides may be reviewed later without audio
- Someone glancing mid-explanation should grasp the point

**Implementation:**
- Meaningful title + clear visual = standalone message
- Highlight conclusions, not just raw data
- Use annotations (arrows, labels) to guide attention
- Don't bury insights in details

**Test**: Show slide to someone without context. Can they identify main point in 5 seconds?

### 5. Minimal Text (Keywords, Not Sentences)

**Critical Rule**: Aside from title, use short phrases. Slides are visual aids, not scripts.

**Why this matters:**
- Audience cannot read and listen simultaneously (dual-channel interference)
- Reading text aloud loses engagement
- Text should guide, not duplicate speech

**Guidelines:**
- Word count per slide (excluding title): <50 words
- No paragraphs or full sentences in body
- Bullets are phrases, not complete sentences
- **Detailed text belongs in presenter notes**

**Example:**
- ✅ Good: "Key benefits: • 40% faster • 2x throughput • Zero downtime"
- ❌ Bad: "The key benefits of this approach are that it is 40% faster than the previous solution, provides twice the throughput, and enables zero-downtime deployments."

### 6. Backup Slides Strategy

**Rule**: Prepare "backup" slides for Q&A, but keep separate from main deck.

**What to include:**
- Detailed data tables
- Extended methodology
- Statistical details
- Alternative approaches considered
- Related work comparison

**Benefits:**
- Keeps main presentation focused
- Maintains timing discipline
- Shows thoroughness without cluttering talk

**Implementation:** Place after "Questions?" slide, don't count toward timing

## Presentation Structure

### Three-Act Structure

Every presentation follows a narrative arc:

**Act 1: Setup** (15-20% of time)
- Hook the audience immediately
- State the problem or opportunity
- Establish credibility
- Preview what's coming

**Act 2: Confrontation** (60-70% of time)
- Present main content
- Build tension or complexity
- Provide evidence and examples
- Address counterarguments

**Act 3: Resolution** (15-20% of time)
- Synthesize key points
- Provide clear takeaways
- Call to action
- Leave lasting impression

### Slide Sequence Pattern

```
1. Title/Cover - Who, what, when
2. Hook - Compelling question or statistic
3. Problem - Why this matters
4. Agenda - What to expect
5-N. Content - Main material
N+1. Summary - Key takeaways
N+2. Next Steps - What to do
N+3. Q&A - Questions
```

## Storytelling Principles

### Start with Why

Lead with purpose, not process:

❌ **Wrong:**
```
Slide 1: About Our Company
Slide 2: Our Technology
Slide 3: How It Works
Slide 4: Why You Should Care
```

✅ **Right:**
```
Slide 1: The Problem Everyone Faces
Slide 2: Why Current Solutions Fail
Slide 3: Our Approach
Slide 4: How It Works
```

### Use Concrete Examples

Abstract concepts need grounding:

❌ **Abstract:** "Our platform improves efficiency by 50%"

✅ **Concrete:** "Sarah used to spend 4 hours on reports. Now it takes 2 hours."

### Create Contrast

Highlight differences to make points memorable:

- Before vs After
- Problem vs Solution
- Old Way vs New Way
- Competitor vs Us

## Visual Hierarchy

### Text Density Guidelines

**Title slides:** 5-7 words maximum
**Content slides:** 20-30 words maximum
**Data slides:** Let visualizations speak, minimal text

**The 6x6 rule:**
- Maximum 6 bullet points per slide
- Maximum 6 words per bullet
- If you need more, split into multiple slides

### Typography

**Heading sizes:**
- H1 (Title): 44-60pt
- H2 (Section): 32-40pt
- H3 (Subsection): 24-28pt
- Body text: 18-24pt

**Font choices:**
- Sans-serif for screens (Arial, Helvetica, Open Sans)
- Limit to 2 font families maximum
- Use font weight for hierarchy (bold for emphasis)

### Color Strategy

**Color roles:**
- Primary: Main brand color (headlines, key elements)
- Secondary: Supporting color (accents, highlights)
- Neutral: Background and body text (black, white, gray)
- Accent: Call-to-action, warnings (sparingly)

**Contrast ratios:**
- Text on background: Minimum 4.5:1 ratio
- Large text (>24pt): Minimum 3:1 ratio
- Test readability from back of room

### White Space

Empty space is not wasted space:
- Margins: Minimum 10% of slide on all sides
- Between elements: At least 20-30px
- Around text blocks: Breathing room improves comprehension
- Resist urge to fill every pixel

## Slide Types

### Data Slides

**When showing numbers:**
- Use charts/graphs instead of tables when possible
- One data point per slide for maximum impact
- Highlight the insight, not just the data
- Remove chart junk (unnecessary gridlines, 3D effects)

**Chart selection:**
- Trends over time: Line chart
- Comparisons: Bar chart
- Proportions: Pie chart (limit to 5 segments)
- Correlations: Scatter plot
- Process flow: Flowchart diagram

### Concept Slides

**Explaining abstract ideas:**
- Use metaphors and analogies
- Visualize with diagrams
- Progressive disclosure (build complexity)
- One concept per slide

**Effective diagrams:**
- Flowcharts for processes
- Venn diagrams for relationships
- Pyramid/hierarchy for structures
- Timeline for sequences

### Transition Slides

**Between sections:**
- Section title only (large, centered)
- Progress indicator (Section 2 of 4)
- Visual separator
- Brief reset for audience

## Audience Engagement

### Opening Hooks

**Strong openings:**
- Provocative question
- Surprising statistic
- Personal story
- Demonstration
- Current event connection

❌ **Weak opening:** "Thanks for having me. Today I'll talk about..."

✅ **Strong opening:** "What if I told you 90% of your users never complete signup?"

### Pacing and Timing

**Default timing: 90 seconds (1.5 minutes) per slide** (configurable)

**Research basis:**
- PLOS Computational Biology: ~1 minute per slide
- Adjusted for technical content: 1.5 minutes more realistic

**Configurable pacing options:**
- **Fast (60s/slide)**: Brief updates, high-level overviews
- **Moderate (90s/slide)**: DEFAULT - technical content, balanced detail
- **Detailed (120s/slide)**: Complex topics, deep dives
- **Deep dive (180s/slide)**: Research talks, comprehensive analysis

**Duration calculations (at 90s/slide):**
- 10-minute presentation: ~6-7 slides
- 15-minute presentation: ~10 slides
- 20-minute presentation: ~13 slides
- 30-minute presentation: ~20 slides
- 45-minute presentation: ~30 slides

**Validation formula:**
```
Expected slides = (duration_minutes × 60) / seconds_per_slide
Acceptable range = expected ± 20%
```

**Adjust timing based on:**
- Content complexity (more complex → slower pace)
- Audience expertise (novices need more time)
- Interaction level (Q&A reduces slide count)
- Demo or video time (subtract from total)

**During practice:**
- If spending 2-3× target time on one slide → split it
- If rushing through slides → consolidate or cut
- Aim for consistency across slides

### Progressive Disclosure

Reveal information incrementally to maintain attention:

**Without progressive disclosure:**
```markdown
- Point 1
- Point 2
- Point 3
- Point 4
```
Audience reads ahead, misses your explanation.

**With progressive disclosure:**
```markdown
- Point 1
- <v-click>Point 2</v-click>
- <v-click>Point 3</v-click>
- <v-click>Point 4</v-click>
```
Control attention, maintain suspense.

### Interaction Patterns

**Rhetorical questions** - Encourage thinking
**Polls** - Gauge understanding
**Demonstrations** - Show, don't just tell
**Examples** - Make abstract concrete
**Challenges** - Pose problems to solve

## Content Organization

### The Pyramid Principle

Start with conclusion, then support:

```
Level 1: Main conclusion/recommendation
Level 2: Key supporting points (3-4)
Level 3: Evidence and data
Level 4: Details and examples
```

**Slide mapping:**
```
Slide 1: Main conclusion (what should they do?)
Slides 2-4: Three supporting reasons
Slides 5-N: Evidence for each reason
```

### Rule of Three

Human memory favors threes:
- 3 main points
- 3 examples
- 3 takeaways
- 3 action items

**Why three works:**
- Minimum for pattern recognition
- Maximum for immediate recall
- Feels complete and balanced

### Signposting

Help audience track progress:

**At section starts:**
- "First, let's look at..."
- "Now that we understand X, let's explore Y..."
- "The second challenge is..."

**At transitions:**
- "To summarize..."
- "This brings us to..."
- "Now for the key question..."

**At conclusions:**
- "In conclusion..."
- "The three takeaways are..."
- "What does this mean for you?"

## Visual Design Patterns

### Slide Layouts

**Full bleed image:** Photo takes entire slide, text overlay
**Split screen:** Content left, image/diagram right (or vice versa)
**Grid:** Multiple images or points in organized grid
**Centered:** Single element, maximum focus
**Quote:** Large text, minimal decoration

### Image Usage

**Image selection criteria:**
- Relevant to content (not decorative filler)
- High quality (minimum 1920x1080)
- Appropriate tone (professional, casual, technical)
- Diverse representation (inclusive imagery)

**Image sources:**
- Stock photos: Unsplash, Pexels (free, high-quality)
- Custom graphics: Diagrams, screenshots, data viz
- AI-generated: For specific concepts
- Icons: Consistent style throughout

**Placement guidelines:**
- Full bleed: Edge to edge, no borders
- Inset: Respect margins, consistent padding
- Background: Lower opacity (30-50%) for text overlay

### Consistency

Maintain throughout presentation:
- Color palette (2-3 colors)
- Font families (1-2 maximum)
- Icon style (outline vs filled)
- Diagram aesthetic
- Slide layout patterns

## Common Mistakes

### Information Overload

❌ **Too much:**
- Walls of text
- Tiny fonts
- Cluttered slides
- Too many points per slide

✅ **Right amount:**
- Key points only
- Large, readable fonts
- White space
- One idea per slide

### Reading Slides

❌ **Don't:**
- Put full sentences on slides
- Read slides verbatim
- Use slides as script

✅ **Do:**
- Use keywords and phrases
- Expand on points verbally
- Slides support, not replace, speech

### Inconsistency

❌ **Avoid:**
- Changing fonts between slides
- Different color schemes
- Mixed icon styles
- Varying alignment

✅ **Maintain:**
- Single template
- Consistent colors
- Uniform icon set
- Regular spacing

## Presentation Types

### Business Pitch

**Structure:**
1. Problem (market pain point)
2. Solution (your product)
3. Market opportunity (size)
4. Business model (how you make money)
5. Traction (proof it works)
6. Competition (why you win)
7. Team (who you are)
8. Ask (what you need)

**Style:** Professional, data-driven, confident
**Duration:** 10-20 minutes typical

### Technical Tutorial

**Structure:**
1. Prerequisites (what you need)
2. Problem context (why this matters)
3. Concepts (theory)
4. Implementation (how-to)
5. Examples (see it work)
6. Practice (try yourself)
7. Resources (learn more)

**Style:** Clear, step-by-step, code-heavy
**Duration:** 30-60 minutes typical

### Academic Presentation

**Structure:**
1. Background (context and literature)
2. Research question (what you studied)
3. Methods (how you studied it)
4. Results (what you found)
5. Discussion (what it means)
6. Conclusions (takeaways)
7. Future work (next steps)

**Style:** Formal, evidence-based, referenced
**Duration:** 15-45 minutes typical

### Conference Talk

**Structure:**
1. Hook (grab attention)
2. Personal connection (why you care)
3. Core idea (one big concept)
4. Supporting points (3-4 examples)
5. Implications (so what?)
6. Takeaway (remember this)

**Style:** Engaging, storytelling, memorable
**Duration:** 20-45 minutes typical

## Accessibility Considerations

### Visual Accessibility Requirements

**Font requirements** (from research):
- **Body text minimum**: 18-24pt (never smaller than 18pt)
- **Headings minimum**: 24pt or larger
- **Font family**: Sans-serif for body text (Calibri, Arial, Verdana, Helvetica)
- **Serif usage**: Optional for headings only (for differentiation)
- **AVOID**: Italics, underlines, ALL CAPS in body text (reduce readability)

**Color requirements:**
- **Contrast ratios**:
  - Normal text: Minimum 4.5:1 ratio
  - Large text (>24pt): Minimum 3:1 ratio
- **Colorblind-safe palettes**: Use ColorBrewer or similar tools to verify
- **Don't rely on color alone**: Add patterns, labels, or shapes for differentiation
- **Core color scheme**: 2 main colors (one light, one dark) for foundation
- **Accent colors**: 1-2 additional for highlighting

**Layout requirements:**
- Clear section demarcation
- Consistent layout across slides
- Adequate margins and white space
- Legible over varying backgrounds (add borders/frames if needed)

**Testing accessibility:**
- Preview slides from back of room distance
- Use colorblind simulator (online tools available)
- Verify contrast ratios with accessibility checker
- Test on different display sizes

### Cognitive Accessibility

- **Simple language:** Avoid jargon, or define technical terms
- **Clear structure:** Obvious organization with signposting
- **Predictable pacing:** Consistent timing across slides
- **Multiple modalities:** Visual + verbal + text reinforcement
- **One idea per slide:** Prevents information overload
- **Progressive disclosure:** Don't overwhelm with all info at once

## Presenter Notes

**Critical principle**: Detailed text belongs in presenter notes, NOT on slides.

**MIT CommLab guidance**: "Take the text off the slide and put it into your presenter notes."

**Use presenter notes for:**
- **Full sentences** you'll speak (slides should only have keywords)
- **Detailed explanations** that would clutter slides
- **Statistics and exact numbers** (slide shows visual, you cite specifics)
- **Timing cues** ("Spend 2 minutes here", "Pause for effect")
- **Transitions** ("Now ask for questions", "Reference demo if time permits")
- **Technical details** to remember
- **Anticipated questions** and answers
- **Stories/anecdotes** to share (slide shows key point, you tell story)

**Script first few slides:**
- Word-for-word opening (calms nerves, ensures strong start)
- After first 2-3 slides, bullet points sufficient
- Corey Quinn's tip: Duplicate title slide - first has no notes (safe for mirrored display), second has scripted intro

**Notes format:**
```markdown
# Experiment X demonstrates 2x performance gain

![Chart showing performance comparison](./images/performance.png)

<!--
NOTES:
Opening: "When we first ran this experiment, I honestly didn't believe the results."

Key points to cover:
- Baseline: 100 req/sec (previous approach)
- New approach: 200 req/sec (sustained over 24 hours)
- Statistical significance: p < 0.01
- Caveat: Results specific to our dataset size (mention in Q&A if asked)

Transition: "This performance gain enables us to handle peak traffic, which brings me to the next challenge..."

Timing: 90 seconds on this slide
-->
```

**Benefits:**
- Slides stay clean and visual
- Audience doesn't read ahead
- You have full guidance without cluttering presentation
- Can include details you might forget under pressure

## Best Practices Summary

### Evidence-Based Core Rules

**The 10 Essential Principles:**
1. **One idea per slide** - Each slide = one central finding
2. **Meaningful titles** - Assertions, not labels ("X demonstrates Y" not "Results")
3. **Minimal text** - <50 words excluding title, keywords not sentences
4. **Visual over text** - Almost never text-only slides
5. **Max 6 elements** - Cognitive load management
6. **Accessibility** - 18pt+ fonts, 4.5:1 contrast, colorblind-safe
7. **Design for distracted** - Title + visual convey point without narration
8. **Progressive disclosure** - Reveal complexity gradually
9. **Timing** - 90s/slide default (configurable 60-180s)
10. **Backup slides** - Detailed data separate from main deck

### DO:
- **Start with compelling hook** (not CV or agenda)
- **Use rule of three** for main points
- **Put detailed text in presenter notes**, not on slides
- **Practice timing** with stopwatch
- **Leave white space** (minimum 10% margins)
- **Use progressive disclosure** for complex content
- **End with clear conclusion statement** (not "Thank you")
- **Test accessibility** (contrast, colorblind, distance)
- **Create backup slides** for Q&A
- **Apply consistent theme** throughout

### DON'T:
- **Overload slides with text** - Audience can't read and listen
- **Use tiny fonts** - Minimum 18pt body, 24pt headings
- **Read slides verbatim** - You lose engagement
- **Use vague titles** - "Results" → "Experiment X shows 2x gain"
- **Cram multiple ideas** - One per slide maximum
- **Exceed 6 elements** - Cognitive overload
- **Skip accessibility** - Exclude audience members
- **Use color alone** - Patterns/labels for colorblind
- **Ignore contrast** - Verify 4.5:1 minimum
- **Use italics/underlines** in body text - Reduces readability

### Validation Checklist

Before finalizing, verify each slide:
- [ ] One clear idea/finding
- [ ] Meaningful title (assertion format)
- [ ] <50 words body text
- [ ] ≤6 distinct elements
- [ ] At least one visual (unless quote/transition)
- [ ] Font sizes: body ≥18pt, heading ≥24pt
- [ ] High contrast verified (4.5:1+)
- [ ] Colorblind-safe colors
- [ ] Explainable in ~90 seconds
- [ ] Title + visual = standalone comprehension

Presentation-level:
- [ ] Total slides appropriate for duration (±20% of duration_minutes × 60 / seconds_per_slide)
- [ ] Logical flow between slides
- [ ] Consistent theme/colors/fonts
- [ ] Strong opening (hook, not bio)
- [ ] Clear conclusion statement
- [ ] Backup slides separated
- [ ] Presenter notes for key slides

---

**Additional Resources:**
- See `references/presentation-best-practices.md` for full research-based guidelines
- Nancy Duarte: *Resonate*, *Slide:ology* (storytelling and visual design)
- Garr Reynolds: *Presentation Zen* (minimalist design philosophy)
- PLOS Computational Biology: "Ten Simple Rules for Effective Presentation Slides"
- MIT Communication Lab: Slide Presentation Guide
