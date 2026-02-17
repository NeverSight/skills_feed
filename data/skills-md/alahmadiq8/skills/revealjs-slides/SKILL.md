---
name: revealjs-slides
description: >
  Generate reveal.js HTML slide presentations from topics, outlines, or content.
  Use when the user asks to create slides, presentations, decks, or talks.
  Triggers on: "create a presentation", "make slides about", "build a deck",
  "generate a talk", "slide deck for", or any request involving presentation creation.
  Supports code highlighting, fragments, speaker notes, math, markdown,
  and Mermaid.js diagrams (flowcharts, sequence, class, ER, mindmap, timeline, etc.).
---

# reveal.js Slide Generator

## Workflow

1. Copy template from `assets/template.html` to the user's target path (default: `slides.html` in cwd)
2. Replace `{{TITLE}}`, `{{SUBTITLE}}`, `{{AUTHOR}}`, `{{DATE}}` placeholders
3. Generate `<section>` elements for each slide between the TITLE SLIDE and closing comments
4. Serve and open the presentation (see **Running** below)

## Running

After generating the HTML file, always serve and open it for the user.

```bash
npx live-server --port=8765 --open=slides.html
```

**Keyboard shortcuts in the presentation:**
- Arrow keys / Space — navigate slides
- `S` — open speaker notes view
- `O` — overview / slide grid
- `F` — fullscreen
- `Esc` — exit overview or fullscreen
- `B` / `.` — pause (black screen)

## Template Location

`assets/template.html` — CDN-based (no npm install needed), uses Inter font, custom theme, includes Markdown, Highlight, Notes, Math, and Mermaid plugins.

## Default Theme: Custom-Style

The template ships with a custom theme built in. Key characteristics:

- **Inter font** (Google Fonts) with Segoe UI / Calibri fallbacks
- **Left-aligned** content slides with top-aligned text (`center: false`)
- **Title/closing slides** use `class="title-slide"` for centered, vertically-centered layout
- **h2 slide titles** have a subtle bottom border separator
- **Bold text** renders in the heading accent color (`#1a3c6e`)
- **Tables** have a dark navy header row with alternating striped rows
- **Blockquotes** have a left blue accent bar with light background
- **Code blocks** are flat with a subtle border (no drop shadow)
- **Slide dimensions**: 1280x720 (16:9), matching typical presentation aspect ratio
- **Slide padding**: 48px top/bottom, 56px sides

### Title / closing slide (vertically centered)
```html
<section class="title-slide">
  <h1>Presentation Title</h1>
  <p>Subtitle text here</p>
  <p class="small">Author &mdash; Date</p>
</section>
```

### Two-column layout (using .columns helper)
```html
<section>
  <h2>Comparison</h2>
  <div class="columns">
    <div><h3>Left</h3><p>Content</p></div>
    <div><h3>Right</h3><p>Content</p></div>
  </div>
</section>
```

## Base Theme Override

The custom theme overrides `white.css`. To change the base, replace `white` in the CSS link: `black`, `league`, `beige`, `night`, `serif`, `simple`, `solarized`, `moon`, `dracula`, `sky`, `blood`. Note: for dark base themes, also update the CSS variable `--r-heading-color` and other colors.

## Slide Patterns

### Basic slide
```html
<section>
  <h2>Title</h2>
  <p>Content here</p>
</section>
```

### Bullet list with fragments (reveal one at a time)
```html
<section>
  <h2>Key Points</h2>
  <ul>
    <li class="fragment">First point</li>
    <li class="fragment">Second point</li>
    <li class="fragment">Third point</li>
  </ul>
</section>
```

### Code with syntax highlighting
```html
<section>
  <h2>Code</h2>
  <pre><code class="language-python" data-trim data-line-numbers>
def hello():
    print("Hello, world!")
  </code></pre>
</section>
```

Use `data-line-numbers="1-2|3-4"` to step through line highlights.

### Image slide
```html
<section>
  <h2>Architecture</h2>
  <img src="diagram.png" alt="Architecture" style="max-height: 500px;">
</section>
```

### Speaker notes
```html
<section>
  <h2>Topic</h2>
  <p>Audience content</p>
  <aside class="notes">Speaker-only notes here. Press 's' to open speaker view.</aside>
</section>
```

### Background color/image
```html
<section data-background-color="#4d7e65">
  <h2>Green Background</h2>
</section>
<section data-background-image="photo.jpg" data-background-size="cover">
  <h2>Photo Background</h2>
</section>
```

### Blockquote
```html
<section>
  <blockquote>"Quote text here." &mdash; Author</blockquote>
</section>
```

### Two-column layout
```html
<section>
  <h2>Comparison</h2>
  <div style="display: flex; gap: 2em;">
    <div style="flex: 1;"><h3>Left</h3><p>Content</p></div>
    <div style="flex: 1;"><h3>Right</h3><p>Content</p></div>
  </div>
</section>
```

### Math (KaTeX)
```html
<section>
  <h2>Equation</h2>
  <p>\[ E = mc^2 \]</p>
</section>
```

### Markdown slide
```html
<section data-markdown>
  <script type="text/template">
    ## Markdown Title
    - Point **one**
    - Point *two*

    Notes:
    Speaker notes in markdown.
  </script>
</section>
```

## Diagram Patterns (Mermaid.js)

The template includes the Mermaid plugin. Use `<div class="mermaid">` blocks inside slides to render diagrams. Mermaid renders to SVG automatically — no images needed.

### Flowchart
```html
<section>
  <h2>User Flow</h2>
  <div class="mermaid">
    flowchart LR
      A[Visit Site] --> B{Logged in?}
      B -- Yes --> C[Dashboard]
      B -- No --> D[Login Page]
      D --> E[Enter Credentials]
      E --> C
  </div>
</section>
```

### Sequence diagram
```html
<section>
  <h2>API Request Flow</h2>
  <div class="mermaid">
    sequenceDiagram
      participant Client
      participant API
      participant DB
      Client->>API: POST /users
      API->>DB: INSERT user
      DB-->>API: user record
      API-->>Client: 201 Created
  </div>
</section>
```

### Class diagram
```html
<section>
  <h2>Domain Model</h2>
  <div class="mermaid">
    classDiagram
      class Animal {
        +String name
        +int age
        +makeSound()
      }
      class Dog {
        +fetch()
      }
      class Cat {
        +purr()
      }
      Animal <|-- Dog
      Animal <|-- Cat
  </div>
</section>
```

### Entity-Relationship diagram
```html
<section>
  <h2>Database Schema</h2>
  <div class="mermaid">
    erDiagram
      USER ||--o{ ORDER : places
      ORDER ||--|{ LINE_ITEM : contains
      PRODUCT ||--o{ LINE_ITEM : "ordered in"
  </div>
</section>
```

### State diagram
```html
<section>
  <h2>Order Lifecycle</h2>
  <div class="mermaid">
    stateDiagram-v2
      [*] --> Pending
      Pending --> Processing : payment received
      Processing --> Shipped : packed
      Shipped --> Delivered : arrived
      Delivered --> [*]
      Processing --> Cancelled : refund
  </div>
</section>
```

### Mindmap
```html
<section>
  <h2>Project Overview</h2>
  <div class="mermaid">
    mindmap
      root((Project))
        Frontend
          React
          Tailwind
        Backend
          Node.js
          PostgreSQL
        DevOps
          Docker
          CI/CD
  </div>
</section>
```

### Timeline
```html
<section>
  <h2>Project Milestones</h2>
  <div class="mermaid">
    timeline
      title Release Timeline
      Q1 2025 : Alpha release
                : Core features
      Q2 2025 : Beta release
                : API launch
      Q3 2025 : GA release
  </div>
</section>
```

### Gantt chart
```html
<section>
  <h2>Sprint Plan</h2>
  <div class="mermaid">
    gantt
      title Sprint 12
      dateFormat YYYY-MM-DD
      section Backend
        API endpoints :a1, 2025-01-06, 5d
        Database migration :a2, after a1, 3d
      section Frontend
        UI components :b1, 2025-01-06, 7d
        Integration :b2, after b1, 3d
  </div>
</section>
```

### Pie chart
```html
<section>
  <h2>Traffic Sources</h2>
  <div class="mermaid">
    pie title Traffic Sources
      "Organic Search" : 45
      "Direct" : 25
      "Social Media" : 20
      "Referral" : 10
  </div>
</section>
```

### Git graph
```html
<section>
  <h2>Branching Strategy</h2>
  <div class="mermaid">
    gitGraph
      commit
      branch feature
      checkout feature
      commit
      commit
      checkout main
      merge feature
      commit
  </div>
</section>
```

### Diagram with custom theme (dark presentations)
For dark themes (`black`, `night`, `dracula`, `league`), add a theme directive:
```html
<div class="mermaid">
  %%{init: {'theme': 'dark'}}%%
  flowchart LR
    A --> B --> C
</div>
```

Available Mermaid themes: `default`, `dark`, `forest`, `neutral`, `base`.

### Diagram with title and description alongside
```html
<section>
  <h2>Architecture</h2>
  <div class="columns">
    <div>
      <div class="mermaid">
        flowchart TD
          LB[Load Balancer] --> S1[Server 1]
          LB --> S2[Server 2]
          S1 --> DB[(Database)]
          S2 --> DB
      </div>
    </div>
    <div>
      <ul>
        <li>Horizontally scalable</li>
        <li>Single database with replicas</li>
        <li>Health-check based routing</li>
      </ul>
    </div>
  </div>
</section>
```

## Diagram Design Guidelines

- **One diagram per slide** — keep diagrams readable; don't crowd
- **Keep under 15-20 nodes** — split complex systems across multiple slides
- **Use meaningful labels** — `User`, `Database`, not `A`, `B`, `C`
- **Match the theme** — use `%%{init: {'theme': 'dark'}}%%` for dark presentation themes
- **Flowchart direction** — use `LR` (left-to-right) for wide slides, `TD` (top-down) for tall diagrams
- **Pair with text** — use two-column layout to add context beside a diagram
- **Prefer flowchart for**: processes, decision trees, architecture
- **Prefer sequence for**: API flows, request/response, protocol interactions
- **Prefer class/ER for**: data models, database schemas, OOP hierarchies
- **Prefer mindmap for**: brainstorming, topic overviews, project structure
- **Prefer timeline/gantt for**: roadmaps, project plans, sprint schedules

## Slide Design Guidelines

- **Title slide**: always first, use `class="title-slide"` with h1, subtitle, and author
- **Closing slide**: use `class="title-slide"` for centered "Questions?" or "Thank You" slides
- **Content slides**: use h2 for the slide title (gets a bottom border separator automatically)
- **~1 idea per slide**: keep content focused
- **Prefer fragments** for bullet lists so content reveals progressively
- **Code blocks**: use `data-trim` to strip whitespace, set `language-*` class
- **Limit text**: prefer visuals, short phrases, and keywords over paragraphs
- **Bold for emphasis**: `<strong>` text renders in the navy accent color automatically
- **Use `.columns` helper**: for side-by-side layouts instead of inline flex styles
- **Never use vertical slides**: do not nest `<section>` inside `<section>`. All slides must be flat/horizontal only

## Config Customization

Modify the `Reveal.initialize({...})` block at the bottom of the HTML:

| Option | Default | Purpose |
|--------|---------|---------|
| `transition` | `'slide'` | `none`, `fade`, `slide`, `convex`, `concave`, `zoom` |
| `slideNumber` | `true` | Show slide numbers |
| `center` | `false` | Content starts at top (title-slide class overrides this) |
| `hash` | `true` | URL hash navigation |
| `progress` | `true` | Show progress bar |
| `controls` | `true` | Show nav arrows |
| `width` | `1280` | Slide width in pixels (16:9) |
| `height` | `720` | Slide height in pixels (16:9) |
| `margin` | `0` | No outer margin (padding is in CSS) |

## PDF Export

Append `?print-pdf` to the URL and use browser print (Cmd/Ctrl+P) to save as PDF.
