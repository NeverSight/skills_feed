---
name: skill-builder
description: |
  Create new Claude Code skills from procedural knowledge. Invoke PROACTIVELY when:
  - Discovering a reusable workflow pattern worth preserving
  - User asks to "capture this as a skill" or "make this reusable"
  - Recognizing institutional knowledge that should persist
  - After solving a problem in a novel way worth repeating
  - Noticing repeated patterns across sessions
  AUTONOMOUS: Create skills proactively, then inform user what was created.
---

# Skill Builder

Build new Claude Code skills that capture procedural knowledge.

## Autonomy Model

**Create then inform**: When recognizing skill-worthy knowledge, create the skill proactively, then inform the user what was created and why. Don't ask permission first.

## When to Invoke (Proactively)

1. **Successful novel solution** - Just solved something in a way worth repeating
2. **Repeated pattern** - Noticed doing the same thing multiple times
3. **Institutional knowledge** - Learning domain-specific rules that should persist
4. **User workflow** - User demonstrates a process they want automated
5. **Research findings** - Discovered best practices worth preserving

## Quality Gates (Pre-Extraction)

Before creating a skill, verify ALL gates pass:

| Gate | Question | Fail Criteria |
|------|----------|---------------|
| **REUSABLE** | Applies beyond this instance? | One-off solution |
| **NON-TRIVIAL** | Required discovery, not docs lookup? | Just followed documentation |
| **SPECIFIC** | Clear trigger conditions defined? | Vague "sometimes useful" |
| **VERIFIED** | Solution confirmed working? | Theoretical, untested |

If ANY gate fails → Stop. Not skill-worthy.

## Skill Creation Workflow

### 0. Research Best Practices

**Before extracting, search for current patterns:**

```bash
# Use Gemini CLI for web-grounded research
gemini "[technology] [feature] best practices 2026"
gemini "[technology] [problem type] official recommendations"
```

Why: Don't just codify what you did. Incorporate current best practices.
Skip if: Pattern is project-specific internal convention.

### 1. Identify the Knowledge
- What problem does this solve?
- What trigger terms would activate it?
- Is it cross-project or project-specific?

### 2. Draft Structure
Reference `references/structure-guide.md` for ideal anatomy.

### 3. Write Description
Reference `references/description-patterns.md` for trigger-rich descriptions (~100 words, explicit trigger terms).

### 4. Validate
Run `scripts/validate_skill.py <skill-path>` to check structure and frontmatter.

### 5. Inform User
After creating, tell user:
- What skill was created and why
- What triggers will activate it
- How to test it works

## Progressive Disclosure

Keep SKILL.md lean (<100 lines). Put detailed specs in `references/`:
- Detailed examples → `references/examples.md`
- Edge cases → `references/edge-cases.md`
- Anti-patterns → `references/anti-patterns.md`

## Code Opportunities

If skill involves deterministic operations (validation, parsing, extraction), create `scripts/` with executable code rather than prose instructions. Scripts:
- Run without loading into context
- Must be executable (`chmod +x`)
- Should handle errors gracefully

## Skill Locations

- Personal: `~/.claude/skills/` - Available across all projects
- Project: `.claude/skills/` - Shared with team via git

## Template

Use `templates/SKILL-TEMPLATE.md` as starting point for new skills.
