---
name: semver-changelog
description: Automate the creation and updating of a CHANGELOG.md file based on Semantic Versioning (SemVer) and "Keep a Changelog" principles. Use this skill when you need to summarize changes between the current HEAD and the latest git tag, or when initializing a new changelog for a project.
---

# Semver Changelog

This skill guides the agent through identifying released versions, analyzing git history, and documenting changes in a standard format.

## Overview

A consistent changelog helps users and contributors understand what has changed between versions. This skill ensures that `CHANGELOG.md` follows the [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format and adheres to [Semantic Versioning](https://semver.org/).

## Workflow

Follow these steps to update or create the changelog:

### 1. Identify Latest Released Tag
Find the most recent git tag that follows Semantic Versioning (e.g., `v1.2.3` or `1.2.3`).
- Use `git tag -l --sort=-v:refname` to list tags in version order.
- Filter for tags that match the `v?MAJOR.MINOR.PATCH` pattern.

### 2. Analyze Changes
Compare the current `HEAD` with the identified latest tag to see what has changed.
- Run `git diff <latest_tag>..HEAD` to see code changes.
- Run `git log <latest_tag>..HEAD --oneline` to see commit messages.

### 3. Group and Categorize Changes
Group the identified changes into the following categories:
- **Added**: New features.
- **Changed**: Changes in existing functionality.
- **Deprecated**: Soon-to-be removed features.
- **Removed**: Now removed features.
- **Fixed**: Bug fixes.
- **Security**: Security vulnerability fixes.

### 4. Update CHANGELOG.md
Update the `CHANGELOG.md` file at the repository root.
- If it doesn't exist, create it using the standard header.
- Add an `[Unreleased]` section if it doesn't exist, or update the existing one with the new changes.
- Ensure the file follows the "Keep a Changelog" structure.

## Guidelines

- Refer to [references/semver_reference.md](references/semver_reference.md) for detailed formatting and versioning rules.
- Always check the repository root for an existing `CHANGELOG.md` before creating a new one.
- Use the `[Unreleased]` section for changes that haven't been tagged yet.

## Examples

### Initializing a Changelog
If no changelog exists:
1. Create `CHANGELOG.md`.
2. Add the standard "Keep a Changelog" header.
3. Identify all tags and their changes to build the history, or start from the latest tag.

## Validation

After updating or creating the changelog, verify the following:
1. **File Existence**: Ensure `CHANGELOG.md` exists at the repository root.
2. **Format**: Check that the file includes the required header and that new changes are correctly categorized under the appropriate heading (e.g., `### Added`).
3. **Links**: If the file uses links at the bottom for versions, ensure they point to valid git comparison URLs (if applicable).
4. **SemVer**: Ensure the version numbers used follow the SemVer specification.

## Example Output

When reporting the update to the user, you can use a format like this:

### Changelog Update Summary
| Category | Changes Identified |
| :--- | :--- |
| **Added** | - New API endpoint for users |
| **Fixed** | - Bug in authentication logic |
| **Security** | - Updated dependencies to patch CVE-2023-XXXX |

**Latest Version:** [1.1.0]
**Previous Version:** [1.0.0]
