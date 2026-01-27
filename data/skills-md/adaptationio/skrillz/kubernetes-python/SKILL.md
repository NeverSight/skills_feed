---
name: kubernetes-python
description: Kubernetes Python client for programmatic cluster management. Use when working with Kubernetes API, managing pods, deployments, services, namespaces, configmaps, secrets, jobs, CRDs, EKS clusters, watching resources, automating K8s operations, or building Kubernetes controllers.
---

# Kubernetes Python Client Skill

Official Python client library for Kubernetes, providing programmatic access to the Kubernetes API for automation, custom tooling, and application integration.

## Quick Start

### Installation

```bash
pip install kubernetes
```

### Basic Usage

```python
from kubernetes import client, config

# Load kubeconfig
config.load_kube_config()

# Create API client
v1 = client.CoreV1Api()

# List pods
pods = v1.list_pod_for_all_namespaces(limit=10)
for pod in pods.items:
    print(f"{pod.metadata.namespace}/{pod.metadata.name}")
```

## Core Concepts

### Client Initialization Patterns

**Local Development** (using kubeconfig):
```python
from kubernetes import client, config

config.load_kube_config()
v1 = client.CoreV1Api()
```

**In-Cluster** (running inside Kubernetes):
```python
from kubernetes import client, config

config.load_incluster_config()
v1 = client.CoreV1Api()
```

**Specific Context**:
```python
config.load_kube_config(context='production-cluster')
v1 = client.CoreV1Api()
```

### API Clients by Resource Type

| API Client | Resources | Usage |
|-----------|-----------|-------|
| `CoreV1Api` | Pods, Services, ConfigMaps, Secrets, Namespaces, PVCs | `client.CoreV1Api()` |
| `AppsV1Api` | Deployments, StatefulSets, DaemonSets, ReplicaSets | `client.AppsV1Api()` |
| `BatchV1Api` | Jobs, CronJobs | `client.BatchV1Api()` |
| `NetworkingV1Api` | Ingresses, NetworkPolicies | `client.NetworkingV1Api()` |
| `CustomObjectsApi` | Custom Resources (CRDs) | `client.CustomObjectsApi()` |

## Common Operations

### Creating a Deployment

```python
from kubernetes import client

apps_v1 = client.AppsV1Api()

deployment = client.V1Deployment(
    metadata=client.V1ObjectMeta(name="nginx-deployment"),
    spec=client.V1DeploymentSpec(
        replicas=3,
        selector=client.V1LabelSelector(
            match_labels={"app": "nginx"}
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": "nginx"}),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="nginx",
                        image="nginx:1.14.2",
                        ports=[client.V1ContainerPort(container_port=80)]
                    )
                ]
            )
        )
    )
)

apps_v1.create_namespaced_deployment(
    namespace="default",
    body=deployment
)
```

### Reading Resources

```python
# Read single pod
pod = v1.read_namespaced_pod(name="my-pod", namespace="default")

# List pods with label selector
pods = v1.list_namespaced_pod(
    namespace="default",
    label_selector="app=nginx,env=production"
)

# List pods with field selector
running_pods = v1.list_namespaced_pod(
    namespace="default",
    field_selector="status.phase=Running"
)
```

### Updating Resources

**Patch** (partial update, preferred):
```python
deployment = apps_v1.read_namespaced_deployment(
    name="nginx-deployment",
    namespace="default"
)

deployment.spec.replicas = 5

apps_v1.patch_namespaced_deployment(
    name="nginx-deployment",
    namespace="default",
    body=deployment
)
```

**Replace** (full update):
```python
deployment.metadata.resource_version = existing.metadata.resource_version
apps_v1.replace_namespaced_deployment(
    name="nginx-deployment",
    namespace="default",
    body=deployment
)
```

### Deleting Resources

```python
v1.delete_namespaced_pod(
    name="my-pod",
    namespace="default"
)

# Delete with grace period
apps_v1.delete_namespaced_deployment(
    name="nginx-deployment",
    namespace="default",
    grace_period_seconds=30
)
```

## Error Handling

```python
from kubernetes.client.rest import ApiException

try:
    pod = v1.read_namespaced_pod(name="my-pod", namespace="default")
except ApiException as e:
    if e.status == 404:
        print("Pod not found")
    elif e.status == 403:
        print("Permission denied")
    else:
        print(f"API error: {e}")
```

### Create or Update Pattern (Idempotent)

```python
from kubernetes.client.rest import ApiException

def create_or_update_deployment(apps_v1, namespace, deployment):
    """Create deployment if it doesn't exist, otherwise update it."""
    name = deployment.metadata.name

    try:
        existing = apps_v1.read_namespaced_deployment(
            name=name,
            namespace=namespace
        )

        deployment.metadata.resource_version = existing.metadata.resource_version
        response = apps_v1.replace_namespaced_deployment(
            name=name,
            namespace=namespace,
            body=deployment
        )
        print(f"Deployment {name} updated")
        return response

    except ApiException as e:
        if e.status == 404:
            response = apps_v1.create_namespaced_deployment(
                namespace=namespace,
                body=deployment
            )
            print(f"Deployment {name} created")
            return response
        else:
            raise
```

## Watch Resources

Watch for resource changes in real-time:

```python
from kubernetes import watch

w = watch.Watch()

# Watch pods with timeout
for event in w.stream(
    v1.list_namespaced_pod,
    namespace="default",
    timeout_seconds=60
):
    print(f"{event['type']}: {event['object'].metadata.name}")

w.stop()
```

### Event Types

- `ADDED`: Resource was created
- `MODIFIED`: Resource was updated
- `DELETED`: Resource was deleted
- `ERROR`: Watch error occurred

## Working with ConfigMaps and Secrets

### ConfigMap

```python
configmap = client.V1ConfigMap(
    metadata=client.V1ObjectMeta(name="my-config"),
    data={"key1": "value1", "key2": "value2"}
)

v1.create_namespaced_config_map(
    namespace="default",
    body=configmap
)
```

### Secret

```python
import base64

secret = client.V1Secret(
    metadata=client.V1ObjectMeta(name="my-secret"),
    type="Opaque",
    data={
        "username": base64.b64encode(b"admin").decode('utf-8'),
        "password": base64.b64encode(b"secretpass").decode('utf-8')
    }
)

v1.create_namespaced_secret(
    namespace="default",
    body=secret
)
```

## Custom Resources (CRDs)

```python
custom_api = client.CustomObjectsApi()

# List custom resources
custom_objects = custom_api.list_namespaced_custom_object(
    group="example.com",
    version="v1",
    namespace="default",
    plural="mycustomresources"
)

# Create custom resource
custom_object = {
    "apiVersion": "example.com/v1",
    "kind": "MyCustomResource",
    "metadata": {"name": "my-cr"},
    "spec": {"replicas": 3}
}

custom_api.create_namespaced_custom_object(
    group="example.com",
    version="v1",
    namespace="default",
    plural="mycustomresources",
    body=custom_object
)
```

## Production Patterns

### Timeout Configuration

```python
# Set timeout for operations
pods = v1.list_namespaced_pod(
    namespace="default",
    _request_timeout=10  # 10 second timeout
)
```

### Pagination for Large Lists

```python
def list_all_pods_paginated(namespace, page_size=100):
    """List all pods with pagination."""
    all_pods = []
    continue_token = None

    while True:
        if continue_token:
            response = v1.list_namespaced_pod(
                namespace=namespace,
                limit=page_size,
                _continue=continue_token
            )
        else:
            response = v1.list_namespaced_pod(
                namespace=namespace,
                limit=page_size
            )

        all_pods.extend(response.items)

        continue_token = response.metadata._continue
        if not continue_token:
            break

    return all_pods
```

### Server-Side Filtering

```python
# Good: Filter server-side (efficient)
running_pods = v1.list_pod_for_all_namespaces(
    field_selector='status.phase=Running'
)

# Bad: Fetch all and filter client-side (inefficient)
all_pods = v1.list_pod_for_all_namespaces()
running_pods = [p for p in all_pods.items if p.status.phase == 'Running']
```

## Reference Documentation

For detailed information, see:

- **[Client Setup](references/client-setup.md)**: Authentication methods, EKS integration, configuration
- **[Resource Operations](references/resource-operations.md)**: Comprehensive CRUD patterns for all resource types
- **[Watch Patterns](references/watch-patterns.md)**: Advanced watch patterns, resilient loops, async operations

## Key Features

### Strengths
- Official Kubernetes client (SIG API Machinery)
- Complete API coverage (all resources)
- Production-ready and battle-tested
- Multiple authentication methods
- Real-time watch/stream capabilities
- Full CRD support

### Considerations
- Auto-generated code (less Pythonic)
- Performance can degrade in very large clusters (3000+ resources)
- No native async support (use `kubernetes_asyncio` package)
- EKS requires manual token refresh (15-minute expiry)

## Version Compatibility

Match client version to Kubernetes cluster version:

| Client Version | K8s 1.29 | K8s 1.30 | K8s 1.31 |
|---------------|----------|----------|----------|
| 29.y.z        | ✓        | +-       | -        |
| 30.y.z        | +-       | ✓        | +-       |
| 31.y.z        | +-       | +-       | ✓        |

- ✓ = Exact feature/API parity
- +- = Most APIs work, some new/removed
- \- = Not recommended

## Security Best Practices

1. **Least Privilege**: Never use cluster-admin for applications
2. **RBAC**: Use Roles (namespaced) instead of ClusterRoles when possible
3. **Secrets**: Don't log secret data, load credentials from environment
4. **SSL Verification**: Always verify SSL in production (`verify_ssl=True`)
5. **In-Cluster Config**: Use service accounts for in-cluster applications

## Quick Reference Links

- GitHub: https://github.com/kubernetes-client/python
- Documentation: https://kubernetes.readthedocs.io/
- PyPI: https://pypi.org/project/kubernetes/
- Examples: https://github.com/kubernetes-client/python/tree/master/examples
