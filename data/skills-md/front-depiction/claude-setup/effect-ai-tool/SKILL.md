---
name: effect-ai-tool
description: Define and implement AI tools using @effect/ai's Tool and Toolkit APIs. Use when building LLM integrations with type-safe tool definitions, parameter validation, and handler implementations. Covers user-defined tools, provider-defined tools, and toolkit composition.
---

# Effect AI Tool Skill

Use this skill when implementing tools for AI language models using the @effect/ai library. This covers tool definition, parameter schemas, success/failure handling, and toolkit composition.

## Effect AI Documentation Access

For comprehensive Effect AI documentation, view the Effect repository git subtree in `.context/effect/packages/ai/`

Reference this for:
- Tool.make API and configuration
- Toolkit.make for composing multiple tools
- Schema.Struct.Fields for parameters
- Handler implementation patterns

## Core Concepts

### Tool Anatomy

```typescript
Effect<A, E, R>
       ↓
Tool<Name, Config, Requirements>

Config := {
  parameters: Schema.Struct<Fields>
  success: Schema<A>
  failure: Schema<E>
  failureMode: "error" | "return"
}
```

### Toolkit Flow

```typescript
Tool₁, Tool₂, Tool₃
       ↓ Toolkit.make
Toolkit<{tool1: Tool₁, tool2: Tool₂, tool3: Tool₃}>
       ↓ .toLayer(handlers)
Layer<Handlers>
       ↓ Effect.provide
Effect with tool execution capability
```

## Creating User-Defined Tools

### Basic Tool Definition

```typescript
import * as Tool from "@effect/ai/Tool"
import { Schema } from "effect"

const GetCurrentTime = Tool.make("GetCurrentTime", {
  description: "Returns the current timestamp in milliseconds",
  success: Schema.Number
})

const result = Tool.Success<typeof GetCurrentTime>
```

**Key Pattern: Tool.make**
- First parameter: tool name (string literal)
- Second parameter: configuration object
- No parameters field = empty parameters `{}`
- Default success: `Schema.Void`
- Default failure: `Schema.Never`

### Tool from TaggedRequest

```typescript
import * as Tool from "@effect/ai/Tool"
import { Schema } from "effect"

class GetUserRequest extends Schema.TaggedRequest<GetUserRequest>()(
  "GetUserRequest",
  {
    failure: Schema.Never,
    success: Schema.Struct({
      id: Schema.String,
      name: Schema.String
    }),
    payload: {
      userId: Schema.String
    }
  }
) {}

const GetUserTool = Tool.fromTaggedRequest(GetUserRequest)

type Params = Tool.Parameters<typeof GetUserTool>
type Success = Tool.Success<typeof GetUserTool>
```

**Key Pattern: fromTaggedRequest**
- Creates Tool directly from TaggedRequest schema
- Inherits success, failure, and payload schemas
- Tool name matches request tag
- Useful for request/response domain models

### Tool with Parameters

```typescript
import * as Tool from "@effect/ai/Tool"
import { Schema } from "effect"

const GetWeather = Tool.make("GetWeather", {
  description: "Get weather information for a location",
  parameters: {
    location: Schema.String,
    units: Schema.optional(Schema.Literal("celsius", "fahrenheit"))
  },
  success: Schema.Struct({
    temperature: Schema.Number,
    condition: Schema.String,
    humidity: Schema.Number
  })
})

type Params = Tool.Parameters<typeof GetWeather>
type Success = Tool.Success<typeof GetWeather>
```

**Key Pattern: Schema.Struct.Fields**
- Parameters use field objects, NOT `Schema.Struct()`
- Tool.make wraps fields in `Schema.Struct` automatically
- Use `Schema.optional()` for optional parameters

### Tool with Failure Handling

```typescript
import * as Tool from "@effect/ai/Tool"
import { Schema, Data } from "effect"

class UserNotFound extends Data.TaggedError("UserNotFound")<{
  readonly userId: string
}> {}

class DatabaseError extends Data.TaggedError("DatabaseError")<{
  readonly message: string
}> {}

const FindUser = Tool.make("FindUser", {
  description: "Find user by ID",
  parameters: {
    userId: Schema.String
  },
  success: Schema.Struct({
    id: Schema.String,
    name: Schema.String,
    email: Schema.String
  }),
  failure: Schema.Union(
    Schema.instanceOf(UserNotFound),
    Schema.instanceOf(DatabaseError)
  ),
  failureMode: "error"
})

type Error = Tool.Failure<typeof FindUser>
```

**Key Pattern: failureMode**
- `"error"` (default): Failures go to Effect error channel
- `"return"`: Failures returned as tool result (captured, not thrown)

### Tool with Service Dependencies

```typescript
import * as Tool from "@effect/ai/Tool"
import * as Context from "effect/Context"
import { Schema } from "effect"

interface Database {
  readonly query: (sql: string) => Effect.Effect<unknown>
}

const Database = Context.GenericTag<Database>("Database")

const QueryDatabase = Tool.make("QueryDatabase", {
  description: "Execute a database query",
  parameters: {
    sql: Schema.String
  },
  success: Schema.Unknown,
  dependencies: [Database]
})

type Requirements = Tool.Requirements<typeof QueryDatabase>
```

**Key Pattern: dependencies**
- Array of Context.Tag instances
- Requirements extracted at type level
- Must be provided when creating handlers

## Creating Toolkits

### Basic Toolkit

```typescript
import * as Toolkit from "@effect/ai/Toolkit"
import * as Tool from "@effect/ai/Tool"
import { Effect, Schema } from "effect"

const GetCurrentTime = Tool.make("GetCurrentTime", {
  description: "Get the current timestamp",
  success: Schema.Number
})

const GetWeather = Tool.make("GetWeather", {
  description: "Get weather for a location",
  parameters: {
    location: Schema.String
  },
  success: Schema.Struct({
    temperature: Schema.Number,
    condition: Schema.String
  })
})

const MyToolkit = Toolkit.make(GetCurrentTime, GetWeather)

type Tools = Toolkit.Tools<typeof MyToolkit>
```

**Key Pattern: Toolkit.make**
- Accepts variadic tool arguments
- Returns `Toolkit<Record<Name, Tool>>`
- Tools indexed by their name property

### Implementing Tool Handlers

```typescript
import { Effect } from "effect"

const MyToolkitLayer = MyToolkit.toLayer({
  GetCurrentTime: () => Effect.succeed(Date.now()),

  GetWeather: ({ location }) =>
    Effect.gen(function* () {
      const data = yield* fetchWeatherData(location)
      return {
        temperature: data.temp,
        condition: data.conditions
      }
    })
})

declare const fetchWeatherData: (location: string) => Effect.Effect<{
  readonly temp: number
  readonly conditions: string
}>
```

**Key Pattern: toLayer**
- Object mapping tool names to handler functions
- Handler signature: `(params) => Effect<Success, Failure, Requirements>`
- Returns `Layer<Handlers>`

### Alternative: Handlers as Context

```typescript
import { Effect } from "effect"

const program = Effect.gen(function* () {
  const context = yield* MyToolkit.toContext({
    GetCurrentTime: () => Effect.succeed(Date.now()),

    GetWeather: ({ location }) =>
      Effect.gen(function* () {
        const data = yield* fetchWeatherData(location)
        return {
          temperature: data.temp,
          condition: data.conditions
        }
      })
  })

  const result = yield* Effect.provide(myEffect, context)
  return result
})

declare const fetchWeatherData: (location: string) => Effect.Effect<{
  readonly temp: number
  readonly conditions: string
}>

declare const myEffect: Effect.Effect<unknown, never, Handlers>
```

**Key Pattern: toContext**
- Similar to toLayer but returns Context instead of Layer
- Use when you need direct Context (not Layer composition)
- Returns `Context<Handlers>`
- Provide directly to effects that require handlers

### Providing Dependencies to Handlers

```typescript
import * as Context from "effect/Context"
import { Effect } from "effect"

interface WeatherService {
  readonly fetch: (location: string) => Effect.Effect<WeatherData>
}

const WeatherService = Context.GenericTag<WeatherService>("WeatherService")

interface WeatherData {
  readonly temperature: number
  readonly condition: string
}

const GetWeatherWithDeps = Tool.make("GetWeather", {
  parameters: {
    location: Schema.String
  },
  success: Schema.Struct({
    temperature: Schema.Number,
    condition: Schema.String
  }),
  dependencies: [WeatherService]
})

const toolkit = Toolkit.make(GetWeatherWithDeps)

const toolkitLayer = toolkit.toLayer({
  GetWeather: ({ location }) =>
    Effect.gen(function* () {
      const service = yield* WeatherService
      const data = yield* service.fetch(location)
      return {
        temperature: data.temperature,
        condition: data.condition
      }
    })
})

const program = Effect.gen(function* () {
  const handlers = yield* toolkitLayer
  const result = yield* handlers.handle("GetWeather", { location: "NYC" })
  return result
}).pipe(
  Effect.provide(WeatherServiceLive)
)

declare const WeatherServiceLive: Layer<WeatherService>
```

**Key Pattern: Handler Context**
- Handlers run with injected dependencies
- Access via `yield* Tag` in Effect.gen
- Dependencies must be provided to final effect

### Merging Toolkits

```typescript
import * as Toolkit from "@effect/ai/Toolkit"

const mathToolkit = Toolkit.make(
  Tool.make("add", {
    parameters: { a: Schema.Number, b: Schema.Number },
    success: Schema.Number
  }),
  Tool.make("subtract", {
    parameters: { a: Schema.Number, b: Schema.Number },
    success: Schema.Number
  })
)

const utilityToolkit = Toolkit.make(
  Tool.make("getCurrentTime", { success: Schema.Number }),
  Tool.make("generateUUID", { success: Schema.String })
)

const combined = Toolkit.merge(mathToolkit, utilityToolkit)

type AllTools = Toolkit.Tools<typeof combined>
```

**Key Pattern: Toolkit.merge**
- Combines multiple toolkits into one
- Later toolkits override earlier ones on name collision
- Type-safe union of all tools

## Provider-Defined Tools

### Basic Provider Tool

```typescript
import * as Tool from "@effect/ai/Tool"
import { Schema } from "effect"

const AnthropicBash = Tool.providerDefined({
  id: "anthropic.bash",
  toolkitName: "Bash",
  providerName: "bash_20241022",
  args: {
    command: Schema.String
  }
})

const bashTool = AnthropicBash({ command: "ls -la" })

type ToolType = typeof bashTool
```

**Key Pattern: Tool.providerDefined**
- Returns a function that accepts args
- `id`: Unique identifier `<provider>.<tool-name>`
- `toolkitName`: Name in your Toolkit
- `providerName`: Name recognized by AI provider
- `args`: Configuration passed to provider

### Provider Tool with Handler

```typescript
import * as Tool from "@effect/ai/Tool"
import { Schema } from "effect"

const WebSearch = Tool.providerDefined({
  id: "openai.web_search",
  toolkitName: "WebSearch",
  providerName: "web_search",
  args: {
    maxResults: Schema.Number
  },
  requiresHandler: true,
  parameters: {
    query: Schema.String
  },
  success: Schema.Struct({
    results: Schema.Array(Schema.Struct({
      title: Schema.String,
      url: Schema.String,
      snippet: Schema.String
    }))
  })
})

const searchTool = WebSearch({ maxResults: 10, failureMode: "return" })

const toolkit = Toolkit.make(searchTool)

const toolkitLayer = toolkit.toLayer({
  WebSearch: ({ query }) =>
    Effect.gen(function* () {
      const results = yield* performSearch(query)
      return { results }
    })
})

declare const performSearch: (query: string) => Effect.Effect<Array<{
  readonly title: string
  readonly url: string
  readonly snippet: string
}>>
```

**Key Pattern: requiresHandler**
- `false` (default): Provider executes tool completely
- `true`: Your handler processes provider results
- Handler receives `parameters` from provider

## Tool Result Flow

### Understanding ToolCallPart and ToolResultPart

```typescript
import * as Prompt from "@effect/ai/Prompt"

const toolCallPart = Prompt.makePart("tool-call", {
  id: "call_123",
  name: "GetWeather",
  params: { location: "NYC" },
  providerExecuted: false
})

const toolResultPart = Prompt.makePart("tool-result", {
  toolCallId: "call_123",
  result: {
    temperature: 72,
    condition: "sunny"
  },
  isError: false
})
```

**Key Pattern: Tool Call Flow**
1. LLM generates ToolCallPart in response
2. Your code extracts tool call via Toolkit.handle
3. Handler executes and returns HandlerResult
4. Create ToolResultPart with handler result
5. Send ToolResultPart back to LLM

### Executing Tool Handlers

```typescript
import { Effect } from "effect"

const program = Effect.gen(function* () {
  const toolkit = yield* MyToolkitLayer

  const result = yield* toolkit.handle("GetWeather", {
    location: "San Francisco"
  })

  console.log(result.isFailure)
  console.log(result.result)
  console.log(result.encodedResult)
})

interface HandlerResult<T> {
  readonly isFailure: boolean
  readonly result: Result<T>
  readonly encodedResult: unknown
}

type Result<T> = Tool.Success<T> | Tool.Failure<T>
```

**Key Pattern: toolkit.handle**
- Returns `HandlerResult<Tool>` with three fields
- `isFailure`: Whether handler failed
- `result`: Typed success or failure value
- `encodedResult`: JSON-serializable for LLM

## Advanced Patterns

### Tool Annotations

```typescript
import * as Tool from "@effect/ai/Tool"
import { Schema } from "effect"

const ReadOnlyQuery = Tool.make("query", {
  parameters: { sql: Schema.String },
  success: Schema.Unknown
}).pipe(
  Tool.annotate(Tool.Readonly, true),
  Tool.annotate(Tool.Destructive, false),
  Tool.annotate(Tool.Idempotent, true)
)
```

**Available Annotations:**
- `Tool.Readonly`: Tool only reads data
- `Tool.Destructive`: Tool performs destructive operations
- `Tool.Idempotent`: Safe to call multiple times
- `Tool.OpenWorld`: Can handle arbitrary external data
- `Tool.Title`: Human-readable title

### JSON Schema Generation

```typescript
import * as Tool from "@effect/ai/Tool"

const tool = Tool.make("example", {
  parameters: {
    name: Schema.String,
    age: Schema.optional(Schema.Number)
  }
})

const jsonSchema = Tool.getJsonSchema(tool)
```

**Output:**
```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "age": { "type": "number" }
  },
  "required": ["name"],
  "additionalProperties": false
}
```

### Tool Guards

```typescript
import * as Tool from "@effect/ai/Tool"

const userTool = Tool.make("example")
const providerTool = Tool.providerDefined({
  id: "provider.tool",
  toolkitName: "Example",
  providerName: "example",
  args: {}
})({})

Tool.isUserDefined(userTool)
Tool.isProviderDefined(providerTool)
```

### Dynamic Tool Selection

```typescript
import { Effect, Match } from "effect"

const executeTool = (toolName: string, params: unknown) =>
  Effect.gen(function* () {
    const toolkit = yield* MyToolkitLayer

    const handler = Match.value(toolName).pipe(
      Match.when("GetWeather", () => toolkit.handle("GetWeather", params)),
      Match.when("GetCurrentTime", () => toolkit.handle("GetCurrentTime", params)),
      Match.orElse(() => Effect.fail(new Error(`Unknown tool: ${toolName}`)))
    )

    return yield* handler
  })
```

## Complete Example

```typescript
import * as Tool from "@effect/ai/Tool"
import * as Toolkit from "@effect/ai/Toolkit"
import { Effect, Schema, Data, Context, Layer } from "effect"

class UserNotFound extends Data.TaggedError("UserNotFound")<{
  readonly userId: string
}> {}

interface Database {
  readonly query: (sql: string) => Effect.Effect<unknown>
}

const Database = Context.GenericTag<Database>("Database")

const GetUser = Tool.make("GetUser", {
  description: "Retrieve user information by ID",
  parameters: {
    userId: Schema.String
  },
  success: Schema.Struct({
    id: Schema.String,
    name: Schema.String,
    email: Schema.String
  }),
  failure: Schema.instanceOf(UserNotFound),
  failureMode: "error",
  dependencies: [Database]
})

const CreateUser = Tool.make("CreateUser", {
  description: "Create a new user",
  parameters: {
    name: Schema.String,
    email: Schema.String
  },
  success: Schema.Struct({
    id: Schema.String,
    name: Schema.String,
    email: Schema.String
  }),
  dependencies: [Database]
})

const GetCurrentTime = Tool.make("GetCurrentTime", {
  description: "Get the current Unix timestamp",
  success: Schema.Number
})

const UserToolkit = Toolkit.make(GetUser, CreateUser, GetCurrentTime)

const UserToolkitLive = UserToolkit.toLayer({
  GetUser: ({ userId }) =>
    Effect.gen(function* () {
      const db = yield* Database
      const user = yield* db.query(`SELECT * FROM users WHERE id = ?`, userId)

      if (!user) {
        return yield* Effect.fail(new UserNotFound({ userId }))
      }

      return user as { id: string; name: string; email: string }
    }),

  CreateUser: ({ name, email }) =>
    Effect.gen(function* () {
      const db = yield* Database
      const id = crypto.randomUUID()

      yield* db.query(
        `INSERT INTO users (id, name, email) VALUES (?, ?, ?)`,
        id, name, email
      )

      return { id, name, email }
    }),

  GetCurrentTime: () =>
    Effect.succeed(Date.now())
})

const DatabaseLive = Layer.succeed(Database, {
  query: (sql: string, ...params: ReadonlyArray<unknown>) =>
    Effect.logInfo(`Query: ${sql}`).pipe(
      Effect.as({})
    )
})

const program = Effect.gen(function* () {
  const toolkit = yield* UserToolkitLive

  const createResult = yield* toolkit.handle("CreateUser", {
    name: "Alice",
    email: "alice@example.com"
  })

  console.log("Created user:", createResult.result)

  const getResult = yield* toolkit.handle("GetUser", {
    userId: (createResult.result as any).id
  })

  console.log("Retrieved user:", getResult.result)

  const timeResult = yield* toolkit.handle("GetCurrentTime", {})

  console.log("Current time:", timeResult.result)
}).pipe(
  Effect.provide(DatabaseLive)
)
```

## Import Patterns

**CRITICAL**: Always use namespace imports:

```typescript
import * as Tool from "@effect/ai/Tool"
import * as Toolkit from "@effect/ai/Toolkit"
import * as Prompt from "@effect/ai/Prompt"
import { Schema, Effect, Data, Context, Layer } from "effect"

const myTool = Tool.make("example")
const myToolkit = Toolkit.make(myTool)
```

**NEVER** do this:

```typescript
import { make } from "@effect/ai/Tool"
import { make as makeToolkit } from "@effect/ai/Toolkit"
```

## Quality Checklist

### Mandatory - Every Tool

- [ ] Tool name is descriptive and unique
- [ ] Description explains what the tool does
- [ ] Parameters use Schema.Struct.Fields (not Schema.Struct)
- [ ] Success schema matches handler return type
- [ ] Failure schema includes all tagged errors
- [ ] failureMode matches recovery strategy
- [ ] Dependencies declared if accessing services
- [ ] Handler implements correct signature
- [ ] Type signatures use Tool.Parameters, Tool.Success, Tool.Failure

### Conditional - Include When Appropriate

- [ ] Tool.Readonly annotation for read-only tools
- [ ] Tool.Destructive annotation for mutating operations
- [ ] Tool.Idempotent annotation for safe retries
- [ ] Custom annotations via Tool.annotate
- [ ] Provider-defined tools for native provider features
- [ ] Toolkit.merge for combining tool collections
- [ ] Error handling with catchTag in handlers

## Common Patterns

### Validation in Handlers

```typescript
const ValidatedTool = Tool.make("validate", {
  parameters: {
    input: Schema.String
  },
  success: Schema.Struct({
    valid: Schema.Boolean,
    errors: Schema.Array(Schema.String)
  })
})

const toolkit = Toolkit.make(ValidatedTool)

const toolkitLayer = toolkit.toLayer({
  validate: ({ input }) =>
    Effect.gen(function* () {
      const errors: Array<string> = []

      if (input.length < 3) {
        errors.push("Input too short")
      }

      if (!/^[a-z]+$/.test(input)) {
        errors.push("Input must be lowercase letters")
      }

      return {
        valid: errors.length === 0,
        errors
      }
    })
})
```

### Async Operations in Handlers

```typescript
const FetchTool = Tool.make("fetch", {
  parameters: {
    url: Schema.String
  },
  success: Schema.String
})

const toolkit = Toolkit.make(FetchTool)

const toolkitLayer = toolkit.toLayer({
  fetch: ({ url }) =>
    Effect.tryPromise({
      try: () => fetch(url).then(r => r.text()),
      catch: (error) => new Error(`Fetch failed: ${error}`)
    })
})
```

### Conditional Tool Execution

```typescript
const ConditionalTool = Tool.make("process", {
  parameters: {
    mode: Schema.Literal("fast", "thorough")
  },
  success: Schema.String
})

const toolkit = Toolkit.make(ConditionalTool)

const toolkitLayer = toolkit.toLayer({
  process: ({ mode }) =>
    mode === "fast"
      ? Effect.succeed("Fast result")
      : Effect.gen(function* () {
          yield* Effect.sleep("1 second")
          return "Thorough result"
        })
})
```

## When to Use This Skill

- Building LLM integrations with tool calling
- Creating type-safe AI agent capabilities
- Implementing function calling for Claude/OpenAI
- Defining validated tool parameters and results
- Composing multiple tools into toolkits
- Managing tool handler dependencies
- Integrating provider-native tools (bash, web search)

## Key Principles Summary

1. **Tool.make** - Define tools with parameters, success, failure schemas
2. **Tool.fromTaggedRequest** - Create tools from TaggedRequest schemas
3. **Schema.Struct.Fields** - Parameters are field objects, not Schema.Struct
4. **Toolkit.make** - Compose multiple tools together
5. **toLayer** - Implement handlers returning Layer
6. **toContext** - Implement handlers returning Context
7. **toolkit.handle** - Execute tools with type-safe parameters
8. **HandlerResult** - Access typed result and encoded JSON
9. **failureMode** - Control error vs return failure strategy
10. **dependencies** - Declare service requirements
11. **Tool.providerDefined** - Use provider-native tools
12. **Namespace imports** - Always `import * as Tool`
13. **Prompt.makePart** - Create tool-call and tool-result parts with params

Your tool implementations should be type-safe, validated, and provide excellent developer experience with full schema support.

## Related Skills

- effect-ai-language-model - Using tools with generateText/streamText
- effect-ai-prompt - Tool call/result message integration
- effect-ai-streaming - Processing tool call streams
- effect-ai-provider - Provider-defined tools
