---
name: agent-orchestrator
description: Coordinate complex work using a phase-gated, multi-agent engineering loop (audit → design → implement → review → validate → deliver). Use when you need to split a task into subsystems, run dual independent audits, reconcile findings into a confirmed issue list, delegate fixes in clusters, enforce dual-review PASS gates, and drive an end-to-end delivery. Prefer discovering and invoking other specialized skills when they can execute part of the work faster or more reliably.
---

# Agent Orchestrator

## Overview

Run a disciplined multi-agent workflow where this instance acts as the coordinator: it delegates audits and fixes to other agents, reconciles results, enforces quality gates, and drives the work to a usable, validated end state.

Core pattern: dispatch a fresh implementer per cluster, then run two-stage review (spec compliance first, then code quality).

## Workflow (Coordinator)

1. Discover and use other skills (when helpful)
   - Check the harness-provided skill list (typically present in system context). If a relevant specialized skill exists, explicitly invoke it (e.g., `$some-skill`) and follow its workflow instead of reinventing it.
   - Use other skills to: fetch external info safely, generate boilerplate reliably, apply framework-specific conventions, or handle fragile formats (docs/PDFs, CI config, release workflows).
   - Keep skill usage intentional: choose the minimal set, state which skills you’re using and why, and avoid duplicating their instructions inside this skill.

2. Freeze scope + success criteria
   - Restate the mission, constraints, and “done” criteria in concrete terms.
   - Identify any authoritative sources (docs/specs) and record what claims must be backed by evidence.

3. Create a phase plan and keep it current
   - Use your environment’s planning mechanism (e.g., `update_plan` if available) to track phases and prevent drifting.
   - Prefer 4–7 steps; keep exactly one step `in_progress`.

4. Decompose into subsystems
   - Choose subsystems that can be audited independently (API surface, core logic, error handling, perf, integrations, tests, docs).
   - For each subsystem, define 2–5 invariants (what must always be true).

5. Run dual independent audits per subsystem
   - Spawn two independent audits per subsystem (auditA and auditB) and keep them independent until reconciliation.
   - Require evidence for every issue (repo location, deterministic repro, expected vs actual, severity).

6. Reconcile audits into a single confirmed issue list
   - Compare auditA vs auditB outputs and keep only mutually confirmed issues.
   - Track rejected candidates with a brief reason (weak evidence, out of scope, non-deterministic).
   - Use this reconciled list as the only input to implementation.

7. Implement in clusters with clear ownership
   - Group confirmed issues into clusters that can be fixed with minimal coupling.
   - Spawn exactly one fixer per cluster; fixers should “own” a file set and avoid broad refactors.
   - Every fix must come with a regression test (unit/integration/e2e as appropriate).
   - For each cluster, run a two-stage review loop:
     - Implementer completes the cluster (tests, self-review, commit) and reports what changed.
     - Spec compliance reviewer validates “nothing more, nothing less” by reading code (do not trust the report).
     - Code quality reviewer validates maintainability and test quality (only after spec compliance passes).
     - If any review FAILs, send concrete feedback back to the implementer and repeat the failed review stage.

8. Enforce review gates
   - Do not merge/land a cluster unless spec compliance PASS and code quality PASS are both recorded with concrete references.

9. Integrate + validate
   - Run the repo’s standard validations (tests, lint, build, typecheck).
   - If the repo has no clear commands, discover them from `README`, `package.json`, `pyproject.toml`, CI config, etc.

10. Deliver a concise completion report
   - What is usable now.
   - What remains intentionally unsupported (with next steps/issues).
   - Commands executed (at least the key validation commands) and results.

## Agent Prompt Templates

Use these as starting points; keep subsystem- and repo-specific details in the message you send.

### Auditor (per subsystem)

Task:
- Audit the `<SUBSYSTEM>` subsystem independently.
- Do not propose fixes yet; identify issues only.
- If a specialized skill is relevant to the subsystem, invoke it and follow its audit/checklist guidance.

Output (bullet list):
- issue title
- severity: critical/high/medium/low
- evidence: repo file + symbol (and line if stable)
- deterministic repro (commands/steps) or reasoning for why repro is not needed
- expected vs actual
- violated invariant (if known) or propose a new invariant

### Reconciler (coordinator task)

Task:
- Compare auditA vs auditB for `<SUBSYSTEM>`.
- Produce a single decision set: confirmed issues (mutual) + rejected candidates (with reason).

Output:
- Confirmed issues (only mutual)
- Rejected candidates (reason)
- Consensus achieved: YES/NO

### Implementer (per cluster)

Task:
- Implement cluster `<CLUSTER_ID>` derived from confirmed issues.
- Work from a fresh context: do not assume prior clusters’ details unless provided.
- Do not open plan files unless explicitly instructed; the coordinator should paste the full cluster/task text and context here.
- Ask questions before you start if anything is unclear.
- Stay within agreed owned files; avoid opportunistic refactors.
- Add/adjust regression tests for every change.
- Run relevant validations (targeted tests first, then broader if appropriate).
- Commit your work (unless the repo workflow forbids local commits).
- Invoke specialized skills when they reduce risk (framework conventions, CI/test harness setup, format-sensitive edits).

Output:
- changed files (paths)
- commands executed + results
- brief behavior change summary
- tests added/updated

### Spec Compliance Reviewer (per cluster)

Task:
- Verify the implementation matches the cluster’s requirements: nothing missing, nothing extra.
- Do not trust the implementer’s report; verify by reading the actual code.
- Call out missing requirements, extra features, or misunderstandings with concrete file references.

Output:
- PASS/FAIL
- missing requirements (if any) with concrete references
- extra/unneeded work (if any) with concrete references

### Code Quality Reviewer (per cluster)

Task:
- Review cluster `<CLUSTER_ID>` changes for maintainability, test quality, and adherence to existing patterns.
- Only run after spec compliance PASS.
- Run the cluster’s relevant tests/commands (or explain what prevented running them).
- Confirm any invoked specialized skills were followed (or explicitly explain deviations).

Output:
- PASS/FAIL
- concrete references (files/symbols)
- any invariant violations or missing tests
