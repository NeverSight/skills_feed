---
name: link-dependencies
description: "Scan all plans and wire up cross-topic dependencies. Finds unresolved external dependencies, matches them to tasks in other plans, and updates both the plan index and output format."
disable-model-invocation: true
hooks:
  PreToolUse:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/workflows/system-check.sh"
          once: true
---

Link cross-topic dependencies across all existing plans.

## Instructions

Follow these steps EXACTLY as written. Do not skip steps or combine them.

## Important

Use simple, individual commands. Never combine multiple operations into bash loops or one-liners. Execute commands one at a time.

## Step 1: Discover All Plans

Scan the codebase for existing plans:

1. **Find plan files**: Look in `docs/workflow/planning/`
   - Run `ls docs/workflow/planning/` to list plan files
   - Each topic is a directory containing `plan.md`

2. **Extract plan metadata**: For each plan file
   - Read the frontmatter to get the `format:` field
   - Note the format used by each plan

**If no plans exist:**

> *Output the next fenced block as a code block:*

```
Dependency Linking

No plans found in docs/workflow/planning/

There are no plans to link. Create plans first.
```

**STOP.** Do not proceed — terminal condition.

**If only one plan exists:**

> *Output the next fenced block as a code block:*

```
Dependency Linking

Only one plan found: {topic}

Cross-topic dependency linking requires at least two plans.
```

**STOP.** Do not proceed — terminal condition.

## Step 2: Check Output Format Consistency

Compare the `format:` field across all discovered plans.

**If plans use different output formats:**

> *Output the next fenced block as a code block:*

```
Dependency Linking

Mixed output formats detected:

  • {topic} ({format})
  • ...

Cross-topic dependencies can only be wired within the same output
format. Consolidate your plans to a single format before linking.
```

**STOP.** Do not proceed — terminal condition.

## Step 3: Extract External Dependencies

For each plan, read the `external_dependencies` field from the frontmatter:

1. **Read `external_dependencies`** from each plan index file's frontmatter
2. **Categorize each dependency** by its `state` field:
   - **Unresolved**: `state: unresolved` (no task linked)
   - **Resolved**: `state: resolved` (has `task_id`)
   - **Satisfied externally**: `state: satisfied_externally`

3. **Build a summary**:

> *Output the next fenced block as a code block:*

```
Dependency Summary

{N} plans found. {M} unresolved dependencies.

Plan: {topic:(titlecase)} (format: {format})
  • {dependency}: {description} ({state:[unresolved|resolved|satisfied externally]})

Plan: ...
```

> *Output the next fenced block as a code block:*

```
Key:

  Dependency state:
    unresolved           — no task linked yet
    resolved             — linked to a task in another plan
    satisfied externally — implemented outside this workflow
```

## Step 4: Match Dependencies to Plans

For each unresolved dependency:

1. **Search for matching plan**: Does `docs/workflow/planning/{dependency-topic}/plan.md` exist?
   - If no match: Mark as "no plan exists" - cannot resolve yet

2. **If plan exists**: Load the format's reading reference
   - Read `format:` from the dependency plan's frontmatter
   - Load `../technical-planning/references/output-formats/{format}/reading.md`
   - Use the task extraction instructions to search for matching tasks

3. **Handle ambiguous matches**:
   - If multiple tasks could satisfy the dependency, present options to user
   - Allow selecting multiple if the dependency requires multiple tasks

## Step 5: Wire Up Dependencies

For each resolved match:

1. **Update the plan index file's frontmatter**:
   - Change the dependency's `state: unresolved` to `state: resolved` and add `task_id: {task-id}`

2. **Create dependency in output format**:
   - Load `../technical-planning/references/output-formats/{format}/graph.md`
   - Follow the "Adding a Dependency" section to create the blocking relationship

## Step 6: Bidirectional Check

For each plan that was a dependency target (i.e., other plans depend on it):

1. **Check reverse dependencies**: Are there other plans that should have this wired up?
2. **Offer to update**: "Plan X depends on tasks you just linked. Update its `external_dependencies` frontmatter?"

## Step 7: Report Results

Present a summary:

> *Output the next fenced block as a code block:*

```
Dependency Linking Complete

Resolved (newly linked):
  • {source} → {target}: {task-id} ({description})

Already resolved (no action needed):
  • {source} → {target}: {task-id}

Satisfied externally (no action needed):
  • {source} → {target}

Unresolved (no matching plan exists):
  • {source} → {target}: {description}

Updated files:
  • docs/workflow/planning/{topic}/plan.md
```

If any dependencies remain unresolved:

> *Output the next fenced block as a code block:*

```
Unresolved dependencies have no corresponding plan. Either:
  • Create a plan for the topic
  • Mark as "satisfied externally" if already implemented
```

## Step 8: Commit Changes

If any files were updated:

> *Output the next fenced block as markdown (not a code block):*

```
· · · · · · · · · · · ·
Shall I commit these dependency updates?
- **`y`/`yes`** — Commit the changes
- **`n`/`no`** — Skip
· · · · · · · · · · · ·
```

**STOP.** Wait for user response.

If yes, commit with message:
```
Link cross-topic dependencies

- {summary of what was linked}
```
