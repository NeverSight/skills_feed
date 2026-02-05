---
name: refactoring
description: Use when restructuring code without changing behavior - extract method, extract class, rename, move, inline, introduce parameter object. Triggers on keywords like "extract", "rename", "move method", "inline", "restructure", "decompose".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, TodoWrite
infer: true
---

# Code Refactoring

Expert code restructuring agent for EasyPlatform. Focuses on structural changes that improve code quality without modifying behavior.

## Refactoring Catalog

### Extract Patterns

| Pattern                | When to Use                         | Platform Example                          |
| ---------------------- | ----------------------------------- | ----------------------------------------- |
| **Extract Method**     | Long method, duplicated code        | Move logic to private method              |
| **Extract Class**      | Class has multiple responsibilities | Create Helper, Service, or Strategy class |
| **Extract Interface**  | Need abstraction for testing/DI     | Create `I{ClassName}` interface           |
| **Extract Expression** | Complex inline expression           | Move to Entity static expression          |
| **Extract Validator**  | Repeated validation logic           | Create validator extension method         |

### Move Patterns

| Pattern               | When to Use                       | Platform Example                         |
| --------------------- | --------------------------------- | ---------------------------------------- |
| **Move Method**       | Method belongs to different class | Move from Handler to Helper/Entity       |
| **Move to Extension** | Reusable repository logic         | Create `{Entity}RepositoryExtensions`    |
| **Move to DTO**       | Mapping logic in handler          | Use `PlatformEntityDto.MapToEntity()`    |
| **Move to Entity**    | Business logic in handler         | Add instance method or static expression |

### Simplify Patterns

| Pattern                     | When to Use                  | Platform Example                   |
| --------------------------- | ---------------------------- | ---------------------------------- |
| **Inline Variable**         | Temporary variable used once | Remove intermediate variable       |
| **Inline Method**           | Method body is obvious       | Replace call with body             |
| **Replace Conditional**     | Complex if/switch            | Use Strategy pattern or expression |
| **Introduce Parameter Obj** | Method has many parameters   | Create Command/Query DTO           |

## Workflow

### Phase 1: Analysis

1. **Identify Target**: Locate code to refactor
2. **Map Dependencies**: Find all usages with Grep
3. **Assess Impact**: List affected files and tests
4. **Verify Tests**: Ensure test coverage exists

### Phase 2: Plan

Document refactoring plan:

```markdown
## Refactoring Plan

**Target**: [file:line_number]
**Type**: [Extract Method | Move to Extension | etc.]
**Reason**: [Why this refactoring improves code]

### Changes

1. [ ] Create/modify [file]
2. [ ] Update usages in [files]
3. [ ] Run tests

### Risks

- [Potential issues]
```

### Phase 3: Execute

```csharp
// BEFORE: Logic in handler
protected override async Task<Result> HandleAsync(Command req, CancellationToken ct)
{
    var isValid = entity.Status == Status.Active &&
                  entity.User?.IsActive == true &&
                  !entity.IsDeleted;
    if (!isValid) throw new Exception();
}

// AFTER: Extracted to entity static expression
// In Entity.cs
public static Expression<Func<Entity, bool>> IsActiveExpr()
    => e => e.Status == Status.Active &&
            e.User != null && e.User.IsActive &&
            !e.IsDeleted;

// In Handler
var entity = await repository.FirstOrDefaultAsync(Entity.IsActiveExpr(), ct)
    .EnsureFound("Entity not active");
```

### Phase 4: Verify

1. Run affected tests
2. Verify no behavior change
3. Check code compiles
4. Review for consistency

## Platform-Specific Refactorings

### Handler to Helper

```csharp
// BEFORE: Reused logic in multiple handlers
var employee = await repo.FirstOrDefaultAsync(Employee.UniqueExpr(userId, companyId), ct)
    ?? await CreateEmployeeAsync(userId, companyId, ct);

// AFTER: Extracted to Helper
// In EmployeeHelper.cs
public async Task<Employee> GetOrCreateEmployeeAsync(string userId, string companyId, CancellationToken ct)
{
    return await repo.FirstOrDefaultAsync(Employee.UniqueExpr(userId, companyId), ct)
        ?? await CreateEmployeeAsync(userId, companyId, ct);
}
```

### Handler to Repository Extension

```csharp
// BEFORE: Query logic in handler
var employees = await repo.GetAllAsync(
    e => e.CompanyId == companyId && e.Status == Status.Active && e.DepartmentIds.Contains(deptId), ct);

// AFTER: Extracted to extension
// In EmployeeRepositoryExtensions.cs
public static async Task<List<Employee>> GetActiveByDepartmentAsync(
    this IPlatformQueryableRootRepository<Employee> repo, string companyId, string deptId, CancellationToken ct)
{
    return await repo.GetAllAsync(
        Employee.OfCompanyExpr(companyId)
            .AndAlso(Employee.IsActiveExpr())
            .AndAlso(e => e.DepartmentIds.Contains(deptId)), ct);
}
```

### Mapping to DTO

```csharp
// BEFORE: Mapping in handler
var config = new AuthConfig
{
    ClientId = req.Dto.ClientId,
    Secret = encryptService.Encrypt(req.Dto.Secret)
};

// AFTER: DTO owns mapping
// In AuthConfigDto.cs : PlatformDto<AuthConfig>
public override AuthConfig MapToObject() => new AuthConfig
{
    ClientId = ClientId,
    Secret = Secret  // Handler applies encryption
};

// In Handler
var config = req.Dto.MapToObject()
    .With(c => c.Secret = encryptService.Encrypt(c.Secret));
```

## Safety Checklist

Before any refactoring:

- [ ] Searched all usages (static + dynamic)?
- [ ] Test coverage exists?
- [ ] Documented in todo list?
- [ ] Changes are incremental?
- [ ] No behavior change verified?

## Code Responsibility Refactoring (Priority Check)

**Before any refactoring, verify logic is in the LOWEST appropriate layer:**

```
Entity/Model (Lowest)  →  Service  →  Component/Handler (Highest)
```

| Wrong Location | Move To           | Example                                     |
| -------------- | ----------------- | ------------------------------------------- |
| Component      | Entity/Model      | Dropdown options, display helpers, defaults |
| Component      | Service (Factory) | Command building, data transformation       |
| Handler        | Entity            | Business rules, static expressions          |
| Handler        | Repository Ext    | Reusable query patterns                     |

```typescript
// Frontend: Component → Entity refactoring
// BEFORE: Logic in component (causes duplication)
readonly statusTypes = [{ value: 1, label: 'Active' }, { value: 2, label: 'Inactive' }];
getStatusClass(config) { return !config.isEnabled ? 'disabled' : 'active'; }

// AFTER: Logic in entity (enables reuse)
readonly statusTypes = EntityConfiguration.getStatusTypeOptions();
getStatusClass(config) { return config.getStatusCssClass(); }
```

## Component HTML Template Standard (BEM Classes)

**All UI elements in component templates MUST have BEM classes, even without styling needs.** This makes HTML self-documenting like OOP class hierarchy.

```html
<!-- ✅ CORRECT: All elements have BEM classes -->
<div class="settings-panel">
    <div class="settings-panel__header">
        <h2 class="settings-panel__title">Settings</h2>
    </div>
    <div class="settings-panel__body">
        <div class="settings-panel__section">
            <label class="settings-panel__label">Option</label>
            <input class="settings-panel__input" formControlName="option" />
        </div>
    </div>
</div>

<!-- ❌ WRONG: Missing BEM classes -->
<div class="settings-panel">
    <div>
        <h2>Settings</h2>
    </div>
    <div>
        <div>
            <label>Option</label>
            <input formControlName="option" />
        </div>
    </div>
</div>
```

**Refactoring Action**: When refactoring components, ensure all HTML elements have proper BEM classes.

## Component SCSS Standard

Always style both the **host element** (Angular selector) and the **main wrapper class**:

```scss
@import '~assets/scss/variables';

// Host element styling - ensures Angular element is a proper block container
my-component {
    display: flex;
    flex-direction: column;
}

// Main wrapper class with full styling
.my-component {
    display: flex;
    flex-direction: column;
    width: 100%;
    flex-grow: 1;

    &__header {
        // BEM child elements...
    }

    &__content {
        flex: 1;
        overflow-y: auto;
    }
}
```

**Why both?**

- **Host element**: Makes the Angular element a real layout element (not an unknown element without display)
- **Main class**: Contains the full styling, matches the wrapper div in HTML

```csharp
// Backend: Handler → Entity refactoring
// BEFORE: Logic in handler
var isValid = entity.Status == Status.Active && entity.User?.IsActive == true;

// AFTER: Logic in entity
var entity = await repository.FirstOrDefaultAsync(Entity.IsActiveExpr(), ct);
```

## Anti-Patterns

- **Big Bang Refactoring**: Make small, incremental changes
- **Refactoring Without Tests**: Ensure coverage first
- **Mixing Refactoring with Features**: Do one or the other
- **Breaking Public APIs**: Maintain backward compatibility
- **Logic in Wrong Layer**: Leads to duplicated code - move to lowest appropriate layer
