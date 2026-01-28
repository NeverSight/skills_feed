---
name: n8n-workflow-builder
description: Build n8n automation workflows using MCP tools. Use when creating workflows, configuring nodes, validating configurations, deploying templates, or integrating n8n with Rails apps. Supports Israeli market (Hebrew, WhatsApp Business, NIS payments).
---

# n8n Workflow Builder

Build production-ready n8n workflows using the available MCP tools.

## MCP Tool Decision Tree

### Discovery Phase
| Need | Tool | Example |
|------|------|---------|
| Find a node | `search_nodes` | `search_nodes({query: "slack"})` |
| Find workflow templates | `search_templates` | `search_templates({searchMode: "by_task", task: "ai_automation"})` |
| Find templates using specific nodes | `search_templates` | `search_templates({searchMode: "by_nodes", nodeTypes: ["n8n-nodes-base.slack"]})` |
| Get a specific template | `get_template` | `get_template({templateId: 123, mode: "full"})` |

### Configuration Phase
| Need | Tool | Example |
|------|------|---------|
| How to configure a node | `get_node` | `get_node({nodeType: "nodes-base.httpRequest", detail: "standard"})` |
| Node documentation | `get_node` | `get_node({nodeType: "nodes-base.slack", mode: "docs"})` |
| Find specific property | `get_node` | `get_node({nodeType: "...", mode: "search_properties", propertyQuery: "auth"})` |
| Real-world examples | `get_node` | `get_node({..., detail: "standard", includeExamples: true})` |

### Validation Phase
| Need | Tool | Example |
|------|------|---------|
| Validate node config | `validate_node` | `validate_node({nodeType: "...", config: {...}, mode: "full"})` |
| Validate full workflow | `validate_workflow` | `validate_workflow({workflow: {...}})` |

### Deployment Phase (requires API)
| Need | Tool |
|------|------|
| Create workflow | `n8n_create_workflow` |
| Update workflow | `n8n_update_partial_workflow` |
| Deploy template | `n8n_deploy_template` |
| Test workflow | `n8n_test_workflow` |
| Get execution results | `n8n_executions` |

## Common Workflow Patterns

### Pattern 1: Webhook -> Process -> Respond
```
Webhook -> Code (validate) -> HTTP Request -> Respond
```
Template: `assets/templates/workflows/webhook-processor.json`

### Pattern 2: Lead Capture -> CRM -> Notify
```
Webhook -> IF (validate) -> CRM -> Slack -> Rails callback
```
Template: `assets/templates/workflows/lead-capture-crm.json`

### Pattern 3: AI Agent with Tools
```
Chat Trigger -> AI Agent <- OpenAI Model
                   ^
                   |- HTTP Request Tool
                   |- Code Tool
```
Template: `assets/templates/workflows/ai-agent-basic.json`

### Pattern 4: WhatsApp Bot (Israeli Market)
```
Webhook -> Code (parse) -> Switch (msg type) -> HTTP Request (WhatsApp API)
```
Template: `assets/templates/workflows/whatsapp-bot.json`

### Pattern 5: Scheduled Reports
```
Schedule Trigger -> HTTP (fetch data) -> Code (format) -> Email/Slack
```
Template: `assets/templates/workflows/scheduled-report.json`

### Pattern 6: Rails Integration
```
Rails App -> Webhook -> Process -> HTTP (callback to Rails)
```
Template: `assets/templates/workflows/rails-webhook-handler.json`

## MCP Tool Usage Examples

### search_nodes - Finding Nodes
```javascript
// Find database nodes
search_nodes({query: "database"})

// Fuzzy search (typo-tolerant)
search_nodes({query: "slak", mode: "FUZZY"})

// With real examples
search_nodes({query: "webhook", includeExamples: true})
```

### get_node - Node Configuration
```javascript
// Standard detail (recommended starting point)
get_node({nodeType: "nodes-base.httpRequest", detail: "standard"})

// With real-world examples
get_node({nodeType: "nodes-base.slack", detail: "standard", includeExamples: true})

// Documentation mode
get_node({nodeType: "nodes-base.webhook", mode: "docs"})

// Search specific properties
get_node({nodeType: "nodes-base.httpRequest", mode: "search_properties", propertyQuery: "header"})

// Version comparison
get_node({nodeType: "nodes-base.httpRequest", mode: "compare", fromVersion: "1.0", toVersion: "2.0"})
```

### validate_node - Pre-build Validation
```javascript
// Full validation with suggestions
validate_node({
  nodeType: "nodes-base.slack",
  config: {resource: "channel", operation: "create"},
  mode: "full",
  profile: "strict"
})

// Quick check
validate_node({
  nodeType: "nodes-base.httpRequest",
  config: {method: "POST", url: "https://api.example.com"},
  mode: "minimal"
})
```

### validate_workflow - Full Workflow Validation
```javascript
validate_workflow({
  workflow: myWorkflowJson,
  options: {
    validateNodes: true,
    validateConnections: true,
    validateExpressions: true,
    profile: "strict"
  }
})
```

### search_templates - Finding Templates
```javascript
// By task type
search_templates({searchMode: "by_task", task: "ai_automation"})
search_templates({searchMode: "by_task", task: "webhook_processing"})

// By nodes used
search_templates({searchMode: "by_nodes", nodeTypes: ["n8n-nodes-base.openAi", "n8n-nodes-langchain.agent"]})

// By complexity
search_templates({searchMode: "by_metadata", complexity: "simple", maxSetupMinutes: 15})

// Keyword search
search_templates({query: "slack notification"})
```

## AI Agent Workflows

### Connection Types (CRITICAL)
AI connections flow TO the consumer node:
| Connection Type | From | To | Purpose |
|----------------|------|------|---------|
| `ai_languageModel` | Language Model | AI Agent | REQUIRED - provides LLM |
| `ai_tool` | Tool Node | AI Agent | Gives agent capabilities |
| `ai_memory` | Memory Node | AI Agent | Conversation history |
| `ai_outputParser` | Parser | Chain | Structured output |

### Minimal AI Agent Setup
1. Add **Chat Trigger** (or Manual Trigger)
2. Add **Language Model** (OpenAI Chat Model / Anthropic)
3. Add **AI Agent**
4. Connect: `Chat Trigger -> AI Agent` (main connection)
5. Connect: `Language Model -> AI Agent` (ai_languageModel type)

### Adding Tools to Agent
```javascript
// HTTP Request Tool - for API calls
{
  "name": "Call API Tool",
  "type": "@n8n/n8n-nodes-langchain.toolHttpRequest",
  "parameters": {
    "description": "Calls external API to fetch data"  // REQUIRED: 15+ chars
  }
}
// Connect: HTTP Tool -> AI Agent (ai_tool type)
```

### Tool Description Requirements
- Minimum 15 characters
- Must clearly describe what the tool does
- Agent uses this to decide when to use the tool

See `references/ai-agents-guide.md` for advanced patterns.

## Israeli Market Integration

### WhatsApp Business API
```javascript
// Send text message
{
  "method": "POST",
  "url": "https://graph.facebook.com/v18.0/{{PHONE_ID}}/messages",
  "headers": {"Authorization": "Bearer {{ACCESS_TOKEN}}"},
  "body": {
    "messaging_product": "whatsapp",
    "to": "972501234567",
    "type": "text",
    "text": {"body": "\u200F" + hebrewText}  // RTL marker for Hebrew
  }
}
```

### Hebrew RTL Handling
```javascript
// Add RTL marker for Hebrew text
const rtlText = "\u200F" + hebrewContent;  // Right-to-Left Mark

// Mixed content
const mixed = `\u200F${hebrewPart}\u200E${englishPart}`;  // LTR mark for English
```

### Rate Limits by Tier
| Tier | Messages/day | Messages/sec |
|------|--------------|--------------|
| Unverified | 250 | 80 |
| Verified | 1,000 | 80 |
| Business | 10,000+ | 80 |

See `references/israeli-market-integrations.md` for WhatsApp templates and payment patterns.

## Rails Integration

### Triggering n8n from Rails
```ruby
# app/services/n8n_service.rb
def trigger_webhook(webhook_url, payload)
  HTTParty.post(webhook_url, {
    body: payload.to_json,
    headers: {'Content-Type' => 'application/json', 'X-Webhook-Secret' => ENV['N8N_SECRET']}
  })
end
```

### Receiving n8n Callbacks
```ruby
# Verify signature
signature = request.headers['X-N8N-Signature']
expected = OpenSSL::HMAC.hexdigest('sha256', ENV['N8N_SECRET'], request.raw_post)
unless ActiveSupport::SecurityUtils.secure_compare(signature.to_s, expected)
  render json: {error: 'Unauthorized'}, status: 401
end
```

### Selling Automations
- Automation model with `workflow_json`, `price`, `demo_webhook_url`
- Purchase model with Stripe integration
- Delivery: JSON download, hosted deploy, or embedded viewer

See `references/rails-integration-patterns.md` for full implementation.

## Validation Checklist

### Before Building
- [ ] Run `search_nodes` to find correct node type
- [ ] Run `get_node` with `detail: "standard"` to understand config
- [ ] Check for required credentials

### Node Level
- [ ] `validate_node({..., mode: "full"})` passes
- [ ] All required fields populated
- [ ] Credentials configured (not hardcoded)
- [ ] Error handling configured

### Workflow Level
- [ ] `validate_workflow({...})` passes
- [ ] All nodes connected (no orphans)
- [ ] Error Trigger node present
- [ ] Webhook paths unique

### AI Workflows
- [ ] Language model connected BEFORE AI Agent
- [ ] All tools have descriptions (15+ chars)
- [ ] Memory node if conversation history needed
- [ ] Streaming: no main outputs from AI Agent

### Pre-Deployment
- [ ] Test with sample data
- [ ] Environment variables for sensitive data
- [ ] Rate limiting considered

## Workflow JSON Structure

```json
{
  "name": "Workflow Name",
  "nodes": [
    {
      "id": "uuid",
      "name": "Node Name",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [250, 300],
      "parameters": {}
    }
  ],
  "connections": {
    "Node Name": {
      "main": [[{"node": "Next Node", "type": "main", "index": 0}]]
    }
  },
  "settings": {
    "executionOrder": "v1"
  }
}
```

## Scripts

### Validate Before Deploy
```bash
python scripts/validate_before_deploy.py workflow.json
```

### Generate Workflow Skeleton
```bash
python scripts/generate_workflow_skeleton.py --type webhook --name "My Workflow"
python scripts/generate_workflow_skeleton.py --type ai-agent --name "Support Bot"
```

## References

| Topic | File |
|-------|------|
| MCP Tools (all 19) | `references/mcp-tools-guide.md` |
| AI Agent Patterns | `references/ai-agents-guide.md` |
| Rails Integration | `references/rails-integration-patterns.md` |
| Israeli Market | `references/israeli-market-integrations.md` |
| Node Configs | `references/node-configuration-patterns.md` |
| Code Patterns | `references/code-node-patterns.md` |
| Validation | `references/validation-checklist.md` |

## Templates

### Workflows
- `assets/templates/workflows/webhook-processor.json`
- `assets/templates/workflows/lead-capture-crm.json`
- `assets/templates/workflows/whatsapp-bot.json`
- `assets/templates/workflows/ai-agent-basic.json`
- `assets/templates/workflows/scheduled-report.json`
- `assets/templates/workflows/rails-webhook-handler.json`

### Nodes
- `assets/templates/nodes/webhook-trigger.json`
- `assets/templates/nodes/http-request-auth.json`
- `assets/templates/nodes/code-transform.json`
- `assets/templates/nodes/if-conditions.json`
- `assets/templates/nodes/error-handler.json`

### Israeli Market
- `assets/templates/israel/whatsapp-message-types.json`
- `assets/templates/israel/hebrew-templates.json`
- `assets/templates/israel/payment-webhook.json`
