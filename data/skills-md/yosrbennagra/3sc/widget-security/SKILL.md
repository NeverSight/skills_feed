---
name: widget-security
description: Security patterns for loading and running third-party widgets in the 3SC host. Covers sandboxing, permissions, code signing, and trust levels.
---

# Widget Security

## Overview

Widgets are third-party code that runs within the 3SC application. This skill covers how to safely load, validate, and run widgets while protecting the user's system.

## Security Model

```
┌─────────────────────────────────────────────────────────────┐
│                      Trust Levels                           │
├─────────────────────────────────────────────────────────────┤
│  Built-in Widgets     │ Full trust, bundled with app        │
│  Signed Widgets       │ Verified publisher, permission-based│
│  Community Widgets    │ User consent required, sandboxed    │
│  Unknown Widgets      │ Blocked by default                  │
└─────────────────────────────────────────────────────────────┘
```

## Definition of Done (DoD)

- [ ] Widget manifests validated before loading
- [ ] Unsigned widgets require explicit user consent
- [ ] Widget permissions declared and enforced
- [ ] Widget loading failures logged with context
- [ ] Widgets isolated via AssemblyLoadContext
- [ ] Resource limits prevent runaway widgets

## Manifest Validation

### Schema Validation

```csharp
public class ManifestValidator
{
    private static readonly string[] RequiredFields = 
    {
        "packageId", "widgetKey", "displayName", 
        "version", "entry", "minAppVersion"
    };
    
    private static readonly string[] AllowedPermissions =
    {
        "network", "filesystem", "clipboard", 
        "notifications", "process"
    };
    
    public ValidationResult Validate(WidgetManifest manifest, string widgetPath)
    {
        var errors = new List<string>();
        
        // Required fields
        if (string.IsNullOrEmpty(manifest.PackageId))
            errors.Add("Missing required field: packageId");
        if (string.IsNullOrEmpty(manifest.WidgetKey))
            errors.Add("Missing required field: widgetKey");
        if (string.IsNullOrEmpty(manifest.Entry))
            errors.Add("Missing required field: entry");
        
        // Widget key format
        if (!InputValidator.IsValidWidgetKey(manifest.WidgetKey))
            errors.Add($"Invalid widget key format: {manifest.WidgetKey}");
        
        // Version format
        if (!SemanticVersion.TryParse(manifest.Version, out _))
            errors.Add($"Invalid version format: {manifest.Version}");
        
        // Entry point security
        if (!PathValidator.IsValidEntryPoint(widgetPath, manifest.Entry))
            errors.Add($"Invalid or missing entry point: {manifest.Entry}");
        
        // Permission validation
        var invalidPermissions = manifest.Permissions?
            .Except(AllowedPermissions)
            .ToList() ?? [];
        
        if (invalidPermissions.Count > 0)
            errors.Add($"Unknown permissions: {string.Join(", ", invalidPermissions)}");
        
        // Size limits
        if (manifest.DefaultSize?.Width > 2000 || manifest.DefaultSize?.Height > 2000)
            errors.Add("Widget size exceeds maximum (2000x2000)");
        
        return new ValidationResult(errors.Count == 0, errors);
    }
}

public record ValidationResult(bool IsValid, IReadOnlyList<string> Errors);
```

## Assembly Loading with Isolation

### Widget Load Context

```csharp
public class WidgetLoadContext : AssemblyLoadContext
{
    private readonly AssemblyDependencyResolver _resolver;
    private readonly string _widgetPath;
    
    public WidgetLoadContext(string widgetPath) 
        : base(isCollectible: true)  // Allows unloading
    {
        _widgetPath = widgetPath;
        _resolver = new AssemblyDependencyResolver(widgetPath);
    }
    
    protected override Assembly? Load(AssemblyName assemblyName)
    {
        // Try to resolve from widget directory first
        var assemblyPath = _resolver.ResolveAssemblyToPath(assemblyName);
        
        if (assemblyPath != null)
        {
            return LoadFromAssemblyPath(assemblyPath);
        }
        
        // Fall back to default context for shared dependencies
        return null;
    }
    
    protected override IntPtr LoadUnmanagedDll(string unmanagedDllName)
    {
        var libraryPath = _resolver.ResolveUnmanagedDllToPath(unmanagedDllName);
        
        if (libraryPath != null)
        {
            return LoadUnmanagedDllFromPath(libraryPath);
        }
        
        return IntPtr.Zero;
    }
}
```

### Safe Widget Loader

```csharp
public class SecureWidgetLoader : IWidgetLoader
{
    private readonly ConcurrentDictionary<string, WidgetLoadContext> _contexts = new();
    private readonly ILogger<SecureWidgetLoader> _logger;
    
    public async Task<IWidgetFactory?> LoadWidgetAsync(
        string widgetKey, 
        string widgetPath, 
        CancellationToken ct)
    {
        _logger.LogInformation("Loading widget: {WidgetKey} from {Path}", 
            widgetKey, widgetPath);
        
        try
        {
            // Create isolated load context
            var context = new WidgetLoadContext(widgetPath);
            _contexts[widgetKey] = context;
            
            // Load the assembly
            var assemblyPath = Path.Combine(widgetPath, $"{widgetKey}.dll");
            var assembly = context.LoadFromAssemblyPath(assemblyPath);
            
            // Find the factory type
            var factoryType = assembly.GetTypes()
                .FirstOrDefault(t => 
                    typeof(IWidgetFactory).IsAssignableFrom(t) && 
                    !t.IsAbstract);
            
            if (factoryType == null)
            {
                _logger.LogWarning("No IWidgetFactory found in widget: {WidgetKey}", widgetKey);
                UnloadWidget(widgetKey);
                return null;
            }
            
            // Create factory instance
            var factory = (IWidgetFactory)Activator.CreateInstance(factoryType)!;
            
            SecurityAudit.LogWidgetLoad(widgetKey, widgetPath, success: true);
            return factory;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to load widget: {WidgetKey}", widgetKey);
            SecurityAudit.LogWidgetLoad(widgetKey, widgetPath, success: false);
            UnloadWidget(widgetKey);
            throw;
        }
    }
    
    public void UnloadWidget(string widgetKey)
    {
        if (_contexts.TryRemove(widgetKey, out var context))
        {
            context.Unload();
            
            // Force GC to collect unloaded assemblies
            for (int i = 0; i < 3; i++)
            {
                GC.Collect();
                GC.WaitForPendingFinalizers();
            }
            
            _logger.LogInformation("Unloaded widget: {WidgetKey}", widgetKey);
        }
    }
}
```

## Permission System

### Permission Enforcement

```csharp
public class PermissionEnforcer
{
    private readonly ConcurrentDictionary<string, WidgetPermissions> _grantedPermissions = new();
    
    public void GrantPermissions(string widgetKey, WidgetPermissions permissions)
    {
        _grantedPermissions[widgetKey] = permissions;
        SecurityAudit.LogPermissionRequest(
            widgetKey, 
            GetPermissionNames(permissions), 
            granted: true);
    }
    
    public void RevokePermissions(string widgetKey)
    {
        _grantedPermissions.TryRemove(widgetKey, out _);
    }
    
    public bool HasPermission(string widgetKey, string permission)
    {
        if (!_grantedPermissions.TryGetValue(widgetKey, out var permissions))
            return false;
        
        return permission switch
        {
            "network" => permissions.CanAccessNetwork,
            "filesystem" => permissions.CanAccessFileSystem,
            "clipboard" => permissions.CanAccessClipboard,
            "process" => permissions.CanStartProcess,
            _ => false
        };
    }
    
    public void EnforcePermission(string widgetKey, string permission)
    {
        if (!HasPermission(widgetKey, permission))
        {
            SecurityAudit.LogSuspiciousActivity(
                "Permission denied", 
                $"Widget {widgetKey} attempted {permission} without permission");
            
            throw new SecurityException(
                $"Widget '{widgetKey}' does not have '{permission}' permission");
        }
    }
    
    private static string[] GetPermissionNames(WidgetPermissions permissions)
    {
        var names = new List<string>();
        if (permissions.CanAccessNetwork) names.Add("network");
        if (permissions.CanAccessFileSystem) names.Add("filesystem");
        if (permissions.CanAccessClipboard) names.Add("clipboard");
        if (permissions.CanStartProcess) names.Add("process");
        return names.ToArray();
    }
}
```

### Permission Consent Dialog

```csharp
public interface IPermissionConsentService
{
    Task<bool> RequestConsentAsync(
        string widgetKey, 
        string displayName, 
        string[] requestedPermissions);
}

public class PermissionConsentDialogService : IPermissionConsentService
{
    public async Task<bool> RequestConsentAsync(
        string widgetKey, 
        string displayName, 
        string[] requestedPermissions)
    {
        if (requestedPermissions.Length == 0)
            return true;  // No permissions needed
        
        var descriptions = requestedPermissions.Select(GetPermissionDescription);
        
        var dialog = new PermissionConsentDialog
        {
            WidgetName = displayName,
            Permissions = descriptions.ToList()
        };
        
        var result = dialog.ShowDialog() == true;
        
        SecurityAudit.LogPermissionRequest(widgetKey, requestedPermissions, result);
        
        return result;
    }
    
    private static string GetPermissionDescription(string permission) => permission switch
    {
        "network" => "Access the internet to fetch data or communicate with services",
        "filesystem" => "Read and write files on your computer",
        "clipboard" => "Read from and write to your clipboard",
        "notifications" => "Show system notifications",
        "process" => "Start other programs on your computer",
        _ => $"Unknown permission: {permission}"
    };
}
```

## Code Signing (Future)

### Signature Verification

```csharp
public interface IPackageSignatureService
{
    SignatureVerificationResult VerifySignature(string packagePath);
    Task<bool> SignPackageAsync(string packagePath, X509Certificate2 certificate);
}

public record SignatureVerificationResult(
    bool IsValid,
    string? PublisherName,
    DateTimeOffset? SignedAt,
    string? Error);

public class PackageSignatureService : IPackageSignatureService
{
    public SignatureVerificationResult VerifySignature(string packagePath)
    {
        // TODO: Implement Authenticode or custom signing
        // For now, return unsigned
        return new SignatureVerificationResult(
            IsValid: false,
            PublisherName: null,
            SignedAt: null,
            Error: "Package is not signed");
    }
    
    public Task<bool> SignPackageAsync(string packagePath, X509Certificate2 certificate)
    {
        // TODO: Implement package signing
        throw new NotImplementedException("Package signing not yet implemented");
    }
}
```

## Resource Limits

### Widget Watchdog

```csharp
public class WidgetWatchdog : IDisposable
{
    private readonly ConcurrentDictionary<string, WidgetMetrics> _metrics = new();
    private readonly Timer _checkTimer;
    private readonly TimeSpan _maxExecutionTime = TimeSpan.FromSeconds(30);
    private readonly long _maxMemoryBytes = 100 * 1024 * 1024;  // 100MB
    
    public event EventHandler<WidgetViolationEventArgs>? ViolationDetected;
    
    public WidgetWatchdog()
    {
        _checkTimer = new Timer(CheckWidgets, null, TimeSpan.FromSeconds(5), TimeSpan.FromSeconds(5));
    }
    
    public void RegisterWidget(string widgetKey)
    {
        _metrics[widgetKey] = new WidgetMetrics
        {
            StartTime = DateTimeOffset.UtcNow,
            LastActivity = DateTimeOffset.UtcNow
        };
    }
    
    public void RecordActivity(string widgetKey)
    {
        if (_metrics.TryGetValue(widgetKey, out var metrics))
        {
            metrics.LastActivity = DateTimeOffset.UtcNow;
            metrics.OperationCount++;
        }
    }
    
    private void CheckWidgets(object? state)
    {
        foreach (var (widgetKey, metrics) in _metrics)
        {
            // Check for hung widgets
            var inactiveTime = DateTimeOffset.UtcNow - metrics.LastActivity;
            if (inactiveTime > _maxExecutionTime)
            {
                ViolationDetected?.Invoke(this, new WidgetViolationEventArgs
                {
                    WidgetKey = widgetKey,
                    Violation = $"Widget unresponsive for {inactiveTime.TotalSeconds}s"
                });
            }
        }
    }
    
    public void Dispose() => _checkTimer.Dispose();
}

public class WidgetMetrics
{
    public DateTimeOffset StartTime { get; set; }
    public DateTimeOffset LastActivity { get; set; }
    public long OperationCount { get; set; }
}

public class WidgetViolationEventArgs : EventArgs
{
    public required string WidgetKey { get; init; }
    public required string Violation { get; init; }
}
```

## Security Best Practices

### Widget Development Guidelines

1. **Declare all required permissions** in manifest
2. **Handle permission denial gracefully** with fallback behavior
3. **Never store credentials** - use host's secure storage API
4. **Validate all external data** before use
5. **Minimize permission requests** - only ask for what's needed

### Host Application Guidelines

1. **Always validate manifests** before loading
2. **Use AssemblyLoadContext** for isolation
3. **Require user consent** for permissions
4. **Log all security events** for audit
5. **Provide uninstall capability** that removes all widget data

## References

- [.NET Assembly Loading](https://docs.microsoft.com/en-us/dotnet/core/dependency-loading/understanding-assemblyloadcontext)
- [Code Access Security](https://docs.microsoft.com/en-us/dotnet/framework/misc/code-access-security)
- [Plugin Architecture](https://docs.microsoft.com/en-us/dotnet/core/tutorials/creating-app-with-plugin-support)
