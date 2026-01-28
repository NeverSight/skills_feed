---
name: wpf-mvvm-generator
description: WPF MVVM code generator. Creates ViewModel, View, and Model with CommunityToolkit.Mvvm source generators. Use when scaffolding new WPF features or entities following MVVM pattern.
user-invocable: true
argument-hint: "<entity_name> [type]"
context: fork
model: sonnet
allowed-tools:
  - Read
  - Glob
  - Write
  - Edit
---

# WPF MVVM Generator Skill

Generates WPF MVVM components using CommunityToolkit.Mvvm source generators.

## Arguments

- `$ARGUMENTS[0]`: Entity name (required) - e.g., `User`, `Product`, `Order`
- `$ARGUMENTS[1]`: Generation type (optional): `viewmodel`, `view`, `model`, `all` (default: `all`)

## Execution Steps

### Step 1: Validate Arguments

If `$ARGUMENTS[0]` is empty:
- Ask user for entity name
- Suggest based on existing Models in the project

### Step 2: Scan Project Structure

Identify existing patterns:
- Check `/ViewModels`, `/Views`, `/Models` directories
- Detect namespace conventions
- Find existing base classes or interfaces

### Step 3: Generate Code

Based on `$ARGUMENTS[1]`:

## Generated Components

### Model (`model`)

```csharp
namespace {Namespace}.Models;

/// <summary>
/// {EntityName} domain model
/// </summary>
public sealed class {EntityName}
{
    public required int Id { get; init; }
    public required string Name { get; init; }
    // Additional properties based on context
}
```

### ViewModel (`viewmodel`)

```csharp
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using CommunityToolkit.Mvvm.Messaging;

namespace {Namespace}.ViewModels;

/// <summary>
/// ViewModel for {EntityName} management
/// </summary>
public partial class {EntityName}ViewModel : ObservableObject
{
    private readonly I{EntityName}Service _{entityName}Service;

    public {EntityName}ViewModel(I{EntityName}Service {entityName}Service)
    {
        _{entityName}Service = {entityName}Service;
    }

    [ObservableProperty]
    [NotifyPropertyChangedFor(nameof(HasSelection))]
    [NotifyCanExecuteChangedFor(nameof(DeleteCommand))]
    private {EntityName}? _selected{EntityName};

    [ObservableProperty]
    [NotifyCanExecuteChangedFor(nameof(SaveCommand))]
    private bool _isModified;

    [ObservableProperty]
    private bool _isLoading;

    public bool HasSelection => Selected{EntityName} is not null;

    [RelayCommand]
    private async Task LoadAsync(CancellationToken cancellationToken = default)
    {
        IsLoading = true;
        try
        {
            // Load logic
        }
        finally
        {
            IsLoading = false;
        }
    }

    [RelayCommand(CanExecute = nameof(CanSave))]
    private async Task SaveAsync(CancellationToken cancellationToken = default)
    {
        await _{entityName}Service.SaveAsync(Selected{EntityName}!, cancellationToken);
        IsModified = false;
    }

    private bool CanSave() => IsModified && Selected{EntityName} is not null;

    [RelayCommand(CanExecute = nameof(CanDelete))]
    private async Task DeleteAsync(CancellationToken cancellationToken = default)
    {
        if (Selected{EntityName} is null) return;

        await _{entityName}Service.DeleteAsync(Selected{EntityName}.Id, cancellationToken);

        WeakReferenceMessenger.Default.Send(
            new {EntityName}DeletedMessage(Selected{EntityName}));

        Selected{EntityName} = null;
    }

    private bool CanDelete() => Selected{EntityName} is not null;
}
```

### View (`view`)

```xml
<UserControl x:Class="{Namespace}.Views.{EntityName}View"
             xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
             xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
             xmlns:vm="{Namespace}.ViewModels"
             mc:Ignorable="d"
             d:DataContext="{d:DesignInstance vm:{EntityName}ViewModel, IsDesignTimeCreatable=False}">

    <Grid>
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="*"/>
            <RowDefinition Height="Auto"/>
        </Grid.RowDefinitions>

        <!-- Header -->
        <TextBlock Grid.Row="0"
                   Text="{EntityName} Management"
                   Style="{StaticResource HeaderStyle}"/>

        <!-- Content -->
        <ContentControl Grid.Row="1"
                        Content="{Binding Selected{EntityName}}"
                        Visibility="{Binding HasSelection, Converter={StaticResource BoolToVisibility}}"/>

        <!-- Actions -->
        <StackPanel Grid.Row="2"
                    Orientation="Horizontal"
                    HorizontalAlignment="Right">
            <Button Content="Save"
                    Command="{Binding SaveCommand}"/>
            <Button Content="Delete"
                    Command="{Binding DeleteCommand}"/>
        </StackPanel>

        <!-- Loading Overlay -->
        <Border Grid.RowSpan="3"
                Background="#80000000"
                Visibility="{Binding IsLoading, Converter={StaticResource BoolToVisibility}}">
            <ProgressBar IsIndeterminate="True" Width="200"/>
        </Border>
    </Grid>
</UserControl>
```

### Code-Behind (minimal)

```csharp
namespace {Namespace}.Views;

public partial class {EntityName}View : UserControl
{
    public {EntityName}View()
    {
        InitializeComponent();
    }
}
```

### Message Types

```csharp
namespace {Namespace}.Messages;

public sealed record {EntityName}DeletedMessage({EntityName} Deleted{EntityName});
public sealed record {EntityName}SelectedMessage({EntityName} Selected{EntityName});
public sealed record {EntityName}SavedMessage({EntityName} Saved{EntityName});
```

### Service Interface

```csharp
namespace {Namespace}.Services;

public interface I{EntityName}Service
{
    Task<IReadOnlyList<{EntityName}>> GetAllAsync(CancellationToken cancellationToken = default);
    Task<{EntityName}?> GetByIdAsync(int id, CancellationToken cancellationToken = default);
    Task SaveAsync({EntityName} entity, CancellationToken cancellationToken = default);
    Task DeleteAsync(int id, CancellationToken cancellationToken = default);
}
```

## Output Format

```markdown
# MVVM Generation Results

## Entity: {EntityName}

### Generated Files
| File | Path | Status |
|------|------|--------|
| Model | /Models/{EntityName}.cs | Created |
| ViewModel | /ViewModels/{EntityName}ViewModel.cs | Created |
| View | /Views/{EntityName}View.xaml | Created |
| Code-Behind | /Views/{EntityName}View.xaml.cs | Created |
| Messages | /Messages/{EntityName}Messages.cs | Created |
| Service Interface | /Services/I{EntityName}Service.cs | Created |

### Next Steps
1. Implement `I{EntityName}Service`
2. Register in DI container
3. Add navigation to the view
4. Create design-time data if needed
```

## Guidelines

- Use CommunityToolkit.Mvvm source generators exclusively
- Follow existing project naming conventions
- Generate minimal code-behind (UI logic only)
- Include proper XML documentation
- Support async operations with cancellation
- Use WeakReferenceMessenger for cross-ViewModel communication
