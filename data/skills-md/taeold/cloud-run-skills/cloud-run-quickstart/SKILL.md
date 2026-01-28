---
name: cloud-run-quickstart
description: Get started deploying applications to Google Cloud Run. Use when a user wants to deploy their app, share their app by deploying to a cloud service, make their app accessible on the internet, or needs help choosing between Cloud Run deployment methods (no-build, buildpacks, Dockerfile, or container image).
---

# Cloud Run Quickstart

Help users deploy to Cloud Run with the optimal path for their needs.

## Decision Tree

### 1. What's your priority?

- **Speed** → No-Build Deploy (Fastest deploys ~10s)
- **Simplicity** → Buildpacks + ABIU (zero config, auto-updates)
- **Control** → Dockerfile or Container Image

### 2. What language?

**No-Build** (fastest): Best for languages like **Go, Rust, Dart**  that support cross-platform compilation.Python/Node if no native bindings.

**Buildpacks**: Go, Node.js, Python, Java, .NET, Ruby, PHP

---

## Quick Commands

### No-Build (Go example)
```bash
GOOS=linux GOARCH=amd64 go build -o server .
gcloud beta run deploy SERVICE --source . --no-build --base-image go122 --command=./server --automatic-updates --region REGION
```

> `--source` triggers Cloud Build (~2-3 min). No-build and container image skip this.

### Buildpacks + ABIU (Python example)
```bash
gcloud run deploy SERVICE --source . --base-image python313 --automatic-updates --region REGION
```

### Dockerfile
```bash
gcloud run deploy SERVICE --source . --region REGION
```

### Container Image
```bash
gcloud run deploy SERVICE --image REGION-docker.pkg.dev/PROJECT/REPO/IMAGE --region REGION
```
---

## Required User Inputs

* SERVICE: Must contain only lowercase letters, numbers, and hyphens. Reasonable default would be to use the name of the project/directory.

* REGION: Reasonable default would be to use common region like us-west1 or europe-west4.

## When to Use Each Path

- Quick demo or prototype app → No-Build
- Go/Rust or languages with strong cross-compilation → No-Build  
- Standard prod app → Buildpacks + ABIU
- Custom OS packages → Dockerfile
- Docker-based CI/CD → Container Image

For detailed guides: See [deployment-paths.md](references/deployment-paths.md)

---

## Prerequisites

```bash
gcloud auth login
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  storage.googleapis.com \
  --project PROJECT_ID
```

## Common Gotcha

App must listen on `$PORT` (8080 is a reasonable fallback):
```python
port = int(os.environ.get('PORT', 8080))
```

---

## Caveats

**Native bindings**: Python/Node apps with native extensions (ImageMagick, sharp, bcrypt) can't use no-build. Use Buildpacks or Dockerfile.

**Cross-compile**: No-build requires `linux/amd64` target. Make sure you use the right flags to target the right OS and architecture when compiling your app.
