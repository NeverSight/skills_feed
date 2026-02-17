---
name: reflection
description: "Analyzes the conversation and tool usage to propose improvements to skills or store user preferences."
---

# Reflection Skill

## Overview
This skill is used to periodically reflect on the interaction with the user. It analyzes what worked, what didn't (tool failures), and identifies recurring patterns or explicit user preferences that should be formalized.

## Objectives
- **Improve Skills:** Identify gaps or inefficiencies in existing skill definitions and propose concise updates.
- **Store Preferences:** Capture user preferences, project-specific rules, or recurring instructions in a `CLAUDE.md` file.

## Process
1.  **Analyze:** Review the conversation history, tool calls, and any failures or corrections from the user.
2.  **Identify:** Determine if a specific behavior should be codified in a skill or if a user preference has emerged.
3.  **Propose:** Formulate a single, concise change.
    -   If updating a skill, show a diff of the proposed change.
    -   If adding a preference, show the proposed addition to `CLAUDE.md`.
4.  **Confirm:** Present the proposal to the user and ask for explicit confirmation before applying it.

## Guidelines
- **One at a time:** Only propose one change per invocation to maintain focus and allow for careful review.
- **Conciseness:** Keep changes as brief as possible. Often a few words are enough to clarify a requirement or fix a common mistake.
- **Accuracy:** Ensure the proposal directly addresses a real issue or preference observed in the session.
- **Failure Analysis:** Pay special attention to tool failures or when the user has to correct your approach. These are primary candidates for reflection.
- **Conflict Resolution:** If a proposed change conflicts with details of an existing skill or user preference, propose a resolution that best serves the user's current intent.
