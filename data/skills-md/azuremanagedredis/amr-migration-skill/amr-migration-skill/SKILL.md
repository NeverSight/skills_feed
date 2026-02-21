---
name: amr-migration-skill
description: |
  Helps users migrate from Azure Cache for Redis (ACR) to Azure Managed Redis (AMR).
  Use when users ask about: Redis migration, AMR vs ACR features, SKU selection, 
  migration best practices, feature compatibility, or Azure Redis cache upgrades.
---

# Azure Managed Redis Migration Skill

This skill assists users in migrating from Azure Cache for Redis (ACR) Basic/Standard/Premium tiers to Azure Managed Redis (AMR).

## 📝 Terminology Note

Users may refer to Azure Cache for Redis by several names:
- **OSS** (open-source Redis)
- **ACR** (Azure Cache for Redis)
- **Basic**, **Standard**, or **Premium** tier

These all refer to the same product: **Azure Cache for Redis**. Treat these terms interchangeably when users ask about migration.

## ⚠️ Scope Limitation: Enterprise Tier NOT Supported

**This skill does NOT cover Azure Cache for Redis Enterprise (ACRE) migrations.**

If users ask about migrating from:
- Azure Cache for Redis **Enterprise** tier
- Azure Cache for Redis **Enterprise Flash** tier

Respond with:
> "This skill only covers migrations from Azure Cache for Redis (Basic, Standard, and Premium tiers) to Azure Managed Redis. Please consult Microsoft support or the official documentation for Enterprise tier migration guidance."

**Supported source tiers**: Basic (C0-C6), Standard (C0-C6), Premium (P1-P5)
**Not supported**: Enterprise, Enterprise Flash

## ⚠️ AMR Terminology: No "Shards"

**Do not use the term "shards" when describing AMR (Azure Managed Redis).** In AMR, sharding is managed internally and not exposed to the customer. The concept of shards only applies to ACR Premium clustered caches. When discussing AMR, refer to the SKU and its memory capacity instead.

---

## When to Use This Skill

Activate this skill when the user:
- Asks about migrating from Azure Cache for Redis to Azure Managed Redis
- Wants to compare ACR features with AMR features
- Needs help selecting the right AMR SKU for their workload
- Has questions about feature compatibility between ACR and AMR
- Wants to understand migration best practices and considerations

## Available Resources

> **Important**: Always use the provided scripts for pricing lookups and metrics retrieval. Do not craft custom API calls or scripts — the provided ones already handle tier-specific calculation logic (HA, shards, MRPP) and metric aggregation correctly. For metrics, use a default time range of **7 days** unless the user specifies otherwise.

### Documentation Access

> **Note**: Most migration guidance is already available in this skill's local reference files. Only use the MCP server to look up information not covered locally (e.g., latest release notes, region availability, or new features).

Use the Microsoft Learn MCP server to fetch up-to-date documentation:
- **MCP Endpoint**: `https://learn.microsoft.com/api/mcp`
- **Setup Guide**: See [MCP Server Configuration](references/mcp-server-config.md) for setup instructions (GitHub Copilot, Claude Desktop)
- Key documentation paths:
  - `/azure/azure-cache-for-redis/` - General Azure Redis documentation
  - `/azure/azure-cache-for-redis/managed-redis/` - AMR-specific documentation
  - `/azure/azure-cache-for-redis/cache-overview` - Product overview

### Azure CLI Command Reference
See [Azure CLI Commands](references/azure-cli-commands.md) for practical `az redis` examples to:
- List ACR caches in a subscription or resource group
- Extract cache details (region, SKU, shard count, replicas)
- Check persistence and geo-replication settings

### SKU Mapping Reference
See [SKU Mapping Guide](references/sku-mapping.md) for guidelines, ACR → AMR mapping tables, selection criteria, and decision matrix. For AMR SKU definitions (M, B, X, Flash series), see [AMR SKU Specs](references/amr-sku-specs.md).

### Dynamic Pricing Lookup
Once you've identified candidate SKUs, get real-time pricing with monthly cost calculations:

```powershell
# Windows PowerShell
.\scripts\get_redis_price.ps1 -SKU M10 -Region westus2
.\scripts\get_redis_price.ps1 -SKU M10 -Region westus2 -NoHA
.\scripts\get_redis_price.ps1 -SKU C3 -Region westus2 -Tier Standard
.\scripts\get_redis_price.ps1 -SKU P2 -Region westus2 -Shards 3 -Replicas 2

# Linux/Mac bash
./scripts/get_redis_price.sh M10 westus2
./scripts/get_redis_price.sh P2 westus2 --shards 3
```

**Script options**:
- `-NoHA` / `--no-ha` - Non-HA deployment (AMR only, 50% savings for dev/test)
- `-Shards N` / `--shards N` - Number of shards (ACR Premium clustered)
- `-Replicas N` / `--replicas N` - Replicas per primary (ACR Premium MRPP, default: 1)
- `-Currency X` / `--currency X` - Currency code (default: USD)

**SKUs supported**:
- ACR: C0-C6 (Basic/Standard - must specify tier), P1-P5 (Premium)
- AMR: M10-M2000, B0-B1000, X3-X700, A250-A4500

**Resources**:
- [Pricing Tier Rules](references/pricing-tiers.md) - Calculation logic for HA, clustering, MRPP
- [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/?service=managed-redis) - Official quotes

### Feature Comparison
See [Feature Comparison](references/feature-comparison.md) for detailed comparison between ACR (Basic/Standard/Premium) and AMR features.

### Retirement FAQ
See [Retirement FAQ](references/retirement-faq.md) for retirement dates, timelines, and common migration questions.

**Relevant to this skill (ACR Basic/Standard/Premium)**:
- **Basic/Standard/Premium**: Retire September 30, 2028

**Not covered by this skill**:
- Enterprise/Enterprise Flash retirement (March 31, 2027) - contact Microsoft support

### Migration Overview
See [Migration Overview](references/migration-overview.md) for detailed migration guidance including:
- Migration strategies (new cache, RDB export/import, dual-write, RIOT)
- Connection string changes
- Clustering policy and network isolation considerations

## Migration Workflow

### Step 1: Assess Current Cache
Gather metrics from the existing ACR cache to inform SKU selection:

```powershell
# Windows PowerShell
.\scripts\get_acr_metrics.ps1 -SubscriptionId <id> -ResourceGroup <rg> -CacheName <name>
.\scripts\get_acr_metrics.ps1 -SubscriptionId <id> -ResourceGroup <rg> -CacheName <name> -Days 7

# Linux/Mac bash
./scripts/get_acr_metrics.sh <subscriptionId> <resourceGroup> <cacheName>
./scripts/get_acr_metrics.sh <subscriptionId> <resourceGroup> <cacheName> 7
```

Also retrieve the actual memory reservation to determine true usable capacity (defaults in the SKU mapping tables assume ~20%):

```bash
az redis show -n <cache-name> -g <resource-group> -o json \
  --query "{maxfragmentationmemoryReserved: redisConfiguration.maxfragmentationmemoryReserved, maxmemoryReserved: redisConfiguration.maxmemoryReserved}"
```

Both values are in MB. **Actual Usable = SKU Capacity − (maxmemoryReserved + maxfragmentationmemoryReserved)**. Use this as the source of truth for sizing.

**Requires**: Azure CLI logged in (`az login`)

> **Fallback**: If the scripts fail (e.g., locked tenant, insufficient permissions, no CLI access), direct the user to retrieve the same metrics manually from the **Azure Portal** under their cache's **Monitoring → Metrics** blade.

**Metrics retrieved** (Peak, P95, and Average for each):
- Used Memory RSS (bytes and GB)
- Server Load (%)
- Connected Clients
- Network Bandwidth — Cache Read and Cache Write (bytes/sec)

Use these values to:
1. Size the target AMR SKU (usable memory ≥ peak used memory — no extra buffer needed with an eviction policy)
2. Choose tier (high Server Load + low memory → Compute Optimized X-series)
3. Verify connection limits are sufficient
4. Use P95 values to distinguish sustained load from occasional spikes

### Step 2: Select Target AMR SKU
1. Refer to the [SKU Mapping Guide](references/sku-mapping.md)
2. Use metrics from Step 1 to validate sizing
3. Get pricing for candidate SKUs:
   ```powershell
   .\scripts\get_redis_price.ps1 -SKU M20 -Region westus2
   .\scripts\get_redis_price.ps1 -SKU B20 -Region westus2
   ```

### Step 3: Plan Migration
1. Determine migration strategy (dual-write, snapshot/restore, etc.)
2. **Clustering policy**: For non-clustered ACR caches (Basic, Standard, non-clustered Premium), create the AMR cache with **Enterprise clustering policy** to avoid client application changes. OSS clustering policy exposes cluster topology and may require a cluster-aware client.
3. **Network isolation**: ACR caches using VNet injection must be replaced with **Private Link** on AMR, as AMR does not support VNet injection. Ensure Private Endpoints are configured before cutover.
4. Plan for potential downtime or data sync requirements
5. Update application connection strings and configuration

### Step 4: Execute Migration
1. Create the target AMR cache
2. Migrate data using appropriate method
3. Validate data integrity
4. Switch application traffic to new cache

## Common Questions

### What is the difference between Azure Cache for Redis (ACR) and Azure Managed Redis (AMR)?
Refer to [Feature Comparison](references/feature-comparison.md) for the full matrix. Key differences include:
- AMR offers Redis Stack features (JSON, Search, Time Series, Bloom filters)
- AMR has different SKU tiers optimized for different workloads
- AMR provides enhanced performance and scalability options

### How do I choose the right AMR SKU?
Refer to [SKU Mapping Guide](references/sku-mapping.md) and consider:
- Current memory usage
- Compute pressure (Server Load %)
- Feature requirements (clustering, geo-replication, Redis modules)
- Budget constraints

### What features are not available in AMR?
Check [Feature Comparison](references/feature-comparison.md) for the current feature matrix. Use the MCP server to fetch the latest documentation for authoritative information.

### What about Enterprise tier migration?
**This skill does not cover Enterprise tier migrations.** If asked about ACRE (Azure Cache for Redis Enterprise) migration, inform the user that Enterprise tier has different considerations and they should consult Microsoft support or official documentation.

## Tips for Effective Migration

1. **Test thoroughly**: Always test in a non-production environment first
2. **Monitor performance**: Compare baseline metrics before and after migration
3. **Plan for rollback**: Have a rollback strategy in case of issues
4. **Update client libraries**: Ensure Redis client libraries support AMR features
5. **Review security settings**: Update firewall rules, private endpoints, and authentication
