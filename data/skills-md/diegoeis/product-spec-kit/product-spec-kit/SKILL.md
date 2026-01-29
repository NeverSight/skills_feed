---
name: product-spec-kit
description: Comprehensive skill for Product Managers to create organize and manage Product Teams, Strategy, PRDs, release plans, user stories, and standalone issues with high-quality acceptance criteria. Supports both full documentation workflows (PRD → Plan → Stories) and quick issue creation (standalone stories, tasks, bugs). All documentation follows design-driven development principles with functional, testable acceptance criteria based on visual designs and user flows.
---

## Overview

This skill helps Product Managers produce structured, high-quality documentation for product development. It supports both comprehensive documentation workflows (PRD → Plan → Stories) and standalone quick issues (individual stories, tasks, or bugs).

Always use the language of the user interaction to create the final files, including headings and default content of templates. If the user explicitly requests a different language, use it.

## When to use?

Use this skill when user asks to:
- Create a PRD specification
- Create an epic and your stories/tasks
- You need to create or clarify a product specification, such as a Product Requirements Document (PRD), a Release Plan, or a User Story. 
- It can also be used to create standalone PRD, Plan, Story, Task or Bug.


## Core Principles Constitution

All documentations need to follow the constitution defined in `rules/product-speckit-constitution.md`. This constitution is a set of non-negotiable principles that govern all product documentation created with this skill. These principles apply regardless of language, workflow type (full or quick), or document format.

### Principle I: Complete & Unambiguous Requirements
Every requirement must be clear enough that a reader with no prior context can understand what's needed and why.

### Principle II: Design-Driven Acceptance Criteria
Acceptance criteria should be based on visual designs, user flows, and specific UI elements - never written from assumptions.

### Principle III: Functional Over Descriptive
Criteria must describe what the system does, not what it looks like. Focus on behavior, actions, and outcomes.

### Principle IV: Right Level of Detail
- PRDs: Macro-level requirements and general rules
- Stories: Detailed, functional acceptance criteria
- Each document serves its purpose without overlap

### Principle V: Never Assume, Always Validate
When information is missing or ambiguous:
- Ask specific questions
- Request designs/mockups
- Reference previous discussions
- Mark uncertain items for validation
- Wait for confirmation before finalizing

## Workflows or Commands

- *Starting the interaction - how to start a new specification*: If the user don't provide the type of specification want to build, always ask for it, using the `workflows/prod-start.md` instructions. Ignore the start step if the user provide the type of specification want to build.
- *Creating a PRD*: When the user want to create a PRD, use the `workflows/prod-spec-prd.md` instructions.
- *Clarifying an specification*: When the user want to clarify an specification (such as PRD, Plan, Story, Task or Bug), use the `workflows/prod-clarify.md` instructions. If the user doesn't provide an existing specification, ask for it.
- *Breakdown specs*: When the user want to break the PRD in smaller parts such as Epics -> Stories / Tasks, use the `workflows/prod-spec-breakdown.md` instructions. You need to validate an existing PRD or create the PRD before breaking it down. If the user doesn't provide an existing PRD, ask for it.
- *Creating a Story*: When the user want to create a story, use the `workflows/prod-spec-story.md` instructions.
- *Creating a Task*: When the user want to create a task, use the `workflows/prod-spec-task.md` instructions.
