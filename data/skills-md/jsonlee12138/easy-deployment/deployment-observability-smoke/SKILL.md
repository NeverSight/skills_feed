---
name: deployment-observability-smoke
description: Run post-deployment smoke checks with Makefile targets (`remote-status`, `remote-logs`) plus optional health URL checks. Use after deployment to verify runtime state before final acceptance.
---

# Deployment Observability Smoke

1. Run remote status check from Makefile.
2. Run remote logs scan for fatal patterns.
3. Optionally check health URL.
4. Return structured pass/fail result.

## Command
```bash
python3 skills/deployment-observability-smoke/scripts/smoke.py --root . --env-mode test --dry-run
python3 skills/deployment-observability-smoke/scripts/smoke.py --root . --env-mode prod --health-url "$HEALTH_URL"
```
