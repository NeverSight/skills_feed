---
name: session-review
description: Analyzes completed agent sessions to identify what went well, what went wrong, and patterns to improve. Reads from .claude/ folder (session logs, progress.md, git history) and produces actionable insights. Use after completing work sessions to learn from agent behavior and improve future runs.
---

# Session Review Skill

Analyze agent sessions to extract lessons and improve future performance.

## Purpose

After an agent session (or series of sessions), this skill helps you:
- Understand what the agent actually did
- Identify good patterns to reinforce
- Spot bad patterns to prevent
- Find wasted effort
- Generate improvements for skills/prompts

## Quick Start

### Trigger Phrases

- "Review the last session"
- "Analyze what went wrong in this project"
- "What patterns do you see in the agent's work?"
- "Help me understand why the agent struggled with X"

### Basic Usage

```
1. Run after completing a project or hitting issues
2. Point to project with .claude/ folder
3. Get structured analysis with recommendations
```

## Input Sources

The skill reads from multiple sources:

```
.claude/
├── progress.md           # Session summaries
├── sessions/             # Detailed session logs
│   ├── 2025-01-10-001.md
│   └── 2025-01-10-002.md
├── features.json         # Original plan
├── tasks.db              # Task tracking
└── checkpoints/          # Human decision points
    └── pending-review.md

Git History
├── Commit messages       # What was done
├── Diffs                 # What actually changed
└── Reverts               # What was undone

Code Quality
├── Build status          # Did it compile?
├── Test results          # Did tests pass?
└── Lint output           # Code quality issues
```

## Analysis Framework

### 1. Execution Analysis

Compare plan vs reality:

| Metric | Source | Question |
|--------|--------|----------|
| Tasks planned | features.json | How many tasks were defined? |
| Tasks completed | progress.md | How many actually finished? |
| Tasks abandoned | git history | What was started but reverted? |
| Scope creep | task additions | What wasn't in original plan? |
| Time estimates | tasks.db | How accurate were estimates? |

### 2. Quality Analysis

Assess work quality:

| Signal | Good | Bad |
|--------|------|-----|
| Build failures | 0-1 per session | Multiple per task |
| Test failures | Caught and fixed | Left broken |
| Reverts | Rare | Frequent |
| Commit size | Focused, small | Huge or tiny |
| Code review flags | Minor style | Logic errors |

### 3. Pattern Detection

Look for recurring behaviors:

**Good Patterns**
- Verifies before starting new work
- Commits after each task
- Updates progress consistently
- Asks clarifying questions
- Tests changes end-to-end

**Bad Patterns**
- Starts multiple tasks before finishing one
- Commits broken code
- Ignores test failures
- Over-engineers simple tasks
- Repeats same mistakes

### 4. Decision Analysis

Review checkpoint decisions:

| Decision Point | What Happened | Outcome |
|----------------|---------------|---------|
| Ambiguity found | Agent guessed | Wrong assumption |
| Scope change | Human approved | Added 2 days |
| Build failure | Auto-fixed | Fixed but fragile |

## Output Format

### Session Review Report

```markdown
# Session Review: [Project Name]

## Summary
- **Sessions analyzed**: 5
- **Tasks completed**: 12/15 (80%)
- **Time spent**: 8.5 hours
- **Estimated time**: 6 hours (42% over)

## What Went Well

### ✓ Consistent Progress Tracking
The agent updated progress.md after every task, making it easy
to resume sessions and understand state.

### ✓ Good Verification Habit
Before starting new features, the agent ran the test suite
and fixed any regressions first.

### ✓ Appropriate Scope Questions
When the export feature was ambiguous, the agent paused and
asked rather than guessing. This saved rework.

## What Went Wrong

### ✗ Underestimated Database Tasks
Database migrations took 3x longer than estimated. The agent
didn't account for data migration complexity.

**Pattern**: Estimates for database work consistently low
**Recommendation**: Add 2x multiplier for DB tasks

### ✗ Repeated Authentication Bug
The same JWT expiration bug was introduced twice across sessions.
The agent didn't learn from the first fix.

**Pattern**: No memory of previous bugs
**Recommendation**: Add known-issues.md to .claude/ folder

### ✗ Over-engineered Settings Page
Simple settings page became a full preferences system with
versioning, import/export, and sync. Scope crept significantly.

**Pattern**: Feature expansion without checkpoint
**Recommendation**: Add scope_change checkpoint at 'pause' level

## Time Analysis

| Category | Planned | Actual | Variance |
|----------|---------|--------|----------|
| Frontend | 3h | 2.5h | -17% ✓ |
| Backend | 2h | 3h | +50% |
| Database | 1h | 3h | +200% ✗ |
| Testing | 0h | 1h | (unplanned) |

## Recommendations

### For This Project

1. **Add database migration checklist**
   Create .claude/checklists/database.md with migration steps

2. **Track known bugs**
   Add .claude/known-issues.md that agent reads each session

3. **Tighten scope checkpoints**
   Change scope_change from 'review' to 'pause'

### For Your Skills

1. **Update api-design skill**
   Add section on JWT token lifecycle, common expiration bugs

2. **Update prd-analyzer skill**
   Add 2x multiplier for database task estimates

### For Future Projects

1. **Start with tighter checkpoints**
   First epic in 'supervised', then graduate to 'semi-auto'

2. **Require tests for auth code**
   Any authentication changes must include test coverage
```

## Analysis Techniques

### Git History Analysis

```bash
# Count commits per session
git log --oneline --since="2025-01-10" --until="2025-01-11"

# Find reverts (indicates mistakes)
git log --oneline --grep="revert" --grep="Revert"

# Find fix commits (indicates bugs)
git log --oneline --grep="fix" --grep="Fix"

# Large commits (might be problematic)
git log --stat --since="2025-01-10" | grep -E "^\s+\d+ file"

# Commit frequency (should be steady)
git log --format="%ai" --since="2025-01-10" | cut -d' ' -f2 | cut -d: -f1 | sort | uniq -c
```

### Progress Analysis

```python
# Pseudocode for analyzing progress.md
def analyze_progress(progress_md: str) -> dict:
    sessions = parse_sessions(progress_md)
    
    metrics = {
        'total_sessions': len(sessions),
        'tasks_per_session': [],
        'checkpoints_hit': [],
        'errors_encountered': [],
        'scope_changes': []
    }
    
    for session in sessions:
        metrics['tasks_per_session'].append(session.tasks_completed)
        metrics['checkpoints_hit'].extend(session.checkpoints)
        metrics['errors_encountered'].extend(session.errors)
        
    return metrics
```

### Task Completion Analysis

```sql
-- Query tasks.db for completion patterns
SELECT 
    task_type,
    COUNT(*) as total,
    AVG(estimate_hours) as avg_estimate,
    AVG(
        CAST((julianday(completed_at) - julianday(started_at)) * 24 AS REAL)
    ) as avg_actual,
    AVG(
        CAST((julianday(completed_at) - julianday(started_at)) * 24 AS REAL)
    ) / AVG(estimate_hours) as accuracy_ratio
FROM tasks
WHERE status = 'done'
GROUP BY task_type;
```

## Pattern Library

### Common Good Patterns

| Pattern | Signal | Reinforce By |
|---------|--------|--------------|
| Verify first | Runs tests before new work | Add to session protocol |
| Small commits | <100 lines per commit | Praise in review |
| Clear messages | Commit messages explain why | Include in prompts |
| Asks questions | Pauses on ambiguity | Keep checkpoints |

### Common Bad Patterns

| Pattern | Signal | Prevent By |
|---------|--------|------------|
| Scope creep | Unplanned features | Tighter checkpoints |
| Broken commits | Build fails after commit | Require build pass |
| Giant commits | >500 lines | Split task definition |
| Repeated bugs | Same fix twice | Known issues file |
| Estimate optimism | Always over time | Add multipliers |

### Warning Signs

| Signal | Meaning | Action |
|--------|---------|--------|
| Multiple reverts | Agent is thrashing | Switch to supervised |
| Long gaps in commits | Stuck on something | Review what's blocking |
| Sudden scope expansion | Agent is over-engineering | Pause and refocus |
| Skipped tests | Agent avoiding verification | Require test runs |

## Integration with Project Harness

### After Each Epic

Run session review at epic boundaries:

```yaml
# In .claude/config.yaml
checkpoints:
  epic_complete: pause  # Good time to review
```

When epic completes:
1. Run session-review on the epic's sessions
2. Apply recommendations to remaining work
3. Adjust estimates for similar future tasks

### After Project Completion

Full project review:
1. Analyze all sessions
2. Generate project retrospective
3. Update skills with learnings
4. Document patterns for future projects

## Output Files

Generate these artifacts:

| File | Purpose |
|------|---------|
| `.claude/reviews/YYYY-MM-DD.md` | Session review report |
| `.claude/patterns.md` | Accumulated good/bad patterns |
| `.claude/known-issues.md` | Bugs to watch for |
| `.claude/estimate-adjustments.md` | Multipliers by task type |

## Review Checklist

When running a session review:

```markdown
## Pre-Review
- [ ] All sessions have logs in .claude/sessions/
- [ ] Git history is available
- [ ] Build/test status known

## Analysis
- [ ] Compared planned vs actual tasks
- [ ] Checked estimate accuracy
- [ ] Identified reverts/fixes
- [ ] Found repeated patterns
- [ ] Reviewed checkpoint decisions

## Output
- [ ] Generated review report
- [ ] Listed actionable recommendations
- [ ] Updated patterns.md if new patterns found
- [ ] Updated known-issues.md if bugs repeated
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Review too late | Lessons forgotten | Review after each epic |
| Blame the agent | Not actionable | Focus on system improvements |
| Ignore estimates | Keep being wrong | Track and adjust multipliers |
| No follow-through | Same mistakes repeat | Track recommendation implementation |
