---
name: airflow-hitl
description: Use when the user needs human-in-the-loop workflows in Airflow (approval/reject, form input, or human-driven branching). Covers ApprovalOperator, HITLOperator, HITLBranchOperator, HITLEntryOperator. Requires Airflow 3.1+.
---

# Airflow Human-in-the-Loop Operators

Implement human approval gates, form inputs, and human-driven branching in Airflow DAGs using the HITL operators. These deferrable operators pause workflow execution until a human responds via the Airflow UI or REST API.

## Implementation Checklist

Execute steps in order. Prefer deferrable HITL operators over custom sensors or polling loops.

CRITICAL: Requires Airflow 3.1+. Not available in Airflow 2.x.

All HITL operators are deferrable and release their worker slot while waiting for input.

UI Location: Browse -> Required Actions in Airflow UI. Respond via the task instance Required Actions tab or the REST API.

## Step 1: Choose operator

| Operator | Human action | Outcome |
| --- | --- | --- |
| `ApprovalOperator` | Approve or reject | Reject causes downstream tasks to be skipped (approval task itself succeeds) |
| `HITLOperator` | Select option(s) plus form | Returns selections |
| `HITLBranchOperator` | Select downstream task(s) | Runs selected, skips others |
| `HITLEntryOperator` | Submit form | Returns form data |

## Step 2: Implement operator

### ApprovalOperator

```python
from airflow.providers.standard.operators.hitl import ApprovalOperator
from airflow.sdk import dag, task, chain, Param
from pendulum import datetime

@dag(start_date=datetime(2025, 1, 1), schedule="@daily")
def approval_example():
    @task
    def prepare():
        return "Review quarterly report"

    approval = ApprovalOperator(
        task_id="approve_report",
        subject="Report Approval",
        body="{{ ti.xcom_pull(task_ids='prepare') }}",
        defaults="Approve",
        params={"comments": Param("", type="string")},
    )

    @task
    def after_approval(result):
        print(f"Decision: {result['chosen_options']}")

    chain(prepare(), approval)
    after_approval(approval.output)

approval_example()
```

### HITLOperator

Required parameters: `subject` and `options`.

```python
from airflow.providers.standard.operators.hitl import HITLOperator
from airflow.sdk import dag, task, chain, Param
from datetime import timedelta
from pendulum import datetime

@dag(start_date=datetime(2025, 1, 1), schedule="@daily")
def hitl_example():
    hitl = HITLOperator(
        task_id="select_option",
        subject="Select Payment Method",
        body="Choose how to process payment",
        options=["ACH", "Wire", "Check"],
        defaults=["ACH"],
        multiple=False,
        execution_timeout=timedelta(hours=4),
        params={"amount": Param(1000, type="number")},
    )

    @task
    def process(result):
        print(f"Selected: {result['chosen_options']}")
        print(f"Amount: {result['params_input']['amount']}")

    process(hitl.output)

hitl_example()
```

### HITLBranchOperator

Options can either match downstream task IDs directly or use `options_mapping`.

```python
from airflow.providers.standard.operators.hitl import HITLBranchOperator
from airflow.sdk import dag, task, chain
from pendulum import datetime

DEPTS = ["marketing", "engineering", "sales"]

@dag(start_date=datetime(2025, 1, 1), schedule="@daily")
def branch_example():
    branch = HITLBranchOperator(
        task_id="select_dept",
        subject="Select Departments",
        options=[f"Fund {d}" for d in DEPTS],
        options_mapping={f"Fund {d}": d for d in DEPTS},
        multiple=True,
    )

    for dept in DEPTS:
        @task(task_id=dept)
        def handle(dept_name: str = dept):
            print(f"Processing {dept_name}")
        chain(branch, handle())

branch_example()
```

### HITLEntryOperator

```python
from airflow.providers.standard.operators.hitl import HITLEntryOperator
from airflow.sdk import dag, task, chain, Param
from pendulum import datetime

@dag(start_date=datetime(2025, 1, 1), schedule="@daily")
def entry_example():
    entry = HITLEntryOperator(
        task_id="get_input",
        subject="Enter Details",
        body="Provide response",
        params={
            "response": Param("", type="string"),
            "priority": Param("p3", type="string"),
        },
    )

    @task
    def process(result):
        print(f"Response: {result['params_input']['response']}")

    process(entry.output)

entry_example()
```

## Step 3: Optional features

### Notifiers

```python
from airflow.sdk import BaseNotifier, Context
from airflow.providers.standard.operators.hitl import HITLOperator

class MyNotifier(BaseNotifier):
    template_fields = ("message",)
    def __init__(self, message=""):
        self.message = message
    def notify(self, context: Context):
        if context["ti"].state == "running":
            url = HITLOperator.generate_link_to_ui_from_context(context, base_url="https://airflow.example.com")
            self.log.info(f"Action needed: {url}")

hitl = HITLOperator(..., notifiers=[MyNotifier("{{ task.subject }}")])
```

### Restrict respondents

Format depends on your auth manager:

| Auth Manager | Format | Example |
| --- | --- | --- |
| SimpleAuthManager | Username | `["admin", "manager"]` |
| FabAuthManager | Email | `["manager@example.com"]` |
| Astro | Astro ID | `["cl1a2b3cd456789ef1gh2ijkl3"]` |

```python
hitl = HITLOperator(..., respondents=["manager@example.com"])
```

### Timeout behavior

Use `execution_timeout` to auto-resolve and `defaults` to set the choice on timeout.
