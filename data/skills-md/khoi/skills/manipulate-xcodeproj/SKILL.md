---
name: manipulate-xcodeproj
description: Manipulate Xcode projects and asset catalogs using XcodeProjectCLI (xcp) only. Use when editing .xcodeproj/.pbxproj files, adding/moving/renaming/deleting groups or files, changing target membership, reading or setting build settings, or managing xcassets assets.
---

# Manipulate Xcodeproj

## Overview

Use `xcp` for all project edits and asset catalog operations. Install it with `brew install xcp` if it is not already available.

## Workflow

1. Identify the `.xcodeproj` or `.xcassets` path.
2. For target-specific actions, run `xcp list-targets` first.
3. Run the appropriate `xcp` subcommand. Use `--project-only` to update the project file without touching the filesystem.
4. Re-run `xcp list-targets` or `xcp list-assets` if you need to verify results.

## Tasks

### Project structure

Use group and file subcommands to add, move, rename, or delete entries. Use `--create-groups` when adding and `--guess-target` when you want the tool to infer targets for a new file.

### Targets and build settings

Use `list-targets` to discover names, `set-target` to update file memberships, and build-setting commands to read or update configuration values.

### Asset catalogs

Operate on `.xcassets` directories directly for image, data, and color assets. Paths are relative to the `.xcassets` root.

## References

- Command and flag reference: `references/xcp-cli.md`
- For flags and usage specifics, prefer `xcp help <subcommand>` as the source of truth.
