---
name: ask-user-question
description: This skill provides structured question-asking capabilities for gathering user input, clarifying requirements, and making decisions during task execution. Use this skill when needing to present multiple choice questions, gather preferences, or get user confirmation on implementation choices.
---

# Ask User Question

## Overview

This skill enables structured, interactive questioning to gather user input during task execution. It provides a framework for presenting clear questions with predefined options, supporting both single and multiple selection modes.

## When to Use

Invoke this skill when:
- Gathering user preferences or requirements
- Clarifying ambiguous instructions
- Making decisions on implementation choices
- Offering directional choices to the user
- Needing structured input rather than free-form responses

## Question Structure

Each question interaction consists of:

1. **Question**: Clear, specific text ending with a question mark
2. **Header**: Short label (max 12 characters) displayed as a chip/tag
3. **Options**: 2-4 distinct choices, each with label and description
4. **Multi-select flag**: Whether multiple answers are allowed

### Option Components

Each option requires:
- **Label**: Concise display text (1-5 words)
- **Description**: Explanation of what this option means or its implications

## Formatting Guidelines

### Question Text
- Keep questions specific and actionable
- End with a question mark
- If multi-select is enabled, phrase accordingly (e.g., "Which features do you want to enable?")

### Header
- Maximum 12 characters
- Use as category indicator
- Examples: "Auth method", "Library", "Approach", "Feature"

### Option Labels
- Keep concise: 1-5 words
- Make mutually exclusive (unless multi-select)
- Place recommended option first with "(Recommended)" suffix

### Option Descriptions
- Explain implications and trade-offs
- Provide context for informed decisions
- Keep focused and relevant

## Question Templates

### Binary Choice Template
```
Header: "Confirm"
Question: "Do you want to proceed with [action]?"
Options:
  - Label: "Yes, proceed"
    Description: "Continue with the proposed action"
  - Label: "No, cancel"
    Description: "Stop and reconsider alternatives"
```

### Implementation Choice Template
```
Header: "Approach"
Question: "Which implementation approach should be used for [feature]?"
Options:
  - Label: "[Option A] (Recommended)"
    Description: "[Benefits and trade-offs of option A]"
  - Label: "[Option B]"
    Description: "[Benefits and trade-offs of option B]"
  - Label: "[Option C]"
    Description: "[Benefits and trade-offs of option C]"
```

### Feature Selection Template (Multi-select)
```
Header: "Features"
Question: "Which features do you want to enable?"
Options:
  - Label: "[Feature 1]"
    Description: "[What this feature provides]"
  - Label: "[Feature 2]"
    Description: "[What this feature provides]"
  - Label: "[Feature 3]"
    Description: "[What this feature provides]"
MultiSelect: true
```

### Library/Tool Selection Template
```
Header: "Library"
Question: "Which library should be used for [purpose]?"
Options:
  - Label: "[Library A] (Recommended)"
    Description: "[Key characteristics, community support, maintenance status]"
  - Label: "[Library B]"
    Description: "[Key characteristics, use cases, limitations]"
```

## Multiple Questions

When gathering related information, batch up to 4 questions in a single interaction. Each question follows the same structure independently.

### Batching Guidelines
- Group logically related questions
- Maintain independent options per question
- Limit to 4 questions maximum per interaction
- Order questions by dependency (independent first)

## Response Handling

Users can always provide custom input via "Other" option. Design questions to:
- Cover the most common/likely choices
- Allow for unexpected user preferences
- Not force users into predefined boxes

## Best Practices

### Do
- Provide clear context in descriptions
- Order options with recommended first
- Use consistent terminology
- Keep option count manageable (2-4)
- Make each option distinct

### Avoid
- Vague or open-ended questions
- Overlapping options
- Technical jargon without explanation
- Questions answerable through code inspection
- Asking permission to proceed (use ExitPlanMode for plan approval)

## Integration with Plan Mode

When in plan mode:
- Use this skill to clarify requirements BEFORE finalizing plans
- Do NOT use to ask "Is my plan ready?" (use ExitPlanMode instead)
- Focus on gathering information needed for planning decisions

## Examples

### Example 1: Authentication Method Selection
```
Header: "Auth method"
Question: "Which authentication method should we implement?"
Options:
  - Label: "JWT tokens (Recommended)"
    Description: "Stateless authentication with token-based sessions, good for APIs"
  - Label: "Session cookies"
    Description: "Traditional server-side sessions, simpler but requires session storage"
  - Label: "OAuth 2.0"
    Description: "Delegate authentication to external providers (Google, GitHub, etc.)"
```

### Example 2: Database Selection
```
Header: "Database"
Question: "Which database should be used for this project?"
Options:
  - Label: "PostgreSQL (Recommended)"
    Description: "Robust relational database with excellent JSON support"
  - Label: "SQLite"
    Description: "Lightweight, file-based database suitable for smaller applications"
  - Label: "MongoDB"
    Description: "Document-oriented NoSQL database for flexible schemas"
```

### Example 3: Multi-select Features
```
Header: "Features"
Question: "Which optional features should be included?"
Options:
  - Label: "Dark mode"
    Description: "Add theme switching capability with dark color scheme"
  - Label: "Internationalization"
    Description: "Support for multiple languages using i18n framework"
  - Label: "Analytics"
    Description: "Track user behavior and usage patterns"
  - Label: "PWA support"
    Description: "Enable offline functionality and app installation"
MultiSelect: true
```

## Output Format

When using this skill, structure the question presentation as:

```
**[Header]**: [Question]

Options:
1. **[Label]**: [Description]
2. **[Label]**: [Description]
...

[If multi-select: "Select all that apply"]
```

Wait for user response before proceeding with the selected approach.
