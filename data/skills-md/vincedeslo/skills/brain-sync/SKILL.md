---
name: brain-sync
description: Commit and push the personal notes vault at ~/repos/personal/brain with a dated commit message. Use when asked to sync, save, commit, or push notes, the brain repo, or the second brain vault, or when the user says "brain-sync" or "brainsync".
compatibility: Requires git and a local clone of the notes vault at ~/repos/personal/brain with a configured remote and push credentials.
---

# brain-sync

Sync the personal notes vault: stage everything, commit with a dated message, push.

## When to use

The user asks to sync, save, commit, or push their notes / brain repo / vault, or says "brain-sync" or "brainsync".

## Instructions

1. Confirm the vault exists:

   ```bash
   test -d ~/repos/personal/brain/.git || echo "vault missing"
   ```

   Stop and report if it is missing.

2. Show what will be committed before changing anything:

   ```bash
   git -C ~/repos/personal/brain status --short
   ```

   If the output is empty, report "nothing to sync" and stop. Do not create an empty commit.

3. If the diff includes deletions of note files the user did not mention, list them and ask before continuing.

4. Run the sync:

   ```bash
   cd ~/repos/personal/brain && git add -A && git commit -m "brainsync $(date +%F)" && git push
   ```

5. Report the resulting commit hash and the push result:

   ```bash
   git -C ~/repos/personal/brain log --oneline -1
   git -C ~/repos/personal/brain status -sb | head -1
   ```

## Notes

- `brainsync` is an interactive shell alias for the command in step 4. Non-interactive agent shells do not load it, so run the full command instead of the alias name.
- The alias takes no arguments. Any argument passed to it is appended to `git push` — for example `brainsync --help` still commits, then prints the `git push` man page. Never invoke it to probe for usage.
- Commit message format is fixed: `brainsync YYYY-MM-DD`.

## Edge cases

- **Push rejected (remote ahead):** the commit is already local. Run `git -C ~/repos/personal/brain pull --rebase`, then push again.
- **Nothing staged:** `git commit` fails and the chain stops before push. This is the expected no-op.
- **Unwanted commit created:** undo with `git -C ~/repos/personal/brain reset --soft HEAD~1`, which keeps the files staged. Only safe before the push.
