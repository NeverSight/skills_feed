---
name: forge-update-changelog
description: Update CHANGELOG.md with user-facing changes from recent commits. Use when the user has merged a PR, completed a release, or wants to document recent changes in the changelog.
allowed-tools: Read, Bash, Grep, Glob, Edit
---

# Update Changelog

Update CHANGELOG.md with user-facing changes from recent development work.

## Input

Optional: A date (YYYY-MM-DD) or commit hash to start from: $ARGUMENTS

If not provided, will look at commits since the last changelog update.

## Process

### Step 1: Read Current Changelog

```bash
# Read the current changelog to understand the format and last update
cat CHANGELOG.md
```

### Step 2: Gather Recent Changes

```bash
# Get recent commits (adjust date/commit as needed)
# Default: commits from the last month
git log --oneline --since="1 month ago"

# For more detail on specific commits
git log --format="%h %s" --since="1 month ago"

# Or since a specific commit
git log --oneline <commit>..HEAD
```

### Step 3: Filter for User-Facing Changes

Review commits and identify only those that affect end users:

**Include:**
- `feat:` - New features users can see or use
- `fix:` - Bug fixes that affected user experience
- `perf:` - Performance improvements users would notice

**Exclude (internal changes):**
- `refactor:` - Code restructuring (unless it changes behavior)
- `test:` - Test additions/changes
- `chore:` - Maintenance tasks
- `ci:` - CI/CD changes
- `docs:` - Documentation changes (unless user-facing help docs)
- Internal API changes
- Development tooling updates

### Step 4: Group Changes by Category

Organize changes into user-friendly categories that match the project. Common categories include:

- **New Features** - Major new functionality
- **Improvements** - Enhancements to existing features
- **Bug Fixes** - Issues that affected users
- **Performance** - Speed and responsiveness improvements
- **Security** - Security-related improvements

Adapt categories to the project's domain (e.g., a SaaS app might use "Dashboard", "Billing", "Integrations").

### Step 5: Write User-Friendly Descriptions

Transform technical commit messages into plain language:

**Technical → User-Friendly Examples:**
- `feat(auth): add OAuth2 login with Google` → "Sign in with your Google account"
- `fix: file upload fails for large images` → "Fixed uploading large images"
- `perf(frontend): optimize bundle size with code splitting` → "Faster app loading times"
- `feat(dashboard): add export to CSV` → "Export your data as a spreadsheet"

**Writing Guidelines:**
- Use active voice ("Create", "See", "Download")
- Focus on benefits, not implementation
- Avoid technical jargon (no "API", "endpoints", "cache", "SSR")
- Keep entries short (one line preferred)
- Use bold for feature names: **Feature name** - description

### Step 6: Update CHANGELOG.md

Add a new section at the top (after the header), following this format:

```markdown
## Month Year

### Category Name
- **Feature name** - Brief, user-friendly description
- **Another feature** - What users can now do

### Another Category
- **Fix description** - What was fixed and how it helps
```

**Formatting Rules:**
- Use `## Month Year` for date headers
- Use `### Category` for grouping related changes
- Use `---` between months for visual separation
- Bold the feature/fix name, then describe it
- Keep the most recent changes at the top

### Step 7: Review and Verify

Before committing, verify:
- [ ] Only user-facing changes are included
- [ ] No technical jargon
- [ ] Consistent formatting with existing entries
- [ ] Changes are in the correct time period
- [ ] No duplicate entries

## Example Transformation

**Git log:**
```
fb6c12f feat(auth): add OAuth2 login with Google (#42)
443f225 feat(dashboard): add CSV export for reports (#41)
0efa767 fix(api): handle rate limiting gracefully (#39)
d9a51f2 perf(frontend): lazy load dashboard charts (#38)
52105d7 fix(notifications): emails not sent for new signups (#37)
```

**Changelog entry:**
```markdown
## January 2025

### New Features
- **Google sign-in** - Sign in with your Google account for faster access
- **Export reports** - Download your reports as CSV spreadsheets

### Bug Fixes
- **Notification emails** - New users now correctly receive welcome emails

### Performance
- **Faster dashboard** - Charts load more quickly on the dashboard
```

## Important Guidelines

1. **User perspective**: Always ask "Would a user notice or care about this?"
2. **No attribution**: Don't include author names or PR numbers
3. **No time estimates**: Don't say "now X% faster" unless you have real metrics
4. **Positive framing**: "Fixed X" is better than "X was broken"
5. **Combine related changes**: Multiple commits for one feature = one changelog entry
6. **Skip internal changes**: Refactors, test updates, CI changes are not user-facing

## Related Skills

**Full workflow:** `forge-setup-project` → `forge-create-issue` → `forge-implement-issue` → `forge-reflect-pr` → `forge-address-pr-feedback` → `forge-update-changelog`

## Example Usage

```
/forge-update-changelog
/forge-update-changelog 2025-01-01
/forge-update-changelog abc123
```
