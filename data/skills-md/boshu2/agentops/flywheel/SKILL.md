---
name: flywheel
description: 'Knowledge flywheel health monitoring. Checks velocity, pool depths, staleness. Triggers: "flywheel status", "knowledge health", "is knowledge compounding".'
---

# Flywheel Skill

Monitor the knowledge flywheel health.

## The Flywheel Model

```
Sessions → Transcripts → Forge → Pool → Promote → Knowledge
     ↑                                               │
     └───────────────────────────────────────────────┘
                    Future sessions find it
```

**Velocity** = Rate of knowledge flowing through
**Friction** = Bottlenecks slowing the flywheel

## Execution Steps

Given `/flywheel`:

### Step 1: Measure Knowledge Pools

```bash
# Count learnings
LEARNINGS=$(ls .agents/learnings/ 2>/dev/null | wc -l)

# Count patterns
PATTERNS=$(ls .agents/patterns/ 2>/dev/null | wc -l)

# Count research
RESEARCH=$(ls .agents/research/ 2>/dev/null | wc -l)

# Count retros
RETROS=$(ls .agents/retros/ 2>/dev/null | wc -l)

echo "Learnings: $LEARNINGS"
echo "Patterns: $PATTERNS"
echo "Research: $RESEARCH"
echo "Retros: $RETROS"
```

### Step 2: Check Recent Activity

```bash
# Recent learnings (last 7 days)
find .agents/learnings/ -mtime -7 2>/dev/null | wc -l

# Recent research
find .agents/research/ -mtime -7 2>/dev/null | wc -l
```

### Step 3: Detect Staleness

```bash
# Old artifacts (> 30 days without modification)
find .agents/ -name "*.md" -mtime +30 2>/dev/null | wc -l
```

### Step 4: Check ao CLI Status

```bash
ao forge status 2>/dev/null || echo "ao CLI not available"
```

### Step 5: Write Health Report

**Write to:** `.agents/flywheel-status.md`

```markdown
# Knowledge Flywheel Health

**Date:** YYYY-MM-DD

## Pool Depths
| Pool | Count | Recent (7d) |
|------|-------|-------------|
| Learnings | <count> | <count> |
| Patterns | <count> | <count> |
| Research | <count> | <count> |
| Retros | <count> | <count> |

## Velocity (Last 7 Days)
- Sessions with extractions: <count>
- New learnings: <count>
- New patterns: <count>

## Health Status
<Healthy/Warning/Critical>

## Friction Points
- <issue 1>
- <issue 2>

## Recommendations
1. <recommendation>
2. <recommendation>
```

### Step 6: Report to User

Tell the user:
1. Overall flywheel health
2. Knowledge pool depths
3. Recent activity
4. Any friction points
5. Recommendations

## Health Indicators

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Learnings/week | 3+ | 1-2 | 0 |
| Stale artifacts | <20% | 20-50% | >50% |
| Research/plan ratio | >0.5 | 0.2-0.5 | <0.2 |

## Key Rules

- **Monitor regularly** - flywheel needs attention
- **Address friction** - bottlenecks slow compounding
- **Feed the flywheel** - run /retro and /post-mortem
- **Prune stale knowledge** - archive old artifacts
