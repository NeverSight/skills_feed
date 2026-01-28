---
name: recollect-worktree
description: Manages Git worktrees for Recollect development. Creates worktrees in .worktrees/, copies .env.local, and runs pnpm install. Use when reviewing PRs in isolation or working on features in parallel.
---

<objective>
Manage Git worktrees for isolated parallel development in the Recollect repository.

**What it does:**

- Creates worktrees from main branch with clear branch names
- Copies `.env.local` automatically (Supabase/Cloudflare keys)
- Runs `pnpm install` to make worktrees dev-ready
- Lists, switches between, and cleans up worktrees

**When to use:**

- Code review (`/review`): Isolated environment for reviewing PRs
- Feature work (`/work`): Parallel work on multiple features
- Testing: Test a feature branch without switching
  </objective>

<quick_start>

```bash
# Create a new worktree (copies .env.local, runs pnpm install)
bash .claude/skills/recollect-worktree/scripts/worktree-manager.sh create feature-name

# List all worktrees
bash .claude/skills/recollect-worktree/scripts/worktree-manager.sh list

# Switch to a worktree
bash .claude/skills/recollect-worktree/scripts/worktree-manager.sh switch feature-name

# Clean up inactive worktrees
bash .claude/skills/recollect-worktree/scripts/worktree-manager.sh cleanup
```

</quick_start>

<commands>
**`create <branch-name> [from-branch]`**

Creates new worktree with dependencies installed.

```bash
bash .claude/skills/recollect-worktree/scripts/worktree-manager.sh create feature-login
```

What happens:

1. Checks if worktree already exists
2. Updates base branch from remote
3. Creates new worktree and branch
4. Copies `.env.local`
5. Runs `pnpm install`
6. Shows path for cd-ing to worktree

**`list` or `ls`**

Lists all worktrees with their branches and status.

**`switch <name>` or `go <name>`**

Switches to an existing worktree.

**`cleanup` or `clean`**

Removes inactive worktrees with confirmation.
</commands>

<workflow_examples>
**PR Review:**

```bash
# Create worktree for PR review
bash .claude/skills/recollect-worktree/scripts/worktree-manager.sh create pr-664-lightbox

# Move to worktree and start dev
cd .worktrees/pr-664-lightbox
pnpm run dev

# After review, return and cleanup
cd ../..
bash .claude/skills/recollect-worktree/scripts/worktree-manager.sh cleanup
```

**Parallel Development:**

```bash
# Start first feature
bash .claude/skills/recollect-worktree/scripts/worktree-manager.sh create feature-a

# Start second feature
bash .claude/skills/recollect-worktree/scripts/worktree-manager.sh create feature-b

# Switch between them
bash .claude/skills/recollect-worktree/scripts/worktree-manager.sh switch feature-a
```

</workflow_examples>

<integration>
**`/review` command:**
1. Check current branch
2. If already on PR branch → stay there
3. If different branch → offer worktree:
   "Use worktree for isolated review? (y/n)"
   - yes → call recollect-worktree skill
   - no → proceed with PR diff on current branch

**`/work` command:**

1. Ask: "How do you want to work?"
   - New branch on current worktree (live work)
   - Worktree (parallel work)
2. If worktree → call recollect-worktree skill
   </integration>

<design_principles>
**KISS:** One manager script, simple commands, sensible defaults

**Opinionated Defaults:**

- Worktrees from `main` (unless specified)
- Stored in `.worktrees/` directory
- Branch name becomes worktree name
- `.env.local` copied automatically
- `pnpm install` runs automatically

**Safety First:**

- Confirms before creating/removing
- Won't remove current worktree
- Clear error messages
  </design_principles>

<technical_details>
**Directory structure:**

```
.worktrees/
├── feature-login/
│   ├── .git
│   ├── .env.local      # Copied from main
│   ├── node_modules/   # Installed via pnpm
│   └── ...
└── pr-664-lightbox/
    └── ...
```

**How it works:**

- Uses `git worktree add` for isolated environments
- Each worktree has its own branch
- Share git history with main repo
- Lightweight (filesystem links, no duplication)
  </technical_details>

<success_criteria>
Worktree is ready when:

- [ ] `.worktrees/<name>/` directory exists
- [ ] `.env.local` is present in worktree
- [ ] `node_modules/` exists (pnpm install completed)
- [ ] `pnpm run dev` starts successfully
      </success_criteria>
