---
name: storytelling-web
description: Create stunning, animation-rich exploratory visual web pages from text content. Supports both Slides mode (presentation-style with slide navigation) and Scrolling mode (scroll-driven narrative with progressive animations). Use when the user wants to transform text into immersive web experiences with distinctive visual design, smooth animations, and engaging interactions. Generates zero-dependency single-file HTML.
---

# Storytelling Web

Create stunning, animation-rich exploratory visual web pages from text content — choose between **slide-based presentations** or **scroll-driven narratives**.

## Core Philosophy

1. **Zero Dependencies** — Single HTML files with inline CSS/JS. No npm, no build tools.
2. **Show, Don't Tell** — Generate visual previews, not abstract choices. People don't know what they want until they see it.
3. **Distinctive Design** — Avoid generic "AI slop" aesthetics. Every experience should feel custom-crafted.
4. **Production Quality** — Code should be well-commented, accessible, and performant.

## Phase 0: Content Discovery

First, understand the user's needs and gather content:

### Step 0.1: User Requirements

Understand what the user wants to achieve:

**Question 1: Purpose**

- Header: "Purpose"
- Question: "What is this for?"
- Options:
  - "Pitch/Investment" — Selling an idea, product, or company
  - "Teaching/Education" — Explaining concepts, tutorials, guides
  - "Story/Narrative" — Sharing experiences, journalism, creative writing
  - "Update/Report" — Status updates, project reviews, documentation

**Question 2: Length**

- Header: "Length"
- Question: "How much content do you have?"
- Options:
  - "Short" — Quick read, 3-5 slides or sections
  - "Medium" — Standard length, 6-15 slides or sections
  - "Long" — Comprehensive, 15+ slides or sections

### Step 0.2: Content Gathering

Get the actual content from the user:

**Question 1: Content Status**

- Header: "Content"
- Question: "Do you have the content ready?"
- Options:
  - "I have all content ready" — Just need to design it
  - "I have rough notes" — Need help organizing
  - "I have a topic only" — Need help creating from scratch

If user has content, ask them to share it (text, bullet points, images, etc.).

## Phase 1: Choose Mode

Based on the content understanding, provide helpful context about both modes, then let the user choose.

### Step 1.1: Mode Analysis (Informational)

Analyze the user's content from Phase 0 and share insights:

**For your content:**

- **Slides mode** works well if: [explain why slides might fit based on their purpose/length]
  - Structured, sequential presentation
  - Speaker-led experience with navigation control
  - Content that benefits from clear boundaries between sections

- **Scrolling mode** works well if: [explain why scrolling might fit based on their purpose/length]
  - Exploratory, narrative-driven experience
  - Reader-controlled pacing
  - Content that flows naturally as a continuous story

**Note:** These are just considerations — choose whichever mode aligns with your vision. You may have a clear preference already.

### Step 1.2: Mode Selection Question

Then ask:

- Header: "Experience Type"
- Question: "Which mode would you like to use?"
- Options:
  - **"Slides"** — Presentation with slide navigation, best for structured content.
  - **"Scrolling Story"** — Continuous scroll narrative, best for exploratory content.

## Phase 2: Style Discovery

### Step 2.1: Mood Selection

**Question 1: Feeling**

- Header: "Vibe"
- Question: "What feeling should the audience have?"
- Options:
  - "Impressed/Confident" — Professional, trustworthy, polished
  - "Excited/Energized" — Innovative, bold, dynamic
  - "Calm/Focused" — Clear, thoughtful, easy to follow
  - "Inspired/Moved" — Emotional, memorable, atmospheric
- multiSelect: true (can choose up to 2)

### Step 2.2: Generate Style Previews

Based on their mood selection and chosen mode (Slides or Scrolling), read the corresponding reference document ([references/slides-mode.md](references/slides-mode.md) or [references/scrolling-mode.md](references/scrolling-mode.md)) to understand the HTML architecture and design patterns for that mode.

Also read [references/style-presets.md](references/style-presets.md) for detailed style presets including specific font pairings, color palettes, animation approaches, and signature elements to ensure distinctive, non-generic designs.

Then generate **3 distinct style previews** as mini HTML files. Each file should contain only a small portion of content, serving as a draft for users to visually select from, showing:

- Typography (font choices, heading/body hierarchy)
- Color palette (background, accent, text colors)
- Animation style (how elements enter)
- Overall aesthetic feel

Preview Styles to Consider (pick 3 based on mood):

| Mood | Slides Options | Scrolling Options |
|------|---------------|-------------------|
| Impressed/Confident | "Corporate Elegant", "Dark Executive", "Clean Minimal" | "Swiss Modern", "Editorial Classic", "Professional Dark" |
| Excited/Energized | "Neon Cyber", "Bold Gradients", "Kinetic Motion" | "Neon Nights", "Dynamic Energy", "Future Forward" |
| Calm/Focused | "Paper & Ink", "Soft Muted", "Swiss Minimal" | "Zen Garden", "Clean Air", "Quiet Space" |
| Inspired/Moved | "Cinematic Dark", "Warm Editorial", "Atmospheric" | "Midnight Cinema", "Golden Hour", "Misty Forest" |

**IMPORTANT: Never use these generic patterns:**

- Purple gradients on white backgrounds
- Inter, Roboto, or system fonts
- Standard blue primary colors
- Predictable layouts

**Instead, use distinctive choices:**

- Unique font pairings (Clash Display, Satoshi, Cormorant Garamond, DM Sans, etc.)
- Cohesive color themes with personality
- Atmospheric backgrounds (gradients, subtle patterns, depth)
- Signature animation moments

### Step 2.3: Present Previews

Create the previews and present them to the user.

Each preview should be:

- Self-contained (inline CSS/JS)
- A single slide (Slides) or hero section (Scrolling) showing the aesthetic
- Animated to demonstrate motion style
- ~50-300 lines

Present to user:

```
I've created 3 style previews for you to compare:

**Style A: [Name]** — [1 sentence description]
**Style B: [Name]** — [1 sentence description]
**Style C: [Name]** — [1 sentence description]

Take a look and tell me:
1. Which style resonates most?
2. What do you like about it?
3. Anything you'd change?
```

Then use AskUserQuestion:

**Question: Pick Your Style**

- Header: "Style"
- Question: "Which style preview do you prefer?"
- Options:
  - "Style A: [Name]" — [Brief description]
  - "Style B: [Name]" — [Brief description]
  - "Style C: [Name]" — [Brief description]
  - "Mix elements" — Combine aspects from different styles

If "Mix elements", ask for specifics.

## Phase 3: Generate Output

### Output Locations

**Style Preview Outputs (Intermediate)**

- Generated in Phase 2 for user to select from
- Saved to `.agent-design/storytelling-web/` directory:

```
.agent-design/storytelling-web/
├── style-a.html    # First style option
├── style-b.html    # Second style option
├── style-c.html    # Third style option
└── assets/         # Any shared assets
```

**Final Output**

- **Location**: User's working directory root (where the task was initiated)
- **Filename**: Based on the content title, e.g., `xxx.html` (use kebab-case, e.g., `my-presentation.html`, `my-story.html`)
- **Requirements**:
  - Single self-contained HTML file with inline CSS/JS
  - Zero external dependencies (except Google Fonts CDN)
  - All content included based on user's provided material

### For Slides Mode

Read [references/slides-mode.md](references/slides-mode.md) for:

- Complete HTML architecture
- Slide type patterns (title, content, split, image, quote, closing)
- Navigation and keyboard controls
- Animation patterns for slide transitions

### For Scrolling Mode

Read [references/scrolling-mode.md](references/scrolling-mode.md) for:

- Complete HTML architecture
- Section type patterns (hero, text, image-text, full-bleed, quote)
- Scroll-triggered animations
- Progress bar implementation

## Design Principles (Both Modes)

1. **Typography Hierarchy** — Clear distinction between headings, body, captions
2. **Color Consistency** — Use CSS custom properties for easy theming
3. **Accessibility** — Sufficient contrast, semantic HTML, keyboard navigation
4. **Mobile Consideration** — Test responsiveness
5. **Performance** — Optimize images, efficient animations

## Tips for Great Experiences

### Slides Mode

- One idea per slide
- Large, readable text
- Visual variety between slides
- Strong opening and closing

### Scrolling Mode

- Start with a hook
- Control pacing (some sections quick, others slow)
- Use images intentionally
- Build to key moments
- End memorably
