---
name: autonomous-fixes
description: 'Fix findings from autonomous-tests. Args: all | critical | high | vulnerability
  | file:<path> (default: interactive selection). Example: /autonomous-fixes vulnerability'
argument-hint: 'all | critical | high | vulnerability | file:<path>'
disable-model-invocation: true
allowed-tools: Bash(*), Read(*), Write(*), Edit(*), Glob(*), Grep(*), Agent(*),
  EnterPlanMode(*), ExitPlanMode(*), TaskCreate(*),
  TaskUpdate(*), TaskList(*), TaskGet(*), TeamCreate(*),
  SendMessage(*), TeamDelete(*), AskUserQuestion(*)
hooks:
  PreToolUse:
    - matcher: ExitPlanMode
      hooks:
        - type: command
          command: "echo '{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\"}}'"
    - matcher: AskUserQuestion
      hooks:
        - type: command
          command: "echo '{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\"}}'"
---

## Dynamic Context

- Args: $ARGUMENTS
- Branch: !`git branch --show-current`
- Config: !`test -f .claude/autonomous-tests.json && echo "YES" || echo "NO — requires autonomous-tests config"`
- Pending fixes: !`find docs/_autonomous/pending-fixes -name '*.md' 2>/dev/null | wc -l | tr -d ' '`
- Fix results: !`find docs/_autonomous/fix-results -name '*.md' 2>/dev/null | wc -l | tr -d ' '`
- Test results: !`find docs/_autonomous/test-results -name '*.md' 2>/dev/null | wc -l | tr -d ' '`
- Agent Teams: !`python3 -c "import json;s=json.load(open('$HOME/.claude/settings.json'));print('ENABLED' if s.get('env',{}).get('CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS')=='1' else 'DISABLED')" 2>/dev/null || echo "DISABLED — settings not found"`

## Role

Project-agnostic autonomous fix runner. Reads findings from `autonomous-tests` output, lets the user select items to fix, plans and executes fixes via Agent Teams, verifies results, and updates documentation to enable re-testing — creating a bidirectional test-fix loop.

## Orchestrator Protocol

The main agent is the Orchestrator. It coordinates phases but NEVER executes operational work.

**Orchestrator MUST delegate to agents:**
- Bash commands (capabilities scan, health checks, port scanning, cleanup)
- Source code reading (only agents read application source)
- File generation (docs, reports)
- Test execution, fix application, verification

**Orchestrator MAY directly:**
- Read config, SKILL.md, and reference files
- Run `date -u` for timestamps, `test -f` for file checks
- Enter/exit plan mode
- Use AskUserQuestion for user interaction
- Use TeamCreate/TaskCreate/TaskUpdate/SendMessage for coordination
- Compile summaries from agent reports
- Make phase-gating decisions (proceed/stop/abort)

**Reporting hierarchy:** Agent → Orchestrator → Plan

## Arguments: $ARGUMENTS

| Arg | Meaning |
|---|---|
| _(empty)_ | Default: interactive selection via AskUserQuestion |
| `all` | Select all fixable items (V, F, T prefixes) |
| `critical` | Pre-select items with Severity = Critical |
| `high` | Pre-select items with Severity = Critical or High |
| `vulnerability` | Pre-select all security/vulnerability items (V-prefix) |
| `file:<path>` | Target a specific pending-fixes or test-results file |

Print resolved scope, then proceed without waiting.

---

## Phase 0 — Bootstrap

**Step 0 — Prerequisites**: Read `~/.claude/settings.json`. Verify `env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is `"1"` → if not, **STOP**: "Run `bash <skill-dir>/scripts/setup-hook.sh`". If `PreToolUse` hooks absent from global settings → inform (skill-scoped hooks work automatically), continue.

**Config hash method**: `python3 -c "import json,hashlib;d=json.load(open('.claude/autonomous-tests.json'));[d.pop(k,None) for k in ('_configHash','lastRun','capabilities')];print(hashlib.sha256(json.dumps(d,sort_keys=True).encode()).hexdigest())"`

**Step 1 — Config Validation**: This skill reuses `.claude/autonomous-tests.json`.
1. `test -f .claude/autonomous-tests.json` → if missing, **STOP**: "Run `/autonomous-tests` first."
2. Read config. Validate `version` equals `5`.
3. Verify config trust: compute hash via **Config hash method**, check against `~/.claude/trusted-configs/`. If untrusted → show config (redact `testCredentials`), confirm via `AskUserQuestion`.
4. Ensure `documentation.fixResults` exists → if missing, add `"fixResults": "docs/_autonomous/fix-results"`, save.
5. If config modified in step 4 → re-stamp trust using **Config hash method**.

**Step 2 — CLAUDE.md Deep Scan**: Delegate to Explore agent. Scan CLAUDE.md files up to 3 levels deep, plus `~/.claude/CLAUDE.md` and `.claude/CLAUDE.md`. Return discovered file list. Cache for Phase 2.

**Step 3 — Findings Scan**: Delegate to Explore agent. Scan configured `_autonomous/` directories (`documentation.pendingFixes`, `documentation.testResults`, `documentation.fixResults`). Report: pending-fixes count, test-results with `### Requires Fix` or `### Vulnerabilities`, prior fix-results. If no actionable findings → **STOP**: "No findings. Run `/autonomous-tests` first."

**Step 4 — Resume Detection**: Delegate to agent. Run `git diff --name-only` and cross-reference modified files against finding source files from Step 3. If fixes appear already applied (modified files overlap with files referenced in findings):
- Print: "Fixes detected in working tree. Skipping to Phase 4 (Verification & Documentation)."
- Execute ALL Phase 4 substeps (4a → 4b → 4c) — no shortcuts.

---

## Phase 1 — Findings (User Selection Gate)

Delegate document parsing to Explore agent. Agent parses all `_autonomous/` documents per `references/finding-parser.md` rules, returns structured findings:

1. **Vulnerabilities** (V-prefix): Category = `Security Gap`/`Data Leak`/`Privacy Violation` or from `### Vulnerabilities`/`### API Response Security`. Each includes: OWASP category, Severity, Regulatory impact (LGPD/GDPR/CCPA/HIPAA), Exploitability, Compliance risk.
2. **Bugs** (F-prefix): Pending-fixes, non-security categories.
3. **Failed Tests** (T-prefix): Test-results `### Requires Fix`.
4. **Informational**: Guided (G) and autonomous (A) — counts only, not selectable.

Orchestrator receives findings, applies pre-selection: `all` → V+F+T | `critical` → Severity=Critical | `high` → Critical+High | `vulnerability` → V-prefix | `file:<path>` → specified file only. No argument → present via `AskUserQuestion` (hook-forced).

Do NOT read any source code during this phase. Source reading happens in Phase 2.

---

## Phase 2 — Plan

**Enter plan mode (Use /plan).**

**Step 0 — Context Reload** (for post-approval reconstruction): Re-read SKILL.md, config, templates. Record: resolved arguments (`$ARGUMENTS`), branch, selected items (IDs, titles, sources), key finding context, user notes.

**Self-containment mandate** — the plan MUST embed directly (not reference "above" or prior phases):
1. All selected items (ID, title, source file, severity, category, OWASP for V-prefix)
2. Fix Context Documents — condensed per item (root cause, affected files, code path, fix design)
3. Concrete per-item agent spawn instructions (source paths, fix steps, verification commands, expected outcomes)
4. Full Phase 3/4 instructions with resolved values — no "see above"
5. Config paths: `documentation.fixResults`, `documentation.pendingFixes`, `documentation.testResults`, `database.connectionCommand`, `testing.unitTestCommand`
6. CLAUDE.md file list from Phase 0 Step 2

- Execution Protocol (embed verbatim — orchestrator uses this after context reset):
  ```
  TEAM: TeamCreate → fix team (team_name for all agents)
  MODEL: Always model: "opus"
  SETUP AGENT: Spawn first (general-purpose, opus, team_name). Reads source files referenced by findings, compiles Fix Context Documents, reads CLAUDE.md files, reports via SendMessage. Shut down before fix agents.
  FLOW: STRICTLY SEQUENTIAL — one fix agent at a time:
    1. For each selected item (in order):
       a. Spawn ONE agent (general-purpose, opus, team_name)
       b. TaskUpdate with: Fix Context Document, source paths, fix instructions, verification steps
       c. BLOCK — wait for completion
       d. SendMessage type: "shutdown_request"
       e. Wait for shutdown confirmation
       f. Next item
  PROHIBITED: multiple agents alive, spawning N+1 before N shutdown, parallel execution, main-conversation fixes
  SHUTDOWN: SendMessage shutdown_request to all teammates after completion
  ```

- Post-Fix Checklist (embed verbatim in every plan):
  ```
  ## Post-Fix Checklist
  1. [ ] 4a: Verification agent confirms tests pass
  2. [ ] 4b: Fix-results doc created at `documentation.fixResults`
  3. [ ] 4b: Resolution blocks appended to pending-fixes
  4. [ ] 4b: Test-results updated for T-prefix items (if applicable)
  5. [ ] 4c: Loop signal printed
  6. [ ] 4c: Source cleanup eligibility checked -> AskUserQuestion if all resolved
  7. [ ] 4c: Unresolved V-prefix warnings printed (if applicable)
  8. [ ] 4c: `/clear` reminder printed
  ```

**Setup agent** (MANDATORY): Spawn setup agent (`general-purpose`, `model: "opus"`, `team_name`) to read all source files referenced by findings, compile Fix Context Documents, read discovered CLAUDE.md files for architecture context, report via `SendMessage`. Shut down after reporting. **Orchestrator MUST embed the setup agent's Fix Context Documents into the plan text** — condensed but complete.

**Fix Context Document per item**:
1. Verify finding reproduces — if code changed and issue gone → `Status: ALREADY_RESOLVED`, skip
2. Read referenced files (endpoint, model, test) — record file paths
3. Trace code path: input → processing → output — summarize path
4. Identify root cause — state explicitly
5. Design fix — concrete steps with file:line references

**V-prefix enhanced context**: Trace full I/O path for affected handler. Identify ALL user-controlled inputs reaching vulnerable code. Check related patterns in same file/module. Assess regulatory exposure. Design security-aware remediation: DTO filtering, validation/sanitization layers, rate limiting, protective guards.

Execution is **STRICTLY SEQUENTIAL** — one agent at a time.

**Wait for user approval.**

---

## Phase 3 — Execution

`TeamCreate` → fix team. For each selected item (in order):
1. Spawn ONE agent (`general-purpose`, `model: "opus"`, `team_name`)
2. `TaskUpdate` with: Fix Context Document, source paths, fix instructions, verification steps
3. BLOCK — wait for completion
4. `SendMessage` → `shutdown_request`
5. Next item

**Standard fix agent instructions**:
1. Read Fix Context Document → re-read source → implement fix (root cause)
2. Run unit tests if configured (`testing.unitTestCommand`)
3. Verify with targeted checks (API calls, DB queries, log inspection)
4. Report: RESOLVED / PARTIAL / UNABLE with details
5. Record `Original Test IDs` from source finding's `Test ID` field into fix-results documentation

**V-prefix additional instructions**:
1. Enforce DTO/serializer filtering — remove sensitive data from responses
2. Add input validation/sanitization at boundary
3. Rate limiting, file size validation, content-type validation where applicable
4. Circuit breakers for external service interactions
5. Harden error responses (no stack traces, internal metadata, debug info)
6. Verify no new attack vectors introduced
7. Check same pattern in related files/endpoints
8. Test with variant attack payloads

Never fix in main conversation — always delegate.

---

## Phase 4 — Results & Docs

Verify fixes, generate documentation, offer source cleanup.

### 4a. Verification

Delegate to agents.

**Standard**: confirm modified files, run unit tests, re-execute failing scenario.

**V-prefix**: re-test original attack vector (must block), test variant payloads, verify no auth bypass/privilege escalation, verify hardened error responses, verify sensitive data removal, check rate limiting.

Mark each: **RESOLVED** / **PARTIAL** / **UNABLE**.

### 4b. Documentation

Delegate to agent. Timestamp via `date -u +"%Y-%m-%d-%H-%M-%S"`. Read `references/templates.md`.

- **Fix-results**: always generated at `documentation.fixResults` path (metadata, per-item results, next steps)
- **Resolution blocks**: append `### Resolution` to pending-fixes entries
- **Test-results updates**: append fix-applied status to T-prefix entries
- **V-prefix**: include `### Security Impact` (OWASP, attack vector, regulatory impact, mitigation, related patterns, residual risk)

### 4c. Loop Signal & Finalize

Print fix cycle summary:
```
## Fix Cycle Complete
- Items attempted: {N} | Resolved: {N} | Partial: {N} | Unable: {N}
Re-run autonomous-tests to verify: `/autonomous-tests`
```

If `Ready for Re-test: YES` → inform user re-testing will be prioritized.

**Source Document Cleanup**: Check resolution status per source document:
- Pending-fixes: every `## Fix N:` has `### Resolution` with `Status: RESOLVED` + `Verification: PASS`
- Test-results `### Requires Fix`: every entry has fix-applied annotation
- Test-results `### Vulnerabilities`/`### API Response Security`: every entry `Status: RESOLVED`

All resolved → offer removal via `AskUserQuestion` ("Fix-results preserved as permanent record"). Any unresolved → keep, inform user. Never remove fix-results.

**Vulnerability warning** (unresolved V-prefix):
```
WARNING: UNRESOLVED SECURITY FINDINGS — manual attention required:
1. Data leaks — {V-prefix items}
2. Credential exposure — {V-prefix items}
3. Privilege escalation — {V-prefix items}
4. Denial-of-service — {V-prefix items}
5. Compliance violations — {V-prefix items}
```

> **Important**: Run `/clear` before invoking another skill to free context tokens and prevent stale state.

Phase 4c is the LAST step. There is no Phase 5.

---

## Rules

- No production data/connections; no credentials in output
- Plan mode before execution (Phase 2)
- Delegate via TeamCreate flow — never fix in main conversation; `Agent` without `team_name` prohibited in Phase 3
- Always `model: "opus"` for agents
- **STRICTLY SEQUENTIAL** — one agent at a time, block until shutdown before next
- Present findings before source reading (Phase 1 before Phase 2)
- AskUserQuestion hook ensures selection in dontAsk/bypass mode
- Security fixes address root causes, not symptoms
- UTC timestamps via `date -u` — never guess
- Reuse `.claude/autonomous-tests.json` — no separate config
- No Docker MCPs where `safe: false`
- V-prefix: always enhanced context + verification + documentation
- Documentation (4b) is NOT the end — 4c (loop signal + cleanup + finalize) is MANDATORY. Never stop after generating docs.
