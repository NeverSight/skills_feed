---
name: start-feature
description: "Start a new feature through the full pipeline. Gathers context via structured interview, creates a discussion, then bridges to continue-feature for specification, planning, and implementation."
disable-model-invocation: true
allowed-tools: Bash(ls docs/workflow/discussion/), Bash(.claude/hooks/workflows/write-session-state.sh)
hooks:
  PreToolUse:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/workflows/system-check.sh"
          once: true
---

Start a new feature and route it through the pipeline: Discussion → Specification → Planning → Implementation.

> **⚠️ ZERO OUTPUT RULE**: Do not narrate your processing. Produce no output until a step or reference file explicitly specifies display content. No "proceeding with...", no discovery summaries, no routing decisions, no transition text. Your first output must be content explicitly called for by the instructions.

## Instructions

Follow these steps EXACTLY as written. Do not skip steps or combine them.

**CRITICAL**: This guidance is mandatory.

- After each user interaction, STOP and wait for their response before proceeding
- Never assume or anticipate user choices
- Even if the user's initial prompt seems to answer a question, still confirm with them at the appropriate step
- Complete each step fully before moving to the next

---

## Step 0: Run Migrations

**This step is mandatory. You must complete it before proceeding.**

Invoke the `/migrate` skill and assess its output.

**If files were updated**: STOP and wait for the user to review the changes (e.g., via `git diff`) and confirm before proceeding to Step 1. Do not continue automatically.

**If no updates needed**: Proceed to Step 1.

---

## Resuming After Context Refresh

Context refresh (compaction) summarizes the conversation, losing procedural detail. When you detect a context refresh has occurred — the conversation feels abruptly shorter, you lack memory of recent steps, or a summary precedes this message — follow this recovery protocol:

1. **Re-read this skill file completely.** Do not rely on your summary of it. The full process, steps, and rules must be reloaded.
2. **Identify the topic.** Check conversation history for the topic name. If unknown, check `docs/workflow/discussion/` for recently modified files via `git log --oneline -5`.
3. **Determine current step from artifacts:**
   - No discussion file exists → resume at **Step 1**
   - Discussion exists with `status: in-progress` → resume at **Step 3** (re-invoke technical-discussion)
   - Discussion exists with `status: concluded` → resume at **Step 4** (phase bridge)
4. **Announce your position** to the user before continuing: what step you believe you're at, what's been completed, and what comes next. Wait for confirmation.

Do not guess at progress or continue from memory. The files on disk and git history are authoritative — your recollection is not.

---

## Step 1: Gather Feature Context

Load **[gather-feature-context.md](references/gather-feature-context.md)** and follow its instructions.

→ Proceed to **Step 2**.

---

## Step 2: Topic Name and Conflict Check

Based on the feature description, suggest a topic name:

> *Output the next fenced block as a code block:*

```
Suggested topic name: {suggested-topic:(kebabcase)}

This will create: docs/workflow/discussion/{suggested-topic}.md
```

> *Output the next fenced block as markdown (not a code block):*

```
· · · · · · · · · · · ·
Is this name okay?

- **`y`/`yes`** — Use this name
- **`s`/`something else`** — Suggest a different name
· · · · · · · · · · · ·
```

**STOP.** Wait for user response.

Once the topic name is confirmed, check for naming conflicts:

```bash
ls docs/workflow/discussion/
```

If a discussion with the same name exists, inform the user:

> *Output the next fenced block as markdown (not a code block):*

```
· · · · · · · · · · · ·
A discussion named "{topic}" already exists.

- **`r`/`resume`** — Resume the existing discussion
- **`n`/`new`** — Choose a different name
· · · · · · · · · · · ·
```

**STOP.** Wait for user response.

If resuming, check the discussion status. If concluded → skip to Step 4. If in-progress → proceed to Step 3.

→ Proceed to **Step 3**.

---

## Step 3: Invoke Discussion

Before invoking the processing skill, save a session bookmark.

> *Output the next fenced block as a code block:*

```
Saving session state so Claude can pick up where it left off and continue the feature pipeline if the conversation is compacted.
```

```bash
.claude/hooks/workflows/write-session-state.sh \
  "{topic}" \
  "skills/technical-discussion/SKILL.md" \
  "docs/workflow/discussion/{topic}.md" \
  --pipeline "This session is part of the feature pipeline. After the discussion concludes, load and follow the phase bridge at skills/start-feature/references/phase-bridge.md for topic '{topic}'."
```

Load **[invoke-discussion.md](references/invoke-discussion.md)** and follow its instructions.

**CRITICAL**: When the discussion concludes (status becomes "concluded"), you MUST proceed to **Step 4** below. Do not end the session — the feature pipeline continues to specification via the phase bridge.

---

## Step 4: Phase Bridge

Load **[phase-bridge.md](references/phase-bridge.md)** and follow its instructions.

The bridge will enter plan mode with instructions to invoke continue-feature for the topic in the next session.
