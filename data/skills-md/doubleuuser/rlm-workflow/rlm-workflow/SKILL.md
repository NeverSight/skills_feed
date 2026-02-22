---
name: rlm-workflow
description: Orchestrates the RLM repo workflow end-to-end with phase gates, locked artifacts, addenda, traceability, and automatic bootstrap/upsert of AGENTS/PLANS scaffolding.
---

# RLM Workflow

## Overview

Implement repository work using the canonical RLM process in `.agent/PLANS.md`, with invocation conventions from `.codex/AGENTS.md`. Treat repository artifacts as the source of truth and keep prompts as path-based commands.

## Bootstrap preflight (always run first)

Before doing anything else, ensure the repo scaffolding exists and is up to date:

- `.codex/AGENTS.md` contains the RLM Workflow block
- `.agent/PLANS.md` is upserted from `references/plans-canonical.md`
- `.codex/rlm/` exists
- Any other files created by `scripts/install-rlm-workflow.ps1` exist

If any are missing/outdated, run:

```powershell
powershell -ExecutionPolicy Bypass -File ./scripts/install-rlm-workflow.ps1 -RepoRoot .
```

If PowerShell execution isn't possible, perform an equivalent manual bootstrap:

- Create missing directories/files listed above
- Copy/upsert canonical plans from `references/plans-canonical.md` into `.agent/PLANS.md`
- Upsert the "RLM Workflow Skill" block into `.codex/AGENTS.md`

Then continue with the workflow phases.

## Read Order

1. Read `.codex/AGENTS.md` intro sections for local invocation conventions.
2. Read `.agent/PLANS.md` for canonical phase rules and requirements.
3. If AGENTS wording and PLANS wording differ, follow PLANS (AGENTS declares PLANS canonical) and note the mismatch in the current phase artifact when relevant.

## Trigger Examples

- `Implement requirement '<run-id>'`
- `Run RLM Phase 2 for .codex/rlm/<run-id>/`
- `Create .codex/rlm/<run-id>/02-to-be-plan.md with Coverage and Approval gates`
- `Update tests and lock Phase 4 artifact for this run`

## Invocation Mode

- Single-command mode:
  - On `Implement requirement '<run-id>'`, resolve run folder and execute phases sequentially.
  - Pause only for manual QA sign-off in Phase 5.
- Single-phase mode:
  - On `Run RLM Phase N`, execute only that phase and write only that phase outputs, but only when all required earlier phases are lock-valid.

## Single-Command Contract (Mandatory)

- Resolve run folder at `.codex/rlm/<run-id>/`.
- If run folder or `00-requirements.md` is missing, stop and ask for it. Do not invent requirements.
- **Auto-resume from current state:**
  - **Phase 0 (Worktree):** Check for isolated worktree. If missing or main branch, create worktree first.
  - If a phase artifact exists as `DRAFT` or with failing gates, resume that phase.
  - If a phase artifact is missing, create it for the next phase in sequence.
  - Never back-edit locked prior-phase artifacts.
- Execute in order: Phase 0 through Phase 7.
- **For Phase 0 (Worktree Isolation - REQUIRED):**
  - Check if worktree exists at `.worktrees/<run-id>` or configured location.
  - If on main/master branch: require explicit consent or auto-create worktree.
  - Verify worktree directory is git-ignored (if project-local).
  - Run project setup (npm install, cargo build, etc.).
  - Verify clean test baseline.
  - Create/lock `00-worktree.md` before proceeding.
  - **Skill:** `skills/rlm-worktree/SKILL.md`
- **For Phase 1.5 (Debug Mode - optional):**
  - Determine if requirement needs debugging (bug fixes, test failures, unexpected behavior).
  - If yes: create/lock `01.5-root-cause.md` before Phase 2.
  - Phase 1.5 uses systematic debugging (see `skills/rlm-debugging/SKILL.md`).
- For Phase 5:
  - Write `05-manual-qa.md` with scenarios in `DRAFT`.
  - Pause and request user results/sign-off.
  - On next invocation, record results, lock Phase 5, then continue to Phase 6 and 7.

## Phase Transition Guardrail (Mandatory, Hard Stop)

- Before starting Phase `N`, validate the lock chain for all prior phases (`0..N-1`) using `.agent/PLANS.md`.
- **If Phase 0 exists:** It must be lock-valid before Phase 1/2 can begin (worktree isolation verified).
- **If Phase 1.5 exists:** It must be lock-valid before Phase 2 can begin.
- A prior phase is considered lock-valid only when its base artifact and phase-local addenda are `LOCKED`, include `LockedAt` and `LockHash`, and end with `Coverage: PASS` and `Approval: PASS`.
- **Lock Verification:** Verify `LockHash` matches SHA-256 of file content. Use `scripts/verify-locks.ps1` for automated validation.
- If any prior phase is not lock-valid, do not create or update later-phase artifacts.
- Resume the earliest failing phase and repair it until lock-valid, then continue.
- Never start Phase 6 or 7 unless `05-manual-qa.md` is lock-valid.
- The only intentional pause is Manual QA in Phase 5; all other pauses are blockers.

## Main Branch Protection (Mandatory)

**The Iron Law:** NEVER WORK ON MAIN/MASTER BRANCH WITHOUT EXPLICIT CONSENT.

### Automatic Protection

When invoked from main/master branch:
1. **STOP** and display warning
2. **Default action:** Create isolated worktree
3. **Require explicit consent** to proceed on main

### Consent Requirements

If user insists on main branch work:
- Document acknowledgment of risks
- Record explicit consent with timestamp
- Note reason for exception
- **Recommendation:** Use worktrees for future requirements

### Worktree Creation (Default)

```bash
# Create feature branch worktree
git worktree add .worktrees/<run-id> -b rlm/<run-id>
cd .worktrees/<run-id>
```

All subsequent phases execute in worktree context.

## TDD Discipline (Phase 3 Mandatory)

**The Iron Law:** NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.

### RED-GREEN-REFACTOR in Phase 3

1. **RED Phase:**
   - Write minimal test showing expected behavior
   - Run test, verify it fails correctly
   - Document failure in Phase 3 artifact TDD Compliance Log

2. **GREEN Phase:**
   - Write simplest code to pass test
   - Run test, verify it passes
   - Document minimal implementation

3. **REFACTOR Phase:**
   - Clean up while staying green
   - Document cleanups

### TDD Compliance Log

Every Phase 3 artifact must include:
```markdown
## TDD Compliance Log

### R1: [description]
**Test:** `path/to/test.ts` - "[name]"
**RED:** [timestamp] - Failed as expected: [output]
**GREEN:** [timestamp] - Minimal implementation: [description]
**REFACTOR:** [timestamp] - Cleanups: [description]
```

### Red Flags - DELETE and Restart

- Code written before test → DELETE IT
- Test passes immediately → Fix the test
- "I'll add tests later" → No you won't

**Reference:** `skills/rlm-tdd/SKILL.md`

## TODO Discipline (All Phases Mandatory)

**The Iron Law:** NO LOCKING OR PHASE ADVANCEMENT WITH UNCHECKED TODOS.

### TODO Requirements

Every phase artifact MUST include a `## TODO` section with:
1. **Checkable items** for every task, sub-phase, and deliverable
2. **Progressive checkoffs** as work completes
3. **Zero unchecked items** before locking

### TODO Structure

```markdown
## TODO

- [ ] Task 1: [description]
- [ ] Task 2: [description]
  - [ ] Sub-task 2a: [description]
  - [ ] Sub-task 2b: [description]
- [ ] Task 3: [description]
```

### TODO Rules

<HG>
#### TODO Hard Gate

Do NOT lock a phase or proceed to next phase until:
- ALL TODO items are checked off ([x])
- NO unchecked items remain ([ ] or empty boxes)
- No "work in progress" or "deferred" items

**Exception:** None. Complete all todos before locking.
</HG>

### Per-Phase TODO Patterns

**Phase 0 Worktree:**
- [ ] Worktree created
- [ ] Branch protection verified
- [ ] Clean baseline confirmed
- [ ] Phase 0 worktree artifact written

**Phase 0 Requirements:**
- [ ] Requirements elicited
- [ ] Acceptance criteria defined
- [ ] Out of scope documented
- [ ] Phase 0 artifact written

**Phase 1 AS-IS:**
- [ ] Current behavior documented
- [ ] Code pointers recorded
- [ ] Known unknowns listed
- [ ] Phase 1 artifact written

**Phase 1.5 (if used):**
- [ ] Error analysis complete
- [ ] Reproduction confirmed
- [ ] Root cause identified
- [ ] Phase 1.5 artifact written

**Phase 2:**
- [ ] Sub-phases defined (if needed)
- [ ] File changes specified
- [ ] Test commands documented
- [ ] Phase 2 artifact written

**Phase 3:**
- [ ] SP1 implemented and tested
- [ ] SP2 implemented and tested
- [ ] ... (per sub-phase)
- [ ] TDD Compliance Log complete
- [ ] Phase 3 artifact written

**Phase 3.5 (if used):**
- [ ] Plan alignment verified
- [ ] Code quality assessed
- [ ] Issues categorized
- [ ] Verdict recorded
- [ ] Phase 3.5 artifact written

**Phase 4:**
- [ ] Unit tests executed
- [ ] Integration tests executed
- [ ] E2E tests executed (Tier A)
- [ ] Phase 4 artifact written

**Phase 5:**
- [ ] QA scenarios executed
- [ ] Results observed
- [ ] User sign-off recorded
- [ ] Phase 5 artifact written

### Enforcement

Before setting `Status: LOCKED`:
1. Scan artifact for any `[ ]` unchecked boxes
2. If found: complete the work OR convert to addendum
3. Verify ALL boxes are `[x]` checked
4. Only then proceed to lock

### Common Anti-Patterns

| Anti-Pattern | Correct Approach |
|--------------|------------------|
| "Will complete later" | Complete now or create addendum |
| Partial checkoff | Check only when fully complete |
| Vague items like "Do work" | Specific: "Implement auth handler" |
| No TODO section | Required in every phase artifact |

## Sequential Phase Isolation (Mandatory, No Parallel Phase Work)

- The workflow is strictly sequential: exactly one active phase per run at any time.
- Active phase = the earliest phase whose base artifact is missing or not lock-valid.
- Do not create, update, or lock artifacts for any later phase while the active phase is unresolved.
- Never keep more than one phase base artifact in `DRAFT` at the same time.
- If multiple phase artifacts are `DRAFT`, treat only the earliest `DRAFT` phase as active; later `DRAFT` artifacts are invalid parallel prework and must not be continued until the active phase is lock-valid.
- After the active phase is lock-valid, continue sequentially and recreate/overwrite any invalid later-phase `DRAFT` artifacts only when those phases become active.

## Run Folder and Artifacts

- Primary run path: `.codex/rlm/<run-id>/`
- Per-run artifacts:
  - `00-worktree.md` (REQUIRED - Phase 0 worktree setup)
  - `00-requirements.md`
  - `01-as-is.md`
  - `01.5-root-cause.md` (optional, for debug mode)
  - `02-to-be-plan.md`
  - `03-implementation-summary.md`
  - `04-test-summary.md`
  - `05-manual-qa.md`
  - `addenda/`
- Global artifacts:
  - `.codex/DECISIONS.md`
  - `.codex/STATE.md`
- Worktree location (isolated):
  - `.worktrees/<run-id>/` (default, project-local, hidden)
  - Or `~/.config/rlm-workflow/worktrees/<project>/<run-id>/` (global)
- Skills (for reference):
  - `skills/rlm-worktree/SKILL.md` - Phase 0 worktree isolation
  - `skills/rlm-tdd/SKILL.md` - TDD discipline for Phase 3
  - `skills/rlm-debugging/SKILL.md` - Systematic debugging for Phase 1.5
  - `references/rationalizations.md` - Common excuse/reality tables
- Scripts (utilities):
  - `scripts/verify-locks.ps1` - Automated lock hash verification

## Phase Execution Protocol

1. Identify phase input base files from `.agent/PLANS.md`.
2. Expand each input to effective input: base file plus stage-local addenda in lexical order.
3. Read all effective inputs before drafting output.
4. Create/update the phase artifact with required header fields:
   - `Run`, `Phase`, `Status`, `Inputs`, `Outputs`, `Scope note`
5. Include a `Traceability` section mapping each `R#` to where it is addressed and evidenced.
6. End with `Coverage Gate` and `Approval Gate`, each concluding with explicit `PASS` or `FAIL`.
7. Keep `Status: DRAFT` until both gates pass.
8. On pass, lock artifact:
   - Set `Status: LOCKED`
   - Add `LockedAt` (ISO8601)
   - Add `LockHash` (SHA-256 of the file content)

Use `references/artifact-template.md` for exact header and gate scaffolding.

## Mandatory PLANS Sections to Enforce

Always enforce these sections from `.agent/PLANS.md` when applicable:

- `Large requirements: Implementation sub-phases (required when scope is large or risky)`
- `Playwright tagging for RLM runs and implementation sub-phases (required)`
- `Testing discipline (TDD + Playwright)` sections for Phase 2, 4, and 5
- **- `RLM TDD Discipline (Phase 3)` - RED-GREEN-REFACTOR cycle, The Iron Law**
- **- `RLM Systematic Debugging (Phase 1.5)` - When and how to use debug mode**
- **- `RLM Rationalization Awareness` - Common traps and how to avoid them**
- `RLM single-command orchestration ("Implement requirement '<run-id>'")`
- `Run folder resolution`
- `Phase auto-resume and phase selection`
- `Phase transition hard-stop lock chain (required)`
- `Strict sequential phase execution (no parallel phase work)`
- `Manual QA stop (the only intentional pause)`
- `Locking rules for single-command execution`

## Immutability and Addenda

- Never edit a locked prior-phase artifact.
- If a gap is discovered in a locked upstream artifact, create an upstream-gap addendum in the current phase.
- Addendum naming:
  - Stage-local: `<base>.addendum-01.md`
  - Upstream-gap: `<current>.upstream-gap.<prior>.addendum-01.md`
- Lock all addenda created in the active phase when that phase locks.

## Phase Expectations

0. **Phase 0 (`00-worktree.md`) - Isolation REQUIRED**
   - **Trigger:** At start of every RLM run, before any other work.
   - **The Iron Law:** NEVER WORK ON MAIN/MASTER BRANCH WITHOUT EXPLICIT CONSENT.
   - Create isolated git worktree at `.worktrees/<run-id>/` (or configured location).
   - Verify worktree directory is git-ignored (if project-local).
   - Run project setup (auto-detect: npm install, cargo build, pip install, etc.).
   - Verify clean test baseline (all tests passing).
   - Document worktree location, branch name, baseline status.
   - **Skill:** `skills/rlm-worktree/SKILL.md`

1. Phase 0 Requirements (`00-requirements.md`)
   - Define stable IDs `R1..Rn` and `OOS1..OOSn`.
   - Define observable acceptance criteria for each `R#`.
   - User-created first to initialize the run.

2. Phase 1 AS-IS (`01-as-is.md`)
   - Provide novice-runnable repro, current behavior, code pointers, known unknowns.
   - Execute in worktree context.

3. **Phase 1.5 (`01.5-root-cause.md`) - Debug Mode (optional)**
   - **Trigger:** Use when requirement involves fixing a bug or investigating unexpected behavior.
   - **The Iron Law:** NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.
   - Follow systematic debugging: error analysis → reproduction → data flow tracing → hypothesis testing → root cause summary.
   - Must be LOCKED before Phase 2 when present.
   - **Skill:** `skills/rlm-debugging/SKILL.md`

4. Phase 2 (`02-to-be-plan.md`)
   - Produce ExecPlan-grade plan with concrete file edits, commands, tests, manual QA scenarios.
   - Add implementation sub-phases (`SP1`, `SP2`, ...) when scope/risk is large.
   - If Phase 1.5 exists: incorporate root cause findings into fix plan.

5. Phase 3 (`03-implementation-summary.md`) - **TDD Discipline + Parallelization**
   - **The Iron Law:** NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.
   - Must include TDD Compliance Log documenting RED-GREEN-REFACTOR cycles.
   - **Parallel Mode (Subagent):** If 3+ independent sub-phases and subagent spawning available:
     - Dispatch fresh subagent per sub-phase
     - Two-stage review: spec compliance → code quality
     - Review loops until approved
     - Integration testing after all sub-phases complete
   - **Sequential Mode (Fallback):** If subagents unavailable:
     - Execute sub-phases sequentially in main agent
     - Extended self-review checklist
     - Integration testing between each sub-phase
   - **Skill:** `skills/rlm-tdd/SKILL.md` for TDD, `skills/rlm-subagent/SKILL.md` for parallelization

6. **Phase 3.5 (`03.5-code-review.md`) - Code Review (optional)**
   - **Trigger:** Large changes, critical paths, or extra confidence needed
   - **When to use:** High-risk changes, complex sub-phases, or when external validation is needed
   - **Parallel Mode:** Dispatch `code-reviewer` subagent
   - **Sequential Mode:** Main agent self-review with extended checklist
   - Must be LOCKED before Phase 4 if used
   - **Skill:** `skills/rlm-subagent/SKILL.md`

7. Phase 4 (`04-test-summary.md`) - **Parallel Testing**
   - Record concrete validation commands, results, and requirement coverage.
   - Verify TDD compliance: all tests passing that were written in Phase 3.
   - **Parallel Mode:** Dispatch subagents for independent test suites:
     - Subagent 1: Unit tests
     - Subagent 2: Integration tests  
     - Subagent 3: E2E Tier A
     - All run concurrently, results aggregated
   - **Sequential Mode:** Run test suites sequentially in main agent

8. Phase 5 (`05-manual-qa.md`)
   - Pause for user sign-off; record observed outcomes and explicit approval.

9. Phase 6 and 7
   - Update `.codex/DECISIONS.md`, then `.codex/STATE.md`.
   - Changes are in worktree context; user merges feature branch when ready.

## RLM Skill Priority

When a requirement involves multiple concerns, use this priority order to determine which skills/phases to apply first:

### Priority Order

1. **Debugging** (bug fixes) → Run Phase 1.5 Root Cause Analysis first
   - **Trigger:** Requirement mentions bug, test failure, or unexpected behavior
   - **Action:** Insert Phase 1.5 between Phase 1 and Phase 2
   - **Skill:** `skills/rlm-debugging/SKILL.md`
   - **Why:** Understanding root cause is prerequisite to planning the fix

2. **Design/Analysis** (new features or changes) → Run full Phase 1 AS-IS Analysis
   - **Trigger:** New feature, enhancement, or behavior modification
   - **Action:** Execute Phase 1 thoroughly before Phase 2
   - **Why:** Must understand current state before defining future state

3. **Implementation** → Proceed to Phase 2+ after analysis complete
   - **Trigger:** Phase 1 (or 1.5) is locked and ready
   - **Action:** Begin Phase 2 (TO-BE planning)
   - **Why:** Plans require complete understanding of current/debugging state

4. **Testing** → Use TDD discipline in Phase 3
   - **Trigger:** Any implementation work
   - **Action:** Apply TDD in Phase 3
   - **Skill:** `skills/rlm-tdd/SKILL.md`
   - **Why:** Tests validate implementation against requirements

5. **Review** → Code review between implementation and final validation
   - **Trigger:** Implementation complete (Phase 3 locked)
   - **Action:** Optional Phase 3.5 Code Review before Phase 4
   - **Why:** Catch issues before final validation

### Decision Flow

```
Requirement received
        │
        ▼
Is it a bug fix? ──YES──► Phase 1.5 (Root Cause Analysis)
        │                      ▼
        NO              Phase 2 (incorporate findings)
        │                      ▼
        ▼              Phase 3 (TDD implementation)
Phase 1 (AS-IS)              ▼
        │              Phase 4 (validation)
        ▼                      ▼
Phase 2 (TO-BE)         Phase 5 (Manual QA)
        │                      ▼
        ▼              Phase 6/7 (global updates)
Phase 3 (TDD)
        │
        ▼
    [etc]
```

### Examples

| Requirement | Priority Applied | Execution Order | Execution Mode |
|-------------|------------------|-----------------|----------------|
| "Fix login crash" | Debugging first | Phase 0 → 1 → **1.5** → 2 → 3 → 4 → 5... | Sequential or Parallel |
| "Add dark mode" | Design first | Phase 0 → **1** → 2 → 3 → 4 → 5... | Sequential (single SP) |
| "Crash on empty input" | Debugging first | Phase 0 → 1 → **1.5** → 2 → 3 → 4... | Sequential or Parallel |
| "Implement OAuth" | Design + Review | Phase 0 → 1 → 2 → 3 → **3.5** → 4 → 5... | Parallel (multiple SPs) |
| "Multi-domain refactor" | Design + Parallel | Phase 0 → 1 → 2 → **3** → **3.5** → 4 → 5... | Parallel (subagents) |

**Execution Mode Legend:**
- **Sequential:** Single sub-phase, no parallelism needed
- **Parallel:** Multiple sub-phases, subagents available → concurrent execution
- **Sequential or Parallel:** Mode determined by subagent availability check

## Hard Gates

Hard gates are non-negotiable checkpoints that MUST be satisfied before proceeding. They prevent rationalization and corner-cutting.

<HG>
### Phase 0 → 1/2 Hard Gate

Do NOT proceed to Phase 1 or 2 until:
- Phase 0 worktree is created and verified
- Worktree directory is git-ignored (if project-local)
- Clean test baseline is verified
- Main branch protection is confirmed
- Phase 0 artifact is LOCKED with LockedAt and LockHash

**Exception:** None. Phase 0 is REQUIRED for all runs.
</HG>

<HG>
### Phase 1 → 3 Hard Gate

Do NOT create 02-to-be-plan.md until 01-as-is.md is LOCKED with:
- Coverage: PASS
- Approval: PASS
- LockedAt and LockHash populated

**Exception:** If Phase 1.5 exists, it must ALSO be locked before Phase 2.
</HG>

<HG>
### Phase 1.5 → 3 Hard Gate (Debug Mode)

Do NOT create TO-BE plan until root cause analysis is complete:
- Phase 1.5 artifact is LOCKED
- Root cause identified (not just symptoms)
- Fix strategy defined
- Coverage: PASS
- Approval: PASS

**Exception:** None. Debug mode requires completion before planning.
</HG>

<HG>
### Phase 3 TDD Hard Gate

Do NOT write implementation code until:
- Failing test exists and has been run
- Test failure is documented in Phase 3 artifact TDD Compliance Log
- RED phase is verified with actual test output

**Exception:** None. The Iron Law has no exceptions.
</HG>

<HG>
### Phase 4 → 6 Hard Gate

Do NOT proceed to Manual QA until:
- All tests from Phase 3 are passing
- TDD Compliance is verified
- Test evidence is documented in Phase 4 artifact
- Phase 4 is LOCKED
</HG>

<HG>
### Phase 5 Manual QA Hard Gate

Do NOT update DECISIONS.md or STATE.md until:
- User has explicitly signed off on QA scenarios
- 05-manual-qa.md contains observed results for all scenarios
- Approval: PASS with user name/date recorded
- Phase 5 is LOCKED with LockHash matching content

**Exception:** None. Global updates require QA completion.
</HG>

<HG>
### Lock Chain Hard Gate (Applies to ALL transitions)

Do NOT start Phase N unless ALL prior phases (0 through N-1) are lock-valid:
- Status: LOCKED
- LockedAt: populated
- LockHash: matches SHA-256 of content
- Coverage: PASS
- Approval: PASS

**Exception:** None. The lock chain is absolute.
</HG>

## Execution Modes: Parallel vs Sequential

RLM supports two execution modes for Phase 3 (Implementation) and Phase 4 (Testing):

### Parallel Mode (Subagent-Driven)

**Requirements:**
- Subagent spawning capability available
- 3+ independent sub-phases defined
- Sub-phases don't share files or have minimal dependencies

**Benefits:**
- 3-5x faster execution for multiple sub-phases
- Fresh context per sub-phase (no confusion)
- Independent review by separate subagents
- Natural TDD enforcement

**Process:**
1. Controller extracts all sub-phases from Phase 2 plan
2. Dispatches implementer subagent per sub-phase (parallel)
3. Each implementer: implements, tests, commits
4. Dispatches spec reviewer per sub-phase (parallel)
5. Dispatches code reviewer per sub-phase (parallel, after spec passes)
6. Review loops if issues found
7. Integration testing after all approved

**Documentation:** Mode and subagent usage recorded in Phase 3 artifact

### Sequential Mode (Fallback)

**Trigger:**
- Subagent spawning not available in current environment
- User explicitly requests sequential execution
- Subagent capability check fails

**Characteristics:**
- Sub-phases executed sequentially in main agent
- Extended self-review checklist
- Integration testing between each sub-phase
- Slower but equally rigorous

**Fallback trigger flow:**
```markdown
**Subagent Check:** ❌ NOT AVAILABLE
**Reason:** [Tool not found / Platform limitation / User request]
**Action:** Using SEQUENTIAL fallback mode
```

### Mode Detection

**Automatic detection at start of Phase 3:**
1. Attempt to determine subagent capability
2. If available → Use PARALLEL mode
3. If unavailable → Use SEQUENTIAL mode with explicit documentation

**Platform-specific detection:**
- **Claude Code:** Check for `Task` tool
- **Codex:** Check native subagent support
- **OpenCode:** Check `skill` tool capabilities
- **Cursor:** Limited subagent support → usually sequential

### User Override

User can explicitly request mode:
```
"Implement requirement 'X' using parallel subagents"
→ Attempt parallel, fallback if unavailable

"Implement requirement 'X' with sequential execution"
→ Force sequential even if subagents available
```

### Mode Comparison

| Aspect | Parallel Mode | Sequential Mode |
|--------|---------------|-----------------|
| Execution | Concurrent subagents | Sequential in main agent |
| Speed | 3-5x faster | Linear |
| Review | Independent subagent reviewers | Self-review |
| Context | Fresh per sub-phase | Accumulates |
| Rigor | Two-stage external review | Extended self-review |
| Fallback | Automatic if unavailable | Default mode |

### Maintaining Quality in Both Modes

**Parallel Mode Quality:**
- Two-stage review (spec + code quality)
- Independent verification
- Review loops for fixes

**Sequential Mode Quality:**
- Extended self-review checklist
- Explicit verification steps
- Regression testing between sub-phases

**Both modes enforce:**
- TDD discipline
- Artifact locking
- Gate compliance
- Integration testing

## Manual QA Pause Rule

Pause only during Phase 5 for explicit user validation/sign-off. Do not pause for approval in other phases when gates can be evaluated mechanically.

## Operating Rules

- Keep prompts short and path-based; keep substantive requirements and plans in repo documents.
- Use deterministic, reproducible commands for implementation and validation.
- If required input is missing, create the minimal current-phase addendum; do not back-edit locked history.

## Rationalization Awareness

When you find yourself thinking "this time is different" or "I can skip this step," **you are rationalizing**.

**Common traps:**
- "This requirement is simple" → Simple is where assumptions cause the most wasted work
- "I already know how it works" → You know how you THINK it works. Verify with evidence.
- "I'll document it later" → Later never comes. Document now.
- "TDD is overkill for this fix" → Simple code breaks. The Iron Law has no exceptions.

**Reference:** `references/rationalizations.md` for comprehensive excuse/reality tables.

**Violating the letter of the process is violating the spirit of quality.**
