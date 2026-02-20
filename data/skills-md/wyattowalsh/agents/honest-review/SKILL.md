---
name: honest-review
description: >-
  Research-driven code review at multiple abstraction levels with strengths
  acknowledgment, creative review lenses, AI code smell detection, and
  severity calibration by project type. Two modes: (1) Session review —
  review and verify changes using parallel reviewers that research-validate
  every assumption; (2) Full codebase audit — deep end-to-end evaluation
  using parallel teams of subagent-spawning reviewers. Use when reviewing
  changes, verifying work quality, auditing a codebase, validating
  correctness, checking assumptions, finding defects, reducing complexity.
  NOT for writing new code, explaining code, or benchmarking.
license: MIT
metadata:
  author: wyattowalsh
  version: "3.0"
---

# Honest Review

Research-driven code review. Every finding validated with evidence.
4-wave pipeline: Triage → Analysis → Research → Judge.

## Dispatch

| $ARGUMENTS | Mode |
|------------|------|
| Empty + changes in session (git diff) | Session review of changed files |
| Empty + no changes (first message) | Full codebase audit |
| File or directory path | Scoped review of that path |
| "audit" | Force full codebase audit |
| PR number/URL | Review PR changes (gh pr diff) |
| Git range (HEAD~3..HEAD) | Review changes in that range |

## Review Posture

**Severity calibration by project type**:
- Prototype: report P0/S0 only. Skip style, structure, and optimization concerns.
- Production: full review at all levels and severities.
- Library: full review plus backward compatibility focus on public API surfaces.

**Confidence-calibrated reporting**:
Every finding carries a confidence score (0.0-1.0). Confidence ≥ 0.7: report.
Confidence 0.3-0.7: report as "unconfirmed". Confidence < 0.3: discard (except P0/S0).
Rubric: references/research-playbook.md § Confidence Scoring Rubric.

**Strengths acknowledgment**:
Call out well-engineered patterns, clean abstractions, and thoughtful design.
Minimum one strength per review scope. Strengths are findings too.

**Positive-to-constructive ratio**:
Target 3:1. Avoid purely negative reports. If the ratio skews negative,
re-examine whether low-severity findings are worth reporting.

**Convention-respecting stance**:
Review against the codebase's own standards, not an ideal standard.

**Healthy codebase acknowledgment**:
If no P0/P1 or S0 findings: state this explicitly. A short report is a good report.

## Review Levels (Both Modes)

Three abstraction levels, each examining defects and unnecessary complexity:

**Correctness** (does it work?):
Error handling, boundary conditions, security, API misuse, concurrency, resource leaks.
Simplify: phantom error handling, defensive checks for impossible states, dead error paths.

**Design** (is it well-built?):
Abstraction quality, coupling, cohesion, test quality, cognitive complexity.
Simplify: dead code, 1:1 wrappers, single-use abstractions, over-engineering.

**Efficiency** (is it economical?):
Algorithmic complexity, N+1, data structure choice, resource usage, caching.
Simplify: unnecessary serialization, redundant computation, premature optimization.

Context-dependent triggers (apply when relevant):
- Security: auth, payments, user data, file I/O, network
- Observability: services, APIs, long-running processes
- AI code smells: LLM-generated code, unfamiliar dependencies
- Config and secrets: environment config, credentials, .env files
- Resilience: distributed systems, external dependencies, queues
- i18n and accessibility: user-facing UI, localized content
- Data migration: schema changes, data transformations
- Backward compatibility: public APIs, libraries, shared contracts
- Requirements validation: changes against stated intent, PR description, ticket
Full checklists: read references/checklists.md

## Creative Lenses

Apply at least 2 lenses per review scope. For security-sensitive code, Adversary is mandatory.

- **Inversion**: assume the code is wrong — what would break first?
- **Deletion**: remove each unit — does anything else notice?
- **Newcomer**: read as a first-time contributor — where do you get lost?
- **Incident**: imagine a 3 AM page — what path led here?
- **Evolution**: fast-forward 6 months of feature growth — what becomes brittle?
- **Adversary**: what would an attacker do with this code?

Reference: read references/review-lenses.md

## Research Validation

THIS IS THE CORE DIFFERENTIATOR. Do not report findings based solely
on LLM knowledge. For every non-trivial finding, validate with research:

**Two-phase review per scope**:
1. **Flag phase**: Analyze code, generate hypotheses
2. **Validate phase**: Spawn research subagents to confirm with evidence:
   - Context7: library docs for API correctness
   - WebSearch: best practices, security advisories
   - WebFetch: package registries (npm, PyPI, crates.io)
   - gh: open issues, security advisories
3. Assign confidence score (0.0-1.0) per Confidence Scoring Rubric
4. Only report findings with evidence. Cite sources.

Research playbook: read references/research-playbook.md

## Mode 1: Session Review

### Step 1: Triage (Wave 0)

Run `git diff --name-only HEAD` to capture changes. Collect `git diff HEAD` for context.
Identify task intent from session history.

For 6+ files: run triage per references/triage-protocol.md:
- `uv run scripts/project-scanner.py [path]` for project profile
- Git history analysis (hot files, blame density, recent changes)
- Risk-stratify all changed files (HIGH/MEDIUM/LOW)
- Determine specialist triggers (security, observability, requirements)

For 1-5 files: lightweight triage — classify risk levels, skip full scanning.

### Step 2: Scale and Launch (Wave 1)

| Scope | Strategy |
|-------|----------|
| 1-2 files | Inline review at all 3 levels. Spawn research subagents for flags. |
| 3-5 files | 3 parallel level-based reviewers (Correctness/Design/Efficiency). Each runs internal waves A→B→C. |
| 6+ files | Team with lead. See below. |

**Team structure for 6+ files:**

```
[Lead: triage (Wave 0), Judge reconciliation (Wave 3), final report]
  |-- Correctness Reviewer → Waves A/B/C internally
  |-- Design Reviewer → Waves A/B/C internally
  |-- Efficiency Reviewer → Waves A/B/C internally
  |-- [Security Specialist if triage triggers]
  |-- [Observability Specialist if triage triggers]
  |-- [Requirements Validator if intent available]
```

Each reviewer runs 3 internal waves (references/team-templates.md § Internal Wave Structure):
- Wave A: quick scan all files (haiku, 3-5 files per subagent)
- Wave B: deep dive HIGH-risk flagged files (opus, 1 per file)
- Wave C: research validate findings (batched per research-playbook.md)

Prompt templates: read references/team-templates.md

### Step 3: Research Validate (Wave 2)

For inline/small reviews: lead collects all findings and dispatches validation wave.
For team reviews: each teammate handles validation internally (Wave C).

Batch findings by validation type. Dispatch order:
1. Slopsquatting detection (security-critical, haiku)
2. HIGH-risk findings (2+ sources, sonnet)
3. MEDIUM-risk findings (1 source, haiku/sonnet)
4. Skip LOW-risk obvious issues

Batch sizing: 5-8 findings per subagent (optimal). See references/research-playbook.md § Batch Optimization.

### Step 4: Judge Reconcile (Wave 3)

Run the 8-step Judge protocol (references/judge-protocol.md):
1. Normalize findings (scripts/finding-formatter.py assigns HR-S-{seq} IDs)
2. Cluster by root cause
3. Deduplicate within clusters
4. Confidence filter (≥0.7 report, 0.3-0.7 unconfirmed, <0.3 discard)
5. Resolve conflicts between contradicting findings
6. Check interactions (fixing A worsens B? fixing A fixes B?)
7. Elevate patterns in 3+ files to systemic findings
8. Rank by score = severity_weight × confidence × blast_radius

### Step 5: Present and Execute

Present all findings with evidence, confidence scores, and citations.
Ask: "Implement fixes? [all / select / skip]"
If approved: parallel subagents by file (no overlapping ownership).
Then verify: build/lint, tests, behavior spot-check.
Output format: read references/output-formats.md

## Mode 2: Full Codebase Audit

### Step 1: Triage (Wave 0)

Full triage per references/triage-protocol.md:
- `uv run scripts/project-scanner.py [path]` for project profile
- Git history analysis (4 parallel haiku subagents: hot files, blame density, recent changes, related issues)
- Risk-stratify all files (HIGH/MEDIUM/LOW)
- Context assembly (project type, architecture, test coverage, PR history)
- Determine specialist triggers for team composition

For 500+ files: prioritize HIGH-risk, recently modified, entry points, public API.
State scope limits in report.

### Step 2: Design and Launch Team (Wave 1)

Use triage results to select team archetype (references/team-templates.md § Full Audit Team Archetypes).
Assign file ownership based on risk stratification — HIGH-risk files get domain reviewer + specialist coverage.

```
[Lead: triage (Wave 0), cross-domain analysis, Judge reconciliation (Wave 3), report]
  |-- Domain A Reviewer → Waves A/B/C internally
  |-- Domain B Reviewer → Waves A/B/C internally
  |-- Domain C Reviewer → Waves A/B/C internally
  |-- Security Specialist (cross-cutting, all HIGH-risk files)
  |-- [Observability Specialist for production services]
  |-- [Requirements Validator if spec/ticket available]
```

Each teammate runs 3 internal waves (references/team-templates.md § Internal Wave Structure).
Scaling: references/team-templates.md § Scaling Matrix.

### Step 3: Cross-Domain Analysis (Lead, parallel with Wave 1)

While teammates review, lead spawns parallel subagents for:
- Architecture: module boundaries, dependency graph
- Data flow: trace key paths end-to-end
- Error propagation: consistency across system
- Shared patterns: duplication vs. necessary abstraction

### Step 4: Research Validate (Wave 2)

Each teammate handles research validation internally (Wave C).
Lead validates cross-domain findings separately.
Batch optimization: references/research-playbook.md § Batch Optimization.

### Step 5: Judge Reconcile (Wave 3)

Collect all findings from all teammates + cross-domain analysis.
Run the 8-step Judge protocol (references/judge-protocol.md).
Cross-domain deduplication: findings spanning multiple domains → elevate to systemic.

### Step 6: Report

Output format: read references/output-formats.md
Required sections: Critical, Significant, Cross-Domain, Health Summary,
Top 3 Recommendations, Statistics. All findings include evidence + citations.

### Step 7: Execute (If Approved)

Ask: "Implement fixes? [all / select / skip]"
If approved: parallel subagents by file (no overlapping ownership).
Then verify: build/lint, tests, behavior spot-check.

## Reference Files

| File | When to Read |
|------|--------------|
| references/triage-protocol.md | During Wave 0 triage (both modes) |
| references/checklists.md | During analysis or building teammate prompts |
| references/research-playbook.md | When setting up research validation (Wave 2) |
| references/judge-protocol.md | During Judge reconciliation (Wave 3) |
| references/output-formats.md | When producing final output |
| references/team-templates.md | When designing teams (Mode 2 or large Mode 1) |
| references/review-lenses.md | When applying creative review lenses |

| Script | When to Run |
|--------|-------------|
| scripts/project-scanner.py | Wave 0 triage — deterministic project profiling |
| scripts/finding-formatter.py | Wave 3 Judge — normalize findings to structured JSON |

## Critical Rules

- Never skip triage (Wave 0) — risk classification informs everything downstream
- Every non-trivial finding must have research evidence or be discarded
- Confidence < 0.3 = discard (except P0/S0 — report as unconfirmed)
- Do not police style — follow the codebase's conventions
- Do not report phantom bugs requiring impossible conditions
- More than 15 findings means re-prioritize — 5 validated findings beat 50 speculative
- Never skip Judge reconciliation (Wave 3)
- Always present before implementing (approval gate)
- Always verify after implementing (build, tests, behavior)
- Never assign overlapping file ownership
