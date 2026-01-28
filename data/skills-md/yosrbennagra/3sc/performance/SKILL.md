---
name: performance
description: Performance optimization patterns for the 3SC widget host. Covers startup time, memory management, UI responsiveness, profiling, and optimization strategies.
---

# Performance

## Overview

A performant desktop application starts quickly, responds immediately to user input, and uses resources efficiently. This skill covers performance patterns for WPF applications.

## Definition of Done (DoD)

- [ ] Application starts in under 3 seconds on typical hardware
- [ ] UI remains responsive during background operations
- [ ] Memory usage stays bounded during normal use
- [ ] No memory leaks after extended use
- [ ] Large operations show progress feedback
- [ ] Performance-critical paths are profiled and optimized

## Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Cold startup | < 3s | Time to usable shell |
| Warm startup | < 1s | Subsequent launches |
| UI response | < 100ms | Input to visual feedback |
| Frame rate | 60 FPS | During animations |
| Memory (idle) | < 150MB | After startup |
| Memory (active) | < 500MB | With 10+ widgets |

## Startup Optimization

### Lazy Initialization

```csharp
public sealed class ServiceLocator
{
    // ✅ GOOD - Defer expensive initialization
    private readonly Lazy<AppDbContext> _dbContext;
    private readonly Lazy<IWorkshopSyncService> _syncService;
    
    private ServiceLocator()
    {
        // Database context created on first use
        _dbContext = new Lazy<AppDbContext>(() =>
        {
            var options = CreateDbOptions();
            var context = new AppDbContext(options);
            context.Database.EnsureCreated();
            return context;
        });
        
        // Sync service not needed until user requests
        _syncService = new Lazy<IWorkshopSyncService>(() =>
            new WorkshopSyncService(/* deps */));
    }
}
```

### Startup Timing

```csharp
public class StartupTimer
{
    public static StartupTimer Instance { get; } = new();
    
    private readonly Stopwatch _stopwatch = new();
    private readonly List<(string Name, long ElapsedMs)> _checkpoints = new();
    private string _currentPhase = "Init";
    
    public void Start() => _stopwatch.Start();
    
    public void BeginPhase(string phase)
    {
        Checkpoint($"{_currentPhase}Complete");
        _currentPhase = phase;
    }
    
    public void Checkpoint(string name)
    {
        _checkpoints.Add((name, _stopwatch.ElapsedMilliseconds));
    }
    
    public void Complete()
    {
        _stopwatch.Stop();
        Checkpoint("StartupComplete");
        
        Log.Information("Startup completed in {TotalMs}ms", _stopwatch.ElapsedMilliseconds);
        
        foreach (var (name, elapsed) in _checkpoints)
        {
            Log.Debug("Startup checkpoint: {Name} at {Elapsed}ms", name, elapsed);
        }
        
        TelemetryEventSource.Log.StartupTiming(_stopwatch.ElapsedMilliseconds);
    }
}

// Usage in App.xaml.cs
protected override void OnStartup(StartupEventArgs e)
{
    StartupTimer.Instance.Start();
    
    StartupTimer.Instance.BeginPhase("Logging");
    LogBootstrapper.Initialize();
    
    StartupTimer.Instance.BeginPhase("UI");
    InitializeTrayIcon();
    InitializeShell();
    
    StartupTimer.Instance.BeginPhase("Data");
    // Async, don't block
    _ = LoadWidgetsAsync();
    
    StartupTimer.Instance.Complete();
}
```

### Defer Non-Critical Work

```csharp
protected override async void OnStartup(StartupEventArgs e)
{
    base.OnStartup(e);
    
    // Critical path - show UI immediately
    _shellWindow = new ShellWindow();
    _shellWindow.Show();
    
    // Defer non-critical initialization
    await Dispatcher.InvokeAsync(async () =>
    {
        await Task.Delay(500);  // Let UI render first
        
        // Now load widgets, sync, etc.
        await LoadWidgetsAsync();
        await CheckForUpdatesAsync();
    }, DispatcherPriority.Background);
}
```

## UI Responsiveness

### Async Commands

```csharp
[RelayCommand]
private async Task LoadWidgetsAsync(CancellationToken ct)
{
    IsLoading = true;
    
    try
    {
        // Run on background thread
        var widgets = await Task.Run(
            () => _repository.GetAllAsync(ct), ct);
        
        // Update UI on dispatcher
        Widgets = new ObservableCollection<WidgetViewModel>(
            widgets.Select(w => new WidgetViewModel(w)));
    }
    finally
    {
        IsLoading = false;
    }
}
```

### Progress Reporting

```csharp
[RelayCommand]
private async Task InstallPackagesAsync(
    IEnumerable<WidgetPackage> packages, 
    CancellationToken ct)
{
    var packageList = packages.ToList();
    var total = packageList.Count;
    var current = 0;
    
    Progress = 0;
    StatusMessage = "Installing widgets...";
    
    foreach (var package in packageList)
    {
        ct.ThrowIfCancellationRequested();
        
        StatusMessage = $"Installing {package.DisplayName}...";
        await _installer.InstallAsync(package, ct);
        
        current++;
        Progress = (double)current / total * 100;
    }
    
    StatusMessage = $"Installed {total} widgets";
}
```

### UI Thread Monitor

```csharp
public class UiResponsivenessMonitor : IDisposable
{
    private readonly DispatcherTimer _timer;
    private DateTimeOffset _lastTick;
    private const int WarningThresholdMs = 200;
    
    public UiResponsivenessMonitor()
    {
        _timer = new DispatcherTimer
        {
            Interval = TimeSpan.FromMilliseconds(100)
        };
        _timer.Tick += OnTick;
    }
    
    public void Start()
    {
        _lastTick = DateTimeOffset.UtcNow;
        _timer.Start();
    }
    
    private void OnTick(object? sender, EventArgs e)
    {
        var now = DateTimeOffset.UtcNow;
        var elapsed = (now - _lastTick).TotalMilliseconds;
        
        if (elapsed > WarningThresholdMs)
        {
            Log.Warning(
                "UI thread blocked for {Elapsed}ms (expected ~100ms)",
                elapsed);
            
            TelemetryEventSource.Log.UiBlocked((long)elapsed);
        }
        
        _lastTick = now;
    }
    
    public void Stop() => _timer.Stop();
    public void Dispose() => _timer.Stop();
}
```

## Memory Management

### Memory Monitoring

```csharp
public class MemoryMonitor
{
    public static MemoryMonitor Instance { get; } = new();
    
    private readonly Dictionary<string, long> _snapshots = new();
    
    public void TakeSnapshot(string name)
    {
        GC.Collect();
        GC.WaitForPendingFinalizers();
        GC.Collect();
        
        var memory = GC.GetTotalMemory(forceFullCollection: false);
        _snapshots[name] = memory;
        
        Log.Debug("Memory snapshot {Name}: {MemoryMB:F2}MB", 
            name, memory / 1024.0 / 1024.0);
    }
    
    public void CheckForLeaks()
    {
        if (_snapshots.TryGetValue("AppStarted", out var startMemory) &&
            _snapshots.TryGetValue("AppShutdown", out var endMemory))
        {
            var growthMb = (endMemory - startMemory) / 1024.0 / 1024.0;
            
            if (growthMb > 100)  // More than 100MB growth
            {
                Log.Warning(
                    "Potential memory leak: Memory grew by {GrowthMB:F2}MB during session",
                    growthMb);
            }
        }
    }
    
    public MemoryInfo GetCurrentInfo()
    {
        var process = Process.GetCurrentProcess();
        
        return new MemoryInfo
        {
            ManagedMemoryMB = GC.GetTotalMemory(false) / 1024.0 / 1024.0,
            WorkingSetMB = process.WorkingSet64 / 1024.0 / 1024.0,
            PrivateMemoryMB = process.PrivateMemorySize64 / 1024.0 / 1024.0,
            Gen0Collections = GC.CollectionCount(0),
            Gen1Collections = GC.CollectionCount(1),
            Gen2Collections = GC.CollectionCount(2)
        };
    }
}

public record MemoryInfo
{
    public double ManagedMemoryMB { get; init; }
    public double WorkingSetMB { get; init; }
    public double PrivateMemoryMB { get; init; }
    public int Gen0Collections { get; init; }
    public int Gen1Collections { get; init; }
    public int Gen2Collections { get; init; }
}
```

### Avoiding Memory Leaks

```csharp
// ❌ BAD - Event handler leak
public class WidgetViewModel
{
    public WidgetViewModel(IEventAggregator events)
    {
        events.ThemeChanged += OnThemeChanged;  // Never unsubscribed!
    }
}

// ✅ GOOD - Weak event or explicit unsubscription
public class WidgetViewModel : IDisposable
{
    private readonly IEventAggregator _events;
    
    public WidgetViewModel(IEventAggregator events)
    {
        _events = events;
        _events.ThemeChanged += OnThemeChanged;
    }
    
    public void Dispose()
    {
        _events.ThemeChanged -= OnThemeChanged;
    }
}

// ✅ BETTER - Use WeakEventManager
public class WidgetViewModel
{
    public WidgetViewModel(IEventAggregator events)
    {
        WeakEventManager<IEventAggregator, EventArgs>.AddHandler(
            events, nameof(events.ThemeChanged), OnThemeChanged);
    }
}
```

### Dispose Pattern

```csharp
public class WidgetWindow : Window, IDisposable
{
    private readonly DispatcherTimer _timer;
    private readonly HttpClient _httpClient;
    private bool _disposed;
    
    protected virtual void Dispose(bool disposing)
    {
        if (_disposed) return;
        
        if (disposing)
        {
            _timer.Stop();
            _httpClient.Dispose();
        }
        
        _disposed = true;
    }
    
    public void Dispose()
    {
        Dispose(true);
        GC.SuppressFinalize(this);
    }
    
    protected override void OnClosed(EventArgs e)
    {
        Dispose();
        base.OnClosed(e);
    }
}
```

## Database Performance

### Query Optimization

```csharp
// ❌ BAD - N+1 queries
foreach (var widget in widgets)
{
    var instances = await _instanceRepo.GetByWidgetKeyAsync(widget.WidgetKey);
}

// ✅ GOOD - Single query with includes
var widgetsWithInstances = await _context.Widgets
    .Include(w => w.Instances)
    .AsNoTracking()
    .ToListAsync(ct);

// ✅ GOOD - Projection to DTO
var widgetSummaries = await _context.Widgets
    .Select(w => new WidgetSummary
    {
        Key = w.WidgetKey,
        Name = w.DisplayName,
        InstanceCount = w.Instances.Count
    })
    .ToListAsync(ct);
```

### Pagination

```csharp
public async Task<PagedResult<Widget>> GetPagedAsync(
    int page, 
    int pageSize, 
    CancellationToken ct)
{
    var query = _context.Widgets.AsNoTracking();
    
    var totalCount = await query.CountAsync(ct);
    
    var items = await query
        .OrderBy(w => w.DisplayName)
        .Skip((page - 1) * pageSize)
        .Take(pageSize)
        .ToListAsync(ct);
    
    return new PagedResult<Widget>
    {
        Items = items,
        TotalCount = totalCount,
        Page = page,
        PageSize = pageSize
    };
}
```

## Virtualization

### UI Virtualization

```xaml
<!-- ✅ GOOD - Virtualized list for large collections -->
<ListBox ItemsSource="{Binding Widgets}"
         VirtualizingStackPanel.IsVirtualizing="True"
         VirtualizingStackPanel.VirtualizationMode="Recycling"
         ScrollViewer.IsDeferredScrollingEnabled="True">
    <ListBox.ItemsPanel>
        <ItemsPanelTemplate>
            <VirtualizingStackPanel />
        </ItemsPanelTemplate>
    </ListBox.ItemsPanel>
</ListBox>

<!-- For grid layouts -->
<ItemsControl ItemsSource="{Binding Widgets}">
    <ItemsControl.ItemsPanel>
        <ItemsPanelTemplate>
            <VirtualizingWrapPanel />  <!-- Custom panel -->
        </ItemsPanelTemplate>
    </ItemsControl.ItemsPanel>
</ItemsControl>
```

## Profiling Checklist

### Before Optimization

1. **Measure first** - Don't guess, profile
2. **Set targets** - Define acceptable performance
3. **Identify bottlenecks** - Focus on hot paths
4. **Test on target hardware** - Not just dev machines

### Tools

| Tool | Purpose |
|------|---------|
| Visual Studio Profiler | CPU, memory, UI analysis |
| PerfView | ETW traces, GC analysis |
| dotMemory | Memory snapshots, leak detection |
| BenchmarkDotNet | Micro-benchmarks |

### Key Metrics to Track

```csharp
public static class PerformanceCounters
{
    private static readonly Stopwatch AppUptime = Stopwatch.StartNew();
    private static long _operationCount;
    
    public static void RecordOperation() => 
        Interlocked.Increment(ref _operationCount);
    
    public static void LogPerformanceSummary()
    {
        var memory = MemoryMonitor.Instance.GetCurrentInfo();
        
        Log.Information(
            "Performance summary - Uptime: {Uptime}, Operations: {OpCount}, " +
            "Memory: {MemoryMB:F1}MB, GC Gen2: {Gen2}",
            AppUptime.Elapsed,
            _operationCount,
            memory.WorkingSetMB,
            memory.Gen2Collections);
    }
}
```

## Anti-Patterns

| Anti-Pattern | Impact | Solution |
|--------------|--------|----------|
| Sync over async | UI freeze | Use async/await properly |
| Large object allocations | GC pressure | Pool or reuse objects |
| Binding to complex objects | Slow rendering | Use lightweight ViewModels |
| Missing virtualization | Memory bloat | Enable UI virtualization |
| Unbounded collections | Memory growth | Use pagination/windowing |

## References

- [WPF Performance](https://docs.microsoft.com/en-us/dotnet/desktop/wpf/advanced/optimizing-wpf-application-performance)
- [.NET Performance Tips](https://docs.microsoft.com/en-us/dotnet/framework/performance/)
- [Memory Management](https://docs.microsoft.com/en-us/dotnet/standard/garbage-collection/)
