---
name: pdf-forge
description: Use when building, extending or using pdf-forge multi-tenant PDF template engine with Typst
---

# pdf-forge

Go module for multi-tenant document templates with PDF generation via Typst.

## Installation

```bash
npx skills add https://github.com/rendis/pdf-forge --skill pdf-forge
```

## How It Works

```plaintext
Tenant → Workspace → Template → Version (DRAFT→PUBLISHED)
                                    ↓
                              Injectables (variables)
                                    ↓
                              Render → PDF
```

## Quick Start

```go
engine := sdk.New(
    sdk.WithConfigFile("config/app.yaml"),
    sdk.WithI18nFile("config/injectors.i18n.yaml"),
)

engine.RegisterInjector(&CustomerNameInjector{})
engine.SetMapper(&MyMapper{})
engine.SetInitFunc(MyInit())

if err := engine.Run(); err != nil {
    log.Fatal(err)
}
```

## Creating an Injector

```go
type CustomerNameInjector struct{}

func (i *CustomerNameInjector) Code() string { return "customer_name" }

func (i *CustomerNameInjector) Resolve() (sdk.ResolveFunc, []string) {
    return func(ctx context.Context, injCtx *sdk.InjectorContext) (*sdk.InjectorResult, error) {
        payload := injCtx.RequestPayload().(map[string]any)
        return &sdk.InjectorResult{Value: sdk.StringValue(payload["name"].(string))}, nil
    }, nil  // dependencies
}

func (i *CustomerNameInjector) IsCritical() bool              { return true }
func (i *CustomerNameInjector) Timeout() time.Duration        { return 5 * time.Second }
func (i *CustomerNameInjector) DataType() sdk.ValueType       { return sdk.ValueTypeString }
func (i *CustomerNameInjector) DefaultValue() *sdk.InjectableValue { return nil }
func (i *CustomerNameInjector) Formats() *sdk.FormatConfig    { return nil }
```

## Value Types

| Type      | Constructor             | Constant              |
| --------- | ----------------------- | --------------------- |
| Text      | `sdk.StringValue(s)`    | `sdk.ValueTypeString` |
| Number    | `sdk.NumberValue(n)`    | `sdk.ValueTypeNumber` |
| Boolean   | `sdk.BoolValue(b)`      | `sdk.ValueTypeBool`   |
| Date/Time | `sdk.TimeValue(t)`      | `sdk.ValueTypeTime`   |
| Image     | `sdk.ImageValue(url)`   | `sdk.ValueTypeImage`  |
| Table     | `sdk.TableValueData(t)` | `sdk.ValueTypeTable`  |
| List      | `sdk.ListValueData(l)`  | `sdk.ValueTypeList`   |

See **types-reference.md** for Tables, Lists, InjectorContext, FormatConfig.

## Built-in Injectors

| Code            | Type   | Formats                            |
| --------------- | ------ | ---------------------------------- |
| `date_now`      | TIME   | DD/MM/YYYY, MM/DD/YYYY, YYYY-MM-DD |
| `time_now`      | TIME   | HH:mm, HH:mm:ss, hh:mm a           |
| `date_time_now` | TIME   | Combined                           |
| `year_now`      | NUMBER | -                                  |
| `month_now`     | NUMBER | number, name, short_name           |
| `day_now`       | NUMBER | -                                  |

## Error Handling

| `IsCritical()` | On Error                         |
| -------------- | -------------------------------- |
| `true`         | Aborts render                    |
| `false`        | Uses `DefaultValue()`, continues |

## Extension Points

| Extension  | Purpose             | Register                                |
| ---------- | ------------------- | --------------------------------------- |
| Injector   | Data resolvers      | `RegisterInjector()`                    |
| Mapper     | Request parsing     | `SetMapper()`                           |
| InitFunc   | Shared setup        | `SetInitFunc()`                         |
| Provider   | Dynamic injectables | `SetWorkspaceInjectableProvider()`      |
| Auth       | Custom render auth  | `SetRenderAuthenticator()`              |
| Middleware | Request handling    | `UseMiddleware()`, `UseAPIMiddleware()` |
| Lifecycle  | Startup/shutdown    | `OnStart()`, `OnShutdown()`             |

See **extensions-reference.md** for implementation examples.

## Configuration

See **config-reference.md** for all YAML keys, env vars, and auth setup.

**Dummy auth**: Omit `auth` config entirely for development mode.

## CLI Commands

```bash
pdfforge-cli              # Interactive menu
pdfforge-cli init <name>  # Create new project
pdfforge-cli doctor       # Check Typst, DB, auth
pdfforge-cli migrate      # Run migrations
```

## Common Mistakes

| Wrong                                | Correct                       |
| ------------------------------------ | ----------------------------- |
| `sdk.NewTextValue()`                 | `sdk.StringValue()`           |
| `sdk.ValueTypeText`                  | `sdk.ValueTypeString`         |
| Forgetting dependencies              | `return fn, []string{"dep1"}` |
| `IsCritical()=true` without handling | Provide `DefaultValue()`      |

## API Headers

| Header           | Purpose                             |
| ---------------- | ----------------------------------- |
| `Authorization`  | `Bearer <JWT>` (omit in dummy mode) |
| `X-Tenant-ID`    | Tenant UUID                         |
| `X-Workspace-ID` | Workspace UUID                      |

## References

- **config-reference.md** - YAML keys, env vars, auth, performance
- **types-reference.md** - Tables, Lists, FormatConfig, InjectorContext
- **extensions-reference.md** - Middleware, Lifecycle, Provider, Auth examples
- **patterns-reference.md** - Logging, error handling, context, anti-patterns
- **enterprise-scenarios.md** - CRM integration, Vault, validation patterns
- **domain-reference.md** - Tenants, workspaces, roles, render flow
- **scripts-reference.md** - Custom scripts system (`make run-script`)
