---
name: rules-capture
description: Automatically detects and documents user preferences, coding rules, and style guidelines when expressed during conversations
version: 1.0.0
tags:
  - preferences
  - rules
  - documentation
  - automation
---

# Rules Capture Skill

This skill automatically detects when users express preferences, rules, or coding standards during conversations and documents them for future sessions.

---

## When This Skill Activates

Automatically activate when the user mentions ANY of these:

### Direct Rule Expressions

- "always do X" / "never do X"
- "I prefer X" / "I don't like X"
- "don't ever X" / "stop doing X"
- "from now on X" / "going forward X"
- "that's not how we do it" / "we do it this way"
- "the rule is X" / "the standard is X"

### Coding Style Expressions

- "use X pattern" / "don't use X pattern"
- "name things like X" / "format like X"
- "import from X" / "don't import from X"
- "the convention is X"
- "follow the X pattern"

### Frustration Indicators (Capture these especially!)

- "why did you X" / "stop doing X"
- "I told you before" / "I already said"
- "that's wrong" / "that's not right"
- "fix this" / "change this"
- Any profanity + instruction (strong signal!)

### Questions About Standards

- "what's the rule for X" / "how should I X"
- "is it X or Y" / "which way is correct"
- "what's the coding style for X"

---

## Capture Process

When a rule/preference is detected:

### 1. Acknowledge Detection

```
I noticed you expressed a preference/rule. Let me capture this.
```

### 2. Extract Rule Details

Parse the user's statement to identify:

- **Category**: What area does this apply to? (coding, naming, imports, patterns, tools, communication)
- **Rule Type**: ALWAYS, NEVER, PREFER, AVOID
- **Specific Action**: What exactly should/shouldn't be done
- **Context**: When does this apply
- **Example**: Good vs bad example if mentioned

### 3. Document to Capture File

Append to `.agent/SYSTEM/CAPTURED-RULES.md`:

````markdown
### [YYYY-MM-DD HH:MM] - [Category]: [Short Title]

**User said:**

> "[Exact quote from user]"

**Rule extracted:**

- **Type**: [ALWAYS | NEVER | PREFER | AVOID]
- **Action**: [What to do/not do]
- **Context**: [When this applies]
- **Category**: [coding | naming | imports | patterns | tools | communication | workflow]

**Example:**

```[language]
// Good
[good example]

// Bad
[bad example]
```
````

**Status**: PENDING_REVIEW

```

### 4. Confirm with User
```

Captured this rule:

- [Brief summary of the rule]

Should I add this to the permanent rules? [Yes/No/Modify]

````

### 5. On Confirmation
- Move to `USER-PREFERENCES.md` under appropriate section
- Or create new section in `RULES.md` if it's a coding standard
- Remove from `CAPTURED-RULES.md` (or mark as PROCESSED)

---

## Rule Categories

### Coding Rules
- Pattern preferences
- Import conventions
- Naming conventions
- File structure
- Component patterns

### Workflow Rules
- Build/test preferences
- Git workflow
- Documentation requirements
- Communication style

### Tool Rules
- CLI preferences
- IDE settings
- Terminal behavior
- Background processes

### Communication Rules
- Response style
- Verbosity preferences
- Explanation depth
- Acknowledgment patterns

---

## Storage Locations

| Rule Type | Storage Location |
|-----------|------------------|
| Personal preferences | `../.agent/SYSTEM/ai/USER-PREFERENCES.md` |
| Coding standards | `.agent/SYSTEM/RULES.md` |
| Critical rules | `../.agent/SYSTEM/critical/CRITICAL-NEVER-DO.md` |
| Pending review | `../.agent/SYSTEM/CAPTURED-RULES.md` |

---

## Auto-Capture File Format

File: `../.agent/SYSTEM/CAPTURED-RULES.md`

```markdown
# Captured Rules - Pending Review

Rules automatically captured from conversations. Review and promote to permanent docs.

---

## Pending Rules

[Auto-captured rules appear here]

---

## Processed Rules

[Rules that have been promoted to permanent docs]
````

---

## Integration with Other Skills

This skill works with:

- **docs**: For formatting captured rules properly
- **session-documenter**: Rules captured during session are included in session docs

---

## Cleanup Command

When user says "clean up rules" or "process captured rules":

1. Read `CAPTURED-RULES.md`
2. Present each pending rule for review
3. User can: Approve, Modify, Delete
4. Approved rules get promoted to permanent docs
5. File is cleaned up

---

## Example Interaction

**User**: "stop using console.log for debugging, use the logger service"

**Claude**:

```
I noticed a new rule. Let me capture it:

Rule: Use logger service instead of console.log for debugging
Category: Coding
Type: NEVER (console.log) / ALWAYS (logger service)

Added to captured rules. Should I promote this to permanent coding rules?
```

---

## Activation Triggers

The skill activates on these regex patterns:

```regex
# Direct commands
(always|never|don't|stop|from now on|going forward)\s+.+
(prefer|like|want|need)\s+(you to|it to|this to)\s+.+
(the rule is|the standard is|the convention is)\s+.+

# Frustration signals
(why (did|do) you|stop doing|I told you|I already said)\s+.+
(that's (wrong|not right|incorrect)|fix this|change this)\s+.+

# Questions about standards
(what's the (rule|standard|convention) for|how should I|which way is)\s+.+
```

---

**When this skill is active**, you will automatically capture and document any rules, preferences, or standards the user expresses, ensuring nothing is forgotten between sessions.
