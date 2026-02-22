---
name: docker-production
description: Deploy Docker containers to production with monitoring, logging, and health checks
sasmp_version: "1.3.0"
bonded_agent: 07-docker-production
bond_type: PRIMARY_BOND
---

# Docker Production Skill

Master production-grade Docker deployments with monitoring, logging, health checks, and resource management.

## Purpose

Configure containers for production with proper observability, resource limits, and deployment strategies.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| monitoring | enum | No | prometheus | prometheus/datadog |
| logging | enum | No | json-file | json-file/loki/elk |
| replicas | number | No | 1 | Number of replicas |

## Production Configuration

### Health Checks
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --retries=3 --start-period=60s \
  CMD curl -f http://localhost:3000/health || exit 1
```

```yaml
# Compose health check
services:
  app:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
```

### Resource Limits
```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
```

### Logging Configuration
```yaml
services:
  app:
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
        labels: "app,environment"
```

## Monitoring Stack

### Prometheus + Grafana
```yaml
services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_PASSWORD}

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    ports:
      - "8080:8080"
```

### Prometheus Config
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'docker-containers'
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
```

## Deployment Strategies

### Rolling Update (Zero Downtime)
```yaml
deploy:
  update_config:
    parallelism: 1
    delay: 10s
    failure_action: rollback
    order: start-first
  rollback_config:
    parallelism: 1
    delay: 10s
```

### Blue-Green
```bash
# Deploy new version
docker compose -p myapp-green up -d

# Switch traffic (update nginx/load balancer)
# Remove old version
docker compose -p myapp-blue down
```

## Error Handling

### Common Errors
| Error | Cause | Solution |
|-------|-------|----------|
| `unhealthy` | Health check failing | Check endpoint, increase start_period |
| `OOMKilled` | Memory exceeded | Increase limit or optimize |
| `restart loop` | App crash | Check logs, fix application |

### Recovery
1. Check logs: `docker logs --tail 100 <container>`
2. Verify health: `docker inspect --format='{{.State.Health.Status}}'`
3. Rollback if needed

## Troubleshooting

### Debug Checklist
- [ ] Health check passing?
- [ ] Resources sufficient? `docker stats`
- [ ] Logs showing errors?
- [ ] Metrics collecting?

### Diagnostics
```bash
# Resource usage
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# Restart count
docker inspect --format='{{.RestartCount}}' <container>

# Recent events
docker events --filter 'container=<name>' --since 1h
```

## Usage

```
Skill("docker-production")
```

## Related Skills
- docker-debugging
- docker-ci-cd
- docker-security
