---
name: vertical-slice-delivery
description: A delivery methodology for shipping work incrementally via independently valuable vertical slices.
---

# Vertical Slice Delivery

Vertical slice delivery structures work as a sequence of small, end-to-end behaviors that each deliver real value on their own. This skill defines how work should be conceptualized and planned.

## When to Apply

Apply this skill when:

- Designing or delivering a feature
- Breaking down a multi-step change into meaningful units
- Estimating progress in terms of user-visible behavior
- Resuming delivery work after a pause
- Coordinating multiple changes that must evolve together

**Key trigger phrases:** "plan this", "break this down", "what tasks", "what are the steps", "plan the fix", "plan the refactor", "how should we fix".

When this skill is selected you MUST load and obey the accompanying `AGENTS.md`.

## What a Vertical Slice Is

A vertical slice is a **complete behavior**, not a technical step.

Each slice:

- delivers a usable end-to-end outcome
- spans all necessary layers (UI, logic, data, tests)
- is valuable even if no further slices are completed
- is safe to deploy to production on its own

A slice that cannot be deployed to production without relying on future work is not a valid slice.

Think:

> skateboard → scooter → bicycle → motorcycle → car

Not:

> wheels → chassis → engine → body → car

The former delivers value at every step.
The latter delivers nothing until the end.

## Planning Constraints

- Work must be divided into **behavioral increments**
- Each behavior must stand on its own
- Behaviors must build additively, never retroactively
- Each behavior must have a clear owner (slice)

**Planning template**

```
Slice ID:
Behavior:
Includes (layers / concerns):
```

**Good vs Bad Slices**

Good:

```
[S1] Users can view their profile
[S2] Users can edit their display name
[S3] Users can upload a profile photo
```

Bad:

```
[S1] Create User model/migrations
[S2] Add profile API endpoints
[S3] Build profile UI components
```

The bad example creates "wheels without a vehicle"—no slice delivers user value until all are complete.

## Completion Definition

Work is complete when:

- All intended behaviors exist as slices
- Each behavior stands independently
- No known gaps remain unowned

Completion is judged by **delivered behavior**, not task lists.

This skill exists to reduce context loss, avoid speculative design, and keep delivery aligned with real product value.