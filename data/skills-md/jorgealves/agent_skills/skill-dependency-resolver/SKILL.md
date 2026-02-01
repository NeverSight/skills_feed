---
name: skill-dependency-resolver
description: Identifies and manages execution dependencies between agent skills by analyzing their inputs and outputs. Use when building multi-step agent workflows to ensure skills are executed in the correct order and that all required data is available.
---
# Skill Dependency Resolver

## Purpose and Intent
The `skill-dependency-resolver` acts as a scheduler and orchestrator. It looks at what each skill "needs" and what it "provides" to determine the logical order of operations for a multi-skill task.

## When to Use
- **Workflow Automation**: When you want an agent to handle a complex task that requires multiple steps (e.g., Audit -> Refactor -> Test).
- **Architecture Planning**: To see if your current skill library has all the necessary "connectors" to solve a business problem.

## When NOT to Use
- **Single-Skill Tasks**: Overkill if you only need a single tool to run once.

## Security and Data-Handling Considerations
- **Structural Analysis Only**: It looks at the "shape" of the skills, not the sensitive data passing through them.
