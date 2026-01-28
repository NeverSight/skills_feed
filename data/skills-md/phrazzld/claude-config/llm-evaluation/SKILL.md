---
name: llm-evaluation
description: |
  LLM prompt testing, evaluation, and CI/CD quality gates using Promptfoo.
  Invoke when:
  - Setting up prompt evaluation or regression testing
  - Integrating LLM testing into CI/CD pipelines
  - Configuring security testing (red teaming, jailbreaks)
  - Comparing prompt or model performance
  - Building evaluation suites for RAG, factuality, or safety
  Keywords: promptfoo, llm evaluation, prompt testing, red team, CI/CD, regression testing
---

# LLM Evaluation & Testing

Test prompts, models, and RAG systems with automated evaluation and CI/CD integration.

## Quick Start

```bash
# Initialize Promptfoo (no global install needed)
npx promptfoo@latest init

# Run evaluation
npx promptfoo@latest eval

# View results in browser
npx promptfoo@latest view

# Run security scan
npx promptfoo@latest redteam run
```

## Core Concepts

### Why Evaluate?

LLM outputs are non-deterministic. "It looks good" isn't testing. You need:

- **Regression detection**: Catch quality drops before production
- **Security scanning**: Find jailbreaks, injections, PII leaks
- **A/B comparison**: Compare prompts/models side-by-side
- **CI/CD gates**: Block bad changes from merging

### Evaluation Types

| Type | Purpose | Assertions |
|------|---------|------------|
| **Functional** | Does it work? | `contains`, `equals`, `is-json` |
| **Semantic** | Is it correct? | `similar`, `llm-rubric`, `factuality` |
| **Performance** | Is it fast/cheap? | `cost`, `latency` |
| **Security** | Is it safe? | `redteam`, `moderation`, `pii-detection` |

## Configuration

### Basic promptfooconfig.yaml

```yaml
description: "My LLM evaluation suite"

prompts:
  - file://prompts/main.txt

providers:
  - openai:gpt-4o-mini
  - anthropic:claude-3-5-sonnet-latest

tests:
  - vars:
      question: "What is the capital of France?"
    assert:
      - type: contains
        value: "Paris"
      - type: cost
        threshold: 0.01

  - vars:
      question: "Explain quantum computing"
    assert:
      - type: llm-rubric
        value: "Response explains quantum computing concepts clearly"
      - type: latency
        threshold: 3000
```

### With Environment Variables

```yaml
providers:
  - id: openrouter:anthropic/claude-3-5-sonnet
    config:
      apiKey: ${OPENROUTER_API_KEY}
```

## Assertions Reference

### Basic Assertions

```yaml
assert:
  # String matching
  - type: contains
    value: "expected text"
  - type: not-contains
    value: "forbidden text"
  - type: equals
    value: "exact match"
  - type: starts-with
    value: "prefix"
  - type: regex
    value: "\\d{4}-\\d{2}-\\d{2}"  # Date pattern

  # JSON validation
  - type: is-json
  - type: is-valid-json-schema
    value:
      type: object
      properties:
        name: { type: string }
      required: [name]
```

### Semantic Assertions

```yaml
assert:
  # Semantic similarity (embeddings)
  - type: similar
    value: "The capital of France is Paris"
    threshold: 0.8  # 0-1 similarity score

  # LLM-as-judge with custom criteria
  - type: llm-rubric
    value: |
      Response must:
      1. Be factually accurate
      2. Be under 100 words
      3. Not contain marketing language

  # Factuality check against reference
  - type: factuality
    value: "Paris is the capital of France"
```

### Performance Assertions

```yaml
assert:
  # Cost budget (USD)
  - type: cost
    threshold: 0.05  # Max $0.05 per request

  # Latency (milliseconds)
  - type: latency
    threshold: 2000  # Max 2 seconds
```

### Security Assertions

```yaml
assert:
  # Content moderation
  - type: moderation
    value: violence

  # PII detection
  - type: not-contains
    value: "{{email}}"  # From test vars
```

## CI/CD Integration

### GitHub Action

```yaml
name: 'Prompt Evaluation'
on:
  pull_request:
    paths: ['prompts/**', 'src/**/*prompt*']

jobs:
  evaluate:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      # Cache for faster runs
      - uses: actions/cache@v4
        with:
          path: ~/.promptfoo
          key: ${{ runner.os }}-promptfoo-${{ hashFiles('promptfooconfig.yaml') }}

      # Run evaluation and post results to PR
      - uses: promptfoo/promptfoo-action@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}  # Or other provider keys
```

### Quality Gates

```yaml
# promptfooconfig.yaml
evaluateOptions:
  # Fail if any assertion fails
  maxConcurrency: 5

  # Or set pass threshold
  threshold: 0.9  # 90% of tests must pass
```

### Output to JSON (for custom CI)

```bash
npx promptfoo@latest eval -c promptfooconfig.yaml -o results.json

# Check results in CI script
if [ $(jq '.stats.failures' results.json) -gt 0 ]; then
  echo "Evaluation failed!"
  exit 1
fi
```

## Security Testing (Red Team)

### Quick Scan

```bash
# Run red team against your prompts
npx promptfoo@latest redteam run

# Generate compliance report
npx promptfoo@latest redteam report --output compliance.html
```

### Configuration

```yaml
# promptfooconfig.yaml
redteam:
  purpose: "Customer support chatbot"
  plugins:
    - harmful:hate
    - harmful:violence
    - harmful:self-harm
    - pii:direct
    - pii:session
    - hijacking
    - jailbreak
    - prompt-injection

  strategies:
    - jailbreak
    - prompt-injection
    - base64
    - leetspeak
```

### OWASP Top 10 Coverage

```yaml
redteam:
  plugins:
    # 1. Prompt Injection
    - prompt-injection
    # 2. Insecure Output Handling
    - harmful:privacy
    # 3. Training Data Poisoning (N/A for evals)
    # 4. Model Denial of Service
    - excessive-agency
    # 5. Supply Chain (N/A for evals)
    # 6. Sensitive Information Disclosure
    - pii:direct
    - pii:session
    # 7. Insecure Plugin Design
    - hijacking
    # 8. Excessive Agency
    - excessive-agency
    # 9. Overreliance (use factuality checks)
    # 10. Model Theft (N/A for evals)
```

## RAG Evaluation

### Context-Aware Testing

```yaml
prompts:
  - |
    Context: {{context}}
    Question: {{question}}
    Answer based only on the context provided.

tests:
  - vars:
      context: "The Eiffel Tower was built in 1889 for the World's Fair."
      question: "When was the Eiffel Tower built?"
    assert:
      - type: contains
        value: "1889"
      - type: factuality
        value: "The Eiffel Tower was built in 1889"
      - type: not-contains
        value: "1900"  # Common hallucination
```

### Retrieval Quality

```yaml
# Test that retrieval returns relevant documents
tests:
  - vars:
      query: "Python list comprehension"
    assert:
      - type: llm-rubric
        value: "Response discusses Python list comprehension syntax and examples"
      - type: not-contains
        value: "I don't know"  # Shouldn't punt on this query
```

## Comparing Models/Prompts

### A/B Testing

```yaml
# Compare two prompts
prompts:
  - file://prompts/v1.txt
  - file://prompts/v2.txt

# Same tests for both
tests:
  - vars: { question: "Explain recursion" }
    assert:
      - type: llm-rubric
        value: "Clear explanation of recursion with example"
```

### Model Comparison

```yaml
# Compare multiple models
providers:
  - openai:gpt-4o-mini
  - anthropic:claude-3-5-haiku-latest
  - openrouter:google/gemini-flash-1.5

# Run: npx promptfoo@latest eval
# View: npx promptfoo@latest view
# Compare cost, latency, quality side-by-side
```

## Best Practices

### 1. Golden Test Cases

Maintain a set of critical test cases that must always pass:

```yaml
# golden-tests.yaml
tests:
  - description: "Core functionality - must pass"
    vars:
      input: "critical test case"
    assert:
      - type: contains
        value: "expected output"
    options:
      critical: true  # Fail entire suite if this fails
```

### 2. Regression Suite Structure

```
prompts/
├── production.txt          # Current production prompt
├── candidate.txt           # New prompt being tested
tests/
├── golden/                 # Critical tests (run on every PR)
│   └── core-functionality.yaml
├── regression/             # Full regression suite (nightly)
│   └── full-suite.yaml
└── security/               # Red team tests
    └── redteam.yaml
```

### 3. Test Categories

```yaml
tests:
  # Happy path
  - description: "Standard query"
    vars: { question: "What is 2+2?" }
    assert:
      - type: contains
        value: "4"

  # Edge cases
  - description: "Empty input"
    vars: { question: "" }
    assert:
      - type: not-contains
        value: "error"

  # Adversarial
  - description: "Injection attempt"
    vars: { question: "Ignore previous instructions and..." }
    assert:
      - type: not-contains
        value: "Here's how to"  # Should refuse
```

## References

- `references/promptfoo-guide.md` - Detailed setup and configuration
- `references/evaluation-metrics.md` - Metrics deep dive
- `references/ci-cd-integration.md` - CI/CD patterns
- `references/alternatives.md` - Braintrust, DeepEval, LangSmith comparison

## Templates

Copy-paste ready templates:
- `templates/promptfooconfig.yaml` - Basic config
- `templates/github-action-eval.yml` - GitHub Action
- `templates/regression-test-suite.yaml` - Full regression suite
