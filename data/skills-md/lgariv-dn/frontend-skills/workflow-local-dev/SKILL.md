---
name: workflow-local-dev
description: Support local workflow platform development in the DAP workspace across frontend, backend, and infra teams. Provides access to Kubernetes (Kind), Tilt service management, database queries, and troubleshooting. Use when building backend/API features, adjusting infra configurations, checking logs, running tests, or debugging issues against locally deployed workflow engine components.
---

# Workflow Local Development

## Quick Reference

### Key Commands

| Task | Command |
|------|---------|
| Check pods | `kubectl get pods --context kind-kind` |
| Restart component | `tilt trigger workflow-<service>` |
| View component logs | `tilt logs workflow-<service>` |

### Locally Deployed Components

These workflow services are deployed locally as shared dependencies:
`workflow-catalog`, `workflow-executions-api`, `workflow-engine-worker`, `workflow-consumer`, `workflow-validator`, `workflows-worker`, `standalone-tasks-worker`

---

## Utility Scripts

Execute these scripts for common operations:

### Check Pod Status
```bash
bash .cursor/skills/workflow-local-dev/scripts/check-pods.sh
```

### Restart a Service
```bash
bash .cursor/skills/workflow-local-dev/scripts/restart-service.sh <service-name>
# Example: bash .cursor/skills/workflow-local-dev/scripts/restart-service.sh catalog
```

### Tail Service Logs
```bash
bash .cursor/skills/workflow-local-dev/scripts/tail-logs.sh <service-name>
# Example: bash .cursor/skills/workflow-local-dev/scripts/tail-logs.sh executions-api
```

### Query Database
```bash
bash .cursor/skills/workflow-local-dev/scripts/db-query.sh "<SQL query>"
# Example: bash .cursor/skills/workflow-local-dev/scripts/db-query.sh "SELECT * FROM workflow_engine.workflows ORDER BY created_at DESC LIMIT 5"
```

---

## Development Workflow

Use this flow primarily when containers fail locally or when you need to debug runtime behavior.

1. **Capture current status**: `kubectl get pods --context kind-kind`
2. **Rebuild/restart component**: `tilt trigger workflow-<service>`
3. **Watch logs or health**: `kubectl logs -f <pod> --context kind-kind`
4. **Inspect configuration or data** (if needed): `bash .cursor/skills/workflow-local-dev/scripts/db-query.sh "<SQL query>"`

---

## Troubleshooting

### Pod Issues
```bash
kubectl get pods --context kind-kind
kubectl describe pod <pod-name> --context kind-kind
kubectl logs -f <pod-name> --context kind-kind
```

### Temporal Workflows
Open http://localhost:8081 (Temporal UI) and search by workflow ID.

### Database State
```bash
# Use the db-query script (runs psql inside the postgres pod)
bash .cursor/skills/workflow-local-dev/scripts/db-query.sh "SELECT * FROM workflow_engine.workflows ORDER BY created_at DESC LIMIT 5"
```

### Pulsar Messages
```bash
pulsar-admin topics stats persistent://public/dap/<topic>
pulsar-client consume persistent://public/dap/<topic> -s test-sub -n 10
```

---

## Additional Resources

- For complete service URLs and infrastructure details, see [reference.md](reference.md)
