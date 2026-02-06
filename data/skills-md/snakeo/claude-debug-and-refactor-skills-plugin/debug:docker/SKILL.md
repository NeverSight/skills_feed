---
name: debug:docker
description: Debug Docker containers, images, and infrastructure with systematic diagnostic techniques. This skill provides comprehensive guidance for troubleshooting container exit codes, OOM kills, image build failures, networking issues, volume mount problems, and permission errors. Covers four-phase debugging methodology from quick assessment to deep analysis, essential Docker commands, debug container techniques for minimal images, and platform-specific troubleshooting for Windows, Mac, and Linux.
---

# Docker Debugging Guide

This guide provides a systematic approach to debugging Docker containers, images, networks, and volumes. Follow the four-phase methodology for efficient problem resolution.

## The Four Phases of Docker Debugging

### Phase 1: Quick Assessment (30 seconds)
Get immediate context about the issue.

```bash
# Check container status
docker ps -a

# View recent logs (last 50 lines)
docker logs --tail 50 <container>

# Check container exit code
docker inspect <container> --format='{{.State.ExitCode}}'

# Quick health check
docker inspect <container> --format='{{.State.Health.Status}}'
```

### Phase 2: Log Analysis (2-5 minutes)
Deep dive into container logs and events.

```bash
# Follow logs in real-time
docker logs -f <container>

# View logs with timestamps
docker logs --timestamps <container>

# View logs since specific time
docker logs --since 30m <container>

# Check Docker daemon events
docker events --since 1h

# View system-wide logs
journalctl -u docker.service --since "1 hour ago"
```

### Phase 3: Interactive Investigation (5-15 minutes)
Get hands-on access to the container environment.

```bash
# Open shell in running container
docker exec -it <container> /bin/sh
# or
docker exec -it <container> /bin/bash

# Run commands without shell
docker exec <container> cat /etc/hosts
docker exec <container> env

# Use docker debug for enhanced debugging (Docker Desktop 4.27+)
docker debug <container>

# Inspect container configuration
docker inspect <container>

# Check network configuration
docker network inspect <network>
```

### Phase 4: Deep Analysis (15+ minutes)
Comprehensive investigation for complex issues.

```bash
# Monitor resource usage
docker stats <container>

# Check disk usage
docker system df -v

# Inspect image layers
docker history <image>

# Export container filesystem for analysis
docker export <container> -o container.tar

# View detailed container info
docker inspect <container> | jq '.'
```

---

## Common Error Patterns and Solutions

### Exit Codes

| Exit Code | Meaning | Common Causes | Solution |
|-----------|---------|---------------|----------|
| **0** | Success | Normal termination | No action needed |
| **1** | General error | Application error, missing file | Check logs, verify files exist |
| **126** | Permission problem | Cannot execute command | Check file permissions, add execute bit |
| **127** | Command not found | Missing binary or PATH issue | Verify command exists in image |
| **137** | SIGKILL (OOM) | Out of memory | Increase memory limit, optimize app |
| **139** | SIGSEGV | Segmentation fault | Debug application code |
| **143** | SIGTERM | Graceful shutdown | Normal behavior during stop |
| **255** | Exit status out of range | Various | Check application error handling |

### OOM Killed Containers (Exit Code 137)

```bash
# Check if container was OOM killed
docker inspect <container> --format='{{.State.OOMKilled}}'

# View memory limits
docker inspect <container> --format='{{.HostConfig.Memory}}'

# Run with increased memory
docker run -m 2g --memory-swap 4g <image>

# Monitor memory in real-time
docker stats --format "table {{.Name}}\t{{.MemUsage}}\t{{.MemPerc}}"
```

### Image Build Failures

```bash
# Build with verbose output
docker build --progress=plain -t <image> .

# Build without cache
docker build --no-cache -t <image> .

# Build specific stage for debugging
docker build --target <stage-name> -t <image> .

# Inspect build cache
docker builder prune --dry-run

# Debug failed layer by running from previous successful layer
docker run -it <last-successful-layer-id> /bin/sh
```

**Common Build Issues:**
- `COPY failed: file not found` - Check paths are relative to build context
- `RUN failed` - Check command syntax, ensure dependencies are installed
- `Permission denied` - Add `chmod` or run as appropriate user

### Networking Issues

```bash
# List networks
docker network ls

# Inspect network
docker network inspect <network>

# Check container network settings
docker inspect <container> --format='{{json .NetworkSettings.Networks}}'

# Test connectivity between containers
docker exec <container1> ping <container2>

# Test DNS resolution
docker exec <container> nslookup <hostname>

# Check exposed ports
docker port <container>

# Debug with network tools
docker run --rm --network=<network> nicolaka/netshoot ping <target>
```

**Common Network Issues:**
- Containers on different networks cannot communicate
- Port already in use: `lsof -i :<port>` to find conflicting process
- DNS resolution fails: Check Docker DNS settings

### Volume Mount Problems

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect <volume>

# Check mount points
docker inspect <container> --format='{{json .Mounts}}'

# Verify host path exists
ls -la /path/to/host/directory

# Check permissions inside container
docker exec <container> ls -la /mount/path

# Test with simple container
docker run --rm -v /host/path:/container/path alpine ls -la /container/path
```

**Common Volume Issues:**
- `Permission denied` - Check UID/GID mapping, use `:z` or `:Z` for SELinux
- Path not found - Ensure host path exists before mounting
- Windows paths - Use forward slashes or escaped backslashes

### Permission Denied Errors

```bash
# Add user to docker group (Linux)
sudo usermod -aG docker $USER
newgrp docker

# Check Docker socket permissions
ls -la /var/run/docker.sock

# Run container as specific user
docker run --user $(id -u):$(id -g) <image>

# Fix file permissions in Dockerfile
RUN chown -R appuser:appuser /app
USER appuser
```

### Container Exits Immediately

```bash
# Check what command is running
docker inspect <container> --format='{{.Config.Cmd}}'
docker inspect <container> --format='{{.Config.Entrypoint}}'

# Keep container running for debugging
docker run -d <image> tail -f /dev/null
# or
docker run -d <image> sleep infinity

# Override entrypoint for debugging
docker run -it --entrypoint /bin/sh <image>

# Check if process is foreground
# (Docker needs a foreground process to keep running)
```

### Docker Desktop Won't Start

**Windows:**
- Enable Hyper-V: `Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All`
- Enable WSL2: `wsl --install`
- Check virtualization in BIOS (VT-x/AMD-V)
- Temporarily disable antivirus

**Mac:**
- Check available disk space
- Reset Docker Desktop: Delete `~/Library/Group\ Containers/group.com.docker/`
- Reinstall Docker Desktop

**Linux:**
- Check Docker daemon: `sudo systemctl status docker`
- View daemon logs: `journalctl -u docker.service`

---

## Debugging Tools Reference

### Essential Commands

```bash
# Container lifecycle
docker ps -a                          # List all containers
docker logs <container>               # View logs
docker logs -f --tail 100 <container> # Follow last 100 lines
docker exec -it <container> sh        # Interactive shell
docker inspect <container>            # Full container details
docker top <container>                # Running processes

# Images
docker images                         # List images
docker history <image>                # Show image layers
docker inspect <image>                # Image details

# System
docker system df                      # Disk usage
docker system events                  # Real-time events
docker system info                    # System-wide info
docker system prune                   # Clean up unused resources

# Network
docker network ls                     # List networks
docker network inspect <network>      # Network details

# Volumes
docker volume ls                      # List volumes
docker volume inspect <volume>        # Volume details
```

### Advanced Debugging

```bash
# Docker debug (Docker Desktop 4.27+)
docker debug <container>              # Enhanced shell with tools

# Process inspection
docker exec <container> ps aux        # List processes
docker exec <container> top           # Interactive process viewer

# Network debugging
docker exec <container> netstat -tlnp # Open ports
docker exec <container> ss -tlnp      # Socket statistics
docker exec <container> curl -v <url> # HTTP debugging

# File system
docker diff <container>               # Changed files
docker cp <container>:/path ./local   # Copy files out
docker cp ./local <container>:/path   # Copy files in

# Resource monitoring
docker stats                          # Live resource usage
docker stats --no-stream              # Single snapshot
```

### Debug Container Image

For minimal images without debugging tools, use a sidecar approach:

```bash
# Use netshoot for network debugging
docker run -it --network container:<target> nicolaka/netshoot

# Use busybox for basic tools
docker run -it --pid container:<target> busybox
```

---

## Quick Reference Commands

```bash
# Most common debugging sequence
docker ps -a                                  # 1. Check status
docker logs --tail 100 -f <container>         # 2. View logs
docker exec -it <container> sh                # 3. Interactive shell
docker inspect <container>                    # 4. Full details

# Performance debugging
docker stats                                  # Resource usage
docker system df                              # Disk usage
docker events                                 # System events

# Network debugging
docker network ls                             # List networks
docker network inspect <network>              # Network details
docker exec <container> ping <host>           # Test connectivity

# Clean up
docker system prune -af                       # Remove all unused data
docker volume prune                           # Remove unused volumes
docker builder prune                          # Remove build cache
```

---

## Troubleshooting Checklist

- [ ] Check container status with `docker ps -a`
- [ ] Review logs with `docker logs <container>`
- [ ] Verify exit code with `docker inspect --format='{{.State.ExitCode}}'`
- [ ] Check for OOM: `docker inspect --format='{{.State.OOMKilled}}'`
- [ ] Verify network connectivity between containers
- [ ] Check volume mounts and permissions
- [ ] Ensure required ports are not in use
- [ ] Verify environment variables are set correctly
- [ ] Check available disk space with `docker system df`
- [ ] Review Docker daemon logs if system-level issue

---

## Sources

- [How to Fix and Debug Docker Containers Like a Superhero - Docker Blog](https://www.docker.com/blog/how-to-fix-and-debug-docker-containers-like-a-superhero/)
- [Docker Debugging: Common Scenarios and 7 Practical Tips - Lumigo](https://lumigo.io/container-monitoring/docker-debugging-common-scenarios-and-7-practical-tips/)
- [docker debug - Docker Docs](https://docs.docker.com/reference/cli/docker/debug/)
- [Docker Logs: Complete Debugging Cheat Sheet - Atmosly](https://atmosly.com/knowledge/docker-logs-the-complete-debugging-cheat-sheet/)
- [100 Common Docker Errors and Solutions - DEV Community](https://dev.to/prodevopsguytech/100-common-docker-errors-solutions-4le0)
- [How to Debug and Fix Common Docker Issues - DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-debug-and-fix-common-docker-issues)
- [Common Docker Topics - Docker Docs](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/topics/)
- [5 Methods to Keep Docker Container Running for Debugging - Spacelift](https://spacelift.io/blog/docker-keep-container-running)
