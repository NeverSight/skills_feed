---
name: improve-skill
description: |
  Improve an existing skill based on conversation context and user feedback. Use when:
  (1) User says "/improve-skill <skill-name>" or "improve the skill" after using a skill
  (2) User wants to refine a skill based on corrections made during conversation
  (3) User provides specific feedback about what a skill should do differently
  (4) User wants to make a skill more tailored to their preferences or workflow

  This skill analyzes the conversation history to identify course corrections, misunderstandings,
  and user preferences, then updates the target skill's SKILL.md and resources accordingly.
---

# Improve Skill

Improve an existing skill based on conversation context and user feedback.

## Inputs

- **skill-name** (required): Name of the skill to improve (e.g., "frontend-design", "pdf-editor")
- **user-input** (optional): Specific instructions on what to improve or focus on

## Workflow

### 1. Parse Input

Extract the skill name and any additional user instructions from the command arguments.

If no skill name is provided, ask the user which skill they want to improve.

### 2. Locate the Skill

Search for the skill in common locations:
1. `~/.claude/skills/<skill-name>/SKILL.md`
2. Project-local `.claude/skills/<skill-name>/SKILL.md`
3. If not found, ask the user for the skill's location

### 3. Read Current Skill

Load and understand the current skill's:
- SKILL.md content (frontmatter + body)
- Any bundled resources (scripts/, references/, assets/)

### 4. Analyze Conversation Context

Review the conversation history to identify:

**Course corrections**: Places where the user said things like:
- "No, I meant..."
- "That's not what I wanted"
- "Actually, do it this way instead"
- "You misunderstood"
- "Please change..."
- "That's wrong because..."

**Repeated patterns**: Things the user consistently:
- Asked for that weren't in the skill
- Had to clarify multiple times
- Preferred over the default approach

**Explicit preferences**: User statements about:
- Preferred formats, styles, or conventions
- Specific requirements for their workflow
- Things they always/never want

### 5. Synthesize Improvements

Based on analysis, determine what changes to make:

**Frontmatter changes**:
- Update description if trigger conditions should change
- Add missing use cases

**Body changes**:
- Add missing instructions or workflows
- Clarify ambiguous sections
- Add user-specific preferences
- Include examples that match user's actual usage
- Remove or modify instructions that led to incorrect behavior

**Resource changes**:
- Update scripts if they produced wrong output
- Add new references for missing domain knowledge
- Modify assets/templates to match preferences

### 6. Present Proposed Changes

Before making changes, show the user:
1. Summary of identified issues from conversation
2. Proposed changes to the skill
3. Ask for confirmation or additional feedback

Format:
```
## Identified Issues

Based on our conversation, I found these areas for improvement:

1. [Issue description] - [Where in skill this relates to]
2. ...

## Proposed Changes

### SKILL.md
- [Change 1]
- [Change 2]

### [Other files if applicable]
- [Change description]

Should I apply these changes? Any adjustments needed?
```

### 7. Apply Changes

After user confirmation:
1. Edit the SKILL.md file with improvements
2. Update any bundled resources as needed
3. Show a diff or summary of what changed

### 8. Suggest Testing

Recommend the user test the improved skill:
```
The skill has been updated. To test the improvements, try using
/<skill-name> with a similar request to see if it better matches
your expectations.
```

## Guidelines

### Preserve Skill Intent

- Don't fundamentally change what the skill does
- Add specificity without breaking generality for other use cases
- If changes would only apply to one user's context, consider noting them as "preferences" rather than hard rules

### Be Conservative

- Only make changes clearly supported by the conversation
- When uncertain, ask the user rather than guess
- Prefer adding clarifying examples over rewriting instructions

### Maintain Skill Quality

- Keep SKILL.md concise (under 500 lines)
- Follow progressive disclosure - move detailed content to references/
- Ensure frontmatter description remains comprehensive for triggering

### Handle Edge Cases

**No conversation context**: If invoked without prior conversation about the skill:
- Ask user what they'd like to improve
- Offer to review the skill and suggest potential improvements

**Skill not found**:
- List available skills
- Ask user to confirm the skill name or provide path

**User provides only general feedback** (e.g., "make it better"):
- Ask clarifying questions about what specifically isn't working
- Offer to analyze the skill and suggest improvements

## Example Usage

**After a conversation where the user corrected output format multiple times:**

User: `/improve-skill frontend-design`

Agent analyzes conversation, finds user repeatedly asked for Tailwind instead of vanilla CSS.

Agent response:
```
## Identified Issues

Based on our conversation, I found these areas for improvement:

1. CSS Framework - You corrected me 3 times to use Tailwind CSS instead
   of vanilla CSS. The skill doesn't specify a preferred CSS approach.

2. Component Structure - You preferred single-file components over
   splitting into multiple files.

## Proposed Changes

### SKILL.md
- Add instruction: "Default to Tailwind CSS for styling unless user
  specifies otherwise"
- Add instruction: "Prefer single-file components unless complexity
  requires splitting"

Should I apply these changes?
```

**With specific user input:**

User: `/improve-skill pdf-editor focus on the rotation script, it keeps failing on large files`

Agent reads the script, identifies the issue, and proposes a fix to handle large files better.
