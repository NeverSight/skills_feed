---
name: api-response-patterns
description: "API response wrapper patterns for consistent, predictable REST APIs in ABP Framework. Use when: (1) designing uniform API response contracts, (2) implementing success/error response wrappers, (3) handling pagination and metadata, (4) standardizing error responses."
layer: 2
tech_stack: [dotnet, csharp, abp]
topics: [response-wrapper, error-response, pagination, metadata, http-status]
depends_on: [api-design-principles]
complements: [abp-framework-patterns]
keywords: [ApiResponse, PagedResultDto, ErrorResponse, StatusCode, ValidationError]
---

# API Response Patterns

Master API response wrapper patterns for building consistent, predictable REST APIs that clients love.

## When to Use This Skill

- Designing uniform API response contracts
- Implementing success/error response wrappers
- Standardizing error response formats
- Adding metadata to API responses (pagination, timing, version)
- Building APIs consumed by multiple client types (web, mobile, third-party)

## Why Response Wrappers?

| Benefit | Description |
|---------|-------------|
| **Consistency** | All endpoints return same structure |
| **Predictability** | Clients know what to expect |
| **Metadata** | Include timing, pagination, version info |
| **Error Handling** | Uniform error format across all endpoints |
| **Debugging** | Include correlation IDs for tracing |

## Response Wrapper Patterns

### 1. Basic ResponseModel

```csharp
// Application.Contracts/Models/ResponseModel.cs
public class ResponseModel<T>
{
    public bool IsSuccess { get; set; }
    public T Data { get; set; }
    public string Message { get; set; }
    public List<string> Errors { get; set; } = new();

    protected ResponseModel() { }

    protected ResponseModel(bool isSuccess, T data, string message, List<string> errors)
    {
        IsSuccess = isSuccess;
        Data = data;
        Message = message;
        Errors = errors ?? new List<string>();
    }

    public static ResponseModel<T> Success(T data, string message = null)
        => new(true, data, message, null);

    public static ResponseModel<T> Failure(string message)
        => new(false, default, message, new List<string> { message });

    public static ResponseModel<T> Failure(List<string> errors)
        => new(false, default, errors.FirstOrDefault(), errors);
}

// Non-generic version for operations without return data
public class ResponseModel : ResponseModel<object>
{
    public static ResponseModel Success(string message = null)
        => new() { IsSuccess = true, Message = message };

    public new static ResponseModel Failure(string message)
        => new() { IsSuccess = false, Message = message, Errors = new List<string> { message } };
}
```

### 2. Extended ApiResponse with Metadata

```csharp
// Application.Contracts/Models/ApiResponse.cs
public class ApiResponse<T>
{
    public bool Success { get; set; }
    public T Data { get; set; }
    public string Message { get; set; }
    public ApiResponseMeta Meta { get; set; }
    public List<ApiError> Errors { get; set; } = new();

    public static ApiResponse<T> Ok(T data, string message = null) => new()
    {
        Success = true,
        Data = data,
        Message = message,
        Meta = new ApiResponseMeta()
    };

    public static ApiResponse<T> Fail(string message, string code = null) => new()
    {
        Success = false,
        Message = message,
        Errors = new List<ApiError>
        {
            new ApiError { Code = code ?? "ERROR", Message = message }
        },
        Meta = new ApiResponseMeta()
    };

    public static ApiResponse<T> Fail(List<ApiError> errors) => new()
    {
        Success = false,
        Message = errors.FirstOrDefault()?.Message,
        Errors = errors,
        Meta = new ApiResponseMeta()
    };
}

public class ApiResponseMeta
{
    public string Version { get; set; } = "1.0";
    public DateTime Timestamp { get; set; } = DateTime.UtcNow;
    public string RequestId { get; set; } = Guid.NewGuid().ToString("N")[..8];
    public long? ProcessingTimeMs { get; set; }
}

public class ApiError
{
    public string Code { get; set; }
    public string Message { get; set; }
    public string Field { get; set; }
    public object Details { get; set; }
}
```

### 3. Paginated Response

```csharp
// Application.Contracts/Models/PagedApiResponse.cs
public class PagedApiResponse<T> : ApiResponse<List<T>>
{
    public PaginationInfo Pagination { get; set; }

    public static PagedApiResponse<T> Ok(
        List<T> items,
        long totalCount,
        int pageNumber,
        int pageSize,
        string message = null) => new()
    {
        Success = true,
        Data = items,
        Message = message,
        Meta = new ApiResponseMeta(),
        Pagination = new PaginationInfo
        {
            TotalCount = totalCount,
            PageNumber = pageNumber,
            PageSize = pageSize,
            TotalPages = (int)Math.Ceiling((double)totalCount / pageSize),
            HasPreviousPage = pageNumber > 1,
            HasNextPage = pageNumber * pageSize < totalCount
        }
    };
}

public class PaginationInfo
{
    public long TotalCount { get; set; }
    public int PageNumber { get; set; }
    public int PageSize { get; set; }
    public int TotalPages { get; set; }
    public bool HasPreviousPage { get; set; }
    public bool HasNextPage { get; set; }
}
```

## Usage in AppServices

### 1. Basic CRUD Operations

```csharp
public class ProductAppService : ApplicationService, IProductAppService
{
    private readonly IRepository<Product, Guid> _productRepository;
    private readonly ILogger<ProductAppService> _logger;

    public async Task<ApiResponse<ProductDto>> GetAsync(Guid id)
    {
        var product = await _productRepository.FirstOrDefaultAsync(x => x.Id == id);

        if (product == null)
        {
            return ApiResponse<ProductDto>.Fail(
                "Product not found",
                "PRODUCT_NOT_FOUND");
        }

        var dto = ObjectMapper.Map<Product, ProductDto>(product);
        return ApiResponse<ProductDto>.Ok(dto);
    }

    public async Task<PagedApiResponse<ProductDto>> GetListAsync(
        PagedAndSortedResultRequestDto input,
        ProductFilter filter)
    {
        var queryable = await _productRepository.GetQueryableAsync();

        var query = queryable
            .WhereIf(!filter.Name.IsNullOrWhiteSpace(),
                x => x.Name.Contains(filter.Name))
            .WhereIf(filter.CategoryId.HasValue,
                x => x.CategoryId == filter.CategoryId);

        var totalCount = await AsyncExecuter.CountAsync(query);

        var products = await AsyncExecuter.ToListAsync(
            query
                .OrderBy(input.Sorting ?? "Name")
                .PageBy(input.SkipCount, input.MaxResultCount));

        var dtos = ObjectMapper.Map<List<Product>, List<ProductDto>>(products);

        return PagedApiResponse<ProductDto>.Ok(
            dtos,
            totalCount,
            pageNumber: (input.SkipCount / input.MaxResultCount) + 1,
            pageSize: input.MaxResultCount);
    }

    public async Task<ApiResponse<ProductDto>> CreateAsync(CreateProductDto input)
    {
        try
        {
            // Validate uniqueness
            var exists = await _productRepository.AnyAsync(
                x => x.ProductCode == input.ProductCode);

            if (exists)
            {
                return ApiResponse<ProductDto>.Fail(
                    $"Product code '{input.ProductCode}' already exists",
                    "DUPLICATE_PRODUCT_CODE");
            }

            var product = new Product(
                GuidGenerator.Create(),
                input.ProductCode,
                input.Name,
                input.Price);

            await _productRepository.InsertAsync(product);

            var dto = ObjectMapper.Map<Product, ProductDto>(product);
            return ApiResponse<ProductDto>.Ok(dto, "Product created successfully");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to create product");
            return ApiResponse<ProductDto>.Fail(ex.Message, "CREATE_FAILED");
        }
    }

    public async Task<ApiResponse<bool>> DeleteAsync(Guid id)
    {
        var product = await _productRepository.FirstOrDefaultAsync(x => x.Id == id);

        if (product == null)
        {
            return ApiResponse<bool>.Fail("Product not found", "NOT_FOUND");
        }

        await _productRepository.DeleteAsync(product);

        return ApiResponse<bool>.Ok(true, "Product deleted successfully");
    }
}
```

### 2. Bulk Operations

```csharp
public async Task<ApiResponse<BulkOperationResult>> BulkDeleteAsync(List<Guid> ids)
{
    var products = await _productRepository.GetListAsync(x => ids.Contains(x.Id));

    if (!products.Any())
    {
        return ApiResponse<BulkOperationResult>.Fail(
            "No products found",
            "NOT_FOUND");
    }

    await _productRepository.DeleteManyAsync(products);

    var result = new BulkOperationResult
    {
        RequestedCount = ids.Count,
        ProcessedCount = products.Count,
        SkippedCount = ids.Count - products.Count
    };

    return ApiResponse<BulkOperationResult>.Ok(
        result,
        $"Deleted {products.Count} of {ids.Count} products");
}

public class BulkOperationResult
{
    public int RequestedCount { get; set; }
    public int ProcessedCount { get; set; }
    public int SkippedCount { get; set; }
    public List<string> SkippedIds { get; set; } = new();
}
```

## Error Response Patterns

### 1. Validation Error Response

```csharp
public class ValidationErrorResponse
{
    public bool Success => false;
    public string Message => "Validation failed";
    public string Code => "VALIDATION_ERROR";
    public List<FieldError> Errors { get; set; } = new();

    public static ValidationErrorResponse Create(List<FieldError> errors) => new()
    {
        Errors = errors
    };
}

public class FieldError
{
    public string Field { get; set; }
    public string Message { get; set; }
    public object AttemptedValue { get; set; }

    public FieldError() { }

    public FieldError(string field, string message, object attemptedValue = null)
    {
        Field = field;
        Message = message;
        AttemptedValue = attemptedValue;
    }
}
```

### 2. Exception Filter for Consistent Errors

```csharp
public class ApiExceptionFilter : IExceptionFilter
{
    private readonly ILogger<ApiExceptionFilter> _logger;

    public ApiExceptionFilter(ILogger<ApiExceptionFilter> logger)
    {
        _logger = logger;
    }

    public void OnException(ExceptionContext context)
    {
        var response = context.Exception switch
        {
            EntityNotFoundException ex => CreateNotFoundResponse(ex),
            AbpValidationException ex => CreateValidationResponse(ex),
            BusinessException ex => CreateBusinessErrorResponse(ex),
            UnauthorizedAccessException => CreateUnauthorizedResponse(),
            _ => CreateInternalErrorResponse(context.Exception)
        };

        context.Result = new ObjectResult(response)
        {
            StatusCode = GetStatusCode(context.Exception)
        };

        context.ExceptionHandled = true;
    }

    private int GetStatusCode(Exception ex) => ex switch
    {
        EntityNotFoundException => 404,
        AbpValidationException => 400,
        BusinessException => 422,
        UnauthorizedAccessException => 401,
        _ => 500
    };

    private ApiResponse<object> CreateNotFoundResponse(EntityNotFoundException ex) =>
        ApiResponse<object>.Fail(ex.Message, "NOT_FOUND");

    private ApiResponse<object> CreateValidationResponse(AbpValidationException ex) =>
        ApiResponse<object>.Fail(
            ex.ValidationErrors.Select(e => new ApiError
            {
                Code = "VALIDATION_ERROR",
                Field = e.MemberNames.FirstOrDefault(),
                Message = e.ErrorMessage
            }).ToList());

    private ApiResponse<object> CreateBusinessErrorResponse(BusinessException ex) =>
        ApiResponse<object>.Fail(ex.Message, ex.Code ?? "BUSINESS_ERROR");

    private ApiResponse<object> CreateUnauthorizedResponse() =>
        ApiResponse<object>.Fail("Unauthorized access", "UNAUTHORIZED");

    private ApiResponse<object> CreateInternalErrorResponse(Exception ex)
    {
        _logger.LogError(ex, "Unhandled exception");
        return ApiResponse<object>.Fail("An internal error occurred", "INTERNAL_ERROR");
    }
}
```

## Controller Patterns

### 1. Standard Controller

```csharp
[ApiController]
[Route("api/products")]
public class ProductController : AbpController
{
    private readonly IProductAppService _productAppService;

    public ProductController(IProductAppService productAppService)
    {
        _productAppService = productAppService;
    }

    [HttpGet("{id}")]
    [ProducesResponseType(typeof(ApiResponse<ProductDto>), 200)]
    [ProducesResponseType(typeof(ApiResponse<object>), 404)]
    public async Task<IActionResult> GetAsync(Guid id)
    {
        var response = await _productAppService.GetAsync(id);

        if (!response.Success)
        {
            return NotFound(response);
        }

        return Ok(response);
    }

    [HttpGet]
    [ProducesResponseType(typeof(PagedApiResponse<ProductDto>), 200)]
    public async Task<IActionResult> GetListAsync(
        [FromQuery] PagedAndSortedResultRequestDto input,
        [FromQuery] ProductFilter filter)
    {
        var response = await _productAppService.GetListAsync(input, filter);
        return Ok(response);
    }

    [HttpPost]
    [ProducesResponseType(typeof(ApiResponse<ProductDto>), 201)]
    [ProducesResponseType(typeof(ApiResponse<object>), 400)]
    public async Task<IActionResult> CreateAsync([FromBody] CreateProductDto input)
    {
        var response = await _productAppService.CreateAsync(input);

        if (!response.Success)
        {
            return BadRequest(response);
        }

        return CreatedAtAction(
            nameof(GetAsync),
            new { id = response.Data.Id },
            response);
    }

    [HttpDelete("{id}")]
    [ProducesResponseType(typeof(ApiResponse<bool>), 200)]
    [ProducesResponseType(typeof(ApiResponse<object>), 404)]
    public async Task<IActionResult> DeleteAsync(Guid id)
    {
        var response = await _productAppService.DeleteAsync(id);

        if (!response.Success)
        {
            return NotFound(response);
        }

        return Ok(response);
    }
}
```

### 2. Response Helper Extension

```csharp
public static class ControllerExtensions
{
    public static IActionResult ToActionResult<T>(
        this ControllerBase controller,
        ApiResponse<T> response)
    {
        if (response.Success)
        {
            return controller.Ok(response);
        }

        var errorCode = response.Errors.FirstOrDefault()?.Code ?? "ERROR";

        return errorCode switch
        {
            "NOT_FOUND" => controller.NotFound(response),
            "VALIDATION_ERROR" => controller.BadRequest(response),
            "UNAUTHORIZED" => controller.Unauthorized(response),
            "FORBIDDEN" => controller.StatusCode(403, response),
            _ => controller.BadRequest(response)
        };
    }
}

// Usage
[HttpGet("{id}")]
public async Task<IActionResult> GetAsync(Guid id)
{
    var response = await _productAppService.GetAsync(id);
    return this.ToActionResult(response);
}
```

## OpenAPI Documentation

```csharp
// Swagger configuration
services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo { Title = "My API", Version = "v1" });

    // Add response examples
    c.OperationFilter<ApiResponseOperationFilter>();
});

public class ApiResponseOperationFilter : IOperationFilter
{
    public void Apply(OpenApiOperation operation, OperationFilterContext context)
    {
        // Add common error responses
        operation.Responses.TryAdd("400", new OpenApiResponse
        {
            Description = "Bad Request - Validation Error"
        });

        operation.Responses.TryAdd("401", new OpenApiResponse
        {
            Description = "Unauthorized"
        });

        operation.Responses.TryAdd("404", new OpenApiResponse
        {
            Description = "Not Found"
        });

        operation.Responses.TryAdd("500", new OpenApiResponse
        {
            Description = "Internal Server Error"
        });
    }
}
```

## Best Practices

1. **Use consistent response structure** - All endpoints should return the same wrapper
2. **Include error codes** - Machine-readable codes alongside human messages
3. **Add metadata** - Timestamps, request IDs for debugging
4. **Paginate lists** - Always include pagination info for collections
5. **Document with OpenAPI** - Generate accurate API documentation
6. **Handle all exceptions** - Use exception filters for consistency
7. **Use appropriate HTTP status codes** - Map response status to HTTP codes
8. **Include timing information** - Help clients understand performance
9. **Version your API** - Include version in responses and routes
10. **Log correlation IDs** - Make debugging distributed systems easier

## References

- [Error Code Standards](references/error-codes.md)
- [Pagination Patterns](references/pagination.md)
