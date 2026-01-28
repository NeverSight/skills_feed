---
name: solution-space
description: Explore candidate solutions before committing. Use when you have a problem statement and need to evaluate approaches - band-aid, optimize, reframe, or redesign.
---

# /solution-space

Explore candidate solutions before committing to implementation. The trap is defending the first workable idea.

Solution Space sits between Problem Statement and Implementation. You have the problem framed; now map the approaches before picking one.

## When to Use

Invoke `/solution-space` when:

- **Problem is understood** - You have a clear problem statement
- **Multiple approaches seem viable** - Not obvious which path is best
- **You're about to start coding** - Pause and explore before committing
- **Patches keep accumulating** - Third config flag for the same bug
- **You feel attached to your first idea** - That's the warning sign

**Do not use when:** You're still clarifying the problem. Use `/problem-statement` first. Solution Space assumes the problem is framed.

## The Local Maximum Trap

> "The hardest part of design has never been coming up with ideas. It is letting go of the first workable idea to look for better ones."

Exploration is cheap. The failure mode is defending the first solution that works.

**Signs you're stuck on a local maximum:**
- First solution considered is the only solution considered
- You're explaining why alternatives won't work before trying them
- You're acting as a crafter (defending) rather than an editor (filtering)
- Implementation details discussed before approaches compared

## The Escalation Ladder

Not all problems need redesigns. The ladder helps you find the right altitude.

### Level 1: Band-Aid Fix
**Don't default to this.** Patch the symptom.

- Fine under deadline pressure
- Toxic as habit
- Signal: "This will break again"

*Example: Add a null check. Catch the exception. Hardcode the edge case.*

### Level 2: Local Optimum
**Better, but limited.** Optimize within current assumptions.

- Classic refactor trap
- Improves what exists without questioning it
- Signal: "This is cleaner but the same shape"

*Example: Extract a method. Add a parameter. Refactor for readability.*

### Level 3: Reframe
**Now you're thinking.** Question the problem statement.

- Different framing yields different solutions
- Often reveals the actual constraint
- Signal: "What if the problem is actually..."

*Example: "We need faster cache invalidation" becomes "Why do we cache this at all?"*

### Level 4: Redesign
**This is the goal.** Change the system so the problem doesn't exist.

- The higher peak, the terraform
- Problems dissolve rather than get solved
- Signal: "With this change, we wouldn't need to..."

*Example: Instead of fixing sync conflicts, make the data flow unidirectional.*

## The Process

### Step 1: State the Problem (Confirm)

Before exploring solutions, confirm the problem statement:

> "The problem we're solving is: [statement]. The key constraint is: [constraint]. Success looks like: [outcome]."

If you can't state this clearly, go back to `/problem-statement`.

### Step 2: Generate Candidates (Breadth)

List at least 3-4 candidate approaches before evaluating any:

```markdown
## Candidate Solutions

### Option A: [Name]
- Approach: [Brief description]
- Level: [Band-Aid / Local Optimum / Reframe / Redesign]
- Trade-off: [Main cost]

### Option B: [Name]
...
```

**Rules for this step:**
- No evaluation yet - just generation
- Include at least one approach from a higher level than your instinct
- Include the "obvious" solution even if you don't like it

### Step 3: Evaluate Trade-offs (Depth)

For each candidate, assess:

1. **Does it solve the stated problem?** (Not a related problem)
2. **What's the implementation cost?** (Time, complexity, risk)
3. **What's the maintenance cost?** (Ongoing burden)
4. **Does it create new problems?** (Second-order effects)
5. **Does it enable future options?** (Optionality)

### Step 4: Recommend with Reasoning

Make a recommendation and state why:

```markdown
## Recommendation

**Approach:** [Selected option]
**Level:** [Band-Aid / Local Optimum / Reframe / Redesign]

**Why this one:**
- [Reason 1]
- [Reason 2]

**Why not the others:**
- Option A: [Reason rejected]
- Option B: [Reason rejected]

**Known trade-offs we're accepting:**
- [Trade-off 1]
- [Trade-off 2]
```

### Step 5: Check for Local Maximum

Before committing, ask:

- Did I defend my first idea or actually explore?
- Is there a higher-level approach I dismissed too quickly?
- Am I optimizing the wrong thing?

If you explored genuinely and still landed on the first idea, that's fine. The danger is never looking.

## Output Format

```markdown
## Solution Space Analysis

**Problem:** [One sentence]
**Key Constraint:** [The binding constraint]

### Candidates Considered

| Option | Level | Approach | Trade-off |
|--------|-------|----------|-----------|
| A | [Level] | [Brief] | [Cost] |
| B | [Level] | [Brief] | [Cost] |
| C | [Level] | [Brief] | [Cost] |

### Evaluation

**Option A: [Name]**
- Solves stated problem: [Yes/Partially/No]
- Implementation cost: [Low/Medium/High]
- Maintenance burden: [Low/Medium/High]
- Second-order effects: [Description]

[Repeat for each option]

### Recommendation

**Selected:** Option [X] - [Name]
**Level:** [Band-Aid / Local Optimum / Reframe / Redesign]

**Rationale:** [Why this approach fits the constraints]

**Accepted trade-offs:**
- [Trade-off 1]
- [Trade-off 2]

### Implementation Notes

[Any specific considerations for the selected approach]
```

## Examples

### Example 1: Performance Problem

```
/solution-space

Users report the dashboard is slow. Loading takes 8 seconds.
```

**Output:**
```markdown
## Solution Space Analysis

**Problem:** Dashboard loads in 8 seconds; users expect <2 seconds
**Key Constraint:** Can't rewrite the entire frontend this quarter

### Candidates Considered

| Option | Level | Approach | Trade-off |
|--------|-------|----------|-----------|
| A | Band-Aid | Add loading spinner | Doesn't fix slowness |
| B | Local Optimum | Add caching layer | Cache invalidation complexity |
| C | Reframe | Lazy-load dashboard sections | Changes UX slightly |
| D | Redesign | Stream data, render incrementally | Larger change |

### Evaluation

**Option A: Loading Spinner**
- Solves stated problem: No (perception only)
- Implementation cost: Low
- Second-order: Users still wait 8 seconds

**Option B: Caching Layer**
- Solves stated problem: Partially (helps repeat visits)
- Implementation cost: Medium
- Second-order: Stale data risk, invalidation complexity

**Option C: Lazy Loading**
- Solves stated problem: Yes (perceived speed)
- Implementation cost: Medium
- Second-order: Slight UX change, content shifts

**Option D: Streaming Render**
- Solves stated problem: Yes (actual + perceived)
- Implementation cost: High
- Second-order: Enables future improvements, larger change

### Recommendation

**Selected:** Option C - Lazy Loading
**Level:** Reframe

**Rationale:** The problem isn't "dashboard is slow" - it's "users wait before seeing anything useful." Lazy loading shows useful content in <1s while loading the rest. Lower cost than streaming, better than caching.

**Accepted trade-offs:**
- Content will shift as sections load
- Need to prioritize which sections load first
```

### Example 2: The Third Config Flag

```
/solution-space

We have a bug where notifications fire twice. This is the third
config flag we're adding to work around notification timing issues.
```

**Output:**
```markdown
## Solution Space Analysis

**Problem:** Notifications fire twice; third config flag proposed
**Key Constraint:** Pattern of band-aids suggests systemic issue

### Candidates Considered

| Option | Level | Approach | Trade-off |
|--------|-------|----------|-----------|
| A | Band-Aid | Add debounce flag | 4th flag incoming |
| B | Local Optimum | Consolidate notification logic | Still reactive model |
| C | Reframe | Why do we notify on this event? | May simplify |
| D | Redesign | Event sourcing for notifications | Larger change |

### Evaluation

**Option A: Debounce Flag**
- Solves stated problem: Temporarily
- Second-order: Maintenance nightmare, flags interact

**Option B: Consolidate Logic**
- Solves stated problem: Probably
- Second-order: Still treating symptoms

**Option C: Question the Trigger**
- Solves stated problem: Possibly dissolves it
- Second-order: May reveal unnecessary complexity

**Option D: Event Sourcing**
- Solves stated problem: Yes, prevents duplicates by design
- Second-order: Significant refactor

### Recommendation

**Selected:** Option C - Reframe, then possibly D
**Level:** Reframe (investigation)

**Rationale:** Three config flags is a code smell. Before adding a fourth, understand why notifications are triggered from multiple paths. The duplication likely indicates unclear ownership of the notification concern.

**Next step:** Map all notification trigger points. If >3 paths trigger the same notification, the problem isn't timing - it's architecture.
```

## Session Persistence

When invoked with a session name (`/solution-space <session>`), this skill reads and writes to `.oh/<session>.md`.

**Reading:** Check for existing session file. Read prior skill outputs—**Aim**, **Problem Statement**, **Problem Space**—to understand what we're solving and the constraints.

**Writing:** After producing output, write the solution space analysis to the session file:

```markdown
## Solution Space
**Updated:** <timestamp>

[solution space analysis and recommendation]
```

## Adaptive Enhancement

### Base Skill (prompt only)
Works anywhere. Produces solution space analysis for discussion. No persistence.

### With .oh/ session file
- Reads `.oh/<session>.md` for prior context (aim, problem statement, constraints)
- Writes solution analysis and recommendation to the session file
- `/execute` can read the selected approach

### With .wm/ (working memory)
- Also reads/writes `.wm/state.md`
- Session file and working memory can coexist

### With Open Horizons MCP
- Queries related past solution decisions
- Finds similar problems across endeavors
- Logs the solution space exploration and decision
- Session file serves as local cache

## Leads To

After solution-space, typically:
- `/execute` - Implement the selected approach
- `/problem-statement` - If exploration revealed the problem is mis-framed
- `/dissent` - If the recommendation feels too easy

---

**Remember:** The goal isn't to always pick Redesign. It's to know you explored before committing. A deliberate Band-Aid beats an accidental one.
