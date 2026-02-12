---
name: sentry-otel-exporter-setup
description: Configure the OpenTelemetry Collector with Sentry Exporter for multi-project routing and automatic project creation. Use when setting up OTel with Sentry, configuring collector pipelines for traces and logs, or routing telemetry from multiple services to Sentry projects.
---

# Sentry OTel Exporter Setup

**Terminology**: Always capitalize "Sentry Exporter" when referring to the exporter component.

Configure the OpenTelemetry Collector to send traces and logs to Sentry using the Sentry Exporter.

## Step 1: Choose Installation Method

Ask the user how they want to run the collector:

```
Question: "How do you want to run the OpenTelemetry Collector?"
Header: "Collector"
Options:
  - label: "Binary"
    description: "Download from GitHub releases. No Docker required."
  - label: "Docker"
    description: "Run as a container. Requires Docker installed."
```

### Binary Installation

The Sentry exporter is included in **otelcol-contrib** v0.145.0+.

Detect the user's platform and download the binary for them:

1. Run `uname -s` and `uname -m` to detect OS and architecture
2. Map to release values:
   - Darwin + arm64 → `darwin_arm64`
   - Darwin + x86_64 → `darwin_amd64`
   - Linux + x86_64 → `linux_amd64`
   - Linux + aarch64 → `linux_arm64`
3. Download and extract:
```bash
curl -LO https://github.com/open-telemetry/opentelemetry-collector-releases/releases/download/v0.145.0/otelcol-contrib_0.145.0_<os>_<arch>.tar.gz
tar -xzf otelcol-contrib_0.145.0_<os>_<arch>.tar.gz
chmod +x otelcol-contrib
```

Perform these steps for the user—do not just show them the commands.

### Docker Installation

1. Verify Docker is installed by running `docker --version`
2. Pull the image for the user:
```bash
docker pull otel/opentelemetry-collector-contrib:0.145.0
```

The `docker run` command comes later in Step 5 after the config is created.

## Step 2: Configure Project Creation

Ask the user whether to enable automatic project creation. Do not recommend either option:

```
Question: "Do you want Sentry to automatically create projects when telemetry arrives?"
Header: "Auto-create"
Options:
  - label: "Yes"
    description: "Projects created from service.name. Requires at least one team in your Sentry org. All new projects are assigned to the first team found. Initial data may be dropped during creation."
  - label: "No"
    description: "Projects must exist in Sentry before telemetry arrives."
```

**If user chooses Yes**: Warn them that the exporter will scan all projects and use the first team it finds. All auto-created projects will be assigned to that team. If they don't have any teams yet, they should create one in Sentry first.

## Step 3: Write Collector Config

Create `collector-config.yaml` with the Sentry exporter:

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

exporters:
  sentry:
    url: https://sentry.io
    org_slug: ${env:SENTRY_ORG_SLUG}
    auth_token: ${env:SENTRY_AUTH_TOKEN}

processors:
  batch:

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [sentry]
    logs:
      receivers: [otlp]
      processors: [batch]
      exporters: [sentry]
```

If user chose auto-create in Step 2, add `auto_create_projects: true` to the sentry exporter.

### Add Debug Exporter (Recommended)

For troubleshooting during setup, add the debug exporter to see telemetry in collector logs:

```yaml
exporters:
  sentry:
    # ... existing config
  debug:
    verbosity: detailed

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [sentry, debug]  # Add debug here
    logs:
      receivers: [otlp]
      processors: [batch]
      exporters: [sentry, debug]  # Add debug here
```

This logs all telemetry to console. Remove `debug` from exporters list once setup is verified.

### Routing (Optional)

To map service names to different project slugs, add `routing.attribute_to_project_mapping` to the sentry exporter. Services not in the mapping fall back to `service.name` as project slug.

## Step 4: Set Up Credentials

Create an Internal Integration in Sentry to get an auth token:

1. Go to **Settings → Developer Settings → Custom Integrations**
2. Click **Create New Integration** → Choose **Internal Integration**
3. Set permissions:
   - **Organization: Read** — required
   - **Project: Read** — required
   - **Project: Write** — required for `auto_create_projects`
4. Save, then click **Create New Token** and copy it

Search for existing `.env` files in the project using glob `**/.env`. If any are found, ask the user which one to add the credentials to:

```
Question: "Where should I add the Sentry credentials?"
Header: "Env file"
Options:
  - label: "<path/to/.env>"  # One option per discovered .env file
    description: "Add to existing file"
  - label: "Create new at root"
    description: "Create .env in project root"
```

Add these environment variables (with placeholder values) to the chosen file:

```bash
SENTRY_ORG_SLUG=your-org-slug
SENTRY_AUTH_TOKEN=your-token-here
```

Tell the user to replace the placeholder values:
- **Org slug**: Found in URL `sentry.io/organizations/{slug}/`
- **Auth token**: The token from step 4

Ensure the chosen `.env` file is in `.gitignore`.

## Step 5: Run the Collector

Provide run instructions based on the installation method chosen in Step 1.

### Binary

```bash
./otelcol-contrib --config collector-config.yaml
```

### Docker

```bash
docker run -d \
  --name otel-collector \
  -p 4317:4317 \
  -p 4318:4318 \
  -p 13133:13133 \
  -v $(pwd)/collector-config.yaml:/etc/otelcol-contrib/config.yaml \
  --env-file .env \
  otel/opentelemetry-collector-contrib:0.145.0
```

