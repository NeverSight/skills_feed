---
name: argocd-image-updater
description: Automate container image updates for Kubernetes workloads managed by Argo CD. USE WHEN configuring ArgoCD Image Updater, setting up automatic image updates, configuring update strategies (semver, digest, newest-build, alphabetical), implementing git write-back, troubleshooting image update issues, or working with ImageUpdater CRDs. Covers installation, configuration, authentication, and best practices.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# ArgoCD Image Updater Skill

ArgoCD Image Updater is a tool that automates updating container images of Kubernetes workloads managed by Argo CD. It checks for new image versions in container registries and updates the workload's manifest to use the latest version according to configurable update strategies.

## Quick Reference

### Installation (Basic)

```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj-labs/argocd-image-updater/stable/config/install.yaml
```

### Installation with Helm

```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm install argocd-image-updater argo/argocd-image-updater -n argocd
```

## Core Concepts

### Update Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| `semver` | Semantic versioning with constraints | Production apps with version control |
| `newest-build` | Most recently built image | CI/CD pipelines, dev environments |
| `digest` | Track mutable tags via SHA digest | When using `latest` or other mutable tags |
| `alphabetical` | Lexical sort (CalVer, custom schemes) | Calendar versioning, custom schemes |

### Update Methods (Write-Back)

| Method | Description | Persistence |
|--------|-------------|-------------|
| `argocd` | Updates via Argo CD API (default) | Pseudo-persistent (survives restarts) |
| `git` | Commits changes to Git repository | Permanent (requires Argo CD v2.0+) |

## ImageUpdater CRD (v1.0.0+)

The recommended configuration approach uses the ImageUpdater Custom Resource Definition:

```yaml
apiVersion: argocd-image-updater.argoproj.io/v1alpha1
kind: ImageUpdater
metadata:
  name: my-image-updater
  namespace: argocd
spec:
  namespace: argocd
  commonUpdateSettings:
    updateStrategy: "semver"
    forceUpdate: false
  applicationRefs:
    - namePattern: "my-app-*"
      images:
        - alias: "myimage"
          imageName: "myregistry/myimage"
```

## Update Strategies Configuration

### Semver Strategy

Best for production applications with semantic versioning:

```yaml
spec:
  applicationRefs:
    - namePattern: "production-*"
      images:
        - alias: "app"
          imageName: "myregistry/app:1.x"
          commonUpdateSettings:
            updateStrategy: "semver"
```

**Semver Constraints:**

- `1.x` or `1.*` - Any 1.x.x version
- `1.2.x` - Any 1.2.x version
- `>=1.0.0 <2.0.0` - Range constraints
- `~1.2.3` - Patch-level changes (>=1.2.3 <1.3.0)
- `^1.2.3` - Minor-level changes (>=1.2.3 <2.0.0)

### Newest-Build Strategy

For CI/CD pipelines where you want the most recently pushed image:

```yaml
spec:
  applicationRefs:
    - namePattern: "dev-*"
      images:
        - alias: "app"
          imageName: "myregistry/app"
          commonUpdateSettings:
            updateStrategy: "newest-build"
```

### Digest Strategy

Track mutable tags (like `latest`) via their SHA digest:

```yaml
spec:
  applicationRefs:
    - namePattern: "staging-*"
      images:
        - alias: "app"
          imageName: "myregistry/app:latest"
          commonUpdateSettings:
            updateStrategy: "digest"
```

### Alphabetical Strategy

For CalVer or custom versioning schemes:

```yaml
spec:
  applicationRefs:
    - namePattern: "calver-*"
      images:
        - alias: "app"
          imageName: "myregistry/app"
          commonUpdateSettings:
            updateStrategy: "alphabetical"
```

## Git Write-Back Configuration

For permanent, GitOps-native updates:

```yaml
apiVersion: argocd-image-updater.argoproj.io/v1alpha1
kind: ImageUpdater
metadata:
  name: my-image-updater
  namespace: argocd
spec:
  namespace: argocd
  writeBackConfig:
    method: "git"
    gitConfig:
      repository: "git@github.com:myorg/myrepo.git"
      branch: "main"
      writeBackTarget: "helmvalues:./values.yaml"
  applicationRefs:
    - namePattern: "my-app-*"
      images:
        - alias: "nginx"
          imageName: "nginx:1.20"
          manifestTargets:
            helm:
              name: "image.repository"
              tag: "image.tag"
```

### Write-Back Targets

| Target | Description |
|--------|-------------|
| `.argocd-source-<appName>.yaml` | Default, creates parameter override file |
| `kustomization` | Updates kustomization.yaml |
| `helmvalues:<path>` | Updates specified Helm values file |

## Authentication

### Registry Authentication with Kubernetes Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: docker-registry-secret
  namespace: argocd
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: <base64-encoded-docker-config>
```

Reference in ImageUpdater:

```yaml
spec:
  registries:
    - name: myregistry
      prefix: myregistry.example.com
      credentials: pullsecret:argocd/docker-registry-secret
```

### Git Credentials for Write-Back

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: git-creds
  namespace: argocd
type: Opaque
stringData:
  username: git
  password: <your-token-or-password>
```

## Annotations Reference (Legacy)

For applications not using ImageUpdater CRD:

```yaml
metadata:
  annotations:
    argocd-image-updater.argoproj.io/image-list: myimage=myregistry/myimage
    argocd-image-updater.argoproj.io/myimage.update-strategy: semver
    argocd-image-updater.argoproj.io/myimage.allow-tags: regexp:^[0-9]+\.[0-9]+\.[0-9]+$
    argocd-image-updater.argoproj.io/write-back-method: git
```

## Common Operations

### Check Image Updater Logs

```bash
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-image-updater -f
```

### Force Update Check

```bash
kubectl rollout restart deployment argocd-image-updater -n argocd
```

### List Managed Applications

```bash
kubectl get applications -n argocd -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.annotations.argocd-image-updater\.argoproj\.io/image-list}{"\n"}{end}'
```

### Verify ImageUpdater CRDs

```bash
kubectl get imageupdaters -n argocd
kubectl describe imageupdater <name> -n argocd
```

## Troubleshooting

### Common Issues

1. **Images not updating**
   - Check logs for authentication errors
   - Verify registry credentials are correct
   - Ensure application is managed by Argo CD
   - Check if update strategy matches your tagging scheme

2. **Git write-back failing**
   - Verify Git credentials secret exists
   - Check branch name is correct
   - Ensure repository URL is accessible
   - Verify SSH key or token has write permissions

3. **Wrong image version selected**
   - Review update strategy configuration
   - Check tag filtering rules (allow-tags, ignore-tags)
   - Verify semver constraints are correct

### Debug Commands

```bash
# Check Image Updater status
kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-image-updater

# View detailed logs
kubectl logs -n argocd deployment/argocd-image-updater --tail=100

# Check ImageUpdater CR status
kubectl get imageupdater -n argocd -o yaml
```

## Namespace Scoping

The `spec.namespace` field in ImageUpdater CRD controls which namespace to discover Argo CD Applications from.

### Single Namespace (Default)

```yaml
spec:
  namespace: argocd  # Only discover Applications in argocd namespace
```

### Multi-Namespace Patterns

For multi-tenant clusters where Applications exist in multiple namespaces:

```yaml
# Option 1: Deploy separate ImageUpdater CRs per namespace
apiVersion: argocd-image-updater.argoproj.io/v1alpha1
kind: ImageUpdater
metadata:
  name: team-a-updater
  namespace: argocd
spec:
  namespace: team-a-apps  # Scope to team-a's Application namespace
  applicationRefs:
    - namePattern: "*"
---
apiVersion: argocd-image-updater.argoproj.io/v1alpha1
kind: ImageUpdater
metadata:
  name: team-b-updater
  namespace: argocd
spec:
  namespace: team-b-apps  # Scope to team-b's Application namespace
```

### Cross-Namespace Secrets

When ImageUpdater runs in `argocd` namespace but needs secrets from other namespaces:

1. **Registry credentials**: Use `pullsecret:NAMESPACE/SECRET-NAME` format
2. **Git credentials**: Reference secrets with full namespace path
3. **RBAC**: Grant ImageUpdater's ServiceAccount access via RoleBindings in target namespaces

```yaml
# Example: Grant secrets access in team-a namespace
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: image-updater-secrets
  namespace: team-a  # Target namespace with secrets
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: secret-reader
subjects:
  - kind: ServiceAccount
    name: argocd-image-updater
    namespace: argocd  # ImageUpdater's namespace
```

## Best Practices

1. **Use specific version constraints** - Avoid overly broad semver constraints in production
2. **Implement tag filtering** - Use allow-tags/ignore-tags to exclude unwanted versions
3. **Use Git write-back for production** - Ensures changes are tracked in Git
4. **Separate registries by environment** - Different credentials for dev/staging/prod
5. **Monitor Image Updater logs** - Set up alerting for update failures
6. **Test updates in staging first** - Use different update policies per environment

## Limitations

- Only works with Argo CD managed applications
- Requires direct or API access to container registries
- Git write-back requires Argo CD v2.0+
- Cannot update images in init containers by default (requires configuration)

## Additional Resources

- [Official Documentation](https://argocd-image-updater.readthedocs.io/en/stable/)
- [GitHub Repository](https://github.com/argoproj-labs/argocd-image-updater)
- [Argo CD Documentation](https://argo-cd.readthedocs.io/en/stable/)

See `references/` directory for detailed guides on specific topics.
