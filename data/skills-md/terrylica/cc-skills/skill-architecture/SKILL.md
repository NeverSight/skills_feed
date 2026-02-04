---
name: skill-architecture
description: Meta-skill for creating Claude Code skills. TRIGGERS - create skill, YAML frontmatter, validate skill, skill architecture.
---

# Skill Architecture

Comprehensive guide for creating effective Claude Code skills following Anthropic's official standards with emphasis on security, CLI-specific features, and progressive disclosure architecture.

> ⚠️ **Scope**: Claude Code CLI Agent Skills (`~/.claude/skills/`), not Claude.ai API skills

## When to Use This Skill

Use this skill when:

- Creating new Claude Code skills from scratch
- Learning skill YAML frontmatter and structure requirements
- Validating skill file format and portability
- Understanding progressive disclosure patterns for skills

---

## FIRST: TodoWrite Task Templates

**MANDATORY**: Select and load the appropriate template into TodoWrite before any skill work.

> For detailed context on each step, see [Skill Creation Process (Detailed Tutorial)](#skill-creation-process-detailed-tutorial) below.

### Template A: Create New Skill

```
1. Gather requirements (ask user for functionality, examples, triggers)
2. Identify reusable resources (scripts, references, assets needed)
3. Run init script to create skill directory structure
4. Create bundled resources first (scripts/, references/, assets/)
5. Write SKILL.md with YAML frontmatter (name, description with triggers)
6. Add TodoWrite task templates section to SKILL.md
7. Add Post-Change Checklist section to SKILL.md
8. Validate with quick_validate.py
9. Validate links (relative paths only): bun run plugins/plugin-dev/scripts/validate-links.ts <skill-path>
10. Test skill on real example
11. Register skill in project CLAUDE.md
12. Verify against Skill Quality Checklist below
```

### Template B: Update Existing Skill

```
1. Read current SKILL.md and understand structure
2. Identify what needs changing (triggers, workflow, resources)
3. Make targeted changes to SKILL.md
4. Update any affected references/ or scripts/
5. Validate with quick_validate.py
6. Validate links (relative paths only): bun run plugins/plugin-dev/scripts/validate-links.ts <skill-path>
7. Test updated behavior
8. Update project CLAUDE.md if description changed
9. Verify against Skill Quality Checklist below
```

### Template C: Add Resources to Skill

```
1. Read current SKILL.md to understand skill purpose
2. Determine resource type (script, reference, or asset)
3. Create resource in appropriate directory
4. Update SKILL.md to document new resource
5. Validate with quick_validate.py
6. Validate links (relative paths only): bun run plugins/plugin-dev/scripts/validate-links.ts <skill-path>
7. Test resource integration
8. Verify against Skill Quality Checklist below
```

### Template D: Convert to Self-Evolving Skill

```
1. Read current SKILL.md structure
2. Add TodoWrite Task Templates section (scenario-specific)
3. Add Post-Change Checklist section
4. Create references/evolution-log.md (reverse chronological - newest on top)
5. Create references/config-reference.md (if skill manages external config)
6. Update description with self-evolution triggers
7. Validate with quick_validate.py
8. Validate links (relative paths only): bun run plugins/plugin-dev/scripts/validate-links.ts <skill-path>
9. Test self-documentation on sample change
10. Verify against Skill Quality Checklist below
```

### Template E: Troubleshoot Skill Not Triggering

```
1. Check YAML frontmatter syntax (no colons in description)
2. Verify trigger keywords in description match user queries
3. Check skill location (~/.claude/skills/ or project .claude/skills/)
4. Validate with quick_validate.py for errors
5. Validate links: bun run plugins/plugin-dev/scripts/validate-links.ts <skill-path>
6. Test with explicit trigger phrase
7. Document findings in skill if new issue discovered
8. Verify against Skill Quality Checklist below
```

### Skill Quality Checklist

After ANY skill work, verify:

- [ ] YAML frontmatter valid (name lowercase-hyphen, description has triggers)
- [ ] Description includes WHEN to use (trigger keywords)
- [ ] TodoWrite templates cover all common scenarios
- [ ] Post-Change Checklist included for self-maintenance
- [ ] Final template step references this checklist
- [ ] Project CLAUDE.md updated if new/renamed skill
- [ ] Validated with quick_validate.py
- [ ] All markdown links use relative paths (plugin-portable)
- [ ] No broken internal links (validate-links.ts passes)
- [ ] No unsafe path patterns (see [Path Patterns](./references/path-patterns.md)):
  - No hardcoded `/Users/<user>` or `/home/<user>` (use `$HOME`)
  - No hardcoded `/tmp` in Python (use `tempfile.TemporaryDirectory`)
  - No hardcoded binary paths (use `command -v` or PATH)
- [ ] Bash compatibility verified (see [Bash Compatibility](./references/bash-compatibility.md)):
  - All bash code blocks wrapped with `/usr/bin/env bash << 'NAME_EOF'`
  - No `declare -A` (associative arrays) - use parallel indexed arrays
  - No `grep -P` (Perl regex) - use `grep -E` with awk
  - No `\!=` in conditionals - use `!=` directly
  - Heredoc EOF marker is descriptive (e.g., `PREFLIGHT_EOF`)

---

## Post-Change Checklist (Self-Maintenance)

After modifying THIS skill (skill-architecture):

1. [ ] Templates and 6 Steps tutorial remain aligned
2. [ ] Skill Quality Checklist reflects current best practices
3. [ ] All referenced files in references/ exist
4. [ ] Append changes to [evolution-log.md](./references/evolution-log.md)
5. [ ] Update user's CLAUDE.md if triggers changed

---

## Continuous Improvement (Proactive Self-Evolution)

**CRITICAL**: Skills must actively evolve. Don't wait for explicit requests—upgrade skills when insights emerge.

### During Every Skill Execution

Watch for these improvement signals:

| Signal                    | Example                        | Action                      |
| ------------------------- | ------------------------------ | --------------------------- |
| **Friction**              | Step feels awkward or unclear  | Rewrite for clarity         |
| **Missing edge case**     | Workflow fails on valid input  | Add handling + document     |
| **Better pattern**        | Discover more elegant approach | Update + log why            |
| **User confusion**        | Same question asked repeatedly | Add clarification or FAQ    |
| **Tool evolution**        | Underlying tool gains features | Update to leverage them     |
| **Repeated manual steps** | Same code written each time    | Create script in `scripts/` |

### Immediate Update Protocol

When improvement opportunity identified:

1. **Pause current task** (briefly)
2. **Make the improvement** to SKILL.md or resources
3. **Log in evolution-log.md** (one-liner is fine for small changes)
4. **Resume original task**

> **Rationale**: Small immediate updates compound. Waiting means insights are forgotten. 30 seconds now saves 5 minutes later.

### What NOT to Update Immediately

- Major structural changes (discuss with user first)
- Changes that would break in-progress work
- Speculative improvements without concrete evidence

### Self-Reflection Trigger

After completing any skill-assisted task, ask:

> "Did anything about this skill feel suboptimal? If I encountered this again, what would help?"

If answer exists → update the skill NOW.

---

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities with specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific domains—transforming Claude from general-purpose to specialized agent with procedural knowledge no model fully possesses.

### What Skills Provide

1. **Specialized workflows** - Multi-step procedures for specific domains
2. **Tool integrations** - Instructions for working with specific file formats or APIs
3. **Domain expertise** - Company-specific knowledge, schemas, business logic
4. **Bundled resources** - Scripts, references, assets for complex/repetitive tasks

---

## Skill Creation Process (Detailed Tutorial)

> **Note**: Use TodoWrite templates above for execution. This section provides detailed context for each phase.

### Step 1: Understanding the Skill with Concrete Examples

Clearly understand concrete examples of how the skill will be used. Ask users:

- "What functionality should this skill support?"
- "Can you give examples of how it would be used?"
- "What would trigger this skill?"

Skip only when usage patterns are already clearly understood.

### Step 2: Planning Reusable Contents

Analyze each example to identify what resources would be helpful:

**Example 1 - PDF Editor**:

- Rotating PDFs requires rewriting code each time
- → Create `scripts/rotate_pdf.py`

**Example 2 - Frontend Builder**:

- Webapps need same HTML/React boilerplate
- → Create `assets/hello-world/` template

**Example 3 - BigQuery**:

- Queries require rediscovering table schemas
- → Create `references/schema.md`

### Step 3: Initialize the Skill

Run the init script from plugin-dev:

```bash
uv run plugins/plugin-dev/scripts/skill-creator/init_skill.py <skill-name> --path <target-path>
```

Creates: skill directory + SKILL.md template + example resource directories

### Step 4: Edit the Skill

**Writing Style**: Imperative/infinitive form (verb-first), not second person

- ✅ "To accomplish X, do Y"
- ❌ "You should do X"

**SKILL.md must include**:

1. What is the purpose? (few sentences)
2. When should it be used? (trigger keywords in description)
3. How should Claude use bundled resources?
4. **TodoWrite Task Templates** - Pre-defined todos for common scenarios
5. **Post-Change Checklist** - Self-maintenance verification

**Start with resources** (`scripts/`, `references/`, `assets/`), then update SKILL.md

### Step 5: Validate the Skill

**For local development** (validation only, no zip creation):

```bash
uv run plugins/plugin-dev/scripts/skill-creator/quick_validate.py <path/to/skill-folder>
```

**For distribution** (validates AND creates zip):

```bash
uv run plugins/plugin-dev/scripts/skill-creator/package_skill.py <path/to/skill-folder>
```

Validates: YAML frontmatter, naming, description, file organization

**Note**: Use `quick_validate.py` for most workflows. Only use `package_skill.py` when actually distributing the skill to others.

### Step 6: Register and Iterate

1. Register skill in project CLAUDE.md (Workspace Skills section)
2. Use skill on real tasks
3. Notice struggles/inefficiencies
4. Update SKILL.md or resources
5. Test again
6. Verify against Skill Quality Checklist above

---

## Skill Anatomy

```
skill-name/
├── SKILL.md                      # Required: YAML frontmatter + instructions
├── scripts/                      # Optional: Executable code (Python/Bash)
├── references/                   # Optional: Documentation loaded as needed
│   └── evolution-log.md          # Recommended: Change history (self-evolving)
└── assets/                       # Optional: Files used in output
```

### YAML Frontmatter (Required)

```yaml
---
name: skill-name-here
description: What this does and when to use it (max 1024 chars for CLI)
allowed-tools: Read, Grep, Bash # Optional, CLI-only feature
---
```

**Field Requirements:**

| Field           | Rules                                                                           |
| --------------- | ------------------------------------------------------------------------------- |
| `name`          | Lowercase, hyphens, numbers. Max 64 chars. Unique.                              |
| `description`   | WHAT it does + WHEN to use. Max 1024 chars (CLI) / 200 (API). Include triggers! |
| `allowed-tools` | **CLI-only**. Comma-separated list restricts tools. Optional.                   |

**Good vs Bad Descriptions:**

✅ **Good**: "Extract text and tables from PDFs, fill forms, merge documents. Use when working with PDF files or when user mentions forms, contracts, document processing."

❌ **Bad**: "Helps with documents" (too vague, no triggers)

**YAML Description Pitfalls:**

| Pitfall          | Problem                          | Fix                                                                                  |
| ---------------- | -------------------------------- | ------------------------------------------------------------------------------------ |
| Multiline syntax | `>` or `\|` not supported        | Single line only                                                                     |
| Colons in text   | `CRITICAL: requires` breaks YAML | Use `CRITICAL - requires`                                                            |
| Quoted strings   | Valid but not idiomatic          | Unquoted preferred (match [anthropics/skills](https://github.com/anthropics/skills)) |

```yaml
# ❌ BREAKS - colon parsed as YAML key:value
description: ...CRITICAL: requires flag

# ✅ WORKS - dash instead of colon
description: ...CRITICAL - requires flag
```

**Validation**: GitHub renders frontmatter - invalid YAML shows red error banner.

### Progressive Disclosure (3 Levels)

Skills use progressive loading to manage context efficiently:

1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed by Claude (unlimited\*)

\*Scripts can execute without reading into context.

---

## Bundled Resources

Skills can include `scripts/`, `references/`, and `assets/` directories. See [Progressive Disclosure](./references/progressive-disclosure.md) for detailed guidance on when to use each.

---

## CLI-Specific Features

CLI skills support `allowed-tools` restriction for security. See [Security Practices](./references/security-practices.md) for details.

---

## Structural Patterns

See [Structural Patterns](./references/structural-patterns.md) for detailed guidance on:

1. **Workflow Pattern** - Sequential multi-step procedures
2. **Task Pattern** - Specific, bounded tasks
3. **Reference Pattern** - Knowledge repository
4. **Capabilities Pattern** - Tool integrations

---

## User Conventions Integration

This skill follows common user conventions:

- **Absolute paths**: Always use full paths (terminal Cmd+click compatible)
- **Unix-only**: macOS, Linux (no Windows support)
- **Python**: `uv run script.py` with PEP 723 inline dependencies
- **Planning**: OpenAPI 3.1.1 specs when appropriate

---

## Marketplace Scripts

See [Scripts Reference](./references/scripts-reference.md) for marketplace script usage.

---

## Reference Documentation

For detailed information, see:

- [Structural Patterns](./references/structural-patterns.md) - 4 skill architecture patterns
- [Workflow Patterns](./references/workflow-patterns.md) - Workflow skill implementation patterns
- [Progressive Disclosure](./references/progressive-disclosure.md) - Context management patterns
- [Creation Workflow](./references/creation-workflow.md) - Step-by-step process
- [Scripts Reference](./references/scripts-reference.md) - Marketplace script usage
- [Security Practices](./references/security-practices.md) - Threats and defenses (CVE references)
- [Token Efficiency](./references/token-efficiency.md) - Context optimization
- [Advanced Topics](./references/advanced-topics.md) - CLI vs API, composition, bugs
- [Path Patterns](./references/path-patterns.md) - Safe/unsafe path references (known bugs documented)
- [Validation Reference](./references/validation-reference.md) - Quality checklist
- [SYNC-TRACKING](./references/SYNC-TRACKING.md) - Marketplace version tracking
- [Evolution Log](./references/evolution-log.md) - This skill's change history

---

## Troubleshooting

| Issue                  | Cause                          | Solution                                                  |
| ---------------------- | ------------------------------ | --------------------------------------------------------- |
| Skill not triggering   | Missing trigger keywords       | Add trigger phrases to description field                  |
| YAML parse error       | Colon in description           | Replace colons with dashes in description                 |
| Skill not found        | Wrong location                 | Place in `~/.claude/skills/` or project `.claude/skills/` |
| validate script fails  | Invalid frontmatter            | Check name format (lowercase-hyphen only)                 |
| Resources not loading  | Wrong path in SKILL.md         | Use relative paths from skill directory                   |
| Script execution fails | Missing shebang or permissions | Add `#!/usr/bin/env python3` and `chmod +x`               |
| allowed-tools ignored  | API skill (not CLI)            | allowed-tools only works in CLI skills                    |
| Description too long   | Over 1024 chars                | Shorten description, move details to SKILL.md body        |
