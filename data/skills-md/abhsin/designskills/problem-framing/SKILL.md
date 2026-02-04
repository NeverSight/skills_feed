---
name: problem-framing
description: Extract and structure fuzzy product ideas into validated problem statements, target users, and jobs-to-be-done. Use when a user has a raw idea, concept, or solution in mind but hasn't clearly articulated the problem, target user, or assumptions. This skill helps users communicate context to coding agents more effectively, reducing iteration cycles and "that's not what I meant" moments.
---

# Problem Framing

Transform raw product ideas into structured context that coding agents can execute on.

## Why This Exists

Extracts fuzzy product ideas from the user's head and structures them into clear problem statements, target users, and assumptions that coding agents can execute against.

## Workflow

### Step 1: Gather Raw Input

Ask the user to share their idea in any form—plain text, voice dump, bullet points, or existing notes. Accept whatever they have.

### Step 2: Run the Question Flow

Work through these questions conversationally. Skip or adapt based on what the user has already provided.

| Question | Purpose |
|----------|---------|
| What are you trying to build? | Get the raw idea out |
| Who specifically is this for? | Force specificity—"everyone" = no one |
| What problem does this solve for them? | Separate solution from problem |
| What are they doing today without this? | Reveals current alternatives, competition |
| When does this problem hit hardest? | Identifies trigger moments, urgency |
| What assumptions are you making? | Surfaces risks early |
| How will you know this worked? | Defines success criteria |

**Questioning style:**
- Ask one question at a time
- Probe vague answers ("Can you be more specific about who?")
- Reflect back what you hear to confirm understanding
- Don't overwhelm—adapt based on what's already clear

### Step 3: Generate Output

Once you have enough context, generate the structured output below. **Automatically save it to `design/01-problem-framing.md` using the Write tool** while continuing the conversation naturally.

## Output Format

```markdown
# Problem Framing: [Project Name]

## Problem Statement
[One clear sentence: WHO has WHAT problem WHEN]

## Target User
[Specific description—not "everyone" or "users"]

## Jobs to Be Done
- **Functional:** [What they're trying to accomplish]
- **Emotional:** [How they want to feel]
- **Social:** [How they want to be perceived]

## Current Alternatives
[What they do today without your solution]

## Trigger Moments
[When does this problem hit hardest?]

## Key Assumptions
- [Assumption 1]
- [Assumption 2]
- [Assumption 3]

## Success Criteria
- [How you'll measure if this works]

## Open Questions
- [Anything still unclear or needing validation]
```

## Handoff

After presenting the output, ask:
> "This captures your problem framing. Ready to move to `/user-modeling`, `/solution-scoping`, or `/prd-generation`, or want to refine anything first?"

**Note:** File is automatically saved to `design/01-problem-framing.md` for context preservation.