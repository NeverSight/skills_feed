---
name: localstack-extensions
description: Manage LocalStack Extensions. Use when users want to install, uninstall, list, or configure LocalStack extensions, or develop custom extensions to extend LocalStack functionality.
---

# LocalStack Extensions

Manage LocalStack Extensions to add custom functionality, integrate third-party tools, and extend LocalStack capabilities.

## Capabilities

- Install and manage LocalStack Extensions
- Discover available extensions
- Configure extension settings
- Develop custom extensions

## Extension Management

### List Installed Extensions

```bash
localstack extensions list
```

### Install Extensions

```bash
# Install from PyPI
localstack extensions install localstack-extension-name

# Install specific version
localstack extensions install localstack-extension-name==1.0.0

# Install from Git repository
localstack extensions install "git+https://github.com/org/extension-repo.git"
```

### Uninstall Extensions

```bash
localstack extensions uninstall localstack-extension-name
```

### Enable/Disable Extensions

```bash
# Extensions are enabled by default after installation
# Disable via environment variable
EXTENSION_NAME_ENABLED=0 localstack start -d
```

## Available Extensions

### Community Extensions

Check the [LocalStack Extensions Registry](https://docs.localstack.cloud/user-guide/extensions/) for community-contributed extensions.

## Using Extensions

### MailHog Extension

```bash
# Install
localstack extensions install localstack-extension-mailhog

# Start LocalStack
localstack start -d

# Access MailHog UI
open http://localhost:8025

# SES emails will be captured by MailHog
awslocal ses send-email \
  --from sender@example.com \
  --to recipient@example.com \
  --subject "Test" \
  --text "Hello"
```

## Developing Custom Extensions

### Extension Structure

```
my-extension/
├── setup.py
├── my_extension/
│   ├── __init__.py
│   └── extension.py
```

### Basic Extension

```python
# extension.py
from localstack.extensions.api import Extension, http

class MyExtension(Extension):
    name = "my-extension"

    def on_extension_load(self):
        print("Extension loaded!")

    def on_platform_start(self):
        print("LocalStack is starting!")

    @http.route("/my-endpoint")
    def my_endpoint(self, request):
        return {"message": "Hello from extension!"}
```

### Install Local Extension

```bash
# Install in development mode
localstack extensions install -e ./my-extension
```

## Configuration

Extensions can be configured via environment variables:

```bash
# General pattern
EXTENSION_<NAME>_<SETTING>=value localstack start -d

# Example
EXTENSION_MAILHOG_PORT=8025 localstack start -d
```

## Troubleshooting

- **Extension not loading**: Check `localstack logs` for errors
- **Conflicts**: Disable conflicting extensions
- **Version issues**: Ensure extension is compatible with your LocalStack version
