---
name: deployment-record-archive
description: Archive deployment records with merged common+environment config context (including remote port) for Makefile-first deployment workflow.
---

# Deployment Record Archive

1. Read `.deploy.env.common` and `.deploy.env.<ENV_MODE>`.
2. Merge context and archive deployment result into JSONL.
3. Return record ID and archive location.

## Command
```bash
python3 skills/deployment-record-archive/scripts/archive_record.py \
  --root . \
  --env-mode prod \
  --version v2026.02.10.1 \
  --actor ci-bot \
  --result success \
  --archive-file deployment-records.jsonl
```
