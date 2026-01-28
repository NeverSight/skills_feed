---
name: error-handling
description: Global error handling for the 3SC widget host. Covers exception handling, crash reporting, user-friendly error surfaces, and recovery strategies.
---

# Error Handling

## Overview

Provide consistent, user-safe error handling across the shell, widgets, and background services. Users should never see stack traces or cryptic error messages.

## Definition of Done (DoD)

- [ ] Global handlers registered in App.xaml.cs for all exception sources
- [ ] All exceptions logged with correlation IDs and context
- [ ] User sees friendly, actionable error messages
- [ ] Crash reports saved locally with sanitized data
- [ ] No swallowed exceptions without explicit justification
- [ ] Widget errors don't crash the host application

## Global Exception Handlers

### App.xaml.cs Registration

```csharp
private void RegisterGlobalExceptionHandlers()
{
    // UI thread exceptions
    DispatcherUnhandledException += OnDispatcherUnhandledException;
    
    // Background thread exceptions
    AppDomain.CurrentDomain.UnhandledException += OnAppDomainUnhandledException;
    
    // Task exceptions that aren't observed
    TaskScheduler.UnobservedTaskException += OnUnobservedTaskException;
}

private void OnDispatcherUnhandledException(object sender, DispatcherUnhandledExceptionEventArgs e)
{
    var correlationId = CorrelationContext.Current ?? Guid.NewGuid().ToString("N")[..8];
    
    Log.Error(e.Exception, 
        "Unhandled UI exception. CorrelationId: {CorrelationId}", correlationId);
    
    // Save crash report
    CrashReportService.SaveReport(e.Exception, correlationId);
    
    // Show user-friendly message
    ShowErrorToUser(e.Exception, correlationId);
    
    // Prevent app crash for recoverable errors
    e.Handled = IsRecoverableError(e.Exception);
}

private void OnAppDomainUnhandledException(object sender, UnhandledExceptionEventArgs e)
{
    var exception = e.ExceptionObject as Exception;
    var correlationId = Guid.NewGuid().ToString("N")[..8];
    
    Log.Fatal(exception, 
        "Fatal unhandled exception. Terminating: {IsTerminating}, CorrelationId: {CorrelationId}", 
        e.IsTerminating, correlationId);
    
    CrashReportService.SaveReport(exception, correlationId);
}

private void OnUnobservedTaskException(object? sender, UnobservedTaskExceptionEventArgs e)
{
    Log.Error(e.Exception, "Unobserved task exception");
    
    // Prevent app crash - log and continue
    e.SetObserved();
}
```

### Recoverable vs Fatal Errors

```csharp
private static bool IsRecoverableError(Exception ex) => ex switch
{
    // Network issues - recoverable
    HttpRequestException => true,
    TaskCanceledException => true,
    
    // Database issues - might recover
    DbUpdateException => true,
    
    // Widget errors - definitely recoverable (isolate the widget)
    WidgetLoadException => true,
    WidgetExecutionException => true,
    
    // Memory/system issues - not recoverable
    OutOfMemoryException => false,
    StackOverflowException => false,
    AccessViolationException => false,
    
    _ => true  // Default to recoverable
};
```

## ViewModel Error Handling

### Async Command Pattern

```csharp
[RelayCommand]
private async Task LoadWidgetsAsync(CancellationToken ct)
{
    IsLoading = true;
    ErrorMessage = null;
    
    try
    {
        var widgets = await _repository.GetAllAsync(ct);
        Widgets = new ObservableCollection<WidgetViewModel>(
            widgets.Select(w => new WidgetViewModel(w)));
    }
    catch (OperationCanceledException)
    {
        // User cancelled - not an error
        Log.Debug("Widget loading cancelled by user");
    }
    catch (Exception ex)
    {
        Log.Error(ex, "Failed to load widgets");
        ErrorMessage = "Failed to load widgets. Please try again.";
        
        // Optionally show toast/notification
        _notifications.ShowError("Could not load widgets");
    }
    finally
    {
        IsLoading = false;
    }
}
```

### Error Display Patterns

```csharp
public partial class WidgetLibraryViewModel : ObservableObject
{
    [ObservableProperty]
    private string? _errorMessage;
    
    [ObservableProperty]
    private ErrorSeverity _errorSeverity = ErrorSeverity.None;
    
    public bool HasError => !string.IsNullOrEmpty(ErrorMessage);
    
    private void SetError(string message, ErrorSeverity severity = ErrorSeverity.Error)
    {
        ErrorMessage = message;
        ErrorSeverity = severity;
        OnPropertyChanged(nameof(HasError));
    }
    
    private void ClearError()
    {
        ErrorMessage = null;
        ErrorSeverity = ErrorSeverity.None;
        OnPropertyChanged(nameof(HasError));
    }
}

public enum ErrorSeverity { None, Info, Warning, Error }
```

## User Error Messages

### Safe Message Mapping

```csharp
public static class UserMessages
{
    public static string FromException(Exception ex) => ex switch
    {
        HttpRequestException => 
            "Unable to connect to the server. Please check your internet connection.",
        
        DbUpdateException => 
            "Failed to save changes. Please try again.",
        
        FileNotFoundException => 
            "The requested file could not be found.",
        
        UnauthorizedAccessException => 
            "Access denied. You may need to run as administrator.",
        
        WidgetLoadException wle => 
            $"Widget '{wle.WidgetKey}' failed to load. It may be corrupted or incompatible.",
        
        TimeoutException => 
            "The operation timed out. Please try again.",
        
        _ => "An unexpected error occurred. Please try again."
    };
    
    public static string WithCorrelationId(string message, string correlationId) =>
        $"{message}\n\nReference: {correlationId}";
}
```

## Widget Error Isolation

```csharp
public async Task<bool> SafeLoadWidgetAsync(string widgetKey)
{
    try
    {
        var widget = await _loader.LoadWidgetAsync(widgetKey);
        await widget.InitializeAsync();
        return true;
    }
    catch (Exception ex)
    {
        Log.Error(ex, "Widget {WidgetKey} failed to load", widgetKey);
        
        // Mark widget as problematic
        await _widgetRepo.MarkAsFailedAsync(widgetKey, ex.Message);
        
        // Notify user but don't crash
        _notifications.ShowError($"Widget '{widgetKey}' failed to load");
        
        return false;
    }
}

// Widget execution wrapper
public void SafeExecuteWidgetAction(string widgetKey, Action action)
{
    try
    {
        action();
    }
    catch (Exception ex)
    {
        Log.Error(ex, "Widget {WidgetKey} action failed", widgetKey);
        
        // Optionally disable the widget
        if (ShouldDisableWidget(ex))
        {
            DisableWidget(widgetKey, "Repeated failures");
        }
    }
}
```

## Crash Reports

### Crash Report Service

```csharp
public static class CrashReportService
{
    private static readonly string CrashFolder = Path.Combine(
        Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
        "3SC", "crashes");
    
    public static void SaveReport(Exception? exception, string correlationId)
    {
        try
        {
            Directory.CreateDirectory(CrashFolder);
            
            var report = new CrashReport
            {
                Timestamp = DateTimeOffset.UtcNow,
                CorrelationId = correlationId,
                AppVersion = GetAppVersion(),
                OsVersion = Environment.OSVersion.ToString(),
                ExceptionType = exception?.GetType().FullName,
                Message = exception?.Message,
                StackTrace = SanitizeStackTrace(exception?.ToString()),
                AdditionalContext = GatherContext()
            };
            
            var fileName = $"crash_{DateTime.UtcNow:yyyyMMdd_HHmmss}_{correlationId}.json";
            var filePath = Path.Combine(CrashFolder, fileName);
            
            File.WriteAllText(filePath, JsonSerializer.Serialize(report, new JsonSerializerOptions
            {
                WriteIndented = true
            }));
            
            // Cleanup old reports (keep last 50)
            CleanupOldReports(maxReports: 50);
        }
        catch
        {
            // Never throw from crash reporting
        }
    }
    
    private static string? SanitizeStackTrace(string? stackTrace)
    {
        if (string.IsNullOrEmpty(stackTrace)) return null;
        
        var userProfile = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
        return stackTrace.Replace(userProfile, "[USER]");
    }
}
```

## Error UI Components

### Error Banner (XAML)

```xml
<Border x:Name="ErrorBanner"
        Visibility="{Binding HasError, Converter={StaticResource BoolToVisibility}}"
        Background="{DynamicResource ErrorBackgroundBrush}"
        Padding="12,8">
    <Grid>
        <Grid.ColumnDefinitions>
            <ColumnDefinition Width="Auto" />
            <ColumnDefinition Width="*" />
            <ColumnDefinition Width="Auto" />
        </Grid.ColumnDefinitions>
        
        <Path Data="{StaticResource ErrorIcon}" 
              Fill="{DynamicResource ErrorForegroundBrush}" />
        
        <TextBlock Grid.Column="1" 
                   Text="{Binding ErrorMessage}"
                   Foreground="{DynamicResource ErrorForegroundBrush}"
                   Margin="8,0" />
        
        <Button Grid.Column="2" 
                Command="{Binding DismissErrorCommand}"
                Content="✕"
                Style="{StaticResource IconButton}" />
    </Grid>
</Border>
```

## Best Practices

| Practice | Reason |
|----------|--------|
| Log before showing user message | Capture full context for debugging |
| Include correlation ID | Enables support to find logs |
| Sanitize sensitive data | Protect user privacy in reports |
| Isolate widget errors | Don't let plugins crash the host |
| Use structured exception types | Easier to handle specifically |
| Provide actionable messages | Help users resolve issues |

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| `catch { }` | Swallows all errors silently | At minimum log the exception |
| Showing stack traces | Confuses users, security risk | Map to friendly messages |
| Throwing from exception handlers | Recursive failure | Always catch in handlers |
| Generic error messages only | User can't act on them | Be specific when possible |

## References

- `references/global-handlers.md` for exception hooks
- `references/ui-errors.md` for UI surface patterns
- `references/crash-reporting.md` for report capture and storage
