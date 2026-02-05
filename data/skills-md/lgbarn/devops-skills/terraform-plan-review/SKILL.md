---
name: terraform-plan-review
description: Use when analyzing terraform/tofu plan output for risks, security issues, and potential service disruptions. Required before any apply operation.
---

# Terraform Plan Review

## Overview

Analyze terraform plan output using parallel agents for comprehensive risk assessment. **Never auto-apply** - always present findings and require explicit approval.

**Announce at start:** "I'm using the terraform-plan-review skill to analyze these changes safely."

## The Process

### Step 1: Verify Environment

Before running any plan:

1. **Check AWS Profile**
   ```bash
   aws sts get-caller-identity
   ```
   - Verify the account ID matches expected environment
   - Verify the role/user is appropriate for this operation
   - If mismatch: STOP and alert user

2. **Identify Environment**
   - Check current directory structure (which environment?)
   - Verify backend configuration matches environment

### Step 2: Generate Plan

```bash
# Initialize if needed
terraform init

# Generate plan file (required for JSON parsing)
terraform plan -out=plan.out

# Convert to JSON for analysis
terraform show -json plan.out > plan.json
```

### Step 3: Dispatch Parallel Analysis Agents

Launch these agents in a **single message with multiple Task calls**:

```
Task 1:
  description: "Analyze plan risks"
  prompt: |
    Analyze this Terraform plan for risks and impact.
    Environment: [env name]
    Account: [account id]

    Plan JSON:
    [plan.json content]

    Focus on destruction, modification risks, and cascade effects.
  subagent_type: "terraform-plan-analyzer"

Task 2:
  description: "Security review plan"
  prompt: |
    Review this Terraform plan for security implications.
    Environment: [env name]

    Plan JSON:
    [plan.json content]

    Focus on IAM, network, encryption, and compliance.
  subagent_type: "security-reviewer"

Task 3:
  description: "Check historical patterns"
  prompt: |
    Analyze git history for patterns related to these resources.
    Resources being changed: [list from plan]

    Look for similar past changes, incidents, and outcomes.
  subagent_type: "historical-pattern-analyzer"
```

**CRITICAL:** All three Task calls in ONE message for parallel execution.

**Agent prompts should include:**
- The plan.json content (or path)
- The environment name
- Any relevant context from memory

### Step 4: Aggregate Findings

Collect results from all agents and create a unified report:

```markdown
## Plan Analysis Summary

### Risk Level: [CRITICAL/HIGH/MEDIUM/LOW]

### Changes Overview
- Resources to create: X
- Resources to update: Y
- Resources to destroy: Z

### Risk Analysis (terraform-plan-analyzer)
[Summary of risks identified]

### Security Analysis (security-reviewer)
[Summary of security implications]

### Pattern Analysis (historical-pattern-analyzer)
[Any similar past changes and their outcomes]

### Required Approvals
- [ ] User acknowledges destruction of X resources
- [ ] User confirms this is the correct environment
- [ ] User approves proceeding with apply
```

### Step 5: Approval Gate

Present the analysis to the user and **wait for explicit approval**:

> "Based on my analysis, this plan has [RISK LEVEL] risk. [Summary of key findings].
>
> Do you want me to proceed with `terraform apply`? Please respond with 'approve' to continue."

**NEVER proceed without explicit "approve" from user.**

### Step 6: Execute Apply (Only After Approval)

If and only if user explicitly approves:

```bash
terraform apply plan.out
```

Monitor output and report results.

## Risk Categories

### CRITICAL - Requires Extra Scrutiny
- Any resource destruction
- IAM policy changes
- Security group rule modifications
- Database modifications
- Encryption key changes
- Cross-account resource access

### HIGH
- Network configuration changes
- Load balancer modifications
- Auto-scaling changes
- DNS record modifications

### MEDIUM
- Instance type changes
- Tag modifications
- Non-critical configuration updates

### LOW
- Pure additions with no dependencies
- Documentation-only changes

## Common Patterns to Flag

1. **Cascade Deletions**: Resource deletion that triggers other deletions
2. **State Drift**: Plan shows changes that weren't in code
3. **Dependency Chains**: Changes that affect many downstream resources
4. **Security Relaxation**: Rules becoming more permissive
5. **Cost Impact**: Significant size/count changes

## Memory Integration

Before analysis, query memory for:
- Similar changes in this project's history
- Known issues with affected resources
- Past incidents related to this type of change

After completion, store:
- Outcome of this change (success/failure)
- Any issues encountered
- User preferences learned

## Verification Checklist

Before presenting to user, verify:
- [ ] AWS profile matches environment
- [ ] Plan was generated successfully
- [ ] All agents completed analysis
- [ ] Risk level is accurately assessed
- [ ] All destruction operations are highlighted
- [ ] Security implications are documented
