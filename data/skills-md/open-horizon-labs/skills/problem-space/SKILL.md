---
name: problem-space
description: Map what we're optimizing and what constraints we treat as real. Use before jumping to solutions, when hitting repeated blockers, or when patches keep accumulating.
---

# /problem-space

Map the terrain where solutions live. What are we optimizing? What constraints do we treat as real? Which constraints can be questioned?

Problem space exploration precedes solution space. Understanding the terrain is the work. Jump to code too early and you'll build the wrong thing fast.

## When to Use

Invoke `/problem-space` when:

- **Starting new work** - Before jumping to implementation, understand what you're actually solving
- **Hitting repeated blockers** - The same problems keep appearing in different forms
- **Patches accumulating** - Third config flag for the same bug signals you're treating symptoms
- **Estimates feel off** - When time estimates are wrong by an order of magnitude, the problem isn't understood
- **Agent is talking itself out of constraints** - "For this prototype we don't have time" when the constraint matters

**Do not use when:** The problem is well-understood and you're already in execution. Problem space is for grounding, not for stalling.

## The Problem Space Process

### Step 1: State the Objective Function

What are we actually optimizing? Not the feature, the outcome.

> "We are optimizing for [outcome]."

Be precise. "Build a login page" is a feature. "Reduce time-to-first-value for new users" is an objective. The aim IS the abstraction.

Ask:
- What change in behavior would indicate success?
- What metric would move if this worked?
- What problem disappears if we get this right?

### Step 2: Map the Constraints

List what we're treating as fixed. Be explicit about each constraint's nature:

```
Constraint: [the boundary]
Type: [hard | soft | assumed]
Reason: [why it exists]
Questioning: [could this be false?]
```

**Hard constraints** - Physics, regulations, signed contracts. These don't bend.

**Soft constraints** - Organizational decisions, technical debt, time pressure. These can be negotiated.

**Assumed constraints** - "We've always done it this way." These should be questioned.

The trap: Agents will talk themselves out of constraints. "For this prototype we don't have time" is often false when code generation takes 15 minutes, not a week. Ground yourself in what's actually fixed.

### Step 3: Identify the Terrain

Where do solutions live? Map the space:

- **What systems are involved?** - Existing code, external APIs, data stores
- **Who is affected?** - Users, operators, downstream systems
- **What's the blast radius?** - If this goes wrong, what breaks?
- **What precedents exist?** - Has this been solved before? Where?

### Step 4: Surface Hidden Assumptions

Every problem statement has embedded assumptions. Make them visible:

> "We assume [assumption]. If this is false, [consequence]."

Common hidden assumptions:
- The current architecture must be preserved
- The feature set is fixed
- The timeline can't change
- Users want what they asked for (not what they need)

### Step 5: Check for X-Y Problems

Are we solving the real problem (X) or the user's attempted solution (Y)?

Signs of X-Y mismatch:
- Request is oddly specific for a simple goal
- You're building something that feels like a workaround
- "How do I do [technique]" without explaining why

If potential X-Y problem detected:
> "The user asked for [Y], but the underlying need might be [X]."

## Output Format

Always produce a problem space map in this structure:

```
## Problem Space Map

**Date:** [timestamp]
**Scope:** [what area this covers]

### Objective
[What we're optimizing for - the outcome, not the feature]

### Constraints

| Constraint | Type | Reason | Question? |
|------------|------|--------|-----------|
| [boundary] | hard/soft/assumed | [why] | [could this be false?] |

### Terrain
- **Systems:** [what's involved]
- **Stakeholders:** [who's affected]
- **Blast radius:** [what breaks if wrong]
- **Precedents:** [existing solutions to examine]

### Assumptions Made Explicit
1. [assumption] - if false: [consequence]
2. [assumption] - if false: [consequence]

### X-Y Check
- **Stated need (Y):** [what was asked for]
- **Underlying need (X):** [what might actually be needed]
- **Confidence:** [high/medium/low that Y=X]

### Ready for Solution Space?
[yes/no] - [why or what's missing]
```

## Examples

### Example 1: Repeated Deployment Failures

```
/problem-space

Deployments keep failing. We've added 3 config flags in the last month
and each one "fixes" something but creates new edge cases.
```

**Output:**
```
## Problem Space Map

**Date:** 2024-01-15
**Scope:** Deployment pipeline reliability

### Objective
We are optimizing for: Reliable deployments that succeed without manual intervention.

### Constraints

| Constraint | Type | Reason | Question? |
|------------|------|--------|-----------|
| Must use existing CI/CD | soft | Team familiarity | Could we evaluate alternatives? |
| Zero-downtime required | hard | SLA commitment | No |
| Config managed in repo | assumed | "Best practice" | Could config live elsewhere? |
| Current rollback approach | soft | Built incrementally | Is this the right rollback model? |

### Terrain
- **Systems:** GitHub Actions, Kubernetes, ArgoCD, 3 microservices
- **Stakeholders:** Dev team, SRE, downstream API consumers
- **Blast radius:** Customer-facing outage, 200+ API consumers
- **Precedents:** Similar system at [X] uses feature flags instead of config

### Assumptions Made Explicit
1. Config flags are the right mechanism for deployment variation - if false: we need environment-aware builds
2. Failures are config-related - if false: we have an architecture problem

### X-Y Check
- **Stated need (Y):** Fix deployment config issues
- **Underlying need (X):** Make deployments reliable
- **Confidence:** Medium - config is a symptom, not the disease

### Ready for Solution Space?
No - Need to understand if this is a band-aid problem (more config) or a redesign problem (change how deployments work).
```

### Example 2: Performance Degradation

```
/problem-space

App is slow. PM wants us to "optimize the database queries."
```

**Output:**
```
## Problem Space Map

**Date:** 2024-01-15
**Scope:** Application performance

### Objective
We are optimizing for: Page load time under 2 seconds for 95th percentile users.

### Constraints

| Constraint | Type | Reason | Question? |
|------------|------|--------|-----------|
| Must use current database | assumed | "Migration too expensive" | Have we actually costed this? |
| Can't change API contracts | soft | Downstream consumers | How many consumers actually use slow endpoints? |
| Feature set is fixed | assumed | PM specified | What if we removed/simplified features? |

### Terrain
- **Systems:** PostgreSQL, Redis cache, React frontend, Node backend
- **Stakeholders:** End users, mobile clients, third-party integrations
- **Blast radius:** User churn, support tickets, competitor migration
- **Precedents:** Similar app moved to read replicas, saw 3x improvement

### Assumptions Made Explicit
1. Database queries are the bottleneck - if false: frontend rendering or network latency is the issue
2. Optimization is cheaper than redesign - if false: N+1 queries need architectural change
3. Current feature set is needed - if false: could eliminate unused expensive features

### X-Y Check
- **Stated need (Y):** Optimize database queries
- **Underlying need (X):** Make app feel fast to users
- **Confidence:** Low - PM prescribed solution without diagnosis

### Ready for Solution Space?
No - Need performance profiling to identify actual bottleneck before optimizing anything.
```

## Session Persistence

When invoked with a session name (`/problem-space <session>`), this skill reads and writes to `.oh/<session>.md`.

**Reading:** Check for existing session file. Read prior skill outputs—especially **Aim** and **Problem Statement**—to ground the exploration.

**Writing:** After producing output, write the problem space map to the session file:

```markdown
## Problem Space
**Updated:** <timestamp>

[problem space map content]
```

## Adaptive Enhancement

### Base Skill (prompt only)
Works anywhere. Produces problem space map through questioning. No persistence.

### With .oh/ session file
- Reads `.oh/<session>.md` for prior context (aim, problem statement)
- Writes problem space map to the session file
- Subsequent skills can read constraints and terrain

### With .wm/ (working memory)
- Also reads/writes `.wm/sessions/` and `.wm/state.md`
- Session file and working memory can coexist

### With Open Horizons MCP
- Queries graph for related past decisions and their outcomes
- Pulls relevant tribal knowledge about similar problem spaces
- Retrieves guardrails that apply to this domain
- Session file serves as local cache

## Leads To

After problem space mapping, typically:
- `/problem-statement` - Crisp articulation of what needs solving
- `/solution-space` - Explore candidate implementations
- Return to stakeholders - If constraints need challenging
- Research/investigation - If terrain is insufficiently understood

---

**Remember:** Problem space is not about delay. It's about building the right thing. The constraint is alignment, not delivery. When execution is cheap, understanding is the leverage.
