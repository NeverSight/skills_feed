---
name: crossplane-debug
description: Debug Crossplane compositions, functions (KCL, Go templates, patch-and-transform, auto-ready), and managed resources. Use when troubleshooting composition rendering issues, function errors, resource creation failures, dependency problems, or claim status issues. Supports remote cluster debugging when composition files are not available locally. Triggers on keywords like "crossplane", "composition", "XR", "claim", "function-kcl", "managed resource", or when debugging Kubernetes resources created by Crossplane.
metadata:
  author: kanzifucius
  version: "1.0.0"
  tags:
    - crossplane
    - kubernetes
    - debugging
    - kcl
    - composition
---

# Crossplane Composition Debugging

Debug Crossplane compositions and functions by systematically identifying issues in rendering, function execution, and resource provisioning.

## Debugging Decision Tree

```
Issue reported
    |
    v
Do you have composition files locally?
    |
    +--NO--> Extract from cluster first
    |        Run: scripts/extract-composition.sh
    |        See: "Remote Cluster Debugging"
    |
    +--YES--> Is the composition rendering correctly?
                 |
                 +--NO--> Run `crossplane beta render` locally
                 |        See: "Local Render Debugging"
                 |
                 +--YES--> Are resources being created in the cluster?
                              |
                              +--NO--> Check XR/Claim status and events
                              |        Run `crossplane beta trace`
                              |        See: "Cluster Debugging"
                              |
                              +--YES--> Are resources in Ready state?
                                           |
                                           +--NO--> Check managed resource conditions
                                           |        See: "Resource Status Debugging"
                                           |
                                           +--YES--> Issue is external to Crossplane
```

## Remote Cluster Debugging

When compositions and functions are deployed to a remote cluster and you don't have the source files locally.

### Quick Extract (Using Script)

Run the extraction script to pull all files needed for local debugging:

```bash
# Extract composition, functions, and sample XR for debugging
./scripts/extract-composition.sh <composition-name> [xr-kind] [xr-name]

# Examples:
./scripts/extract-composition.sh my-database-composition
./scripts/extract-composition.sh my-app-composition XMyApp my-app-instance
```

This creates a `debug-<composition-name>/` directory with all files needed for `crossplane beta render`.

### Manual Extraction

#### 1. Extract Composition

```bash
# List available compositions
kubectl get compositions

# Extract specific composition
kubectl get composition <name> -o yaml > composition.yaml
```

#### 2. Extract Function Definitions

```bash
# List installed functions
kubectl get functions

# Extract all functions to single file
kubectl get functions -o yaml > functions.yaml

# Or extract specific function
kubectl get function <name> -o yaml >> functions.yaml
```

#### 3. Extract Sample XR/Claim

```bash
# Find XRs using this composition
kubectl get <xr-kind> -A

# Extract an XR as sample input (clean up status for render)
kubectl get <xr-kind> <name> -o yaml | \
  yq 'del(.status) | del(.metadata.resourceVersion) | del(.metadata.uid) | del(.metadata.generation) | del(.metadata.creationTimestamp) | del(.metadata.managedFields)' \
  > xr.yaml
```

#### 4. View Inline KCL Code

For compositions with embedded KCL, extract and view the code:

```bash
# View all pipeline steps and their inputs
kubectl get composition <name> -o jsonpath='{.spec.pipeline}' | jq

# Extract KCL source from specific step (adjust index [0] as needed)
kubectl get composition <name> -o jsonpath='{.spec.pipeline[0].input.source}' 

# Pretty print KCL from inline composition
kubectl get composition <name> -o json | \
  jq -r '.spec.pipeline[] | select(.functionRef.name == "function-kcl") | .input.source'
```

### View Function Logs in Cluster

```bash
# Find function pods
kubectl get pods -n crossplane-system -l pkg.crossplane.io/function

# Logs for specific function
kubectl logs -n crossplane-system -l pkg.crossplane.io/function=function-kcl -f --tail=100

# All function logs
kubectl logs -n crossplane-system -l pkg.crossplane.io/revision --tail=50
```

### Debug Without Local Functions

If you can't run functions locally, use cluster-side debugging:

```bash
# 1. Check function health
kubectl get functions
kubectl describe function <name>

# 2. Check function pod status
kubectl get pods -n crossplane-system -l pkg.crossplane.io/function=<name>

# 3. View function errors in XR events
kubectl describe <xr-kind> <xr-name> | grep -A5 "Events:"

# 4. Check crossplane core logs for function errors
kubectl logs -n crossplane-system deploy/crossplane --tail=100 | grep -i function
```

## Local Render Debugging

Use `crossplane beta render` to test composition rendering without applying to cluster.

### Basic Render Command

```bash
crossplane beta render <xr-file.yaml> <composition.yaml> <functions.yaml>
```

**Required files:**
- `xr-file.yaml` - Example XR or Claim with spec values
- `composition.yaml` - The Composition to test  
- `functions.yaml` - Function definitions (can combine multiple)

### Functions File for Cluster-Deployed Functions

When functions are in the cluster but not running locally, use `Default` runtime to pull from registry:

```yaml
---
apiVersion: pkg.crossplane.io/v1beta1
kind: Function
metadata:
  name: function-kcl
  annotations:
    render.crossplane.io/runtime: Default
---
apiVersion: pkg.crossplane.io/v1beta1
kind: Function
metadata:
  name: function-auto-ready
  annotations:
    render.crossplane.io/runtime: Default
```

### Functions File for Local Development

When running functions locally in Docker:

```yaml
---
apiVersion: pkg.crossplane.io/v1beta1
kind: Function
metadata:
  name: function-kcl
  annotations:
    render.crossplane.io/runtime: Development
    render.crossplane.io/runtime-development-target: localhost:9443
---
apiVersion: pkg.crossplane.io/v1beta1
kind: Function
metadata:
  name: function-auto-ready
```

### Running KCL Function Locally

Start the KCL function in development mode:

```bash
# Terminal 1: Run KCL function server
docker run --rm -p 9443:9443 xpkg.upbound.io/crossplane-contrib/function-kcl:latest --insecure --debug
```

```bash
# Terminal 2: Render with local function
crossplane beta render xr.yaml composition.yaml functions.yaml
```

### Interpreting Render Output

The output shows the desired state after all functions run. Check for:

1. **Missing resources** - Function didn't generate expected output
2. **Wrong resource values** - Function logic error
3. **Function errors** - Check stderr for stack traces

### Common Render Issues

| Symptom | Likely Cause | Action |
|---------|--------------|--------|
| Empty output | Function not matched or no resources generated | Check function name matches pipeline step |
| KCL syntax error | Invalid KCL in composition | See references/kcl-patterns.md |
| "function not found" | Function not in functions.yaml | Add function definition |
| Wrong resource apiVersion | KCL schema mismatch | Update KCL imports |

## Cluster Debugging

### Trace Resource Relationships

```bash
# Trace from claim to all managed resources
crossplane beta trace <claim-kind>/<claim-name> -n <namespace>

# Trace from XR
crossplane beta trace <xr-kind>/<xr-name>
```

Output shows the resource tree with status of each resource.

### Check XR Status

```bash
kubectl get <xr-kind> <xr-name> -o yaml
```

Key fields to inspect:
- `status.conditions` - Synced, Ready, and custom conditions
- `status.connectionDetails` - Connection secret propagation
- `spec.compositionRef` - Which composition is being used
- `spec.resourceRefs` - List of composed resources

### Check Claim Status

```bash
kubectl describe <claim-kind> <claim-name> -n <namespace>
```

Look for:
- Events showing errors
- `status.conditions` with False values
- Missing `status.connectionDetails`

### View Composition Revisions

```bash
kubectl get compositionrevision -l crossplane.io/composition-name=<composition-name>
```

## Resource Status Debugging

### Check Managed Resource

```bash
kubectl describe <managed-resource-kind> <name>
```

Key sections:
- **Conditions**: Look for `Synced=False` or `Ready=False`
- **Events**: Provider-specific errors
- **Status.AtProvider**: Actual state from cloud provider

### Common Managed Resource Issues

| Condition | Message Pattern | Cause |
|-----------|----------------|-------|
| Synced=False | "cannot create" | Missing permissions or invalid spec |
| Synced=False | "rate limit" | API throttling, retry later |
| Ready=False | "pending" | Resource still provisioning |
| Ready=False | "failed" | External creation error |

### Provider Logs

```bash
# Find provider pod
kubectl get pods -n crossplane-system | grep provider

# View logs
kubectl logs -n crossplane-system <provider-pod> -f
```

## Function-Specific Debugging

### KCL Functions

See [references/kcl-patterns.md](references/kcl-patterns.md) for:
- Common KCL syntax patterns
- Reading composite resource inputs
- Generating multiple resources
- Conditional logic

**Quick KCL debugging:**

```bash
# Extract and validate inline KCL
kubectl get composition <name> -o json | \
  jq -r '.spec.pipeline[] | select(.functionRef.name == "function-kcl") | .input.source' \
  > extracted.k
kcl extracted.k

# Run with debug output
crossplane beta render xr.yaml composition.yaml functions.yaml 2>&1 | head -100
```

### Go Template Functions

Check template syntax:
- Ensure `{{ }}` delimiters are correct
- Verify `.observed.composite.resource.spec` paths
- Check for nil pointer access

### Patch and Transform

Common issues:
- `fromFieldPath` pointing to non-existent field
- `toFieldPath` targeting immutable field
- Transform type mismatch

### Auto-Ready Function

Must be last in pipeline. Issues:
- Not detecting composed resources correctly
- Ready condition not propagating

## Validation

```bash
# Validate composition against schema
crossplane beta validate <composition.yaml>

# Validate with extensions
crossplane beta validate <composition.yaml> --extensions=<extensions-dir>
```

## Quick Reference Commands

```bash
# Remote cluster: Extract for local debugging
kubectl get composition <name> -o yaml > composition.yaml
kubectl get functions -o yaml > functions.yaml
kubectl get <xr> <name> -o yaml > xr.yaml

# Full debugging session
crossplane beta trace <kind>/<name>                    # See resource tree
kubectl get events --field-selector involvedObject.name=<name>  # Recent events
kubectl get <xr> -o jsonpath='{.status.conditions}'    # XR conditions

# Function debugging
crossplane beta render xr.yaml comp.yaml funcs.yaml   # Local render
crossplane beta render xr.yaml comp.yaml funcs.yaml -o json | jq  # Parse output

# View inline KCL
kubectl get composition <name> -o json | jq -r '.spec.pipeline[].input.source'

# Provider debugging  
kubectl logs -n crossplane-system deploy/<provider> --tail=100
```

## References

- [references/kcl-patterns.md](references/kcl-patterns.md) - KCL syntax patterns for compositions
- [references/common-errors.md](references/common-errors.md) - Error messages and solutions
