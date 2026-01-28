---
name: docker-helper
description: Expert helper for Docker containers, Docker Compose, and container optimization
---

# Docker-helper

## Instructions

When helping with Docker tasks:
1. Check running containers: docker ps -a
2. View logs: docker logs -f <container>
3. Inspect container: docker inspect <container>
4. Execute commands: docker exec -it <container> /bin/bash
- Use multi-stage builds to reduce image size
- Order Dockerfile commands by frequency of change
- Use .dockerignore to exclude unnecessary files
- Avoid running as root; create non-privileged users
- Use health checks in docker-compose
- Networking: Check bridge networks and port mappings
- Volumes: Verify volume mounts and permissions
- Build cache: Use --no-cache when needed
- Resource limits: Set memory/CPU limits appropriately
- Use version 3+ syntax
- Leverage environment files (.env)
- Use depends_on with health checks
- Implement restart policies


## Examples

Add examples of how to use this skill here.

## Notes

- This skill was auto-generated
- Edit this file to customize behavior
