---
name: jira-project-management
description: Administer Jira projects. Use when creating/archiving projects, managing components, versions, roles, permissions, or project configuration.
---

# Jira Project Management Skill

## Purpose
Comprehensive project administration including CRUD operations, components, versions, roles, permissions, and configuration.

## When to Use
- Creating/updating/deleting/archiving projects
- Managing project components (modules, teams)
- Managing versions/releases
- Configuring project roles and permissions
- Setting project properties and metadata
- Validating project keys and names

## Prerequisites
- Authenticated JiraClient (see jira-auth skill)
- Jira admin or project admin permissions
- Project key format: 2-10 uppercase letters

## Implementation Pattern

### Step 1: Define Types

```typescript
interface Project {
  id: string;
  key: string;
  name: string;
  self: string;
  projectTypeKey: 'software' | 'service_desk' | 'business';
  simplified: boolean;
  style: 'classic' | 'next-gen';
  isPrivate: boolean;
  lead: {
    accountId: string;
    displayName: string;
  };
  description?: string;
  url?: string;
  avatarUrls: Record<string, string>;
  projectCategory?: {
    id: string;
    name: string;
  };
}

interface Component {
  id: string;
  name: string;
  description?: string;
  lead?: { accountId: string; displayName: string };
  assigneeType: 'PROJECT_DEFAULT' | 'COMPONENT_LEAD' | 'PROJECT_LEAD' | 'UNASSIGNED';
  project: string;
  projectId: number;
}

interface Version {
  id: string;
  name: string;
  description?: string;
  archived: boolean;
  released: boolean;
  startDate?: string;
  releaseDate?: string;
  projectId: number;
  overdue?: boolean;
}

interface ProjectRole {
  id: number;
  name: string;
  description: string;
  actors: Array<{
    id: number;
    displayName: string;
    type: 'atlassian-user-role-actor' | 'atlassian-group-role-actor';
    actorUser?: { accountId: string };
    actorGroup?: { name: string; displayName: string };
  }>;
}
```

### Step 2: Project CRUD Operations

```typescript
// Create Project
interface CreateProjectInput {
  key: string;                    // 2-10 uppercase letters
  name: string;
  projectTypeKey: 'software' | 'service_desk' | 'business';
  leadAccountId: string;
  description?: string;
  assigneeType?: 'PROJECT_LEAD' | 'UNASSIGNED';
  categoryId?: number;
}

async function createProject(
  client: JiraClient,
  input: CreateProjectInput
): Promise<Project> {
  return client.request<Project>('/project', {
    method: 'POST',
    body: JSON.stringify({
      key: input.key,
      name: input.name,
      projectTypeKey: input.projectTypeKey,
      leadAccountId: input.leadAccountId,
      description: input.description,
      assigneeType: input.assigneeType || 'UNASSIGNED',
      categoryId: input.categoryId,
    }),
  });
}

// Update Project
async function updateProject(
  client: JiraClient,
  projectKeyOrId: string,
  updates: Partial<{
    key: string;
    name: string;
    description: string;
    leadAccountId: string;
    assigneeType: string;
    categoryId: number;
  }>
): Promise<Project> {
  return client.request<Project>(`/project/${projectKeyOrId}`, {
    method: 'PUT',
    body: JSON.stringify(updates),
  });
}

// Delete Project (moves to trash, recoverable for 60 days)
async function deleteProject(
  client: JiraClient,
  projectKeyOrId: string,
  enableUndo: boolean = true
): Promise<void> {
  await client.request(`/project/${projectKeyOrId}?enableUndo=${enableUndo}`, {
    method: 'DELETE',
  });
}

// Archive Project
async function archiveProject(
  client: JiraClient,
  projectKeyOrId: string
): Promise<void> {
  await client.request(`/project/${projectKeyOrId}/archive`, {
    method: 'POST',
  });
}

// Restore Project
async function restoreProject(
  client: JiraClient,
  projectKeyOrId: string
): Promise<Project> {
  return client.request<Project>(`/project/${projectKeyOrId}/restore`, {
    method: 'POST',
  });
}
```

### Step 3: List and Search Projects

```typescript
interface ProjectSearchOptions {
  startAt?: number;
  maxResults?: number;
  orderBy?: 'category' | '-category' | 'key' | '-key' | 'name' | '-name' | 'owner' | '-owner';
  query?: string;           // Search in name/key
  typeKey?: string;         // software, service_desk, business
  categoryId?: number;
  expand?: ('description' | 'lead' | 'issueTypes' | 'url' | 'projectKeys' | 'permissions' | 'insight')[];
}

async function searchProjects(
  client: JiraClient,
  options: ProjectSearchOptions = {}
): Promise<{ values: Project[]; total: number; isLast: boolean }> {
  const params = new URLSearchParams();
  if (options.startAt) params.set('startAt', String(options.startAt));
  if (options.maxResults) params.set('maxResults', String(options.maxResults));
  if (options.orderBy) params.set('orderBy', options.orderBy);
  if (options.query) params.set('query', options.query);
  if (options.typeKey) params.set('typeKey', options.typeKey);
  if (options.categoryId) params.set('categoryId', String(options.categoryId));
  if (options.expand) params.set('expand', options.expand.join(','));

  return client.request(`/project/search?${params.toString()}`);
}

// Get recent projects
async function getRecentProjects(
  client: JiraClient,
  maxResults: number = 20
): Promise<Project[]> {
  const params = new URLSearchParams();
  params.set('maxResults', String(maxResults));
  params.set('expand', 'description,lead');
  return client.request(`/project/recent?${params.toString()}`);
}
```

### Step 4: Component Management

```typescript
// List Components
async function getProjectComponents(
  client: JiraClient,
  projectKeyOrId: string
): Promise<Component[]> {
  return client.request(`/project/${projectKeyOrId}/components`);
}

// Create Component
interface CreateComponentInput {
  project: string;        // Project key
  name: string;
  description?: string;
  leadAccountId?: string;
  assigneeType?: 'PROJECT_DEFAULT' | 'COMPONENT_LEAD' | 'PROJECT_LEAD' | 'UNASSIGNED';
}

async function createComponent(
  client: JiraClient,
  input: CreateComponentInput
): Promise<Component> {
  return client.request<Component>('/component', {
    method: 'POST',
    body: JSON.stringify({
      project: input.project,
      name: input.name,
      description: input.description,
      leadAccountId: input.leadAccountId,
      assigneeType: input.assigneeType || 'PROJECT_DEFAULT',
    }),
  });
}

// Update Component
async function updateComponent(
  client: JiraClient,
  componentId: string,
  updates: Partial<{
    name: string;
    description: string;
    leadAccountId: string;
    assigneeType: string;
  }>
): Promise<Component> {
  return client.request<Component>(`/component/${componentId}`, {
    method: 'PUT',
    body: JSON.stringify(updates),
  });
}

// Delete Component
async function deleteComponent(
  client: JiraClient,
  componentId: string,
  moveIssuesTo?: string  // Component ID to move issues to
): Promise<void> {
  const query = moveIssuesTo ? `?moveIssuesTo=${moveIssuesTo}` : '';
  await client.request(`/component/${componentId}${query}`, {
    method: 'DELETE',
  });
}

// Get Component Issue Counts
async function getComponentIssueCounts(
  client: JiraClient,
  componentId: string
): Promise<{ issueCount: number }> {
  return client.request(`/component/${componentId}/relatedIssueCounts`);
}
```

### Step 5: Version/Release Management

```typescript
// List Versions
async function getProjectVersions(
  client: JiraClient,
  projectKeyOrId: string,
  options: {
    startAt?: number;
    maxResults?: number;
    orderBy?: 'description' | '-description' | 'name' | '-name' | 'releaseDate' | '-releaseDate' | 'sequence' | '-sequence' | 'startDate' | '-startDate';
    status?: 'released' | 'unreleased' | 'archived';
    expand?: string;
  } = {}
): Promise<{ values: Version[]; total: number; isLast: boolean }> {
  const params = new URLSearchParams();
  if (options.startAt) params.set('startAt', String(options.startAt));
  if (options.maxResults) params.set('maxResults', String(options.maxResults));
  if (options.orderBy) params.set('orderBy', options.orderBy);
  if (options.status) params.set('status', options.status);
  if (options.expand) params.set('expand', options.expand);

  return client.request(`/project/${projectKeyOrId}/version?${params.toString()}`);
}

// Create Version
interface CreateVersionInput {
  projectId: number;
  name: string;
  description?: string;
  startDate?: string;     // YYYY-MM-DD
  releaseDate?: string;   // YYYY-MM-DD
  released?: boolean;
  archived?: boolean;
}

async function createVersion(
  client: JiraClient,
  input: CreateVersionInput
): Promise<Version> {
  return client.request<Version>('/version', {
    method: 'POST',
    body: JSON.stringify(input),
  });
}

// Update Version
async function updateVersion(
  client: JiraClient,
  versionId: string,
  updates: Partial<{
    name: string;
    description: string;
    startDate: string;
    releaseDate: string;
    released: boolean;
    archived: boolean;
    moveUnfixedIssuesTo: string;  // Version ID when releasing
  }>
): Promise<Version> {
  return client.request<Version>(`/version/${versionId}`, {
    method: 'PUT',
    body: JSON.stringify(updates),
  });
}

// Release Version (mark as released)
async function releaseVersion(
  client: JiraClient,
  versionId: string,
  moveUnfixedIssuesTo?: string
): Promise<Version> {
  return updateVersion(client, versionId, {
    released: true,
    releaseDate: new Date().toISOString().split('T')[0],
    moveUnfixedIssuesTo,
  });
}

// Delete Version
async function deleteVersion(
  client: JiraClient,
  versionId: string,
  options: {
    moveFixedIssuesTo?: string;
    moveAffectedIssuesTo?: string;
  } = {}
): Promise<void> {
  const params = new URLSearchParams();
  if (options.moveFixedIssuesTo) params.set('moveFixedIssuesTo', options.moveFixedIssuesTo);
  if (options.moveAffectedIssuesTo) params.set('moveAffectedIssuesTo', options.moveAffectedIssuesTo);

  const query = params.toString() ? `?${params.toString()}` : '';
  await client.request(`/version/${versionId}${query}`, {
    method: 'DELETE',
  });
}

// Get Version Issue Counts
async function getVersionIssueCounts(
  client: JiraClient,
  versionId: string
): Promise<{
  issuesFixedCount: number;
  issuesAffectedCount: number;
  issueCountWithCustomFieldsShowingVersion: number;
}> {
  return client.request(`/version/${versionId}/relatedIssueCounts`);
}

// Get Unresolved Issue Count
async function getUnresolvedIssueCount(
  client: JiraClient,
  versionId: string
): Promise<{ issuesUnresolvedCount: number; self: string }> {
  return client.request(`/version/${versionId}/unresolvedIssueCount`);
}
```

### Step 6: Project Roles

```typescript
// Get Project Roles
async function getProjectRoles(
  client: JiraClient,
  projectKeyOrId: string
): Promise<Record<string, string>> {
  // Returns map of role name -> role URL
  return client.request(`/project/${projectKeyOrId}/role`);
}

// Get Role Details
async function getProjectRole(
  client: JiraClient,
  projectKeyOrId: string,
  roleId: number
): Promise<ProjectRole> {
  return client.request(`/project/${projectKeyOrId}/role/${roleId}`);
}

// Add User to Role
async function addUserToRole(
  client: JiraClient,
  projectKeyOrId: string,
  roleId: number,
  accountId: string
): Promise<ProjectRole> {
  return client.request(`/project/${projectKeyOrId}/role/${roleId}`, {
    method: 'POST',
    body: JSON.stringify({
      user: [accountId],
    }),
  });
}

// Add Group to Role
async function addGroupToRole(
  client: JiraClient,
  projectKeyOrId: string,
  roleId: number,
  groupName: string
): Promise<ProjectRole> {
  return client.request(`/project/${projectKeyOrId}/role/${roleId}`, {
    method: 'POST',
    body: JSON.stringify({
      group: [groupName],
    }),
  });
}

// Remove Actor from Role
async function removeActorFromRole(
  client: JiraClient,
  projectKeyOrId: string,
  roleId: number,
  actorType: 'user' | 'group',
  actorValue: string  // accountId or groupName
): Promise<void> {
  const param = actorType === 'user' ? 'user' : 'group';
  await client.request(
    `/project/${projectKeyOrId}/role/${roleId}?${param}=${encodeURIComponent(actorValue)}`,
    { method: 'DELETE' }
  );
}
```

### Step 7: Project Properties

```typescript
// List Project Properties
async function getProjectProperties(
  client: JiraClient,
  projectKeyOrId: string
): Promise<{ keys: Array<{ key: string; self: string }> }> {
  return client.request(`/project/${projectKeyOrId}/properties`);
}

// Get Property
async function getProjectProperty(
  client: JiraClient,
  projectKeyOrId: string,
  propertyKey: string
): Promise<{ key: string; value: any }> {
  return client.request(`/project/${projectKeyOrId}/properties/${propertyKey}`);
}

// Set Property
async function setProjectProperty(
  client: JiraClient,
  projectKeyOrId: string,
  propertyKey: string,
  value: any
): Promise<void> {
  await client.request(`/project/${projectKeyOrId}/properties/${propertyKey}`, {
    method: 'PUT',
    body: JSON.stringify(value),
  });
}

// Delete Property
async function deleteProjectProperty(
  client: JiraClient,
  projectKeyOrId: string,
  propertyKey: string
): Promise<void> {
  await client.request(`/project/${projectKeyOrId}/properties/${propertyKey}`, {
    method: 'DELETE',
  });
}
```

### Step 8: Project Validation

```typescript
// Validate Project Key
async function validateProjectKey(
  client: JiraClient,
  key: string
): Promise<{ errorMessages: string[]; errors: Record<string, string> }> {
  return client.request(`/projectvalidate/key?key=${encodeURIComponent(key)}`);
}

// Get Valid Project Key Suggestion
async function getValidProjectKey(
  client: JiraClient,
  key: string
): Promise<string> {
  return client.request(`/projectvalidate/validProjectKey?key=${encodeURIComponent(key)}`);
}

// Get Valid Project Name
async function getValidProjectName(
  client: JiraClient,
  name: string
): Promise<string> {
  return client.request(`/projectvalidate/validProjectName?name=${encodeURIComponent(name)}`);
}

// Get Project Types
async function getProjectTypes(
  client: JiraClient
): Promise<Array<{
  key: string;
  formattedKey: string;
  descriptionI18nKey: string;
  icon: string;
  color: string;
}>> {
  return client.request('/project/type');
}
```

### Step 9: High-Level Helpers

```typescript
// Full project setup with components and version
async function setupProject(
  client: JiraClient,
  config: {
    key: string;
    name: string;
    leadAccountId: string;
    description?: string;
    components?: string[];
    initialVersion?: string;
  }
): Promise<{
  project: Project;
  components: Component[];
  version?: Version;
}> {
  // Create project
  const project = await createProject(client, {
    key: config.key,
    name: config.name,
    projectTypeKey: 'software',
    leadAccountId: config.leadAccountId,
    description: config.description,
  });

  // Create components
  const components: Component[] = [];
  for (const compName of config.components || []) {
    const comp = await createComponent(client, {
      project: project.key,
      name: compName,
    });
    components.push(comp);
  }

  // Create initial version
  let version: Version | undefined;
  if (config.initialVersion) {
    version = await createVersion(client, {
      projectId: parseInt(project.id),
      name: config.initialVersion,
    });
  }

  return { project, components, version };
}

// Clone project structure (components + unreleased versions)
async function cloneProjectStructure(
  client: JiraClient,
  sourceProjectKey: string,
  targetProjectKey: string
): Promise<{
  componentsCloned: number;
  versionsCloned: number;
}> {
  // Get source components
  const sourceComponents = await getProjectComponents(client, sourceProjectKey);

  // Get source versions (unreleased only)
  const sourceVersions = await getProjectVersions(client, sourceProjectKey, {
    status: 'unreleased',
  });

  // Get target project
  const targetProject = await client.request<Project>(`/project/${targetProjectKey}`);

  // Clone components
  for (const comp of sourceComponents) {
    await createComponent(client, {
      project: targetProjectKey,
      name: comp.name,
      description: comp.description,
    });
  }

  // Clone versions
  for (const ver of sourceVersions.values) {
    await createVersion(client, {
      projectId: parseInt(targetProject.id),
      name: ver.name,
      description: ver.description,
      startDate: ver.startDate,
      releaseDate: ver.releaseDate,
    });
  }

  return {
    componentsCloned: sourceComponents.length,
    versionsCloned: sourceVersions.values.length,
  };
}
```

## curl Examples

### Create Project
```bash
curl -X POST "$JIRA_BASE_URL/rest/api/3/project" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "NEWPROJ",
    "name": "New Project",
    "projectTypeKey": "software",
    "leadAccountId": "5b10a2844c20165700ede21g",
    "description": "Project description"
  }'
```

### Update Project
```bash
curl -X PUT "$JIRA_BASE_URL/rest/api/3/project/SCRUM" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Project Name",
    "description": "Updated description"
  }'
```

### Delete Project
```bash
curl -X DELETE "$JIRA_BASE_URL/rest/api/3/project/SCRUM?enableUndo=true" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)"
```

### Search Projects
```bash
curl -X GET "$JIRA_BASE_URL/rest/api/3/project/search?query=scrum&expand=description,lead" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)" \
  -H "Accept: application/json"
```

### Create Component
```bash
curl -X POST "$JIRA_BASE_URL/rest/api/3/component" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "project": "SCRUM",
    "name": "Backend",
    "description": "Backend services"
  }'
```

### Create Version
```bash
curl -X POST "$JIRA_BASE_URL/rest/api/3/version" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "projectId": 10000,
    "name": "v1.0.0",
    "description": "First release",
    "releaseDate": "2025-01-15"
  }'
```

### Release Version
```bash
curl -X PUT "$JIRA_BASE_URL/rest/api/3/version/10001" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "released": true,
    "releaseDate": "2025-12-10"
  }'
```

### Get Project Roles
```bash
curl -X GET "$JIRA_BASE_URL/rest/api/3/project/SCRUM/role" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)" \
  -H "Accept: application/json"
```

### Add User to Role
```bash
curl -X POST "$JIRA_BASE_URL/rest/api/3/project/SCRUM/role/10002" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "user": ["5b10a2844c20165700ede21g"]
  }'
```

### Validate Project Key
```bash
curl -X GET "$JIRA_BASE_URL/rest/api/3/projectvalidate/key?key=NEWPROJ" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)" \
  -H "Accept: application/json"
```

### Set Project Property
```bash
curl -X PUT "$JIRA_BASE_URL/rest/api/3/project/SCRUM/properties/custom-config" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)" \
  -H "Content-Type: application/json" \
  -d '{"setting1": "value1", "setting2": true}'
```

## API Endpoints Summary

| Operation | Method | Path |
|-----------|--------|------|
| Create project | POST | `/project` |
| Get project | GET | `/project/{projectIdOrKey}` |
| Update project | PUT | `/project/{projectIdOrKey}` |
| Delete project | DELETE | `/project/{projectIdOrKey}` |
| Archive project | POST | `/project/{projectIdOrKey}/archive` |
| Restore project | POST | `/project/{projectIdOrKey}/restore` |
| Search projects | GET | `/project/search` |
| Recent projects | GET | `/project/recent` |
| List components | GET | `/project/{projectIdOrKey}/components` |
| Create component | POST | `/component` |
| Update component | PUT | `/component/{id}` |
| Delete component | DELETE | `/component/{id}` |
| List versions | GET | `/project/{projectIdOrKey}/version` |
| Create version | POST | `/version` |
| Update version | PUT | `/version/{id}` |
| Delete version | DELETE | `/version/{id}` |
| Get roles | GET | `/project/{projectIdOrKey}/role` |
| Get role | GET | `/project/{projectIdOrKey}/role/{roleId}` |
| Add to role | POST | `/project/{projectIdOrKey}/role/{roleId}` |
| Remove from role | DELETE | `/project/{projectIdOrKey}/role/{roleId}` |
| List properties | GET | `/project/{projectIdOrKey}/properties` |
| Get property | GET | `/project/{projectIdOrKey}/properties/{key}` |
| Set property | PUT | `/project/{projectIdOrKey}/properties/{key}` |
| Delete property | DELETE | `/project/{projectIdOrKey}/properties/{key}` |
| Validate key | GET | `/projectvalidate/key` |
| Valid key | GET | `/projectvalidate/validProjectKey` |
| Project types | GET | `/project/type` |

## Common Patterns

### Project Key Rules
- 2-10 uppercase letters only
- Must be unique across instance
- Cannot be reused for 60 days after deletion

### Permission Requirements
| Operation | Required Permission |
|-----------|-------------------|
| Create project | Jira admin |
| Update project | Project admin |
| Delete project | Jira admin |
| Manage components | Project admin |
| Manage versions | Project admin |
| Manage roles | Project admin |

### Project Types
| Type | Use Case |
|------|----------|
| `software` | Scrum/Kanban dev projects |
| `service_desk` | Customer support projects |
| `business` | Simple task tracking |

## Common Mistakes
- Using lowercase in project keys
- Forgetting to get projectId (numeric) for version creation
- Not handling 404 for deleted/archived projects
- Assuming role IDs are consistent (query first)
- Not using enableUndo=true for safe deletion

## References
- [Projects API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-projects/)
- [Project Components](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-project-components/)
- [Project Versions](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-project-versions/)
- [Project Roles](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-project-roles/)
- [Project Properties](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-project-properties/)

## Version History
- 2025-12-10: Created comprehensive project management skill
