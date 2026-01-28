---
name: apisix-adc
description: Use ADC (APISIX Declarative CLI) to manage all Apache APISIX resources. Trigger when user mentions "APISIX", "manage APISIX", "configure APISIX", "APISIX route", "APISIX service", "APISIX upstream", "APISIX consumer", "APISIX plugin", "APISIX SSL", "APISIX gateway", "global rules", "install adc", "adc ping", "adc sync", "adc diff", "adc dump", "adc lint", "create route", "add consumer", "configure upstream", "rate limiting", "API authentication", "API gateway", or any APISIX/ADC configuration task.
---

# ADC - APISIX Declarative CLI

ADC (APISIX Declarative CLI) is the official tool to manage **all** Apache APISIX resources declaratively via YAML configuration files.

**Managed Resources:**

- **Services** - Group routes with shared upstream configuration
- **Routes** - Request matching and forwarding rules
- **Upstreams** - Backend service definitions with load balancing
- **Consumers** - API users with authentication credentials
- **Plugins** - Authentication, rate limiting, transformation, observability
- **Global Rules** - Plugins applied to all requests
- **SSL Certificates** - HTTPS configuration
- **Plugin Configs** - Reusable plugin configurations

## Quick Start Example

Here's a minimal working example to proxy requests:

```yaml
services:
  - name: my-backend
    upstream:
      type: roundrobin
      nodes:
        - host: backend.example.com
          port: 8080
          weight: 1
    routes:
      - name: api-route
        uris:
          - /api/*
        methods:
          - GET
          - POST
```

**Key points**:

- ONLY use top-level keys: `services`, `consumers`, `global_rules`, `ssls`, `plugin_configs`
- DO NOT add `name`, `version`, or other fields at the root level
- Each service must have: `name`, `upstream`, and `routes`

## Guided Workflow

When working with APISIX, follow this workflow:

### Step 1: Ensure ADC is Installed

Check if ADC is installed:

```bash
which adc || adc --version
```

If not installed, install it:

```bash
curl -sL "https://run.api7.ai/adc/install" | sh
```

### Step 2: Configure Connection

Create or update `.env` file in the working directory with connection details:

```bash
ADC_SERVER=http://localhost:9180
ADC_TOKEN=edd1c9f034335f136f87ad84b625c8f1
```

**Note**: These are the default APISIX Admin API settings. If the user has custom settings, ask them for:

- **Server URL**: Their APISIX Admin API endpoint
- **Admin API Key**: Their custom admin key

Export environment variables and verify connection:

```bash
export ADC_SERVER=http://localhost:9180
export ADC_TOKEN=edd1c9f034335f136f87ad84b625c8f1
adc ping
```

If connection fails, help user troubleshoot:

- Check if APISIX is running: `docker ps` or `systemctl status apisix`
- Verify the server URL and port (Admin API default: 9180)
- Confirm the Admin API key matches their APISIX configuration
- Check network connectivity: `curl http://localhost:9180/apisix/admin/routes`

### Step 3: Maintain Configuration File

Maintain an `adc.yaml` file based on user descriptions. The configuration file location should be in the current working directory or a location specified by the user.

When user describes their API requirements:

1. Create or update `adc.yaml` with the appropriate configuration
2. Use the schema from `references/configuration-schema.md` for correct YAML structure
3. Validate the configuration:

**IMPORTANT**: Always export environment variables before running `adc lint`:

```bash
export ADC_SERVER=http://localhost:9180
export ADC_TOKEN=edd1c9f034335f136f87ad84b625c8f1
adc lint -f adc.yaml
```

Or use the bundled validation script:

```bash
${CLAUDE_PLUGIN_ROOT}/skills/adc/scripts/validate-yaml.sh adc.yaml
```

**Translation guide for user descriptions:**

| User says                        | Create/Update                     |
| -------------------------------- | --------------------------------- |
| "I have a backend at host:port"  | Add upstream node                 |
| "Route /api/users to my backend" | Add route with uri                |
| "Add rate limiting"              | Add limit-count plugin            |
| "Require API key"                | Add key-auth plugin + consumer    |
| "Enable CORS"                    | Add cors plugin                   |
| "Add health check"               | Add upstream.checks configuration |

### Step 4: Preview and Sync

Before applying changes, always preview:

```bash
export ADC_SERVER=http://localhost:9180
export ADC_TOKEN=edd1c9f034335f136f87ad84b625c8f1
adc diff -f adc.yaml
```

Show the diff output to user and explain what will be created/updated/deleted.

Apply configuration to APISIX:

```bash
export ADC_SERVER=http://localhost:9180
export ADC_TOKEN=edd1c9f034335f136f87ad84b625c8f1
adc sync -f adc.yaml
```

### Step 5: Verify

After sync, optionally verify by dumping current config:

```bash
adc dump -o current.yaml
```

## Configuration Structure

ADC uses YAML format with these top-level resources:

```yaml
services:
  - name: my-service
    upstream:
      nodes:
        - host: backend.example.com
          port: 8080
          weight: 1
    routes:
      - name: my-route
        uris:
          - /api/*
        methods:
          - GET
          - POST
        plugins:
          key-auth:
            _meta:
              disable: false

consumers:
  - username: api-user
    plugins:
      key-auth:
        key: my-secret-key

global_rules:
  - id: 1
    plugins:
      prometheus:
        prefer_name: true
```

## APISIX Core Concepts

### Routes

Match client requests and forward to upstreams. Support path matching, host matching, and method filtering.

### Upstreams

Backend service definitions with load balancing. Support roundrobin, chash, ewma, least_conn algorithms.

### Services

Reusable configuration grouping routes with shared upstream and plugins.

### Consumers

API users with authentication credentials. Used with auth plugins (key-auth, jwt-auth, basic-auth).

### Plugins

Middleware for authentication, rate limiting, transformation, observability. Applied at route, service, or consumer level.

## Common Plugin Configurations

### Rate Limiting

```yaml
plugins:
  limit-count:
    count: 100
    time_window: 60
    key: remote_addr
    rejected_code: 429
```

### API Key Authentication

```yaml
# On route:
plugins:
  key-auth:
    _meta:
      disable: false

# Consumer:
consumers:
  - username: my-user
    plugins:
      key-auth:
        key: secret-api-key
```

### CORS

```yaml
plugins:
  cors:
    allow_origins: '*'
    allow_methods: 'GET,POST,PUT,DELETE'
    allow_headers: 'Authorization,Content-Type'
    max_age: 3600
```

## Default Ports

| Service       | Port                      |
| ------------- | ------------------------- |
| Gateway Proxy | 9080 (HTTP), 9443 (HTTPS) |
| Admin API     | 9180                      |
| etcd          | 2379                      |

## Troubleshooting

### Common Configuration Errors

#### Error: "Configuration file contains an unknown key"

**Problem**: You added invalid fields at the root level of `adc.yaml`.

```yaml
# ❌ WRONG - Don't add these at root level
name: my-api
version: 1.0.0
services:
  - name: my-service
```

**Solution**: Only use valid root-level keys:

```yaml
# ✅ CORRECT - Only these keys at root level
services:
  - name: my-service
    # ...
consumers:
  - username: user1
    # ...
global_rules:
  - id: 1
    # ...
```

Valid root-level keys: `services`, `consumers`, `global_rules`, `ssls`, `plugin_configs`

#### Error: Connection refused or "adc ping" fails

**Symptoms**: Cannot connect to APISIX Admin API.

**Solutions**:

1. Verify APISIX is running: `docker ps | grep apisix` or `systemctl status apisix`
2. Check if Admin API port (9180) is accessible: `curl http://localhost:9180/apisix/admin/routes -H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1"`
3. Ensure environment variables are set:
   ```bash
   export ADC_SERVER=http://localhost:9180
   export ADC_TOKEN=edd1c9f034335f136f87ad84b625c8f1
   ```
4. If using Docker, verify network connectivity between containers

#### Error: "Invalid route configuration" or validation fails

**Common causes**:

- Missing required fields (`name`, `upstream`, `routes`)
- Invalid plugin configuration
- Incorrect URI patterns

**Solution**: Run `adc lint -f adc.yaml` with detailed output to identify the specific issue.

#### Environment Variables Not Persisting

**Problem**: `adc` commands fail even after setting environment variables.

**Solution**: Always export variables in the same shell session:

```bash
# Add to .env file
echo "ADC_SERVER=http://localhost:9180" >> .env
echo "ADC_TOKEN=edd1c9f034335f136f87ad84b625c8f1" >> .env

# Export in current session
export ADC_SERVER=http://localhost:9180
export ADC_TOKEN=edd1c9f034335f136f87ad84b625c8f1

# Or source .env file
set -a; source .env; set +a
```

## Additional Resources

### Scripts

Utility scripts in `scripts/`:

- **`scripts/validate-yaml.sh`** - Two-step validation (YAML syntax + APISIX schema)

### Reference Files

For detailed information, consult:

- **`references/adc-commands.md`** - Complete ADC command reference
- **`references/configuration-schema.md`** - Full YAML schema with all fields

### Example Files

Working examples in `examples/`:

- **`examples/basic-route.yaml`** - Simple route configuration
- **`examples/proxy-rewrite.yaml`** - Route with URI rewriting (strip path prefix)
- **`examples/full-api.yaml`** - Complete API with auth and rate limiting
