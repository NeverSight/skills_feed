---
name: blazor
description: |
  Builds Blazor WASM components for admin and main UI applications.
  Use when: Creating/modifying Razor components, configuring render modes, implementing authentication, managing component state, or working with MudBlazor components.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# Blazor Skill

Sorcha uses Blazor with hybrid rendering (Server + WebAssembly). The Admin UI (`src/Apps/Sorcha.Admin/`) runs behind YARP API Gateway. Components use MudBlazor for UI and support three render modes: static server, interactive server, and interactive WASM.

## Quick Start

### Render Mode Selection

```razor
@* WASM - Complex interactive pages (Designer, Diagrams) *@
@page "/designer"
@rendermode InteractiveWebAssembly
@attribute [Authorize]

@* Server - Admin pages needing real-time SignalR *@
@page "/admin/audit"
@rendermode @(new InteractiveServerRenderMode(prerender: false))
@attribute [Authorize(Roles = "Administrator")]

@* Static - Public pages (Login) - no @rendermode directive *@
@page "/login"
@attribute [AllowAnonymous]
```

### Component with Loading State

```razor
@inject HttpClient Http

<MudPaper Elevation="2" Class="pa-4">
    @if (_isLoading && !_hasLoadedOnce)
    {
        <MudProgressCircular Indeterminate="true" Size="Size.Small" />
    }
    else if (_data != null)
    {
        <MudText>@_data.Title</MudText>
    }
    else if (_errorMessage != null)
    {
        <MudAlert Severity="Severity.Error">@_errorMessage</MudAlert>
    }
</MudPaper>

@code {
    private DataDto? _data;
    private string? _errorMessage;
    private bool _isLoading;
    private bool _hasLoadedOnce;

    protected override async Task OnAfterRenderAsync(bool firstRender)
    {
        if (firstRender)
            await LoadDataAsync();
    }

    private async Task LoadDataAsync()
    {
        _isLoading = true;
        try
        {
            _data = await Http.GetFromJsonAsync<DataDto>("/api/data");
            _hasLoadedOnce = true;
        }
        catch (Exception ex)
        {
            _errorMessage = ex.Message;
        }
        finally
        {
            _isLoading = false;
            StateHasChanged();
        }
    }
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Render Mode | Control where component runs | `@rendermode InteractiveWebAssembly` |
| CascadingParameter | Receive parent state | `[CascadingParameter] MudBlazor.IDialogReference? MudDialog` |
| OnAfterRenderAsync | Initialize after DOM ready | `if (firstRender) await LoadAsync();` |
| StateHasChanged | Trigger re-render | Call after async state updates |
| NavigationManager | Programmatic navigation | `Navigation.NavigateTo("/", forceLoad: true)` |

## Project Structure

| Project | Purpose | Render Mode |
|---------|---------|-------------|
| `Sorcha.Admin` | Server host, auth, API proxy | Server + prerender |
| `Sorcha.Admin.Client` | WASM components | WebAssembly |
| `Sorcha.UI.Core` | Shared components | Both |
| `Sorcha.UI.Web` | Main UI server | Server |
| `Sorcha.UI.Web.Client` | Main UI WASM | WebAssembly |

## Common Patterns

### MudBlazor Dialog

```razor
<MudDialog DisableSidePadding="false">
    <DialogContent>
        <MudTextField @bind-Value="_value" Label="Input" />
    </DialogContent>
    <DialogActions>
        <MudButton OnClick="Cancel">Cancel</MudButton>
        <MudButton Color="Color.Primary" OnClick="Submit">OK</MudButton>
    </DialogActions>
</MudDialog>

@code {
    [CascadingParameter] MudBlazor.IDialogReference? MudDialog { get; set; }
    private string _value = "";
    
    private void Cancel() => MudDialog?.Close();
    private void Submit() => MudDialog?.Close(DialogResult.Ok(_value));
}
```

### Opening Dialog from Parent

```csharp
var dialog = await DialogService.ShowAsync<LoginDialog>("Login");
var result = await dialog.Result;
if (result is { Canceled: false })
{
    // Handle success
}
```

## See Also

- [patterns](references/patterns.md) - Component and authentication patterns
- [workflows](references/workflows.md) - Development and deployment workflows

## Related Skills

- See the **aspire** skill for service discovery configuration
- See the **signalr** skill for real-time notifications
- See the **jwt** skill for authentication token handling
- See the **yarp** skill for API Gateway configuration
- See the **mudblazor** skill for component library details

## Documentation Resources

> Fetch latest Blazor/MudBlazor documentation with Context7.

**Library ID:** `/websites/mudblazor` _(MudBlazor component library documentation)_

**Recommended Queries:**
- "MudBlazor dialog service usage"
- "MudBlazor form validation"
- "MudBlazor data grid filtering"