---
name: wp-plugin-onboard
description: "Automated plugin onboarding - clones repo, generates architecture docs, creates CLAUDE.md. Use when starting work on any WordPress plugin. Saves tokens by pre-indexing codebase."
compatibility: "WordPress plugins/themes. Requires git."
---

# WordPress Plugin Onboard

Automated workflow for onboarding WordPress plugins with architecture documentation to minimize token usage on repeat visits.

## When to use

**ALWAYS use this skill when:**
- Cloning a new plugin repository
- Starting work on a plugin for the first time
- Plugin has no `CLAUDE.md` or outdated docs

## Workflow

### Step 1: Clone & Check

```bash
# Clone the repository
git clone <repo-url> <target-dir>
cd <target-dir>

# Check if CLAUDE.md exists
if [ -f "CLAUDE.md" ]; then
    echo "CLAUDE.md exists - checking if docs are current"
    # Check docs folder
    if [ -d "docs/architecture" ]; then
        echo "Architecture docs exist"
    fi
fi
```

### Step 2: Generate Architecture (if missing)

If no `docs/architecture/` folder exists:

1. Create docs structure:
```bash
mkdir -p docs/architecture/manifest
```

2. Run codebase-architect skill with `hybrid` scope:
```
/codebase-architect
- Path: current directory
- Scope: hybrid (or architectural for 500+ files)
- Output: docs/architecture/
```

3. Wait for completion and verify FINAL_REPORT.md exists.

### Step 3: Create CLAUDE.md

Generate `CLAUDE.md` in plugin root using template:

```markdown
# Plugin: [Plugin Name]

## Quick Reference
- **Main File**: [main-plugin-file.php]
- **Version**: [x.x.x]
- **Text Domain**: [text-domain]

## Architecture Docs
Full documentation in `docs/architecture/`:
- [PLUGIN_ARCHITECTURE.md](docs/architecture/PLUGIN_ARCHITECTURE.md) - Complete reference
- [manifest/](docs/architecture/manifest/) - Index files

## Key Entry Points
<!-- Extract from architecture docs -->
- Main class: `includes/class-[plugin-name].php`
- Admin: `admin/class-[plugin-name]-admin.php`
- Public: `public/class-[plugin-name]-public.php`

## Database
<!-- From db-tables.txt manifest -->

## Hooks (Most Used)
<!-- Top 10 from hooks manifest -->

## REST API
<!-- From rest-endpoints.txt manifest -->

## Recent Changes
<!-- Auto-updated by post-commit hook -->
| Date | Type | Description | Files |
|------|------|-------------|-------|

## Known Issues / TODOs
<!-- Track ongoing work -->
```

### Step 4: Commit Documentation

```bash
git add CLAUDE.md docs/architecture/
git commit -m "docs: add architecture documentation for Claude Code"
```

### Step 5: Store in Memory (Optional)

Store plugin summary in automem for cross-session recall:

```
store_memory({
    content: "Plugin [name]: [one-line description]. Key files: [main files]. REST API: [endpoints]. DB tables: [tables].",
    tags: ["plugin", "[plugin-name]", "architecture"],
    importance: 0.85
})
```

## Post-Change Updates

After ANY code changes (bug fix, feature, refactor):

### Quick Index Update

Run this to update CLAUDE.md "Recent Changes" section:

```bash
# Get recent commits
RECENT=$(git log --oneline -5 --pretty=format:"| %ad | %s |" --date=short)

# Get changed files
FILES=$(git diff --name-only HEAD~1)
```

Update CLAUDE.md Recent Changes table.

### Full Re-index (Monthly or Major Changes)

If significant changes (new classes, hooks, APIs):

```bash
# Re-run enumeration for changed categories only
grep -rn "^class " --include="*.php" | wc -l  # Compare to manifest
```

If counts differ significantly, re-run `/codebase-architect` with `verify` scope.

## Verification

Onboarding is COMPLETE when:
- [ ] CLAUDE.md exists in plugin root
- [ ] docs/architecture/PLUGIN_ARCHITECTURE.md exists
- [ ] docs/architecture/manifest/ has all index files
- [ ] FINAL_REPORT.md shows 100% coverage
- [ ] Git commit created with docs

## Token Savings

| Without Onboard | With Onboard |
|-----------------|--------------|
| ~50,000 tokens (full scan) | ~2,000 tokens (read CLAUDE.md) |
| Every session | One-time setup |
| 10 min scanning | Instant context |

## Example Usage

```
User: Clone and set up bp-member-blog plugin

Claude:
1. git clone https://github.com/user/bp-member-blog.git
2. cd bp-member-blog
3. Check: No CLAUDE.md found
4. Run /codebase-architect with hybrid scope
5. Generate CLAUDE.md from architecture docs
6. Commit documentation
7. Ready to work!
```

## Related Skills
- `codebase-architect` - Full documentation generation
- `wp-plugin-development` - Plugin development patterns
- `code-review` - Review before commits
