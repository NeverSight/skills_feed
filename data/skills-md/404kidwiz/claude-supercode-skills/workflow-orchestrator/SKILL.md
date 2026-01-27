---
name: workflow-orchestrator
description: Expert in designing durable, scalable workflow systems using Temporal, Camunda, and Event-Driven Architectures.
---

# Workflow Orchestrator

## Purpose
Provides expertise in designing and implementing durable workflow systems that coordinate complex business processes. Specializes in workflow engines like Temporal and Camunda, saga patterns, and building reliable long-running processes.

## When to Use
- Designing multi-step business workflows
- Implementing saga patterns for distributed transactions
- Building with Temporal, Camunda, or similar workflow engines
- Handling long-running processes with durability requirements
- Coordinating activities across multiple services
- Implementing compensation and rollback logic
- Building human-in-the-loop approval workflows
- Managing state machines for complex processes

## Quick Start
**Invoke this skill when:**
- Designing multi-step business workflows
- Implementing saga patterns for distributed transactions
- Building with Temporal, Camunda, or similar workflow engines
- Handling long-running processes with durability requirements
- Coordinating activities across multiple services

**Do NOT invoke when:**
- Simple async job processing → use appropriate queue solution
- Task distribution for agents → use task-distributor
- Event streaming → use event-driven-architect
- CI/CD pipelines → use devops-engineer

## Decision Framework
```
Workflow Need?
├── Durable Long-Running → Temporal or durable execution engine
├── Human Tasks → Camunda or process orchestration platform
├── Choreography → Event-driven with eventual consistency
├── Simple Steps → State machine or queue-based
├── Saga Pattern → Orchestrated or choreographed compensations
└── Scheduled Jobs → Cron-based with workflow wrapper
```

## Core Workflows

### 1. Temporal Workflow Implementation
1. Define workflow interface and activities
2. Implement workflow logic with Temporal SDK
3. Create activity implementations for external calls
4. Configure retry policies and timeouts
5. Implement signals and queries for external interaction
6. Add versioning for workflow updates
7. Deploy workers and monitor execution
8. Implement testing with Temporal test framework

### 2. Saga Pattern Implementation
1. Identify distributed transaction boundaries
2. Define forward actions and compensating actions
3. Choose orchestration (central) or choreography (events)
4. Implement idempotent operations
5. Handle partial failures with compensation
6. Add timeout handling for stuck sagas
7. Implement observability for saga state
8. Test failure scenarios thoroughly

### 3. Human-in-the-Loop Workflow
1. Design process with human task points
2. Model workflow with BPMN or similar notation
3. Implement automated steps as activities
4. Create task inbox UI for human actions
5. Add escalation and timeout handling
6. Implement delegation and reassignment
7. Add audit trail for compliance
8. Monitor SLAs for human tasks

## Best Practices
- Make all activities idempotent for safe retries
- Use workflow versioning for production updates
- Implement comprehensive compensation for failures
- Set appropriate timeouts at each step
- Add observability with traces spanning workflow
- Design for failure; assume any step can fail

## Anti-Patterns
- **Non-idempotent activities** → Design for safe retry
- **Missing compensations** → Plan rollback from the start
- **Infinite retries** → Set max attempts and handle failures
- **Blocking human tasks** → Add timeouts and escalation
- **Tight coupling** → Keep workflows decoupled from activity impl
