---
name: geist-learning-lab
description: Build explorative, interactive learning experiences as Next.js apps using the Geist design system. Use when creating tutorials, explorable explanations, interactive lessons, code sandboxes, quizzes, or any educational UI. Covers the Learning Loop pedagogy, 23+ learning component patterns, progress tracking, spaced repetition, and Bret-Victor-style interactive exploration — all with Geist's dark-first minimal aesthetic.
---

# Geist Learning Lab

Build interactive learning experiences that teach by making the learner *do something, get feedback, and iterate* — using Geist's dark-first, minimal, precise UI language.

## Design Philosophy

- **Learning loops, not pages** — Every screen completes: prompt → attempt → feedback → refinement → checkpoint
- **Cognitive load management** — Progressive disclosure, chunking, one concept + one action at a time
- **Error-friendly design** — Mistakes are expected; the UI normalizes them and turns them into learning moments
- **Interactive representations** — Sliders, toggles, diagrams, live code — not just text
- **Geist precision** — Dark backgrounds, tight tracking, semantic color, 4px grid, Swiss typography

## Critical Rules

1. **Every lesson must include at least one attempt+feedback loop** — No passive-only pages
2. **Every interactive control must have a visible effect** — Within ~100ms or show loading state
3. **Progress/review must exist even in a prototype** — Track steps completed, checkpoints passed
4. **Active attempt before explanation** — Ask a question or show a task, then explain
5. **Immediate, specific feedback** — "Correct" isn't enough; explain *why*
6. **Multiple representations** — Always at least 2 of: text, code, visual, interactive, real data
7. **Color is learning signal** — Green=correct, Red=incorrect, Amber=hint/warning, Blue=info/definition
8. **Progressive disclosure by default** — Depth behind "Why?", "Edge Cases", "Formal Definition"
9. **URL state for exploration** — Shareable slider/toggle configurations via search params
10. **Misconception-first design** — Bake in common traps: "Most people get this wrong because..."

## The Learning Loop (Central Doctrine)

Every lesson repeats this cycle:

| Step | What Happens | Component |
|------|-------------|-----------|
| **Orient** | What you'll learn in 5-10 min | Heading + learning objective |
| **Attempt** | Learner predicts/answers/edits first | QuickCheck, CodePlayground, ParameterDock |
| **Feedback** | Immediate + specific response | Feedback surface (green/red panel) |
| **Explain** | Short explanation anchored to their attempt | Callout, WorkedExample |
| **Extend** | Variation, edge case, or transfer task | BeforeAfterSplit, ConceptExplorer |
| **Checkpoint** | Quick recall question | QuickCheck with ConfidenceRating |
| **Reflect** | "What changed in your understanding?" | Optional text input or self-rating |

## "Aha Moment" Design Patterns

| Pattern | How It Works | When to Use |
|---------|-------------|-------------|
| **Prediction Gap** | "What do you think happens if...?" then reveal | Before introducing a concept |
| **Contrast Pair** | Two near-identical cases with different outcomes | Clarifying subtle distinctions |
| **Slider to Failure** | Let learner push a parameter until it breaks | Understanding boundaries/limits |
| **Time Travel** | Scrub algorithm step-by-step, watch invariants | Algorithms, state machines |
| **Misconception Trap** | Tempting wrong option, then explain why wrong | Common errors in a domain |

## Quick Color Reference (Learning Semantics)

| Signal | Color Token | Hex | Usage |
|--------|------------|-----|-------|
| Correct | green-700 | `#46A758` | Success feedback, completed steps |
| Incorrect | red-700 | `#E5484D` | Error feedback, failed checks |
| Hint/Caution | amber-700 | `#FFB224` | Hints, warnings, "watch out" |
| Info/Definition | blue-700 | `#0070F3` | Definitions, current step, links |
| Default | gray-400 | `#737373` | Everything else: borders, muted text |
| Progress done | green-700 dot | `#46A758` | Completed step indicator |
| Progress current | blue-700 ring | `#0070F3` | Current step focus state |
| Progress pending | gray-400 dot | `#737373` | Upcoming steps |

## Component Library (23 Patterns)

### Lesson Flow & Progress
`<LessonShell />` `<ProgressRail />` `<StepFlow />` `<CheckpointCard />` `<ResumeBanner />`

### Explorable Explanations
`<ParameterDock />` `<LiveOutputPanel />` `<ConceptExplorer />` `<InteractiveDiagram />` `<BeforeAfterSplit />` `<TimelineExplorer />` `<ConceptMap />`

### Code Learning
`<CodePlayground />` `<DiffEditor />` `<TaskRunner />` `<SnippetCopy />`

### Quizzes & Active Recall
`<QuickCheck />` `<ConfidenceRating />` `<HintLadder />` `<MistakeAnalyzer />`

### Reading Support
`<GlossaryPopover />` `<Callout />` `<WorkedExample />`

## Typography in Learning Context

| Element | What It Means | Style |
|---------|--------------|-------|
| Big heading | "What you're doing" | `text-heading-{32\|24}` semibold, negative tracking |
| Small label | "Where you are" | `text-label-{14\|12}` gray-400 |
| Mono | "What the computer sees" | `text-copy-14-mono` or `text-label-14-mono` |
| Body | Reading content | `text-copy-14` or `text-copy-16`, max-w-2xl |

## Layout Patterns

| Context | Max Width | Structure |
|---------|-----------|-----------|
| Reading content | `max-w-2xl` / `max-w-4xl` | Single column, comfortable line length |
| Interactive lab | `max-w-6xl` | Two panels: explanation + playground |
| Full explorer | `max-w-7xl` | Three zones: nav + content + lab panel |

## App Router Structure

```
/                                    → Landing / course picker
/learn                               → Course catalog + resume
/learn/[courseSlug]                   → Course overview, modules, progress
/learn/[courseSlug]/[moduleSlug]      → Module overview
/learn/[courseSlug]/[moduleSlug]/[lessonSlug]  → Lesson shell
```

## File Organization

```
content/courses/<courseSlug>/course.json       → Metadata, module order
content/courses/<courseSlug>/<module>/<lesson>.mdx  → Lesson content
components/learning/                           → Reusable learning components
lib/learning/progress.ts                       → Schema + storage adapters
lib/learning/grading.ts                        → Quiz validation, code tests
lib/learning/spaced.ts                         → Review scheduling
```

## References

- `references/lesson-shell.md` — LessonShell, ProgressRail, StepFlow, CheckpointCard, ResumeBanner TSX patterns
- `references/explorable-explanations.md` — ParameterDock, LiveOutputPanel, ConceptExplorer, InteractiveDiagram, BeforeAfterSplit, TimelineExplorer, ConceptMap
- `references/code-learning.md` — CodePlayground (read-only/guided/free), DiffEditor, TaskRunner, SnippetCopy
- `references/quiz-assessment.md` — QuickCheck, ConfidenceRating, HintLadder, MistakeAnalyzer with feedback patterns
- `references/reading-support.md` — GlossaryPopover, Callout variants, WorkedExample with stepwise reveal
- `references/pedagogical-framework.md` — The Learning Loop doctrine, progressive disclosure rules, aha patterns, scaffolded complexity
- `references/architecture.md` — Next.js App Router routing, MDX content system, state management, file organization
- `references/progress-state.md` — Progress schema, localStorage adapter, spaced repetition, URL state for explorations
- `references/learning-animations.md` — Step transitions, feedback reveals, diagram animations, reduced-motion compliance
