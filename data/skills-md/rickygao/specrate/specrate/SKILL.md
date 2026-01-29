---
name: specrate
description: Skill to manage specs and changes. Use this when working with specrate-managed documents.
license: Apache-2.0
---

# Specrate

## Overview

The specrate system is designed to manage specs and changes to those specs in a structured manner. It provides a framework for proposing, planning, implementing, and archiving changes to the system's specs.

- [PRINCIPLE.md](./references/PRINCIPLE.md) must be read first to understand how specrate works.
- [actions](./references/actions/) folder defines detailed steps for each specrate action.
- [templates](./assets/templates/) folder contains templates for various specrate artifacts and reports.

## Decisions

Based on the user's request, decide which action to take.

- If the user intends to show the current status of specs and changes,
  follow [SHOW-STATUS.md](./references/actions/SHOW-STATUS.md) action.
- If the user intends to propose a new change,
  follow [PROPOSE-CHANGE.md](./references/actions/PROPOSE-CHANGE.md) action.
- If the user intends to amend an existing change,
  follow [AMEND-CHANGE.md](./references/actions/AMEND-CHANGE.md) action.
- If the user intends to plan a proposed change,
  follow [PLAN-CHANGE.md](./references/actions/PLAN-CHANGE.md) action.
- If the user intends to implement a planned change,
  follow [IMPLEMENT-CHANGE.md](./references/actions/IMPLEMENT-CHANGE.md) action.
- If the user intends to archive an implemented change,
  follow [ARCHIVE-CHANGE.md](./references/actions/ARCHIVE-CHANGE.md) action.
- If the user intends to fix a spec according to the codebase,
  follow [FIX-SPEC.md](./references/actions/FIX-SPEC.md) action.
- If the user's intent mixes multiple actions,
  break down the intent into individual actions, ask for confirmation, and execute them one by one.
- If the user's intent is ambiguous (e.g., “update the spec”),
  ask a clarifying question with possible options to determine the specific action needed.

## Disciplines

- Always ask for clarifications if needed, and ensure the workspace remains consistent after each step. When asking for clarifications, provide concise options to the user if applicable.
- All specrate-managed artifacts that this skill creates/updates in the user's repository **MUST** reside in the `.specrate/` folder at the repository root.
- Do **NOT** create auxiliary documents (README, index, etc.) outside `.specrate/` unless explicitly instructed by the user.
