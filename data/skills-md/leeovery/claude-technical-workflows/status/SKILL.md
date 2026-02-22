---
name: status
description: "Show workflow status - what exists, where you are, and what to do next."
disable-model-invocation: true
allowed-tools: Bash(.claude/skills/status/scripts/discovery.sh)
hooks:
  PreToolUse:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/workflows/system-check.sh"
          once: true
---

Show the current state of the workflow for this project.

## Step 0: Run Migrations

**This step is mandatory. You must complete it before proceeding.**

Invoke the `/migrate` skill and assess its output.

**If files were updated**: STOP and wait for the user to review the changes (e.g., via `git diff`) and confirm before proceeding to Step 1. Do not continue automatically.

**If no updates needed**: Proceed to Step 1.

---

## Step 1: Discovery State

!`.claude/skills/status/scripts/discovery.sh`

If the above shows a script invocation rather than YAML output, the dynamic content preprocessor did not run. Execute the script before continuing:

```bash
.claude/skills/status/scripts/discovery.sh
```

If YAML content is already displayed, it has been run on your behalf.

Parse the discovery output. **IMPORTANT**: Use ONLY this script for discovery. Do NOT run additional bash commands (ls, head, cat, etc.) to gather state.

→ Proceed to **Step 2**.

---

## Step 2: Present Status

Build the display from discovery data. Only show sections for phases that have content.

**CRITICAL**: Entities don't flow one-to-one across phases. Multiple discussions may combine into one specification, topic names may change between phases, and specs may be superseded. The display must make these relationships visible — primarily through the specification's `sources` array.

### 2a: Summary

> *Output the next fenced block as a code block:*

```
Workflow Status

  Research:       {count} file(s)
  Discussion:     {count} ({concluded} concluded, {in_progress} in-progress)
  Specification:  {active} active ({feature} feature, {crosscutting} cross-cutting)
  Planning:       {count} ({concluded} concluded, {in_progress} in-progress)
  Implementation: {count} ({completed} completed, {in_progress} in-progress)
```

Only show lines for phases that have content. If a phase has zero items but a later phase has content, show the line as `(none)` to highlight the gap.

#### If no workflow content exists at all

> *Output the next fenced block as a code block:*

```
Workflow Status

No workflow files found in docs/workflow/

Start with /start-research to explore ideas,
or /start-discussion if you already know what to build.
```

**STOP.** Do not proceed — terminal condition.

### 2b: Specifications

Show if any specifications exist. This is the most important section — it reveals many-to-one relationships between discussions and specifications.

> *Output the next fenced block as a code block:*

```
Specifications

  1. {name:(titlecase)} ({status})
     └─ Sources: @if(no_sources) (none) @else
        ├─ {src} ({src_status})
        └─ ...
     @endif

  2. ...
```

**Rules:**

- Each numbered item is an active (non-superseded) specification
- Show `(cross-cutting)` after status for cross-cutting specs; omit type label for feature specs
- Blank line between numbered items
- If superseded specs exist, show after the numbered list:

```
  Superseded:
    • {name} → {superseded_by}
```

### 2c: Plans

Show if any plans exist.

> *Output the next fenced block as a code block:*

```
Plans

  1. {name:(titlecase)} ({status})
     └─ Spec: {specification_name}
     @if(has_unresolved_deps) └─ Blocked:
        ├─ {dep_topic}:{dep_task_id} ({dep_state})
        └─ ...
     @endif

  2. ...
```

**Rules:**

- Map raw `planning` status to `in-progress` in the display
- Show spec name without `.md` extension

### 2d: Implementation

Show if any implementations exist.

> *Output the next fenced block as a code block:*

```
Implementation

  1. {topic:(titlecase)} ({status})
     └─ Phase {current_phase}, {completed_tasks}/{total_tasks} tasks done

  2. ...
```

**Rules:**

- `not-started` → `└─ Not started`
- `in-progress` → phase and task progress; if `total_tasks` is 0, show `{completed_tasks} tasks done` without denominator
- `completed` → `└─ Complete`

### 2e: Unlinked Discussions

Derive which discussions are NOT referenced in any active (non-superseded) specification's `sources` array. Show only if unlinked discussions exist.

> *Output the next fenced block as a code block:*

```
Discussions not yet in a specification:

  • {name} ({status})
```

### 2f: Key

Show if the display uses statuses that benefit from explanation. Only include statuses actually shown. No `---` separator before this section.

> *Output the next fenced block as a code block:*

```
Key:

  Status:
    in-progress — work is ongoing
    concluded   — complete, ready for next step
    superseded  — replaced by another specification

  Spec type:
    cross-cutting — architectural policy, not directly plannable
```

Omit categories with no entries.

---

## Step 3: Suggest Next Steps

Based on gaps in the workflow, briefly suggest 2-3 most relevant actions:

- Concluded discussions not in any spec → `/start-specification`
- In-progress specs → finish with `/start-specification`
- Concluded feature specs without plans → `/start-planning`
- Concluded plans not yet implemented → `/start-implementation`
- Completed implementations → `/start-review`

If plans exist, mention `/view-plan` for detailed plan viewing.

Keep suggestions brief — the user knows their project better than we do.

## Notes

- Keep output scannable — this is a status check, not a deep analysis
- Discussions may appear in multiple specifications' sources
- A discussion not appearing in any active spec's sources is "unlinked"
- Research files are project-wide, not topic-specific
- Topic names may differ across phases (e.g., discussions "auth-flow" and "session-mgmt" may combine into specification "auth-system")
