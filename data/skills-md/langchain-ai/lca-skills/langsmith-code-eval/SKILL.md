---
name: langsmith-code-eval
description: Creates code-based evaluators for LangSmith-traced agents. Use when building custom evaluation logic, testing tool usage patterns, or scoring agent outputs programmatically. Triggers on requests to evaluate agents, create evaluators, or run experiments against LangSmith datasets.
---

# LangSmith Code Evaluator Creation

Creates evaluators for LangSmith experiments through structured inspection and implementation.

## Prerequisites

- `langsmith` Python package installed
- `LANGSMITH_API_KEY` environment variable set (check project's `.env` file)

## Workflow

Copy this checklist and track progress:

```
Evaluator Creation Progress:
- [ ] Step 1: Gather info from user
- [ ] Step 2: Inspect trace and dataset structure
- [ ] Step 3: Read agent code
- [ ] Step 4: Write evaluator
- [ ] Step 5: Write experiment runner
- [ ] Step 6: Run and iterate
```

### Step 1: Gather Info from User

**IMPORTANT: Do NOT search or explore the codebase. Ask the user all of these questions upfront using AskUserQuestion before doing anything else.**

Ask the user the following in a single AskUserQuestion call:

1. **Python command**: How do you run Python in this project? (e.g., `python`, `python3`, `uv run python`, `poetry run python`)
2. **Agent file path**: What is the path to your agent file?
3. **LangSmith project name**: What is your LangSmith project name (where traces are logged)?
4. **LangSmith dataset name**: What is the name of the dataset to evaluate against?
5. **Evaluation goal**: What behavior should pass vs fail? Common types:
   - **Tool usage**: Did the agent call the correct tool?
   - **Output correctness**: Does output match expected format/content?
   - **Policy compliance**: Did it follow specific rules?
   - **Classification**: Did it categorize correctly?

### Step 2: Inspect Trace and Dataset Structure

Using the info from Step 1, run the inspection scripts located in this skill's directory:

```bash
{python_cmd} {skill_dir}/scripts/inspect_trace.py PROJECT_NAME [RUN_ID]
{python_cmd} {skill_dir}/scripts/inspect_dataset.py DATASET_NAME
```

Replace `{python_cmd}` with the command from Step 1, and `{skill_dir}` with this skill's directory path.

**Verify the trace matches the agent:**
- Does the trace type match? (e.g., OpenAI trace for OpenAI agent)
- Does it contain the data needed for evaluation?
- If mismatched, clarify before proceeding.

**From the dataset inspection, note:**
- Input schema (what gets passed to the agent)
- Output schema (reference/expected outputs)
- Metadata fields (e.g., `expected_tool`, `difficulty`, labels)

**The dataset metadata often contains ground truth for evaluation** (e.g., which tool should be called, expected classification).

### Step 3: Read Agent Code

Read the agent file provided in Step 1 to identify:
- Entry point function (look for `@traceable` decorator)
- Available tools
- Output format (what the function returns)

### Step 4: Write the Evaluator

Create evaluator functions based on trace and dataset structure. See [EVALUATOR_REFERENCE.md](EVALUATOR_REFERENCE.md) for function signatures and return formats.

### Step 5: Write Experiment Runner

Create a script that:
1. Imports the agent's entry function
2. Wraps it as a target function
3. Runs `evaluate()` or `aevaluate()` against the dataset

See [EVALUATOR_REFERENCE.md](EVALUATOR_REFERENCE.md) for `evaluate()` usage.

### Step 6: Run and Iterate

Execute the experiment, review results in LangSmith, refine evaluators as needed.
