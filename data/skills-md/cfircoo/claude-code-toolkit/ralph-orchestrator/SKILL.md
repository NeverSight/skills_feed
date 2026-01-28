---
name: ralph-orchestrator
description: Orchestrates the full Ralph autonomous agent pipeline from requirements gathering to execution. Use when building new features, platforms, or complex tasks that need structured development through spec-interview, PRD generation, and autonomous implementation.
model: claude-opus-4-5
context: fork
---

<objective>
Orchestrate the complete Ralph pipeline for autonomous feature development:

1. **spec-interview** → Gather comprehensive requirements through guided discovery
2. **generate-prd** → Create actionable Product Requirements Document
3. **ralph-convert-prd** → Transform PRD into atomic user stories (prd.json)
4. **ralph.sh** → Execute autonomous implementation loop

This skill coordinates these tools while keeping you in control at decision points.
</objective>

<essential_principles>

<principle name="fresh_context_per_iteration">
Ralph spawns fresh Claude instances for each story. Memory persists only through:
- Git history (committed code)
- progress.txt (learnings between iterations)
- prd.json (story status tracking)

**Never assume Ralph "remembers" previous iterations.**
</principle>

<principle name="atomic_stories">
Each user story MUST be completable in ONE context window.

**Right-sized:**
- Add a database column
- Create a UI component
- Update a server action
- Implement a filter

**Too large (will fail):**
- Build entire dashboard
- Add authentication system
- Refactor entire API
</principle>

<principle name="quality_gates">
All checks must pass before Ralph commits:
- TypeCheck passes
- Tests pass
- UI verified in browser (for frontend stories)

Broken code compounds across iterations. Never skip quality checks.
</principle>

<principle name="user_control_points">
You approve at each stage:
1. After spec-interview → Review SPEC.md
2. After generate-prd → Review PRD
3. After ralph-convert-prd → Review prd.json stories
4. Before ralph.sh → Confirm ready to execute

Don't rush. Bad requirements = wasted iterations.
</principle>

</essential_principles>

<intake>
What would you like to do?

1. **Full pipeline** - Start from scratch (spec → PRD → prd.json → execute)
2. **Continue from PRD** - Already have PRD, convert and execute
3. **Execute only** - Already have prd.json, run Ralph
4. **Check status** - View current prd.json progress

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "full", "start", "new feature" | `workflows/full-pipeline.md` |
| 2, "continue", "have PRD", "convert" | `workflows/from-prd.md` |
| 3, "execute", "run ralph", "have prd.json" | `workflows/execute-only.md` |
| 4, "status", "check", "progress" | `workflows/check-status.md` |

**After reading the workflow, follow it exactly.**
</routing>

<quick_reference>

**Key Files:**
| File | Purpose |
|------|---------|
| SPEC.md | Comprehensive requirements from spec-interview |
| tasks/prd-*.md | Product Requirements Document |
| prd.json | Atomic user stories for Ralph (in project root) |
| progress.txt | Learnings between iterations (in project root) |
| scripts/ralph.sh | Ralph execution script (in this skill folder) |
| scripts/prompt.md | Iteration prompt template |

**Commands:**
```bash
# Run Ralph from your project directory
# (assumes toolkit is at ~/projects/claude-code-toolkit)
~/projects/claude-code-toolkit/skills/ralph-orchestrator/scripts/ralph.sh

# Or create an alias in ~/.bashrc:
alias ralph='~/projects/claude-code-toolkit/skills/ralph-orchestrator/scripts/ralph.sh'

# Run with custom iteration limit
ralph 5

# Check story status
cat prd.json | jq '.userStories[] | {id, title, passes}'

# View learnings
cat progress.txt
```

</quick_reference>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| full-pipeline.md | Complete flow: spec → PRD → prd.json → execute |
| from-prd.md | Convert existing PRD and execute |
| execute-only.md | Run Ralph on existing prd.json |
| check-status.md | View current progress |
</workflows_index>

<success_criteria>
Pipeline is complete when:
- [ ] Requirements gathered through spec-interview
- [ ] PRD created with verifiable acceptance criteria
- [ ] prd.json has atomic, right-sized stories
- [ ] All stories have `passes: true` in prd.json
- [ ] Code committed and quality checks passing
</success_criteria>
