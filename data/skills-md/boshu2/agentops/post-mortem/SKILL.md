---
name: post-mortem
description: 'Tools-first post-implementation validation. Runs toolchain (linters, tests, scanners), then dispatches agents to synthesize findings. Triggers: "post-mortem", "validate completion", "final check", "wrap up epic".'
---

# Post-Mortem Skill

> **Quick Ref:** Toolchain → Agent Synthesis → Knowledge Extraction. Output: `.agents/retros/*.md` + `.agents/learnings/*.md`

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

**Architecture:** Tools do 95% of validation. Agents synthesize the 5%.

## Execution Steps

Given `/post-mortem [epic-id]`:

### Step 1: Run Toolchain Validation (MANDATORY FIRST)

**Before anything else, run the toolchain:**

```bash
./scripts/toolchain-validate.sh --gate 2>&1 | tee .agents/tooling/run.log
TOOL_EXIT=$?
```

**Check exit code:**
- `0` = All tools pass → proceed
- `2` = CRITICAL findings → STOP, report to user
- `3` = HIGH findings only → proceed with warnings

### Step 1a: Early Exit on CRITICAL Tool Failures

**If TOOL_EXIT == 2:**

```
STOP IMMEDIATELY.

Report to user:
  "Toolchain validation found CRITICAL issues. Fix before post-mortem."

  Tool outputs in .agents/tooling/:
  - gitleaks.txt: <count> secret findings
  - ruff.txt: <count> lint errors
  - ...

  Run: cat .agents/tooling/<tool>.txt
  Fix the issues, then re-run /post-mortem
```

**DO NOT dispatch agents.** Tools found definitive problems.

### Step 2: Identify What Was Completed

**If epic ID provided:** Use it directly.

**If no epic ID:** Find recently completed work:
```bash
bd list --status closed --since "7 days ago" 2>/dev/null | head -5
```

Or check recent git activity:
```bash
git log --oneline --since="24 hours ago" | head -10
```

### Step 3: Build Mechanical Comparison Table

**Generate checklist from plan before reading code:**

If plan exists (`.agents/plans/*.md`):
```
1. Extract all TODO/deliverable items from plan
2. For each item:
   - Expected file: <path>
   - File exists: yes/no
   - Implementation matches spec: yes/no (cite file:line)
```

This creates ground truth for plan-compliance, not gestalt impression.

Write comparison table to prompt text for plan-compliance-expert agent.

### Step 4: Dispatch Synthesis Agents (with Tool Output)

**Before dispatching, substitute placeholders:**
- `<epic-id>`: From Step 2
- `<paste .agents/tooling/X.txt>`: Read and inline file contents
- `<from Step 3>`: Use the comparison table built in Step 3

**Now dispatch agents to TRIAGE tool findings, not to FIND issues.**

Launch 4 agents in parallel (single message, 4 Task tool calls):

```
Tool: Task (ALL 4 IN PARALLEL)
Parameters:
  subagent_type: "agentops:security-reviewer"
  model: "haiku"
  description: "Triage security tool findings"
  prompt: |
    Tool output from gitleaks and other scanners:
    <paste .agents/tooling/gitleaks.txt>
    <paste .agents/tooling/semgrep.txt if exists>

    For each finding:
    1. Read the cited file:line
    2. Assess: true positive or false positive?
    3. If true positive: severity (CRITICAL/HIGH/MEDIUM/LOW) and fix

    Output format:
    | File:Line | Tool Finding | Verdict | Severity | Fix |
    |-----------|--------------|---------|----------|-----|

Tool: Task
Parameters:
  subagent_type: "agentops:code-reviewer"
  model: "haiku"
  description: "Triage code quality findings"
  prompt: |
    Tool output from linters:
    <paste .agents/tooling/ruff.txt or golangci-lint.txt>

    Complexity output:
    <paste .agents/tooling/radon.txt if exists>

    For each finding:
    1. Read the cited file:line
    2. Assess: worth fixing now, tech debt, or noise?
    3. If worth fixing: suggest specific change

    Output format:
    | File:Line | Tool Finding | Priority | Suggested Fix |
    |-----------|--------------|----------|---------------|

Tool: Task
Parameters:
  subagent_type: "agentops:plan-compliance-expert"
  model: "haiku"
  description: "Verify plan completion"
  prompt: |
    Plan file: <path to .agents/plans/*.md>
    Mechanical comparison table: <from Step 3>

    For each plan item marked "no" or "partial":
    1. Is this a real gap or scope change?
    2. Should it be tracked as follow-up issue?

    Output format:
    | Plan Item | Status | Gap Type | Action |
    |-----------|--------|----------|--------|

Tool: Task
Parameters:
  subagent_type: "agentops:flywheel-feeder"
  model: "haiku"
  description: "Extract verified learnings"
  prompt: |
    Completed work: <epic-id or description>
    Files changed: <git diff --name-only HEAD~N>

    Extract learnings that are VERIFIED (appeared in multiple places or have source citation):

    For each learning:
    - ID: L-<date>-<N>
    - Category: technical/process/architecture
    - What: <1 sentence>
    - Source: <file:line or commit hash>
    - Verification: <how we know this is true>

    DO NOT include confidence scores. Include source citations only.
```

**Timeout:** 3 minutes per agent.

**On timeout:**
- Mark agent as timed-out
- Note in report which agents timed out
- If >2 agents timeout, stop and report INCOMPLETE

### Step 5a: Log Triage Decisions

**For each TRUE_POS or FALSE_POS verdict from agents, log it for accuracy tracking:**

```bash
# Log each triage decision
./scripts/log-triage-decision.sh "src/auth.go:42" "semgrep" "TRUE_POS" "security-reviewer"
./scripts/log-triage-decision.sh "tests/mock.py:15" "gitleaks" "FALSE_POS" "security-reviewer"
```

This enables accuracy tracking over time. Ground truth is added later when:
- CI confirms (test pass/fail)
- Production incident occurs
- Human reviews the decision

**View accuracy report:**
```bash
./scripts/compute-triage-accuracy.sh
```

### Step 5: Synthesize Results

Combine agent outputs:
1. Deduplicate findings by file:line
2. Sort by severity (CRITICAL → HIGH → MEDIUM → LOW)
3. Count verified vs disputed findings

**Compute grade based on TOOL findings, not agent opinions:**

```
Grade A: 0 critical tool findings
Grade B: 0 critical, <5 high tool findings
Grade C: 0 critical, 5-15 high tool findings
Grade D: 1+ critical tool findings
Grade F: Multiple critical, tests failing
```

### Step 6: Request Human Approval (Gate 4)

```
Tool: AskUserQuestion
Parameters:
  questions:
    - question: "Post-mortem complete. Grade: <grade>. Tool findings triaged. Store learnings?"
      header: "Gate 4"
      options:
        - label: "TEMPER & STORE"
          description: "Learnings are good - lock and index"
        - label: "ITERATE"
          description: "Need another round of fixes"
      multiSelect: false
```

### Step 7: Write Post-Mortem Report

**Write to:** `.agents/retros/YYYY-MM-DD-post-mortem-<topic>.md`

**Merge agent outputs:**
1. Collect tables from all 4 agents
2. Deduplicate by file:line (within 5 lines tolerance)
3. Sort by severity (CRITICAL -> HIGH -> MEDIUM -> LOW)
4. List which agents agreed on each finding

```markdown
# Post-Mortem: <Topic/Epic>

**Date:** YYYY-MM-DD
**Epic:** <epic-id or description>
**Duration:** <how long>

## Toolchain Results

| Tool | Status | Findings |
|------|--------|----------|
| gitleaks | PASS/FAIL | <count> |
| ruff | PASS/FAIL | <count> |
| pytest | PASS/FAIL | <count> |

**Gate Status:** <PASS/BLOCKED>

## Triaged Findings

### True Positives (actionable)
| File:Line | Issue | Severity | Status |
|-----------|-------|----------|--------|

### False Positives (dismissed)
| File:Line | Tool Claimed | Why Dismissed |
|-----------|--------------|---------------|

## Plan Compliance

<Mechanical comparison table from Step 3>

## Learnings Extracted

| ID | Category | Learning | Source |
|----|----------|----------|--------|

**Note:** No confidence scores. Source citations only.

## Follow-up Issues

<Issues created from findings>

## Knowledge Flywheel Status

- **Learnings indexed:** <count from ao forge>
- **Session provenance:** <session-id>
- **ao forge status:** PASS/SKIP (not available)
```

### Step 7a: Index Learnings via ao forge (Knowledge Flywheel)

**If user approved TEMPER & STORE in Gate 4, index learnings into knowledge base:**

```bash
# Check if ao CLI is available
if command -v ao &>/dev/null; then
  # Index learnings from the retro/learnings directory
  ao forge index .agents/learnings/ 2>&1 | tee -a .agents/tooling/ao-forge.log
  AO_EXIT=$?

  # Add provenance tracking - link learnings to this session
  SESSION_ID=$(ao session id 2>/dev/null || echo "unknown")
  echo "Provenance: session=$SESSION_ID, timestamp=$(date -Iseconds)" >> .agents/learnings/provenance.txt

  # Check flywheel status
  FLYWHEEL_STATUS=$(ao flywheel status --json 2>/dev/null || echo '{"indexed": 0}')
  INDEXED_COUNT=$(echo "$FLYWHEEL_STATUS" | jq -r '.indexed // 0')

  if [ $AO_EXIT -eq 0 ]; then
    echo "Flywheel: Learnings indexed successfully"
  else
    echo "Flywheel: ao forge failed (exit $AO_EXIT) - learnings NOT indexed"
  fi
else
  echo "Flywheel: ao CLI not available - learnings written but NOT indexed"
  echo "  Install ao or run manually: ao forge index .agents/learnings/"
fi
```

**Fallback:** If ao is not available, learnings are still written to `.agents/learnings/*.md` but won't be searchable via `ao search`. The skill continues normally.

### Step 8: Report to User

Tell the user:
1. Toolchain results (which tools ran, pass/fail)
2. Grade (based on tool findings)
3. Key triaged findings
4. Learnings extracted
5. Gate 4 decision
6. **Flywheel status** (learnings indexed count)

## Key Differences from Previous Version

| Before | After |
|--------|-------|
| Agents find issues | Tools find issues, agents triage |
| Vague prompts | Checklist-driven prompts with tool output |
| Fake confidence scores | Source citations only |
| Always produces report | Gates on tool failures |
| 6 agents | 4 agents (focused on synthesis) |
