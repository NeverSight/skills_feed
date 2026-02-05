---
name: terraform-best-practices
description: Terraform and Infrastructure as Code optimization guidelines from Terramate. This skill should be used when writing, reviewing, or refactoring Terraform/OpenTofu code to ensure optimal patterns for security, maintainability, and reliability. Triggers on tasks involving Terraform modules, infrastructure provisioning, state management, or IaC optimization.
license: MIT
metadata:
  author: terramate
  version: "1.0.0"
---

# Terraform Best Practices

Comprehensive optimization guide for Terraform and Infrastructure as Code, maintained by Terramate. Contains 37 rules across 10 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Writing new Terraform modules or configurations
- Implementing infrastructure patterns (AWS, GCP, Azure, etc.)
- Reviewing code for security and reliability issues
- Refactoring existing Terraform/OpenTofu code
- Optimizing state management and performance
- Setting up team workflows and governance

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Organization & Workflow | CRITICAL | `org-` |
| 2 | State Management | CRITICAL | `state-` |
| 3 | Security Best Practices | CRITICAL | `security-` |
| 4 | Module Design | HIGH | `module-` |
| 5 | Resource Organization | MEDIUM-HIGH | `resource-` |
| 6 | Variable & Output Patterns | MEDIUM | `variable-`, `output-` |
| 7 | Language Best Practices | MEDIUM | `language-` |
| 8 | Provider Configuration | MEDIUM | `provider-` |
| 9 | Performance Optimization | LOW-MEDIUM | `perf-` |
| 10 | Testing & Validation | LOW | `test-` |

## Quick Reference

### 1. Organization & Workflow (CRITICAL) - 5 rules

- `org-version-control` - All Terraform code in version control
- `org-workspaces` - One workspace per environment per configuration
- `org-access-control` - Control who can change what infrastructure
- `org-change-workflow` - Formal process for infrastructure changes
- `org-audit-logging` - Track all infrastructure changes

### 2. State Management (CRITICAL) - 3 rules

- `state-remote-backend` - Always use remote state backends
- `state-locking` - Enable state locking to prevent corruption
- `state-import` - Import existing infrastructure into Terraform

### 3. Security Best Practices (CRITICAL) - 3 rules

- `security-no-hardcoded-secrets` - Never hardcode secrets in code
- `security-credentials` - Use proper credential management (OIDC, Vault, IAM roles)
- `security-iam-least-privilege` - Follow least privilege principle

### 4. Module Design (HIGH) - 5 rules

- `module-single-responsibility` - One module per logical component
- `module-naming` - Use consistent naming conventions (terraform-<PROVIDER>-<NAME>)
- `module-versioning` - Version all module references
- `module-composition` - Compose modules like building blocks
- `module-registry` - Use existing community/shared modules

### 5. Resource Organization (MEDIUM-HIGH) - 5 rules

- `resource-naming` - Use consistent naming conventions
- `resource-tagging` - Tag all resources for cost tracking
- `resource-lifecycle` - Use lifecycle blocks (prevent_destroy, ignore_changes)
- `resource-count-vs-foreach` - Prefer for_each over count
- `resource-immutable` - Prefer immutable infrastructure patterns

### 6. Variable & Output Patterns (MEDIUM) - 6 rules

- `variable-types` - Use specific types, positive naming, nullable
- `variable-validation` - Add validation rules for early error detection
- `variable-sensitive` - Mark secrets as sensitive, no defaults
- `variable-descriptions` - Document all variables with descriptions
- `output-descriptions` - Document all outputs with descriptions
- `output-no-secrets` - Never output secrets directly

### 7. Language Best Practices (MEDIUM) - 5 rules

- `language-no-heredoc-json` - Use jsonencode/yamlencode, not HEREDOC
- `language-locals` - Use locals to name complex expressions
- `language-linting` - Run terraform fmt and tflint
- `language-data-sources` - Use data sources instead of hardcoding
- `language-dynamic-blocks` - Use dynamic blocks for DRY code

### 8. Provider Configuration (MEDIUM) - 1 rule

- `provider-version-constraints` - Pin provider versions

### 9. Performance Optimization (LOW-MEDIUM) - 2 rules

- `perf-parallelism` - Tune parallelism for large deployments
- `perf-debug` - Enable debug logging for troubleshooting

### 10. Testing & Validation (LOW) - 2 rules

- `test-strategies` - Testing pyramid (validate, lint, plan, integration)
- `test-policy-as-code` - Implement policy checks (OPA, Checkov, tfsec)

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/state-remote-backend.md
rules/security-no-hardcoded-secrets.md
rules/module-versioning.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
