---
name: laravel-mcp
description: Laravel v12 - The PHP Framework For Web Artisans (project, gitignored)
---

# Laravel MCP Skill

Comprehensive assistance with Laravel MCP (Model Context Protocol) development. Laravel MCP provides a simple and elegant way for AI clients to interact with your Laravel application through the Model Context Protocol, enabling you to define servers, tools, resources, and prompts for AI-powered interactions.

## When to Use This Skill

This skill should be triggered when:
- Building MCP servers for Laravel applications
- Creating AI tools that perform actions in Laravel
- Defining reusable prompts for AI interactions
- Exposing Laravel resources (data/content) to AI clients
- Implementing OAuth 2.1 or Sanctum authentication for MCP
- Registering and configuring MCP routes (web or local)
- Testing MCP servers and tools
- Working with Laravel JSON Schema builder for tool inputs
- Implementing streaming responses or progress notifications
- Building AI-powered Laravel features using MCP

## Key Concepts

### Core Components

**MCP Server**: The central communication point that exposes MCP capabilities. Each server has:
- `name`: Server identifier
- `version`: Server version
- `instructions`: Description of the server's purpose
- `tools`: Array of tool classes
- `resources`: Array of resource classes
- `prompts`: Array of prompt classes

**Tools**: Enable AI clients to perform actions. Tools can:
- Define input schemas using Laravel's JSON Schema builder
- Validate arguments with Laravel validation rules
- Support dependency injection
- Return single or multiple responses
- Stream responses using generators
- Use annotations like `#[IsReadOnly]` and `#[IsIdempotent]`

**Prompts**: Reusable prompt templates that provide a standardized way to structure common queries with argument definitions and validation.

**Resources**: Enable your server to expose data and content that AI clients can read, including text and blob responses with customizable MIME types and URIs.

## Quick Reference

### 1. Basic MCP Server Definition

```php
<?php
namespace App\Mcp\Servers;

use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    protected string $name = 'Weather Server';
    protected string $version = '1.0.0';
    protected string $instructions = 'This server provides weather information and forecasts.';

    protected array $tools = [
        // CurrentWeatherTool::class,
    ];

    protected array $resources = [
        // WeatherGuidelinesResource::class,
    ];

    protected array $prompts = [
        // DescribeWeatherPrompt::class,
    ];
}
```

### 2. Tool with Input Schema

```php
<?php
namespace App\Mcp\Tools;

use Illuminate\JsonSchema\JsonSchema;
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    protected string $description = 'Fetches the current weather forecast for a specified location.';

    public function handle(Request $request): Response
    {
        $location = $request->get('location');
        // Get weather...
        return Response::text('The weather is...');
    }

    public function schema(JsonSchema $schema): array
    {
        return [
            'location' => $schema->string()
                ->description('The location to get the weather for.')
                ->required(),
        ];
    }
}
```

### 3. Tool with Validation

```php
public function handle(Request $request): Response
{
    $validated = $request->validate([
        'location' => 'required|string|max:100',
        'units' => 'in:celsius,fahrenheit',
    ], [
        'location.required' => 'You must specify a location.',
        'units.in' => 'You must specify either "celsius" or "fahrenheit".',
    ]);
    // Fetch weather data...
}
```

### 4. Tool with Dependency Injection

```php
<?php
namespace App\Mcp\Tools;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    public function __construct(
        protected WeatherRepository $weather,
    ) {}

    public function handle(Request $request, WeatherRepository $weather): Response
    {
        $location = $request->get('location');
        $forecast = $weather->getForecastFor($location);
        // ...
    }
}
```

### 5. Tool with Annotations

```php
<?php
namespace App\Mcp\Tools;

use Laravel\Mcp\Server\Tools\Annotations\IsIdempotent;
use Laravel\Mcp\Server\Tools\Annotations\IsReadOnly;
use Laravel\Mcp\Server\Tool;

#[IsIdempotent]
#[IsReadOnly]
class CurrentWeatherTool extends Tool
{
    // ...
}
```

### 6. Streaming Tool Response

```php
<?php
namespace App\Mcp\Tools;

use Generator;
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    public function handle(Request $request): Generator
    {
        $locations = $request->array('locations');

        foreach ($locations as $index => $location) {
            yield Response::notification('processing/progress', [
                'current' => $index + 1,
                'total' => count($locations),
                'location' => $location,
            ]);
            yield Response::text($this->forecastFor($location));
        }
    }
}
```

### 7. Prompt Definition

```php
<?php
namespace App\Mcp\Prompts;

use Laravel\Mcp\Server\Prompt;
use Laravel\Mcp\Server\Prompts\Argument;

class DescribeWeatherPrompt extends Prompt
{
    protected string $description = 'Generates a natural-language explanation of the weather.';

    public function arguments(): array
    {
        return [
            new Argument(
                name: 'tone',
                description: 'The tone to use in the weather description.',
                required: true,
            ),
        ];
    }

    public function handle(Request $request): array
    {
        $tone = $request->string('tone');
        return [
            Response::text("You are a weather assistant. Provide a {$tone} tone.")->asAssistant(),
            Response::text("What is the current weather like in New York City?"),
        ];
    }
}
```

### 8. Resource Definition

```php
<?php
namespace App\Mcp\Resources;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    protected string $description = 'Comprehensive guidelines for using the Weather API.';
    protected string $uri = 'weather://resources/guidelines';
    protected string $mimeType = 'application/pdf';

    public function handle(Request $request): Response
    {
        return Response::text($weatherData);
    }
}
```

### 9. Server Registration (Web)

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/weather', WeatherServer::class);

// With middleware
Mcp::web('/mcp/weather', WeatherServer::class)
    ->middleware(['throttle:mcp']);
```

### 10. Server Registration (Local)

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::local('weather', WeatherServer::class);
```

### 11. OAuth 2.1 Authentication Setup

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::oauthRoutes();

Mcp::web('/mcp/weather', WeatherExample::class)
    ->middleware('auth:api');
```

### 12. Sanctum Authentication

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/demo', WeatherExample::class)
    ->middleware('auth:sanctum');
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **other.md** - Complete Laravel MCP documentation from Laravel 12.x official docs, including:
  - Installation and setup instructions
  - Server, tool, resource, and prompt creation
  - Input schema definition using JSON Schema builder
  - Validation and dependency injection
  - Streaming responses and progress notifications
  - Authentication (OAuth 2.1 and Sanctum)
  - Registration (web and local routes)
  - Testing and inspection

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners

Start by understanding the core concepts:
1. **Installation**: Install Laravel MCP via `composer require laravel/mcp`
2. **Setup**: Run `php artisan vendor:publish --tag=ai-routes` to create `routes/ai.php`
3. **First Server**: Generate your first server with `php artisan make:mcp-server`
4. **Register**: Add your server to `routes/ai.php` using `Mcp::web()` or `Mcp::local()`

Begin with simple read-only tools using the `#[IsReadOnly]` annotation before moving to tools that modify data.

### For Intermediate Users

Focus on building robust tools:
- Use JSON Schema builder for precise input validation
- Leverage Laravel's validation rules for complex constraints
- Implement dependency injection for clean, testable code
- Use prompts to create reusable AI interaction patterns
- Expose resources to provide context to AI clients

### For Advanced Users

Implement production-ready features:
- Add OAuth 2.1 or Sanctum authentication to secure your MCP servers
- Use streaming responses for long-running operations with progress notifications
- Apply middleware for rate limiting and custom authentication
- Create idempotent tools using `#[IsIdempotent]` annotation
- Build complex multi-tool workflows
- Use the MCP Inspector for debugging and testing

### Navigation Tips

- **Quick implementation**: Use the Quick Reference section above for common patterns
- **Detailed learning**: Read `references/other.md` for comprehensive documentation
- **Examples**: All code examples include proper namespaces and imports
- **Testing**: Refer to documentation for MCP Inspector usage and unit testing

## Common Patterns

### Creating a New MCP Server

```bash
# Generate server class
php artisan make:mcp-server WeatherServer

# Edit app/Mcp/Servers/WeatherServer.php
# Add tools, resources, and prompts

# Register in routes/ai.php
Mcp::web('/mcp/weather', WeatherServer::class);
```

### Input Schema Patterns

```php
// Simple required string
'location' => $schema->string()->required()

// Optional with default
'units' => $schema->string()->default('celsius')

// Number with constraints
'temperature' => $schema->number()->minimum(0)->maximum(100)

// Array of items
'cities' => $schema->array()->items($schema->string())

// Object with properties
'forecast' => $schema->object()->properties([
    'temperature' => $schema->number(),
    'humidity' => $schema->number(),
])
```

### Response Patterns

```php
// Text response
return Response::text('The weather is sunny');

// Multiple responses
return [
    Response::text('First message'),
    Response::text('Second message'),
];

// Notification (streaming)
yield Response::notification('processing/progress', ['status' => 'processing']);
```

## Resources

### Installation

```bash
composer require laravel/mcp
php artisan vendor:publish --tag=ai-routes
```

### Official Documentation

- **Laravel MCP Docs**: https://laravel.com/docs/12.x/mcp
- **Model Context Protocol Spec**: https://modelcontextprotocol.io/

### Related Laravel Features

- **JSON Schema Builder**: For defining tool input schemas
- **Validation**: For validating tool arguments
- **Service Container**: For dependency injection in tools and resources
- **OAuth/Sanctum**: For authentication

## Notes

- This skill was generated from official Laravel 12.x MCP documentation
- All code examples use proper PHP 8+ syntax with typed properties
- Examples demonstrate Laravel's elegant API design
- Tools support both synchronous and streaming responses
- Authentication is optional but recommended for production use
- Both web (HTTP) and local (CLI) server registration are supported

## Tips & Best Practices

1. **Start Simple**: Begin with read-only tools marked with `#[IsReadOnly]`
2. **Validate Input**: Always define schemas and use validation for user input
3. **Use DI**: Leverage dependency injection for repositories and services
4. **Stream Progress**: For long operations, use generators to stream progress
5. **Secure Your Servers**: Add authentication middleware for production
6. **Test Thoroughly**: Use the MCP Inspector and unit tests to validate functionality
7. **Document Well**: Write clear descriptions for servers, tools, prompts, and resources
8. **Follow Conventions**: Use Laravel's service container patterns and naming conventions
