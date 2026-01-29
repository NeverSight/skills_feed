---
name: using-firebase
description: Comprehensive Firebase development guidance for GCP-hosted applications. Covers Firestore database operations (CRUD, queries, transactions, data modeling), Cloud Functions (1st and 2nd generation, TypeScript and Python, all trigger types), Firebase CLI operations, emulator setup and data persistence, security rules (Firestore and Storage), authentication integration, hosting configuration, and GCP service integration. Use when working with Firebase projects, deploying Cloud Functions, querying Firestore, setting up triggers (Firestore, Auth, Storage, HTTP, Callable, Scheduled, Pub/Sub), managing security rules, configuring hosting rewrites/headers, managing secrets, or integrating with GCP services like BigQuery and Cloud Tasks. Triggers include firebase, firestore, cloud functions, firebase functions, firebase hosting, firebase auth, firebase storage, firebase emulator, firebase deploy, firebase init, firebase rules, callable function, scheduled function, onDocumentCreated, onRequest, onCall, onSchedule.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - WebFetch
  - Glob
  - Grep
metadata:
  version: 1.0.0
  last-updated: 2025-12-27
  author: Claude Skills Community
---

# Firebase Development Skill

## Table of Contents

- [Quick Start](#quick-start)
- [Scope](#scope)
- [Task Navigation](#task-navigation)
- [Scripts](#scripts)
- [Cloud Functions Generation](#cloud-functions-generation)
- [Assets](#assets)
- [Common Workflows](#common-workflows)
- [Pre-Deployment Checklist](#pre-deployment-checklist)
- [Emulator Ports](#emulator-ports)
- [Key Decisions](#key-decisions)

## Quick Start

1. **New project**: Run `scripts/init_project.sh [project-id]`
2. **Local development**: Run `scripts/start_emulators.sh`
3. **Deploy**: Run `scripts/deploy.sh`

## Scope

**Use this skill for:** Firebase development including Firestore CRUD/queries, Cloud Functions (1st/2nd gen), Firebase CLI, emulator setup, security rules, authentication, hosting, and GCP integration.

**Do not use for:** Pure GCP without Firebase, AWS/Azure services, non-serverless architectures, self-hosted solutions, or complex relational queries (use Cloud SQL instead).

## Task Navigation

| Task | Action |
|------|--------|
| Initialize Firebase project | `scripts/init_project.sh` |
| Start local emulators | `scripts/start_emulators.sh` |
| Deploy to production | `scripts/deploy.sh` |
| Deploy functions only | `scripts/deploy_functions.sh` |
| Set up Python functions | `python scripts/setup_python_functions.py` |
| Manage secrets | `scripts/manage_secrets.sh` |
| Export Firestore data | `scripts/export_firestore.sh` |
| Import Firestore data | `scripts/import_firestore.sh` |

| Topic | Reference |
|-------|-----------|
| CLI commands | `references/cli-commands.md` |
| Firestore CRUD, queries, modeling | `references/firestore.md` |
| Cloud Functions triggers | `references/functions-triggers.md` |
| Error handling, optimization | `references/functions-patterns.md` |
| Security rules | `references/security-rules.md` |
| Authentication | `references/auth-integration.md` |
| Hosting configuration | `references/hosting-config.md` |
| GCP integration | `references/gcp-integration.md` |

## Scripts

For complete CLI reference, see `references/cli-commands.md`.

### init_project.sh
Initialize Firebase project with Firestore, Functions, Hosting, Storage, Emulators.
```bash
./scripts/init_project.sh              # Interactive
./scripts/init_project.sh my-project   # Specific project
```

### start_emulators.sh
Start emulator suite with data persistence.
```bash
./scripts/start_emulators.sh                    # Auto-persistence
./scripts/start_emulators.sh --debug            # Enable debugging
./scripts/start_emulators.sh --import ./backup  # Import data
./scripts/start_emulators.sh --only functions,firestore
```

### deploy.sh
Deploy with safety confirmations.
```bash
./scripts/deploy.sh                     # Full deploy
./scripts/deploy.sh --dry-run           # Preview only
./scripts/deploy.sh --only hosting      # Specific target
./scripts/deploy.sh --force             # Skip confirmation
```

### deploy_functions.sh
Deploy Cloud Functions with granular control.
```bash
./scripts/deploy_functions.sh                    # All functions
./scripts/deploy_functions.sh myFunction         # Single function
./scripts/deploy_functions.sh --codebase python  # Specific codebase
```

### manage_secrets.sh
Manage Cloud Functions secrets for 2nd gen functions. Uses GCP Secret Manager for secure storage. Prefer this script over direct `gcloud` commands for Firebase-integrated secret management with proper function access binding.

**Secret lifecycle:** Create secrets before first deploy, update via `set` (creates new version), bind to functions via `runWith({ secrets: [...] })`, and rotate by setting new values.

```bash
./scripts/manage_secrets.sh set API_KEY      # Set secret (creates or updates)
./scripts/manage_secrets.sh get API_KEY      # View metadata and versions
./scripts/manage_secrets.sh list             # List all project secrets
./scripts/manage_secrets.sh delete API_KEY   # Delete secret and all versions
```

### export_firestore.sh / import_firestore.sh
Backup and restore Firestore data.
```bash
./scripts/export_firestore.sh --emulator              # From emulator
./scripts/export_firestore.sh --output gs://bucket    # Production to GCS
./scripts/import_firestore.sh --input ./data --emulator
```

### setup_python_functions.py
Create Python Cloud Functions project.
```bash
python scripts/setup_python_functions.py --path python-functions --codebase python
```

## Cloud Functions Generation

**Use 2nd generation** (recommended):
- HTTP, Firestore, Storage, Scheduled, Pub/Sub triggers
- Higher concurrency, longer timeouts

**Use 1st generation** only for:
- Auth `onCreate`/`onDelete` triggers (not available in 2nd gen)

### 2nd Gen Example (TypeScript)
```typescript
import { onDocumentCreated } from "firebase-functions/v2/firestore";
import { onRequest } from "firebase-functions/v2/https";

export const onUserCreated = onDocumentCreated("users/{userId}", (event) => {
  console.log("New user:", event.params.userId, event.data?.data());
});

export const api = onRequest({ cors: true }, (req, res) => {
  res.json({ status: "ok" });
});
```

### 1st Gen Auth Trigger
```typescript
import * as functions from "firebase-functions/v1";

export const onUserCreate = functions.auth.user().onCreate((user) => {
  console.log("New user:", user.uid);
  return null;
});
```

See `references/functions-triggers.md` for all trigger types with TypeScript and Python examples.

## Assets

| File | Use |
|------|-----|
| `assets/firebase.json.template` | Copy to `firebase.json` and customize |
| `assets/firestore.rules.template` | Copy to `firestore.rules` |
| `assets/storage.rules.template` | Copy to `storage.rules` |
| `assets/tsconfig.functions.json` | Copy to `functions/tsconfig.json` |

## Common Workflows

### New Project Setup
1. Run `scripts/init_project.sh`
2. Copy templates from `assets/` directory
3. Start emulators: `scripts/start_emulators.sh`

### Add Python Functions
1. Run `python scripts/setup_python_functions.py`
2. Update `firebase.json` with provided config
3. Deploy: `scripts/deploy_functions.sh --codebase python`

### Security Rules Development
1. Start with `assets/firestore.rules.template`
2. Test with emulator
3. Deploy: `firebase deploy --only firestore:rules`

See `references/security-rules.md` for patterns.

### Production Deployment
1. Set secrets: `scripts/manage_secrets.sh set API_KEY`
2. Dry run: `scripts/deploy.sh --dry-run`
3. Deploy: `scripts/deploy.sh`

## Pre-Deployment Checklist

Before deploying to production, verify:

- [ ] **Security Rules**: Tested rules in emulator, no open access patterns
- [ ] **Secrets**: All required secrets configured via `scripts/manage_secrets.sh list`
- [ ] **Environment**: Correct project selected (`firebase use`)
- [ ] **Functions**: All functions tested locally with emulator
- [ ] **Indexes**: Firestore indexes deployed (`firebase deploy --only firestore:indexes`)
- [ ] **Dry Run**: `scripts/deploy.sh --dry-run` shows expected changes
- [ ] **App Check**: Enabled for production apps (prevents abuse)
- [ ] **Billing**: Budget alerts configured in GCP Console
- [ ] **Monitoring**: Cloud Logging and Error Reporting enabled

## Emulator Ports

| Service | Port |
|---------|------|
| Auth | 9099 |
| Functions | 5001 |
| Firestore | 8080 |
| Storage | 9199 |
| Hosting | 5000 |
| UI | 4000 |

## Key Decisions

### Firestore Data Modeling
- **Embed** data read together that rarely changes
- **Reference** data that changes frequently or is shared
- **Subcollections** for parent-child relationships
- **Root collections** for cross-document queries

See `references/firestore.md` for patterns.

### TypeScript vs Python Functions
- **TypeScript**: JavaScript teams, Firebase client SDK integration
- **Python**: ML/data science, Python ecosystem

Both can coexist via multiple codebases in `firebase.json`.