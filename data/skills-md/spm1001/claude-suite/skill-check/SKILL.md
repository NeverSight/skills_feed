---
name: skill-check
description: Quality gate for skill development and sharing. Validates naming, description quality, and structure. Before sharing, scans for PII/secrets. Triggers on 'check this skill', 'validate skill', 'can I share this', 'scan for sharing'. Complements skill-creator (process) with validation (requirements). (user)
---

# Skill Quality Gate

Validate skill quality before deployment. **Complements skill-creator** (Anthropic's process skill) with specific requirements and quality checks.

**Core Principle:** Skills encode patterns that Claude needs to apply consistently. The skill should teach Claude HOW to do something, not just WHAT to do.

## Relationship with skill-creator

**skill-creator** (Anthropic) = **PROCESS**
- 6-step workflow: understand → plan → init → edit → package → iterate
- Template generation and packaging utilities
- Progressive disclosure principle

**skill-quality-gate** (this skill) = **VALIDATION**
- Naming conventions and requirements
- Description quality standards with examples
- Quality checklist before deployment
- Anti-patterns to avoid
- Real-world pattern guidance

**Use together:** Invoke skill-creator for the HOW (process steps), then validate with this skill for the WHAT (quality requirements).

## When to Use This Skill

**Use when:**
- BEFORE writing any SKILL.md file (mandatory gate)
- After skill-creator generates template (validate before editing)
- Reviewing skills for quality before deployment
- Extracting patterns from repeated workflows into codified skills

**NOT for:**
- One-off instructions (just put in CLAUDE.md)
- Simple tool usage (Claude already knows)
- Tasks that don't repeat across sessions
- The process steps (use skill-creator for that)

## Naming Requirements

**Skill name (YAML frontmatter):**
- Lowercase letters, numbers, hyphens only
- Max 64 characters
- **Match directory name exactly** (critical)
- Use gerund or capability form: `systematic-debugging`, `workspace-fluency`

**Good names:**
- `systematic-debugging` - clear, action-oriented
- `workspace-fluency` - describes capability
- `test-driven-development` - known pattern name
- `desired-outcomes` - describes the concept

**Bad names:**
- `pdf-helper` - vague, "helper" is meaningless
- `utils` - generic, no information
- `my-skill` - doesn't describe purpose
- `debug` - verb, not gerund/capability

## Description Requirements (CRITICAL)

**The description is how Claude discovers your skill.** This is the most important part.

**Pattern for high invocation likelihood:**
```
[ACTION TYPE] + [SPECIFIC TRIGGER] + [METHOD/VALUE PREVIEW]
```

**Best: MANDATORY gate with BEFORE condition**
```yaml
description: MANDATORY gate before writing any SKILL.md file. Invoke this skill FIRST when building new skills - provides structure template, naming conventions, description requirements, and quality checklist that MUST be validated before deployment.
```

Why best:
- "MANDATORY gate" - not optional
- "before writing" - timing condition
- "FIRST" - positioning requirement
- "MUST be validated" - imperative

**Good: Specific trigger with method**
```yaml
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes - four-phase framework (root cause investigation, pattern analysis, hypothesis testing, implementation) that ensures understanding before attempting solutions
```

Why good:
- Specific trigger: "encountering any bug, test failure"
- Timing gate: "before proposing fixes"
- Method preview: "four-phase framework"
- Value: "ensures understanding before attempting solutions"

**Good: Natural phrase triggers**
```yaml
description: Coach on outcome quality with Tier 2 vs Tier 3 distinction. Triggers on 'check my outcomes', 'is this a good outcome', 'review my Todoist', 'why isn't this working' when discussing strategic work vs tactical projects.
```

Why good:
- Explicit trigger phrases in quotes
- Context qualifier ("when discussing...")
- Domain-specific terms

**Bad: Passive and vague**
```yaml
description: Helps with debugging code problems
```

Why bad:
- No specific trigger
- Vague ("helps with")
- No insight into method or timing

**Bad: Generic action**
```yaml
description: Use when creating skills
```

Why bad:
- Too generic (I "know" patterns without invoking)
- No timing gate
- No method preview

## Quality Checklist (MANDATORY)

Before considering a skill complete, validate ALL items:

### Structure
- [ ] SKILL.md under 500 lines
- [ ] Name matches directory name exactly
- [ ] Name is kebab-case, gerund/capability form
- [ ] **Description is third-person** (verbs: "Orchestrates", "Calibrates", not "Use", "Invoke")
- [ ] **Description includes trigger AND method AND timing**
- [ ] **Description ends with (user) tag** for user-defined skills
- [ ] References one level deep from SKILL.md (if used)
- [ ] YAML frontmatter present with name and description

### Content
- [ ] No time-sensitive information ("after Aug 2025...")
- [ ] Consistent terminology throughout
- [ ] Concrete examples, not abstract rules
- [ ] Configuration values justified (why these numbers?)
- [ ] Error handling documented
- [ ] Dependencies explicitly listed
- [ ] Anti-patterns section present

### Workflow
- [ ] Clear phases/steps with success criteria
- [ ] When to Use AND When NOT to Use sections
- [ ] Integration points with other skills explicit
- [ ] Verification/validation included
- [ ] Quick reference for common operations

### Discovery
- [ ] Description uses BEFORE/MANDATORY/FIRST patterns where appropriate
- [ ] Trigger phrases are natural language users actually say
- [ ] Context qualifiers included (when appropriate)
- [ ] Method preview gives Claude enough to decide if relevant
- [ ] If paired with a command (`~/.claude/commands/*.md`), command explicitly names the skill

## Anti-Patterns to Avoid

### In Discovery (Most Critical)

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| "Use when creating..." | Too generic, Claude bypasses | "MANDATORY gate before...", "Invoke FIRST when..." |
| "Helps with..." | Vague, no specific trigger | "Triggers on [phrases]", "Use before [action]" |
| No timing condition | Skill invocation is optional | Add BEFORE/FIRST/MANDATORY language |
| Generic actions | Claude "knows" without loading | Specific phrases: 'check my outcomes', 'build skill' |
| Command doesn't name skill | Link not discoverable when reviewing | "**Invoke the `skill-name` skill**" in command |

### In Structure

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| SKILL.md over 500 lines | Token expensive | Split into references/ |
| Name doesn't match directory | Claude can't find it | Keep synchronized |
| Deeply nested files | Discovery fails | One level deep max |
| Missing YAML frontmatter | Not discoverable | Always include name and description |

### In Content

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Explaining what Claude knows | Wastes tokens | Focus on domain-specific knowledge |
| Magic constants without explanation | Unclear reasoning | Justify all configuration values |
| Too many options without defaults | Analysis paralysis | Provide recommended path |
| Mixing terminology | Confusion | Pick one term, use consistently |

## Integration with Other Skills

**This skill complements:**
- **skill-creator** - Anthropic's process (template generation, packaging)
- **verification-before-completion** - Validate after skill-creator steps

**How to reference in your skill:**
```markdown
## Integration with Other Skills

**Requires:**
- **root-cause-tracing** - When error is deep in call stack (Phase 1, Step 5)

**Complements:**
- **verification-before-completion** - Verify fix before claiming success
```

## Real-World Skill Quality Patterns

From analyzing Claude Code skills that work well:

### High-Invocation Skills Share

1. **BEFORE conditions** in description (systematic-debugging, verification-before-completion)
2. **Specific trigger phrases** in quotes (crash-recovery, desired-outcomes)
3. **Method preview** that's actionable (test-driven-development, brainstorming)
4. **Clear anti-patterns** that catch mistakes (workspace-fluency)
5. **Integration points** that compose (skill referencing skill)

### Low-Invocation Skills Suffer From

1. **Generic "Use when..."** descriptions (Claude knows patterns without loading)
2. **Vague value propositions** ("helps with", "guides", "assists")
3. **Missing timing gates** (no BEFORE/FIRST/MANDATORY)
4. **Documenting what Claude already knows** (not teaching new patterns)

## Common Skill Types

### Process Skills (like systematic-debugging)
- Iron law or core principle
- Phases with explicit success criteria
- Anti-patterns with rationalizations
- Red flags that trigger "STOP"
- BEFORE condition in description

### Fluency Skills (like workspace-fluency)
- Tool selection guidance
- Workflows for common tasks
- Best practices for domain
- Error handling patterns
- Integration with data skills

### Coaching Skills (like desired-outcomes)
- Quality criteria (good vs poor examples)
- Coaching questions to ask
- Pattern recognition for bad input
- Pattern intervention points
- Specific trigger phrases

### Quality Gate Skills (like this one)
- MANDATORY language in description
- Checklist-driven validation
- Requirements with examples
- Anti-patterns to catch
- Complement process skills

## Quick Reference

### Minimum Viable Skill

```markdown
---
name: kebab-case-name
description: [TIMING] + [TRIGGER] + [METHOD/VALUE]. Specific phrases: 'phrase1', 'phrase2'.
---

# Skill Title

[Core principle]

## When to Use
[Specific triggers with examples]

## When NOT to Use
[Clear boundaries]

## Workflow/Process
[Steps with success criteria]

## Anti-Patterns
[What to avoid with fixes]

## Quick Reference
[Common operations]
```

### Files to Include

| File | Purpose | When Required |
|------|---------|---------------|
| SKILL.md | Core instructions | Always |
| references/*.md | Detailed guides | When >500 lines |
| scripts/*.py | Utility scripts | When deterministic code needed |

Use skill-creator to generate this structure automatically.

## Before Sharing

**After quality validation, ask:** "Are you planning to share this skill/repo publicly?"

If yes, run the sharing scanner:

```bash
# Scan for PII, secrets, paths
~/.claude/skills/skill-check/scripts/scan.py /path/to/skill

# High-risk only (blocking issues)
~/.claude/skills/skill-check/scripts/scan.py --risk high /path/to/skill

# JSON output for processing
~/.claude/skills/skill-check/scripts/scan.py --format json /path/to/skill
```

**Workflow:**
1. Run scanner on target
2. Triage findings by risk level (high first)
3. Remediate or accept each finding
4. Rescan to verify clean
5. Share

See `references/sharing-scan.md` for detailed triage guidelines.

## Success Criteria

This skill works when:
- Every skill built passes the quality checklist
- Description triggers invocation reliably (not bypassed)
- Naming conventions are consistent across skills
- Anti-patterns are caught before deployment
- Integration with skill-creator is smooth

**The test:** If you find yourself "knowing" skill patterns without formally invoking, the skill's trigger failed. Fix the description.

## Remember

**Skills must be discovered to be useful.** The description is everything.

**Process (skill-creator):** How to build
**Validation (skill-making):** What quality to meet

Use both. The process without validation produces inconsistent skills. Validation without process is inefficient.
