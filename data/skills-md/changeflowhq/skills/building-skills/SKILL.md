---
name: building-skills
description: |
  Create, restructure, and validate Claude Code skills following best practices.
  Handles directory structure, YAML frontmatter, progressive disclosure, credential
  management, self-learning with consolidation, and script organization.
  Use when creating new skills, restructuring existing skills, reviewing skills for
  quality, or asking about skill structure, patterns, or best practices.
allowed-tools: Bash Read Write Edit
---

# Building Skills

Read [LEARNED.md](LEARNED.md) before building or reviewing any skill.

## Core Principles

### 1. Context Window is Sacred

Skills share context with system prompt, conversation history, other skills, and the user's request. Only add what Claude doesn't already know.

**For every line ask:** Does this justify its token cost? If Claude knows it, cut it.

### 2. Progressive Disclosure

Skills load in three stages. Design for this.

| Stage | What loads | Budget | Contains |
|-------|-----------|--------|----------|
| Discovery | `name` + `description` | ~100 tokens | Trigger keywords, when to use |
| Activation | SKILL.md body | <5000 tokens | Instructions, workflows, quick start |
| Execution | references/, scripts/ | As needed | Detailed docs, executable code |

**Critical:** The `description` field is the trigger mechanism. All "when to use" info goes there, not the body. The body only loads AFTER triggering.

### 3. Degrees of Freedom

Match instruction specificity to how fragile the task is:

- **High freedom** (text guidance): Creative tasks, multiple valid approaches. "Write a blog post following these guidelines."
- **Medium freedom** (parameterized scripts): Preferred pattern exists but adapts. "Run the audit script, interpret results."
- **Low freedom** (exact scripts, few params): Fragile operations, API calls, deploys. "Run exactly: `python scripts/deploy.py --env prod`"

### 4. Self-Learning is Mandatory

Every skill MUST have `LEARNED.md` with consolidation rules. No exceptions.

## Required Structure

```
skill-name/
├── SKILL.md           # Required. <500 lines. Core instructions.
├── LEARNED.md         # Required. <50 lines. Dated entries + consolidation.
├── scripts/           # Executable code. Runs but never loaded into context.
├── references/        # Detailed docs. Loaded into context on demand (costs tokens).
├── setup/             # Credential templates, setup instructions.
└── assets/            # Files used in output (templates, icons). Never loaded into context.
```

**Key distinction:** `references/` costs tokens when read. `scripts/` and `assets/` don't - scripts execute and return output, assets are used in generated files. Put large docs, templates, and data in assets/ not references/.

## Frontmatter

```yaml
---
name: skill-name
description: |
  Third person. WHAT it does + WHEN to use it + trigger keywords.
  This is the primary trigger. Max 1024 chars. No angle brackets.
allowed-tools: Bash Read Write
---
```

**name:** kebab-case, max 64 chars, no consecutive/leading/trailing hyphens. Must match directory name.

**description:** The most important field. Claude reads ALL descriptions to decide which skill to trigger. Front-load trigger conditions. Include keywords users would actually say. Bad: "Manages Google Ads." Good: "Control Google Ads via official API. Create, pause, optimize campaigns, ads, keywords, bids. Run audits. Use when user mentions Google Ads, PPC, AdWords, Quality Score, or ad performance."

**allowed-tools:** Only tools the skill needs. Common: `Bash Read Write Edit`.

**Allowed keys:** `name`, `description`, `license`, `allowed-tools`, `metadata`, `compatibility`. Nothing else.

## Creating a New Skill

### 1. Define trigger examples

Write 3-5 user requests this skill should fire on. These become description keywords and test cases.

### 2. Scaffold

```bash
python3 ~/.claude/skills/building-skills/scripts/init_skill.py my-skill --path ~/.claude/skills
```

This creates SKILL.md, LEARNED.md, scripts/, references/, setup/, and assets/ with guided TODOs.

### 3. Write the description FIRST

Before the body. The description determines if the skill ever triggers.

**Pattern:** [What it does] + [How/via what] + [Specific actions] + [Trigger keywords]

Example: "Local semantic search for markdown knowledge bases using qmd (tobi/qmd). Indexes markdown with BM25 keyword search, vector embeddings, and hybrid reranked queries. Auto-indexes on edits via Claude Code hooks. Use when searching project docs, knowledge bases, meeting notes, or any indexed markdown collection."

### 4. Write SKILL.md body

```markdown
# Skill Name

## Quick Start
[Minimal working example - simplest successful use]

## Core Operations
[Brief list. Link to references/ for detail if >100 lines.]

## Workflows
[Checklists for multi-step tasks. Conditional routing for different paths.]

## Error Reference
[Common errors and fixes. Keep actionable, not exhaustive.]

## Self-Learning
[LEARNED.md link + what to record + consolidation rules]
```

**Stay under 500 lines.** If approaching 300, start splitting to references/.

### 5. Add self-learning

Create LEARNED.md:

```markdown
# skill-name - Learned

<!-- Keep under 50 lines. Consolidate before adding. -->

## [Category]

- (YYYY-MM-DD) Observation here
```

Add Self-Learning section to SKILL.md (see [template below](#self-learning-template)).

### 6. Add scripts with dependency checking

Scripts must detect missing deps and guide setup, not fail silently:

```python
import os, sys
required = ['MY_API_KEY']
missing = [v for v in required if not os.environ.get(v)]
if missing:
    print(f"Missing: {', '.join(missing)}")
    print("Add to ~/.claude/settings.json under \"env\"")
    sys.exit(1)
```

### 7. Validate

```bash
python3 ~/.claude/skills/building-skills/scripts/validate_skill.py ~/.claude/skills/my-skill
```

Fix errors, address warnings, re-run until clean.

## Restructuring an Existing Skill

1. **Audit**: SKILL.md line count (<500?), scripts inside skill?, credentials via env vars?, frontmatter valid?, LEARNED.md exists?, description has trigger keywords?
2. **Split**: Core instructions → SKILL.md. Detailed docs → references/. Code → scripts/. Config → setup/. Output files → assets/.
3. **Fix description**: Is it the trigger mechanism? Does it front-load keywords? Third person?
4. **Add self-learning**: LEARNED.md + consolidation section.
5. **Validate**: Run validate_skill.py.

## Patterns

### Credentials
`~/.claude/settings.json` env vars. Never hardcode. Scripts detect and print setup instructions. Document in `setup/README.md`.

### Workflow Checklists
Multi-step tasks get numbered, copy-able checklists with explicit steps.

### Conditional Routing
```markdown
**Creating new?** → See [Creation](#creation)
**Editing?** → See [Editing](#editing)
**Debugging?** → See [references/troubleshooting.md](references/troubleshooting.md)
```

### Feedback Loops
```markdown
1. Make changes → 2. Run validator → 3. If errors, fix and go to 2
```

### Output Templates
Strict format: provide exact template in assets/. Flexible format: show examples.

### Hook Integration
Skills can hook into Claude Code (PreToolUse/PostToolUse) for system-level behavior like auto-indexing or domain blocking. Document in hooks/ subdirectory.

For detailed pattern examples, see [references/patterns.md](references/patterns.md).

## Anti-Patterns

| Don't | Do |
|-------|-----|
| Trigger info only in body | Put trigger keywords in `description` |
| Credentials in skill files | `~/.claude/settings.json` env vars |
| Scripts in global folder | Scripts inside skill directory |
| SKILL.md >500 lines | Split to references/ |
| Nested references (A→B→C) | One level deep from SKILL.md |
| No LEARNED.md | Every skill must self-learn |
| Unbounded LEARNED.md | Cap 50 lines, consolidate |
| README.md, CHANGELOG.md etc | Skills are for AI, not human docs |
| "You can use..." in description | Third person: "Processes..." |
| Assume deps installed | Check and guide setup on failure |
| Large docs in references/ | Put in assets/ if not needed in context |

## Self-Learning Template

```markdown
## Self-Learning

Read [LEARNED.md](LEARNED.md) before using this skill.

**Update LEARNED.md when you discover:** [list skill-specific things to record]

**Consolidation (keep under 50 lines):**
Before adding a new entry, check file length. If over 50 lines:
1. Merge duplicate/overlapping entries into single proven patterns
2. Remove entries older than 3 months that haven't been reinforced
3. Drop one-off observations that never recurred
4. Move detailed context to `LEARNED-archive.md` if worth preserving
5. Keep only entries that would change behavior - if obvious, cut it
```

## Self-Learning

Read [LEARNED.md](LEARNED.md) before building or reviewing any skill.

**Update LEARNED.md when you discover:**
- Patterns that worked well in production skills
- Description wording that improved or hurt triggering
- Common mistakes when building skills
- Validation gaps (things the validator should catch)
- Structure decisions that helped or hurt

**Consolidation (keep under 50 lines):**
Before adding, check length. If over 50: merge duplicates, prune stale (>3mo unreinforced), drop one-offs, archive to LEARNED-archive.md.

## References

- [Patterns Reference](references/patterns.md) - Workflow, output, credential, hook, and testing patterns
- [Anthropic Skill Spec](https://github.com/anthropics/skills) - Official skill specification and examples
