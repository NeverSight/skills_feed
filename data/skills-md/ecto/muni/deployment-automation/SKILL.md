---
name: deployment-automation
description: Guides deployment of Muni software to rovers (aarch64 cross-compilation, systemd) and depot (Docker Compose). Use when deploying firmware updates, installing services, configuring environments, troubleshooting deployment failures, or setting up new rovers/depot instances. Covers cross-compilation with `cross` tool, deploy.sh script usage, systemd service management, Docker Compose profiles, environment variables, and rollback procedures.
allowed-tools: Read, Grep, Glob, Bash(cross:build), Bash(cargo:build), Bash(scp), Bash(ssh), Bash(docker:*), Bash(systemctl)
---

# Deployment Automation Skill

Guides deployment of Muni software across heterogeneous platforms: rovers (ARM64) and depot (x86_64).

## Overview

Muni has two deployment targets with different strategies:

| Target | Platform | Method | Build Tool | Deploy Tool |
|--------|----------|--------|------------|-------------|
| **Rovers** | aarch64 (ARM64) | Binary + systemd | `cross` / `cargo` | `deploy.sh` (scp + ssh) |
| **Depot** | x86_64 | Docker containers | Docker | docker-compose |

### Key Files

**Rover Deployment**:
- `bvr/firmware/deploy.sh` - Deployment script
- `bvr/firmware/config/bvr.toml` - Runtime configuration
- `bvr/firmware/config/*.service` - Systemd service units

**Depot Deployment**:
- `depot/docker-compose.yml` - Service orchestration
- `depot/.env` - Environment variables
- `depot/*/Dockerfile` - Service images

## Rover Deployment

### Cross-Compilation Setup

#### Install Cross

**Requirements**:
- Rust 1.83+
- Docker (for cross)
- `cross` tool

```bash
# Install cross tool
cargo install cross --git https://github.com/cross-rs/cross

# Verify installation
cross --version
```

**Why cross?**
- Handles cross-compilation toolchains automatically
- Uses Docker to provide consistent build environment
- Supports aarch64-unknown-linux-gnu target
- Easier than setting up native cross-compilation

**Alternative: Native cargo**
```bash
# Add target
rustup target add aarch64-unknown-linux-gnu

# Install GCC cross-compiler (macOS)
brew install aarch64-unknown-linux-gnu

# Build (may not work for complex dependencies)
cargo build --release --target aarch64-unknown-linux-gnu
```

⚠️ **Native cross-compilation limitations**:
- May fail with system dependencies (e.g., GStreamer)
- Requires manual toolchain setup
- Platform-specific quirks

✅ **cross is recommended** for reliability

#### Cross.toml Configuration

```toml
# bvr/firmware/Cross.toml (if needed)
[build]
default-target = "aarch64-unknown-linux-gnu"

[target.aarch64-unknown-linux-gnu]
# Use custom Docker image with dependencies
image = "ghcr.io/cross-rs/aarch64-unknown-linux-gnu:latest"
```

### Deploy Script Usage

#### Basic Deployment

```bash
cd bvr/firmware

# Deploy bvrd binary only (default)
./deploy.sh frog-0

# Deploy without restarting service
./deploy.sh frog-0 --no-restart

# Deploy to specific user
./deploy.sh frog-0 --user admin
```

#### Full Deployment

```bash
# Deploy everything (--all)
# - bvrd binary
# - muni CLI tool
# - Config file (bvr.toml)
# - Systemd services (bvrd, can, kiosk)
# - Sync timer (bvr-sync)
./deploy.sh frog-0 --all

# Equivalent to:
./deploy.sh frog-0 --cli --config --services --sync
```

#### Partial Deployment

```bash
# Deploy bvrd + CLI tool
./deploy.sh frog-0 --cli

# Deploy and update config
./deploy.sh frog-0 --config

# Install/update systemd services only
./deploy.sh frog-0 --services

# Install sync timer only
./deploy.sh frog-0 --sync
```

### Deploy Script Internals

**What deploy.sh does**:

1. **Build Phase**:
   ```bash
   # Uses cross or cargo to build for aarch64
   cross build --release --target aarch64-unknown-linux-gnu --bin bvrd
   ```

2. **Pre-Deploy Phase**:
   ```bash
   # Stop service before deploying
   ssh $REMOTE "sudo systemctl stop bvrd"
   ```

3. **Deploy Phase**:
   ```bash
   # Copy binary to rover
   scp target/aarch64-unknown-linux-gnu/release/bvrd $REMOTE:/tmp/
   ssh $REMOTE "sudo mv /tmp/bvrd /usr/local/bin/ && sudo chmod +x /usr/local/bin/bvrd"

   # Copy config (if --config)
   scp config/bvr.toml $REMOTE:/tmp/
   ssh $REMOTE "sudo mv /tmp/bvr.toml /etc/bvr/"

   # Install services (if --services)
   scp config/*.service $REMOTE:/tmp/
   ssh $REMOTE "sudo mv /tmp/*.service /etc/systemd/system/ && sudo systemctl daemon-reload"
   ```

4. **Post-Deploy Phase**:
   ```bash
   # Start/restart service (unless --no-restart)
   ssh $REMOTE "sudo systemctl start bvrd"
   ssh $REMOTE "sudo systemctl status bvrd"
   ```

### Systemd Service Management

#### Service Units

**bvrd.service** (main daemon):
```ini
[Unit]
Description=BVR Daemon
After=network.target can.service
Requires=can.service

[Service]
Type=simple
User=cam
ExecStart=/usr/local/bin/bvrd
Restart=always
RestartSec=5
Environment="RUST_LOG=info"
WorkingDirectory=/home/cam

[Install]
WantedBy=multi-user.target
```

**can.service** (CAN bus setup):
```ini
[Unit]
Description=CAN Bus Setup
Before=bvrd.service

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/local/bin/setup-can.sh
ExecStop=/usr/local/bin/teardown-can.sh

[Install]
WantedBy=multi-user.target
```

**bvr-sync.service** (session sync):
```ini
[Unit]
Description=BVR Session Sync
After=network.target

[Service]
Type=oneshot
User=cam
ExecStart=/usr/local/bin/bvr-sync
Environment="RUST_LOG=info"
```

**bvr-sync.timer** (periodic sync):
```ini
[Unit]
Description=BVR Session Sync Timer
Requires=bvr-sync.service

[Timer]
OnBootSec=5min
OnUnitActiveSec=15min

[Install]
WantedBy=timers.target
```

#### Service Commands

```bash
# Start service
ssh frog-0 "sudo systemctl start bvrd"

# Stop service
ssh frog-0 "sudo systemctl stop bvrd"

# Restart service
ssh frog-0 "sudo systemctl restart bvrd"

# Check status
ssh frog-0 "sudo systemctl status bvrd"

# Enable on boot
ssh frog-0 "sudo systemctl enable bvrd"

# Disable on boot
ssh frog-0 "sudo systemctl disable bvrd"

# View logs
ssh frog-0 "sudo journalctl -u bvrd -f"

# View last 100 lines
ssh frog-0 "sudo journalctl -u bvrd -n 100"

# Reload service files after editing
ssh frog-0 "sudo systemctl daemon-reload"
```

### Configuration Management

**bvr.toml** (runtime configuration):
```toml
# Rover identification
[rover]
id = "frog-0"
name = "Frog Zero"

# Network configuration
[network]
discovery_url = "http://10.0.0.1:4860"
teleop_bind = "0.0.0.0:4850"
video_bind = "0.0.0.0:4851"

# CAN bus configuration
[can]
interface = "can0"
bitrate = 500000

# GPS configuration
[gps]
port = "/dev/ttyUSB0"
baudrate = 115200
```

**Deploying config changes**:
```bash
# Edit config locally
vim bvr/firmware/config/bvr.toml

# Deploy config
./deploy.sh frog-0 --config

# Restart service to reload config
./deploy.sh frog-0 --config  # Restarts by default
```

### Troubleshooting Rover Deployment

#### Build Failures

**cross not found**:
```bash
# Install cross
cargo install cross --git https://github.com/cross-rs/cross
```

**Docker not running**:
```bash
# Start Docker
# macOS: Start Docker Desktop
# Linux: sudo systemctl start docker
```

**Compilation errors**:
```bash
# Clean build
cargo clean
cross build --release --target aarch64-unknown-linux-gnu

# Check Rust version
rustup show

# Update Rust
rustup update
```

#### Deployment Failures

**SSH connection failed**:
```bash
# Test SSH
ssh frog-0

# Check Tailscale
tailscale status

# Check SSH keys
ssh-add -l
```

**Permission denied on rover**:
```bash
# User needs sudo without password for:
# - systemctl
# - mv to /usr/local/bin/, /etc/bvr/, /etc/systemd/system/

# Add to sudoers
ssh frog-0 "echo '$USER ALL=(ALL) NOPASSWD: /bin/systemctl, /bin/mv' | sudo tee /etc/sudoers.d/$USER"
```

**Service won't start**:
```bash
# Check service status
ssh frog-0 "sudo systemctl status bvrd"

# View logs
ssh frog-0 "sudo journalctl -u bvrd -n 100"

# Check binary permissions
ssh frog-0 "ls -l /usr/local/bin/bvrd"

# Check config file
ssh frog-0 "cat /etc/bvr/bvr.toml"

# Test binary manually
ssh frog-0 "/usr/local/bin/bvrd"
```

#### Rollback Procedure

```bash
# Keep previous binary
ssh frog-0 "sudo cp /usr/local/bin/bvrd /usr/local/bin/bvrd.backup"

# Deploy new version
./deploy.sh frog-0

# If new version fails, rollback:
ssh frog-0 "sudo systemctl stop bvrd"
ssh frog-0 "sudo mv /usr/local/bin/bvrd.backup /usr/local/bin/bvrd"
ssh frog-0 "sudo systemctl start bvrd"
```

## Depot Deployment

### Docker Compose Deployment

#### Initial Setup

```bash
cd depot

# Create .env file from example
cp .env.example .env

# Edit environment variables
vim .env
```

**.env file**:
```bash
# Authentication
CONSOLE_PASSWORD=your_secure_password
GRAFANA_ADMIN_PASSWORD=your_grafana_password

# InfluxDB
INFLUXDB_ADMIN_TOKEN=your_influxdb_token
INFLUXDB_ORG=muni
INFLUXDB_BUCKET=muni

# Storage
SESSIONS_PATH=/data/sessions
MAPS_PATH=/data/maps

# Retention
RETENTION_DAYS=30
```

#### Build and Start

```bash
# Build all services
docker compose build

# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Check status
docker compose ps
```

#### Service Profiles

**Base services** (always run):
- console (web UI)
- discovery (rover tracking)
- dispatch (mission planning)
- map-api (map serving)
- influxdb (metrics)
- grafana (dashboards)
- postgres (dispatch database)
- sftp (session sync)

**GPU profile** (optional):
```bash
# Start with GPU support for 3D reconstruction
docker compose --profile gpu up -d

# Enables:
# - splat-worker (Gaussian splatting)
# - mapper (map processing)
```

**RTK profile** (optional):
```bash
# Start with RTK base station support
docker compose --profile rtk up -d

# Enables:
# - rtk-base (GNSS base station)
# - gps-status (RTK monitoring)
```

**Multiple profiles**:
```bash
# Run everything
docker compose --profile gpu --profile rtk up -d
```

### Service Updates

#### Update Single Service

```bash
# Pull latest code
git pull

# Rebuild service
docker compose build discovery

# Restart service
docker compose up -d discovery

# View logs
docker compose logs -f discovery
```

#### Update All Services

```bash
# Pull latest code
git pull

# Rebuild all
docker compose build

# Restart all
docker compose up -d

# Check for issues
docker compose ps
docker compose logs -f
```

#### Rolling Updates

```bash
# Update services one at a time
for service in discovery dispatch map-api gps-status; do
    echo "Updating $service..."
    docker compose build $service
    docker compose up -d $service
    sleep 5
    docker compose ps $service
done
```

### Database Migrations

**Dispatch service** (PostgreSQL):

Migrations run automatically on service startup (see `depot/dispatch/src/main.rs`).

**Manual migration** (if needed):
```bash
# Connect to database
docker compose exec postgres psql -U postgres -d dispatch

# Run migration SQL
\i /path/to/migration.sql

# Restart service
docker compose restart dispatch
```

**Reset database** (DESTRUCTIVE):
```bash
# Stop services
docker compose down

# Remove database volume
docker volume rm depot_postgres-data

# Restart services (migrations run automatically)
docker compose up -d
```

### Environment Configuration

#### Updating Environment Variables

```bash
# Edit .env
vim depot/.env

# Restart affected services
docker compose up -d
```

**Which services need restart after .env changes?**
- **Console**: `CONSOLE_PASSWORD`, `CONSOLE_USERNAME`
- **InfluxDB**: `INFLUXDB_*` variables
- **Grafana**: `GRAFANA_*` variables
- **Discovery**: `SESSIONS_PATH`
- **Dispatch**: `DATABASE_URL`

#### Secrets Management

**Development**:
```bash
# Use .env file
# chmod 600 .env to restrict access
```

**Production**:
```bash
# Use Docker secrets (Swarm mode)
docker secret create database_password /path/to/secret.txt

# Reference in docker-compose.yml:
services:
  dispatch:
    secrets:
      - database_password

secrets:
  database_password:
    external: true
```

### Troubleshooting Depot Deployment

#### Service Won't Start

```bash
# Check logs
docker compose logs -f <service>

# Check status
docker compose ps <service>

# Check exit code
docker inspect --format='{{.State.ExitCode}}' depot-<service>

# Run service with shell override
docker compose run --rm <service> sh
```

#### Network Issues

```bash
# List networks
docker network ls

# Inspect network
docker network inspect depot_default

# Test connectivity
docker compose exec console ping discovery
docker compose exec console wget -O- http://discovery:4860/health
```

#### Volume Issues

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect depot_sessions-data

# Check permissions
docker compose exec discovery ls -la /data/sessions
```

#### Health Check Failing

```bash
# Check health status
docker inspect depot-discovery | jq '.[0].State.Health'

# Test health endpoint manually
docker compose exec discovery wget -O- http://localhost:4860/health

# Check service logs
docker compose logs -f discovery
```

#### Port Conflicts

```bash
# Check if port is in use
lsof -i :4860

# Change port in docker-compose.yml:
ports:
  - "4870:4860"  # Map host 4870 to container 4860
```

#### Out of Disk Space

```bash
# Check disk usage
df -h

# Check Docker disk usage
docker system df

# Clean up
docker system prune -a --volumes

# Remove old images
docker image prune -a

# Remove unused volumes
docker volume prune
```

### Backup and Restore

#### Backup

```bash
# Backup volumes
docker run --rm \
  -v depot_postgres-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/postgres-backup.tar.gz /data

# Backup .env
cp depot/.env depot/.env.backup

# Backup config files
tar czf depot-config-backup.tar.gz depot/.env depot/docker-compose.yml depot/grafana/
```

#### Restore

```bash
# Stop services
docker compose down

# Remove old volume
docker volume rm depot_postgres-data

# Create new volume
docker volume create depot_postgres-data

# Restore data
docker run --rm \
  -v depot_postgres-data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/postgres-backup.tar.gz -C /

# Restore config
tar xzf depot-config-backup.tar.gz

# Start services
docker compose up -d
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Deploy Depot

on:
  push:
    branches: [main]
    paths:
      - 'depot/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build images
        run: |
          cd depot
          docker compose build

      - name: Push to registry
        run: |
          echo "${{ secrets.REGISTRY_PASSWORD }}" | docker login -u "${{ secrets.REGISTRY_USERNAME }}" --password-stdin
          docker compose push

      - name: Deploy to server
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.DEPLOY_HOST }}
          username: ${{ secrets.DEPLOY_USER }}
          key: ${{ secrets.DEPLOY_KEY }}
          script: |
            cd /opt/depot
            docker compose pull
            docker compose up -d
```

### GitLab CI

```yaml
stages:
  - build
  - deploy

build:
  stage: build
  script:
    - cd depot
    - docker compose build
    - docker compose push

deploy:
  stage: deploy
  only:
    - main
  script:
    - ssh $DEPLOY_USER@$DEPLOY_HOST "cd /opt/depot && docker compose pull && docker compose up -d"
```

## Deployment Checklists

### New Rover Setup

- [ ] Install Ubuntu 22.04 on Jetson Orin NX
- [ ] Install Tailscale and join network
- [ ] Set hostname (e.g., `frog-0`)
- [ ] Create user account with sudo access
- [ ] Install CAN tools: `sudo apt install can-utils`
- [ ] Configure CAN interface in `/etc/network/interfaces`
- [ ] Copy `bvr/firmware/config/bvr.toml` and customize
- [ ] Deploy with `--all`: `./deploy.sh frog-0 --all`
- [ ] Enable services: `ssh frog-0 "sudo systemctl enable bvrd can"`
- [ ] Test: check discovery service shows rover online

### New Depot Setup

- [ ] Clone repository
- [ ] Install Docker and Docker Compose
- [ ] Create `depot/.env` from example
- [ ] Configure environment variables
- [ ] Create data directories: `/data/sessions`, `/data/maps`
- [ ] Set permissions: `sudo chown -R 1000:1000 /data/`
- [ ] Start services: `docker compose up -d`
- [ ] Check health: `docker compose ps`
- [ ] Access console: `http://localhost`
- [ ] Configure Grafana dashboards
- [ ] Set up SSL (if exposing to internet)

### Deployment Smoke Tests

**Rover**:
- [ ] Service running: `ssh frog-0 "systemctl is-active bvrd"`
- [ ] Registers with discovery: check console UI
- [ ] CAN bus active: `ssh frog-0 "ip link show can0"`
- [ ] GPS receiving: `ssh frog-0 "journalctl -u bvrd | grep GPS"`
- [ ] Teleop works: connect via console

**Depot**:
- [ ] All services healthy: `docker compose ps`
- [ ] Console accessible: `curl http://localhost/health`
- [ ] Discovery API works: `curl http://localhost:4860/rovers`
- [ ] Database connected: `docker compose exec postgres pg_isready`
- [ ] InfluxDB receiving metrics: check Grafana
- [ ] Grafana dashboards load

## References

- [Cross documentation](https://github.com/cross-rs/cross)
- [Docker Compose reference](https://docs.docker.com/compose/)
- [Systemd service docs](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
- [CLAUDE.md](../../CLAUDE.md) - Project conventions
- [depot/README.md](../../depot/README.md) - Depot architecture
- [bvr/firmware/README.md](../../bvr/firmware/README.md) - Firmware build guide
