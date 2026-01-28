---
name: docker-security-guide
description: Comprehensive Docker security guidelines and threat mitigation strategies
---

## 🚨 CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

**Examples:**
- ❌ WRONG: `D:/repos/project/file.tsx`
- ✅ CORRECT: `D:\repos\project\file.tsx`

This applies to:
- Edit tool file_path parameter
- Write tool file_path parameter
- All file operations on Windows systems


### Documentation Guidelines

**NEVER create new documentation files unless explicitly requested by the user.**

- **Priority**: Update existing README.md files rather than creating new documentation
- **Repository cleanliness**: Keep repository root clean - only README.md unless user requests otherwise
- **Style**: Documentation should be concise, direct, and professional - avoid AI-generated tone
- **User preference**: Only create additional .md files when user specifically asks for documentation


---

# Docker Security Guide

This skill provides comprehensive security guidelines for Docker across all platforms, covering threats, mitigations, and compliance requirements.

## Security Principles

### Defense in Depth

Apply security at multiple layers:
1. **Image security:** Minimal, scanned, signed images
2. **Build security:** Secure build process, no secrets in layers
3. **Runtime security:** Restricted capabilities, resource limits
4. **Network security:** Isolation, least privilege
5. **Host security:** Hardened host OS, updated Docker daemon
6. **Orchestration security:** Secure configuration, RBAC
7. **Monitoring:** Detection, logging, alerting

### Least Privilege

Grant only the minimum permissions necessary:
- Non-root users
- Dropped capabilities
- Read-only filesystems
- Minimal network exposure
- Restricted syscalls (seccomp)
- Limited resources

## Image Security

### Base Image Selection

**Threat:** Vulnerable or malicious base images

**Mitigation:**
```dockerfile
# Use official images only
FROM node:20.11.0-alpine3.19  # Official, specific version

# NOT
FROM randomuser/node  # Unverified source
FROM node:latest      # Unpredictable, can break
```

**Verification:**
```bash
# Verify image source
docker image inspect node:20-alpine | grep -A 5 "Author"

# Enable Docker Content Trust (image signing)
export DOCKER_CONTENT_TRUST=1
docker pull node:20-alpine
```

### Minimal Images

**Threat:** Larger attack surface, more vulnerabilities

**Mitigation:**
```dockerfile
# Prefer minimal distributions
FROM alpine:3.19           # ~7MB
FROM gcr.io/distroless/static  # ~2MB
FROM scratch               # 0MB (for static binaries)

# vs
FROM ubuntu:22.04          # ~77MB with more packages
```

**Benefits:**
- Fewer packages = fewer vulnerabilities
- Smaller attack surface
- Faster downloads and starts
- Less disk space

### Micro-Distros for Security-Critical Applications (2025)

**Wolfi/Chainguard Images:**
- Zero-CVE goal, SBOM included by default
- Nightly security patches, signed with provenance
- Available for: Node, Python, Go, Java, .NET, etc.

**Usage:**
```dockerfile
# Development stage (includes build tools)
FROM cgr.dev/chainguard/node:latest-dev AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Production stage (minimal, zero-CVE goal)
FROM cgr.dev/chainguard/node:latest
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
USER node
ENTRYPOINT ["node", "server.js"]
```

**When to use:** Security-critical apps, compliance requirements (SOC2, HIPAA, PCI-DSS), zero-trust environments, supply chain security emphasis.

See `docker-best-practices` skill for full image comparison table.

### Vulnerability Scanning

**Tools:**
- Docker Scout (built-in)
- Trivy
- Grype
- Snyk
- Clair

**Process:**
```bash
# Scan with Docker Scout
docker scout cves IMAGE_NAME
docker scout recommendations IMAGE_NAME

# Scan with Trivy
trivy image IMAGE_NAME
trivy image --severity HIGH,CRITICAL IMAGE_NAME

# Scan Dockerfile
trivy config Dockerfile

# Scan for secrets
trivy fs --scanners secret .
```

**CI/CD Integration:**
```yaml
# GitHub Actions example
- name: Scan image
  run: |
    docker scout cves my-image:${{ github.sha }}
    trivy image --exit-code 1 --severity CRITICAL my-image:${{ github.sha }}
```

### Multi-Stage Builds for Security

**Threat:** Build tools and secrets in final image

**Mitigation:**
```dockerfile
# Build stage with build tools
FROM golang:1.21 AS builder
WORKDIR /app
COPY . .
RUN go build -o app

# Final stage - minimal, no build tools
FROM gcr.io/distroless/base-debian11
COPY --from=builder /app/app /
USER nonroot:nonroot
ENTRYPOINT ["/app"]
```

**Benefits:**
- No compiler/build tools in production image
- Secrets used in build don't persist
- Smaller, more secure final image

## Build-Time Security

### Secrets Management

**NEVER:**
```dockerfile
# BAD - Secret in layer history
ENV API_KEY=abc123
RUN git clone https://user:password@github.com/repo.git
COPY .env /app/.env
```

**DO:**
```dockerfile
# Use BuildKit secrets
# syntax=docker/dockerfile:1

FROM alpine
RUN --mount=type=secret,id=github_token \
    git clone https://$(cat /run/secrets/github_token)@github.com/repo.git
```

```bash
# Build with secret (not in image)
docker build --secret id=github_token,src=./token.txt .
```

### BuildKit Frontend Security (2025)

**Threat:** Malicious or compromised BuildKit frontends can execute arbitrary code during build

**🚨 2025 CRITICAL WARNING:** BuildKit supports custom frontends (parsers) via `# syntax=` directive. Untrusted frontends have FULL BUILD-TIME code execution and can:
- Steal secrets from build context
- Modify build outputs
- Exfiltrate data
- Compromise the build environment

**Risk Example:**
```dockerfile
# 🔴 DANGER - Untrusted frontend (code execution risk!)
# syntax=docker/dockerfile:1@sha256:abc123...untrusted

FROM alpine
RUN echo "This frontend could do anything during build"
```

**Mitigation:**

1. **Only use official Docker frontends:**
```dockerfile
# ✅ Safe - Official Docker frontend
# syntax=docker/dockerfile:1

# ✅ Safe - Specific version
# syntax=docker/dockerfile:1.5

# ✅ Safe - Pinned with digest (verify from docker.com)
# syntax=docker/dockerfile:1@sha256:ac85f380a63b13dfcefa89046420e1781752bab202122f8f50032edf31be0021
```

2. **Verify frontend sources:**
- Use ONLY `docker/dockerfile:*` frontends
- Pin to specific versions with SHA256 digest
- Verify digests from official Docker documentation
- Never use third-party frontends without thorough vetting

3. **Audit all Dockerfiles for unsafe syntax directives:**
```bash
# Check all Dockerfiles for potentially malicious syntax directives
grep -r "^# syntax=" . --include="Dockerfile*"

# Verify all frontends are official Docker images
grep -r "^# syntax=" . --include="Dockerfile*" | grep -v "docker/dockerfile"
```

4. **BuildKit security configuration (defense in depth):**
```bash
# Restrict frontend sources in BuildKit config
# /etc/buildkit/buildkitd.toml
[frontend."dockerfile.v0"]
  # Only allow official Docker frontends
  allowedImages = ["docker.io/docker/dockerfile:*"]
```

**Supply Chain Protection:**
- Treat custom frontends as HIGH RISK code execution vectors
- Review ALL `# syntax=` directives in Dockerfiles before builds
- Use content trust for frontend images
- Monitor for frontend vulnerabilities
- Include frontend verification in CI/CD security gates

### SBOM (Software Bill of Materials) Generation (2025)

**Critical 2025 Requirement:** Document origin and history of all components for supply chain transparency and compliance.

**Why SBOM is Mandatory:**
- Supply chain security visibility
- Vulnerability tracking and response
- Compliance requirements (Executive Order 14028, etc.)
- License compliance
- Incident response readiness

**Generate SBOM with Docker Scout:**
```bash
# Generate SBOM for image
docker scout sbom IMAGE_NAME

# Export SBOM in different formats
docker scout sbom --format spdx IMAGE_NAME > sbom.spdx.json
docker scout sbom --format cyclonedx IMAGE_NAME > sbom.cyclonedx.json

# Include SBOM attestation during build
# ⚠️ WARNING: BuildKit attestations are NOT cryptographically signed!
docker buildx build \
  --sbom=true \
  --provenance=true \
  --tag my-image:latest \
  .

# View SBOM attestations (unsigned metadata only)
docker buildx imagetools inspect my-image:latest --format "{{ json .SBOM }}"
```

**🚨 CRITICAL SECURITY LIMITATION:**
BuildKit attestations (`--sbom=true`, `--provenance=true`) are **NOT cryptographically signed**. This means:
- Anyone with push access can create tampered attestations
- SBOMs can be incomplete or falsified
- Provenance data cannot be trusted without external verification
- **For production:** Use external signing tools (cosign, Notary) and Syft for SBOM generation

**Generate SBOM with Syft:**
```bash
# Install Syft
curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh

# Generate SBOM from image
syft my-image:latest

# Generate in specific format
syft my-image:latest -o spdx-json > sbom.spdx.json
syft my-image:latest -o cyclonedx-json > sbom.cyclonedx.json

# Generate from Dockerfile
syft dir:. -o spdx-json > sbom.spdx.json
```

**SBOM in CI/CD Pipeline:**
```yaml
# GitHub Actions example
name: Build with SBOM

jobs:
  build:
    steps:
      - name: Build image with SBOM
        run: |
          docker buildx build \
            --sbom=true \
            --provenance=true \
            --tag my-image:${{ github.sha }} \
            --push \
            .

      - name: Generate SBOM with Syft
        run: |
          syft my-image:${{ github.sha }} -o spdx-json > sbom.json

      - name: Upload SBOM artifact
        uses: actions/upload-artifact@v3
        with:
          name: sbom
          path: sbom.json

      - name: Scan SBOM for vulnerabilities
        run: |
          grype sbom:sbom.json --fail-on high
```

**SBOM Best Practices:**

1. **Generate for every image:**
   - Production images: mandatory
   - Development images: recommended
   - Base images: critical

2. **Store SBOMs with provenance:**
   - Version control alongside Dockerfile
   - Artifact registry with image
   - Dedicated SBOM repository

3. **Automate SBOM generation:**
   - Integrate into CI/CD pipeline
   - Generate on every build
   - Fail builds if SBOM generation fails

4. **Use SBOM for vulnerability management:**
```bash
# Scan SBOM instead of image (faster)
grype sbom:sbom.json
trivy sbom sbom.json

# Compare SBOMs between versions
diff <(syft old-image:1.0 -o json) <(syft new-image:2.0 -o json)
```

5. **SBOM formats:**
   - **SPDX:** Industry standard, ISO/IEC 5962:2021
   - **CycloneDX:** OWASP standard, security-focused
   - Choose based on compliance requirements

**Chainguard Images with Built-in SBOM:**
```bash
# Chainguard images include SBOM attestation by default
docker buildx imagetools inspect cgr.dev/chainguard/node:latest

# Extract SBOM
cosign download sbom cgr.dev/chainguard/node:latest > chainguard-node-sbom.json
```

**Or use multi-stage and don't include secrets:**
```dockerfile
FROM node AS builder
ARG NPM_TOKEN
RUN echo "//registry.npmjs.org/:_authToken=${NPM_TOKEN}" > .npmrc && \
    npm install && \
    rm .npmrc  # Still in layer history!

# Better - secret only in build stage
FROM node AS dependencies
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm install

FROM node AS runtime
COPY --from=dependencies /app/node_modules ./node_modules
# No .npmrc in final image
```

### Secure Build Context

**Threat:** Sensitive files included in build context

**Mitigation:**
Create comprehensive `.dockerignore`:
```
# Secrets
.env
.env.local
*.key
*.pem
credentials.json
secrets/

# Version control
.git
.gitignore

# Cloud credentials
.aws/
.gcloud/

# Private data
database.sql
backups/

# SSH keys
.ssh/
id_rsa
id_rsa.pub

# Sensitive logs
*.log
logs/
```

### Image Signing

**Enable Docker Content Trust:**
```bash
# Enable image signing
export DOCKER_CONTENT_TRUST=1

# Set up keys
docker trust key generate my-key
docker trust signer add --key my-key.pub my-name my-image

# Push signed image
docker push my-image:tag

# Pull only signed images
docker pull my-image:tag  # Fails if not signed
```

## Runtime Security

### User Privileges

**Threat:** Container escape via root

**Mitigation:**
```dockerfile
# Create and use non-root user
FROM node:20-alpine
RUN addgroup -g 1001 appuser && \
    adduser -S appuser -u 1001 -G appuser
USER appuser
WORKDIR /home/appuser/app
COPY --chown=appuser:appuser . .
CMD ["node", "server.js"]
```

**Verification:**
```bash
# Check user in running container
docker exec container-name whoami  # Should not be root
docker exec container-name id       # Check UID/GID
```

### Capabilities

**Threat:** Excessive kernel capabilities

**Default Docker capabilities:**
- CHOWN, DAC_OVERRIDE, FOWNER, FSETID
- KILL, SETGID, SETUID, SETPCAP
- NET_BIND_SERVICE, NET_RAW
- SYS_CHROOT, MKNOD, AUDIT_WRITE, SETFCAP

**Mitigation:**
```bash
# Drop all, add only needed
docker run \
  --cap-drop=ALL \
  --cap-add=NET_BIND_SERVICE \
  my-image
```

**In docker-compose.yml:**
```yaml
services:
  app:
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
```

**Common needed capabilities:**
- `NET_BIND_SERVICE`: Bind to ports < 1024
- `NET_ADMIN`: Network configuration
- `SYS_TIME`: Set system time

### Read-Only Filesystem

**Threat:** Container modification, malware persistence

**Mitigation:**
```bash
docker run \
  --read-only \
  --tmpfs /tmp:noexec,nosuid,size=64M \
  --tmpfs /var/run:noexec,nosuid,size=64M \
  my-image
```

**In Compose:**
```yaml
services:
  app:
    read_only: true
    tmpfs:
      - /tmp:noexec,nosuid,size=64M
      - /var/run:noexec,nosuid,size=64M
```

### Security Options

**no-new-privileges:**
```bash
docker run --security-opt="no-new-privileges:true" my-image
```

Prevents privilege escalation via setuid/setgid binaries.

**AppArmor (Linux):**
```bash
docker run --security-opt="apparmor=docker-default" my-image
```

**SELinux (Linux):**
```bash
docker run --security-opt="label=type:container_runtime_t" my-image
```

**Seccomp (syscall filtering):**
```bash
# Use default profile
docker run --security-opt="seccomp=default" my-image

# Or custom profile
docker run --security-opt="seccomp=./seccomp-profile.json" my-image
```

### Resource Limits

**Threat:** DoS via resource exhaustion

**Mitigation:**
```bash
docker run \
  --memory="512m" \
  --memory-swap="512m" \  # Disable swap
  --cpus="1.0" \
  --pids-limit=100 \
  --ulimit nofile=1024:1024 \
  my-image
```

**In Compose:**
```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
          pids: 100
        reservations:
          cpus: '0.5'
          memory: 256M
    ulimits:
      nofile:
        soft: 1024
        hard: 1024
```

### Comprehensive Secure Run Command

```bash
docker run \
  --name secure-app \
  --detach \
  --restart unless-stopped \
  --user 1000:1000 \
  --cap-drop=ALL \
  --cap-add=NET_BIND_SERVICE \
  --read-only \
  --tmpfs /tmp:noexec,nosuid,size=64M \
  --security-opt="no-new-privileges:true" \
  --security-opt="seccomp=default" \
  --memory="512m" \
  --cpus="1.0" \
  --pids-limit=100 \
  --network=isolated-network \
  --publish 127.0.0.1:8080:8080 \
  --volume secure-data:/data:ro \
  --health-cmd="curl -f http://localhost/health || exit 1" \
  --health-interval=30s \
  my-secure-image:1.2.3
```

## Network Security

### Network Isolation

**Threat:** Lateral movement between containers

**Mitigation:**
```yaml
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # No external access

services:
  web:
    networks:
      - frontend

  api:
    networks:
      - frontend
      - backend

  database:
    networks:
      - backend  # Isolated from frontend
```

### Port Exposure

**Threat:** Unnecessary network exposure

**Mitigation:**
```bash
# Bind to localhost only
docker run -p 127.0.0.1:8080:8080 my-image

# NOT (binds to all interfaces)
docker run -p 8080:8080 my-image
```

**In Compose:**
```yaml
services:
  app:
    ports:
      - "127.0.0.1:8080:8080"  # Localhost only
```

### Inter-Container Communication

```yaml
# Disable default inter-container communication
# /etc/docker/daemon.json
{
  "icc": false
}
```

Then explicitly allow via networks:
```yaml
services:
  app1:
    networks:
      - app-network
  app2:
    networks:
      - app-network  # Can communicate with app1

networks:
  app-network:
    driver: bridge
```

## Secrets Management

### Docker Secrets (Swarm Mode)

```bash
# Create secret
echo "mypassword" | docker secret create db_password -

# Use in service
docker service create \
  --name my-service \
  --secret db_password \
  my-image

# Access in container at /run/secrets/db_password
```

**In stack file:**
```yaml
version: '3.8'

services:
  app:
    image: my-image
    secrets:
      - db_password

secrets:
  db_password:
    external: true
```

### Secrets Best Practices

1. **Never in environment variables** (visible in `docker inspect`)
2. **Never in images** (in layer history)
3. **Never in version control** (Git history)
4. **Mount as files** with restricted permissions
5. **Use secret management systems** (Vault, AWS Secrets Manager, etc.)
6. **Rotate regularly**

**Alternative: Mounted secrets:**
```bash
docker run -v /secure/secrets:/run/secrets:ro my-image
```

## Compliance & Benchmarking

### CIS Docker Benchmark

Automated checking:
```bash
# Clone docker-bench-security
git clone https://github.com/docker/docker-bench-security.git
cd docker-bench-security
sudo sh docker-bench-security.sh

# Or run as container
docker run --rm --net host --pid host --userns host \
  --cap-add audit_control \
  -v /var/lib:/var/lib:ro \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /usr/lib/systemd:/usr/lib/systemd:ro \
  -v /etc:/etc:ro \
  docker/docker-bench-security
```

### Key CIS Recommendations

1. **Host Configuration**
   - Keep Docker up to date
   - Restrict network traffic between containers
   - Set logging level to 'info'
   - Enable Docker Content Trust

2. **Docker Daemon**
   - Use TLS for Docker daemon socket
   - Don't expose daemon on TCP without TLS
   - Enable user namespace support

3. **Docker Files**
   - Verify Docker files ownership and permissions
   - Audit Docker files and directories

4. **Container Images**
   - Create user for container
   - Use trusted base images
   - Don't install unnecessary packages

5. **Container Runtime**
   - Run containers with limited privileges
   - Set resource limits
   - Don't share host network namespace

## Monitoring & Detection

### Logging

```yaml
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
        labels: "service,env"
        env: "ENV,VERSION"
```

**Centralized logging:**
```yaml
services:
  app:
    logging:
      driver: "syslog"
      options:
        syslog-address: "tcp://log-server:514"
        tag: "{{.Name}}/{{.ID}}"
```

### Runtime Monitoring

**Tools:**
- Falco: Runtime security monitoring
- Sysdig: Container visibility
- Prometheus + cAdvisor: Metrics
- Docker events: Real-time events

**Monitor for:**
- Unexpected processes
- File modifications
- Network connections
- Resource spikes
- Failed authentication
- Privilege escalation attempts

```bash
# Monitor Docker events
docker events --filter 'type=container' --filter 'event=start'

# Watch specific container
docker events --filter "container=my-container"

# Runtime security with Falco
docker run --rm -it \
  --privileged \
  -v /var/run/docker.sock:/host/var/run/docker.sock \
  -v /dev:/host/dev \
  -v /proc:/host/proc:ro \
  falcosecurity/falco
```

## Platform-Specific Security

### Linux

**User namespace remapping:**
```json
// /etc/docker/daemon.json
{
  "userns-remap": "default"
}
```

Benefits: Root in container → unprivileged on host

**SELinux:**
```bash
# Enable SELinux for Docker
setenforce 1

# Run with SELinux labels
docker run --security-opt label=type:svirt_sandbox_file_t my-image

# Volumes with SELinux
docker run -v /host/path:/container/path:z my-image
```

**AppArmor:**
```bash
# Check AppArmor status
aa-status

# Run with AppArmor profile
docker run --security-opt apparmor=docker-default my-image
```

### Windows

**Hyper-V isolation:**
```powershell
# More isolated than process isolation
docker run --isolation=hyperv my-image
```

**Windows Defender:**
- Ensure real-time protection enabled
- Configure exclusions carefully
- Scan images regularly

### macOS

**Docker Desktop security:**
- Keep Docker Desktop updated
- Enable "Use gRPC FUSE for file sharing"
- Limit file sharing to necessary paths
- Review resource allocation

## Security Checklist

**Image:**
- [ ] Based on official, minimal image
- [ ] Specific version tag (not `latest`)
- [ ] Scanned for vulnerabilities
- [ ] No secrets in layers
- [ ] Runs as non-root user
- [ ] Signed (Content Trust)

**Build:**
- [ ] .dockerignore configured
- [ ] Multi-stage build (if applicable)
- [ ] Build secrets handled properly
- [ ] Build from trusted sources only

**Runtime:**
- [ ] Non-root user
- [ ] Capabilities dropped
- [ ] Read-only filesystem (where possible)
- [ ] Security options set
- [ ] Resource limits configured
- [ ] Isolated network
- [ ] Minimal port exposure
- [ ] Secrets mounted securely

**Operations:**
- [ ] CIS benchmark compliance
- [ ] Logging configured
- [ ] Monitoring in place
- [ ] Regular vulnerability scans
- [ ] Incident response plan
- [ ] Regular updates
- [ ] Audit logs enabled

## Common Security Mistakes

❌ **NEVER:**
- Run as root
- Use `--privileged`
- Mount Docker socket (`/var/run/docker.sock`)
- Hardcode secrets
- Use `latest` tag
- Skip vulnerability scanning
- Expose unnecessary ports
- Disable security features
- Ignore security updates
- Trust unverified images

✅ **ALWAYS:**
- Run as non-root
- Drop capabilities
- Scan for vulnerabilities
- Use secrets management
- Tag with specific versions
- Enable security options
- Apply least privilege
- Keep systems updated
- Monitor runtime behavior
- Use official images

This security guide represents current best practices. Security threats evolve constantly—always check the latest Docker security documentation and CVE databases.
