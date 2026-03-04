---
name: skill-review
displayName: Skill Review & Garden
description: "Audit and maintain the joelclaw skill inventory. Use when checking skill health, fixing broken symlinks, finding stale skills, or running the skill garden. Triggers: 'skill audit', 'check skills', 'stale skills', 'skill health', 'skill garden', 'broken skill', 'skill review', 'fix skills', 'garden skills', or any task involving skill inventory maintenance."
version: 1.0.0
author: Joel Hooks
tags: [joelclaw, skills, maintenance, gardening, automation]
---

# Skill Review & Gardening

Automated and manual processes for keeping the 51+ joelclaw skills accurate and healthy. ADR-0179.

## Canonical Contract

- **Source of truth**: `~/Code/joelhooks/joelclaw/skills/` (repo, fully git-tracked)
- **Home dir consumers** (symlink IN to repo):
  - `~/.agents/skills/<name>` → `~/Code/joelhooks/joelclaw/skills/<name>`
  - `~/.pi/agent/skills/<name>` → `~/Code/joelhooks/joelclaw/skills/<name>`
- **Never** put skill content in dot directories (`.agents/`, `.pi/`, `.claude/`). Those are symlink consumers.
- Third-party skill packs (axiom-*, marketing, etc.) live in `~/.agents/skills/` as external installs — NOT in the repo.

## Automated Garden (Inngest)

The `skill-garden` function runs daily at 6am PT and checks:

### Daily (structural + patterns)
1. **Broken symlinks** — dead links in `~/.agents/skills/`, `~/.pi/agent/skills/`
2. **Non-canonical REAL DIRs** — directories in home skill dirs that should be symlinks
3. **Missing frontmatter** — skills without SKILL.md or required frontmatter (name, description)
4. **Stale patterns** — skills referencing known-dead infrastructure:
   - legacy lightweight-k8s distro terms → replaced by Talos on Colima
   - retired vector DB terms → replaced by Typesense vector search
   - launchctl commands targeting worker labels → worker runs in k8s
   - old standalone worker clone paths → monorepo `packages/system-bus/`
   - old standalone CLI repo paths/aliases → CLI is `packages/cli/` + `joelclaw`
5. **Orphans** — skills in repo with no symlink from any home dir

### Monthly (1st of month, LLM deep review)
- Reads current `AGENTS.md` as ground truth
- Compares each skill's content against system reality via `pi` inference
- Flags outdated workflows, wrong versions, missing capabilities
- Produces structured report

### Triggers
```bash
# On-demand via event
joelclaw send "skill-garden/check"
joelclaw send "skill-garden/check" --data '{"deep": true}'  # force LLM review

# Daily cron: 0 6 * * * (automatic)
```

### Output
- OTEL event: `skill-garden.findings`
- Gateway notification when issues found (zero noise on clean days)
- Structured JSON report with findings by type

## Manual Review Process

When the automated garden flags issues, or for periodic deep review:

### 1. Run the audit
```bash
joelclaw send "skill-garden/check" --data '{"deep": true}'
```

### 2. Check for structural issues
```bash
# Broken symlinks
find ~/.agents/skills/ ~/.pi/agent/skills/ -maxdepth 1 -type l ! -exec test -e {} \; -print

# REAL DIRs that should be symlinks
for dir in ~/.agents/skills ~/.pi/agent/skills; do
  find "$dir" -maxdepth 1 -type d ! -type l | while read d; do
    name=$(basename "$d")
    [ -d ~/Code/joelhooks/joelclaw/skills/"$name" ] && echo "NON-CANONICAL: $d"
  done
done

# Orphan skills (in repo, no home dir symlink)
for skill in ~/Code/joelhooks/joelclaw/skills/*/; do
  name=$(basename "$skill")
  [ ! -L ~/.agents/skills/"$name" ] && [ ! -L ~/.pi/agent/skills/"$name" ] && echo "ORPHAN: $name"
done
```

### 3. Fix structural issues
```bash
# Fix a broken symlink
rm ~/.agents/skills/<name>
ln -s ~/Code/joelhooks/joelclaw/skills/<name> ~/.agents/skills/<name>

# Convert a REAL DIR to symlink
rm -rf ~/.pi/agent/skills/<name>
ln -s ~/Code/joelhooks/joelclaw/skills/<name> ~/.pi/agent/skills/<name>

# Add missing home dir symlink
ln -s ~/Code/joelhooks/joelclaw/skills/<name> ~/.agents/skills/<name>
ln -s ~/Code/joelhooks/joelclaw/skills/<name> ~/.pi/agent/skills/<name>
```

### 4. Fix stale content

When a skill references outdated architecture:

1. Read the skill: `cat skills/<name>/SKILL.md`
2. Cross-reference with `AGENTS.md` and current system state
3. Update the skill with current facts
4. Commit: `git add skills/<name> && git commit -m "skill(<name>): update for current architecture"`

### 5. Adding a new skill

```bash
mkdir -p skills/<name>
# Write SKILL.md with frontmatter: name, description, version, author, tags
# Symlink from home dirs:
ln -s ~/Code/joelhooks/joelclaw/skills/<name> ~/.agents/skills/<name>
ln -s ~/Code/joelhooks/joelclaw/skills/<name> ~/.pi/agent/skills/<name>
git add skills/<name>
git commit -m "skill(<name>): add new skill"
```

See the [add-skill skill](../add-skill/SKILL.md) for the full idiomatic process.

## Stale Pattern Registry

Keep this list updated as infrastructure changes. The Inngest function reads these patterns.

| Pattern | What it means | Current reality |
|---------|--------------|-----------------|
| legacy k8s distro token | Old k8s distribution reference | Talos v1.12.4 on Colima |
| legacy vector DB token | Old vector store reference | Typesense with vector search |
| launchctl worker command token | Old worker deploy mode | k8s Deployment |
| standalone worker clone path token | Old worker path | `packages/system-bus/` in monorepo |
| standalone CLI path token | Old CLI path | `packages/cli/` in monorepo |
| short CLI alias token | Old CLI name | `joelclaw` CLI |

**When infrastructure changes, update this table AND the exact regex list in `STALE_PATTERNS` inside `skill-garden.ts`.**

## Required Frontmatter

Every skill MUST have:
```yaml
---
name: skill-name
description: "What this skill does and when to use it"
---
```

Recommended additional fields:
```yaml
version: 1.0.0
author: Joel Hooks
tags: [relevant, tags]
displayName: Human Readable Name
```

## Key Paths

| What | Path |
|------|------|
| Repo skills (canonical) | `~/Code/joelhooks/joelclaw/skills/` |
| Inngest function | `packages/system-bus/src/inngest/functions/skill-garden.ts` |
| ADR | `~/Vault/docs/decisions/0179-automated-skill-gardening.md` |
| Home dir: agents | `~/.agents/skills/` |
| Home dir: pi | `~/.pi/agent/skills/` |
| Stale patterns | `STALE_PATTERNS` in `skill-garden.ts` |
