---
name: security
description: Security patterns for the 3SC widget host. Covers credential storage, input validation, secure coding practices, and protecting user data.
---

# Security

## Overview

Security is critical for a desktop application that handles user data and loads external plugins. This skill covers security patterns for protecting credentials, validating input, and secure coding practices.

## Definition of Done (DoD)

- [ ] Credentials stored using DPAPI (Windows Data Protection)
- [ ] User input validated before use
- [ ] Sensitive data never logged
- [ ] File paths validated to prevent traversal attacks
- [ ] Error messages don't expose internal details
- [ ] Security-sensitive operations are audited

## Credential Storage

### Windows Data Protection API (DPAPI)

```csharp
public class SecureStorageService : ISecureStorage
{
    private readonly string _storePath;
    
    public SecureStorageService()
    {
        _storePath = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            "3SC", "secure");
        Directory.CreateDirectory(_storePath);
    }
    
    public void Store(string key, string value)
    {
        ArgumentException.ThrowIfNullOrEmpty(key);
        
        var plainBytes = Encoding.UTF8.GetBytes(value);
        var protectedBytes = ProtectedData.Protect(
            plainBytes, 
            entropy: null,  // Add entropy for additional security
            scope: DataProtectionScope.CurrentUser);
        
        var filePath = GetFilePath(key);
        File.WriteAllBytes(filePath, protectedBytes);
        
        Log.Debug("Credential stored: {Key}", key);  // Never log the value!
    }
    
    public string? Retrieve(string key)
    {
        var filePath = GetFilePath(key);
        
        if (!File.Exists(filePath))
            return null;
        
        try
        {
            var protectedBytes = File.ReadAllBytes(filePath);
            var plainBytes = ProtectedData.Unprotect(
                protectedBytes,
                entropy: null,
                scope: DataProtectionScope.CurrentUser);
            
            return Encoding.UTF8.GetString(plainBytes);
        }
        catch (CryptographicException ex)
        {
            Log.Warning(ex, "Failed to decrypt credential: {Key}", key);
            return null;
        }
    }
    
    public void Delete(string key)
    {
        var filePath = GetFilePath(key);
        
        if (File.Exists(filePath))
        {
            // Overwrite before delete for security
            File.WriteAllBytes(filePath, new byte[64]);
            File.Delete(filePath);
        }
    }
    
    private string GetFilePath(string key)
    {
        // Sanitize key to prevent path traversal
        var safeKey = Path.GetFileName(key);
        return Path.Combine(_storePath, $"{safeKey}.dat");
    }
}
```

### Credential Manager for API Keys

```csharp
public class CredentialManagerService : ICredentialManager
{
    private const string CredentialPrefix = "3SC:";
    
    public void SaveCredential(string target, string username, string password)
    {
        var credential = new Credential
        {
            Target = CredentialPrefix + target,
            Username = username,
            Password = password,
            Type = CredentialType.Generic,
            Persist = PersistType.LocalMachine
        };
        
        credential.Save();
        Log.Information("Credential saved for target: {Target}", target);
    }
    
    public (string? Username, string? Password) GetCredential(string target)
    {
        var credential = new Credential { Target = CredentialPrefix + target };
        
        if (credential.Load())
        {
            return (credential.Username, credential.Password);
        }
        
        return (null, null);
    }
    
    public void DeleteCredential(string target)
    {
        var credential = new Credential { Target = CredentialPrefix + target };
        credential.Delete();
    }
}
```

## Input Validation

### Path Validation

```csharp
public static class PathValidator
{
    private static readonly char[] InvalidChars = Path.GetInvalidPathChars()
        .Concat(new[] { '*', '?', '"', '<', '>', '|' })
        .ToArray();
    
    /// <summary>
    /// Validates and normalizes a file path to prevent traversal attacks.
    /// </summary>
    public static string ValidatePath(string basePath, string relativePath)
    {
        ArgumentException.ThrowIfNullOrEmpty(basePath);
        ArgumentException.ThrowIfNullOrEmpty(relativePath);
        
        // Check for invalid characters
        if (relativePath.IndexOfAny(InvalidChars) >= 0)
        {
            throw new ArgumentException("Path contains invalid characters", nameof(relativePath));
        }
        
        // Normalize and get full path
        var fullPath = Path.GetFullPath(Path.Combine(basePath, relativePath));
        var normalizedBase = Path.GetFullPath(basePath);
        
        // Ensure the path is within the base directory
        if (!fullPath.StartsWith(normalizedBase, StringComparison.OrdinalIgnoreCase))
        {
            throw new SecurityException($"Path traversal attempt detected: {relativePath}");
        }
        
        return fullPath;
    }
    
    /// <summary>
    /// Validates a widget package entry point path.
    /// </summary>
    public static bool IsValidEntryPoint(string widgetPath, string entry)
    {
        if (string.IsNullOrEmpty(entry))
            return false;
        
        // Entry must be a simple filename, no paths
        if (entry != Path.GetFileName(entry))
            return false;
        
        // Must be a DLL
        if (!entry.EndsWith(".dll", StringComparison.OrdinalIgnoreCase))
            return false;
        
        // File must exist within widget directory
        var fullPath = Path.Combine(widgetPath, entry);
        return File.Exists(fullPath);
    }
}
```

### String Validation

```csharp
public static class InputValidator
{
    private static readonly Regex SafeNamePattern = new(
        @"^[a-zA-Z0-9][a-zA-Z0-9\-_.]{0,63}$",
        RegexOptions.Compiled);
    
    public static bool IsValidWidgetKey(string? key)
    {
        return !string.IsNullOrEmpty(key) 
            && key.Length <= 64 
            && SafeNamePattern.IsMatch(key);
    }
    
    public static bool IsValidDisplayName(string? name)
    {
        return !string.IsNullOrWhiteSpace(name) 
            && name.Length <= 128
            && !name.Contains('<')  // Prevent XSS
            && !name.Contains('>');
    }
    
    public static string SanitizeHtml(string input)
    {
        if (string.IsNullOrEmpty(input))
            return string.Empty;
        
        return WebUtility.HtmlEncode(input);
    }
    
    public static string? TruncateWithEllipsis(string? input, int maxLength)
    {
        if (string.IsNullOrEmpty(input) || input.Length <= maxLength)
            return input;
        
        return input[..(maxLength - 3)] + "...";
    }
}
```

## Error Message Security

### Safe Error Messages

```csharp
public static class SafeErrors
{
    // Public-facing error messages (user-visible)
    public const string GenericError = "An unexpected error occurred. Please try again.";
    public const string NetworkError = "Unable to connect. Please check your internet connection.";
    public const string DatabaseError = "Failed to save changes. Please try again.";
    public const string WidgetLoadError = "Failed to load widget. It may be corrupted or incompatible.";
    public const string AuthenticationError = "Authentication failed. Please check your credentials.";
    
    // Never expose these to users:
    // - Stack traces
    // - File paths
    // - Database connection strings
    // - Internal exception messages
    // - Server names or IPs
    
    public static string ToUserMessage(Exception ex)
    {
        return ex switch
        {
            HttpRequestException => NetworkError,
            Microsoft.Data.Sqlite.SqliteException => DatabaseError,
            FileNotFoundException => "The requested file was not found.",
            UnauthorizedAccessException => "Access denied. You may not have permission for this operation.",
            OperationCanceledException => "Operation was cancelled.",
            _ => GenericError
        };
    }
}

// Usage in ViewModel
catch (Exception ex)
{
    Log.Error(ex, "Detailed error for debugging");  // Full details to logs
    ErrorMessage = SafeErrors.ToUserMessage(ex);     // Safe message to UI
}
```

## Audit Logging

### Security Events

```csharp
public static class SecurityAudit
{
    public static void LogCredentialAccess(string target, bool success)
    {
        Log.Information(
            "Security: Credential access - Target: {Target}, Success: {Success}",
            target, success);
    }
    
    public static void LogWidgetLoad(string widgetKey, string path, bool success)
    {
        Log.Information(
            "Security: Widget load - Key: {WidgetKey}, Path: {Path}, Success: {Success}",
            widgetKey, LogSanitizer.MaskPath(path), success);
    }
    
    public static void LogPermissionRequest(string widgetKey, string[] permissions, bool granted)
    {
        Log.Information(
            "Security: Permission request - Widget: {WidgetKey}, Permissions: {@Permissions}, Granted: {Granted}",
            widgetKey, permissions, granted);
    }
    
    public static void LogSuspiciousActivity(string activity, string details)
    {
        Log.Warning(
            "Security: Suspicious activity - Activity: {Activity}, Details: {Details}",
            activity, details);
    }
}
```

## Secure Coding Practices

### Memory Security

```csharp
// Use SecureString for sensitive data in memory (when possible)
public class SecureCredential : IDisposable
{
    private SecureString? _password;
    
    public void SetPassword(string password)
    {
        _password?.Dispose();
        _password = new SecureString();
        
        foreach (var c in password)
        {
            _password.AppendChar(c);
        }
        
        _password.MakeReadOnly();
    }
    
    public string GetPassword()
    {
        if (_password == null)
            return string.Empty;
        
        var ptr = Marshal.SecureStringToBSTR(_password);
        try
        {
            return Marshal.PtrToStringBSTR(ptr);
        }
        finally
        {
            Marshal.ZeroFreeBSTR(ptr);
        }
    }
    
    public void Dispose()
    {
        _password?.Dispose();
        _password = null;
    }
}
```

### Principle of Least Privilege

```csharp
// Widget permissions model
public class WidgetPermissions
{
    public bool CanAccessNetwork { get; init; }
    public bool CanAccessFileSystem { get; init; }
    public bool CanAccessClipboard { get; init; }
    public bool CanStartProcess { get; init; }
    
    public static WidgetPermissions Default => new()
    {
        CanAccessNetwork = false,
        CanAccessFileSystem = false,
        CanAccessClipboard = false,
        CanStartProcess = false
    };
    
    public static WidgetPermissions FromManifest(string[] permissions)
    {
        return new WidgetPermissions
        {
            CanAccessNetwork = permissions.Contains("network"),
            CanAccessFileSystem = permissions.Contains("filesystem"),
            CanAccessClipboard = permissions.Contains("clipboard"),
            CanStartProcess = permissions.Contains("process")
        };
    }
}
```

## Security Checklist

### Before Release

- [ ] All credentials use DPAPI storage
- [ ] No hardcoded secrets in code
- [ ] Error messages sanitized for users
- [ ] File paths validated
- [ ] Input validated at boundaries
- [ ] Audit logging for security events
- [ ] Widget permissions enforced
- [ ] No sensitive data in logs

### Code Review Security Questions

1. Does this code handle user input? Is it validated?
2. Does this code load external data? Is it sanitized?
3. Does this code access credentials? Is access logged?
4. Does this error message expose internal details?
5. Does this file operation validate paths?
6. Does this widget operation check permissions?

## Common Vulnerabilities to Avoid

| Vulnerability | Prevention |
|--------------|------------|
| Path traversal | Validate and normalize all paths |
| Credential exposure | Use DPAPI, never log credentials |
| Information disclosure | Sanitize error messages |
| Arbitrary code execution | Sandbox widgets, validate assemblies |
| Injection | Parameterize all queries |
| XSS in WebView | Sanitize HTML content |

## References

- [OWASP Desktop App Security](https://owasp.org/www-project-desktop-app-security-top-10/)
- [Data Protection in .NET](https://docs.microsoft.com/en-us/aspnet/core/security/data-protection/)
- [Secure Coding Guidelines](https://docs.microsoft.com/en-us/dotnet/standard/security/secure-coding-guidelines)
