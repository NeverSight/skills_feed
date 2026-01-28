---
name: azure-devops
description: Comprehensive skill for working with Azure DevOps REST API across all services including Boards (work items, queries, backlogs), Repos (Git, pull requests, commits), Pipelines (builds, releases, deployments), Test Plans, Artifacts, organizations, projects, security, extensions, and more. Use when implementing Azure DevOps integrations, automating DevOps workflows, or building applications that interact with Azure DevOps services.
version: 1.0
---

# Azure DevOps API Skill

This skill provides comprehensive guidance for working with the Azure DevOps REST API, enabling programmatic access to all Azure DevOps Services and Azure DevOps Server resources.

## Overview

Azure DevOps REST API is a RESTful web API enabling you to access and manage work items, repositories, pipelines, test plans, artifacts, and more across all Azure DevOps services.

**Base URL:** `https://dev.azure.com/{organization}/{project}/_apis/{area}/{resource}?api-version={version}`
- **Organization:** Your Azure DevOps organization name
- **Project:** Project name (optional for org-level resources)
- **API Version:** Required on all requests (e.g., `7.1`, `7.0`, `6.0`)
- **Authentication:** Personal Access Tokens (PAT), OAuth 2.0, or Azure AD

## Quick Start

### Authentication Requirements

Azure DevOps supports multiple authentication methods:

1. **Personal Access Token (PAT)** - Most common for scripts and integrations
2. **OAuth 2.0** - For web applications
3. **Azure Active Directory** - For enterprise applications
4. **SSH Keys** - For Git operations only

### Basic PAT Authentication
```http
GET https://dev.azure.com/{organization}/_apis/projects?api-version=7.1
Authorization: Basic {base64-encoded-PAT}
```

To encode PAT: `base64(":{PAT}")` - Note the colon before the PAT.

### Common Request Pattern
```http
GET https://dev.azure.com/{organization}/{project}/_apis/{resource}?api-version=7.1
Authorization: Basic {encoded-PAT}
Content-Type: application/json
```

## Core Services

Azure DevOps is organized into major service areas. Each area has its own set of REST APIs:

### Azure Boards - Work Item Tracking

**Work Items**
- **Create work item:** `POST /{organization}/{project}/_apis/wit/workitems/${type}?api-version=7.1`
- **Get work item:** `GET /{organization}/{project}/_apis/wit/workitems/{id}?api-version=7.1`
- **Update work item:** `PATCH /{organization}/{project}/_apis/wit/workitems/{id}?api-version=7.1`
- **Delete work item:** `DELETE /{organization}/{project}/_apis/wit/workitems/{id}?api-version=7.1`

Request body uses JSON Patch format:
```json
[
  {
    "op": "add",
    "path": "/fields/System.Title",
    "value": "New bug report"
  },
  {
    "op": "add",
    "path": "/fields/System.AssignedTo",
    "value": "user@example.com"
  }
]
```

**Queries**
- **Run stored query:** `GET /{organization}/{project}/_apis/wit/wiql/{id}?api-version=7.1`
- **Run WIQL query:** `POST /{organization}/{project}/_apis/wit/wiql?api-version=7.1`
  ```json
  {
    "query": "SELECT [System.Id], [System.Title] FROM WorkItems WHERE [System.WorkItemType] = 'Bug' AND [System.State] = 'Active'"
  }
  ```

**Boards & Backlogs**
- **Get boards:** `GET /{organization}/{project}/{team}/_apis/work/boards?api-version=7.1`
- **Get backlog items:** `GET /{organization}/{project}/{team}/_apis/work/backlogs/{backlogId}/workItems?api-version=7.1`
- **Get iterations:** `GET /{organization}/{project}/{team}/_apis/work/teamsettings/iterations?api-version=7.1`
- **Get capacity:** `GET /{organization}/{project}/{team}/_apis/work/teamsettings/iterations/{iterationId}/capacities?api-version=7.1`

**Work Item Types & Fields**
- **List work item types:** `GET /{organization}/{project}/_apis/wit/workitemtypes?api-version=7.1`
- **List fields:** `GET /{organization}/{project}/_apis/wit/fields?api-version=7.1`
- **Get field:** `GET /{organization}/{project}/_apis/wit/fields/{fieldNameOrRefName}?api-version=7.1`

**Area & Iteration Paths**
- **Get areas:** `GET /{organization}/{project}/_apis/wit/classificationnodes/areas?api-version=7.1`
- **Get iterations:** `GET /{organization}/{project}/_apis/wit/classificationnodes/iterations?api-version=7.1`
- **Create area:** `POST /{organization}/{project}/_apis/wit/classificationnodes/areas?api-version=7.1`

### Azure Repos - Source Control

**Git Repositories**
- **List repositories:** `GET /{organization}/{project}/_apis/git/repositories?api-version=7.1`
- **Get repository:** `GET /{organization}/{project}/_apis/git/repositories/{repositoryId}?api-version=7.1`
- **Create repository:** `POST /{organization}/{project}/_apis/git/repositories?api-version=7.1`
- **Delete repository:** `DELETE /{organization}/{project}/_apis/git/repositories/{repositoryId}?api-version=7.1`

**Commits**
- **Get commits:** `GET /{organization}/{project}/_apis/git/repositories/{repositoryId}/commits?api-version=7.1`
- **Get commit:** `GET /{organization}/{project}/_apis/git/repositories/{repositoryId}/commits/{commitId}?api-version=7.1`
- **Get commit changes:** `GET /{organization}/{project}/_apis/git/repositories/{repositoryId}/commits/{commitId}/changes?api-version=7.1`

**Branches**
- **Get branches:** `GET /{organization}/{project}/_apis/git/repositories/{repositoryId}/refs?filter=heads/&api-version=7.1`
- **Create branch:** `POST /{organization}/{project}/_apis/git/repositories/{repositoryId}/refs?api-version=7.1`
- **Delete branch:** `POST /{organization}/{project}/_apis/git/repositories/{repositoryId}/refs?api-version=7.1`
  ```json
  [
    {
      "name": "refs/heads/feature-branch",
      "oldObjectId": "0000000000000000000000000000000000000000",
      "newObjectId": "{commitId}"
    }
  ]
  ```

**Pull Requests**
- **Get pull requests:** `GET /{organization}/{project}/_apis/git/repositories/{repositoryId}/pullrequests?api-version=7.1`
- **Get pull request:** `GET /{organization}/{project}/_apis/git/repositories/{repositoryId}/pullrequests/{pullRequestId}?api-version=7.1`
- **Create pull request:** `POST /{organization}/{project}/_apis/git/repositories/{repositoryId}/pullrequests?api-version=7.1`
  ```json
  {
    "sourceRefName": "refs/heads/feature",
    "targetRefName": "refs/heads/main",
    "title": "PR Title",
    "description": "PR Description"
  }
  ```
- **Update pull request:** `PATCH /{organization}/{project}/_apis/git/repositories/{repositoryId}/pullrequests/{pullRequestId}?api-version=7.1`
- **Get PR reviewers:** `GET /{organization}/{project}/_apis/git/repositories/{repositoryId}/pullrequests/{pullRequestId}/reviewers?api-version=7.1`
- **Add PR reviewer:** `PUT /{organization}/{project}/_apis/git/repositories/{repositoryId}/pullrequests/{pullRequestId}/reviewers/{reviewerId}?api-version=7.1`
- **Get PR work items:** `GET /{organization}/{project}/_apis/git/repositories/{repositoryId}/pullrequests/{pullRequestId}/workitems?api-version=7.1`
- **Get PR threads:** `GET /{organization}/{project}/_apis/git/repositories/{repositoryId}/pullrequests/{pullRequestId}/threads?api-version=7.1`
- **Add PR comment:** `POST /{organization}/{project}/_apis/git/repositories/{repositoryId}/pullrequests/{pullRequestId}/threads?api-version=7.1`

**Pushes**
- **Get pushes:** `GET /{organization}/{project}/_apis/git/repositories/{repositoryId}/pushes?api-version=7.1`
- **Get push:** `GET /{organization}/{project}/_apis/git/repositories/{repositoryId}/pushes/{pushId}?api-version=7.1`

**Items (Files & Folders)**
- **Get item:** `GET /{organization}/{project}/_apis/git/repositories/{repositoryId}/items?path={path}&api-version=7.1`
- **Get item content:** `GET /{organization}/{project}/_apis/git/repositories/{repositoryId}/items?path={path}&download=true&api-version=7.1`
- **Get items batch:** `POST /{organization}/{project}/_apis/git/repositories/{repositoryId}/itemsbatch?api-version=7.1`

**Policies**
- **Get policy configurations:** `GET /{organization}/{project}/_apis/policy/configurations?api-version=7.1`
- **Create policy:** `POST /{organization}/{project}/_apis/policy/configurations?api-version=7.1`

### Azure Pipelines - CI/CD

**Build Definitions (Pipelines)**
- **List definitions:** `GET /{organization}/{project}/_apis/build/definitions?api-version=7.1`
- **Get definition:** `GET /{organization}/{project}/_apis/build/definitions/{definitionId}?api-version=7.1`
- **Create definition:** `POST /{organization}/{project}/_apis/build/definitions?api-version=7.1`
- **Update definition:** `PUT /{organization}/{project}/_apis/build/definitions/{definitionId}?api-version=7.1`
- **Delete definition:** `DELETE /{organization}/{project}/_apis/build/definitions/{definitionId}?api-version=7.1`

**Builds**
- **Queue build:** `POST /{organization}/{project}/_apis/build/builds?api-version=7.1`
  ```json
  {
    "definition": {
      "id": 123
    },
    "sourceBranch": "refs/heads/main"
  }
  ```
- **Get builds:** `GET /{organization}/{project}/_apis/build/builds?api-version=7.1`
- **Get build:** `GET /{organization}/{project}/_apis/build/builds/{buildId}?api-version=7.1`
- **Update build:** `PATCH /{organization}/{project}/_apis/build/builds/{buildId}?api-version=7.1`
- **Delete build:** `DELETE /{organization}/{project}/_apis/build/builds/{buildId}?api-version=7.1`
- **Get build logs:** `GET /{organization}/{project}/_apis/build/builds/{buildId}/logs?api-version=7.1`
- **Get build timeline:** `GET /{organization}/{project}/_apis/build/builds/{buildId}/timeline?api-version=7.1`
- **Get build artifacts:** `GET /{organization}/{project}/_apis/build/builds/{buildId}/artifacts?api-version=7.1`

**Release Definitions**
- **List definitions:** `GET https://vsrm.dev.azure.com/{organization}/{project}/_apis/release/definitions?api-version=7.1`
- **Get definition:** `GET https://vsrm.dev.azure.com/{organization}/{project}/_apis/release/definitions/{definitionId}?api-version=7.1`
- **Create definition:** `POST https://vsrm.dev.azure.com/{organization}/{project}/_apis/release/definitions?api-version=7.1`

**Releases**
- **Create release:** `POST https://vsrm.dev.azure.com/{organization}/{project}/_apis/release/releases?api-version=7.1`
- **Get releases:** `GET https://vsrm.dev.azure.com/{organization}/{project}/_apis/release/releases?api-version=7.1`
- **Get release:** `GET https://vsrm.dev.azure.com/{organization}/{project}/_apis/release/releases/{releaseId}?api-version=7.1`
- **Update release:** `PATCH https://vsrm.dev.azure.com/{organization}/{project}/_apis/release/releases/{releaseId}?api-version=7.1`
- **Get release environment:** `GET https://vsrm.dev.azure.com/{organization}/{project}/_apis/release/releases/{releaseId}/environments/{environmentId}?api-version=7.1`
- **Update release environment:** `PATCH https://vsrm.dev.azure.com/{organization}/{project}/_apis/release/releases/{releaseId}/environments/{environmentId}?api-version=7.1`

**Approvals**
- **Get approvals:** `GET https://vsrm.dev.azure.com/{organization}/{project}/_apis/release/approvals?api-version=7.1`
- **Update approval:** `PATCH https://vsrm.dev.azure.com/{organization}/{project}/_apis/release/approvals/{approvalId}?api-version=7.1`

**Agent Pools**
- **List pools:** `GET /{organization}/_apis/distributedtask/pools?api-version=7.1`
- **Get pool:** `GET /{organization}/_apis/distributedtask/pools/{poolId}?api-version=7.1`
- **Add pool:** `POST /{organization}/_apis/distributedtask/pools?api-version=7.1`

**Agents**
- **List agents:** `GET /{organization}/_apis/distributedtask/pools/{poolId}/agents?api-version=7.1`
- **Get agent:** `GET /{organization}/_apis/distributedtask/pools/{poolId}/agents/{agentId}?api-version=7.1`
- **Update agent:** `PATCH /{organization}/_apis/distributedtask/pools/{poolId}/agents/{agentId}?api-version=7.1`

**Variable Groups**
- **List variable groups:** `GET /{organization}/{project}/_apis/distributedtask/variablegroups?api-version=7.1`
- **Get variable group:** `GET /{organization}/{project}/_apis/distributedtask/variablegroups/{groupId}?api-version=7.1`
- **Create variable group:** `POST /{organization}/{project}/_apis/distributedtask/variablegroups?api-version=7.1`
- **Update variable group:** `PUT /{organization}/{project}/_apis/distributedtask/variablegroups/{groupId}?api-version=7.1`

**Task Groups**
- **List task groups:** `GET /{organization}/{project}/_apis/distributedtask/taskgroups?api-version=7.1`
- **Get task group:** `GET /{organization}/{project}/_apis/distributedtask/taskgroups/{taskGroupId}?api-version=7.1`

**Service Endpoints (Connections)**
- **List endpoints:** `GET /{organization}/{project}/_apis/serviceendpoint/endpoints?api-version=7.1`
- **Get endpoint:** `GET /{organization}/{project}/_apis/serviceendpoint/endpoints/{endpointId}?api-version=7.1`
- **Create endpoint:** `POST /{organization}/{project}/_apis/serviceendpoint/endpoints?api-version=7.1`

### Azure Test Plans

**Test Plans**
- **List test plans:** `GET /{organization}/{project}/_apis/testplan/plans?api-version=7.1`
- **Get test plan:** `GET /{organization}/{project}/_apis/testplan/plans/{planId}?api-version=7.1`
- **Create test plan:** `POST /{organization}/{project}/_apis/testplan/plans?api-version=7.1`
- **Update test plan:** `PATCH /{organization}/{project}/_apis/testplan/plans/{planId}?api-version=7.1`

**Test Suites**
- **List test suites:** `GET /{organization}/{project}/_apis/testplan/plans/{planId}/suites?api-version=7.1`
- **Get test suite:** `GET /{organization}/{project}/_apis/testplan/plans/{planId}/suites/{suiteId}?api-version=7.1`
- **Create test suite:** `POST /{organization}/{project}/_apis/testplan/plans/{planId}/suites?api-version=7.1`

**Test Cases**
- **List test cases:** `GET /{organization}/{project}/_apis/testplan/plans/{planId}/suites/{suiteId}/testcases?api-version=7.1`
- **Get test case:** `GET /{organization}/{project}/_apis/testplan/plans/{planId}/suites/{suiteId}/testcases/{testCaseId}?api-version=7.1`
- **Add test cases:** `POST /{organization}/{project}/_apis/testplan/plans/{planId}/suites/{suiteId}/testcases?api-version=7.1`

**Test Runs**
- **Create test run:** `POST /{organization}/{project}/_apis/test/runs?api-version=7.1`
- **Get test runs:** `GET /{organization}/{project}/_apis/test/runs?api-version=7.1`
- **Get test run:** `GET /{organization}/{project}/_apis/test/runs/{runId}?api-version=7.1`
- **Update test run:** `PATCH /{organization}/{project}/_apis/test/runs/{runId}?api-version=7.1`

**Test Results**
- **Get test results:** `GET /{organization}/{project}/_apis/test/runs/{runId}/results?api-version=7.1`
- **Get test result:** `GET /{organization}/{project}/_apis/test/runs/{runId}/results/{resultId}?api-version=7.1`
- **Update test results:** `PATCH /{organization}/{project}/_apis/test/runs/{runId}/results?api-version=7.1`
- **Add test results:** `POST /{organization}/{project}/_apis/test/runs/{runId}/results?api-version=7.1`

**Test Configurations**
- **List configurations:** `GET /{organization}/{project}/_apis/testplan/configurations?api-version=7.1`
- **Get configuration:** `GET /{organization}/{project}/_apis/testplan/configurations/{configurationId}?api-version=7.1`

### Azure Artifacts

**Feeds**
- **List feeds:** `GET https://feeds.dev.azure.com/{organization}/_apis/packaging/feeds?api-version=7.1`
- **Get feed:** `GET https://feeds.dev.azure.com/{organization}/_apis/packaging/feeds/{feedId}?api-version=7.1`
- **Create feed:** `POST https://feeds.dev.azure.com/{organization}/_apis/packaging/feeds?api-version=7.1`
- **Update feed:** `PATCH https://feeds.dev.azure.com/{organization}/_apis/packaging/feeds/{feedId}?api-version=7.1`

**Packages**
- **List packages:** `GET https://feeds.dev.azure.com/{organization}/_apis/packaging/feeds/{feedId}/packages?api-version=7.1`
- **Get package:** `GET https://feeds.dev.azure.com/{organization}/_apis/packaging/feeds/{feedId}/packages/{packageId}?api-version=7.1`
- **Delete package:** `DELETE https://feeds.dev.azure.com/{organization}/_apis/packaging/feeds/{feedId}/packages/{packageId}?api-version=7.1`

**Package Versions**
- **List package versions:** `GET https://feeds.dev.azure.com/{organization}/_apis/packaging/feeds/{feedId}/packages/{packageId}/versions?api-version=7.1`
- **Get package version:** `GET https://feeds.dev.azure.com/{organization}/_apis/packaging/feeds/{feedId}/packages/{packageId}/versions/{versionId}?api-version=7.1`
- **Delete package version:** `DELETE https://feeds.dev.azure.com/{organization}/_apis/packaging/feeds/{feedId}/packages/{packageId}/versions/{versionId}?api-version=7.1`

**Feed Permissions**
- **Get feed permissions:** `GET https://feeds.dev.azure.com/{organization}/_apis/packaging/feeds/{feedId}/permissions?api-version=7.1`
- **Set feed permissions:** `PATCH https://feeds.dev.azure.com/{organization}/_apis/packaging/feeds/{feedId}/permissions?api-version=7.1`

## Organization & Project Management

**Organizations**
- **List organizations:** Available via Azure DevOps Profile API
- **Get organization details:** `GET https://dev.azure.com/{organization}/_apis/projectcollections?api-version=7.1`

**Projects**
- **List projects:** `GET /{organization}/_apis/projects?api-version=7.1`
- **Get project:** `GET /{organization}/_apis/projects/{projectId}?api-version=7.1`
- **Create project:** `POST /{organization}/_apis/projects?api-version=7.1`
  ```json
  {
    "name": "MyProject",
    "description": "Project description",
    "capabilities": {
      "versioncontrol": {
        "sourceControlType": "Git"
      },
      "processTemplate": {
        "templateTypeId": "6b724908-ef14-45cf-84f8-768b5384da45"
      }
    }
  }
  ```
- **Update project:** `PATCH /{organization}/_apis/projects/{projectId}?api-version=7.1`
- **Delete project:** `DELETE /{organization}/_apis/projects/{projectId}?api-version=7.1`

**Teams**
- **List teams:** `GET /{organization}/_apis/teams?api-version=7.1`
- **Get team:** `GET /{organization}/_apis/projects/{projectId}/teams/{teamId}?api-version=7.1`
- **Create team:** `POST /{organization}/_apis/projects/{projectId}/teams?api-version=7.1`
- **Update team:** `PATCH /{organization}/_apis/projects/{projectId}/teams/{teamId}?api-version=7.1`
- **Delete team:** `DELETE /{organization}/_apis/projects/{projectId}/teams/{teamId}?api-version=7.1`

**Team Members**
- **Get team members:** `GET /{organization}/_apis/projects/{projectId}/teams/{teamId}/members?api-version=7.1`
- **Add team member:** `PUT /{organization}/_apis/projects/{projectId}/teams/{teamId}/members/{userId}?api-version=7.1`
- **Remove team member:** `DELETE /{organization}/_apis/projects/{projectId}/teams/{teamId}/members/{userId}?api-version=7.1`

**Processes**
- **List processes:** `GET /{organization}/_apis/process/processes?api-version=7.1`
- **Get process:** `GET /{organization}/_apis/process/processes/{processId}?api-version=7.1`
- **Create process:** `POST /{organization}/_apis/process/processes?api-version=7.1`

## Security & Identity

**Identities (Users & Groups)**
- **Read identities:** `GET https://vssps.dev.azure.com/{organization}/_apis/identities?api-version=7.1`
- **Read identity:** `GET https://vssps.dev.azure.com/{organization}/_apis/identities/{identityId}?api-version=7.1`

**Graph (Azure DevOps specific)**
- **List users:** `GET https://vssps.dev.azure.com/{organization}/_apis/graph/users?api-version=7.1-preview.1`
- **Get user:** `GET https://vssps.dev.azure.com/{organization}/_apis/graph/users/{userDescriptor}?api-version=7.1-preview.1`
- **Create user:** `POST https://vssps.dev.azure.com/{organization}/_apis/graph/users?api-version=7.1-preview.1`
- **Delete user:** `DELETE https://vssps.dev.azure.com/{organization}/_apis/graph/users/{userDescriptor}?api-version=7.1-preview.1`

**Groups**
- **List groups:** `GET https://vssps.dev.azure.com/{organization}/_apis/graph/groups?api-version=7.1-preview.1`
- **Get group:** `GET https://vssps.dev.azure.com/{organization}/_apis/graph/groups/{groupDescriptor}?api-version=7.1-preview.1`
- **Create group:** `POST https://vssps.dev.azure.com/{organization}/_apis/graph/groups?api-version=7.1-preview.1`
- **Delete group:** `DELETE https://vssps.dev.azure.com/{organization}/_apis/graph/groups/{groupDescriptor}?api-version=7.1-preview.1`

**Group Memberships**
- **List memberships:** `GET https://vssps.dev.azure.com/{organization}/_apis/graph/memberships/{subjectDescriptor}?api-version=7.1-preview.1`
- **Add membership:** `PUT https://vssps.dev.azure.com/{organization}/_apis/graph/memberships/{subjectDescriptor}/{containerDescriptor}?api-version=7.1-preview.1`
- **Remove membership:** `DELETE https://vssps.dev.azure.com/{organization}/_apis/graph/memberships/{subjectDescriptor}/{containerDescriptor}?api-version=7.1-preview.1`

**Access Control Lists (ACLs)**
- **Query ACLs:** `GET /{organization}/_apis/accesscontrollists/{securityNamespaceId}?api-version=7.1`
- **Set ACLs:** `POST /{organization}/_apis/accesscontrollists/{securityNamespaceId}?api-version=7.1`
- **Remove ACLs:** `DELETE /{organization}/_apis/accesscontrollists/{securityNamespaceId}?api-version=7.1`

**Security Namespaces**
- **List security namespaces:** `GET /{organization}/_apis/securitynamespaces?api-version=7.1`
- **Get security namespace:** `GET /{organization}/_apis/securitynamespaces/{securityNamespaceId}?api-version=7.1`

**Permissions**
- **Query permissions:** `GET /{organization}/_apis/permissions/{securityNamespaceId}/{permissions}?api-version=7.1`
- **Check permission:** `GET /{organization}/_apis/security/permissions/{securityNamespaceId}?api-version=7.1`

## Extensions & Integrations

**Extensions**
- **List installed extensions:** `GET /{organization}/_apis/extensionmanagement/installedextensions?api-version=7.1`
- **Get installed extension:** `GET /{organization}/_apis/extensionmanagement/installedextensions/{publisherName}/{extensionName}?api-version=7.1`
- **Install extension:** `POST /{organization}/_apis/extensionmanagement/installedextensions?api-version=7.1`
- **Uninstall extension:** `DELETE /{organization}/_apis/extensionmanagement/installedextensions/{publisherName}/{extensionName}?api-version=7.1`

**Service Hooks**
- **List subscriptions:** `GET /{organization}/_apis/hooks/subscriptions?api-version=7.1`
- **Get subscription:** `GET /{organization}/_apis/hooks/subscriptions/{subscriptionId}?api-version=7.1`
- **Create subscription:** `POST /{organization}/_apis/hooks/subscriptions?api-version=7.1`
  ```json
  {
    "publisherId": "tfs",
    "eventType": "git.push",
    "resourceVersion": "1.0",
    "consumerId": "webHooks",
    "consumerActionId": "httpRequest",
    "publisherInputs": {
      "projectId": "{projectId}"
    },
    "consumerInputs": {
      "url": "https://example.com/webhook"
    }
  }
  ```
- **Delete subscription:** `DELETE /{organization}/_apis/hooks/subscriptions/{subscriptionId}?api-version=7.1`

**Notifications**
- **List subscriptions:** `GET /{organization}/_apis/notification/subscriptions?api-version=7.1`
- **Create subscription:** `POST /{organization}/_apis/notification/subscriptions?api-version=7.1`

## Additional Services

**Wiki**
- **List wikis:** `GET /{organization}/{project}/_apis/wiki/wikis?api-version=7.1`
- **Get wiki:** `GET /{organization}/{project}/_apis/wiki/wikis/{wikiId}?api-version=7.1`
- **Create wiki:** `POST /{organization}/{project}/_apis/wiki/wikis?api-version=7.1`
- **Get wiki page:** `GET /{organization}/{project}/_apis/wiki/wikis/{wikiId}/pages?path={path}&api-version=7.1`
- **Create/update wiki page:** `PUT /{organization}/{project}/_apis/wiki/wikis/{wikiId}/pages?path={path}&api-version=7.1`

**Search**
- **Search work items:** `POST /{organization}/{project}/_apis/search/workitemsearchresults?api-version=7.1`
- **Search code:** `POST /{organization}/{project}/_apis/search/codesearchresults?api-version=7.1`

**Dashboards**
- **List dashboards:** `GET /{organization}/{project}/{team}/_apis/dashboard/dashboards?api-version=7.1`
- **Get dashboard:** `GET /{organization}/{project}/{team}/_apis/dashboard/dashboards/{dashboardId}?api-version=7.1`
- **Create dashboard:** `POST /{organization}/{project}/{team}/_apis/dashboard/dashboards?api-version=7.1`

**Widgets**
- **List widgets:** `GET /{organization}/{project}/{team}/_apis/dashboard/dashboards/{dashboardId}/widgets?api-version=7.1`
- **Create widget:** `POST /{organization}/{project}/{team}/_apis/dashboard/dashboards/{dashboardId}/widgets?api-version=7.1`

**Audit**
- **Query audit log:** `GET /{organization}/_apis/audit/auditlog?api-version=7.1-preview.1`
- **Download audit log:** `GET /{organization}/_apis/audit/downloadlog?api-version=7.1-preview.1`

## Common Operations

### Pagination

Azure DevOps API uses continuation tokens for pagination:

**Response with continuation token:**
```json
{
  "count": 100,
  "value": [...],
  "continuationToken": "MTIz"
}
```

**Next request:**
```http
GET /{endpoint}?continuationToken=MTIz&api-version=7.1
```

Some endpoints use `$top` and `$skip`:
```http
GET /{endpoint}?$top=100&$skip=100&api-version=7.1
```

### Filtering & Querying

**OData-style filters (select endpoints):**
```http
GET /{endpoint}?$filter=state eq 'Active'&api-version=7.1
```

**Work item queries use WIQL (Work Item Query Language):**
```sql
SELECT [System.Id], [System.Title], [System.State]
FROM WorkItems
WHERE [System.WorkItemType] = 'Bug'
  AND [System.State] = 'Active'
  AND [System.AssignedTo] = @Me
ORDER BY [System.ChangedDate] DESC
```

### Batch Operations

Some Azure DevOps APIs support batch operations:

**Work Items batch get:**
```http
GET /{organization}/_apis/wit/workitemsbatch?ids=1,2,3,4,5&api-version=7.1
```

**Git items batch:**
```http
POST /{organization}/{project}/_apis/git/repositories/{repositoryId}/itemsbatch?api-version=7.1
{
  "itemDescriptors": [
    {"path": "/file1.txt", "version": "main"},
    {"path": "/file2.txt", "version": "main"}
  ]
}
```

### JSON Patch for Updates

Work items and some other resources use JSON Patch (RFC 6902):

**Operations:**
- `add` - Add a field or relationship
- `remove` - Remove a field
- `replace` - Replace field value
- `test` - Test a value (for concurrency)
- `copy` - Copy a value
- `move` - Move a value

**Example:**
```json
[
  {
    "op": "add",
    "path": "/fields/System.Title",
    "value": "New title"
  },
  {
    "op": "replace",
    "path": "/fields/System.State",
    "value": "Active"
  },
  {
    "op": "add",
    "path": "/relations/-",
    "value": {
      "rel": "System.LinkTypes.Hierarchy-Reverse",
      "url": "https://dev.azure.com/{org}/_apis/wit/workItems/123"
    }
  }
]
```

## Error Handling

Azure DevOps API returns standard HTTP status codes:
- `200 OK` - Success
- `201 Created` - Resource created
- `202 Accepted` - Request accepted (async operation)
- `204 No Content` - Success, no content
- `400 Bad Request` - Invalid request
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `409 Conflict` - Conflict (e.g., version mismatch)
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Service unavailable

**Error response format:**
```json
{
  "id": "request-id",
  "innerException": null,
  "message": "TF401019: The Git repository with name or identifier MyRepo does not exist or you do not have permissions for the operation you are attempting.",
  "typeName": "Microsoft.TeamFoundation.Git.Server.GitRepositoryNotFoundException",
  "typeKey": "GitRepositoryNotFoundException",
  "errorCode": 0,
  "eventId": 3000
}
```

### Rate Limiting

Azure DevOps enforces rate limits:
- **Global limit:** Varies by service (typically 200-300 requests per minute)
- **TSTUs (Team Services Time Units):** Used to measure resource consumption
- **Retry-After header:** Indicates when to retry after 429 error

**Best practices:**
- Implement exponential backoff
- Respect `Retry-After` header
- Cache responses when appropriate
- Use batch operations when available

## Permissions & Scopes

### PAT Scopes

When creating Personal Access Tokens, select appropriate scopes:

- **Agent Pools:** Read & manage
- **Analytics:** Read
- **Audit:** Read audit log
- **Build:** Read & execute
- **Code:** Full, Read, or Status
- **Extensions:** Read & manage
- **Graph:** Read
- **Identity:** Read
- **Marketplace:** Acquire, manage, publish
- **Member Entitlement Management:** Read & write
- **Packaging:** Read, write, & manage
- **Project and Team:** Read, write, & manage
- **Release:** Read, write, execute, & manage
- **Secure Files:** Read, create, & manage
- **Service Connections:** Read, query, & manage
- **Symbols:** Read
- **Task Groups:** Read, create, & manage
- **Test Management:** Read & write
- **Tokens:** Read & manage
- **User Profile:** Read & write
- **Variable Groups:** Read, create, & manage
- **Work Items:** Full, Read, & write

**Important:** Always use the least privileged scope required.

### OAuth 2.0 Scopes

For OAuth applications, use scopes in the format:
- `vso.work` - Work items (read)
- `vso.work_write` - Work items (write)
- `vso.code` - Code (read)
- `vso.code_write` - Code (write)
- `vso.build` - Build (read)
- `vso.build_execute` - Build (execute)

Full list: https://docs.microsoft.com/azure/devops/integrate/get-started/authentication/oauth

## API Versioning

Azure DevOps APIs use explicit versioning:

**Versions:**
- `7.1` - Latest stable (recommended)
- `7.0` - Stable
- `6.0` - Stable
- `5.1` - Older stable
- Versions with `-preview` suffix (e.g., `7.1-preview.1`) - Preview features

**Version format:**
- `api-version=7.1` - Latest patch of 7.1
- `api-version=7.1-preview.1` - Preview version 1 of 7.1

**Important:**
- Always specify `api-version` (required on all requests)
- Preview APIs may change or be removed
- Use stable versions for production
- Monitor deprecation notices

## Best Practices

### Performance
1. Use batch operations when fetching multiple items
2. Implement pagination for large result sets
3. Use specific fields with `$select` where supported
4. Cache responses when appropriate
5. Use delta queries for incremental sync
6. Leverage continuation tokens properly

### Security
1. Store PATs securely (use Azure Key Vault or similar)
2. Use appropriate scopes (least privilege)
3. Rotate PATs regularly (set expiration)
4. Use HTTPS only
5. Validate input to prevent injection
6. Implement proper error handling
7. Log security events
8. Never commit PATs to source control

### Development
1. Use latest stable API version
2. Handle rate limits with retry logic
3. Implement exponential backoff
4. Check for preview API stability before using
5. Monitor service health
6. Use JSON Patch for updates
7. Validate responses
8. Handle pagination correctly
9. Test with various edge cases
10. Use descriptive error messages

### Integration Patterns
1. **Webhooks (Service Hooks):** For event-driven integrations
2. **Polling:** For batch processing (avoid excessive polling)
3. **Scheduled Jobs:** For periodic sync operations
4. **Real-time sync:** Using service hooks + API calls

## Common Use Cases

### Create Work Item
```http
POST https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$Bug?api-version=7.1
Content-Type: application/json-patch+json

[
  {
    "op": "add",
    "path": "/fields/System.Title",
    "value": "Critical bug in login flow"
  },
  {
    "op": "add",
    "path": "/fields/System.Description",
    "value": "Users cannot log in with SSO"
  },
  {
    "op": "add",
    "path": "/fields/Microsoft.VSTS.Common.Priority",
    "value": 1
  }
]
```

### Create Pull Request
```http
POST https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repositoryId}/pullrequests?api-version=7.1
Content-Type: application/json

{
  "sourceRefName": "refs/heads/feature/new-feature",
  "targetRefName": "refs/heads/main",
  "title": "Add new feature",
  "description": "This PR adds the new feature",
  "reviewers": [
    {"id": "reviewer-id-1"},
    {"id": "reviewer-id-2"}
  ]
}
```

### Queue Build
```http
POST https://dev.azure.com/{organization}/{project}/_apis/build/builds?api-version=7.1
Content-Type: application/json

{
  "definition": {
    "id": 123
  },
  "sourceBranch": "refs/heads/main",
  "parameters": "{\"param1\":\"value1\"}"
}
```

### Run WIQL Query
```http
POST https://dev.azure.com/{organization}/{project}/_apis/wit/wiql?api-version=7.1
Content-Type: application/json

{
  "query": "SELECT [System.Id], [System.Title], [System.State] FROM WorkItems WHERE [System.WorkItemType] = 'Bug' AND [System.State] = 'Active' AND [System.AssignedTo] = @Me ORDER BY [System.Priority] ASC"
}
```

### Create Service Hook Subscription
```http
POST https://dev.azure.com/{organization}/_apis/hooks/subscriptions?api-version=7.1
Content-Type: application/json

{
  "publisherId": "tfs",
  "eventType": "workitem.updated",
  "resourceVersion": "1.0",
  "consumerId": "webHooks",
  "consumerActionId": "httpRequest",
  "publisherInputs": {
    "projectId": "{projectId}",
    "workItemType": "Bug"
  },
  "consumerInputs": {
    "url": "https://example.com/webhook",
    "httpHeaders": "Content-Type:application/json"
  }
}
```

## Tools & Testing

### REST Client Tools
- **Postman** - Popular API testing tool
- **curl** - Command-line tool
- **PowerShell** - `Invoke-RestMethod`
- **Python** - `requests` library
- **Azure DevOps CLI** - Official CLI tool

### Azure DevOps CLI
Install and use the official CLI:
```bash
# Install
pip install azure-devops

# Login
az devops login --organization https://dev.azure.com/{organization}

# Configure defaults
az devops configure --defaults organization=https://dev.azure.com/{organization} project={project}

# Examples
az repos list
az pipelines build list
az boards work-item create --title "Bug" --type Bug
```

### Testing Authentication
Test PAT authentication:
```bash
# Encode PAT
PAT_ENCODED=$(echo -n ":YOUR_PAT" | base64)

# Test
curl -H "Authorization: Basic $PAT_ENCODED" \
  "https://dev.azure.com/{organization}/_apis/projects?api-version=7.1"
```

### SDKs Available
- **.NET** - `Microsoft.TeamFoundationServer.Client`, `Microsoft.VisualStudio.Services.Client`
- **Node.js** - `azure-devops-node-api`
- **Python** - `azure-devops`
- **Java** - Azure DevOps SDK for Java

## Progressive Loading

This skill provides comprehensive coverage of Azure DevOps API. For specific tasks:

1. **Identify the service area** (Boards, Repos, Pipelines, Test, Artifacts)
2. **Find the relevant section** in this document
3. **Use the API reference** for detailed parameter information
4. **Test with Azure DevOps CLI or REST client** before implementing

## Reference Links

- **Official Docs:** https://docs.microsoft.com/rest/api/azure/devops/
- **API Reference:** https://docs.microsoft.com/rest/api/azure/devops/?view=azure-devops-rest-7.1
- **Authentication:** https://docs.microsoft.com/azure/devops/integrate/get-started/authentication/authentication-guidance
- **Service Hooks:** https://docs.microsoft.com/azure/devops/service-hooks/overview
- **Rate Limits:** https://docs.microsoft.com/azure/devops/integrate/concepts/rate-limits
- **API Versioning:** https://docs.microsoft.com/azure/devops/integrate/concepts/rest-api-versioning
- **Azure DevOps CLI:** https://docs.microsoft.com/cli/azure/devops
- **Node.js SDK:** https://github.com/microsoft/azure-devops-node-api
- **Python SDK:** https://github.com/microsoft/azure-devops-python-api
- **Status Page:** https://status.dev.azure.com/

## API URL Patterns

Different Azure DevOps services use different base URLs:

- **Core services:** `https://dev.azure.com/{organization}/`
- **Release Management:** `https://vsrm.dev.azure.com/{organization}/`
- **Package Management:** `https://feeds.dev.azure.com/{organization}/`
- **Identity:** `https://vssps.dev.azure.com/{organization}/`
- **Analytics:** `https://analytics.dev.azure.com/{organization}/`

## Notes

- This skill covers the Azure DevOps REST API version 7.1 (latest stable)
- Some endpoints may require preview API versions
- Always check the official documentation for latest changes
- API versions and endpoints may evolve over time
- Rate limits and throttling policies apply
- Proper authentication and permissions are required for all operations
- Some features are only available in Azure DevOps Services, not Server
