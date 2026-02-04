---
name: prd-generation
description: Generate lean, actionable Product Requirements Documents from upstream design thinking artifacts or raw input. Use when a user needs to define what they're building with enough structure to guide development but without enterprise bloat. Outputs a PRD that feeds directly into UX specs and development prompts.
---

# PRD Generator

Create right-sized Product Requirements Documents that solo devs and small teams can actually use.

## Why This Exists

Generates lean PRDs with enough structure to guide development without enterprise bloat.

## Input Requirements

This skill works best with upstream context from:
- `problem-framing` output (problem statement, target user, JTBD, assumptions)
- `user-modeling` output (personas, scenarios)
- `solution-scoping` output (feature priorities, MVP boundaries)

Can also work from scratch if user provides enough context about their idea.

## Workflow

### Step 1: Gather Context

If upstream artifacts exist, ingest them. If not, ask for:
- What are you building?
- Who is it for?
- What problem does it solve?
- What's the MVP scope?

### Step 2: Fill Gaps

Check for missing elements and ask targeted questions:

| Missing Element | Question |
|-----------------|----------|
| Success metrics | "How will you know this worked? What would you measure?" |
| Feature priorities | "If you could only ship one thing, what would it be?" |
| Constraints | "Any technical constraints? Timeline? Budget?" |
| Non-goals | "What are you explicitly NOT building?" |

Keep it conversational—don't interrogate.

### Step 3: Generate PRD

Use the output format below. Adapt sections based on project complexity.

## Output Format

**Automatically save the output to `design/05-prd.md` using the Write tool** while presenting it to the user.

```markdown
# PRD: [Project Name]

## Overview
[2-3 sentences: what this is and why it matters]

## Problem Statement
[One clear sentence: WHO has WHAT problem WHEN]

## Target User
[Specific description of primary user]

**Characteristics:**
- [Key trait 1]
- [Key trait 2]
- [Key trait 3]

## Goals & Success Metrics

| Goal | Metric | Target |
|------|--------|--------|
| [Goal 1] | [How measured] | [Success threshold] |
| [Goal 2] | [How measured] | [Success threshold] |

## User Stories

### Must Have (MVP)
- As a [user], I want to [action] so that [outcome]
- As a [user], I want to [action] so that [outcome]
- As a [user], I want to [action] so that [outcome]

### Should Have (v1.1)
- As a [user], I want to [action] so that [outcome]
- As a [user], I want to [action] so that [outcome]

### Could Have (Future)
- As a [user], I want to [action] so that [outcome]

## Features

### [Feature 1 Name]
**Priority:** Must Have
**Description:** [What it does]
**User value:** [Why it matters]
**Acceptance criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

### [Feature 2 Name]
**Priority:** Must Have
**Description:** [What it does]
**User value:** [Why it matters]
**Acceptance criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

### [Feature 3 Name]
**Priority:** Should Have
[Same structure]

## Scope

### In Scope (MVP)
- [What you're building]
- [What you're building]

### Out of Scope
- [What you're NOT building]
- [What you're NOT building]

### Future Considerations
- [What might come later]

## Assumptions & Risks

### Assumptions
- [Assumption 1]
- [Assumption 2]

### Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk 1] | [High/Med/Low] | [How to address] |
| [Risk 2] | [High/Med/Low] | [How to address] |

## Technical Considerations
[Optional — include only if relevant]
- **Platform:** [Web/mobile/desktop]
- **Key integrations:** [APIs, services]
- **Data:** [Storage, persistence needs]
- **Constraints:** [Performance, security, compliance]

## Open Questions
- [Anything still unresolved]
- [Decisions needed before development]

## Appendix
[Optional — link to research, competitive analysis, wireframes]
```

## Adaptation Guidelines

**For simple projects (weekend build):**
- Skip Technical Considerations
- Collapse User Stories into Features
- Minimal Risks section
- 1-2 pages total

**For medium projects (side project, MVP):**
- Full structure as shown
- 2-4 pages total

**For complex projects (startup MVP, team project):**
- Add more detail to Features
- Expand Technical Considerations
- Include Appendix with research
- 4-6 pages total

## Writing Guidelines

- **Be specific, not generic** — "Users can filter tasks by due date" not "Users can filter tasks"
- **Acceptance criteria are testable** — Can you verify yes/no if it's done?
- **Priorities are honest** — If everything is "Must Have," nothing is
- **Out of Scope is explicit** — Prevents scope creep later

## Handoff

After presenting the PRD, ask:
> "Want to move to `/ux-specification` for detailed flows and screens, or go straight to `/prompt-export`?"

**Note:** File is automatically saved to `design/05-prd.md` for context preservation.