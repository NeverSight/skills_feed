---
name: ship-ios-app
description: Ships new versions of iOS/macOS apps. Use when asked to ship, release, or deploy an app, or when checking if a version is ready to ship.
allowed-tools: Read, Bash, Grep, Glob, Edit, Task
---

# Ship iOS/macOS App Version

This skill manages the release workflow for iOS and macOS apps distributed via App Store Connect.

## Pre-flight Checks

Before shipping, verify ALL of the following conditions:

### 1. Check for Ready Pull Request
```bash
gh pr list --state open --json number,title,headRefName,statusCheckRollup
```

A PR is ready to ship ONLY if:
- There is an open PR targeting the main branch
- All status checks have passed (all items in statusCheckRollup show "SUCCESS")

**If no PR exists with passing tests, STOP and report: "No Pull Request ready to ship. A PR with passing tests is required."**

### 2. Verify Version Bump Has Occurred

Compare the version in README.md and CLAUDE.md against the last tagged version:

```bash
# Get the last tagged version
git fetch --tags
git tag --sort=-v:refname | head -1

# Check versions in documentation files
grep -i "version" README.md
grep -i "version" CLAUDE.md
```

**If the versions in README.md and CLAUDE.md match the last tagged version, STOP and report: "Version has not been bumped. Please update the version in README.md and CLAUDE.md before shipping."**

### 3. Verify Version Consistency with App Store

Check that BOTH marketing version AND build number are correct:

```bash
# Check local marketing version (what users see: 1.0, 2.0, 22, 23...)
MARKETING_VERSION=$(grep "MARKETING_VERSION" <YourApp>.xcodeproj/project.pbxproj | head -1 | grep -oE '[0-9]+(\.[0-9]+)*')
echo "Local Marketing Version: ${MARKETING_VERSION}"

# Check local build number (internal counter: 274, 275, 276...)
BUILD_NUMBER=$(agvtool what-version -terse)
echo "Local Build Number: ${BUILD_NUMBER}"
```

**CRITICAL**: iOS apps use TWO version numbers:
- **Marketing Version** (user-visible): 1.0, 2.0, 22, 23... (shown in App Store)
- **Build Number** (auto-incrementing): 274, 275, 276... (internal tracking)

Verify on TestFlight:
1. Marketing Version should match the version shown in TestFlight "Version" field
2. Build Number must be HIGHER than the latest TestFlight build number

**If marketing version doesn't match App Store, STOP and report: "Marketing version mismatch with App Store."**
**If build number is not higher than App Store, STOP and report: "Build number must be incremented beyond App Store Connect."**

### 4. Verify Changelog Entry Exists

Check that CHANGELOG.md has an entry for the current release in development:

```bash
# Get the version from project
VERSION=$(grep "MARKETING_VERSION" <YourApp>.xcodeproj/project.pbxproj | head -1 | grep -oE '[0-9]+(\.[0-9]+)*')

# Check if CHANGELOG.md has an entry for this version
grep -i "version ${VERSION}\|## ${VERSION}\|# ${VERSION}" CHANGELOG.md
```

**If no changelog entry exists for the current version, STOP and report: "Missing changelog entry. CHANGELOG.md must have an entry for version ${VERSION} before shipping."**

### 5. Determine Next Version

The next version is always one more than the last tag:
- If last tag is `v1.2.3`, next version is `v1.2.4`
- If last tag is `1.2.3`, next version is `1.2.4` (preserve format)

## Shipping Process

Once all pre-flight checks pass:

### Step 1: Merge the Pull Request

Squash merge to keep main branch history clean:

```bash
gh pr merge <PR_NUMBER> --squash --delete-branch
```

### Step 2: Fetch the Merge Commit

```bash
git fetch origin main
git checkout main
git pull origin main
```

### Step 3: Tag the Merge Commit

Tag the merge commit that was just created with the agreed-upon version:

```bash
git tag <VERSION>
git push origin <VERSION>
```

### Step 4: Verify and Report

```bash
# Verify the tag exists on remote
git ls-remote --tags origin | grep <VERSION>

# Show the tagged commit
git show <VERSION> --oneline --no-patch
```

Report success with:
- The version number that was shipped
- The PR number that was merged
- A link to the new tag/release

## Important Rules

1. **NEVER ship without a passing PR** - Quality gates are mandatory
2. **NEVER ship if version hasn't been bumped** - Each release must have a unique version
3. **NEVER ship if version doesn't match App Store canonical version** - Version consistency is critical
4. **NEVER ship without a changelog entry** - Users need to know what changed
5. **ALWAYS use squash merge** - Keep main branch history clean with `--squash` flag
6. **ALWAYS increment from last tag** - Version is always last tag + 1 (patch version)
7. **ALWAYS delete the branch after merge** - Keep the repo clean

## Failure Scenarios

| Scenario | Action |
|----------|--------|
| No open PR | Report "No PR ready to ship" |
| PR has failing tests | Report "Tests failing, cannot ship" |
| Version not bumped | Report "Version must be bumped before shipping" |
| Version doesn't match App Store | Report "Version mismatch with App Store canonical version" |
| Missing changelog entry | Report "CHANGELOG.md missing entry for current version" |
| Merge conflict | Report conflict and ask user to resolve |
| Tag already exists | Report error and verify correct version |
