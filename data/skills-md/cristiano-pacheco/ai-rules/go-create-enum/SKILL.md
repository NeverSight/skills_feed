---
name: go-create-enum
description: Generate Go enums following GO modular architechture conventions (string-based enums with validation, constructor, and String method). Use when creating type-safe string enumerations in internal/modules/<module>/enum/ or when user asks to create an enum, add an enum type, or define enum constants.
---

# Go Enum Generator

Generate type-safe Go enums following GO modular architechture conventions.

## Pattern

Place enums in `internal/modules/<module>/enum/<name>_enum.go`.

Each enum file contains:
1. String constants for each enum value
2. Validation map for O(1) lookups
3. Enum struct type
4. Constructor with validation (`New<Type>Enum`)
5. `String()` method
6. Private validation function (`validate<Type>`)

## Example Structure

For an enum named "ContactType" with values "email" and "webhook":

```go
package enum

import "github.com/cristiano-pacheco/pingo/internal/modules/monitor/errs"

const (
	ContactTypeEmail   = "email"
	ContactTypeWebhook = "webhook"
)

var validContactTypes = map[string]struct{}{
	ContactTypeEmail:   {},
	ContactTypeWebhook: {},
}

type ContactTypeEnum struct {
	value string
}

func NewContactTypeEnum(value string) (ContactTypeEnum, error) {
	if err := validateContactType(value); err != nil {
		return ContactTypeEnum{}, err
	}
	return ContactTypeEnum{value: value}, nil
}

func (e ContactTypeEnum) String() string {
	return e.value
}

func validateContactType(contactType string) error {
	if _, ok := validContactTypes[contactType]; !ok {
		return errs.ErrInvalidContactType
	}
	return nil
}
```

## Generation Steps

1. **Identify enum details**:
   - Enum name (e.g., "ContactType", "Status", "Priority")
   - Possible values (e.g., ["email", "webhook"], ["active", "inactive"])
   - Target module (e.g., "monitor", "auth")

2. **Create error constant**:
   - Add error to `internal/modules/<module>/errs/errs.go`
   - Format: `ErrInvalid<EnumName> = errors.New("invalid <enum_name>")`
   - Example: `ErrInvalidContactType = errors.New("invalid contact type")`
   - Add translation entry for the new error in `locales/en.json`
   - If additional locale files exist (e.g., `locales/pt_BR.json`), add the same translation key there too

3. **Generate enum file**:
   - Filename: `<snake_case_enum_name>_enum.go`
   - Package: `enum`
   - Import module errs package
   - Follow structure above with all components

## Naming Conventions

- **File**: `<snake_case>_enum.go` (e.g., `contact_type_enum.go`)
- **Constants**: `<EnumName><Value>` (e.g., `ContactTypeEmail`)
- **Validation map**: `valid<EnumName>s` (lowercase, plural)
- **Struct**: `<EnumName>Enum` (e.g., `ContactTypeEnum`)
- **Constructor**: `New<EnumName>Enum`
- **Validator**: `validate<EnumName>` (private, singular, takes string param)
- **Error**: `ErrInvalid<EnumName>` in module's `errs` package

## Implementation Checklist

- [ ] Add `ErrInvalid<EnumName>` to `internal/modules/<module>/errs/errors.go`
- [ ] Add translation for the new error in `locales/en.json`
- [ ] Add the same translation key in every other existing locale file (e.g., `locales/pt_BR.json`)
- [ ] Create `internal/modules/<module>/enum/<name>_enum.go`
- [ ] Define all constant values
- [ ] Create validation map with all values
- [ ] Define enum struct type (private `value string` field)
- [ ] Implement `New<EnumName>Enum(value string) (<EnumName>Enum, error)` constructor
- [ ] Implement `String() string` method
- [ ] Implement `validate<EnumName>(value string) error` private function

## Usage Pattern

Other code creates enums via the constructor (validation happens internally):

```go
// Create typed enum (validation is automatic)
contactType, err := enum.NewContactTypeEnum(input)
if err != nil {
    return err
}
fmt.Println(contactType.String()) // "email"

// Use constants directly when value is known at compile time
const defaultType = enum.ContactTypeEmail
```

## Critical Rules

- Every new custom error created for enum validation must include locale entries in `locales/en.json` and all other existing locale files
