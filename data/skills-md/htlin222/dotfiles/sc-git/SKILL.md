---
name: sc-git
description: Git operations with intelligent commit messages and branch management. Use when user needs git operations, commits, or branch management.
---

# Git Operations

Execute Git operations with intelligent commit messages, branch management, and workflow optimization.

## When to use

- User needs to commit changes with good messages
- Branch creation or management needed
- Git workflow operations required
- Merge or rebase assistance needed
- Repository state analysis requested

## Instructions

### Usage

```
/sc:git [operation] [args] [--smart-commit] [--branch-strategy]
```

### Arguments

- `operation` - Git operation (add, commit, push, pull, merge, branch, status)
- `args` - Operation-specific arguments
- `--smart-commit` - Generate intelligent commit messages
- `--branch-strategy` - Apply branch naming conventions
- `--interactive` - Interactive mode for complex operations

### Execution

1. Analyze current Git state and repository context
2. Execute requested Git operations with validation
3. Apply intelligent commit message generation
4. Handle merge conflicts and branch management
5. Provide clear feedback and next steps

### Claude Code Integration

- Uses Bash for Git command execution
- Leverages Read for repository analysis
- Applies TodoWrite for operation tracking
- Maintains Git best practices and conventions
