---
name: docker-swarm
description: Docker Swarm orchestration, cluster management, and production deployments
sasmp_version: "1.3.0"
bonded_agent: 08-docker-orchestration
bond_type: PRIMARY_BOND
---

# Docker Swarm Skill

Master Docker Swarm for container orchestration, cluster management, and production deployments.

## Purpose

Set up and manage Docker Swarm clusters for high availability, service scaling, and production orchestration.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| managers | number | No | 3 | Number of manager nodes |
| workers | number | No | - | Number of worker nodes |
| encrypted | boolean | No | true | Encrypt overlay networks |

## Cluster Setup

### Initialize Swarm
```bash
# Initialize on first manager
docker swarm init --advertise-addr <MANAGER_IP>

# Get join tokens
docker swarm join-token worker
docker swarm join-token manager

# Join as worker
docker swarm join --token <WORKER_TOKEN> <MANAGER_IP>:2377

# Join as manager
docker swarm join --token <MANAGER_TOKEN> <MANAGER_IP>:2377
```

### High Availability (3 or 5 managers)
```bash
# Manager quorum: N/2 + 1
# 3 managers = tolerates 1 failure
# 5 managers = tolerates 2 failures
```

## Service Deployment

### Basic Service
```bash
# Create service
docker service create \
  --name webapp \
  --replicas 3 \
  --publish 80:80 \
  nginx:alpine

# Scale
docker service scale webapp=5

# Update image
docker service update --image nginx:1.25-alpine webapp

# Rollback
docker service rollback webapp
```

### Full Service Configuration
```bash
docker service create \
  --name api \
  --replicas 3 \
  --network backend \
  --publish 8080:3000 \
  --mount type=volume,source=data,target=/data \
  --secret db_password \
  --env NODE_ENV=production \
  --limit-cpu 0.5 \
  --limit-memory 512M \
  --update-delay 10s \
  --update-parallelism 1 \
  --update-failure-action rollback \
  --health-cmd "curl -f http://localhost:3000/health" \
  --health-interval 30s \
  myapp:latest
```

## Stack Deployment

### Production Stack
```yaml
# stack.yaml
services:
  frontend:
    image: frontend:${VERSION:-latest}
    deploy:
      replicas: 3
      placement:
        constraints:
          - node.role == worker
      update_config:
        parallelism: 1
        delay: 10s
        failure_action: rollback
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
    ports:
      - "80:80"
    networks:
      - frontend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s

  backend:
    image: backend:${VERSION:-latest}
    deploy:
      replicas: 3
    secrets:
      - db_password
    networks:
      - frontend
      - backend

networks:
  frontend:
    driver: overlay
  backend:
    driver: overlay
    internal: true

secrets:
  db_password:
    external: true
```

```bash
# Deploy stack
docker stack deploy -c stack.yaml myapp

# List services
docker stack services myapp

# Remove stack
docker stack rm myapp
```

## Secrets & Configs

### Secrets
```bash
# Create secret
echo "password" | docker secret create db_password -

# Use in service
docker service update --secret-add db_password myservice

# Rotate secret
echo "newpassword" | docker secret create db_password_v2 -
docker service update \
  --secret-rm db_password \
  --secret-add source=db_password_v2,target=db_password \
  myservice
```

### Configs
```bash
# Create config
docker config create nginx_config ./nginx.conf

# Use in service
docker service create \
  --config source=nginx_config,target=/etc/nginx/nginx.conf \
  nginx
```

## Node Management
```bash
# List nodes
docker node ls

# Drain node (maintenance)
docker node update --availability drain <node>

# Activate node
docker node update --availability active <node>

# Add label
docker node update --label-add role=database <node>

# Promote to manager
docker node promote <node>

# Demote from manager
docker node demote <node>
```

## Error Handling

### Common Errors
| Error | Cause | Solution |
|-------|-------|----------|
| `no suitable node` | Constraints not met | Relax or add nodes |
| `not converging` | Health check failing | Check service logs |
| `Raft: no leader` | Quorum lost | Restore managers |

### Manager Recovery
```bash
# If quorum lost, force new cluster
docker swarm init --force-new-cluster --advertise-addr <IP>
```

## Troubleshooting

### Debug Checklist
- [ ] Swarm active? `docker info | grep Swarm`
- [ ] Nodes healthy? `docker node ls`
- [ ] Service running? `docker service ls`
- [ ] Tasks placed? `docker service ps <svc>`

### Diagnostics
```bash
# Service status
docker service ls

# Task status
docker service ps <service> --no-trunc

# Service logs
docker service logs -f <service>

# Node issues
docker node inspect <node> --pretty
```

## Usage

```
Skill("docker-swarm")
```

## Assets
- `assets/swarm-stack.yaml` - Stack template
- `scripts/swarm-init.sh` - Init script

## Related Skills
- docker-networking
- docker-security
- docker-production
