---
name: prompt-export
description: Convert structured UX specs and product context into a sequenced prompts.md file for Claude Code. Use when a user has completed upstream design thinking (problem framing, PRD, UX spec) and needs to translate that into step-by-step prompts that coding agents can execute incrementally. This skill bridges design artifacts to code generation.
---

# Prompt Export

Transform design artifacts into a sequenced `prompts.md` file that guides coding agents through incremental development.

## Why This Exists

Breaks development into sequenced prompts with checkpoints, preventing agents from losing focus or making assumptions.

## Input Requirements

This skill expects upstream context from one or more of:
- Problem framing document
- PRD
- UX spec (flows, screens, interactions)
- Any combination of the above

If the user hasn't completed upstream work, suggest they start with `problem-framing` or `prd-generation` first.

## Workflow

### Step 1: Gather Artifacts

Ask the user to provide their design artifacts. Accept any format—markdown, docs, images of sketches, bullet points.

### Step 2: Extract Key Elements

From the provided artifacts, identify:

| Element | Source |
|---------|--------|
| Project overview | Problem statement, target user |
| Core features | PRD, solution scope |
| User flows | UX spec |
| Screen/component descriptions | UX spec |
| Interactions & states | UX spec |
| Tech preferences | User input or infer from context |
| Constraints | MVP scope, what's out |
| Success criteria | Problem framing, PRD |

### Step 3: Clarify Gaps

If critical information is missing, ask targeted questions:
- "What tech stack do you want? (React, vanilla JS, etc.)"
- "Any specific libraries or frameworks to use or avoid?"
- "Mobile-first, desktop-first, or responsive?"
- "Any authentication or data persistence needs?"

Keep questions minimal—infer where possible.

### Step 4: Decompose Into Prompts

Break the project into a logical sequence. Typical prompt sequence:

1. **Project setup** — scaffold, dependencies, config
2. **Data/state foundation** — types, schemas, state structure
3. **Core component(s)** — one prompt per major component or screen
4. **Feature implementation** — one prompt per feature
5. **Integration** — connect components, wire up flows
6. **Polish** — error states, loading states, edge cases
7. **Final review** — cleanup, optimization, documentation

Adapt based on project complexity. Simple projects might be 3-4 prompts. Complex ones might be 10+.

### Step 5: Generate prompts.md

Output a single file the user can reference as they work through Claude Code.

## Output Format

**Automatically save the output to `prompts.md` (in project root) using the Write tool** while presenting it to the user.

```markdown
# [Project Name] — Development Prompts

## Context
[2-3 sentences: what this is, who it's for, core problem it solves]

**Tech stack:** [framework, styling, key libraries]
**Key constraints:** [what's in/out of scope]

---

## Prompt 1: Project Setup
> [Prompt text the user pastes into Claude Code]

**Goal:** [What this accomplishes]
**Checkpoint:** [How to verify it worked before moving on]

---

## Prompt 2: [Name]
> [Prompt text]

**Goal:** [What this accomplishes]
**Checkpoint:** [How to verify]

---

## Prompt 3: [Name]
> [Prompt text]

**Goal:** [What this accomplishes]
**Checkpoint:** [How to verify]

---

[Continue for all prompts...]

---

## Final Checklist
- [ ] [Success criterion 1]
- [ ] [Success criterion 2]
- [ ] [Success criterion 3]
```

## Prompt Writing Guidelines

Each prompt should:
- **Be self-contained** — agent shouldn't need to read previous prompts
- **Reference existing files** — "In `src/components/Header.jsx`, add..."
- **Specify acceptance criteria** — what "done" looks like
- **Stay focused** — one logical unit of work

**Good prompt:**
> "Create a TaskList component in src/components/TaskList.jsx that displays an array of tasks. Each task shows a title, due date, and completion checkbox. Clicking the checkbox toggles completion state. Use Tailwind for styling. The component receives tasks as a prop."

**Bad prompt:**
> "Build the task management features."

## Adaptation Guidelines

**Simple project (3-5 prompts):**
- Setup → Core UI → Features → Polish

**Medium project (5-8 prompts):**
- Setup → Data layer → Screen 1 → Screen 2 → Feature A → Feature B → Integration → Polish

**Complex project (10+ prompts):**
- Consider grouping into phases with phase summaries
- Add dependency notes ("Run after Prompt 3")
- Include rollback hints for risky steps

## Handoff

After presenting the prompts, inform the user:
> "Work through these prompts sequentially with Claude Code—each builds on the last. Check the checkpoint before moving to the next prompt."

Offer to:
- Adjust prompt granularity (more/fewer steps)
- Reorder sequence
- Add detail to specific prompts

**Note:** File is automatically saved to `prompts.md` in the project root.