---
name: holmesgpt-skill
description: Guide for implementing HolmesGPT - an AI agent for troubleshooting cloud-native environments. Use when investigating Kubernetes issues, analyzing alerts from Prometheus/AlertManager/PagerDuty, performing root cause analysis, configuring HolmesGPT installations (CLI/Helm/Docker), setting up AI providers (OpenAI/Anthropic/Azure), creating custom toolsets, or integrating with observability platforms (Grafana, Loki, Tempo, DataDog).
---

# HolmesGPT Skill

AI-powered troubleshooting for Kubernetes and cloud-native environments.

## Overview

HolmesGPT is a CNCF Sandbox project that connects AI models with live
observability data to investigate infrastructure problems, find root
causes, and suggest remediations. It operates with **read-only access**
and respects RBAC permissions, making it safe for production environments.

## Quick Reference

| Topic | Reference |
|-------|-----------|
| **Installation** | `references/installation.md` |
| **Configuration** | `references/configuration.md` |
| **Data Sources** | `references/data-sources.md` |
| **Commands** | `references/commands.md` |
| **Troubleshooting** | `references/troubleshooting.md` |
| **HTTP API** | `references/http-api.md` |
| **Integrations** | `references/integrations.md` |

## Key Features

- **Root Cause Analysis**: Investigates alerts and cluster issues
- **Multi-Source Integration**: 30+ toolsets (K8s, Prometheus, Grafana)
- **Alert Integration**: AlertManager, PagerDuty, OpsGenie, Jira, Slack
- **Interactive Mode**: Troubleshooting with `/run`, `/show`, `/clear`
- **Custom Toolsets**: Extend with proprietary tools via YAML configuration
- **CI/CD Integration**: Automated deployment failure investigation

## Installation Quick Start

### CLI (Homebrew)

```bash
brew tap robusta-dev/homebrew-holmesgpt
brew install holmesgpt
export ANTHROPIC_API_KEY="your-key"  # or OPENAI_API_KEY
holmes ask "what pods are unhealthy?"
```

### Kubernetes (Helm)

```bash
helm repo add robusta https://robusta-charts.storage.googleapis.com
helm repo update
helm install holmesgpt robusta/holmes -f values.yaml
```

### Docker

```bash
docker run -it --net=host \
  -e OPENAI_API_KEY="your-key" \
  -v ~/.kube/config:/root/.kube/config \
  us-central1-docker.pkg.dev/genuine-flight-317411/devel/holmes \
  ask "what pods are crashing?"
```

## Essential Commands

```bash
# Basic investigation
holmes ask "what pods are unhealthy and why?"
holmes ask "why is my deployment failing?"

# Interactive mode
holmes ask "investigate issue" --interactive

# Alert investigation
holmes investigate alertmanager --alertmanager-url http://localhost:9093
holmes investigate pagerduty --pagerduty-api-key <KEY> --update

# With file context
holmes ask "summarize the key points" -f ./logs.txt

# CI/CD integration
holmes ask "why did deployment fail?" --destination slack --slack-token <TOKEN>
```

## Supported AI Providers

| Provider | Environment Variable | Models |
|----------|---------------------|--------|
| **Anthropic** | `ANTHROPIC_API_KEY` | Sonnet 4, Opus 4.5 |
| **OpenAI** | `OPENAI_API_KEY` | GPT-4.1, GPT-4o |
| **Azure OpenAI** | `AZURE_API_KEY` | GPT-4.1 |
| **AWS Bedrock** | AWS credentials | Claude 3.5 Sonnet |
| **Google Gemini** | `GEMINI_API_KEY` | Gemini 1.5 Pro |
| **Vertex AI** | `VERTEXAI_PROJECT` | Gemini 1.5 Pro |
| **Ollama** | Local install | Llama 3.1, Mistral |

## Basic Helm Values Structure

```yaml
# values.yaml for Kubernetes deployment
image:
  repository: robustadev/holmes
  tag: latest

env:
  - name: ANTHROPIC_API_KEY
    valueFrom:
      secretKeyRef:
        name: holmesgpt-secrets
        key: anthropic-api-key

# Model configuration
modelList:
  sonnet:
    api_key: "{{ env.ANTHROPIC_API_KEY }}"
    model: anthropic/claude-sonnet-4-20250514
    temperature: 0

# Toolsets to enable
toolsets:
  kubernetes/core:
    enabled: true
  kubernetes/logs:
    enabled: true
  prometheus/metrics:
    enabled: true

# Resources
resources:
  requests:
    memory: "1024Mi"
    cpu: "100m"
  limits:
    memory: "1024Mi"

# RBAC (read-only by default)
createServiceAccount: true
```

## Interactive Mode Commands

| Command | Description |
|---------|-------------|
| `/clear` | Reset context when changing topics |
| `/run` | Execute custom commands and share output with AI |
| `/show` | Display complete tool outputs |
| `/context` | Review accumulated investigation information |

## Custom Toolset Example

```yaml
# custom-toolset.yaml
toolsets:
  my-custom-tool:
    description: "Custom diagnostic tool"
    tools:
      - name: check_service_health
        description: "Check health of a specific service"
        command: |
          curl -s http://{{ service_name }}.{{ namespace }}.svc.cluster.local/health
        parameters:
          - name: service_name
            description: "Name of the service"
          - name: namespace
            description: "Kubernetes namespace"
```

Use with: `holmes ask "check health" -t custom-toolset.yaml`

## Kubernetes Annotations for Integration

```yaml
# Add to Services/Deployments for HolmesGPT context
metadata:
  annotations:
    holmesgpt.dev/runbook: |
      This service handles payment processing.
      Common issues: database connectivity, API rate limits.
      Check: kubectl logs -l app=payment-service
```

## Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `HOLMES_CONFIG_PATH` | Config file path | `~/.holmes/config.yaml` |
| `HOLMES_LOG_LEVEL` | Log verbosity | `INFO` |
| `PROMETHEUS_URL` | Prometheus server URL | - |
| `GITHUB_TOKEN` | GitHub API token | - |
| `DATADOG_API_KEY` | DataDog API key | - |
| `CONFLUENCE_BASE_URL` | Confluence URL | - |

## Best Practices

1. **Use Specific Queries**: Include namespace, deployment name, symptoms
2. **Start with Claude Sonnet 4.0/4.5**: Best accuracy for complex investigations
3. **Enable Relevant Toolsets**: Only enable what you need to reduce noise
4. **Use Interactive Mode**: For complex multi-step investigations
5. **Set Up Runbooks**: Provide context for known alert types
6. **CI/CD Integration**: Automate deployment failure analysis

## Security Considerations

- HolmesGPT uses **read-only access** (`get`, `list`, `watch` only)
- Respects existing RBAC permissions
- Never modifies, creates, or deletes resources
- API keys stored in Kubernetes Secrets
- Data not used for model training

## Official Resources

- Documentation: <https://holmesgpt.dev/>
- GitHub: <https://github.com/robusta-dev/holmesgpt>
- Helm Chart: <https://github.com/robusta-dev/holmesgpt/tree/master/helm/holmes>
- Slack Community: Cloud Native Slack
