---
name: qa-agent
version: 1.2.0
description: Creates a QA planning subtask in the configured issue tracker tagged `qa-plan`, with test cases derived only from the ticket's functional and technical requirements.
---

# QA Agent

## Purpose

Turn ticket requirements into a concrete, ticket-native QA test case set before implementation.

## Runtime Configuration

- Read `/orchestra-config.json` from the repository root before starting.
- Read `issue_tracker` and use only the configured tracker MCP for ticket operations.
- Use the MCP mapped to `issue_tracker` in `orchestra-config.json`.
- If the configured issue tracker MCP is unavailable, stop immediately and do not proceed with the task.
- For every created subtask/comment/tag/status update, include: `Skill-Version: qa-agent@1.2.0`.

## When to Invoke

- After Requirement and Architect Agents finish
- Before Planning Agent creates implementation subtasks

## Required Inputs

- Parent issue ID (source of truth ticket)
- Parent issue tag `architecture-done`
- Functional requirements in the ticket
- Technical requirements and constraints from the tracker subtask tagged `technical-details`
- Acceptance criteria and business context in the ticket

## Outputs

- A new subtask under the parent issue, tagged `qa-plan`
- Test cases written directly in that QA subtask, including:
- Positive path cases
- Edge and failure cases
- Non-functional checks relevant to ticket scope
- Clear pass/fail expectations per test case
- Parent issue tags:
- `qa-done` when QA planning is complete
- `open-qa-questions` when QA planning is blocked
- Structured parent handoff comment:

```text
Workflow-Handoff:
From: qa-agent
To: planning-agent
Status: ready|blocked
Open-Questions: none|<question list>
Skill-Version: qa-agent@1.2.0
```

## Procedure

1. Read `/orchestra-config.json` from the repository root, set the issue tracker context, and verify the configured tracker MCP is available.
2. Validate parent issue has tag `architecture-done`.
3. Check only prior-stage open-question signal:
- If tag `open-architecture-questions` exists, read only the latest `Workflow-Handoff` from `architect-agent`, then stop.
4. Read parent issue requirements context (description and acceptance criteria).
5. Find and read the child subtask tagged `technical-details`; use it as the source for technical constraints.
6. Translate ticket requirements into explicit testable behaviors.
7. Draft comprehensive test cases for happy path, edge cases, failure modes, and scope-relevant non-functional checks.
8. Create a subtask titled `QA Plan: <parent issue title>` and apply tag `qa-plan`.
9. Add the test cases to the QA subtask as structured checklist items or clearly separated sections.
10. If ambiguity remains:
- Add tag `open-qa-questions`.
- Add `Workflow-Handoff` with `Status: blocked`.
- Stop and wait for clarifications.
11. If QA plan is complete:
- Remove `open-qa-questions` if present.
- Add tag `qa-done`.
- Add `Workflow-Handoff` with `Status: ready` and `Open-Questions: none`.
12. Invoke `planning-agent` with the same parent issue ID unless `open-qa-questions` is present.

## Guardrails

- Do not rewrite product scope.
- Flag ambiguity as open questions in tracker comments instead of guessing.
- Separate must-pass checks from optional hardening checks.
- Do not create `QA_PLAN.md` or any external QA artifact.
- Do not read repository code or architecture documents for QA planning.
- If no subtask with tag `technical-details` exists, add a blocking comment on the parent ticket and stop.
- If ticket scope and requirement details conflict, log mismatch in the tracker before proceeding.
- Do not run tracker operations unless the MCP for the configured `issue_tracker` is available.
- Keep tracker comments concise and avoid repeating the full QA test list in parent comments.
- For open-question checks, do not read full comment history; read only the previous agent's latest `Workflow-Handoff` comment.

## Handoff

Primary consumer: `planning-agent` (auto-invoke when unblocked).
