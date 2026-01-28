---
name: n8n-mcp-orchestrator
description: Expert MCP (Model Context Protocol) orchestration with n8n workflow automation. Master bidirectional MCP integration, expose n8n workflows as AI agent tools, consume MCP servers in workflows, build agentic systems, orchestrate multi-agent workflows, and create production-ready AI-powered automation pipelines with Claude Code integration.
---

# n8n MCP Orchestrator

A comprehensive skill for orchestrating AI agents and workflows using n8n's Model Context Protocol (MCP) integration. This skill enables bidirectional MCP patterns, agentic workflow automation, and production-ready AI-powered systems with Claude Code integration.

## When to Use This Skill

Use this skill when:

- Building AI-powered automation workflows with n8n
- Exposing n8n workflows as tools for AI agents (Claude Code, Claude Desktop)
- Consuming external MCP servers from n8n workflows
- Orchestrating multi-agent systems and agentic workflows
- Creating tool-using AI agents with n8n backend
- Integrating Claude Code with business process automation
- Building context-aware automation with MCP resources
- Coordinating complex workflows across multiple AI agents
- Developing production-ready AI orchestration pipelines
- Implementing bidirectional MCP communication patterns
- Creating autonomous agent systems with workflow orchestration
- Building AI-first automation with 400+ service integrations

## Core Concepts

### Model Context Protocol (MCP)

The Model Context Protocol is an open standard for connecting AI assistants to external systems:

- **Bidirectional Communication**: Clients and servers can both initiate requests
- **Resource Management**: Expose data and context as resources
- **Tool Invocation**: AI agents can execute tools (functions/workflows)
- **Prompt Templates**: Provide structured prompts to AI systems
- **Security**: Built-in authentication and authorization patterns
- **Scalability**: Designed for production AI orchestration

### MCP Architecture Components

**1. MCP Servers**
- Expose capabilities (tools, resources, prompts) to AI clients
- Can be standalone services or embedded in applications
- Handle authentication, rate limiting, and security
- n8n workflows can act as MCP servers

**2. MCP Clients**
- Connect to MCP servers and invoke their capabilities
- AI assistants like Claude Code and Claude Desktop
- n8n workflows can act as MCP clients

**3. Resources**
- Data sources and context exposed by MCP servers
- Examples: documents, database records, API responses
- AI agents can read resources for context

**4. Tools**
- Functions/workflows that AI agents can invoke
- Accept parameters and return results
- n8n workflows become AI-callable tools

**5. Prompts**
- Structured prompt templates for AI interactions
- Include context, instructions, and variables
- Guide AI behavior in specific scenarios

### n8n's Bidirectional MCP Capability

**n8n as MCP Server** (Expose workflows as tools):
- MCP Server Trigger node activates workflow when called by AI
- Workflows become tools that Claude Code can invoke
- Enable AI agents to automate complex business processes
- Return structured data to AI clients

**n8n as MCP Client** (Call external MCP servers):
- MCP Client Tool node invokes external MCP servers
- Call tools from other MCP-compatible services
- Orchestrate multiple MCP servers in single workflow
- Build complex automation chains

### Key MCP Nodes in n8n

**1. MCP Server Trigger**
- Workflow entry point for MCP tool invocations
- Receives parameters from AI agents
- Returns results to calling AI client
- Supports authentication and validation

**2. MCP Client Tool**
- Call external MCP server tools
- Pass parameters to remote tools
- Handle responses and errors
- Chain multiple MCP calls

## n8n as MCP Server

### Exposing Workflows as AI Agent Tools

When you create a workflow with an MCP Server Trigger, that workflow becomes a tool that AI agents can invoke.

**Architecture Pattern:**

```
┌─────────────────────────────────────────────────────────────────┐
│                    Claude Code / Claude Desktop                 │
│                                                                 │
│  Agent decides to use tool:                                     │
│  "I need to create a support ticket for this bug"              │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ↓ MCP Tool Invocation
┌─────────────────────────────────────────────────────────────────┐
│                    n8n Workflow (MCP Server)                    │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ MCP Server Trigger                                        │  │
│  │ Tool: "create_support_ticket"                             │  │
│  │ Receives: {title, description, priority}                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                          │                                      │
│                          ↓                                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ HTTP Request: Call Jira API                               │  │
│  └──────────────────────────────────────────────────────────┘  │
│                          │                                      │
│                          ↓                                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Slack Notification: Notify team                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                          │                                      │
│                          ↓                                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Respond to MCP: Return ticket ID                          │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ↓ MCP Response
┌─────────────────────────────────────────────────────────────────┐
│                    Claude Code                                  │
│                                                                 │
│  Receives: {ticketId: "JIRA-12345", status: "created"}        │
│  Continues conversation with user                              │
└─────────────────────────────────────────────────────────────────┘
```

### MCP Server Trigger Configuration

**Basic Setup:**

1. **Create New Workflow** in n8n
2. **Add MCP Server Trigger** node as entry point
3. **Configure Tool Definition**:
   - **Tool Name**: Unique identifier (e.g., "create_support_ticket")
   - **Description**: Clear description for AI to understand when to use
   - **Parameters**: Define input schema (JSON Schema format)
   - **Authentication**: Optional authentication settings

4. **Build Workflow Logic**: Add nodes to process the request
5. **Return Response**: Last node output becomes MCP response

**MCP Server Trigger Parameters:**

```json
{
  "toolName": "create_support_ticket",
  "description": "Create a support ticket in Jira with automatic team notification",
  "parameters": {
    "type": "object",
    "properties": {
      "title": {
        "type": "string",
        "description": "Brief ticket title"
      },
      "description": {
        "type": "string",
        "description": "Detailed problem description"
      },
      "priority": {
        "type": "string",
        "enum": ["low", "medium", "high", "critical"],
        "description": "Ticket priority level"
      },
      "component": {
        "type": "string",
        "description": "System component affected"
      }
    },
    "required": ["title", "description"]
  }
}
```

### Response Format

The final node output in your workflow is returned to the AI agent:

```json
{
  "success": true,
  "ticketId": "JIRA-12345",
  "url": "https://company.atlassian.net/browse/JIRA-12345",
  "assignee": "john.doe@company.com",
  "createdAt": "2025-10-20T10:30:00Z"
}
```

### Authentication Patterns

**1. API Key Authentication**
```json
{
  "authenticationType": "apiKey",
  "apiKeyHeader": "X-API-Key",
  "requiredScopes": ["workflows:execute"]
}
```

**2. OAuth 2.0**
```json
{
  "authenticationType": "oauth2",
  "authorizationUrl": "https://auth.company.com/oauth/authorize",
  "tokenUrl": "https://auth.company.com/oauth/token",
  "scopes": ["workflows:read", "workflows:execute"]
}
```

**3. No Authentication** (internal use only)
```json
{
  "authenticationType": "none"
}
```

## n8n as MCP Client

### Consuming External MCP Servers

The MCP Client Tool node allows n8n workflows to call external MCP servers and use their tools.

**Architecture Pattern:**

```
┌─────────────────────────────────────────────────────────────────┐
│                    n8n Workflow                                 │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Schedule Trigger: Every day at 9am                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                          │                                      │
│                          ↓                                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ MCP Client Tool                                           │  │
│  │ Server: "analytics-mcp-server"                            │  │
│  │ Tool: "generate_daily_report"                             │  │
│  │ Params: {date: "today"}                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ↓ MCP Request
┌─────────────────────────────────────────────────────────────────┐
│                    External MCP Server                          │
│                    (Analytics Service)                          │
│                                                                 │
│  Processes request, generates report, returns data             │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ↓ MCP Response
┌─────────────────────────────────────────────────────────────────┐
│                    n8n Workflow (continued)                     │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Email: Send report to stakeholders                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### MCP Client Tool Configuration

**Basic Setup:**

1. **Add MCP Client Tool node** to workflow
2. **Configure MCP Server Connection**:
   - **Server URL**: MCP server endpoint
   - **Authentication**: API key, OAuth, or none
   - **Timeout**: Request timeout (default: 30s)

3. **Select Tool**: Choose from available tools on MCP server
4. **Provide Parameters**: Map workflow data to tool parameters
5. **Handle Response**: Process returned data in subsequent nodes

**MCP Client Tool Configuration:**

```json
{
  "serverUrl": "https://mcp.analytics-service.com",
  "authentication": {
    "type": "apiKey",
    "apiKey": "{{$credentials.analyticsApiKey}}"
  },
  "tool": "generate_daily_report",
  "parameters": {
    "date": "{{DateTime.now().toISODate()}}",
    "metrics": ["revenue", "users", "engagement"],
    "format": "json"
  },
  "timeout": 60000
}
```

### Discovering Available Tools

MCP servers expose their available tools through the protocol:

```json
{
  "tools": [
    {
      "name": "generate_daily_report",
      "description": "Generate daily analytics report",
      "parameters": {
        "type": "object",
        "properties": {
          "date": {"type": "string"},
          "metrics": {"type": "array"},
          "format": {"type": "string"}
        }
      }
    },
    {
      "name": "query_metrics",
      "description": "Query specific metrics",
      "parameters": {
        "type": "object",
        "properties": {
          "metric": {"type": "string"},
          "startDate": {"type": "string"},
          "endDate": {"type": "string"}
        }
      }
    }
  ]
}
```

## Claude Code Integration

### Connecting Claude Code to n8n Workflows

**Prerequisites:**
1. n8n instance running (self-hosted or cloud)
2. n8n workflow with MCP Server Trigger configured
3. Claude Code with MCP client capability

**Configuration Steps:**

**1. Create n8n MCP Server Workflow**

```
Workflow: "create_task"
┌──────────────────────────────────────┐
│ MCP Server Trigger                   │
│ Tool: create_task                    │
│ Params: title, description, due_date │
└──────────────────────────────────────┘
          ↓
┌──────────────────────────────────────┐
│ HTTP Request: POST to Todoist API    │
└──────────────────────────────────────┘
          ↓
┌──────────────────────────────────────┐
│ Return: Task created confirmation    │
└──────────────────────────────────────┘
```

**2. Get n8n MCP Server URL**

n8n exposes MCP servers at:
```
https://your-n8n-instance.com/mcp
```

**3. Configure Claude Code MCP Client**

Add to `mcp_config.json`:

```json
{
  "mcpServers": {
    "n8n-workflows": {
      "url": "https://your-n8n-instance.com/mcp",
      "apiKey": "your-n8n-api-key",
      "description": "n8n workflow automation tools",
      "tools": [
        "create_task",
        "send_email",
        "create_support_ticket",
        "generate_report"
      ]
    }
  }
}
```

**4. Use in Claude Code**

Claude Code automatically discovers and uses n8n tools:

```
User: "Create a task to review the PR tomorrow at 2pm"

Claude Code:
- Recognizes create_task tool from n8n
- Invokes: create_task(
    title="Review PR",
    description="Code review for authentication feature",
    due_date="2025-10-21T14:00:00Z"
  )
- n8n workflow executes
- Returns task confirmation
- Claude responds: "Task created in Todoist: Review PR (tomorrow at 2pm)"
```

### Bidirectional Claude Code ↔ n8n Integration

**Pattern 1: Claude triggers n8n workflow**
```
Claude Code → MCP Tool Call → n8n MCP Server → Workflow executes
```

**Pattern 2: n8n calls Claude via MCP**
```
n8n Workflow → MCP Client Tool → Claude API → AI processing → Response
```

**Combined Pattern: Agentic Workflow**
```
1. User asks Claude to analyze sales data
2. Claude calls n8n tool: get_sales_data()
3. n8n retrieves data from database
4. Claude analyzes data
5. Claude calls n8n tool: generate_report(analysis)
6. n8n creates PDF report and emails stakeholders
7. Claude confirms completion to user
```

## Agentic Workflow Patterns

### Pattern 1: Multi-Step Agent Workflow

**Scenario:** Customer support ticket processing

```
┌─────────────────────────────────────────────────────────────────┐
│ User: "Customer reports login issue"                            │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ Claude Code (Agent)                                             │
│ 1. Calls: create_support_ticket(issue_type="login")            │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ n8n Workflow 1: Create Ticket                                   │
│ - Create Jira ticket                                            │
│ - Notify support team in Slack                                  │
│ - Return ticket ID                                              │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ Claude Code (Agent)                                             │
│ 2. Calls: search_knowledge_base(query="login issues")          │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ n8n Workflow 2: Knowledge Search                                │
│ - Query internal docs                                           │
│ - Search past tickets                                           │
│ - Return relevant solutions                                     │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ Claude Code (Agent)                                             │
│ 3. Analyzes solutions                                           │
│ 4. Calls: update_ticket(id, suggested_solution)                │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ n8n Workflow 3: Update Ticket                                   │
│ - Update Jira with solution                                     │
│ - Auto-assign to engineer if complex                            │
│ - Send email to customer with workaround                        │
└─────────────────────────────────────────────────────────────────┘
```

### Pattern 2: Multi-Agent Orchestration

**Scenario:** Content creation pipeline with multiple specialized agents

```
┌─────────────────────────────────────────────────────────────────┐
│ Orchestrator Agent (Claude Code)                                │
│ "Create a blog post about our new feature"                      │
└─────────────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ↓                 ↓                 ↓
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Research     │  │ Writing      │  │ SEO          │
│ Agent        │  │ Agent        │  │ Agent        │
└──────────────┘  └──────────────┘  └──────────────┘
        │                 │                 │
        ↓ MCP             ↓ MCP             ↓ MCP
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ n8n: Gather  │  │ n8n: Generate│  │ n8n: Optimize│
│ data         │  │ content      │  │ for search   │
└──────────────┘  └──────────────┘  └──────────────┘
        │                 │                 │
        └─────────────────┼─────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ n8n: Publishing Workflow                                        │
│ - Format content                                                │
│ - Upload images to CDN                                          │
│ - Publish to CMS                                                │
│ - Share on social media                                         │
│ - Notify marketing team                                         │
└─────────────────────────────────────────────────────────────────┘
```

### Pattern 3: Autonomous Agent Loop

**Scenario:** Continuous monitoring and remediation

```
┌─────────────────────────────────────────────────────────────────┐
│ n8n: Monitoring Workflow (runs every 5 minutes)                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ 1. Check system health metrics                              │ │
│ │ 2. If anomaly detected → Trigger MCP call to Claude        │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ↓ Anomaly detected
┌─────────────────────────────────────────────────────────────────┐
│ Claude Code (Remediation Agent)                                 │
│ 1. Analyze metrics and logs                                     │
│ 2. Determine root cause                                         │
│ 3. Call: execute_remediation(action)                           │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ n8n: Remediation Workflow                                       │
│ - Restart service if needed                                     │
│ - Scale resources                                               │
│ - Clear cache                                                   │
│ - Create incident ticket                                        │
│ - Alert on-call engineer                                        │
│ - Return results                                                │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ Claude Code                                                     │
│ - Verify remediation successful                                 │
│ - Document incident                                             │
│ - Call: update_incident_log()                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Tool Composition and Chaining

### Pattern: Sequential Tool Calls

Build complex automations by chaining multiple MCP tool calls:

```javascript
// Claude Code orchestrates sequence
async function processCustomerOrder(orderId) {
  // Step 1: Get order details
  const order = await mcpCall('n8n', 'get_order', { orderId });

  // Step 2: Validate inventory
  const inventory = await mcpCall('n8n', 'check_inventory', {
    items: order.items
  });

  if (!inventory.available) {
    // Step 3a: Order out of stock items
    await mcpCall('n8n', 'create_purchase_order', {
      items: inventory.missing
    });

    // Step 3b: Notify customer of delay
    await mcpCall('n8n', 'send_email', {
      to: order.customerEmail,
      template: 'order_delayed',
      data: { estimatedDate: inventory.restockDate }
    });
  } else {
    // Step 3: Process payment
    const payment = await mcpCall('n8n', 'process_payment', {
      orderId,
      amount: order.total
    });

    // Step 4: Create shipment
    await mcpCall('n8n', 'create_shipment', {
      orderId,
      address: order.shippingAddress
    });

    // Step 5: Send confirmation
    await mcpCall('n8n', 'send_email', {
      to: order.customerEmail,
      template: 'order_confirmed',
      data: { trackingNumber: payment.trackingNumber }
    });
  }
}
```

### Pattern: Parallel Tool Execution

Execute multiple tools simultaneously for efficiency:

```javascript
// Claude Code executes in parallel
async function enrichCustomerProfile(customerId) {
  const [
    orders,
    supportTickets,
    socialData,
    emailEngagement
  ] = await Promise.all([
    mcpCall('n8n', 'get_customer_orders', { customerId }),
    mcpCall('n8n', 'get_support_history', { customerId }),
    mcpCall('n8n', 'get_social_data', { customerId }),
    mcpCall('n8n', 'get_email_metrics', { customerId })
  ]);

  // Combine all data
  const profile = {
    totalSpent: orders.reduce((sum, o) => sum + o.total, 0),
    supportIssues: supportTickets.length,
    sentimentScore: socialData.sentiment,
    emailEngagement: emailEngagement.averageClickRate
  };

  // Update CRM
  await mcpCall('n8n', 'update_crm', {
    customerId,
    profile
  });
}
```

## Resource Management

### Exposing Resources via MCP

Resources provide context to AI agents without requiring tool invocation.

**Resource Types:**
1. **Documents**: Markdown, text, PDFs
2. **Data**: JSON, CSV, structured data
3. **Context**: Configuration, metadata
4. **Templates**: Prompt templates, code snippets

**Example: Expose API Documentation as Resource**

```json
{
  "resources": [
    {
      "uri": "resource://api-docs/authentication",
      "name": "Authentication API Docs",
      "description": "Complete authentication API documentation",
      "mimeType": "text/markdown",
      "content": "# Authentication API\n\n## Endpoints\n\n### POST /auth/login..."
    },
    {
      "uri": "resource://api-docs/users",
      "name": "Users API Docs",
      "description": "User management API documentation",
      "mimeType": "text/markdown",
      "content": "# Users API\n\n## Endpoints\n\n### GET /users..."
    }
  ]
}
```

**n8n Workflow to Serve Resources:**

```
┌──────────────────────────────────────┐
│ MCP Server Trigger                   │
│ Resource: api-docs/*                 │
└──────────────────────────────────────┘
          ↓
┌──────────────────────────────────────┐
│ Switch: Route by resource URI        │
└──────────────────────────────────────┘
          ↓
┌──────────────────────────────────────┐
│ HTTP Request: Fetch from docs repo   │
└──────────────────────────────────────┘
          ↓
┌──────────────────────────────────────┐
│ Format and return markdown           │
└──────────────────────────────────────┘
```

### Using Resources in AI Workflows

Claude Code can read resources for context:

```
User: "How do I authenticate with the API?"

Claude Code:
1. Reads resource: resource://api-docs/authentication
2. Analyzes documentation
3. Provides answer with code examples
```

## Production Deployment

### Hosting n8n MCP Servers

**Deployment Options:**

**1. Self-Hosted n8n**
```yaml
# docker-compose.yml
version: '3.8'
services:
  n8n:
    image: n8nio/n8n:latest
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD}
      - N8N_MCP_ENABLED=true
      - N8N_MCP_PORT=8080
    volumes:
      - n8n_data:/home/node/.n8n
    restart: unless-stopped

volumes:
  n8n_data:
```

**2. n8n Cloud**
- Fully managed n8n hosting
- Built-in MCP support
- Automatic scaling
- SSL/TLS included

**3. Kubernetes Deployment**
```yaml
# n8n-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: n8n-mcp-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: n8n
  template:
    metadata:
      labels:
        app: n8n
    spec:
      containers:
      - name: n8n
        image: n8nio/n8n:latest
        ports:
        - containerPort: 5678
          name: http
        - containerPort: 8080
          name: mcp
        env:
        - name: N8N_MCP_ENABLED
          value: "true"
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
```

### Security Best Practices

**1. Authentication**
```json
{
  "mcp": {
    "authentication": {
      "type": "oauth2",
      "provider": "okta",
      "clientId": "${OAUTH_CLIENT_ID}",
      "clientSecret": "${OAUTH_CLIENT_SECRET}",
      "authorizationUrl": "https://company.okta.com/oauth2/v1/authorize",
      "tokenUrl": "https://company.okta.com/oauth2/v1/token"
    }
  }
}
```

**2. Rate Limiting**
```json
{
  "mcp": {
    "rateLimiting": {
      "enabled": true,
      "maxRequests": 100,
      "windowMs": 60000,
      "message": "Too many requests, please try again later"
    }
  }
}
```

**3. IP Whitelisting**
```json
{
  "mcp": {
    "ipWhitelist": [
      "10.0.0.0/8",
      "172.16.0.0/12",
      "192.168.1.100"
    ]
  }
}
```

**4. HTTPS Only**
```nginx
# nginx.conf
server {
    listen 443 ssl http2;
    server_name mcp.company.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    location / {
        proxy_pass http://n8n:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Monitoring and Debugging

**Workflow Execution Logging:**

```javascript
// Add to n8n workflow
{
  "nodes": [
    {
      "name": "Log MCP Request",
      "type": "n8n-nodes-base.function",
      "parameters": {
        "functionCode": `
          const mcpRequest = $input.item.json;

          console.log('MCP Tool Invoked:', {
            tool: mcpRequest.tool,
            parameters: mcpRequest.parameters,
            timestamp: new Date().toISOString(),
            clientId: mcpRequest.clientId
          });

          return { json: mcpRequest };
        `
      }
    }
  ]
}
```

**Error Handling:**

```javascript
// MCP error response format
{
  "error": {
    "code": "INVALID_PARAMETERS",
    "message": "Missing required parameter: customerId",
    "details": {
      "parameter": "customerId",
      "expected": "string",
      "received": "undefined"
    }
  }
}
```

**Monitoring Metrics:**

```yaml
# Prometheus metrics for n8n MCP
metrics:
  - mcp_tool_invocations_total
  - mcp_tool_execution_duration_seconds
  - mcp_tool_errors_total
  - mcp_active_connections
  - mcp_requests_per_second
```

## Best Practices

### MCP Server Design

1. **Clear Tool Names**: Use verb-noun format (create_ticket, get_user)
2. **Comprehensive Descriptions**: Help AI understand when to use each tool
3. **Validate Parameters**: Always validate input parameters
4. **Return Structured Data**: Use consistent JSON response formats
5. **Handle Errors Gracefully**: Return meaningful error messages
6. **Version Your Tools**: Support versioning for breaking changes
7. **Document Everything**: Provide examples and usage guides

### MCP Client Usage

1. **Connection Pooling**: Reuse MCP client connections
2. **Timeout Configuration**: Set appropriate timeouts
3. **Retry Logic**: Implement exponential backoff
4. **Error Handling**: Catch and handle MCP errors
5. **Cache Responses**: Cache expensive tool calls when appropriate
6. **Parallel Execution**: Use Promise.all for independent calls
7. **Logging**: Log all MCP interactions for debugging

### Workflow Optimization

1. **Minimize Tool Calls**: Batch operations when possible
2. **Use Webhooks**: For long-running operations
3. **Async Patterns**: Don't block on slow operations
4. **Resource Limits**: Set memory and CPU limits
5. **Monitoring**: Track execution times and errors
6. **Testing**: Test MCP tools independently
7. **Documentation**: Keep tool documentation up-to-date

### Security Guidelines

1. **Authentication**: Always require authentication in production
2. **Authorization**: Implement role-based access control
3. **Input Validation**: Sanitize all inputs
4. **Rate Limiting**: Prevent abuse
5. **Audit Logging**: Log all tool invocations
6. **Secrets Management**: Use environment variables
7. **HTTPS**: Always use TLS in production

## Troubleshooting

### Common Issues

**Tool Not Appearing in Claude Code**

Possible causes:
- MCP server not registered in mcp_config.json
- Tool description missing or unclear
- Authentication failure
- n8n workflow not activated

Solution:
1. Verify MCP server URL is correct
2. Check authentication credentials
3. Ensure workflow is active in n8n
4. Restart Claude Code to refresh tool list

**MCP Tool Invocation Fails**

Possible causes:
- Invalid parameters
- Timeout
- n8n workflow error
- Authentication expired

Solution:
1. Check parameter types match schema
2. Increase timeout in configuration
3. Review n8n workflow execution logs
4. Refresh authentication token

**Slow Tool Execution**

Possible causes:
- Complex workflow
- External API delays
- Database queries
- Network latency

Solution:
1. Optimize workflow logic
2. Add caching for repeated queries
3. Use async patterns
4. Scale n8n instances

**Authentication Errors**

Possible causes:
- Expired API key
- Wrong credentials
- IP not whitelisted
- OAuth token expired

Solution:
1. Regenerate API key
2. Verify credentials in configuration
3. Add IP to whitelist
4. Refresh OAuth token

## Advanced Patterns

### Pattern: Event-Driven Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│ External System (e.g., Stripe)                                  │
│ Event: payment_succeeded                                        │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ↓ Webhook
┌─────────────────────────────────────────────────────────────────┐
│ n8n: Webhook Trigger                                            │
│ 1. Receive payment event                                        │
│ 2. Call MCP: analyze_payment_risk()                            │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ↓ MCP Call
┌─────────────────────────────────────────────────────────────────┐
│ Claude Code (Risk Analysis Agent)                               │
│ - Analyze transaction pattern                                   │
│ - Check customer history                                        │
│ - Assess fraud risk                                             │
│ - Return risk score                                             │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ n8n: Risk-Based Routing                                         │
│ IF risk_score > 0.7:                                            │
│   - Flag for manual review                                      │
│   - Notify fraud team                                           │
│ ELSE:                                                           │
│   - Auto-approve                                                │
│   - Trigger fulfillment                                         │
└─────────────────────────────────────────────────────────────────┘
```

### Pattern: Human-in-the-Loop

```
┌─────────────────────────────────────────────────────────────────┐
│ Claude Code: Draft email response                               │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ↓ Call MCP tool
┌─────────────────────────────────────────────────────────────────┐
│ n8n: request_human_approval(draft)                              │
│ 1. Send draft to manager via Slack                              │
│ 2. Wait for approval (webhook)                                  │
│ 3. Return approval status                                       │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ↓ Approval received
┌─────────────────────────────────────────────────────────────────┐
│ Claude Code: Send approved email                                │
│ Call: send_email(approved_draft)                               │
└─────────────────────────────────────────────────────────────────┘
```

### Pattern: Multi-Modal Processing

```
┌─────────────────────────────────────────────────────────────────┐
│ User uploads image to chat                                      │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ Claude Code: Analyze image                                      │
│ - Extract text (OCR)                                            │
│ - Detect objects                                                │
│ - Identify action items                                         │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ↓ For each action item
┌─────────────────────────────────────────────────────────────────┐
│ n8n MCP Tools:                                                  │
│ - create_task(item)                                             │
│ - send_notification(team)                                       │
│ - update_dashboard(metrics)                                     │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Reference

### Essential n8n MCP Nodes

**MCP Server Trigger**
- Exposes workflow as AI-callable tool
- Define tool name, description, parameters
- Returns workflow output to AI client

**MCP Client Tool**
- Calls external MCP servers
- Specify server URL and tool name
- Pass parameters and handle response

### Common Tool Patterns

**Create Resource**
```json
{
  "tool": "create_resource",
  "parameters": {
    "type": "string",
    "data": "object"
  },
  "returns": {
    "id": "string",
    "status": "string"
  }
}
```

**Update Resource**
```json
{
  "tool": "update_resource",
  "parameters": {
    "id": "string",
    "updates": "object"
  },
  "returns": {
    "success": "boolean",
    "resource": "object"
  }
}
```

**Query Data**
```json
{
  "tool": "query_data",
  "parameters": {
    "filters": "object",
    "limit": "number"
  },
  "returns": {
    "data": "array",
    "total": "number"
  }
}
```

## Resources

- n8n Documentation: https://docs.n8n.io
- MCP Specification: https://modelcontextprotocol.io
- n8n MCP Nodes Guide: https://docs.n8n.io/integrations/builtin/core-nodes/mcp/
- Claude Code MCP Integration: https://docs.anthropic.com/claude/docs/mcp
- n8n Community: https://community.n8n.io
- MCP Examples Repository: https://github.com/anthropics/model-context-protocol

---

**Skill Version**: 1.0.0
**Last Updated**: October 2025
**Skill Category**: AI Orchestration, Workflow Automation, MCP Integration
**Compatible With**: n8n, Claude Code, Claude Desktop, MCP Protocol
