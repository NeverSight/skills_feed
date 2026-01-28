---
name: brainstorming
description: "Collaboratively explore ideas and design solutions through guided dialogue before implementation. Use this skill when creating features, building components, adding functionality, designing systems, or when the user says \"brainstorm\", \"design this\", \"help me think through\", or \"let's plan\"."
---

# Brainstorming Ideas Into Designs

## Overview

Help turn ideas into fully formed designs and specs through natural collaborative dialogue.

Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present the design in small sections (200-300 words), checking after each section whether it looks right so far.

## Tool Usage

**ALWAYS use the `AskUserQuestion` tool** when asking questions to the user. This provides a structured interface for gathering input.

- Use `multiSelect: false` for single-choice questions (most common)
- Use `multiSelect: true` when multiple options can be selected together
- Provide 2-4 clear options with descriptions
- Keep the `header` short (max 12 chars) - e.g., "Approach", "Auth type", "Storage"
- **Always include your recommendation**: Put your recommended option first and add "(Recommended)" to the label
- **Always explain why**: In the question text or option descriptions, explain your reasoning for the recommendation

## The Process

**Understanding the idea:**

- Check out the current project state first (files, docs, recent commits)
- Use `AskUserQuestion` to ask one question at a time to refine the idea
- Prefer multiple choice questions when possible, but open-ended is fine too
- Only one question per message - if a topic needs more exploration, break it into multiple questions
- Focus on understanding: purpose, constraints, success criteria

**Exploring approaches:**

- Propose 2-3 different approaches with trade-offs
- Present options conversationally with your recommendation and reasoning
- Lead with your recommended option and explain why

**Presenting the design:**

- Once you believe you understand what you're building, present the design
- Break it into sections of 200-300 words
- Use `AskUserQuestion` after each section to validate (e.g., "Does this section look right?")
- Cover: architecture, components, data flow, error handling, testing
- Be ready to go back and clarify if something doesn't make sense

## Key Principles

- **Use AskUserQuestion tool** - Always use the tool for structured user input
- **Recommend with reasoning** - Every question must include your recommendation and why
- **One question at a time** - Don't overwhelm with multiple questions
- **Multiple choice preferred** - Easier to answer than open-ended when possible
- **YAGNI ruthlessly** - Remove unnecessary features from all designs
- **Explore alternatives** - Always propose 2-3 approaches before settling
- **Incremental validation** - Present design in sections, validate each
- **Be flexible** - Go back and clarify when something doesn't make sense
