---
name: git-commit-workflow
description:
  Expertise in structured Git commit workflow with Chinese team conventions. Use
  this skill when the user asks to "commit", "提交", "stage", "暂存", "show status",
  "git status", or any variant related to managing git changes. The user does NOT
  need to explicitly mention "git-commit-workflow" - ANY request to commit changes
  or manage git state should automatically trigger this skill. Handles automatic
  commit message generation with PMS and GitHub Issue tracking, following strict
  80-character line limits.
---

# Git Commit Workflow

You are an expert in Git commit workflows with structured commit message generation.
Follow this procedure when assisting users with git operations.

## Core Principles

- **Never auto-commit**: Always get explicit user confirmation before executing `git commit`
- **Interactive staging**: Ask user to stage files if there are any unstaged changes, regardless of staged status
- **Structured messages**: Generate commit messages following the defined format
- **PMS/Issue tracking**: Ask for PMS and GitHub Issue numbers, parse them correctly

## Workflow Steps

### Step 1: Check Git Status

When user wants to commit, first check the current git status:

```bash
git status --porcelain
```

Interpret the output:
- First column: staged status (`M`=modified, `A`=added, `D`=deleted, `R`=renamed)
- Second column: working tree status
- Files with no first column: untracked/new files

Present the results to user with file lists separated by:
- **Staged files**: files with entries in first column (already staged)
- **Unstaged files**: files with entries in second column (changes in working directory) - includes both new and modified files

**Action guidance**:
- No staged, no unstaged → Inform user, ask to make changes first
- Has unstaged (regardless of staged status) → Must ask user which files to stage
- No unstaged, has staged → Ready for diff review (skip staging)

### Step 2: Stage Files (if needed)

User confirms which files to stage. Stage them:

```bash
git add <path1> <path2> ...
```

Ask user: "现在请查看暂存区的差异并生成提交信息草稿。"

### Step 3: Get Staged Diff and Generate Draft

Retrieve the staged changes:

```bash
git diff --staged
```

Analyze the diff and generate a commit message draft following the specified format.

## Commit Message Format

Follow this exact structure:

```
<type>[optional scope]: <english description> [MUST NOT exceed 80 chars]

[English body - optional, max 80 chars per line]

[Chinese body - optional, max 80 chars per line, must pair with English]

Log: [short description in Chinese]
PMS: <BUG-number or TASK-number> or omit this line if user has none
Issue: Fixes #<number> or omit this line if user has none
Influence: [explain impact in Chinese]
```

### Type Options

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect code meaning (formatting, spacing)
- `refactor`: Code refactoring without feature changes
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (build, deps, etc.)
- `ci`: CI/CD configuration changes

### Constraints

- Body lines must not exceed 80 characters
- English and Chinese body must appear in pairs if provided
- Log should be concise Chinese description

### Step 3.1: Handle PMS Number

**You MUST ask the user for PMS number**. Accept these formats:

1. **PMS URL**: `https://pms.uniontech.com/task-view-385999.html` or `https://pms.uniontech.com/bug-view-385999.html`
2. **Direct format**: `BUG-123456` or `TASK-123456`

Parse the input **using your own understanding** (no scripts needed):
- If URL contains `/task-view-` → extract the number, format as `TASK-xxxxxx`
- If URL contains `/bug-view-` → extract the number, format as `BUG-xxxxxx`
- If already in correct format (starting with BUG- or TASK-), use as-is
- If user provides just a number without prefix, **ask them** which type it is

Examples:
- `https://pms.uniontech.com/task-view-385999.html` → `TASK-385999`
- `https://pms.uniontech.com/bug-view-123456.html` → `BUG-123456`
- `TASK-789012` → `TASK-789012`

If user explicitly states they have **no PMS number**, remove the entire `PMS:` line from the commit message.

### Step 3.2: Handle GitHub Issue Number

**You MUST ask the user for GitHub Issue number**. Accept these formats:

1. **Issue URL**: `https://github.com/owner/repo/issues/183`
2. **Direct format**: `#183` (for current repo) or `owner/repo#183` (for other repos)

Parse the input **using your own understanding** (no scripts needed):
- From URL: extract owner, repo name, and issue number from the path
- From direct input: parse the format
- Determine if it's the current repository:
  - Run `git remote get-url origin` to check the current repo name
  - If the issue's repo matches, use `#<number>` format
  - If different, use `owner/repo#<number>` format
- If just a number without `#`, infer it's for current repo: `#183`

Examples:
- For repo `Pimzino/spec-workflow-mcp`:
  - `https://github.com/Pimzino/spec-workflow-mcp/issues/183` → `#183`
  - `#183` → `#183`
  - `183` → `#183`
  - `https://github.com/other/repo/issues/42` → `other/repo#42`

If user explicitly states they have **no Issue number**, remove the entire `Issue:` line from the commit message.

### Step 4: User Confirmation

Present the complete commit message draft in this format:

```
=== Commit Message Draft ===
<full draft content>
=== End Draft ===

Confirm? (Yes/No/Modify)
```

- If user confirms with "Yes" → proceed to commit
- If user says "No" → ask for feedback and regenerate
- If user wants to "Modify" → incorporate their changes and present again for confirmation

**Important**: You must get explicit user approval before committing. Never auto-commit.

### Step 5: Execute Commit

After user confirms, execute:

```bash
git commit -m "<commit message>"
```

Return success message to user.

## Handling Special Cases

### Initial Commit

If repository has no commits yet (detached HEAD or `git status` shows no HEAD), the first commit will be:

```bash
git commit -m "<commit message>"
```

This works without parent commits automatically.

### Empty Diff

If `git diff --staged` returns no output, inform user that there are no staged changes and they need to stage files first.

## Examples

### Example 1: Feature with PMS and Issue

User request: "帮我提交这个功能的代码"

1. Check status → User stages `src/auth.rs` and `src/auth_test.rs`
2. Diff shows authentication logic addition
3. Provide draft:
```
feat(auth): add JWT authentication support

Add JWT-based authentication middleware with token validation.

添加JWT认证中间件，支持令牌验证。

Log: 添加JWT认证功能
PMS: TASK-385999
Issue: Fixes #183
Influence: 所有API请求现在需要有效的JWT令牌通过认证，提升系统安全性。
```
4. User confirms "可以提交"
5. Execute `git commit`

### Example 2: Bug fix without PMS

User request: "commit this bug fix"

1. User stages fix, no PMS or Issue
2. Provide draft:
```
fix(user): resolve incorrect user role assignment

Use correct role mapping from database configuration.

修复用户角色分配错误的bug，使用正确的数据库配置映射。

Log: 修复角色映射bug
Influence: 修复后用户角色分配逻辑正确，避免权限错误。
```
3. User confirms and commit

## Tips

- Always explain what you're about to do before executing git commands
- If user provides feedback on the draft, show the complete revised message again for confirmation
- The Log field should be the most concise Chinese summary
- Influence should clearly state the impact on the system/users
- When in doubt, ask user for clarification rather than guessing
