---
name: charted-review
description: Reviews a design doc with expert sub-agents
---

# Context

- designDocPath: $ARGUMENTS[0]

# Goal

Review the design doc at `${designDocPath}` by dispatching **four expert sub-agents in parallel**, then synthesize their feedback into a single, actionable review.

# Step 1 - Set up agents

If the sub-agents from [Step 2](#step-2--parallel-expert-reviews) are not already configured, ask me to install them.
If I confirm, copy sub-agents from the [./assets/agents](./assets/agents) folder to the [{workspaceRoot}/.cursor/agents]({workspaceRoot}/.cursor/agents) folder if using Cursor. Adapt the paths if I am not using Cursor.

# Step 2 — Parallel Expert Reviews

Spawn the following four sub-agents **simultaneously** (all in one message). Each agent receives the full design doc content and must return a structured review.

| Sub-agent type         | Focus area                                                                                                                            |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `accessibility-expert` | Accessibility of the proposed UI — ARIA, keyboard navigation, screen-reader support, color contrast, focus management, semantic HTML. |
| `security-analyst`     | Security implications — input validation, injection risks, auth/authz gaps, data exposure, secure defaults.                           |
| `ux-expert`            | Usability — interaction patterns, error/empty/loading states, information architecture, responsiveness, cognitive load.               |
| `xp-coach`             | Engineering practices — testability, incremental delivery, PR plan quality, simplicity, YAGNI, refactoring opportunities.             |

Each sub-agent prompt must include:

1. The **full content** of the design doc.
2. Instructions to return a review with exactly these sections:
   - **Praise** — what the design does well (keep brief).
   - **Concerns** — numbered list. Each concern has a short title, an explanation, and a concrete suggestion.
   - **Verdict** — one of: `approve`, `request-changes`, or `needs-discussion`.

# Step 3 — Synthesize & Detect Conflicts

Collect the four reviews. Present a **summary table** to the user:

| Expert | Verdict | # Concerns |
| ------ | ------- | ---------- |

Then list all concerns grouped by expert.

After listing, identify **conflicts** — cases where two or more experts give **contradictory guidance** (e.g., one says "add a confirmation dialog" and another says "reduce interaction steps", or one says "split into more PRs" and another says "too many PRs already").

# Step 4 — Challenge Round (if conflicts exist)

For **each conflict**:

1. Clearly describe the disagreement to both involved experts.
2. Re-launch each conflicting sub-agent with:
   - The original design doc.
   - Their own original review.
   - The opposing expert's concern that contradicts theirs.
   - Instructions to either **revise** their position or **defend** it with stronger justification.
3. Run conflicting pairs **in parallel** when they are independent.

After the challenge round, check if the experts now agree.

# Step 5 — Resolution

- **If all conflicts are resolved**: present the final consolidated review with the agreed-upon changes.
- **If any conflict remains unresolved**: present the remaining disagreement(s) to the user in a clear format:

> **Unresolved: {short title}**
>
> **{Expert A}** argues: _{summary of position}_
>
> **{Expert B}** argues: _{summary of position}_
>
> What is your call?

Wait for the user's decision on each unresolved conflict before producing the final consolidated review.

# Step 6 — Final Output

Produce a **consolidated review** with:

1. **Overall Verdict** — `approve`, `request-changes`, or `approve-with-nits` based on the aggregated outcome.
2. **Action Items** — a numbered checklist of concrete changes to make to the design doc, ordered by priority.
3. **Resolved Conflicts** — brief note on how each conflict was settled (expert concession or user decision).
