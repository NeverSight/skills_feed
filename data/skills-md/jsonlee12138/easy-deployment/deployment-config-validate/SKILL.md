---
name: deployment-config-validate
description: Validate deployment configuration from .deploy.env.common and .deploy.env.<ENV_MODE> for config-dependent stages. Use before make-based deploy actions to catch missing variables, invalid ports, or compose issues.
---

# Deployment Config Validate

1. Validate only config-dependent stages.
2. Ensure Makefile deployment block and required targets exist.
3. Ensure `.deploy.env.common` and `.deploy.env.<ENV_MODE>` exist and merge correctly.
4. Ensure required keys and `REMOTE_PORT` are valid.
5. Validate compose file for stages that depend on compose.

## Command
```bash
python3 skills/deployment-config-validate/scripts/validate_config.py \
  --root . \
  --env-mode test \
  --stage remote-deploy
```
