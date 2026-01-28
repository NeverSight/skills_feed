---
name: api-integration-testing
description: "Integration testing patterns for ABP Framework APIs using xUnit and WebApplicationFactory. Use when: (1) testing API endpoints end-to-end, (2) verifying HTTP status codes and responses, (3) testing authorization, (4) database integration tests."
layer: 3
tech_stack: [csharp, dotnet, xunit, abp]
topics: [integration-tests, api-testing, webapplicationfactory, http-testing]
depends_on: [xunit-testing-patterns, abp-framework-patterns]
complements: [test-data-generation]
keywords: [WebApplicationFactory, HttpClient, IntegrationTest, API, HttpApi]
---

# API Integration Testing

Test ABP Framework APIs end-to-end using xUnit and WebApplicationFactory.

## When to Use

- Testing API endpoints with real HTTP requests
- Verifying authorization and authentication
- Testing request/response serialization
- End-to-end flow validation
- Database integration testing

## Test Project Setup

### Project Structure

```
test/
├── [Module].HttpApi.Tests/
│   ├── [Module]HttpApiTestBase.cs
│   ├── [Module]HttpApiTestModule.cs
│   ├── Controllers/
│   │   ├── PatientControllerTests.cs
│   │   └── DoctorControllerTests.cs
│   └── TestData/
│       └── TestDataSeeder.cs
```

### Test Base Class

```csharp
public abstract class ClinicHttpApiTestBase : AbpIntegratedTest<ClinicHttpApiTestModule>
{
    protected HttpClient Client { get; }
    protected IServiceProvider Services => ServiceProvider;

    protected ClinicHttpApiTestBase()
    {
        Client = GetHttpClient();
    }

    protected HttpClient GetHttpClient()
    {
        var factory = new WebApplicationFactory<Program>()
            .WithWebHostBuilder(builder =>
            {
                builder.ConfigureServices(services =>
                {
                    // Replace database with in-memory
                    services.RemoveAll<DbContextOptions<ClinicDbContext>>();
                    services.AddDbContext<ClinicDbContext>(options =>
                        options.UseInMemoryDatabase("TestDb"));
                });
            });

        return factory.CreateClient();
    }

    protected async Task AuthenticateAsAsync(string username, string[] permissions = null)
    {
        // Set authentication headers
        var token = GenerateTestToken(username, permissions);
        Client.DefaultRequestHeaders.Authorization =
            new AuthenticationHeaderValue("Bearer", token);
    }

    protected async Task<T> GetAsync<T>(string url)
    {
        var response = await Client.GetAsync(url);
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<T>();
    }

    protected async Task<HttpResponseMessage> PostAsync<T>(string url, T content)
    {
        return await Client.PostAsJsonAsync(url, content);
    }
}
```

### Test Module Configuration

```csharp
[DependsOn(
    typeof(ClinicHttpApiModule),
    typeof(AbpAspNetCoreTestBaseModule)
)]
public class ClinicHttpApiTestModule : AbpModule
{
    public override void ConfigureServices(ServiceConfigurationContext context)
    {
        // Configure test-specific services
        context.Services.AddSingleton<ICurrentUser, TestCurrentUser>();
    }
}
```

## Common Test Patterns

### CRUD Endpoint Tests

```csharp
public class PatientControllerTests : ClinicHttpApiTestBase
{
    private const string BaseUrl = "/api/app/patients";

    #region GetList

    [Fact]
    public async Task GetList_ReturnsPagedResult()
    {
        // Act
        var response = await Client.GetAsync(BaseUrl);

        // Assert
        response.StatusCode.ShouldBe(HttpStatusCode.OK);

        var result = await response.Content
            .ReadFromJsonAsync<PagedResultDto<PatientDto>>();
        result.ShouldNotBeNull();
        result.Items.ShouldNotBeNull();
    }

    [Fact]
    public async Task GetList_WithFilter_ReturnsFilteredResults()
    {
        // Act
        var response = await Client.GetAsync($"{BaseUrl}?filter=John");

        // Assert
        response.StatusCode.ShouldBe(HttpStatusCode.OK);
        var result = await response.Content
            .ReadFromJsonAsync<PagedResultDto<PatientDto>>();
        result.Items.ShouldAllBe(p => p.Name.Contains("John"));
    }

    [Fact]
    public async Task GetList_WithPagination_RespectsLimits()
    {
        // Act
        var response = await Client.GetAsync($"{BaseUrl}?skipCount=0&maxResultCount=5");

        // Assert
        var result = await response.Content
            .ReadFromJsonAsync<PagedResultDto<PatientDto>>();
        result.Items.Count.ShouldBeLessThanOrEqualTo(5);
    }

    #endregion

    #region Get

    [Fact]
    public async Task Get_ExistingId_ReturnsPatient()
    {
        // Arrange
        var patientId = TestData.PatientId;

        // Act
        var response = await Client.GetAsync($"{BaseUrl}/{patientId}");

        // Assert
        response.StatusCode.ShouldBe(HttpStatusCode.OK);
        var patient = await response.Content.ReadFromJsonAsync<PatientDto>();
        patient.Id.ShouldBe(patientId);
    }

    [Fact]
    public async Task Get_NonExistingId_Returns404()
    {
        // Act
        var response = await Client.GetAsync($"{BaseUrl}/{Guid.NewGuid()}");

        // Assert
        response.StatusCode.ShouldBe(HttpStatusCode.NotFound);
    }

    #endregion

    #region Create

    [Fact]
    public async Task Create_ValidInput_Returns201WithEntity()
    {
        // Arrange
        var input = new CreatePatientDto
        {
            Name = "Jane Doe",
            Email = "jane@example.com",
            DateOfBirth = new DateTime(1990, 1, 1)
        };

        // Act
        var response = await Client.PostAsJsonAsync(BaseUrl, input);

        // Assert
        response.StatusCode.ShouldBe(HttpStatusCode.Created);

        var created = await response.Content.ReadFromJsonAsync<PatientDto>();
        created.Name.ShouldBe(input.Name);
        created.Id.ShouldNotBe(Guid.Empty);

        // Verify Location header
        response.Headers.Location.ShouldNotBeNull();
    }

    [Fact]
    public async Task Create_MissingRequiredField_Returns400()
    {
        // Arrange
        var input = new CreatePatientDto
        {
            // Name is missing (required)
            Email = "jane@example.com"
        };

        // Act
        var response = await Client.PostAsJsonAsync(BaseUrl, input);

        // Assert
        response.StatusCode.ShouldBe(HttpStatusCode.BadRequest);

        var error = await response.Content.ReadFromJsonAsync<RemoteServiceErrorResponse>();
        error.Error.ValidationErrors
            .ShouldContain(e => e.Members.Contains("Name"));
    }

    [Fact]
    public async Task Create_DuplicateEmail_Returns409()
    {
        // Arrange
        var input = new CreatePatientDto
        {
            Name = "Another Patient",
            Email = TestData.ExistingEmail // Already exists
        };

        // Act
        var response = await Client.PostAsJsonAsync(BaseUrl, input);

        // Assert
        response.StatusCode.ShouldBe(HttpStatusCode.Conflict);
    }

    #endregion

    #region Update

    [Fact]
    public async Task Update_ValidInput_Returns200()
    {
        // Arrange
        var patientId = TestData.PatientId;
        var input = new UpdatePatientDto
        {
            Name = "Updated Name",
            Email = "updated@example.com"
        };

        // Act
        var response = await Client.PutAsJsonAsync($"{BaseUrl}/{patientId}", input);

        // Assert
        response.StatusCode.ShouldBe(HttpStatusCode.OK);

        var updated = await response.Content.ReadFromJsonAsync<PatientDto>();
        updated.Name.ShouldBe(input.Name);
    }

    [Fact]
    public async Task Update_NonExisting_Returns404()
    {
        // Arrange
        var input = new UpdatePatientDto { Name = "Test" };

        // Act
        var response = await Client.PutAsJsonAsync($"{BaseUrl}/{Guid.NewGuid()}", input);

        // Assert
        response.StatusCode.ShouldBe(HttpStatusCode.NotFound);
    }

    #endregion

    #region Delete

    [Fact]
    public async Task Delete_ExistingId_Returns204()
    {
        // Arrange
        var patientId = TestData.DeletablePatientId;

        // Act
        var response = await Client.DeleteAsync($"{BaseUrl}/{patientId}");

        // Assert
        response.StatusCode.ShouldBe(HttpStatusCode.NoContent);

        // Verify deleted (soft delete returns 404)
        var getResponse = await Client.GetAsync($"{BaseUrl}/{patientId}");
        getResponse.StatusCode.ShouldBe(HttpStatusCode.NotFound);
    }

    #endregion
}
```

### Authorization Tests

```csharp
public class PatientAuthorizationTests : ClinicHttpApiTestBase
{
    [Fact]
    public async Task Create_WithoutPermission_Returns403()
    {
        // Arrange
        await AuthenticateAsAsync("user-without-create-permission");
        var input = new CreatePatientDto { Name = "Test" };

        // Act
        var response = await Client.PostAsJsonAsync("/api/app/patients", input);

        // Assert
        response.StatusCode.ShouldBe(HttpStatusCode.Forbidden);
    }

    [Fact]
    public async Task Create_WithPermission_Returns201()
    {
        // Arrange
        await AuthenticateAsAsync("admin", new[] { "Clinic.Patients.Create" });
        var input = new CreatePatientDto
        {
            Name = "Test",
            Email = "unique@test.com"
        };

        // Act
        var response = await Client.PostAsJsonAsync("/api/app/patients", input);

        // Assert
        response.StatusCode.ShouldBe(HttpStatusCode.Created);
    }

    [Fact]
    public async Task GetList_Unauthenticated_Returns401()
    {
        // Arrange - clear any auth headers
        Client.DefaultRequestHeaders.Authorization = null;

        // Act
        var response = await Client.GetAsync("/api/app/patients");

        // Assert
        response.StatusCode.ShouldBe(HttpStatusCode.Unauthorized);
    }

    [Theory]
    [InlineData("Clinic.Patients.Read", HttpStatusCode.OK)]
    [InlineData("Clinic.Doctors.Read", HttpStatusCode.Forbidden)]
    public async Task GetList_PermissionVariants_ReturnsExpectedStatus(
        string permission,
        HttpStatusCode expected)
    {
        // Arrange
        await AuthenticateAsAsync("user", new[] { permission });

        // Act
        var response = await Client.GetAsync("/api/app/patients");

        // Assert
        response.StatusCode.ShouldBe(expected);
    }
}
```

### Response Format Tests

```csharp
public class ApiResponseTests : ClinicHttpApiTestBase
{
    [Fact]
    public async Task ValidationError_HasCorrectFormat()
    {
        // Arrange
        var input = new CreatePatientDto(); // All required fields missing

        // Act
        var response = await Client.PostAsJsonAsync("/api/app/patients", input);
        var content = await response.Content.ReadAsStringAsync();

        // Assert
        response.StatusCode.ShouldBe(HttpStatusCode.BadRequest);

        var error = JsonSerializer.Deserialize<RemoteServiceErrorResponse>(content);
        error.Error.ShouldNotBeNull();
        error.Error.Code.ShouldBe("Volo.Abp.Validation:ValidationError");
        error.Error.ValidationErrors.ShouldNotBeEmpty();
    }

    [Fact]
    public async Task NotFound_HasCorrectFormat()
    {
        // Act
        var response = await Client.GetAsync($"/api/app/patients/{Guid.NewGuid()}");

        // Assert
        response.StatusCode.ShouldBe(HttpStatusCode.NotFound);

        var error = await response.Content
            .ReadFromJsonAsync<RemoteServiceErrorResponse>();
        error.Error.Code.ShouldContain("EntityNotFound");
    }

    [Fact]
    public async Task PagedResult_HasCorrectStructure()
    {
        // Act
        var response = await Client.GetAsync("/api/app/patients");
        var content = await response.Content.ReadAsStringAsync();

        // Assert
        using var doc = JsonDocument.Parse(content);
        doc.RootElement.TryGetProperty("totalCount", out _).ShouldBeTrue();
        doc.RootElement.TryGetProperty("items", out var items).ShouldBeTrue();
        items.ValueKind.ShouldBe(JsonValueKind.Array);
    }
}
```

### File Upload Tests

```csharp
public class FileUploadTests : ClinicHttpApiTestBase
{
    [Fact]
    public async Task UploadProfileImage_ValidFile_Returns200()
    {
        // Arrange
        var patientId = TestData.PatientId;
        var content = new MultipartFormDataContent();
        var fileContent = new ByteArrayContent(TestData.SampleImageBytes);
        fileContent.Headers.ContentType = new MediaTypeHeaderValue("image/jpeg");
        content.Add(fileContent, "file", "profile.jpg");

        // Act
        var response = await Client.PostAsync(
            $"/api/app/patients/{patientId}/profile-image",
            content);

        // Assert
        response.StatusCode.ShouldBe(HttpStatusCode.OK);
    }

    [Fact]
    public async Task UploadProfileImage_OversizedFile_Returns400()
    {
        // Arrange
        var patientId = TestData.PatientId;
        var content = new MultipartFormDataContent();
        var largeFile = new byte[10 * 1024 * 1024]; // 10MB
        content.Add(new ByteArrayContent(largeFile), "file", "large.jpg");

        // Act
        var response = await Client.PostAsync(
            $"/api/app/patients/{patientId}/profile-image",
            content);

        // Assert
        response.StatusCode.ShouldBe(HttpStatusCode.BadRequest);
    }
}
```

## Test Data Management

```csharp
public static class TestData
{
    public static readonly Guid PatientId = Guid.Parse("...");
    public static readonly Guid DeletablePatientId = Guid.Parse("...");
    public static readonly string ExistingEmail = "existing@example.com";

    public static readonly byte[] SampleImageBytes = Convert.FromBase64String("...");
}

public class TestDataSeeder : IDataSeedContributor
{
    public async Task SeedAsync(DataSeedContext context)
    {
        var patientRepository = context.ServiceProvider
            .GetRequiredService<IPatientRepository>();

        await patientRepository.InsertAsync(new Patient(
            TestData.PatientId,
            "Test Patient",
            TestData.ExistingEmail,
            new DateTime(1990, 1, 1)
        ));

        await patientRepository.InsertAsync(new Patient(
            TestData.DeletablePatientId,
            "Deletable Patient",
            "deletable@example.com",
            new DateTime(1990, 1, 1)
        ));
    }
}
```

## Quick Reference

| Test Type | HTTP Code | Pattern |
|-----------|-----------|---------|
| Success (GET) | 200 | `response.StatusCode.ShouldBe(HttpStatusCode.OK)` |
| Created | 201 | Verify Location header + body |
| No Content | 204 | For successful DELETE |
| Bad Request | 400 | Check ValidationErrors |
| Unauthorized | 401 | Missing/invalid token |
| Forbidden | 403 | Missing permission |
| Not Found | 404 | Invalid ID |
| Conflict | 409 | Duplicate/business rule violation |

## Related Skills

- `xunit-testing-patterns` - Base testing patterns
- `test-data-generation` - Test data setup
- `abp-framework-patterns` - ABP application patterns
