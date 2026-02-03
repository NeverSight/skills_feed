---
name: skill-development
description: |
  Tools for creating, auditing, and maintaining Claude Code skills. Includes /create-skill
  for scaffolding, /review-skill for quality checks, and /audit commands for bulk verification.

  Use when: building new skills, maintaining skill quality, or forking claude-skills repo.
user-invocable: true
---

# Skill Development

Tools for creating, auditing, and maintaining Claude Code skills. Essential for anyone building skills or forking this repository.

---

## Slash Commands

### `/create-skill <name>`

Scaffold a new skill from templates.

**What it does**:
1. Validates skill name (lowercase-hyphen-case, max 40 chars)
2. Asks about skill type (Cloudflare/AI/Frontend/Auth/Database/Tooling/Generic)
3. Copies `templates/skill-skeleton/` to `skills/<name>/`
4. Auto-populates name and dates in SKILL.md
5. Creates README.md with auto-trigger keywords
6. Runs metadata check
7. Installs skill for testing

**Usage**: `/create-skill my-new-skill`

---

### `/review-skill <name>`

Quality review and audit of an existing skill.

**What it does**:
1. Checks SKILL.md structure and metadata
2. Validates package versions against latest
3. Reviews error documentation
4. Checks template completeness
5. Suggests improvements

**Usage**: `/review-skill cloudflare-worker-base`

---

### `/audit [name]`

Multi-agent audit swarm for parallel skill verification.

**What it does**:
1. Launches parallel agents to audit multiple skills
2. Checks versions, metadata, content quality
3. Generates consolidated report

**Usage**:
- `/audit` - Audit all skills
- `/audit cloudflare-*` - Audit matching skills

---

### `/audit-skill-deep <name>`

Deep content validation against official documentation.

**What it does**:
1. Fetches official documentation for the skill's technology
2. Compares patterns and versions
3. Identifies knowledge gaps or outdated content
4. Suggests corrections and updates

**Usage**: `/audit-skill-deep tailwind-v4-shadcn`

---

### `/deep-audit <name>`

Extended deep audit with comprehensive doc scraping.

**What it does**:
1. Scrapes multiple documentation sources
2. Caches scraped content in `archive/audit-cache/`
3. Cross-references with skill content
4. Produces detailed accuracy report

**Usage**: `/deep-audit openai-api`

---

## Templates

This skill includes templates for creating new skills:

| Template | Purpose |
|----------|---------|
| `templates/skill-skeleton/` | Complete skill directory to copy |
| `templates/SKILL-TEMPLATE.md` | SKILL.md with TODOs to fill |
| `templates/README-TEMPLATE.md` | README.md with keywords section |
| `templates/skill-metadata-v2.yaml` | YAML frontmatter reference |
| `templates/RESEARCH_FINDINGS_TEMPLATE.md` | Research output format |
| `templates/CONTENT_AUDIT_TEMPLATE.md` | Audit checklist |

### Using Templates

```bash
# Option 1: Use /create-skill (recommended)
/create-skill my-new-skill

# Option 2: Manual copy
cp -r skills/skill-development/templates/skill-skeleton/ skills/my-new-skill/
# Then fill in the TODOs
```

---

## Quality Standards

Skills should meet these criteria before publishing:

### Required
- [ ] YAML frontmatter with `name` and `description`
- [ ] Description includes "Use when" scenarios
- [ ] Third-person description style
- [ ] Package versions are current
- [ ] Templates tested and working

### Recommended
- [ ] README.md with auto-trigger keywords
- [ ] Token efficiency measured (target: 50%+ savings)
- [ ] Known issues documented with sources
- [ ] Examples include error prevention

**Full checklist**: See `ONE_PAGE_CHECKLIST.md` in repo root.

---

## Agents

This skill provides agents for automated skill maintenance:

| Agent | Purpose |
|-------|---------|
| `skill-creator` | Scaffold new skills with proper structure |
| `version-checker` | Verify package versions are current |
| `content-accuracy-auditor` | Compare skill content vs official docs |
| `code-example-validator` | Validate code examples are syntactically correct |
| `api-method-checker` | Verify documented API methods exist |
| `doc-validator` | Check documentation quality |
| `bulk-updater` | Apply changes across multiple skills |

These agents are in `.claude/agents/` and used by the audit commands.

---

## Workflow

### Creating a New Skill

```
1. /create-skill my-skill
2. Fill in TODOs in SKILL.md
3. Add templates, references, scripts as needed
4. /review-skill my-skill
5. Fix any issues
6. Test: /plugin install ./skills/my-skill
7. Commit and push
```

### Auditing Skills

```
1. /audit                          # Quick check all skills
2. /audit-skill-deep my-skill      # Deep check specific skill
3. Review findings
4. Fix issues or document as known limitations
5. Update metadata.last_verified date
```

### Quarterly Maintenance

```
1. Run: ./scripts/check-all-versions.sh
2. Review VERSIONS_REPORT.md
3. /audit for all skills needing updates
4. Update package versions
5. Test affected skills
6. Commit: "chore: quarterly version updates"
```

---

## For Forkers

If you've forked this repo to maintain your own skills:

1. **Install this skill**: `/plugin install ./skills/skill-development`
2. **Use /create-skill**: Creates skills with proper structure
3. **Use /review-skill**: Validates before publishing
4. **Customize agents**: Modify `.claude/agents/` for your needs
5. **Pull upstream updates**: `git fetch upstream && git merge upstream/main`

The tooling is designed to work standalone - you don't need the full repo to use these commands.
