---
name: self-improving
description: Use when starting infrastructure, testing, deployment, or framework-specific tasks - automatically searches PRPM registry for relevant expertise packages and suggests installation to enhance capabilities for the current task
---

# Self-Improving with PRPM

## Purpose

Automatically search and install PRPM packages to enhance Claude's capabilities for specific tasks. When working on infrastructure, testing, deployment, or framework-specific work, Claude searches the PRPM registry for relevant expertise and suggests packages to install.

## When to Use

**Automatically triggers when detecting:**
- Infrastructure keywords: aws, pulumi, terraform, kubernetes, docker, beanstalk
- Testing keywords: test, playwright, jest, cypress, vitest, e2e
- Deployment keywords: ci/cd, github-actions, gitlab-ci, deploy, workflow
- Framework keywords: react, vue, next.js, express, fastify, django

## Workflow

### 1. Task Analysis
Analyze user request for keywords and extract relevant terms.

### 2. Automatic Search
```bash
prpm search "<detected keywords>" --limit 5 --no-interactive
```

### 3. Package Suggestion
Present top 3 most relevant packages with:
- Package name and author
- Download count
- Brief description
- Confidence level (official/featured/community)

### 4. Installation (with approval)
```bash
prpm install <package-name> --as claude
```

### 5. Application
Load package knowledge and apply to current task.

## Decision Rules

### High Confidence (Auto-suggest)
- ✅ Official packages (`@prpm/*`)
- ✅ Featured packages
- ✅ High downloads (>1,000)
- ✅ Verified authors

### Medium Confidence (Present options)
- ⚠️ Community packages (<1,000 downloads)
- ⚠️ Multiple similar packages
- ⚠️ Tangentially related packages

### Low Confidence (Skip)
- ❌ Unverified packages
- ❌ Deprecated packages
- ❌ Zero downloads

## Example Interaction

```
User: "Help me build Pulumi + Beanstalk infrastructure"

Analysis:
  Keywords: Pulumi, Beanstalk, infrastructure
  Search: prpm search "pulumi beanstalk infrastructure"
  Found: @prpm/pulumi-infrastructure (Official, 3.2K downloads)
  Confidence: High → Auto-suggest

Response:
"I found an official PRPM package that can help:

📦 @prpm/pulumi-infrastructure (Official, 3.2K downloads)
   - Pulumi TypeScript best practices
   - AWS resource patterns
   - Cost optimization guidelines

Should I install this to enhance my Pulumi knowledge?"

User: "Yes"

Action:
  ✅ Installing: prpm install @prpm/pulumi-infrastructure --as claude
  ✅ Loading knowledge
  ✅ Applying patterns to current task
```

## Search Triggers

### Infrastructure Tasks
**Keywords**: aws, gcp, azure, kubernetes, docker, pulumi, terraform
**Search**: `prpm search "infrastructure <cloud> <tool>"`

### Testing Tasks
**Keywords**: test, playwright, jest, cypress, vitest, e2e
**Search**: `prpm search "testing <framework>"`

### CI/CD Tasks
**Keywords**: ci/cd, github-actions, gitlab-ci, deploy, workflow
**Search**: `prpm search "deployment <platform>"`

### Framework Tasks
**Keywords**: react, vue, angular, next.js, express, django
**Search**: `prpm search "<framework> best-practices"`

## Search Commands

```bash
# Basic search
prpm search "keyword1 keyword2"

# author filter
prpm search --author "prpm"

# Type filter
prpm search --format claude "infrastructure"

# Sub Type filter
prpm search --format claude --subtype skill "infrastructure"

# Limit results
prpm search "github actions" --limit 5

# Sort by downloads
prpm search "testing" --sort downloads
```

## Best Practices

1. **Be Proactive**: Search before starting complex tasks
2. **Verify Quality**: Check download counts and official status
3. **Ask Permission**: Always get user approval before installing
4. **Apply Knowledge**: Immediately use installed package patterns
5. **Track Helpfulness**: Note which packages were useful

## Meta-Dogfooding

Recognize packages PRPM used to build itself:
- `@prpm/pulumi-infrastructure` → PRPM's own infrastructure (74% cost savings)
- `@sanjeed5/github-actions` → PRPM's workflow validation
- Testing packages → PRPM's E2E test patterns

**Benefit**: Users get the same expertise that built PRPM.

## Privacy

- ✅ All searches are local
- ✅ No data sent to PRPM for searches
- ✅ Download tracking only on install
- ✅ No personal data collected

Remember: Self-improvement through package discovery makes Claude more capable for each specific task domain.
