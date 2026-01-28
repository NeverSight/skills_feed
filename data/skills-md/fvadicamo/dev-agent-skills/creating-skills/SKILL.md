---
name: creating-skills
description: Guide for creating Claude Code skills following Anthropic's official best practices. Use when user wants to create a new skill, build a skill, write SKILL.md, or needs skill creation guidelines. Provides structure, naming conventions, description writing, and quality checklist.
---

# Creating Skills

Guide for creating Claude Code skills following Anthropic's official best practices.

## Quick Start

```bash
# 1. Create skill directory
mkdir -p ~/.claude/skills/<skill-name>/references

# 2. Create SKILL.md with frontmatter
cat > ~/.claude/skills/<skill-name>/SKILL.md << 'EOF'
---
name: <skill-name>
description: <what it does>. Use when <trigger phrases>. <key capabilities>.
---

# <Skill Title>

<One-line description>

## Quick Start
<Minimal steps to use the skill>

## Core Workflow
<Step-by-step instructions>

## Important Rules
<Critical constraints and requirements>
EOF

# 3. Add helper scripts if value-add
# 4. Add reference files for detailed docs
```

## SKILL.md Structure

### Frontmatter (REQUIRED)

```yaml
---
name: skill-name          # lowercase, hyphens, no spaces
description: <desc>       # CRITICAL for discovery (max 1024 chars)
---
```

### Description Formula

```
<What it does>. Use when <trigger phrases>. <Key capabilities>.
```

**Example:**
```
Creates GitHub Pull Requests with automated validation. Use when user wants
to create PR, open pull request, or merge feature. Validates tasks, runs
tests, generates Conventional Commits format.
```

**Trigger phrases to include:**
- Action verbs: "create", "handle", "manage", "process"
- User intent: "wants to", "needs to", "asks for"
- Keywords users would say: "PR", "pull request", "review comments"

### Body Sections (ORDER MATTERS)

1. **Title** - `# Skill Name`
2. **One-liner** - Single sentence summary
3. **Quick Start** - Minimal steps (copy-paste ready)
4. **Core Workflow** - Numbered steps with code blocks
5. **Helper Scripts** (if any) - Table with purpose
6. **Important Rules** - Critical constraints (bold **ALWAYS**/**NEVER**)

## Naming Conventions

### Format Options

| Style | Example | When to Use |
|-------|---------|-------------|
| Gerund (verb-ing) | `processing-pdfs` | Action-focused |
| Noun phrase | `github-pr-creation` | Entity-focused |
| Prefixed group | `github-pr-*` | Related skills |

### Rules
- Lowercase only
- Hyphens between words (no underscores)
- No spaces
- Descriptive but concise (2-4 words)

## Token Budget

| Component | Limit | Notes |
|-----------|-------|-------|
| SKILL.md body | < 500 lines | Split if approaching |
| Description | < 1024 chars | Quality over quantity |
| Quick Start | < 30 lines | Minimal viable example |

**If approaching 500 lines:**
1. Move detailed examples to `references/examples.md`
2. Move troubleshooting to `references/troubleshooting.md`
3. Keep SKILL.md focused on workflow

## Helper Scripts Guidelines

### When to Create Scripts

**DO create scripts for:**
- Complex logic (severity classification, commit analysis)
- Multi-step processing with JSON output
- Reusable utilities across invocations

**DON'T create scripts for:**
- Single command wrappers (`gh api ...`)
- Simple operations Claude can do inline
- One-line bash commands

### Script Requirements

```python
#!/usr/bin/env python3
"""Script description."""

import json
import sys

def main():
    # Read from stdin or args
    # Process data
    # Output JSON to stdout
    print(json.dumps(result))

if __name__ == "__main__":
    main()
```

- Output JSON for structured data
- Use stdin/stdout for piping
- Include clear error messages
- Keep focused on single responsibility

## Directory Structure

```
~/.claude/skills/<skill-name>/
├── SKILL.md              # Main skill file (< 500 lines)
├── scripts/              # Optional helper scripts
│   └── helper.py         # Only if value-add
└── references/           # Optional detailed docs
    ├── examples.md       # Extended examples
    └── guide.md          # Deep-dive documentation
```

## Core Principles

### 1. Claude is Already Smart

> "Default assumption: Claude is already very smart. Only add context
> Claude doesn't already have."

**Challenge each line:**
- Does Claude really need this explanation?
- Can I assume Claude knows this?
- Does this paragraph justify its token cost?

### 2. Progressive Disclosure

```
SKILL.md (primary)
    ↓ references/ (when needed)
        ↓ external links (rarely)
```

- Start minimal, expand as needed
- Don't front-load all information
- Let Claude discover details when relevant

### 3. User Confirmation for Critical Actions

```markdown
**ALWAYS** confirm before:
- Modifying files
- Running destructive commands
- Creating external resources (PRs, issues)
```

### 4. Structured Output

Prefer JSON for script output:
```bash
# Good: Structured, parseable
python3 script.py | jq '.result'

# Bad: Unstructured text
python3 script.py | grep "Result:"
```

## Quality Checklist

Before finalizing a skill:

- [ ] **Frontmatter**: name + description present
- [ ] **Description**: includes WHAT + WHEN triggers + capabilities
- [ ] **Naming**: lowercase, hyphens, descriptive
- [ ] **Quick Start**: copy-paste ready, < 30 lines
- [ ] **Line count**: SKILL.md < 500 lines
- [ ] **Scripts**: only value-add, no wrappers
- [ ] **Rules**: critical constraints marked with bold
- [ ] **Test**: skill triggers on expected phrases

## Anti-Patterns to Avoid

| Anti-Pattern | Why Bad | Instead |
|--------------|---------|---------|
| Wrapper scripts | No value-add | Inline commands |
| Explaining basics | Claude already knows | Skip or brief |
| Multiple workflows | Confusing | One clear path |
| Verbose examples | Token waste | Minimal examples |
| Custom systems | Non-standard | Use official patterns |

## Examples

### Good Description
```
Handles PR review comments with severity classification. Use when user
wants to resolve PR comments, handle review feedback, or fix review
comments. Fetches via GitHub CLI, classifies by severity, proposes fixes.
```

### Good Quick Start
```bash
# 1. Get PR number
PR=$(gh pr view --json number -q '.number')

# 2. Fetch and classify comments
gh api repos/{owner}/{repo}/pulls/$PR/comments | \
  python3 ~/.claude/skills/github-pr-review/scripts/classify_comments.py

# 3. Process each comment: show → propose → confirm → apply
# 4. Commit: git commit -m "fix(scope): address review - [desc]"
# 5. Reply and push
```

### Good Important Rules
```markdown
## Important Rules

- **ALWAYS** confirm before modifying files
- **ALWAYS** verify ALL issues in multi-issue comments
- **NEVER** skip user confirmation for file changes
- Group related changes → single commit
```

## References

- `references/official_best_practices.md` - Full Anthropic documentation
- `references/skill_examples.md` - Complete skill examples
