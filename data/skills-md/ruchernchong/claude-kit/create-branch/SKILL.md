---
name: create-branch
description: Create and checkout a new git branch with smart validation and GitHub issue integration
allowed-tools: Bash(git status) Bash(git branch) Bash(git checkout) Bash(git push) Bash(git rev-parse) Bash(git ls-remote) Bash(gh issue develop) Bash(gh issue list) Bash(gh issue view)
metadata:
  model: sonnet
---

## Language Conventions

**Infer language style from the project:**
- Analyze existing branches, commit messages, and documentation to detect the project's language variant (US English, UK English, etc.)
- Match the spelling conventions found in the project (e.g., "synchronize" vs "synchronise", "center" vs "centre")
- Maintain consistency with the project's established language style throughout branch names and command outputs

---

# Create Branch Command

This command creates and checks out a new git branch with intelligent validation and GitHub issue integration.

## Priority: GitHub Issue Integration

**IMPORTANT**: If the user provides an issue number (e.g., "#123", "123", or "issue 123"), ALWAYS prioritise using GitHub CLI's issue development workflow:

1. **Check for GitHub CLI availability**:
   ```bash
   gh --version
   ```
   If not available, inform the user and fall back to manual branch creation.

2. **Verify the issue exists**:
   ```bash
   gh issue view <issue-number>
   ```
   Display issue title and status to confirm.

3. **Create branch linked to issue**:
   ```bash
   gh issue develop <issue-number> -c
   ```
   - The `-c` flag automatically checks out the newly created branch
   - GitHub automatically generates an appropriate branch name from the issue title
   - The branch is linked to the issue for better project tracking

4. **Skip to remote push step** (step 8 below)

## Manual Branch Creation Workflow

If no issue number is provided, follow this workflow:

### 1. Check Repository Status

```bash
git status
```

Verify:
- Clean working directory or acceptable uncommitted changes
- Current branch information
- Whether we're in a git repository

### 2. Get Branch Name Input

Ask the user for the desired branch name. Accept input in any format - the command will handle formatting and validation.

### 3. Auto-Detect and Apply Prefix

Analyse the branch name input for keywords and automatically add appropriate prefixes:

- **feature/** - Keywords: "add", "implement", "create", "new", "feature"
- **bugfix/** - Keywords: "fix", "bug", "resolve", "patch", "repair"
- **hotfix/** - Keywords: "hotfix", "urgent", "critical", "emergency"
- **chore/** - Keywords: "chore", "refactor", "update", "upgrade", "maintain"
- **docs/** - Keywords: "docs", "documentation", "readme", "guide"

If the user's input already starts with a recognised prefix (feature/, bugfix/, etc.), keep it as-is.

### 4. Validate Branch Name

Apply comprehensive validation:

#### Kebab-Case Enforcement
- Convert to lowercase
- Replace spaces and underscores with hyphens
- Ensure format is: `prefix/kebab-case-name`

#### Character Validation
Reject branch names containing:
- Spaces (convert to hyphens)
- Special characters: `~`, `^`, `:`, `?`, `*`, `[`, `]`, `\`, `@{`, `..`
- Control characters or non-ASCII (except hyphens and slashes)
- Leading or trailing slashes or hyphens

#### Length Validation
- Minimum: 3 characters (excluding prefix)
- Maximum: 100 characters (total)

### 5. Check for Duplicates

Check both local and remote branches:

```bash
# Check local branches
git branch --list "<branch-name>"

# Check remote branches
git ls-remote --heads origin "<branch-name>"
```

If branch exists:
- **Locally**: Offer to checkout existing branch instead
- **Remotely**: Warn user and suggest alternative name
- **Both**: Inform user and ask if they want to checkout or choose different name

### 6. Determine Base Branch

Use smart defaulting:

1. Check if `main` exists:
   ```bash
   git rev-parse --verify main
   ```

2. If not, check if `master` exists:
   ```bash
   git rev-parse --verify master
   ```

3. If neither exists, use current HEAD

4. Allow user to specify different base branch if needed (ask before creating)

### 7. Create and Checkout Branch

```bash
git checkout -b <validated-branch-name> <base-branch>
```

Confirm successful creation with a message showing:
- Branch name
- Base branch used
- Current status

### 8. Remote Push Recommendation

Ask the user: "Would you like to push this branch to remote and set up tracking?"

If yes:
```bash
git push -u origin <branch-name>
```

This enables:
- Remote backup of the branch
- Collaboration with team members
- GitHub PR creation workflow
- Branch visibility in GitHub UI

## Error Handling

Provide clear, actionable error messages:

- **Not a git repository**: "This directory is not a git repository. Initialise one with `git init` or navigate to a repository."
- **GitHub CLI not available**: "GitHub CLI (`gh`) is not installed. Install it from https://cli.github.com or use manual branch creation."
- **Issue not found**: "Issue #123 not found. Check the issue number or create a branch manually."
- **Invalid branch name**: "Branch name contains invalid characters. Suggested: `feature/valid-branch-name`"
- **Branch exists**: "Branch `feature/existing` already exists. Switch to it with `git checkout feature/existing` or choose a different name."
- **Network issues**: "Unable to check remote branches. Proceeding with local creation only."

## Examples

### Example 1: GitHub Issue Integration
```
User: "Create a branch for issue #456"
Command: gh issue view 456
Output: #456 - Add user authentication (open)
Command: gh issue develop 456 -c
Output: Created and checked out branch: feature/456-add-user-authentication
```

### Example 2: Manual with Auto-Prefix
```
User: "Create branch: fix login bug"
Analysis: Contains "fix" → apply "bugfix/" prefix
Validated: "bugfix/login-bug"
Command: git checkout -b bugfix/login-bug main
```

### Example 3: Custom Prefix
```
User: "Create branch: docs/update readme"
Analysis: Already has "docs/" prefix → keep as-is
Validated: "docs/update-readme"
Command: git checkout -b docs/update-readme main
```

## Best Practises

1. **Always prioritise GitHub issue workflow** when issue numbers are mentioned
2. **Validate thoroughly** before creating branches to avoid git errors
3. **Use descriptive names** that clearly indicate the purpose
4. **Follow team conventions** - check existing branch names for patterns
5. **Push to remote early** for backup and collaboration
6. **Link branches to issues** whenever possible for better project tracking
