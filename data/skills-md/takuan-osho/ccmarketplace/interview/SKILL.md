---
name: interview
description: Conduct structured interviews to gather requirements, clarify specifications, or understand context. This skill should be used when starting a new task that requires understanding user intent, requirements, technical specifications, or context. It supports various interview types including requirements definition, debugging investigation, architecture review, and general information gathering.
---

# Interview

## Overview

This skill provides a structured interview framework to systematically gather information before starting work. It helps reduce ambiguity, ensure comprehensive understanding, and produce actionable outputs. The interview adapts to different contexts: requirements definition, debugging, architecture decisions, security review, and more.

## When to Use

- Starting a new feature implementation
- Investigating bugs or issues
- Reviewing architecture or security
- Creating documentation or reports
- Any task requiring clarification of scope, constraints, or expectations

## Workflow

### Phase 1: Preparation (Silent)

Before asking questions, gather background context silently.

> **Parallel Fan-Out Pattern**: The following three preparation tasks have no dependencies on each other and SHOULD be executed in parallel. This reduces Phase 1 completion time by approximately 66%.
>
> Reference: [Google ADK Multi-Agent Patterns](https://google.github.io/adk-docs/agents/multi-agents/)

**Codebase Exploration:** *(parallel task 1/3)*
- Project structure - Identify key directories, config files, entry points
- Recent changes - Check git history if applicable
- Related code - Search for relevant patterns or implementations

**Documentation Review:** *(parallel task 2/3)*
- Read any referenced files or URLs provided by user
- Check for existing specifications, ADRs, or design documents
- Review related issues or PRs if applicable

**Web Research (if applicable):** *(parallel task 3/3)*
- Best practices for the domain
- Similar implementations or patterns
- Security considerations

For detailed exploration commands per environment (Claude Code, Codex, API), see `references/exploration-patterns.md`.

### Phase 2: Interview

Conduct the interview in stages, adapting questions based on interview type.

#### Stage 1: Goal Confirmation

Start by confirming the overall objective:

**Environment-specific approach:**
- **Claude Code**: Use AskUserQuestion tool for structured choices
- **Other environments**: Present numbered options and ask user to reply with number or description

**Core Questions:**
- What is the primary goal or outcome expected?
- Who are the stakeholders or users affected?
- What does success look like?

**Interview Type Selection:**

Ask the user to select the interview type to tailor subsequent questions:

| Type | Use Case |
|------|----------|
| Requirements | New feature, specification, API design |
| Investigation | Bug analysis, performance issue, incident |
| Architecture | Design review, technology selection, refactoring |
| Security | Security audit, vulnerability assessment |
| Documentation | Report creation, knowledge transfer |
| General | Open-ended exploration, brainstorming |

#### Stage 2: Deep Dive

Based on the selected interview type, ask targeted questions.

For detailed question frameworks and output templates per interview type, read `references/interview-types.md`.

#### Stage 3: Confirmation and Prioritization

Before concluding:

1. **Summarize Understanding** - Restate key points for confirmation
2. **Identify Gaps** - Note any undecided or unclear items
3. **Prioritize** - Classify requirements as Must/Should/Could
4. **Confirm Scope** - Agree on what is in/out of scope

### Deep Dive Strategies

Use these techniques to reduce ambiguity:

| Technique | When to Use |
|-----------|-------------|
| "Specifically?" | When details are vague |
| "Why?" | When motivation is unclear |
| "What else?" | When list seems incomplete |
| "For example?" | When concept needs illustration |
| "What if...?" | When edge cases need exploration |

### Phase 3: Output

Generate a structured summary document.

#### Output Template

```markdown
# [Interview Type]: [Topic]

## Summary
[1-2 sentence overview]

## Goal
- **Objective**: [Primary goal]
- **Stakeholders**: [Who is affected]
- **Success Criteria**: [How to measure success]

## Requirements / Findings
### Must Have
- [Item 1]
- [Item 2]

### Should Have
- [Item 1]

### Could Have
- [Item 1]

## Constraints
- [Technical constraints]
- [Business constraints]
- [Timeline constraints]

## Undecided / Open Questions
- [ ] [Question 1]
- [ ] [Question 2]

## Next Steps
1. [Action item 1]
2. [Action item 2]

## References
- [Link or file reference 1]
- [Link or file reference 2]

## Affected Files / Components
- `path/to/file1`
- `path/to/file2`
```

## Usage Examples

For detailed usage examples with sample outputs, see `references/usage-examples.md`.

Quick reference:
- `/interview Add user authentication` → Requirements interview
- `/interview Investigate 504 errors` → Investigation interview
- `/interview Review database schema` → Architecture interview

## Guidelines

1. **Adapt to Context** - Adjust question depth based on task complexity
2. **Avoid Overwhelming** - Ask 2-3 questions at a time, not all at once
3. **Be Specific** - Reference actual code, files, or examples when possible
4. **Document Everything** - Capture decisions and their rationale
5. **Identify Gaps Early** - Surface undecided items for follow-up
6. **Output Language** - Follow user's language preference (check conversation history)

## User Input Methods

### Claude Code Environment

Use the AskUserQuestion tool for structured choices:

```
Question: "What type of interview is this?"
Header: "Type"
Options:
  - "Requirements (Recommended)" - New feature or specification
  - "Investigation" - Bug or issue analysis
  - "Architecture" - Design or technology review
  - "Security" - Security assessment
```

This enables efficient selection with clickable options.

### Other Environments (Codex, API, etc.)

Present numbered options in plain text and wait for user response:

```
What type of interview is this?

1. Requirements - New feature or specification (Recommended)
2. Investigation - Bug or issue analysis
3. Architecture - Design or technology review
4. Security - Security assessment
5. Documentation - Report creation, knowledge transfer
6. General - Open-ended exploration

Please reply with a number (1-6) or describe your needs:
```

Wait for the user's response before proceeding. Accept both:
- Number selection (e.g., "1", "2")
- Free-form description (e.g., "I need to investigate a performance issue")
