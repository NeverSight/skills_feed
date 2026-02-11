---
name: deployment-execute
description: Execute deployment through Makefile targets with ENV_MODE and optional VERSION overrides. Use when running real deployment or dry-run preview in Makefile-first workflow.
---

# Deployment Execute

1. Run deployment using `make ENV_MODE=<env> <target>`.
2. Support dry-run preview using `make -n`.
3. Return command output and status in structured JSON.

## Command
```bash
python3 skills/deployment-execute/scripts/deploy.py --root . --env-mode test --target remote-deploy --dry-run
python3 skills/deployment-execute/scripts/deploy.py --root . --env-mode prod --target remote-deploy --version v2026.02.10.1
```
