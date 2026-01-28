---
name: Skill Builder
description: Create and validate Agent Skills with proper structure and effective descriptions. Use when building custom skills, testing skill discovery, or designing new skill workflows.
---

# Skill Builder

Create focused, discoverable Agent Skills that solve specific problems with clear descriptions and progressive disclosure patterns.

## Workflow

### 1. Design the Skill

Before building, clarify:

- **What**: What specific problem does this skill solve?
- **When**: What triggers would tell Claude to use it? (3-5 concrete phrases)
- **Scope**: Single capability or multiple related features?
- **Location**: Personal (`~/.claude/skills/`) or project (`.claude/skills/`)?

**Example**:

- What: "Generate clear commit messages from git diffs"
- When: "user wants to create a commit", "reviewing staged changes", "explaining code changes"
- Scope: Single capability (commit messages only, not other git tasks)
- Location: Personal (useful across projects)

### 2. Write the Description

Description formula: `<What it does>. Use when <trigger> or <trigger> or <trigger>`

**Good**: "Generate clear commit messages from git diffs. Use when creating commits, reviewing staged changes, or explaining what changed in your code."

**Weak**: "Helps with git" (too vague, no triggers)

**Effective trigger words**:

- Action verbs: extract, analyze, generate, review, validate, debug, migrate
- File types: PDF, .xlsx, Python files, YAML
- Domain terms: commits, staging, forms, spreadsheets, SwiftUI

**Length**: Name max 64 chars, Description max 1024 chars

### 3. Create Directory Structure

For minimal skills (single focused task):

```text
my-skill/
└── SKILL.md
```

For skills needing supporting files:

```text
my-skill/
├── SKILL.md              (main instructions - keep <200 lines)
└── REFERENCE.md          (detailed patterns, examples)
```

### 4. Write the SKILL.md

**Minimal template** (under 200 lines):

```markdown
---
name: Your Skill Name
description: What it does and when to use. [Include 3-5 trigger phrases]
---

# Your Skill Name

## Quick Start

[One-paragraph overview of what this skill does]

## Instructions

1. Understand the requirement: [Ask clarifying questions]
2. [Core step with specific approach]
3. [Next step]
4. [Final step with verification]

## Examples

[2-3 concrete, realistic examples]

## Best Practices

- Do X in situation Y
- Avoid Z because...
- Use this pattern when...
```

### 5. Validate Skill Quality

**Structure checklist**:

- [ ] YAML frontmatter valid (--- on line 1 and before content)
- [ ] `name` under 64 characters
- [ ] `description` under 1024 characters
- [ ] `description` includes 3-5 trigger phrases and covers "what" + "when"
- [ ] Markdown syntax correct (# for headers, ``` for code blocks)
- [ ] All referenced files exist in skill directory

**Discovery checklist**:

- [ ] Description could NOT describe a different skill
- [ ] Trigger words match how users actually phrase problems
- [ ] 3-5 concrete terms, not generic language
- [ ] Clear distinction from related skills

**Functionality checklist**:

- [ ] Instructions are step-by-step and clear
- [ ] Examples are concrete, not abstract
- [ ] Edge cases or limitations documented
- [ ] Workflow is focused on single capability

### 6. Test Discovery

Generate 2-3 natural prompts matching your description:

**For "Commit Message Generator"**:

- ✅ "Write a commit message for these staged changes"
- ✅ "Help me create a clear git commit"
- ✅ "I need to describe what I just changed"
- ❌ "Analyze my code" (wrong skill territory)

**For "SwiftUI Engineer"**:

- ✅ "Review my SwiftUI code for anti-patterns"
- ✅ "Debug this view rendering issue"
- ✅ "Help me migrate this from AppKit to SwiftUI"
- ❌ "Write Python code" (wrong domain)

### 7. Common Patterns

**Single-capability skill**: One specific task (commit messages, PDF extraction)

**Multi-mode skill**: Related capabilities under one umbrella

- SwiftUI Engineer: architecture, review, debugging, modernization
- Keep main file 150-200 lines, use REFERENCE.md for detailed patterns
- Main file explains "what mode to use when"

## Structure Reference

### Minimal Single-File

Use when: Focused skill with simple instructions

```text
skill/
└── SKILL.md (100-150 lines)
```

### With Progressive Disclosure

Use when: Related capabilities or lots of examples

```text
skill/
├── SKILL.md (150-200 lines with quick patterns)
└── REFERENCE.md (300-400 lines with detailed examples and TOC)
```

## Key Principles

**Focused scope**: One skill = one primary capability or related group

**Specific triggers**: Include domain terms users actually say

**Progressive disclosure**: Load details only when needed (use REFERENCE.md)

**Concrete examples**: Show real scenarios, not abstract ideas

**One-level references**: All references point from SKILL.md to supporting files only

**No duplication**: Don't repeat patterns across skills

## Anti-Patterns to Avoid

❌ **Overloaded**: "Does commits, reviews code, analyzes data, generates docs..."
→ Split into separate focused skills

❌ **Vague triggers**: "Helps with stuff", "General purpose"
→ Add 3-5 specific domain terms

❌ **Nested references**: SKILL.md → REFERENCE.md → DETAILS.md
→ Keep references flat (only one level deep)

❌ **Marketing language**: "Amazing tool for awesome results!"
→ Be specific about what it does

## When to Iterate

If Claude doesn't use your skill when expected:

1. Check YAML syntax first (most common issue)
2. Add more specific trigger words to description
3. Verify description covers both "what" AND "when"
4. Test with natural language phrasings
5. Make sure trigger words match user vocabulary
