---
name: azcli
description: >-
  Azure CLI (az). Use when: managing Azure resources, deploying to App Service/Functions/Container Apps/AKS,
  working with Storage, SQL Database, Cosmos DB, VMs, VNets, NSGs, Key Vault,
  Entra ID (Azure AD), RBAC, Service Bus, Event Hubs, Container Registry,
  Azure Monitor, DNS, or any Azure service.
  Also covers: authentication, subscription management, CI/CD integration (GitHub Actions/Azure DevOps),
  Bicep/ARM templates, managed identities, and infrastructure automation.
---

# azcli — Azure Command-Line Interface

Command-line interface for managing Azure resources.
Covers `az` and its 200+ command groups for all Azure services.

Docs: https://learn.microsoft.com/en-us/cli/azure/

## Platform Notes (Windows + Git Bash)

- Install: `winget install --exact --id Microsoft.AzureCLI` (preferred) or MSI from https://aka.ms/installazurecliwindows
- After install/update: **close and reopen terminal** — required for PATH
- Config: `~/.azure/` (credentials, config, profiles)
- Secrets: use Key Vault or env vars, **never commit credentials**
- Extensions: `az extension add --name NAME` (some features require extensions)
- Version: `az version` (check for updates: `az upgrade`)

### ⚠️ Quoting Gotchas

Git Bash, PowerShell, and cmd have different quoting rules for `--query` (JMESPath):

```bash
# Git Bash — use single quotes for JMESPath
az vm list --query '[].name' -o tsv

# PowerShell — use single quotes or escaped double quotes
az vm list --query '[].name' -o tsv

# Avoid: Git Bash may mangle double-quoted JMESPath
```

> **⚠️ Cost**: Commands that create resources (VMs, databases, clusters) incur
> Azure charges. Always confirm subscription and region before creating.

## Agent Safety Model

Operations classified by risk. **Follow this model for all az commands.**

| Level | Gate | Examples |
|-------|------|----------|
| **READ** | Proceed autonomously | `list`, `show`, `get`, `account show`, `monitor log-analytics query` |
| **WRITE** | Confirm with user; note cost if billable | `create`, `deploy`, `update`, `az storage blob upload` |
| **DESTRUCTIVE** | Always confirm; show what's affected | `delete`, `purge`, `az group delete`, RBAC removal |
| **EXPENSIVE** | Confirm + state approximate cost | AKS clusters (~$70+/mo), SQL Database (~$5-2k/mo), VMs (~$5-2k/mo) |
| **SECURITY** | Confirm + explain impact | NSG rules opening ports, `--allow-unauthenticated`, RBAC owner/contributor grants, Key Vault access policies |
| **FORBIDDEN** | Refuse; escalate to human | `az ad app credential reset` with plaintext secrets, `az group delete` on production RGs, passwords in CLI args |

**Rules**:

- **Never combine `--yes` with destructive operations** — it suppresses the only safety gate
- **Never put passwords/secrets as command-line arguments** — visible in process list & shell history
- **Always use `-o json`** for machine-parseable output (agents can't reliably parse tables)
- **When in doubt, treat as DESTRUCTIVE**

## Command Structure

```text
az [GROUP] [SUBGROUP] COMMAND [ARGS] [FLAGS]
```

Key global flags: `--subscription`, `--output` (`-o`), `--query`, `--verbose`, `--debug`, `--only-show-errors`, `--yes`

## Service Reference

| Service | File | Key Commands |
|---------|------|-------------|
| Auth & Config | [auth.md](ref/auth.md) | Login, service principals, managed identities, subscriptions, config |
| IAM & Resources | [iam.md](ref/iam.md) | Resource groups, RBAC, Entra ID (Azure AD), Key Vault |
| Compute & Networking | [compute.md](ref/compute.md) | VMs, VNets, NSGs, DNS, load balancers, monitoring |
| Serverless & Containers | [serverless.md](ref/serverless.md) | App Service, Functions, Container Apps, AKS, Container Registry |
| Storage | [storage.md](ref/storage.md) | Storage accounts, blobs, file shares, queues, tables |
| Data | [data.md](ref/data.md) | SQL Database, Cosmos DB, Service Bus, Event Hubs |
| Automation & CI/CD | [automation.md](ref/automation.md) | Scripting, output formats, JMESPath, Bicep/ARM, GitHub Actions |

**Read the per-service file for full command reference.**

## Pre-Flight Checks

Before working with any Azure service:

```bash
# 1. Logged in?
az account show -o json

# 2. Correct subscription?
az account show --query '{Name:name, Id:id, State:state}' -o json

# 3. Change subscription if needed
az account set --subscription "<name-or-id>"

# 4. Default location set?
az config get defaults.location 2>/dev/null

# 5. Set default location (optional)
az config set defaults.location=westeurope

# 6. Resource provider registered? (most are auto-registered)
az provider show --namespace Microsoft.ContainerApp --query "registrationState" -o tsv
az provider register --namespace Microsoft.ContainerApp --wait
```

## Troubleshooting

| Problem | Diagnosis | Fix |
|---------|-----------|-----|
| Auth failure | `az account show` | `az login` or check service principal |
| Permission denied | Check RBAC (see [iam.md](iam.md)) | Grant correct role |
| Provider not registered | Error says which provider | `az provider register --namespace Microsoft.X` |
| Quota exceeded | Error message | Request increase in Portal or `az quota` |
| Wrong subscription | `az account show` | `az account set --subscription X` |
| Wrong region | Check resource's `location` | Recreate in correct region |
| Extension missing | `az extension list` | `az extension add --name NAME` |
| Slow commands | Large result set | Use `--query`, `--top`, or `--output tsv` |

```bash
# Debug mode
az vm list --debug 2>&1 | head -50

# Full environment info
az version
az account show -o json
```

## Quick Reference

| Task | Command |
|------|---------|
| Login | `az login` |
| Set subscription | `az account set --subscription "NAME_OR_ID"` |
| Current subscription | `az account show -o json` |
| List subscriptions | `az account list -o table` |
| Register provider | `az provider register --namespace Microsoft.X` |
| List anything | `az RESOURCE list -o json` |
| Show anything | `az RESOURCE show --name NAME -g RG -o json` |
| JSON output | `-o json` |
| TSV (single values) | `-o tsv` |
| JMESPath query | `--query "expression"` |
| Suppress prompts ⚠️ | `--yes` — suppresses ALL confirmations |
| Help | `az RESOURCE --help` or `az find "search term"` |
| Upgrade CLI | `az upgrade` |
