---
name: kubectl
description: This skill should be used when users need to interact with Kubernetes clusters via kubectl CLI. It covers pod management, deployment operations, log viewing, debugging, resource monitoring, scaling, ConfigMaps, Secrets, Services, and all standard kubectl operations. Supports multiple clusters (production, staging, local k3s) with predefined aliases. Triggers on requests mentioning Kubernetes, k8s, pods, deployments, containers, or cluster operations.
---

# Kubectl Skill

This skill enables comprehensive Kubernetes cluster management using kubectl and related tools.

## Environment

### Cluster Aliases

Three cluster/namespace combinations are pre-configured:

| Alias | Cluster | Namespace | Purpose |
|-------|---------|-----------|---------|
| `k1` | AWS EKS Production | `production` | 生产环境 |
| `k2` | AWS EKS Production | `staging` | 预发布环境 |
| `k` | K3s (192.168.10.117) | `simplex` | 本地开发环境 |

**Usage:**
```bash
k1 get pods          # 查看生产环境 pods
k2 get pods          # 查看预发布环境 pods
k get pods           # 查看本地环境 pods
```

### Additional Tools

- `kubectx` - Switch between clusters
- `kubens` - Switch between namespaces
- `argocd` - GitOps deployments (see separate skill)
- `kargo` - Progressive delivery (see separate skill)

## Safety Protocol

### Dangerous Operations Requiring Confirmation

Before executing any of the following operations, explicitly confirm with the user:

- **Delete operations**: `delete pod`, `delete deployment`, `delete service`, `delete pvc`
- **Scale to zero**: `scale --replicas=0`
- **Production modifications**: Any `k1` command that modifies resources
- **Drain/cordon nodes**: `drain`, `cordon`, `uncordon`
- **Apply/patch**: Changes to production resources

### Confirmation Format

```
⚠️ 危险操作确认

环境: [Production/Staging/Local]
操作: [具体操作描述]
资源: [受影响的资源]
影响: [潜在影响说明]

是否继续执行？
```

## Common Operations Reference

### Resource Viewing

#### Pods

```bash
# List pods with status
k1 get pods
k1 get pods -o wide                    # Include node and IP info
k1 get pods --show-labels              # Show labels
k1 get pods -l app=simplex-api         # Filter by label

# Pod details
k1 describe pod <pod-name>

# Watch pods in real-time
k1 get pods -w
```

#### Deployments

```bash
# List deployments
k1 get deployments
k1 get deploy -o wide

# Deployment details
k1 describe deployment <name>

# Rollout status
k1 rollout status deployment/<name>

# Rollout history
k1 rollout history deployment/<name>
```

#### Services & Endpoints

```bash
# List services
k1 get services
k1 get svc

# Service details with endpoints
k1 describe svc <name>
k1 get endpoints <name>
```

#### All Resources

```bash
# Get all common resources
k1 get all

# Get specific resource types
k1 get pods,svc,deploy

# Get all resources with labels
k1 get all -l app=simplex-api
```

### Logs & Debugging

#### Viewing Logs

```bash
# Basic logs
k1 logs <pod-name>

# Follow logs (streaming)
k1 logs -f <pod-name>

# Last N lines
k1 logs --tail=100 <pod-name>

# Logs since time
k1 logs --since=1h <pod-name>
k1 logs --since=10m <pod-name>

# Previous container logs (after restart)
k1 logs --previous <pod-name>

# Multi-container pod
k1 logs <pod-name> -c <container-name>

# All containers in pod
k1 logs <pod-name> --all-containers=true
```

#### Executing Commands

```bash
# Execute command in container
k1 exec <pod-name> -- <command>

# Interactive shell
k1 exec -it <pod-name> -- /bin/sh
k1 exec -it <pod-name> -- /bin/bash

# Specific container in multi-container pod
k1 exec -it <pod-name> -c <container> -- /bin/sh
```

#### Debugging

```bash
# Pod events and status
k1 describe pod <pod-name>

# Get pod YAML
k1 get pod <pod-name> -o yaml

# Debug with ephemeral container
k1 debug <pod-name> -it --image=busybox

# Check resource usage
k1 top pods
k1 top nodes
```

### Deployment Management

#### Scaling

```bash
# Scale deployment
k1 scale deployment/<name> --replicas=3

# Autoscale
k1 autoscale deployment/<name> --min=2 --max=5 --cpu-percent=80
```

#### Rolling Updates

```bash
# Update image
k1 set image deployment/<name> <container>=<image>:<tag>

# Rollout status
k1 rollout status deployment/<name>

# Pause/resume rollout
k1 rollout pause deployment/<name>
k1 rollout resume deployment/<name>

# Rollback
k1 rollout undo deployment/<name>
k1 rollout undo deployment/<name> --to-revision=2
```

#### Restart

```bash
# Restart deployment (rolling restart)
k1 rollout restart deployment/<name>
```

### Configuration Resources

#### ConfigMaps

```bash
# List ConfigMaps
k1 get configmaps
k1 get cm

# View ConfigMap content
k1 describe cm <name>
k1 get cm <name> -o yaml

# Create from file
k1 create configmap <name> --from-file=<path>

# Create from literal
k1 create configmap <name> --from-literal=key=value
```

#### Secrets

```bash
# List Secrets
k1 get secrets

# View Secret (base64 encoded)
k1 get secret <name> -o yaml

# Decode Secret value
k1 get secret <name> -o jsonpath='{.data.password}' | base64 -d

# Create Secret
k1 create secret generic <name> --from-literal=password=xxx
```

#### PersistentVolumeClaims

```bash
# List PVCs
k1 get pvc

# PVC details
k1 describe pvc <name>
```

### Network Operations

#### Port Forwarding

```bash
# Forward local port to pod
k1 port-forward pod/<name> 8080:80

# Forward to service
k1 port-forward svc/<name> 8080:80

# Background port-forward
k1 port-forward pod/<name> 8080:80 &
```

#### Service Exposure

```bash
# Expose deployment as service
k1 expose deployment/<name> --port=80 --target-port=8080

# Get service external IP
k1 get svc <name> -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
```

### Cluster Management

#### Nodes

```bash
# List nodes
k1 get nodes
k1 get nodes -o wide

# Node details
k1 describe node <name>

# Node resource usage
k1 top nodes
```

#### Namespaces

```bash
# List namespaces
k1 get namespaces

# Switch namespace (using kubens)
kubens <namespace>

# Create namespace
k1 create namespace <name>
```

#### Context Management

```bash
# List contexts
kubectx

# Switch context
kubectx <context-name>

# Show current context
kubectl config current-context
```

### Resource Monitoring

```bash
# Pod resource usage
k1 top pods
k1 top pods --sort-by=cpu
k1 top pods --sort-by=memory

# Node resource usage
k1 top nodes

# HPA status
k1 get hpa
k1 describe hpa <name>
```

## Output Formatting

### For Status Checks

Provide concise summaries:

```
✅ Pod 状态 (production)
┌──────────────────────────┬─────────┬──────────┬─────────┐
│ Pod                      │ Status  │ Restarts │ Age     │
├──────────────────────────┼─────────┼──────────┼─────────┤
│ simplex-api-xxx-abc      │ Running │ 0        │ 2d      │
│ simplex-api-xxx-def      │ Running │ 0        │ 2d      │
└──────────────────────────┴─────────┴──────────┴─────────┘
```

### For Troubleshooting

When investigating issues, gather:

1. Pod status: `k1 get pod <name>`
2. Pod events: `k1 describe pod <name>`
3. Recent logs: `k1 logs --tail=50 <name>`
4. Resource usage: `k1 top pod <name>`

### Custom Output Formats

```bash
# JSON output
k1 get pods -o json

# YAML output
k1 get pod <name> -o yaml

# Custom columns
k1 get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase

# JSONPath
k1 get pods -o jsonpath='{.items[*].metadata.name}'
```

## Troubleshooting Workflows

### Pod Not Starting

1. Check pod status: `k1 get pod <name>`
2. Check events: `k1 describe pod <name>` (look at Events section)
3. Check logs: `k1 logs <name>` or `k1 logs --previous <name>`
4. Common issues:
   - `ImagePullBackOff`: Check image name and registry credentials
   - `CrashLoopBackOff`: Check application logs
   - `Pending`: Check resource requests and node capacity

### High Resource Usage

1. Check pod usage: `k1 top pods --sort-by=memory`
2. Check node usage: `k1 top nodes`
3. Check HPA status: `k1 get hpa`
4. Consider scaling: `k1 scale deployment/<name> --replicas=N`

### Service Not Accessible

1. Check service: `k1 get svc <name>`
2. Check endpoints: `k1 get endpoints <name>`
3. Check pod labels match service selector
4. Test from within cluster: `k1 exec -it <pod> -- curl <service>:<port>`

## Integration Notes

For GitOps operations (deployments via git), use the ArgoCD and Kargo skills:
- ArgoCD: Application sync, rollback, status
- Kargo: Progressive delivery, freight promotion

For AWS infrastructure operations, use the AWS CLI skill.
