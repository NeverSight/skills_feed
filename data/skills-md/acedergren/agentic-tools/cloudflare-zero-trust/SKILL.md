---
name: cloudflare-zero-trust
description: Use when working with Cloudflare Tunnel or Access - tunnel setup, authentication configuration, 502 Bad Gateway errors, Docker/Kubernetes deployment, service token management, private network routing (SSH/RDP/databases), WebSocket/gRPC connection issues, replica scaling problems, WARP routing, Terraform/IaC automation, local development with quick tunnels, audit logging setup, compliance requirements (SOC2/HIPAA), or advanced network debugging. Keywords - cloudflared, 502 error, service tokens, terraform, metrics port 20241, trycloudflare, Logpush, SIEM. CRITICAL - Authentication mandatory not optional.
---

# Cloudflare Zero Trust

## Overview

Cloudflare Zero Trust provides secure remote access to applications without VPN, using Cloudflare Tunnel (secure connectivity) and Cloudflare Access (authentication/authorization).

**Core principle:** Authentication is not optional. Every tunnel must have access controls from day one.

## When to Use

Use this skill when:
- Setting up Cloudflare Tunnel for any application
- Configuring Cloudflare Access authentication
- Exposing internal applications securely
- Replacing VPN access with zero-trust model
- Integrating OIDC/SSO providers (Azure AD, Okta, Google)
- Running cloudflared in Docker containers
- Troubleshooting 502 Bad Gateway errors
- Managing tunnels via dashboard or CLI

**Symptoms that trigger this skill:**
- "Need to expose local app to internet"
- "Setting up Cloudflare Tunnel"
- "Add authentication to tunnel"
- "Configure Azure AD / Okta / OIDC"
- "502 Bad Gateway on Cloudflare Tunnel"
- "Run cloudflared in Docker"

## Security-First Principle

```
UNAUTHENTICATED TUNNEL = PUBLICLY EXPOSED SERVICE = SECURITY INCIDENT
```

**Authentication is mandatory, not optional.**

If you find yourself thinking:
- "We'll add authentication later"
- "It's been working fine without auth"
- "Don't want to disrupt users with login"
- "Can we skip auth for internal apps?"
- "Demo first, secure later"

**STOP. These are security violations.**

Correct mindset:
- Tunnel without auth = exposed service = critical vulnerability
- User convenience < security requirement
- "Internal only" is not a security control
- Demos should be secure by default

## Quick Reference

| Task | Remotely-Managed (Dashboard) | Locally-Managed (config.yml) |
|------|------------------------------|------------------------------|
| **Best for** | GUI users, quick setup, team collaboration | IaC, automation, version control, CI/CD |
| **Setup** | Dashboard → Create Tunnel → Configure routes | `cloudflared tunnel create` + config.yml |
| **Changes** | Click to update | Edit config, restart service |
| **Access Control** | Always via dashboard (Zero Trust → Access) | Tunnel via config, Access via dashboard |
| **Docker** | Env vars for credentials | Mount config.yml + credentials JSON |

## Tunnel Setup Workflow

**BEFORE creating tunnel, choose management approach** using the decision tree in "Dashboard vs CLI Decision Tree" section below.

```dot
digraph tunnel_setup {
    rankdir=TD;
    node [shape=box, style=rounded];

    start [label="Need to expose app", shape=ellipse];
    requirements [label="Define requirements\n• Who needs access?\n• Auth provider?\n• Docker or host?"];
    choose_method [label="Choose management", shape=diamond];

    dashboard [label="Dashboard Method\n1. Create tunnel\n2. Install cloudflared\n3. Run connector"];
    config [label="Config File Method\n1. cloudflared tunnel create\n2. Write config.yml\n3. Start service"];

    access [label="Configure Access\nBEFORE going live", style="filled", fillcolor="#ffcccc"];
    test [label="Test authentication"];
    deploy [label="Enable for users"];
    monitor [label="Monitor logs"];

    start -> requirements;
    requirements -> choose_method;
    choose_method -> dashboard [label="GUI\nQuick start"];
    choose_method -> config [label="IaC\nAutomation"];
    dashboard -> access;
    config -> access;
    access -> test;
    test -> deploy;
    deploy -> monitor;
}
```

**Critical:** Configure Access authentication BEFORE exposing the tunnel. Never deploy unauthenticated tunnels, even "temporarily."

## Remotely-Managed Tunnels (Dashboard)

**When to use:**
- Team prefers GUI
- Quick proof-of-concept (that still needs auth!)
- Visual route management
- Less technical team members

**Setup:**
1. **Zero Trust → Networks → Tunnels → Create**
2. **Choose connector type:** Cloudflared
3. **Name tunnel:** e.g., `prod-api-tunnel`
4. **Install cloudflared** on origin server
5. **Run connector:** Copy token from dashboard
   ```bash
   cloudflared service install <TOKEN>
   ```
6. **Configure routes:** Dashboard → Public Hostname
   - Hostname: `api.example.com`
   - Service: `http://localhost:8080`
7. **Configure Access** (see Access Configuration section)

**Advantages:**
- Visual configuration
- Easy for team members
- Built-in health monitoring

**Disadvantages:**
- Not in version control
- Harder to automate
- Must use dashboard for changes

## Locally-Managed Tunnels (config.yml)

**When to use:**
- Infrastructure as code
- CI/CD automation
- Version control for config
- Multiple environments (dev/staging/prod)
- Docker containers

**Setup:**

1. **Create tunnel:**
   ```bash
   cloudflared tunnel create myapp-tunnel
   ```
   Outputs: `~/.cloudflared/<TUNNEL_ID>.json` (credentials)

2. **Create config file** (`~/.cloudflared/config.yml`):
   ```yaml
   # === REQUIRED FIELDS (tunnel breaks without these) ===
   tunnel: <TUNNEL_ID>
   credentials-file: /etc/cloudflared/<TUNNEL_ID>.json

   ingress:
     # Route myapp.example.com to local service
     - hostname: myapp.example.com
       service: http://localhost:8080  # REQUIRED: origin URL
       originRequest:
         # === DANGEROUS (wrong value = security risk or outage) ===
         noTLSVerify: false  # NEVER set true without specific reason (security risk)

         # === SAFE (tune based on your needs) ===
         connectTimeout: 30s
         httpHostHeader: myapp.example.com

     # Multiple services example
     - hostname: api.example.com
       service: http://localhost:8080
     - hostname: admin.example.com
       service: http://localhost:3000

     # REQUIRED: Catch-all rule (must be last)
     - service: http_status:404

   # === SAFE (change freely) ===
   loglevel: info  # or: debug, warn, error
   ```

3. **Route DNS:**
   ```bash
   cloudflared tunnel route dns myapp-tunnel myapp.example.com
   ```

4. **Run tunnel:**
   ```bash
   # Foreground (testing)
   cloudflared tunnel run myapp-tunnel

   # As service (production)
   sudo cloudflared service install
   sudo systemctl start cloudflared
   sudo systemctl enable cloudflared
   ```

5. **Configure Access** (see next section)

**Advantages:**
- Version controlled
- Easy automation
- Consistent across environments
- Docker-friendly

**Disadvantages:**
- Requires editing config files
- Restart needed for changes
- More initial setup

## Modern Protocols (WebSockets, HTTP/2, gRPC)

## Modern Protocols (WebSockets, HTTP/2, gRPC)

**MANDATORY when working with WebSockets, HTTP/2, or gRPC:**
Load [`protocols.md`](references/protocols.md) for complete protocol configuration, tuning parameters, and troubleshooting.

**Quick reference:**
- WebSockets: `keepAliveTimeout: 300s` for stable connections
- HTTP/2: Requires TLS origin with `http2Origin: true`
- gRPC: Use WARP routing (not public hostname)

**Do NOT load** for basic HTTP tunnel setup.


**When to use:**
- Containerized infrastructure
- Docker Compose environments
- Kubernetes/orchestration
- Portable deployments

### Container-Specific Patterns

**Critical networking difference (Docker/Kubernetes):**

```yaml
# ❌ WRONG - localhost doesn't resolve in containers
ingress:
  - hostname: myapp.example.com
    service: http://localhost:8080

# ✅ RIGHT - use service/pod name
# Docker Compose:
    service: http://myapp:8080  # Container name from docker-compose.yml

# Kubernetes:
    service: http://myapp-service:8080  # Service name
```

**Credential mounting patterns:**

```yaml
# Docker Compose:
volumes:
  - ./cloudflared/config.yml:/etc/cloudflared/config.yml:ro  # Read-only
  - ./cloudflared/credentials.json:/etc/cloudflared/credentials.json:ro

# Kubernetes:
# Use ConfigMap for config, Secret for credentials
```

**Health check setup:**

```yaml
# Docker Compose:
healthcheck:
  test: ["CMD", "cloudflared", "tunnel", "info"]
  interval: 30s
  timeout: 10s
  retries: 3

# Kubernetes:
livenessProbe:
  exec:
    command: ["cloudflared", "tunnel", "info"]
  initialDelaySeconds: 30
  periodSeconds: 30
```

**Redundancy for production:**

```yaml
# Docker Compose - use multiple instances behind load balancer
# Kubernetes - use replicas:
spec:
  replicas: 2  # Minimum 2 for zero-downtime updates
```

**Setup workflow:**

1. Create tunnel: `cloudflared tunnel create myapp-tunnel`
2. Get credentials: `~/.cloudflared/<TUNNEL_ID>.json`
3. Mount config + credentials in container
4. Set service URL to container/service name (NOT localhost)
5. Configure Access authentication
6. Deploy with health checks enabled

**Verification:**

```bash
# Docker Compose
docker-compose logs cloudflared
docker-compose exec cloudflared cloudflared tunnel info

# Kubernetes
kubectl logs -l app=cloudflared
kubectl exec deploy/cloudflared -- cloudflared tunnel info
```

## Private Network Routing (Non-HTTP Services)

## Private Network Routing (Non-HTTP Services)

**MANDATORY when exposing SSH, RDP, databases, or custom TCP/UDP protocols:**
Load [`private-networks.md`](references/private-networks.md) for complete private network configuration, WARP routing setup, container networking, and access policies.

**Quick reference:**
- SSH: `service: ssh://192.168.1.10:22`
- RDP: `service: rdp://192.168.1.20:3389`
- Database: `service: tcp://192.168.1.30:5432`
- Use service names in Docker: `tcp://database:5432` NOT `tcp://localhost:5432`

**Do NOT load** for HTTP application tunnels.


**Configure Access BEFORE exposing tunnel to users.**

### Self-Hosted Applications

1. **Zero Trust → Access → Applications → Add an application**

2. **Choose "Self-hosted"**

3. **Application Configuration:**
   - **Name:** `My Application`
   - **Session Duration:** `24 hours` (default)
   - **Application domain:** `myapp.example.com`
   - **Accept all available identity providers:** Checked (or select specific)

4. **Add policies** (at least one Allow policy required):

**Example policies:**

**Email-based:**
```
Name: Allow specific users
Action: Allow
Include: Emails → user1@example.com, user2@example.com
```

**Domain-based:**
```
Name: Allow company domain
Action: Allow
Include: Email domains → @company.com
```

**Group-based (requires IdP groups):**
```
Name: Allow admins group
Action: Allow
Include: Azure AD Groups → Admins
```

**Multi-factor authentication:**
```
Name: Require MFA for admins
Action: Allow
Include: Email domains → @company.com
Require: Authentication Method → mTLS, WARP, Service Token (select MFA method)
```

5. **Optional settings:**
   - **Purpose justification:** Require users to state reason for access
   - **Temporary authentication:** Approve access requests manually
   - **IdP groups:** Use groups from Azure AD, Okta, etc.

### SaaS Applications

For integrated SaaS apps (Salesforce, Workday, etc.):

1. **Zero Trust → Access → Applications → Add an application**
2. **Choose "SaaS"**
3. **Select application** from catalog
4. **Follow integration wizard** (varies by app)
5. **Configure policies** (same as self-hosted)

### OIDC / SSO Integration

#### Azure AD (Entra ID)

**Azure AD setup:**
1. **Azure Portal → Azure Active Directory → App registrations → New registration**
2. **Name:** `Cloudflare Access`
3. **Redirect URI:** `https://<your-team-name>.cloudflareaccess.com/cdn-cgi/access/callback`
4. **Register**, copy **Application (client) ID**
5. **Certificates & secrets → New client secret**, copy value
6. **API permissions → Add permission → Microsoft Graph → Group.Read.All** (for group-based policies)
7. **Token configuration → Add groups claim → Security groups**

**Cloudflare configuration:**
1. **Zero Trust → Settings → Authentication → Add new → Azure AD**
2. **Name:** `Azure AD`
3. **App ID:** `<Application (client) ID>`
4. **Client secret:** `<Secret value>`
5. **Directory (tenant) ID:** From Azure AD overview
6. **Support groups:** Checked (if using group-based policies)
7. **Test** and **Save**

**Use in policies:**
```
Name: Allow Admins group
Action: Allow
Include: Azure AD Groups → select "Admins" group
```

#### Okta

1. **Okta Admin → Applications → Create App Integration → OIDC - Web Application**
2. **Name:** `Cloudflare Access`
3. **Grant type:** Authorization Code
4. **Sign-in redirect URI:** `https://<team-name>.cloudflareaccess.com/cdn-cgi/access/callback`
5. **Assignments:** Select groups
6. Copy **Client ID** and **Client secret**

**Cloudflare:**
1. **Zero Trust → Settings → Authentication → Add new → Okta**
2. **Okta account URL:** `https://your-domain.okta.com`
3. **App ID** and **Client secret**
4. **Support groups:** Checked
5. **Test** and **Save**

#### Generic OIDC Provider

For providers not in catalog:

1. **Zero Trust → Settings → Authentication → Add new → OpenID Connect**
2. **Name:** Provider name
3. **App ID (Client ID)**
4. **Client Secret**
5. **Auth URL:** `https://provider.com/oauth2/authorize`
6. **Token URL:** `https://provider.com/oauth2/token`
7. **Certificate URL (JWKS):** `https://provider.com/.well-known/jwks.json`
8. **Proof Key for Code Exchange (PKCE):** Checked if supported
9. **Support groups:** If provider supports groups claim
10. **Test** and **Save**

### Access Policy Design

**Principle: Least privilege by default.**

**Policy evaluation order:**
1. Bypass policies (skip authentication)
2. Block policies (explicit deny)
3. Allow policies (grant access)
4. Service Auth (API tokens, service-to-service)

**Good policy patterns:**

**Production application with role-based access:**
```
Policy 1: Block non-employees
  Action: Block
  Include: Everyone
  Exclude: Email domains → @company.com

Policy 2: Allow developers
  Action: Allow
  Include: Azure AD Groups → Developers

Policy 3: Allow admins
  Action: Allow
  Include: Azure AD Groups → Admins
  Require: MFA
```

**Staging environment:**
```
Policy 1: Allow dev team
  Action: Allow
  Include: Email domains → @company.com
  Require: Azure AD Groups → Developers OR Admins
```

**API with service authentication:**
```
Policy 1: Service-to-service
  Action: Service Auth
  Include: Service Token → api-service-token
```

## Service Authentication (M2M / API Access)

## Service Authentication (M2M / API Access)

**MANDATORY when configuring CI/CD pipelines, microservices, or any non-human authentication:**
Load [`service-auth.md`](references/service-auth.md) for service token creation, rotation workflows, security best practices, and M2M patterns.

**Quick reference:**
- Create token: Zero Trust → Access → Service Auth
- Use headers: `CF-Access-Client-Id`, `CF-Access-Client-Secret`
- Rotate every 90 days
- Store in secrets manager, never in code

**Do NOT load** for user authentication (use SSO/OIDC instead).


### 502 Bad Gateway

**Error:** `502 Bad Gateway - Unable to reach the origin service`

**Meaning:** Tunnel is connected to Cloudflare, but can't reach your origin.

**Systematic diagnosis:**

```dot
digraph troubleshoot_502 {
    rankdir=TD;
    node [shape=box, style=rounded];

    start [label="502 Bad Gateway", shape=ellipse, style=filled, fillcolor="#ffcccc"];
    check_origin [label="Can you curl origin\nlocally?", shape=diamond];
    origin_down [label="Origin service down\nRestart service", style=filled, fillcolor="#ffcccc"];
    check_docker [label="Is cloudflared\nin Docker?", shape=diamond];
    wrong_service [label="Using localhost?\nChange to container name:\nhttp://myapp:8080", style=filled, fillcolor="#ccffcc"];
    check_tls [label="Origin uses\nHTTPS?", shape=diamond];
    tls_issue [label="Self-signed cert?\nSet noTLSVerify: true\nOR add caPool", style=filled, fillcolor="#ccffcc"];
    check_port [label="Port correct\nin config?", shape=diamond];
    wrong_port [label="Fix port number\nin config.yml", style=filled, fillcolor="#ccffcc"];
    firewall [label="Check firewall\nrules/logs", style=filled, fillcolor="#ffffcc"];

    start -> check_origin;
    check_origin -> origin_down [label="No"];
    check_origin -> check_docker [label="Yes"];
    check_docker -> wrong_service [label="Yes"];
    check_docker -> check_tls [label="No"];
    check_tls -> tls_issue [label="Yes"];
    check_tls -> check_port [label="No"];
    check_port -> wrong_port [label="No"];
    check_port -> firewall [label="Yes"];
}
```

**Quick diagnostic commands:**

```bash
# 1. Test origin locally
curl -v http://localhost:8080
# Success? Continue. Connection refused? Origin is down.

# 2. Check cloudflared logs
sudo journalctl -u cloudflared -n 50 --no-pager  # Systemd
docker logs cloudflared  # Docker
# Look for: "dial tcp", "connection refused", "context deadline exceeded"

# 3. Test from cloudflared container (if Docker)
docker exec cloudflared curl http://myapp:8080
# Fails? Wrong service name or network issue

# 4. Run tunnel in foreground (see real-time errors)
sudo systemctl stop cloudflared
cloudflared tunnel run myapp-tunnel
```

### Authentication Loop (Redirect Loop)

**Symptom:** Browser keeps redirecting to login, never reaches app

**Systematic diagnosis:**

```dot
digraph troubleshoot_auth_loop {
    rankdir=TD;
    node [shape=box, style=rounded];

    start [label="Authentication Loop", shape=ellipse, style=filled, fillcolor="#ffcccc"];
    check_policy [label="Does an Allow policy\nmatch your user?", shape=diamond];
    policy_issue [label="Add/update Allow policy\nCheck email/groups match", style=filled, fillcolor="#ccffcc"];
    check_idp [label="IdP redirect URI\nmatches Cloudflare?", shape=diamond];
    idp_issue [label="Fix redirect URI:\nhttps://<team>.cloudflareaccess.com\n/cdn-cgi/access/callback", style=filled, fillcolor="#ccffcc"];
    check_groups [label="Using group-based\npolicies?", shape=diamond];
    groups_issue [label="Verify IdP sends group claims\nCheck 'Support groups' enabled", style=filled, fillcolor="#ccffcc"];
    check_cookies [label="Try incognito mode\nClear all cookies", shape=diamond];
    cookie_issue [label="Browser blocking 3rd-party\ncookies or privacy mode active", style=filled, fillcolor="#ffffcc"];
    check_session [label="Session duration\nadequate?", shape=diamond];
    session_issue [label="Increase session duration\nDefault 24h may be too short", style=filled, fillcolor="#ccffcc"];
    escalate [label="Check Cloudflare Access logs\nfor specific error", style=filled, fillcolor="#ffffcc"];

    start -> check_policy;
    check_policy -> policy_issue [label="No"];
    check_policy -> check_idp [label="Yes"];
    check_idp -> idp_issue [label="No"];
    check_idp -> check_groups [label="Yes"];
    check_groups -> groups_issue [label="Yes"];
    check_groups -> check_cookies [label="No"];
    check_cookies -> cookie_issue [label="Still loops"];
    check_cookies -> check_session [label="Works in\nincognito"];
    check_session -> session_issue [label="No"];
    check_session -> escalate [label="Yes"];
}
```

**Quick diagnostic steps:**

```bash
# 1. Verify Access policy matches you
# Dashboard → Zero Trust → Access → Applications → <Your App> → Policies
# Check: Does an Allow policy include your email/domain/group?

# 2. Test in incognito window (eliminates cookie issues)
# If works in incognito → Clear cookies
# If still loops → Policy or IdP issue

# 3. Check IdP redirect URI
# Must exactly match: https://<your-team-name>.cloudflareaccess.com/cdn-cgi/access/callback

# 4. Verify group claims (if using group-based policies)
# Azure AD: Token configuration → Add groups claim
# Okta: Profile → Edit → Include in token
# Cloudflare: Settings → Authentication → <IdP> → Support groups ✓

# 5. Check Access logs for specific error
# Dashboard → Zero Trust → Logs → Access
# Look for: policy evaluation failures, IdP errors
```

### Tunnel Not Connecting

**Symptom:** Tunnel shows "Inactive" or "Down" in dashboard

**Troubleshooting:**

1. **Check cloudflared is running:**
   ```bash
   sudo systemctl status cloudflared  # or: docker ps | grep cloudflared
   ```

2. **Verify credentials file exists:**
   ```bash
   ls -la ~/.cloudflared/<TUNNEL_ID>.json
   ```

3. **Firewall requirement:** Cloudflared needs outbound HTTPS (443) to `*.argotunnel.com`

4. **Restart tunnel:**
   ```bash
   sudo systemctl restart cloudflared
   ```

### DNS Not Resolving

**Symptom:** `nslookup myapp.example.com` returns no records

**Fix:**

1. **Check DNS record exists:**
   - Cloudflare dashboard → DNS → Records
   - Look for CNAME: `myapp.example.com` → `<TUNNEL_ID>.cfargotunnel.com`

2. **Create if missing:**
   ```bash
   cloudflared tunnel route dns myapp-tunnel myapp.example.com
   ```

3. **Verify:** DNS record should be "Proxied" (orange cloud) in Cloudflare dashboard

## Common Mistakes

## Advanced Troubleshooting

**MANDATORY when basic troubleshooting fails or for performance debugging:**
Load [`advanced-troubleshooting.md`](references/advanced-troubleshooting.md) for network path analysis, performance tuning, certificate debugging, connection limits, and metrics interpretation.

**Quick reference:**
- Metrics ports: 20241-20245 (auto-selected)
- Connection limits: 4 per instance, 100 total (25 replicas max)
- Default keepAliveConnections: 100

**Do NOT load** for simple 502 or DNS issues.


### 1. Deploying Without Authentication

**❌ Wrong:**
```bash
# Create tunnel
cloudflared tunnel create myapp
# Route DNS
cloudflared tunnel route dns myapp myapp.example.com
# Run tunnel
cloudflared tunnel run myapp
# ⚠️ APP IS NOW PUBLICLY ACCESSIBLE
```

**✅ Right:**
```bash
# Create tunnel
cloudflared tunnel create myapp
# Route DNS
cloudflared tunnel route dns myapp myapp.example.com
# Configure Access FIRST (dashboard)
# THEN run tunnel
cloudflared tunnel run myapp
```

### 2. Using `noTLSVerify: true` Without Reason

**❌ Wrong:**
```yaml
originRequest:
  noTLSVerify: true  # "Just in case"
```

**✅ Right:**
```yaml
# Only if origin uses self-signed cert
originRequest:
  noTLSVerify: false  # Verify by default
  # OR if self-signed:
  # noTLSVerify: true
  # caPool: /path/to/custom-ca.pem
```

### 3. Wrong Service URL in Docker

**❌ Wrong:**
```yaml
# config.yml
ingress:
  - hostname: app.example.com
    service: http://localhost:8080  # Won't work in Docker!
```

**✅ Right:**
```yaml
# config.yml
ingress:
  - hostname: app.example.com
    service: http://myapp:8080  # Use container name
```

### 4. Bypass Policy for "Internal" Apps

**❌ Wrong:**
```
Policy: Skip auth for internal
Action: Bypass
Include: Everyone
# ⚠️ Anyone with URL can access!
```

**✅ Right:**
```
Policy: Allow employees
Action: Allow
Include: Email domains → @company.com
```

### 5. Hardcoding Credentials in Config

**❌ Wrong:**
```yaml
# config.yml checked into git
tunnel: abc123-def456-...
credentials-file: /etc/cloudflared/credentials.json
# ⚠️ credentials.json also in git!
```

**✅ Right:**
```bash
# .gitignore
*.json
credentials.json
```

Use environment-specific credentials, never commit.

## Dashboard vs CLI Decision Tree

```dot
digraph decision {
    rankdir=TD;
    node [shape=box, style=rounded];

    start [label="Need tunnel", shape=ellipse];
    team [label="Team has IaC\nexperience?", shape=diamond];
    automation [label="Need automation\nor CI/CD?", shape=diamond];
    multi_env [label="Multiple\nenvironments?", shape=diamond];

    cli [label="Use config.yml\n(Locally-managed)", style="filled", fillcolor="#ccffcc"];
    dashboard [label="Use Dashboard\n(Remotely-managed)", style="filled", fillcolor="#ccccff"];

    start -> team;
    team -> automation [label="Yes"];
    team -> dashboard [label="No"];
    automation -> cli [label="Yes"];
    automation -> multi_env [label="No"];
    multi_env -> cli [label="Yes"];
    multi_env -> dashboard [label="No"];
}
```

## Browser Automation (Dashboard Management)

**Note:** Browser automation for dashboard management requires MCP claude-in-chrome tools.

**Use cases:**
- Automated tunnel creation via dashboard
- Bulk configuration changes
- Scheduled tunnel audits
- Programmatic route updates

**Pattern:**
```typescript
// Pseudocode - requires claude-in-chrome MCP
const { navigate, click, fill } = mcp_claude_in_chrome;

// Navigate to Zero Trust dashboard
await navigate('https://one.dash.cloudflare.com/');

// Login flow (use saved session or credentials)
// ...

// Create tunnel
await navigate('Networks/Tunnels');
await click('Create a tunnel');
await fill('Tunnel name', 'new-tunnel');
await click('Save tunnel');

// Configure route
await click('Public Hostname');
await fill('Subdomain', 'myapp');
await fill('Domain', 'example.com');
await fill('Service', 'http://localhost:8080');
await click('Save');
```

**Better alternative: Use Cloudflare API**

```bash
# Get tunnels
curl -X GET "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/cfd_tunnel" \
  -H "Authorization: Bearer ${API_TOKEN}"

# Create tunnel
curl -X POST "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/cfd_tunnel" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{
    "name": "new-tunnel",
    "tunnel_secret": "<base64-secret>"
  }'

# Update config
curl -X PUT \
  "https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/cfd_tunnel/${TUNNEL_ID}/configurations" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{
    "config": {
      "ingress": [
        {
          "hostname": "myapp.example.com",
          "service": "http://localhost:8080"
        },
        {
          "service": "http_status:404"
        }
      ]
    }
  }'
```

**When to use browser automation vs API:**
- **API:** Preferred for automation, CI/CD, scripts
- **Browser:** When API doesn't support feature, visual verification needed


## API Automation

**MANDATORY when automating via Cloudflare API, CI/CD pipelines, or GitOps:**
Load [`api-automation.md`](references/api-automation.md) for complete API reference including Access applications, policies, tunnel management, service tokens, IdP configuration, device posture, and analytics.

**Quick reference:**
- Base URL: `https://api.cloudflare.com/client/v4/`
- Auth: `Authorization: Bearer ${API_TOKEN}`
- Rate limit: 1200 requests per 5 minutes
- All tunnel config updates apply immediately (no restart)

**Do NOT load** if using dashboard or Terraform (use terraform.md instead).


## Local Development Workflows

**MANDATORY when using quick tunnels, preview environments, or local dev setups:**
Load [`local-development.md`](references/local-development.md) for quick tunnel patterns (trycloudflare.com), preview environments, hot reload setups, and webhook testing.

**Quick reference:**
- Quick tunnel: `cloudflared tunnel --url http://localhost:8080`
- 200 concurrent request limit
- Random subdomain (changes each run)
- Free, no account needed

**Do NOT load** for production deployments.


## Terraform / Infrastructure as Code

**MANDATORY when managing Cloudflare with Terraform or other IaC tools:**
Load [`terraform.md`](references/terraform.md) for complete provider setup, resource examples, multi-environment patterns, state management, and deployment workflows.

**Quick reference:**
- Provider: `cloudflare/cloudflare` v4.0+
- Resources: `cloudflare_tunnel`, `cloudflare_access_application`, `cloudflare_access_policy`
- Use modules for reusability

**Do NOT load** for dashboard-based management.


## Audit Logging & Compliance

**MANDATORY for compliance requirements (SOC2, HIPAA, ISO 27001) or SIEM integration:**
Load [`audit-logging.md`](references/audit-logging.md) for Logpush configuration, SIEM patterns, compliance checklists, log retention, and alerting strategies.

**Quick reference:**
- Every auth attempt logged (user, app, IP, timestamp, decision)
- Logpush to S3, Splunk, Datadog, custom SIEM
- Free: 24h retention, Paid: 6 months, Enterprise: 18 months

**Do NOT load** for basic tunnel setup.


Stop and reconsider if you find yourself:

- ✋ Creating tunnel without Access configuration
- ✋ Using Bypass policy for "internal" applications
- ✋ Accepting "we'll add auth later" as valid approach
- ✋ Prioritizing demo speed over security
- ✋ Setting `noTLSVerify: true` without specific reason
- ✋ Storing credentials in version control
- ✋ Exposing admin interfaces without MFA requirement
- ✋ Using "it's been working without auth" as argument

**All of these are security incidents, not acceptable tradeoffs.**

## Command Quick Reference

```bash
# Create tunnel
cloudflared tunnel create <NAME>

# List tunnels
cloudflared tunnel list

# Run tunnel (foreground)
cloudflared tunnel run <NAME>

# Route DNS
cloudflared tunnel route dns <NAME> <HOSTNAME>

# Install as service
sudo cloudflared service install

# Service management
sudo systemctl start cloudflared
sudo systemctl stop cloudflared
sudo systemctl restart cloudflared
sudo systemctl status cloudflared

# Check logs
sudo journalctl -u cloudflared -f

# Tunnel info
cloudflared tunnel info <NAME>

# Delete tunnel
cloudflared tunnel delete <NAME>

# Update cloudflared
# macOS
brew upgrade cloudflare/cloudflare/cloudflared
# Linux
wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb
```

## Sources

This skill is based on:
- [Cloudflare Tunnel Documentation](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/)
- [Cloudflare Access Documentation](https://developers.cloudflare.com/cloudflare-one/policies/access/)
- [Designing ZTNA Access Policies](https://developers.cloudflare.com/reference-architecture/design-guides/designing-ztna-access-policies/)
- Community troubleshooting patterns from January 2026
