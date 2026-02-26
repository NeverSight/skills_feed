---
name: solo-pipeline
description: Launch automated multi-skill pipeline that chains skills into a loop. Use when user says "run pipeline", "automate research to PRD", "full pipeline", "research and validate", "scaffold to build", "loop until done", or "chain skills". Do NOT use for single skills (use the skill directly).
license: MIT
metadata:
  author: fortunto2
  version: "1.4.0"
  openclaw:
    emoji: "🔄"
allowed-tools: Bash, Read, Write, AskUserQuestion
argument-hint: "research <idea> | dev <name> <stack> [--feature desc]"
---

# /pipeline

Launch an automated multi-skill pipeline. The Stop hook chains skills automatically — no manual invocation needed between stages.

## Available Pipelines

### Research Pipeline
`/pipeline research "AI therapist app"`

Chains: `/research` -> `/validate`
Produces: `research.md` -> `prd.md`

### Dev Pipeline
`/pipeline dev "project-name" "stack"`
`/pipeline dev "project-name" "stack" --feature "user onboarding"`

Chains: `/scaffold` -> `/setup` -> `/plan` -> `/build`
Produces: full project with workflow, plan, and implementation

## Steps

### 1. Parse Arguments

Extract from `$ARGUMENTS`:
- Pipeline type: first word (`research` or `dev`)
- Remaining args: passed to the launcher script

If no arguments or unclear, ask:

```
Which pipeline do you want to run?

1. Research Pipeline — /research → /validate (idea to PRD)
2. Dev Pipeline — /scaffold → /setup → /plan → /build (PRD to running code)
```

### 2. Confirm with User

Show what will happen:

```
Pipeline: {type}
Stages: {stage1} → {stage2} → ...
Idea/Project: {name}

This will run multiple skills automatically. Continue?
```

Ask via AskUserQuestion.

### 3. Start First Stage

Run the first skill in the pipeline directly:

For research pipeline: Run `/research "idea name"`
For dev pipeline: Run `/scaffold project-name stack`

The Stop hook (if configured) will handle subsequent stages automatically.
Without a Stop hook, manually invoke each skill in sequence.

### 3b. Launcher Scripts (optional, Claude Code plugin only)

If you have the solo-factory plugin installed, launcher scripts provide tmux dashboard and logging:

```bash
# Only available with Claude Code plugin — skip if not installed
solo-research.sh "idea name" [--project name]
solo-dev.sh "project-name" "stack" [--feature "desc"]
```

Pass `--no-dashboard` when running from within a skill context.

### 5. Pipeline Completion

When all stages are done, output:
```
<solo:done/>
```

The Stop hook checks for this signal and cleans up the state file.

## State File

Location: `.solo/pipelines/solo-pipeline-{project}.local.md` (project-local) or `~/.solo/pipelines/solo-pipeline-{project}.local.md` (global fallback)
Log file: `.solo/pipelines/solo-pipeline-{project}.log`

Format: YAML frontmatter with stages list, `project_root`, and `log_file` fields.
The Stop hook reads this file on every session exit attempt.

To cancel a pipeline manually: delete the state file `solo-pipeline-{project}.local.md`

## Monitoring

### tmux Dashboard (terminal use)

When launched from terminal (without `--no-dashboard`), a tmux dashboard opens automatically with:
- Pane 0: work area
- Pane 1: `tail -f` on log file
- Pane 2: live status display (refreshes every 2s)

### Manual Monitoring

Monitor pipeline progress with standard tools:
```bash
# Watch log file
tail -f .solo/pipelines/solo-pipeline-<project>.log

# Check pipeline state

# Auto-refresh
watch -n2 -c solo-pipeline-status.sh
```

Otherwise, use standard tools:
```bash
# Log tail
tail -f .solo/pipelines/solo-pipeline-<project>.log

# Check state file
cat .solo/pipelines/solo-pipeline-<project>.local.md
```

### Session Reuse

Re-running a pipeline reuses any existing state — completed stages are skipped automatically.
- No need to close/recreate — just run the same command again

### Log Format

```
[22:30:15] START    | my-app | stages: research -> validate | max: 5
[22:30:16] STAGE    | iter 1/5 | stage 1/2: research
[22:30:16] INVOKE   | /research "AI therapist app"
[22:35:42] CHECK    | research | .../research.md -> FOUND
[22:35:42] STAGE    | iter 2/5 | stage 2/2: validate
[22:35:42] INVOKE   | /validate "AI therapist app"
[22:40:10] CHECK    | validate | .../prd.md -> FOUND
[22:40:10] DONE     | All stages complete! Promise detected.
[22:40:10] FINISH   | Duration: 10m
```

## Critical Rules

1. **Always confirm** before starting a pipeline.
2. **Don't skip stages** — the hook handles progression.
3. **Cancel = delete state file** — tell users this if they want to stop.
4. **Max iterations** prevent infinite loops (default 5 for research, 15 for dev).
5. **Use `--no-dashboard`** when running from within Claude Code skill context.
