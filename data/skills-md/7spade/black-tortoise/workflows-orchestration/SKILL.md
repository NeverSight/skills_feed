---
name: workflows-orchestration
description: Workflow orchestration patterns for src/app/workflows, focusing on application-layer use cases, long-running flows, event-driven coordination, and deterministic state transitions; use when implementing multi-step user journeys or cross-capability processes.
---

# Workflows Orchestration

## Intent
Implement multi-step processes as explicit application workflows that coordinate capabilities via events, not via direct imports.

## Workflow Model
- A workflow is a state machine: explicit states, transitions, and terminal states.
- Keep transitions deterministic and driven by events/commands.

## Where Logic Lives
- Workflow coordination lives in the Application layer (stores/use cases).
- Domain invariants stay in Domain; do not encode rules in UI components.

## Event-Driven Coordination
- Workflows subscribe to events to advance state.
- Publish events only after persistence (append-before-publish).

## Concurrency
- Choose explicit concurrency semantics for async operations (cancel, queue, ignore).
- Avoid parallel append/publish operations that break causal ordering.

## Observability
- Include correlation IDs so a whole workflow run can be traced end-to-end.
