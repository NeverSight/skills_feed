---
name: ux-flow-designer
description: "Design and document app user flows, screens, and use cases using Mermaid diagrams and HTML wireframes. Use when creating user flow diagrams (flowcharts, state diagrams, sequence diagrams), screen wireframes (HTML), use case documentation, screen maps, or when the user mentions 'flows', 'wireframes', 'user journey', 'screen map', 'navigation flow', 'use cases', 'app flow', 'screen layout', 'flujos', 'pantallas', 'casos de uso'. Bridges Product (PRD) and Visual Design phases. Outputs serve as input for ui-ux-pro-max. Optional Figma export when user explicitly requests it."
---

# UX Flow Designer

Bridge between Product (PRD/features) and Visual Design.
Generate user flow documentation, Mermaid diagrams, and HTML wireframes.

## Role and Context

- **Input**: PRD (`docs/product/prd.md`) or user-provided feature descriptions
- **Output**: Diagrams + wireframes in `docs/ux-flows/`
- **Downstream**: Outputs feed into `ui-ux-pro-max` for visual design
- **Standalone**: Usable independently or as saas-pipeline Phase 4 step 1

## Prerequisites

On every invocation, verify:

```
CHECK ~/.claude/skills/ui-ux-pro-max/ exists
  IF missing → READ references/install-commands.md, offer install

CHECK docs/product/prd.md exists
  IF missing → CHECK ~/.claude/skills/product-manager-toolkit/
    IF missing → READ references/install-commands.md, offer install
    OR accept direct user input as feature descriptions

IF user mentions "figma" or "export to figma" →
  INFORM user of all requirements (see "Figma Export" section below)
  WAIT for user confirmation before reading references/figma-integration.md or checking MCPs
```

## Workflow

Designing app flows involves these steps. ALL four phases are mandatory and must be executed in order.

1. Extract use cases (from PRD or user input)
2. Generate Mermaid flow diagrams (screen map + per use case)
3. **Generate HTML wireframes as a clickable prototype (with inter-screen navigation) and offer browser preview** — NEVER skip this phase
4. Consolidate into master handoff document

---

### Phase 1 — Use Case Extraction

Read `docs/product/prd.md` if it exists. If no PRD, ask user for feature list or use case descriptions.

For each use case, document:

| Field | Description |
|-------|-------------|
| ID | `UC-001`, `UC-002`, etc. |
| Name | Short descriptive name |
| Actors | Who participates (User, System, Admin, etc.) |
| Preconditions | What must be true before the flow starts |
| Main Flow | Numbered step-by-step sequence |
| Alternative Flows | Branches, error paths, edge cases |
| Postconditions | What is true after the flow completes |

Save to `docs/ux-flows/use-cases.md`.

Present the use case list to user for approval before proceeding. Do not advance to Phase 2 without explicit confirmation.

---

### Phase 2 — Mermaid Diagrams

Read `references/mermaid-patterns.md` for syntax patterns and best practices.

**Step 1: Master Screen Map**

Generate `docs/ux-flows/diagrams/screen-map.md` — a flowchart showing ALL screens and general navigation paths of the entire app.

**Step 2: Per Use Case Diagrams**

For each approved use case, generate 3 diagrams:

1. **Flowchart** (`graph TD`) — screen-to-screen navigation with decision nodes
2. **State diagram** (`stateDiagram-v2`) — app states (loading, error, success, idle, etc.)
3. **Sequence diagram** (`sequenceDiagram`) — frontend-backend interaction with HTTP methods

Save to `docs/ux-flows/diagrams/{use-case-id}/`:
- `flow.md` — flowchart
- `states.md` — state diagram
- `sequence.md` — sequence diagram

**Constraints:**
- Max 15-20 nodes per diagram
- Split into sub-flows if more complex (link with `click` or reference)
- Use `classDef` for consistent styling across diagrams

Generate index at `docs/ux-flows/diagrams/INDEX.md` listing all diagrams with links.

---

### Phase 3 — HTML Wireframes (Clickable Prototype)

> **MANDATORY**: This phase MUST NOT be skipped, summarized, or deferred. Every invocation of this skill that reaches Phase 2 MUST continue to Phase 3. Do not ask the user whether to proceed — just do it.

**Step 1: Generate HTML files**

For each unique screen identified in the flowcharts, generate an HTML file using `assets/wireframe-template.html` as the base template.

Requirements:
- Self-contained: inline CSS only, no external dependencies
- Mobile-first: 375px viewport width
- Wireframe aesthetic: grays (`#f5f5f5` bg), dashed borders (`#ccc`), placeholder text (`#666`)
- Use template CSS classes: `.wf-header`, `.wf-input`, `.wf-button`, `.wf-card`, `.wf-nav`, `.wf-list-item`, `.wf-tab-bar`, `.wf-icon-placeholder`, `.wf-link`, `.wf-back`
- Include screen name and related use case in footer metadata

**Step 2: Add inter-screen navigation**

Every wireframe must link to other screens using `<a href="target.html" class="wf-link">`. This creates a clickable prototype navigable in any browser — no JavaScript needed.

Navigation rules:
- **Buttons** that logically navigate: wrap in `<a href="target.html" class="wf-link"><div class="wf-button">Label</div></a>`
- **Tab bar**: each tab is an `<a class="wf-link">` pointing to its screen. Tab bar must be consistent across all screens that share it.
- **Back buttons**: `<a href="previous.html" class="wf-link wf-back">&larr; Back</a>` in the `.wf-nav` bar
- **Tappable list items**: wrap in `<a href="detail.html" class="wf-link"><div class="wf-list-item">...</div></a>`
- **Tappable cards**: wrap in `<a href="target.html" class="wf-link"><div class="wf-card">...</div></a>`
- **No dead ends**: every screen must have at least one outgoing link (back button, tab bar, or action button)
- **No JavaScript**: pure HTML `<a>` navigation only — no onclick, no form submissions, no JS

**Step 3: Save and generate index**

Save all wireframes to `docs/ux-flows/wireframes/`.

Generate inventory at `docs/ux-flows/wireframes/INDEX.md`:

| Column | Description |
|--------|-------------|
| Screen name | Human-readable name |
| File link | Relative link to .html file |
| Related use cases | UC-IDs |
| Key elements | Main components on the screen |
| Outgoing links | List of screens this screen links to |

**Step 4: Offer browser preview**

After generating all wireframes, propose opening the main entry screen in the browser:
- If Chrome DevTools MCP is available: use `navigate_page` to open the file
- Fallback: use `open docs/ux-flows/wireframes/{entry-screen}.html` via Bash

Do not wait for the user to ask — proactively offer the preview.

---

### Phase 4 — Consolidation and Handoff

Generate master document `docs/ux-flows/UX-FLOWS.md`:

```markdown
# UX Flows — [App Name]

## Master Screen Map
Link to screen-map.md

## Screen Inventory
| Screen | Purpose | Wireframe | Use Cases |
|--------|---------|-----------|-----------|
| ...    | ...     | link      | UC-001    |

## Use Case Diagrams
### UC-001: [Name]
- Flow: link
- States: link
- Sequence: link

## Clickable Prototype Links
| From Screen | Element | To Screen |
|-------------|---------|-----------|
| login.html  | [Login] button | home.html |
| ...         | ...     | ...       |

## Navigation Patterns
Summary of recurring navigation patterns (tab bar, back navigation,
modal flows, drawer menus, etc.)

## Open Questions
Design decisions and open questions for ui-ux-pro-max phase.
```

After completing the handoff document, inform the user:
- The wireframes can be exported to Figma using the official **Code to Canvas** integration
- Only requires Figma desktop app with Dev Mode MCP Server enabled (2-step setup)
- If interested, the user can request "export to figma" and the setup steps will be presented

---

## Output Structure

```
docs/ux-flows/
├── UX-FLOWS.md                          # Master handoff document
├── use-cases.md                         # All use cases
├── diagrams/
│   ├── INDEX.md                         # Diagram index
│   ├── screen-map.md                    # Master app navigation
│   ├── uc-001-{name}/
│   │   ├── flow.md                      # Flowchart
│   │   ├── states.md                    # State diagram
│   │   └── sequence.md                  # Sequence diagram
│   └── ...
└── wireframes/
    ├── INDEX.md                         # Screen inventory
    ├── home.html
    ├── login.html
    └── ...
```

## Figma Export (Optional)

This skill can export wireframes to Figma. Do not check for Figma MCP automatically.

**When to mention**: At the end of Phase 4 (handoff), inform the user that Figma export is available as an optional next step.

**When the user requests Figma export**, follow this protocol:
1. **First**: Inform the requirements before attempting anything:
   - Figma desktop app with **Dev Mode MCP Server** enabled (Preferences → Enable "Dev Mode MCP Server")
   - MCP added to Claude Code: `claude mcp add --transport sse figma-dev-mode-mcp-server http://127.0.0.1:3845/sse`
   - Chrome DevTools MCP (already used for wireframe preview)
   - See full details in `references/figma-integration.md`
2. **Then**: Ask user to confirm they have or want to set up these prerequisites
3. **Only then**: Read `references/figma-integration.md` and follow the export workflow

Never silently attempt Figma operations. Always present the requirements first.
