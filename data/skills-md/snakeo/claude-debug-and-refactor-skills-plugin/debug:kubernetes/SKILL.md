---
name: debug:kubernetes
description: Debug Kubernetes clusters and workloads systematically with this comprehensive troubleshooting skill. Covers CrashLoopBackOff, ImagePullBackOff, OOMKilled, pending pods, service connectivity issues, PVC binding failures, and RBAC permission errors. Provides structured four-phase debugging methodology with kubectl commands, ephemeral debug containers, and essential one-liners for diagnosing pod, service, network, and storage problems across namespaces.
---

# Kubernetes Debugging Guide

A systematic approach to diagnosing and resolving Kubernetes issues. Always start with the basics: check events and logs first.

## Common Error Patterns

### CrashLoopBackOff
**What it means:** Container repeatedly crashes and fails to start. Kubernetes restarts it with exponential backoff (10s, 20s, 40s... up to 5 minutes).

**Common causes:**
- Insufficient memory/CPU resources
- Missing dependencies in container image
- Misconfigured liveness/readiness probes
- Application code errors or misconfigurations
- Missing environment variables or secrets

**Debug steps:**
```bash
# Check pod events and status
kubectl describe pod <pod-name> -n <namespace>

# View current and previous container logs
kubectl logs <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --previous

# Check resource limits vs actual usage
kubectl top pod <pod-name> -n <namespace>
```

**Solutions:**
- Tune probe `initialDelaySeconds` and `timeoutSeconds`
- Increase resource limits if hitting memory/CPU caps
- Fix missing dependencies in Dockerfile
- Review application startup code for errors

---

### ImagePullBackOff
**What it means:** Kubernetes cannot pull the container image. Retries with increasing delay (5s, 10s, 20s... up to 5 minutes).

**Common causes:**
- Incorrect image name or tag
- Missing registry authentication credentials
- Private registry without imagePullSecrets configured
- Network connectivity issues to registry
- Image does not exist in registry

**Debug steps:**
```bash
# Check pod events for specific error
kubectl describe pod <pod-name> -n <namespace>

# Verify image name in deployment
kubectl get deployment <name> -n <namespace> -o yaml | grep image:

# Check if imagePullSecrets are configured
kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A5 imagePullSecrets

# Test pulling image from node (if you have node access)
docker pull <image-name>
```

**Solutions:**
- Correct image name/tag in deployment spec
- Create and attach imagePullSecret for private registries
- Verify network access to container registry
- Check registry credentials haven't expired

---

### Pending Pods (Scheduling Failures)
**What it means:** Pod cannot be scheduled to any node.

**Common causes:**
- Insufficient cluster resources (CPU/memory)
- Node selectors or affinity rules cannot be satisfied
- Taints without matching tolerations
- PersistentVolumeClaim not bound
- Resource quotas exceeded

**Debug steps:**
```bash
# Check why pod is pending
kubectl describe pod <pod-name> -n <namespace>

# View cluster events
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# Check node resources
kubectl describe nodes | grep -A5 "Allocated resources"
kubectl top nodes

# Check PVC status if using persistent storage
kubectl get pvc -n <namespace>
```

**Solutions:**
- Scale up cluster or reduce resource requests
- Adjust nodeSelector/affinity rules
- Add tolerations for node taints
- Create or fix PersistentVolume bindings
- Increase namespace resource quotas

---

### OOMKilled
**What it means:** Container was forcefully terminated (SIGKILL, exit code 137) for exceeding memory limit.

**Common causes:**
- Memory limit set too low for application
- Memory leak in application code
- Processing large files or datasets
- High concurrency causing memory spikes
- JVM/runtime heap misconfiguration

**Debug steps:**
```bash
# Check termination reason
kubectl describe pod <pod-name> -n <namespace> | grep -A10 "Last State"

# View logs before termination
kubectl logs <pod-name> -n <namespace> --previous

# Check memory limits vs usage
kubectl top pod <pod-name> -n <namespace>
kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A5 resources:
```

**Solutions:**
- Increase memory limits in deployment spec
- Profile application for memory leaks
- Configure application memory settings (e.g., JVM -Xmx)
- Implement memory-efficient processing patterns
- Add horizontal pod autoscaling for load distribution

---

### Service Not Reachable
**What it means:** Cannot connect to service from within or outside cluster.

**Common causes:**
- Service selector doesn't match pod labels
- Pod not ready (failing readiness probe)
- NetworkPolicy blocking traffic
- Service port mismatch with container port
- Ingress/LoadBalancer misconfiguration

**Debug steps:**
```bash
# Check service and endpoints
kubectl get svc <service-name> -n <namespace>
kubectl get endpoints <service-name> -n <namespace>
kubectl describe svc <service-name> -n <namespace>

# Verify pod labels match service selector
kubectl get pods -n <namespace> --show-labels
kubectl get svc <service-name> -n <namespace> -o yaml | grep -A5 selector

# Test connectivity from within cluster
kubectl run debug --rm -it --image=busybox -- wget -qO- http://<service-name>.<namespace>:port

# Check network policies
kubectl get networkpolicy -n <namespace>
```

**Solutions:**
- Fix service selector to match pod labels
- Ensure pods are passing readiness probes
- Update NetworkPolicy to allow required traffic
- Verify port configurations match

---

### PVC Binding Failures
**What it means:** PersistentVolumeClaim cannot bind to a PersistentVolume.

**Common causes:**
- No PV available matching PVC requirements
- StorageClass not found or misconfigured
- Access mode mismatch (RWO vs RWX)
- Storage capacity insufficient
- Zone/region constraints not met

**Debug steps:**
```bash
# Check PVC status
kubectl get pvc -n <namespace>
kubectl describe pvc <pvc-name> -n <namespace>

# List available PVs
kubectl get pv

# Check StorageClass
kubectl get storageclass
kubectl describe storageclass <name>

# View provisioner events
kubectl get events -n <namespace> --field-selector reason=ProvisioningFailed
```

**Solutions:**
- Create matching PersistentVolume manually
- Fix StorageClass name or create required class
- Adjust access mode or capacity requirements
- Enable dynamic provisioning if available

---

### RBAC Permission Denied
**What it means:** Service account lacks required permissions for API operations.

**Common causes:**
- Missing Role or ClusterRole
- RoleBinding not created for service account
- Wrong namespace for RoleBinding
- Insufficient permissions in Role

**Debug steps:**
```bash
# Check what service account pod uses
kubectl get pod <pod-name> -n <namespace> -o yaml | grep serviceAccountName

# Test permissions
kubectl auth can-i <verb> <resource> --as=system:serviceaccount:<namespace>:<sa-name>

# List roles and bindings
kubectl get roles,rolebindings -n <namespace>
kubectl get clusterroles,clusterrolebindings | grep <relevant-name>

# Describe specific binding
kubectl describe rolebinding <name> -n <namespace>
```

**Solutions:**
- Create Role/ClusterRole with required permissions
- Create RoleBinding/ClusterRoleBinding
- Verify binding references correct service account
- Use namespace-scoped roles when possible

---

## Debugging Tools Reference

### kubectl describe
Get detailed information about any resource including events.
```bash
kubectl describe pod <pod-name> -n <namespace>
kubectl describe node <node-name>
kubectl describe svc <service-name> -n <namespace>
kubectl describe deployment <name> -n <namespace>
```

### kubectl logs
View container stdout/stderr logs.
```bash
kubectl logs <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> -c <container-name>  # specific container
kubectl logs <pod-name> -n <namespace> --previous           # previous instance
kubectl logs <pod-name> -n <namespace> -f                   # follow/stream
kubectl logs <pod-name> -n <namespace> --tail=100           # last 100 lines
kubectl logs -l app=myapp -n <namespace>                    # by label selector
```

### kubectl exec
Execute commands inside running container.
```bash
kubectl exec -it <pod-name> -n <namespace> -- /bin/sh
kubectl exec -it <pod-name> -n <namespace> -- /bin/bash
kubectl exec <pod-name> -n <namespace> -- cat /etc/config/app.conf
kubectl exec <pod-name> -n <namespace> -c <container> -- env  # specific container
```

### kubectl debug
Debug nodes or pods with ephemeral containers (K8s 1.23+).
```bash
# Debug a running pod with ephemeral container
kubectl debug -it <pod-name> -n <namespace> --image=busybox --target=<container>

# Debug a node
kubectl debug node/<node-name> -it --image=busybox

# Create debug copy of pod with different image
kubectl debug <pod-name> -it --copy-to=debug-pod --container=app --image=busybox
```

### kubectl get events
View cluster events for troubleshooting.
```bash
kubectl get events -n <namespace>
kubectl get events -n <namespace> --sort-by='.lastTimestamp'
kubectl get events -n <namespace> --field-selector type=Warning
kubectl get events -n <namespace> -w  # watch for new events
kubectl get events -A --sort-by='.lastTimestamp' | tail -20  # cluster-wide recent
```

### kubectl top
View resource usage metrics (requires metrics-server).
```bash
kubectl top pods -n <namespace>
kubectl top pods -n <namespace> --sort-by=memory
kubectl top nodes
kubectl top pod <pod-name> -n <namespace> --containers
```

---

## The Four Phases of Kubernetes Debugging

### Phase 1: Gather Information
Start broad, then narrow down. Never assume the cause.

```bash
# Quick status overview
kubectl get pods,svc,deploy,rs -n <namespace>

# Recent events (often reveals the issue immediately)
kubectl get events -n <namespace> --sort-by='.lastTimestamp' | tail -20

# Describe the problematic resource
kubectl describe <resource-type> <name> -n <namespace>
```

### Phase 2: Check Logs and Metrics
Logs reveal application-level issues; metrics reveal resource issues.

```bash
# Application logs
kubectl logs <pod-name> -n <namespace> --tail=200
kubectl logs <pod-name> -n <namespace> --previous  # if crashed

# Resource metrics
kubectl top pod <pod-name> -n <namespace>
kubectl top nodes
```

### Phase 3: Interactive Investigation
Get inside the environment when logs aren't enough.

```bash
# Shell into the container
kubectl exec -it <pod-name> -n <namespace> -- /bin/sh

# Use ephemeral debug container
kubectl debug -it <pod-name> -n <namespace> --image=nicolaka/netshoot

# Check connectivity from inside
wget -qO- http://service-name:port
nslookup service-name
curl -v http://endpoint
```

### Phase 4: Validate and Fix
Make changes, verify they work, document the solution.

```bash
# Apply fix
kubectl apply -f fixed-manifest.yaml

# Watch for success
kubectl get pods -n <namespace> -w
kubectl get events -n <namespace> -w

# Verify health
kubectl logs <pod-name> -n <namespace> -f
```

---

## Quick Reference Commands

### Essential One-Liners
```bash
# Get all pods with their status across namespaces
kubectl get pods -A -o wide

# Find pods not in Running state
kubectl get pods -A --field-selector=status.phase!=Running

# Get pod restart counts
kubectl get pods -n <namespace> -o=custom-columns='NAME:.metadata.name,RESTARTS:.status.containerStatuses[0].restartCount'

# Show pod resource requests and limits
kubectl get pods -n <namespace> -o=custom-columns='NAME:.metadata.name,MEM_REQ:.spec.containers[0].resources.requests.memory,MEM_LIM:.spec.containers[0].resources.limits.memory'

# Get events sorted by time (most recent last)
kubectl get events --sort-by='.lastTimestamp' -n <namespace>

# Watch pods in real-time
kubectl get pods -n <namespace> -w

# Get logs from all pods with label
kubectl logs -l app=myapp -n <namespace> --all-containers=true

# Check endpoints for a service
kubectl get endpoints <service-name> -n <namespace>

# Test DNS resolution
kubectl run dnstest --rm -it --image=busybox --restart=Never -- nslookup <service-name>.<namespace>

# Check RBAC permissions
kubectl auth can-i --list --as=system:serviceaccount:<namespace>:<sa-name>
```

### Debugging Network Issues
```bash
# Run network debug pod
kubectl run netshoot --rm -it --image=nicolaka/netshoot -- /bin/bash

# Test service connectivity
kubectl run curl --rm -it --image=curlimages/curl -- curl -v http://<service>:<port>

# Check CoreDNS logs
kubectl logs -n kube-system -l k8s-app=kube-dns

# Trace network path
kubectl exec -it <pod> -- traceroute <destination>
```

### Debugging Storage Issues
```bash
# List all PVCs with status
kubectl get pvc -A

# Describe PVC for binding issues
kubectl describe pvc <name> -n <namespace>

# Check storage provisioner logs
kubectl logs -n kube-system -l app=<provisioner-name>

# Verify mount inside pod
kubectl exec -it <pod> -n <namespace> -- df -h
kubectl exec -it <pod> -n <namespace> -- ls -la /path/to/mount
```

---

## Useful Debug Images

| Image | Use Case |
|-------|----------|
| `busybox` | Basic shell, networking tools |
| `nicolaka/netshoot` | Comprehensive network debugging |
| `curlimages/curl` | HTTP testing |
| `alpine` | Minimal Linux with package manager |
| `gcr.io/kubernetes-e2e-test-images/jessie-dnsutils` | DNS debugging |

---

## Prevention Best Practices

1. **Always set resource requests and limits** - Prevents noisy neighbor issues and OOMKilled
2. **Configure proper health probes** - Liveness, readiness, and startup probes with appropriate delays
3. **Use namespaces** - Isolate workloads for easier debugging
4. **Label everything** - Makes filtering and selection reliable
5. **Implement monitoring** - Prometheus, Grafana, ELK stack for visibility
6. **Validate manifests before deployment** - Use kubeval, kube-linter, or similar tools
7. **Use GitOps** - Track changes and enable rollback
8. **Document runbooks** - For common issues specific to your applications
