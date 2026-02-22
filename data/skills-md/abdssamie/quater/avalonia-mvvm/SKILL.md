---
name: avalonia-mvvm
description: Implement MVVM patterns using CommunityToolkit.Mvvm in Avalonia applications with ViewModels, Commands, and Dependency Injection
license: MIT
compatibility: opencode
metadata:
  audience: avalonia-developers
  framework: avalonia
---

# MVVM Patterns in Avalonia

Complete guide to MVVM patterns using CommunityToolkit.Mvvm in Avalonia applications.

## What I do

- Guide implementation of ViewModels with ObservableObject base class
- Show how to create observable properties with [ObservableProperty] attribute
- Demonstrate command patterns with [RelayCommand] including async and CanExecute
- Explain View-ViewModel mapping using DataTemplates (critical for navigation)
- Show dependency injection patterns for passing services to ViewModels

## When to use me

Use this skill when you need to:

- Create new ViewModels for Avalonia views
- Implement observable properties that notify the UI of changes
- Add commands to handle user interactions (button clicks, etc.)
- Set up navigation patterns with SukiSideMenu or ContentControl
- Pass services (like ISukiToastManager) between ViewModels
- Implement validation on ViewModel properties

## ViewModel Base Classes

### Basic ViewModel

```cs
using CommunityToolkit.Mvvm.ComponentModel;

namespace YourApp.ViewModels;

public partial class ViewModelBase : ObservableObject
{
}
```

### Page ViewModel Base

```cs
using CommunityToolkit.Mvvm.ComponentModel;

namespace YourApp.ViewModels;

public abstract partial class PageViewModelBase : ViewModelBase
{
    public abstract string DisplayName { get; }
    public abstract string Icon { get; }
}
```

## Observable Properties

### Basic Observable Property

```cs
[ObservableProperty]
private string _name = "";
```

### With Validation

```cs
using System.ComponentModel.DataAnnotations;

[ObservableProperty]
[Required(ErrorMessage = "Name is required")]
[MinLength(3, ErrorMessage = "Name must be at least 3 characters")]
private string _name = "";
```

### With Property Changed Notification

```cs
[ObservableProperty]
private string _firstName = "";

[ObservableProperty]
private string _lastName = "";

public string FullName => $"{FirstName} {LastName}";

partial void OnFirstNameChanged(string value)
{
    OnPropertyChanged(nameof(FullName));
}

partial void OnLastNameChanged(string value)
{
    OnPropertyChanged(nameof(FullName));
}
```

## Commands

### Basic Command

```cs
[RelayCommand]
private void Save()
{
    // Save logic
}
```

### Command with Parameter

```cs
[RelayCommand]
private void ButtonClick(string buttonName)
{
    LastButtonClicked = buttonName;
}
```

**View:**

```xml
<Button Content="Save" 
        Command="{Binding ButtonClickCommand}" 
        CommandParameter="Save Button" />
```

### Async Command

```cs
[RelayCommand]
private async Task LoadDataAsync()
{
    IsLoading = true;
    await Task.Delay(1000);
    IsLoading = false;
}
```

### Command with CanExecute

```cs
[ObservableProperty]
private bool _isDataLoaded;

[RelayCommand(CanExecute = nameof(CanSave))]
private void Save()
{
    // Save logic
}

private bool CanSave() => IsDataLoaded;

partial void OnIsDataLoadedChanged(bool value)
{
    SaveCommand.NotifyCanExecuteChanged();
}
```

## Critical Pattern: DataTemplates

When using navigation patterns where ViewModels are displayed in a ContentControl (like SukiSideMenu), you MUST define DataTemplates to map ViewModels to their corresponding Views.

**In SukiWindow:**

```xml
<suki:SukiWindow.DataTemplates>
    <DataTemplate DataType="vm:HomePageViewModel">
        <views:HomePage />
    </DataTemplate>
    <DataTemplate DataType="vm:SettingsPageViewModel">
        <views:SettingsPage />
    </DataTemplate>
</suki:SukiWindow.DataTemplates>
```

## Dependency Injection

### Passing Services to ViewModels

**Parent ViewModel:**

```csharp
public partial class MainWindowViewModel : ViewModelBase
{
    private readonly ISukiToastManager _toastManager;

    public MainWindowViewModel()
    {
        _toastManager = new SukiToastManager();
        Pages = new ObservableCollection<PageViewModelBase>
        {
            new NotificationsPageViewModeler)
        };
    }
}
```

**Child ViewModel:**

```csharp
public partial class NotificationsPageViewModel : PageViewModelBase
{
    private readonly ISukiToastManager _toastManager;

    public NotificationsPageViewModel(ISukiToastManager toastManager)
    {
        _toastManager = toastManager;
    }
}
```

## Common Mistakes to Avoid

1. Forgetting DataTemplates - Navigation won't work without ViewModel-to-View mapping
2. Not using partial class - CommunityToolkit.Mvvm requires partial keyword
3. Missing OnPropertyChanged - Computed properties won't update without manual notification
4. Not calling NotifyCanEuteChanged - Commands with CanExecute won't re-evaluate automatically
5. Using wrong field naming - Observable property fields must start with underscore and be private

## Best Practices

1. Always use partial keyword on ViewModels
2. Use [ObservableProperty] instead of manual INotifyPropertyChanged
3. Use [RelayCommand] instead of manual ICommand implementation
4. Define DataTemplates in the root window for navigation scenarios
5. Pass services through constructor injection
6. Use computed properties for derived values
7. Implement validation attributes on properties need validation
