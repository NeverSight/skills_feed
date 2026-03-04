---
name: debug-log-analysis
description: 'Structured debug log analysis for Claude Code sessions — copy log, run reducer, extract error patterns, correlate with full log, produce observability report. Fills 5 identified gaps: hook error body capture, agent identity, file path tracking, stall correlation, success visibility.'
version: 1.2.0
model: sonnet
invoked_by: both
user_invocable: true
category: Debugging
agents: [reflection-agent, devops-troubleshooter, developer]
tags: [debugging, observability, debug-log, errors, reflection, telemetry]
tools: [Read, Write, Bash, Grep]
error_handling: graceful
streaming: supported
verified: true
lastVerifiedAt: '2026-03-01'
---

**Mode: Cognitive/Prompt-Driven** — No standalone utility script; use via agent context.

# Debug Log Analysis

Structured workflow for extracting actionable signal from Claude Code session debug logs. Use during reflection cycles, incident response, or when diagnosing agent failures.

## When to Use

- After any session with unexpected agent failures or stalls
- When reflection-agent needs telemetry to contextualize task completions
- When debugging hook errors that appear opaque in task outputs
- When the router reports "agent completed but didn't call TaskUpdate"

## Prerequisites

Read `scripts/reduce-debug-log.mjs` first to understand reducer arguments.

## Step 1: Locate the Debug Log

Claude Code writes debug logs when started with `-d` flag. Current session log path is in the Claude Code UI header. Format:

```
C:\Users\{user}\.claude\debug\{session-id}.txt
```

Also check: `C:\dev\projects\agent-studio\.tmp\{session-id}.txt`

## Step 2: Copy + Reduce

```bash
# 1. Copy the log (never operate on original)
cp "{debug-log-path}" ".claude/context/tmp/debug-session-{date}.txt"

# 2. Run reducer (98%+ noise reduction)
node scripts/reduce-debug-log.mjs \
  ".claude/context/tmp/debug-session-{date}.txt" \
  --output ".claude/context/tmp/debug-session-{date}-reduced.txt"

# 3. Check reducer output size
wc -l ".claude/context/tmp/debug-session-{date}-reduced.txt"
```

## Step 3: Read Reduced Log

Read `.claude/context/tmp/debug-session-{date}-reduced.txt` in full.

## Step 4: Categorize Error Patterns

For each line in the reduced log, classify into:

| Category                    | Signal Pattern                                                 | Action                                   |
| --------------------------- | -------------------------------------------------------------- | ---------------------------------------- |
| **Hook Block (Write)**      | `PreToolUse:Write` + block                                     | Count; find triggering agent + file path |
| **Hook Block (TaskUpdate)** | `PreToolUse:TaskUpdate` + burst                                | Count; find looping agent                |
| **Read Miss**               | `File does not exist` or placeholder text                      | Count; list missing files                |
| **Token Overflow**          | `FileTooLargeError` or `token limit`                           | Count; identify large files              |
| **Streaming Stall**         | Gap > 60s between log entries                                  | Sum duration; note what preceded stall   |
| **Agent Drop**              | `TaskUpdate not called` or `agent returned` without completion | List by task ID                          |
| **Tool Error**              | `EISDIR`, `ENOENT`, `sibling tool call errored`                | Categorize by tool                       |

## Step 5: Cross-Reference Top Errors in Full Log

For the top 3 most frequent error categories:

1. Grep the FULL (unreduced) log copy for the error signature
2. Find the 10 lines before and after each occurrence
3. Identify: which tool call triggered it, which agent was running, what it was trying to do

```bash
grep -n "PreToolUse:Write" ".claude/context/tmp/debug-session-{date}.txt" | head -30
```

## Step 6: Produce Structured Report

Write to `.claude/context/reports/reflections/debug-log-analysis-{date}.md`:

```markdown
# Debug Log Analysis — {date}

**Session:** {session-id}
**Log size:** {N} lines → {M} lines after reduction ({X}% reduction)
**Analysis duration:** {time}

## Error Summary

| Category           | Count | Severity | Root Cause |
| ------------------ | ----- | -------- | ---------- |
| Hook Block (Write) | N     | CRITICAL | ...        |
| Read Miss          | N     | HIGH     | ...        |
| ...                |       |          |            |

## Top 3 Deep Dives

### 1. {Most frequent error}

**Frequency:** N occurrences
**First occurrence:** line {N}, timestamp {T}
**Context:** {what the agent was doing}
**Root cause:** {why it happened}
**Fix:** {concrete recommendation}

### 2. ...

### 3. ...

## Observability Gaps Found

List any gaps where the log entry doesn't have enough info to diagnose the error.

## Recommendations

- [ ] Immediate P0: {fix}
- [ ] P1: {fix}
- [ ] P2: {fix}
```

## Known Observability Gaps (Agent-Studio v2026-02)

These gaps exist in the current debug log format:

1. **Hook rejection body not logged** — When `unified-creator-guard.cjs` blocks a Write, the rejection reason is not captured in the debug log. You see `PreToolUse:Write blocked` but not WHY.
   - Workaround: Check `process.stderr` output separately; or read the hook source to infer the rule that fired.

2. **Agent identity missing from error lines** — Error lines don't include which spawned agent caused the error.
   - Workaround: Correlate timestamps with task spawn/completion entries.

3. **Read failure file path omitted** — `File does not exist` lines don't always include the file path.
   - Workaround: Look at the preceding tool call line for the attempted path.

4. **Streaming stalls unattributed** — A 5+ minute stall appears as a timestamp gap with no context.
   - Workaround: The tool call preceding the gap is the likely cause.

5. **No success logging** — Only failures are prominent. Successful tool calls produce minimal log entries.
   - Workaround: Count total tool uses from task summary metadata.

## Integration with Reflection

Reflection agents should invoke this skill for HIGH-priority reflection requests:

```javascript
// In reflection agent, for high-priority triggers:
if (priority === 'high' && debugLogPath) {
  Skill({ skill: 'debug-log-analysis' });
  // Include findings in reflection report
}
```

## Iron Laws

1. **ALWAYS** copy the debug log before any analysis — never operate on the original file; in-place operations corrupt the forensic artifact.
2. **NEVER** report a root cause based on a single grep match — always read at least 10 lines of context before and after the match to understand what the agent was actually doing.
3. **ALWAYS** run the reducer script (Step 2) before attempting to read a full debug log — unfiltered debug logs contain 98%+ noise that obscures real signals.
4. **NEVER** skip the structured error report (Step 6) — an informal verbal summary is not a deliverable; the markdown report is required for reflection-agent to incorporate findings.
5. **ALWAYS** write new recurring error patterns to `.claude/context/memory/issues.md` — patterns not written to memory will recur invisibly across sessions.

## Anti-Patterns

| Anti-Pattern                              | Why It Fails                                                         | Correct Approach                                                                    |
| ----------------------------------------- | -------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Grepping the original log file directly   | Modifies timestamps, corrupts forensic artifact, no rollback         | Always copy first: `cp debug.txt .claude/context/tmp/debug-{date}.txt`              |
| Reading the full unreduced log            | 98%+ noise-to-signal ratio; analysis takes hours and misses patterns | Run `reduce-debug-log.mjs` first; work from the reduced output                      |
| Reporting root cause from single grep hit | Single matches are often false positives from unrelated tool calls   | Read ±10 lines of context for every match before concluding root cause              |
| Informal verbal summary instead of report | Reflection agent can't parse informal summaries into memory entries  | Write the full structured markdown report to `.claude/context/reports/reflections/` |
| Skipping memory writes after analysis     | Error patterns recur invisibly; no institutional learning            | Write every new pattern to issues.md or learnings.md before task complete           |

## Memory Protocol (MANDATORY)

**After completing:**

- New error pattern found → `.claude/context/memory/issues.md`
- New observability gap found → `.claude/context/memory/issues.md`
- Pattern that recurs across sessions → `.claude/context/memory/learnings.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
