---
name: testing
description: Testing strategies for the 3SC widget host. Covers unit tests, integration tests, ViewModel testing, mocking patterns, and test organization.
---

# Testing

## Overview

A comprehensive testing strategy ensures code quality, prevents regressions, and enables confident refactoring. This skill covers testing patterns for WPF desktop applications.

## Definition of Done (DoD)

- [ ] New features have unit tests for business logic
- [ ] ViewModels have tests for command behavior
- [ ] Repository operations have integration tests
- [ ] Critical paths have edge case coverage
- [ ] Tests are independent and repeatable
- [ ] Test names clearly describe the scenario

## Test Project Structure

```
3SC.Domain.Tests/
├── Entities/
│   ├── WidgetTests.cs
│   └── LayoutTests.cs
└── ValueObjects/
    ├── WidgetSizeTests.cs
    └── SemanticVersionTests.cs

3SC.Infrastructure.Tests/
├── Repositories/
│   ├── WidgetRepositoryTests.cs
│   └── LayoutRepositoryTests.cs
├── Security/
│   └── SecureStorageServiceTests.cs
└── DbTestFactory.cs  # Shared test database setup

3SC.UI.Tests/
├── ViewModels/
│   ├── ShellViewModelTests.cs
│   └── WidgetLibraryViewModelTests.cs
├── Services/
│   └── NavigationServiceTests.cs
└── Converters/
    └── BoolToVisibilityConverterTests.cs
```

## Naming Conventions

Use the pattern: `MethodName_Scenario_ExpectedResult`

```csharp
public class WidgetTests
{
    [Fact]
    public void Constructor_WithValidParameters_CreatesWidget() { }
    
    [Fact]
    public void Constructor_WithEmptyKey_ThrowsArgumentException() { }
    
    [Fact]
    public void UpdatePosition_WithNewPosition_RaisesPropertyChanged() { }
    
    [Theory]
    [InlineData("")]
    [InlineData("   ")]
    [InlineData(null)]
    public void Validate_WithInvalidName_ReturnsFalse(string? name) { }
}
```

## Domain Layer Testing

Domain entities should be pure and testable without mocks:

```csharp
public class WidgetSizeTests
{
    [Fact]
    public void Constructor_WithValidDimensions_CreateSize()
    {
        // Arrange & Act
        var size = new WidgetSize(300, 200);
        
        // Assert
        Assert.Equal(300, size.Width);
        Assert.Equal(200, size.Height);
    }
    
    [Theory]
    [InlineData(0, 100)]
    [InlineData(100, 0)]
    [InlineData(-1, 100)]
    public void Constructor_WithInvalidDimensions_ThrowsArgumentException(int width, int height)
    {
        // Act & Assert
        Assert.Throws<ArgumentException>(() => new WidgetSize(width, height));
    }
    
    [Fact]
    public void Equals_WithSameDimensions_ReturnsTrue()
    {
        // Arrange
        var size1 = new WidgetSize(300, 200);
        var size2 = new WidgetSize(300, 200);
        
        // Assert
        Assert.Equal(size1, size2);
        Assert.True(size1 == size2);
    }
}
```

## ViewModel Testing

### Setup with Mocks

```csharp
public class WidgetLibraryViewModelTests : IDisposable
{
    private readonly Mock<IWidgetRepository> _widgetRepoMock;
    private readonly Mock<IWidgetPackageInstaller> _installerMock;
    private readonly Mock<IUserNotificationService> _notificationMock;
    private readonly WidgetLibraryViewModel _viewModel;
    
    public WidgetLibraryViewModelTests()
    {
        _widgetRepoMock = new Mock<IWidgetRepository>();
        _installerMock = new Mock<IWidgetPackageInstaller>();
        _notificationMock = new Mock<IUserNotificationService>();
        
        _viewModel = new WidgetLibraryViewModel(
            _widgetRepoMock.Object,
            _installerMock.Object,
            _notificationMock.Object);
    }
    
    public void Dispose()
    {
        // Cleanup if needed
    }
}
```

### Testing Commands

```csharp
[Fact]
public async Task LoadWidgetsCommand_OnSuccess_PopulatesWidgets()
{
    // Arrange
    var widgets = new List<Widget>
    {
        new Widget("clock", "Clock", "1.0.0"),
        new Widget("weather", "Weather", "2.0.0")
    };
    _widgetRepoMock
        .Setup(r => r.GetAllAsync(It.IsAny<CancellationToken>()))
        .ReturnsAsync(widgets);
    
    // Act
    await _viewModel.LoadWidgetsCommand.ExecuteAsync(null);
    
    // Assert
    Assert.Equal(2, _viewModel.Widgets.Count);
    Assert.False(_viewModel.IsLoading);
    Assert.Null(_viewModel.ErrorMessage);
}

[Fact]
public async Task LoadWidgetsCommand_OnError_SetsErrorMessage()
{
    // Arrange
    _widgetRepoMock
        .Setup(r => r.GetAllAsync(It.IsAny<CancellationToken>()))
        .ThrowsAsync(new InvalidOperationException("Database error"));
    
    // Act
    await _viewModel.LoadWidgetsCommand.ExecuteAsync(null);
    
    // Assert
    Assert.Empty(_viewModel.Widgets);
    Assert.False(_viewModel.IsLoading);
    Assert.NotNull(_viewModel.ErrorMessage);
}

[Fact]
public async Task LoadWidgetsCommand_WhenCancelled_DoesNotSetError()
{
    // Arrange
    var cts = new CancellationTokenSource();
    cts.Cancel();
    
    _widgetRepoMock
        .Setup(r => r.GetAllAsync(It.IsAny<CancellationToken>()))
        .ThrowsAsync(new OperationCanceledException());
    
    // Act
    await _viewModel.LoadWidgetsCommand.ExecuteAsync(cts.Token);
    
    // Assert
    Assert.Null(_viewModel.ErrorMessage);
}
```

### Testing Property Changes

```csharp
[Fact]
public void SelectedWidget_WhenChanged_NotifiesPropertyChanged()
{
    // Arrange
    var widget = new WidgetViewModel(new Widget("test", "Test", "1.0.0"));
    var changedProperties = new List<string>();
    _viewModel.PropertyChanged += (_, e) => changedProperties.Add(e.PropertyName!);
    
    // Act
    _viewModel.SelectedWidget = widget;
    
    // Assert
    Assert.Contains(nameof(WidgetLibraryViewModel.SelectedWidget), changedProperties);
    Assert.Contains(nameof(WidgetLibraryViewModel.HasSelection), changedProperties);
}
```

## Integration Testing

### In-Memory Database

```csharp
public class DbTestFactory
{
    public static AppDbContext CreateInMemoryContext()
    {
        var options = new DbContextOptionsBuilder<AppDbContext>()
            .UseSqlite("DataSource=:memory:")
            .Options;
        
        var context = new AppDbContext(options);
        context.Database.OpenConnection();
        context.Database.EnsureCreated();
        
        return context;
    }
    
    public static AppDbContext CreateTestContext(string testName)
    {
        var dbPath = Path.Combine(
            Path.GetTempPath(), 
            $"3sc_test_{testName}_{Guid.NewGuid():N}.db");
        
        var options = new DbContextOptionsBuilder<AppDbContext>()
            .UseSqlite($"Data Source={dbPath}")
            .Options;
        
        var context = new AppDbContext(options);
        context.Database.EnsureCreated();
        
        return context;
    }
}
```

### Repository Integration Tests

```csharp
public class WidgetRepositoryTests : IDisposable
{
    private readonly AppDbContext _context;
    private readonly WidgetRepository _repository;
    
    public WidgetRepositoryTests()
    {
        _context = DbTestFactory.CreateInMemoryContext();
        _repository = new WidgetRepository(_context);
    }
    
    public void Dispose()
    {
        _context.Database.CloseConnection();
        _context.Dispose();
    }
    
    [Fact]
    public async Task AddAsync_WithValidWidget_PersistsToDatabase()
    {
        // Arrange
        var widget = new Widget("test-widget", "Test Widget", "1.0.0");
        
        // Act
        await _repository.AddAsync(widget);
        await _context.SaveChangesAsync();
        
        // Assert
        var saved = await _context.Widgets.FirstOrDefaultAsync(w => w.WidgetKey == "test-widget");
        Assert.NotNull(saved);
        Assert.Equal("Test Widget", saved.DisplayName);
    }
    
    [Fact]
    public async Task GetAllAsync_WithMultipleWidgets_ReturnsAll()
    {
        // Arrange
        _context.Widgets.AddRange(
            new Widget("widget1", "Widget 1", "1.0.0"),
            new Widget("widget2", "Widget 2", "1.0.0"));
        await _context.SaveChangesAsync();
        
        // Act
        var widgets = await _repository.GetAllAsync();
        
        // Assert
        Assert.Equal(2, widgets.Count);
    }
}
```

## Mocking Guidelines

### What to Mock

| Mock | Why |
|------|-----|
| Repositories | Avoid database in unit tests |
| External APIs | Avoid network calls |
| File system | Avoid file dependencies |
| Time providers | Control time in tests |
| User dialogs | Avoid UI interactions |

### What NOT to Mock

| Don't Mock | Why |
|------------|-----|
| Domain entities | Pure, no dependencies |
| Value objects | Pure, no dependencies |
| Simple utilities | More complex than needed |
| The thing being tested | Defeats the purpose |

### Mock Verification

```csharp
[Fact]
public async Task InstallCommand_OnSuccess_ShowsNotification()
{
    // Arrange
    var package = CreateTestPackage();
    _installerMock
        .Setup(i => i.InstallAsync(package, It.IsAny<CancellationToken>()))
        .ReturnsAsync(InstallResult.Success);
    
    // Act
    _viewModel.SelectedPackage = package;
    await _viewModel.InstallCommand.ExecuteAsync(null);
    
    // Assert
    _notificationMock.Verify(
        n => n.ShowSuccess(It.Is<string>(s => s.Contains("installed"))),
        Times.Once);
}
```

## Test Data Builders

For complex object creation:

```csharp
public class WidgetBuilder
{
    private string _key = "test-widget";
    private string _displayName = "Test Widget";
    private string _version = "1.0.0";
    private bool _hasSettings = false;
    
    public WidgetBuilder WithKey(string key)
    {
        _key = key;
        return this;
    }
    
    public WidgetBuilder WithDisplayName(string name)
    {
        _displayName = name;
        return this;
    }
    
    public WidgetBuilder WithSettings()
    {
        _hasSettings = true;
        return this;
    }
    
    public Widget Build() => new(_key, _displayName, _version) { HasSettings = _hasSettings };
}

// Usage
var widget = new WidgetBuilder()
    .WithKey("clock")
    .WithDisplayName("Clock Widget")
    .WithSettings()
    .Build();
```

## Async Testing

```csharp
[Fact]
public async Task LongRunningOperation_WithCancellation_ThrowsOperationCancelledException()
{
    // Arrange
    using var cts = new CancellationTokenSource();
    cts.CancelAfter(TimeSpan.FromMilliseconds(100));
    
    // Act & Assert
    await Assert.ThrowsAsync<OperationCanceledException>(
        () => _service.LongRunningOperationAsync(cts.Token));
}

[Fact]
public async Task AsyncOperation_WithTimeout_CompletesInTime()
{
    // Arrange
    var timeout = TimeSpan.FromSeconds(5);
    
    // Act
    var task = _service.OperationAsync();
    var completedInTime = await Task.WhenAny(task, Task.Delay(timeout)) == task;
    
    // Assert
    Assert.True(completedInTime, $"Operation did not complete within {timeout}");
}
```

## Test Organization

### Arrange-Act-Assert

```csharp
[Fact]
public void MethodName_Scenario_ExpectedResult()
{
    // Arrange - Set up test data and dependencies
    var input = CreateTestInput();
    
    // Act - Execute the method under test
    var result = _sut.MethodUnderTest(input);
    
    // Assert - Verify the outcome
    Assert.Equal(expected, result);
}
```

### Theory for Parameterized Tests

```csharp
[Theory]
[InlineData("1.0.0", "1.0.0", 0)]   // Equal
[InlineData("1.0.0", "1.0.1", -1)]  // Less than
[InlineData("2.0.0", "1.9.9", 1)]   // Greater than
public void CompareTo_VersionComparison_ReturnsExpected(
    string version1, 
    string version2, 
    int expected)
{
    var v1 = SemanticVersion.Parse(version1);
    var v2 = SemanticVersion.Parse(version2);
    
    var result = Math.Sign(v1.CompareTo(v2));
    
    Assert.Equal(expected, result);
}
```

## Coverage Goals

| Layer | Target | Focus |
|-------|--------|-------|
| Domain | 90%+ | Business rules, validation |
| ViewModels | 80%+ | Commands, state changes |
| Infrastructure | 70%+ | Happy paths, edge cases |
| UI/Converters | 60%+ | Edge cases, null handling |

## References

- [xUnit Documentation](https://xunit.net/)
- [Moq Quickstart](https://github.com/moq/moq4/wiki/Quickstart)
- [Testing Best Practices](https://docs.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices)
