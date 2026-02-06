---
name: interview
description: "Interview user in-depth to create a detailed spec. Use when user wants to define requirements, spec out a feature, or needs help articulating product details."
argument-hint: [topic/instructions]
allowed-tools: AskUserQuestion, Write, Task
---

# Interview for Specification

## Phase 1: Exploration

Before asking any questions, use the Task tool with `subagent_type=Explore` to do a deep-dive on the codebase and understand how the topic in the instructions works. Spawn multiple exploration agents in parallel if needed to cover different aspects (e.g., data flow, UI components, state management, related systems).

Once the exploration is complete, present a **full exhaustive summary** to the user covering:
- How the feature/system currently works
- Key files and their responsibilities
- Data flow and state management
- Dependencies and integrations with other systems
- Any existing patterns or conventions used

## Phase 2: Interview

After presenting the summary, interview me in detail using the AskUserQuestion tool about literally anything: technical implementation, UI & UX, concerns, tradeoffs, etc. but make sure the questions are not obvious. Leverage your exploration findings to ask informed, specific questions rather than generic ones. Be very in-depth and continue interviewing me continually until it's complete.

## Phase 3: Specification

Once the interview is complete, write the spec to a file.

<instructions>$ARGUMENTS</instructions>
