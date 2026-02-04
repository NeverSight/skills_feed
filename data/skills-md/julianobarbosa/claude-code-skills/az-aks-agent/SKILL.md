---
name: az-aks-agent
description: Azure AKS Agentic CLI - AI-powered troubleshooting and insights tool for Azure Kubernetes Service. Use when diagnosing AKS cluster issues, getting cluster health insights, troubleshooting networking/storage/security problems, or analyzing cluster configuration with natural language queries.
---

# Azure AKS Agent CLI Skill

## Overview

The **Agentic CLI for Azure Kubernetes Service (AKS)** is an AI-powered troubleshooting and insights tool (currently in preview) that brings advanced diagnostics directly to your terminal. It allows you to ask natural language questions about your cluster's health, configuration, and issues without requiring deep Kubernetes expertise or knowledge of complex command syntax.

**Primary Command**: `az aks agent`

## Quick Reference

### Installation

```bash
# Prerequisites: Azure CLI version 2.76 or higher
az version

# Install the extension (takes 5-10 minutes)
az extension add --name aks-agent --debug

# Verify installation
az extension list
az aks agent --help

# Initialize LLM configuration (interactive wizard)
az aks agent-init

# Remove extension if needed
az extension remove --name aks-agent --debug
```

### Basic Usage

```bash
# Get cluster credentials first
az aks get-credentials --resource-group <rg-name> --name <cluster-name>

# Start interactive troubleshooting
az aks agent -g <resource-group> -n <cluster-name>

# Ask a specific question
az aks agent -g <resource-group> -n <cluster-name> --query "What's wrong with my cluster?"

# Non-interactive mode (batch processing)
az aks agent -g <resource-group> -n <cluster-name> --no-interactive --query "Check pod health"
```

## Workflow Decision Tree

```
What do you need to do?
├── Cluster Health Check?
│   └── Use: az aks agent --query "What's the health status of my cluster?"
├── Troubleshoot Pod Issues?
│   └── Use: az aks agent --query "Why are my pods failing?"
├── Networking Problems?
│   └── Use: az aks agent --query "Diagnose networking issues"
├── Storage Issues?
│   └── Use: az aks agent --query "Check storage configuration"
├── Security/RBAC Issues?
│   └── Use: az aks agent --query "Review RBAC configuration"
├── Node Pool Problems?
│   └── Use: az aks agent --query "Check node pool health"
└── Configuration Review?
    └── Use: az aks agent --query "Review cluster configuration"
```

## Command Reference

### Core Commands

| Command | Description |
|---------|-------------|
| `az aks agent` | Start interactive AI-powered troubleshooting |
| `az aks agent-init` | Initialize LLM provider configuration |
| `az aks agent --help` | Show help and available options |

### Command Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `-g, --resource-group` | Resource group name | Required |
| `-n, --name` | AKS cluster name | Required |
| `--api-key` | LLM API key | From env or config |
| `--config-file` | Config file path | `~/.azure/aksAgent.config` |
| `--max-steps` | Max investigation steps | 10 |
| `--model` | LLM model specification | From config |
| `--no-interactive` | Run in batch mode | false |
| `--show-tool-output` | Display tool call outputs | false |
| `--refresh-toolsets` | Refresh toolsets status | false |

### LLM Model Specifications

```bash
# Azure OpenAI
--model "azure/gpt-4o"
--model "azure/gpt-4o-mini"

# OpenAI
--model "gpt-4o"
--model "gpt-4o-mini"

# Anthropic
--model "anthropic/claude-sonnet-4"
--model "anthropic/claude-3-5-sonnet"

# Gemini
--model "gemini/gemini-pro"
```

## Configuration

### Environment Variables

```bash
# Azure OpenAI API Key
export AZURE_API_KEY="your-azure-openai-key"

# OpenAI API Key
export OPENAI_API_KEY="your-openai-key"

# Anthropic API Key
export ANTHROPIC_API_KEY="your-anthropic-key"
```

### Config File Structure (~/.azure/aksAgent.config)

```yaml
# Azure OpenAI Configuration
llm_provider: azure
azure_api_base: https://<your-endpoint>.openai.azure.com/
azure_api_version: 2025-04-01-preview
model: gpt-4o

# OR OpenAI Configuration
llm_provider: openai
model: gpt-4o

# OR Anthropic Configuration
llm_provider: anthropic
model: claude-sonnet-4
```

### Azure OpenAI Requirements

- **Deployment name**: Must match model name
- **Minimum TPM**: 1,000,000+ (Tokens Per Minute)
- **Minimum context size**: 128,000+ tokens
- **API Base Format**: `https://{endpoint}.openai.azure.com/` (NOT AI Foundry URI)

## Common Use Cases

### Cluster Health Analysis

```bash
# General health check
az aks agent -g myRG -n myCluster --query "What's the overall health of my cluster?"

# Node status
az aks agent -g myRG -n myCluster --query "Are all nodes healthy and ready?"

# Resource utilization
az aks agent -g myRG -n myCluster --query "Show me resource utilization across nodes"
```

### Pod Troubleshooting

```bash
# Failed pods analysis
az aks agent -g myRG -n myCluster --query "Why are pods in CrashLoopBackOff?"

# Pending pods
az aks agent -g myRG -n myCluster --query "Why are some pods stuck in Pending state?"

# OOMKilled pods
az aks agent -g myRG -n myCluster --query "Investigate OOMKilled containers"
```

### Networking Issues

```bash
# Network policy review
az aks agent -g myRG -n myCluster --query "Are there network policies blocking traffic?"

# DNS troubleshooting
az aks agent -g myRG -n myCluster --query "Diagnose DNS resolution issues"

# Service connectivity
az aks agent -g myRG -n myCluster --query "Why can't pods reach external services?"
```

### Storage Troubleshooting

```bash
# PVC issues
az aks agent -g myRG -n myCluster --query "Why are PersistentVolumeClaims pending?"

# Storage class review
az aks agent -g myRG -n myCluster --query "Review storage class configuration"
```

### Security Analysis

```bash
# RBAC review
az aks agent -g myRG -n myCluster --query "Are RBAC permissions configured correctly?"

# Security best practices
az aks agent -g myRG -n myCluster --query "What security improvements do you recommend?"
```

## AKS Events Reference

### Viewing Cluster Events

```bash
# Get cluster credentials first
az aks get-credentials --resource-group $RESOURCE_GROUP --name $AKS_CLUSTER

# List all events
kubectl get events

# Filter by namespace
kubectl get events --namespace default

# Watch auto-repair events
kubectl get events --field-selector=source=aks-auto-repair --watch

# Detailed pod events
kubectl describe pod $POD_NAME
```

### Event Types

| Type | Description |
|------|-------------|
| `Normal` | Routine operations and expected activities |
| `Warning` | Potentially problematic situations requiring attention |

### Common Event Reasons

| Reason | Description |
|--------|-------------|
| `FailedScheduling` | Pod failed to be scheduled on a node |
| `CrashLoopBackOff` | Container is in a restart loop |
| `Scheduled` | Pod successfully assigned to a node |
| `Pulled` | Container image successfully pulled |
| `Created` | Container created |
| `Started` | Container started |
| `OOMKilled` | Container killed due to out of memory |

### Event Fields

| Field | Description |
|-------|-------------|
| `type` | Warning or Normal |
| `reason` | Short reason code |
| `message` | Human-readable description |
| `namespace` | Kubernetes namespace |
| `firstSeen` | First observation timestamp |
| `lastSeen` | Most recent observation |
| `object` | Associated Kubernetes object |

## Best Practices

### Effective Query Strategies

1. **Start broad, then narrow**

   ```bash
   # Start with general health
   "What's wrong with my cluster?"
   # Then focus on specific issues
   "Why are pods in namespace X failing?"
   ```

2. **Provide context about symptoms**

   ```bash
   "Pods are restarting frequently in the production namespace"
   "Services are experiencing intermittent timeouts"
   ```

3. **Ask for specific recommendations**

   ```bash
   "What changes do you recommend to improve cluster performance?"
   "How can I fix the networking issues you identified?"
   ```

4. **Request historical analysis**

   ```bash
   "What patterns do you see in recent pod failures?"
   "Have there been any unusual events in the last 24 hours?"
   ```

### Security Considerations

- Ensure proper RBAC permissions are configured
- Use Azure AD integration for authentication
- Follow principle of least privilege
- Audit command usage through Azure activity logs
- Service account tokens for automation

### Integration Tips

1. **Combine with traditional monitoring**: Use alongside Azure Monitor and Container Insights
2. **Proactive monitoring**: Run health checks regularly
3. **Document findings**: Save important diagnostic outputs
4. **Enable Container Insights**: For events beyond 1-hour retention

## Troubleshooting the Agent

### Installation Issues

```bash
# Verify Azure CLI version
az version

# Upgrade Azure CLI if needed
az upgrade

# Force reinstall extension
az extension remove --name aks-agent
az extension add --name aks-agent --debug
```

### Authentication Issues

```bash
# Verify Azure login
az account show

# Re-authenticate
az login

# Check subscription
az account set --subscription <subscription-id>
```

### LLM Connection Issues

```bash
# Reinitialize LLM configuration
az aks agent-init

# Check API key environment variable
echo $AZURE_API_KEY

# Test with explicit API key
az aks agent -g myRG -n myCluster --api-key "your-key"
```

### Rate Limiting

- **Symptom**: Slow responses or errors
- **Solution**: Increase TPM quota in Azure OpenAI deployment
- **Minimum recommended**: 1,000,000 TPM

## Important Notes

1. **Preview Feature**: This is currently in preview with limited warranty coverage
2. **Not for Production Critical**: Not recommended for production-critical decision making
3. **Event Retention**: Kubernetes events only persist for 1 hour by default
4. **Context Window**: Requires 128,000+ token context for optimal performance
5. **Authentication**: Always authenticate with `az login` before using

## Resources

### References

#### Core References

- `references/cli-commands.md` - Complete CLI command reference
- `references/troubleshooting.md` - Extended troubleshooting guide
- `references/examples.md` - Practical usage examples

#### Diagnostics & Monitoring

- `references/diagnostics.md` - AKS Diagnose and Solve Problems guide
- `references/monitoring.md` - Comprehensive AKS monitoring guide
- `references/control-plane-metrics.md` - Control plane metrics (API Server, etcd)

#### Troubleshooting Guides

- `references/kubelet-logs.md` - Kubelet logs access and analysis
- `references/memory-saturation.md` - Memory saturation identification and resolution
- `references/node-auto-repair.md` - Node auto-repair process and monitoring
- `references/api-server-etcd.md` - API server and etcd troubleshooting

### External Documentation

- [AKS Agent Overview](https://learn.microsoft.com/en-us/azure/aks/cli-agent-for-aks-overview)
- [AKS Agent Installation](https://learn.microsoft.com/en-us/azure/aks/cli-agent-for-aks-install)
- [AKS Events](https://learn.microsoft.com/en-us/azure/aks/events)
- [AKS Diagnostics](https://learn.microsoft.com/en-us/azure/aks/aks-diagnostics)
- [Monitor AKS](https://learn.microsoft.com/en-us/azure/aks/monitor-aks)
- [Control Plane Metrics](https://learn.microsoft.com/en-us/azure/aks/control-plane-metrics-monitor)
- [Kubelet Logs](https://learn.microsoft.com/en-us/azure/aks/kubelet-logs)
- [Memory Saturation](https://learn.microsoft.com/en-us/troubleshoot/azure/azure-kubernetes/availability-performance/identify-memory-saturation-aks)
- [Node Auto-Repair](https://learn.microsoft.com/en-us/azure/aks/node-auto-repair)
- [API Server/etcd Troubleshooting](https://learn.microsoft.com/en-us/troubleshoot/azure/azure-kubernetes/create-upgrade-delete/troubleshoot-apiserver-etcd)
- [AKS Monitoring Reference](https://learn.microsoft.com/en-us/azure/aks/monitor-aks-reference)
- [AKS Agent Troubleshooting](https://learn.microsoft.com/en-us/azure/aks/cli-agent-for-aks-troubleshoot)
- [AKS Agent FAQ](https://learn.microsoft.com/en-us/azure/aks/cli-agent-for-aks-faq)
- [GitHub Repository](https://github.com/Azure/agentic-cli-for-aks)
- [Example Config](https://github.com/Azure/agentic-cli-for-aks/blob/main/exampleconfig.yaml)
