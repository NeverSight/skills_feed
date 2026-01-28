---
name: skill-capture
description: Extracts valuable learnings, patterns, and workflows from conversations and persists them as reusable skill files. This skill should be used when a complex problem was solved, a valuable workflow was discovered, or the user explicitly requests to capture knowledge as a skill.
version: 1.0.0
tags:
  - skills
  - capture
  - automation
  - knowledge-management
---

# Skill Capture

This skill extracts valuable learnings, patterns, and workflows from conversations and persists them as reusable skill files for future sessions.

---

## When This Skill Activates

Activate when the user mentions ANY of these:

### Explicit Requests

- "let's save this as a skill"
- "this workflow should be reusable"
- "capture this as a skill"
- "make this a skill"
- "turn this into a skill"
- "save this pattern"

### Workflow Completion Signals

- Complex problem solved after multiple iterations
- Multi-step procedure successfully executed
- Valuable domain knowledge discovered through research
- Code pattern emerged that could benefit other projects

### Learning Moments

- "this was tricky to figure out"
- "glad we finally got this working"
- "I wish I knew this earlier"
- "this should be documented"

---

## Capture Process

Follow these 5 phases in order:

### Phase 1: Identification

Review the conversation to identify capturable content:

**What to Look For:**

| Category | Example |
|----------|---------|
| Workflows | Multi-step procedures that took iterations to perfect |
| Domain Knowledge | Information requiring research or expertise |
| Problem Solutions | Approaches that resolved complex issues |
| Code Patterns | Reusable patterns that could help other projects |
| Decision Rationale | Architectural choices with clear reasoning |

**Questions to Ask:**

- Is this generalizable beyond this specific project?
- Would another Claude instance benefit from this knowledge?
- Did this require multiple iterations to get right?
- Is this non-obvious procedural knowledge?

### Phase 2: Destination Planning

Determine where the skill should live:

```
1. Check if an existing skill should be updated
   - Glob for skills/*/SKILL.md
   - Read related skills to check for overlap

2. If creating new skill:
   - Choose descriptive kebab-case name
   - Create in skills/<skill-name>/ directory
```

**Skill vs. Rule Decision:**

| Create a Skill | Capture a Rule |
|----------------|----------------|
| Workflow with multiple steps | Single preference statement |
| Procedural knowledge | "always/never do X" |
| Domain expertise | Style/format preferences |
| Code patterns with context | Import/naming conventions |

If it's a rule/preference, delegate to `rules-capture` skill instead.

### Phase 3: Content Drafting

Transform conversational insights into SKILL.md format:

```markdown
---
name: <skill-name>
description: <One sentence describing what the skill does and when to use it>
version: 1.0.0
tags:
  - <relevant>
  - <tags>
---

# <Skill Title>

<Brief description of the skill's purpose>

---

## When to Use

<Clear triggers for when this skill should activate>

---

## Process

<Step-by-step workflow or procedure>

---

## Examples

<Concrete examples showing the skill in action>

---

## Integration

<How this skill works with other skills, if applicable>
```

### Phase 4: Distillation

Extract and refine the content:

1. **Extract the Final Approach** - Capture only what worked, not the failed attempts
2. **Generalize** - Remove project-specific details that don't apply broadly
3. **Add Context** - Explain why certain approaches work, not just what to do
4. **Include Examples** - Add concrete examples that demonstrate usage

**Checklist:**

- [ ] Removed project-specific paths and names
- [ ] Generalized any hardcoded values
- [ ] Added explanatory context for non-obvious steps
- [ ] Included both good and bad examples where helpful
- [ ] Kept language in imperative form

### Phase 5: Verification

Ensure the skill is ready for use:

**Quality Checks:**

| Check | Requirement |
|-------|-------------|
| Length | Under 500 lines (use references/ for large content) |
| Frontmatter | Valid YAML with name and description |
| Completeness | All sections have meaningful content |
| Actionability | Instructions are specific enough to follow |
| Formatting | Follows library patterns (see rules-capture for reference) |

**Validation:**

```bash
# Run the package script to validate
scripts/package_skill.py skills/<skill-name>
```

---

## What to Capture

### Good Candidates

- Workflows that took multiple iterations to get right
- Domain knowledge that required research
- Problem-solving approaches that worked
- Code patterns that could be reused across projects
- Decision rationale for architectural choices
- Integration patterns between tools or services
- Debugging approaches for specific technologies

### Anti-Patterns (Do NOT Capture)

- One-off solutions specific to a single project
- Trivial fixes or obvious patterns
- Information already documented elsewhere
- Sensitive or proprietary information
- Incomplete workflows still being refined
- Preferences without procedural value (use rules-capture instead)

---

## Output Structure

Create two files for each skill:

### SKILL.md

See Phase 3 template above. Key principles:

- Use imperative form ("Do X" not "You should do X")
- Be specific about triggers and activation conditions
- Include concrete examples
- Reference any bundled resources

### plugin.json

```json
{
  "name": "<skill-name>",
  "version": "1.0.0",
  "description": "<Same description as SKILL.md frontmatter>",
  "author": {
    "name": "Ship Shit Dev",
    "email": "hello@shipshit.dev",
    "url": "https://github.com/shipshitdev"
  },
  "license": "MIT",
  "skills": "."
}
```

---

## Integration

This skill works with:

| Skill | Integration |
|-------|-------------|
| `rules-capture` | Delegates preference capture; handles skill creation |
| `session-documenter` | Skills captured during session are noted |
| `skill-creator` | Uses creation patterns and validation |
| `docs` | For formatting help with SKILL.md |

---

## Example Interaction

**Context**: User spent 30 minutes debugging a NestJS queue integration issue. The solution involved specific configuration patterns.

**User**: "This was a pain to figure out. Let's save this for next time."

**Claude**:

```
I'll capture this as a skill. Let me analyze what we learned:

Capturable Knowledge:
- NestJS Bull queue configuration pattern
- Redis connection handling for queues
- Processor registration requirements

This would make a good standalone skill or could extend `nestjs-queue-architect`.

Let me check the existing skill...
[Reads skills/nestjs-queue-architect/SKILL.md]

The existing skill covers queue setup but not this specific debugging pattern.
I'll add a new "Troubleshooting" section.

Created: skills/nestjs-queue-architect/SKILL.md (updated)
- Added troubleshooting section
- Documented Redis connection requirements
- Added common error patterns

Should I also create session documentation for this debugging session?
```

---

## Activation Triggers

The skill activates on these patterns:

```regex
# Explicit capture requests
(save|capture|turn|make).*(skill|reusable|pattern)
(this should be|let's make this).*(skill|documented|reusable)

# Workflow completion signals
(finally|glad).*(working|figured|solved)
(this was|that was).*(tricky|hard|difficult|complex)
(multiple|several).*(iterations|attempts|tries)

# Learning signals
(wish I knew|should have known|next time|for future)
```

---

**When this skill is active**, automatically identify valuable knowledge from the conversation and offer to persist it as reusable skills for future sessions.
