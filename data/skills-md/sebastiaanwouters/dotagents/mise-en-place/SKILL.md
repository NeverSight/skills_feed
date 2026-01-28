---
name: mise-en-place
description: "Transforms raw ideas into complete specs via adaptive interview. Triggers on: mise-en-place, prep my idea, spec this out. Starts from SPEC.md or user-specified file. Uses chef (Telegram) or built-in conversation, compound for knowledge priming."
---

# Mise-en-Place 🍳

**Everything in its place before cooking begins.**

Transform an idea into a complete, implementation-ready specification through adaptive conversation, starting from existing documentation.

## Goal

Build a complete mental model of what we're building:
- **What** we're building and why
- **Who** it's for and their journey
- **How** it works technically (exact stack, libraries, integrations)
- **How** it looks and feels (design system, theme, personality)
- **What** each part/page/step does in detail

## Communication Mode

**Two modes available:**

| Mode | When to use | How |
|------|-------------|-----|
| **Chef (Telegram)** | User says "use chef" or "via telegram" | Load chef skill, use `chef ask` for BLOCKING questions |
| **Built-in (default)** | Normal conversation | Ask questions directly in chat, wait for user response |

If chef is not explicitly requested, use built-in conversation mode.

## Five Phases

| Phase | Purpose | Output |
|-------|---------|--------|
| **0. Bootstrap** | Read existing spec file as starting point | Context for discovery |
| **1. Discovery** | Adaptive interview to fill gaps | `docs/SPEC.md` |
| **2. Design System** | Create visual/component foundation | `docs/design/` folder |
| **3. Research** | Prime knowledge base with stack docs | Compound store |
| **4. Initialize** | Set up agent guidelines for implementation | `AGENTS.md` |

---

## Phase 0: Bootstrap

**Start here — never from scratch.**

### Codebase Analysis (if exists)

Before reading spec files, check if this is an existing project with code:

1. **Detect existing codebase** — Look for:
   - `package.json`, `composer.json`, `Cargo.toml`, `go.mod`, `requirements.txt`, etc.
   - `src/`, `app/`, `lib/` directories
   - Framework-specific files (e.g., `next.config.js`, `vite.config.ts`, `artisan`)

2. **If codebase exists, analyze it first:**
   - **Tech stack detection** — Parse lock files, configs, imports to identify exact frameworks/libraries/versions
   - **Project structure** — Map out directories, key files, architectural patterns
   - **Existing features** — Scan routes, components, models to understand what's already built
   - **Design patterns in use** — Check styling approach (CSS modules, Tailwind, styled-components), component patterns
   - **Database/API layer** — Identify ORM, migrations, API structure
   - **Authentication** — Check for existing auth implementation
   - **Deployment setup** — Look for Docker, CI/CD configs, deploy scripts

3. **Create analysis summary:**
   ```
   ## Codebase Analysis
   
   **Stack detected:** [exact versions from package.json/lock files]
   **Structure:** [brief architecture overview]
   **Features built:** [list of existing functionality]
   **Patterns in use:** [styling, state management, API patterns]
   **Missing/incomplete:** [obvious gaps or TODO markers found]
   ```

4. **Use analysis to guide Discovery** — Skip questions about already-implemented choices. Focus on:
   - Gaps in existing implementation
   - New features to add
   - Improvements to current patterns
   - Design refinements

### Source File

1. Check for existing spec file in this order:
   - User-specified file (if provided, e.g., "use README.md" or "start from docs/idea.md")
   - `SPEC.md` in project root
   - `docs/SPEC.md`
   - `README.md` as fallback

2. Read the file and extract:
   - Project description/vision
   - Any mentioned features or requirements
   - Tech stack hints (cross-reference with codebase analysis)
   - Design preferences
   - Referenced resources (URLs, repos, apps)

3. Summarize what you learned from **both** codebase analysis and spec files before proceeding to Discovery.

### Gather Resources (Optional)

Ask user for reference materials:
- **URLs** — Documentation, design inspiration, competitor sites
- **Example apps** — "Like Notion but for X", "Similar to Linear's UI"
- **GitHub repos** — Reference implementations, starter templates, design systems
- **Figma/design files** — If available

Store these references for use in Discovery and Design System phases.

---

## Phase 1: Discovery

Ask intelligent, open-ended questions. Each question builds on previous answers. Wait for user response before proceeding.

### Starting Point

Review what Bootstrap phase extracted (codebase analysis + spec files), then identify gaps. 

**If existing codebase was analyzed:**
- DO NOT ask about tech stack choices already implemented
- DO NOT ask about patterns/conventions already established
- REFERENCE existing implementation when asking about extensions ("I see you're using Convex for the backend. For the new feature, should we...")
- FOCUS on: what's missing, what needs improvement, new features to add

Focus questions on what's unclear or missing — don't re-ask what's already documented or implemented.

### Adaptive Questioning

Dynamically choose your next question based on what's missing or unclear. Fill these knowledge areas:

#### 1. Problem & Users
- What specific pain point does this solve?
- Who experiences this pain? Describe them.
- How do they currently deal with it?
- What would success look like for them?

#### 2. User Journey (Start to Finish)
- How does someone discover/find this?
- What's the signup/onboarding flow?
- What's the core action they repeat?
- What progression or value accumulation happens?
- How does a session typically end?
- What brings them back?

#### 3. Structure & Parts
- What are all the pages/screens/views?
- For each page: what can the user do there?
- How do pages connect/flow into each other?
- What's always visible (nav, sidebar, etc)?
- What are the key states (loading, empty, error, success)?

#### 4. Tech Stack (Be Specific)
**Skip if codebase analysis already detected the stack.** Only ask about missing layers or new additions.

For greenfield projects, ask about each layer, get exact library/framework names:
- Frontend framework & version
- Routing solution
- State management approach
- Styling approach (CSS framework, component library)
- Backend/API approach
- Database & ORM
- Authentication method
- Real-time needs (if any)
- File storage (if any)
- Third-party integrations/APIs
- Deployment target

For existing codebases, focus on:
- New integrations needed for planned features
- Gaps in current stack (e.g., "I see no testing setup, should we add one?")
- Upgrades or migrations being considered

#### 5. Design & Theme
- What's the visual style? (Show examples/references if possible)
- Color palette or mood?
- Typography feel?
- Light/dark mode?
- Brand personality (serious, playful, minimal, bold)?
- Any existing brand assets to match?

#### 6. Features Deep-Dive
For each major feature:
- What exactly does it do?
- What inputs does it need?
- What outputs/results does it produce?
- What edge cases exist?
- How does it interact with other features?

#### 7. Deployment & Infrastructure
- Where will this be hosted? (Fly.io, Vercel, AWS, self-hosted, etc.)
- Domain name / URL structure?
- Environment setup (staging, production)?
- CI/CD requirements? (GitHub Actions, etc.)
- SSL/TLS needs?
- CDN for assets?
- Monitoring/logging requirements?
- Backup strategy?
- Scaling expectations? (concurrent users, traffic patterns)

#### 8. Constraints & Requirements
- Timeline or deadline?
- Performance requirements?
- Accessibility needs?
- Security/compliance needs?
- Budget constraints?
- Team size/skills?

### Question Strategy

- After each answer, analyze what's still unclear or missing
- Ask the MOST valuable next question
- Go deep on unclear areas — don't accept vague answers for critical details
- Be specific about tech — get exact library names, not categories

### Wrapping Up Discovery

When you have the full picture, confirm understanding with the user before writing the spec.

---

## Spec Generation

Generate `docs/SPEC.md` covering:

- Vision & Problem
- Target Users
- User Journey (discovery → onboarding → core usage → return)
- Pages & Structure (every page with purpose and capabilities)
- Features (full detail, inputs, outputs, edge cases)
- Tech Stack (exact technologies with versions)
- Design & Theme (visual direction, references, personality)
- Data Model (key entities and relationships)
- Integrations (third-party services and APIs)
- Deployment & Infrastructure (hosting, CI/CD, environments, scaling)
- Constraints & Requirements
- Open Questions

---

## Phase 2: Design System

Create a design foundation based on the spec, gathered resources, and project description.

### Inputs

Use these sources to inform the design system:
- **SPEC.md** — Design & Theme section, brand personality
- **Reference resources** — URLs, example apps, GitHub repos from Bootstrap phase
- **Tech stack** — Component library choice affects design tokens

### Research References

For each provided resource:
- **URLs** — Fetch and analyze visual patterns, color usage, typography, spacing
- **Example apps** — Document what makes their design work (if accessible)
- **GitHub repos** — Check for existing design tokens, theme configs, component patterns
- **Design systems** — If referencing known systems (Tailwind, Radix, shadcn), pull their conventions

### Generate `docs/design/` folder

Create a modular design system with separate files for each concern:

```bash
mkdir -p docs/design
```

#### 1. `docs/design/tokens.md` — Design Tokens

```markdown
---
updated: YYYY-MM-DD
---

# Design Tokens

## Colors
| Token | Value | Usage |
|-------|-------|-------|
| `--color-primary` | oklch(...) | CTAs, links, active states |
| `--color-secondary` | oklch(...) | Secondary actions |
| `--color-surface` | oklch(...) | Card backgrounds |
| `--color-background` | oklch(...) | Page background |
| `--color-text` | oklch(...) | Body text |
| `--color-text-muted` | oklch(...) | Secondary text |
| `--color-border` | oklch(...) | Borders, dividers |
| `--color-error` | oklch(...) | Error states |
| `--color-success` | oklch(...) | Success states |
| `--color-warning` | oklch(...) | Warning states |

## Typography
| Token | Value | Usage |
|-------|-------|-------|
| `--font-display` | 'Font Name', serif | Headings |
| `--font-body` | 'Font Name', sans-serif | Body text |
| `--font-mono` | 'Font Name', monospace | Code |
| `--text-xs` | 0.75rem | Small labels |
| `--text-sm` | 0.875rem | Secondary text |
| `--text-base` | 1rem | Body text |
| `--text-lg` | 1.125rem | Emphasis |
| `--text-xl` | 1.25rem | Subheadings |
| `--text-2xl` | 1.5rem | Headings |
| `--text-3xl` | 2rem | Large headings |

## Spacing
| Token | Value |
|-------|-------|
| `--space-1` | 0.25rem |
| `--space-2` | 0.5rem |
| `--space-3` | 0.75rem |
| `--space-4` | 1rem |
| `--space-6` | 1.5rem |
| `--space-8` | 2rem |
| `--space-12` | 3rem |
| `--space-16` | 4rem |

## Border Radius
| Token | Value |
|-------|-------|
| `--radius-sm` | 4px |
| `--radius-md` | 8px |
| `--radius-lg` | 12px |
| `--radius-full` | 9999px |

## Shadows
| Token | Value |
|-------|-------|
| `--shadow-sm` | 0 1px 2px oklch(0% 0 0 / 0.05) |
| `--shadow-md` | 0 4px 6px oklch(0% 0 0 / 0.1) |
| `--shadow-lg` | 0 10px 15px oklch(0% 0 0 / 0.1) |
| `--shadow-xl` | 0 20px 25px oklch(0% 0 0 / 0.15) |

## Breakpoints
| Token | Value |
|-------|-------|
| `--bp-sm` | 640px |
| `--bp-md` | 768px |
| `--bp-lg` | 1024px |
| `--bp-xl` | 1280px |
| `--bp-2xl` | 1536px |
```

#### 2. `docs/design/components.md` — Component Patterns

```markdown
---
updated: YYYY-MM-DD
---

# Component Patterns

## Buttons
- **Primary**: solid bg `--color-primary`, white text
- **Secondary**: border `--color-primary`, transparent bg
- **Ghost**: no border, subtle hover bg
- **Destructive**: `--color-error` bg, white text
- Sizes: sm (h-8), md (h-10), lg (h-12)
- All: `--radius-sm`, appropriate padding

## Inputs
- Height: 40px (md), 36px (sm), 48px (lg)
- Border: 1px `--color-border`
- Focus: 2px ring `--color-primary`
- Error: border `--color-error`
- Labels above, `--space-1` gap

## Cards
- Background: `--color-surface`
- Border: 1px `--color-border`
- Radius: `--radius-md`
- Padding: `--space-4` to `--space-6`

## Modals/Dialogs
- Backdrop: black/50%
- Radius: `--radius-lg`
- Shadow: `--shadow-xl`
- Max-width: 500px (sm), 700px (md), 900px (lg)

## Navigation
- Header height: 64px
- Sidebar width: 280px (expanded), 64px (collapsed)
- Active indicator: `--color-primary`

## Loading States
- Skeleton: animated gradient
- Spinner: `--color-primary`

## Empty States
- Centered, icon + heading + description + action

## Notifications/Toasts
- Position: bottom-right
- Duration: 5000ms default
- Variants: info, success, warning, error
```

#### 3. `docs/design/layout.md` — Layout Patterns

```markdown
---
updated: YYYY-MM-DD
---

# Layout Patterns

## Container
- Max-width: 1280px
- Padding: `--space-4` (mobile), `--space-8` (desktop)
- Centered with auto margins

## Page Layouts
- **Sidebar**: 280px fixed left, fluid content
- **Stacked**: header → main → footer (vertical)
- **Centered**: constrained content width, centered

## Grid System
- 12-column base
- Gap: `--space-4` default
- Responsive columns: 1 (mobile) → 2-3 (tablet) → 4+ (desktop)

## Responsive Behavior
- Mobile-first approach
- Breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)
```

#### 4. `docs/design/motion.md` — Motion & Animation

```markdown
---
updated: YYYY-MM-DD
---

# Motion & Animation

## Durations
| Token | Value | Usage |
|-------|-------|-------|
| `--duration-fast` | 150ms | Micro-interactions |
| `--duration-normal` | 300ms | Standard transitions |
| `--duration-slow` | 500ms | Complex animations |

## Easing
| Token | Value | Usage |
|-------|-------|-------|
| `--ease-default` | cubic-bezier(0.4, 0, 0.2, 1) | General purpose |
| `--ease-in` | cubic-bezier(0.4, 0, 1, 1) | Enter |
| `--ease-out` | cubic-bezier(0, 0, 0.2, 1) | Exit |

## Animation Patterns
- **Fade**: opacity 0 → 1
- **Slide**: translateY(8px) → 0
- **Scale**: scale(0.95) → 1
- **Stagger**: 50ms delay between items
```

### Integration with Tech Stack

Based on the chosen styling approach, also generate:
- **Tailwind** — `tailwind.config.js` theme extension referencing tokens
- **CSS Variables** — `:root` variable definitions matching tokens.md
- **styled-components/emotion** — Theme object matching tokens
- **Component library (shadcn, Radix)** — Customization notes in components.md

---

## Phase 3: Research & Prime Compound

After spec and design system are written, research all chosen technologies and store in compound.

1. **Extract stack** from SPEC.md
2. **Research each technology** via web_search and read_web_page:
   - Installation, configuration, patterns
   - Integration with other stack items
   - Common gotchas
3. **Include design system** — Store design tokens and patterns for implementing agents
4. **Store in compound** — for each tech: setup commands, config files, API patterns, code examples, pitfalls
5. **Notify completion** — via chef if using Telegram mode, otherwise inform user in chat

---

## Phase 4: Initialize AGENTS.md

Use the `agents-md` skill to create project-specific agent guidelines based on the spec and design system.

This ensures implementing agents know:
- Project structure and conventions
- Tech stack specifics and patterns
- **Design system tokens and patterns**
- Commands for build, test, lint, etc.
- Code style preferences
- Any project-specific rules from the spec

---

## Rules

- **Open questions over multiple choice** — let users express freely
- **Each question builds on previous** — show you're listening
- **Go deep on unclear areas** — don't accept vague answers for critical details
- **Be specific about tech** — get exact library names, not categories
- **One question at a time** — wait for user response before asking next
- **Batch when appropriate** — in built-in mode, can group 2-3 related questions if context warrants it
