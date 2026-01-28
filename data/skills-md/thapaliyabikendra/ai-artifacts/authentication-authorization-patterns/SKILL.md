---
name: authentication-authorization-patterns
description: Master authentication and authorization patterns including OAuth 2.0, OpenID Connect, JWT tokens, refresh tokens, role-based access control (RBAC), claims-based authorization, and secure token storage for .NET applications with OpenIddict and ABP Framework.
---

# Authentication & Authorization Patterns

Master secure authentication and authorization for healthcare applications using OpenIddict, OAuth 2.0, and ABP Framework.

## When to Use This Skill

- Implementing user authentication
- Setting up OAuth 2.0 / OpenID Connect
- Managing JWT tokens and refresh tokens
- Implementing role-based access control (RBAC)
- Securing API endpoints
- Handling user permissions
- Multi-factor authentication (MFA)
- Single Sign-On (SSO)

## Core Concepts

### 1. Authentication vs Authorization

**Authentication**: "Who are you?" - Verifying identity
**Authorization**: "What can you do?" - Verifying permissions

```csharp
// Authentication: User proves identity
[HttpPost("login")]
public async Task<TokenResponse> Login(LoginRequest request)
{
    // Verify credentials
    var user = await _userManager.FindByEmailAsync(request.Email);
    if (user == null || !await _userManager.CheckPasswordAsync(user, request.Password))
    {
        throw new UnauthorizedException("Invalid credentials");
    }

    // User authenticated, generate token
    return await GenerateTokenAsync(user);
}

// Authorization: Check if user has permission
[Authorize(ClinicPermissions.Patients.Create)] // Authorization
public async Task<PatientDto> CreatePatient(CreatePatientDto input)
{
    // User must be authenticated AND have permission
}
```

### 2. OAuth 2.0 with OpenIddict

**Configure OpenIddict in ABP:**
```csharp
// HttpApi.Host/ClinicHttpApiHostModule.cs
public override void PreConfigureServices(ServiceConfigurationContext context)
{
    var hostingEnvironment = context.Services.GetHostingEnvironment();
    var configuration = context.Services.GetConfiguration();

    PreConfigure<OpenIddictBuilder>(builder =>
    {
        builder.AddValidation(options =>
        {
            options.AddAudiences("Clinic");
            options.UseLocalServer();
            options.UseAspNetCore();
        });
    });

    if (!hostingEnvironment.IsDevelopment())
    {
        PreConfigure<AbpOpenIddictAspNetCoreOptions>(options =>
        {
            options.AddDevelopmentEncryptionAndSigningCertificate = false;
        });

        PreConfigure<OpenIddictServerBuilder>(builder =>
        {
            builder.AddSigningCertificate(
                GetSigningCertificate(hostingEnvironment, configuration));
            builder.AddEncryptionCertificate(
                GetEncryptionCertificate(hostingEnvironment, configuration));
        });
    }
}
```

**OAuth 2.0 Flows:**

**1. Authorization Code Flow (Most Secure):**
```csharp
// For web applications and mobile apps
// Client redirects to authorization endpoint
// GET /connect/authorize?
//   client_id=clinic-web&
//   redirect_uri=https://clinic.com/callback&
//   response_type=code&
//   scope=openid profile email&
//   state=random_state&
//   code_challenge=hash&
//   code_challenge_method=S256

// After user login, redirected with code
// POST /connect/token
// grant_type=authorization_code&
// code=ABC123&
// redirect_uri=https://clinic.com/callback&
// client_id=clinic-web&
// code_verifier=original_value
```

**2. Client Credentials Flow (Service-to-Service):**
```csharp
// For backend services, no user involved
public class ExternalApiClient
{
    private readonly HttpClient _httpClient;
    private string _accessToken;

    public async Task<string> GetAccessTokenAsync()
    {
        var request = new HttpRequestMessage(HttpMethod.Post, "/connect/token");
        request.Content = new FormUrlEncodedContent(new[]
        {
            new KeyValuePair<string, string>("grant_type", "client_credentials"),
            new KeyValuePair<string, string>("client_id", "reporting-service"),
            new KeyValuePair<string, string>("client_secret", "secret"),
            new KeyValuePair<string, string>("scope", "clinic-api")
        });

        var response = await _httpClient.SendAsync(request);
        var content = await response.Content.ReadFromJsonAsync<TokenResponse>();

        return content.AccessToken;
    }
}
```

**3. Resource Owner Password Credentials (Legacy/Internal):**
```csharp
// Only for trusted first-party applications
// POST /connect/token
// grant_type=password&
// username=user@example.com&
// password=secretPassword&
// client_id=mobile-app&
// scope=openid profile email offline_access

[HttpPost("token")]
public async Task<IActionResult> Token([FromForm] TokenRequest request)
{
    if (request.GrantType == "password")
    {
        var user = await _userManager.FindByNameAsync(request.Username);
        if (user == null || !await _userManager.CheckPasswordAsync(user, request.Password))
        {
            return BadRequest(new { error = "invalid_grant" });
        }

        return Ok(await CreateTokenResponseAsync(user, request.Scope));
    }

    return BadRequest(new { error = "unsupported_grant_type" });
}
```

### 3. JWT Token Structure

**JWT Anatomy:**
```csharp
// Header (algorithm and token type)
{
  "alg": "RS256",
  "typ": "JWT",
  "kid": "key-id"
}

// Payload (claims)
{
  "sub": "user-id-123",                    // Subject (user ID)
  "email": "doctor@clinic.com",
  "name": "Dr. John Smith",
  "role": ["Doctor", "Admin"],             // Roles
  "permission": [                          // Permissions
    "Patients.View",
    "Appointments.Create"
  ],
  "iat": 1234567890,                       // Issued at
  "exp": 1234571490,                       // Expiration (1 hour)
  "iss": "https://auth.clinic.com",        // Issuer
  "aud": "clinic-api"                      // Audience
}

// Signature
RSASHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  private_key
)
```

**Creating JWT with Custom Claims:**
```csharp
public async Task<string> GenerateJwtTokenAsync(User user)
{
    var claims = new List<Claim>
    {
        new Claim(JwtRegisteredClaimNames.Sub, user.Id.ToString()),
        new Claim(JwtRegisteredClaimNames.Email, user.Email),
        new Claim(JwtRegisteredClaimNames.Name, user.Name),
        new Claim("tenant_id", user.TenantId?.ToString() ?? ""),
    };

    // Add roles
    var roles = await _userManager.GetRolesAsync(user);
    claims.AddRange(roles.Select(role => new Claim(ClaimTypes.Role, role)));

    // Add permissions
    var permissions = await _permissionManager.GetAllForUserAsync(user.Id);
    claims.AddRange(permissions.Select(p => new Claim("permission", p)));

    var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_jwtSettings.SecretKey));
    var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

    var token = new JwtSecurityToken(
        issuer: _jwtSettings.Issuer,
        audience: _jwtSettings.Audience,
        claims: claims,
        expires: DateTime.UtcNow.AddHours(1),
        signingCredentials: creds
    );

    return new JwtSecurityTokenHandler().WriteToken(token);
}
```

**Validating JWT:**
```csharp
// Startup configuration
public void ConfigureServices(IServiceCollection services)
{
    services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
        .AddJwtBearer(options =>
        {
            options.Authority = "https://auth.clinic.com";
            options.Audience = "clinic-api";
            options.RequireHttpsMetadata = true;

            options.TokenValidationParameters = new TokenValidationParameters
            {
                ValidateIssuer = true,
                ValidateAudience = true,
                ValidateLifetime = true,
                ValidateIssuerSigningKey = true,
                ClockSkew = TimeSpan.FromMinutes(5) // Allow 5 min clock skew
            };

            options.Events = new JwtBearerEvents
            {
                OnAuthenticationFailed = context =>
                {
                    if (context.Exception is SecurityTokenExpiredException)
                    {
                        context.Response.Headers.Add("Token-Expired", "true");
                    }
                    return Task.CompletedTask;
                }
            };
        });
}
```

### 4. Refresh Tokens

**Token Pair Pattern:**
```csharp
public class TokenResponse
{
    public string AccessToken { get; set; }       // Short-lived (1 hour)
    public string RefreshToken { get; set; }      // Long-lived (30 days)
    public int ExpiresIn { get; set; }            // 3600 seconds
    public string TokenType { get; set; } = "Bearer";
}

public async Task<TokenResponse> GenerateTokensAsync(User user)
{
    var accessToken = await GenerateAccessTokenAsync(user);
    var refreshToken = GenerateRefreshToken();

    // Store refresh token in database
    await _refreshTokenRepository.InsertAsync(new RefreshToken
    {
        Token = refreshToken,
        UserId = user.Id,
        ExpiresAt = DateTime.UtcNow.AddDays(30),
        CreatedAt = DateTime.UtcNow
    });

    return new TokenResponse
    {
        AccessToken = accessToken,
        RefreshToken = refreshToken,
        ExpiresIn = 3600
    };
}

private string GenerateRefreshToken()
{
    var randomBytes = new byte[32];
    using var rng = RandomNumberGenerator.Create();
    rng.GetBytes(randomBytes);
    return Convert.ToBase64String(randomBytes);
}
```

**Refresh Token Endpoint:**
```csharp
[HttpPost("refresh")]
public async Task<ActionResult<TokenResponse>> RefreshToken(RefreshTokenRequest request)
{
    // Validate refresh token
    var refreshToken = await _refreshTokenRepository
        .FirstOrDefaultAsync(rt => rt.Token == request.RefreshToken);

    if (refreshToken == null || refreshToken.IsRevoked || refreshToken.IsExpired)
    {
        return Unauthorized(new { error = "invalid_grant" });
    }

    var user = await _userManager.FindByIdAsync(refreshToken.UserId.ToString());
    if (user == null)
    {
        return Unauthorized(new { error = "invalid_grant" });
    }

    // Revoke old refresh token (rotation)
    refreshToken.IsRevoked = true;
    await _refreshTokenRepository.UpdateAsync(refreshToken);

    // Generate new token pair
    return await GenerateTokensAsync(user);
}
```

**Token Rotation (Security Best Practice):**
```csharp
// Always issue new refresh token when refreshing
// Revoke old refresh token immediately
// Detect token reuse (possible attack)
public async Task<TokenResponse> RefreshTokenAsync(string refreshToken)
{
    var token = await _refreshTokenRepository
        .FirstOrDefaultAsync(rt => rt.Token == refreshToken);

    if (token == null)
    {
        throw new SecurityException("Invalid refresh token");
    }

    if (token.IsRevoked)
    {
        // Token reuse detected! Possible attack
        // Revoke all refresh tokens for this user
        await RevokeAllUserTokensAsync(token.UserId);
        throw new SecurityException("Token reuse detected");
    }

    // Mark as revoked and issue new token
    token.IsRevoked = true;
    await _refreshTokenRepository.UpdateAsync(token);

    var user = await _userManager.FindByIdAsync(token.UserId.ToString());
    return await GenerateTokensAsync(user);
}
```

### 5. Role-Based Access Control (RBAC)

**Define Roles:**
```csharp
public static class ClinicRoles
{
    public const string Admin = "Admin";
    public const string Doctor = "Doctor";
    public const string Receptionist = "Receptionist";
    public const string Patient = "Patient";
}

// Seed roles
public async Task SeedRolesAsync()
{
    var roles = new[] { "Admin", "Doctor", "Receptionist", "Patient" };

    foreach (var roleName in roles)
    {
        if (!await _roleManager.RoleExistsAsync(roleName))
        {
            await _roleManager.CreateAsync(new IdentityRole(roleName));
        }
    }
}
```

**Role-Based Authorization:**
```csharp
// Single role
[Authorize(Roles = ClinicRoles.Doctor)]
public async Task<List<AppointmentDto>> GetMyAppointments()
{
    var doctorId = CurrentUser.Id;
    // Return doctor's appointments
}

// Multiple roles (OR)
[Authorize(Roles = "Admin,Doctor")]
public async Task<PatientDto> GetPatient(Guid id)
{
    // Accessible by Admin OR Doctor
}

// Combine multiple Authorize attributes (AND)
[Authorize(Roles = ClinicRoles.Doctor)]
[Authorize(Policy = "RequireEmailVerified")]
public async Task PrescribeMedication(PrescriptionDto input)
{
    // Must be Doctor AND have verified email
}
```

**Policy-Based Authorization:**
```csharp
// Define policies
public void ConfigureServices(IServiceCollection services)
{
    services.AddAuthorization(options =>
    {
        // Age requirement
        options.AddPolicy("RequireAdult", policy =>
            policy.Requirements.Add(new MinimumAgeRequirement(18)));

        // Role + claim requirement
        options.AddPolicy("DoctorWithSpecialization", policy =>
            policy.RequireRole("Doctor")
                  .RequireClaim("specialization"));

        // Custom requirement
        options.AddPolicy("CanAccessPatientRecord", policy =>
            policy.Requirements.Add(new PatientAccessRequirement()));
    });
}

// Custom requirement
public class PatientAccessRequirement : IAuthorizationRequirement { }

public class PatientAccessHandler : AuthorizationHandler<PatientAccessRequirement>
{
    private readonly IHttpContextAccessor _httpContextAccessor;

    protected override async Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        PatientAccessRequirement requirement)
    {
        var user = context.User;
        var httpContext = _httpContextAccessor.HttpContext;

        // Get patient ID from route
        var patientId = httpContext.GetRouteValue("patientId")?.ToString();

        // Admin can access any patient
        if (user.IsInRole("Admin"))
        {
            context.Succeed(requirement);
            return;
        }

        // Doctor can access their patients
        if (user.IsInRole("Doctor"))
        {
            var doctorId = user.FindFirst(ClaimTypes.NameIdentifier)?.Value;
            // Check if patient is assigned to this doctor
            // ...
        }

        // Patient can access own record
        var userId = user.FindFirst(ClaimTypes.NameIdentifier)?.Value;
        if (userId == patientId)
        {
            context.Succeed(requirement);
        }
    }
}
```

### 6. Claims-Based Authorization

**Working with Claims:**
```csharp
// Add claims to user
public async Task AddClaimsToUserAsync(User user, List<Claim> claims)
{
    await _userManager.AddClaimsAsync(user, claims);
}

// Authorize by claim
[Authorize(Policy = "RequireSpecialization")]
public async Task PerformSurgery()
{
    // Requires claim: specialization = surgery
}

// Define claim policy
services.AddAuthorization(options =>
{
    options.AddPolicy("RequireSpecialization", policy =>
        policy.RequireClaim("specialization", "cardiology", "surgery", "pediatrics"));
});

// Check claims in code
public async Task<bool> CanPrescribeMedicationAsync()
{
    var user = await _userManager.GetUserAsync(User);
    var claims = await _userManager.GetClaimsAsync(user);

    return claims.Any(c => c.Type == "can_prescribe" && c.Value == "true");
}
```

### 7. Multi-Factor Authentication (MFA)

**Enable MFA:**
```csharp
public async Task<MfaSetupDto> SetupMfaAsync()
{
    var user = await _userManager.GetUserAsync(User);

    // Generate secret key
    var key = KeyGeneration.GenerateRandomKey(20);
    var base32Key = Base32Encoding.ToString(key);

    // Store in user profile
    user.MfaSecret = base32Key;
    await _userManager.UpdateAsync(user);

    // Generate QR code for authenticator app
    var qrCodeUrl = $"otpauth://totp/Clinic:{user.Email}?secret={base32Key}&issuer=Clinic";

    return new MfaSetupDto
    {
        Secret = base32Key,
        QrCodeUrl = qrCodeUrl
    };
}

public async Task<bool> VerifyMfaCodeAsync(string code)
{
    var user = await _userManager.GetUserAsync(User);

    var twoFactorCode = new TwoFactorAuthenticator();
    var isValid = twoFactorCode.ValidateTwoFactorPIN(user.MfaSecret, code);

    if (isValid)
    {
        user.IsMfaEnabled = true;
        await _userManager.UpdateAsync(user);
    }

    return isValid;
}
```

**MFA Login Flow:**
```csharp
[HttpPost("login")]
public async Task<ActionResult<LoginResponse>> Login(LoginRequest request)
{
    var user = await _userManager.FindByEmailAsync(request.Email);
    if (user == null || !await _userManager.CheckPasswordAsync(user, request.Password))
    {
        return Unauthorized();
    }

    // Check if MFA is enabled
    if (user.IsMfaEnabled)
    {
        // Generate temporary token
        var tempToken = GenerateTempToken(user.Id);

        return Ok(new LoginResponse
        {
            RequiresMfa = true,
            TempToken = tempToken
        });
    }

    // No MFA, generate full tokens
    return Ok(await GenerateTokensAsync(user));
}

[HttpPost("mfa/verify")]
public async Task<ActionResult<TokenResponse>> VerifyMfa(MfaVerifyRequest request)
{
    var userId = ValidateTempToken(request.TempToken);
    var user = await _userManager.FindByIdAsync(userId.ToString());

    var twoFactorCode = new TwoFactorAuthenticator();
    var isValid = twoFactorCode.ValidateTwoFactorPIN(user.MfaSecret, request.Code);

    if (!isValid)
    {
        return Unauthorized(new { error = "invalid_code" });
    }

    return Ok(await GenerateTokensAsync(user));
}
```

## Security Best Practices

1. **Always use HTTPS** in production
2. **Store passwords hashed** (BCrypt, Argon2)
3. **Use refresh token rotation** to prevent replay attacks
4. **Short-lived access tokens** (15-60 minutes)
5. **Long-lived refresh tokens** (7-30 days)
6. **Validate token signature** on every request
7. **Check token expiration** with clock skew tolerance
8. **Revoke tokens** on logout and security events
9. **Use PKCE** for public clients (mobile/SPA)
10. **Rate limit** authentication endpoints

## Common Attack Vectors

### Token Theft Prevention
```csharp
// Store refresh tokens securely
// - HttpOnly cookies (web)
// - Secure storage (mobile)
// - Never in localStorage

// Use CSRF protection for cookie-based auth
services.AddAntiforgery(options =>
{
    options.HeaderName = "X-CSRF-TOKEN";
});
```

### Brute Force Prevention
```csharp
// Rate limit login attempts
public class RateLimitingMiddleware
{
    public async Task InvokeAsync(HttpContext context)
    {
        var ip = context.Connection.RemoteIpAddress;
        var key = $"login_attempts:{ip}";

        var attempts = await _cache.GetOrCreateAsync(key, async entry =>
        {
            entry.AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(15);
            return 0;
        });

        if (attempts >= 5)
        {
            context.Response.StatusCode = 429; // Too Many Requests
            await context.Response.WriteAsync("Too many login attempts");
            return;
        }

        await _next(context);

        if (context.Response.StatusCode == 401)
        {
            await _cache.SetAsync(key, attempts + 1);
        }
    }
}
```

## Resource Access Control Patterns

```csharp
// Pattern: Check if user owns resource
public async Task<PatientDto> GetPatient(Guid id)
{
    var patient = await _patientRepository.GetAsync(id);

    // Patient can only view own record
    if (CurrentUser.IsInRole("Patient") && patient.UserId != CurrentUser.Id)
    {
        throw new AuthorizationException("Access denied");
    }

    // Doctor can only view assigned patients
    if (CurrentUser.IsInRole("Doctor"))
    {
        var hasAccess = await _appointmentRepository.AnyAsync(a =>
            a.PatientId == id && a.DoctorId == CurrentUser.Id);

        if (!hasAccess)
        {
            throw new AuthorizationException("Access denied");
        }
    }

    return ObjectMapper.Map<Patient, PatientDto>(patient);
}
```

## Resources

- **OAuth 2.0 RFC**: https://datatracker.ietf.org/doc/html/rfc6749
- **OpenID Connect**: https://openid.net/connect/
- **JWT.io**: https://jwt.io/
- **OWASP Authentication Cheat Sheet**: https://cheatsheetseries.owasp.org/
