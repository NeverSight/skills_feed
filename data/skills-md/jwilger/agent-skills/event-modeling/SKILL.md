---
name: event-modeling
description: >-
  Event modeling facilitation for discovering and designing event-sourced
  systems. Four phases: domain discovery, workflow design (9-step process),
  GWT scenario generation, and model validation. Activate when starting a
  new project, designing features, modeling domains, writing Given/When/Then
  scenarios, or discussing event sourcing and domain-driven design.
license: CC0-1.0
metadata:
  author: jwilger
  version: "1.0"
  requires: []
  context: [event-model]
  phase: understand
  standalone: true
---

# Event Modeling

**Value:** Communication -- event modeling is a structured conversation that
surfaces hidden domain knowledge and creates shared understanding between
humans and agents before any code is written.

## Purpose

Teaches the agent to facilitate event modeling sessions following Martin
Dilger's "Understanding Eventsourcing" methodology. Produces a complete
event model (actors, events, commands, read models, automations, slices)
that drives all downstream implementation. The model lives in
`docs/event_model/`.

## Practices

### Two-Phase Process: Discovery Then Design

Never jump into detailed workflow design without broad domain understanding
first. Phase 1 maps the territory; Phase 2 explores each region.

**Phase 1 -- Domain Discovery.** Identify what the business does, who the
actors are, what major processes exist, what external systems integrate, and
which workflows to model. Ask these questions of the user; do not assume
answers. Output: `docs/event_model/domain/overview.md`.

**Phase 2 -- Workflow Design.** For each workflow, follow the 9-step
process. You MUST follow `references/nine-steps.md` for the full methodology. Design
one workflow at a time. Complete all 9 steps before starting the next
workflow. Output: `docs/event_model/workflows/<name>/overview.md` plus
individual slice files in `slices/`.

### The Prime Directive: Not Losing Information

Store what happened (events), not just current state. Events are immutable
past-tense facts in business language. Every read model field must trace
back to an event. If a field has no source event, something is missing from
the model.

### Event Design Rules

1. Name events in past tense using business language: `OrderPlaced`, not
   `PlaceOrder` or `CreateOrderDTO`
2. Events are immutable facts -- never modify or delete
3. Include relevant data: what happened, when, who/what caused it
4. Find the right granularity -- not `DataUpdated` (too broad) and not
   `FieldXChanged` (too narrow)
5. Commands depend on user inputs and the event stream, not read models.
   Read models serve views and automations only.
6. Events record domain facts (true on any machine). Runtime context
   (file paths, hostnames, PIDs, working directories) does not belong
   in event data.

### The Four Patterns

Every event-sourced system uses these patterns. Each pattern maps to one
vertical slice.

1. **State Change:** Command -> Event. The only way to modify state. A
   command may produce multiple events as part of a single operation.
2. **State View:** Events -> Read Model. How the system answers queries.
   When the domain supports concurrent instances, use collection types
   in read model fields, not singular values.
   Commands derive their inputs from user-provided data and the event
   stream — never from read models. No `ReadModel → Command` edges
   should appear in diagrams. If a command needs to check whether
   something already happened (e.g., idempotency), it checks the event
   stream, not a read model.
   Read models represent meaningful domain projections. Infrastructure
   preconditions ("does directory exist?", "is service running?") that
   are implicit in the command's execution context do not need their own
   read model.
3. **Automation:** Event -> Read Model (todo list) -> Process -> Command
   -> Event. Background work triggered by events. Requires all four
   components: triggering event, read model consulted, conditional
   process logic, and resulting command. If there is no read model and
   no conditional logic, it is NOT an automation — it is a command
   producing multiple events. Must have clear termination conditions.
4. **Translation:** External Data -> Internal Event. Anti-corruption layer
   for workflow-specific external integrations. Generic infrastructure
   shared by all workflows (event persistence, message transport) is NOT
   a Translation — it is cross-cutting infrastructure that belongs
   outside the event model.

### Required Layers Per Slice Pattern

Each slice pattern implies a minimum set of architectural layers. A slice is not complete until all required layers are implemented and wired together.

- **State View**: infrastructure (read events/data from store) + domain (projection/query logic) + presentation (render or return result to caller) + application wiring (connect layers end-to-end)
- **State Change**: presentation (accept user input or external request) + domain (command validation and business rules) + infrastructure (persist resulting events/data) + application wiring (connect layers end-to-end)
- **Automation**: infrastructure (detect triggering condition — timer, external event, threshold) + domain (policy/decision logic) + infrastructure (execute resulting action — send message, write data, call service) + application wiring (connect trigger to policy to action)
- **Translation**: infrastructure (receive from external system) + domain (mapping/transformation logic) + infrastructure (deliver to target system) + application wiring (connect inbound adapter to mapper to outbound adapter)

When decomposing a slice, verify that your acceptance criteria and task breakdown cover every required layer. A slice that only implements domain logic without presentation or infrastructure is incomplete — it is a component, not a vertical slice.

### GWT Scenarios

After workflow design, generate Given/When/Then scenarios for each slice.
These become acceptance criteria for implementation.

**Command scenarios:** Given = prior events establishing state. When = the
command with concrete data. Then = events produced OR an error (never both).

**View scenarios:** Given = current projection state. When = one new event.
Then = resulting projection state. Views cannot reject events.

**Critical distinction:** GWT scenarios test business rules (state-dependent
policies), not data validation (format/structure checks that belong in the
type system). If the type system can make the invalid state unrepresentable,
it is not a GWT scenario.

You MUST use `references/gwt-template.md` for the full scenario format and examples.

### Application-Boundary Acceptance Scenarios

Every vertical slice MUST include at least one GWT scenario defined at the application boundary:

- **Given**: The system is in a known state (prior events, seed data, configuration)
- **When**: A user (or external caller) interacts through the application's external interface — the specific interface depends on the project (HTTP endpoint, CLI command, message queue consumer, UI action, etc.)
- **Then**: The result is observable at that same boundary — a response, output, rendered state change, emitted event, etc.

A GWT scenario that can be satisfied entirely by calling an internal function in a unit test describes a unit-level specification, not a slice acceptance criterion. Slice acceptance criteria must exercise the path from external input to observable output.

### Acceptance Test Strategy

Where the application boundary is programmatically testable — HTTP endpoints, CLI output parsing, headless browser automation, message queue assertions, API contract tests, etc. — write automated acceptance tests that exercise the full GWT scenario from external input to observable output. These tests provide fast feedback and serve as living documentation of slice behavior.

Where automated boundary testing is not feasible (complex GUI interactions, hardware-dependent behavior, visual/aesthetic verification), document what the human should manually verify: the specific steps to perform and the expected observable result. This manual verification checklist becomes part of the slice's definition of done.

### Slice Independence

Slices sharing an event schema are independent. The event schema is the
shared contract. Command slices test by asserting on produced events; view
slices test with synthetic event fixtures. Neither needs the other to be
implemented first. No artificial dependency chains between slices.

### Model Validation

After GWT scenarios are written, validate the model for completeness:

1. Every read model field traces to an event
2. Every event has a triggering command, automation, or translation
3. Every command has documented rejection conditions (business rules)
4. Every automation has a termination condition
5. GWT Given/When/Then clauses do not reference undefined elements

When gaps are found, ask the user to clarify, create the missing element,
and re-validate. Do not proceed with gaps remaining.

### Facilitation Mindset

You are a facilitator, not a stenographer. Ask probing questions. Challenge
assumptions. Keep asking "And then what happens?" after every event, every
command, every answer. Use business language, not technical jargon. Do not
discuss databases, APIs, frameworks, or implementation during event modeling.
The only exception: note mandatory third-party integrations by name and
purpose.

**Do:**
- Follow all steps in order -- the process reveals understanding
- Ask "And then what happens?" relentlessly
- Use concrete, realistic data in all examples and scenarios
- Design one workflow at a time
- Ensure information completeness before proceeding
- Ask "Can there be more than one of these at the same time?" for read model fields
- Verify automations have all four components before labeling them as such

**Do not:**
- Skip steps because you think you know enough
- Make architecture or implementation decisions during modeling
- Write GWT scenarios for data validation (use the type system)
- Design multiple workflows simultaneously
- Proceed with gaps in the model

## Enforcement Note

This skill provides advisory guidance. It instructs the agent on the event
modeling methodology but cannot mechanically prevent skipping steps or
producing incomplete models. When used with the `tdd` skill, GWT scenarios
from event modeling become acceptance tests that enforce the model. Without
it, the agent follows these practices by convention. If you observe steps
being skipped, point it out.

## Verification

After completing event modeling work, verify:

- [ ] Domain overview exists at `docs/event_model/domain/overview.md` with
      actors, workflows, external integrations, and recommended starting
      workflow
- [ ] Each designed workflow has `docs/event_model/workflows/<name>/overview.md`
      with all 9 steps completed
- [ ] All events are past tense, business language, immutable facts
- [ ] Every read model field traces to a source event
- [ ] Every event has a trigger (command, automation, or translation)
- [ ] Automations have all four components (event, read model, conditional logic, command)
- [ ] Read model fields use collection types when domain supports concurrent instances
- [ ] No cross-cutting infrastructure modeled as Translation slices
- [ ] GWT scenarios exist for each slice (inline in `docs/event_model/workflows/<name>/slices/*.md`) with concrete data
- [ ] GWT error scenarios test business rules only, not data validation
- [ ] Slices sharing an event schema are independently testable (no
      artificial dependency chains)
- [ ] No gaps remain in the model after validation

If any criterion is not met, revisit the relevant practice before proceeding.

## Dependencies

This skill works standalone. For enhanced workflows, it integrates with:

- **domain-modeling:** Events reveal domain types (Email, Money, OrderStatus)
  that the domain modeling skill refines
- **tdd:** Each vertical slice maps to one TDD cycle
- **architecture-decisions:** Event model informs architecture; ADRs should
  not be written during event modeling itself
- **task-management:** Workflows map to epics, slices map to tasks

Missing a dependency? Install with:
```
npx skills add jwilger/agent-skills --skill domain-modeling
```
