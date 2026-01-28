---
name: generate-agent-skills
description: Generate documentation skills for AI agents from downloaded docs. Use after /build-my-context7 to create skills.
---

# Generate Agent Skills

Generate SKILL.md files for Claude, Codex, and OpenCode agents.

## Usage

```
/generate-agent-skills              # Generate ALL skills
/generate-agent-skills zod-docs     # Generate only zod-docs skill
```

## Instructions

### Step 1: Verify docs exist

- If argument provided: verify `output/{argument}/` exists
- If no argument: process all `output/*-docs/` directories
- If missing, tell user to run `/build-my-context7` first

### Step 2: Copy to shared folder

```bash
mkdir -p dotfiles/shared
rm -rf dotfiles/shared/{skill-name}
cp -r output/{skill-name} dotfiles/shared/
```

### Step 3: Determine tier

```bash
file_count=$(find dotfiles/shared/{skill-name} -name "*.md" -o -name "*.mdx" | wc -l)
total_size=$(du -sk dotfiles/shared/{skill-name} | cut -f1)
```

| Tier | Criteria | Template |
|------|----------|----------|
| 1 | < 30 files AND < 500KB | [templates/tier1.md](templates/tier1.md) |
| 2 | 30-100 files OR 500KB-2MB | [templates/tier2.md](templates/tier2.md) |
| 3 | > 100 files OR > 2MB | [templates/tier3.md](templates/tier3.md) |

### Step 3.5: Generate STRUCTURE.md (Tier 3 only)

For tier 3 docs, generate `dotfiles/shared/{skill-name}/STRUCTURE.md` with:

```markdown
# {Library} Documentation Structure

Total: {N} files

## {directory1}/ ({count} files)

- `{directory1}/file1.md`
- `{directory1}/file2.md`
- `{directory1}/subdir/file3.md`

## {directory2}/ ({count} files)

- `{directory2}/file1.md`
...
```

**Generation approach:**
1. List all `.md` and `.mdx` files in the docs folder
2. Group files by top-level directory
3. Sort directories alphabetically
4. Include full relative paths for each file
5. Add file counts per directory and total

This gives the agent a complete map of available documentation before it starts searching.

### Step 4: Generate SKILL.md

For each agent (Claude, Codex, OpenCode):
1. Create `dotfiles/<agent>/skills/<skill-name>/SKILL.md`
2. Use the appropriate tier template
3. Do NOT create `references/` - install script handles this

### Step 5: Report results

Summarize which skills were generated and recommend `/install-agent-skills` to deploy.
