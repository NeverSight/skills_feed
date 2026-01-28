---
name: tfccli
description: |
  Use tfccli CLI for Terraform Cloud API operations: workspaces, runs, plans, applies, organizations, projects, configuration versions, variables and any other queries or commands you want to execute against Terraform Cloud. Trigger when user mentions Terraform Cloud, TFC, HCP Terraform, or needs to manage Terraform Cloud resources programmatically.
---

# tfccli

CLI for Terraform Cloud / HCP Terraform. Binary: `tfccli`.

## Setup

```bash
tfccli init                     # Initialize ~/.tfccli/settings.json
tfccli doctor                   # Validate settings, token, connectivity
```

Token discovery (checked in order):
1. **Environment variable**: `TF_TOKEN_<sanitized_hostname>` (e.g., `TF_TOKEN_app_terraform_io`)
2. **CLI config file**: `TF_CLI_CONFIG_FILE` env var, or `~/.terraformrc` (Unix) / `%APPDATA%\terraform.rc` (Windows)
3. **Credentials file**: `~/.terraform.d/credentials.tfrc.json` (created by `terraform login`)

## Discovering Commands

```bash
tfccli --help                   # List all commands and global flags
tfccli <command> --help         # Show subcommands (e.g., tfccli workspaces --help)
tfccli <command> <subcommand> --help  # Show flags for a subcommand
```

Use `--help` to discover available options when unsure about syntax.

## Global Flags

| Flag              | Purpose                                      |
|-------------------|----------------------------------------------|
| `--context NAME`  | Select named context                         |
| `--address URL`   | Override API address                         |
| `--org NAME`      | Override default organization                |
| `--output-format` | `table` (default) or `json`                  |
| `--debug`         | Enable debug logging                         |
| `--force`         | Skip confirmation prompts                    |

## Commands

### Organizations
```bash
tfccli organizations list
tfccli organizations get --id org-xxxxx
tfccli organizations create --name myorg --email admin@example.com
tfccli organizations update --id org-xxxxx --name newname
tfccli organizations delete --id org-xxxxx
```

### Projects
```bash
tfccli projects list
tfccli projects get --id prj-xxxxx
tfccli projects create --name myproject
tfccli projects update --id prj-xxxxx --name newname
tfccli projects delete --id prj-xxxxx
```

### Workspaces
```bash
tfccli workspaces list [--project prj-xxxxx] [--search name] [--tags tag1,tag2]
tfccli workspaces get --id ws-xxxxx
tfccli workspaces create --name myworkspace [--project prj-xxxxx] [--execution-mode remote|local|agent]
tfccli workspaces update --id ws-xxxxx [--name newname] [--description "desc"]
tfccli workspaces delete --id ws-xxxxx
```

### Workspace Variables
```bash
tfccli workspace-variables list --workspace-id ws-xxxxx
tfccli workspace-variables get --id var-xxxxx
tfccli workspace-variables create --workspace-id ws-xxxxx --key KEY --value VALUE [--category terraform|env] [--sensitive]
tfccli workspace-variables update --id var-xxxxx [--value newvalue]
tfccli workspace-variables delete --id var-xxxxx
```

### Workspace Resources
```bash
tfccli workspace-resources list --workspace-id ws-xxxxx
```

### Runs
```bash
tfccli runs list --workspace-id ws-xxxxx [--limit N]
tfccli runs get --id run-xxxxx
tfccli runs create --workspace-id ws-xxxxx [--message "reason"]
tfccli runs apply --id run-xxxxx [--comment "approved"]
tfccli runs discard --id run-xxxxx [--comment "not needed"]
tfccli runs cancel --id run-xxxxx [--comment "stopping"]
tfccli runs force-cancel --id run-xxxxx [--comment "emergency stop"]
```

### Plans
```bash
tfccli plans get --id plan-xxxxx
tfccli plans json-output --id plan-xxxxx       # Download JSON execution plan
tfccli plans sanitized-json --id plan-xxxxx    # Download sanitized plan
```

### Applies
```bash
tfccli applies get --id apply-xxxxx
tfccli applies errored-state --id apply-xxxxx  # Download errored state file
```

### Configuration Versions
```bash
tfccli configuration-versions list --workspace-id ws-xxxxx
tfccli configuration-versions get --id cv-xxxxx
tfccli configuration-versions create --workspace-id ws-xxxxx [--speculative]
tfccli configuration-versions upload --id cv-xxxxx --path ./terraform-dir
tfccli configuration-versions download --id cv-xxxxx --output ./download-dir
tfccli configuration-versions archive --id cv-xxxxx
```

### Users
```bash
tfccli users me                                # Current user info
tfccli users get --id user-xxxxx
```

### Invoices (HCP Terraform only)
```bash
tfccli invoices list
tfccli invoices next                           # Preview next invoice
```

### Contexts
```bash
tfccli contexts list
tfccli contexts add --name prod --address app.terraform.io --org myorg
tfccli contexts use --name prod
tfccli contexts show
tfccli contexts remove --name oldcontext
```

## Exit Codes

- `0` – Success
- `1` – Usage/parse error
- `2` – Runtime error (API failure, auth issue)
- `3` – Unexpected/internal error

## Common Workflows

**Trigger a run and approve:**
```bash
tfccli runs create --workspace-id ws-xxxxx --message "Deploy v1.2.3"
# Wait for plan to complete, then:
tfccli runs apply --id run-xxxxx --comment "Approved by automation"
```

**Export workspace variables for backup:**
```bash
tfccli workspace-variables list --workspace-id ws-xxxxx --output-format json > vars.json
```

**Check run status:**
```bash
tfccli runs get --id run-xxxxx --output-format json | jq '.status'
```
