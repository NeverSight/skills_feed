---
name: pulumi-cli
description: Pulumi CLI command reference for infrastructure deployments. Use when the user asks about "pulumi commands", "deploy with pulumi", "pulumi up", "pulumi preview", "manage pulumi stacks", "pulumi state management", "export/import pulumi state", or needs help with Pulumi CLI operations and workflows.
version: 1.2.0
---

# Pulumi CLI Skill

## Quick Command Reference

### Deployment Workflow

```bash
# 1. Create new project
pulumi new typescript                    # Interactive
pulumi new aws-typescript --name myapp --stack dev --yes  # Non-interactive

# 2. Preview changes
pulumi preview                           # Interactive preview
pulumi preview --diff                    # Show detailed diff

# 3. Deploy
pulumi up                                # Interactive deployment
pulumi up --yes                          # Non-interactive
pulumi up --skip-preview --yes           # Skip preview step

# 4. View outputs
pulumi stack output
pulumi stack output --json

# 5. Tear down
pulumi destroy --yes
```

### Stack Management

```bash
# List stacks
pulumi stack ls

# Create and select stacks
pulumi stack init dev
pulumi stack select prod

# View stack info
pulumi stack
pulumi stack history

# Stack outputs
pulumi stack output
pulumi stack output bucketName --show-secrets

# Remove stack
pulumi stack rm dev --yes
```

### State Operations

```bash
# Refresh state from cloud
pulumi refresh --yes

# Export/import state
pulumi stack export --file backup.json
pulumi stack import --file backup.json

# Delete resource from state (keeps cloud resource)
pulumi state delete 'urn:pulumi:dev::myproject::aws:s3/bucket:Bucket::my-bucket'

# Move resource between stacks
pulumi state move --source dev --dest prod 'urn:...'

# Protect critical resources
pulumi state protect 'urn:...'
```

### Configuration

```bash
# Set config values
pulumi config set aws:region us-west-2
pulumi config set dbPassword secret --secret

# Get config
pulumi config get aws:region
pulumi config                            # List all

# Link ESC environment (see language-specific skills for ESC details)
pulumi config env add myorg/myproject-dev
```

## Common Flags

| Flag | Description |
|------|-------------|
| `--yes` / `-y` | Skip confirmation prompts |
| `--stack` / `-s` | Specify stack name |
| `--parallel` / `-p` | Limit concurrent operations |
| `--target` | Target specific resource URNs |
| `--refresh` | Refresh state before operation |
| `--diff` | Show detailed diff |
| `--json` | Output in JSON format |
| `--skip-preview` | Skip preview step |
| `--suppress-outputs` | Hide stack outputs |

## CI/CD Quick Setup

```bash
# Required environment variables
export PULUMI_ACCESS_TOKEN=pul-xxx
export PULUMI_CI=true
export PULUMI_SKIP_UPDATE_CHECK=true

# Typical CI workflow
pulumi login
pulumi stack select prod
pulumi preview
pulumi up --yes
```

## Importing Existing Resources

```bash
# Import single resource
pulumi import aws:s3/bucket:Bucket my-bucket existing-bucket-name

# Bulk import from file
pulumi import --file resources.json
```

**resources.json format:**
```json
{
  "resources": [
    {"type": "aws:s3/bucket:Bucket", "name": "my-bucket", "id": "existing-bucket-name"}
  ]
}
```

## State Recovery Patterns

### Resource deleted outside Pulumi
```bash
pulumi refresh --yes
# Or manually remove from state:
pulumi state delete 'urn:pulumi:dev::myproject::aws:s3/bucket:Bucket::deleted-bucket'
```

### Stuck pending operations
```bash
pulumi refresh --clear-pending-creates --yes
# Or:
pulumi cancel --yes
pulumi state repair
```

### State corruption
```bash
# Backup current state
pulumi stack export --file current.json

# Try repair
pulumi state repair

# Or restore from history
pulumi stack export --version <previous-version> --file good.json
pulumi stack import --file good.json
```

## URN Format

```
urn:pulumi:<stack>::<project>::<type>::<name>

Example:
urn:pulumi:dev::myproject::aws:s3/bucket:Bucket::my-bucket
```

## Backend Options

```bash
# Pulumi Cloud (default)
pulumi login

# Self-hosted backends
pulumi login s3://my-bucket
pulumi login azblob://my-container
pulumi login gs://my-bucket
pulumi login file://~/.pulumi-state
```

## References

- [references/pulumi-cli-commands.md](references/pulumi-cli-commands.md) - Complete command documentation
- [references/pulumi-state-management.md](references/pulumi-state-management.md) - State operations and recovery
- [references/pulumi-environment-variables.md](references/pulumi-environment-variables.md) - CI/CD environment variables
