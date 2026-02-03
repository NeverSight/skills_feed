---
name: designing-beautiful-websites
description: >-
  Designs UX/UI for websites and web apps: UX strategy, information architecture,
  user flows, wireframes, UI systems, component specs, and polished visual design.
  Use when the user asks to design, redesign, modernise, critique, or improve a
  website, landing page, web app interface, design system, style guide, or UI kit.
allowed-tools: Read,Write,Bash(python:*)
---

# Designing Beautiful Websites

> **Core philosophy:** Make the next action obvious. Build from user goals upward. Systemise visuals. Validate early.

## Why this exists
Websites fail when they look “nice” but:
- don’t match user goals,
- hide key actions,
- require too much thinking,
- or are visually inconsistent.

This skill turns vague requests like “make it look better” into a **repeatable workflow** that produces:
- clear structure,
- usable interactions,
- and a cohesive visual system.

## What “done” looks like
Deliverables should be **usable by builders** (engineers, no-code builders, future agents):
- **Design brief**: users, goals, constraints, success metrics.
- **IA + flows**: sitemap (or nav model), and 1–3 key user journeys.
- **Layout + wireframes**: responsive page structure, component inventory.
- **Visual system**: tokens (type, spacing, colour, radius, shadow), and usage rules.
- **Component specs**: states, behaviour, empty/loading/error.
- **QA notes**: accessibility, responsiveness, edge cases.

If time is limited, prioritise: **clarity + hierarchy + consistency + accessibility**.

## Quick start workflow
Copy this checklist into the working notes and tick it off:

- [ ] **0. Inputs**: goal, audience, content, constraints, brand signals.
- [ ] **1. Strategy**: user goals + business goals + success metrics.
- [ ] **2. Scope**: pages/features/content; prioritise “key paths”.
- [ ] **3. Structure**: IA + navigation model + flows.
- [ ] **4. Skeleton**: wireframes + component inventory + responsive layout.
- [ ] **5. Surface**: visual system + page comps + states.
- [ ] **6. Validate**: usability pass + accessibility pass + consistency pass.
- [ ] **7. Hand-off**: tokens + component specs + implementation notes.

**Default rule:** do not jump to surface polish until structure and skeleton are believable.

## Non‑negotiables
### 1) Reduce thinking
Design so users rarely wonder:
- “Where am I?”
- “What do I do next?”
- “Is that clickable?”
- “Why did they call it that?”

Prefer **obvious** over clever.

### 2) Use conventions aggressively
Use familiar patterns unless there is a measured reason to deviate.
Unusual UI is a tax on every user interaction.

### 3) Clear visual hierarchy
Every screen must answer (at a glance):
- what this page is,
- what the primary action is,
- where the navigation is,
- what is secondary.

### 4) Grouping must be unambiguous
If spacing is doing grouping work:
- there must be **more space around groups than within groups**.

### 5) Feedback and forgiveness
Users should:
- see results of actions quickly,
- understand system status,
- and recover via undo/back/cancel where possible.

Prefer preventing errors over scolding users.

### 6) Accessibility is part of “beautiful”
Good aesthetics survive:
- keyboard-only use,
- low vision,
- colour‑blindness,
- small screens,
- slow networks.

## Default outputs format
When responding, produce:
1. **Design brief** (bullets)
2. **IA + key flows** (bullets + simple diagrams if useful)
3. **Component inventory** (table or list)
4. **Design tokens** (CSS variables or JSON)
5. **Page-level guidance** (for each page/section)
6. **States & edge cases**
7. **Implementation notes** (HTML structure, CSS approach, ARIA, etc.)

If the user asked for a critique/audit, output:
- issues (grouped by severity),
- fixes,
- and a “next iteration plan”.

## The workflow in practice
### Step 0 — Gather inputs (fast)
Ask only what’s needed; otherwise assume and state assumptions.

Minimum questions:
- **Primary user**: who is this for?
- **Primary goal**: what must they do?
- **Business goal**: what does success look like?
- **Content**: what is real copy/data?
- **Brand signals**: existing colours/logo/type/voice?
- **Constraints**: tech stack, deadline, accessibility level.

If inputs are missing, create a **working brief** with explicit assumptions.

### Step 1 — Strategy (align intent)
Produce:
- primary + secondary user goals,
- business objectives,
- success metrics,
- constraints/risk.

### Step 2 — Scope (decide what exists)
Define:
- pages/screens,
- features,
- content requirements,
- and what is out of scope.

Pick 1–3 **key paths** (the journeys that matter most). Optimise these first.

### Step 3 — Structure (make it findable)
Create:
- sitemap / nav model (global + local nav),
- page purpose statements,
- user flows for key paths.

Rule: navigation labels should be self‑evident; avoid internal jargon.

### Step 4 — Skeleton (arrange the UI)
Create:
- wireframes per page,
- component inventory,
- layout constraints (container widths, grids, spacing rhythm),
- and priority order per breakpoint.

Rule: start with the **feature/content**, not the “app shell”.

### Step 5 — Surface (make it beautiful)
Build a consistent system:
- spacing + sizing scale,
- typography scale,
- colour palette + shades,
- radius + border rules,
- elevation/shadow scale,
- icon + illustration style,
- motion rules (optional).

Apply to page comps.

### Step 6 — Validate (fast loops)
Run these checks:
- **Glance test (5–10 seconds):** can someone tell what this is and what to do?
- **Key‑path walkthrough:** can a first‑time user complete the main task?
- **Consistency pass:** are tokens respected? is hierarchy consistent?
- **Accessibility pass:** contrast, focus states, semantics, error messaging.

### Step 7 — Hand-off (make it buildable)
Provide:
- tokens,
- component specs (states + spacing + behaviour),
- responsive rules,
- and edge cases.

## Default starter system
Use this system unless the project already has one.

### Spacing & sizing scale (px)
Use a **non-linear** scale so choices are easy:
`0, 4, 8, 12, 16, 24, 32, 48, 64, 96, 128`

Rules:
- pick from the scale; avoid “one-off” numbers.
- for grouping: **inside-group spacing < between-group spacing**.

### Typography scale (px)
Keep it tight: 6–8 sizes is enough.

Suggested:
- `12` caption
- `14` small/body-secondary
- `16` body
- `20` subheading
- `24` h3
- `30` h2
- `40` h1/hero

Rules:
- default body line-height ~ `1.5–1.7`.
- limit line length for reading (~45–80 characters).
- use weight/colour/spacing before adding new sizes.

### Colour system
- define neutrals (backgrounds + text), one primary, and semantic accents.
- define **shades up front** (e.g., 100–900), don’t generate ad-hoc lightens/darkens.
- “Grey” can be warm or cool; keep a consistent temperature.

Contrast rules:
- normal text target: **≥ 4.5:1**
- large text target: **≥ 3:1**

### Elevation / shadow system
Use 3–5 shadow levels that map to meaning:
- 1: buttons/cards (subtle)
- 2: popovers/menus
- 3: sticky headers
- 4: modals
- 5: high priority overlays

### Borders
Prefer:
- spacing,
- subtle shadows,
- or small background changes
over heavy borders.

### Empty states
Empty states are a first impression.
They must:
- explain what’s empty,
- why it matters,
- and what to do next.

## Progressive disclosure
Use these reference files when deeper detail is needed:
- **Workflow & deliverables** → [references/WORKFLOW.md](references/WORKFLOW.md)
- **Page patterns** → [references/PAGE-PATTERNS.md](references/PAGE-PATTERNS.md)
- **Audit / critique** → [references/DESIGN-AUDIT.md](references/DESIGN-AUDIT.md)
- **Usability & navigation** → [references/USABILITY.md](references/USABILITY.md)
- **Visual design systems** → [references/VISUAL-DESIGN.md](references/VISUAL-DESIGN.md)
- **Interaction & forms** → [references/INTERACTION-DESIGN.md](references/INTERACTION-DESIGN.md)
- **Information architecture** → [references/INFORMATION-ARCHITECTURE.md](references/INFORMATION-ARCHITECTURE.md)
- **Content & microcopy** → [references/CONTENT-COPY.md](references/CONTENT-COPY.md)
- **Responsive rules** → [references/RESPONSIVE.md](references/RESPONSIVE.md)
- **Accessibility** → [references/ACCESSIBILITY.md](references/ACCESSIBILITY.md)
- **Checklists & templates** → [references/CHECKLISTS.md](references/CHECKLISTS.md)

## Quick search
If running locally:
```bash
grep -i "empty state\|hierarchy\|spacing" -n references/*.md
```

## THE EXACT PROMPT — UX/UI plan

```
You are designing a website UI/UX.

1) Write a crisp design brief (users, goals, constraints, success metrics).
2) Define information architecture + navigation model.
3) Identify 1–3 key user paths; write step-by-step flows.
4) Produce a component inventory for the key pages.
5) Propose a design token system (spacing, type, colour, radius, shadow) with rules.
6) Describe page layouts (mobile-first) and key interactions.
7) List empty/loading/error states and edge cases.
8) Run a usability + accessibility + consistency pass; revise.

Output must be specific and implementable.
Avoid vague advice.
```

## THE EXACT PROMPT — Visual polish pass

```
Review this UI for visual quality.

- Fix hierarchy (what is primary vs secondary vs tertiary?)
- Fix spacing (grouping clarity; rhythm; alignment)
- Fix typography (scale, weights, line height, line length)
- Fix colour (contrast, palette consistency, accent usage)
- Fix depth (shadows/borders; focus on meaning)
- Improve empty states and microcopy

Return:
1) a list of concrete changes
2) updated tokens (if needed)
3) before/after descriptions of the most important screens.
```

## THE EXACT PROMPT — Usability “glance test”

```
Pretend you have 10 seconds to look at this page.

Answer:
- What is this page?
- Who is it for?
- What are the top 3 things I can do here?
- What is the primary action?
- Where is the navigation?

Then list everything that created a question mark, and propose fixes.
```

## THE EXACT PROMPT — Component spec (single component)

```
Write a build-ready spec for this component.

Include:
- Purpose + when to use
- Anatomy (parts)
- Variants
- States: default/hover/focus/active/disabled/loading/error/success/empty
- Behaviour rules (keyboard + mouse + touch)
- Spacing + typography + colour tokens used
- Accessibility notes (ARIA if needed)
- Edge cases (long text, missing data, localisation)

Keep it concise but unambiguous.
```

## THE EXACT PROMPT — Accessibility pass

```
Review this design for accessibility.

Check:
- text contrast (normal and large text)
- keyboard navigation and focus visibility
- semantic element choices (button vs link vs div)
- form labelling and error announcement
- motion and reduced-motion behaviour

Return:
1) issues grouped by severity
2) concrete fixes (design + implementation)
3) any token changes needed (colours, focus styles)
```

## THE EXACT PROMPT — Responsive pass

```
Define responsive behaviour for this page/component.

For each breakpoint (small phone, large phone, tablet, desktop):
- layout (stack/columns)
- what becomes primary vs secondary
- how text wraps/truncates
- how tables, toolbars, and secondary actions adapt

Then list edge cases (long text, empty, error) and how they render.
```
