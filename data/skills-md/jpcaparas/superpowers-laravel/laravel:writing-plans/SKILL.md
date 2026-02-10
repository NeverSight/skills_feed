---
name: laravel:writing-plans
description: Create an actionable Laravel implementation plan—bite-sized tasks with TDD-first steps, migrations, services, jobs, and validation points
---

# Writing Plans (Laravel)

Turn a confirmed design into a sequence of small, testable steps. Include guardrails and validation before handoff.

## Structure

1. Scaffolding
   - Runner: confirm Sail or host
   - Branch & workspace prep (worktrees optional)
2. Data Model
   - Migrations and factories (one commit per change)
   - Seeders if needed for demo flows
3. Services & Interfaces
   - Controllers/Requests/Resources (or actions)
   - Ports & adapters for external systems
   - Jobs/events/listeners as needed
4. Tests (TDD)
   - Feature tests for behavior; unit tests for pure logic
   - Use factories; verify failure first, then pass
5. Quality Gates
   - Pint, static analysis, tests clean
6. Rollout & Observability
   - Logs/metrics; Horizon queues; toggles/migrations safety

## Example Task Format

- Add migration + model + factory for X
- Write failing feature test for route Y
- Implement controller + request + policy for Y
- Add service with port+adapter for Z
- Dispatch job; add listener + events as needed
- Verify queues; add tags and Horizon metrics
- Run quality checks; update docs

After writing the plan, use `laravel:executing-plans` to execute in batches.

