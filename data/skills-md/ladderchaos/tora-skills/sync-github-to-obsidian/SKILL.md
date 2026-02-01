---
name: sync-github-to-obsidian
description: Syncs markdown documentation from GitHub projects to Obsidian vault. Use when user wants to sync, export, or copy .md files from their code repositories to Obsidian for documentation browsing.
---

# Sync GitHub to Obsidian

Automatically extract and organize markdown documentation from GitHub projects into Obsidian vaults.

## Configuration

Default paths (can be overridden by user):

- **GitHub folder**: `/Users/danieltang/GitHub`
- **Obsidian vault**: `~/Obsidian`

## Instructions

1. **Scan the GitHub folder** for project directories:
   ```bash
   ls -la /Users/danieltang/GitHub
   ```

2. **For each project**, find relevant .md files excluding:
   - `node_modules/`
   - `.git/`
   - `lib/` (dependency folders)
   - `target/` (Rust build)
   - `.changeset/` (auto-generated changesets)

3. **Create project folders** in the Obsidian vault:
   ```bash
   mkdir -p ~/Obsidian/PROJECT_NAME
   ```

4. **Copy .md files** preserving directory structure:
   ```bash
   find /Users/danieltang/GitHub/PROJECT_NAME -name "*.md" -type f \
     -not -path "*/node_modules/*" \
     -not -path "*/.git/*" \
     -not -path "*/lib/*" \
     -not -path "*/target/*" \
     -not -path "*/.changeset/*" \
     | while read f; do
       relpath="${f#/Users/danieltang/GitHub/PROJECT_NAME/}"
       dir=$(dirname "$relpath")
       mkdir -p ~/Obsidian/PROJECT_NAME/"$dir"
       cp "$f" ~/Obsidian/PROJECT_NAME/"$relpath"
     done
   ```

5. **Report summary** with file counts per project

## Options

When user requests sync, ask if they want to:
- Sync all projects or specific ones
- Clean existing folders first (full refresh) or merge
- Include or exclude `_legacy/` and `_archive/` folders

## Example Usage

User: "sync my github to obsidian"
User: "update obsidian with latest docs from github"
User: "export markdown from sooth-alpha to obsidian"

## Output Format

Provide a summary table:

| Project | Files | Description |
|---------|-------|-------------|
| project-name | 42 | Brief description from README |
