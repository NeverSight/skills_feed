---
name: kargo-skill
description: Comprehensive Kargo GitOps continuous promotion platform skill. Use when implementing progressive delivery pipelines, promotion workflows, freight management, ArgoCD integration, warehouse configuration, stage pipelines, verification templates, or any Kargo-related tasks. Covers installation, core concepts, patterns, security, and complete YAML examples.
---

# Kargo Skill

Complete guide for Kargo - an unopinionated continuous promotion platform that extends GitOps principles with progressive delivery capabilities.

## Overview

Kargo manages the promotion of desired state through environments while tools like ArgoCD handle syncing actual state to desired state in Git. Kargo complements ArgoCD by handling promotion logic.

## Installation

### Prerequisites

- Helm v3.13.1 or later
- Kubernetes cluster with cert-manager pre-installed
- Optional: ArgoCD v2.13.0+, Argo Rollouts v1.7.2+

### Basic Installation (Helm)

```bash
# Generate required values
export ADMIN_PASSWORD_HASH=$(htpasswd -bnBC 10 admin <password> | cut -d: -f2)
export TOKEN_SIGNING_KEY=$(openssl rand -base64 48)

# Install Kargo
helm install kargo \
  oci://ghcr.io/akuity/kargo-charts/kargo \
  --namespace kargo \
  --create-namespace \
  --set api.adminAccount.passwordHash="$ADMIN_PASSWORD_HASH" \
  --set api.adminAccount.tokenSigningKey="$TOKEN_SIGNING_KEY" \
  --wait
```

### Quick Start (All-in-One)

```bash
curl -L https://raw.githubusercontent.com/akuity/kargo/main/hack/quickstart/install.sh | sh
```

### Troubleshooting

- `401` errors: Update Helm to v3.13.1+
- `403` errors: Run `docker logout ghcr.io`

## Core Concepts

### Projects

Units of tenancy for organizing promotion pipelines. Each project maps to a Kubernetes namespace.

```yaml
apiVersion: kargo.akuity.io/v1alpha1
kind: Project
metadata:
  name: my-project
```

### Warehouses

Monitor repositories for new artifact revisions and package them into Freight.

```yaml
apiVersion: kargo.akuity.io/v1alpha1
kind: Warehouse
metadata:
  name: my-warehouse
  namespace: my-project
spec:
  subscriptions:
  - image:
      repoURL: public.ecr.aws/nginx/nginx
      imageSelectionStrategy: SemVer
      constraint: ^1.26.0
  - git:
      repoURL: https://github.com/example/repo.git
      branch: main
      commitSelectionStrategy: NewestFromBranch
  - chart:
      repoURL: https://charts.example.com
      name: my-chart
      semverConstraint: ^1.0.0
```

#### Image Selection Strategies

| Strategy | Description |
|----------|-------------|
| `SemVer` (default) | Semantic versioning constraints |
| `Lexical` | For date-stamped tags (e.g., `nightly-20231225`) |
| `Digest` | Tracks mutable tags like `latest` |
| `NewestBuild` | Uses image metadata (performance-intensive) |

#### Git Commit Selection Strategies

| Strategy | Description |
|----------|-------------|
| `NewestFromBranch` (default) | Latest commit from branch |
| `SemVer` | Tagged releases with constraint |
| `Lexical` | Lexicographically greatest tag |
| `NewestTag` | Most recently created tag |

#### Git Expression Filters

```yaml
# Exclude bot commits
expressionFilter: !(author contains '<bot@example.com>')

# Filter by commit message
expressionFilter: subject contains 'feat:' || subject contains 'fix:'

# Filter by date
expressionFilter: creatorDate.Year() >= 2024
```

#### Path Filtering

```yaml
includePaths:
  - apps/guestbook
  - glob:apps/*/config
excludePaths:
  - apps/guestbook/README.md
  - regex:.*\.test\.yaml$
```

### Freight

Meta-artifacts containing references to specific artifact revisions. Ensures related artifacts move together through the pipeline.

```yaml
# Update freight alias
kargo update freight \
  --project my-project \
  --name <freight-hash> \
  --new-alias frozen-tauntaun

# Manual approval
kargo approve \
  --project my-project \
  --freight <freight-id> \
  --stage prod
```

### Stages

Promotion targets that link together to form pipelines.

```yaml
apiVersion: kargo.akuity.io/v1alpha1
kind: Stage
metadata:
  name: test
  namespace: my-project
spec:
  vars:
    - name: gitopsRepo
      value: https://github.com/example/repo.git
    - name: targetBranch
      value: stage/test

  requestedFreight:
    - origin:
        kind: Warehouse
        name: my-warehouse
      sources:
        direct: true

  promotionTemplate:
    spec:
      steps:
        - uses: git-clone
        - uses: kustomize-set-image
        - uses: git-commit
        - uses: git-push
        - uses: argocd-update

  verification:
    analysisTemplates:
      - name: integration-test
```

#### Freight Availability Strategies

- `OneOf` (default): Verification needed in at least one upstream stage
- `All`: Verification required across all upstream stages

#### Auto-Promotion Policies

- `NewestFreight`: Continuously promotes newest verified/approved freight
- `MatchUpstream`: Promotes freight matching upstream stage's current version

### Promotions

Move code and configuration changes through application lifecycle stages using GitOps.

```bash
# Promote via CLI
kargo promote \
  --project my-project \
  --freight <freight-id> \
  --stage prod

# Using alias
kargo promote \
  --project my-project \
  --freight-alias frozen-tauntaun \
  --stage prod
```

## Promotion Steps Reference

### Git Operations

#### git-clone

```yaml
- uses: git-clone
  config:
    repoURL: https://github.com/example/repo.git
    author:
      name: "Kargo Bot"
      email: "kargo@example.com"
    checkout:
      - branch: main
        path: ./out
      - commit: abc123def456
        path: ./config
        create: true  # Create orphaned branch if missing
```

#### git-commit

```yaml
- uses: git-commit
  as: commit
  config:
    path: ./out
    message: |
      Update image to ${{ imageFrom(vars.imageRepo).Tag }}
    author:
      name: "Kargo Automation"
      email: "kargo@example.com"
```

#### git-push

```yaml
- uses: git-push
  as: push
  config:
    path: ./out
    targetBranch: ${{ vars.targetBranch }}
    maxAttempts: 50
    # OR for PR workflow:
    generateTargetBranch: true
    provider: github
```

**Output**: `branch`, `commit`, `commitURL`

#### git-open-pr

```yaml
- uses: git-open-pr
  as: open-pr
  config:
    repoURL: https://github.com/example/repo.git
    provider: github
    sourceBranch: ${{ outputs['push'].branch }}
    targetBranch: main
    title: "Promote to ${{ ctx.stage }}"
    labels:
      - kargo
      - automated
```

**Output**: `pr.id`, `pr.url`

#### git-wait-for-pr

```yaml
- uses: git-wait-for-pr
  config:
    repoURL: https://github.com/example/repo.git
    prNumber: ${{ outputs['open-pr'].pr.id }}
    provider: github
```

#### git-merge-pr

```yaml
- uses: git-merge-pr
  config:
    repoURL: https://github.com/example/repo.git
    prNumber: ${{ outputs['open-pr'].pr.id }}
    wait: true
```

#### git-clear

```yaml
- uses: git-clear
  config:
    path: ./out
```

### Configuration Management

#### kustomize-set-image

```yaml
- uses: kustomize-set-image
  config:
    path: ./out
    images:
    - image: ghcr.io/example/app
      tag: ${{ imageFrom(vars.imageRepo).Tag }}
    - image: ghcr.io/example/other
      newName: registry.example.com/other
      digest: ${{ imageFrom('ghcr.io/example/other').Digest }}
```

#### kustomize-build

```yaml
- uses: kustomize-build
  config:
    path: ./src/overlays/test
    outPath: ./out/manifests.yaml
    plugin.helm.kubeVersion: "1.28.0"
```

#### helm-template

```yaml
- uses: helm-template
  config:
    path: ./charts/my-chart
    outPath: ./out/manifests.yaml
    releaseName: my-release
    namespace: default
    outLayout: helm  # or 'flat'
    valuesFiles:
      - ./values-prod.yaml
    buildDependencies: true
    includeCRDs: true
    setValues:
      - key: image.tag
        value: ${{ imageFrom(vars.imageRepo).Tag }}
```

#### helm-update-chart

```yaml
- uses: helm-update-chart
  config:
    path: ./src/my-chart
    charts:
      - repository: https://charts.example.com
        name: dependency-chart
        version: 2.0.0
```

#### yaml-update

```yaml
- uses: yaml-update
  config:
    path: ./src/values.yaml
    updates:
      - key: image.tag
        value: ${{ imageFrom(vars.imageRepo).Tag }}
      - key: replicas
        value: "3"
```

#### json-update

```yaml
- uses: json-update
  config:
    path: ./src/config.json
    updates:
      - key: version
        value: ${{ imageFrom(vars.imageRepo).Tag }}
```

### ArgoCD Integration

#### argocd-update

```yaml
- uses: argocd-update
  config:
    apps:
    - name: my-app
      namespace: argocd
      sources:
      - repoURL: https://github.com/example/repo.git
        desiredRevision: ${{ outputs.push.commit }}
        updateTargetRevision: true
```

**Required Application Annotation:**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  annotations:
    kargo.akuity.io/authorized-stage: "my-project:my-stage"
```

### File Operations

#### copy

```yaml
- uses: copy
  config:
    inPath: ./overlay/kustomization.yaml
    outPath: ./src/kustomization.yaml
```

#### delete

```yaml
- uses: delete
  config:
    path: ./temp
```

### External Integrations

#### http

```yaml
- uses: http
  config:
    method: POST
    url: https://api.example.com/deploy
    headers:
      - name: Authorization
        value: "Bearer ${{ secrets.apiToken }}"
    body: '{"version":"${{ ctx.freight.displayID }}"}'
    timeout: 5m
    successExpression: response.status >= 200 && response.status < 300
    failureExpression: response.status >= 500
```

#### compose-output

```yaml
- uses: compose-output
  config:
    pr_url: "${{ vars.repoURL }}/pull/${{ outputs['open-pr'].pr.id }}"
    commit_sha: "${{ outputs['commit'].commit }}"
```

## Expression Language

### Syntax

```yaml
${{ expression }}
```

### Built-in Variables

| Variable | Description |
|----------|-------------|
| `ctx.project` | Project name |
| `ctx.stage` | Stage name |
| `ctx.promotion` | Promotion name |
| `ctx.freight` | Target freight |
| `vars.<name>` | User-defined variables |
| `outputs.<step>.<field>` | Previous step outputs |

### Functions

#### Artifact Functions

```yaml
# Git commits
${{ commitFrom("https://github.com/example/repo.git").ID }}
${{ commitFrom("https://github.com/example/repo.git").Branch }}
${{ commitFrom("https://github.com/example/repo.git").Message }}
${{ commitFrom("https://github.com/example/repo.git").Author }}

# Container images
${{ imageFrom("public.ecr.aws/nginx/nginx").Tag }}
${{ imageFrom("public.ecr.aws/nginx/nginx").Digest }}
${{ imageFrom("public.ecr.aws/nginx/nginx").RepoURL }}

# Helm charts
${{ chartFrom("https://example.com/charts", "my-chart").Version }}
${{ chartFrom("https://example.com/charts", "my-chart").RepoURL }}
```

#### Status Functions

```yaml
# Conditional execution
if: ${{ success() }}      # All preceding steps succeeded
if: ${{ failure() }}      # Any preceding step failed
if: ${{ always() }}       # Always execute
if: ${{ status("my-step") == "Succeeded" }}
```

#### Utility Functions

```yaml
${{ quote(42) }}                    # Convert to quoted string
${{ configMap("my-config").key }}   # Read ConfigMap data
${{ secret("my-secret").password }} # Read Secret data
${{ warehouse("my-warehouse") }}    # Get Warehouse freight origin
${{ semverDiff("1.2.3", "1.3.0") }} # Returns: "Minor"
```

## Verification

### AnalysisTemplate Structure

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: integration-test
  namespace: my-project
spec:
  args:
    - name: commit
  metrics:
  - name: test-job
    provider:
      job:
        spec:
          template:
            spec:
              containers:
              - name: test
                image: alpine:latest
                command: ["sh", "-c", "sleep 10 && exit 0"]
              restartPolicy: Never
          backoffLimit: 1
```

### Stage Verification Configuration

```yaml
spec:
  verification:
    analysisTemplates:
      - name: integration-test
    analysisRunMetadata:
      labels:
        env: test
    args:
      - name: commit
        value: ${{ commitFrom("https://github.com/example/repo.git").ID }}
```

### Soak Time

```yaml
spec:
  requestedFreight:
    - origin:
        kind: Warehouse
        name: my-warehouse
      sources:
        stages:
          - uat
        requiredSoakTime: 24h
```

## Patterns

### Image Updater Pattern

Single Warehouse monitors image repository, produces Freight for each new version.

### Config Updater Pattern

Warehouse tracks Git commits, stages combine base config with overlays.

### Common Case Pattern

Single Warehouse subscribes to both image AND Git repositories, promoting both together.

### Multiple Warehouses Pattern

Separate Warehouses for images and configs, enabling independent promotion cadences.

### Grouped Services Pattern

Single Warehouse subscribes to multiple repositories, ensuring coordinated promotion.

### Fanning Out/In Pattern

Non-linear pipeline with branching (e.g., A/B testing) and convergence.

### PR Workflow Pattern

```yaml
steps:
  - uses: git-push
    config:
      generateTargetBranch: true
      provider: github

  - uses: git-open-pr
    as: open-pr
    config:
      targetBranch: main
      title: "Promote to ${{ ctx.stage }}"

  - uses: git-wait-for-pr
    config:
      prNumber: ${{ outputs['open-pr'].pr.id }}
      timeout: 48h
```

## Security

### OIDC Configuration

```yaml
api:
  oidc:
    enabled: true
    issuerURL: https://idp.example.com
    clientID: kargo-ui
    cliClientID: kargo-cli
    admins:
      claims:
        groups: [devops]
    projectCreators:
      claims:
        groups: [leads]
```

### User-to-ServiceAccount Mapping

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin
  namespace: my-project
  annotations:
    rbac.kargo.akuity.io/claims: |
      {
        "sub": ["alice", "bob"],
        "groups": ["devops", "kargo-admin"]
      }
```

### Pre-defined Project Roles

- `kargo-admin`: Full project management permissions
- `kargo-viewer`: Read-only access
- `default`: Kubernetes-managed baseline

### Credential Management

#### Git Credentials

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: git-credentials
  namespace: my-project
  labels:
    kargo.akuity.io/cred-type: git
stringData:
  repoURL: https://github.com/example/repo.git
  username: my-username
  password: my-personal-access-token
```

#### SSH Key Authentication

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: git-ssh-credentials
  labels:
    kargo.akuity.io/cred-type: git
stringData:
  repoURL: git@github.com:example/repo.git
  sshPrivateKey: <base64-encoded-ssh-key>
```

#### GitHub App Authentication

```yaml
stringData:
  repoURL: https://github.com/example/repo.git
  githubAppClientID: "1234567"
  githubAppPrivateKey: <base64-encoded-app-key>
  githubAppInstallationID: "98765432"
```

#### Container Registry Credentials

**AWS ECR:**

```yaml
metadata:
  labels:
    kargo.akuity.io/cred-type: image
stringData:
  repoURL: 123456789.dkr.ecr.us-west-2.amazonaws.com
  awsRegion: us-west-2
  awsAccessKeyID: AKIA...
  awsSecretAccessKey: ...
```

**Google Artifact Registry:**

```yaml
stringData:
  repoURL: us-central1-docker.pkg.dev/my-project/my-repo
  gcpServiceAccountKey: |
    { "type": "service_account", ... }
```

#### CLI Credential Management

```bash
# Create credentials
kargo create credentials \
  --project my-project my-creds \
  --git \
  --repo-url https://github.com/example/repo.git \
  --username my-username \
  --password my-pat

# List credentials
kargo get credentials --project my-project

# Delete credentials
kargo delete credentials --project my-project my-creds
```

## Project Configuration

### ProjectConfig Resource

```yaml
apiVersion: kargo.akuity.io/v1alpha1
kind: ProjectConfig
metadata:
  name: my-project
  namespace: my-project
spec:
  promotionPolicies:
    - stages: ["test", "uat"]
      autoPromotionEnabled: true
    - stages: ["prod"]
      autoPromotionEnabled: false

  webhookReceivers:
    - name: github-webhook
      github:
        secretRef:
          name: github-secret
```

### Namespace Management

```yaml
# Adopt pre-existing namespace
metadata:
  labels:
    kargo.akuity.io/project: "true"

# Preserve namespace after project deletion
metadata:
  annotations:
    kargo.akuity.io/keep-namespace: "true"
```

## CLI Commands

```bash
# Authentication
kargo login https://kargo.example.com --admin
kargo login https://kargo.example.com --sso

# Projects
kargo create project my-project
kargo get project my-project
kargo delete project my-project

# Stages
kargo create -f stage.yaml
kargo get stage my-stage --project my-project
kargo refresh stage my-stage --project my-project
kargo delete stage my-stage --project my-project

# Freight
kargo get freight --project my-project
kargo approve --project my-project --freight <id> --stage prod

# Promotions
kargo promote --project my-project --freight <id> --stage prod
kargo promote --project my-project --freight-alias my-alias --stage prod

# Verification
kargo verify stage my-stage --project my-project
kargo verify stage my-stage --project my-project --abort

# Roles
kargo get roles --project my-project
kargo create role developer --project my-project
kargo grant --role developer --claim groups=dev --project my-project
kargo delete role developer --project my-project

# Credentials
kargo get credentials --project my-project
kargo create credentials --project my-project my-creds --git --repo-url <url> --username <user> --password <token>
kargo update credentials --project my-project my-creds --password <new-token>
kargo delete credentials --project my-project my-creds
```

## Complete Stage Example

```yaml
apiVersion: kargo.akuity.io/v1alpha1
kind: Stage
metadata:
  name: production
  namespace: my-project
spec:
  vars:
    - name: imageRepo
      value: ghcr.io/example/app
    - name: gitRepo
      value: https://github.com/example/deployment.git
    - name: gitBranch
      value: main
    - name: appName
      value: my-app

  requestedFreight:
    - origin:
        kind: Warehouse
        name: prod-warehouse
      sources:
        stages:
          - staging
        requiredSoakTime: 24h

  verification:
    analysisTemplates:
      - name: smoke-tests
    args:
      - name: imageTag
        value: ${{ imageFrom(vars.imageRepo).Tag }}

  promotionTemplate:
    spec:
      steps:
        - uses: git-clone
          as: clone
          config:
            repoURL: ${{ vars.gitRepo }}
            checkout:
              - branch: ${{ vars.gitBranch }}
                path: ./out

        - uses: kustomize-set-image
          config:
            path: ./out
            images:
              - image: ${{ vars.imageRepo }}
                tag: ${{ imageFrom(vars.imageRepo).Tag }}

        - uses: git-commit
          as: commit
          config:
            path: ./out
            message: |
              Promote to production
              Image: ${{ imageFrom(vars.imageRepo).Tag }}

        - uses: git-push
          as: push
          config:
            path: ./out
            targetBranch: ${{ vars.gitBranch }}

        - uses: argocd-update
          config:
            apps:
              - name: ${{ vars.appName }}
                sources:
                  - repoURL: ${{ vars.gitRepo }}
                    desiredRevision: ${{ outputs.push.commit }}
                    updateTargetRevision: true
```

## References

For detailed documentation, see:

- `references/promotion-steps.md` - Complete promotion steps reference
- `references/expressions.md` - Expression language reference
- `references/patterns.md` - Deployment patterns
- `references/security.md` - Security configuration

## Official Documentation

- Main Docs: <https://docs.kargo.io/>
- GitHub: <https://github.com/akuity/kargo>
- Examples: <https://github.com/akuity/kargo-examples>
