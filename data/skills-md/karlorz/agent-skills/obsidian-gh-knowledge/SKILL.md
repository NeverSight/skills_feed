---
name: obsidian-gh-knowledge
description: Operate an Obsidian vault stored in GitHub using a bundled gh-based CLI. Use when users ask to list folders, read notes, search content, create/update notes from templates, find project tasks/plans, or move/rename notes in a remote vault.
---

# Obsidian GitHub Knowledge

Use this skill to operate on a remote Obsidian vault stored in a GitHub repository without relying on local filesystem edits.

This skill should NOT guess which repo is your vault.

If the user does not provide `--repo`, require the user to either:

- Provide `--repo <owner/repo>` explicitly, or
- Set up the local config file described below, then use its `default_repo`.

## Practical Tips (Paths & Emoji)

- Always wrap `--path` values and file paths in quotes (emoji and spaces are common).
- Prefer copy/pasting the exact `path` returned by `list`/`search` instead of hand-typing emoji segments.
- Treat URL-encoded emoji in API output (e.g., `%EF%B8%8F%E2%83%A3`) as normal.
- If you get `HTTP 404`, assume the path is wrong or the file does not exist; verify with `list` or `search`.

## SAFETY RULES (CRITICAL)

These rules prevent accidental data loss. **NEVER bypass them.**

### 1. NEVER Force Push to Main

```bash
# FORBIDDEN - This can delete all files
gh api -X PATCH repos/.../git/refs/heads/main -F force=true

# FORBIDDEN - Direct reset
git push --force origin main
```

### 2. ALWAYS Use Feature Branches for Writes

All write operations MUST use a dedicated feature branch:
- `write`, `move`, `copy` commands require `--branch <name>`
- Branch name should be descriptive (e.g., `update-cmux-docs-20260222`)
- NEVER commit directly to `main`

### 3. ALWAYS Create PR for Merge

After writing to a branch, create a PR and let user review:
```bash
gh pr create --repo <owner/repo> --head <branch> --base main \
  --title "Update notes" --body "Changes: ..."
```

NEVER auto-merge without user confirmation.

### 4. Prefer Local Vault When Available

If a local vault exists at `~/Documents/obsidian_vault/`:
1. Use local git operations instead of GitHub API
2. Commit changes locally first
3. Push with `git push` (not force push)
4. This preserves git history and allows easy recovery via `git reflog`

### 5. Read Before Write

Before updating any file:
1. `read` the existing file content
2. Show diff to user if content differs significantly
3. Only proceed with user confirmation for large changes

### 6. Single-File Operations Only

- Write/move/copy ONE file per commit
- NEVER batch multiple unrelated files in one branch
- This makes rollback easier if something goes wrong

## Obsidian Note Authoring Guidelines

When creating or editing notes in an Obsidian vault, follow these conventions:

- If the workspace/repo has an `AGENTS.md`, read it and follow it (it overrides these defaults).

### Markdown

- Prefer a short `## TL;DR` near the top for human scanning.
- Use Obsidian wikilinks (`[[note-title]]`) for internal references instead of raw URLs.
- Keep headings stable; rename/move only when explicitly asked (links depend on titles/paths).
- Use YAML frontmatter for metadata (tags, aliases, dates).

### Mermaid (Obsidian Compatibility)

Obsidian's Mermaid renderer has quirks. Follow these rules to avoid rendering failures:

- Prefer `graph TB` / `sequenceDiagram` over newer Mermaid syntaxes.
- Avoid `subgraph ID[Label]` style; use quoted titles: `subgraph "Title"`.
- Avoid `\n` in node labels; use `<br/>` or keep labels single-line.
- Avoid parentheses and slashes in node labels; Obsidian chokes on `(...)` or `a/b` inside `[...]`.
- Keep node IDs ASCII and simple (`OC_GW`, `CMUX_DB`); avoid punctuation in IDs.
- If a diagram fails to render, simplify first (remove subgraphs/line breaks), then add complexity back.

### Vault Organization Conventions

Typical Obsidian vault folder structure (emoji prefixes for sorting):

| Directory          | Purpose                              |
|--------------------|--------------------------------------|
| `0️⃣-Inbox/`       | Uncategorized new notes              |
| `1️⃣-Index/`       | Maps of content (MOCs), overviews    |
| `2️⃣-Drafts/`      | Work-in-progress ideas               |
| `3️⃣-Plugins/`     | Plugin docs and configs              |
| `4️⃣-Attachments/` | Non-image assets (PDFs, sheets)      |
| `5️⃣-Projects/`    | Project documentation by category    |
| `assets/`          | Images and media                     |
| `100-Templates/`   | Reusable note templates              |

### Project Folder Convention (`5️⃣-Projects/`)

Each project folder **MUST** have a `_Overview.md` file as its Map of Content (MOC):

```
5️⃣-Projects/
├── GitHub/
│   ├── cmux/
│   │   ├── _Overview.md          # MOC index (required)
│   │   ├── cmux-tech-stack.md
│   │   └── ...
│   └── openclaw/
│       ├── _Overview.md          # MOC index (required)
│       ├── openclaw-local-status.md
│       └── ...
├── Infrastructure/
│   └── k8s/
│       └── _Overview.md
└── Research/
    └── _Overview.md
```

**`_Overview.md` Template Structure**:
- Start with `# Project Name (MOC)` heading
- Use `> [!info] Map of Content` callout with project metadata (repo, stack, updated date)
- Include Quick Navigation table linking key documents
- Include Documentation Index with Status column (Current, Reference, Active, etc.)
- Add architecture diagram (Mermaid) if applicable
- Include Cross-References section by topic
- End with Document Status Legend and Last Updated date

**When creating a new project folder**:
1. Create the folder under appropriate category (GitHub, Infrastructure, Research)
2. Create `_Overview.md` as the first file
3. Follow the MOC template structure
4. Link all related documents from the overview

When creating new notes:
- Place uncategorized notes in `Inbox` for later review.
- Use links and tags for navigation, not deep folder nesting.
- Check existing structure with `list` before assuming folder names.

### Templates

- For GitHub project notes, read and use `100-Templates/github-project-template.md` as the starting structure.
- Read the template:
  ```bash
  python3 ~/.agents/skills/obsidian-gh-knowledge/scripts/github_knowledge_skill.py --repo <owner/repo> read \
    "100-Templates/github-project-template.md"
  ```
- To scaffold a new project folder with `_Overview.md`:
  ```bash
  # Create the _Overview.md as the MOC index
  python3 ~/.agents/skills/obsidian-gh-knowledge/scripts/github_knowledge_skill.py --repo <owner/repo> copy \
    "100-Templates/github-project-template.md" \
    "5️⃣-Projects/GitHub/<project>/_Overview.md" \
    --branch "add-project-docs" \
    --message "Add project overview MOC"
  ```
- For additional notes in the project folder:
  ```bash
  python3 ~/.agents/skills/obsidian-gh-knowledge/scripts/github_knowledge_skill.py --repo <owner/repo> write \
    "5️⃣-Projects/GitHub/<project>/<note-name>.md" \
    --stdin \
    --branch "add-project-docs" \
    --message "Add project note"
  ```

## Repo Resolution Policy

Resolve the repository in this order:

1. If the user provides `--repo <owner/repo>`, use it.
2. If the user provides `--repo <key>` (no `/`), resolve it via `~/.config/obsidian-gh-knowledge/config.json` at `repos.<key>`.
3. If `--repo` is omitted, use `default_repo` from the same config file.
4. If none of the above is available, ask the user for the repo or ask them to set local config.

Never guess repo names.

## Requirements

- GitHub CLI installed: `gh`
- Authenticated: `gh auth status`

## Commands

All operations are performed via the bundled script:

```bash
python3 scripts/github_knowledge_skill.py --repo <owner/repo> <command> [args]
```

If the skill is installed globally, the script is typically located at:

```bash
python3 ~/.agents/skills/obsidian-gh-knowledge/scripts/github_knowledge_skill.py --repo <owner/repo> <command> [args]
```

- `list --path <path>`: List files in a directory.
- `read <file_path>`: Read file content.
- `search <query>`: Search code/content.
- `move <src> <dest> --branch <branch_name> --message <commit_msg>`: Move/rename a file by creating the destination file and deleting the source file on a branch.
- `copy <src> <dest> --branch <branch_name> --message <commit_msg>`: Copy a file by creating the destination file on a branch.
- `write <file_path> --stdin|--from-file <path> --branch <branch_name> --message <commit_msg>`: Create or update a file on a branch.

## Repo Selection (Local Config)

To avoid hard-coding a personal repo in prompts, store your vault repo(s) locally and have the agent/tooling read it.

First-time setup: create `~/.config/obsidian-gh-knowledge/config.json`:

```json
{
  "default_repo": "<owner>/<vault-repo>",
  "repos": {
    "personal": "<owner>/<vault-repo>",
    "work": "<org>/<work-vault-repo>"
  }
}
```

Usage (resolve repo at runtime):

```bash
REPO="$(python3 -c 'import json,os; p=os.path.expanduser("~/.config/obsidian-gh-knowledge/config.json"); print(json.load(open(p))["default_repo"])')"
python3 ~/.agents/skills/obsidian-gh-knowledge/scripts/github_knowledge_skill.py --repo "$REPO" list --path "0️⃣-Inbox"
```

If the user specifies a repo key (e.g., `work`), resolve it from `repos.<key>` instead of `default_repo`.

Example (resolve repo key):

```bash
REPO="$(python3 -c 'import json,os; p=os.path.expanduser("~/.config/obsidian-gh-knowledge/config.json"); c=json.load(open(p)); print(c["repos"]["work"])')"
python3 ~/.agents/skills/obsidian-gh-knowledge/scripts/github_knowledge_skill.py --repo "$REPO" search "dev plan"
```

## Quick Workflow Example

When asked to find and read a note:

1. List to discover exact paths:
   ```bash
   python3 ~/.agents/skills/obsidian-gh-knowledge/scripts/github_knowledge_skill.py --repo "$REPO" list --path "1️⃣-Index"
   ```

2. Search if the path is unknown:
   ```bash
   python3 ~/.agents/skills/obsidian-gh-knowledge/scripts/github_knowledge_skill.py --repo "$REPO" search "MOC"
   ```

3. Read the target file:
   ```bash
   python3 ~/.agents/skills/obsidian-gh-knowledge/scripts/github_knowledge_skill.py --repo "$REPO" read "1️⃣-Index/README.md"
   ```

## Search Query Tips

The `search` command uses GitHub code search. Include qualifiers directly in your query string:

```bash
# Search in specific folder
python3 ~/.agents/skills/obsidian-gh-knowledge/scripts/github_knowledge_skill.py --repo "$REPO" search "TODO path:1️⃣-Index/"

# Search project notes
python3 ~/.agents/skills/obsidian-gh-knowledge/scripts/github_knowledge_skill.py --repo "$REPO" search "project plan path:5️⃣-Projects/ extension:md"

# Find all project overviews
python3 ~/.agents/skills/obsidian-gh-knowledge/scripts/github_knowledge_skill.py --repo "$REPO" search "filename:_Overview.md"

# Find specific project overview
python3 ~/.agents/skills/obsidian-gh-knowledge/scripts/github_knowledge_skill.py --repo "$REPO" search "filename:_Overview.md path:5️⃣-Projects/GitHub/cmux"
```

## Workflow Reference

See `references/obsidian-organizer.md` for a concrete organizing workflow that uses these commands.

## Notes

- `search` uses GitHub code search; results may be empty for new commits until GitHub indexes them (typically seconds to minutes).
- Qualifiers like `path:`, `extension:`, `filename:` can narrow results - include them directly in the query string.
- Paths must match the repo exactly (including emoji and normalization). Use `list` to discover the exact directory names.
- Every project folder under `5️⃣-Projects/` MUST have a `_Overview.md` file as its MOC index.
- When creating new project documentation, always create `_Overview.md` first, then add related notes.

## Recovery Procedures

If files are accidentally deleted or corrupted:

### From Local Vault (Preferred)
```bash
cd ~/Documents/obsidian_vault
git reflog                          # Find good commit
git reset --hard <commit-sha>       # Restore locally
git push --force origin main        # Sync to remote (only if local is source of truth)
```

### From Remote (if local is lost)
```bash
# List commits to find pre-deletion state
gh api repos/<owner>/<repo>/commits --jq '.[].sha' | head -10

# Check file count at each commit
gh api repos/<owner>/<repo>/git/trees/<sha>?recursive=1 --jq '.tree | length'

# Reset remote to good commit (DANGEROUS - confirm with user first)
gh api -X PATCH repos/<owner>/<repo>/git/refs/heads/main \
  -F sha=<good-commit-sha> -F force=true
```

## Comparison: GitHub API vs Local Git

| Operation | GitHub API | Local Git |
|-----------|-----------|-----------|
| Recovery | Hard (no reflog) | Easy (reflog) |
| Atomic commits | Per-file only | Multi-file |
| Speed | Slower (HTTP) | Faster |
| Offline | No | Yes |
| Audit trail | Limited | Full |

**Recommendation**: When `~/Documents/obsidian_vault/` exists, prefer local git operations.
