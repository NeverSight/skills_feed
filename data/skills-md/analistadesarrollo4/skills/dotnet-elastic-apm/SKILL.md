---
name: dotnet-elastic-apm
description: "Elasticsearch and Elastic APM integration with Serilog structured logging for .NET applications. Use when: (1) Implementing or configuring Serilog with Elasticsearch sink, (2) Setting up Elastic APM with data streams and authentication, (3) Creating logging extension methods in Infrastructure layer, (4) Enriching logs with app-name and app-type properties, (5) Configuring log levels and environment-specific logging, (6) Questions about logging security (PII, credentials), or (7) Troubleshooting observability and monitoring setup."
---

# Elasticsearch and Elastic APM Integration

## Logging and Observability Standards

- **Logging Standard**: All logging must be implemented using **Serilog** with structured logging.
- **Centralized Destination**: All logs must be centralized in **Elasticsearch**, using Elastic APM authentication and Data Streams configuration.
- **Enriched Information**: Logs must be enriched with context properties such as `app-name` and `app-type`.
- **Bootstrapping**: Serilog initialization must be **COMPLETELY OMITTED IN `Program.cs`** and performed through an **Extension Method** from the Infrastructure layer.

## Security and Data Privacy

- **Sensitive Information**: **PII (Personally Identifiable Information), credentials, and tokens must NEVER be logged**.
- Sanitize sensitive data before logging.
- Use log filters to exclude sensitive endpoints or data.

## Serilog Configuration Extension Method

Create an extension method in `Infrastructure/Extensions/ExtensionLogging.cs`:

```csharp
using Serilog;
using Serilog.Events;
using Serilog.Sinks.Elasticsearch;
using Elastic.Ingest.Elasticsearch.DataStreams;
using Elastic.Ingest.Elasticsearch;
using Elastic.Transport;

namespace Infrastructure.Extensions
{
    /// <summary>
    /// Extension class for configuring Serilog with Elasticsearch and Elastic APM.
    /// </summary>
    public static class ExtensionLogging
    {
        /// <summary>
        /// Configures Serilog with Elasticsearch using Elastic APM.
        /// </summary>
        /// <param name="configuration">Application configuration.</param>
        public static void AddLog(IConfiguration configuration)
        {
            string? elasticUrl = configuration.GetValue<string>("Global:Elastic:Url");
            string? environment = configuration.GetValue<string>("Global:Elastic:Env");
            string? elasticUser = configuration.GetValue<string>("Global:Elastic:User");
            string? elasticPass = configuration.GetValue<string>("Global:Elastic:Pass");
            string? logLevelEnv = configuration.GetValue<string>("Global:Elastic:LogLevel");

            LogEventLevel logEventLevel = (LogEventLevel)int.Parse(logLevelEnv!);

            Log.Logger = new LoggerConfiguration()
                .Enrich.FromLogContext()
                .Enrich.WithProperty("app-name", configuration.GetSection("Elastic").GetValue<string>("app-name"))
                .Enrich.WithProperty("app-type", configuration.GetSection("Elastic").GetValue<string>("app-type"))
                .WriteTo.Console()
                .WriteTo.Elasticsearch([new Uri(elasticUrl!)], opts =>
                {
                    // Use DataStream for Elastic APM compatibility
                    opts.DataStream = new DataStreamName("app", environment!, "logs");
                    opts.BootstrapMethod = BootstrapMethod.None;
                    opts.MinimumLevel = logEventLevel;
                }, transport =>
                {
                    // Basic Authentication
                    transport.Authentication(new BasicAuthentication(elasticUser!, elasticPass!));
                    // Callback to accept certificates (e.g., in development)
                    transport.ServerCertificateValidationCallback((a, b, c, d) => true);
                })
                .CreateLogger();
        }
    }
}
```

## Program.cs Configuration

Configure Serilog and Elastic APM in `Program.cs` only for development:

```csharp
if (app.Environment.IsDevelopment())
{
    builder.Services.AddLogging(loggingBuilder => loggingBuilder.AddSerilog(dispose: true));
    ExtensionLogging.AddLog(builder.Configuration);
    builder.Services.AddAllElasticApm();
}
```

## Required NuGet Packages

- **Serilog.AspNetCore**
- **Serilog.Sinks.Elasticsearch**
- **Elastic.Apm.NetCoreAll**
- **Elastic.Ingest.Elasticsearch**
- **Elastic.Ingest.Elasticsearch.DataStreams**
- **Elastic.Transport**

## Configuration Settings (appsettings.json)

```json
{
  "Elastic": {
    "app-name": "your-app-name",
    "app-type": "api",
    "Url": "https://your-elastic-url:9200",
    "Env": "development",
    "User": "elastic_user",
    "Pass": "elastic_password",
    "LogLevel": "2"
  }
}
```

## Log Level Values

- 0 = Verbose
- 1 = Debug
- 2 = Information
- 3 = Warning
- 4 = Error
- 5 = Fatal

## Best Practices

- Use structured logging with named properties: `Log.Information("User {UserId} logged in", userId);`
- Avoid string interpolation in log messages.
- Use log context to enrich logs with request-specific data.
- Configure appropriate log levels for different environments.
- Monitor APM metrics alongside logs for complete observability.
