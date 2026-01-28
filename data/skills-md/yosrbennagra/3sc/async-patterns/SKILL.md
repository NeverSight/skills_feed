---
name: async-patterns
description: Async/await patterns for the 3SC widget host. Covers Task handling, cancellation, ConfigureAwait, fire-and-forget prevention, and async command patterns in WPF.
---

# Async Patterns

## Overview

Proper async/await usage is critical for UI responsiveness and application stability. This skill covers patterns specific to WPF desktop applications.

## Definition of Done (DoD)

- [ ] All async methods return `Task` or `Task<T>` (never `async void` except event handlers)
- [ ] Long-running operations support `CancellationToken`
- [ ] No `.Result` or `.Wait()` calls on UI thread
- [ ] Fire-and-forget tasks are handled with proper error logging
- [ ] Async commands show loading state and handle exceptions

## Core Rules

### 1. Never Block the UI Thread

```csharp
// ❌ BAD - Blocks UI thread
var result = SomeAsyncMethod().Result;
var result = SomeAsyncMethod().GetAwaiter().GetResult();

// ✅ GOOD - Async all the way
var result = await SomeAsyncMethod();
```

### 2. Always Use CancellationToken

```csharp
// ✅ GOOD - Supports cancellation
public async Task<List<Widget>> LoadWidgetsAsync(CancellationToken cancellationToken = default)
{
    cancellationToken.ThrowIfCancellationRequested();
    
    return await _repository.GetAllAsync(cancellationToken);
}
```

### 3. ConfigureAwait in Library Code

```csharp
// In Infrastructure/Application layers (non-UI code):
public async Task<Widget> GetByIdAsync(Guid id, CancellationToken ct)
{
    return await _context.Widgets
        .FirstOrDefaultAsync(w => w.Id == id, ct)
        .ConfigureAwait(false);  // Don't capture UI context
}

// In UI layer (ViewModels) - capture context for UI updates:
public async Task LoadAsync()
{
    var widgets = await _service.GetWidgetsAsync();  // No ConfigureAwait
    Widgets = new ObservableCollection<Widget>(widgets);  // Must run on UI thread
}
```

## Async Command Pattern

### Standard Async Command

```csharp
public partial class WidgetLibraryViewModel : ObservableObject
{
    [ObservableProperty]
    [NotifyPropertyChangedFor(nameof(IsNotLoading))]
    private bool _isLoading;
    
    public bool IsNotLoading => !IsLoading;

    [RelayCommand]
    private async Task LoadWidgetsAsync(CancellationToken cancellationToken)
    {
        if (IsLoading) return;  // Prevent double-execution
        
        IsLoading = true;
        ErrorMessage = null;
        
        try
        {
            var widgets = await _repository.GetAllAsync(cancellationToken);
            Widgets = new ObservableCollection<WidgetViewModel>(
                widgets.Select(w => new WidgetViewModel(w)));
        }
        catch (OperationCanceledException)
        {
            // Expected when user cancels - don't log as error
        }
        catch (Exception ex)
        {
            Log.Error(ex, "Failed to load widgets");
            ErrorMessage = "Failed to load widgets. Please try again.";
        }
        finally
        {
            IsLoading = false;
        }
    }
}
```

### Command with Automatic Busy State

```csharp
// CommunityToolkit.Mvvm automatically sets IsRunning on async commands
[RelayCommand]
private async Task RefreshAsync(CancellationToken ct)
{
    await _service.RefreshAsync(ct);
}

// In XAML - bind to command's IsRunning
<Button Command="{Binding RefreshCommand}"
        IsEnabled="{Binding RefreshCommand.IsRunning, Converter={StaticResource InverseBoolConverter}}" />
        
<ProgressRing IsActive="{Binding RefreshCommand.IsRunning}" />
```

## Fire-and-Forget Pattern

When you genuinely need fire-and-forget (rare), use this pattern:

```csharp
public static class TaskExtensions
{
    /// <summary>
    /// Safely executes a fire-and-forget task with error logging.
    /// Use sparingly - prefer proper async/await chains.
    /// </summary>
    public static void FireAndForget(
        this Task task, 
        Action<Exception>? onError = null,
        [CallerMemberName] string? callerName = null)
    {
        task.ContinueWith(t =>
        {
            if (t.IsFaulted && t.Exception != null)
            {
                var ex = t.Exception.Flatten().InnerException ?? t.Exception;
                Log.Error(ex, "Fire-and-forget task failed in {Caller}", callerName);
                onError?.Invoke(ex);
            }
        }, TaskContinuationOptions.OnlyOnFaulted);
    }
}

// Usage:
_syncService.SyncAsync().FireAndForget(
    onError: ex => NotifyUser("Sync failed"));
```

## Startup Async Pattern

For async operations during app startup:

```csharp
// ❌ BAD - Blocks startup
protected override void OnStartup(StartupEventArgs e)
{
    base.OnStartup(e);
    InitializeAsync().GetAwaiter().GetResult();  // Blocks!
}

// ✅ GOOD - Non-blocking startup
protected override async void OnStartup(StartupEventArgs e)
{
    base.OnStartup(e);
    
    // Show splash/shell immediately
    _shellWindow = new ShellWindow();
    _shellWindow.Show();
    
    try
    {
        await InitializeAsync();
    }
    catch (Exception ex)
    {
        Log.Fatal(ex, "Startup initialization failed");
        ShowCriticalError("Failed to start application");
        Shutdown(-1);
    }
}
```

## Parallel Operations

### When to Use Parallel

```csharp
// ✅ GOOD - Independent operations
var widgetsTask = _widgetRepo.GetAllAsync(ct);
var layoutsTask = _layoutRepo.GetAllAsync(ct);
var settingsTask = _settingsService.LoadAsync(ct);

await Task.WhenAll(widgetsTask, layoutsTask, settingsTask);

var widgets = await widgetsTask;
var layouts = await layoutsTask;
var settings = await settingsTask;
```

### Bounded Parallelism

```csharp
// ✅ GOOD - Limit concurrent operations
public async Task ProcessWidgetsAsync(
    IEnumerable<Widget> widgets, 
    CancellationToken ct)
{
    var semaphore = new SemaphoreSlim(maxConcurrency: 4);
    
    var tasks = widgets.Select(async widget =>
    {
        await semaphore.WaitAsync(ct);
        try
        {
            await ProcessWidgetAsync(widget, ct);
        }
        finally
        {
            semaphore.Release();
        }
    });
    
    await Task.WhenAll(tasks);
}
```

## Timeout Pattern

```csharp
public async Task<T> WithTimeoutAsync<T>(
    Func<CancellationToken, Task<T>> operation,
    TimeSpan timeout,
    CancellationToken cancellationToken = default)
{
    using var cts = CancellationTokenSource.CreateLinkedTokenSource(cancellationToken);
    cts.CancelAfter(timeout);
    
    try
    {
        return await operation(cts.Token);
    }
    catch (OperationCanceledException) when (!cancellationToken.IsCancellationRequested)
    {
        throw new TimeoutException($"Operation timed out after {timeout}");
    }
}

// Usage:
var result = await WithTimeoutAsync(
    ct => _api.FetchDataAsync(ct),
    timeout: TimeSpan.FromSeconds(30));
```

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| `async void` | Exceptions lost, can't await | Use `async Task`, except event handlers |
| `.Result` / `.Wait()` | Deadlock on UI thread | `await` all the way |
| Missing `try-catch` in commands | Unhandled exceptions crash | Wrap async commands |
| Ignoring `CancellationToken` | Can't cancel operations | Pass token through chain |
| Fire-and-forget without logging | Silent failures | Use `FireAndForget` extension |
| `Task.Run` for I/O | Wastes thread pool | Use async I/O APIs |

## Testing Async Code

```csharp
[Fact]
public async Task LoadWidgetsAsync_WhenCancelled_ThrowsOperationCancelledException()
{
    // Arrange
    var cts = new CancellationTokenSource();
    cts.Cancel();
    
    // Act & Assert
    await Assert.ThrowsAsync<OperationCanceledException>(
        () => _viewModel.LoadWidgetsCommand.ExecuteAsync(cts.Token));
}

[Fact]
public async Task LoadWidgetsAsync_OnError_SetsErrorMessage()
{
    // Arrange
    _mockRepo.Setup(r => r.GetAllAsync(It.IsAny<CancellationToken>()))
        .ThrowsAsync(new InvalidOperationException("DB error"));
    
    // Act
    await _viewModel.LoadWidgetsCommand.ExecuteAsync(null);
    
    // Assert
    Assert.NotNull(_viewModel.ErrorMessage);
    Assert.False(_viewModel.IsLoading);
}
```

## References

- [Async/Await Best Practices](https://docs.microsoft.com/en-us/archive/msdn-magazine/2013/march/async-await-best-practices-in-asynchronous-programming)
- [ConfigureAwait FAQ](https://devblogs.microsoft.com/dotnet/configureawait-faq/)
