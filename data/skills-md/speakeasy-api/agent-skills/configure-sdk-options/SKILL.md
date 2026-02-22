---
name: configure-sdk-options
description: >-
  Use when CONFIGURING an existing SDK - NOT for initial generation.
  Covers gen.yaml configuration for all languages: TypeScript, Python, Go, Java, C#, PHP, Ruby.
  Also covers runtime overrides (retries, timeouts, server selection) in application code.
  Triggers on "configure SDK", "gen.yaml", "SDK options", "SDK config", "SDK configuration",
  "runtime override", "SDK client config", "override timeout", "per-call config".
  For NEW SDK generation, use start-new-sdk-project instead.
license: Apache-2.0
---

# Configure SDK Options

Configure gen.yaml options for an existing Speakeasy SDK. Supports TypeScript, Python, Go, Java, C#, PHP, and Ruby.

> **For new SDK projects**: Use `start-new-sdk-project` skill instead. This skill is for configuring an existing SDK.

## Language-Specific Guides

For comprehensive configuration details, see the language-specific guides:

| Language | Guide | Key Features |
|----------|-------|--------------|
| TypeScript | [content/languages/typescript.md](content/languages/typescript.md) | Zod validation, React Query, standalone functions, dual module format |
| Python | [content/languages/python.md](content/languages/python.md) | Pydantic models, async modes (both/split), uv/poetry support |
| Go | [content/languages/go.md](content/languages/go.md) | Response formats, interface generation, K8s integration |
| Java | [content/languages/java.md](content/languages/java.md) | Builder pattern, Gradle customization, Maven Central publishing |
| C# | [content/languages/csharp.md](content/languages/csharp.md) | Async/await, cancellation tokens, DI integration, NuGet |
| PHP | [content/languages/php.md](content/languages/php.md) | Laravel integration, Guzzle config, Packagist publishing |
| Ruby | [content/languages/ruby.md](content/languages/ruby.md) | Sorbet typing, Rails integration, RubyGems publishing |

These guides include detailed configuration options, code examples, framework integrations, and publishing instructions.

## When to Use

- Configuring language-specific gen.yaml options on an existing SDK
- Setting up SDK hooks, async patterns, or publishing
- Configuring runtime behavior (retries, timeouts, server selection) in application code
- User says: "configure SDK", "gen.yaml options", "SDK config", "runtime override", "per-call config"
- User asks about: Zod, Pydantic, NuGet, PyPI, npm, Maven Central, Packagist, RubyGems

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Existing SDK | Yes | SDK with `.speakeasy/workflow.yaml` already created |
| Target language | Yes | TypeScript, Python, Go, Java, C#, PHP, or Ruby |

## Outputs

| Output | Description |
|--------|-------------|
| Updated gen.yaml | Language-specific configuration |
| Hook files | Custom hooks if enabled |

## Prerequisites

You must have an existing SDK with `.speakeasy/workflow.yaml`. If not, run:

```bash
speakeasy quickstart --skip-interactive --output console \
  -s openapi.yaml -t <language> -n "MySDK" -p "<package-name>"
```

## Common Configuration (All Languages)

These options apply to all SDK targets in gen.yaml:

```yaml
<language>:
  version: 1.0.0
  packageName: "my-sdk"

  # Method signatures
  maxMethodParams: 4              # Params before request object
  flatteningOrder: parameters-first

  # Error handling
  responseFormat: flat            # or "envelope" (Go)
  clientServerStatusCodesAsErrors: true
```

## TypeScript Configuration

```yaml
typescript:
  version: 1.0.0
  packageName: "@myorg/my-sdk"
  moduleFormat: dual              # esm, commonjs, or dual
  zodVersion: v4-mini             # v3, v4, or v4-mini
  enableCustomCodeRegions: true   # For custom code
  enableReactQuery: true          # React Query hooks
```

| Feature | Notes |
|---------|-------|
| Zod validation | Automatic for all models |
| Tree-shaking | Use `moduleFormat: dual` + standalone functions |
| JSR publishing | Create `jsr.json`, run `deno publish` |
| npm publishing | Standard `npm publish` |

**Standalone functions for tree-shaking:**
```typescript
import { TodoCore } from "my-sdk/core.js";
import { todosCreate } from "my-sdk/funcs/todosCreate.js";
const sdk = new TodoCore({ apiKey: "..." });
```

## Python Configuration

```yaml
python:
  version: 1.0.0
  packageName: "my-sdk"
  asyncMode: both                 # both or split
  packageManager: uv              # uv or poetry
  envVarPrefix: ""                # Prefix for env config
```

| Feature | Notes |
|---------|-------|
| Pydantic models | Automatic for all models |
| Async mode `both` | `sdk.method()` and `sdk.method_async()` |
| Async mode `split` | `SDK()` and `AsyncSDK()` constructors |
| PyPI publishing | `uv publish` or `poetry publish` |

**Async patterns:**
```python
# asyncMode: both (default)
result = sdk.users.list()           # sync
result = await sdk.users.list_async() # async

# asyncMode: split
sdk = MySDK()                       # sync only
async_sdk = AsyncMySDK()            # async only
```

## Go Configuration

```yaml
go:
  version: 0.1.0
  packageName: github.com/myorg/my-sdk
  maxMethodParams: 2
  methodArguments: require-security-and-request
  responseFormat: envelope
  flattenGlobalSecurity: true
```

| Feature | Notes |
|---------|-------|
| Interfaces | Generate with ifacemaker |
| Mocks | Generate with mockery |
| K8s integration | Add kubebuilder markers, run controller-gen |

**Interface generation for testing:**
```bash
go install github.com/vburenin/ifacemaker@latest
go install github.com/vektra/mockery/v2@latest
ifacemaker --file consumers.go --struct Consumers --iface ConsumersSDK --output consumers_i.go
mockery
```

## Java Configuration

```yaml
java:
  version: 1.0.0
  groupID: com.myorg
  artifactID: my-sdk
  packageName: com.myorg.mysdk
  methodArguments: require-security-and-request
```

| Feature | Notes |
|---------|-------|
| Builder pattern | Automatic for all classes |
| Build customization | Use `build-extras.gradle` (preserved) |
| Maven Central | `./gradlew publishToSonatype closeAndReleaseSonatypeStagingRepository` |

**Client usage:**
```java
MySdk sdk = MySdk.builder()
    .security(Security.builder().apiKey("key").build())
    .build();
```

## C# Configuration

```yaml
csharp:
  version: 1.0.0
  packageName: MyOrg.MySDK
  dotnetVersion: "6.0"
  baseErrorName: MySDKException
```

| Feature | Notes |
|---------|-------|
| Async/await | All operations async by default |
| SSE streaming | `EventStream<T>` support |
| NuGet publishing | `dotnet pack -c Release && dotnet nuget push` |

**Async with cancellation:**
```csharp
var cts = new CancellationTokenSource(TimeSpan.FromSeconds(30));
var result = await sdk.Users.ListAsync(cancellationToken: cts.Token);
```

## PHP Configuration

```yaml
php:
  version: 1.0.0
  packageName: myorg/my-sdk
  namespace: MyOrg\MySDK
```

| Feature | Notes |
|---------|-------|
| PHP 8.2+ | Required minimum version |
| Guzzle | HTTP client (configurable timeout) |
| Packagist | Tag release, register on Packagist.org |

**Security callback for token refresh:**
```php
$sdk = MySDK\MySDK::builder()
    ->setSecuritySource(fn() => getTokenFromCache() ?? refreshToken())
    ->build();
```

## Ruby Configuration

```yaml
ruby:
  version: 1.0.0
  packageName: my-sdk
  module: MySdk
  typingStrategy: sorbet          # sorbet or none
```

| Feature | Notes |
|---------|-------|
| Sorbet typing | Optional, enable with `typingStrategy: sorbet` |
| Faraday | HTTP client |
| RubyGems | `gem build && gem push` |

## SDK Hooks (All Languages)

Enable custom hooks with `enableCustomCodeRegions: true`. Hook files are preserved across regeneration.

| Language | Hook Location |
|----------|---------------|
| TypeScript | `src/hooks/` |
| Python | `src/<pkg>/_hooks/` |
| Go | `internal/hooks/` |
| Java | `src/main/java/.../hooks/` |
| C# | `src/.../Hooks/` |
| PHP | `src/Hooks/` |
| Ruby | `lib/.../sdk_hooks/` |

See `customize-sdk-hooks` skill for detailed hook implementation.

## Runtime Overrides

Runtime behavior can be configured at SDK instantiation or per-call. These override gen.yaml defaults.

### Server Selection

Define server IDs in OpenAPI spec, then select at runtime:

```yaml
# OpenAPI spec
servers:
  - url: https://api.example.com
    x-speakeasy-server-id: production
  - url: https://sandbox.example.com
    x-speakeasy-server-id: sandbox
```

| Language | SDK Constructor | Custom URL |
|----------|-----------------|------------|
| TypeScript | `new SDK({ server: "sandbox" })` | `new SDK({ serverURL: "..." })` |
| Python | `SDK(server="sandbox")` | `SDK(server_url="...")` |
| Go | `SDK.New(SDK.WithServer("sandbox"))` | `SDK.WithServerURL("...")` |

### Retry Overrides

Override retry behavior per-call (spec defaults set via `x-speakeasy-retries`):

**TypeScript:**
```typescript
const res = await sdk.payments.create({ amount: 1000 }, {
  retries: {
    strategy: "backoff",
    backoff: { initialInterval: 1000, maxInterval: 30000, maxElapsedTime: 120000, exponent: 2.0 },
    retryConnectionErrors: true,
  },
});
```

**Python:**
```python
from sdk.utils import BackoffStrategy, RetryConfig
res = sdk.payments.create(amount=1000, retries=RetryConfig("backoff",
    backoff=BackoffStrategy(1000, 30000, 120000, 2.0), retry_connection_errors=True))
```

**Go:**
```go
res, err := sdk.Payments.Create(ctx, req, operations.WithRetries(retry.Config{
    Strategy: "backoff", Backoff: &retry.BackoffStrategy{
        InitialInterval: 1000, MaxInterval: 30000, MaxElapsedTime: 120000, Exponent: 2.0},
    RetryConnectionErrors: true}))
```

### Timeout Overrides

Set global timeout on SDK constructor, or per-call:

| Language | Global | Per-call |
|----------|--------|----------|
| TypeScript | `new SDK({ timeoutMs: 30000 })` | `sdk.op({}, { timeoutMs: 60000 })` |
| Python | `SDK(timeout_ms=30000)` | `sdk.op(timeout_ms=60000)` |
| Go | `SDK.WithTimeoutMs(30000)` | `operations.WithTimeoutMs(60000)` |

### Pagination Usage

SDK auto-generates pagination helpers when `x-speakeasy-pagination` is set in spec:

```typescript
// Auto-iterate all pages
for await (const user of await sdk.users.list({ limit: 50 })) {
  console.log(user.name);
}

// Manual pagination
let page = await sdk.users.list({ limit: 50 });
while (page) {
  for (const user of page.data) { console.log(user.name); }
  page = await page.next();
}
```

## Decision Framework

| Situation | Action |
|-----------|--------|
| Need tree-shaking (TS) | Set `moduleFormat: dual`, use standalone functions |
| Need async/sync (Python) | Set `asyncMode: both` (default) |
| Need separate async client | Set `asyncMode: split` (Python) |
| Need interfaces for testing (Go) | Use ifacemaker + mockery |
| Need custom build config (Java) | Edit `build-extras.gradle` |
| Need runtime retry override | Pass `retries` config in per-call options |
| Need runtime timeout override | Set `timeoutMs` on constructor or per-call |
| Need server switching | Use `x-speakeasy-server-id` in spec, select at runtime |

## What NOT to Do

- **Do NOT** use this skill for initial SDK generation - use `start-new-sdk-project`
- **Do NOT** edit generated files outside custom code regions
- **Do NOT** modify files in `src/` that aren't in preserved directories (hooks, extra)

## Troubleshooting

| Language | Issue | Solution |
|----------|-------|----------|
| TypeScript | Bundle too large | Use standalone functions |
| Python | Async pagination blocking | Enable `fixFlags.asyncPaginationSep2025: true` |
| Go | Interface not generated | Ensure struct is exported (capitalized) |
| Java | Gradle sync fails | Run `./gradlew --refresh-dependencies` |
| C# | Async deadlock | Use `await` not `.Result` |
| PHP | PHP version error | Requires PHP 8.2+ |
| Ruby | Sorbet errors | Run `bundle exec tapioca gems` |
| All | Retries not working | Ensure `x-speakeasy-retries` at document root or operation level |
| All | Server ID not recognized | Add `x-speakeasy-server-id` to each server entry |
| All | Pagination `next()` undefined | Add `x-speakeasy-pagination` to the list operation |

## After Making Changes

After modifying gen.yaml configuration, **prompt the user** to regenerate the SDK:

> **Configuration complete.** Would you like to regenerate the SDK now with `speakeasy run`?

If the user confirms, run:

```bash
speakeasy run --output console
```

Changes to gen.yaml only take effect after regeneration.

## Related Skills

- `start-new-sdk-project` - Initial SDK generation
- `customize-sdk-hooks` - Detailed hook implementation
- `manage-openapi-overlays` - Spec customization
