---
name: capabilitys-layer
description: Patterns for implementing features under src/app/capabilitys, including presentation/application/domain/integration boundaries, NgRx Signals stores, event-driven communication, and Angular 20 template rules; use when adding or changing a capability.
---

# Capabilitys Layer

## Intent
Deliver independent capabilities as bounded contexts that interact only via events and the workspace context.

## Structure Rules
- Keep each capability cohesive: UI + application orchestration + domain model (if needed).
- Do not create cross-capability imports for business logic; communicate via events.

## State Management
- Use `@ngrx/signals` stores as the source of truth for capability state.
- Derive view state via computed signals; avoid mutable arrays/objects and avoid `.push()`.
- Async side effects run through `rxMethod` + `tapResponse` with explicit operator choice.

## Event-Driven Interactions
- Publish domain/application events after persistence (append-before-publish).
- Subscribe to events in application stores/effects, not in presentation components.

## UI Rules
- Standalone, zone-less components.
- Templates bind to signals only and use Angular control flow (`@if`, `@for`, `@switch`, `@defer`).
- Material Design 3 token usage only; no hardcoded colors.

## Data Boundaries
- Infrastructure returns Observables/Promises; convert to signals before templates.
- Do not leak Firebase/DataConnect DTOs outside integration/infrastructure.

## Testing Expectations
- Cover critical flows with unit tests for store transitions and Playwright for happy paths.
- Use stable selectors (`data-testid`, roles/labels).
