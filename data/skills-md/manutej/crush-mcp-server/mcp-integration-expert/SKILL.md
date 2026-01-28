---
name: mcp-integration-expert
description: Expert guidance for researching, documenting, and integrating Model Context Protocol (MCP) servers and tools. Covers MCP architecture, server/client implementation patterns, tool discovery, integration workflows, security best practices, and multi-language SDK usage (Python, TypeScript, C#, Java, Rust). Enables seamless integration of MCP tools into Claude Code and AI applications.
---

# MCP Integration Expert

Comprehensive skill for researching, documenting, and integrating Model Context Protocol (MCP) servers and tools into Claude Code and AI applications.

## When to Use This Skill

Use this skill when you need to:
- Research and evaluate MCP servers for integration
- Build custom MCP servers or clients
- Integrate existing MCP tools into Claude Code
- Document MCP server capabilities and usage patterns
- Troubleshoot MCP integration issues
- Implement MCP security and authentication patterns
- Create multi-language MCP implementations (Python, TypeScript, C#, Java, Rust)
- Design MCP-based AI agent workflows
- Evaluate MCP server trust scores and documentation quality

## Model Context Protocol (MCP) Overview

### What is MCP?

The **Model Context Protocol (MCP)** is an open standard introduced by Anthropic in November 2024 that standardizes how AI applications and Large Language Models (LLMs) integrate with external data sources, tools, and systems.

**Key Analogy**: MCP is like a "USB-C port for AI" - providing a universal, standardized interface for connecting AI models to diverse data sources and tools.

### Core Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        MCP Client                           │
│                     (AI Application)                        │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Claude     │  │   ChatGPT    │  │    Custom    │    │
│  │     Code     │  │   Desktop    │  │      App     │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ MCP Protocol
                          │
┌─────────────────────────────────────────────────────────────┐
│                      MCP Servers                            │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  Linear  │  │ Postgres │  │  GitHub  │  │  Custom  │  │
│  │  Server  │  │  Server  │  │  Server  │  │  Server  │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### MCP Protocol Communication Flow

```mermaid
sequenceDiagram
    autonumber
    actor User as 👤 User
    participant ClientApp as 🖥️ Client App
    participant ClientLLM as 🧠 Client LLM
    participant Server1 as 🔧 MCP Server 1
    participant Server2 as 📚 MCP Server 2

    %% Discovery Phase
    rect rgb(220, 240, 255)
        Note over ClientApp, Server2: TOOL DISCOVERY PHASE
        ClientApp->>+Server1: Request available tools/resources
        Server1-->>-ClientApp: Return tool list (JSON)
        ClientApp->>+Server2: Request available tools/resources
        Server2-->>-ClientApp: Return tool list (JSON)
        Note right of ClientApp: Store combined tool<br/>catalog locally
    end

    %% User Interaction
    rect rgb(255, 240, 220)
        Note over User, ClientLLM: USER INTERACTION PHASE
        User->>+ClientApp: Enter natural language prompt
        ClientApp->>+ClientLLM: Forward prompt + tool catalog
        ClientLLM->>-ClientLLM: Analyze prompt & select tools
    end

    %% Tool Execution
    rect rgb(220, 255, 220)
        Note over ClientApp, Server1: TOOL EXECUTION PHASE
        ClientLLM->>+ClientApp: Request tool execution
        ClientApp->>+Server1: Execute specific tool
        Server1-->>-ClientApp: Return results
        ClientApp->>+ClientLLM: Process results
        ClientLLM-->>-ClientApp: Generate response
        ClientApp-->>-User: Display final answer
    end
```

### MCP Core Primitives

MCP provides three core primitives for context exchange:

1. **Resources**: Expose data sources (files, databases, APIs)
2. **Tools**: Enable actions and operations
3. **Prompts**: Provide reusable prompt templates

## MCP Integration Workflow

### Phase 1: Research & Discovery

#### 1.1 Identify MCP Server Needs

Questions to ask:
- What data sources do you need to access?
- What actions/tools do you need to perform?
- Are there existing MCP servers for your use case?
- Do you need to build a custom MCP server?

#### 1.2 Research Available MCP Servers

**Official MCP Server Repository**: https://github.com/modelcontextprotocol

**Popular MCP Servers (2025)**:
- **Linear MCP**: Project management and issue tracking
- **Playwright MCP**: Browser automation and testing
- **Context7 MCP**: Library documentation retrieval
- **GitHub MCP**: Repository management and automation
- **Postgres MCP**: Database queries and operations
- **Google Drive MCP**: File storage and retrieval
- **Slack MCP**: Team communication
- **Stripe MCP**: Payment processing
- **Puppeteer MCP**: Web scraping and automation

#### 1.3 Evaluate MCP Server Quality

**Trust Score Criteria** (1-10 scale):
- **9-10**: Highly authoritative (official SDKs, major platforms)
- **7-9**: Well-maintained community projects
- **5-7**: Experimental or niche implementations
- **<5**: Proof-of-concept or unmaintained

**Documentation Coverage**:
- **High**: 500+ code snippets
- **Medium**: 100-500 code snippets
- **Low**: <100 code snippets

### Phase 2: MCP Server Architecture

#### 2.1 MCP Server Components

```typescript
// TypeScript MCP Server Structure
import { FastMCP } from '@modelcontextprotocol/typescript-sdk';

const mcp = new FastMCP({
    name: "My MCP Server",
    version: "1.0.0"
});

// 1. Resources: Expose data
mcp.resource("greeting://{name}", (name: string) => {
    return `Hello, ${name}!`;
});

// 2. Tools: Enable actions
mcp.tool("calculate", {
    description: "Perform calculations",
    parameters: {
        operation: { type: "string" },
        a: { type: "number" },
        b: { type: "number" }
    }
}, async (params) => {
    // Tool implementation
});

// 3. Prompts: Reusable templates
mcp.prompt("code-review", {
    description: "Code review template",
    arguments: ["language", "code"]
});
```

#### 2.2 Transport Mechanisms

MCP supports multiple transport mechanisms:

**1. Stdio Transport** (Default for local servers)
```python
from mcp.server.fastmcp import FastMCP
from mcp.transports.stdio import serve_stdio

mcp = FastMCP("Demo")

# Run with stdio
asyncio.run(serve_stdio(mcp))
```

**2. HTTP/SSE Transport** (For remote servers)
```typescript
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/typescript-sdk';

const transport = new StreamableHTTPServerTransport(8000);
await server.connect(transport);
```

### Phase 3: MCP Client Integration

#### 3.1 Client Setup (Python)

```python
from mcp.client import stdio_client, ClientSession

async def run_client():
    server_params = {
        "command": "python",
        "args": ["server.py"]
    }

    async with stdio_client(server_params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            # Initialize connection
            await session.initialize()

            # Discover tools
            tools = await session.list_tools()

            # Call a tool
            result = await session.call_tool("add", arguments={"a": 5, "b": 7})
            print(f"Result: {result}")
```

#### 3.2 Client Setup (TypeScript)

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

class MCPClient {
    private client: Client;

    constructor() {
        this.client = new Client({
            name: "example-client",
            version: "1.0.0"
        }, {
            capabilities: {
                prompts: {},
                resources: {},
                tools: {}
            }
        });
    }

    async connectToServer(transport: Transport) {
        await this.client.connect(transport);
    }

    async listTools() {
        return await this.client.listTools();
    }

    async callTool(name: string, args: any) {
        return await this.client.callTool({
            name: name,
            arguments: args
        });
    }
}
```

#### 3.3 Client Setup (C#)

```csharp
using ModelContextProtocol.Client;
using ModelContextProtocol.Protocol.Transport;

var clientTransport = new StdioClientTransport(new()
{
    Name = "Demo Server",
    Command = "/path/to/server/executable",
    Arguments = [],
});

await using var mcpClient = await McpClientFactory.CreateAsync(clientTransport);

// List tools
var tools = await mcpClient.ListToolsAsync();

foreach (var tool in tools)
{
    Console.WriteLine($"Tool: {tool.Name}");
    Console.WriteLine($"Description: {tool.Description}");
}

// Call a tool
var result = await mcpClient.CallToolAsync("add", new { a = 5, b = 7 });
```

### Phase 4: Building Custom MCP Servers

#### 4.1 Python MCP Server (FastMCP)

```python
from fastmcp import FastMCP
from fastmcp.transports.stdio import serve_stdio
import asyncio

mcp = FastMCP(
    name="Weather MCP Server",
    version="1.0.0"
)

@mcp.tool()
def get_weather(location: str) -> dict:
    """Gets current weather for a location."""
    # Implementation would call weather API
    return {
        "temperature": 72.5,
        "conditions": "Sunny",
        "location": location
    }

@mcp.resource("weather://{location}")
def weather_resource(location: str) -> str:
    """Get weather data as a resource"""
    return f"Current weather in {location}"

class WeatherTools:
    @mcp.tool()
    def forecast(self, location: str, days: int = 1) -> dict:
        """Gets weather forecast"""
        return {
            "location": location,
            "forecast": [
                {"day": i+1, "temperature": 70 + i, "conditions": "Partly Cloudy"}
                for i in range(days)
            ]
        }

weather_tools = WeatherTools()

if __name__ == "__main__":
    asyncio.run(serve_stdio(mcp))
```

#### 4.2 TypeScript MCP Server

```typescript
import { FastMCP } from '@modelcontextprotocol/typescript-sdk';
import { serve_stdio } from '@modelcontextprotocol/typescript-sdk/transports/stdio';

const mcp = new FastMCP({
    name: "Weather MCP Server",
    version: "1.0.0"
});

mcp.tool("get_weather", {
    description: "Gets current weather for a location",
    parameters: {
        location: { type: "string", required: true }
    }
}, async (params) => {
    return {
        temperature: 72.5,
        conditions: "Sunny",
        location: params.location
    };
});

mcp.resource("weather://{location}", async (location: string) => {
    return `Current weather in ${location}`;
});

// Start server
serve_stdio(mcp);
```

#### 4.3 Java MCP Server

```java
import io.modelcontextprotocol.server.McpServer;
import io.modelcontextprotocol.server.McpToolDefinition;
import io.modelcontextprotocol.server.transport.StdioServerTransport;

public class WeatherMcpServer {
    public static void main(String[] args) throws Exception {
        McpServer server = McpServer.builder()
            .name("Weather MCP Server")
            .version("1.0.0")
            .build();

        server.registerTool(McpToolDefinition.builder("weatherTool")
            .description("Gets current weather for a location")
            .parameter("location", String.class)
            .execute((ctx) -> {
                String location = ctx.getParameter("location", String.class);
                WeatherData data = getWeatherData(location);

                return ToolResponse.content(
                    String.format("Temperature: %.1f°F, Conditions: %s",
                        data.getTemperature(),
                        data.getConditions())
                );
            })
            .build());

        try (StdioServerTransport transport = new StdioServerTransport()) {
            server.connect(transport);
            Thread.currentThread().join();
        }
    }
}
```

### Phase 5: LLM Integration Patterns

#### 5.1 Integrating MCP with OpenAI

```typescript
import OpenAI from "openai";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";

class MCPOpenAIClient {
    private openai: OpenAI;
    private mcpClient: Client;

    constructor() {
        this.openai = new OpenAI({
            apiKey: process.env.OPENAI_API_KEY,
        });

        this.mcpClient = new Client({
            name: "openai-mcp-client",
            version: "1.0.0"
        }, {
            capabilities: { tools: {} }
        });
    }

    // Adapt MCP tools to OpenAI format
    mcpToolToOpenAITool(tool: any) {
        return {
            type: "function" as const,
            function: {
                name: tool.name,
                description: tool.description,
                parameters: {
                    type: "object",
                    properties: tool.input_schema.properties,
                    required: tool.input_schema.required,
                },
            },
        };
    }

    async processRequest(userMessage: string) {
        // Get MCP tools
        const mcpTools = await this.mcpClient.listTools();
        const openaiTools = mcpTools.map(t => this.mcpToolToOpenAITool(t));

        // Call OpenAI with tools
        const response = await this.openai.chat.completions.create({
            model: "gpt-4",
            messages: [{ role: "user", content: userMessage }],
            tools: openaiTools,
        });

        // Handle tool calls
        const toolCalls = response.choices[0].message.tool_calls;
        if (toolCalls) {
            for (const toolCall of toolCalls) {
                const result = await this.mcpClient.callTool({
                    name: toolCall.function.name,
                    arguments: JSON.parse(toolCall.function.arguments),
                });
                console.log("Tool result:", result);
            }
        }
    }
}
```

#### 5.2 Integrating MCP with Azure OpenAI (C#)

```csharp
using Azure.AI.Inference;
using Azure;
using ModelContextProtocol.Client;
using System.Text.Json;

var endpoint = "https://models.inference.ai.azure.com";
var token = Environment.GetEnvironmentVariable("GITHUB_TOKEN");
var client = new ChatCompletionsClient(new Uri(endpoint), new AzureKeyCredential(token));

var mcpClient = await McpClientFactory.CreateAsync(clientTransport);

// Convert MCP tools to Azure format
ChatCompletionsToolDefinition ConvertFrom(string name, string description, JsonElement schema)
{
    FunctionDefinition functionDefinition = new FunctionDefinition(name)
    {
        Description = description,
        Parameters = BinaryData.FromObjectAsJson(new
        {
            Type = "object",
            Properties = schema
        })
    };

    return new ChatCompletionsToolDefinition(functionDefinition);
}

// Get tools from MCP server
var mcpTools = await mcpClient.ListToolsAsync();
var toolDefinitions = new List<ChatCompletionsToolDefinition>();

foreach (var tool in mcpTools)
{
    JsonElement propertiesElement;
    tool.JsonSchema.TryGetProperty("properties", out propertiesElement);

    var def = ConvertFrom(tool.Name, tool.Description, propertiesElement);
    toolDefinitions.Add(def);
}

// Use tools in chat completion
var chatHistory = new List<ChatRequestMessage>
{
    new ChatRequestSystemMessage("You are a helpful assistant"),
    new ChatRequestUserMessage("What's the weather in Seattle?")
};

var response = await client.CompleteAsync(chatHistory,
    new ChatCompletionsOptions { Tools = toolDefinitions });
```

### Phase 6: MCP Configuration in Claude Code

#### 6.1 Claude Code MCP Configuration

Claude Code automatically discovers and loads MCP servers configured in `claude_desktop_config.json`:

**Location**:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

**Configuration Format**:
```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@linear/mcp-server"],
      "env": {
        "LINEAR_API_KEY": "your-api-key"
      }
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp-server"]
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://user:pass@localhost/db"
      }
    },
    "custom-server": {
      "command": "python",
      "args": ["/path/to/custom/server.py"]
    }
  }
}
```

#### 6.2 Verify MCP Server Connection

Once configured, MCP servers automatically connect when Claude Code starts.

**Available MCP tools in Claude Code**:
```typescript
// All MCP tools are prefixed with "mcp__<server-name>__<tool-name>"
mcp__linear__create_issue
mcp__linear__list_issues
mcp__linear__update_issue
mcp__playwright__browser_navigate
mcp__playwright__browser_screenshot
mcp__context7__resolve_library_id
mcp__context7__get_library_docs
```

### Phase 7: Security & Best Practices

#### 7.1 Security Considerations (2025 Update)

**Known Security Issues** (April 2025):
- **Prompt Injection**: MCP tools can be exploited via prompt injection attacks
- **Tool Permissions**: Combining tools can enable unintended file exfiltration
- **Lookalike Tools**: Malicious tools can silently replace trusted ones
- **Credential Exposure**: API keys and credentials must be protected

**Security Best Practices**:

1. **Validate Tool Inputs**
```python
@mcp.tool()
def read_file(filepath: str) -> str:
    """Read a file - with security validation"""
    # Validate filepath to prevent path traversal
    import os
    filepath = os.path.normpath(filepath)

    # Ensure within allowed directory
    allowed_dir = "/home/user/documents"
    if not filepath.startswith(allowed_dir):
        raise ValueError("Access denied: Path outside allowed directory")

    with open(filepath, 'r') as f:
        return f.read()
```

2. **Implement Authentication**
```python
from fastmcp import FastMCP
import os

mcp = FastMCP("Secure Server", version="1.0.0")

@mcp.middleware
async def authenticate(request, call_next):
    api_key = request.headers.get("X-API-Key")
    expected_key = os.getenv("MCP_API_KEY")

    if api_key != expected_key:
        raise PermissionError("Invalid API key")

    return await call_next(request)
```

3. **Rate Limiting**
```python
from collections import defaultdict
import time

call_counts = defaultdict(list)

@mcp.middleware
async def rate_limit(request, call_next):
    client_id = request.client_id
    now = time.time()

    # Clean old entries
    call_counts[client_id] = [t for t in call_counts[client_id] if now - t < 60]

    # Check rate limit (10 calls per minute)
    if len(call_counts[client_id]) >= 10:
        raise Exception("Rate limit exceeded")

    call_counts[client_id].append(now)
    return await call_next(request)
```

#### 7.2 Error Handling Best Practices

```python
from fastmcp import FastMCP
from typing import Optional
import logging

mcp = FastMCP("Robust Server", version="1.0.0")
logger = logging.getLogger(__name__)

@mcp.tool()
def safe_api_call(endpoint: str, params: Optional[dict] = None) -> dict:
    """Make an API call with comprehensive error handling"""
    try:
        # Validate inputs
        if not endpoint.startswith("https://"):
            raise ValueError("Only HTTPS endpoints allowed")

        # Make API call
        response = requests.get(endpoint, params=params, timeout=5)
        response.raise_for_status()

        return {
            "success": True,
            "data": response.json()
        }

    except requests.Timeout:
        logger.error(f"Timeout calling {endpoint}")
        return {
            "success": False,
            "error": "Request timeout",
            "error_type": "timeout"
        }

    except requests.HTTPError as e:
        logger.error(f"HTTP error calling {endpoint}: {e}")
        return {
            "success": False,
            "error": str(e),
            "error_type": "http_error",
            "status_code": e.response.status_code
        }

    except Exception as e:
        logger.exception(f"Unexpected error calling {endpoint}")
        return {
            "success": False,
            "error": "Internal server error",
            "error_type": "internal_error"
        }
```

#### 7.3 Testing MCP Servers

**Integration Testing (Python)**:
```python
import pytest
from mcp.server import McpServer
from mcp.client import McpClient

@pytest.mark.asyncio
async def test_mcp_server_integration():
    # Start test server
    server = McpServer()
    server.register_tool(WeatherForecastTool(MockWeatherService()))
    await server.start(port=5000)

    try:
        # Create client
        client = McpClient("http://localhost:5000")

        # Test tool discovery
        tools = await client.discover_tools()
        assert "weatherForecast" in [t.name for t in tools]

        # Test tool execution
        response = await client.execute_tool("weatherForecast", {
            "location": "Seattle",
            "days": 3
        })

        # Verify response
        assert response.status_code == 200
        assert "Seattle" in response.content[0].text

    finally:
        await server.stop()
```

### Phase 8: Advanced MCP Patterns

#### 8.1 Chain of Tools Workflow

```python
class ChainWorkflow:
    def __init__(self, tools_chain):
        self.tools_chain = tools_chain

    async def execute(self, mcp_client, initial_input):
        current_result = initial_input
        all_results = {"input": initial_input}

        for tool_name in self.tools_chain:
            response = await mcp_client.execute_tool(tool_name, current_result)
            all_results[tool_name] = response.result
            current_result = response.result

        return {
            "final_result": current_result,
            "all_results": all_results
        }

# Usage
data_pipeline = ChainWorkflow([
    "dataFetch",
    "dataCleaner",
    "dataAnalyzer",
    "dataVisualizer"
])

result = await data_pipeline.execute(
    mcp_client,
    {"source": "sales_database", "table": "transactions"}
)
```

#### 8.2 Parallel Tool Execution

```typescript
async function executeParallelTools(mcpClient: Client, tools: ToolCall[]) {
    const promises = tools.map(tool =>
        mcpClient.callTool({
            name: tool.name,
            arguments: tool.arguments
        })
    );

    const results = await Promise.all(promises);
    return results;
}

// Usage
const toolCalls = [
    { name: "get_weather", arguments: { location: "Seattle" } },
    { name: "get_weather", arguments: { location: "Portland" } },
    { name: "get_weather", arguments: { location: "Vancouver" } }
];

const weatherData = await executeParallelTools(mcpClient, toolCalls);
```

#### 8.3 Context-Aware Tool Selection

```python
from typing import List, Dict
import openai

class ContextAwareToolSelector:
    def __init__(self, mcp_client, llm_client):
        self.mcp_client = mcp_client
        self.llm_client = llm_client

    async def select_tools(self, user_query: str, available_tools: List[Dict]) -> List[str]:
        """Use LLM to intelligently select which tools to use"""

        tool_descriptions = "\n".join([
            f"- {tool['name']}: {tool['description']}"
            for tool in available_tools
        ])

        prompt = f"""
        User query: {user_query}

        Available tools:
        {tool_descriptions}

        Select the most relevant tools to answer this query.
        Return a JSON array of tool names.
        """

        response = await self.llm_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        selected_tools = json.loads(response.choices[0].message.content)
        return selected_tools["tools"]
```

## MCP Ecosystem (2025)

### Major Platform Adoptions

**OpenAI** (March 2025):
- MCP integrated into ChatGPT Desktop
- MCP support in Agents SDK
- MCP compatibility in Responses API

**Google** (April 2025):
- MCP support in Gemini models
- Data Commons MCP Server (public datasets)
- MCP integration in Google DeepMind infrastructure

**Microsoft** (2025):
- MCP in Copilot Studio (GA)
- Semantic Kernel integration
- Azure OpenAI compatibility

**Anthropic**:
- Native MCP support in Claude Code
- Reference MCP server implementations
- MCP specification maintenance

### Official MCP Servers

Repository: https://github.com/modelcontextprotocol

**Enterprise Integrations**:
- Google Drive, Slack, GitHub, GitLab
- Postgres, MySQL, MongoDB
- AWS, Azure, GCP
- Stripe, Salesforce

**Development Tools**:
- Puppeteer, Playwright
- Docker, Kubernetes
- Git, GitHub Actions

### MCP SDK Support (2025)

**Official SDKs**:
- Python: `pip install modelcontextprotocol`
- TypeScript: `npm install @modelcontextprotocol/sdk`
- C#: NuGet package
- Java: Maven/Gradle
- Rust: Cargo package
- Swift: Swift Package Manager

## Documentation Research Workflow

### Using Context7 for MCP Research

When researching MCP servers and integration patterns:

```bash
# 1. Resolve library ID
/ctx7 model context protocol

# 2. Get comprehensive documentation
# Context7 returns documentation with:
# - Trust Score (7-10 for quality sources)
# - Code Snippets (100-5000+)
# - Implementation examples
# - Best practices

# 3. Evaluate quality
# - Trust Score 9-10: Official documentation
# - Trust Score 7-9: Well-maintained projects
# - Code Snippets 500+: Comprehensive coverage
```

**Best Context7 Sources for MCP** (by Trust Score):
1. `/microsoft/mcp-for-beginners` (Trust: 9.9, Snippets: 30,945)
2. `/modelcontextprotocol/python-sdk` (Trust: 7.8, Snippets: 119)
3. `/modelcontextprotocol/typescript-sdk` (Trust: 7.8, Snippets: 55)
4. `/modelcontextprotocol/csharp-sdk` (Trust: 7.8, Snippets: 59)

## Common MCP Integration Patterns

### Pattern 1: Simple Tool Integration

**Use Case**: Add a single MCP tool to Claude Code

```json
// claude_desktop_config.json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["weather_server.py"]
    }
  }
}
```

```python
# weather_server.py
from fastmcp import FastMCP
from fastmcp.transports.stdio import serve_stdio
import asyncio

mcp = FastMCP("Weather", version="1.0.0")

@mcp.tool()
def get_weather(location: str) -> str:
    return f"Weather in {location}: Sunny, 72°F"

asyncio.run(serve_stdio(mcp))
```

### Pattern 2: Multi-Server Integration

**Use Case**: Combine multiple MCP servers for complex workflows

```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@linear/mcp-server"],
      "env": { "LINEAR_API_KEY": "..." }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "..." }
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp-server"]
    }
  }
}
```

### Pattern 3: Custom Resource Server

**Use Case**: Expose internal documentation or data

```python
from fastmcp import FastMCP
from fastmcp.transports.stdio import serve_stdio
import asyncio
import os

mcp = FastMCP("Internal Docs", version="1.0.0")

@mcp.resource("docs://{path}")
def get_documentation(path: str) -> str:
    """Get internal documentation by path"""
    docs_dir = "/company/docs"
    filepath = os.path.join(docs_dir, path)

    if not os.path.exists(filepath):
        return f"Documentation not found: {path}"

    with open(filepath, 'r') as f:
        return f.read()

@mcp.tool()
def search_docs(query: str) -> list:
    """Search internal documentation"""
    # Implementation would use search index
    return [
        {"title": "Getting Started", "path": "onboarding/getting-started.md"},
        {"title": "API Reference", "path": "api/reference.md"}
    ]

asyncio.run(serve_stdio(mcp))
```

## Troubleshooting MCP Integration

### Issue 1: MCP Server Not Connecting

**Symptoms**: Tools not appearing in Claude Code

**Solutions**:
1. Check configuration file location
2. Verify command and args are correct
3. Test server independently: `python server.py`
4. Check logs in Claude Code
5. Ensure environment variables are set

### Issue 2: Tool Execution Failures

**Symptoms**: Tool calls return errors

**Solutions**:
1. Validate tool parameter schemas
2. Add error handling in tool implementation
3. Check server logs for exceptions
4. Test with simple inputs first
5. Verify authentication/API keys

### Issue 3: Performance Issues

**Symptoms**: Slow tool responses

**Solutions**:
1. Add caching for repeated calls
2. Implement connection pooling
3. Use async/await properly
4. Add timeout handling
5. Consider HTTP transport for remote servers

## Best Practices Summary

1. **Start Simple**: Begin with a single tool, expand gradually
2. **Use Official SDKs**: Leverage maintained libraries (Python, TypeScript, C#, Java)
3. **Implement Security**: Validate inputs, authenticate, rate limit
4. **Handle Errors Gracefully**: Return structured error responses
5. **Document Thoroughly**: Provide clear tool descriptions and parameter schemas
6. **Test Extensively**: Write integration tests for all tools
7. **Monitor Performance**: Track response times and error rates
8. **Version Your Servers**: Use semantic versioning for changes
9. **Leverage Context7**: Research documentation before implementation
10. **Follow MCP Specification**: Adhere to official protocol standards

## Quick Reference

### MCP Server Checklist

- [ ] Server name and version defined
- [ ] Tools have clear descriptions
- [ ] Parameter schemas are complete
- [ ] Error handling implemented
- [ ] Authentication/authorization configured
- [ ] Logging enabled
- [ ] Tests written
- [ ] Documentation created
- [ ] Security validated
- [ ] Performance tested

### Essential Commands

```bash
# Install MCP SDKs
pip install modelcontextprotocol
npm install @modelcontextprotocol/sdk

# Test server independently
python server.py

# Verify Claude Code config
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Research with Context7
/ctx7 [library-name]
```

### Resources

**Official Documentation**:
- MCP Specification: https://modelcontextprotocol.io/specification
- MCP GitHub: https://github.com/modelcontextprotocol
- MCP Servers: https://github.com/modelcontextprotocol (servers directory)

**SDKs**:
- Python SDK: https://github.com/modelcontextprotocol/python-sdk
- TypeScript SDK: https://github.com/modelcontextprotocol/typescript-sdk
- C# SDK: https://github.com/modelcontextprotocol/csharp-sdk
- Java SDK: https://github.com/modelcontextprotocol/java-sdk

**Learning Resources**:
- Microsoft MCP for Beginners: https://github.com/microsoft/mcp-for-beginners
- Anthropic MCP Announcement: https://www.anthropic.com/news/model-context-protocol

---

**Skill Version**: 1.0.0
**Last Updated**: 2025-10-18
**Context7 Research**: Microsoft MCP for Beginners (Trust: 9.9)
