---
name: git-workflow
description: Manage Git branches, commits, and pull requests following best practices
---

# Git Workflow

Manage Git operations and follow branching best practices.

## Capabilities

- Create and manage feature branches
- Write meaningful commit messages
- Handle merge conflicts
- Create and review pull requests

## Branch Naming

```
feature/  - New features (feature/add-user-auth)
bugfix/   - Bug fixes (bugfix/fix-login-error)
hotfix/   - Urgent production fixes (hotfix/security-patch)
release/  - Release preparation (release/v1.2.0)
```

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance

### Example
```
feat(auth): add OAuth2 login support

- Implement Google OAuth2 provider
- Add token refresh mechanism
- Store tokens securely in session

Closes #123
```

## Common Workflows

### Feature Branch
```bash
git checkout -b feature/new-feature
# ... make changes ...
git add .
git commit -m "feat: add new feature"
git push -u origin feature/new-feature
# Create PR
```

### Sync with Main
```bash
git checkout main
git pull origin main
git checkout feature/my-feature
git rebase main
```

## PR Checklist

- [ ] Tests pass
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] No merge conflicts
