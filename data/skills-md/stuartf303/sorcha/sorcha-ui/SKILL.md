---
name: sorcha-ui
description: |
  Builds Sorcha.UI Blazor WASM pages with accompanying Playwright E2E tests using the Docker test infrastructure.
  Use when: Working on Sorcha.UI, building new pages, replacing template pages, adding UI features, or testing UI functionality against Docker.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# Sorcha UI Development Skill

Test-driven UI development for Sorcha.UI. Every page change is paired with Playwright E2E tests that run against the Docker environment (`docker-compose up -d`). Tests automatically validate console errors, network failures, MudBlazor CSS health, and take screenshots on failure.

## Prerequisites

Docker must be running with all services:
```bash
docker-compose up -d
# UI at http://localhost:5400 | API Gateway at http://localhost:80
# Login: admin@sorcha.local / Dev_Pass_2025!
```

## Workflow: Building a Page

For every page you build or modify, follow these steps in order:

### Step 1: Create the Page Object

Create `tests/Sorcha.UI.E2E.Tests/PageObjects/{PageName}Page.cs`:

```csharp
using Microsoft.Playwright;
using Sorcha.UI.E2E.Tests.Infrastructure;
using Sorcha.UI.E2E.Tests.PageObjects.Shared;

namespace Sorcha.UI.E2E.Tests.PageObjects;

public class WalletListPage
{
    private readonly IPage _page;
    public WalletListPage(IPage page) => _page = page;

    // Use data-testid as primary selector strategy
    public ILocator WalletCards => MudBlazorHelpers.TestIdPrefix(_page, "wallet-card-");
    public ILocator CreateButton => MudBlazorHelpers.TestId(_page, "create-wallet-btn");
    public ILocator EmptyState => MudBlazorHelpers.TestId(_page, "wallet-empty-state");
    public ILocator SearchInput => _page.Locator("input[placeholder*='Search']");

    // Fallback to MudBlazor class selectors
    public ILocator Table => MudBlazorHelpers.Table(_page);
    public ILocator LoadingSpinner => MudBlazorHelpers.CircularProgress(_page);

    public async Task NavigateAsync()
    {
        await _page.GotoAsync($"{TestConstants.UiWebUrl}{TestConstants.AuthenticatedRoutes.Wallets}");
        await _page.WaitForLoadStateAsync(LoadState.NetworkIdle);
        await MudBlazorHelpers.WaitForBlazorAsync(_page);
    }

    public async Task<int> GetWalletCountAsync() => await WalletCards.CountAsync();
    public async Task<bool> IsEmptyStateVisibleAsync() =>
        await EmptyState.CountAsync() > 0 && await EmptyState.IsVisibleAsync();
}
```

### Step 2: Write the Playwright Tests (Test-First)

Create `tests/Sorcha.UI.E2E.Tests/Docker/{Feature}Tests.cs`:

```csharp
using Sorcha.UI.E2E.Tests.Infrastructure;
using Sorcha.UI.E2E.Tests.PageObjects;

namespace Sorcha.UI.E2E.Tests.Docker;

[Parallelizable(ParallelScope.Self)]
[TestFixture]
[Category("Docker")]
[Category("Wallets")]
[Category("Authenticated")]
public class WalletListTests : AuthenticatedDockerTestBase
{
    private WalletListPage _walletList = null!;

    [SetUp]
    public override async Task BaseSetUp()
    {
        await base.BaseSetUp();
        _walletList = new WalletListPage(Page);
    }

    [Test]
    [Retry(2)]
    public async Task WalletList_LoadsWithoutErrors()
    {
        await NavigateAuthenticatedAsync(TestConstants.AuthenticatedRoutes.Wallets);
        // Base class automatically checks console errors, network 5xx, CSS health
    }

    [Test]
    public async Task WalletList_ShowsEmptyStateOrWallets()
    {
        await _walletList.NavigateAsync();
        var count = await _walletList.GetWalletCountAsync();
        if (count == 0)
        {
            Assert.That(await _walletList.IsEmptyStateVisibleAsync(), Is.True,
                "Empty system should show empty state message");
        }
        else
        {
            Assert.That(count, Is.GreaterThan(0));
        }
    }
}
```

### Step 3: Build the Blazor Page

Edit `src/Apps/Sorcha.UI/Sorcha.UI.Web.Client/Pages/{Page}.razor`:

```razor
@page "/wallets"
@layout MainLayout
@rendermode @(new InteractiveWebAssemblyRenderMode(prerender: false))
@attribute [Authorize]
@inject HttpClient Http

<PageTitle>Wallets - Sorcha</PageTitle>

@if (_isLoading)
{
    <MudProgressCircular Indeterminate="true" data-testid="wallet-loading" />
}
else if (_wallets.Count == 0)
{
    <MudAlert Severity="Severity.Info" data-testid="wallet-empty-state">
        No wallets found. Create your first wallet to get started.
    </MudAlert>
}
else
{
    @foreach (var wallet in _wallets)
    {
        <MudCard data-testid="wallet-card-@wallet.Id" Class="mb-3">
            <MudCardContent>
                <MudText Typo="Typo.h6">@wallet.Name</MudText>
            </MudCardContent>
        </MudCard>
    }
}

<MudButton data-testid="create-wallet-btn" Variant="Variant.Filled"
           Color="Color.Primary" Href="wallets/create">
    Create Wallet
</MudButton>
```

### Step 4: Run Tests

```bash
# Run tests for the feature you just built
dotnet test tests/Sorcha.UI.E2E.Tests --filter "Category=Wallets"

# Run all smoke tests (fast CI gate)
dotnet test tests/Sorcha.UI.E2E.Tests --filter "Category=Smoke"

# Run all Docker tests
dotnet test tests/Sorcha.UI.E2E.Tests --filter "Category=Docker"
```

### Step 5: Check Artifacts on Failure

Screenshots are saved to `tests/Sorcha.UI.E2E.Tests/bin/Debug/net10.0/screenshots/` on any test failure. Console errors and network failures are reported in the test output.

## Key Concepts

| Concept | Usage | Location |
|---------|-------|----------|
| `DockerTestBase` | Unauthenticated tests with auto error capture | `Infrastructure/DockerTestBase.cs` |
| `AuthenticatedDockerTestBase` | Login once, reuse auth state across tests | `Infrastructure/AuthenticatedDockerTestBase.cs` |
| `TestConstants` | URLs, credentials, routes, timeouts | `Infrastructure/TestConstants.cs` |
| Page Objects | Encapsulate selectors and actions per page | `PageObjects/*.cs` |
| `MudBlazorHelpers` | Shared MudBlazor locators and layout validation | `PageObjects/Shared/MudBlazorHelpers.cs` |
| `data-testid` | Primary selector strategy for resilient tests | Added to Razor components |
| Categories | Filter tests by feature or concern | `[Category("Wallets")]` on test classes |

## Test Inheritance

```
PageTest (Playwright NUnit)
  └── DockerTestBase (console errors, network failures, screenshots)
        ├── ComponentHealthTests, LoginTests (unauthenticated)
        └── AuthenticatedDockerTestBase (login once, reuse state, layout health)
              ├── DashboardTests
              ├── NavigationTests
              ├── WalletTests
              └── ... (one per feature area)
```

## Test Categories

| Category | Scope | Use |
|----------|-------|-----|
| `Smoke` | All pages load, no JS errors | CI gate |
| `Docker` | All tests targeting Docker | Full Docker suite |
| `Auth` | Login, logout, redirects | Authentication features |
| `Authenticated` | All tests needing login | Post-login features |
| `Dashboard` | Dashboard page | Dashboard development |
| `Navigation` | Drawer, app bar, routing | Layout changes |
| `Components` | CSS, MudBlazor, responsive | Style/component changes |
| `Wallets` | Wallet pages | Wallet features |
| `Blueprints` | Blueprint pages | Blueprint features |
| `Registers` | Register pages | Register features |
| `Schemas` | Schema library | Schema features |
| `Admin` | Administration pages | Admin features |

## File Locations

| What | Where |
|------|-------|
| Blazor pages | `src/Apps/Sorcha.UI/Sorcha.UI.Web.Client/Pages/` |
| Shared components | `src/Apps/Sorcha.UI/Sorcha.UI.Core/` |
| Layout | `src/Apps/Sorcha.UI/Sorcha.UI.Web.Client/Components/Layout/` |
| Test infrastructure | `tests/Sorcha.UI.E2E.Tests/Infrastructure/` |
| Page objects | `tests/Sorcha.UI.E2E.Tests/PageObjects/` |
| Docker tests | `tests/Sorcha.UI.E2E.Tests/Docker/` |
| MudBlazor helpers | `tests/Sorcha.UI.E2E.Tests/PageObjects/Shared/MudBlazorHelpers.cs` |

## See Also

- [patterns](references/patterns.md) - Page implementation and test patterns
- [workflows](references/workflows.md) - Development workflow and checklist

## Related Skills

- See the **blazor** skill for Blazor WASM component architecture
- See the **playwright** skill for Playwright API reference
- See the **frontend-design** skill for MudBlazor styling
- See the **minimal-apis** skill for backend API endpoints the pages call
- See the **jwt** skill for authentication token handling

## Documentation Resources

> Fetch latest Playwright .NET and MudBlazor documentation with Context7.

**Library IDs:**
- `/websites/playwright_dev_dotnet` (Playwright .NET)
- `/websites/mudblazor` (MudBlazor component library)

**Recommended Queries:**
- "Locators selectors data-testid"
- "NUnit test fixtures parallel"
- "MudBlazor card table dialog"
- "MudBlazor form validation"
- "Browser storage state authentication"
