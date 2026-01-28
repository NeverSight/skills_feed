---
name: problem-statement
description: Define the framing of a problem. Change the statement, change the solution space. Use when starting work, when solutions feel wrong, or when you suspect an X-Y problem.
---

# /problem-statement

Define the framing. **Change the statement, change the solution space.**

A problem statement is not the problem itself—it's the lens through which you see the problem. Different framings open different solution spaces. The right framing makes good solutions obvious; the wrong framing makes them invisible.

## When to Use

Invoke `/problem-statement` when:

- **Starting new work** - Before diving into solutions, articulate what you're actually solving
- **Solutions feel off** - When proposed solutions seem convoluted or like workarounds
- **Oscillating on approach** - When you keep changing direction, the framing might be wrong
- **Suspected X-Y problem** - When someone asks for a specific solution but the underlying need is unclear
- **Requirements keep expanding** - Scope creep often signals a framing mismatch
- **After `/aim` but before `/solution-space`** - The natural sequence: aim defines outcome, problem statement frames the challenge

**Do not use when:** You already have a crisp problem statement and are ready to explore solutions. Move to `/solution-space`.

## The Framing Process

### Step 1: Surface the Current Framing

Before reframing, understand how the problem is currently being seen:

> "The problem is currently framed as: [how it's being described]"

Capture:
- What's the stated problem?
- What assumptions are embedded in how it's described?
- What's being treated as fixed vs. changeable?

### Step 2: Detect X-Y Problems

Watch for the X-Y problem pattern: someone asks for Y (their attempted solution) when they actually need X (the real problem).

**Signs of X-Y mismatch:**
- Request is oddly specific for what seems like a simple goal
- The solution feels like a workaround
- "How do I do [technique]?" without explaining why
- Convoluted multi-step approach to something that should be simple

**If X-Y problem detected:**
> "You're asking for [Y], but the underlying need seems to be [X]. Is that right? If so, we should reframe around [X]."

### Step 3: Separate WHAT from HOW

A good problem statement articulates WHAT needs to change, not HOW to change it.

**Wrong:** "We need to add a caching layer to reduce latency"
**Right:** "Page loads take 3+ seconds; users abandon before content appears"

**Wrong:** "We need to refactor the auth module"
**Right:** "Adding a new auth provider takes 2 weeks and touches 6 files"

Test your statement:
- Does it describe a symptom or a solution?
- Could someone unfamiliar with the codebase understand what's wrong?
- Does it leave room for multiple solution approaches?

### Step 4: Identify Constraints and Flexibility

Every problem exists within constraints. Name them explicitly:

**Hard constraints** (actually immovable):
- Regulatory requirements
- Laws of physics
- Existing user commitments

**Soft constraints** (feel fixed but aren't):
- "We've always done it this way"
- Technical debt
- Team preferences

**Questions to surface flexibility:**
- What would we do if [constraint] didn't exist?
- Who decided [constraint] was fixed? Can we revisit?
- What's the cost of violating [constraint] vs. the cost of keeping it?

### Step 5: Craft the Problem Statement

Structure: **[Who] needs [what outcome] because [why it matters], but currently [what's blocking].**

Good problem statements are:
- **Crisp** - One or two sentences, not a paragraph
- **Outcome-focused** - Describes the desired state, not the current mess
- **Testable** - You'll know when it's solved
- **Solution-agnostic** - Leaves room to explore approaches

**Examples:**

| Bad | Good |
|-----|------|
| "The API is slow" | "API responses take 800ms; our SLA requires 200ms" |
| "We need microservices" | "Deploying a fix requires coordinating 4 teams and takes 2 weeks" |
| "Users don't understand the UI" | "40% of support tickets are 'how do I X' where X is a core feature" |
| "We need better tests" | "Last 3 production incidents were caught by users, not tests" |

### Step 6: Validate the Framing

Before committing to a problem statement, test it:

1. **State it to someone else** - If they immediately suggest a solution, the framing is too narrow
2. **Invert it** - What would the world look like if this problem didn't exist?
3. **Zoom out** - Is this a symptom of a larger problem?
4. **Zoom in** - Is this actually multiple problems masquerading as one?

## Output Format

Produce a problem statement in this structure:

```
## Problem Statement

**Current framing:** [How the problem is currently being described]

**Reframed as:** [Your crisp problem statement]

**The shift:** [What changed in how we see it]

### Constraints
- **Hard:** [Actually immovable constraints]
- **Soft:** [Constraints that feel fixed but might be flexible]

### What this framing enables
[What solution approaches become visible with this framing]

### What this framing excludes
[What approaches are off the table with this framing—and whether that's intentional]
```

## Examples

### Example 1: X-Y Problem Detection

**User asks:**
> "How do I parse this JSON and extract the user IDs into a separate array?"

**X-Y detection:**
```
## Problem Statement

**Current framing:** Need to parse JSON and extract user IDs into an array.

**But wait—why?** This sounds like an attempted solution. What's the underlying need?

**Clarifying questions:**
- What will you do with the array of user IDs?
- Where does this JSON come from?
- How often does this need to happen?

**If the answer is:** "I need to check if the current user is in this list"

**Reframed as:** Need to determine if current user has permission to access this resource.

**The shift:** From data transformation to authorization check. This might be solvable without extracting IDs at all—a simple `includes()` check or a backend permission endpoint.
```

### Example 2: Reframing Infrastructure as User Problem

**Original request:**
> "We need to set up a message queue between services"

**Problem statement work:**
```
## Problem Statement

**Current framing:** Set up message queue between services.

**That's a solution. What's the problem?**

After discussion: "When Service A updates, Service B doesn't know about it. Users see stale data."

**Reframed as:** Users see stale data after updates because services don't communicate changes in real-time.

**The shift:** From infrastructure request to user experience problem. Now we can evaluate: Does this need real-time? Is eventual consistency acceptable? Could we solve this with cache invalidation instead?

### Constraints
- **Hard:** Users must see accurate data within 5 seconds of update
- **Soft:** "We use message queues for this" (actually flexible—polling, webhooks, or even a shared cache might work)

### What this framing enables
- Evaluate real-time vs. eventual consistency needs
- Consider polling intervals as a simpler solution
- Question whether these should be separate services at all

### What this framing excludes
- Building complex event-driven architecture before validating the need
```

### Example 3: Scope Creep Signal

**Context:**
> Started as "add a dark mode toggle." Now touching 14 files and we realize there's no theme system.

**Problem statement work:**
```
## Problem Statement

**Current framing:** Add dark mode toggle.

**What's actually happening:** We can't add the toggle because there's no theme infrastructure to toggle between.

**Reframed as:** The codebase has no theming system; colors are hardcoded across components.

**The shift:** This is two problems:
1. Build theming infrastructure (larger)
2. Add dark mode as first alternate theme (smaller, depends on #1)

The original ask revealed a missing capability, not a feature to add.

### Constraints
- **Hard:** None identified
- **Soft:** "Ship dark mode this sprint" (may not be realistic given scope)

### What this framing enables
- Properly scope the work (infrastructure then feature)
- Consider: is dark mode the most valuable first use of a theme system?
- Evaluate CSS-in-JS vs. CSS variables vs. other approaches

### What this framing excludes
- Hacking dark mode without addressing the underlying issue (band-aid)
```

## Session Persistence

When invoked with a session name (`/problem-statement <session>`), this skill reads and writes to `.oh/<session>.md`.

**Reading:** Check for existing session file. If found, read prior skill outputs—especially the **Aim** section—for context. The aim informs what problem we're actually trying to solve.

**Writing:** After producing output, write the problem statement to the session file:

```markdown
## Problem Statement
**Updated:** <timestamp>

[problem statement content]
```

If the section exists, replace it. If not, append it after the Aim section.

## Adaptive Enhancement

### Base Skill (prompt only)
Works anywhere. Produces problem statement for discussion. No persistence.

### With .oh/ session file
- Reads `.oh/<session>.md` for prior context (especially aim)
- Writes problem statement to the session file
- Subsequent skills can read the framing

### With .wm/ (working memory)
- Also reads/writes `.wm/state.md` and `.wm/dive_context.md`
- Session file and working memory can coexist

### With Open Horizons MCP
- Queries graph for similar problems and their eventual framings
- Retrieves tribal knowledge about framing patterns that worked/failed
- Logs the problem statement as a decision point in the endeavor
- Session file serves as local cache

## Leads To

After problem statement, typically:
- `/solution-space` - Explore candidate solutions given this framing
- `/problem-space` - If you need to map the broader landscape first
- `/aim` - If the outcome itself is unclear (go back to clarify)

---

**Remember:** The problem statement isn't just documentation—it's the leverage point. A different framing doesn't just describe the problem differently; it literally changes what solutions become possible.
