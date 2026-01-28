---
name: spice-secrets
description: Configure secret stores in Spice (environment variables, Kubernetes, AWS Secrets Manager, keyring). Use when asked to "configure secrets", "add API keys", "set up credentials", or "manage passwords".
---

# Spice Secret Stores

Secret stores securely manage sensitive data like API keys, passwords, and tokens.

## Basic Configuration

```yaml
secrets:
  - from: <store_type>
    name: <store_name>
```

## Supported Secret Stores

| Store                  | From Format                | Description                      |
|------------------------|----------------------------|----------------------------------|
| `env`                  | `env`                      | Environment variables (default)  |
| `kubernetes`           | `kubernetes:<secret_name>` | Kubernetes secrets               |
| `aws_secrets_manager`  | `aws_secrets_manager`      | AWS Secrets Manager              |
| `keyring`              | `keyring`                  | OS keyring (macOS/Linux/Windows) |

## Default: Environment Variables

The `env` store is loaded automatically. It reads from environment variables and `.env` / `.env.local` files.

```yaml
secrets:
  - from: env
    name: env
```

## Using Secrets

Reference secrets in component parameters with `${ store_name:KEY }`:

```yaml
datasets:
  - from: postgres:my_table
    name: my_table
    params:
      pg_user: ${ env:PG_USER }
      pg_pass: ${ env:PG_PASSWORD }

models:
  - from: openai:gpt-4o
    name: gpt4
    params:
      openai_api_key: ${ secrets:OPENAI_API_KEY }
```

## Multiple Secret Stores

Configure multiple stores with precedence (last defined wins):

```yaml
secrets:
  - from: env
    name: env
  - from: keyring
    name: keyring
```

Use `${ secrets:KEY }` to search all stores in precedence order:
```yaml
params:
  api_key: ${ secrets:API_KEY }  # checks keyring first, then env
```

## Examples

### Kubernetes Secrets
```yaml
secrets:
  - from: kubernetes:my-app-secrets
    name: k8s
```

### AWS Secrets Manager
```yaml
secrets:
  - from: aws_secrets_manager
    name: aws
    params:
      aws_region: us-east-1
```

### Within Connection Strings
```yaml
params:
  mysql_connection_string: mysql://${env:USER}:${env:PASSWORD}@localhost:3306/db
```

## Documentation

- [Secret Stores Overview](https://spiceai.org/docs/components/secret-stores)
