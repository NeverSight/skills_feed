---
name: writing
description: DEPRECATED - Use writing-skills instead. Writing style guidelines have been merged into writing-skills.
version: 1.0.1
deprecated: true
superseded_by: writing-skills
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash]

best_practices:
  - Use writing-skills instead of this skill
error_handling: graceful
streaming: supported
---

# Writing Skill (DEPRECATED)

> **DEPRECATION NOTICE**
>
> This skill has been merged into `writing-skills`. Please use `writing-skills` instead.
>
> ```javascript
> Skill({ skill: 'writing-skills' });
> ```
>
> The writing style guidelines from this skill are now available in the "Writing Style Guidelines" section of `writing-skills`.

## Redirect

For writing style guidelines (voice, tone, banned words, punctuation), use:

```javascript
Skill({ skill: 'writing-skills' });
```

The `writing-skills` skill now includes:

1. TDD methodology for creating skills
2. Writing style guidelines (merged from this skill)
3. Claude Search Optimization (CSO)
4. Skill testing patterns

## Original Content (Archived)

The original writing guidelines have been preserved in `writing-skills` under the "Writing Style Guidelines" section.

Key content migrated:

- Voice and tone guidelines
- Specificity and evidence rules
- Banned words and phrases
- LLM pattern avoidance
- Punctuation and formatting

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:** Record any new patterns or exceptions discovered.

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
