---
name: npm-publisher
description: This skill must be loaded via the skill tool when the user mentions anything related to publishing or release an npm package. It contains essential knowledge about the complete release workflow. Things a user might say are Publish the npm package,Release a new version,Deploy to npm,Create a new release,Bump the version and publish
---

# NPM Publisher

## Overview

This skill provides a complete workflow for publishing npm packages with automated CI/CD. It handles version bumping, git tagging, and triggering automated npm publishing through GitHub Actions.

## Release Workflow

Follow this workflow when releasing a new version with unstaged changes:

### Step 1: Stage All Changes

Stage all pending changes:

```bash
git add .
```

### Step 2: Commit the Changes

Commit with a meaningful message describing what changed:

```bash
git commit -m "$(cat <<'EOF'
<Description of changes>

<Optional: more details>
EOF
)"
```

**Important:** Never add attributions to a coding agent in commit messages.

### Step 3: Determine Version Type

Ask the user which type of version bump is appropriate, or infer from the changes:

- **patch** - Bug fixes (3.0.2 → 3.0.3)
- **minor** - New features (3.0.3 → 3.1.0)
- **major** - Breaking changes (3.1.0 → 4.0.0)

If unclear, analyze the git diff to determine the appropriate version type based on:

- Bug fixes only → patch
- New features without breaking changes → minor
- Breaking changes or major refactors → major

### Step 4: Bump Version

Bump the version using npm:

```bash
npm version <patch|minor|major>
```

This command will:

- Increment the version in package.json
- Create a git commit with the version bump
- Create a git tag (e.g., v3.0.3)

### Step 5: Push Commits and Tags

Push both commits and tags to the remote repository:

```bash
git push && git push --tags
```

### Step 6: Verify Publishing

After pushing, publishing happens automatically through CI/CD:

1. GitHub Actions automatically publishes to npm when a new tag is pushed
2. Wait approximately 30 seconds for CI to complete
3. Verify the release succeeded:

```bash
gh run list --limit 1
```

### Step 7: Test the New Version

After CI completes successfully, verify the published version:

```bash
# Clear npx cache if needed
npx clear-npx-cache

# Test the new version (replace 'universal-skills' with the actual package name)
npx <package-name> --version
```

## Error Handling

### Common Issues

**Uncommitted changes error:**

- Ensure all changes are committed before running `npm version`
- Use `git status` to check for uncommitted changes

**Push rejected:**

- Pull latest changes with `git pull --rebase`
- Resolve any conflicts
- Retry the push

**CI/CD failure:**

- Check GitHub Actions logs: `gh run view --log`
- Common causes: failing tests, missing credentials, npm registry issues
- Fix the issue and create a new patch release if needed

**Version already exists:**

- Check if the version was already published: `npm view <package-name> versions`
- Bump to the next version if needed

## Best Practices

1. **Always review changes** before publishing with `git status` and `git diff`
2. **Run tests** before publishing to catch issues early
3. **Write meaningful commit messages** that explain the "why" not just the "what"
4. **Use semantic versioning** consistently to manage user expectations
5. **Verify the release** by testing the published package

## Pre-Release Checklist

Before starting the release workflow, ensure:

- [ ] All tests pass
- [ ] Build succeeds without errors
- [ ] Breaking changes are documented
- [ ] Dependencies are up to date
- [ ] No sensitive information in commits
