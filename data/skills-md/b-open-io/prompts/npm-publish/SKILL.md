---
name: npm-publish
version: 1.0.1
description: This skill should be used when the user wants to publish a package to npm, bump a version, release a new version, or mentions "npm publish", "bun publish", "version bump", or "release". Handles changelog updates, git push, and npm publishing with OTP authentication.
---

# npm-publish

Publish npm packages using bun with proper versioning, changelog management, and git workflow.

## Workflow

### 1. Verify npm Login

**First, check if the user is logged into npm:**

```bash
npm whoami
```

If this returns a username, proceed. If it errors with "not logged in", **stop and instruct the user:**

> "You need to log into npm first. Please run `npm login` in your terminal and complete authentication, then let me know when you're ready."

**Do not proceed with any publish steps until `npm whoami` succeeds.** The user must handle npm login themselves as it requires interactive authentication.

### 2. Check Current State

Determine what needs to be released:

```bash
# Check last published version
npm view <package-name> version

# Check local package.json version
cat package.json | grep '"version"'

# Check commits since last release
git log --oneline $(git describe --tags --abbrev=0 2>/dev/null || echo HEAD~10)..HEAD
```

If no tags exist, check git log for release commits to identify the last published state.

### 3. Update Version

For projects in rapid/early development (0.x.x), always bump the patch version:

```
0.0.1 → 0.0.2 → 0.0.3 ...
```

Avoid major or minor bumps unless explicitly requested. Early-stage projects benefit from frequent small releases.

Edit `package.json` to update the version field.

### 4. Update CHANGELOG.md

Check if a changelog exists. If so, add an entry for the new version following the existing format. Typical structure:

```markdown
## [X.X.X] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes to existing functionality

### Fixed
- Bug fixes
```

Summarize the commits since the last release into appropriate categories.

### 5. Build and Verify

Run the project's build command to ensure everything compiles:

```bash
bun run build
```

### 6. Commit and Push FIRST

**Critical: Always push to git before publishing to npm.**

```bash
git add package.json CHANGELOG.md
git commit -m "Release vX.X.X"
git push origin <branch>
```

This ensures the published code matches what's in the repository. Publishing before pushing creates version mismatches that require additional releases to fix.

### 7. Request OTP

Before attempting to publish, ask the user for their npm OTP (One-Time Password) code. This is standard practice for npm 2FA:

> "Please provide your npm OTP code for publishing."

Wait for the user to provide the 6-digit code before proceeding.

### 8. Publish with bun

Use `bun publish` with the OTP:

```bash
bun publish --access public --otp <code>
```

For scoped packages (@org/package), `--access public` is required unless publishing to a private registry.

### 9. Verify Publication

After publishing, verify the new version is live:

```bash
npm view <package-name> version
```

**Note:** The bun/npm registry may take up to 5 minutes to reflect the new version. Do not attempt to work around this delay by using npm directly or re-publishing. Simply wait and verify again if needed.

## Common Issues

### Version Already Published

If the version already exists on npm, bump to the next patch version and repeat the workflow.

### OTP Expired

OTP codes are time-sensitive (usually 30 seconds). If publishing fails due to expired OTP, request a fresh code from the user.

### Registry Delay

After successful publish, `npm view` may still show the old version for several minutes. This is normal behavior—do not re-publish or attempt workarounds.
