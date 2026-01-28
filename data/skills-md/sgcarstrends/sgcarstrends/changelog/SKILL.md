---
name: changelog
description: Generate and maintain CHANGELOG.md using semantic-release and conventional commits. Use when preparing releases, documenting changes, or reviewing version history.
allowed-tools: Read, Edit, Write, Bash, Grep
---

# Changelog Management Skill

This skill helps you generate and maintain changelogs using semantic-release and conventional commits.

## When to Use This Skill

- Generating changelogs for releases
- Documenting version changes
- Reviewing release history
- Preparing release notes
- Understanding what changed between versions
- Communicating changes to users

## Changelog Overview

The project uses **semantic-release** to automatically generate changelogs based on conventional commits:
- **Automatic Generation**: Changelog generated from git commits
- **Version Bumping**: Automatic versioning based on commit types
- **Release Notes**: GitHub releases with changelog
- **Breaking Changes**: Highlighted prominently
- **Categorized Changes**: Features, fixes, chores grouped

## Changelog Format

### Keep a Changelog Format

The project follows [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New feature description

### Changed
- Change description

### Deprecated
- Deprecated feature notice

### Removed
- Removed feature notice

### Fixed
- Bug fix description

### Security
- Security fix description

## [1.2.0] - 2024-01-15

### Added
- Add blog post generation with Gemini AI
- Add social media integration (Discord, LinkedIn, Telegram, Twitter)

### Changed
- Update Next.js to v16
- Migrate to Cache Components mode

### Fixed
- Fix database connection timeout issue
- Fix chart rendering on mobile devices

## [1.1.0] - 2024-01-01

### Added
- Add COE bidding results endpoint
- Add interactive charts with Recharts

### Fixed
- Fix pagination in car makes endpoint

## [1.0.0] - 2023-12-15

### Added
- Initial release
- Car registration data API
- Next.js web application
- PostgreSQL database with Drizzle ORM
- Redis caching
- SST v3 infrastructure

[Unreleased]: https://github.com/username/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/username/repo/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/username/repo/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/username/repo/releases/tag/v1.0.0
```

## Semantic Release Configuration

### .releaserc.json

```json
{
  "branches": ["main"],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    "@semantic-release/changelog",
    "@semantic-release/npm",
    "@semantic-release/github",
    "@semantic-release/git"
  ],
  "preset": "conventionalcommits",
  "releaseRules": [
    { "type": "feat", "release": "minor" },
    { "type": "fix", "release": "patch" },
    { "type": "perf", "release": "patch" },
    { "type": "revert", "release": "patch" },
    { "type": "docs", "release": false },
    { "type": "style", "release": false },
    { "type": "chore", "release": false },
    { "type": "refactor", "release": false },
    { "type": "test", "release": false" },
    { "type": "build", "release": false },
    { "type": "ci", "release": false }
  ],
  "parserOpts": {
    "noteKeywords": ["BREAKING CHANGE", "BREAKING CHANGES"]
  }
}
```

## Automated Changelog Generation

### GitHub Actions

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    branches:
      - main

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      issues: write
      pull-requests: write

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          persist-credentials: false

      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "pnpm"

      - run: pnpm install

      - name: Release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
        run: npx semantic-release
```

## Manual Changelog Updates

### Adding Unreleased Changes

```bash
# Edit CHANGELOG.md
vim CHANGELOG.md

# Add changes under [Unreleased] section
## [Unreleased]

### Added
- Add new feature X

### Fixed
- Fix bug Y
```

### Creating a New Release Entry

```markdown
## [1.3.0] - 2024-02-01

### Added
- Add user authentication
- Add admin panel

### Changed
- Upgrade Next.js to v16.1.0
- Update database schema

### Fixed
- Fix memory leak in cache
- Fix broken links in documentation

### Security
- Update vulnerable dependencies
```

## Commit Types and Changelog Sections

| Commit Type | Changelog Section | Version Bump |
|-------------|------------------|--------------|
| `feat:` | Added | Minor (0.x.0) |
| `fix:` | Fixed | Patch (0.0.x) |
| `perf:` | Performance | Patch |
| `refactor:` | Changed | None |
| `docs:` | Documentation | None |
| `style:` | Changed | None |
| `test:` | None | None |
| `chore:` | None | None |
| `build:` | None | None |
| `ci:` | None | None |
| `revert:` | Fixed | Patch |
| `BREAKING CHANGE` | Breaking Changes | Major (x.0.0) |

## Example Changelog Entries

### Feature Addition

```markdown
## [1.2.0] - 2024-01-15

### Added
- **Blog Generation**: Automatically generate blog posts from car registration data using Google Gemini AI
  - Configurable prompts for different content styles
  - Automatic SEO optimization
  - Support for custom topics
- **Social Media Integration**: Post updates to Discord, LinkedIn, Telegram, and Twitter
  - Automated posting when new data is available
  - Customizable message templates
  - Rate limiting support
```

### Bug Fix

```markdown
### Fixed
- **Database**: Fix connection timeout issue when processing large datasets
  - Increased connection pool size
  - Added connection retry logic
  - Improved error handling
- **Charts**: Fix chart rendering on mobile devices
  - Updated responsive breakpoints
  - Fixed touch event handling
  - Improved performance on low-end devices
```

### Breaking Change

```markdown
## [2.0.0] - 2024-03-01

### BREAKING CHANGES

- **API**: Changed authentication method from API keys to JWT tokens
  - Migration guide: https://docs.sgcarstrends.com/migration/v2
  - API keys deprecated and will be removed in v2.1.0
  - Update clients to use new authentication flow

- **Database**: Renamed `cars` table to `vehicle_registrations`
  - Run migration: `pnpm db:migrate`
  - Update queries to use new table name
  - Backward compatibility maintained until v2.1.0

### Added
- New authentication system with JWT tokens
- Support for refresh tokens
```

## Changelog Best Practices

### 1. Clear Descriptions

```markdown
# ❌ Vague
### Added
- Added stuff
- Fixed things

# ✅ Clear
### Added
- Add blog post generation with Gemini AI
- Add rate limiting to API endpoints (100 req/min per IP)

### Fixed
- Fix database connection timeout during large data imports
- Fix chart rendering issue on iOS Safari
```

### 2. Group Related Changes

```markdown
# ❌ Ungrouped
### Added
- Add feature A
- Fix bug X
- Add feature B
- Fix bug Y

# ✅ Grouped
### Added
- Add feature A with support for X
- Add feature B with support for Y

### Fixed
- Fix bug X that affected feature A
- Fix bug Y that affected feature B
```

### 3. Include Context

```markdown
# ❌ No context
### Fixed
- Fix bug

# ✅ With context
### Fixed
- Fix database connection timeout when processing > 10,000 records
  - Issue affected nightly data import job
  - Now uses connection pooling and batch processing
  - Performance improved by 50%
```

### 4. Link to Issues/PRs

```markdown
### Added
- Add user authentication ([#123](https://github.com/username/repo/pull/123))
- Add admin panel ([#124](https://github.com/username/repo/pull/124))

### Fixed
- Fix memory leak ([#125](https://github.com/username/repo/issues/125))
```

## Viewing Changelog

### GitHub Releases

1. Navigate to repository
2. Click "Releases" tab
3. View auto-generated release notes

### Local Viewing

```bash
# View CHANGELOG.md
cat CHANGELOG.md

# View specific version
grep -A 20 "## \[1.2.0\]" CHANGELOG.md

# View unreleased changes
grep -A 50 "## \[Unreleased\]" CHANGELOG.md
```

## Generating Changelog Manually

### Using semantic-release

```bash
# Dry run (preview without releasing)
npx semantic-release --dry-run

# Generate changelog
npx semantic-release
```

### Using git-changelog

```bash
# Install git-changelog
npm install -g generate-changelog

# Generate changelog
changelog

# Generate for specific version
changelog -p 1.2.0

# Generate from git history
git log --oneline --decorate
```

## Changelog Validation

### Check Format

```bash
# Install markdownlint
pnpm add -D markdownlint-cli

# Lint CHANGELOG.md
pnpm markdownlint CHANGELOG.md

# Fix formatting issues
pnpm markdownlint --fix CHANGELOG.md
```

### Check Links

```bash
# Check for broken links in changelog
grep -o 'http[s]*://[^)]*' CHANGELOG.md | xargs -I {} curl -s -o /dev/null -w "%{http_code} {}\n" {}
```

## Migration Guide Template

When creating breaking changes, include a migration guide:

```markdown
## [2.0.0] - 2024-03-01

### BREAKING CHANGES

#### Authentication Method Changed

**What changed:**
- API authentication now uses JWT tokens instead of API keys

**Migration steps:**

1. **Update client code** to use new authentication:
   ```javascript
   // Before
   headers: { 'X-API-Key': 'your-key' }

   // After
   headers: { 'Authorization': 'Bearer your-jwt-token' }
   \```

2. **Obtain JWT token** from new `/auth/login` endpoint:
   ```bash
   curl -X POST https://api.sgcarstrends.com/auth/login \
     -H 'Content-Type: application/json' \
     -d '{"username":"user","password":"pass"}'
   \```

3. **Update environment variables**:
   ```bash
   # Remove
   API_KEY=your-old-key

   # Add
   JWT_SECRET=your-jwt-secret
   \```

**Timeline:**
- API keys supported until: **April 1, 2024**
- Must migrate by: **March 31, 2024**

**Support:**
- Questions: [GitHub Discussions](https://github.com/username/repo/discussions)
- Issues: [GitHub Issues](https://github.com/username/repo/issues)
```

## Troubleshooting

### Semantic Release Not Generating Changelog

```bash
# Issue: No changelog generated
# Possible causes:
# 1. No conventional commits since last release
# 2. Wrong branch
# 3. Missing GITHUB_TOKEN

# Check commits
git log --oneline

# Check branch
git branch

# Verify GITHUB_TOKEN
echo $GITHUB_TOKEN
```

### Duplicate Entries

```bash
# Issue: Duplicate changelog entries
# Solution: Clean up CHANGELOG.md manually

# Remove duplicates
vim CHANGELOG.md

# Commit fix
git add CHANGELOG.md
git commit -m "docs: remove duplicate changelog entries"
```

## References

- Keep a Changelog: https://keepachangelog.com
- Semantic Versioning: https://semver.org
- Semantic Release: https://semantic-release.gitbook.io
- Conventional Commits: https://www.conventionalcommits.org
- Related files:
  - `CHANGELOG.md` - Project changelog
  - `.releaserc.json` - Semantic release config
  - Root CLAUDE.md - Release process

## Best Practices Summary

1. **Automatic Generation**: Use semantic-release for automated changelog
2. **Clear Descriptions**: Write clear, descriptive changelog entries
3. **Group Changes**: Group related changes together
4. **Breaking Changes**: Highlight breaking changes prominently
5. **Migration Guides**: Include migration steps for breaking changes
6. **Link References**: Link to issues and pull requests
7. **Regular Updates**: Keep changelog updated with each release
8. **User-Focused**: Write for end users, not developers
