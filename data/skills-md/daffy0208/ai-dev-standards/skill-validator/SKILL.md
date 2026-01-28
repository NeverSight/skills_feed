---
name: Skill Validator
description: Validates that a skill or MCP implementation matches its manifest by running Codex-powered semantic comparisons across descriptions, preconditions, effects, and API surface.
version: 0.1.0
category: testing
tags:
  - codex
  - validation
  - quality
---

# Skill Validator

**Validate implementations match manifests using Codex for semantic comparison**

## Purpose

Ensures that skill/MCP implementations actually deliver what their manifests promise. Uses Codex to perform semantic analysis comparing descriptions, preconditions, and effects against actual code. Detects drift, missing functionality, and over-promised capabilities.

## When to Use

- After updating skill implementations
- During quality audits to verify accuracy
- When manifests feel outdated or incorrect
- To detect description-implementation drift
- Before releasing new versions of resources

## Key Capabilities

- **Semantic Comparison**: Uses Codex to understand if code matches description
- **Precondition Validation**: Verifies claimed preconditions are actually checked
- **Effect Verification**: Confirms code produces claimed effects
- **API Surface Analysis**: Validates exposed functions match manifest
- **Drift Detection**: Identifies when implementation diverges from manifest
- **Coverage Scoring**: Measures how much of manifest is implemented

## Inputs

```yaml
inputs:
  resource_path: string # Path to skill/MCP directory
  manifest_path: string # Path to manifest.yaml (default: resource_path/manifest.yaml)
  implementation_path: string # Path to code (default: resource_path/index.js)
  strict_mode: boolean # Fail on warnings (default: false)
```

## Process

### Step 1: Load Manifest and Implementation

```bash
#!/bin/bash
# Load manifest and implementation

RESOURCE_PATH="$1"
MANIFEST_PATH="${2:-$RESOURCE_PATH/manifest.yaml}"
IMPL_PATH="${3:-$RESOURCE_PATH/index.js}"

if [ ! -f "$MANIFEST_PATH" ]; then
  echo "❌ Manifest not found: $MANIFEST_PATH"
  exit 1
fi

if [ ! -f "$IMPL_PATH" ]; then
  # Try alternative extensions
  if [ -f "$RESOURCE_PATH/index.ts" ]; then
    IMPL_PATH="$RESOURCE_PATH/index.ts"
  elif [ -f "$RESOURCE_PATH/SKILL.md" ]; then
    # Skill might be declarative only
    IMPL_PATH=""
  else
    echo "⚠️  No implementation file found, validating description only"
    IMPL_PATH=""
  fi
fi

# Read manifest
MANIFEST=$(cat "$MANIFEST_PATH")

# Read implementation (if exists)
if [ -n "$IMPL_PATH" ]; then
  IMPLEMENTATION=$(cat "$IMPL_PATH")
else
  IMPLEMENTATION=""
fi
```

### Step 2: Validate Description Accuracy

```bash
# Use Codex to compare description with implementation
codex exec "
Compare this manifest description with the actual implementation:

MANIFEST:
$MANIFEST

IMPLEMENTATION:
$IMPLEMENTATION

Questions:
1. Does the implementation match the description?
2. Are there features described but not implemented?
3. Are there features implemented but not described?
4. Is the description accurate and complete?

Output JSON:
{
  \"description_accurate\": boolean,
  \"missing_features\": [\"feature1\", \"feature2\"],
  \"undocumented_features\": [\"feature3\"],
  \"accuracy_score\": 0.0-1.0,
  \"issues\": [
    {
      \"type\": \"missing_feature\",
      \"severity\": \"high|medium|low\",
      \"description\": \"...\",
      \"suggestion\": \"...\"
    }
  ]
}
" > /tmp/validation-description.json
```

### Step 3: Validate Preconditions

```bash
# Check if preconditions are actually enforced in code
PRECONDITIONS=$(python3 -c "
import yaml, json
manifest = yaml.safe_load(open('$MANIFEST_PATH'))
print(json.dumps(manifest.get('preconditions', []), indent=2))
")

codex exec "
Analyze if these preconditions are actually checked in the code:

PRECONDITIONS:
$PRECONDITIONS

IMPLEMENTATION:
$IMPLEMENTATION

For each precondition, determine:
1. Is it checked in the code?
2. Where is it checked (function name, line number)?
3. Does it fail gracefully if not met?
4. Is the error message clear?

Output JSON:
{
  \"preconditions_validated\": [
    {
      \"check\": \"file_exists('package.json')\",
      \"enforced\": boolean,
      \"location\": \"function:line\",
      \"error_handling\": \"good|poor|missing\",
      \"suggestion\": \"...\"
    }
  ],
  \"coverage_score\": 0.0-1.0
}
" > /tmp/validation-preconditions.json
```

### Step 4: Validate Effects

```bash
# Check if claimed effects are actually produced
EFFECTS=$(python3 -c "
import yaml, json
manifest = yaml.safe_load(open('$MANIFEST_PATH'))
print(json.dumps(manifest.get('effects', []), indent=2))
")

codex exec "
Verify that this code actually produces the claimed effects:

CLAIMED EFFECTS:
$EFFECTS

IMPLEMENTATION:
$IMPLEMENTATION

For each effect, determine:
1. Is the effect actually produced?
2. Where in the code does it happen?
3. Are there conditions where it might not happen?
4. Are there other effects not listed?

Output JSON:
{
  \"effects_validated\": [
    {
      \"effect\": \"creates_vector_index\",
      \"implemented\": boolean,
      \"location\": \"function:line\",
      \"conditional\": boolean,
      \"confidence\": 0.0-1.0
    }
  ],
  \"missing_effects\": [\"effect1\"],
  \"extra_effects\": [\"effect2\"],
  \"coverage_score\": 0.0-1.0
}
" > /tmp/validation-effects.json
```

### Step 5: Validate API Surface

```bash
# For MCPs/tools with defined APIs, validate exports
if [ -n "$IMPLEMENTATION" ]; then
  codex exec "
Analyze the API surface of this implementation:

IMPLEMENTATION:
$IMPLEMENTATION

Questions:
1. What functions/classes are exported?
2. What are their signatures?
3. Are they documented?
4. Do they match what the manifest describes?

Output JSON:
{
  \"exports\": [
    {
      \"name\": \"functionName\",
      \"type\": \"function|class|object\",
      \"signature\": \"(args) => result\",
      \"documented\": boolean
    }
  ],
  \"api_complete\": boolean,
  \"documentation_quality\": \"good|fair|poor\"
}
" > /tmp/validation-api.json
fi
```

### Step 6: Generate Validation Report

```bash
# Combine all validation results
python3 <<'PYTHON_SCRIPT'
import json
from datetime import datetime

# Load validation results
with open('/tmp/validation-description.json') as f:
    desc_validation = json.load(f)

with open('/tmp/validation-preconditions.json') as f:
    precond_validation = json.load(f)

with open('/tmp/validation-effects.json') as f:
    effects_validation = json.load(f)

try:
    with open('/tmp/validation-api.json') as f:
        api_validation = json.load(f)
except FileNotFoundError:
    api_validation = None

# Calculate overall score
scores = [
    desc_validation.get('accuracy_score', 0),
    precond_validation.get('coverage_score', 0),
    effects_validation.get('coverage_score', 0)
]
overall_score = sum(scores) / len(scores)

# Collect all issues
all_issues = []
all_issues.extend(desc_validation.get('issues', []))

for precond in precond_validation.get('preconditions_validated', []):
    if not precond.get('enforced'):
        all_issues.append({
            'type': 'unenforced_precondition',
            'severity': 'medium',
            'description': f"Precondition not enforced: {precond['check']}",
            'suggestion': precond.get('suggestion', '')
        })

for effect in effects_validation.get('effects_validated', []):
    if not effect.get('implemented'):
        all_issues.append({
            'type': 'unimplemented_effect',
            'severity': 'high',
            'description': f"Effect not implemented: {effect['effect']}",
            'suggestion': 'Implement this effect or remove from manifest'
        })

# Generate report
report = {
    'resource': 'RESOURCE_NAME_PLACEHOLDER',
    'validated_at': datetime.utcnow().isoformat() + 'Z',
    'overall_score': round(overall_score, 3),
    'scores': {
        'description_accuracy': desc_validation.get('accuracy_score', 0),
        'precondition_coverage': precond_validation.get('coverage_score', 0),
        'effect_coverage': effects_validation.get('coverage_score', 0)
    },
    'validation_results': {
        'description': desc_validation,
        'preconditions': precond_validation,
        'effects': effects_validation,
        'api': api_validation
    },
    'issues': all_issues,
    'issue_count': len(all_issues),
    'passed': overall_score >= 0.8 and len([i for i in all_issues if i['severity'] == 'high']) == 0
}

with open('/tmp/validation-report.json', 'w') as f:
    json.dump(report, f, indent=2)

# Print summary
print(f"\nValidation Score: {overall_score:.2f}")
print(f"Issues Found: {len(all_issues)}")
print(f"Status: {'✅ PASSED' if report['passed'] else '❌ FAILED'}")
PYTHON_SCRIPT
```

## Validation Criteria

### Scoring Rules

```javascript
// Overall score is average of component scores
overallScore = (descriptionAccuracy + preconditionCoverage + effectCoverage) / 3

// Pass criteria
passed = overallScore >= 0.8 && highSeverityIssues.length === 0
```

### Severity Levels

- **High**: Missing core functionality, unenforced preconditions, unimplemented effects
- **Medium**: Incomplete features, poor error handling, undocumented exports
- **Low**: Minor inconsistencies, documentation gaps, style issues

## Example Output

```json
{
  "resource": "rag-implementer",
  "validated_at": "2025-10-28T12:00:00Z",
  "overall_score": 0.85,
  "scores": {
    "description_accuracy": 0.9,
    "precondition_coverage": 0.8,
    "effect_coverage": 0.85
  },
  "validation_results": {
    "description": {
      "description_accurate": true,
      "missing_features": [],
      "undocumented_features": ["vector_index_optimization"],
      "accuracy_score": 0.9,
      "issues": [
        {
          "type": "undocumented_feature",
          "severity": "low",
          "description": "Implementation includes vector optimization not mentioned in manifest",
          "suggestion": "Add 'optimizes_vector_queries' to effects"
        }
      ]
    },
    "preconditions": {
      "preconditions_validated": [
        {
          "check": "file_exists('package.json')",
          "enforced": true,
          "location": "validateProject:12",
          "error_handling": "good"
        },
        {
          "check": "env_var_set('OPENAI_API_KEY')",
          "enforced": true,
          "location": "setupEmbeddings:45",
          "error_handling": "good"
        }
      ],
      "coverage_score": 0.8
    },
    "effects": {
      "effects_validated": [
        {
          "effect": "creates_vector_index",
          "implemented": true,
          "location": "createIndex:120",
          "conditional": false,
          "confidence": 0.95
        },
        {
          "effect": "adds_embedding_pipeline",
          "implemented": true,
          "location": "setupPipeline:85",
          "conditional": false,
          "confidence": 0.9
        }
      ],
      "missing_effects": [],
      "extra_effects": ["optimizes_vector_queries"],
      "coverage_score": 0.85
    }
  },
  "issues": [
    {
      "type": "undocumented_feature",
      "severity": "low",
      "description": "Implementation includes vector optimization not mentioned in manifest",
      "suggestion": "Add 'optimizes_vector_queries' to effects"
    }
  ],
  "issue_count": 1,
  "passed": true
}
```

## Integration

### With manifest-generator

Validates that generated manifests are accurate by comparing with implementation.

### With capability-graph-builder

Ensures graph relationships are based on accurate capability descriptions.

### CI/CD Pipeline

```yaml
# .github/workflows/validate-skills.yml
name: Validate Skills

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Validate all skills
        run: |
          for skill in SKILLS/*/; do
            bash SKILLS/skill-validator/validate.sh "$skill"
          done
```

## Success Metrics

- ✅ All skills score >= 0.8
- ✅ No high severity issues in production skills
- ✅ 100% of preconditions enforced
- ✅ 95%+ of effects implemented
- ✅ API surface matches manifest

## Related Skills

- manifest-generator: Generates manifests to be validated
- capability-graph-builder: Uses validated manifests
- system-diagnostician: Uses validation results for health checks
