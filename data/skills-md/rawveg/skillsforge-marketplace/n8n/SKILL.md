---
name: n8n
description: N8N Documentation - Workflow automation platform with AI capabilities
---

# N8N Skill

Comprehensive assistance with n8n development, generated from official documentation. n8n is a fair-code licensed workflow automation tool that combines AI capabilities with business process automation.

## When to Use This Skill

This skill should be triggered when:
- Building or debugging n8n workflows
- Working with the Code node (JavaScript or Python)
- Using expressions and data transformations
- Implementing AI agents, chains, or RAG workflows
- Configuring n8n deployments (Docker, npm, self-hosted)
- Setting up webhooks, credentials, or integrations
- Handling errors in workflows
- Scaling n8n with queue mode
- Creating custom nodes or white labeling n8n
- Using the n8n API programmatically
- Working with LangChain in n8n
- Migrating to n8n v1.0

## Key Concepts

### Core Components
- **Workflows**: Visual automation flows with nodes connected together
- **Nodes**: Individual operations in a workflow (trigger, action, logic, etc.)
- **Expressions**: Code snippets using `{{ }}` syntax to access and transform data
- **Credentials**: Secure storage for API keys and authentication
- **Executions**: Individual workflow runs with their data and status

### Data Structure
- n8n passes data between nodes as **items** (array of JSON objects)
- Each item has a `json` property containing the main data
- Binary data is stored separately in the `binary` property
- Use `$json` to access current item's data in expressions

### AI Capabilities
- **Agents**: AI that can use tools and make decisions
- **Chains**: Predefined sequences of AI operations
- **Memory**: Store conversation history for context
- **Tools**: Functions that AI agents can call
- **Vector Databases**: Store and retrieve embeddings for RAG

## Quick Reference

### Example 1: Basic Expression to Access Data
```javascript
// Access data from the current item
{{ $json.name }}

// Access data from a specific node
{{ $node["HTTP Request"].json.response }}

// Access all items from a node
{{ $("HTTP Request").all() }}
```

### Example 2: HTTP Request with Authentication
When working with the HTTP Request node, handle errors and rate limits:

```javascript
// In HTTP Request node settings:
// - Enable "Retry on Fail"
// - Set Max Tries to 3
// - Set Wait Between Tries (ms) to 1000

// For rate limiting, use Batching:
// - Items per Batch: 10
// - Batch Interval (ms): 1000
```

### Example 3: Code Node - Transform Data (JavaScript)
```javascript
// Access input data
const items = $input.all();

// Transform each item
return items.map(item => {
  return {
    json: {
      fullName: `${item.json.firstName} ${item.json.lastName}`,
      email: item.json.email.toLowerCase(),
      timestamp: new Date().toISOString()
    }
  };
});
```

### Example 4: Code Node - Filter Data (Python)
```python
# Filter items based on a condition
output = []

for item in items:
    if item['json']['status'] == 'active':
        output.append({
            'json': {
                'id': item['json']['id'],
                'name': item['json']['name']
            }
        })

return output
```

### Example 5: Expression - Date Handling with Luxon
```javascript
// Current date
{{ $now }}

// Format date
{{ $now.toFormat('yyyy-MM-dd') }}

// Add 7 days
{{ $now.plus({ days: 7 }) }}

// Parse and format custom date
{{ DateTime.fromISO($json.dateString).toFormat('LLL dd, yyyy') }}
```

### Example 6: JWT Authentication Credential
For APIs requiring JWT authentication:

```javascript
// Use JWT credential with:
// - Key Type: Passphrase (for HMAC) or PEM Key (for RSA/ECDSA)
// - Secret: Your secret key
// - Algorithm: HS256, RS256, ES256, etc.

// The JWT credential automatically generates tokens
// Use it in HTTP Request node > Authentication > JWT
```

### Example 7: Handle Errors in Workflow
```javascript
// In Code node, use try-catch:
try {
  const result = $json.data.someField.toUpperCase();
  return [{ json: { result } }];
} catch (error) {
  // Return error information
  return [{
    json: {
      error: error.message,
      originalData: $json
    }
  }];
}

// Or set up Error Workflow in Workflow Settings
// to catch all failures and send notifications
```

### Example 8: Pagination in HTTP Request
```javascript
// Use pagination to fetch all pages
// In HTTP Request node > Pagination:

// Type: Generic Pagination
// Request URL: {{ $url }}&page={{ $pageNumber }}
// Complete When: {{ $response.body.hasMore === false }}
// Next Page URL: Automatic
```

### Example 9: AI Agent with Tools
```javascript
// In AI Agent node:
// 1. Connect a Chat Model (OpenAI, etc.)
// 2. Add tools (Calculator, HTTP Request, etc.)
// 3. Configure memory if needed

// The agent can:
// - Analyze user input
// - Decide which tools to use
// - Execute tools and process results
// - Return final answer
```

### Example 10: Environment Variables and Static Data
```javascript
// Access environment variables
{{ $env.MY_API_KEY }}

// Store workflow static data (persists across executions)
const staticData = getWorkflowStaticData('global');
staticData.lastRun = new Date().toISOString();
staticData.counter = (staticData.counter || 0) + 1;

// Retrieve static data
{{ $workflow.staticData.counter }}
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **llms-txt.md** - Complete n8n documentation formatted for LLMs
  - Installation and setup guides
  - Node reference documentation
  - API documentation
  - Code examples and patterns
  - Configuration options
  - Troubleshooting guides

- **llms-full.md** - Extended documentation with deep technical details
  - Advanced configuration
  - Scaling and performance
  - Security and authentication
  - Custom node development
  - White labeling and embed options

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
1. Start with basic workflow creation:
   - Trigger nodes (Webhook, Schedule, Manual)
   - Action nodes (HTTP Request, Set, Edit Fields)
   - Learn expression syntax with simple `{{ $json.field }}` access

2. Understand data structure:
   - Each node outputs an array of items
   - Use the data inspector to see item structure
   - Practice with the Edit Fields node for data transformation

3. Common patterns:
   - Webhook → HTTP Request → Set → Respond to Webhook
   - Schedule → Code → HTTP Request → Conditional
   - Manual → Loop Over Items → Process Each

### For Intermediate Users
1. Master the Code node:
   - JavaScript mode for complex transformations
   - Access `$input.all()` for all items
   - Return properly formatted items with `json` property

2. Work with expressions:
   - Use built-in methods: `.first()`, `.last()`, `.item`
   - Date manipulation with Luxon
   - JMESPath for complex JSON queries

3. Error handling:
   - Use Try-Catch in Code nodes
   - Set up Error Workflows
   - Configure Retry on Fail for API calls

4. Data operations:
   - Merge data from multiple sources
   - Split and filter items
   - Loop over items for batch processing

### For Advanced Users
1. AI and LangChain:
   - Build AI agents with custom tools
   - Implement RAG with vector databases
   - Use memory for conversational workflows
   - Chain multiple AI operations

2. Scaling and performance:
   - Configure queue mode for distributed execution
   - Optimize database settings
   - Use execution data pruning
   - Configure task runners

3. Custom development:
   - Create custom nodes
   - White label n8n for embedding
   - Use the n8n API for workflow management
   - Implement external secrets with AWS/Azure/GCP

4. Advanced patterns:
   - Sub-workflows for reusability
   - Webhook authentication and validation
   - Complex data transformations with JMESPath
   - Real-time data processing with SSE/WebSockets

## Common Issues and Solutions

### HTTP Request Errors
- **400 Bad Request**: Check query parameters and array formatting
- **403 Forbidden**: Verify credentials and API permissions
- **429 Rate Limit**: Use Batching or Retry on Fail options
- **404 Not Found**: Verify endpoint URL is correct

### Expression Errors
- Workflows now fail on expression errors in v1.0+
- Set up Error Workflows to catch failures
- Test expressions in the expression editor
- Check for undefined values before accessing properties

### Data Type Issues
- Use `.toString()`, `.toNumber()` for type conversion
- Handle null/undefined with `{{ $json.field || 'default' }}`
- Binary data requires special handling with buffers

### Migration to v1.0
- New execution order (depth-first instead of breadth-first)
- Python support in Code node (Pyodide)
- Mandatory user management (no more BasicAuth)
- WebSocket push backend is now default
- Node 18.17.0 or higher required

## Environment Configuration

### Docker Setup
```bash
# Basic n8n with Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# With environment variables
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=admin \
  -e N8N_BASIC_AUTH_PASSWORD=password \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

### Key Environment Variables
- `N8N_HOST`: Hostname (default: localhost)
- `N8N_PORT`: Port (default: 5678)
- `N8N_PROTOCOL`: http or https
- `WEBHOOK_URL`: External webhook URL
- `N8N_ENCRYPTION_KEY`: Encryption key for credentials
- `DB_TYPE`: Database type (sqlite, postgres)
- `EXECUTIONS_MODE`: queue or main (queue for scaling)

## Resources

### Official Resources
- [n8n Documentation](https://docs.n8n.io/)
- [n8n Community Forum](https://community.n8n.io/)
- [n8n Workflow Templates](https://n8n.io/workflows/)
- [n8n GitHub Repository](https://github.com/n8n-io/n8n)

### Learning Paths
- Level One Course: Basic workflow building
- Level Two Course: Advanced data handling and error management
- Video Courses: Visual learning resources
- AI Tutorial: Build AI workflows from scratch

### API and Development
- [API Reference](https://docs.n8n.io/api/api-reference/)
- [Creating Custom Nodes](https://docs.n8n.io/integrations/creating-nodes/)
- [Node Development](https://docs.n8n.io/integrations/creating-nodes/build/)

## Notes

- This skill was automatically generated from official n8n documentation
- Code examples use proper language tags for syntax highlighting
- Examples are extracted from real-world patterns in the docs
- Focus on practical, actionable patterns for immediate use

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information
3. Review Quick Reference section for new examples
