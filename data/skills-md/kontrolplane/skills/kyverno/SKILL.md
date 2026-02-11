---
name: kyverno
description: Kyverno Kubernetes policy engine for validation, mutation, and generation. Use when writing ClusterPolicies to enforce security standards, auto-mutate resources with defaults, generate companion resources, or verify container image signatures.
---

# Kyverno

## Policy Structure

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy  # or Policy (namespaced)
metadata:
  name: policy-name
spec:
  validationFailureAction: Enforce  # Enforce (block) or Audit (warn)
  background: true                   # Scan existing resources
  rules:
    - name: rule-name
      match:
        any:                         # OR logic
          - resources:
              kinds: [Pod]
              namespaces: [prod-*]   # Glob patterns supported
      exclude:                       # Optional exclusions
        any:
          - resources:
              namespaces: [kube-system]
      validate: {}  # or mutate: {} or generate: {}
```

## Validation Patterns

### Pattern Matching
```yaml
validate:
  pattern:
    metadata:
      labels:
        app: "?*"          # Non-empty string
    spec:
      containers:
        - image: "!*:latest"   # Negation
          resources:
            limits:
              memory: "?*"      # Required field
```

### Deny with Conditions
```yaml
validate:
  message: "Privileged containers not allowed"
  deny:
    conditions:
      any:
        - key: "{{ request.object.spec.containers[].securityContext.privileged || `false` }}"
          operator: AnyIn
          value: [true]
```

### Operators
- `Equals`, `NotEquals`, `In`, `AnyIn`, `AllIn`, `NotIn`, `AnyNotIn`, `AllNotIn`
- `GreaterThan`, `LessThan`, `GreaterThanOrEquals`, `LessThanOrEquals`

## Mutation Patterns

### Strategic Merge
```yaml
mutate:
  patchStrategicMerge:
    metadata:
      labels:
        +(app): default     # + adds only if missing
    spec:
      containers:
        - (name): "*"       # Match anchor
          imagePullPolicy: Always
```

### JSON Patch
```yaml
mutate:
  patchesJson6902: |
    - op: add
      path: /metadata/labels/env
      value: production
```

## Generation Patterns

```yaml
generate:
  apiVersion: v1
  kind: ConfigMap
  name: "{{request.object.metadata.name}}-config"
  namespace: "{{request.object.metadata.namespace}}"
  synchronize: true    # Keep in sync with source
  data:
    kind: ConfigMap
    metadata:
      labels:
        generated: "true"
    data:
      key: value
```

`synchronize: true` means changes to generated resource revert; `false` means generate once.

## Context (External Data)

```yaml
context:
  - name: images
    configMap:
      name: allowed-images
      namespace: kyverno
  - name: ns
    apiCall:
      urlPath: "/api/v1/namespaces/{{request.namespace}}"
      jmesPath: "metadata.labels"
```

Use in expressions: `{{ images.data.registries }}`, `{{ ns.team }}`

## Common Gotchas

- `background: true` only works for validation, not mutation/generation
- `match.any` is OR, `match.all` is AND
- `exclude` takes precedence over `match`
- JMESPath uses backticks for literals: `` `true` ``, `` `"string"` ``
- `||` provides defaults: `{{ value || `"default"` }}`
- PolicyException (v2beta1) exempts specific resources from policies
