---
name: dotnet-azure-keyvault
description: "Azure Key Vault integration with Managed Identity for .NET applications. Use when: (1) Implementing Azure Key Vault as configuration source, (2) Setting up Managed Identity authentication with DefaultAzureCredential, (3) Creating AddAzureKeyVault extension method in Infrastructure, (4) Configuring Key Vault secrets and naming conventions, (5) Questions about local development authentication, (6) Implementing custom KeyVaultSecretManager, or (7) Troubleshooting Key Vault access and permissions."
---

# Azure Key Vault Integration

## Overview

Azure Key Vault provides secure storage and management of secrets, keys, and certificates. Integration with .NET applications should use Managed Identity for authentication and follow the extension method pattern for clean configuration.

## Extension Method Pattern

Create an extension method in `Infrastructure/Extensions/ExtensionKeyVault.cs`:

```csharp
using Azure.Identity;
using Azure.Security.KeyVault.Secrets;
using Microsoft.Extensions.Configuration;

namespace Infrastructure.Extensions
{
    /// <summary>
    /// Extension class for configuring Azure Key Vault integration.
    /// </summary>
    public static class ExtensionKeyVault
    {
        /// <summary>
        /// Adds Azure Key Vault as a configuration source using Managed Identity.
        /// </summary>
        /// <param name="builder">The configuration builder.</param>
        /// <param name="configuration">The current configuration to read Key Vault settings.</param>
        /// <returns>The updated configuration builder.</returns>
        public static IConfigurationBuilder AddAzureKeyVault(
            this IConfigurationBuilder builder, 
            IConfiguration configuration)
        {
            var clientId = Environment.GetEnvironmentVariable("AKS_CLIENT_ID") 
                ?? configuration["AzureKeyVault:AksAgentPoolClientId"];
            var keyVaultName = Environment.GetEnvironmentVariable("KEY_VAULT_NAME") 
                ?? configuration["AzureKeyVault:KeyVaultName"];
            var azureKeyVaultUri = string.Format(
                configuration["AzureKeyVault:Uri"]!, 
                keyVaultName);
            
            if (string.IsNullOrEmpty(azureKeyVaultUri))
            {
                throw new InvalidOperationException(
                    "Azure Key Vault URI is not configured");
            }

            DefaultAzureCredentialOptions tokenOptions = new()
            {
                ManagedIdentityClientId = clientId
            };

            SecretClient client = new(
                new Uri(azureKeyVaultUri),
                new DefaultAzureCredential(tokenOptions)
            );

            builder.AddAzureKeyVault(client, new KeyVaultSecretManager());

            return builder;
        }
    }
}
```

## Program.cs Configuration

Configure Azure Key Vault in `Program.cs` before building the configuration:

```csharp
var builder = WebApplication.CreateBuilder(args);

// Add Azure Key Vault to configuration
builder.Configuration.AddAzureKeyVault(builder.Configuration);

// Continue with service configuration...
```

## Required NuGet Packages

- **Azure.Extensions.AspNetCore.Configuration.Secrets**
- **Azure.Identity**
- **Azure.Security.KeyVault.Secrets**

## Configuration Settings (appsettings.json)

```json
{
  "AzureKeyVault": {
    "KeyVaultName": "your-keyvault-name",
    "Uri": "https://{0}.vault.azure.net/",
    "AksAgentPoolClientId": "your-managed-identity-client-id"
  }
}
```

## Environment Variables

These environment variables can override configuration settings:

- **AKS_CLIENT_ID**: The client ID of the Managed Identity (User-Assigned)
- **KEY_VAULT_NAME**: The name of the Azure Key Vault

## Authentication Methods

### Managed Identity (Recommended for Production)

Use Managed Identity when deployed to Azure services (AKS, App Service, Functions):

```csharp
DefaultAzureCredentialOptions tokenOptions = new()
{
    ManagedIdentityClientId = clientId
};

var credential = new DefaultAzureCredential(tokenOptions);
```

### Local Development

For local development, `DefaultAzureCredential` will automatically use:
1. Environment variables
2. Visual Studio authentication
3. Azure CLI authentication
4. Azure PowerShell authentication

Ensure you're logged in via Azure CLI or Visual Studio.

## Secret Naming Convention

Azure Key Vault secret names:
- Use hyphens instead of colons: `ConnectionStrings--DefaultConnection`
- .NET automatically converts hyphens to colons when reading configuration


## Best Practices

- Use Managed Identity for authentication in production environments.
- Never hardcode secrets or credentials in application code.
- Use environment-specific Key Vaults (dev, staging, production).
- Grant least-privilege access to Key Vault (only "Get" and "List" permissions for secrets).
- Monitor Key Vault access logs for security auditing.
- Cache secrets appropriately to minimize Key Vault calls.
- Use Key Vault references in Azure App Service configuration when possible.
