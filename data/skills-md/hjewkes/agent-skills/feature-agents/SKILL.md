---
name: feature-agents
description: Specialized feature development agents. Use for deep codebase exploration and architecture design during feature development.
---

# Feature Development Agents

Available agents (spawn via Task tool with `general-purpose` type):

- **code-explorer** — traces execution paths, maps architecture layers, documents dependencies
- **code-architect** — designs feature architectures and implementation blueprints

For code review, see the code-review skill.

## Usage

1. Read the corresponding reference file for the agent's full system prompt
2. Spawn a `general-purpose` Task agent with that prompt as the task description
3. Include the specific feature/files/scope in the prompt

## Reference Files

| Agent | Reference |
|-------|-----------|
| code-explorer | [references/code-explorer.md](references/code-explorer.md) |
| code-architect | [references/code-architect.md](references/code-architect.md) |

## Domain Specialization

When spawning feature agents, include domain context to focus their analysis:

| Domain | Priority Focus |
|--------|---------------|
| API/Backend | Routes, middleware, auth, DB queries, error handling |
| Frontend/UI | Components, state management, rendering, accessibility |
| Data/Pipeline | Transformations, validation, schema, performance |
| Infrastructure | Config, deployment, monitoring, secrets management |
| CLI/Tools | Argument parsing, output formatting, error messages |

Include the domain in the agent's spawn prompt: "Domain: API/Backend — prioritize route handlers, middleware chain, and auth flow."
