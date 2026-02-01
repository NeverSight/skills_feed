---
name: maui-blazor-development
description: |
  Expert guidance for .NET MAUI Blazor Hybrid development combining native mobile/desktop apps with Blazor web UI.
  Use when working with: (1) .NET MAUI Blazor Hybrid apps, (2) BlazorWebView components, (3) Cross-platform apps sharing Blazor UI,
  (4) Platform integration in Blazor Hybrid, (5) MVVM with Blazor components, (6) Navigation between MAUI pages and Razor components,
  (7) Shared Razor Class Libraries (RCL) for MAUI and Web. Applies to any .NET MAUI project using Blazor for UI.
---

# .NET MAUI Blazor Hybrid Development

Expert guidance for building cross-platform apps with .NET MAUI and Blazor.

## Implementation Workflow

### 1. Analysis Phase (Required)

Before implementation, determine:

- **App type**: Pure MAUI Blazor or MAUI + Blazor Web App (shared UI)
- **Platform targets**: Android, iOS, Windows, macOS
- **Native features needed**: Sensors, camera, file system, notifications
- **State management**: Component state, MVVM, or hybrid approach
- **Navigation pattern**: Blazor-only, Shell, or mixed navigation

### 2. Architecture Decision

| Scenario | Recommended Approach |
|----------|---------------------|
| Mobile-first with some web | `maui-blazor` template |
| Shared UI across mobile + web | `maui-blazor-web` template with RCL |
| Complex native integration | MVVM with platform services |
| Simple data-driven UI | Component state with DI services |

### 3. Project Setup

```csharp
// MauiProgram.cs - Essential setup
public static MauiApp CreateMauiApp()
{
    var builder = MauiApp.CreateBuilder();
    builder
        .UseMauiApp<App>()
        .ConfigureFonts(fonts =>
        {
            fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
        });

    builder.Services.AddMauiBlazorWebView();
#if DEBUG
    builder.Services.AddBlazorWebViewDeveloperTools();
#endif

    // Register services
    builder.Services.AddSingleton<IDeviceService, DeviceService>();
    builder.Services.AddScoped<IDataService, DataService>();

    return builder.Build();
}
```

### 4. BlazorWebView Configuration

```xml
<!-- MainPage.xaml -->
<ContentPage xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:b="clr-namespace:Microsoft.AspNetCore.Components.WebView.Maui;assembly=Microsoft.AspNetCore.Components.WebView.Maui">
    <b:BlazorWebView HostPage="wwwroot/index.html">
        <b:BlazorWebView.RootComponents>
            <b:RootComponent Selector="#app" ComponentType="{x:Type local:Main}" />
        </b:BlazorWebView.RootComponents>
    </b:BlazorWebView>
</ContentPage>
```

## Core Patterns

### Dependency Injection

| Lifetime | Use Case |
|----------|----------|
| `AddSingleton<T>` | App-wide state, device services, settings |
| `AddScoped<T>` | Per-BlazorWebView instance state |
| `AddTransient<T>` | Stateless utilities, factories |

```csharp
// Interface for platform-specific implementation
public interface IDeviceService
{
    string GetDeviceModel();
    Task<bool> HasPermissionAsync(string permission);
}

// Platform implementation registered in MauiProgram.cs
builder.Services.AddSingleton<IDeviceService, DeviceService>();
```

### Component Lifecycle

```csharp
@code {
    [Parameter] public string Id { get; set; } = "";

    // Called once when component initializes
    protected override async Task OnInitializedAsync()
    {
        await LoadDataAsync();
    }

    // Called when parameters change (including first render)
    protected override void OnParametersSet()
    {
        // React to parameter changes
    }

    // Called after each render
    protected override void OnAfterRender(bool firstRender)
    {
        if (firstRender)
        {
            // JS interop safe here
        }
    }
}
```

### Platform Feature Access

```csharp
// Check platform and access native features
@inject IDeviceService DeviceService

@if (DeviceInfo.Current.Platform == DevicePlatform.Android)
{
    <AndroidSpecificComponent />
}

@code {
    private async Task AccessCameraAsync()
    {
        var status = await Permissions.CheckStatusAsync<Permissions.Camera>();
        if (status != PermissionStatus.Granted)
        {
            status = await Permissions.RequestAsync<Permissions.Camera>();
        }

        if (status == PermissionStatus.Granted)
        {
            // Use camera
        }
    }
}
```

### State Updates from External Events

```csharp
@implements IDisposable
@inject IDataService DataService

<p>@message</p>

@code {
    private string message = "";

    protected override void OnInitialized()
    {
        DataService.OnDataChanged += HandleDataChanged;
    }

    private async void HandleDataChanged(object? sender, EventArgs e)
    {
        message = "Data updated!";
        await InvokeAsync(StateHasChanged); // Required for external events
    }

    public void Dispose()
    {
        DataService.OnDataChanged -= HandleDataChanged;
    }
}
```

## Reference Documentation

For detailed patterns and examples, see:

- **[Project Structure](../../references/project-structure.md)**: Solution templates, RCL setup, multi-targeting
- **[Blazor Components](../../references/blazor-components.md)**: Lifecycle, RenderFragment, EventCallback, data binding
- **[Platform Integration](../../references/platform-integration.md)**: Device APIs, permissions, platform-specific code
- **[Navigation & Routing](../../references/navigation-routing.md)**: Blazor routing, Shell, deep linking
- **[State Management](../../references/state-management.md)**: MVVM, DI patterns, CommunityToolkit.Mvvm

## Quick Reference

### Common Service Registration

```csharp
// Services
builder.Services.AddSingleton<ISettingsService, SettingsService>();
builder.Services.AddSingleton<IConnectivity>(Connectivity.Current);
builder.Services.AddSingleton<IGeolocation>(Geolocation.Default);

// ViewModels (if using MVVM)
builder.Services.AddTransient<MainViewModel>();
builder.Services.AddTransient<SettingsViewModel>();

// Pages with DI
builder.Services.AddTransient<MainPage>();
```

### Platform Checks

```csharp
// Runtime platform check
if (DeviceInfo.Current.Platform == DevicePlatform.iOS) { }
if (DeviceInfo.Current.Platform == DevicePlatform.Android) { }
if (DeviceInfo.Current.Platform == DevicePlatform.WinUI) { }
if (DeviceInfo.Current.Platform == DevicePlatform.macOS) { }

// Compile-time platform check
#if ANDROID
    // Android-specific code
#elif IOS
    // iOS-specific code
#elif WINDOWS
    // Windows-specific code
#endif
```

### Navigation Patterns

```csharp
// Blazor navigation (within BlazorWebView)
@inject NavigationManager Navigation
Navigation.NavigateTo("/details/123");

// MAUI navigation (to other pages)
await Navigation.PushAsync(new SettingsPage());
await Shell.Current.GoToAsync("//settings");
```
