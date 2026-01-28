---
name: mcp-client-builder
description: Build production-ready MCP clients in TypeScript or Python. Handles connection lifecycle, transport abstraction, tool orchestration, security, and error handling. Use for integrating LLM applications with MCP servers.
license: Apache License 2.0 (see LICENSE.txt)
---

# MCP Client Development Guide

## Core Mental Model

```
Host Application (user-facing app like Claude Desktop)
  └─> Creates 1+ MCP Clients (protocol components)
       └─> Each Client connects to exactly 1 Server (1:1 mapping)
            └─> Server exposes Tools/Resources/Prompts
                 └─> LLM decides which to use
                      └─> Client executes, returns results
```

**Key Principle**: Client = stateful messenger, NOT decision maker. LLM chooses tools, client facilitates execution.

---

# Development Workflow

## Phase 1: Architecture Design

### 1.1 Determine Requirements

**Client Capabilities** (what client provides TO servers):
- [ ] `sampling` - Allow server to request LLM completions
- [ ] `roots` - Declare filesystem boundaries
- [ ] `elicitation` - Allow server to request user input

**Expected Server Capabilities** (what servers provide TO client):
- [ ] `tools` - Execute operations
- [ ] `resources` - Access data
- [ ] `prompts` - Use templates

### 1.2 Select Transport Strategy

| Transport | Use When | Pros | Cons |
|-----------|----------|------|------|
| **stdio** | Server on same machine | Fast, simple | Local only |
| **HTTP Stream** | Remote server, modern | Bidirectional, sessions | More complex |
| **SSE** | Legacy compatibility | Simple | Unidirectional |

**Decision Rule**: stdio for local development/testing, HTTP Stream for production remote servers.

### 1.3 Plan Connection Management

**1:1 Mapping Pattern**:
```typescript
// CORRECT: One client per server
const weatherClient = new Client(/* weather server config */);
const calendarClient = new Client(/* calendar server config */);

// INCORRECT: One client trying to talk to multiple servers
const multiClient = new Client(/* won't work */);
```

**Host Manages Multiple Clients**:
```typescript
class HostApplication {
  private clients: Map<string, Client> = new Map();

  connectToServer(serverConfig) {
    const client = new Client(config);
    this.clients.set(serverConfig.id, client);
  }
}
```

---

## Phase 2: Implementation

### 2.1 Project Structure

**TypeScript**:
```
src/
  client.ts          # Main Client class
  transports/        # stdio, http, sse implementations
  types.ts           # Zod schemas
  errors.ts          # Error handling
  session.ts         # Session management
```

**Python**:
```
client.py            # Main Client class
transports/          # stdio, http, sse
schemas.py           # Pydantic models
errors.py            # Error handling
session.py           # Session management
```

### 2.2 Connection Lifecycle Implementation

**Three-Phase Pattern**:

```typescript
// Phase 1: Initialize
async connect(transport: Transport) {
  await transport.connect();

  const initResponse = await this.sendRequest({
    method: "initialize",
    params: {
      protocolVersion: "2025-06-18",
      capabilities: {
        sampling: {},          // If client supports sampling
        roots: { listChanged: true },  // If client supports roots
        elicitation: {}        // If client supports elicitation
      },
      clientInfo: { name: "my-client", version: "1.0.0" }
    }
  });

  this.serverCapabilities = initResponse.capabilities;

  // Phase 2: Confirm
  await this.sendNotification({ method: "initialized" });

  // Phase 3: Ready for operations
}
```

**Server Capabilities Extraction**:
```typescript
interface ServerCapabilities {
  tools?: { listChanged?: boolean };
  resources?: { subscribe?: boolean, listChanged?: boolean };
  prompts?: { listChanged?: boolean };
  logging?: {};
}
```

### 2.3 Transport Abstraction

**Interface Pattern**:
```typescript
interface Transport {
  connect(): Promise<void>;
  send(message: JSONRPCMessage): Promise<void>;
  receive(): AsyncIterator<JSONRPCMessage>;
  close(): Promise<void>;
}

class StdioTransport implements Transport { /* ... */ }
class HTTPStreamTransport implements Transport { /* ... */ }
class SSETransport implements Transport { /* ... */ }
```

**Usage**:
```typescript
const transport = config.remote
  ? new HTTPStreamTransport(config.url)
  : new StdioTransport(config.command, config.args);

await client.connect(transport);
```

### 2.4 Tool Orchestration Pattern

**Critical: LLM Decides, Client Executes**:

```typescript
async processUserQuery(query: string): Promise<string> {
  // 1. Get available tools from server
  const toolsResponse = await this.request({ method: "tools/list" });
  const tools = toolsResponse.tools;

  // 2. Present tools to LLM in structured format
  const llmTools = tools.map(tool => ({
    name: tool.name,
    description: tool.description,
    input_schema: tool.inputSchema
  }));

  // 3. LLM DECIDES which tools to use
  const llmResponse = await anthropic.messages.create({
    model: "claude-3-5-sonnet-20241022",
    messages: [{ role: "user", content: query }],
    tools: llmTools  // LLM sees available tools
  });

  // 4. Execute LLM-requested tool calls
  for (const toolUse of llmResponse.content) {
    if (toolUse.type === 'tool_use') {
      const result = await this.request({
        method: "tools/call",
        params: {
          name: toolUse.name,
          arguments: toolUse.input
        }
      });

      // 5. Return results to LLM for final response
      // ... continuation logic
    }
  }
}
```

**Key Point**: Client never chooses tools. Client only:
1. Discovers available tools
2. Presents them to LLM
3. Executes LLM's choices
4. Returns results to LLM

### 2.5 Error Handling Strategy

**JSON-RPC Error Codes**:
```typescript
enum ErrorCode {
  ParseError = -32700,      // Invalid JSON
  InvalidRequest = -32600,  // Malformed request
  MethodNotFound = -32601,  // Tool doesn't exist
  InvalidParams = -32602,   // Wrong arguments
  InternalError = -32603,   // Server failure

  // Custom range: -32000 to -32099
  Timeout = -32001,
  ResourceNotFound = -32002,
  Unauthorized = -32003
}
```

**Error Classification & Retry Logic**:
```typescript
class ErrorHandler {
  async handleError(error: JSONRPCError): Promise<'retry' | 'fail' | 'escalate'> {
    // Transient errors: retry with exponential backoff
    if ([ErrorCode.InternalError, ErrorCode.Timeout].includes(error.code)) {
      return 'retry';
    }

    // Permanent errors: fail immediately
    if ([ErrorCode.MethodNotFound, ErrorCode.InvalidParams].includes(error.code)) {
      return 'fail';
    }

    // Security errors: escalate to user
    if (error.code === ErrorCode.Unauthorized) {
      return 'escalate';
    }
  }
}
```

**Retry Pattern**:
```typescript
async executeWithRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
  baseDelay = 1000
): Promise<T> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      const action = await this.errorHandler.handleError(error);

      if (action === 'retry' && attempt < maxRetries - 1) {
        await sleep(baseDelay * Math.pow(2, attempt));
        continue;
      }
      throw error;
    }
  }
}
```

### 2.6 Session Management (HTTP Transport)

**Session ID Propagation**:
```typescript
class HTTPStreamTransport {
  private sessionId?: string;

  async send(message: JSONRPCMessage) {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json'
    };

    // Propagate session ID bidirectionally
    if (this.sessionId) {
      headers['Mcp-Session-Id'] = this.sessionId;
    }

    const response = await fetch(this.url, {
      method: 'POST',
      headers,
      body: JSON.stringify(message)
    });

    // Extract session ID from response
    const receivedSessionId = response.headers.get('Mcp-Session-Id');
    if (receivedSessionId) {
      this.sessionId = receivedSessionId;
    }
  }
}
```

**Session State Management**:
```typescript
interface SessionState {
  id: string;
  lastActivity: Date;
  conversationHistory: Message[];
  resources: Map<string, ResourceState>;
}
```

---

## Phase 3: Security Implementation

### 3.1 Multi-Layer Defense

**Layer 1: Network Security**:
```typescript
class SecureTransport {
  validateTLS(url: string) {
    if (!url.startsWith('https://') && !this.isLocalhost(url)) {
      throw new Error('Remote servers must use HTTPS');
    }
  }

  validateOrigin(origin: string) {
    // DNS rebinding protection
    if (!this.allowedOrigins.includes(origin)) {
      throw new Error(`Untrusted origin: ${origin}`);
    }
  }
}
```

**Layer 2: Authentication**:
```typescript
interface AuthProvider {
  authenticate(): Promise<Credentials>;
  refresh(credentials: Credentials): Promise<Credentials>;
}

class OAuth2PKCEProvider implements AuthProvider {
  async authenticate(): Promise<Credentials> {
    const codeVerifier = generateCodeVerifier();
    const codeChallenge = await generateCodeChallenge(codeVerifier);

    // OAuth 2.1 with PKCE flow
    const authUrl = buildAuthUrl({ challenge: codeChallenge });
    const code = await getUserConsent(authUrl);

    return await exchangeCodeForToken(code, codeVerifier);
  }
}
```

**Layer 3: Authorization**:
```typescript
class AuthorizationManager {
  async checkPermissions(toolName: string, params: any): Promise<boolean> {
    const tool = await this.getToolMetadata(toolName);

    // Destructive operations require explicit user consent
    if (tool.destructiveHint === true) {
      return await this.requestUserApproval(
        `Allow ${toolName}? This will modify data.`
      );
    }

    // Check scopes
    const requiredScopes = tool.requiredScopes || [];
    return this.hasScopes(requiredScopes);
  }
}
```

**Layer 4: Validation**:
```typescript
async callTool(name: string, args: unknown) {
  // 1. Schema validation
  const tool = await this.getTool(name);
  const validatedArgs = tool.inputSchema.parse(args);  // Zod/Pydantic

  // 2. Sanitization
  const sanitized = sanitizeInputs(validatedArgs);

  // 3. Authorization check
  const authorized = await this.authz.checkPermissions(name, sanitized);
  if (!authorized) throw new UnauthorizedError();

  // 4. Execute
  return await this.executeToolCall(name, sanitized);
}
```

### 3.2 Credential Management

**NEVER**:
```typescript
// ❌ WRONG: Hardcoded credentials
const client = new Client({ apiKey: "sk-1234..." });

// ❌ WRONG: Environment variables (visible to process)
const client = new Client({ apiKey: process.env.API_KEY });
```

**ALWAYS**:
```typescript
// ✅ CORRECT: OS keychain
import { getSecret } from '@keychain/secure-store';
const apiKey = await getSecret('mcp-server-credentials');

// ✅ CORRECT: Vault service
const credentials = await vault.getCredentials('mcp-server');
```

---

## Phase 4: Performance & Optimization

### 4.1 Token Efficiency (Primary Goal)

**Problem**: Every token in tool I/O consumes LLM context window.

**Solution Pattern**:
```typescript
interface ToolResponse {
  format: 'concise' | 'detailed';  // Let LLM choose
}

async executeTool(name: string, args: { format?: string }) {
  const result = await this.server.callTool(name, args);

  // Default to concise
  if (args.format !== 'detailed') {
    return this.truncateResponse(result, MAX_TOKENS);
  }

  return result;
}

private truncateResponse(data: any, maxTokens: number): any {
  // Remove low-signal fields
  const { id, timestamp, metadata, ...essential } = data;

  // Truncate arrays
  if (Array.isArray(essential.items)) {
    essential.items = essential.items.slice(0, 10);
    essential.truncated = true;
  }

  return essential;
}
```

**Server Response Design**:
```typescript
// ❌ BAD: Verbose response
{
  "temperature": 72.5,
  "temperature_unit": "fahrenheit",
  "humidity": 65,
  "humidity_unit": "percentage",
  "wind_speed": 5,
  "wind_speed_unit": "mph",
  "wind_direction": "N",
  "pressure": 1013,
  "pressure_unit": "mb",
  // ... 20 more fields
}

// ✅ GOOD: Concise response
{
  "temp": "72°F",
  "conditions": "cloudy",
  "wind": "5mph N"
}
```

### 4.2 Connection Pooling

**For Database-Backed Servers**:
```typescript
class ConnectionPool {
  private pool: Connection[] = [];
  private maxSize = 10;

  async acquire(): Promise<Connection> {
    if (this.pool.length > 0) {
      return this.pool.pop()!;
    }

    if (this.activeConnections < this.maxSize) {
      return await this.createConnection();
    }

    // Wait for available connection
    return await this.waitForConnection();
  }

  release(conn: Connection) {
    this.pool.push(conn);
  }
}
```

### 4.3 Request Queuing

**Handle Burst Traffic**:
```typescript
class RequestQueue {
  private queue: PendingRequest[] = [];
  private processing = 0;
  private maxConcurrent = 5;

  async enqueue(request: Request): Promise<Response> {
    return new Promise((resolve, reject) => {
      this.queue.push({ request, resolve, reject });
      this.processQueue();
    });
  }

  private async processQueue() {
    while (this.queue.length > 0 && this.processing < this.maxConcurrent) {
      const { request, resolve, reject } = this.queue.shift()!;
      this.processing++;

      try {
        const result = await this.executeRequest(request);
        resolve(result);
      } catch (error) {
        reject(error);
      } finally {
        this.processing--;
        this.processQueue();
      }
    }
  }
}
```

---

## Phase 5: Testing & Validation

### 5.1 Use MCP Inspector

```bash
npx @modelcontextprotocol/inspector <server-command>
# UI: http://localhost:5173
# Proxy: http://localhost:3000
```

**Validation Checklist**:
- [ ] Connection establishes successfully
- [ ] Capabilities negotiated correctly
- [ ] Tools discovered and listed
- [ ] Tool calls execute and return results
- [ ] Errors display meaningful messages
- [ ] Session IDs propagate (HTTP transport)
- [ ] OAuth flow completes (if applicable)

### 5.2 Automated Testing

**Technical Tests** (fast, comprehensive):
```typescript
describe('Client', () => {
  it('negotiates capabilities', async () => {
    const client = new Client({ capabilities: { sampling: {} } });
    await client.connect(mockTransport);

    expect(client.serverCapabilities).toBeDefined();
  });

  it('handles tool calls', async () => {
    const result = await client.callTool('test_tool', { arg: 'value' });
    expect(result.content).toBeDefined();
  });

  it('retries on transient errors', async () => {
    mockTransport.failTimes(2);  // Fail twice, then succeed
    const result = await client.callTool('flaky_tool', {});
    expect(result).toBeDefined();
  });
});
```

**Behavioral Tests** (with real LLM):
```typescript
describe('Client with LLM', () => {
  it('LLM can discover and use tools', async () => {
    const query = "What's the weather in Tokyo?";
    const response = await client.processQuery(query);

    expect(response).toContain('Tokyo');
    expect(response).toMatch(/\d+°[FC]/);  // Contains temperature
  });
});
```

---

## Reference Architecture

### Recommended Client Structure

```typescript
class MCPClient {
  private transport: Transport;
  private session: SessionManager;
  private auth: AuthProvider;
  private authz: AuthorizationManager;
  private errorHandler: ErrorHandler;
  private requestQueue: RequestQueue;

  // Core protocol methods
  async connect(transport: Transport): Promise<void> { /* ... */ }
  async listTools(): Promise<Tool[]> { /* ... */ }
  async callTool(name: string, args: any): Promise<ToolResult> { /* ... */ }
  async listResources(): Promise<Resource[]> { /* ... */ }
  async readResource(uri: string): Promise<ResourceContent> { /* ... */ }
  async listPrompts(): Promise<Prompt[]> { /* ... */ }
  async getPrompt(name: string, args: any): Promise<PromptContent> { /* ... */ }

  // Client capability implementations
  async handleSamplingRequest(request: SamplingRequest): Promise<SamplingResult> { /* ... */ }
  async handleElicitationRequest(request: ElicitationRequest): Promise<ElicitationResult> { /* ... */ }

  // Lifecycle
  async close(): Promise<void> { /* ... */ }
}
```

---

## Common Patterns

### Pattern: Bidirectional Communication

```typescript
class Client {
  // Client → Server requests
  async request(method: string, params: any): Promise<any> {
    return this.sendRequest({ method, params });
  }

  // Server → Client requests (handlers)
  private handlers = new Map<string, RequestHandler>();

  registerHandler(method: string, handler: RequestHandler) {
    this.handlers.set(method, handler);
  }

  // Message router
  private async handleIncomingMessage(message: JSONRPCMessage) {
    if ('method' in message && 'id' in message) {
      // This is a request FROM server TO client
      const handler = this.handlers.get(message.method);
      if (handler) {
        const result = await handler(message.params);
        await this.sendResponse(message.id, result);
      }
    }
  }
}

// Usage:
client.registerHandler('sampling/createMessage', async (params) => {
  // Server is asking client to get LLM completion
  return await this.llm.complete(params.messages);
});
```

### Pattern: Resource vs Tool Usage

```typescript
// Resources: Data client can READ
const calendarData = await client.readResource('calendar://events/today');
// Returns: { text: "Meeting at 3pm, Lunch at 12pm" }

// Tools: Actions client can EXECUTE
const result = await client.callTool('create_event', {
  title: "Team Meeting",
  time: "2024-01-15T15:00:00Z"
});
// Returns: { content: [{ type: "text", text: "Event created" }] }
```

### Pattern: Prompts as Templates

```typescript
// Get prompt template from server
const prompt = await client.getPrompt('write_email', {
  recipient: "boss@company.com",
  topic: "project update"
});

// prompt.messages contains pre-filled conversation
// Send to LLM with additional context
const completion = await llm.complete([
  ...prompt.messages,
  { role: "user", content: "Include metrics from Q4" }
]);
```

---

## Anti-Patterns to Avoid

### ❌ Client Choosing Tools
```typescript
// WRONG: Client decides what to do
if (query.includes('weather')) {
  return await client.callTool('check_weather', { city: extractCity(query) });
}
```

### ❌ Forgetting Session IDs
```typescript
// WRONG: Not propagating session
fetch(url, {
  headers: { 'Content-Type': 'application/json' }  // Missing Mcp-Session-Id
});
```

### ❌ No Retry Logic
```typescript
// WRONG: Fail on first error
const result = await client.callTool('flaky_api', {});  // Will fail randomly
```

### ❌ Verbose Responses
```typescript
// WRONG: Returning all data
return await database.query('SELECT * FROM users');  // 10,000 rows

// CORRECT: Return summary
return { count: 10000, sample: users.slice(0, 10) };
```

---

## Quick Start Templates

See reference files:
- **TypeScript**: [typescript_mcp_client.md](./reference/typescript_mcp_client.md)
- **Python**: [python_mcp_client.md](./reference/python_mcp_client.md)
- **Architecture**: [client_architecture.md](./reference/client_architecture.md)
- **Best Practices**: [mcp_client_best_practices.md](./reference/mcp_client_best_practices.md)

---

## Success Criteria

Client is production-ready when:
- [x] Connects to servers via all required transports
- [x] Negotiates capabilities correctly
- [x] Discovers and executes tools, resources, prompts
- [x] Implements retry logic with exponential backoff
- [x] Handles errors gracefully with actionable messages
- [x] Enforces security at network, auth, authz, validation layers
- [x] Optimizes for token efficiency
- [x] Passes both technical and behavioral tests
- [x] Includes comprehensive logging to stderr (never stdout in stdio mode)
- [x] Manages sessions correctly (HTTP transport)
