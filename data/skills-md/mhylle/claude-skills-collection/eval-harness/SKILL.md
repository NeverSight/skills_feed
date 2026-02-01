---
name: eval-harness
description: Comprehensive evaluation framework for systematic testing, measurement, and quality assurance of AI-assisted implementations. Supports capability evals, regression testing, multiple grader types, and standardized metrics.
argument-hint: "[mode: create|run|report]"
---

# Eval Harness

## Design Philosophy

### Evaluation-Driven Development

Evaluation-driven development (EDD) is a methodology where evaluations are defined before or alongside implementation, ensuring that success criteria are explicit, measurable, and testable from the start.

**Core Principles:**

1. **Define Success First**: Before implementing a feature, define what "working correctly" means through explicit evaluations
2. **Measure Continuously**: Run evals throughout development, not just at the end
3. **Automate Where Possible**: Prefer automated graders for speed and consistency
4. **Human Review for Nuance**: Use human graders when quality judgments require context or subjectivity
5. **Track Regressions**: Every capability added should become a regression test
6. **Iterate on Failures**: Failed evals provide specific, actionable feedback for improvement

**Benefits of EDD:**

- **Clear Success Criteria**: No ambiguity about what "done" means
- **Early Problem Detection**: Issues found before they compound
- **Confidence in Changes**: Regressions caught immediately
- **Documentation as Tests**: Evals serve as executable specifications
- **Progress Tracking**: Quantitative measurement of improvement over time

**The Eval Mindset:**

```
Traditional: "Build it, then figure out if it works"
EDD:         "Define what 'works' means, then build to pass those evals"
```

---

## Eval Types

### Capability Evals

**Purpose:** Verify that a new capability works correctly. Capability evals test whether the system can do something it couldn't do before, or does something better than before.

**When to Use:**
- Adding new features
- Improving existing functionality
- Testing edge cases
- Validating complex behaviors

**Structure:**

```yaml
capability_eval:
  id: string                    # Unique identifier
  name: string                  # Human-readable name
  description: string           # What this eval tests
  category: string              # Grouping for organization

  input:
    type: string                # "prompt", "file", "api_call", etc.
    content: any                # The actual input data
    context: object             # Additional context if needed

  expected_output:
    type: string                # "exact", "contains", "pattern", "semantic"
    value: any                  # Expected result or pattern
    alternatives: list          # Acceptable alternative outputs

  grader:
    type: string                # "code", "model", "human"
    config: object              # Grader-specific configuration

  metadata:
    difficulty: string          # "easy", "medium", "hard"
    tags: list                  # For filtering and organization
    timeout_seconds: number     # Maximum time allowed
    retries: number             # Number of retry attempts
    weight: number              # Importance weight for scoring
```

**Examples:**

```yaml
# Example 1: Code generation capability
- id: "cap-codegen-001"
  name: "Generate Python function from description"
  description: "Test ability to generate correct Python code from natural language"
  category: "code_generation"

  input:
    type: "prompt"
    content: "Write a Python function that calculates the factorial of a number recursively"
    context:
      language: "python"
      style: "functional"

  expected_output:
    type: "functional"
    value:
      test_cases:
        - input: [5]
          output: 120
        - input: [0]
          output: 1
        - input: [1]
          output: 1
        - input: [10]
          output: 3628800

  grader:
    type: "code"
    config:
      executor: "python"
      function_name: "factorial"
      timeout_per_case: 5

  metadata:
    difficulty: "easy"
    tags: ["python", "recursion", "math"]
    timeout_seconds: 30
    weight: 1.0

# Example 2: Semantic understanding capability
- id: "cap-semantic-001"
  name: "Extract key information from technical document"
  description: "Test ability to identify and extract relevant technical details"
  category: "information_extraction"

  input:
    type: "file"
    content: "path/to/technical-spec.md"
    context:
      extraction_targets: ["dependencies", "api_endpoints", "configuration"]

  expected_output:
    type: "semantic"
    value:
      must_include:
        - "PostgreSQL 14+"
        - "/api/v1/users"
        - "DATABASE_URL environment variable"
      must_not_include:
        - "deprecated"
        - "legacy"

  grader:
    type: "model"
    config:
      model: "claude-3-5-sonnet"
      rubric: |
        Score the extraction on these criteria:
        1. Completeness: Did it find all required items? (0-5)
        2. Accuracy: Are the extracted items correct? (0-5)
        3. Relevance: Did it avoid including irrelevant information? (0-5)

  metadata:
    difficulty: "medium"
    tags: ["extraction", "documentation", "comprehension"]
    timeout_seconds: 60
    weight: 1.5
```

---

### Regression Evals

**Purpose:** Verify that existing functionality still works after changes. Regression evals protect against unintended breakage.

**When to Use:**
- After any code change
- Before merging PRs
- After dependency updates
- During refactoring

**Structure:**

```yaml
regression_eval:
  id: string                    # Unique identifier
  name: string                  # Human-readable name
  description: string           # What behavior this protects
  baseline_version: string      # Version/commit where baseline was captured

  baseline:
    output: any                 # Known-good output
    captured_at: datetime       # When baseline was established
    environment: object         # Environment details at capture

  current:
    input: any                  # Input to reproduce
    execution: object           # How to run the current version

  comparison:
    type: string                # "exact", "semantic", "numeric", "structural"
    tolerance: object           # Acceptable deviation from baseline
    ignore_fields: list         # Fields to exclude from comparison

  metadata:
    criticality: string         # "critical", "high", "medium", "low"
    last_passed: datetime       # Last successful run
    failure_count: number       # Number of times this has failed
```

**Examples:**

```yaml
# Example 1: API response regression
- id: "reg-api-001"
  name: "User list endpoint response structure"
  description: "Ensure user list API maintains backward compatibility"
  baseline_version: "v2.3.1"

  baseline:
    output:
      status: 200
      body:
        users:
          - id: "{{any_uuid}}"
            name: "{{any_string}}"
            email: "{{any_email}}"
            created_at: "{{any_iso_datetime}}"
        pagination:
          page: 1
          per_page: 20
          total: "{{any_number}}"
    captured_at: "2024-01-15T10:30:00Z"
    environment:
      node_version: "18.x"
      database: "postgresql"

  current:
    input:
      method: "GET"
      endpoint: "/api/v1/users"
      headers:
        Authorization: "Bearer {{test_token}}"
    execution:
      type: "http"
      base_url: "{{api_base_url}}"

  comparison:
    type: "structural"
    tolerance:
      allow_additional_fields: true
      allow_field_reordering: true
    ignore_fields:
      - "users.*.id"
      - "users.*.created_at"
      - "pagination.total"

  metadata:
    criticality: "critical"
    last_passed: "2024-01-20T14:00:00Z"
    failure_count: 0

# Example 2: Output quality regression
- id: "reg-quality-001"
  name: "Code review comment quality"
  description: "Maintain quality standards for generated code review comments"
  baseline_version: "v1.0.0"

  baseline:
    output:
      quality_scores:
        specificity: 4.2
        actionability: 4.5
        correctness: 4.8
        tone: 4.6
      sample_comments:
        - "Consider using `const` instead of `let` since this value is never reassigned"
        - "This function exceeds 50 lines; consider extracting the validation logic"
    captured_at: "2024-01-10T09:00:00Z"
    environment:
      model: "claude-3-5-sonnet"
      prompt_version: "2.1"

  current:
    input:
      code_diff: "path/to/test-diff.patch"
      context: "React component refactoring"
    execution:
      type: "skill"
      skill_name: "code-review"
      parameters:
        depth: "thorough"

  comparison:
    type: "numeric"
    tolerance:
      quality_scores:
        min_delta: -0.3          # Allow up to 0.3 point decrease
        max_delta: null          # No upper limit on improvement

  metadata:
    criticality: "high"
    last_passed: "2024-01-19T16:30:00Z"
    failure_count: 1
```

---

## Grader Types

### Code-Based Graders

Code-based graders use programmatic logic to evaluate outputs. They are fast, consistent, and deterministic.

**Types:**

#### Exact Match

Compares output exactly against expected value.

```yaml
grader:
  type: "code"
  config:
    method: "exact_match"
    case_sensitive: true
    trim_whitespace: true
    normalize_newlines: true
```

**When to Use:**
- Deterministic outputs (hashes, IDs, specific values)
- Formatted data with strict requirements
- API response codes and status

**Example:**

```python
def exact_match_grader(output, expected, config):
    actual = output
    target = expected

    if config.get("trim_whitespace", True):
        actual = actual.strip()
        target = target.strip()

    if config.get("normalize_newlines", True):
        actual = actual.replace("\r\n", "\n")
        target = target.replace("\r\n", "\n")

    if not config.get("case_sensitive", True):
        actual = actual.lower()
        target = target.lower()

    return {
        "passed": actual == target,
        "score": 1.0 if actual == target else 0.0,
        "details": {
            "expected": target,
            "actual": actual
        }
    }
```

#### Regex Match

Validates output against regular expression patterns.

```yaml
grader:
  type: "code"
  config:
    method: "regex"
    pattern: "^function\\s+\\w+\\s*\\([^)]*\\)\\s*\\{"
    flags: ["multiline", "ignorecase"]
    must_match: true
    capture_groups: ["function_name"]
```

**When to Use:**
- Validating format/structure without exact content
- Extracting specific patterns from output
- Flexible matching with variations allowed

**Example:**

```python
import re

def regex_grader(output, config):
    pattern = config["pattern"]
    flags = 0

    if "multiline" in config.get("flags", []):
        flags |= re.MULTILINE
    if "ignorecase" in config.get("flags", []):
        flags |= re.IGNORECASE
    if "dotall" in config.get("flags", []):
        flags |= re.DOTALL

    match = re.search(pattern, output, flags)

    result = {
        "passed": (match is not None) == config.get("must_match", True),
        "score": 1.0 if match else 0.0,
        "details": {
            "pattern": pattern,
            "matched": match is not None
        }
    }

    if match and config.get("capture_groups"):
        result["details"]["captures"] = {
            name: match.group(name) if name in match.groupdict() else match.group(i+1)
            for i, name in enumerate(config["capture_groups"])
        }

    return result
```

#### Function Output

Executes generated code and validates results.

```yaml
grader:
  type: "code"
  config:
    method: "function_output"
    executor: "python"
    function_name: "solve"
    test_cases:
      - args: [1, 2]
        kwargs: {}
        expected: 3
        comparator: "equals"
      - args: [[1, 2, 3]]
        expected: 6
        comparator: "equals"
    timeout_per_case: 5
    sandbox: true
```

**When to Use:**
- Code generation tasks
- Algorithm implementation verification
- Function correctness testing

**Example:**

```python
import subprocess
import json
import tempfile
from typing import List, Dict, Any

def function_output_grader(code: str, config: Dict[str, Any]) -> Dict[str, Any]:
    results = []
    passed_count = 0

    for i, test_case in enumerate(config["test_cases"]):
        # Create test harness
        test_code = f'''
import json
import sys

{code}

result = {config["function_name"]}(*{json.dumps(test_case["args"])}, **{json.dumps(test_case.get("kwargs", {}))})
print(json.dumps({{"result": result}}))
'''

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_code)
            temp_path = f.name

        try:
            result = subprocess.run(
                ["python", temp_path],
                capture_output=True,
                text=True,
                timeout=config.get("timeout_per_case", 5)
            )

            if result.returncode == 0:
                output = json.loads(result.stdout)["result"]
                expected = test_case["expected"]

                if compare(output, expected, test_case.get("comparator", "equals")):
                    passed_count += 1
                    results.append({"case": i, "passed": True, "output": output})
                else:
                    results.append({
                        "case": i,
                        "passed": False,
                        "output": output,
                        "expected": expected
                    })
            else:
                results.append({
                    "case": i,
                    "passed": False,
                    "error": result.stderr
                })

        except subprocess.TimeoutExpired:
            results.append({"case": i, "passed": False, "error": "timeout"})
        except Exception as e:
            results.append({"case": i, "passed": False, "error": str(e)})

    return {
        "passed": passed_count == len(config["test_cases"]),
        "score": passed_count / len(config["test_cases"]),
        "details": {
            "test_results": results,
            "passed_count": passed_count,
            "total_count": len(config["test_cases"])
        }
    }
```

---

### Model-Based Graders

Model-based graders use LLMs to evaluate output quality. They excel at nuanced judgments that are difficult to codify.

**Configuration:**

```yaml
grader:
  type: "model"
  config:
    model: "claude-3-5-sonnet"           # Model to use for grading
    temperature: 0.0                      # Low temperature for consistency
    max_tokens: 1000                      # Response limit
    rubric: string                        # Evaluation criteria
    scoring:
      type: "numeric"                     # "numeric", "categorical", "boolean"
      range: [1, 5]                       # For numeric scoring
      categories: []                      # For categorical scoring
    examples: []                          # Few-shot examples for calibration
```

**When to Use:**
- Evaluating writing quality, tone, clarity
- Judging relevance or appropriateness
- Complex semantic matching
- When multiple valid outputs exist

**Prompt Template:**

```yaml
model_grader_prompt: |
  You are an expert evaluator. Your task is to grade the following output according to the rubric provided.

  ## Input Given to System
  {input}

  ## System Output
  {output}

  ## Expected Output (Reference)
  {expected}

  ## Evaluation Rubric
  {rubric}

  ## Instructions
  1. Carefully compare the system output against the expected output
  2. Apply each criterion from the rubric
  3. Provide specific justification for each score
  4. Be consistent and objective

  ## Response Format
  Respond in JSON format:
  ```json
  {
    "scores": {
      "criterion_1": <score>,
      "criterion_2": <score>,
      ...
    },
    "overall_score": <weighted_average>,
    "passed": <true/false>,
    "justification": "<brief explanation>",
    "specific_feedback": [
      "<point 1>",
      "<point 2>"
    ]
  }
  ```
```

**Example Rubrics:**

```yaml
# Code quality rubric
code_quality_rubric: |
  Evaluate the generated code on these criteria (1-5 scale):

  1. **Correctness** (weight: 0.4)
     - 5: Fully correct, handles all cases
     - 4: Mostly correct, minor issues
     - 3: Works for basic cases, fails edge cases
     - 2: Partially works, significant bugs
     - 1: Does not work

  2. **Readability** (weight: 0.2)
     - 5: Excellent naming, clear structure, good comments
     - 4: Good readability, minor improvements possible
     - 3: Acceptable, some unclear parts
     - 2: Hard to follow, poor naming
     - 1: Incomprehensible

  3. **Efficiency** (weight: 0.2)
     - 5: Optimal time and space complexity
     - 4: Good efficiency, minor improvements possible
     - 3: Acceptable for typical inputs
     - 2: Inefficient, may timeout on large inputs
     - 1: Extremely inefficient

  4. **Best Practices** (weight: 0.2)
     - 5: Follows all conventions, excellent patterns
     - 4: Follows most practices
     - 3: Some practices followed
     - 2: Few practices followed
     - 1: Ignores conventions

# Documentation quality rubric
documentation_rubric: |
  Evaluate the generated documentation on these criteria (1-5 scale):

  1. **Completeness** (weight: 0.3)
     - Does it cover all necessary topics?
     - Are there gaps in the explanation?

  2. **Accuracy** (weight: 0.3)
     - Is the information technically correct?
     - Are examples accurate and working?

  3. **Clarity** (weight: 0.25)
     - Is the writing clear and understandable?
     - Is jargon explained when used?

  4. **Organization** (weight: 0.15)
     - Is information logically structured?
     - Are sections appropriately sized?
```

**Calibration with Examples:**

```yaml
grader:
  type: "model"
  config:
    model: "claude-3-5-sonnet"
    rubric: "Evaluate code review comment quality..."
    examples:
      - input: "Added console.log for debugging"
        output: "Remove debug statement before merging"
        score: 2
        justification: "Too brief, doesn't explain why or provide context"

      - input: "Added console.log for debugging"
        output: |
          Consider removing this `console.log` statement before merging.
          Debug logs can clutter production output and potentially expose
          sensitive data. If you need logging, consider using a proper
          logging library with log levels.
        score: 5
        justification: "Specific, explains why, provides alternative solution"
```

---

### Human Graders

Human graders provide expert evaluation when automated methods are insufficient.

**When to Use:**
- Subjective quality judgments
- Novel or creative outputs
- High-stakes decisions requiring human accountability
- Calibrating automated graders
- Edge cases where automated graders fail

**Configuration:**

```yaml
grader:
  type: "human"
  config:
    interface: "web"                      # "web", "cli", "api"
    evaluators:
      min_required: 2                     # Minimum evaluators per item
      max_allowed: 5                      # Maximum evaluators
      agreement_threshold: 0.8            # Inter-rater agreement required
    rating_scale:
      type: "likert"                      # "likert", "binary", "ranking"
      range: [1, 5]
      labels:
        1: "Poor"
        2: "Below Average"
        3: "Average"
        4: "Good"
        5: "Excellent"
    rubric: string                        # Detailed instructions for evaluators
    time_limit_minutes: 10                # Time allowed per evaluation
    blind_evaluation: true                # Hide metadata from evaluators
```

**Rating Scales:**

```yaml
# Binary scale
binary_scale:
  type: "binary"
  options:
    - value: true
      label: "Pass"
      description: "Output meets requirements"
    - value: false
      label: "Fail"
      description: "Output does not meet requirements"

# Likert scale
likert_scale:
  type: "likert"
  range: [1, 5]
  labels:
    1: "Strongly Disagree"
    2: "Disagree"
    3: "Neutral"
    4: "Agree"
    5: "Strongly Agree"
  criteria:
    - "The output is accurate"
    - "The output is complete"
    - "The output is well-organized"
    - "The output is appropriate in tone"

# Ranking scale
ranking_scale:
  type: "ranking"
  description: "Rank the outputs from best to worst"
  tie_allowed: false
  min_items: 2
  max_items: 5
```

**Rubric Template:**

```yaml
human_grader_rubric: |
  ## Evaluation Task
  You are evaluating {task_description}.

  ## Context
  - Input provided: {input_summary}
  - Task requirements: {requirements}

  ## Evaluation Criteria
  Please rate the output on each criterion below:

  ### 1. {criterion_1_name}
  {criterion_1_description}
  - What to look for: {criterion_1_indicators}
  - Common issues: {criterion_1_issues}

  ### 2. {criterion_2_name}
  ...

  ## Instructions
  1. Read the output carefully
  2. Consider each criterion independently
  3. Provide specific examples to support your ratings
  4. Note any concerns or edge cases

  ## Important Notes
  - {special_instructions}
  - If unsure, err on the side of {conservative/generous}
```

---

## Metrics

### pass@k

**Definition:** The probability that at least one of k samples passes the evaluation.

**Formula:**

```
pass@k = 1 - C(n-c, k) / C(n, k)

Where:
- n = total number of samples
- c = number of correct samples
- k = number of samples considered
- C(a,b) = binomial coefficient "a choose b"
```

**Unbiased Estimator:**

```python
import numpy as np
from math import comb

def pass_at_k(n: int, c: int, k: int) -> float:
    """
    Calculate pass@k metric.

    Args:
        n: Total number of samples generated
        c: Number of samples that passed
        k: Number of samples to consider

    Returns:
        Probability of at least one pass in k samples
    """
    if n - c < k:
        return 1.0
    return 1.0 - comb(n - c, k) / comb(n, k)

# Example usage
n_samples = 10
n_correct = 3

print(f"pass@1: {pass_at_k(10, 3, 1):.3f}")  # 0.300
print(f"pass@5: {pass_at_k(10, 3, 5):.3f}")  # 0.738
print(f"pass@10: {pass_at_k(10, 3, 10):.3f}") # 1.000
```

**Interpretation:**
- pass@1 = 0.30 means 30% chance of getting it right on first try
- pass@5 = 0.74 means 74% chance of at least one correct in 5 attempts
- Higher k values give higher pass rates (more chances to succeed)

**When to Use:**
- Code generation tasks where any working solution is acceptable
- Creative tasks with multiple valid outputs
- When retry/regeneration is cheap and acceptable
- Measuring "can it ever get this right?"

---

### pass^k (pass-hat-k)

**Definition:** The probability that all k samples pass the evaluation. Measures consistency and reliability.

**Formula:**

```
pass^k = (c/n)^k

Where:
- n = total number of samples
- c = number of correct samples
- k = number of samples required to all pass
```

**Implementation:**

```python
def pass_hat_k(n: int, c: int, k: int) -> float:
    """
    Calculate pass^k metric (all k samples must pass).

    Args:
        n: Total number of samples generated
        c: Number of samples that passed
        k: Number of samples that must all pass

    Returns:
        Probability of all k samples passing
    """
    if n == 0:
        return 0.0
    pass_rate = c / n
    return pass_rate ** k

# Example usage
n_samples = 10
n_correct = 8

print(f"pass^1: {pass_hat_k(10, 8, 1):.3f}")  # 0.800
print(f"pass^3: {pass_hat_k(10, 8, 3):.3f}")  # 0.512
print(f"pass^5: {pass_hat_k(10, 8, 5):.3f}")  # 0.328
```

**Interpretation:**
- pass^1 = 0.80 means 80% of individual attempts pass
- pass^3 = 0.51 means 51% chance of 3 consecutive passes
- Higher k values give lower pass rates (harder to be consistently correct)

**When to Use:**
- Safety-critical applications where consistency matters
- Production deployments requiring reliability
- When failures are costly (can't just retry)
- Measuring "can it reliably get this right?"

---

### Metric Comparison

| Metric | Formula | Use Case | Example |
|--------|---------|----------|---------|
| pass@1 | P(at least 1 in 1) | Single-shot capability | "Can it solve this?" |
| pass@k | P(at least 1 in k) | Best-of-k capability | "Can it ever solve this?" |
| pass^k | P(all k pass) | Consistency/reliability | "Can it always solve this?" |

**Decision Guide:**

```
Are failures acceptable?
├── Yes, can retry → Use pass@k
│   └── How many retries allowed? → Set k accordingly
└── No, must be reliable → Use pass^k
    └── How many consecutive successes needed? → Set k accordingly
```

---

## Eval Workflow

### Phase 1: Define

Create the evaluation specification before or alongside implementation.

```yaml
# eval-definition.yaml
eval_suite:
  name: "Feature X Evaluation Suite"
  version: "1.0.0"
  description: "Comprehensive evaluation for Feature X"

  config:
    parallel_execution: true
    max_workers: 4
    timeout_global: 3600
    retry_failed: true
    retry_count: 2

  evals:
    - $ref: "./evals/capability/cap-001.yaml"
    - $ref: "./evals/capability/cap-002.yaml"
    - $ref: "./evals/regression/reg-001.yaml"

  reporting:
    format: ["json", "markdown", "html"]
    output_dir: "./eval-results"
    include_details: true
    notify_on_failure: true
```

**Checklist:**
- [ ] Define success criteria clearly
- [ ] Identify capability evals needed
- [ ] Identify regression evals to include
- [ ] Choose appropriate grader types
- [ ] Set realistic thresholds
- [ ] Document edge cases

### Phase 2: Implement

Build the feature being evaluated, using evals as guidance.

```
Implementation Loop:
1. Write/modify code
2. Run relevant evals locally
3. Fix failures
4. Repeat until evals pass
5. Commit changes
```

**Best Practices:**
- Run evals frequently during development
- Start with simple cases, add complexity
- Use failing evals to guide implementation
- Don't modify evals to pass (unless requirements changed)

### Phase 3: Evaluate

Run the full evaluation suite and collect results.

```bash
# Run all evals
eval-harness run --suite ./eval-suite.yaml

# Run specific category
eval-harness run --suite ./eval-suite.yaml --category capability

# Run with verbose output
eval-harness run --suite ./eval-suite.yaml --verbose

# Run with specific grader override
eval-harness run --suite ./eval-suite.yaml --grader-type model
```

**Execution Flow:**

```
┌─────────────────────────────────────────────────────────────┐
│                    Evaluation Runner                         │
├─────────────────────────────────────────────────────────────┤
│  1. Load eval suite configuration                           │
│  2. Validate all eval definitions                           │
│  3. Initialize graders (code, model, human queues)          │
│  4. Execute evals (parallel where possible)                 │
│  5. Collect results from all graders                        │
│  6. Aggregate scores and metrics                            │
│  7. Generate reports                                        │
└─────────────────────────────────────────────────────────────┘
```

### Phase 4: Report

Generate comprehensive evaluation reports.

```yaml
# Sample eval report structure
eval_report:
  metadata:
    suite_name: "Feature X Evaluation Suite"
    run_id: "eval-20240120-143052"
    timestamp: "2024-01-20T14:30:52Z"
    duration_seconds: 127
    environment:
      model: "claude-3-5-sonnet"
      version: "1.2.3"

  summary:
    total_evals: 25
    passed: 22
    failed: 3
    skipped: 0
    pass_rate: 0.88

    by_category:
      capability:
        total: 15
        passed: 13
        pass_rate: 0.867
      regression:
        total: 10
        passed: 9
        pass_rate: 0.90

    by_grader:
      code: { total: 18, passed: 17 }
      model: { total: 5, passed: 4 }
      human: { total: 2, passed: 1 }

  metrics:
    pass_at_1: 0.88
    pass_at_3: 0.96
    pass_hat_3: 0.68

  failures:
    - eval_id: "cap-003"
      name: "Complex nested extraction"
      reason: "Missed nested array handling"
      details: { ... }
    - eval_id: "cap-011"
      name: "Edge case: empty input"
      reason: "Threw exception instead of returning empty"
      details: { ... }
    - eval_id: "reg-007"
      name: "API response time regression"
      reason: "Response time 2.3s exceeds 2.0s threshold"
      details: { ... }

  recommendations:
    - "Improve nested data structure handling"
    - "Add empty input validation"
    - "Investigate response time regression"
```

---

## Eval File Format

### YAML Structure

```yaml
# evals/capability/string-processing.yaml
---
schema_version: "1.0"
eval_type: "capability"

metadata:
  id: "cap-string-001"
  name: "String reversal"
  description: "Test basic string manipulation capability"
  category: "string_processing"
  tags: ["strings", "basic", "manipulation"]
  created: "2024-01-15"
  author: "eval-team"

config:
  timeout_seconds: 30
  retries: 1
  parallel: true

test_cases:
  - id: "tc-001"
    name: "Simple string"
    input:
      type: "prompt"
      content: "Reverse the string: hello"
    expected:
      type: "exact"
      value: "olleh"
    grader:
      type: "code"
      config:
        method: "exact_match"
        case_sensitive: true

  - id: "tc-002"
    name: "String with spaces"
    input:
      type: "prompt"
      content: "Reverse the string: hello world"
    expected:
      type: "exact"
      value: "dlrow olleh"
    grader:
      type: "code"
      config:
        method: "exact_match"

  - id: "tc-003"
    name: "Empty string"
    input:
      type: "prompt"
      content: "Reverse the string: ''"
    expected:
      type: "exact"
      value: ""
    grader:
      type: "code"
      config:
        method: "exact_match"

  - id: "tc-004"
    name: "Unicode string"
    input:
      type: "prompt"
      content: "Reverse the string: cafe"
    expected:
      type: "exact"
      value: "efac"
    grader:
      type: "code"
      config:
        method: "exact_match"
```

### JSON Structure

```json
{
  "schema_version": "1.0",
  "eval_type": "regression",
  "metadata": {
    "id": "reg-api-users-001",
    "name": "Users API endpoint stability",
    "description": "Verify users API maintains response structure",
    "category": "api_stability",
    "tags": ["api", "users", "critical"],
    "criticality": "critical"
  },
  "baseline": {
    "version": "v2.3.1",
    "captured_at": "2024-01-10T12:00:00Z",
    "response": {
      "status": 200,
      "headers": {
        "content-type": "application/json"
      },
      "body": {
        "data": [],
        "meta": {
          "page": 1,
          "per_page": 20
        }
      }
    }
  },
  "test_case": {
    "input": {
      "method": "GET",
      "path": "/api/v1/users",
      "headers": {
        "Authorization": "Bearer {{TEST_TOKEN}}"
      }
    },
    "comparison": {
      "type": "structural",
      "options": {
        "ignore_values": ["data.*", "meta.total"],
        "require_keys": ["data", "meta.page", "meta.per_page"]
      }
    }
  },
  "grader": {
    "type": "code",
    "config": {
      "method": "structural_match",
      "strict": false
    }
  }
}
```

### Directory Structure

```
evals/
├── eval-suite.yaml              # Main suite configuration
├── config/
│   ├── graders.yaml             # Grader configurations
│   └── thresholds.yaml          # Pass/fail thresholds
├── capability/
│   ├── code-generation/
│   │   ├── python-functions.yaml
│   │   ├── javascript-async.yaml
│   │   └── sql-queries.yaml
│   ├── comprehension/
│   │   ├── document-summary.yaml
│   │   └── code-explanation.yaml
│   └── reasoning/
│       ├── logic-puzzles.yaml
│       └── math-problems.yaml
├── regression/
│   ├── api/
│   │   ├── users-endpoint.yaml
│   │   └── auth-endpoint.yaml
│   └── output-quality/
│       ├── code-review-comments.yaml
│       └── documentation-generation.yaml
├── baselines/
│   ├── api-responses/
│   └── quality-scores/
└── results/
    ├── 2024-01-20/
    │   ├── run-143052.json
    │   └── run-143052.md
    └── latest -> 2024-01-20/
```

---

## Integration with Implement-Phase

The eval harness integrates with the implement-phase skill as an optional quality gate.

### Configuration

In your phase definition, add an eval step:

```yaml
# In implementation plan phase
phase:
  name: "Implement user authentication"
  steps:
    - type: "implement"
      description: "Build authentication logic"

    - type: "test"
      description: "Run unit tests"

    - type: "eval"                          # Optional eval step
      description: "Run capability evals"
      config:
        suite: "./evals/auth-capability.yaml"
        required_pass_rate: 0.9
        blocking: true                       # Fail phase if evals fail
        metrics:
          - "pass@1"
          - "pass^3"
```

### Workflow Integration

```
┌─────────────────────────────────────────────────────────────┐
│                   Implement-Phase Workflow                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Implementation                                           │
│     └── Write code for the phase                            │
│                                                              │
│  2. Unit Tests                                               │
│     └── Run automated tests                                 │
│                                                              │
│  3. Code Review                                              │
│     └── Automated code review check                         │
│                                                              │
│  4. Eval Harness (Optional)          ◄── NEW                │
│     ├── Run capability evals                                │
│     ├── Run regression evals                                │
│     ├── Check pass rate threshold                           │
│     └── Generate eval report                                │
│                                                              │
│  5. Completion                                               │
│     └── Phase marked complete if all gates pass             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Triggering Evals

```yaml
# From implement-phase, trigger evals
eval_trigger:
  when: "after_tests_pass"
  suite: "./evals/feature-x.yaml"

  filters:
    categories: ["capability"]
    tags: ["critical", "feature-x"]

  thresholds:
    pass_at_1: 0.85
    pass_hat_3: 0.70

  on_failure:
    action: "block"
    notification: true
    report_path: "./eval-results/phase-{phase_id}.md"

  on_success:
    action: "continue"
    archive_results: true
```

### Eval Results in Phase Report

```markdown
## Phase Completion Report

### Implementation Summary
- Files modified: 5
- Lines added: 234
- Lines removed: 45

### Test Results
- Unit tests: 45/45 passed
- Integration tests: 12/12 passed

### Eval Results
| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| pass@1 | 0.92 | 0.85 | PASS |
| pass^3 | 0.78 | 0.70 | PASS |

#### Capability Evals (12/13 passed)
- [x] cap-auth-001: Login flow
- [x] cap-auth-002: Token refresh
- [ ] cap-auth-003: Session timeout (FAILED)
  - Expected: Session expires after 30 min
  - Actual: Session persists indefinitely

#### Regression Evals (8/8 passed)
- [x] reg-auth-001: Password hashing unchanged
- [x] reg-auth-002: Token format stable
...

### Recommendations
1. Fix session timeout handling (cap-auth-003)
2. Add explicit session cleanup logic
```

---

## Appendix: Quick Reference

### Grader Selection Guide

| Output Type | Recommended Grader | Rationale |
|-------------|-------------------|-----------|
| Exact values | Code (exact match) | Fast, deterministic |
| Formatted text | Code (regex) | Validates structure |
| Code output | Code (function) | Tests correctness |
| Natural language | Model | Handles variation |
| Creative content | Human | Subjective judgment |
| Safety-critical | Human + Model | Double verification |

### Metric Selection Guide

| Scenario | Recommended Metric |
|----------|-------------------|
| Code generation (any solution works) | pass@k |
| Production system reliability | pass^k |
| Single-shot capability | pass@1 |
| Best-effort with retries | pass@5 or pass@10 |
| Consistency requirements | pass^3 or pass^5 |

### Common Thresholds

| Context | pass@1 | pass@k | pass^k |
|---------|--------|--------|--------|
| Development | 0.70 | 0.90 | 0.50 |
| Staging | 0.80 | 0.95 | 0.65 |
| Production | 0.90 | 0.99 | 0.80 |
| Critical | 0.95 | 0.999 | 0.90 |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-01-20 | Initial release |
