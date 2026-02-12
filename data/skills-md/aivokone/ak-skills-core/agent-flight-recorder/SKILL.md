---
name: agent-flight-recorder
version: "2.2"
description: >
  Flight recorder for agent work sessions. Always on. Recorder-only: logs only
  deviations from the expected path as append-only entries. One run per file.
  No analysis, no developer guidance.
---

# Agent Flight Recorder

## Purpose

Keep a black-box flight recorder. Whenever you deviate from the straight path
during a task (retry, workaround, unexpected setup, missing context, quality
rework, blocker), create a concise log entry.

You are the recorder, not the analyst.

## Activation

Always active. You do not need to be asked.

- Record silently. Do not mention logging mid-task.
- Logging must not slow you down or change your approach.
- At task end (or abort), if entries exist, add exactly one line to your final
  response:

  `Flight recorder: N entries logged. See <path>.`

- If zero entries, say nothing.

## Run log file (one run per file)

Create a new file per run:

`<project-root>/.agent/flight-recorder/flight-YYYY-MM-DD-HHMMSS-TZ.md`

- Use local time if known, otherwise UTC and write `UTC` as TZ.
- If a name collision occurs, append `-1`, `-2`, ... until unique.
- Do not edit old run files.
- Within the current run file, entries are append-only.
- If the directory does not exist, create it.

When creating a new run file, write this header once:

```yaml
schema: flight-recorder/v2.2
run_started: 2026-02-11T09:10:00Z
```

### Fallback

If file write is impossible, include the full log inline at the end of your
final response under:

`## Flight recorder log (inline)`

Also state in one sentence that file write failed.

## Write strategy (batch by default)

Default: keep entries in memory and write/append to file only:
1. at task end or abort,
2. immediately before asking the user a blocking clarification question,
3. immediately before a major context switch where you might lose state,
4. immediately after creating a `high` severity entry.

When you flush, append all accumulated entries in one write.

## When to write an entry (only deviations)

Write an entry when any of the following occurs and it is a deviation from the
expected path:

| trigger | default severity | meaning |
| --- | --- | --- |
| detour | medium | You changed approach because the expected path failed. |
| setup | medium | Unexpected install/config required. |
| retry | medium | You repeated a step due to failure or ambiguity. |
| missing-context | low | You had to ask for info that should have been in initial context, or needed a blocking clarification. |
| quality | high | Output required rework to meet expected standard. |
| slow-step | high | A single step was unusually slow (ordinal estimate). |
| assumption | low | You proceeded on an assumption that could be wrong. |
| blocker | high | You could not proceed without external action. |

Notes:
- Do not log normal expected steps.
- `missing-context` is not normal interaction. Log it only when it blocks
  progress or reveals missing initial inputs.
- Override severity if warranted.

## Entry format

Each entry is a fenced YAML block for reliable parsing. Keep it concise.
IDs are assigned per run as `e1`, `e2`, `e3`, in the order you flush them.

`why` must be one short sentence (max 15 words).

### Standard YAML entry

```yaml
id: e1
severity: high | medium | low
trigger: detour | setup | retry | missing-context | quality | slow-step | assumption | blocker
situation: One sentence. What you were trying to do.
stuck: One sentence. Where exactly it got stuck.
why: One short sentence. Best hypothesis.
workaround: What you did to get past it (or attempted).
resolved: true | false | partial

# Cost signal (do NOT invent minutes unless measured)
waste: low | medium | high
waste_min: 10            # optional, only if measured or explicitly provided
time_basis: timestamped | command_duration | explicit_user | other  # required if waste_min present
retries: 2               # optional integer

# Optional routing/context
scope: env | build | deploy | web | parsing | auth | data | other
file: path/to/relevant/file
repeat_of: e3
signal: A short symptom or error signature to recognize early
```

### Compact YAML entry (low severity only)

Use this for low-severity entries to keep logging cheap:

```yaml
id: e4
severity: low
trigger: assumption | missing-context
situation: One sentence.
stuck: One sentence.
why: One short sentence. Best hypothesis.
resolved: true | false | partial
waste: low | medium | high
signal: Optional short symptom.
```

## Rules

- Recorder-only: do not include analysis, developer guidance, or improvement
  suggestions.
- Do not include secrets, tokens, raw user data, or PII. Summarize and
  anonymize.
- Prefer writing the entry after the deviation is resolved, so `resolved` and
  `retries` are accurate.
- Do not edit earlier entries. If something repeats, create a new entry with
  `repeat_of`.
