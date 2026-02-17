---
name: subagent-task-execution
description: Use when executing tasks from a task breakdown document in the current session.
---

# Subagent Task Execution

## Overview
This skill is used to execute a set of tasks (typically from a task breakdown or plan). It focuses on high-quality execution by dispatching specialized subagents for each task, ensuring each task is performed correctly and verified before moving to the next.

## Core Principle
**One Task, One Subagent, Multi-Stage Review.** 
By isolating each task and applying a structured review process, we ensure high quality and prevent context pollution.

## The Process

1.  **Preparation:**
    - Read the entire plan or task breakdown.
    - Extract all tasks with their full context.
    - Create a structured todo list using the `TodoWrite` tool.

2.  **Per-Task Execution Loop:**
    - **Skill Discovery:** Before starting a task, identify which specialized skill(s) are needed for its execution (e.g., `coding`, `brainstorming`, or any project-specific skills).
    - **Dispatch Implementer:** Dispatch a subagent to perform the task. Provide the subagent with the full task description, any identified skills, and the necessary context.
    - **Interactive Clarification:** If the subagent has questions, answer them clearly before they proceed with implementation.
    - **Task Implementation:** The subagent performs the task, following the identified best practices and skills.
    - **Verification & Review:**
        - **Spec Compliance Review:** A separate subagent verifies that the result exactly matches the task requirements (no more, no less).
        - **Quality Review:** A final review stage to ensure the output meets the highest standards of the domain (e.g., code quality, documentation clarity, etc.).
    - **Completion:** Mark the task as completed in the todo list.

3.  **Finalization:**
    - Once all tasks are complete, perform a final holistic review of the entire body of work to ensure consistency and overall quality.

## Key Principles
- **Discovery First:** Always look for and apply the most relevant skills for the specific task at hand.
- **Isolation:** Each task should be treated as a distinct unit of work.
- **Review Loops:** Never move to the next task if the current one has open issues from either the spec or quality reviews.
- **Subagent Specialization:** Use subagents as specialized workers, providing them with all the context they need upfront.

## Red Flags
- Skipping the skill discovery phase.
- Combining multiple tasks into a single subagent invocation.
- Proceeding with a task while reviews are still pending or failing.
- Ignoring subagent questions or providing vague answers.
- Failing to update the todo list as progress is made.
