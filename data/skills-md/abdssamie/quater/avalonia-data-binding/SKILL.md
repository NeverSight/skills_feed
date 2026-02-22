---
name: avalonia-data-binding
description: Comprehensive guide to data binding patterns in Avalonia for AI agents.
license: MIT
compatibility: opencode
metadata:
  audience: avalonia-developers
  framework: avalonia
---

# Data Binding in Avalonia

Comprehensive guide to data binding patterns in Avalonia for AI agents.

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
- Set up navigation patterns with DataTemplates and ContentControl

# Data Binding in Avalonia

Comprehensive guide to data binding patterns in Avalonia for AI agents.

## Binding Modes

### OneWay Binding

```xml
<!-- ViewModel property updates UI -->
<TextBlock Text="{Binding UserName}" />
<TextBlock Text="{Binding UserName, Mode=OneWay}" />  <!-- Explicit -->
```

### TwoWay Binding

```xml
<!-- UI and ViewModel stay synchronized -->
<TextBox Text="{Binding UserName, Mode=TwoWay}" />
<Slider Value="{Binding Volume, Mode=TwoWay}" />
<CheckBox IsChecked="{Binding IsEnabled, Mode=TwoWay}" />
```

**ViewModel:**

```csharp
[ObservableProperty]
private string _userName = "";

[ObservableProperty]
private double _volume = 50;

[ObservableProperty]
private bool _isEnabled = true;
```

### OneTime Binding

```xml
<!-- Set once, never updates -->
<TextBlock Text="{Binding AppVersion, Mode=OneTime}" />
<Image Source="{Binding StaticImage, Mode=OneTime}" />
```

### OneWayToSource Binding

```xml
<!-- Target updates source, but not vice versa -->
<TextBox Text="{Binding SearchQuery, Mode=OneWayToSource}" />
```

### When to use each

Use:
- **OneWay**: Display data that changes infrequently
- **TwoWay**: User input controls (TextBox, Slider, CheckBox)
- **OneTime**: Static data that won't change after load
- **OneWayToSource**: When UI updates ViewModel but not the other way

## Binding Paths

### Simple Property

```xml
<TextBlock Text="{Binding Name}" />
```

```csharp
[ObservableProperty]
private string _name = "John";
```

### Nested Property

```xml
<TextBlock Text="{Binding Person.Address.Street}" />
<TextBlock Text="{Binding User.Profile.Email}" />
```

```csharp
[ObservableProperty]
private Person _person = new();

public class Person
{
    public Address Address { get; set; } = new();
}

public class Address
{
    public string Street { get; set; } = "";
}
```

### Collection Indexer

```xml
<TextBlock Text="{Binding Items[0]}" />
<TextBlock Text="{Binding Users[5].Name}" />
```

```csharp
public ObservableCollection<string> Items { get; } = new();
public ObservableCollection<User> Users { get; } = new();
```

### Attached Property

```xml
<TextBlock Text="{Binding (Grid.Row)}" />
<TextBlock Text="{Binding (DockPanel.Dock)}" />
```

### Current Item

```xml
<!-- Bind to current item in collection -->
<TextBlock Text="{Binding /}" />
<TextBlock Text="{Binding /Name}" />  <!-- Property of current item -->
```

## Binding Sources

### DataContext (Default)

```xml
<!-- Binds to DataContext -->
<TextBlock Text="{Binding PropertyName}" />
```

### Element Binding

```xml
<!-- Bind to another element by name -->
<Slider x:Name="VolumeSlider" Minimum="0" Maximum="100" />
<TextBlock Text="{Binding #VolumeSlider.Value}" />

<!-- Alternative syntax -->
<TextBlock Text="{Binding ElementName=VolumeSlider, Path=Value}" />
```

### Relative Source - Parent

```xml
<!-- Find ancestor by type -->
<TextBlock Text="{Binding $parent[Window].Title}" />
<TextBlock Text="{Binding $parent[UserControl].DataContext.PropertyName}" />
<TextBlock Text="{Binding $parent[ListBox].SelectedItem}" />

<!-- Multiple levels -->
<TextBlock Text="{Binding $parent[Grid].$parent[Window].Title}" />
```

### Relative Source - Self

```xml
<!-- Bind to own property -->
<TextBlock Text="{Binding $self.Tag}" 
           Tag="Hello" />
<Button Content="{Binding $self.Width}" 
        Width="100" />
```

### Static Resource

```xml
<!-- Bind to resource -->
<TextBlock Text="{StaticResource WelcomeMessage}" />
<Button Background="{DynamicResource ThemeBrush}" />
```

### Static Property

```xml
<!-- Bind to static property -->
<TextBlock Text="{x:Static local:Constants.AppName}" />
<PathIcon Data="{x:Static icons:Icons.Home}" />
```

## Value Converters

### Built-in Converters

#### Boolean Converters

```xml
<!-- Not -->
<TextBlock IsVisible="{Binding IsHidden, Converter={x:Static BoolConverters.Not}}" />

<!-- And -->
<Button IsEnabled="{Binding IsValid, Converter={x:Static BoolConverters.And}, ConverterParameter={Binding IsReady}}" />

<!-- Or -->
<Control IsVisible="{Binding ShowA, Converter={x:Static BoolConverters.Or}, ConverterParameter={Binding ShowB}}" />
```

#### Object Converters

```xml
<!-- IsNull -->
<TextBlock IsVisible="{Binding Data, Converter={x:Static ObjectConverters.IsNull}}" />

<!-- IsNotNull -->
<TextBlock IsVisible="{Binding Data, Converter={x:Static ObjectConverters.IsNotNull}}" />

<!-- Equal -->
<RadioButton IsChecked="{Binding SelectedOption, Converter={x:Static ObjectConverters.Equal}, ConverterParameter=Option1}" />
```

### Custom Converter

**Define Converter:**

```csharp
public class BoolToColorConverter : IValueConverter
{
    public object? Convert(object? value, Type targetType, object? parameter, CultureInfo culture)
    {
        if (value is bool boolValue)
        {
            return boolValue ? Brushes.Green : Brushes.Red;
        }
        return Brushes.Gray;
    }

    public object? ConvertBack(object? va, Type targetType, object? parameter, CultureInfo culture)
    {
        throw new NotImplementedException();
    }
}
```

**Register in Resources:**

```xml
<UserControl.Resources>
    <local:BoolToColorConverter x:Key="BoolToColorConverter" />
</UserControl.Resources>
```

**Use Converter:**

```xml
<TextBlock Foreground="{Binding IsActive, Converter={StaticResource BoolToColorConverter}}" />
```

### Converter with Parameter

```xml
<TextBlock Text="{Binding Value, 
                          Converter={StaticResource NumberToStringConverter}, 
                          ConverterParamet
```

```csharp
public object? Convert(object? value, Type targetType, object? parameter, CultureInfo culture)
{
    if (value is double number && parameter is string decimals)
    {
        return number.ToString($"F{decimals}");
    }
    return value?.ToString();
}
```

## String Formatting

### Basic Formatting

```xml
<!-- Number formatting -->
<TextBlock Text="{Binding Price, StringFormat='${0:F2}'}" />
<!-- Output: $19.99 -->

<TextBlock Text="{Binding Count, StringFormat='{}{0} items'}" />
<!-- Output: 5 items (note: {} escapes the opening brace) -->

<!-- Date formatting -->
<TextBlock Text="{Binding Date, StringForma{0:yyyy-MM-dd}'}" />
<!-- Output: Date: 2024-01-23 -->

<TextBlock Text="{Binding Time, StringFormat='{0:HH:mm:ss}'}" />
<!-- Output: 14:30:45 -->
```

### Format Specifiers

#### Numeric Formats

```xml
<!-- Currency -->
<TextBlock Text="{Binding Amount, StringFormat='{}{0:C}'}" />
<!-- $1,234.56 -->

<!-- Fixed-point -->
<TextBlock Text="{Binding Value, StringFormat='{}{0:F2}'}" />
<!-- 123.46 -->

<!-- Number with separators -->
<TextBlock Text="{Binding Count, StringFormat='{}{0:N0}'}" />
<!-- 1,234 -->

<!-- Percentage -->
<TextBlock Text="{Binding Ratio, StringFormat='{}{0:P1}'}" />
<!-- 45.6% -->

<!-- Hexadecimal -->
<TextBlock Text="{Binding ColorValue, StringFormat='{}{0:X6}'}" />
<!-- FF00AA -->
```

#### Date/Time Formats

```xml
<!-- Short date -->
<TextBlock Text="{Binding Date, StringFormat='{}{0:d}'}" />
<!-- 1/23/2024 -->

<!-- Long date -->
<TextBlock Text="{Binding Date, StringFormat='{}{0:D}'}" />
<!-- Tuesday, January 23, 2024 -->

<!-- Custom date -->
<TextBlock Text="{Binding Date, StringFormat='{}{0:MMM dd, yyyy}'}" />
<!-- Jan 23, 2024 -->

<!-- Time -->
<TextBlock Text="{Binding Time, StringFormat='{}{0:t}'}" />
<!-- 2:30 PM -->

<!-- Date and time -->
<TextBlock Text="{Binding DateTime, StringFormat='{}{0:g}'}" />
<!-- 1/23/2024 2:30 PM -->
```

### Escaping Braces

```xml
<!-- Need {} to escape opening brace -->
<TextBlock Text="{Binding Count, StringFormat='{}{0} items'}" />

<!-- Without escape (error) -->
<TextBlock Text="{Binding Count, StringFormat='{0} items'}" />  <!-- ❌ -->
```

## Compiled Bindings

### Why Compiled Bindings?

- **Performance**: 2-3x faster than reflection-based bindings
- **Type Safety**: Compile-time errors instead of runtime
- **IntelliSense**: Better IDE support
- **Required**: For Avalon with `AvaloniaUseCompiledBindingsByDefault`

### Enabling Compiled Bindings

**Project File:**

```xml
<PropertyGroup>
    <AvaloniaUseCompiledBindingsByDefault>true</AvaloniaUseCompiledBindingsByDefault>
</PropertyGroup>
```

**AXAML:**

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             xmlns:vm="using:YourApp.ViewModels"
             x:DataType="vm:YourViewModel">  <!-- Required! -->
    
    <TextBlock Text="{Binding PropertyName}" />  <!-- Compiled -->
</UserControl>
```

### Compiled Binding Syntax

```xml
<!-- Standard binding (compiled if x:DataType is set) -->
<TextBlock Text="{Binding Name}" />

<!-- Explicit compiled binding -->
<TextBlock Text="{CompiledBinding Name}" />

<!-- Reflection binding (opt-out) -->
<TextBlock Text="{ReflectionBinding Name}" />
```

### DataType for Collections

```xml
<ItemsControl ItemsSource="{Binding People}">
    <ItemsControl.ItemTemplate>
        <DataTemplate DataType="vm:PersonViewModel">
            <!-- Compiled bindings for PersonViewModel -->
            <TextBlock Text="{Binding Name}" />
            <TextBlock Text="{Binding Age}" />
        </DataTemplate>
    </ItemsControl.ItemTemplate>
</ItemsControl>
```

### DataType Inheritance

```xml
<UserControl x:DataType="vm:MainViewModel">
    <!-- Binds to MainViewModel -->
    <TextBlock Text="{Binding Title}" />
    
    <ContentControl Content="{Binding ChildViewModel}">
        <ContentControl.ContentTemplate>
            <DataTemplate x:DataType="vm:ChildViewModel">
                <!-- Binds to ChildViewModel -->
                <TextBlock Text="{Binding ChildProperty}" />
            </DataTemplate>
        </ContentControl.ContentTemplate>
    </ContentControl>
</UserControl>
```

## Common Patterns

### Binding to Commands```xml

<Button Content="Save" Command="{Binding SaveCommand}" />
<Button Content="Delete" Command="{Binding DeleteCommand}" 
        CommandParameter="{Binding SelectedItem}" />

```
```csharp
[RelayCommand]
private void Save()
{
    // Save logic
}

[RelayCommand]
private void Delete(object? parameter)
{
    if (parameter is Item item)
    {
        // Delete item
    }
}
```

### Binding to Collections

```xml
<!-- ItemsControl -->
<ItemsControl ItemsSource="{Binding Items}">
    <ItemsControl.ItemTemplate>
        <DataTemplate>
            <TextBlock Text="{Binding Name}" />
        </DataTemplate>
    </ItemsControl.ItemTemplate>
</ItemsControl>

<!-- ListBox with selection -->
<ListBox ItemsSource="{Binding Items}"
         SelectedItem="{Binding SelectedItem, Mode=TwoWay}" />

<!-- DataGrid -->
<DataGrid ItemsSource="{Binding People}"
          SelectedItem="{Binding SelectedPerson, Mode=TwoWay}">
    <DataGrid.Columns>
        <DataGridTextColumn Header="Name" Binding="{Binding Name}" />
        <DataGridTextColumn Header="Age" Binding="{Binding Age}" />
    </DataGrid.Columns>
</DataGrid>
```

```csharp
public ObservableCollection<Item> Items { get; } = new();

[ObservableProperty]
private Item? _selectedItem;
```

### Binding to Enums

```xml
<!-- ComboBox with enum -->
<ComboBox ItemsSource="{Binding AllStatuses}"
          SelectedItem="{Binding CurrentStatus, Mode=TwoWay}" />
```

```csharp
public enum Status { Active, Inactive, Pending }

public IEnumerable<Status> AllStatuses => Enum.GetValues<Status>();

[ObservableProperty]
private Status _currentStatus = Status.Active;
```

### Conditional Visibility

```xml
<!-- Show/hide based on boolean -->
<TextBlock Text="Loading..." 
           IsVisible="{Binding IsLoading}" />

<!-- Show when NOT loading -->
<TextBlock Text="Content" 
           IsVisible="{Binding IsLoading, Converter={x:Static BoolConverters.Not}}" />

<!-- Show when data exists -->
<TextBlock Text="No data" 
           IsVisible="{Binding Data, Converter={x:Static ObjectConverters.IsNull}}" />
```

### Multi-Binding (Alternative Approaches)

**Option 1: Computed Property**

```csharp
[ObservableProperty]
private string _firstName = "";

[ObservableProperty]
private string _lastName = "";

public string FullName => $"{FirstName} {LastName}";

partial void OnFirstNameChanged(string value) => OnPropertyChanged(nameof(FullName));
partial void OnLastNameChanged(string value) => OnPropertyChanged(nameof(FullName));
```

```xml
<TextBlock Text="{Binding FullName}" />
```

**Option 2: Converter**

```xml
<TextBlock>
    <TextBlock.Text>
        <MultiBinding Converter="{StaticResource FullNameConverter}">
            <Binding Path="FirstName" />
            <Binding Path="LastName" />
        </MultiBinding>
    </TextBlock.Text>
</TextBlock>
```

### Binding with Fallback

```xml
<!-- Show fallback if binding fails -->
<TextBlock Text="{Binding Name, FallbackValue='Unknown'}" />
<TextBlock Text="{Binding Age, FallbackValue=0}" />
<Image Source="{Binding ImagePath, FallbackValue='/Assets/placeholder.png'}" />
```

### Binding with TargetNullValue

```xml
<!-- Show specific value when source is null -->
<TextBlock Text="{Binding Description, TargetNullValue='No description'}" />
<TextBlock Text="{Binding Count, TargetNullValue=0}" />
```

## Best Practices

1. **Always set x:DataType** for compiled bindings
2. **Use TwoWay explicitly** for input controls
3. **Use OneTimetic data to improve performance
4. **Prefer computed properties** over complex converters
5. **Use StringFormat** for simple formatting
6. **Use converters** for complex transformations
7. **Bind to commands** instead of event handlers
8. **Use ObservableCollection** for dynamic lists
9. **Implement INotifyPropertyChanged** (via CommunityToolkit.Mvvm)
10. **Test bindings** with design-time data

## Common Mistakes

❌ **DatePicker Binding Type Mismatch**

```csharp
[ObservableProperty]
private DateTime _selectedDate = DateTime.Now; // ❌ InvalidCastException
```

✅ **Correct**

```csharp
[ObservableProperty]
private DateTimeOffset? _selectedDate = DateTimeOffset.Now; // ✅ Use DateTimeOffset?
```

❌ **Missing Mode for input**

```xml
<TextBox Text="{Binding Name}" />  <!-- OneWay by default -->
```

✅ **Correct**

```xml
<TextBox Text="{Binding Name, Mode=TwoWay}" />
```

❌ **Forgetting x:DataType**

```xml
<UserControl x:Class="MyView">
    <TextBlock Text="{Binding Name}" />  <!-- Reflection binding -->
</UserControl>
```

✅ **Correct**

```xml
<UserControl x:Class="MyView" x:DataType="vm:MyViewModel">
    <TextBlock Text="{Binding Name}" />  <!-- Compiled binding -->
</UserControl>
```

❌ **Not notifying property changes**

```csharp
private string _name;
public string Name
{
    get => _name;
    set => _name = value;  // UI won't update!
}
```

✅ **Correct**

```csharp
[ObservableProperty]
private string _name = "";  // Generates proper notification
```