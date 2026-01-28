---
name: flightcontrol-config
description: Flightcontrol configuration management. Use this skill when adding, editing, creating, or modifying flightcontrol.json or flightcontrol.cue configuration files. Covers services, environments, build settings, and deployment configurations.
license: MIT
metadata:
  author: flightcontrol
  version: "1.0.0"
---

# Flightcontrol Configuration

Manage Flightcontrol deployment configurations, usually via `flightcontrol.json` or `flightcontrol.cue`.

## When to Apply

Use this skill when:

- Creating or updating `flightcontrol.json` or `flightcontrol.cue`
- Adding, editing, or removing services (web, worker, database, etc.)
- Configuring environments (production, staging, preview)
- Setting up build, deploy, or CI runner settings
- Managing environment variables and cross-service references
- Troubleshooting deployment configuration issues

## Canonical Schema and Docs

The hosted JSON schema is the source of truth for all properties, defaults, and validation rules.

- Schema: `https://app.flightcontrol.dev/schema.json`
- Docs: `https://www.flightcontrol.dev/docs`

Always include the schema in config files for editor validation and autocompletion:

```json
{
  "$schema": "https://app.flightcontrol.dev/schema.json",
  "environments": []
}
```

## Minimal Structure

```json
{
  "$schema": "https://app.flightcontrol.dev/schema.json",
  "envVariables": {},
  "environments": [
    {
      "id": "production",
      "name": "Production",
      "region": "us-west-2",
      "source": { "branch": "main" },
      "services": []
    }
  ]
}
```

## Core Concepts

- Root: `envVariables` apply to every environment and service.
- Environment: `id`, `name`, `region`, `source`, `services`, optional `envVariables`, optional `vpc`.
- Service: `id`, `name`, `type`, optional `envVariables`, optional `dependsOn`, optional `watchPaths`.

## Service Type Quick Guide

- `web`: public HTTP service with load balancing and CDN.
- `web-private`: internal HTTP service in the VPC.
- `worker`: background processes, no HTTP port.
- `scheduler`: cron-based jobs.
- `static`: static site hosted on S3 + CloudFront.
- `rds`: managed Postgres/MySQL/MariaDB database.
- `elasticache`: managed Redis or Valkey cache.
- `lambda-function`: Lambda with Docker image or zip build.
- `network-server`: TCP/UDP/gRPC via Network Load Balancer.
- `s3`: managed S3 bucket.

## Example Snippets

### Web Service

```json
{
  "id": "api",
  "name": "API Server",
  "type": "web",
  "buildType": "nixpacks",
  "cpu": 0.5,
  "memory": 1,
  "port": 3000,
  "minInstances": 1,
  "maxInstances": 3
}
```

### Worker Service

```json
{
  "id": "worker",
  "name": "Background Worker",
  "type": "worker",
  "buildType": "nixpacks",
  "cpu": 0.5,
  "memory": 1,
  "startCommand": "npm run worker"
}
```

### Scheduler Service

```json
{
  "id": "cron",
  "name": "Scheduled Tasks",
  "type": "scheduler",
  "buildType": "nixpacks",
  "cpu": 0.5,
  "memory": 1,
  "jobs": {
    "daily-report": {
      "schedule": "0 0 * * *",
      "startCommand": ["node", "scripts/daily-report.js"]
    }
  }
}
```

### Static Site

```json
{
  "id": "frontend",
  "name": "Frontend",
  "type": "static",
  "buildType": "nixpacks",
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "singlePageApp": true
}
```

### RDS Database

```json
{
  "id": "db",
  "name": "Database",
  "type": "rds",
  "engine": "postgres",
  "engineVersion": "16",
  "instanceSize": "db.t4g.micro",
  "storage": 20,
  "private": true
}
```

### ElastiCache

```json
{
  "id": "redis",
  "name": "Redis Cache",
  "type": "elasticache",
  "engine": "redis",
  "engineVersion": "7.1",
  "instanceSize": "cache.t4g.micro"
}
```

### Lambda Function (Image)

```json
{
  "id": "lambda-api",
  "name": "Lambda API",
  "type": "lambda-function",
  "buildType": "docker",
  "dockerfilePath": "./Dockerfile.lambda",
  "lambda": {
    "packageType": "image",
    "memory": 512,
    "timeoutSecs": 30
  }
}
```

### Network Server

```json
{
  "id": "grpc-api",
  "name": "gRPC API",
  "type": "network-server",
  "buildType": "docker",
  "cpu": 1,
  "memory": 2,
  "ports": [
    {
      "port": 50051,
      "protocol": "grpc",
      "healthCheck": {}
    }
  ]
}
```

### S3 Bucket

```json
{
  "id": "uploads",
  "name": "User Uploads",
  "type": "s3",
  "bucketNameBase": "myapp-uploads"
}
```

## Environment Variables

Environment variables can be set at three levels: project, environment, service. Lower levels override higher.

### Static Values

```json
"envVariables": {
  "NODE_ENV": "production",
  "DEBUG": false
}
```

### From Service

```json
"DATABASE_URL": {
  "fromService": {
    "id": "db",
    "value": "dbConnectionString"
  }
}
```

### From Parameter Store or Secrets Manager

```json
"STRIPE_SECRET_KEY": {
  "fromParameterStore": "myapp/stripe/secret_key"
}
```

```json
"DB_PASSWORD": {
  "fromSecretsManager": "arn:aws:secretsmanager:us-west-2:123456789:secret:myapp/db-password"
}
```

## Preview Environments

```json
{
  "id": "preview",
  "name": "Preview",
  "region": "us-west-2",
  "source": {
    "pr": true,
    "trigger": "push",
    "filter": {
      "toBranches": ["main"],
      "fromBranches": ["feature/**"]
    }
  },
  "services": []
}
```

## Build & Deploy Commands

### When buildType is nixpacks

- All build, deploy, and start commands are single string

### When buildType is Dockerfile

- The pre and post deploy and start commands will be passed to the docker image as CMD at runtime
- The CMD value is passed to the ENTRYPOINT value
- If ENTRYPOINT not defined, the commands need to be an array like `["/bin/sh", "-c", "pnpm start"]`

## Validation

After every change to a Flightcontrol config file, validate it using:

```bash
npx flightcontrol-validate <config-file>
```

### Exit Codes

- `0` = valid config
- `1` = validation errors (fix before proceeding)
- `2` = file not found or parse error

### Example Output

Success:

```json
{ "valid": true, "file": "flightcontrol.json" }
```

Validation errors:

```json
{
  "valid": false,
  "file": "flightcontrol.json",
  "errors": {
    "environments": [
      {
        "services": [
          {
            "memory": "Invalid input: expected number, received string"
          }
        ]
      }
    ]
  }
}
```

## AI Guidance

- **Always validate** with `npx flightcontrol-validate <file>` after each config edit. Fix any errors and re-validate before proceeding. Only show validation output to the user when there are errors.
- Always keep `$schema` and prefer the hosted schema for exact fields and defaults.
- Changing existing `id` values will create a new entity. The old one will be orphaned and can be deleted from the dashboard.
- Validate `fromService.id` references against existing service IDs.
- Ensure region consistency for VPC, Parameter Store, and Secrets Manager.

## References

- [Flightcontrol Documentation](https://www.flightcontrol.dev/docs)
- [Config documentation](https://www.flightcontrol.dev/docs/guides/flightcontrol/using-code)
- [Configuration Schema](https://app.flightcontrol.dev/schema.json)
- [AWS Regions](https://awsregion.info/)
- [Nixpacks Configuration](https://nixpacks.com/docs/configuration/file)
- [CUE lang documentation](https://cuelang.org/docs/concept/how-cue-works-with-json/)
