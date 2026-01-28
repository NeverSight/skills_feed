---
name: aim
description: Clarify the outcome you want - a change in user behavior, not a feature shipped. Use at the start of any work to ground the session in strategic intent.
---

# /aim

Clarify the outcome you want. An aim is a change in user behavior, not a feature shipped. This is the first step in the Intent-Execution-Review loop.

**The aim IS the abstraction.** When you clarify what behavior you want to change, you're abstracting the business domain itself. Features are just the mechanism; the aim is why they matter.

## When to Use

Invoke `/aim` when:

- **Starting new work** - Before diving into problem-statement or problem-space
- **Scope feels fuzzy** - You can describe what you're building but not why
- **Multiple solutions seem valid** - Aim clarifies which one actually moves the needle
- **Work has drifted** - Return to aim to check if you're still on track
- **Team is misaligned** - Shared aim surfaces hidden assumptions

**Do not use when:** You already have a crisp aim and need to explore the problem space or solution space. Move to `/problem-statement` or `/problem-space` instead.

## The Aim Process

### Step 1: State the Desired Behavior Change

Start with the user, not the system. What do you want users to do differently after this work ships?

> "Users will [specific behavior] instead of [current behavior]."

Bad: "Add dark mode toggle"
Good: "Users can work comfortably at night without eye strain"

Bad: "Improve onboarding flow"
Good: "New users reach their first value moment within 5 minutes"

**Key distinction:** Features are outputs. Behavior changes are outcomes.

### Step 2: Identify the Mechanism

The mechanism is your hypothesis - the causal lever you believe will produce the behavior change. It's the "because" that connects your work to the outcome.

> "This will happen because [mechanism]."

Format:
```
Mechanism: [What you're changing]
Hypothesis: [Why you believe it will produce the outcome]
Assumptions: [What must be true for this to work]
```

### Step 3: Define the Feedback Signal

How will you know if the aim is achieved? What signal validates or disproves the mechanism?

> "We'll know it's working when [observable signal]."

Good feedback signals are:
- **Observable** - You can actually measure or see them
- **Timely** - You'll know within a reasonable timeframe
- **Attributable** - The signal connects to your mechanism, not noise

### Step 4: Set Guardrails

What constraints should bound this work? What would cause you to stop or change direction?

Format:
```
Guardrail: [boundary]
Reason: [why this matters]
Trigger: [when to revisit this constraint]
```

## Output Format

Always produce an aim statement in this structure:

```
## Aim Statement

**Aim:** [One sentence: the behavior change you want]

**Current State:** [What users do now]
**Desired State:** [What users will do after]

### Mechanism
**Change:** [What you're building/changing]
**Hypothesis:** [Why you believe this produces the outcome]
**Assumptions:** [What must be true]

### Feedback
**Signal:** [How you'll know it's working]
**Timeframe:** [When you'll have signal]

### Guardrails
- [Guardrail 1]
- [Guardrail 2]
```

## Examples

### Example 1: Feature Request to Aim

**Input:**
```
/aim

We need to add a dark mode toggle to the settings page.
```

**Output:**
```
## Aim Statement

**Aim:** Users can work comfortably during extended evening sessions without eye strain.

**Current State:** Users either strain their eyes or stop using the app after dark.
**Desired State:** Users work as long as they need, regardless of ambient lighting.

### Mechanism
**Change:** Theme system with dark variant, exposed via settings toggle
**Hypothesis:** Reducing screen brightness and contrast in low-light environments reduces eye strain, increasing comfortable usage time.
**Assumptions:**
- Users actually work in low-light conditions (validate with usage time data)
- Eye strain is the blocker, not just preference (could survey)
- A toggle is discoverable enough (vs. auto-detect)

### Feedback
**Signal:** Session duration in evening hours (6pm-midnight) increases
**Timeframe:** 2 weeks post-launch to see pattern

### Guardrails
- Don't break existing light theme (test both paths)
- Don't over-engineer: one dark theme, not a theme builder
- Revisit if <5% of users actually enable it after 30 days
```

### Example 2: Vague Strategic Goal to Aim

**Input:**
```
/aim

We need to improve developer experience.
```

**Output:**
```
## Aim Statement

**Aim:** Developers spend less than 10 minutes from git clone to running their first successful test.

**Current State:** New developers report 45-90 minutes to get a working dev environment. Some give up.
**Desired State:** Developers are productive within their first coffee break.

### Mechanism
**Change:** Containerized dev environment with pre-configured dependencies
**Hypothesis:** Most setup time is spent on environment configuration, not understanding code. A working container removes the configuration variable.
**Assumptions:**
- Docker is acceptable for dev workflow (some devs resist containers)
- Environment issues are the primary friction (not docs, not code complexity)
- Container startup time is acceptable (<2 min)

### Feedback
**Signal:** Time from clone to first passing test (measured in onboarding script)
**Timeframe:** Immediate per-developer, aggregate after 5 new devs

### Guardrails
- Container must work on Mac, Linux, and Windows (WSL2)
- Don't require Docker for those who prefer native setup
- Revisit if container approach creates new friction (debugging, IDE integration)
```

### Example 3: Checking Aim Mid-Work

**Input:**
```
/aim

I'm three days into this auth refactor and not sure if I'm still solving the right problem.
```

**Output:**
```
## Aim Check

**Original aim (inferred):** Simplify the authentication flow for easier maintenance.

Let me ask clarifying questions to validate:

1. **What behavior change were you targeting?**
   - Faster feature development in auth-adjacent code?
   - Fewer auth-related bugs in production?
   - Easier onboarding for new devs to the auth system?

2. **What's the current state?**
   - How long does an auth change take today?
   - What breaks most often?
   - What do devs complain about?

3. **What signal will tell you this worked?**
   - PR cycle time for auth changes?
   - Bug count in auth module?
   - Onboarding feedback?

Without clear answers, consider `/salvage` to extract what you've learned, then restart with a crisp aim.

**Red flag:** If "simplify" is the aim, you need a measurable definition. Simplicity is a mechanism, not an outcome. What does simpler auth enable that complex auth blocks?
```

## Session Persistence

When invoked with a session name (`/aim <session>`), this skill reads and writes to `.oh/<session>.md`.

**Reading:** Check for existing session file. If found, read prior skill outputs (problem-statement, problem-space, etc.) for context.

**Writing:** After producing output, write the aim statement to the session file:

```markdown
# Session: <session>

## Aim
**Updated:** <timestamp>

[aim statement content]
```

If the file exists, replace the `## Aim` section. If it doesn't exist, create it.

**Session naming:** User provides the session name - could be a PR number (`PR-123`), feature name (`feature-auth`), or any identifier meaningful to them.

## Adaptive Enhancement

### Base Skill (prompt only)
Works anywhere. Produces aim statement for discussion. No persistence.

### With .oh/ session file
- Reads `.oh/<session>.md` for prior context from other skills
- Writes aim statement to the session file
- Subsequent skills (`/problem-statement`, `/solution-space`, etc.) can read the aim

### With .wm/ (working memory)
- Also reads/writes `.wm/sessions/` and `.wm/state.md`
- Session file and working memory can coexist

### With Open Horizons MCP
- Queries related endeavors to see if aim already exists
- Pulls relevant tribal knowledge that might inform mechanism choice
- Logs aim statement to graph database
- Links aim to active endeavors
- Session file serves as local cache for MCP data

## Relationship to Other Commands

**Aim vs Problem-Statement:**
- Aim is the WHY - what outcome do you want?
- Problem-Statement is the WHAT - how do you frame what needs solving?
- Aim comes first. Problem-statement is derived from aim.

**Aim vs Problem-Space:**
- Aim is the destination
- Problem-space maps the territory and constraints
- You can't navigate effectively without knowing where you're going

**Flow:**
```
/aim → /problem-statement → /problem-space → /solution-space → /execute
         ↑                                                         |
         └──────────────── /review, /salvage ──────────────────────┘
```

## Leads To

After establishing aim, typically:
- `/problem-statement` - Frame what needs solving to achieve the aim
- `/problem-space` - Map constraints and what you're optimizing
- `/review` - Check if current work still serves the aim

---

**Remember:** The aim IS the abstraction. Features are outputs; behavior changes are outcomes. Start with what you want users to do differently.
