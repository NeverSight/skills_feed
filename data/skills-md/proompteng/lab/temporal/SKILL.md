---
name: temporal
description: "Operate Temporal workflows in this repo: start/list/inspect workflows, fetch history, debug nondeterminism, reset/cancel/terminate, and check task queues via Temporal CLI."
---

# Temporal

## Overview

Operate workflows with explicit namespace, address, and task queue. Use repo scripts for starting workflows, then use the CLI to inspect and control them.

## Connection

```bash
export TEMPORAL_ADDRESS=temporal-grpc.ide-newton.ts.net:7233
export TEMPORAL_NAMESPACE=default
export TEMPORAL_TASK_QUEUE=bumba
```

Validate connectivity:

```bash
temporal --namespace "$TEMPORAL_NAMESPACE" workflow list --limit 5
```

## From UI URL to CLI args

Example UI URL:

```
http://temporal/namespaces/default/workflows/bumba-repo-0e6476cd-6df7-4ee3-8184-95029cd50c88/019b7788-e535-752c-8a4a-2ee44de7065e/history
```

Derive:

```bash
export WORKFLOW_ID=bumba-repo-0e6476cd-6df7-4ee3-8184-95029cd50c88
export RUN_ID=019b7788-e535-752c-8a4a-2ee44de7065e
```

## Inspect workflows

Describe:

```bash
temporal --namespace "$TEMPORAL_NAMESPACE" workflow describe   --workflow-id "$WORKFLOW_ID"   --run-id "$RUN_ID"
```

History (JSON):

```bash
temporal --namespace "$TEMPORAL_NAMESPACE" workflow show   --workflow-id "$WORKFLOW_ID"   --run-id "$RUN_ID"   --output json > /tmp/workflow-history.json
```

Trace:

```bash
temporal --namespace "$TEMPORAL_NAMESPACE" workflow trace   --workflow-id "$WORKFLOW_ID"   --run-id "$RUN_ID"
```

## List and filter

```bash
temporal --namespace "$TEMPORAL_NAMESPACE" workflow list --limit 20

temporal --namespace "$TEMPORAL_NAMESPACE" workflow list   --query 'WorkflowType="enrichFile" and ExecutionStatus="Running"'

temporal --namespace "$TEMPORAL_NAMESPACE" workflow list   --query 'WorkflowType="enrichRepository" and ExecutionStatus="Failed"'
```

## Start workflows (repo scripts)

`enrichRepository`:

```bash
bun run packages/scripts/src/bumba/enrich-repository.ts   --path-prefix services/bumba   --max-files 50   --wait
```

`enrichFile`:

```bash
bun run packages/scripts/src/bumba/enrich-file.ts   --file services/bumba/src/worker.ts   --wait
```

## Reset nondeterminism

1. Use `workflow show` to locate the last good event ID.
2. Reset to `FirstWorkflowTask` or the safe event.
3. Confirm the new run replays deterministically.

```bash
temporal --namespace "$TEMPORAL_NAMESPACE" workflow reset   --workflow-id "$WORKFLOW_ID"   --run-id "$RUN_ID"   --reason "reset to known-good event"   --event-id 31   --reset-type FirstWorkflowTask
```

## Cancel / terminate

```bash
temporal --namespace "$TEMPORAL_NAMESPACE" workflow cancel --workflow-id "$WORKFLOW_ID"

temporal --namespace "$TEMPORAL_NAMESPACE" workflow terminate   --workflow-id "$WORKFLOW_ID"   --reason "manual cleanup"
```

## Task queues / workers

```bash
temporal --namespace "$TEMPORAL_NAMESPACE" task-queue describe   --task-queue "$TEMPORAL_TASK_QUEUE"
```

## Worker logs

```bash
kubectl logs -n jangar deploy/bumba --tail=200
```

## Resources

- Reference: `references/temporal-cli.md`
- Runner: `scripts/temporal-run.sh`
- Triage template: `assets/temporal-triage.md`
