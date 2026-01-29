---
name: rules-workflows
description: Use to standardize project context (Rules) or automate complex multi-step tasks (Workflows).
license: MIT
compatibility: Requires Antigravity CLI
allowed-tools: read_file write_to_file run_command
---

# Rules & Workflows Orchestrator

This skill outlines the standards for acting as an **Autonomous Process Orchestrator**, managing behavior and workflows to align with Agile best practices and project constraints.

## 🧠 Core Philosophy: Autonomy & Reasoning

**"Think before you Act"**

Before creating any rule or workflow, the Agent MUST:

1.  **Analyze the Goal**: What is the user trying to achieve?
2.  **Orchestrate Capabilities**: Identify which _other_ skills (Frontend, Backend, QA) are needed.
3.  **Separate Concerns**:
    - **Workflows** = Process (Steps, Sequences)
    - **Skills** = Knowledge (Standards, Implementation)

## 📚 Reference Library

This skill relies on specialized guides located in the `references/` directory. **You MUST consult these files for specific tasks.**

| Task                          | Reference File                         | Purpose                                                                         |
| :---------------------------- | :------------------------------------- | :------------------------------------------------------------------------------ |
| **Creating & Managing Rules** | `references/rules-guide.md`            | Standard Operating Procedures (SOPs), Context Injection, Rule Activation Types. |
| **Building Workflows**        | `references/workflows-guide.md`        | High-Performance Workflow Design, "Turbo" Execution, Checkpoints.               |
| **Orchestrating Skills**      | `references/orchestration-patterns.md` | Skill Chaining Patterns (e.g., Spec-First, TDD), Conflict Resolution.           |

---

## 1. Orchestration Strategy

**👉 For best practices on sequencing skills, refer to `references/orchestration-patterns.md`**.

Key principles:

1.  **Never Silo Skills**: Code requires Architecture; Design requires Requirements.
2.  **Sequential Thinking**: Use `sequential-thinking` for complex problems before acting.
3.  **Process vs. Knowledge**: Ensure workflows delegate "how-to" knowledge to the appropriate Skill.

---

## 2. Self-Correction & Learning

The Agent can modify its own rules (Meta-Programming).

- **User Correction**: "Don't do X anymore" -> Trigger `workflow-rule-from-feedback.md`.
- **New Project**: "Read this codebase" -> Trigger `workflow-rule-from-codebase.md`.
