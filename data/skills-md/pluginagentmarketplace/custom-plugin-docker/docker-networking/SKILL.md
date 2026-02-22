---
name: docker-networking
description: Configure Docker networking for containers including bridge, overlay, and service discovery
sasmp_version: "1.3.0"
bonded_agent: 03-docker-networking
bond_type: PRIMARY_BOND
---

# Docker Networking Skill

Master Docker networking concepts and configuration for container communication, service discovery, and network isolation.

## Purpose

Configure and troubleshoot Docker networks for development and production environments with proper isolation and service discovery.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| driver | enum | No | bridge | bridge/overlay/host/macvlan |
| subnet | string | No | - | Custom subnet CIDR |
| internal | boolean | No | false | Internal-only network |

## Network Drivers

| Driver | Use Case | Multi-Host | Encryption |
|--------|----------|------------|------------|
| bridge | Single host, default | No | No |
| overlay | Swarm, multi-host | Yes | Optional |
| host | Max performance | No | N/A |
| macvlan | Physical network | No | No |
| none | Disable networking | No | N/A |

## Configuration Examples

### Custom Bridge Network
```bash
# Create network with custom subnet
docker network create \
  --driver bridge \
  --subnet 172.28.0.0/16 \
  --gateway 172.28.0.1 \
  my_network

# Run container on network
docker run -d --name app \
  --network my_network \
  nginx:alpine
```

### Docker Compose Networking
```yaml
services:
  frontend:
    image: nginx:alpine
    networks:
      - public
    ports:
      - "80:80"

  backend:
    image: node:20-alpine
    networks:
      - public
      - private
    expose:
      - "3000"

  database:
    image: postgres:16-alpine
    networks:
      - private  # Internal only

networks:
  public:
    driver: bridge
  private:
    driver: bridge
    internal: true  # No external access
```

### Service Discovery
```yaml
# Containers can reach each other by service name
services:
  app:
    image: myapp
    environment:
      # Use service name as hostname
      DATABASE_HOST: database
      CACHE_HOST: redis

  database:
    image: postgres:16-alpine

  redis:
    image: redis:alpine
```

### Overlay Network (Swarm)
```bash
# Create encrypted overlay
docker network create \
  --driver overlay \
  --attachable \
  --opt encrypted \
  my_overlay
```

## Port Mapping

```bash
# Map host:container
docker run -p 8080:80 nginx

# Bind to specific interface
docker run -p 127.0.0.1:8080:80 nginx

# Random host port
docker run -P nginx

# UDP port
docker run -p 53:53/udp dnsserver
```

## Error Handling

### Common Errors
| Error | Cause | Solution |
|-------|-------|----------|
| `network not found` | Typo or deleted | Create network |
| `address in use` | Port conflict | Change port |
| `cannot reach` | Wrong network | Check network membership |
| `DNS failed` | Service not ready | Add health checks |

### Fallback Strategy
1. Verify network exists: `docker network ls`
2. Check container membership: `docker network inspect <net>`
3. Test DNS: `docker exec app nslookup backend`

## Troubleshooting

### Debug Checklist
- [ ] Network created? `docker network ls`
- [ ] Container connected? `docker inspect <container>`
- [ ] DNS resolving? `nslookup` from container
- [ ] Port mapped? `docker port <container>`

### Diagnostic Commands
```bash
# List networks
docker network ls

# Inspect network
docker network inspect my_network

# Test connectivity
docker exec app ping -c 3 database

# Check DNS
docker exec app nslookup backend

# View port mappings
docker port container_name
```

### Network Debugging
```bash
# Enter container network namespace
docker exec -it app sh

# Check DNS resolution
cat /etc/resolv.conf
nslookup database

# Check connectivity
ping -c 3 backend
curl http://backend:3000/health
```

## Usage

```
Skill("docker-networking")
```

## Related Skills
- docker-compose-setup
- docker-swarm
