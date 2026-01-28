---
name: git
description: Git operations for committing, pushing, and opening PRs using gh CLI. Use when performing version control tasks.
---

<essential_principles>

<git_safety>
**Never run destructive commands without explicit user request:**
- No `git push --force` to main/master
- No `git reset --hard`
- No `--no-verify` flag (skip hooks)
- No `git commit --amend` on pushed commits

**Always verify before acting:**
- Check `git status` before staging
- Check `git log` for commit style
- Check remote tracking before push
</git_safety>

<commit_format>
End all commit messages with:
```

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

Use HEREDOC for multi-line messages:
```bash
git commit -m "$(cat <<'EOF'
Message here

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```
</commit_format>

<pr_format>
PR body structure:
```markdown
## Summary
<1-3 bullet points>

## Test plan
- [ ] Test item 1
- [ ] Test item 2

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```
</pr_format>

</essential_principles>

<intake>
What would you like to do?

1. **Commit** - Stage and commit changes
2. **Push** - Push commits to remote
3. **PR** - Open a pull request
4. **Ship** - Full workflow: commit + push + PR

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "commit", "stage" | `workflows/commit.md` |
| 2, "push", "upload" | `workflows/push.md` |
| 3, "pr", "pull request", "open pr" | `workflows/pr.md` |
| 4, "ship", "full", "all" | Run commit → push → pr sequentially |

**After reading the workflow, follow it exactly.**
</routing>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| commit.md | Stage changes and create commit with proper message |
| push.md | Push commits to remote, create branch if needed |
| pr.md | Create pull request with gh CLI |
</workflows_index>
