---
name: workflow-builder
description: Design and implement multi-step automation workflows
---


# Workflow Builder Skill

> Build the YAML workflow engine for multi-step agent automation.

## Overview

The workflow engine provides declarative automation capabilities:
- YAML-based workflow definitions
- Variable interpolation between steps
- Conditional execution and error handling
- Multi-agent orchestration

## Prerequisites

```bash
pip install pyyaml
```

## Build Steps

### Step 1: Create the Workflow Executor

**File: `workflows/executor.py`**

```python
#!/usr/bin/env python3
"""
Workflow Executor - Parse and execute YAML workflow definitions.

Provides step-by-step execution with variable interpolation,
conditional logic, and error handling.
"""

import re
import yaml
import json
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from enum import Enum
from datetime import datetime


class StepStatus(Enum):
    """Status of a workflow step."""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


class ErrorAction(Enum):
    """What to do when a step fails."""
    FAIL = "fail"
    SKIP = "skip"
    RETRY = "retry"


@dataclass
class StepResult:
    """Result of executing a step."""
    step_id: str
    status: StepStatus
    output: Any = None
    outputs: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    duration_ms: int = 0


@dataclass
class WorkflowResult:
    """Result of executing a workflow."""
    workflow_name: str
    status: StepStatus
    step_results: List[StepResult] = field(default_factory=list)
    outputs: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    @property
    def duration_ms(self) -> int:
        if self.started_at and self.completed_at:
            return int((self.completed_at - self.started_at).total_seconds() * 1000)
        return 0

    def to_dict(self) -> dict:
        return {
            "workflow_name": self.workflow_name,
            "status": self.status.value,
            "step_results": [
                {
                    "step_id": r.step_id,
                    "status": r.status.value,
                    "output": r.output,
                    "outputs": r.outputs,
                    "error": r.error,
                    "duration_ms": r.duration_ms
                }
                for r in self.step_results
            ],
            "outputs": self.outputs,
            "error": self.error,
            "duration_ms": self.duration_ms
        }


class VariableResolver:
    """Resolve variable references in workflow definitions."""

    PATTERN = re.compile(r'\{\{([^}]+)\}\}')

    def __init__(self):
        self.workflow_inputs: Dict[str, Any] = {}
        self.step_results: Dict[str, StepResult] = {}
        self.env_vars: Dict[str, str] = dict(os.environ)

    def set_inputs(self, inputs: Dict[str, Any]):
        """Set workflow input values."""
        self.workflow_inputs = inputs

    def add_step_result(self, result: StepResult):
        """Add a completed step result."""
        self.step_results[result.step_id] = result

    def resolve(self, value: Any) -> Any:
        """Resolve variables in a value."""
        if isinstance(value, str):
            return self._resolve_string(value)
        elif isinstance(value, dict):
            return {k: self.resolve(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [self.resolve(v) for v in value]
        return value

    def _resolve_string(self, text: str) -> Any:
        """Resolve variables in a string."""
        match = self.PATTERN.fullmatch(text.strip())
        if match:
            return self._get_value(match.group(1).strip())

        def replacer(m):
            val = self._get_value(m.group(1).strip())
            return "" if val is None else str(val)

        return self.PATTERN.sub(replacer, text)

    def _get_value(self, path: str) -> Any:
        """Get value for a variable path."""
        parts = path.split('.')

        if len(parts) < 2:
            return None

        root = parts[0]

        if root == 'workflow' and len(parts) >= 3 and parts[1] == 'inputs':
            input_name = '.'.join(parts[2:])
            return self.workflow_inputs.get(input_name)

        elif root == 'steps' and len(parts) >= 3:
            step_id = parts[1]
            result = self.step_results.get(step_id)
            if not result:
                return None

            field = parts[2]
            if field == 'output':
                return result.output
            elif field == 'outputs' and len(parts) >= 4:
                output_name = '.'.join(parts[3:])
                return result.outputs.get(output_name)
            elif field == 'success':
                return result.status == StepStatus.SUCCESS
            elif field == 'error':
                return result.error

        elif root == 'env' and len(parts) >= 2:
            var_name = '.'.join(parts[1:])
            return self.env_vars.get(var_name)

        return None


class WorkflowExecutor:
    """Execute workflow definitions."""

    def __init__(self, agent_executor=None):
        self.agent_executor = agent_executor or self._mock_executor
        self.definitions_path = Path(__file__).parent / "definitions"

    def _mock_executor(self, agent: str, action: str, inputs: Dict[str, Any]) -> Any:
        """Mock executor for testing."""
        return {
            "agent": agent,
            "action_summary": action[:100] + "..." if len(action) > 100 else action,
            "inputs_received": list(inputs.keys()),
            "mock": True
        }

    def load_workflow(self, name: str) -> dict:
        """Load a workflow definition by name."""
        paths = [
            self.definitions_path / f"{name}.yaml",
            self.definitions_path / f"{name}.yml",
            self.definitions_path / name
        ]

        for path in paths:
            if path.exists():
                with open(path) as f:
                    return yaml.safe_load(f)

        raise FileNotFoundError(f"Workflow not found: {name}")

    def list_workflows(self) -> List[dict]:
        """List all available workflows."""
        workflows = []
        if self.definitions_path.exists():
            for path in self.definitions_path.glob("*.yaml"):
                try:
                    with open(path) as f:
                        data = yaml.safe_load(f)
                        workflows.append({
                            "name": data.get("name", path.stem),
                            "description": data.get("description", ""),
                            "file": path.name,
                            "inputs": [
                                {"name": i.get("name"), "required": i.get("required", False)}
                                for i in data.get("inputs", [])
                            ]
                        })
                except Exception:
                    pass
        return workflows

    def validate_workflow(self, workflow: dict) -> List[str]:
        """Validate a workflow definition. Returns list of errors."""
        errors = []

        if "name" not in workflow:
            errors.append("Missing required field: name")
        if "steps" not in workflow:
            errors.append("Missing required field: steps")
        elif not isinstance(workflow["steps"], list):
            errors.append("steps must be a list")
        elif len(workflow["steps"]) == 0:
            errors.append("steps cannot be empty")

        step_ids = set()
        for i, step in enumerate(workflow.get("steps", [])):
            step_num = i + 1
            if "id" not in step:
                errors.append(f"Step {step_num}: missing required field 'id'")
            elif step["id"] in step_ids:
                errors.append(f"Step {step_num}: duplicate step id '{step['id']}'")
            else:
                step_ids.add(step["id"])

            if "agent" not in step:
                errors.append(f"Step {step_num}: missing required field 'agent'")
            if "action" not in step:
                errors.append(f"Step {step_num}: missing required field 'action'")

        return errors

    def execute(
        self,
        workflow: Union[str, dict],
        inputs: Optional[Dict[str, Any]] = None
    ) -> WorkflowResult:
        """Execute a workflow."""
        if isinstance(workflow, str):
            workflow = self.load_workflow(workflow)

        errors = self.validate_workflow(workflow)
        if errors:
            return WorkflowResult(
                workflow_name=workflow.get("name", "unknown"),
                status=StepStatus.FAILED,
                error=f"Validation failed: {'; '.join(errors)}"
            )

        result = WorkflowResult(
            workflow_name=workflow["name"],
            status=StepStatus.RUNNING,
            started_at=datetime.now()
        )

        resolver = VariableResolver()
        resolver.set_inputs(inputs or {})

        # Apply input defaults
        for input_def in workflow.get("inputs", []):
            name = input_def["name"]
            if name not in (inputs or {}):
                if "default" in input_def:
                    resolver.workflow_inputs[name] = input_def["default"]
                elif input_def.get("required", False):
                    result.status = StepStatus.FAILED
                    result.error = f"Missing required input: {name}"
                    result.completed_at = datetime.now()
                    return result

        on_workflow_error = workflow.get("on_workflow_error", "fail")

        for step in workflow["steps"]:
            step_result = self._execute_step(step, resolver)
            result.step_results.append(step_result)
            resolver.add_step_result(step_result)

            if step_result.status == StepStatus.FAILED:
                if on_workflow_error == "fail":
                    result.status = StepStatus.FAILED
                    result.error = f"Step '{step_result.step_id}' failed: {step_result.error}"
                    break

        if result.status != StepStatus.FAILED:
            result.status = StepStatus.SUCCESS

        for output_def in workflow.get("outputs", []):
            name = output_def["name"]
            if result.step_results:
                last_result = result.step_results[-1]
                if name in last_result.outputs:
                    result.outputs[name] = last_result.outputs[name]
                elif last_result.output is not None:
                    result.outputs[name] = last_result.output

        result.completed_at = datetime.now()
        return result

    def _execute_step(self, step: dict, resolver: VariableResolver) -> StepResult:
        """Execute a single workflow step."""
        step_id = step["id"]
        start_time = datetime.now()

        condition = step.get("condition")
        if condition:
            resolved_condition = resolver.resolve(condition)
            if not resolved_condition:
                return StepResult(
                    step_id=step_id,
                    status=StepStatus.SKIPPED,
                    output=None,
                    duration_ms=0
                )

        action = resolver.resolve(step["action"])
        step_inputs = resolver.resolve(step.get("inputs", {}))

        on_error = ErrorAction(step.get("on_error", "fail"))
        retry_config = step.get("retry", {})
        max_attempts = retry_config.get("max_attempts", 1) if on_error == ErrorAction.RETRY else 1

        last_error = None
        for attempt in range(max_attempts):
            try:
                output = self.agent_executor(step["agent"], action, step_inputs)

                duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)

                outputs = {}
                for output_def in step.get("outputs", []):
                    name = output_def["name"]
                    if isinstance(output, dict) and name in output:
                        outputs[name] = output[name]

                return StepResult(
                    step_id=step_id,
                    status=StepStatus.SUCCESS,
                    output=output,
                    outputs=outputs,
                    duration_ms=duration_ms
                )

            except Exception as e:
                last_error = str(e)
                if attempt < max_attempts - 1:
                    import time
                    delay = retry_config.get("delay_seconds", 1)
                    time.sleep(delay)

        duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)

        if on_error == ErrorAction.SKIP:
            return StepResult(
                step_id=step_id,
                status=StepStatus.SKIPPED,
                error=last_error,
                duration_ms=duration_ms
            )

        return StepResult(
            step_id=step_id,
            status=StepStatus.FAILED,
            error=last_error,
            duration_ms=duration_ms
        )
```

### Step 2: Create the Workflow MCP Server

**File: `mcp/servers/workflow-server/server.py`**

```python
#!/usr/bin/env python3
"""
Workflow MCP Server - Execute and manage workflow definitions.
"""

import json
import sys
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from fastmcp import FastMCP

mcp = FastMCP("workflow-server")

_executor = None

def get_executor():
    global _executor
    if _executor is None:
        from workflows.executor import WorkflowExecutor
        _executor = WorkflowExecutor()
    return _executor


@mcp.tool()
def list_workflows() -> str:
    """List all available workflow definitions."""
    executor = get_executor()
    workflows = executor.list_workflows()
    return json.dumps({"workflows": workflows, "count": len(workflows)}, indent=2)


@mcp.tool()
def get_workflow(name: str) -> str:
    """Get details of a specific workflow."""
    executor = get_executor()
    try:
        workflow = executor.load_workflow(name)
        return json.dumps(workflow, indent=2)
    except FileNotFoundError:
        return json.dumps({
            "error": f"Workflow '{name}' not found",
            "available": [w["name"] for w in executor.list_workflows()]
        })


@mcp.tool()
def validate_workflow(workflow_yaml: str) -> str:
    """Validate a workflow definition."""
    import yaml
    try:
        workflow = yaml.safe_load(workflow_yaml)
    except yaml.YAMLError as e:
        return json.dumps({"valid": False, "errors": [f"YAML parse error: {e}"]})

    executor = get_executor()
    errors = executor.validate_workflow(workflow)
    return json.dumps({
        "valid": len(errors) == 0,
        "errors": errors,
        "workflow_name": workflow.get("name", "unnamed")
    })


@mcp.tool()
def execute_workflow(name: str, inputs: str = "{}") -> str:
    """Execute a workflow by name."""
    executor = get_executor()
    try:
        input_dict = json.loads(inputs)
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Invalid inputs JSON: {e}"})

    try:
        result = executor.execute(name, input_dict)
        return json.dumps(result.to_dict(), indent=2)
    except FileNotFoundError:
        return json.dumps({
            "error": f"Workflow '{name}' not found",
            "available": [w["name"] for w in executor.list_workflows()]
        })


@mcp.tool()
def get_workflow_schema() -> str:
    """Get the workflow schema documentation."""
    schema_path = PROJECT_ROOT / "workflows" / "SCHEMA.md"
    if schema_path.exists():
        return schema_path.read_text()
    return "Schema documentation not found"


if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### Step 3: Create the Schema Documentation

**File: `workflows/SCHEMA.md`**

```markdown
# Workflow Schema

Workflow definitions use YAML format to describe multi-step agent workflows.

## Schema Version

```yaml
version: "1.0"
```

## Full Schema

```yaml
version: "1.0"

# Workflow metadata
name: workflow-name
description: What this workflow does
author: optional-author
tags: [tag1, tag2]

# Input parameters
inputs:
  - name: parameter_name
    type: string | number | boolean | list | object
    required: true | false
    default: optional-default-value
    description: What this parameter is for

# Output definition
outputs:
  - name: output_name
    type: string | number | boolean | list | object
    description: What this output contains

# Workflow steps
steps:
  - id: step-id
    name: Human readable name
    agent: researcher | coder | writer | analyst
    action: The task instruction for the agent
    inputs:
      param: "{{workflow.inputs.parameter_name}}"
      previous: "{{steps.previous-step-id.output}}"
    outputs:
      - name: output_name
        description: What this step produces
    condition: "{{steps.previous-step.success}}"
    on_error: fail | skip | retry
    retry:
      max_attempts: 3
      delay_seconds: 5

# Error handling
on_workflow_error: fail | continue
timeout_seconds: 3600
```

## Variable Interpolation

| Pattern | Description |
|---------|-------------|
| `{{workflow.inputs.NAME}}` | Access workflow input parameter |
| `{{steps.STEP_ID.output}}` | Access output from previous step |
| `{{steps.STEP_ID.outputs.NAME}}` | Access named output from step |
| `{{steps.STEP_ID.success}}` | Boolean: did step succeed |
| `{{steps.STEP_ID.error}}` | Error message if step failed |
| `{{env.VAR_NAME}}` | Access environment variable |
```

### Step 4: Create Test Script

**File: `workflows/test_workflows.py`**

```python
#!/usr/bin/env python3
"""Test workflow executor components."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

def test_variable_resolver():
    from workflows.executor import VariableResolver, StepResult, StepStatus

    resolver = VariableResolver()
    resolver.set_inputs({"topic": "AI", "count": 5})

    assert resolver.resolve("{{workflow.inputs.topic}}") == "AI"
    assert resolver.resolve("{{workflow.inputs.count}}") == 5
    assert resolver.resolve("Topic: {{workflow.inputs.topic}}") == "Topic: AI"
    print("✅ Variable resolver working")


def test_workflow_validation():
    from workflows.executor import WorkflowExecutor

    executor = WorkflowExecutor()

    valid_workflow = {
        "name": "test",
        "steps": [{"id": "s1", "agent": "researcher", "action": "test"}]
    }
    assert executor.validate_workflow(valid_workflow) == []

    invalid_workflow = {"steps": []}
    errors = executor.validate_workflow(invalid_workflow)
    assert len(errors) > 0
    print("✅ Workflow validation working")


def test_workflow_execution():
    from workflows.executor import WorkflowExecutor, StepStatus

    executor = WorkflowExecutor()

    workflow = {
        "name": "test-workflow",
        "inputs": [{"name": "topic", "required": True}],
        "steps": [
            {"id": "step1", "agent": "researcher", "action": "Research {{workflow.inputs.topic}}"},
            {"id": "step2", "agent": "writer", "action": "Write about {{steps.step1.output}}"}
        ]
    }

    result = executor.execute(workflow, {"topic": "testing"})
    assert result.status == StepStatus.SUCCESS
    assert len(result.step_results) == 2
    print("✅ Workflow execution working")


def test_list_workflows():
    from workflows.executor import WorkflowExecutor

    executor = WorkflowExecutor()
    workflows = executor.list_workflows()
    assert isinstance(workflows, list)
    print(f"✅ Found {len(workflows)} workflow definitions")


if __name__ == "__main__":
    test_variable_resolver()
    test_workflow_validation()
    test_workflow_execution()
    test_list_workflows()
    print("
✅ All workflow tests passed!")
```

### Step 5: Create Example Workflow Template

**File: `workflows/templates/basic-template.yaml`**

```yaml
version: "1.0"

name: your-workflow-name
description: Describe what this workflow does

inputs:
  - name: input_param
    type: string
    required: true
    description: Description of this input

outputs:
  - name: result
    type: string
    description: The final output

steps:
  - id: first-step
    name: First Step
    agent: researcher  # or: coder, writer, analyst
    action: |
      Your instruction here.
      Use {{workflow.inputs.input_param}} for inputs.
    outputs:
      - name: finding

  - id: second-step
    name: Second Step
    agent: writer
    action: |
      Process the result from first step.
      Previous output: {{steps.first-step.output}}
    inputs:
      data: "{{steps.first-step.output}}"

on_workflow_error: fail
timeout_seconds: 600
```

## Verification

```bash
# Navigate to project root
cd /path/to/agentic-workspace

# Activate virtual environment
source .venv/bin/activate

# Run tests
python workflows/test_workflows.py

# Expected output:
# ✅ Variable resolver working
# ✅ Workflow validation working
# ✅ Workflow execution working
# ✅ Found N workflow definitions
# ✅ All workflow tests passed!
```

## Usage Examples

### Execute a workflow via MCP

```python
# List available workflows
list_workflows()

# Get workflow details
get_workflow("research-and-document")

# Execute with inputs
execute_workflow(
    "research-and-document",
    '{"topic": "quantum computing", "depth": "deep"}'
)
```

### Execute programmatically

```python
from workflows.executor import WorkflowExecutor

# With mock executor (for testing)
executor = WorkflowExecutor()
result = executor.execute("research-and-document", {"topic": "AI agents"})

# With real agent executor
def agent_executor(agent: str, action: str, inputs: dict):
    # Your agent invocation logic here
    pass

executor = WorkflowExecutor(agent_executor=agent_executor)
result = executor.execute("data-analysis", {"dataset": "sales_data.csv"})
```

## Creating New Workflows

1. Copy `workflows/templates/basic-template.yaml`
2. Save to `workflows/definitions/your-workflow.yaml`
3. Define inputs, steps, and outputs
4. Add route in `routing/routes/workflows.yaml`
5. Test with `validate_workflow()`

## Available Agents

| Agent | Best For |
|-------|----------|
| `researcher` | Information gathering, fact-checking |
| `coder` | Code generation, debugging, refactoring |
| `writer` | Documentation, content creation, editing |
| `analyst` | Data analysis, visualization, reporting |

## Error Handling

### Per-Step

```yaml
steps:
  - id: risky-step
    agent: coder
    action: Attempt risky operation
    on_error: retry
    retry:
      max_attempts: 3
      delay_seconds: 10
```

### Workflow-Level

```yaml
on_workflow_error: continue  # Keep going even if steps fail
```

## After Building

1. ✅ Run tests to verify
2. Update `CLAUDE.md` status
3. Add your own workflow definitions

## Refinement Notes

> Add notes here as you build and discover what works/doesn't work.

- [ ] Initial implementation
- [ ] Tested with example workflows
- [ ] Integrated with MCP config
- [ ] Connected to real agent executor
