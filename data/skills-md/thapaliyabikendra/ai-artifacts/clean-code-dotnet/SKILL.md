---
name: clean-code-dotnet
description: "Clean Code principles adapted for C#/.NET including naming, variables, functions, SOLID, error handling, and async patterns. Use when: (1) reviewing C# code, (2) refactoring for clarity, (3) writing new code, (4) code review feedback."
layer: 1
tech_stack: [dotnet, csharp]
topics: [clean-code, naming, solid, refactoring, code-quality, best-practices]
depends_on: []
complements: [code-review-excellence, csharp-advanced-patterns, error-handling-patterns]
keywords: [CleanCode, SOLID, SRP, DRY, naming, refactor, code-smell, readability]
---

# Clean Code .NET

Clean Code principles from Robert C. Martin, adapted for C#/.NET. Use as checklist during code reviews and refactoring.

## Naming

### Use Meaningful Names

```csharp
// ❌ Bad
int d;
var dataFromDb = db.GetFromService().ToList();

// ✅ Good
int daySinceModification;
var employees = _employeeService.GetEmployees().ToList();
```

### Avoid Hungarian Notation

```csharp
// ❌ Bad
int iCounter;
string strFullName;
public bool IsShopOpen(string pDay, int pAmount) { }

// ✅ Good
int counter;
string fullName;
public bool IsShopOpen(string day, int amount) { }
```

### Use Pronounceable Names

```csharp
// ❌ Bad
public class Employee
{
    public DateTime sWorkDate { get; set; }
    public DateTime modTime { get; set; }
}

// ✅ Good
public class Employee
{
    public DateTime StartWorkingDate { get; set; }
    public DateTime ModificationTime { get; set; }
}
```

### Use Domain Names

```csharp
// ✅ Good - Use patterns developers know
var singletonObject = SingleObject.GetInstance();
var factory = new PatientFactory();
var repository = new PatientRepository();
```

---

## Variables

### Return Early, Avoid Deep Nesting

```csharp
// ❌ Bad - Deep nesting
public bool IsShopOpen(string day)
{
    if (!string.IsNullOrEmpty(day))
    {
        day = day.ToLower();
        if (day == "friday")
        {
            return true;
        }
        else if (day == "saturday")
        {
            return true;
        }
        // ... more nesting
    }
    return false;
}

// ✅ Good - Guard clauses + early return
public bool IsShopOpen(string day)
{
    if (string.IsNullOrEmpty(day))
        return false;

    var openingDays = new[] { "friday", "saturday", "sunday" };
    return openingDays.Contains(day.ToLower());
}
```

### Avoid Magic Strings

```csharp
// ❌ Bad
if (userRole == "Admin") { }

// ✅ Good
const string AdminRole = "Admin";
if (userRole == AdminRole) { }

// ✅ Better - Use enum
public enum UserRole { Admin, User, Guest }
if (userRole == UserRole.Admin) { }
```

### Don't Add Unneeded Context

```csharp
// ❌ Bad - Redundant prefix
public class Car
{
    public string CarMake { get; set; }
    public string CarModel { get; set; }
    public string CarColor { get; set; }
}

// ✅ Good
public class Car
{
    public string Make { get; set; }
    public string Model { get; set; }
    public string Color { get; set; }
}
```

### Use Default Arguments

```csharp
// ❌ Bad
public void CreateMicrobrewery(string name = null)
{
    var breweryName = !string.IsNullOrEmpty(name) ? name : "Hipster Brew Co.";
}

// ✅ Good
public void CreateMicrobrewery(string breweryName = "Hipster Brew Co.")
{
    // breweryName is always valid
}
```

---

## Functions

### Functions Should Do One Thing

```csharp
// ❌ Bad - Multiple responsibilities
public void SendEmailToListOfClients(string[] clients)
{
    foreach (var client in clients)
    {
        var clientRecord = db.Find(client);
        if (clientRecord.IsActive())
        {
            Email(client);
        }
    }
}

// ✅ Good - Single responsibility
public void SendEmailToActiveClients(string[] clients)
{
    var activeClients = GetActiveClients(clients);
    activeClients.ForEach(client => Email(client));
}

public List<Client> GetActiveClients(string[] clients)
{
    return db.Find(clients).Where(c => c.IsActive).ToList();
}
```

### Avoid Side Effects

```csharp
// ❌ Bad - Modifies global state
var name = "Ryan McDermott";

public void SplitAndEnrichFullName()
{
    var temp = name.Split(" ");
    name = $"First: {temp[0]}, Last: {temp[1]}"; // Side effect!
}

// ✅ Good - Pure function
public string SplitAndEnrichFullName(string name)
{
    var temp = name.Split(" ");
    return $"First: {temp[0]}, Last: {temp[1]}";
}
```

### Avoid Negative Conditionals

```csharp
// ❌ Bad
public bool IsDOMNodeNotPresent(string node) { }
if (!IsDOMNodeNotPresent(node)) { }  // Double negative!

// ✅ Good
public bool IsDOMNodePresent(string node) { }
if (IsDOMNodePresent(node)) { }
```

### Avoid Flag Parameters

```csharp
// ❌ Bad - Flag indicates multiple responsibilities
public void CreateFile(string name, bool temp = false)
{
    if (temp)
        Touch("./temp/" + name);
    else
        Touch(name);
}

// ✅ Good - Separate methods
public void CreateFile(string name) => Touch(name);
public void CreateTempFile(string name) => Touch("./temp/" + name);
```

### Limit Function Arguments (2 or fewer)

```csharp
// ❌ Bad
public void CreateMenu(string title, string body, string buttonText, bool cancellable) { }

// ✅ Good - Use object
public class MenuConfig
{
    public string Title { get; set; }
    public string Body { get; set; }
    public string ButtonText { get; set; }
    public bool Cancellable { get; set; }
}

public void CreateMenu(MenuConfig config) { }
```

### Encapsulate Conditionals

```csharp
// ❌ Bad
if (article.state == "published") { }

// ✅ Good
if (article.IsPublished()) { }
```

### Remove Dead Code

```csharp
// ❌ Bad
public void OldRequestModule(string url) { }  // Unused!
public void NewRequestModule(string url) { }

var request = NewRequestModule(requestUrl);

// ✅ Good - Delete unused code
public void RequestModule(string url) { }

var request = RequestModule(requestUrl);
```

---

## SOLID Principles

### Single Responsibility (SRP)

```csharp
// ❌ Bad - Two responsibilities
class UserSettings
{
    public void ChangeSettings(Settings settings)
    {
        if (VerifyCredentials()) { /* ... */ }
    }

    private bool VerifyCredentials() { /* ... */ }  // Auth responsibility
}

// ✅ Good - Separated
class UserAuth
{
    public bool VerifyCredentials() { /* ... */ }
}

class UserSettings
{
    private readonly UserAuth _auth;

    public void ChangeSettings(Settings settings)
    {
        if (_auth.VerifyCredentials()) { /* ... */ }
    }
}
```

### Open/Closed (OCP)

```csharp
// ❌ Bad - Must modify to extend
class HttpRequester
{
    public bool Fetch(string url)
    {
        if (adapterName == "ajaxAdapter")
            return MakeAjaxCall(url);
        else if (adapterName == "httpNodeAdapter")
            return MakeHttpCall(url);
        // Must add more else-if for new adapters!
    }
}

// ✅ Good - Open for extension, closed for modification
interface IAdapter
{
    bool Request(string url);
}

class AjaxAdapter : IAdapter
{
    public bool Request(string url) { /* ... */ }
}

class HttpRequester
{
    private readonly IAdapter _adapter;
    public bool Fetch(string url) => _adapter.Request(url);
}
```

### Liskov Substitution (LSP)

```csharp
// ❌ Bad - Square breaks Rectangle behavior
class Square : Rectangle
{
    public override void SetWidth(double width) { Width = Height = width; }
}

// ✅ Good - Use abstraction
abstract class Shape
{
    public abstract double GetArea();
}

class Rectangle : Shape { /* ... */ }
class Square : Shape { /* ... */ }
```

### Interface Segregation (ISP)

```csharp
// ❌ Bad - Robot can't eat but must implement
interface IEmployee { void Work(); void Eat(); }

class Robot : IEmployee
{
    public void Work() { /* ... */ }
    public void Eat() { /* Robot can't eat! */ }
}

// ✅ Good - Segregated interfaces
interface IWorkable { void Work(); }
interface IFeedable { void Eat(); }

class Human : IWorkable, IFeedable { /* ... */ }
class Robot : IWorkable { /* ... */ }
```

### Dependency Inversion (DIP)

```csharp
// ❌ Bad - Depends on concrete types
class Manager
{
    private readonly Robot _robot;
    private readonly Human _human;
}

// ✅ Good - Depends on abstractions
class Manager
{
    private readonly IEnumerable<IEmployee> _employees;

    public Manager(IEnumerable<IEmployee> employees)
    {
        _employees = employees;
    }
}
```

### Constructor Dependency Smell (SRP Indicator)

Too many constructor dependencies indicate SRP violation:

```csharp
// ❌ Code Smell: 15 dependencies = too many responsibilities!
public class LicensePlateAppService : ApplicationService
{
    public LicensePlateAppService(
        IRepository<LicensePlate, Guid> licensePlateRepository,
        IRepository<LicensePlateWithoutTag, Guid> licensePlateWithoutTagRepository,
        IRepository<ASN, Guid> asnRepository,
        IRepository<Project, Guid> projectRepository,
        IRepository<Tag, Guid> tagRepository,
        IRepository<SKU, Guid> skuRepository,
        IRepository<Customer, Guid> customerRepository,
        IRepository<LicensePlateHold, Guid> licensePlateHoldRepository,
        IRepository<LicensePlateLocation, Guid> licensePlateLocationRepository,
        IRepository<Location, Guid> locationRepository,
        IWarehouseAppService warehouseAppService,
        IWarehouseOwnerAppService warehouseOwnerAppService,
        IBlobContainer<BulkUpdateLPExcelFileContainer> fileContainer,
        LicensePlateService.LicensePlateServiceClient licensePlateServiceClient,
        CommonDependencies<LicensePlateAppService> commonDependencies)
    { }
}

// ✅ Good: Split by responsibility
public class LicensePlateAppService { }      // CRUD only (~5 deps)
public class LicensePlateBulkService { }     // Bulk imports (~4 deps)
public class LicensePlateEventPublisher { }  // Events (~3 deps)
```

**Dependency Count Guidelines:**

| Dependencies | Status | Action |
|--------------|--------|--------|
| 1-5 | ✅ Normal | Acceptable |
| 6-8 | ⚠️ Warning | Review for splitting opportunities |
| 9+ | ❌ Smell | Refactor required - class has too many responsibilities |

**Refactoring Strategies:**
1. **Extract Service** - Move related operations to a dedicated service
2. **Facade Pattern** - Group related dependencies behind a facade
3. **Domain Events** - Decouple via publish/subscribe instead of direct calls
4. **Mediator Pattern** - Use MediatR to reduce direct dependencies

---

## Error Handling

### Don't Use `throw ex`

```csharp
// ❌ Bad - Loses stack trace
catch (Exception ex)
{
    logger.LogError(ex);
    throw ex;  // Stack trace lost!
}

// ✅ Good - Preserves stack trace
catch (Exception ex)
{
    logger.LogError(ex);
    throw;  // Rethrows with original stack
}

// ✅ Also Good - Wrap with inner exception
catch (Exception ex)
{
    throw new BusinessException("Operation failed", ex);
}
```

### Don't Ignore Caught Errors

```csharp
// ❌ Bad - Silent swallow
catch (Exception ex) { }  // Never do this!

// ✅ Good - Handle or propagate
catch (Exception ex)
{
    _logger.LogError(ex, "Operation failed");
    throw;  // Or handle appropriately
}
```

### Use Multiple Catch Blocks

```csharp
// ❌ Bad - Type checking in catch
catch (Exception ex)
{
    if (ex is TaskCanceledException) { /* ... */ }
    else if (ex is TaskSchedulerException) { /* ... */ }
}

// ✅ Good - Separate catch blocks
catch (TaskCanceledException ex)
{
    // Handle cancellation
}
catch (TaskSchedulerException ex)
{
    // Handle scheduler error
}
```

---

## Comments

### Avoid Positional Markers and Regions

```csharp
// ❌ Bad
#region Scope Model Instantiation
var model = new Model();
#endregion

#region Action setup
void Actions() { }
#endregion

// ✅ Good - Let code speak
var model = new Model();

void Actions() { }
```

### Don't Leave Commented Code

```csharp
// ❌ Bad
DoStuff();
// DoOtherStuff();
// DoSomeMoreStuff();

// ✅ Good - Use version control
DoStuff();
```

### Only Comment Business Logic Complexity

```csharp
// ❌ Bad - Obvious comments
var hash = 0;  // The hash
var length = data.Length;  // Length of string

// ✅ Good - Explains WHY, not WHAT
// Using djb2 hash for good speed/collision tradeoff
hash = ((hash << 5) - hash) + character;
```

---

## Quick Reference Checklist

### Code Review Checklist

- [ ] **Naming**: Meaningful, pronounceable, no Hungarian
- [ ] **Functions**: Single responsibility, <3 args, no flags
- [ ] **Variables**: No magic strings, early returns, no nesting >2
- [ ] **SOLID**: Interfaces over concrete, small focused classes
- [ ] **Dependencies**: Constructor has <8 dependencies (SRP indicator)
- [ ] **Error Handling**: No `throw ex`, no silent catch, specific exception types
- [ ] **Comments**: No regions, no dead code, explains WHY

---

## References

- **references/solid-principles.md**: Full SOLID examples
- **references/async-patterns.md**: Async/await guidelines
- **references/editorconfig-template.md**: .editorconfig template

**Source**: [clean-code-dotnet](https://github.com/thangchung/clean-code-dotnet)
