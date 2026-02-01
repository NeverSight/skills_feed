---
name: kubernetes-health-check
description: Verify Kubernetes cluster health, resource availability, and readiness before deploying applications
allowed-tools: bash_tool
---

# Kubernetes Health Check

## Purpose
Perform comprehensive health checks on Kubernetes clusters to ensure readiness for application deployments. Validates cluster connectivity, resource availability, and essential components.

## Prerequisites
- kubectl installed and configured
- Access to Kubernetes cluster (Minikube, cloud cluster, etc.)
- Sufficient permissions to query cluster resources

## Instructions

### Step 1: Verify Cluster Connectivity

Check if kubectl can connect to the cluster:
```bash
# Check cluster info
kubectl cluster-info

# Verify current context
kubectl config current-context

# List all nodes
kubectl get nodes
```

**Expected Results:**
- Cluster-info shows running control plane
- At least one node in `Ready` state
- No connection errors

### Step 2: Check Node Resources

Verify sufficient resources are available:
```bash
# Get detailed node information
kubectl describe nodes

# Check resource usage (requires metrics-server)
kubectl top nodes
```

**Minimum Requirements:**
- CPU: >2 cores available
- Memory: >4GB available
- Disk: >20GB available
- Status: All nodes `Ready`

### Step 3: Verify System Components

Ensure essential Kubernetes components are running:
```bash
# Check system pods
kubectl get pods -n kube-system

# Check critical components
kubectl get pods -n kube-system | grep -E 'coredns|etcd|kube-apiserver|kube-controller|kube-scheduler'
```

**All pods should be:**
- Status: `Running`
- Restarts: <3 (some restarts normal during startup)
- Ready: All containers ready (e.g., 1/1, 2/2)

### Step 4: Validate Storage

Verify storage classes are available:
```bash
# List storage classes
kubectl get storageclass

# Check for default storage class
kubectl get storageclass -o json | jq -r '.items[] | select(.metadata.annotations."storageclass.kubernetes.io/is-default-class"=="true") | .metadata.name'
```

**Requirements:**
- At least one storage class exists
- One marked as `(default)`

### Step 5: Test Networking

Validate cluster networking:
```bash
# Check kube-proxy
kubectl get pods -n kube-system | grep kube-proxy

# Verify DNS resolution
kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup kubernetes.default

# Check CNI plugin
kubectl get pods -n kube-system | grep -E 'calico|flannel|weave|cilium'
```

**Networking is healthy when:**
- kube-proxy pods running
- DNS lookups succeed
- CNI plugin pods running

## Validation

Pre-deployment checks passed when:
- [ ] kubectl connects successfully
- [ ] All nodes are Ready
- [ ] System pods running (coredns, etcd, kube-apiserver)
- [ ] Default storage class exists
- [ ] DNS resolution works
- [ ] Resources meet requirements (2 CPU, 4GB RAM)

## Troubleshooting

**Problem**: Cannot connect to cluster
```bash
kubectl config get-contexts
kubectl config use-context <correct-context>

# For Minikube
minikube status
minikube start
```

**Problem**: Nodes NotReady
```bash
kubectl describe node <node-name>

# Restart Minikube with more resources
minikube stop
minikube start --cpus=4 --memory=8192
```

## Best Practices

1. **Always Check First**: Run health checks before any deployment
2. **Save Reports**: Keep health reports for troubleshooting
3. **Automate**: Add to CI/CD pipelines
4. **Monitor Trends**: Track resource usage over time
5. **Document Baseline**: Know what "healthy" looks like
