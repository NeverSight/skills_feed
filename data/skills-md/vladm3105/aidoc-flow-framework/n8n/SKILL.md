---
title: "n8n: Develop workflows, custom nodes, and integrations for n8n automation platform"
name: n8n
description: Develop workflows, custom nodes, and integrations for n8n automation platform
tags:
  - sdd-workflow
  - shared-architecture
  - domain-specific
custom_fields:
  layer: null
  artifact_type: null
  architecture_approaches: [ai-agent-based, traditional-8layer]
  priority: shared
  development_status: active
  skill_category: domain-specific
  upstream_artifacts: []
  downstream_artifacts: []
---

# n8n Workflow Automation Skill

## Purpose

Provide specialized guidance for developing workflows, custom nodes, and integrations on the n8n automation platform. Enable AI assistants to design workflows, write custom code nodes, build TypeScript-based custom nodes, integrate external services, and implement AI agent patterns.

## When to Use This Skill

Invoke this skill when:

- Designing automation workflows combining multiple services
- Writing JavaScript/Python code within workflow nodes
- Building custom nodes in TypeScript
- Integrating APIs, databases, and cloud services
- Creating AI agent workflows with LangChain
- Troubleshooting workflow execution errors
- Planning self-hosted n8n deployments
- Converting manual processes to automated workflows

Do NOT use this skill for:

- Generic automation advice (use appropriate language/platform skill)
- Cloud platform-specific integrations (combine with cloud provider skill)
- Database design (use database-specialist skill)
- Frontend development (n8n has minimal UI customization)

## Core n8n Concepts

### Platform Architecture

**Runtime Environment:**
- Node.js-based execution engine
- TypeScript (90.7%) and Vue.js frontend
- pnpm monorepo structure
- Self-hosted or cloud deployment options

**Workflow Execution Models:**
1. **Manual trigger** - User-initiated execution
2. **Webhook trigger** - HTTP endpoint activation
3. **Schedule trigger** - Cron-based timing
4. **Event trigger** - External service events (database changes, file uploads)
5. **Error trigger** - Workflow failure handling

**Fair-code License:**
- Apache 2.0 with Commons Clause
- Free for self-hosting and unlimited executions
- Commercial restrictions for SaaS offerings

### Node Types and Categories

**Core Nodes** (Data manipulation):
- **Code** - Execute JavaScript/Python
- **Set** - Assign variable values
- **If** - Conditional branching
- **Switch** - Multi-branch routing
- **Merge** - Combine data streams
- **Split In Batches** - Process large datasets incrementally
- **Loop Over Items** - Iterate through data

**Trigger Nodes** (Workflow initiation):
- **Webhook** - HTTP endpoint
- **Schedule** - Time-based execution
- **Manual Trigger** - User activation
- **Error Trigger** - Catch workflow failures
- **Start** - Default entry point

**Action Nodes** (500+ integrations):
- API connectors (REST, GraphQL, SOAP)
- Database clients (PostgreSQL, MongoDB, MySQL, Redis)
- Cloud services (AWS, GCP, Azure, Cloudflare)
- Communication (Email, Slack, Discord, SMS)
- File operations (FTP, S3, Google Drive, Dropbox)
- Authentication (OAuth2, API keys, JWT)

**AI Nodes** (LangChain integration):
- **AI Agent** - Autonomous decision-making
- **AI Chain** - Sequential LLM operations
- **AI Transform** - Data manipulation with LLMs
- **Vector Store** - Embedding storage and retrieval
- **Document Loaders** - Text extraction from files

### Data Flow and Connections

**Connection Types:**
1. **Main connection** - Primary data flow (solid line)
2. **Error connection** - Failure routing (dashed red line)

**Data Structure:**
```javascript
// Input/output format for all nodes
[
  {
    json: { /* Your data object */ },
    binary: { /* Optional binary data (files, images) */ },
    pairedItem: { /* Reference to source item */ }
  }
]
```

**Data Access Patterns:**
- **Expression** - `{{ $json.field }}` (current node output)
- **Input reference** - `{{ $('NodeName').item.json.field }}` (specific node)
- **All items** - `{{ $input.all() }}` (entire dataset)
- **First item** - `{{ $input.first() }}` (single item)
- **Item index** - `{{ $itemIndex }}` (current iteration)

### Credentials and Authentication

**Credential Types:**
- **Predefined** - Pre-configured for popular services (OAuth2, API key)
- **Generic** - HTTP authentication (Basic, Digest, Header Auth)
- **Custom** - User-defined credential structures

**Security Practices:**
- Credentials stored encrypted in database
- Environment variable support for sensitive values
- Credential sharing across workflows (optional)
- Rotation: Manual update required

## Workflow Design Methodology

### Planning Phase

**Step 1: Define Requirements**
- Input sources (webhooks, schedules, databases)
- Data transformations needed
- Output destinations (APIs, files, databases)
- Error handling requirements
- Execution frequency and volume

**Step 2: Map Data Flow**
- Identify trigger events
- List transformation steps
- Specify validation rules
- Define branching logic
- Plan error recovery

**Step 3: Select Nodes**

Decision criteria:
- Use **native nodes** when available (optimized, maintained)
- Use **Code node** for custom logic <50 lines
- Build **custom node** for reusable complex logic >100 lines
- Use **HTTP Request node** for APIs without native nodes
- Use **Execute Command node** for system operations (security risk)

### Implementation Phase

**Workflow Structure Pattern:**

```
[Trigger] → [Validation] → [Branch (If/Switch)] → [Processing] → [Error Handler]
                                ↓                      ↓
                          [Path A nodes]        [Path B nodes]
                                ↓                      ↓
                          [Merge/Output]         [Output]
```

**Modular Design:**
- Extract reusable logic to sub-workflows
- Use Execute Workflow node for modularity
- Limit main workflow to 15-20 nodes (readability)
- Parameterize workflows with input variables

**Error Handling Strategy:**

1. **Error Trigger workflows** - Capture all failures
2. **Try/Catch pattern** - Error output connections on nodes
3. **Retry logic** - Configure per-node retry settings
4. **Validation nodes** - If/Switch for data checks
5. **Notification** - Alert on critical failures (Email, Slack)

### Testing Phase

**Local Testing:**
- Execute with sample data
- Verify each node output (inspect data panel)
- Test error paths with invalid data
- Check credential connections

**Production Validation:**
- Enable workflow, monitor executions
- Review execution history for failures
- Check resource usage (execution time, memory)
- Validate output data quality

## Code Execution in Workflows

### Code Node (JavaScript)

**Available APIs:**
- **Node.js built-ins** - `fs`, `path`, `crypto`, `https`
- **Lodash** - `_.groupBy()`, `_.sortBy()`, etc.
- **Luxon** - DateTime manipulation
- **n8n helpers** - `$input`, `$json`, `$binary`

**Basic Structure:**
```javascript
// Access input items
const items = $input.all();

// Process data
const processedItems = items.map(item => {
  const inputData = item.json;

  return {
    json: {
      // Output fields
      processed: inputData.field.toUpperCase(),
      timestamp: new Date().toISOString()
    }
  };
});

// Return transformed items
return processedItems;
```

**Data Transformation Patterns:**

*Filtering:*
```javascript
const items = $input.all();
return items.filter(item => item.json.status === 'active');
```

*Aggregation:*
```javascript
const items = $input.all();
const grouped = _.groupBy(items, item => item.json.category);

return [{
  json: {
    summary: Object.keys(grouped).map(category => ({
      category,
      count: grouped[category].length
    }))
  }
}];
```

*API calls (async):*
```javascript
const items = $input.all();
const results = [];

for (const item of items) {
  const response = await fetch(`https://api.example.com/data/${item.json.id}`);
  const data = await response.json();

  results.push({
    json: {
      original: item.json,
      enriched: data
    }
  });
}

return results;
```

**Error Handling in Code:**
```javascript
const items = $input.all();

return items.map(item => {
  try {
    // Risky operation
    const result = JSON.parse(item.json.data);
    return { json: { parsed: result } };
  } catch (error) {
    return {
      json: {
        error: error.message,
        original: item.json.data
      }
    };
  }
});
```

### Code Node (Python)

**Available Libraries:**
- **Standard library** - `json`, `datetime`, `re`, `requests`
- **NumPy** - Array operations
- **Pandas** - Data analysis (if installed)

**Basic Structure:**
```python
# Access input items
items = _input.all()

# Process data
processed_items = []
for item in items:
    input_data = item['json']

    processed_items.append({
        'json': {
            'processed': input_data['field'].upper(),
            'timestamp': datetime.now().isoformat()
        }
    })

# Return transformed items
return processed_items
```

**Complexity Rating: Code Nodes**
- Simple transformations (map/filter): **1**
- API calls with error handling: **2**
- Multi-step async operations: **3**
- Complex algorithms with libraries: **4**
- Performance-critical processing: **5** (consider custom node)

## Custom Node Development

### When to Build Custom Nodes

**Build custom node when:**
- Reusable logic across multiple workflows (>3 workflows)
- Complex authentication requirements
- Performance-critical operations (Code node overhead)
- Community contribution (public npm package)
- Organization-specific integrations

**Use Code node when:**
- One-off transformations
- Rapid prototyping
- Simple API calls (<100 lines)

### Development Styles

[See Code Examples: examples/n8n_custom_node.ts]

**1. Programmatic Style** (Full control)

*Use for:*
- Complex authentication flows
- Advanced parameter validation
- Custom UI components
- Polling operations with state management

[See: `CustomNode` class in examples/n8n_custom_node.ts]

**2. Declarative Style** (Simplified)

*Use for:*
- Standard CRUD operations
- RESTful API wrappers
- Simple integrations without complex logic

[See: `operations` and `router` exports in examples/n8n_custom_node.ts]

**Additional Examples:**

- Credential configuration: `customApiCredentials` in examples/n8n_custom_node.ts
- Credential validation: `validateCredentials()` in examples/n8n_custom_node.ts
- Polling trigger: `PollingTrigger` class in examples/n8n_custom_node.ts

### Development Workflow

**Step 1: Initialize Node**
```bash
# Create from template
npm create @n8n/node my-custom-node

# Directory structure created:
# ├── nodes/
# │   └── MyCustomNode/
# │       └── MyCustomNode.node.ts
# ├── credentials/
# │   └── MyCustomNodeApi.credentials.ts
# └── package.json
```

**Step 2: Implement Logic**
- Define node properties (parameters, credentials)
- Implement execute method
- Add error handling
- Write unit tests (optional)

**Step 3: Build and Test**
```bash
# Build TypeScript
npm run build

# Link locally for testing
npm link

# In n8n development environment
cd ~/.n8n/nodes
npm link my-custom-node

# Restart n8n to load node
n8n start
```

**Step 4: Publish**
```bash
# Community node (npm package)
npm publish

# Install in n8n
Settings → Community Nodes → Install → Enter package name
```

**Complexity Rating: Custom Nodes**
- Declarative CRUD wrapper: **2**
- Programmatic with authentication: **3**
- Complex state management: **4**
- Advanced polling/webhooks: **5**

## Integration Patterns

### API Integration Strategy

**Decision Tree:**

```
Has native node? ──Yes──> Use native node
     │
     No
     ├──> Simple REST API? ──Yes──> HTTP Request node
     ├──> Complex auth (OAuth2)? ──Yes──> Build custom node
     ├──> Reusable across workflows? ──Yes──> Build custom node
     └──> One-off integration? ──Yes──> Code node with fetch()
```

### HTTP Request Node Patterns

**GET with query parameters:**
```
URL: https://api.example.com/users
Method: GET
Query Parameters:
  - status: active
  - limit: 100
Authentication: Header Auth
  - Name: Authorization
  - Value: Bearer {{$credentials.apiKey}}
```

**POST with JSON body:**
```
URL: https://api.example.com/users
Method: POST
Body Content Type: JSON
Body:
{
  "name": "={{ $json.name }}",
  "email": "={{ $json.email }}"
}
```

**Pagination handling (Code node):**
```javascript
let allResults = [];
let page = 1;
let hasMore = true;

while (hasMore) {
  const response = await this.helpers.request({
    method: 'GET',
    url: `https://api.example.com/data?page=${page}`,
    json: true,
  });

  allResults = allResults.concat(response.results);
  hasMore = response.hasNext;
  page++;
}

return allResults.map(item => ({ json: item }));
```

### Webhook Patterns

**Receiving webhooks:**
1. Create webhook trigger node
2. Configure HTTP method (POST/GET)
3. Set authentication (None/Header Auth/Basic Auth)
4. Get webhook URL from node
5. Register URL with external service

**Responding to webhooks:**
```javascript
// In Code node after webhook trigger
const webhookData = $input.first().json;

// Process data
const result = processData(webhookData);

// Return response (synchronous webhook)
return [{
  json: {
    status: 'success',
    data: result
  }
}];
```

**Webhook URL structure:**
```
Production: https://your-domain.com/webhook/workflow-id
Test: https://your-domain.com/webhook-test/workflow-id
```

### Database Integration

**Common patterns:**

*Query with parameters:*
```sql
-- PostgreSQL node
SELECT * FROM users
WHERE created_at > $1
  AND status = $2
ORDER BY created_at DESC

-- Parameters from previous node
Parameters: ['{{ $json.startDate }}', 'active']
```

*Batch insert:*
```javascript
// Code node preparing data for database
const items = $input.all();
const values = items.map(item => ({
  name: item.json.name,
  email: item.json.email,
  created_at: new Date().toISOString()
}));

return [{ json: { values } }];

// Next node: PostgreSQL
// INSERT INTO users (name, email, created_at)
// VALUES {{ $json.values }}
```

### File Operations

**Upload to S3:**
```
Workflow: File Trigger → S3 Upload
- File Trigger: Monitor directory for new files
- S3 node:
  - Operation: Upload
  - Bucket: my-bucket
  - File Name: {{ $json.fileName }}
  - Binary Data: true (from file trigger)
```

**Download and process:**
```
HTTP Request (download) → Code (process) → Google Drive (upload)
- HTTP Request: Binary response enabled
- Code: Process $binary.data
- Google Drive: Upload with binary data
```

## AI Agent Workflows

### LangChain Integration

**AI Agent Node Configuration:**
- **Agent type**: OpenAI Functions, ReAct, Conversational
- **LLM**: OpenAI, Anthropic, Hugging Face, Ollama (local)
- **Memory**: Buffer, Buffer Window, Summary
- **Tools**: Calculator, Webhook, Database query, Custom API calls

**Basic Agent Pattern:**
```
Manual Trigger → AI Agent → Output
- AI Agent:
  - Prompt: "You are a helpful assistant that {{$json.task}}"
  - Tools: [Calculator, HTTP Request]
  - Memory: Conversation Buffer Window
```

### Gatekeeper Pattern (Supervised AI)

**Use case:** Human approval before agent actions

```
Webhook → AI Agent → If (requires approval) → Send Email → Wait for Webhook → Execute Action
                            ↓ (auto-approve)
                        Execute Action
```

**Implementation:**
1. AI Agent generates action plan
2. If node checks confidence score
3. Low confidence → Email approval request
4. Wait for webhook (approve/reject)
5. Execute or abort based on response

### Iterative Agent Pattern

**Use case:** Multi-step problem solving with state

```
Loop Start → AI Agent → Tool Execution → State Update → Loop End (condition check)
     ↑______________________________________________________________|
```

**State management:**
```javascript
// Code node - Initialize state
return [{
  json: {
    task: 'Research topic',
    iteration: 0,
    maxIterations: 5,
    context: [],
    completed: false
  }
}];

// Code node - Update state
const state = $json;
state.iteration++;
state.context.push($('AI Agent').item.json.response);
state.completed = state.iteration >= state.maxIterations || checkGoalMet(state);

return [{ json: state }];
```

### RAG (Retrieval Augmented Generation) Pattern

```
Query Input → Vector Store Search → Format Context → LLM → Response Output
```

**Vector Store setup:**
1. Document Loader node → Split text into chunks
2. Embeddings node → Generate vectors (OpenAI, Cohere)
3. Vector Store node → Store in Pinecone/Qdrant/Supabase
4. Query: Retrieve relevant chunks → Inject into LLM prompt

**Complexity Rating: AI Workflows**
- Simple LLM call: **1**
- Agent with tools: **3**
- Gatekeeper pattern: **4**
- Multi-agent orchestration: **5**

## Deployment and Hosting

### Self-Hosting Options

[See Code Examples: examples/n8n_deployment.yaml]

**Docker (Recommended):**
- Docker Compose with PostgreSQL
- Queue mode configuration for scaling
- Resource requirements by volume

[See: docker-compose configurations in examples/n8n_deployment.yaml]

**npm (Development):**
```bash
npm install n8n -g
n8n start
# Access: http://localhost:5678
```

**Environment Configuration:**

[See: Complete environment variable reference in examples/n8n_deployment.yaml]

Essential variables:
- `N8N_HOST` - Public URL for webhooks
- `WEBHOOK_URL` - Webhook endpoint base
- `N8N_ENCRYPTION_KEY` - Credential encryption (must persist)
- `DB_TYPE` - Database (SQLite/PostgreSQL/MySQL/MariaDB)
- `EXECUTIONS_DATA_SAVE_ON_ERROR` - Error logging
- `EXECUTIONS_DATA_SAVE_ON_SUCCESS` - Success logging

Performance tuning variables documented in examples/n8n_deployment.yaml

### Scaling Considerations

**Queue Mode (High volume):**
```bash
# Separate main and worker processes
# Main process (UI + queue management)
N8N_QUEUE_MODE=main n8n start

# Worker processes (execution only)
N8N_QUEUE_MODE=worker n8n worker
```

**Database:**
- SQLite: Development/low volume (<1000 executions/day)
- PostgreSQL: Production (recommended)
- MySQL/MariaDB: Alternative for existing infrastructure

**Resource Requirements:**

| Workflow Volume | CPU | RAM | Database |
|----------------|-----|-----|----------|
| <100 exec/day | 1 core | 512MB | SQLite |
| 100-1000/day | 2 cores | 2GB | PostgreSQL |
| 1000-10000/day | 4 cores | 4GB | PostgreSQL |
| >10000/day | 8+ cores | 8GB+ | PostgreSQL + Queue mode |

**Monitoring:**
- Enable execution logs (EXECUTIONS_DATA_SAVE_*)
- Set up error workflows (Error Trigger node)
- Monitor database size (execution history cleanup)
- Track webhook response times

## Best Practices

### Workflow Design

**1. Modularity:**
- Extract reusable logic to Execute Workflow nodes
- Limit workflows to single responsibility
- Use sub-workflows for common operations (validation, formatting)

**2. Error Resilience:**
- Add error outputs to critical nodes
- Implement retry logic (node settings)
- Create Error Trigger workflows for alerts
- Log errors to external systems (Sentry, CloudWatch)

**3. Performance:**
- Use Split In Batches for large datasets (>1000 items)
- Minimize HTTP requests in loops (batch API calls)
- Disable execution logging for high-frequency workflows
- Cache expensive operations in variables

**4. Security:**
- Store secrets in credentials (not hardcoded)
- Use environment variables for configuration
- Enable webhook authentication
- Restrict Execute Command node usage (or disable globally)
- Review code nodes for injection vulnerabilities

**5. Maintainability:**
- Add notes to complex workflows (Sticky Note node)
- Use consistent naming (verb + noun: "Fetch Users", "Transform Data")
- Document workflow purpose in workflow settings
- Version control workflows (export JSON, commit to Git)

### Code Quality in Nodes

**1. Data validation:**
```javascript
// Always validate input structure
const items = $input.all();

for (const item of items) {
  if (!item.json.email || !item.json.name) {
    throw new Error(`Invalid input: missing required fields at item ${item.json.id}`);
  }
}
```

**2. Error context:**
```javascript
// Provide debugging information
try {
  const result = await apiCall(item.json.id);
} catch (error) {
  throw new Error(`API call failed for ID ${item.json.id}: ${error.message}`);
}
```

**3. Idempotency:**
```javascript
// Check existence before creation
const exists = await checkExists(item.json.uniqueId);
if (!exists) {
  await createRecord(item.json);
}
```

## Workflow Pattern Library

### Pattern 1: API Sync

**Use case:** Sync data between two systems

```
Schedule Trigger (hourly) → Fetch Source Data → Transform → If (record exists) → Update Target
                                                                    ↓ (new)
                                                                Create in Target
```

**Complexity:** 2

### Pattern 2: Error Recovery

**Use case:** Retry failed operations with exponential backoff

```
Main Workflow → Process → Error → Error Trigger Workflow
                                        ↓
                                   Wait (delay) → Retry → If (max retries) → Alert
```

**Complexity:** 3

### Pattern 3: Data Enrichment

**Use case:** Augment data with external sources

```
Webhook → Split In Batches → For Each Item:
                                  ↓
                             API Call (enrich) → Code (merge) → Batch Results
                                                                      ↓
                                                                Database Insert
```

**Complexity:** 3

### Pattern 4: Event-Driven Processing

**Use case:** Process events from message queue

```
SQS Trigger → Parse Message → Switch (event type) → [Handler A, Handler B, Handler C] → Confirm/Delete Message
```

**Complexity:** 3

### Pattern 5: Human-in-the-Loop

**Use case:** Approval workflow

```
Trigger → Generate Request → Send Email (approval link) → Webhook (approval response) → If (approved) → Execute Action
                                                                                              ↓ (rejected)
                                                                                         Send Rejection Notice
```

**Complexity:** 4

### Pattern 6: Multi-Stage ETL

**Use case:** Complex data pipeline

```
Schedule → Extract (API) → Validate → Transform → Load (Database) → Success Notification
                               ↓                                            ↓
                          Error Handler ────────────────────> Error Notification
```

**Complexity:** 3

## Quality Gates

### Definition of Done: Workflows

A workflow is production-ready when:

1. **Functionality:**
   - ✓ All nodes execute without errors on test data
   - ✓ Error paths tested with invalid input
   - ✓ Output format validated against requirements

2. **Error Handling:**
   - ✓ Error outputs configured on critical nodes
   - ✓ Error Trigger workflow created for alerts
   - ✓ Retry logic configured where applicable

3. **Security:**
   - ✓ Credentials used (no hardcoded secrets)
   - ✓ Webhook authentication enabled
   - ✓ Input validation implemented

4. **Documentation:**
   - ✓ Workflow description filled in settings
   - ✓ Complex logic documented with notes
   - ✓ Parameter descriptions clear

5. **Performance:**
   - ✓ Tested with realistic data volume
   - ✓ Execution time acceptable
   - ✓ Resource usage within limits

### Definition of Done: Custom Nodes

A custom node is production-ready when:

1. **Functionality:**
   - ✓ All operations implemented and tested
   - ✓ Credentials integration working
   - ✓ Parameters validated

2. **Code Quality:**
   - ✓ TypeScript types defined
   - ✓ Error handling comprehensive
   - ✓ No hardcoded values (use parameters)

3. **Documentation:**
   - ✓ README with installation instructions
   - ✓ Parameter descriptions clear
   - ✓ Example workflows provided

4. **Distribution:**
   - ✓ Published to npm (if public)
   - ✓ Versioned appropriately
   - ✓ Dependencies declared in package.json

## Error Handling Guide

### Common Issues and Resolutions

**Issue: Workflow fails with "Invalid JSON"**
- **Cause:** Node output not in correct format
- **Resolution:**
  ```javascript
  // Ensure return format
  return [{ json: { your: 'data' } }];
  // NOT: return { your: 'data' };
  ```

**Issue: "Cannot read property of undefined"**
- **Cause:** Missing data from previous node
- **Resolution:**
  ```javascript
  // Check existence before access
  const value = $json.field?.subfield ?? 'default';
  ```

**Issue: Webhook not receiving data**
- **Cause:** Incorrect webhook URL or authentication
- **Resolution:**
  - Verify URL matches external service configuration
  - Check authentication method matches (None/Header/Basic)
  - Test with curl:
    ```bash
    curl -X POST https://your-n8n.com/webhook/test \
      -H "Content-Type: application/json" \
      -d '{"test": "data"}'
    ```

**Issue: Custom node not appearing**
- **Cause:** Not properly linked/installed
- **Resolution:**
  ```bash
  # Check installation
  npm list -g | grep n8n-nodes-

  # Reinstall if needed
  npm install -g n8n-nodes-your-node

  # Restart n8n
  ```

**Issue: High memory usage**
- **Cause:** Processing large datasets without batching
- **Resolution:**
  - Use Split In Batches node (batch size: 100-1000)
  - Disable execution data saving for high-frequency workflows
  - Set EXECUTIONS_DATA_PRUNE=true

**Issue: Credentials not working**
- **Cause:** Incorrect credential configuration or expired tokens
- **Resolution:**
  - Re-authenticate OAuth2 credentials
  - Verify API key/token validity
  - Check credential permissions in service

### Debugging Strategies

**1. Inspect node output:**
- Click node → View executions data
- Check json and binary tabs
- Verify data structure matches expectations

**2. Add debug Code nodes:**
```javascript
// Log intermediate values
const data = $json;
console.log('Debug data:', JSON.stringify(data, null, 2));
return [{ json: data }];
```

**3. Use If node for validation:**
```javascript
// Expression to check data quality
{{ $json.email && $json.email.includes('@') }}
```

**4. Enable execution logging:**
- Settings → Log → Set level to debug
- Check docker logs: `docker logs n8n -f`

**5. Test in isolation:**
- Create test workflow with Manual Trigger
- Copy problematic nodes
- Use static test data

## References

### Official Documentation
- **Main docs:** https://docs.n8n.io
- **Node reference:** https://docs.n8n.io/integrations/builtin/
- **Custom node development:** https://docs.n8n.io/integrations/creating-nodes/
- **Expression reference:** https://docs.n8n.io/code/expressions/

### Code Repositories
- **Core platform:** https://github.com/n8n-io/n8n
- **Documentation:** https://github.com/n8n-io/n8n-docs
- **Community nodes:** https://www.npmjs.com/search?q=n8n-nodes

### Community Resources
- **Forum:** https://community.n8n.io
- **Templates:** https://n8n.io/workflows (workflow library)
- **YouTube:** Official n8n channel (tutorials)

### Related Skills
- For cloud integrations: Use `cloud-devops-expert` skill
- For database design: Use `database-specialist` skill
- For API design: Use `api-design-architect` skill
- For TypeScript development: Use language-specific skills

---

**Version:** 1.0.0
**Last Updated:** 2025-11-13
**Complexity Rating:** 3 (Moderate - requires platform-specific knowledge)
**Estimated Learning Time:** 8-12 hours for proficiency
