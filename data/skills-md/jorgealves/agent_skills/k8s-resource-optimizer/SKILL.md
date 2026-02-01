---
name: k8s-resource-optimizer
description: Analyzes Kubernetes resource usage metrics and historical data to suggest optimal CPU and Memory requests and limits. Use to reduce cloud costs, prevent OOMKills, and improve overall cluster reliability by right-sizing your deployments.
---
# K8s Resource Optimizer

## Purpose and Intent
The `k8s-resource-optimizer` helps teams balance performance and cost. It identifies containers that are either "starving" (causing crashes) or "bloated" (wasting money) by comparing their configuration against actual usage patterns.

## When to Use
- **Cloud Cost Optimization**: Run monthly to identify waste in your clusters.
- **Reliability Engineering**: Use after a production incident involving OOMKills to find the correct memory threshold.
- **Pre-production Scaling**: Set realistic requests/limits before a major launch.

## When NOT to Use
- **Initial Development**: Don't over-optimize before you have real traffic patterns.
- **Real-time Autoscaling**: This tool is for "right-sizing" configuration; use a HPA/VPA for real-time adjustments.

## Security and Data-Handling Considerations
- No live cluster interaction required if metrics are passed as text/json.
- Safe to run on infrastructure-as-code files.
