---
name: localstack-state
description: Manage LocalStack state and snapshots. Use when users want to save, load, export, or import LocalStack state, work with Cloud Pods, create local snapshots, or enable persistence across restarts.
---

# State Management

Save, load, and manage LocalStack state for reproducible development environments and state snapshots.

## Capabilities

- Export and import state locally to files
- Save and load state to/from Cloud Pods (remote storage)
- Share state across teams via Cloud Pods
- Enable persistent state across container restarts

## Local Snapshots (state export/import)

Local snapshots allow you to export LocalStack state to files and import them back. This works without requiring a Pro subscription.

### Export State

```bash
# Export current state to a local file
localstack state export my-state.zip

# Export to a specific path
localstack state export /path/to/backup/state.zip
```

### Import State

```bash
# Import state from a local file
localstack state import my-state.zip

# Import from a specific path
localstack state import /path/to/backup/state.zip
```

### Use Cases for Local Snapshots

- **Backup/restore**: Save state before destructive operations
- **CI/CD pipelines**: Commit state files to version control for reproducible tests
- **Offline workflows**: Work with state files without cloud connectivity
- **Quick snapshots**: Fast local save/restore during development

## Cloud Pods (pod save/load)

Cloud Pods store state in LocalStack's cloud platform, enabling team collaboration and remote state management.

### Prerequisites

Cloud Pods require a LocalStack Pro subscription and auth token:

```bash
export LOCALSTACK_AUTH_TOKEN=<your-token>
```

### Save to Cloud Pod

```bash
# Save current state to a Cloud Pod
localstack pod save my-pod-name

# Save with a message
localstack pod save my-pod-name --message "Initial setup with S3 and DynamoDB"
```

### Load from Cloud Pod

```bash
# Load state from a Cloud Pod
localstack pod load my-pod-name

# Load and merge with existing state
localstack pod load my-pod-name --merge
```

### List Cloud Pods

```bash
# List all available Cloud Pods
localstack pod list
```

### Delete Cloud Pods

```bash
# Delete a Cloud Pod
localstack pod delete my-pod-name
```

### Inspect Cloud Pods

```bash
# View Cloud Pod details
localstack pod inspect my-pod-name
```

### Use Cases for Cloud Pods

- **Team collaboration**: Share consistent development environments across team members
- **Demo environments**: Prepare and share demo-ready states
- **Cross-machine development**: Access the same state from different machines

## Local Persistence

For automatic persistence across LocalStack restarts (without explicit export/import):

```bash
# Enable local persistence
PERSISTENCE=1 localstack start -d

# State is saved to .localstack/ directory
# Survives container restarts
```

## Comparison

| Feature | Local Snapshots (export/import) | Cloud Pods (save/load) |
|---------|----------------------------|------------------------|
| Storage | Local files | LocalStack cloud |
| Pro required | No | Yes |
| Team sharing | Manual file sharing | Built-in |
| Version control | Can commit files | Cloud-managed |
| Offline use | Yes | No |

## Best Practices

- Use `state export/import` for local development and CI/CD pipelines
- Use Cloud Pods for team collaboration and shared environments
- Use descriptive names that indicate the state contents
- Enable `PERSISTENCE=1` for simple state retention across restarts
