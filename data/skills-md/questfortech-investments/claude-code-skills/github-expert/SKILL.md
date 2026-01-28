---
name: github-expert
description: Complete GitHub expertise covering GitHub Actions, CI/CD workflows, automation, repository management, and best practices. Use when setting up GitHub Actions, creating workflows, managing pull requests, configuring automation (Dependabot, CodeQL), or implementing GitHub best practices. Includes workflow generators, templates, and production-ready configurations.
---

# GitHub Expert

## Overview

Transform into a GitHub expert with comprehensive knowledge of GitHub Actions, CI/CD workflows, repository automation, and development best practices. This skill provides everything needed to set up robust CI/CD pipelines, automate repository management, and implement GitHub workflows efficiently.

## Core Capabilities

### 1. GitHub Actions & CI/CD Workflows

Create and manage GitHub Actions workflows for continuous integration and deployment.

**Script: `scripts/create_workflow.py`**

Generate production-ready workflow files for common scenarios:

```bash
# Node.js CI workflow
python scripts/create_workflow.py ci --type nodejs-ci

# Python CI workflow
python scripts/create_workflow.py ci --type python-ci

# Docker build and push
python scripts/create_workflow.py docker --type docker-build

# Automated releases
python scripts/create_workflow.py release --type release

# Azure deployment
python scripts/create_workflow.py deploy-azure --type deploy-azure

# Dependabot auto-merge
python scripts/create_workflow.py dependabot --type dependabot-auto-merge
```

**Available Templates:**
- `nodejs-ci`: Node.js testing and building with multiple versions
- `python-ci`: Python testing with multiple Python versions
- `docker-build`: Docker build and push to GitHub Container Registry
- `release`: Automated release creation with changelog
- `deploy-azure`: Deploy to Azure App Service
- `dependabot-auto-merge`: Auto-merge Dependabot PRs

**When to use:**
- Setting up new project CI/CD
- Adding automated testing
- Implementing deployment automation
- Configuring Docker builds
- Setting up release automation

**Reference: `references/github_actions_guide.md`**

Comprehensive guide covering:
- Workflow syntax and structure
- Common events and triggers
- Matrix strategies for multi-platform testing
- Caching and optimization
- Secrets management
- Best practices (pinning actions, minimizing permissions)
- Troubleshooting common issues
- Advanced patterns (reusable workflows, composite actions)

**When to consult:**
- Learning GitHub Actions syntax
- Debugging workflow issues
- Need optimization strategies
- Security best practices
- Advanced workflow patterns

### 2. Repository Automation

Automate repository management with Dependabot and CodeQL.

**Assets available:**

**`assets/dependabot.yml`**
Configure automated dependency updates:
- Weekly updates for npm, GitHub Actions
- Security updates daily
- Auto-labels and commit messages
- Grouped updates to reduce PR noise

**Usage:**
1. Copy to `.github/dependabot.yml`
2. Customize package ecosystems (npm, pip, docker, etc.)
3. Adjust update schedule
4. Set up auto-merge workflow (optional)

**`assets/codeql-analysis.yml`**
Automated security scanning:
- Scans on push, PR, and scheduled
- Multi-language support
- Automatic vulnerability detection
- Security alerts integration

**Usage:**
1. Copy to `.github/workflows/codeql-analysis.yml`
2. Select languages to scan
3. Enable in repository security settings
4. Review security alerts regularly

**When to use:**
- Keeping dependencies updated
- Security scanning
- Vulnerability detection
- Compliance requirements

### 3. Pull Request Management

Standardize pull request process with templates.

**`assets/pull_request_template.md`**
Comprehensive PR template with:
- Description and change type
- Related issues linking
- Testing checklist
- Deployment notes
- Review guidelines

**Usage:**
1. Copy to `.github/pull_request_template.md`
2. Customize sections for your workflow
3. All new PRs will use this template

**Benefits:**
- Consistent PR documentation
- Ensures testing is done
- Links issues automatically
- Improves code review process

### 4. Issue Management

Create structured issue templates.

**`assets/bug_report_template.md`**
Bug report template with:
- Clear bug description
- Reproduction steps
- Expected vs actual behavior
- Environment information
- Screenshots and logs

**Usage:**
1. Create `.github/ISSUE_TEMPLATE/`
2. Copy bug_report_template.md there
3. Create additional templates (feature request, etc.)

**Benefits:**
- Consistent bug reports
- Easier triaging
- Faster debugging
- Better user experience

### 5. Release Automation

Generate release notes automatically.

**Script: `scripts/generate_release_notes.sh`**

Generates formatted release notes from git history:

```bash
# Generate notes between tags
./scripts/generate_release_notes.sh v1.0.0 v1.1.0

# Generate notes from last tag to HEAD
./scripts/generate_release_notes.sh

# Save to file
./scripts/generate_release_notes.sh > notes.md

# Create GitHub release
gh release create v1.1.0 --notes-file notes.md
```

**Features:**
- Categorizes commits (features, fixes, docs, etc.)
- Lists contributors
- Shows statistics
- Conventional commit support

**When to use:**
- Creating releases
- Publishing changelogs
- Documenting version changes
- Communicating updates

## Workflow Examples

### Example 1: "Set up CI/CD for my Node.js project"

1. **Generate CI workflow**:
   ```bash
   python scripts/create_workflow.py ci --type nodejs-ci
   ```

2. **Review generated workflow**:
   - Check `.github/workflows/ci.yml`
   - Verify Node.js versions in matrix
   - Ensure test scripts match package.json

3. **Add deployment** (if needed):
   ```bash
   python scripts/create_workflow.py deploy --type deploy-azure
   ```

4. **Set up secrets**:
   ```bash
   gh secret set AZURE_CREDENTIALS --body "$(az ad sp create-for-rbac --sdk-auth)"
   ```

5. **Push and verify**:
   - Commit workflows
   - Push to GitHub
   - Check Actions tab

### Example 2: "Enable automated dependency updates"

1. **Add Dependabot config**:
   - Copy `assets/dependabot.yml` to `.github/dependabot.yml`
   - Customize ecosystems and schedule

2. **Set up auto-merge** (optional):
   ```bash
   python scripts/create_workflow.py dependabot --type dependabot-auto-merge
   ```

3. **Configure branch protection**:
   - Require status checks
   - Require review for manual PRs
   - Allow Dependabot to bypass for minor/patch

4. **Monitor**:
   - Check Insights → Dependency graph
   - Review Dependabot PRs
   - Merge or configure as needed

### Example 3: "Add security scanning"

1. **Enable CodeQL**:
   - Copy `assets/codeql-analysis.yml` to `.github/workflows/`
   - Select languages for your project

2. **Enable security features**:
   - Settings → Security → Code security and analysis
   - Enable Dependabot alerts
   - Enable Dependabot security updates
   - Enable Secret scanning

3. **Review alerts**:
   - Check Security tab
   - Review and fix vulnerabilities
   - Update dependencies

### Example 4: "Standardize PR and issue process"

1. **Add PR template**:
   ```bash
   cp assets/pull_request_template.md .github/pull_request_template.md
   ```

2. **Add issue templates**:
   ```bash
   mkdir -p .github/ISSUE_TEMPLATE
   cp assets/bug_report_template.md .github/ISSUE_TEMPLATE/
   ```

3. **Configure branch protection**:
   - Require PR before merging
   - Require reviews
   - Require status checks
   - Enforce linear history (optional)

4. **Test**:
   - Create new PR - should show template
   - Create new issue - should show template options

### Example 5: "Create a release with notes"

1. **Generate release notes**:
   ```bash
   ./scripts/generate_release_notes.sh v1.0.0 v1.1.0 > notes.md
   ```

2. **Review and edit notes**:
   - Check categorization
   - Add highlights
   - Note breaking changes

3. **Create release**:
   ```bash
   gh release create v1.1.0 --notes-file notes.md
   ```

4. **Or use workflow**:
   - Push tag: `git tag v1.1.0 && git push --tags`
   - Workflow creates release automatically

## Best Practices

### GitHub Actions
- Pin actions to SHA for security
- Use caching to speed up workflows
- Minimize permissions (least privilege)
- Use concurrency to cancel old runs
- Enable debug mode for troubleshooting
- Use reusable workflows for common patterns

### Repository Management
- Enable branch protection on main
- Require status checks before merge
- Use CODEOWNERS for auto-assignment
- Configure auto-merge for trusted automation
- Regular security audits

### CI/CD Pipeline
- Test on multiple platforms/versions
- Fail fast (don't waste resources)
- Cache dependencies appropriately
- Separate build and deploy jobs
- Use environments for deployment gates
- Monitor workflow execution times

### Security
- Never log secrets
- Use environment secrets, not repository secrets for sensitive data
- Enable secret scanning
- Regular dependency updates
- Use Dependabot security updates
- Review and rotate tokens regularly

## Quick Reference

### Common Commands

```bash
# Generate workflow
python scripts/create_workflow.py <name> --type <template>

# Generate release notes
./scripts/generate_release_notes.sh [prev-tag] [current-tag]

# GitHub CLI
gh workflow run <workflow-name>
gh run list
gh run watch
gh secret set <name>
gh release create <tag>
```

### File Locations

```
.github/
├── workflows/          # GitHub Actions workflows
│   ├── ci.yml
│   ├── deploy.yml
│   └── codeql.yml
├── dependabot.yml     # Dependabot configuration
├── CODEOWNERS         # Code ownership
├── pull_request_template.md
└── ISSUE_TEMPLATE/
    ├── bug_report.md
    └── feature_request.md
```

### Common Workflow Events

- `push`: Code pushed to branch
- `pull_request`: PR opened/updated/closed
- `release`: Release published
- `workflow_dispatch`: Manual trigger
- `schedule`: Cron schedule
- `issues`: Issue opened/closed
- `pull_request_target`: PR from fork (security)

## Reference Documentation

### references/github_actions_guide.md

**Read when:**
- Learning GitHub Actions
- Creating custom workflows
- Debugging workflow issues
- Need advanced patterns
- Security questions

**Key sections:**
- Quick Reference (syntax, events, common actions)
- CI/CD Patterns (matrix, caching, conditionals)
- Secrets Management
- Best Practices
- Common Workflows
- Troubleshooting
- Advanced Patterns

## When NOT to Use This Skill

- **GitLab CI/CD**: Different syntax and platform
- **Bitbucket Pipelines**: Different platform
- **Jenkins**: Self-hosted CI/CD tool
- **GitHub Enterprise Server**: May have different features/limitations

For these topics, provide general CI/CD guidance but acknowledge platform differences.

## Success Metrics

Your GitHub repository should have:
- ✅ CI workflow running on PRs
- ✅ Automated dependency updates
- ✅ Security scanning enabled
- ✅ PR template in place
- ✅ Branch protection configured
- ✅ All workflows passing
- ✅ Secrets properly managed
- ✅ Regular releases with notes
