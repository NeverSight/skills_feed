---
name: brainstorming
description: "You MUST use this skill before any creative or complex work. Explores user intent, requirements and design before actually executing on the task."
---

# Brainstorming Ideas Into Specs

## Overview

Help turn ideas into fully formed designs or specs through natural collaborative dialogue.

Start by understanding the current project context in the project's root directory, then ask questions one at a time to refine the idea. Once you understand what you're creating, present the specs in small sections (200-300 words), checking after each section whether it looks right so far.

## The Process

**Understanding the idea:**
- Check out the current project state first (files, docs, recent git commits) using subagent(s) to minimize LLM token usage
- Ask questions one at a time to refine the idea
- Prefer multiple choice questions when possible, but open-ended is fine too
- Only one question per message - if a topic needs more exploration, break it into multiple questions
- Only ask questions where the answer cannot be easily inferred from the project context, etc.
- Focus on understanding: purpose, constraints, success criteria

**Exploring approaches:**
- Propose 2-3 different approaches with trade-offs
- Present options conversationally with your recommendation and reasoning
- Lead with your recommended option and explain why

**Presenting the specs:**
- Once you believe you understand what you're building, present the specs
- Break it into sections of 200-300 words
- Ask after each section whether it looks right so far
- Cover all important aspects: 
  - for coding projects: architecture, components, data flow, performance, security, multithreading / async processing, error handling, testing
  - for non-coding projects: confirm the list of aspects to cover with the user
- Be ready to go back and clarify if something doesn't make sense

## After the Specs

**Documentation:**
- Write the validated specs to `docs/YYYY-MM-DD-<topic>-specs.md`

**Detailed Execution Plan (if continuing):**
- Ask: "Ready to continue with a detailed task breakdown?"
- Use the task-breakdown skill to create detailed task breakdown

## Key Principles

- **One question at a time** - Don't overwhelm with multiple questions
- **Multiple choice preferred** - Easier to answer than open-ended when possible
- **YAGNI ruthlessly** - Remove unnecessary features from all designs
- **Explore alternatives** - Always propose 2-3 approaches before settling
- **Incremental validation** - Present specs in sections, validate each
- **Be flexible** - Go back and clarify when something doesn't make sense
- **AskUserQuestion tool** - must use this tool to ask questions to the user