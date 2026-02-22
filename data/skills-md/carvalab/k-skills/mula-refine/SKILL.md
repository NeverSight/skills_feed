---
name: mula-refine
description: Unified prompt engineering and requirements planning. Use when exploring ideas, improving prompts, creating PRDs, generating task breakdowns, or iterating on existing plans. Includes Jira integration for creating subtasks from plans.
tools: Read, Grep, Glob, Bash
---

# Mula Refine

Single entry-point for all prompt engineering, requirements gathering, and planning workflows. Routes to 6 internal capabilities based on user intent. Supports Jira integration to push task breakdowns as subtasks.

## Context

This skill runs in **planning-only refine sessions**:
- **No MR creation** — refine sessions never create merge requests or feature branches
- **Multi-repo workspace** — the workspace may contain multiple cloned repos for codebase analysis
- **Jira integration** — use `mula-tool jira` to create subtasks and update parent issues

## Quick Start

1. Detect user intent (see routing below)
2. Load the matching rule: `mula-tool skill read mula-refine` then read the appropriate reference
3. Follow that rule exactly

## Intent Routing

| User Intent | Mode | Reference |
|-------------|------|-----------|
| Vague idea, needs discovery | Start | `references/start.md` |
| Has a prompt to optimize | Improve | `references/improve.md` |
| Extract requirements from chat | Summarize | `references/summarize.md` |
| Needs full requirements doc | PRD | `references/prd.md` |
| Has PRD, needs task breakdown | Plan | `references/plan.md` |
| Update existing PRD or prompt | Refine | `references/refine.md` |

**Default: When intent is unclear, use Improve mode** (analyzes and optimizes any input).

## Workflow

```
Vague Idea --> START --> conversation --> SUMMARIZE --> mini-PRD
                                              |
Clear Feature --> PRD ------------------------+-> full PRD --> PLAN --> tasks.md
                                                                |
Existing Prompt --> IMPROVE                                     v
                                                     Jira subtasks (optional)
Existing PRD/Prompt --> REFINE --> back to any mode
```

## Key Behaviors

1. **Announce mode** before starting (State Assertion)
2. **Never write implementation code** - planning only
3. **Self-correct** mistakes (DETECT/STOP/CORRECT/RESUME)
4. **Verify file saves** - Write then Read to confirm
5. **One question at a time** in Start and PRD modes
6. **Always present plan before creating Jira issues** - never push to Jira without confirmation
7. **Always score quality** - Every mode uses the 6-dimension quality assessment

## Universal Quality Assessment

**All modes** must evaluate outputs using 6 dimensions (0-100%):

| Dimension | What It Measures |
|-----------|-----------------|
| **Clarity** | Is the objective clear and unambiguous? |
| **Efficiency** | Is the content concise without losing critical information? |
| **Structure** | Is information organized logically? |
| **Completeness** | Are all necessary details provided? |
| **Actionability** | Can an AI take immediate action on this? |
| **Specificity** | How concrete and precise? (versions, paths, identifiers) |

**Quality gate:** If overall score < 70%, recommend running **Improve** mode first to optimize before proceeding to the next step.

## Jira Integration

After generating `tasks.md`, offer to push tasks as Jira subtasks:

```bash
# Show parent issue details first
mula-tool jira show --key PROJ-456

# Create subtask with priority (always prefix with [repo-name])
mula-tool jira create-subtask --parent PROJ-456 \
  --title "[payments-api] Add retry logic" \
  --description "Scope: files to change..." \
  --assignee me --priority High

# Link dependencies (MRTCH-1 blocks MRTCH-2)
mula-tool jira link --from MRTCH-1 --to MRTCH-2 --type Blocks

# Update parent issue title with repo context
mula-tool jira update --key PROJ-456 \
  --title "[payments-api] Updated title" \
  --description "Updated requirements..."
```

### Subtask Conventions

- **Always prefix with `[repo-name]`**: Every subtask title starts with the repo name in brackets (e.g., `[payments-api] Add retry logic`)
- **Single-repo tasks**: Also update the parent task title with the repo prefix
- **Priority**: Use `--priority` with: `Highest`, `High`, `Medium`, `Low`, `Lowest`
- **Dependencies**: Use `mula-tool jira link --from X --to Y --type Blocks` (X blocks Y)
- **Assignee**: Use `--assignee me` to auto-assign subtasks to the current user
- **Description**: Include scope (files to change), context, and enough detail for the next agent to work autonomously
- **Granularity**: Each subtask should be completable in one coding session

### Transitioning Issues

Workflows differ per project. Always check available transitions before moving:

```bash
# Check what transitions are available from current status
mula-tool jira transitions PROJ-456

# Move to a specific status
mula-tool jira transition PROJ-456 --name "Development"

# Close an issue (walks all transitions to Done automatically)
mula-tool jira close PROJ-456
```

### Deleting Subtasks

When the user asks to delete subtasks (e.g., "delete the subtasks", "remove all subtasks", "start fresh"):

```bash
# List subtasks first to confirm what will be deleted
mula-tool jira list-subtasks PROJ-456

# Delete individual subtasks
mula-tool jira delete MRTCH-1371
mula-tool jira delete MRTCH-1372

# If delete fails (403), close them instead
mula-tool jira close MRTCH-1371
mula-tool jira close MRTCH-1372

# Or delete a parent and all its subtasks at once
mula-tool jira delete PROJ-456 --delete-subtasks
```

**Always list subtasks before deleting** to confirm with the user. Never delete without showing what will be removed.

## Output Location

All outputs save to `.mula/outputs/`:
- PRDs: `.mula/outputs/{project}/`
- Prompts: `.mula/outputs/prompts/{id}.md`
- Tasks: `.mula/outputs/{project}/tasks.md`

## After Planning

When plan mode generates `tasks.md`:

1. Present the task breakdown to the user
2. Ask: "Would you like me to create these as Jira subtasks under the parent issue?"
3. If yes, use `mula-tool jira create-subtask` for each task
4. If no: "Your task breakdown is ready. Implement using your preferred workflow."

## References

| Reference | Purpose |
|-----------|---------|
| `references/start.md` | Conversational exploration and requirements gathering |
| `references/improve.md` | 6-dimension prompt quality assessment and optimization |
| `references/summarize.md` | Extract requirements from conversation into mini-PRD |
| `references/prd.md` | Strategic questioning to create comprehensive PRD |
| `references/plan.md` | Transform PRD into actionable task breakdown + Jira subtasks |
| `references/refine.md` | Iterate on existing PRD or saved prompt + Jira updates |
