---
name: scraps-coordination
description: Enables safe multi-agent collaboration on shared git repositories using the scraps.sh coordination primitives. Use this skill when multiple AI agents need to work on the same codebase simultaneously, when you need to claim files before editing to prevent conflicts, or when coordinating work with other agents.
---

# Scraps Multi-Agent Coordination

This skill enables AI coding assistants to safely collaborate on shared codebases using the scraps.sh git server's coordination primitives: Claim, Release, and Watch.

## When to Use This Skill

Use this skill when:

- Multiple AI agents are working on the same repository simultaneously
- You need to edit files in a shared codebase and want to prevent conflicts
- You want to coordinate work with other agents on a team
- You need to monitor repository activity or wait for files to become available
- The codebase is hosted on scraps.sh

## What is Scraps?

Scraps is a git hosting service with built-in coordination primitives for multi-agent development. The core commands are:

- `scraps claim` - Reserve file patterns before editing
- `scraps release` - Relinquish claims when done
- `scraps watch` - Monitor repository activity and claim changes in real-time

**Prerequisites:** Ensure you're authenticated before using scraps commands:

```bash
scraps login
scraps status  # Verify connection
```

## How to Coordinate with Other Agents

### Step 1: Claim Files Before Editing

**Always claim the files you intend to modify before editing them.**

```bash
scraps claim <store/repo:branch> <patterns...> -m "<description>"
```

Examples:

```bash
# Claim a specific file
scraps claim alice/webapp:main "src/components/Button.tsx" -m "Fixing button styling"

# Claim a directory
scraps claim alice/webapp:main "src/api/**" -m "Adding authentication endpoints"

# Claim multiple patterns
scraps claim alice/webapp:main "src/utils/**" "tests/utils/**" -m "Refactoring utility functions"
```

**Options:**

| Option | Description |
|--------|-------------|
| `-m, --message <msg>` | Describe your planned changes (required for coordination) |
| `--ttl <seconds>` | Claim duration (default: 300s / 5 minutes) |
| `--agent-id <id>` | Your identifier (auto-generated if omitted) |

**Important:** Save the agent-id from your claim - you'll need it to release.

### Step 2: Handle Claim Conflicts

If another agent has already claimed overlapping files, you'll receive a `claim_conflict` error showing which patterns conflict, which agent holds the claim, and their stated intent.

**When you encounter a conflict:**

1. Wait for the other agent to release their claim
2. Use `scraps watch <store/repo:branch> --claims` to monitor when files become available
3. Choose different files to work on
4. Coordinate with the other agent if possible

### Step 3: Make Your Changes

Once your claim is successful:

1. Make your code changes
2. Commit and push using standard git commands
3. Release your claim

### Step 4: Release When Done

**Always release your claims after pushing changes or abandoning work.**

```bash
scraps release <store/repo:branch> <patterns...> --agent-id <your-agent-id>
```

Example:

```bash
scraps release alice/webapp:main "src/api/**" --agent-id cli-abc12345
```

## Monitoring Repository Activity

### Watch for Commits and Branch Updates

```bash
scraps watch alice/webapp           # All branches
scraps watch alice/webapp -b main   # Specific branch
```

### Watch for Claim Activity

Monitor when files become available or claimed:

```bash
scraps watch alice/webapp:main --claims
```

This streams events when agents claim or release files, helping you know when contested files become available.

## Best Practices

### Pull Before Claiming

```bash
git pull origin main
scraps claim myteam/project:main "src/**" -m "Adding feature X"
```

### Use Small, Focused Claims

Claim only what you need. Broad claims like `"**"` block other agents unnecessarily.

**Good:**
```bash
scraps claim team/app:main "src/auth/login.ts" -m "Fixing login bug"
```

**Avoid:**
```bash
scraps claim team/app:main "src/**" -m "Fixing login bug"  # Too broad
```

### Use Appropriate TTLs

If your task is quick, use a shorter TTL:

```bash
scraps claim team/app:main "README.md" -m "Updating docs" --ttl 60
```

### Commit Frequently, Release Promptly

```bash
git add -A && git commit -m "Add login validation"
git push origin main
scraps release team/app:main "src/auth/**" --agent-id cli-abc123
```

## Reference Formats

| Format | Example | Usage |
|--------|---------|-------|
| Store/Repo | `alice/my-project` | Repo operations, clone |
| Store/Repo:Branch | `alice/my-project:main` | Claims, releases, branch-specific watch |
| Store/Repo:Branch:Path | `alice/my-project:main:src/index.ts` | File read operations |

## Pattern Syntax

Claims use glob patterns:

| Pattern | Matches |
|---------|---------|
| `src/index.ts` | Exact file |
| `src/*.ts` | All .ts files in src/ |
| `src/**` | Everything under src/ recursively |
| `**/*.test.ts` | All test files anywhere |
| `src/{api,utils}/**` | Both api and utils directories |

## Command Reference

### Claim

```bash
scraps claim <store/repo:branch> <patterns...> [options]
  -m, --message <msg>     Description of planned changes
  --agent-id <id>         Your agent identifier
  --ttl <seconds>         Claim duration (default: 300)
```

### Release

```bash
scraps release <store/repo:branch> <patterns...> --agent-id <id>
```

### Watch

```bash
scraps watch <store/repo[:branch]> [options]
  -b, --branch <branch>   Filter to specific branch
  --claims                Watch claim/release activity (requires branch)
  --last-event <id>       Resume from event ID
```

### Clone

```bash
scraps clone <store/repo> [directory]
  --url-only              Print clone URL only
```

### File Operations

```bash
scraps file read <store/repo:branch:path>    # Read file content
scraps file tree <store/repo:branch> [path]  # List directory
scraps log <store/repo:branch> [-n <count>]  # Commit history
```

## Example Multi-Agent Session

**Agent A** (working on API):

```bash
scraps claim team/app:main "src/api/**" "tests/api/**" -m "Adding user endpoints"
# ... makes changes ...
git add -A && git commit -m "Add user CRUD endpoints"
git push origin main
scraps release team/app:main "src/api/**" "tests/api/**" --agent-id cli-aaa111
```

**Agent B** (working on UI, runs concurrently):

```bash
scraps claim team/app:main "src/components/**" -m "Building user profile component"
# ... makes changes ...
git add -A && git commit -m "Add UserProfile component"
git push origin main
scraps release team/app:main "src/components/**" --agent-id cli-bbb222
```

**Agent C** (wants API files, must wait):

```bash
scraps claim team/app:main "src/api/users.ts" -m "Fixing user validation"
# Error: claim_conflict - Agent cli-aaa111 has claimed src/api/**

# Watch for availability:
scraps watch team/app:main --claims
# ... waits for release event ...

# Try again after Agent A releases:
scraps claim team/app:main "src/api/users.ts" -m "Fixing user validation"
# Success!
```

## Error Handling

| Error | Meaning | Action |
|-------|---------|--------|
| `claim_conflict` | Another agent holds conflicting claim | Wait, watch, or choose different files |
| `not_found` | Repo or branch doesn't exist | Verify the reference format |
| `unauthorized` | Not logged in or no access | Run `scraps login` or check permissions |
| `release_failed` | Agent ID doesn't match claim | Use the same agent-id from your claim |

## Summary

1. **Always claim before editing** - Prevents conflicts with other agents
2. **Use specific patterns** - Don't over-claim
3. **Release promptly** - Free files for others when done
4. **Watch for availability** - Monitor contested files
5. **Pull before claiming** - Start from latest code
6. **Push before releasing** - Ensure your changes are saved
