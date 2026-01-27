---
name: eks-troubleshooting
description: EKS troubleshooting and debugging guide covering pod failures, cluster issues, networking problems, and performance diagnostics. Use when diagnosing cluster issues, debugging pod failures (CrashLoopBackOff, Pending, OOMKilled), resolving networking problems, investigating performance issues, troubleshooting IAM/IRSA permissions, fixing image pull errors, or analyzing EKS cluster health.
---

# EKS Troubleshooting Guide

## Overview

Comprehensive troubleshooting guide for Amazon EKS clusters covering control plane issues, node problems, pod failures, networking, storage, security, and performance diagnostics. Based on 2025 AWS best practices.

**Keywords**: EKS, Kubernetes, kubectl, debugging, troubleshooting, pod failure, node issues, networking, DNS, AWS, diagnostics

## When to Use This Skill

**Pod Issues:**
- Pods stuck in Pending, CrashLoopBackOff, ImagePullBackOff
- OOMKilled containers or CPU throttling
- Pod evictions or unexpected terminations
- Application errors in container logs

**Cluster Issues:**
- Nodes showing NotReady status
- Control plane API server timeouts
- Cluster autoscaling failures
- etcd performance problems

**Networking Problems:**
- DNS resolution failures
- Service connectivity issues
- Load balancer provisioning errors
- Cross-AZ traffic problems
- VPC CNI IP exhaustion

**Security & Permissions:**
- IAM/IRSA permission denied errors
- RBAC access issues
- Image pull authentication failures
- Service account problems

**Performance Issues:**
- Slow pod startup times
- High memory/CPU usage
- Resource contention
- Network latency

## Quick Diagnostic Workflow

### 1. Initial Triage (First 60 Seconds)

```bash
# Check cluster accessibility
kubectl cluster-info

# Get overall cluster status
kubectl get nodes
kubectl get pods --all-namespaces | grep -v Running

# Check recent events
kubectl get events --all-namespaces --sort-by='.lastTimestamp' | tail -20

# Check control plane components
kubectl get --raw /healthz
kubectl get componentstatuses  # Deprecated in 1.19+ but still useful
```

### 2. Identify Problem Area

**Pod Issues:**
```bash
# Get pod status
kubectl get pods -n <namespace>
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --previous  # Previous container logs
```

**Node Issues:**
```bash
# Check node status
kubectl get nodes -o wide
kubectl describe node <node-name>
kubectl top nodes  # Requires metrics-server
```

**Cluster-Wide Issues:**
```bash
# Check all resources
kubectl get all --all-namespaces
kubectl get events --all-namespaces --sort-by='.lastTimestamp'

# Check EKS cluster health (AWS CLI)
aws eks describe-cluster --name <cluster-name> --query 'cluster.health'
```

### 3. Deep Dive (See Reference Guides)

- **Pod/Workload Issues** → `references/workload-issues.md`
- **Node/Cluster Issues** → `references/cluster-issues.md`
- **Networking Issues** → `references/networking-issues.md`

## Common Pod Failure Patterns

### Pending Pods

**Symptoms:**
- Pod stuck in Pending state indefinitely
- No containers running

**Quick Check:**
```bash
kubectl describe pod <pod-name> -n <namespace> | grep -A 10 Events
```

**Common Causes:**
1. **Insufficient Resources**: No nodes with available CPU/memory
2. **Node Selector Mismatch**: Pod requires node labels that don't exist
3. **PVC Not Available**: Persistent volume claim not bound
4. **Taints/Tolerations**: Pod can't tolerate node taints

**Quick Fixes:**
```bash
# Check resource requests
kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 5 resources

# Check node capacity
kubectl describe nodes | grep -A 5 "Allocated resources"

# For Karpenter clusters - check provisioner logs
kubectl logs -n karpenter -l app.kubernetes.io/name=karpenter
```

### CrashLoopBackOff

**Symptoms:**
- Pod repeatedly crashing and restarting
- Restart count keeps increasing

**Quick Check:**
```bash
# View current logs
kubectl logs <pod-name> -n <namespace>

# View previous container logs (most useful)
kubectl logs <pod-name> -n <namespace> --previous

# Get exit code
kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.status.containerStatuses[0].lastState.terminated.exitCode}'
```

**Common Exit Codes:**
- **0**: Success (shouldn't crash)
- **1**: Application error
- **137**: SIGKILL (OOMKilled - out of memory)
- **139**: SIGSEGV (segmentation fault)
- **143**: SIGTERM (terminated)

**Quick Fixes:**
```bash
# Check for OOMKilled
kubectl describe pod <pod-name> -n <namespace> | grep -i oom

# Increase memory limit
kubectl set resources deployment <deployment-name> \
  -c <container-name> \
  --limits=memory=512Mi

# Check liveness/readiness probes
kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 10 Probe
```

### ImagePullBackOff

**Symptoms:**
- Pod can't pull container image
- ErrImagePull or ImagePullBackOff status

**Quick Check:**
```bash
kubectl describe pod <pod-name> -n <namespace> | grep -A 5 "Failed to pull image"
```

**Common Causes:**
1. **ECR Authentication**: Service account lacks ECR pull permissions
2. **Image Doesn't Exist**: Wrong repository, tag, or region
3. **Rate Limiting**: Docker Hub rate limits exceeded
4. **Registry Unreachable**: Network connectivity issues

**Quick Fixes:**
```bash
# Check if image exists (for ECR)
aws ecr describe-images --repository-name <repo-name> --image-ids imageTag=<tag>

# Verify IRSA role has ECR permissions
kubectl describe serviceaccount <sa-name> -n <namespace> | grep Annotations

# For ECR - ensure IAM role has this policy:
# AmazonEC2ContainerRegistryReadOnly or ecr:GetAuthorizationToken, ecr:BatchGetImage

# Test image pull manually on node
kubectl debug node/<node-name> -it --image=busybox
# Then: docker pull <image>
```

### OOMKilled

**Symptoms:**
- Container killed due to out of memory
- Exit code 137
- Last State shows "OOMKilled"

**Quick Check:**
```bash
# Check memory limits
kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 3 "limits:"

# Check actual memory usage
kubectl top pod <pod-name> -n <namespace>
```

**Quick Fix:**
```bash
# Increase memory limit
kubectl set resources deployment <deployment-name> \
  --limits=memory=1Gi \
  --requests=memory=512Mi
```

## Common Node Issues

### Node NotReady

**Quick Check:**
```bash
kubectl get nodes
kubectl describe node <node-name> | grep -A 10 Conditions
```

**Common Causes:**
1. **Disk Pressure**: Node running out of disk space
2. **Memory Pressure**: Node running out of memory
3. **Network Issues**: kubelet can't reach API server
4. **Kubelet Issues**: kubelet service crashed or unhealthy

**Quick Fixes:**
```bash
# Check node conditions
kubectl describe node <node-name> | grep -E "MemoryPressure|DiskPressure|PIDPressure"

# For EKS managed nodes - check EC2 instance health
aws ec2 describe-instance-status --instance-ids <instance-id>

# Drain and delete node (if managed node group - ASG will replace)
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data
kubectl delete node <node-name>
```

### IP Address Exhaustion

**Symptoms:**
- Pods can't get IP addresses
- Nodes showing high ENI usage
- CNI errors in logs

**Quick Check:**
```bash
# Check VPC CNI logs
kubectl logs -n kube-system -l k8s-app=aws-node --tail=100

# Check IP addresses per node
kubectl get nodes -o custom-columns=NAME:.metadata.name,ADDRESSES:.status.addresses[*].address

# Check ENI usage
aws ec2 describe-instances --instance-ids <instance-id> \
  --query 'Reservations[].Instances[].NetworkInterfaces[].PrivateIpAddresses'
```

**Quick Fixes:**
```bash
# Enable prefix delegation (for new nodes)
kubectl set env daemonset aws-node \
  -n kube-system \
  ENABLE_PREFIX_DELEGATION=true

# Increase warm pool targets
kubectl set env daemonset aws-node \
  -n kube-system \
  WARM_IP_TARGET=5
```

## Essential kubectl Commands

### Information Gathering

```bash
# Pod debugging
kubectl get pods -n <namespace> -o wide
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --tail=100 -f
kubectl logs <pod-name> -n <namespace> -c <container-name>  # Multi-container pods
kubectl logs <pod-name> -n <namespace> --previous  # Previous crash logs

# Node debugging
kubectl get nodes -o wide
kubectl describe node <node-name>
kubectl top nodes
kubectl top pods -n <namespace>

# Events (VERY useful)
kubectl get events -n <namespace> --sort-by='.lastTimestamp'
kubectl get events --all-namespaces --sort-by='.lastTimestamp' | tail -50

# Resource usage
kubectl top pods -n <namespace> --containers
kubectl describe node <node-name> | grep -A 5 "Allocated resources"
```

### Advanced Debugging

```bash
# Execute command in running pod
kubectl exec -it <pod-name> -n <namespace> -- /bin/sh

# Port forward for local testing
kubectl port-forward <pod-name> -n <namespace> 8080:80

# Debug with ephemeral container (K8s 1.23+)
kubectl debug <pod-name> -n <namespace> -it --image=busybox

# Debug node issues
kubectl debug node/<node-name> -it --image=ubuntu

# Copy files from pod
kubectl cp <namespace>/<pod-name>:/path/to/file ./local-file

# Get pod YAML
kubectl get pod <pod-name> -n <namespace> -o yaml

# Get all resources in namespace
kubectl get all -n <namespace>
kubectl api-resources --verbs=list --namespaced -o name \
  | xargs -n 1 kubectl get --show-kind --ignore-not-found -n <namespace>
```

### Filtering & Formatting

```bash
# Get pods not running
kubectl get pods --all-namespaces --field-selector=status.phase!=Running

# Get pods by label
kubectl get pods -n <namespace> -l app=myapp

# Custom columns
kubectl get pods -n <namespace> -o custom-columns=\
NAME:.metadata.name,\
STATUS:.status.phase,\
NODE:.spec.nodeName,\
IP:.status.podIP

# JSONPath queries
kubectl get pods -n <namespace> -o jsonpath='{.items[*].metadata.name}'

# Get pod restart count
kubectl get pods -n <namespace> -o jsonpath=\
'{range .items[*]}{.metadata.name}{"\t"}{.status.containerStatuses[0].restartCount}{"\n"}{end}'
```

## AWS-Specific Troubleshooting

### EKS Cluster Health

```bash
# Check EKS cluster status
aws eks describe-cluster --name <cluster-name> \
  --query 'cluster.{Status:status,Health:health,Version:version}'

# List all EKS clusters
aws eks list-clusters

# Check addon status
aws eks list-addons --cluster-name <cluster-name>
aws eks describe-addon --cluster-name <cluster-name> --addon-name vpc-cni

# Update kubeconfig
aws eks update-kubeconfig --name <cluster-name> --region <region>
```

### IAM/IRSA Troubleshooting

```bash
# Check service account IRSA annotation
kubectl get sa <sa-name> -n <namespace> -o yaml | grep eks.amazonaws.com/role-arn

# Verify pod has correct service account
kubectl get pod <pod-name> -n <namespace> -o yaml | grep serviceAccountName

# Check if pod has AWS credentials
kubectl exec <pod-name> -n <namespace> -- env | grep AWS

# Test IAM permissions from pod
kubectl exec <pod-name> -n <namespace> -- aws sts get-caller-identity
kubectl exec <pod-name> -n <namespace> -- aws s3 ls  # Test S3 access
```

### ECR Authentication

```bash
# Get ECR login password
aws ecr get-login-password --region <region>

# Test ECR access
aws ecr describe-repositories --region <region>

# Check if IAM role/user has ECR permissions
aws iam get-role --role-name <role-name>
aws iam list-attached-role-policies --role-name <role-name>
```

### Karpenter Troubleshooting

```bash
# Check Karpenter logs
kubectl logs -n karpenter -l app.kubernetes.io/name=karpenter --tail=100 -f

# Check provisioner configuration
kubectl get provisioner -o yaml

# Check Karpenter controller status
kubectl get pods -n karpenter

# Debug why nodes not provisioning
kubectl describe provisioner default
kubectl get events -n karpenter --sort-by='.lastTimestamp'
```

## Performance Diagnostics

### Resource Contention

```bash
# Check node resource usage
kubectl top nodes

# Check pod resource usage
kubectl top pods -n <namespace> --sort-by=memory
kubectl top pods -n <namespace> --sort-by=cpu

# Check resource requests vs limits
kubectl get pods -n <namespace> -o custom-columns=\
NAME:.metadata.name,\
CPU_REQ:.spec.containers[*].resources.requests.cpu,\
CPU_LIM:.spec.containers[*].resources.limits.cpu,\
MEM_REQ:.spec.containers[*].resources.requests.memory,\
MEM_LIM:.spec.containers[*].resources.limits.memory
```

### Application Performance

```bash
# Check pod readiness/liveness probes
kubectl get pods -n <namespace> -o yaml | grep -A 10 Probe

# Check pod startup time
kubectl describe pod <pod-name> -n <namespace> | grep Started

# Profile application in pod
kubectl exec <pod-name> -n <namespace> -- top
kubectl exec <pod-name> -n <namespace> -- netstat -tuln
```

## Log Analysis

### CloudWatch Container Insights

```bash
# Enable Container Insights (if not enabled)
# Via AWS CLI:
aws eks update-cluster-config \
  --name <cluster-name> \
  --logging '{"clusterLogging":[{"types":["api","audit","authenticator","controllerManager","scheduler"],"enabled":true}]}'

# Check control plane logs in CloudWatch
# Log groups:
# - /aws/eks/<cluster-name>/cluster
# - /aws/containerinsights/<cluster-name>/application
# - /aws/containerinsights/<cluster-name>/host
# - /aws/containerinsights/<cluster-name>/dataplane
```

### Fluent Bit Logs

```bash
# Check Fluent Bit daemonset
kubectl get pods -n amazon-cloudwatch -l k8s-app=fluent-bit

# Check Fluent Bit logs
kubectl logs -n amazon-cloudwatch -l k8s-app=fluent-bit --tail=50
```

## Emergency Procedures

### Pod Stuck Terminating

```bash
# Force delete pod
kubectl delete pod <pod-name> -n <namespace> --grace-period=0 --force

# If still stuck, remove finalizers
kubectl patch pod <pod-name> -n <namespace> -p '{"metadata":{"finalizers":null}}'
```

### Node Stuck Draining

```bash
# Force drain
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data --force

# If still stuck, delete pods directly
kubectl delete pods -n <namespace> --field-selector spec.nodeName=<node-name> --force --grace-period=0
```

### Cluster Unresponsive

```bash
# Check API server health
kubectl get --raw /healthz

# Check control plane logs (CloudWatch)
aws logs tail /aws/eks/<cluster-name>/cluster --follow

# Restart coredns if DNS issues
kubectl rollout restart deployment coredns -n kube-system

# Check etcd health (EKS manages this, but can check API responsiveness)
time kubectl get nodes  # Should be < 1 second
```

## Prevention Best Practices

### Resource Management

```yaml
# Always set resource requests and limits
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"  # CPU limits optional, can cause throttling
```

### Health Checks

```yaml
# Implement probes for all applications
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3

startupProbe:  # For slow-starting apps
  httpGet:
    path: /healthz
    port: 8080
  failureThreshold: 30
  periodSeconds: 10
```

### High Availability

```yaml
# Pod disruption budgets
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: app-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: myapp
```

## Reference Guides

For detailed troubleshooting of specific areas:

- **[Cluster & Node Issues](references/cluster-issues.md)** - Control plane, nodes, autoscaling, etcd
- **[Workload Issues](references/workload-issues.md)** - Pods, deployments, jobs, statefulsets
- **[Networking Issues](references/networking-issues.md)** - DNS, connectivity, load balancers, CNI

## Additional Resources

**AWS Documentation:**
- [EKS Best Practices Guide](https://aws.github.io/aws-eks-best-practices/)
- [EKS User Guide](https://docs.aws.amazon.com/eks/latest/userguide/)
- [EKS Troubleshooting](https://docs.aws.amazon.com/eks/latest/userguide/troubleshooting.html)

**Kubernetes Documentation:**
- [Kubernetes Debugging Guide](https://kubernetes.io/docs/tasks/debug/)
- [Application Introspection and Debugging](https://kubernetes.io/docs/tasks/debug/debug-application/)

**Tools:**
- [kubectl-debug](https://github.com/aylei/kubectl-debug) - Advanced debugging
- [Popeye](https://github.com/derailed/popeye) - Cluster sanitizer
- [kube-bench](https://github.com/aquasecurity/kube-bench) - CIS benchmark checker

---

**Quick Start**: Use diagnostic workflow above → Identify issue type → Jump to relevant reference guide
**Last Updated**: November 27, 2025 (2025 AWS Best Practices)
