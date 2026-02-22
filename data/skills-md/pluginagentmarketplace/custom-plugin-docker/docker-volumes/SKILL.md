---
name: docker-volumes
description: Implement persistent storage with Docker volumes, bind mounts, and backup strategies
sasmp_version: "1.3.0"
bonded_agent: 04-docker-volumes
bond_type: PRIMARY_BOND
---

# Docker Volumes Skill

Master Docker persistent storage including named volumes, bind mounts, tmpfs, and data backup/restore procedures.

## Purpose

Implement reliable data persistence for containers with proper volume management, backup strategies, and permission handling.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| volume_name | string | No | - | Name for the volume |
| mount_type | enum | No | volume | volume/bind/tmpfs |
| backup | boolean | No | false | Include backup commands |

## Storage Types

| Type | Persistence | Use Case | Managed By |
|------|-------------|----------|------------|
| Named Volume | Yes | Production data | Docker |
| Bind Mount | Yes | Development, configs | Host |
| tmpfs | No (memory) | Secrets, temp files | Docker |
| Anonymous | Container lifetime | Scratch space | Docker |

## Volume Operations

### Named Volumes
```bash
# Create volume
docker volume create app_data

# Use in container
docker run -d \
  -v app_data:/var/lib/postgresql/data \
  postgres:16-alpine

# Inspect volume
docker volume inspect app_data

# List volumes
docker volume ls

# Remove unused volumes
docker volume prune
```

### Bind Mounts
```bash
# Development - mount source code
docker run -d \
  -v $(pwd)/src:/app/src \
  node:20-alpine

# Read-only config
docker run -d \
  -v /etc/app/config.yaml:/app/config.yaml:ro \
  myapp
```

### tmpfs Mounts
```bash
# Sensitive data in memory
docker run -d \
  --tmpfs /app/secrets:rw,noexec,nosuid,size=64m \
  myapp

# Compose syntax
services:
  app:
    volumes:
      - type: tmpfs
        target: /app/tmp
        tmpfs:
          size: 100m
```

## Docker Compose Volumes
```yaml
services:
  database:
    image: postgres:16-alpine
    volumes:
      - db_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}

  app:
    image: myapp
    volumes:
      - uploads:/app/uploads
      - ./config:/app/config:ro

volumes:
  db_data:
    driver: local
  uploads:
    external: true  # Pre-created
```

## Backup & Restore

### Backup Volume
```bash
# Backup to tar file
docker run --rm \
  -v app_data:/source:ro \
  -v $(pwd)/backups:/backup \
  alpine tar cvf /backup/app_data_$(date +%Y%m%d).tar -C /source .

# Compressed backup
docker run --rm \
  -v app_data:/source:ro \
  -v $(pwd)/backups:/backup \
  alpine tar czvf /backup/app_data_$(date +%Y%m%d).tar.gz -C /source .
```

### Restore Volume
```bash
# Restore from tar
docker run --rm \
  -v app_data:/dest \
  -v $(pwd)/backups:/backup:ro \
  alpine tar xvf /backup/app_data_20240101.tar -C /dest
```

### Clone Volume
```bash
docker run --rm \
  -v source_volume:/from:ro \
  -v target_volume:/to \
  alpine cp -av /from/. /to/
```

## Error Handling

### Common Errors
| Error | Cause | Solution |
|-------|-------|----------|
| `volume in use` | Container running | Stop container first |
| `permission denied` | UID mismatch | Fix ownership |
| `no space left` | Disk full | Clean up or expand |
| `path not found` | Bind mount missing | Create directory |

### Permission Fixes
```bash
# Check ownership
docker run --rm -v app_data:/data alpine ls -la /data

# Fix ownership (match container user)
docker run --rm -v app_data:/data alpine chown -R 1000:1000 /data

# SELinux (RHEL/CentOS)
docker run -v /host/path:/container/path:Z myimage
```

## Troubleshooting

### Debug Checklist
- [ ] Volume exists? `docker volume ls`
- [ ] Mount visible? `docker exec <c> df -h`
- [ ] Permissions correct? `ls -la` in container
- [ ] Data persisting? Stop/start container

### Diagnostic Commands
```bash
# Check volume location
docker volume inspect app_data --format '{{.Mountpoint}}'

# Check container mounts
docker inspect <container> --format '{{json .Mounts}}'

# Check disk usage
docker system df -v
```

## Usage

```
Skill("docker-volumes")
```

## Related Skills
- docker-compose-setup
- docker-production
