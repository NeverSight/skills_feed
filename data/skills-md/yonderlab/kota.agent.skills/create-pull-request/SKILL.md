---
name: create-pull-request
description: Create a pull request following the team's PR template and validation rules. Use when the user asks to create a pull request, create a PR, open a pull request, draft a PR, or prepare changes for review.
license: MIT
metadata:
  author: kota
  version: "1.1.0"
---

# Create Pull Request

## Preconditions

1. Verify `gh auth status` succeeds. If not, prompt user to run `gh auth login`.
2. Verify not on `main`/`master`. If so, prompt user to create a feature branch.
3. Verify no uncommitted changes. If found, prompt user to commit first (consider using `conventional-commit` skill).
4. If no upstream exists, run `git push -u origin HEAD`.

## PR Template

The PR description must follow the team's template structure. **See [references/pr-template.md](references/pr-template.md) for the full template, validation rules, and examples.**

Required sections:
1. **About PR 📝** - What changed and why (cannot be empty)
2. **Preview 🖼️** - Screenshot/recording (required for: Bug fix, New feature, Refactor, Improvement)
3. **How to test 🧪** - Testing instructions for reviewers
4. **Type of change 🔧** - Check at least one checkbox

Validation levels:
- **BLOCKING**: New feature, Improvement (PR cannot merge if validation fails)
- **WARNING**: Bug fix, Refactor
- **INFORMATIONAL**: Documentation, Testing

## Steps

### 1. Gather context

```bash
git diff main...HEAD --stat
git log main..HEAD --oneline
```

Understand: What problem does this solve? What is the impact?

### 2. Determine PR type

Identify the primary type based on changes. If multiple apply, choose the primary one.

### 3. Collect visual proof (if required)

For Bug fix, New feature, Refactor, or Improvement:

- Ask the user to provide a screenshot, recording, or link
- Verify the format is acceptable (see acceptable formats above)
- If the user cannot provide visual proof, warn them that:
  - Automated validation (if present) will fail
  - Manual review will require justification for missing visual proof

### 4. Draft the PR description

Use the template from [references/pr-template.md](references/pr-template.md):

```markdown
## About PR 📝

[2-3 sentences on value/impact, not implementation details]

## Preview (screenshot or recording) 🖼️

[If required: screenshot, video, or link]

## How to test 🧪

1. [Step-by-step testing instructions]
2. [What reviewers should check]

## Type of change 🔧

- [ ] Bug fix 🐛
- [ ] New feature ✨
- [ ] Refactor 🧹
- [ ] Improvement 📈
- [ ] Documentation 📝
- [ ] Testing 🧪
```

Mark the appropriate type with `[x]`.

### 5. Generate a concise title

Create a title that:

- Starts with a verb (Add, Fix, Update, Refactor, etc.)
- Is concise (< 72 characters)
- Describes the change, not the implementation

Examples:

- ✅ "Add user profile settings page"
- ✅ "Fix age validation for student dependants"
- ❌ "Update UserProfile.tsx and add new component"

### 6. Create the PR

Use the GitHub CLI to create the PR:

```bash
gh pr create --title "Your title here" --body "$(cat <<'EOF'
[Your complete PR description here]
EOF
)"
```

If creating a draft PR:

```bash
gh pr create --draft --title "Your title here" --body "$(cat <<'EOF'
[Your complete PR description here]
EOF
)"
```

### 7. Verify creation

After creation:

- Display the PR URL to the user
- If the repository has automated PR validation (e.g., `scripts/validate-pr-description.js`), note that GitHub Actions will validate the PR description
- Remind the user to review the PR checklist manually if no automated validation exists
- The PR can be edited on GitHub if any issues are found

## Validation Checklist

Verify the PR includes:

1. **About PR section** - Substantive content explaining value/impact
2. **Type of change** - At least one checkbox selected
3. **Visual proof** (if applicable) - For Bug fix, New feature, Refactor, Improvement
4. **Testing instructions** - Clear steps for reviewers
5. **Meaningful title** - Concise, verb-first description

## Notes

- Do not create PRs with empty or placeholder descriptions
- Visual proof is required for the specified types
- The PR can be edited after creation if validation fails
