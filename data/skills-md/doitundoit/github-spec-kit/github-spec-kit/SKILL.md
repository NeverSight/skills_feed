---
name: github-spec-kit
description: Expert guidance for Spec-Driven Development using the GitHub Spec Kit. Use when the user wants to initialize a project, create specifications, plan implementations, or execute tasks based on the Spec Kit workflow. Triggers on "spec kit", "specify", "create spec", "spec-driven development".
---

# Github Spec Kit

## Overview

This skill guides the Spec-Driven Development (SDD) process using the GitHub Spec Kit. It helps you shift from code-first to specification-first development, ensuring high-quality software by focusing on product scenarios and predictable outcomes.

## Workflow

The Github Spec Kit workflow consists of the following key stages. Follow them sequentially for new features or projects.

1.  **Initialize**: Set up the project structure.
2.  **Constitution**: Define project principles.
3.  **Specify**: Create a functional specification.
4.  **Plan**: Design the technical implementation.
5.  **Tasks**: Break down the plan into actionable tasks.
6.  **Implement**: Execute the tasks.

For detailed instructions on each step, see [WORKFLOW.md](references/workflow.md).

## Usage Guide

### 1. Initialization
- **Goal**: Bootstrap a new project.
- **Action**: Use `uvx --from specify-cli specify init . --here --ai [MODEL]`.
- **Git Check**: Before execution, check if the directory is already a git repository (e.g., `git rev-parse --is-inside-work-tree`). Use the `--no-git` flag **only** if a git repository is already initialized to avoid conflicts.
- **Check**: Ensure `specify-cli` is accessible; `uvx` is preferred for consistency.

### 2. Principles (Constitution)
- **Goal**: Establish governing principles.
- **Trigger**: Respond to `/speckit.constitution`.
- **Action**: Create or update `.specify/memory/constitution.md`.
- **Focus**: Define core values like code quality, testing standards, and performance.

### 3. Specification
- **Goal**: Describe "what" and "why".
- **Trigger**: Respond to `/speckit.specify`.
- **Action**: Create `specs/<feature>/spec.md` using the template in `.specify/templates/spec-template.md`.
- **Focus**: User scenarios, outcomes, functional requirements. Avoid implementation details.

### 4. Planning
- **Goal**: Define "how".
- **Trigger**: Respond to `/speckit.plan`.
- **Action**: Create `specs/<feature>/plan.md` (and optional `data-model.md`, `research.md`).
- **Focus**: Architecture, tech stack, data structures, algorithms.

### 5. Tasks
- **Goal**: Create a checklist.
- **Trigger**: Respond to `/speckit.tasks`.
- **Action**: Create `specs/<feature>/tasks.md` based on the plan and specification.
- **Focus**: Small, verifiable steps grouped by user story.

### 6. Implementation
- **Goal**: Write code.
- **Trigger**: Respond to `/speckit.implement`.
- **Action**: Execute tasks from `tasks.md` sequentially.
- **Behavior**: Read the current task, implement, verify, and mark as completed.

## Resources

- **Workflow Details**: [WORKFLOW.md](references/workflow.md)
