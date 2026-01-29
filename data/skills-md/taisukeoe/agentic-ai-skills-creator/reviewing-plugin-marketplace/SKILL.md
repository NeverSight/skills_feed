---
name: reviewing-plugin-marketplace
description: Review Claude Code plugin marketplace configurations against official best practices. Use when analyzing marketplace.json and plugin.json files for structural issues, common errors, path validation, and consistency with Anthropic's official format. Detects repository URL mismatches, incorrect source paths, and missing required fields.
license: Apache-2.0
metadata:
  author: Softgraphy GK
  version: "0.1.0"
---

# Reviewing Plugin Marketplace Configurations

Comprehensive review of Claude Code plugin marketplace and plugin configurations against official best practices and common pitfalls.

## Quick Start

### Automated Review (Recommended)

Run the verification script:

```bash
bash scripts/verify-marketplace.sh [marketplace-directory]
```

This automatically checks:
- marketplace.json structure
- Skills paths validation
- Git remote URL
- README.md repository references
- plugin.json presence (warns if exists)

### Manual Review

1. Ask user for marketplace directory (e.g., `.claude-plugin/`)
2. Read marketplace.json and plugin.json (if exists)
3. Check against official format and common errors
4. Provide detailed feedback with priorities

**Example review output**:
```
## Critical Issues
- ❌ Repository URL mismatch: README.md uses "owner-a/repo" but marketplace.json uses "owner-b/repo"
- ❌ Source path "./.claude-plugin" does not exist

## Important Issues
- ⚠ plugin.json exists but Anthropic's official format uses marketplace.json only
- ⚠ Skills path "./skills/missing-skill" not found

## Compliance Score
- Structure: ✓ Valid JSON
- Required fields: ✓ Present
- Path validation: ✗ 2 invalid paths
```

## Review Process

### Step 1: Read Configuration Files

Read and analyze:
- `.claude-plugin/marketplace.json` (required for marketplaces)
- `.claude-plugin/plugin.json` (optional, check if present)
- `README.md` (for repository URL consistency)
- Git remote URL (if in git repository)

### Step 2: Validate marketplace.json Structure

**Required fields**:
- [ ] `name` - Marketplace identifier
- [ ] `owner.name` - Owner name
- [ ] `plugins` - Array of plugin definitions

**Each plugin must have**:
- [ ] `name` - Plugin identifier
- [ ] `source` - Source path (must start with `./`, e.g., `"./plugins/plugin-name"`)
- [ ] `description` - What the plugin does

**Recommended fields**:
- [ ] `metadata.description` - Marketplace description
- [ ] `metadata.version` - Version number

**Note**: `skills` field specifies skills directory path (root-relative, e.g., `"./plugins/plugin-name/skills/"`)

**Optional fields** (context-dependent):
- [ ] `strict: false` - Only needed if plugins lack plugin.json files (see references/common-errors.md)

### Step 3: Check Common Errors

**Repository URL consistency**:
- Compare URLs in marketplace.json, plugin.json, README.md, git remote
- All should point to the same repository
- Common issue: Using organization name instead of personal username

**Source path validation**:
- Verify `source` path exists
- Must start with `./` (e.g., `"./plugins/plugin-name"`)
- Check that source directory contains `skills/` subdirectory with SKILL.md files

**Skills path validation**:
- Verify `skills` path exists (root-relative, e.g., `"./plugins/plugin-name/skills/"`)
- Directory should contain subdirectories with SKILL.md files

**plugin.json conflicts**:
- Anthropic's official format uses marketplace.json only
- Having both may cause confusion
- If both exist, ensure names match

**README.md consistency checks**:
- **Skills documentation**: Verify all skills in marketplace.json are documented in README.md
  - Check "Skills Included" section lists each skill from the `skills` array
  - Each skill should have description and "Use when" guidance
- **Project Structure accuracy**:
  - If `plugin.json` mentioned in README but doesn't exist, suggest using `marketplace.json`
  - Verify structure diagram matches actual files in `.claude-plugin/`
- **Permissions section completeness**:
  - Check if README.md settings.json examples include all skills from marketplace.json
  - Example: `"Skill(skill-name)"` for each skill should be in permissions array
- **Repository references**: Ensure consistent GitHub URLs across README installation examples

### Step 4: Compare with Anthropic Format

See [references/anthropic-format.md](references/anthropic-format.md) for official structure.

**Key patterns from Anthropic**:
- marketplace.json at `.claude-plugin/marketplace.json`
- No plugin.json (marketplace.json only)
- `source: "./plugins/plugin-name"` pointing to plugin directory (must start with `./`)
- `strict: false` (optional - only needed when plugin.json is missing)
- `skills` field specifies skills directory (root-relative path)

### Step 5: Generate Feedback

Organize findings by priority:

**Critical Issues** (breaks functionality):
- enabledPlugins format error (array instead of object)
- Repository URL mismatch with git remote
- Invalid source path (doesn't exist)
- Missing required fields
- Invalid JSON syntax

**Important Issues** (causes confusion):
- Repository URL inconsistency across files
- Invalid skills paths
- Conflicting plugin.json and marketplace.json
- Missing recommended fields

**Suggestions** (best practices):
- Add `metadata` section (improves discoverability)
- Add `strict: false` only if plugins lack plugin.json (otherwise no effect)
- Follow Anthropic's single-file pattern
- Explicit `skills` array

## Common Issues Reference

See [references/common-errors.md](references/common-errors.md) for detailed error patterns and solutions.

**Top 3 issues from real experience** (by actual impact):

1. **enabledPlugins format error** ⚠️ BREAKS FUNCTIONALITY
   - Error: Plugins don't load, no activation
   - Cause: Using array `["plugin@marketplace"]` instead of object `{"plugin@marketplace": true}`
   - Fix: Change to object format in settings.json
   - **This is the #1 cause of "plugin not working" issues**

2. **Repository URL mismatch**
   - Error: `Plugin 'name' not found in marketplace`
   - Cause: README/settings use different owner than actual git remote
   - Fix: Ensure all URLs match `git remote -v`

3. **Wrong source path**
   - Error: `Plugin 'name' not found`
   - Cause: Source points to non-existent directory
   - Fix: Use `"./"` for root, verify path exists

## Output Format

Structure review with these sections:
- **Summary**: Overall assessment
- **Critical Issues**: Must fix (with file:line references)
- **Important Issues**: Should fix (with explanations)
- **Suggestions**: Best practices alignment
- **Compliance Score**: Quick visual assessment

## Tips for Effective Reviews

**Be Specific**: Don't say "URL is wrong" - say "marketplace.json line 7 uses 'owner-a/repo' but git remote shows 'owner-b/repo'"

**Verify Paths**: Actually check if files/directories exist, don't just validate format

**Check Consistency**: Cross-reference all files that mention repository URLs

**Use Official Examples**: Compare against Anthropic's format at https://github.com/anthropics/skills

## References

**Anthropic Format**: See [references/anthropic-format.md](references/anthropic-format.md) for official marketplace.json structure

**Common Errors**: See [references/common-errors.md](references/common-errors.md) for detailed error patterns and solutions
