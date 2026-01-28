---
name: kubernetes
description: |-
  Production-grade Kubernetes manifests and debugging for containerized applications.
  This skill should be used when users ask to deploy to Kubernetes, create K8s manifests,
  containerize for K8s, set up Deployments/Services/Jobs/StatefulSets/CronJobs, create
  namespaces with resource quotas, set up multi-team isolation, configure ResourceQuota/
  LimitRange, secure with RBAC (ServiceAccount, Role, RoleBinding), configure init
  containers (model download, db wait, migrations), set up sidecars (logging, metrics),
  or debug pods (CrashLoopBackOff, logs, exec, describe, events). Auto-detects from
  Dockerfile/code, generates hardened manifests with educational comments. CKAD-aligned.
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "bash \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/verify-kubectl-context.sh"
---

# Kubernetes

Production-grade K8s manifests with security-first defaults and educational comments.

---

## Resource Detection & Adaptation

**Before generating manifests, detect the target environment:**

```bash
# Detect node resources
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}: {.status.capacity.memory}, {.status.capacity.cpu}{"\n"}{end}'

# Detect if Docker Desktop (local) or real cluster
kubectl get nodes -o jsonpath='{.items[0].metadata.labels.node\.kubernetes\.io/instance-type}' 2>/dev/null || echo "local"

# Detect available resources
kubectl describe nodes | grep -A 5 "Allocated resources"
```

**Adapt configurations based on detection:**

| Detected Environment | Profile | Default Limits | Agent Action |
|---------------------|---------|----------------|--------------|
| Docker Desktop < 6GB | Minimal | 128Mi-256Mi | Warn, reduce replicas |
| Docker Desktop 6-10GB | Standard | 256Mi-512Mi | Normal deployment |
| Cloud/Real cluster | Production | Based on node size | Full features |

### Agent Behavior

1. **Detect** cluster type and resources before generating manifests
2. **Adapt** resource requests/limits to cluster capacity
3. **Warn** if requested workload exceeds available resources
4. **Calculate** safe limits: `(node_memory * 0.7) / expected_pod_count`

### Adaptive Resource Templates

**Local/Constrained (< 6GB allocatable):**
```yaml
resources:
  requests:
    memory: 128Mi
    cpu: 100m
  limits:
    memory: 256Mi
    cpu: 500m
```

**Standard (6-16GB allocatable):**
```yaml
resources:
  requests:
    memory: 256Mi
    cpu: 100m
  limits:
    memory: 512Mi
    cpu: 1000m
```

**Production (> 16GB or cloud):**
```yaml
resources:
  requests:
    memory: 512Mi
    cpu: 250m
  limits:
    memory: 1Gi
    cpu: 2000m
```

### Pre-Deployment Validation

Before applying manifests, agent should verify:
```bash
# Check if deployment would exceed node capacity
kubectl get nodes -o jsonpath='{.items[0].status.allocatable.memory}'
```

If insufficient: warn user and suggest scaling down or increasing Docker Desktop resources.

---

## What This Skill Does

**Analysis & Detection:**
- Auto-detects from Dockerfile: ports, health endpoints, resources
- Identifies workload type from project structure
- Reads existing manifests to understand patterns
- Detects GPU requirements from dependencies

**Generation:**
- Creates production-hardened manifests (non-root, read-only, resource limits)
- Generates all supporting resources (Service, ConfigMap, HPA, PDB)
- Creates namespace governance (ResourceQuota, LimitRange, NetworkPolicy)
- Supports multi-team isolation with environment progression (dev → staging → prod)
- Adds educational comments explaining WHY each config choice
- Outputs ArgoCD-compatible directory structure

**Validation:**
- Verifies kubectl context exists
- Creates namespace if needed
- Deploys to local cluster (kind/minikube)
- Confirms pods are running before delivering

**Security:**
- Non-root user by default (runAsNonRoot: true)
- Read-only root filesystem
- No privilege escalation
- Dropped capabilities
- Resource limits always set
- **Unprivileged ports only** (>=1024) - privileged ports (<1024) require root

## What This Skill Does NOT Do

- Generate Helm charts (document in references for future)
- Create Kustomize overlays (document in references for future)
- Handle Dapr sidecar injection (separate skill)
- Deploy Kafka/Strimzi operators (separate skill)
- Generate ArgoCD Application CRDs (separate skill)

---

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Dockerfile, existing manifests, port/health patterns |
| **Conversation** | Target environment, namespace, special requirements |
| **Skill References** | Security contexts, health probes, resource limits |
| **User Guidelines** | Cluster conventions, naming standards |

---

## Required Clarifications

After auto-detection, confirm with user if ambiguous:

| Question | When to Ask |
|----------|-------------|
| Target environment | "Deploying to local (kind/minikube) or remote cluster?" |
| Namespace | "Use existing namespace or create new?" |
| Image availability | "Is image in registry or needs to be built/loaded?" |
| Service exposure | "Internal only (ClusterIP) or external access needed?" |
| Namespace governance | "Need ResourceQuota/LimitRange for resource isolation?" |
| Multi-team setup | "Single team or multi-team with namespace isolation?" |
| Environment progression | "Creating dev/staging/prod namespaces with quota progression?" |

---

## Pre-flight Checks (CRITICAL)

Before generating manifests, verify:

```bash
# 1. Cluster access
kubectl cluster-info

# 2. Current context
kubectl config current-context

# 3. Target namespace (create if needed)
kubectl get namespace $NAMESPACE || kubectl create namespace $NAMESPACE

# 4. Image exists (or build it)
docker images | grep $IMAGE_NAME || docker build -t $IMAGE_NAME .

# 5. For local clusters: load image
kind load docker-image $IMAGE_NAME  # or minikube image load
```

**If any check fails → stop and report. Don't generate manifests for broken state.**

---

## Auto-Detection Matrix

### From Dockerfile

| Detect | How | Example |
|--------|-----|---------|
| **Port** | EXPOSE instruction | `EXPOSE 8000` → containerPort: 8000 |
| **Health** | CMD with health endpoint | `uvicorn` → /health or /healthz |
| **User** | USER instruction | `USER 1000` → runAsUser: 1000 |
| **Workdir** | WORKDIR instruction | Context for volume mounts |

### Port Selection (CRITICAL for Security)

**Privileged ports (<1024) conflict with `runAsNonRoot: true`.**

| Detected Port | Action |
|---------------|--------|
| 80, 443 | ⚠️ Use unprivileged variant (nginx-unprivileged:8080) or remap |
| 8080, 8000, 3000+ | ✅ Compatible with non-root |

**Common remappings:**
| Standard Image | Security-Compatible Alternative |
|----------------|--------------------------------|
| `nginx` (port 80) | `nginxinc/nginx-unprivileged` (port 8080) |
| `httpd` (port 80) | Configure `Listen 8080` or use unprivileged image |
| `redis` (port 6379) | ✅ Already unprivileged |
| `postgres` (port 5432) | ✅ Already unprivileged |

**Service abstracts this:** Service `port: 80` → `targetPort: 8080` keeps external API stable.

### From Code

| Detect | How | Example |
|--------|-----|---------|
| **Framework health** | Route definitions | FastAPI `/health`, Express `/healthz` |
| **Readiness** | DB connection check | `/health/ready` with DB ping |
| **Startup time** | Heavy imports | ML models → startupProbe needed |

### Workload Type Decision

```
Is this a one-time task that completes?
  → Job (or CronJob if scheduled)

Does it need stable network identity or ordered deployment?
  → StatefulSet

Must run on every node?
  → DaemonSet

Otherwise → Deployment (default)
```

---

## Workflow

```
1. PRE-FLIGHT
   - Verify kubectl context
   - Check namespace exists
   - Verify image exists or build it
         ↓
2. ANALYZE PROJECT
   - Read Dockerfile for EXPOSE, HEALTHCHECK, USER
   - Scan code for health endpoints
   - Check existing k8s/ directory
   - Detect GPU requirements (torch, tensorflow)
         ↓
3. DETERMINE WORKLOAD TYPE
   - Deployment (default)
   - Job/CronJob (batch processing)
   - StatefulSet (databases, ordered)
   - DaemonSet (node-level agents)
         ↓
4. GENERATE MANIFESTS
   - Deployment/Job/StatefulSet with hardened security
   - Service (ClusterIP, NodePort, or LoadBalancer)
   - ConfigMap for non-secret config
   - HPA if autoscaling needed
   - PDB for availability
   - All with educational comments
         ↓
5. VALIDATE
   - kubectl apply --dry-run=server
   - kubectl apply -n $NAMESPACE
   - kubectl wait --for=condition=Ready pod
   - kubectl logs to verify startup
         ↓
6. DELIVER
   - Files in k8s/base/ directory
   - Summary of what was created
   - Next steps for production
```

---

## Generated Directory Structure

```
k8s/
├── base/                         # Raw manifests (ArgoCD-compatible)
│   ├── namespace.yaml            # Optional, if new namespace
│   ├── resourcequota.yaml        # Namespace-wide resource caps
│   ├── limitrange.yaml           # Per-container defaults and bounds
│   ├── networkpolicy.yaml        # Namespace isolation rules
│   ├── deployment.yaml           # Or job.yaml, statefulset.yaml
│   ├── service.yaml              # ClusterIP by default
│   ├── configmap.yaml            # Non-secret configuration
│   ├── hpa.yaml                  # If autoscaling enabled
│   ├── pdb.yaml                  # Pod Disruption Budget
│   └── kustomization.yaml        # For future Kustomize use
└── README.md                     # Deployment instructions
```

---

## Manifest Patterns

### Deployment (Default)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${APP_NAME}
  labels:
    # Standard K8s labels (see references/labels-annotations.md)
    app.kubernetes.io/name: ${APP_NAME}
    app.kubernetes.io/instance: ${APP_NAME}-${ENV}
    app.kubernetes.io/version: "${VERSION}"
    app.kubernetes.io/component: api  # or worker, frontend
    app.kubernetes.io/part-of: ${PROJECT}
    app.kubernetes.io/managed-by: kubectl
spec:
  replicas: 2  # WHY: Minimum for availability during rolling updates
  selector:
    matchLabels:
      app.kubernetes.io/name: ${APP_NAME}
  template:
    metadata:
      labels:
        app.kubernetes.io/name: ${APP_NAME}
    spec:
      # WHY: Security hardening - never run as root
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
      containers:
      - name: ${APP_NAME}
        image: ${IMAGE}:${TAG}
        # WHY: Never use :latest - breaks reproducibility
        imagePullPolicy: IfNotPresent
        ports:
        # WHY: Port must be >=1024 for runAsNonRoot (privileged ports need root)
        # Use Service port:80 → targetPort:8080 to expose standard ports externally
        - containerPort: ${PORT}  # Must be >=1024 (e.g., 8080, 8000, 3000)
          protocol: TCP
        # WHY: Container-level security context
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop: ["ALL"]
        # WHY: Prevent resource starvation, enable HPA
        resources:
          requests:
            cpu: "100m"      # 0.1 CPU cores
            memory: "128Mi"
          limits:
            cpu: "500m"      # 0.5 CPU cores
            memory: "512Mi"
        # WHY: K8s restarts if app deadlocks
        livenessProbe:
          httpGet:
            path: /health/live
            port: ${PORT}
          initialDelaySeconds: 10
          periodSeconds: 15
          failureThreshold: 3
        # WHY: Only route traffic when ready
        readinessProbe:
          httpGet:
            path: /health/ready
            port: ${PORT}
          initialDelaySeconds: 5
          periodSeconds: 10
        # WHY: Slow-starting apps (ML models) need longer startup
        startupProbe:
          httpGet:
            path: /health/live
            port: ${PORT}
          initialDelaySeconds: 0
          periodSeconds: 10
          failureThreshold: 30  # 5 minutes to start
        # WHY: Graceful shutdown for in-flight requests
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 5"]
        # WHY: Allow time for graceful shutdown
      terminationGracePeriodSeconds: 30
```

### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ${APP_NAME}
  labels:
    app.kubernetes.io/name: ${APP_NAME}
spec:
  # WHY: ClusterIP is safest default - internal only
  # Use NodePort for dev/testing, LoadBalancer for prod external access
  type: ClusterIP
  ports:
  # WHY: Service abstracts internal port - clients connect to :80, Pod runs on :8080
  # This allows standard external ports while container runs unprivileged
  - port: 80              # WHY: Service port (what clients connect to)
    targetPort: ${PORT}   # WHY: Pod port (>=1024, e.g., 8080)
    protocol: TCP
    name: http
  selector:
    # CRITICAL: Must EXACTLY match Pod template labels from Deployment
    # Mismatch = zero endpoints = Service routes to nothing
    app.kubernetes.io/name: ${APP_NAME}
```

**Verify Service→Pod connection**: `kubectl get endpoints ${APP_NAME}`
- Shows Pod IPs if selector matches
- Shows `<none>` if selector MISMATCHES Pod labels

---

## Security Context (Always Applied)

See `references/security-contexts.md` for full patterns.

```yaml
# Pod level
securityContext:
  runAsNonRoot: true           # WHY: Never run as root
  runAsUser: 1000              # WHY: Consistent non-root UID
  runAsGroup: 1000             # WHY: Consistent GID
  fsGroup: 1000                # WHY: Volume permissions
  seccompProfile:
    type: RuntimeDefault       # WHY: Block dangerous syscalls

# Container level
securityContext:
  allowPrivilegeEscalation: false  # WHY: Prevent root escalation
  readOnlyRootFilesystem: true     # WHY: Immutable container
  capabilities:
    drop: ["ALL"]                  # WHY: Minimal capabilities
```

---

## Output Checklist

Before delivering, verify:

### Pre-flight
- [ ] kubectl context is valid
- [ ] Namespace exists or was created
- [ ] Image exists locally or in registry
- [ ] For kind/minikube: image loaded into cluster

### Manifests
- [ ] All manifests have `app.kubernetes.io/*` labels
- [ ] Security context applied (runAsNonRoot, readOnlyRootFilesystem)
- [ ] **containerPort >= 1024** (privileged ports incompatible with runAsNonRoot)
- [ ] Resource requests AND limits defined
- [ ] Liveness and readiness probes configured
- [ ] No hardcoded secrets (use Secret references or env vars)

### Namespace Governance (if applicable)
- [ ] ResourceQuota sets namespace-wide CPU/memory/pod limits
- [ ] LimitRange provides default requests/limits for containers
- [ ] LimitRange max prevents single container from consuming quota
- [ ] NetworkPolicy isolates namespace (default-deny + explicit allows)
- [ ] Monitoring namespace allowed to scrape metrics

### Validation
- [ ] `kubectl apply --dry-run=server` passes
- [ ] Deployed to cluster successfully
- [ ] Pods reach Running state
- [ ] Health endpoints respond
- [ ] Service has endpoints (`kubectl get endpoints` shows Pod IPs, not `<none>`)

### Documentation
- [ ] Comments explain WHY for each config choice
- [ ] README.md with deployment instructions

---

## Reference Files

### Always Read First

| File | Purpose |
|------|---------|
| `references/security-contexts.md` | **CRITICAL**: Hardened security patterns |
| `references/health-probes.md` | **CRITICAL**: Liveness/readiness/startup |
| `references/resource-limits.md` | **CRITICAL**: CPU/memory guidance |
| `references/namespace-governance.md` | **CRITICAL**: ResourceQuota, LimitRange, NetworkPolicy, multi-team isolation |

### Debugging & Operations

| File | When to Read |
|------|--------------|
| `references/debugging-workflow.md` | **CRITICAL**: CrashLoopBackOff, command safety, logs, exec, debug containers |
| `references/deployment-gotchas.md` | **CRITICAL**: Architecture mismatch, ImagePull failures, pre-deploy validation, Helm gotchas |
| `references/networking-patterns.md` | **DEBUGGING**: Service has no endpoints, selector mismatch, DNS issues |
| `references/control-plane.md` | **DEBUGGING**: When deployments fail, pods stuck, rollback needed |

### Workload-Specific

| File | When to Read |
|------|--------------|
| `references/workload-types.md` | Choosing Deployment vs Job vs StatefulSet |
| `references/init-sidecar-patterns.md` | Init containers (model download, db wait), sidecars (logging, metrics) |
| `references/autoscaling-patterns.md` | HPA, custom metrics, KEDA |
| `references/gpu-workloads.md` | AI/ML workloads with GPU |
| `references/keda-patterns.md` | Event-driven scale-to-zero |

### Infrastructure

| File | When to Read |
|------|--------------|
| `references/networking-patterns.md` | Service types, Ingress, mesh |
| `references/storage-patterns.md` | PVC, ephemeral, shared storage |
| `references/configmap-patterns.md` | ConfigMap creation, env vars, volumes, hot-reload |
| `references/secrets-patterns.md` | ESO, Sealed Secrets, K8s Secrets |
| `references/rbac-patterns.md` | **SECURITY**: ServiceAccount, Role, RoleBinding, least privilege |
| `references/labels-annotations.md` | Standard labels, ArgoCD compat |
