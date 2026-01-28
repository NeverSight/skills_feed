---
name: devcontainer-helper
description: Use this skill when the user asks to create, configure, update, or explain a `devcontainer.json` file or development container environment.
---

# DevContainer Helper

This skill assists in creating and managing `devcontainer.json` files for consistent development environments.

## Workflow

### 1. specific Requirements

Before generating the file, determine the user's needs:
- **Base Environment**: Do they want a pre-built image (e.g., Ubuntu, Python, Node), a custom `Dockerfile`, or a `docker-compose.yml` setup?
- **Languages & Tools**: What languages (Node.js, Python, Go, Rust, etc.) and tools (Git, CLI utilities) are needed?
- **Extensions**: Are there specific VS Code extensions required?
- **Ports**: What ports need to be forwarded?

### 2. Generate Configuration

Use the template in `assets/devcontainer-template.json` as a starting point.

**For Image-based (Simplest):**
Use the `image` property. Add `features` for additional tools.

**For Dockerfile:**
Use `build.dockerfile` property pointing to their Dockerfile.

**For Docker Compose:**
Use `dockerComposeFile` and `service` properties.

### 3. Add Features

Encourage using "Features" over manual `Dockerfile` commands when possible for better maintainability.
Common features:
- Node.js: `ghcr.io/devcontainers/features/node:1`
- Python: `ghcr.io/devcontainers/features/python:1`
- Docker-in-Docker: `ghcr.io/devcontainers/features/docker-in-docker:2`
- Git: `ghcr.io/devcontainers/features/git:1`

### 4. Lifecycle Scripts

If the user needs to run commands (like `npm install` or `pip install`) after the container builds:
- Use `postCreateCommand` for one-time setup.
- Use `postStartCommand` for commands that run every time the container starts.

## References

See [references/cheatsheet.md](references/cheatsheet.md) for a list of common `devcontainer.json` properties and valid values.