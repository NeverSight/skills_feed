---
name: logging
description: Structured logging patterns for the 3SC widget host. Covers Serilog configuration, log levels, correlation IDs, sensitive data handling, and diagnostic contexts.
---

# Logging

## Overview

Effective logging is essential for debugging, monitoring, and understanding application behavior. This skill covers structured logging patterns using Serilog.

## Definition of Done (DoD)

- [ ] All significant operations are logged with appropriate level
- [ ] Logs include correlation IDs for request tracing
- [ ] Sensitive data is never logged (passwords, tokens, PII)
- [ ] Log messages are structured (use templates, not string concatenation)
- [ ] Errors include exception details and context
- [ ] Log levels are appropriate (not everything is Warning/Error)

## Log Levels Guide

| Level | When to Use | Example |
|-------|-------------|---------|
| **Verbose** | Detailed debugging only | Method entry/exit, loop iterations |
| **Debug** | Development diagnostics | Parameter values, state changes |
| **Information** | Normal operations | Startup, shutdown, user actions |
| **Warning** | Unexpected but handled | Retry attempted, fallback used |
| **Error** | Operation failed | Exception caught, feature unavailable |
| **Fatal** | App cannot continue | Startup failure, critical resource missing |

## Structured Logging

### Do's and Don'ts

```csharp
// ❌ BAD - String interpolation loses structure
Log.Information($"User {userId} loaded widget {widgetId}");

// ❌ BAD - String concatenation
Log.Information("User " + userId + " loaded widget " + widgetId);

// ✅ GOOD - Message template with named properties
Log.Information("User {UserId} loaded widget {WidgetId}", userId, widgetId);

// ✅ GOOD - Destructure complex objects
Log.Information("Widget loaded: {@Widget}", widget);

// ✅ GOOD - Stringify instead of destructure for simple representation
Log.Information("Position changed to {$Position}", position);
```

### Property Naming

```csharp
// Use PascalCase for consistency
Log.Information("Widget {WidgetKey} installed by {UserName}", key, user);

// Prefix counts/durations with descriptive names
Log.Information("Loaded {WidgetCount} widgets in {LoadDurationMs}ms", count, elapsed);

// Use consistent names across the codebase
// - WidgetKey, not WidgetId or Key
// - UserId, not User or UserID
// - DurationMs, not Time or Elapsed
```

## Correlation Context

### Setting Correlation ID

```csharp
public static class CorrelationContext
{
    private static readonly AsyncLocal<string?> CurrentId = new();
    
    public static string? Current => CurrentId.Value;
    
    public static IDisposable BeginScope(string? correlationId = null)
    {
        var id = correlationId ?? GenerateId();
        var previous = CurrentId.Value;
        CurrentId.Value = id;
        
        // Push to Serilog context
        return new CorrelationScope(previous, LogContext.PushProperty("CorrelationId", id));
    }
    
    private static string GenerateId() => Guid.NewGuid().ToString("N")[..8];
    
    private class CorrelationScope : IDisposable
    {
        private readonly string? _previous;
        private readonly IDisposable _logContext;
        
        public CorrelationScope(string? previous, IDisposable logContext)
        {
            _previous = previous;
            _logContext = logContext;
        }
        
        public void Dispose()
        {
            CurrentId.Value = _previous;
            _logContext.Dispose();
        }
    }
}
```

### Using Correlation

```csharp
[RelayCommand]
private async Task InstallWidgetAsync(WidgetPackage package, CancellationToken ct)
{
    using var _ = CorrelationContext.BeginScope($"install-{package.PackageId}");
    
    Log.Information("Starting widget installation: {PackageId}", package.PackageId);
    
    try
    {
        await _installer.InstallAsync(package, ct);
        Log.Information("Widget installation completed: {PackageId}", package.PackageId);
    }
    catch (Exception ex)
    {
        Log.Error(ex, "Widget installation failed: {PackageId}", package.PackageId);
        throw;
    }
}
```

## Operation Logging

### Timed Operations

```csharp
public class OperationLogger : IDisposable
{
    private readonly string _operationName;
    private readonly Stopwatch _stopwatch;
    private readonly IDisposable _logContext;
    private bool _completed;
    
    private OperationLogger(string operationName, params (string Key, object Value)[] properties)
    {
        _operationName = operationName;
        _stopwatch = Stopwatch.StartNew();
        
        var enrichers = properties
            .Select(p => LogContext.PushProperty(p.Key, p.Value))
            .ToList();
        
        _logContext = new CompositeDisposable(enrichers);
        
        Log.Debug("Operation started: {OperationName}", operationName);
    }
    
    public static OperationLogger Begin(string operationName, params (string, object)[] properties)
        => new(operationName, properties);
    
    public void Complete()
    {
        _completed = true;
        Log.Information(
            "Operation completed: {OperationName} in {DurationMs}ms",
            _operationName, _stopwatch.ElapsedMilliseconds);
    }
    
    public void Dispose()
    {
        _stopwatch.Stop();
        
        if (!_completed)
        {
            Log.Warning(
                "Operation abandoned: {OperationName} after {DurationMs}ms",
                _operationName, _stopwatch.ElapsedMilliseconds);
        }
        
        _logContext.Dispose();
    }
}

// Usage
public async Task ProcessWidgetsAsync(CancellationToken ct)
{
    using var op = OperationLogger.Begin("ProcessWidgets", ("Count", widgets.Count));
    
    foreach (var widget in widgets)
    {
        await ProcessAsync(widget, ct);
    }
    
    op.Complete();
}
```

## Sensitive Data Handling

### Never Log These

```csharp
// ❌ NEVER log sensitive data
Log.Information("User logged in with password: {Password}", password);
Log.Information("API Key: {ApiKey}", apiKey);
Log.Information("Token: {Token}", accessToken);
Log.Information("SSN: {SSN}", socialSecurityNumber);

// ✅ Log existence, not value
Log.Information("User logged in: {Username}", username);
Log.Information("API Key configured: {HasApiKey}", !string.IsNullOrEmpty(apiKey));
Log.Information("Token received: {TokenLength} characters", token?.Length ?? 0);
```

### Masking Helper

```csharp
public static class LogSanitizer
{
    public static string Mask(string? value, int visibleChars = 4)
    {
        if (string.IsNullOrEmpty(value))
            return "[empty]";
        
        if (value.Length <= visibleChars * 2)
            return new string('*', value.Length);
        
        return value[..visibleChars] + new string('*', value.Length - visibleChars * 2) + value[^visibleChars..];
    }
    
    public static string MaskPath(string path)
    {
        var userProfile = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
        return path.Replace(userProfile, "[USER]");
    }
}

// Usage
Log.Information("Credential stored for: {MaskedKey}", LogSanitizer.Mask(apiKey));
Log.Error(ex, "Failed to read file: {Path}", LogSanitizer.MaskPath(filePath));
```

## Logger Adapter

For infrastructure code that needs ILogger<T>:

```csharp
public class SerilogLoggerAdapter<T> : ILogger<T>
{
    private readonly Serilog.ILogger _logger;
    
    public SerilogLoggerAdapter()
    {
        _logger = Serilog.Log.ForContext<T>();
    }
    
    public void Log(LogLevel logLevel, string message, params object[] args)
    {
        var serilogLevel = logLevel switch
        {
            LogLevel.Trace => LogEventLevel.Verbose,
            LogLevel.Debug => LogEventLevel.Debug,
            LogLevel.Information => LogEventLevel.Information,
            LogLevel.Warning => LogEventLevel.Warning,
            LogLevel.Error => LogEventLevel.Error,
            LogLevel.Critical => LogEventLevel.Fatal,
            _ => LogEventLevel.Information
        };
        
        _logger.Write(serilogLevel, message, args);
    }
    
    public void LogError(Exception ex, string message, params object[] args)
    {
        _logger.Error(ex, message, args);
    }
    
    // ... other interface methods
}
```

## Serilog Configuration

### Development

```csharp
Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Debug()
    .MinimumLevel.Override("Microsoft", LogEventLevel.Warning)
    .MinimumLevel.Override("System", LogEventLevel.Warning)
    .Enrich.FromLogContext()
    .Enrich.WithMachineName()
    .Enrich.WithThreadId()
    .WriteTo.Debug(outputTemplate: 
        "[{Timestamp:HH:mm:ss} {Level:u3}] {CorrelationId} {Message:lj}{NewLine}{Exception}")
    .WriteTo.File(
        path: "logs/3sc-.log",
        rollingInterval: RollingInterval.Day,
        retainedFileCountLimit: 7,
        outputTemplate: 
            "{Timestamp:yyyy-MM-dd HH:mm:ss.fff} [{Level:u3}] {CorrelationId} {Message:lj}{NewLine}{Exception}")
    .CreateLogger();
```

### Production

```csharp
Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Information()
    .MinimumLevel.Override("Microsoft", LogEventLevel.Warning)
    .MinimumLevel.Override("System", LogEventLevel.Warning)
    .Enrich.FromLogContext()
    .Enrich.WithMachineName()
    .WriteTo.File(
        path: Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            "3SC", "logs", "3sc-.log"),
        rollingInterval: RollingInterval.Day,
        retainedFileCountLimit: 30,
        fileSizeLimitBytes: 50_000_000,  // 50MB
        outputTemplate: 
            "{Timestamp:yyyy-MM-dd HH:mm:ss.fff} [{Level:u3}] [{CorrelationId}] {Message:lj}{NewLine}{Exception}")
    .CreateLogger();
```

## Best Practices

| Practice | Reason |
|----------|--------|
| Use message templates | Enables structured querying |
| Include correlation IDs | Trace operations across components |
| Log at appropriate levels | Don't flood with noise |
| Time long operations | Performance visibility |
| Context over comments | Logs explain what code is doing |
| Consistent property names | Enables aggregation |

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| String interpolation | Loses structure | Use message templates |
| Logging in hot paths | Performance impact | Sample or disable |
| Swallowing exceptions | Hidden failures | Always log errors |
| PII in logs | Security/compliance | Mask sensitive data |
| ToString() in logs | Allocations even when filtered | Let Serilog handle |

## References

- [Serilog Best Practices](https://benfoster.io/blog/serilog-best-practices/)
- [Structured Logging](https://messagetemplates.org/)
