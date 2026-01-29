---
name: repo-scan-2-jira
description: Scan a repo scope for actionable work items (bugs, TODO/FIXME, doc inconsistencies, performance/maintainability risks) and emit Jira-ready issues in a strict JSON schema. Use when asked to scan a specific module/path/page/route and produce evidence-backed Jira tickets.
---

# Repo Scan 2 Jira

## Overview
Generate Jira-ready issues from a constrained scope in this monorepo. Operate on evidence only and emit JSON that matches schema.json.

## Non-negotiable Rules
- Obey scope strictly: scan only target.paths and the specified module.
- Require evidence for every issue: file:line plus snippet or log excerpt.
- Make issues executable: include what/why/how, acceptance criteria, and definition of done.
- No speculative tickets. If reproduction is missing, create a Task to add repro/logging/tests.
- Output JSON only; match schema.json exactly.
- Use stable dedupeKey values across runs.

## Arguments Contract
Use a structured Args block.

Required fields:
- target.module: docs | frontend | backend | prototype | cross
- target.paths: array of glob-ish paths (scope boundary)
- target.keywords: optional array of strings
- target.routes_or_pages: optional array of strings
- focus.issue_types: array of Bug | Task | Improvement
- focus.signals: array of TODO, FIXME, bug, doc_inconsistency, perf, lint, test_failures
- focus.depth: quick | standard | deep
- jira.project_key, jira.component, jira.labels_prefix; optional jira.epic_key
- output.format: json (required), optional markdown_report
- output.max_issues, output.min_confidence
- loop (optional): { mode: ralph, stop_condition: no_new_issues_in_scope | max_iterations, iteration_budget: number }

If target.paths is empty, stop and request scope.

## Workflow
1. Validate Args and scope. Refuse to scan outside target.paths.
2. Collect signals inside scope only.
   - Use scripts/collect-signals.sh for TODO/FIXME/BUG/PERF markers and keyword hits.
   - If lint/test logs are provided, extract failures as evidence.
3. Correlate signals into distinct issues and dedupe aggressively.
4. For each issue, include evidence, reproduction (when applicable), acceptance criteria, and DoD.
5. Compute stable dedupeKey values. Preferred format:
   component:path:line:hash
   - Hash should be stable across runs (example: sha1 of component|path|line|summary).
6. Emit JSON only, matching schema.json.

## Ralph Loop Mode
When loop.mode is ralph:
1. Run a fresh scan for the same scope.
2. Generate issues and compute dedupeKey values.
3. Compare with prior output stored at .repo-scan-2-jira/last.json.
4. Stop when no new dedupeKeys appear or iteration_budget is reached.
5. Persist the latest output to .repo-scan-2-jira/last.json.

## Output Schema
Follow schema.json exactly. Do not emit any extra keys or prose.

## Prompt Template
Use prompts/invoke.txt as the wrapper prompt. Only edit the Args block.

## Scripts
- scripts/collect-signals.sh: scoped ripgrep for TODO/FIXME/BUG/PERF/keywords, optional log parsing.
- scripts/dedupe.js: fill missing dedupeKey values and optionally filter out issues found in a prior run.
- scripts/jira-bulk-payload.js: convert output JSON to Jira bulk issue payload.
