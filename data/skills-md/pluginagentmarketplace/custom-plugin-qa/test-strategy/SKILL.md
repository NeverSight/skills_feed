---
name: test-strategy
description: Production-grade test strategy skill with risk-based testing, coverage analysis, quality gates, and resource optimization
sasmp_version: "1.3.0"
bonded_agent: qa-expert
bond_type: PRIMARY_BOND
version: "2.1.0"
---

# Test Strategy Skill

## Overview

Enterprise-grade test strategy capabilities for risk-based test planning, coverage optimization, and quality gate management.

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "action": {
      "type": "string",
      "enum": ["create_strategy", "analyze_coverage", "assess_risk", "optimize", "generate_plan"],
      "description": "Strategy action to perform"
    },
    "project_context": {
      "type": "object",
      "properties": {
        "type": {"type": "string", "enum": ["web", "mobile", "api", "desktop", "embedded"]},
        "size": {"type": "string", "enum": ["small", "medium", "large", "enterprise"]},
        "methodology": {"type": "string", "enum": ["agile", "waterfall", "hybrid", "devops"]},
        "team_size": {"type": "integer", "minimum": 1},
        "timeline_weeks": {"type": "integer", "minimum": 1}
      }
    },
    "requirements": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {"type": "string"},
          "description": {"type": "string"},
          "priority": {"type": "string", "enum": ["critical", "high", "medium", "low"]},
          "complexity": {"type": "string", "enum": ["simple", "moderate", "complex"]}
        }
      }
    },
    "constraints": {
      "type": "object",
      "properties": {
        "budget": {"type": "string"},
        "resources": {"type": "integer"},
        "deadline": {"type": "string", "format": "date"},
        "automation_target": {"type": "number", "minimum": 0, "maximum": 100}
      }
    },
    "quality_targets": {
      "type": "object",
      "properties": {
        "code_coverage": {"type": "number", "minimum": 0, "maximum": 100},
        "defect_escape_rate": {"type": "number", "minimum": 0, "maximum": 100},
        "test_pass_rate": {"type": "number", "minimum": 0, "maximum": 100}
      }
    }
  },
  "required": ["action"]
}
```

## Output Schema

```json
{
  "type": "object",
  "properties": {
    "status": {"type": "string", "enum": ["success", "partial", "failed"]},
    "strategy": {
      "type": "object",
      "properties": {
        "scope": {"type": "object"},
        "approach": {"type": "string"},
        "test_levels": {"type": "array"},
        "test_types": {"type": "array"},
        "automation_strategy": {"type": "object"},
        "resource_allocation": {"type": "object"},
        "timeline": {"type": "object"},
        "quality_gates": {"type": "array"}
      }
    },
    "risk_assessment": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "area": {"type": "string"},
          "risk_level": {"type": "string"},
          "mitigation": {"type": "string"},
          "testing_focus": {"type": "string"}
        }
      }
    },
    "coverage_analysis": {
      "type": "object",
      "properties": {
        "requirements_coverage": {"type": "number"},
        "code_coverage_estimate": {"type": "number"},
        "risk_coverage": {"type": "number"},
        "gaps": {"type": "array"}
      }
    },
    "recommendations": {"type": "array", "items": {"type": "string"}}
  }
}
```

## Parameter Validation

```yaml
project_context.type:
  required: false
  default: web
  validate:
    - type: enum
      values: [web, mobile, api, desktop, embedded]

project_context.size:
  required: false
  default: medium
  validate:
    - type: enum
      values: [small, medium, large, enterprise]

quality_targets.code_coverage:
  required: false
  default: 80
  validate:
    - type: range
      min: 0
      max: 100
    - type: realistic_check
      warn_below: 50
      warn_above: 95

constraints.automation_target:
  required: false
  default: 70
  validate:
    - type: range
      min: 0
      max: 100
```

## Error Handling

```yaml
retry_config:
  strategy: exponential_backoff
  max_retries: 3
  base_delay_ms: 1000
  max_delay_ms: 15000
  retryable_errors:
    - CALCULATION_TIMEOUT
    - INCOMPLETE_ANALYSIS

error_categories:
  input_errors:
    - MISSING_REQUIREMENTS
    - INVALID_CONSTRAINTS
    - CONFLICTING_PRIORITIES
    recovery: request_clarification

  analysis_errors:
    - COVERAGE_CALCULATION_FAILED
    - RISK_ASSESSMENT_INCOMPLETE
    - RESOURCE_ESTIMATION_FAILED
    recovery: use_defaults_with_warning

  optimization_errors:
    - NO_FEASIBLE_SOLUTION
    - CONSTRAINTS_TOO_STRICT
    - TIMELINE_UNREALISTIC
    recovery: suggest_constraint_relaxation
```

## Strategy Templates

### Agile Sprint Strategy
```yaml
name: agile_sprint_strategy
methodology: agile
sprint_duration: 2_weeks

test_distribution:
  unit_tests: 70%
  integration_tests: 20%
  e2e_tests: 10%

automation_approach:
  sprint_1: Setup framework, core flows
  sprint_2_onwards: Maintain 80% automation
  regression: Fully automated

quality_gates:
  - name: Sprint Ready
    criteria:
      - All stories have acceptance criteria
      - Test cases written before development

  - name: Development Complete
    criteria:
      - Unit tests pass (>80% coverage)
      - No critical bugs open

  - name: Sprint Done
    criteria:
      - All acceptance tests pass
      - Regression suite green
      - Performance baseline met
```

### Risk-Based Strategy
```yaml
name: risk_based_strategy
approach: focus_on_high_risk

risk_categories:
  critical:
    testing_effort: 40%
    automation: 100%
    test_depth: exhaustive

  high:
    testing_effort: 30%
    automation: 90%
    test_depth: comprehensive

  medium:
    testing_effort: 20%
    automation: 70%
    test_depth: standard

  low:
    testing_effort: 10%
    automation: 50%
    test_depth: basic

risk_factors:
  - Business impact
  - Technical complexity
  - Change frequency
  - Integration points
  - Security sensitivity
```

### Enterprise Strategy
```yaml
name: enterprise_strategy
scale: large

testing_pyramid:
  unit:
    percentage: 60%
    responsibility: developers
    automation: 100%

  integration:
    percentage: 25%
    responsibility: qa_and_developers
    automation: 95%

  e2e:
    percentage: 10%
    responsibility: qa
    automation: 80%

  exploratory:
    percentage: 5%
    responsibility: qa
    automation: 0%

governance:
  quality_gates: mandatory
  sign_off: required
  metrics_tracking: continuous
  compliance: enforced
```

## Coverage Analysis

### Requirements Coverage
```yaml
formula: (tested_requirements / total_requirements) * 100

categories:
  full_coverage: >= 95%
  adequate_coverage: 80-94%
  partial_coverage: 60-79%
  insufficient: < 60%

tracking:
  - Requirements traceability matrix
  - Automated coverage reports
  - Gap analysis
```

### Risk Coverage
```yaml
formula: weighted_average(
  critical_area_coverage * 4 +
  high_area_coverage * 3 +
  medium_area_coverage * 2 +
  low_area_coverage * 1
) / total_weight

target:
  critical: 100%
  high: 95%
  medium: 80%
  low: 60%
```

### Code Coverage
```yaml
types:
  - line_coverage
  - branch_coverage
  - function_coverage
  - statement_coverage

targets:
  unit_tests: >= 80%
  integration_tests: >= 60%
  overall: >= 75%

exclusions:
  - Generated code
  - Third-party libraries
  - Test utilities
```

## Quality Gates

### Gate 1: Requirements Ready
```yaml
name: requirements_ready
stage: pre_development
criteria:
  - [ ] All requirements documented
  - [ ] Acceptance criteria defined
  - [ ] Edge cases identified
  - [ ] Non-functional requirements specified
exit_criteria:
  completion: 100%
  sign_off: product_owner
```

### Gate 2: Development Complete
```yaml
name: development_complete
stage: post_development
criteria:
  - [ ] Unit tests passing (>80% coverage)
  - [ ] Code review completed
  - [ ] No critical/high bugs open
  - [ ] Integration tests passing
exit_criteria:
  unit_test_pass_rate: >= 95%
  code_coverage: >= 80%
  critical_bugs: 0
```

### Gate 3: Release Ready
```yaml
name: release_ready
stage: pre_release
criteria:
  - [ ] All test types executed
  - [ ] Performance benchmarks met
  - [ ] Security scan passed
  - [ ] Regression suite green
  - [ ] UAT sign-off obtained
exit_criteria:
  test_pass_rate: >= 98%
  defect_escape_rate: < 1%
  performance: within_sla
  security: no_critical_vulnerabilities
```

## Troubleshooting

### Issue: Coverage Targets Not Met
```yaml
symptoms:
  - Code coverage below threshold
  - Requirements gaps identified
  - Risk areas untested

diagnosis:
  1. Analyze coverage reports
  2. Identify untested areas
  3. Review test case mapping
  4. Check automation gaps

solutions:
  - Add missing test cases
  - Increase automation coverage
  - Focus on high-risk areas
  - Review and update requirements traceability
```

### Issue: Timeline Unrealistic
```yaml
symptoms:
  - Test execution delayed
  - Resources overallocated
  - Quality compromised

diagnosis:
  1. Review resource utilization
  2. Analyze bottlenecks
  3. Check dependencies
  4. Evaluate scope

solutions:
  - Prioritize by risk
  - Increase automation
  - Add resources
  - Negotiate scope reduction
  - Extend timeline
```

### Issue: High Defect Escape Rate
```yaml
symptoms:
  - Production bugs increasing
  - Customer complaints
  - Release rollbacks

diagnosis:
  1. Analyze escaped defects
  2. Review test coverage
  3. Check quality gates
  4. Evaluate testing depth

solutions:
  - Enhance test coverage for escape patterns
  - Add missing test types
  - Strengthen quality gates
  - Implement shift-left testing
  - Add exploratory testing
```

## Best Practices

```yaml
planning:
  - Start with risk assessment
  - Define clear quality gates
  - Set realistic targets
  - Plan for contingencies

execution:
  - Automate early and often
  - Track metrics continuously
  - Communicate status regularly
  - Adapt to changes quickly

optimization:
  - Review and refine regularly
  - Learn from defect escapes
  - Balance coverage and efficiency
  - Focus on value delivery
```

## Metrics Dashboard Template

```yaml
key_metrics:
  - name: Test Execution Rate
    formula: executed_tests / planned_tests * 100
    target: >= 100%

  - name: Test Pass Rate
    formula: passed_tests / executed_tests * 100
    target: >= 95%

  - name: Defect Detection Rate
    formula: defects_found / (defects_found + defects_escaped) * 100
    target: >= 95%

  - name: Automation Rate
    formula: automated_tests / total_tests * 100
    target: >= 70%

  - name: Coverage Score
    formula: weighted_average(requirements, code, risk)
    target: >= 85%
```

## Logging & Observability

```yaml
log_events:
  - strategy_created
  - quality_gate_evaluated
  - coverage_calculated
  - risk_assessed

metrics:
  - strategy_generation_time
  - coverage_trend
  - quality_gate_pass_rate
  - risk_score_distribution

dashboards:
  - Strategy Overview
  - Coverage Analysis
  - Quality Gate Status
  - Risk Heatmap
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.1.0 | 2025-01 | Production-grade with quality gates |
| 2.0.0 | 2024-12 | SASMP v1.3.0 compliance |
| 1.0.0 | 2024-11 | Initial release |
