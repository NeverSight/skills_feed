---
name: auto-claude-workspace
description: Auto-Claude workspace and git worktree management. Use when reviewing changes, merging builds, managing branches, or understanding isolation strategy.
version: 1.0.0
auto-claude-version: 2.7.2
---

# Auto-Claude Workspace Management

Git worktree isolation, branch management, and merge operations.

## Workspace Architecture

### Git Worktree Strategy

Auto-Claude uses git worktrees for complete isolation:

```
project-root/
├── .git/                      # Main git directory
├── src/                       # Your project files
├── .auto-claude/              # Auto-Claude data
│   └── specs/                 # Spec definitions
└── .worktrees/                # Isolated workspaces
    └── auto-claude/
        └── 001-feature/       # Feature worktree
            ├── src/           # Copy of project
            └── ...            # Changes made here
```

### Branch Strategy

```
main (or your current branch)
└── auto-claude/{spec-name}    # Isolated branch per spec
```

**Key Principles:**
- ONE branch per spec
- All changes in isolated worktree
- NO automatic pushes to remote
- User controls when to merge/push

## Workspace Operations

### Review Changes

```bash
cd apps/backend

# Review what was built
python run.py --spec 001 --review
```

Output shows:
- Files changed
- Additions/deletions
- Commit history

### Test in Worktree

```bash
# Navigate to worktree
cd .worktrees/auto-claude/001-feature/

# Run your project
npm run dev
# or
python manage.py runserver
# or your project's run command

# Test the feature
# ...

# Return to backend
cd ../../apps/backend
```

### Merge Changes

```bash
# Merge completed build into your project
python run.py --spec 001 --merge
```

This:
1. Checks for conflicts
2. Merges `auto-claude/001-feature` into current branch
3. Uses AI resolver for conflicts (if any)
4. Cleans up worktree

### Discard Build

```bash
# Discard if you don't want the changes
python run.py --spec 001 --discard
```

This:
1. Asks for confirmation
2. Deletes worktree
3. Deletes branch
4. Keeps spec for reference (optional)

## Manual Worktree Operations

### Create Worktree Manually

```bash
# Create new worktree
git worktree add .worktrees/experiment -b experiment-branch

# Work in it
cd .worktrees/experiment
# make changes...

# Return and cleanup
cd ../..
git worktree remove .worktrees/experiment
```

### List Worktrees

```bash
git worktree list
```

### Prune Stale Worktrees

```bash
# Remove worktrees for deleted directories
git worktree prune
```

## Conflict Resolution

### AI-Powered Merge

Auto-Claude uses AI to resolve merge conflicts:

1. **Detection**: Identifies conflicting files
2. **Analysis**: Understands both versions
3. **Resolution**: Merges intelligently
4. **Verification**: Validates result

### Manual Resolution

If AI merge fails:

```bash
# Navigate to worktree
cd .worktrees/auto-claude/001-feature/

# Attempt manual merge
git merge main

# Resolve conflicts in your editor
code .

# Complete merge
git add .
git commit -m "Resolved merge conflicts"

# Return and complete
cd ../../apps/backend
python run.py --spec 001 --merge
```

## Branch Management

### View Branches

```bash
# List all branches
git branch -a

# See auto-claude branches
git branch | grep auto-claude
```

### Delete Old Branches

```bash
# Delete local branch
git branch -d auto-claude/old-feature

# Delete remote branch (if pushed)
git push origin --delete auto-claude/old-feature
```

### Switch Base Branch

```bash
# Set default base branch in .env
echo "DEFAULT_BRANCH=develop" >> apps/backend/.env
```

## Workspace Data

### Worktree Metadata

```bash
# View worktree info
cat .auto-claude/specs/001-feature/worktree.json
```

```json
{
  "worktree_path": ".worktrees/auto-claude/001-feature",
  "branch_name": "auto-claude/001-feature",
  "base_branch": "main",
  "created_at": "2024-01-01T10:00:00Z",
  "status": "active"
}
```

### Build Isolation

Each worktree is completely isolated:
- Separate working directory
- Own git index
- Independent node_modules (if needed)
- No interference with main branch

## Best Practices

### Before Merging

1. **Review changes thoroughly**
   ```bash
   python run.py --spec 001 --review
   ```

2. **Test in worktree**
   ```bash
   cd .worktrees/auto-claude/001-feature/
   npm test
   npm run build
   ```

3. **Check for conflicts**
   ```bash
   git diff main...auto-claude/001-feature
   ```

### After Merging

1. **Run full test suite**
   ```bash
   npm test
   ```

2. **Verify functionality**
   ```bash
   npm run dev
   # Test manually
   ```

3. **Commit and push when ready**
   ```bash
   git push origin main
   ```

### Cleanup Old Worktrees

```bash
# List and remove old worktrees
git worktree list
git worktree remove .worktrees/auto-claude/old-feature

# Or use discard command
python run.py --spec old --discard
```

## Troubleshooting

### Worktree Already Exists

```bash
# Remove existing worktree
git worktree remove .worktrees/auto-claude/001-feature

# Retry build
python run.py --spec 001
```

### Branch Already Exists

```bash
# Delete existing branch
git branch -D auto-claude/001-feature

# Retry build
python run.py --spec 001
```

### Merge Conflicts

```bash
# Manual resolution
cd .worktrees/auto-claude/001-feature/
git merge main --no-commit

# Resolve each file
git status
code path/to/conflicted/file

# Complete
git add .
git commit
cd ../../apps/backend
```

### Corrupted Worktree

```bash
# Remove and recreate
git worktree remove --force .worktrees/auto-claude/001-feature
git worktree prune

# Delete spec and restart
rm -rf .auto-claude/specs/001-feature
python spec_runner.py --task "Your task"
```

## Related Skills

- **auto-claude-cli**: CLI commands
- **auto-claude-build**: Build process
- **auto-claude-troubleshooting**: Debugging
