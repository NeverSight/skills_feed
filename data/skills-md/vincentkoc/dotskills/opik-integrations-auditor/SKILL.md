---
name: opik-integrations-auditor
description: Audit, compare, and document Opik integrations across Python SDK, TypeScript SDK, and OTEL/API backend. Use when adding a new integration, reviewing an existing one, or generating first-pass integration docs and gap analysis.
metadata:
  internal: true
---

# Opik Integrations Auditor

## Purpose

Audit, compare, and document Opik integrations across Python, TypeScript, and backend OTEL/API surfaces with a repeatable evidence-first workflow.

## When to use

Use this skill when the task involves:

- reviewing existing Opik integrations for behavior, coverage, or documentation quality
- designing or implementing a new integration
- producing integration pattern docs across Python, TypeScript, and OTEL/API
- identifying gaps between code, tests, and docs

## Required outputs

Produce these artifacts in the response (or files if asked):

1. Integration inventory table
2. Pattern classification per integration
3. Cross-surface comparison matrix (Python / TypeScript / OTEL/API)
4. Findings list (bugs/risks/gaps)
5. Documentation patch plan
6. Test plan (unit + integration + e2e)

## Workflow

1. Build inventory and classify pattern per integration.
2. Extract behavior contract (capture, streaming, errors, flush, span hierarchy).
3. Extract data contract (usage, metadata/tags, thread propagation).
4. Validate backend compatibility (OTEL endpoint/protocol/mapping rules).
5. Review tests for coverage and missing edge cases.
6. Produce documentation updates with consistent template.

## Load references as needed

- For matrix schema and scoring: `references/matrix-and-rubric.md`
- For pattern definitions: `references/patterns.md`
- For evidence collection paths and commands: `references/evidence-collection.md`
- For documentation update template: `references/doc-template.md`
- For testing checklist: `references/testing-checklist.md`
- For subagent prompt templates: `references/subagent-prompts.md`

## Inputs

- Integration scope (specific integration or full inventory)
- Target surfaces to compare (Python, TypeScript, OTEL/API)
- Relevant repo paths and branch/diff scope
- Output expectations (table depth, doc patch format, test depth)

## Outputs

- Inventory and comparison matrix
- Findings and risk summary
- Documentation patch plan
- Test plan with missing coverage calls

## Default evidence locations (override if repo differs)

- Python:
  - `sdks/python/src/opik/integrations`
  - `sdks/python/design/INTEGRATIONS.md`
  - `sdks/python/design/TESTING.md`
- TypeScript:
  - `sdks/typescript/design/INTEGRATIONS.md`
  - `sdks/typescript/design/TESTING.md`
- Backend OTEL:
  - `apps/opik-backend/src/main/java/com/comet/opik/api/resources/v1/priv/OpenTelemetryResource.java`
  - `apps/opik-backend/src/main/java/com/comet/opik/domain/OpenTelemetryService.java`
  - `apps/opik-backend/src/main/java/com/comet/opik/domain/OpenTelemetryMapper.java`
  - `apps/opik-backend/src/main/java/com/comet/opik/domain/mapping/OpenTelemetryMappingRuleFactory.java`
  - `apps/opik-backend/docs/integrations.md`
