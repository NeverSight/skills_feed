---
name: tool-design-style-selector
description: "Use when you need to define or converge a project's visual direction. Scan project documentation to identify intent, then produce a design-system.md (either preserve existing style or pick from 30 presets). Triggers: design system, design spec, UI style, visual style, design tokens, color palette, typography, layout. Flow: scan → intent → (gate) preserve vs preset → deploy design-system.md after confirmation → (default) implement UI/UX per design-system.md (plan first, then execute)."
---

# Design Style Selector

Scan project, identify intent, recommend and deploy the most suitable design system style.

## Style Presets

This skill can either:

1) **Preserve existing style** and extract it into `design-system.md` (recommended when the project already looks “mature”), or  
2) Apply one of **30 preset styles** and generate `design-system.md`.

Style files live in `styles/` and are indexed in:
- [`styles-index.md`](styles-index.md) (ID → filename → theme)

Quick examples of presets:
- `05-saas` (B2B tools, dashboards)
- `08-swiss-minimalist` (clean hierarchy, corporate)
- `13-neo-brutalism` (bold, indie/creative)
- `19-minimal-dark` (focus mode, dev tools)

## Execution Flow

### Step 1: Scan Project
```
Scan the following files to identify project intent:
- README.md / README
- package.json / pyproject.toml / Cargo.toml
- Existing Claude.md / agent.md / AGENTS.md
- src/ or app/ directory structure
- Existing style files (tailwind.config, globals.css)
- Brand assets (logo, favicon)
```

### Step 2: Analyze Intent
Extract the following information:
- **Project Type**: SaaS/corporate site/e-commerce/blog/tool/game/...
- **Target Users**: Developers/enterprises/consumers/children/professionals/...
- **Brand Tone**: Professional/playful/luxury/minimal/bold/...
- **Tech Stack**: React/Vue/Next.js/static site/...
- **Existing Design Constraints**: Current colors/fonts/component libraries

### Step 2.5: Existing Style Gate (For existing projects, first determine whether to "preserve style")

> Purpose: Avoid forcing a reskin on projects that are "already good-looking/already branded", preventing unnecessary UI rework and cognitive costs.

When a repo already has UI, first do a quick "style maturity" assessment and write out evidence (don't be purely subjective):

**Signals of mature style (meeting multiple criteria is sufficient):**
- Has clear design tokens: `tailwind.config.*` has fairly complete color/font/radius/shadow/spacing config, or `:root` CSS variables form a system
- Component library/component style is consistent (buttons/inputs/cards etc. semantic components have high reuse)
- Layout and spacing are basically consistent across pages (rarely see hardcoded color values/pixels/inline styles)
- Has brand assets (logo, favicon, brand colors) consistently reflected in UI

**Signals of immature/inconsistent style:**
- Same type of components appear in multiple styles (buttons/forms/cards inconsistent)
- Mixed use of multiple UI libraries/multiple sets of tokens (e.g., multiple Tailwind color schemes + multiple globals.css)
- Lots of scattered hex values/inline styles/random spacing

**Gate Output (required):**
- If you judge "style is mature": default recommend **preserve style and extract to design-system.md** (don't force switch to preset)
- If you judge "not mature": proceed to Step 3, recommend from presets and replace

**Ask only one question (multiple choice) for user to select strategy:**
> I've scanned the current project style as [fairly mature / not very unified]. What would you like:
> 1) Preserve existing style: I'll reverse-extract current UI into `design-system.md` (document only + light unification, no major reskin)
> 2) Use this repo's preset: Select one from 30 styles, replace with unified style (requires more significant UI changes)
> 3) Hybrid: Keep the general direction, but use design tokens/component specs to converge inconsistencies (moderate changes)

If selecting 1): Step 3 doesn't need "recommend 30 styles", instead do "extract and generate design-system.md".

### Step 3: Recommend Styles
Based on analysis results, recommend **Top 3** best matching styles:
```
Recommendation #1: [Style Name] ⭐ Best Match
- Match Score: 95%
- Reason: ...
- Fit Points: ...

Recommendation #2: [Style Name]
- Match Score: 85%
- Reason: ...

Recommendation #3: [Style Name]
- Match Score: 75%
- Reason: ...
```

### Step 3.5 (Default when installed): Enrich tokens via `tool-ui-ux-pro-max`

If `tool-ui-ux-pro-max` is installed, run it by default to make `design-system.md` more concrete (palette + typography + UX constraints), instead of relying on a single preset text blob. Only skip if the user explicitly asks to keep the spec minimal, and record the reason.

Recommended searches (pick 1–3 results per category, then synthesize into `design-system.md`):

```bash
# Typography pairing (heading + body + CSS import)
python3 ~/.claude/skills/tool-ui-ux-pro-max/scripts/search.py "<brand tone keywords>" --domain typography

# Color palette (primary/secondary/CTA/background/text/border)
python3 ~/.claude/skills/tool-ui-ux-pro-max/scripts/search.py "<product type keywords>" --domain color

# UX / accessibility guardrails (avoid common “looks good but feels broken” issues)
python3 ~/.claude/skills/tool-ui-ux-pro-max/scripts/search.py "accessibility" --domain ux
python3 ~/.claude/skills/tool-ui-ux-pro-max/scripts/search.py "animation" --domain ux

# Stack-specific implementation constraints (pick the actual project stack)
python3 ~/.claude/skills/tool-ui-ux-pro-max/scripts/search.py "layout responsive" --stack nextjs
```

### Step 4: User Confirmation
- Present recommendation reasons
- Allow user to select or request more options
- Proceed to deployment after confirmation

### Step 5: Deploy Design System
```
1. Copy selected style file to project
2. Rename to design-system.md
3. Placement location:
   - Primary: Project root directory
   - Alternative: docs/ or .cursor/ or .claude/
4. If Claude.md / agent.md exists:
   - Add reference at the top of that file
   - Explain that design-system.md is the unified design constraint
```

> If "preserve existing style" was selected in Step 2.5: "deployment" here is not copying a preset, but writing the tokens, typography rules, component style constraints you extracted from code/styles into `design-system.md` (also placed at root).

### Step 6: Implement UI/UX According to design-system.md (Execute by Default)

> The goal of this step is: **Make design-system.md actually "live in the UI"**, not just generate a document and stop.

Execution requirements:
- First produce an executable UI/UX transformation plan (clearly specify which pages/components, scope of changes, acceptance criteria, how to rollback).
- Then implement according to plan (when involving large-scale visual/layout/interaction changes, must have confirmation points).

Recommended implementation order (start from "where it can best align the style"):
1. **Design tokens / global style entry**: Fonts, colors, spacing, radius, shadows, basic typography (prioritize centralizing in one place, avoid scattering).
2. **Component layer**: Unify style for buttons, inputs, cards, dialogs and other base components (to be reused by all pages later).
3. **Page layer**: Prioritize changing "first impression pages" and "core flow pages" to ensure overall consistency.

Note:
- If user explicitly states "don't want to change UI, just want documentation", skip this step and record the reason (e.g., write to run's notes/summary).

## Output Format

### Scan Report
```
📁 Project Scan Complete

Project Name: [name]
Project Type: [type]
Tech Stack: [stack]
Target Users: [audience]
Brand Tone: [tone]

Existing Design Assets:
- ✅ tailwind.config.js (has color config)
- ❌ No design system documentation
- ⚠️ Claude.md exists (needs integration)
```

### Deployment Confirmation
```
✅ Design System Deployed

File: /design-system.md
Style: [selected style]

Completed:
1. Created design-system.md
2. Added reference in Claude.md

Next Steps (execute by default):
- Generate UI/UX transformation plan based on design-system.md (clarify page/component scope and acceptance criteria)
- After user confirmation, redo UI/UX according to plan to implement design specs (avoid "document exists but UI unchanged")
```

## Integration Rules

### When Claude.md / agent.md Exists
Add at the top of the file:
```markdown
## Design System

This project uses a unified design system, see [design-system.md](./design-system.md).

All UI development must follow the design-system.md for:
- Color specifications
- Typography rules
- Component styles
- Spacing system
```

### When No Existing Config Files
Create design-system.md directly in root directory.

## Style File Location

All style prompt files are located at: `styles/`

File naming: `[id]-[name].md` (e.g., `01-monochrome.md`)

## Notes

1. **Don't overwrite existing files**: If design-system.md already exists, ask whether to replace
2. **Preserve user choice**: Recommendation doesn't mean mandatory, user can choose any style
3. **Explain integration method**: Clearly explain how to use after deployment
4. **Tech stack adaptation**: Adjust specific implementation suggestions based on project tech stack
