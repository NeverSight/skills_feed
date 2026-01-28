---
name: changelog-generator
description: Generate CHANGELOG entries following conventional commits format with
  semantic versioning. Use when finalizing features to maintain proper change history.
allowed-tools: Read, Write, Edit, Bash, Grep
---

# CHANGELOG Generator Skill

## Purpose

This skill provides systematic guidance for generating CHANGELOG entries that follow conventional commits format and semantic versioning principles, ensuring clear and consistent change history documentation.

## When to Use

- After feature implementation and documentation updates
- Need to document changes for users and developers
- Following conventional commits format
- Determining semantic version increments
- Creating release notes

## CHANGELOG Generation Workflow

### 1. Analyze Changes

**Objective**: Understand what changed in this feature/fix.

**Review commit history**:
```bash
# View commits since last release/main
git log --oneline main..HEAD

# View detailed commits
git log main..HEAD

# View files changed
git diff --stat main..HEAD

# View actual changes
git diff main..HEAD
```

**Identify change types**:
- New features added
- Bug fixes implemented
- Documentation updates
- Performance improvements
- Security enhancements
- Breaking changes
- Deprecations

**Review issue and PR**:
- Read original issue description
- Review acceptance criteria
- Check PR description
- Note any breaking changes
- Identify security implications

**Deliverable**: Clear understanding of all changes

---

### 2. Determine Change Type

**Objective**: Classify the change according to conventional commits.

**Conventional Commit Types**:

| Type | Description | Version Impact | Use When |
|------|-------------|----------------|----------|
| `feat` | New feature | MINOR (0.X.0) | Adding new functionality |
| `fix` | Bug fix | PATCH (0.0.X) | Fixing a bug |
| `docs` | Documentation | PATCH (0.0.X) | Only docs changed |
| `style` | Code style | PATCH (0.0.X) | Formatting, whitespace |
| `refactor` | Code refactoring | PATCH (0.0.X) | Code restructure, no behavior change |
| `perf` | Performance | PATCH (0.0.X) | Performance improvements |
| `test` | Tests | PATCH (0.0.X) | Adding/updating tests |
| `chore` | Maintenance | PATCH (0.0.X) | Build, deps, configs |
| `BREAKING CHANGE` | Breaking change | MAJOR (X.0.0) | Incompatible API changes |

**Decision Tree**:
```
Does it add new functionality?
  └─ Yes → `feat` (MINOR bump)
  └─ No  → Does it fix a bug?
      └─ Yes → `fix` (PATCH bump)
      └─ No  → Is it a breaking change?
          └─ Yes → `BREAKING CHANGE` (MAJOR bump)
          └─ No  → Choose appropriate type (PATCH bump)
```

**Breaking Changes**:
A breaking change occurs when:
- Public API signature changes
- Required parameters added
- Return types changed
- Behavior changes in incompatible way
- Configuration format changes
- Removal of features

**Examples**:
```markdown
feat: add user authentication system (#123)
fix: resolve memory leak in cache manager (#124)
docs: update API documentation for v2.0 (#125)
refactor: simplify database connection logic (#126)
perf: optimize query performance with indexing (#127)
BREAKING CHANGE: change authentication API (#128)
```

**Deliverable**: Identified change type and version impact

---

### 3. Calculate Semantic Version

**Objective**: Determine the next version number.

**Semantic Versioning Format**: `MAJOR.MINOR.PATCH`

**Version Increment Rules**:
- **MAJOR** (X.0.0): Breaking changes, incompatible API
- **MINOR** (0.X.0): New features, backward compatible
- **PATCH** (0.0.X): Bug fixes, backward compatible

**Read current version**:
```bash
# From CHANGELOG.md
head -20 CHANGELOG.md

# From pyproject.toml (Python)
grep "^version" pyproject.toml

# From package.json (Node.js)
grep '"version"' package.json

# From __init__.py (Python)
grep "__version__" src/__init__.py
```

**Calculate next version**:
```python
# Example calculation
current = "1.2.3"  # Current version

# For MAJOR bump (breaking change)
next = "2.0.0"

# For MINOR bump (new feature)
next = "1.3.0"

# For PATCH bump (bug fix)
next = "1.2.4"
```

**Pre-release versions**:
```
1.0.0-alpha.1  # Alpha release
1.0.0-beta.1   # Beta release
1.0.0-rc.1     # Release candidate
```

**Deliverable**: Next version number

---

### 4. Generate CHANGELOG Entry

**Objective**: Create properly formatted CHANGELOG entry.

**Read existing CHANGELOG**:
```bash
# Read CHANGELOG to understand format
Read CHANGELOG.md
```

**CHANGELOG Format** (Keep a Changelog):
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.0] - 2024-01-15

### Added
- User authentication system with JWT tokens (#123)
- Password reset functionality (#125)
- Email verification for new accounts (#126)

### Changed
- Updated user profile API to include avatar URL (#127)
- Improved error messages for validation failures (#128)

### Fixed
- Memory leak in cache manager (#124)
- Race condition in concurrent requests (#129)

### Security
- Implemented rate limiting for login attempts (#130)
- Added CSRF protection for all forms (#131)

### Performance
- Optimized database queries with proper indexing (#132)
- Reduced API response time by 40% (#133)

### Deprecated
- `/api/v1/users` endpoint (use `/api/v2/users`) (#134)

### Removed
- Legacy authentication method (#135)

## [1.2.3] - 2024-01-01

### Fixed
- Critical bug in payment processing (#120)

[Unreleased]: https://github.com/user/repo/compare/v1.3.0...HEAD
[1.3.0]: https://github.com/user/repo/compare/v1.2.3...v1.3.0
[1.2.3]: https://github.com/user/repo/compare/v1.2.2...v1.2.3
```

**Entry Categories**:

| Category | Use For |
|----------|---------|
| **Added** | New features, new capabilities |
| **Changed** | Changes in existing functionality |
| **Fixed** | Bug fixes |
| **Deprecated** | Features marked for removal |
| **Removed** | Removed features |
| **Security** | Security improvements/fixes |
| **Performance** | Performance improvements |

**Writing Guidelines**:
- Start with verb: "Add", "Fix", "Update", "Remove"
- Be specific and clear
- Include issue/PR reference (#number)
- Write from user perspective
- Group related changes
- Highlight breaking changes

**Example Entries**:
```markdown
### Added
- User authentication system with JWT tokens and refresh token support (#123)
  - Supports email/password and OAuth providers
  - Includes session management and logout functionality
- Comprehensive test suite with 95% coverage (#125)

### Changed
- **BREAKING**: Authentication API now requires `Authorization` header instead of query parameter (#126)
- Database schema updated to support user roles (#127)

### Fixed
- Memory leak in cache manager causing high RAM usage (#124)
- Race condition in concurrent file uploads (#128)
- Incorrect error messages for validation failures (#129)

### Security
- Implemented rate limiting (100 req/min per IP) to prevent brute force attacks (#130)
- Added input sanitization to prevent XSS attacks (#131)
- Updated dependencies to fix security vulnerabilities (CVE-2024-1234) (#132)

### Performance
- Optimized database queries with proper indexing, reducing query time by 60% (#133)
- Implemented Redis caching for frequently accessed data (#134)
- Reduced API response time from 500ms to 200ms average (#135)
```

**Deliverable**: CHANGELOG entry content

---

### 5. Update CHANGELOG.md

**Objective**: Insert new entry into CHANGELOG.md.

**Process**:
1. Read current CHANGELOG.md
2. Find insertion point (after "## [Unreleased]" or at top)
3. Insert new version entry
4. Update comparison links at bottom
5. Verify formatting

**Update CHANGELOG.md**:
```markdown
# Changelog

## [Unreleased]

## [1.3.0] - 2024-01-15  ← NEW ENTRY HERE

### Added
- Your new features

### Fixed
- Your bug fixes

## [1.2.3] - 2024-01-01  ← Previous entry

### Fixed
- Previous fixes

[Unreleased]: https://github.com/user/repo/compare/v1.3.0...HEAD  ← Update this
[1.3.0]: https://github.com/user/repo/compare/v1.2.3...v1.3.0  ← Add this
[1.2.3]: https://github.com/user/repo/compare/v1.2.2...v1.2.3
```

**Use Edit tool**:
```python
# Read the file first
Read CHANGELOG.md

# Then edit to insert new entry
Edit CHANGELOG.md
old_string: "## [Unreleased]\n\n## [1.2.3]"
new_string: "## [Unreleased]\n\n## [1.3.0] - 2024-01-15\n\n### Added\n- Feature description (#123)\n\n## [1.2.3]"
```

**Deliverable**: Updated CHANGELOG.md file

---

### 6. Update Version Numbers

**Objective**: Update version in all relevant files.

**Files to update**:

#### pyproject.toml (Python)
```toml
[project]
name = "project-name"
version = "1.3.0"  # Update this
```

#### __init__.py (Python)
```python
"""Package initialization."""

__version__ = "1.3.0"  # Update this
__author__ = "Author Name"
```

#### package.json (Node.js)
```json
{
  "name": "package-name",
  "version": "1.3.0",  // Update this
  "description": "Package description"
}
```

#### setup.py (Python legacy)
```python
setup(
    name="package-name",
    version="1.3.0",  # Update this
    ...
)
```

**Update process**:
```bash
# Find all files with version numbers
Grep pattern="version.*=.*[0-9]+\.[0-9]+\.[0-9]+"

# Update each file
Edit pyproject.toml
old_string: 'version = "1.2.3"'
new_string: 'version = "1.3.0"'

Edit src/__init__.py
old_string: '__version__ = "1.2.3"'
new_string: '__version__ = "1.3.0"'
```

**Deliverable**: Version numbers updated in all files

---

### 7. Verify CHANGELOG Quality

**Objective**: Ensure CHANGELOG meets quality standards.

**Quality Checklist**:
- [ ] Version number correct (semantic versioning)
- [ ] Date is today's date (YYYY-MM-DD format)
- [ ] All changes categorized correctly
- [ ] Each entry has issue/PR reference
- [ ] Entries written from user perspective
- [ ] Breaking changes clearly marked
- [ ] Security fixes highlighted
- [ ] No typos or grammar errors
- [ ] Markdown formatted correctly
- [ ] Comparison links updated
- [ ] Consistent with previous entries

**Review Examples**:

**Good Entry**:
```markdown
### Added
- User authentication system with JWT and OAuth support (#123)
- Password reset flow with email verification (#125)
```
✅ Clear, specific, includes references

**Bad Entry**:
```markdown
### Added
- Authentication stuff
- Password thing
```
❌ Vague, no references, not informative

**Good Breaking Change**:
```markdown
### Changed
- **BREAKING**: Authentication API now requires `Authorization: Bearer <token>` header instead of `?token=` query parameter (#126)
  - Migration: Update client code to send token in header
  - Old method will be removed in v2.0.0
```
✅ Clearly marked, explains change, provides migration path

**Bad Breaking Change**:
```markdown
### Changed
- Auth API changed (#126)
```
❌ Not marked as breaking, no details, no migration help

**Deliverable**: Quality-verified CHANGELOG entry

---

## CHANGELOG Best Practices

### Writing Style

**DO**:
- ✅ Use clear, descriptive language
- ✅ Write from user perspective
- ✅ Be specific about what changed
- ✅ Include issue/PR references
- ✅ Group related changes
- ✅ Highlight breaking changes
- ✅ Explain security fixes
- ✅ Note performance improvements

**DON'T**:
- ❌ Use vague descriptions
- ❌ Write from developer perspective only
- ❌ Skip issue references
- ❌ Hide breaking changes
- ❌ Use technical jargon unnecessarily
- ❌ Forget to categorize changes

### Version Numbering

**DO**:
- ✅ Follow semantic versioning strictly
- ✅ Increment MAJOR for breaking changes
- ✅ Increment MINOR for new features
- ✅ Increment PATCH for bug fixes
- ✅ Use pre-release versions (alpha, beta, rc)

**DON'T**:
- ❌ Use arbitrary version numbers
- ❌ Skip versions
- ❌ Use wrong version format
- ❌ Forget to update all version files

### Change Categorization

**Added**: New features that users can now use
```markdown
### Added
- Dark mode toggle in settings (#123)
- Export data to CSV functionality (#124)
```

**Changed**: Modifications to existing features
```markdown
### Changed
- Improved search performance by 50% (#125)
- Updated UI layout for better mobile experience (#126)
```

**Fixed**: Bug fixes that users will notice
```markdown
### Fixed
- Crash when opening large files (#127)
- Incorrect calculation in reports (#128)
```

**Deprecated**: Features marked for future removal
```markdown
### Deprecated
- Legacy API endpoints (use v2 API) (#129)
  - Will be removed in version 3.0.0
```

**Removed**: Features that have been deleted
```markdown
### Removed
- Support for Internet Explorer 11 (#130)
```

**Security**: Security improvements or fixes
```markdown
### Security
- Fixed XSS vulnerability in comment system (CVE-2024-1234) (#131)
- Added rate limiting to prevent brute force attacks (#132)
```

**Performance**: Performance improvements
```markdown
### Performance
- Reduced page load time by 40% through lazy loading (#133)
- Optimized database queries for reports (#134)
```

---

## Examples

### Example 1: New Feature

**Scenario**: Added user authentication system

**Change Type**: `feat`
**Version**: 1.0.0 → 1.1.0 (MINOR bump)

**CHANGELOG Entry**:
```markdown
## [1.1.0] - 2024-01-15

### Added
- User authentication system with email/password and OAuth support (#123)
  - JWT-based authentication with refresh tokens
  - Session management with configurable timeout
  - Password reset flow with email verification
- User profile management interface (#125)
- Role-based access control (RBAC) system (#126)

### Security
- Implemented bcrypt password hashing (#124)
- Added rate limiting for login attempts (5 per minute) (#127)
- CSRF protection for all authenticated endpoints (#128)

[1.1.0]: https://github.com/user/repo/compare/v1.0.0...v1.1.0
```

---

### Example 2: Bug Fix

**Scenario**: Fixed memory leak

**Change Type**: `fix`
**Version**: 1.1.0 → 1.1.1 (PATCH bump)

**CHANGELOG Entry**:
```markdown
## [1.1.1] - 2024-01-16

### Fixed
- Memory leak in cache manager causing gradual RAM increase (#129)
- Race condition in concurrent file uploads (#130)
- Incorrect timezone handling in date filters (#131)

[1.1.1]: https://github.com/user/repo/compare/v1.1.0...v1.1.1
```

---

### Example 3: Breaking Change

**Scenario**: Changed authentication API

**Change Type**: `BREAKING CHANGE`
**Version**: 1.1.1 → 2.0.0 (MAJOR bump)

**CHANGELOG Entry**:
```markdown
## [2.0.0] - 2024-01-20

### Changed
- **BREAKING**: Authentication API now requires Bearer token in Authorization header (#132)
  - **Before**: `GET /api/resource?token=xxx`
  - **After**: `GET /api/resource` with `Authorization: Bearer xxx` header
  - **Migration**: Update all API clients to send token in header
  - Query parameter authentication will be removed in this version

- **BREAKING**: User model now requires email verification (#133)
  - All existing users marked as verified
  - New registrations require email confirmation
  - **Migration**: No action needed for existing users

### Added
- Improved token security with short-lived access tokens (#134)
- Automatic token refresh mechanism (#135)

### Deprecated
- `/auth/login-legacy` endpoint (use `/auth/login`) (#136)
  - Will be removed in v3.0.0

[2.0.0]: https://github.com/user/repo/compare/v1.1.1...v2.0.0
```

---

## Supporting Resources

### References
- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)

### Tools
```bash
# View git log
git log --oneline --graph --all

# View changes since tag
git log v1.0.0..HEAD

# View files changed
git diff --stat main..HEAD

# Create git tag
git tag -a v1.1.0 -m "Release version 1.1.0"
git push origin v1.1.0
```

---

## Integration with Deployment Flow

**Input**: Completed feature implementation and documentation
**Process**: Systematic CHANGELOG generation following conventions
**Output**: Updated CHANGELOG.md with proper versioning
**Next Step**: PR creation with CHANGELOG included

---

## Complete Workflow Example

```bash
# 1. Review changes
git log --oneline main..HEAD
git diff --stat main..HEAD

# 2. Determine change type
# Decision: New feature → feat → MINOR bump

# 3. Calculate next version
# Current: 1.2.3
# Next: 1.3.0 (MINOR bump for new feature)

# 4. Read current CHANGELOG
Read CHANGELOG.md

# 5. Generate entry content
# Write comprehensive entry with all changes

# 6. Update CHANGELOG.md
Edit CHANGELOG.md
# Insert new version section

# 7. Update version files
Edit pyproject.toml
# Change version to 1.3.0

Edit src/__init__.py
# Change __version__ to "1.3.0"

# 8. Verify quality
# Review entry for completeness and clarity

# 9. Commit
git add CHANGELOG.md pyproject.toml src/__init__.py
git commit -m "chore: update CHANGELOG for v1.3.0"
```

---

## Quality Standards

CHANGELOG is complete when:
- Version number follows semantic versioning
- All changes categorized correctly
- Each entry has issue/PR reference
- Breaking changes clearly marked
- Security fixes highlighted
- User perspective maintained
- Markdown properly formatted
- Version files updated
- Comparison links added
- No typos or errors