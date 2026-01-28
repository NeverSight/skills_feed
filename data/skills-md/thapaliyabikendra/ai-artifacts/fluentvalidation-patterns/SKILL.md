---
name: fluentvalidation-patterns
description: "Master FluentValidation patterns for ABP Framework including async validators, repository checks, conditional rules, localized messages, and custom validators. Use when creating input DTO validators for AppServices."
layer: 2
tech_stack: [dotnet, csharp, abp]
topics: [validation, dto-validation, async-validation, business-rules, localization]
depends_on: [error-handling-patterns]
complements: [abp-framework-patterns]
keywords: [FluentValidation, AbstractValidator, RuleFor, MustAsync, NotEmpty, MaximumLength]
---

# FluentValidation Patterns

FluentValidation patterns for ABP Framework input DTO validation.

## When to Use

- Creating validators for Create/Update DTOs
- Implementing async validation with repository checks
- Building conditional validation rules
- Creating reusable custom validators
- Localizing validation error messages

## ABP Integration

### Basic Validator Structure

```csharp
// Application/{Feature}/CreateUpdate{Entity}DtoValidator.cs
public class CreateUpdate{Entity}DtoValidator : AbstractValidator<CreateUpdate{Entity}Dto>
{
    public CreateUpdatePatientDtoValidator()
    {
        RuleFor(x => x.FirstName)
            .NotEmpty()
            .MaximumLength(100);

        RuleFor(x => x.LastName)
            .NotEmpty()
            .MaximumLength(100);

        RuleFor(x => x.Email)
            .NotEmpty()
            .EmailAddress()
            .MaximumLength(255);

        RuleFor(x => x.DateOfBirth)
            .NotEmpty()
            .LessThan(DateTime.Today)
            .WithMessage("Date of birth must be in the past");
    }
}
```

### ABP Module Registration

```csharp
// ApplicationModule.cs
public override void PreConfigureServices(ServiceConfigurationContext context)
{
    PreConfigure<AbpFluentValidationAutoValidationOptions>(options =>
    {
        options.AutoValidateMethodInvocations = true;
    });
}

public override void ConfigureServices(ServiceConfigurationContext context)
{
    // Auto-register all validators in assembly
    context.Services.AddValidatorsFromAssembly(typeof({ProjectName}ApplicationModule).Assembly);
}
```

## Common Validation Rules

### String Validation

```csharp
RuleFor(x => x.Name)
    .NotEmpty()
    .WithMessage("Name is required")
    .MinimumLength(2)
    .MaximumLength(100)
    .Matches(@"^[a-zA-Z\s]+$")
    .WithMessage("Name can only contain letters and spaces");

RuleFor(x => x.Email)
    .NotEmpty()
    .EmailAddress()
    .Must(email => !email.EndsWith("@test.com"))
    .WithMessage("Test emails are not allowed");

RuleFor(x => x.Phone)
    .NotEmpty()
    .Matches(@"^\+?[1-9]\d{1,14}$")
    .WithMessage("Invalid phone number format");
```

### Numeric Validation

```csharp
RuleFor(x => x.Age)
    .InclusiveBetween(0, 150)
    .WithMessage("Age must be between 0 and 150");

RuleFor(x => x.Price)
    .GreaterThan(0)
    .LessThanOrEqualTo(1000000)
    .PrecisionScale(10, 2, false);

RuleFor(x => x.Quantity)
    .GreaterThanOrEqualTo(1)
    .When(x => x.IsRequired);
```

### Date Validation

```csharp
RuleFor(x => x.DateOfBirth)
    .NotEmpty()
    .LessThan(DateTime.Today)
    .GreaterThan(DateTime.Today.AddYears(-150));

RuleFor(x => x.AppointmentDate)
    .NotEmpty()
    .GreaterThan(DateTime.Now)
    .WithMessage("Appointment must be in the future");

RuleFor(x => x.EndDate)
    .GreaterThan(x => x.StartDate)
    .When(x => x.EndDate.HasValue)
    .WithMessage("End date must be after start date");
```

### Collection Validation

```csharp
RuleFor(x => x.Tags)
    .NotEmpty()
    .Must(tags => tags.Count <= 10)
    .WithMessage("Maximum 10 tags allowed");

RuleForEach(x => x.Items)
    .ChildRules(item =>
    {
        item.RuleFor(i => i.ProductId).NotEmpty();
        item.RuleFor(i => i.Quantity).GreaterThan(0);
    });

RuleFor(x => x.Emails)
    .Must(emails => emails.Distinct().Count() == emails.Count)
    .WithMessage("Duplicate emails are not allowed");
```

## Async Validation with Repository

### Unique Email Check

```csharp
public class CreateUpdate{Entity}DtoValidator : AbstractValidator<CreateUpdate{Entity}Dto>
{
    private readonly IRepository<{Entity}, Guid> _repository;

    public CreateUpdate{Entity}DtoValidator(IRepository<{Entity}, Guid> repository)
    {
        _repository = repository;

        RuleFor(x => x.Email)
            .NotEmpty()
            .EmailAddress()
            .MustAsync(BeUniqueEmail)
            .WithMessage("Email already exists");
    }

    private async Task<bool> BeUniqueEmail(string email, CancellationToken cancellationToken)
    {
        return !await _repository.AnyAsync(e => e.Email == email);
    }
}
```

### Unique Check with Edit Context

```csharp
public class CreateUpdate{Entity}DtoValidator : AbstractValidator<CreateUpdate{Entity}Dto>
{
    private readonly IRepository<{Entity}, Guid> _repository;
    private readonly IHttpContextAccessor _httpContextAccessor;

    public CreateUpdate{Entity}DtoValidator(
        IRepository<{Entity}, Guid> repository,
        IHttpContextAccessor httpContextAccessor)
    {
        _repository = repository;
        _httpContextAccessor = httpContextAccessor;

        RuleFor(x => x.Email)
            .NotEmpty()
            .EmailAddress()
            .MustAsync(BeUniqueEmailAsync)
            .WithMessage("Email already exists");
    }

    private async Task<bool> BeUniqueEmailAsync(string email, CancellationToken cancellationToken)
    {
        // Get entity ID from route (for updates)
        var routeData = _httpContextAccessor.HttpContext?.GetRouteData();
        var idString = routeData?.Values["id"]?.ToString();

        if (Guid.TryParse(idString, out var entityId))
        {
            // Exclude current entity from check (update scenario)
            return !await _repository.AnyAsync(
                e => e.Email == email && e.Id != entityId);
        }

        // Create scenario
        return !await _repository.AnyAsync(e => e.Email == email);
    }
}
```

### Foreign Key Exists Check

```csharp
public class Create{Entity}DtoValidator : AbstractValidator<Create{Entity}Dto>
{
    private readonly IRepository<{ParentEntity}, Guid> _parentRepository;
    private readonly IRepository<{RelatedEntity}, Guid> _relatedRepository;

    public Create{Entity}DtoValidator(
        IRepository<{ParentEntity}, Guid> parentRepository,
        IRepository<{RelatedEntity}, Guid> relatedRepository)
    {
        _parentRepository = parentRepository;
        _relatedRepository = relatedRepository;

        RuleFor(x => x.{ParentEntity}Id)
            .NotEmpty()
            .MustAsync(ParentExistsAsync)
            .WithMessage("{ParentEntity} not found");

        RuleFor(x => x.{RelatedEntity}Id)
            .NotEmpty()
            .MustAsync(RelatedExistsAsync)
            .WithMessage("{RelatedEntity} not found");
    }

    private async Task<bool> ParentExistsAsync(Guid id, CancellationToken ct)
    {
        return await _parentRepository.AnyAsync(e => e.Id == id);
    }

    private async Task<bool> RelatedExistsAsync(Guid id, CancellationToken ct)
    {
        return await _relatedRepository.AnyAsync(e => e.Id == id);
    }
}
```

## Conditional Validation

### When/Unless

```csharp
RuleFor(x => x.CompanyName)
    .NotEmpty()
    .When(x => x.CustomerType == CustomerType.Business)
    .WithMessage("Company name is required for business customers");

RuleFor(x => x.TaxId)
    .NotEmpty()
    .Matches(@"^\d{9}$")
    .When(x => x.CustomerType == CustomerType.Business);

RuleFor(x => x.BirthDate)
    .NotEmpty()
    .Unless(x => x.CustomerType == CustomerType.Business);
```

### Complex Conditional Logic

```csharp
RuleFor(x => x.EndDate)
    .NotEmpty()
    .GreaterThan(x => x.StartDate)
    .When(x => x.IsRecurring && x.RecurrenceType != RecurrenceType.Indefinite);

When(x => x.PaymentMethod == PaymentMethod.CreditCard, () =>
{
    RuleFor(x => x.CardNumber).NotEmpty().CreditCard();
    RuleFor(x => x.ExpirationDate).NotEmpty().GreaterThan(DateTime.Today);
    RuleFor(x => x.CVV).NotEmpty().Length(3, 4);
});

When(x => x.PaymentMethod == PaymentMethod.BankTransfer, () =>
{
    RuleFor(x => x.BankAccountNumber).NotEmpty();
    RuleFor(x => x.RoutingNumber).NotEmpty();
});
```

## Custom Validators

### Reusable Property Validator

```csharp
// Validators/PhoneNumberValidator.cs
public class PhoneNumberValidator<T> : PropertyValidator<T, string>
{
    public override string Name => "PhoneNumberValidator";

    public override bool IsValid(ValidationContext<T> context, string value)
    {
        if (string.IsNullOrEmpty(value))
            return true; // Let NotEmpty handle required check

        // E.164 format
        return Regex.IsMatch(value, @"^\+[1-9]\d{1,14}$");
    }

    protected override string GetDefaultMessageTemplate(string errorCode)
        => "'{PropertyName}' must be a valid phone number in E.164 format";
}

// Extension method for fluent usage
public static class ValidatorExtensions
{
    public static IRuleBuilderOptions<T, string> PhoneNumber<T>(
        this IRuleBuilder<T, string> ruleBuilder)
    {
        return ruleBuilder.SetValidator(new PhoneNumberValidator<T>());
    }
}

// Usage
RuleFor(x => x.Phone).PhoneNumber();
```

### Async Custom Validator

```csharp
public class UniqueEmailValidator<T> : AsyncPropertyValidator<T, string>
{
    private readonly IRepository<{Entity}, Guid> _repository;

    public UniqueEmailValidator(IRepository<{Entity}, Guid> repository)
    {
        _repository = repository;
    }

    public override string Name => "UniqueEmailValidator";

    public override async Task<bool> IsValidAsync(
        ValidationContext<T> context,
        string value,
        CancellationToken cancellation)
    {
        if (string.IsNullOrEmpty(value))
            return true;

        return !await _repository.AnyAsync(e => e.Email == value);
    }

    protected override string GetDefaultMessageTemplate(string errorCode)
        => "'{PropertyName}' must be unique";
}
```

## Localization

### Using ABP Localization

```csharp
public class CreateUpdate{Entity}DtoValidator : AbstractValidator<CreateUpdate{Entity}Dto>
{
    private readonly IStringLocalizer<{ProjectName}Resource> _localizer;

    public CreateUpdate{Entity}DtoValidator(
        IStringLocalizer<{ProjectName}Resource> localizer)
    {
        _localizer = localizer;

        RuleFor(x => x.FirstName)
            .NotEmpty()
            .WithMessage(_localizer["Validation:FirstNameRequired"])
            .MaximumLength(100)
            .WithMessage(_localizer["Validation:FirstNameMaxLength", 100]);

        RuleFor(x => x.Email)
            .NotEmpty()
            .WithMessage(_localizer["Validation:EmailRequired"])
            .EmailAddress()
            .WithMessage(_localizer["Validation:EmailInvalid"]);
    }
}

// Localization JSON: Localization/{ProjectName}/en.json
{
  "Validation:FirstNameRequired": "First name is required",
  "Validation:FirstNameMaxLength": "First name cannot exceed {0} characters",
  "Validation:EmailRequired": "Email is required",
  "Validation:EmailInvalid": "Please enter a valid email address"
}
```

## Validation in AppService

### Manual Validation

```csharp
public class {Entity}AppService : ApplicationService, I{Entity}AppService
{
    private readonly IValidator<CreateUpdate{Entity}Dto> _validator;

    public async Task<{Entity}Dto> CreateAsync(CreateUpdate{Entity}Dto input)
    {
        // Manual validation (if auto-validation disabled)
        var validationResult = await _validator.ValidateAsync(input);
        if (!validationResult.IsValid)
        {
            throw new AbpValidationException(
                validationResult.Errors
                    .Select(e => new ValidationResult(e.ErrorMessage, new[] { e.PropertyName }))
                    .ToList()
            );
        }

        // Proceed with creation
    }
}
```

### Validation with Custom Context

```csharp
public async Task<{Entity}Dto> UpdateAsync(Guid id, CreateUpdate{Entity}Dto input)
{
    var context = new ValidationContext<CreateUpdate{Entity}Dto>(input)
    {
        RootContextData =
        {
            ["EntityId"] = id
        }
    };

    var validationResult = await _validator.ValidateAsync(context);
    // ...
}

// In validator
private async Task<bool> BeUniqueEmailAsync(
    CreateUpdate{Entity}Dto dto,
    string email,
    ValidationContext<CreateUpdate{Entity}Dto> context,
    CancellationToken ct)
{
    var entityId = context.RootContextData.TryGetValue("EntityId", out var id)
        ? (Guid?)id
        : null;

    if (entityId.HasValue)
    {
        return !await _repository.AnyAsync(p => p.Email == email && p.Id != entityId);
    }

    return !await _repository.AnyAsync(p => p.Email == email);
}
```

## Best Practices

1. **One validator per DTO** - Keep validators focused
2. **Inject dependencies** - Use constructor injection for repositories
3. **Use async for DB checks** - Always use `MustAsync` for repository queries
4. **Localize messages** - Use ABP localization for user-facing messages
5. **Reuse validators** - Create custom validators for common patterns
6. **Conditional rules** - Use `When`/`Unless` for context-dependent validation
7. **Order matters** - Put cheap validations first, async last
8. **Handle null gracefully** - Let `NotEmpty` handle required checks

## Quality Checklist

- [ ] Validator created for each input DTO
- [ ] All required fields have `NotEmpty()` rule
- [ ] String fields have `MaximumLength()` matching entity
- [ ] Email fields use `EmailAddress()` validator
- [ ] Foreign keys validated with `MustAsync` existence check
- [ ] Unique constraints validated with repository check
- [ ] Error messages are localized
- [ ] Validators registered in module

## Shared Knowledge

For foundational patterns, see the shared knowledge base:

| Topic | File | Description |
|-------|------|-------------|
| Naming conventions | [knowledge/conventions/naming.md](../../knowledge/conventions/naming.md) | Validator naming patterns |
| Validation example | [knowledge/examples/validation-chain.md](../../knowledge/examples/validation-chain.md) | Complete validation examples |
| Folder structure | [knowledge/conventions/folder-structure.md](../../knowledge/conventions/folder-structure.md) | Validator file locations |

## Integration Points

This skill is used by:
- **abp-developer**: DTO validator implementation
- **abp-code-reviewer**: Validation pattern review
- **/generate:entity**: Validator scaffolding
