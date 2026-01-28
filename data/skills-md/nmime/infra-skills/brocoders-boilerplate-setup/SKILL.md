---
name: brocoders-boilerplate-setup
description: Full-stack setup with Brocoders NestJS backend and Extensive React frontend boilerplates.
---

# Brocoders Boilerplate Setup

Comprehensive guide for setting up full-stack applications using:
- **Backend**: [NestJS Boilerplate](https://github.com/brocoders/nestjs-boilerplate)
- **Frontend**: [Extensive React Boilerplate](https://github.com/brocoders/extensive-react-boilerplate)

## Quick Start

### 1. Choose Your Git Provider

Ask user which platform they want to use:
- **GitHub** → See [references/github-setup.md](references/github-setup.md)
- **GitLab (Cloud)** → See [references/gitlab-setup.md](references/gitlab-setup.md)
- **GitLab (Self-Hosted)** → See [references/gitlab-selfhosted-setup.md](references/gitlab-selfhosted-setup.md)

### 2. Project Structure Decision

Ask user about repository strategy:
- **Monorepo**: Both frontend and backend in single repository
- **Polyrepo**: Separate repositories for frontend and backend (recommended for larger teams)

## Setup Workflow

### Step 1: Clone Boilerplates

```bash
# Create project directory
mkdir my-fullstack-app && cd my-fullstack-app

# Clone backend
git clone https://github.com/brocoders/nestjs-boilerplate.git backend
cd backend && rm -rf .git && cd ..

# Clone frontend
git clone https://github.com/brocoders/extensive-react-boilerplate.git frontend
cd frontend && rm -rf .git && cd ..
```

### Step 2: Initialize Git

Based on chosen provider, follow the corresponding reference guide.

### Step 3: Environment Setup

See [references/environment-setup.md](references/environment-setup.md) for:
- Backend environment configuration
- Frontend environment configuration
- Docker setup
- Database initialization

### Step 4: CI/CD Configuration

CI/CD templates available per provider in their respective reference files.

## Boilerplate-Specific Guides

- **NestJS Backend Details** → [references/nestjs-boilerplate.md](references/nestjs-boilerplate.md)
- **React Frontend Details** → [references/react-boilerplate.md](references/react-boilerplate.md)

## Decision Tree

```
Start
  │
  ├─► Git Provider?
  │     ├─► GitHub → references/github-setup.md
  │     ├─► GitLab Cloud → references/gitlab-setup.md
  │     └─► GitLab Self-Hosted → references/gitlab-selfhosted-setup.md
  │
  ├─► Monorepo or Polyrepo?
  │     ├─► Monorepo → Single repo setup in chosen provider guide
  │     └─► Polyrepo → Separate repos setup in chosen provider guide
  │
  └─► Environment Setup → references/environment-setup.md
```

## Reference Files

- [references/github-setup.md](references/github-setup.md) - GitHub setup
- [references/gitlab-setup.md](references/gitlab-setup.md) - GitLab Cloud setup
- [references/gitlab-selfhosted-setup.md](references/gitlab-selfhosted-setup.md) - Self-hosted GitLab setup
- [references/environment-setup.md](references/environment-setup.md) - Environment configuration
- [references/nestjs-boilerplate.md](references/nestjs-boilerplate.md) - NestJS backend details
- [references/react-boilerplate.md](references/react-boilerplate.md) - React frontend details
- [references/kubernetes-manifests.md](references/kubernetes-manifests.md) - K8s manifests
- [references/helm-charts.md](references/helm-charts.md) - Helm charts