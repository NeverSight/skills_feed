---
name: podman
description: Manages containers, builds images, configures pods and networks with Podman. Use when running containers, creating Containerfiles, grouping services in pods, or managing container resources.
---

# Podman

Rootless container management compatible with Docker commands.

## Container Management

### Basic Lifecycle

```bash
# Run a container (detached)
podman run -d --name my-app alpine sleep 1000

# List running containers
podman ps

# List all containers (including stopped ones)
podman ps -a

# Stop and remove a container
podman stop my-app
podman rm my-app

# Inspect container details
podman inspect my-app
```

### Logs and Execution

```bash
# View container logs (non-interactive)
podman logs my-app

# Execute a command in a running container
podman exec my-app ls /app
```

## Image Management

```bash
# Pull an image
podman pull alpine:latest

# List local images
podman images

# Build an image from a Containerfile (or Dockerfile)
podman build -t my-custom-image .

# Remove an image
podman rmi my-custom-image
```

## Pods (Unique to Podman)

Pods allow grouping multiple containers together so they share the same network namespace (localhost).

```bash
# Create a pod
podman pod create --name my-stack -p 8080:80

# Run a container inside a pod
podman run -d --pod my-stack --name nginx nginx

# List pods
podman pod ps
```

## Maintenance and Cleanup

```bash
# Remove all stopped containers, unused networks, and dangling images
podman system prune -f

# Show disk usage by containers/images
podman system df
```

## Headless / Non-Interactive Tips

- **Force Flag**: Use `-f` or `--force` with `rm`, `rmi`, and `prune` to avoid confirmation prompts.
- **Detached Mode**: Always use `-d` for long-running services to prevent the command from hanging. For interactive sessions, use: `tmux new -d 'podman run -it --name my-app alpine sh'`
- **Rootless**: Podman runs in rootless mode by default for the current user. Ensure subuid/subgid are configured if running complex workloads.
- **Docker Compatibility**: Most `docker` commands can be prefixed with `podman` instead.

## Networking

```bash
# Create a network
podman network create my-network

# Run container on a network
podman run --network my-network --name web nginx

# Connect existing container to network
podman network connect my-network web

# List networks
podman network ls

# Inspect network
podman network inspect my-network
```

## Secrets Management

```bash
# Create a secret
echo "my-secret-value" | podman secret create my-secret -

# List secrets
podman secret ls

# Use secret in container
podman run --secret my-secret,type=env,target=MY_SECRET alpine env
```

## Health Checks

```bash
# Run container with health check
podman run -d --health-cmd "curl -f http://localhost/ || exit 1" \
  --health-interval 30s --health-retries 3 \
  --name web nginx

# Check health status
podman inspect web | grep -A 10 "Health"
```

## Auto Updates

```bash
# Run container with auto-update policy
podman run -d --label "io.containers.autoupdate=registry" \
  --name web nginx

# Check for updates
podman auto-update

# Apply updates
podman auto-update --dry-run=false
```

## Systemd Integration (Quadlet)

Podman can generate systemd service files for containers:

```bash
# Create a .container file
cat > ~/.config/containers/systemd/my-app.container << EOF
[Container]
Image=nginx:latest
PublishPort=8080:80
EOF

# Generate systemd service
podman generate systemd --new --files --name my-app

# Enable and start
systemctl --user enable --now container-my-app.service
```

## Docker Compose Compatibility

```bash
# Native podman compose support
podman compose up -d
podman compose down
podman compose logs

# Or use podman-compose (third-party tool)
pip install podman-compose
podman-compose up -d
```

## Kubernetes Integration

```bash
# Generate Kubernetes YAML from container/pod
podman generate kube my-pod > pod.yaml

# Play Kubernetes YAML
podman kube play pod.yaml

# Stop and remove Kubernetes resources
podman kube down pod.yaml
```

## Remote Builds (Farm)

```bash
# Farm out builds to remote machines
podman farm build -t myimage .

# List configured farms
podman farm list
```

## Artifact Management

```bash
# Push OCI artifacts
podman artifact push myartifact.tar oci://registry.example.com/artifact

# Pull OCI artifacts
podman artifact pull oci://registry.example.com/artifact
```

## Related Skills

- **tmux**: Run containers in background sessions
- **nix**: Alternative reproducible environments
