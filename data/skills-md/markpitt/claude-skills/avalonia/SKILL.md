---
name: avalonia
description: Expert guidance for developing cross-platform desktop applications with Avalonia UI framework. Use when building, debugging, or optimizing Avalonia apps including MVVM architecture, XAML design, data binding, styling, theming, custom controls, and cross-platform deployment for Windows, macOS, Linux, iOS, Android, and WebAssembly.
version: 2.0
---

# Avalonia UI Framework - Orchestration Hub

Modular guidance for cross-platform desktop and mobile development using Avalonia, a WPF-inspired XAML-based framework for .NET.

## Quick Reference: When to Load Which Resource

| Task/Goal | Load Resource |
|-----------|---------------|
| MVVM patterns, data binding, dependency injection, value converters | `resources/mvvm-databinding.md` |
| UI controls reference (layouts, inputs, collections, menus) | `resources/controls-reference.md` |
| Custom controls, advanced layouts, performance optimization, virtualization | `resources/custom-controls-advanced.md` |
| Styling, themes, animations, control templates | `resources/styling-guide.md` |
| Reactive patterns, commands, observables, animations | `resources/reactive-animations.md` |
| Windows, macOS, Linux, iOS, Android implementation details | `resources/platform-specific.md` |

## Framework Overview

**Avalonia** is a cross-platform XAML framework supporting:
- **Platforms**: Windows, macOS, Linux, iOS, Android, WebAssembly
- **Architecture**: MVVM with ReactiveUI support
- **Styling**: CSS-like selectors with Fluent/Simple themes
- **Features**: Data binding, reactive commands, observable collections, custom controls
- **Modern .NET**: .NET 6+ and .NET Standard 2.0

### Standard Project Structure

```
MyAvaloniaApp/
├── MyAvaloniaApp/                  # Shared code
│   ├── App.axaml
│   ├── Views/                      # XAML views
│   ├── ViewModels/                 # Business logic + state
│   ├── Models/                     # Data models
│   ├── Services/                   # Application services
│   ├── Converters/                 # Value converters
│   ├── Assets/                     # Images, fonts
│   └── Styles/                     # Style resources
├── MyAvaloniaApp.Desktop/          # Desktop-specific (Win/Mac/Linux)
├── MyAvaloniaApp.Android/          # Android-specific (optional)
├── MyAvaloniaApp.iOS/              # iOS-specific (optional)
└── MyAvaloniaApp.Browser/          # WebAssembly (optional)
```

## Getting Started

### Minimal Setup

```csharp
// Program.cs
public static void Main(string[] args)
{
    BuildAvaloniaApp().StartWithClassicDesktopLifetime(args);
}

public static AppBuilder BuildAvaloniaApp() =>
    AppBuilder.Configure<App>()
        .UsePlatformDetect()
        .LogToTrace();
```

```xml
<!-- App.axaml -->
<Application xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             x:Class="MyApp.App">
    <Application.Styles>
        <FluentTheme />
    </Application.Styles>
</Application>
```

```xml
<!-- Views/MainWindow.axaml -->
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        x:Class="MyApp.Views.MainWindow"
        Title="My Application"
        Width="800"
        Height="600">
    <StackPanel Padding="20" Spacing="10">
        <TextBlock Text="Hello, Avalonia!" FontSize="24" FontWeight="Bold" />
    </StackPanel>
</Window>
```

## Core Patterns

### MVVM Architecture Pattern

1. **View** (XAML): UI presentation with data bindings
2. **ViewModel** (C#): State management and commands
3. **Model** (C#): Business logic and data access
4. **Service**: Cross-cutting concerns (DI/IoC)

**Load** `resources/mvvm-databinding.md` for:
- ViewModel base classes
- Data binding modes and paths
- Multi-binding and converters
- Dependency injection setup
- Design-time data

### Reactive Programming Pattern

Leverage ReactiveUI for event-driven UI updates:

```csharp
this.WhenAnyValue(x => x.SearchText)
    .Debounce(TimeSpan.FromMilliseconds(300))
    .Subscribe(text => PerformSearch(text));
```

**Load** `resources/reactive-animations.md` for:
- Reactive properties and commands
- Observable sequences
- Animations and transitions
- Performance optimization

### Platform-Adaptive Pattern

Design once, adapt per platform:

```xml
<OnPlatform Default="16">
    <On Options="Windows" Content="14" />
    <On Options="macOS" Content="15" />
</OnPlatform>
```

**Load** `resources/platform-specific.md` for:
- Runtime platform detection
- Platform-specific services
- Conditional UI rendering
- Native dialogs and features

## Navigation by Task

### "I need to build a form with validation"

1. Load `resources/mvvm-databinding.md` → Implement ViewModel with property validation
2. Load `resources/controls-reference.md` → Find TextBox, ComboBox, Button controls
3. Load `resources/reactive-animations.md` → Add debounced validation with observables

### "I'm seeing poor performance with large lists"

1. Load `resources/custom-controls-advanced.md` → Enable virtualization
2. Load `resources/mvvm-databinding.md` → Use compiled bindings
3. Load `resources/reactive-animations.md` → Debounce/throttle updates

### "I need platform-specific behavior"

1. Load `resources/platform-specific.md` → Implement service interfaces
2. Load `resources/mvvm-databinding.md` → Register platform implementations via DI
3. Platform-specific `resources/` → Implement per-platform project

### "I want custom styling and animations"

1. Load `resources/styling-guide.md` → Define styles and themes
2. Load `resources/reactive-animations.md` → Add animations to styles
3. Load `resources/custom-controls-advanced.md` → Custom control templates

### "I'm building a complex control"

1. Load `resources/custom-controls-advanced.md` → TemplatedControl or UserControl pattern
2. Load `resources/mvvm-databinding.md` → Attached properties and data binding
3. Load `resources/styling-guide.md` → Control templates and styling

## Resource Organization

### `mvvm-databinding.md` (Primary)
- Architecture overview
- ViewModel patterns with ReactiveUI
- Binding modes and syntax
- Value converters
- Collections and list binding
- Design-time data
- Master-detail and tab patterns

### `controls-reference.md` (Primary)
- Layout controls (Grid, StackPanel, DockPanel, etc.)
- Input controls (TextBox, Button, CheckBox, ComboBox, etc.)
- Display controls (TextBlock, Image, ProgressBar, etc.)
- Collection controls (ListBox, DataGrid, TreeView, etc.)
- Navigation (Menu, TabControl, SplitView, etc.)
- Shapes and drawing

### `styling-guide.md` (Primary)
- CSS-like selectors (type, class, pseudo-classes)
- Resource dictionaries and themes
- Control templates
- Data templates
- Animations and transitions
- Easing functions
- Theme variants (light/dark)

### `reactive-animations.md` (Advanced)
- ReactiveUI integration
- Reactive properties
- Reactive commands (sync and async)
- Observable sequences
- Filtering, transformation, combining
- Programmatic animations
- Common patterns (search, validation, auto-complete)

### `custom-controls-advanced.md` (Advanced)
- Custom TemplatedControl creation
- User control composition
- Advanced layouts
- Virtualization
- Performance optimization
- Render transforms
- Graphics and drawing

### `platform-specific.md` (Advanced)
- Runtime platform detection
- Multi-project structure
- Service abstractions
- Platform-specific implementations
- Window management per platform
- File system access
- Native features (Windows DLL, macOS Cocoa, etc.)

## Common Workflows

### Build a Desktop App (Windows/macOS/Linux)

```
1. → Setup: Standard project structure + FluentTheme
2. → Create Views and ViewModels following MVVM
3. → Use controls-reference for UI layouts
4. → Add styles with styling-guide
5. → Implement services with DI (mvvm-databinding)
6. → Add animations with reactive-animations
7. → Test on each platform with platform-specific guidance
```

### Build a Cross-Platform Mobile+Desktop App

```
1. → Create shared project + platform-specific projects
2. → Define service interfaces in shared code (mvvm-databinding)
3. → Implement services per platform (platform-specific)
4. → Use OnPlatform for adaptive UI
5. → Register platform implementations via DI
6. → Test thoroughly on each target (iOS/Android/Windows/Mac)
```

### Add Real-Time Search

```
1. → Create SearchViewModel (mvvm-databinding)
2. → Use ObservableCollection for results (mvvm-databinding)
3. → Implement with reactive search pattern (reactive-animations)
4. → Debounce input to reduce API calls
5. → Display with ListBox (controls-reference)
6. → Style with appropriate CSS selectors (styling-guide)
```

### Build Complex Data-Driven UI

```
1. → Design ViewModel hierarchy (mvvm-databinding)
2. → Create master-detail view (mvvm-databinding)
3. → Use DataGrid for tabular data (controls-reference)
4. → Add sorting/filtering with observables (reactive-animations)
5. → Optimize with virtualization (custom-controls-advanced)
6. → Add custom controls if needed (custom-controls-advanced)
```

## Best Practices Summary

**Architecture**
- Maintain strict MVVM separation of concerns
- Use dependency injection for testability
- Keep business logic in ViewModels, not Views

**Performance**
- Enable compiled bindings with `x:DataType`
- Virtualize large collections
- Debounce rapid updates

**Styling**
- Use resource dictionaries for consistency
- Support light and dark themes
- Test styles on all target platforms

**Reactive Patterns**
- Use observables for event-driven updates
- Debounce/throttle input-triggered operations
- Always handle ThrownExceptions on commands

**Testing**
- Unit test ViewModels in isolation
- Use Avalonia.Headless for UI testing
- Provide design-time DataContext in XAML

## Cross-Platform Deployment

- **Windows**: ClickOnce, MSI, portable exe
- **macOS**: DMG, homebrew
- **Linux**: AppImage, snap, flatpak
- **Mobile**: Apple App Store, Google Play Store
- **Web**: Static hosting (WASM runtime required)

Refer to `resources/platform-specific.md` for platform-specific build and deployment guidance.

---

**Navigation**: Choose a resource above based on your task. Each resource is self-contained with comprehensive examples and best practices.
