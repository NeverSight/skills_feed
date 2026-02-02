---
name: eventing-hub
description: Event-sourcing and EventBus directives for Black-Tortoise, covering structured event schemas, append-before-publish flow, causality/id rules, and safe subscribers; use when touching src/app/eventing, EventBus, or any event handlers/projections.
---

# Eventing Hub Master Guide

## Intent
Describe event contracts, persistence/publish order, and consumer safety for the shared EventBus described in `src/app/eventing/AGENTS.md` and `.github/instructions/20-ddd-event-sourcing-copilot-instructions.md`.

## Event Schema
- Declare events with a Type, Payload, Metadata, and Semantics structure; keep payloads immutable and document any allowed mutations in the metadata.
- Use a `correlationId` to tie related events, and assign a `causationId` that points to the triggering event (null only for root events).
- Emit only typed events from the Aggregates/Application services; do not publish raw DTOs or Firebase objects.

## Append → Publish → React
- Persist every outcome (Append) before invoking the `EventBus` publish step; never wrap append/publish in `Promise.all` or parallel flows to avoid causality gaps.
- After the append promise resolves, publish the event and let downstream stores/projections react via the global `EventBus` singleton.
- Reactions should be limited to simple projections or side effects; long-running work belongs to dedicated use cases handled by the Application layer.

## Causality Tracking & Immutability
- Maintain causation/correlation IDs for every published event; log them for tracing and include them in metadata for audit tooling.
- Treat emitted events as read-only facts; consumers may inspect but must never mutate payload or metadata objects.
- Use `Object.freeze()` or deep copies when broadcasting to ensure immutability guarantees reach all subscribers.

## Safe Subscriptions
- Convert the RxJS stream behind `EventBus` into signals at the Application boundary using `toSignal()` before exposing data to Presentation stores.
- Guard subscriptions with `takeUntilDestroyed()` or signal-based cleanup so that event handlers do not leak after a component/store is destroyed.
- Prefer `@ngrx/signals` stores for reacting to events; their `withMethods` handlers should call `patchState` based on event payloads rather than mutating the store directly.

## Validation & Monitoring
- Validate payload schemas before append, using domain value objects to enforce invariants (Domain layer) and rejecting invalid data early.
- Emit audit events when Append or Publish steps fail so `docs/AUDIT-*` trackers capture the problem context.
- Feed causality IDs into any observability tooling to verify the Append→Publish→React chain during CI or runtime tracing.
