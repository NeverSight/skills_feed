---
name: homebrew-formula-updater
description: Update Homebrew formula files with latest GitHub release URLs and SHA256 checksums. This skill should be used when the user wants to update a Homebrew tap formula (.rb file) with a new version from a GitHub release. Triggers on phrases like "update formula", "update homebrew", "new release", "bump version", or when pointing to a .rb formula file that needs version updates.
license: MIT
allowed-tools: Read Write Edit Bash(python3:*)
metadata:
  group: "automation"
  category: "packaging"
  difficulty: "beginner"
  step-count: "3"
---

# Homebrew Formula Updater

## Overview

This skill automates updating Homebrew formula files with the latest release information from GitHub repositories. It fetches the newest release tag, downloads release assets to compute SHA256 checksums, and updates the formula file with new URLs and hashes.

## When to Use

- Updating a Homebrew formula after a new release is published
- Refreshing SHA256 checksums for release assets
- Bumping version numbers in formula files
- Syncing a homebrew-tap repository with upstream releases

## When NOT to Use

- Formulas that build from source (no prebuilt release assets)
- Formulas with non-standard asset naming conventions (not `<repo>-<tag>-<platform>.tar.gz`)
- Releases hosted outside GitHub (e.g., GitLab, self-hosted)
- Formulas requiring manual patching or complex post-download processing
- Creating new formulas from scratch (this skill only updates existing formulas)

## Workflow

### Step 1: Identify the Formula and Repository

Determine the following from the user's request or by examining the formula file:

1. **Formula file path** - The `.rb` file to update (e.g., `skulto.rb`)
2. **GitHub repository** - The source repo in `owner/repo` format (e.g., `asteroid-belt/skulto`)

The repository can often be inferred from the `homepage` or `url` fields in the formula.

### Step 2: Run the Update Script

Execute the bundled Python script to fetch the latest release and update the formula:

```bash
python3 <skill-path>/scripts/update_formula.py <github_repo> <formula_file>
```

Example:
```bash
python3 scripts/update_formula.py asteroid-belt/skulto skulto.rb
```

The script will:
1. Query the GitHub API for the latest release tag
2. Download each platform-specific asset (darwin-amd64, darwin-arm64, linux-amd64, linux-arm64)
3. Compute SHA256 checksums for each asset
4. Update the formula file with new version, URLs, and checksums
5. Create a backup of the original file (`.bak` extension)

### Step 3: Verify Changes

After the script completes:

1. Review the updated formula file to ensure changes are correct
2. Optionally run `brew audit --strict <formula>` to validate the formula syntax
3. Test installation with `brew install --build-from-source <formula>`

### Dry Run Mode

To preview changes without modifying the formula:

```bash
python3 <skill-path>/scripts/update_formula.py <github_repo> <formula_file> --dry-run
```

## Expected Formula Structure

The script expects formulas with platform-specific blocks like:

```ruby
on_macos do
  if Hardware::CPU.intel?
    url "https://github.com/owner/repo/releases/download/vX.Y.Z/name-vX.Y.Z-darwin-amd64.tar.gz"
    sha256 "..."
  elsif Hardware::CPU.arm?
    url "https://github.com/owner/repo/releases/download/vX.Y.Z/name-vX.Y.Z-darwin-arm64.tar.gz"
    sha256 "..."
  end
end

on_linux do
  if Hardware::CPU.intel?
    url "https://github.com/owner/repo/releases/download/vX.Y.Z/name-vX.Y.Z-linux-amd64.tar.gz"
    sha256 "..."
  elsif Hardware::CPU.arm?
    url "https://github.com/owner/repo/releases/download/vX.Y.Z/name-vX.Y.Z-linux-arm64.tar.gz"
    sha256 "..."
  end
end
```

## Asset Naming Convention

The script expects release assets named:
```
<repo-name>-<tag>-<platform>.tar.gz
```

Where `<platform>` is one of: `darwin-amd64`, `darwin-arm64`, `linux-amd64`, `linux-arm64`

## Quality Checklist

Before completing the update:

- [ ] Verified the GitHub repository has the expected release asset naming convention
- [ ] Ran with `--dry-run` first to preview changes
- [ ] Reviewed the updated formula for correctness
- [ ] Backup file (`.bak`) preserved in case rollback is needed
- [ ] Optionally ran `brew audit --strict <formula>` to validate syntax
- [ ] Optionally tested with `brew install --build-from-source <formula>`

## Resources

### scripts/

- **update_formula.py** - Python script that fetches the latest release and updates formula files (requires Python 3.8+)
