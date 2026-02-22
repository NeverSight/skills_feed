---
name: docker-debugging
description: Container debugging and troubleshooting techniques for production issues
sasmp_version: "1.3.0"
bonded_agent: 07-docker-production
bond_type: PRIMARY_BOND
---

# Docker Debugging Skill

Master container debugging and troubleshooting for development and production issues.

## Purpose

Diagnose and resolve container issues including crashes, performance problems, networking failures, and resource constraints.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| container | string | No | - | Container name/ID |
| issue_type | enum | No | - | crash/network/resource/health |
| verbose | boolean | No | false | Detailed output |

## Debugging Commands

### Container Logs
```bash
# Last 100 lines
docker logs --tail 100 <container>

# Follow logs
docker logs -f <container>

# With timestamps
docker logs -t <container>

# Specific time range
docker logs --since 1h --until 30m <container>
```

### Interactive Debugging
```bash
# Execute shell in running container
docker exec -it <container> /bin/sh

# As root (for debugging)
docker exec -u 0 -it <container> /bin/sh

# Run command
docker exec <container> ps aux
```

### Container Inspection
```bash
# Full inspection
docker inspect <container>

# Specific fields
docker inspect --format='{{.State.Status}}' <container>
docker inspect --format='{{.State.Health.Status}}' <container>
docker inspect --format='{{json .NetworkSettings}}' <container>
```

## Issue Diagnosis

### Container Won't Start
```bash
# Check exit code
docker inspect --format='{{.State.ExitCode}}' <container>

# View last logs
docker logs --tail 50 <container>

# Check events
docker events --filter 'container=<name>' --since 1h
```

### Exit Code Reference
| Code | Meaning | Action |
|------|---------|--------|
| 0 | Success | Normal exit |
| 1 | General error | Check logs |
| 137 | OOMKilled | Increase memory |
| 139 | Segfault | Check app code |
| 143 | SIGTERM | Graceful shutdown |

### Health Check Failures
```bash
# Check health status
docker inspect --format='{{json .State.Health}}' <container>

# View health logs
docker inspect --format='{{range .State.Health.Log}}{{.Output}}{{end}}' <container>

# Manually test health
docker exec <container> curl -f http://localhost/health
```

### Resource Issues
```bash
# Live stats
docker stats <container>

# Formatted output
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

# Check limits
docker inspect --format='{{.HostConfig.Memory}}' <container>
```

### Network Issues
```bash
# Check network
docker network inspect <network>

# Test DNS
docker exec <container> nslookup <service>

# Test connectivity
docker exec <container> ping -c 3 <target>
docker exec <container> curl http://<service>:port

# View ports
docker port <container>
```

## Troubleshooting Flowchart

```
Container Issue?
│
├─ Won't Start
│  ├─ Check logs: docker logs <c>
│  ├─ Check exit code: docker inspect
│  └─ Verify image: docker pull
│
├─ Unhealthy
│  ├─ Check health logs
│  ├─ Test health endpoint manually
│  └─ Increase start_period
│
├─ High Resource
│  ├─ Check stats: docker stats
│  ├─ Increase limits
│  └─ Profile application
│
└─ Network Failed
   ├─ Check DNS: nslookup
   ├─ Check connectivity: ping/curl
   └─ Verify network membership
```

## Debug Container
```bash
# Run debug container in same network
docker run --rm -it --network <network> \
  nicolaka/netshoot

# Available tools: curl, dig, nmap, tcpdump, etc.
```

## Error Handling

### Common Errors
| Error | Cause | Solution |
|-------|-------|----------|
| `container not found` | Wrong name/ID | Use `docker ps -a` |
| `exec failed` | Container stopped | Start container first |
| `no such file` | Missing binary | Use correct image |

## Usage

```
Skill("docker-debugging")
```

## Assets
- `assets/debug-commands.yaml` - Command reference
- `scripts/container-health-check.sh` - Health check script

## Related Skills
- docker-production
- docker-networking
