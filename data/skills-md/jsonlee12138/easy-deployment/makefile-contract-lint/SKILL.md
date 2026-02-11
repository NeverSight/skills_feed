---
name: makefile-contract-lint
description: Lint Makefile contract for common+env override deployment workflow. Use when validating deployment variables, include rules, remote port handling, and required targets.
---

# Makefile Contract Lint

1. Validate deployment markers and required variables.
2. Validate common+env include strategy.
3. Validate required Makefile targets.
4. Validate `FULL_REGISTRY_IMAGE` composition and `ssh/scp` port usage.

## Command
```bash
python3 skills/makefile-contract-lint/scripts/lint_makefile.py --root .
```
