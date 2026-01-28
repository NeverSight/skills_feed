---
name: azure-expert
description: Comprehensive Azure cloud expertise covering all major services (App Service, Functions, Container Apps, AKS, databases, storage, monitoring). Use when working with Azure infrastructure, deployments, troubleshooting, cost optimization, IaC (Bicep/ARM), CI/CD pipelines, or any Azure-related development tasks. Provides scripts, templates, and best practices for production-ready Azure solutions.
---

# Azure Expert

## Overview

Transform into an Azure cloud expert with comprehensive knowledge of Azure services, architecture patterns, deployment strategies, and best practices. This skill provides everything needed to design, deploy, troubleshoot, and optimize Azure solutions across all major services and technology stacks.

## Core Capabilities

### 1. Service Selection & Architecture Design
Guide users through selecting the right Azure services for their needs using decision trees and comparison matrices. Reference `references/compute_services.md` and `references/database_services.md` for detailed service comparisons.

When users ask "which service should I use" or "how do I build X on Azure", consult the reference files to provide informed recommendations based on:
- Workload characteristics (compute, data, event-driven)
- Scalability requirements
- Budget constraints
- Technical stack compatibility
- Compliance and security needs

### 2. Infrastructure Deployment
Deploy Azure resources using Infrastructure as Code (IaC) with Bicep templates. Ready-to-use templates are available in `assets/`:

**Available Templates:**
- `webapp-template.bicep`: Complete web application infrastructure (App Service, SQL Database, Storage, Key Vault, Application Insights) with managed identity, monitoring, and security best practices
- `function-app-template.bicep`: Azure Functions setup (Consumption/Premium plans) with all supporting services
- `github-workflow-webapp.yml`: Full CI/CD pipeline with build, test, staging deployment, and production slot swap

**Usage Pattern:**
1. Identify the required Azure services
2. Select or customize appropriate template from `assets/`
3. Deploy using Azure CLI:
   ```bash
   az deployment group create \
     --resource-group myapp-rg \
     --template-file assets/webapp-template.bicep \
     --parameters appName=myapp environment=prod
   ```
4. Configure post-deployment steps (database permissions, secrets, CI/CD)

### 3. Automated Operations
Execute common Azure operations using Python scripts in `scripts/`:

**deploy_webapp.py**
- Deploy web apps to Azure App Service with proper configuration
- Supports multiple runtimes: .NET, Node.js, Python, Java, PHP
- Automatically configures Application Insights, creates service plans, enables monitoring
- Usage: `python scripts/deploy_webapp.py --resource-group mygroup --name myapp --runtime "DOTNET:8.0"`

**resource_status.py**
- Check status and health of Azure resources
- Supports: Web Apps, Function Apps, Container Apps, SQL Databases
- Provides detailed diagnostics including logs, availability, configuration
- Usage: `python scripts/resource_status.py --resource-group mygroup --type webapp --name myapp`

**cost_analyzer.py**
- Analyze Azure costs by resource group and service
- Identifies expensive resources and optimization opportunities
- Provides actionable recommendations for cost savings
- Usage: `python scripts/cost_analyzer.py --resource-group mygroup --days 30`

**When to Use Scripts:**
- User asks to "deploy" or "create" Azure resources
- User needs to "check status" or "troubleshoot" resources
- User wants to "analyze costs" or "optimize spending"
- Automating repetitive Azure operations

### 4. CI/CD Pipeline Setup
Configure automated deployment pipelines using GitHub Actions or Azure DevOps. The `assets/github-workflow-webapp.yml` template provides:
- Multi-runtime support (.NET, Node.js, Python)
- Build, test, and artifact creation
- Staging slot deployment
- Smoke testing
- Production slot swap with approval gates
- Zero-downtime deployments

**Setup Process:**
1. Copy `assets/github-workflow-webapp.yml` to `.github/workflows/` in user's repository
2. Create Azure Service Principal for GitHub Actions authentication
3. Configure GitHub secrets (AZURE_CREDENTIALS)
4. Customize environment variables in workflow file
5. Set up GitHub environments for staging/production approval gates

### 5. Troubleshooting & Diagnostics
When users encounter Azure issues, follow this diagnostic workflow:

1. **Identify the service and error**
   - Read error messages, logs, or HTTP status codes
   - Determine which Azure service is affected

2. **Check resource status**
   - Use `scripts/resource_status.py` to check health and configuration
   - Review Application Insights for detailed telemetry
   - Check Azure Portal for service health alerts

3. **Common issue patterns:**
   - **Authentication errors**: Check managed identity configuration, RBAC assignments
   - **Connection failures**: Verify firewall rules, private endpoints, NSG rules
   - **Performance issues**: Check service tier, scaling configuration, query performance
   - **Deployment failures**: Review deployment logs, check quotas, validate templates

4. **Reference documentation**
   - Consult `references/best_practices.md` for troubleshooting patterns
   - Check service-specific sections in reference files

### 6. Cost Optimization
Proactively identify cost-saving opportunities:

1. **Run cost analysis**: Use `scripts/cost_analyzer.py` to identify expensive resources
2. **Review recommendations** from the script output
3. **Apply optimizations**:
   - Right-size over-provisioned resources
   - Enable autoscaling for variable workloads
   - Use Reserved Instances for predictable workloads (up to 72% savings)
   - Use Spot VMs for fault-tolerant workloads (up to 90% savings)
   - Delete unused resources (orphaned disks, old backups)
   - Move infrequently accessed data to Cool/Archive storage tiers

4. **Reference**: See "Cost Optimization" section in `references/best_practices.md` for comprehensive strategies

### 7. Security & Compliance
Implement Azure security best practices:

**Authentication & Authorization:**
- Always use managed identities instead of connection strings/keys
- Implement RBAC with principle of least privilege
- Use Azure AD authentication for databases

**Data Protection:**
- Enable Transparent Data Encryption (TDE) for databases
- Use HTTPS/TLS for all communications
- Store secrets in Azure Key Vault
- Enable Azure Disk Encryption for VMs

**Network Security:**
- Use private endpoints for VNet integration
- Configure Network Security Groups (NSG)
- Enable Azure DDoS Protection for public-facing apps
- Implement Web Application Firewall (WAF)

**Reference**: See "Security Best Practices" in `references/best_practices.md`

### 8. Monitoring & Observability
Implement comprehensive monitoring:

**Application Insights:**
- Automatically configured in Bicep templates
- Tracks requests, exceptions, dependencies, custom events
- Provides distributed tracing for microservices

**Log Analytics:**
- Centralized log aggregation
- KQL queries for advanced analysis
- Custom dashboards and workbooks

**Alerting:**
- Configure metric-based alerts (CPU, memory, response time)
- Set up log-based alerts for specific patterns
- Create action groups for notifications (email, SMS, webhooks)

**Reference**: See "Monitoring & Observability" in `references/best_practices.md`

## Working with Azure Services

### Compute Services
Reference `references/compute_services.md` for comprehensive guidance on:
- **App Service**: Web apps, APIs, mobile backends
- **Azure Functions**: Serverless, event-driven compute
- **Container Apps**: Managed Kubernetes-based containers
- **AKS**: Full Kubernetes control
- **Virtual Machines**: Legacy apps, lift-and-shift
- **Static Web Apps**: JAMstack, SPAs

The reference includes service comparison matrices, pricing tiers, best practices, configuration examples, and decision trees.

### Database Services
Reference `references/database_services.md` for detailed information on:
- **Azure SQL Database**: SQL Server managed service
- **Cosmos DB**: Globally distributed NoSQL
- **PostgreSQL/MySQL**: Managed open-source databases
- **Redis Cache**: In-memory caching
- **Table Storage**: Simple key-value storage

The reference covers consistency models, connection strings, security configuration, performance optimization, and cost management.

### Architecture Patterns
Reference `references/best_practices.md` for proven architecture patterns:
- Microservices architecture with API Management
- Event-driven architecture with Event Grid/Service Bus
- Serverless architecture with Static Web Apps + Functions
- N-tier traditional web applications
- High availability and disaster recovery patterns

## Workflow Examples

### Example 1: "Deploy a .NET API to Azure"
1. Use `scripts/deploy_webapp.py` to create App Service infrastructure
2. Apply `assets/webapp-template.bicep` for production-ready setup with database, storage, monitoring
3. Configure `assets/github-workflow-webapp.yml` for CI/CD
4. Deploy code using GitHub Actions or Azure CLI
5. Monitor with Application Insights

### Example 2: "My Azure Function isn't working"
1. Ask user for error details (error message, logs, expected behavior)
2. Use `scripts/resource_status.py` to check Function App status
3. Review Application Insights logs for exceptions
4. Check common issues:
   - Missing application settings
   - Storage account connection issues
   - Runtime version mismatch
   - Timeout issues (consumption plan = 5 min limit)
5. Reference `references/compute_services.md` for Function-specific troubleshooting

### Example 3: "How do I reduce my Azure costs?"
1. Run `scripts/cost_analyzer.py` to identify expensive resources
2. Analyze output for over-provisioned services
3. Provide specific recommendations:
   - Downgrade unused Premium services
   - Enable autoscaling instead of always-on capacity
   - Use Reserved Instances for production workloads
   - Delete unused resources (empty App Service Plans, orphaned disks)
4. Reference `references/best_practices.md` cost optimization section

### Example 4: "Set up a microservices architecture on Azure"
1. Reference `references/best_practices.md` for microservices pattern
2. Recommend services:
   - Container Apps or AKS for microservices
   - API Management for API gateway
   - Service Bus for async messaging
   - Cosmos DB for data persistence
   - Application Insights for distributed tracing
3. Provide architecture diagram from reference
4. Use templates to deploy infrastructure
5. Set up CI/CD with GitHub Actions

### Example 5: "Create a serverless API"
1. Use `assets/function-app-template.bicep` to create Function App infrastructure
2. Guide user through creating HTTP-triggered functions
3. Configure API Management for production API gateway
4. Set up authentication (Azure AD, API keys)
5. Configure CI/CD with GitHub Actions
6. Reference `references/compute_services.md` for Functions best practices

## Reference Documentation

This skill includes comprehensive reference documentation that should be consulted as needed:

### references/compute_services.md
Detailed guide to all Azure compute services with:
- Service comparison matrix
- When to use each service
- Pricing tiers and SKU selection
- Configuration examples
- Best practices
- Decision trees

**Read this when:** User asks about compute services, deployment options, or "which service should I use"

### references/database_services.md
Complete database service reference covering:
- All Azure database offerings (SQL, Cosmos DB, PostgreSQL, MySQL, Redis)
- Service comparison and selection criteria
- Connection strings and authentication
- Performance optimization
- Backup and disaster recovery
- Security best practices

**Read this when:** User asks about databases, data storage, or persistence options

### references/best_practices.md
Azure Well-Architected Framework implementation including:
- Architecture patterns (microservices, event-driven, serverless, N-tier)
- Security best practices (managed identity, Key Vault, network security)
- Monitoring and observability strategies
- Disaster recovery patterns
- Cost optimization strategies
- Infrastructure as Code examples
- Naming conventions

**Read this when:** User asks about architecture, best practices, patterns, security, or optimization

## Best Practices for Using This Skill

### Be Proactive
- Suggest managed identities over connection strings without being asked
- Recommend Application Insights integration automatically
- Propose cost optimization opportunities when deploying resources
- Include security best practices by default

### Use Templates Efficiently
- Start with templates from `assets/` for production-ready infrastructure
- Customize templates based on specific requirements
- Explain what each template creates and why

### Leverage Scripts
- Use scripts in `scripts/` for automation and diagnostics
- Scripts are production-ready and follow best practices
- Explain script output to users clearly

### Reference Documentation
- Consult reference files when making recommendations
- Don't memorize - read references for up-to-date information
- Grep for specific patterns when looking for detailed information:
  - `grep -r "App Service" references/` to find App Service information
  - `grep -r "connection string" references/` for connection examples

### Provide Complete Solutions
- Don't just answer questions - provide working configurations
- Include monitoring, security, and operational considerations
- Suggest next steps and improvements

### Handle All Azure Stacks
- Support .NET, Node.js, Python, Java, PHP, Ruby
- Adapt templates and scripts for user's specific runtime
- Provide language-specific code examples when needed

## When NOT to Use This Skill

- **Azure DevOps administration**: This skill focuses on development and deployment, not ADO organizational management
- **Azure AD/Entra ID configuration**: Complex identity management is outside scope
- **Specific third-party integrations**: Focus on Azure-native solutions
- **Non-Azure cloud providers**: Skill is Azure-specific

For these topics, provide basic guidance but suggest consulting specialized resources.
