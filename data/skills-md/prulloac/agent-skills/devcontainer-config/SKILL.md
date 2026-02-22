---
name: devcontainer-config
description: Comprehensive guide for creating, editing, and validating devcontainer.json configuration files. Use when working with Development Container configurations for any scenario including creating new devcontainer.json files, modifying existing configurations, troubleshooting dev container issues, adding features or lifecycle scripts, configuring ports and environment variables, setting up multi-container environments with Docker Compose, or understanding devcontainer properties and their usage.
---

# Dev Container Configuration

## Overview

This skill provides comprehensive guidance for working with `devcontainer.json` files - the configuration files that define Development Containers. It covers all configuration scenarios (image-based, Dockerfile-based, and Docker Compose), property usage, common patterns, and validation.

## Quick Start

### Determine Configuration Type

Choose the appropriate base configuration:

**1. Image-based** - Use an existing container image:
- Best for: Standard development environments, quick setup
- Template: `assets/basic-image.json`
- Required property: `image`

**2. Dockerfile-based** - Build from a custom Dockerfile:
- Best for: Custom environments, specific tool versions
- Template: `assets/dockerfile-based.json`
- Required property: `build.dockerfile`

**3. Docker Compose** - Multi-container environments:
- Best for: Apps with databases, microservices
- Template: `assets/docker-compose.json`
- Required properties: `dockerComposeFile`, `service`

### Basic Workflow

1. **Start with template**: Copy the appropriate template from `assets/`
2. **Configure basics**: Set `name`, add `features`, configure `customizations`
3. **Add lifecycle scripts**: Set `postCreateCommand`, `postStartCommand`, etc.
4. **Configure ports**: Add `forwardPorts` and `portsAttributes` as needed
5. **Validate**: Run `scripts/validate.py` to check for issues

## Common Configuration Tasks

### Adding Dev Container Features

Features extend container functionality. Add them using the `features` property:

```json
{
  "features": {
    "ghcr.io/devcontainers/features/node:1": {
      "version": "20"
    },
    "ghcr.io/devcontainers/features/github-cli:1": {},
    "ghcr.io/devcontainers/features/docker-in-docker:2": {}
  }
}
```

Browse available features at: https://containers.dev/features

### Configuring Environment Variables

Use `containerEnv` for static, container-wide variables:

```json
{
  "containerEnv": {
    "NODE_ENV": "development",
    "API_URL": "http://localhost:3000"
  }
}
```

Use `remoteEnv` for client-specific variables that may change:

```json
{
  "remoteEnv": {
    "LOCAL_USER": "${localEnv:USER}"
  }
}
```

### Setting Up Lifecycle Scripts

Configure commands that run at different stages:

```json
{
  "onCreateCommand": "npm ci",
  "updateContentCommand": "npm install",
  "postCreateCommand": "npm run build",
  "postStartCommand": "npm run dev"
}
```

**Command formats:**
- String: Runs in shell, supports `&&` and pipes
- Array: Direct execution without shell
- Object: Parallel execution of multiple commands

### Port Forwarding

Forward ports with custom behavior:

```json
{
  "forwardPorts": [3000, 5432],
  "portsAttributes": {
    "3000": {
      "label": "Application",
      "onAutoForward": "openBrowser"
    },
    "5432": {
      "label": "Database",
      "onAutoForward": "silent"
    }
  }
}
```

### VS Code Extensions

Add extensions via customizations:

```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode"
      ]
    }
  }
}
```

## Advanced Configuration

### Security and Debugging

For debugging languages like C++, Go, Rust:

```json
{
  "capAdd": ["SYS_PTRACE"],
  "securityOpt": ["seccomp=unconfined"]
}
```

For Docker-in-Docker:

```json
{
  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {}
  },
  "privileged": true
}
```

### Custom Mounts

Mount additional directories or volumes:

```json
{
  "mounts": [
    {
      "source": "${localEnv:HOME}/.ssh",
      "target": "/home/vscode/.ssh",
      "type": "bind"
    },
    {
      "source": "project-cache",
      "target": "/workspace/.cache",
      "type": "volume"
    }
  ]
}
```

### User Configuration

Control which user runs commands:

```json
{
  "containerUser": "vscode",
  "remoteUser": "vscode",
  "updateRemoteUserUID": true
}
```

- `containerUser`: User for all container operations
- `remoteUser`: User for dev tools/terminals
- `updateRemoteUserUID`: Match local user UID/GID on Linux

## Validation

Use the validation script to check configurations:

```bash
python scripts/validate.py /path/to/devcontainer.json
```

The validator checks for:
- Required properties based on scenario
- Proper lifecycle script formats
- Valid port configurations
- Correct variable syntax
- Common configuration issues

Example output:
```
============================================================
Validation Results for: devcontainer.json
============================================================

❌ ERRORS:
  - Must specify one of: 'image', 'build.dockerfile', or 'dockerComposeFile'

⚠️  WARNINGS:
  - Missing 'name' property - recommended for UI display

❌ Validation failed with 1 error(s)
```

## Reference Documentation

For detailed property information:
- **references/properties.md**: Complete reference of all devcontainer.json properties
- **references/patterns.md**: Real-world examples and common patterns

Use these references when:
- Looking up specific property syntax
- Understanding property interactions
- Finding examples for specific scenarios
- Learning about advanced features

## Variables

Available variables for use in string values:

- `${localEnv:VAR_NAME}` - Environment variable from host machine
- `${containerEnv:VAR_NAME}` - Environment variable from container
- `${localWorkspaceFolder}` - Local path to workspace
- `${containerWorkspaceFolder}` - Container path to workspace
- `${localWorkspaceFolderBasename}` - Workspace folder name
- `${devcontainerId}` - Unique container identifier

Default values: `${localEnv:VAR:default_value}`

## Troubleshooting

### Container won't start
- Check that required properties are present (`image`, `build.dockerfile`, or `dockerComposeFile`)
- Validate JSON syntax
- Check that referenced files (Dockerfile, docker-compose.yml) exist

### Permission issues
- Set `updateRemoteUserUID: true` on Linux
- Configure `containerUser` and `remoteUser` appropriately

### Ports not forwarding
- Ensure application listens on `0.0.0.0` not just `localhost`
- Check `forwardPorts` configuration
- Review `portsAttributes` settings

### Features not installing
- Verify feature IDs are correct
- Check network connectivity
- Use `overrideFeatureInstallOrder` if dependencies exist

### Lifecycle scripts failing
- Check script syntax (string vs array vs object)
- Review script output in dev container log
- Ensure required tools are available in container
- Remember: If a script fails, subsequent scripts won't run
