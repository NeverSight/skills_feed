---
name: deployment-config-create
description: Configure deployment files with a common baseline file plus environment override files. Use when setting up or adjusting Makefile-first deployment for test/prod/custom environments and non-default SSH/SCP ports.
---

# Deployment Config Create

1. Use a Makefile-first workflow, but keep environment data in files.
2. Keep shared values in `.deploy.env.common`.
3. Keep environment differences in `.deploy.env.<ENV_MODE>`.
4. Run `scripts/create_config.py` to patch or create:
- `Makefile` deployment block (shared command contract)
- `Dockerfile` template (if missing)
- `docker-compose.local.yaml`, `docker-compose.test.yaml`, `docker-compose.yaml`
- `docker-compose.<custom-env>.yaml` for custom environments
- `.deploy.env.common`, `.deploy.env.test`, `.deploy.env.prod`, `.deploy.env.<custom-env>`
5. Use `REMOTE_PORT` in common or env override files for non-22 SSH/SCP.
6. Keep changes idempotent via managed markers.

## Command
```bash
python3 skills/deployment-config-create/scripts/create_config.py \
  --root . \
  --app-name "$APP_NAME" \
  --registry-host "$REGISTRY_HOST" \
  --remote-user "$REMOTE_USER" \
  --remote-host "$REMOTE_HOST" \
  --remote-port "$REMOTE_PORT" \
  --test-remote-host "$TEST_REMOTE_HOST" \
  --test-remote-port "$TEST_REMOTE_PORT" \
  --prod-remote-host "$PROD_REMOTE_HOST" \
  --prod-remote-port "$PROD_REMOTE_PORT" \
  --custom-env "$CUSTOM_ENV"

# Optional JSON profile input
python3 skills/deployment-config-create/scripts/create_config.py --root . --from-json deploy-profile.json
```
