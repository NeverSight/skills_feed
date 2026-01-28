---
name: azure-devops
description: "Provides expert guidance on Azure DevOps tasks including work item management, pipelines, repositories, pull requests, and CI/CD workflows. Use when working with Azure DevOps projects, configuring pipelines, managing work items, or integrating Azure DevOps with development workflows."
---

# Azure DevOps Skill

## Instructions

When working with Azure DevOps, follow these workflows based on task type:

### Work Items & Tracking
1. Identify the work item type (Epic, Feature, User Story, Task, Bug)
2. Set appropriate fields: Title, Description, Acceptance Criteria, State
3. Link related items (depends on, related to, blocked by)
4. Assign to team member and set sprint/iteration
5. Apply area path and tags for organization

### Repositories & Branches
1. Identify repository type (Git or TFVC)
2. For Git: Create feature branches following naming convention
3. Configure branch policies (require reviewers, build validation)
4. Set branch protection rules for main/develop branches
5. Configure merge strategies (squash, rebase, or three-way)

### Pull Requests
1. Create PR with clear title and description
2. Link to related work items (#1234 syntax)
3. Request appropriate reviewers
4. Ensure build passes and policy requirements met
5. Address review comments and iterate
6. Complete PR with appropriate merge strategy

### Pipelines & CI/CD
1. Determine pipeline type (Build, Release, Multi-stage YAML)
2. Configure triggers (commit, PR, scheduled, manual)
3. Set up agent pool and demands
4. Define stages and jobs
5. Add tasks for build, test, and deployment
6. Configure approvals and gates
7. Set up notifications and retention policies

### Test Management
1. Create test plans and test suites
2. Define test cases with steps and expected results
3. Run manual tests or automated tests
4. Link tests to work items
5. Generate test reports and track metrics

## Examples

### Example 1: Creating a Feature Work Item

**Scenario:** Need to add user authentication to a project

**Process:**
1. Create Feature work item with title "Implement User Authentication"
2. Add acceptance criteria:
   - Users can register with email/password
   - Users can login securely
   - Sessions persist across page reloads
   - Password reset functionality works
3. Create child User Stories:
   - "Registration form UI and validation"
   - "Authentication API endpoints"
   - "Session management"
   - "Password reset flow"
4. Link to Epic "Security & Auth"
5. Assign to team and add to sprint
6. Add tags: #authentication, #backend, #frontend

### Example 2: Setting Up YAML Pipeline

**Scenario:** Configure CI/CD for .NET project

**Pipeline Structure:**
```yaml
trigger:
  - main
  - develop

pr:
  - main
  - develop

pool:
  vmImage: 'windows-latest'

variables:
  buildConfiguration: 'Release'
  dotnetVersion: '6.0.x'

stages:
  - stage: Build
    jobs:
      - job: BuildJob
        steps:
          - task: UseDotNet@2
            inputs:
              version: $(dotnetVersion)
          - task: DotNetCoreCLI@2
            inputs:
              command: 'build'
              arguments: '--configuration $(buildConfiguration)'
          - task: DotNetCoreCLI@2
            inputs:
              command: 'test'
              arguments: '--configuration $(buildConfiguration) --no-build'

  - stage: Deploy
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - deployment: DeployJob
        environment: 'production'
        strategy:
          runOnce:
            deploy:
              steps:
                - task: PublishBuildArtifacts@1
                - task: AzureWebApp@1
                  inputs:
                    azureSubscription: 'Azure Connection'
                    appName: 'your-app-name'
```

### Example 3: Branch Policy Configuration

**Scenario:** Protect main branch with quality gates

**Settings:**
1. **Require pull request reviews:**
   - Minimum reviewers: 2
   - Require at least one approval from codeowners

2. **Build validation:**
   - Build policy: require build to pass
   - Build expiration: 720 minutes

3. **Automatic code review:**
   - Require approval from code owners

4. **Merge restrictions:**
   - Prevent completion with active comments
   - Default merge strategy: Squash commit

5. **Status checks:**
   - No optional status checks required

### Example 4: Pull Request Workflow

**PR Description Template:**
```markdown
## Description
Brief description of changes

## Linked Work Items
Fixes #1234
Related to #5678

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing Done
Describe testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Tests pass locally
- [ ] No new warnings generated
```

**Review Workflow:**
1. Create PR from feature branch to main/develop
2. Wait for build validation and status checks
3. Request reviewers (typically 2-3 team members)
4. Address feedback in follow-up commits
5. Once approved and checks pass, complete PR
6. Delete branch after merge (keep repository clean)

### Example 5: Multi-stage Pipeline with Approvals

**Scenario:** Production deployment requires approval

**Pipeline Configuration:**
1. Build stage: Automated on every commit
2. Integration stage: Run integration tests (requires build pass)
3. Staging stage: Deploy to staging (requires manual approval)
4. Production stage: Deploy to production (requires business approval + sign-off)

**Approval Gates:**
- Technical lead approves staging deployment
- Product manager approves production deployment
- Maximum wait time: 24 hours, then auto-reject
- Notifications sent to stakeholders

## Best Practices

### Work Item Management
- Keep descriptions concise but detailed enough to understand scope
- Break down large features into smaller user stories
- Use acceptance criteria to define "done"
- Link related items to show dependencies
- Update state and progress regularly
- Estimate using consistent units (story points or hours)
- Review and prioritize backlog regularly

### Repository & Code Management
- Use meaningful commit messages (Conventional Commits)
- Keep commits focused on single logical change
- Push frequently to avoid long-lived branches
- Delete merged branches to keep repo clean
- Protect critical branches with policies
- Use .gitignore and .gitattributes appropriately
- Tag releases for easy identification

### Pull Request Best Practices
- Create PRs early, even if still in progress (draft PR)
- Link to related work items
- Keep PRs focused and reasonably sized
- Write clear PR descriptions
- Respond to feedback promptly
- Approve PRs only when confident in changes
- Keep review comments constructive and actionable

### Pipeline Best Practices
- Start simple, add complexity as needed
- Use variables for configuration
- Implement caching for faster builds
- Run tests in parallel when possible
- Keep build times under 10 minutes if feasible
- Use templates for reusable pipeline logic
- Monitor pipeline health and success rates
- Archive and clean up old artifacts

### Team Collaboration
- Define clear code review standards
- Establish naming conventions for branches/items
- Create templates for work items and PRs
- Document deployment procedures
- Use notifications effectively (avoid alert fatigue)
- Have regular backlog refinement sessions
- Celebrate completed features and wins

## Common Commands & Workflows

### Azure CLI (az devops)
```bash
# View work items
az boards work-item show --id 1234

# Create work item
az boards work-item create --title "New Feature" --type Feature

# Update work item state
az boards work-item update --id 1234 --state "Active"

# Clone repository
az repos show --repo-id [repo-id]
```

### Common Azure DevOps Tasks in Pipelines
```yaml
# Run tests with coverage
- task: DotNetCoreCLI@2
  inputs:
    command: 'test'
    arguments: '--configuration Release /p:CollectCoverage=true'

# Deploy to Azure Web App
- task: AzureWebApp@1
  inputs:
    azureSubscription: 'subscription'
    appName: 'app-name'
    package: '$(Pipeline.Workspace)/**/*.zip'

# Create release annotation
- task: CreateWorkItem@1
  inputs:
    workItemType: 'Issue'
    title: 'Production Release: v1.0.0'

# Send notification
- task: SendEmail@1
  inputs:
    to: 'team@company.com'
    subject: 'Deployment Complete'
```

## Troubleshooting

**Build Fails Without Clear Error:**
- Check agent logs in pipeline run details
- Verify agent pool has required software installed
- Test build locally before pushing to Azure DevOps
- Check environment variables and secrets configuration

**Pull Request Won't Complete:**
- Verify all required reviewers have approved
- Check that build validation passes
- Ensure no active comments blocking completion
- Confirm you have permission to complete PR

**Pipeline Doesn't Trigger:**
- Check trigger configuration in YAML or UI
- Verify branch matches trigger conditions
- Check if pipeline is enabled/paused
- Review commit filters and path filters

**Tests Pass Locally but Fail in Pipeline:**
- Agent may have different environment/dependencies
- Check test output logs for actual error
- Verify test data and fixtures are available
- Consider environment-specific configuration

## Integration Tips

- Link Azure DevOps work items to GitHub when using GitHub repos
- Integrate with Slack for notifications
- Use Azure Artifacts for package management
- Configure security scanning in pipelines
- Set up continuous deployment with environment approvals
- Monitor pipeline metrics and trends over time
