---
name: pulumi-esc
description: Guidance for working with Pulumi ESC (Environments, Secrets, and Configuration). Use when users ask about managing secrets, configuration, environments, short-term credentials, configuring OIDC for AWS, Azure, GCP, integrating with secret stores (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault, 1Password), or using ESC with Pulumi stacks.
---

# Pulumi ESC (Environments, Secrets, and Configuration)

Pulumi ESC is a centralized service for managing environments, secrets, and configuration across cloud infrastructure and applications.

## What is ESC?

ESC enables teams to:

- **Centralize secrets and configuration** in one secure location
- **Compose environments** by importing and layering configuration
- **Generate dynamic credentials** via OIDC for AWS, Azure, GCP
- **Integrate external secret stores** (AWS Secrets Manager, Azure Key Vault, Vault, 1Password)
- **Version and audit** all configuration changes
- **Control access** with fine-grained RBAC

## Essential CLI Commands

```bash
# Create a new environment
pulumi env init <org>/<project-name>/<environment-name>

# Edit environment (opens in editor)
pulumi env edit <org>/<project-name>/<environment-name>

# Set values
pulumi env set <org>/<project-name>/<environment-name> <key> <value>
pulumi env set <org>/<project-name>/<environment-name> <key> <value> --secret

# View definition (secrets hidden)
pulumi env get <org>/<project-name>/<environment-name>

# Open and resolve (reveals secrets)
pulumi env open <org>/<project-name>/<environment-name>

# Run command with environment
pulumi env run <org>/<project-name>/<environment-name> -- <command>

# Link to Pulumi stack
pulumi config env add <project-name>/<environment-name>
```

## Key Concepts

### Command Distinctions

- **`pulumi env get`**: Shows static definition, secrets appear as `[secret]`
- **`pulumi env open`**: Resolves and reveals all values including secrets and dynamic credentials
- **`pulumi env run`**: Executes commands with environment variables loaded
- **`pulumi config env add`**: Only takes the <project-name>/<environment-name> portion

### Environment Structure

Environments are YAML documents with reserved top-level keys:

- **`imports`**: Import and compose other environments
- **`values`**: Define configuration and secrets

Reserved sub-keys under `values`:

- **`environmentVariables`**: Map values to shell environment variables
- **`pulumiConfig`**: Configure Pulumi stack settings
- **`files`**: Generate files with environment data

### Basic Example

```yaml
imports:
  - common/base-config

values:
  environment: production
  region: us-west-2

  dbPassword:
    fn::secret: super-secure-password

  environmentVariables:
    AWS_REGION: ${region}
    DB_PASSWORD: ${dbPassword}

  pulumiConfig:
    aws:region: ${region}
    app:dbPassword: ${dbPassword}
```

## Working with the User

### For Simple Questions

If the user asks basic questions like "How do I create an environment?" or "What's the difference between get and open?", answer directly using the information above.

### For Detailed Documentation

When users need more information, use the web-fetch tool to get content from the official Pulumi ESC documentation:

- **Complete YAML syntax and functions** → https://www.pulumi.com/docs/esc/environments/syntax/
- **Provider integrations** (AWS, Azure, GCP, Vault, 1Password):
  - AWS: https://www.pulumi.com/docs/esc/integrations/dynamic-login-credentials/aws-login/
  - Azure: https://www.pulumi.com/docs/esc/integrations/dynamic-login-credentials/azure-login/
  - GCP: https://www.pulumi.com/docs/esc/integrations/dynamic-login-credentials/gcp-login/
  - Short-term credential (OIDC) providers: https://www.pulumi.com/docs/esc/integrations/dynamic-login-credentials/
  - Dynamic secret providers: https://www.pulumi.com/docs/esc/integrations/dynamic-secrets/
- **Getting started guide** → https://www.pulumi.com/docs/esc/get-started/
- **CLI reference** → https://www.pulumi.com/docs/esc/cli/commands/
  - Prefer using the `pulumi env` subcommands over `esc` CLI.

Use the web-fetch tool with specific prompts to extract relevant information from these docs.

### For Complex Tasks

When helping users:

1. **Understand the goal**: Are they setting up new environments, migrating from stack config, or debugging?
2. **Check existing setup**: Use `pulumi env` commands to list environments or read definitions
3. **Fetch relevant documentation**: Use the web-fetch to get specific examples or syntax from the official docs
4. **Provide step-by-step guidance**: Walk through the process with specific commands
5. **Validate**: Help them test with `pulumi env get` or `pulumi preview`
  a. Only use `pulumi env open` when the full resolved values are needed, but use cautiously as it reveals secrets.

### Example: Helping with AWS OIDC Setup

```text
User: "How do I set up AWS OIDC credentials in ESC?"

1. Use the web-fetch tool to get AWS OIDC documentation from "https://www.pulumi.com/docs/esc/integrations/dynamic-login-credentials/aws-login/"
2. Provide the user with the configuration
3. Ask the user if they have a pre-defined role or need one created for them
4. Set up as much of the environment as possible, then guide them through any steps that you can't do for them
5. Help them test with `pulumi env get` or `pulumi env open` if necessary
```

## Common Workflows

### Creating an Environment

```bash
pulumi env init my-org/my-project/dev-config
# Edit environment (accepts new definition from a file, better for agents, more difficult for users)
pulumi env edit --file /tmp/example.yml my-org/my-project/dev-config
```

### Linking to Stack

```bash
pulumi config env add my-project/dev-config
pulumi config  # Verify environment values are accessible
```

### API Access (Rare)

**Always prefer CLI commands.** Only use the API when absolutely necessary (e.g., bulk operations, automation).

Available API endpoints include:

- `GET /api/esc/environments/{orgName}` - List environments
- `GET /api/esc/environments/{orgName}/{projectName}/{envName}` - Read environment definition
- `GET /api/esc/providers?orgName={orgName}` - List available providers

Use `call_pulumi_cloud_api()` tool to make requests when needed.

## Best Practices

1. Always use `fn::secret` for sensitive values
2. Prefer OIDC over static keys
3. Use descriptive names like `<org>/my-app/production-aws` not `<org>/app/prod`
4. Layer environments: base → cloud-provider → stack-specific
5. Verify that `pulumi config` shows expected values after linking an environment to a stack
6. Prefer using `pulumi env run` for commands needing environment variables
7. Only use `pulumi env open` when absolutely necessary, as it reveals secrets

## Quick Troubleshooting

- **"Environment not found"**: Check permissions with `pulumi env ls -o <org>`
- **"Secret decryption failed"**: Use `pulumi env open` not `pulumi env get`
- **"Stack can't read values"**: Verify `pulumi config env ls` to ensure the stack is listed.
  - Ensure the environment is referenced only by the project-name/environment-name format.
  - Get the specific environment definition with `pulumi env get <org>/<project-name>/<environment-name>`.
  - Verify the `pulumiConfig` key exists and is nested under the `values` key.
