---
name: salvage
description: Extract learning before restarting. Code is a draft; learning is the asset. Use when work is drifting, approach has reversed 3+ times, or scope is expanding while "done" keeps fuzzing.
---

# /salvage

Extract learning from a session or piece of work before restarting. The insight: **code is cheap now; learning is the asset.**

Salvage is the bridge from Review back to Problem Space. When drift is detected, salvage captures what was learned so you can restart clean without losing understanding.

## When to Use

Invoke `/salvage` when:

- **Work is drifting** - approach has changed direction multiple times
- **Approach reversed 3+ times** - you're oscillating, not converging
- **Scope expanding while "done" keeps fuzzing** - the finish line keeps moving
- **You're protecting code you've invested in** - afraid to throw it away
- **Starting over feels right** - but you don't want to lose what you learned

**Do not use when:** Work is on track and converging. Salvage is for extraction before restart, not routine reflection.

## The Salvage Process

### Step 1: Acknowledge the State

Before extracting, name what happened:

> "This session/approach is being salvaged because [reason]. The original aim was [aim]. What actually happened was [reality]."

Be direct. No judgment—just clarity.

### Step 2: Extract Five Things

Work through these extraction categories. Not everything will apply; extract what's present.

#### 1. Model Shifts (What changed your understanding?)

- What assumptions were wrong?
- What did you learn about the problem that you didn't know before?
- What would you tell yourself at the start of this work?

> "I thought X, but actually Y."

#### 2. Guardrails (Constraints discovered the hard way)

- What boundaries should have been explicit from the start?
- What "don't do this" rules emerged?
- What edge cases bit you?

Format as explicit constraints:
```
Guardrail: [boundary]
Reason: [why this matters]
Trigger: [when to revisit this constraint]
```

#### 3. Missing Context (What would have helped upfront?)

- What questions should have been asked at the start?
- What existing code/patterns should have been found first?
- What documentation was missing or would have prevented this?

> "If I had known about [X], I would have [Y] instead."

#### 4. Local Practices (Hard-won lessons worth encoding)

Local practices = practical wisdom, the kind you can only get from experience.

- What tribal knowledge did this work surface?
- What would help future-you (or future teammates) in similar situations?
- What patterns should be captured?

Good tribal knowledge is:
- Specific enough to be actionable
- General enough to apply beyond this exact case
- Non-obvious (not "write tests" but "this API silently returns 200 on auth failure")

#### 5. What Worked (Don't lose the wins)

- What approaches or code fragments are worth keeping?
- What partial solutions could seed the restart?
- What tools or techniques proved useful?

### Step 3: Package for Fresh Start

Synthesize the extraction into a restart kit:

```markdown
## Salvage Summary

### Original Aim
[What we were trying to achieve]

### Why Salvaged
[Direct statement of what went wrong]

### Key Learnings
1. [Learning 1]
2. [Learning 2]
3. [Learning 3]

### New Guardrails
- [Guardrail 1]
- [Guardrail 2]

### Context for Restart
[What the next attempt should know before starting]

### Reusable Fragments
[Any code, patterns, or approaches worth keeping]
```

### Step 4: Update Persistent Memory (if available)

If working memory (`.wm/`) or Open Horizons is available:

1. **Add to state.md** - Update working memory with key learnings
2. **Log to OH** - If OH MCP tools available, log tribal knowledge and guardrails
3. **Update CLAUDE.md** - If learnings are project-wide, suggest additions

If no persistent storage is available, output the salvage summary for the user to capture manually.

## Output Format

Always produce a salvage summary in this structure:

```
## Salvage Report

**Salvaged:** [date/session identifier]
**Reason:** [why this work is being salvaged]
**Original Aim:** [what we were trying to do]

### Learnings
[Numbered list of key insights]

### New Guardrails
[Explicit constraints with reason and trigger]

### Missing Context
[What would have helped]

### Local Practices
[Hard-won wisdom to encode]

### Reusable Fragments
[Code or patterns worth keeping]

### Fresh Start Recommendation
[How to approach this next time]
```

## Examples

### Example 1: Drifting Implementation

```
/salvage

The auth refactor has changed direction 4 times. Originally simplifying
the flow, now it's more complex than before.
```

**Output:**
```
## Salvage Report

**Salvaged:** Auth refactor session
**Reason:** Approach reversed 4 times, complexity increased not decreased
**Original Aim:** Simplify authentication flow

### Learnings
1. The complexity isn't in the auth code—it's in the 6 different OAuth providers
2. Each provider has subtly different token refresh behavior
3. The "simple" unified flow breaks provider-specific error handling

### New Guardrails
- Guardrail: Don't abstract OAuth providers into single interface
- Reason: Provider differences are semantic, not syntactic
- Trigger: Revisit if we drop to 2 providers or less

### Missing Context
- The original auth was complex for a reason (provider edge cases)
- Should have read the PR that introduced each provider

### Local Practices
OAuth providers aren't interchangeable. The abstraction leak is the feature.

### Fresh Start Recommendation
Instead of unifying the flow, document each provider's quirks explicitly.
Consider: is "simplify" the right aim? Maybe "make visible" is better.
```

### Example 2: Scope Creep

```
/salvage

Started as "add dark mode toggle." Now touching 14 files and the
theme system doesn't exist yet.
```

**Output:**
```
## Salvage Report

**Salvaged:** Dark mode implementation
**Reason:** Scope expanded from toggle to theme system
**Original Aim:** Add dark mode toggle to settings

### Learnings
1. No theme system exists—colors are hardcoded across components
2. A toggle without infrastructure is meaningless
3. This is actually two tasks: (1) build theme system, (2) add toggle

### New Guardrails
- Guardrail: UI feature requests need infrastructure check first
- Reason: "Add X" often implies "build system for X"
- Trigger: Any request that touches visual consistency

### Missing Context
- Should have grepped for color usage before starting
- No design tokens or CSS variables in codebase

### Local Practices
"Add [feature]" is not the same as "build [feature]." Check if the
infrastructure exists before estimating.

### Reusable Fragments
- Color mapping I started: styles/colors.js (incomplete but useful)
- Component audit list: 14 files that hardcode colors

### Fresh Start Recommendation
1. First: Create theme system (CSS variables, ThemeContext)
2. Then: Add dark mode as first theme variant
3. The toggle is the easy part—do it last
```

## Session Persistence

When invoked with a session name (`/salvage <session>`), this skill reads and writes to `.oh/<session>.md`.

**Reading:** Check for existing session file. Read **everything**—Aim, Problem Statement, Problem Space, Solution Space, Execute, Review—to understand what was attempted and what happened.

**Writing:** After producing the salvage report:

```markdown
## Salvage
**Updated:** <timestamp>
**Outcome:** [extracted learnings, ready for restart]

[salvage report: learnings, guardrails, context for fresh start]
```

The salvage section is the capstone—it captures what was learned before the session ends or restarts.

## Adaptive Enhancement

### Base Skill (prompt only)
Works anywhere. Produces salvage summary for manual capture. No persistence.

### With .oh/ session file
- Reads `.oh/<session>.md` for full session context
- Writes salvage report to the session file
- The salvage report can seed the next session

### With .wm/ (working memory)
- Also reads/writes `.wm/state.md` and `.wm/dive_context.md`
- Session file and working memory can coexist

### With Open Horizons MCP
- Queries related past decisions before salvaging
- Logs learnings to graph database
- Creates dive pack for restart session
- Session file serves as local cache

## Leads To

After salvage, typically:
- `/problem-space` - Fresh start with new understanding
- `/aim` - Reclarify what we're actually trying to achieve
- Create new task/issue with salvage context attached

---

**Remember:** Salvage is not failure. It's learning made explicit. The only failure is losing what you learned.
