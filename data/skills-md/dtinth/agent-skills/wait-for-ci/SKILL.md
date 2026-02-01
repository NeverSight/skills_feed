---
name: wait-for-ci
description: Use this skill to wait for checks on GitHub Actions to finish on the current pull request
---

Make sure there is an active pull request for the current branch, then run this command in the project directory (not the skill base directory):

```
mise exec deno -- deno run --allow-run=gh --allow-env https://github.com/dtinth/wait-for-ci/raw/main/wait-for-ci.ts
```

This command:

- Monitors a GitHub pull request's status checks.
- Periodically polls and prints status updates and any changes.
- When all checks are finished, prints a summary of results, and exits.
