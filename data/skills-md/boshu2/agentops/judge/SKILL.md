---
name: judge
description: 'Multi-model validation council. Spawns independent judges to review changes and reports PASS/FAIL/DISAGREE consensus. Triggers: judge, council, multi-model validation, consensus.'
dependencies:
  - vibe  # optional - reuse vibe checklist / toolchain outputs
  - swarm # optional - use swarm to spawn judges if Task tool is unavailable
---

# Judge Skill

Spawn multiple independent judges (preferably different models) to validate the same target and produce a consensus verdict.

**Purpose:** Reduce self-grading bias by getting external agreement (or surfacing disagreement early).

**Output:** A structured council report (PASS/FAIL/DISAGREE) with judge-by-judge findings and a disagreement section.

---

## Interface

```bash
/judge <target>
/judge recent
/judge path/to/dir
/judge <bead-id>                # e.g., epic-123, gt-55
/judge --models=opus,sonnet
/judge --count=3
```

**Target resolution (best-effort):**
- `recent`: last ~3 commits (or last 24h)
- file/dir path: validate only that scope
- bead/epic id: validate changes associated with that work (usually `recent` unless additional tooling exists)

---

## Execution Steps

### Step 0: Choose Council Configuration

Defaults (override if user specifies):
- `COUNT=2`
- `MODELS=opus,sonnet` (or closest equivalents available)
- `TARGET=recent`

**Model availability rule:** If you cannot run a requested model, substitute the closest available model and record the substitution in the report.

### Step 1: Build a Judge Packet (Single Source of Truth)

Create one packet that every judge receives, containing:
- target definition (what to review)
- changed files list (if available)
- how to run validations (tests/lint/build commands)
- the checklist to apply
- required report format

If you are in a git repo, prefer:
```bash
git diff --name-only HEAD~3 2>/dev/null | head -200
git log --oneline -5 2>/dev/null
```

If you have `/vibe` outputs, include:
- `.agents/tooling/*.txt` summaries (or the single most relevant tool logs)

### Step 2: Spawn Judges (Independent, No Cross-Talk)

**Preferred (Full profile):** Use background agents with explicit model selection (if supported).

Example (pseudocode):
```
Task(
  subagent_type="general-purpose",
  run_in_background=true,
  model="<judge-model>",
  prompt="<judge packet>"
)
```

**If model selection is NOT supported:**
- Still spawn `COUNT` judges with the same packet, but enforce independence:
  - don’t share intermediate conclusions between judges
  - run them sequentially (fresh context) or in parallel if your platform supports it

**If background agents are NOT supported (manual profile):**
- Run the same packet in separate external chats/sessions (or separate provider tabs).
- Paste each judge’s raw report into this session and continue to Step 3.

### Step 3: Collect Reports + Compute Consensus

Collect each judge report and compute:
- `PASS` if all judges say PASS
- `FAIL` if any judge says FAIL
- `DISAGREE` if verdicts differ (e.g., PASS + WARN/FAIL), or if judges disagree materially on risk/severity

### Step 4: Produce the Council Report (Required Format)

```markdown
## Council Consensus: PASS | FAIL | DISAGREE

**Target:** <target>
**Models:** <list>
**Judges:** <count>

| Judge | Model | Verdict | Key Findings |
|------:|-------|---------|--------------|
| 1 | opus | PASS | ... |
| 2 | sonnet | FAIL | ... |

### Shared Findings
- ...

### Disagreements (if any)
- ...

### Recommended Actions
- ...
```

**Quality bar:** If any judge reports “cannot verify”, treat that as a disagreement unless the missing capability is clearly irrelevant to the target.

---

## Judge Checklist (What Each Judge Must Do)

Each judge must independently answer:
1. What changed (files, behavior, interfaces)?
2. What could break (tests, edge cases, backwards compatibility)?
3. Security concerns (auth, secrets, injection, supply chain)?
4. Quality concerns (dead code, unclear abstractions, copy/paste, missing docs)?
5. Verification evidence: what command/output proves correctness?

Judges should cite concrete evidence when possible (file paths, command output, specific diffs), and explicitly call out uncertainty.

---

## Integration: `/vibe --council`

If invoked via `/vibe --council`, treat the vibe result as the baseline and run a council pass over the same target. The council report should be appended to the vibe report as an additional section, not as a replacement.

