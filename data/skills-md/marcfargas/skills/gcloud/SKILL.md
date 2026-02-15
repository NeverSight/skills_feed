---
name: gcloud
description: >-
  Google Cloud Platform CLI (gcloud, gcloud storage, bq).
  Use when: managing GCP resources, deploying to Cloud Run/Cloud Functions/GKE/App Engine,
  working with Cloud Storage, BigQuery, IAM, Compute Engine, Cloud SQL, Pub/Sub,
  Secret Manager, Artifact Registry, Cloud Build, Cloud Scheduler, Cloud Tasks,
  Vertex AI, VPC/networking, DNS, logging/monitoring, or any GCP service.
  Also covers: authentication, project/config management, CI/CD integration,
  serverless deployments, container registry, docker push to GCP, managing secrets,
  Workload Identity Federation, and infrastructure automation.
---

# gcloud — Google Cloud Platform CLI

Command-line interface for managing Google Cloud resources.
Covers `gcloud`, `gcloud storage` (replaces `gsutil`), and `bq` (BigQuery).

## Platform Notes (Windows + Git Bash)

- Install: `scoop install gcloud` (preferred) or `GoogleCloudSDKInstaller.exe`
- If installed via scoop, `gcloud components install` may not work — use scoop to manage
- Config: `%APPDATA%/gcloud/` (PowerShell) or `~/.config/gcloud/` (Git Bash)
- Service account keys: store in `$TEMP` or project `.secrets/`, **never commit**
- Python: gcloud requires Python; scoop install handles this automatically

### ⚠️ Path Translation Gotcha

Git Bash auto-translates `/`-prefixed args, breaking some gcloud commands:

```bash
# FIX — disable MSYS path conversion:
export MSYS_NO_PATHCONV=1

# Or per-command:
MSYS_NO_PATHCONV=1 gcloud projects add-iam-policy-binding my-project ...
```

> **⚠️ Cost**: Commands that create resources (instances, clusters, databases) incur
> GCP charges. Always confirm project and region before creating.

## Agent Safety Model

Operations classified by risk. **Follow this model for all gcloud commands.**

| Level | Gate | Examples |
|-------|------|----------|
| **READ** | Proceed autonomously | `list`, `describe`, `get`, `logs read`, `config list`, `gcloud storage ls` |
| **WRITE** | Confirm with user; note cost if billable | `create`, `deploy`, `update`, `enable`, `gcloud storage cp` (upload) |
| **DESTRUCTIVE** | Always confirm; show what's affected | `delete`, `rm`, `gsutil rm -r`, `bq rm -r`, `rsync -d`, IAM removal |
| **EXPENSIVE** | Confirm + state approximate cost | GKE clusters (~$70+/mo), SQL instances (~$8-400/mo), VMs (~$5-2k/mo) |
| **SECURITY** | Confirm + explain impact | `--allow-unauthenticated`, firewall rules, IAM owner/editor grants |
| **FORBIDDEN** | Refuse; escalate to human | `gcloud iam service-accounts keys create`, `gcloud projects delete`, passwords in CLI args |

**Rules**:

- **Never combine `--quiet` with destructive operations** — it suppresses the only safety gate
- **Never put passwords/secrets as command-line arguments** — visible in process list & shell history
- **Always use `--format=json`** for machine-parseable output (agents can't reliably parse tables)
- **When in doubt, treat as DESTRUCTIVE**

## Command Structure

```text
gcloud [RELEASE_LEVEL] COMPONENT ENTITY OPERATION [ARGS] [FLAGS]
```

Key global flags: `--project`, `--format`, `--filter`, `--limit`, `--quiet`, `--verbosity`, `--async`

## Service Reference

| Service | File | Key Commands |
|---------|------|-------------|
| Auth & Config | [auth.md](ref/auth.md) | Login, ADC, impersonation, config profiles |
| IAM & Projects | [iam.md](ref/iam.md) | Projects, APIs, service accounts, Secret Manager |
| Compute & Networking | [compute.md](ref/compute.md) | VMs, SSH, firewall, VPC, DNS, static IPs |
| Serverless | [serverless.md](ref/serverless.md) | Cloud Run, Functions, App Engine, Scheduler, Tasks |
| Storage & Artifacts | [storage.md](ref/storage.md) | gcloud storage, Artifact Registry |
| Data | [data.md](ref/data.md) | Cloud SQL, BigQuery (bq), Pub/Sub |
| Automation & CI/CD | [automation.md](ref/automation.md) | Scripting, output formats, filtering, GitHub Actions, operations |

**Read the per-service file for full command reference.**

## Pre-Flight Checks

Before working with any GCP service:

```bash
# 1. Correct project?
gcloud config get-value project

# 2. Default region set?
gcloud config get-value compute/region

# 3. Required API enabled? (most APIs are disabled by default)
gcloud services list --filter="name:run.googleapis.com" --format="value(name)" | grep -q run || \
  gcloud services enable run.googleapis.com

# 4. Billing enabled?
gcloud billing projects describe $(gcloud config get-value project) --format="value(billingEnabled)"
```

**If you hit `PERMISSION_DENIED: ... API has not been enabled`**, enable the API
mentioned in the error and retry.

## Troubleshooting

| Problem | Diagnosis | Fix |
|---------|-----------|-----|
| Auth failure | `gcloud auth list` | `gcloud auth login` or check key file |
| Permission denied | Check IAM (see [iam.md](iam.md)) | Grant correct role |
| API not enabled | Error message says which API | `gcloud services enable API_NAME` |
| Quota exceeded | `gcloud compute project-info describe` | Request increase in Console |
| Wrong project | `gcloud config get-value project` | `gcloud config set project X` |
| Wrong region | `gcloud config get-value compute/region` | Set correct region; related resources must match |
| Config confusion | `gcloud config configurations list` | Check active config, override with `--project` |
| Slow commands | Large result set | Use `--filter`, `--limit`, `--format=value` |

```bash
# Debug mode
gcloud compute instances list --verbosity=debug

# Full environment info
gcloud info
```

## Quick Reference

| Task | Command |
|------|---------|
| Login | `gcloud auth login` |
| Set project | `gcloud config set project PROJECT_ID` |
| Current project | `gcloud config get-value project` |
| Enable API | `gcloud services enable API.googleapis.com` |
| List anything | `gcloud COMPONENT list --format=json` |
| Describe anything | `gcloud COMPONENT describe NAME --format=json` |
| JSON output | `--format=json` |
| Single value | `--format="value(field)"` |
| Filter | `--filter="field=value"` |
| Quiet ⚠️ | `--quiet` — suppresses ALL prompts including delete confirmations |
| Help | `gcloud COMPONENT --help` |
