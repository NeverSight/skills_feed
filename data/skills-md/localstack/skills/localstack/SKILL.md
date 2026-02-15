---
name: localstack
description: Manage LocalStack container lifecycle. Use when users need to start, stop, restart, or check status of LocalStack, configure LocalStack environment variables, or troubleshoot LocalStack container issues.
---

# LocalStack Lifecycle Management

Manage the LocalStack container lifecycle including starting, stopping, and monitoring the local cloud environment.

## Capabilities

- Start LocalStack with custom configuration
- Stop running LocalStack instances
- Check LocalStack status and health
- Restart LocalStack with new settings
- View LocalStack version and configuration

## Common Commands

### Start LocalStack

```bash
# Basic start
localstack start -d

# Start with debug mode
DEBUG=1 localstack start -d

# Start with Pro features (requires auth token)
LOCALSTACK_AUTH_TOKEN=<token> localstack start -d
```

### Check Status

```bash
# Check if LocalStack is running
localstack status

# Check service health
curl http://localhost:4566/_localstack/health

# View running Docker container
docker ps | grep localstack
```

### Stop LocalStack

```bash
# Graceful stop
localstack stop

# Force stop via Docker
docker stop localstack-main
```

### View Logs

```bash
# Follow logs
localstack logs -f

# View last 100 lines
localstack logs --tail 100
```

## Configuration Options

Key environment variables for LocalStack:

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug logging | `0` |
| `PERSISTENCE` | Enable persistence across restarts | `0` |
| `LOCALSTACK_AUTH_TOKEN` | Auth token for Pro features | None |
| `GATEWAY_LISTEN` | Port configuration | `4566` |

## Troubleshooting

- **Container won't start**: Check if port 4566 is already in use
- **Services unavailable**: Verify Docker is running and has sufficient resources
- **Auth errors**: Ensure `LOCALSTACK_AUTH_TOKEN` is set for Pro features
