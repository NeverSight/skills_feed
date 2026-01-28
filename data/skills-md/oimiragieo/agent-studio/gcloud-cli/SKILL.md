---
name: gcloud-cli
description: Google Cloud CLI operations and resource management
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Bash, Read]
best_practices:
  - Never expose service account keys
  - Resource deletion requires confirmation
  - Verify project before operations
error_handling: graceful
streaming: supported
---

# Google Cloud CLI Skill

## Overview

Google Cloud Platform CLI operations. 90%+ context savings.

## Requirements

- gcloud CLI installed
- GOOGLE_PROJECT_ID environment variable
- Authenticated via gcloud auth

## Tools (Progressive Disclosure)

### Compute

| Tool             | Description       | Confirmation |
| ---------------- | ----------------- | ------------ |
| instances-list   | List VM instances | No           |
| instances-create | Create VM         | Yes          |
| instances-delete | Delete VM         | **REQUIRED** |

### Storage

| Tool       | Description          | Confirmation |
| ---------- | -------------------- | ------------ |
| storage-ls | List buckets/objects | No           |
| storage-cp | Copy objects         | Yes          |
| storage-rm | Delete objects       | Yes          |

### IAM

| Tool             | Description           |
| ---------------- | --------------------- |
| iam-list         | List IAM policies     |
| service-accounts | List service accounts |

### Logging

| Tool      | Description            |
| --------- | ---------------------- |
| logs-read | Read logs              |
| logs-tail | Tail logs in real-time |

### BLOCKED

| Tool              | Status      |
| ----------------- | ----------- |
| projects delete   | **BLOCKED** |
| iam-policy delete | **BLOCKED** |

## Agent Integration

- **devops** (primary): Cloud operations
- **gcp-cloud-agent** (primary): GCP specific
- **cloud-integrator** (secondary): Multi-cloud

## Security

⚠️ Never expose service account keys
⚠️ Resource deletion requires confirmation

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
