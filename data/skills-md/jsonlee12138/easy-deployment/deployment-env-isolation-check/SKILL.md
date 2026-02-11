---
name: deployment-env-isolation-check
description: Validate environment isolation using merged values from .deploy.env.common and .deploy.env.<ENV_MODE>. Use when ensuring test/prod/custom do not share the same registry, remote host, user, and port identity.
---

# Deployment Env Isolation Check

1. Read `.deploy.env.common` and all `.deploy.env.<env>` files.
2. Merge common defaults with per-env overrides.
3. Compare environment identities (`registry + user + host + port`).
4. Fail when non-prod and prod identities are identical.

## Command
```bash
python3 skills/deployment-env-isolation-check/scripts/check_isolation.py --root .
```
