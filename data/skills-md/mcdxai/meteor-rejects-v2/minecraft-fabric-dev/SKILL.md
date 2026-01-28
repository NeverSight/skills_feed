---
name: minecraft-fabric-dev
description: Comprehensive guidance for Minecraft mod development with Fabric, including porting from other mod loaders (Forge, NeoForge). Integrates MCP servers for decompilation, documentation access, and mixin validation. Use when developing Fabric mods, porting from Forge, or working with Minecraft source code.
---

# Minecraft Fabric Mod Development Skill

## Overview

This skill provides comprehensive guidance for Minecraft mod development with Fabric, including porting from other mod loaders (Forge, NeoForge). It integrates three MCP servers to provide complete tooling for mod development.

## Available MCP Servers

### 1. minecraft-dev-mcp
Core Minecraft development tools for source code access, decompilation, and analysis.

### 2. fabric-docs-mcp
Official Fabric documentation access with version-specific content.

### 3. baritone-docs-mcp
Baritone pathfinding library documentation (useful for AI/automation mods).

---

## Core Workflows

### Initial Setup Workflow

**When starting ANY Minecraft development task:**

1. **Sync documentation first:**
   ```
   sync_fabric_docs (force: false) → Get latest Fabric docs
   baritone_refresh_docs → Get Baritone docs if needed
   ```

2. **Identify target version:**
   ```
   list_fabric_versions → See available Fabric versions
   list_minecraft_versions → See available/cached Minecraft versions
   ```

3. **Decompile target version (if needed):**
   ```
   decompile_minecraft_version (version, mapping: "yarn", force: false)
   ```

### Understanding Mappings

**Mapping Types (in priority order for Fabric):**
- **yarn** - Community-driven, human-readable names (PREFERRED for Fabric)
- **mojmap** - Official Mojang names (good for vanilla reference)
- **intermediary** - Stable obfuscation-independent IDs (used internally by Fabric)
- **official** - Obfuscated names (a, b, c, etc.) - **NOTE: Minecraft is transitioning to de-obfuscated releases**

**When to use each:**
- Development: Use **yarn** (best community support)
- Reading vanilla code: Use **mojmap** (official names)
- Mapping translation: Use **intermediary** as bridge
- Deobfuscating: From **official** to yarn/mojmap

**Future-Proofing Note:**
Starting with experimental snapshots after 1.21.11, Minecraft is releasing de-obfuscated builds. Eventually, the "official" mapping will contain human-readable names instead of obfuscated ones (a, b, c). The MCP server is already prepared for this transition. When this becomes standard:
- Official releases will be immediately readable
- Yarn/Mojmap will still provide value for consistent naming
- Intermediary remains important for Fabric's stability guarantees
- Legacy versions will still require deobfuscation

**Current State (1.21.11 and earlier):** Official = obfuscated, use yarn/mojmap for development
**Future State (experimental snapshots+):** Official = de-obfuscated, still prefer yarn for Fabric consistency

---

## De-Obfuscated Minecraft Releases

### The Transition

Starting with experimental snapshots after version 1.21.11, Minecraft is releasing **de-obfuscated builds**. This is a gradual transition that will eventually become the standard for all Minecraft releases.

**What This Means:**
- Official Minecraft JARs will ship with human-readable class/method/field names
- No more obfuscated names like `a`, `b`, `c` in official releases
- Directly readable source code from vanilla JARs
- Reduced need for deobfuscation tools for newer versions

### Impact on Development Workflow

**For New Versions (De-obfuscated):**
- Official mappings will be immediately useful
- Yarn/Mojmap still valuable for:
  - Consistent naming conventions
  - Better documentation
  - Community-agreed terminology
  - Cross-version stability
- Intermediary remains critical for Fabric's version-independent mod loading

**For Legacy Versions (1.21.11 and earlier):**
- Still require traditional deobfuscation
- Use yarn/mojmap as primary mappings
- Official mappings remain obfuscated (a, b, c)
- All existing workflows continue unchanged

### MCP Server Compatibility

**The minecraft-dev-mcp server is already future-proof:**
- Handles both obfuscated and de-obfuscated official mappings
- Automatically detects mapping format
- Tools work identically regardless of obfuscation state
- No workflow changes needed when transitioning

**What You Don't Need to Worry About:**
- Manual detection of obfuscation state
- Different tool invocations for different versions
- Mapping compatibility issues
- Legacy version support

### Recommended Practices

**For Maximum Compatibility:**

```
# Still use yarn as primary for Fabric development
decompile_minecraft_version (version: "1.21.11", mapping: "yarn")
decompile_minecraft_version (version: "1.22-experimental", mapping: "yarn")

# Both work identically, server handles the difference
```

**When Working Across Version Boundaries:**

```
# Comparing old (obfuscated) to new (de-obfuscated)
compare_versions (
  fromVersion: "1.21.11",  # Obfuscated official
  toVersion: "1.22",        # De-obfuscated official
  mapping: "yarn"           # Consistent naming across both
)
```

**Why Still Use Yarn/Mojmap:**

1. **Consistency** - Names don't change between versions arbitrarily
2. **Documentation** - Community documentation references yarn names
3. **Stability** - Intermediary + yarn provides Fabric's version independence
4. **Compatibility** - Existing mods use yarn, maintain consistency
5. **Tooling** - Fabric ecosystem built around yarn conventions

### Migration Strategy

**No Action Required:**
- Continue using yarn for all Fabric development
- MCP server automatically handles both formats
- Existing validation tools work unchanged
- Documentation remains accurate

**Optional Optimizations:**
- For quick vanilla reference, official source becomes viable
- Cross-reference official names with yarn for learning
- Use official for understanding Mojang's intended naming

### Version Detection

**The tools automatically handle version type:**

```
# Works for both obfuscated and de-obfuscated
get_minecraft_source (version, className, mapping: "yarn")

# Server internally detects:
# - Is this version obfuscated? → Apply traditional deobfuscation
# - Is this version de-obfuscated? → Use direct mapping translation
```

**You never need to specify obfuscation state manually.**

---

## Common Development Tasks

### 1. Understanding Minecraft Source Code

**Workflow:**
```
Step 1: Find the class
  → search_fabric_docs (query: "entity", mcVersion: "latest")
  → search_minecraft_code (version, query: "Entity", searchType: "class", mapping: "yarn")

Step 2: Get source code
  → get_minecraft_source (version, className: "net.minecraft.entity.Entity", mapping: "yarn")

Step 3: Get documentation context
  → get_documentation (className: "Entity")
  → get_fabric_doc (path: "develop/entities.md", mcVersion: "latest")
```

**Best practices:**
- ALWAYS use yarn mappings for Fabric development
- Start broad with searches, then narrow down
- Check both Fabric docs AND Minecraft source
- Look for related classes using search results

### 2. Creating Mixins

**Essential workflow:**

```
Step 1: Understand the target
  → get_minecraft_source (version, className: "[target]", mapping: "yarn")
  → get_fabric_doc (path: "develop/mixins.md", mcVersion: "latest")

Step 2: Write mixin code
  [User writes mixin based on source + docs]

Step 3: Validate mixin
  → analyze_mixin (source: "[mixin code]", mcVersion: "[version]", mapping: "yarn")

Step 4: Fix issues
  [Review validation results, make corrections]
  → analyze_mixin (source: "[updated code]", mcVersion: "[version]", mapping: "yarn")
```

**Critical rules:**
- Mixins MUST use yarn mappings for Fabric
- Validate EVERY mixin before suggesting it's complete
- Check injection points exist in target class
- Verify method signatures match exactly
- Consider mixin priority and conflicts

**When validation fails:**
- Check if target class/method exists in that version
- Verify mapping is correct (yarn for Fabric)
- Look for renamed methods between versions
- Check method signatures (return type, parameters)

### 3. Using Access Wideners

**Workflow:**

```
Step 1: Identify what needs widening
  → get_minecraft_source (version, className: "[class]", mapping: "yarn")
  [Check field/method visibility]

Step 2: Create access widener file
  [Write .accesswidener with proper syntax]

Step 3: Validate
  → validate_access_widener (content: "[file content]", mcVersion: "[version]", mapping: "yarn")

Step 4: Apply fixes from validation
  [Update based on validation results]
```

**Access widener syntax:**
```
accessWidener v2 named
accessible class net/minecraft/class/Name
accessible method net/minecraft/class/Name methodName (Lparams;)Lreturn;
accessible field net/minecraft/class/Name fieldName Ltype;
extendable class net/minecraft/class/Name
mutable field net/minecraft/class/Name fieldName Ltype;
```

### 4. Analyzing Existing Mods

**For understanding/porting:**

```
Step 1: Extract mod metadata
  → analyze_mod_jar (jarPath: "[path]", includeAllClasses: false, includeRawMetadata: true)

Step 2: Examine mixins (if present)
  → analyze_mixin (source: "[jar path]", mcVersion: "[version]", mapping: "yarn")

Step 3: Check dependencies and entry points
  [Review metadata from Step 1]

Step 4: Decompile/remap if needed
  → remap_mod_jar (inputJar, outputJar, mcVersion, toMapping: "yarn")
```

**Path normalization:**
- Tool accepts both WSL (`/mnt/c/...`) and Windows (`C:\...`) paths
- Paths are automatically normalized internally

### 5. Version Migration & Porting

**Comparing Minecraft versions:**

```
Step 1: Get high-level overview
  → compare_versions (fromVersion, toVersion, mapping: "yarn", category: "all")

Step 2: Detailed API changes
  → compare_versions_detailed (fromVersion, toVersion, mapping: "yarn", 
     packages: ["net.minecraft.entity", "net.minecraft.world"], maxClasses: 500)

Step 3: Check registry changes
  → get_registry_data (version: "[old]", registry: "blocks")
  → get_registry_data (version: "[new]", registry: "blocks")

Step 4: Search for specific changes
  → search_fabric_docs (query: "migration [version]", mcVersion: "all")
```

**Breaking changes checklist:**
- Class renames/moves
- Method signature changes
- Field type changes
- Registry ID changes
- Removed/deprecated APIs

### 6. Porting from Forge to Fabric

**Comprehensive porting workflow:**

```
Step 1: Analyze Forge mod
  → analyze_mod_jar (jarPath: "[forge-mod.jar]", includeAllClasses: true, includeRawMetadata: true)

Step 2: Understand Forge-specific code
  [Review: @Mod annotations, event handlers, capability system, sided proxies]

Step 3: Find Fabric equivalents
  → search_fabric_docs (query: "[forge concept]", mcVersion: "latest")
  → get_fabric_doc (path: "develop/[topic].md", mcVersion: "latest")

Step 4: Map common patterns
  Forge Events → Fabric Events (different registration)
  Capabilities → Cardinal Components API or custom solution
  @Mod annotation → fabric.mod.json
  FMLJavaModLoadingContext → Fabric Mod Initializer
  DeferredRegister → Registry.register in onInitialize

Step 5: Check Minecraft version compatibility
  → get_minecraft_source (version, className: "[needed class]", mapping: "yarn")
  → compare_versions (fromVersion: "[forge ver]", toVersion: "[fabric ver]", mapping: "yarn")

Step 6: Validate converted mixins
  [If Forge mod uses CoreMods/ASM]
  → analyze_mixin (source: "[converted mixin]", mcVersion, mapping: "yarn")
```

**Forge → Fabric translation patterns:**

| Forge Pattern | Fabric Equivalent |
|---------------|-------------------|
| `@Mod` class | `ModInitializer` interface in fabric.mod.json |
| `MinecraftForge.EVENT_BUS.register()` | Event callbacks in respective classes |
| `@SubscribeEvent` | Direct method registration with event |
| Capabilities | Cardinal Components API (separate library) |
| `@ObjectHolder` | Direct `Registry.register()` calls |
| Config (ForgeConfig) | Cloth Config API or custom solution |
| `@OnlyIn(Dist.CLIENT)` | `client` entrypoint in fabric.mod.json |
| Network packets (SimpleChannel) | Fabric Networking API |
| `@Mod.EventBusSubscriber` | `ClientModInitializer` / `DedicatedServerModInitializer` |

**Critical Fabric-specific requirements:**
- `fabric.mod.json` replaces `mods.toml`
- Mixins config file (`modid.mixins.json`)
- Access widener file (if needed)
- Proper entrypoint registration
- Different event system architecture

---

## Advanced Workflows

### Large-Scale Code Search

**When you need to find patterns across entire codebase:**

```
Step 1: Index the version (one-time, enables fast search)
  → index_minecraft_version (version, mapping: "yarn")

Step 2: Fast full-text search
  → search_indexed (query: "entity damage", version, mapping: "yarn", 
     types: ["method", "field"], limit: 100)

Alternative: Direct search (slower, no index needed)
  → search_minecraft_code (version, query: "damage", searchType: "all", 
     mapping: "yarn", limit: 50)
```

**Search type guide:**
- `"class"` - Class name matching
- `"method"` - Method definitions
- `"field"` - Field declarations  
- `"content"` - Any code content
- `"all"` - Everything

### Finding Mappings Between Systems

**Use case: You have an obfuscated name and need the yarn name (legacy versions):**

```
find_mapping (symbol: "a", version: "1.21.11", sourceMapping: "official", targetMapping: "yarn")
find_mapping (symbol: "Entity", version: "1.21.11", sourceMapping: "mojmap", targetMapping: "yarn")
find_mapping (symbol: "class_1234", version: "1.21.11", sourceMapping: "intermediary", targetMapping: "yarn")
```

**Use case: De-obfuscated releases (1.22+ experimental):**

```
# Official names are now readable, but still translate to yarn for consistency
find_mapping (symbol: "Entity", version: "1.22", sourceMapping: "official", targetMapping: "yarn")
find_mapping (symbol: "LivingEntity", version: "1.22", sourceMapping: "official", targetMapping: "intermediary")
```

**Returns:**
- Class mappings
- Method mappings (with descriptors)
- Field mappings

**Cross-version mapping:**
```
# Works across obfuscated/de-obfuscated boundary
find_mapping (symbol: "Entity", version: "1.21.11", sourceMapping: "yarn", targetMapping: "yarn")
find_mapping (symbol: "Entity", version: "1.22", sourceMapping: "yarn", targetMapping: "yarn")
# Yarn provides consistency even as official format changes
```

### Registry Data Analysis

**For blocks, items, entities, etc.:**

```
# Get all registries
get_registry_data (version, registry: undefined)

# Get specific registry
get_registry_data (version, registry: "blocks")
get_registry_data (version, registry: "items")
get_registry_data (version, registry: "entities")
get_registry_data (version, registry: "biomes")
```

**Use cases:**
- Finding valid registry IDs for your mod
- Checking what changed between versions
- Validating data pack references

---

## Documentation Strategy

### When to Search Documentation

**Fabric Docs - Priority 1:**
```
# Feature implementation
search_fabric_docs (query: "custom blocks", mcVersion: "latest", limit: 15)
get_fabric_doc (path: "develop/blocks.md", mcVersion: "latest")

# Concept learning
list_fabric_sections (mcVersion: "latest")
get_fabric_doc_headings (path: "develop/mixins.md", mcVersion: "latest")
```

**Minecraft Source - Priority 2:**
```
# When you need to see how vanilla does it
get_minecraft_source (version, className: "BlockItem", mapping: "yarn")
search_minecraft_code (version, query: "registerBlock", searchType: "method", mapping: "yarn")
```

**Baritone Docs - Priority 3 (AI/pathfinding specific):**
```
# Only for pathfinding/AI mods
baritone_search_docs (query: "GoalBlock")
baritone_read_doc (path: "baritone/api/pathing/goals/GoalBlock.md")
```

### Documentation Reading Priority

1. **Start with Fabric docs** - Official, maintained, version-specific
2. **Reference Minecraft source** - See vanilla implementation
3. **Check related classes** - Understand the full system
4. **Validate with tools** - Test mixins/access wideners

---

## Error Handling & Troubleshooting

### Common Issues

**"Decompiled source not found"**
→ Run `decompile_minecraft_version` first

**"Mixin validation failed"**
→ Check target class exists: `get_minecraft_source`
→ Verify method signatures match exactly
→ Ensure using yarn mappings

**"Documentation not found"**
→ Run `sync_fabric_docs` (Fabric)
→ Run `baritone_refresh_docs` (Baritone)

**"Invalid mapping type"**
→ Fabric ALWAYS uses "yarn" (not mojmap)
→ Check available mappings with `find_mapping`

**"Path not found" (mod analysis)**
→ Check path format (both WSL and Windows supported)
→ Verify file exists at specified location
→ Use normalized paths (auto-converted)

### Validation Best Practices

**ALWAYS validate before suggesting code is complete:**
- Mixins: `analyze_mixin`
- Access wideners: `validate_access_widener`
- Version compatibility: `compare_versions`
- Registry IDs: `get_registry_data`

---

## Tool Selection Decision Tree

```
User wants to...

├─ Understand Minecraft code
│  ├─ Find a class → search_minecraft_code (searchType: "class")
│  ├─ See implementation → get_minecraft_source
│  └─ Find all usages → search_indexed (after indexing)
│
├─ Learn Fabric concepts
│  ├─ Browse topics → list_fabric_sections
│  ├─ Search for feature → search_fabric_docs
│  └─ Read full guide → get_fabric_doc
│
├─ Write a mixin
│  ├─ Get target class → get_minecraft_source
│  ├─ Check Fabric mixin docs → get_fabric_doc (path: "develop/mixins.md")
│  └─ Validate mixin → analyze_mixin
│
├─ Access private members
│  ├─ Check what exists → get_minecraft_source
│  ├─ Write access widener → [user writes]
│  └─ Validate → validate_access_widener
│
├─ Port a mod
│  ├─ Analyze original → analyze_mod_jar
│  ├─ Check Forge→Fabric patterns → search_fabric_docs
│  ├─ Compare MC versions → compare_versions_detailed
│  └─ Validate converted code → analyze_mixin
│
├─ Update for new version
│  ├─ High-level changes → compare_versions
│  ├─ Detailed API diff → compare_versions_detailed
│  ├─ Registry changes → get_registry_data (both versions)
│  └─ Migration guide → search_fabric_docs (query: "migration")
│
└─ Understand mappings
   ├─ Translate obfuscated → find_mapping
   ├─ See all mappings → List available in tool
   └─ Convert between systems → find_mapping

```

---

## Output Formatting for Users

### When Providing Mixin Code

**ALWAYS include:**
1. Full mixin class with imports
2. Validation command they should run
3. Explanation of what it does
4. Warning about testing

**Template:**
```java
// Your mixin code here
```

**Validation:**
```
analyze_mixin (source: "[above code]", mcVersion: "1.21.11", mapping: "yarn")
```

**Important:** Test this in a development environment before using in production.

### When Suggesting Access Wideners

**Template:**
```
accessWidener v2 named
[entries here]
```

**Validation:**
```
validate_access_widener (content: "[above content]", mcVersion: "1.21.11", mapping: "yarn")
```

### When Showing Version Differences

**Provide:**
1. Summary of changes
2. Breaking changes highlighted
3. Recommended actions
4. Migration code examples

---

## Performance Considerations

### Indexing Strategy

**When to index:**
- User will do extensive searching
- Working on large-scale refactoring
- Analyzing patterns across codebase

**When to skip indexing:**
- One-off queries
- Just looking up single class
- Quick reference checks

**Index command:**
```
index_minecraft_version (version, mapping: "yarn")
```

### Caching Awareness

**These are cached (fast after first run):**
- `decompile_minecraft_version`
- `get_minecraft_source`
- `get_registry_data`
- Fabric/Baritone docs (after sync)

**These are not cached (always fresh):**
- `search_minecraft_code` (unless indexed)
- `analyze_mixin`
- `validate_access_widener`
- `compare_versions`

---

## Version Compatibility Matrix

### Minecraft Version Support

**Check available versions:**
```
list_minecraft_versions → See what's available
list_fabric_versions → See what Fabric supports
```

**Typical workflow:**
1. User states target version
2. Verify version exists: `list_minecraft_versions`
3. Check Fabric support: `list_fabric_versions`
4. Decompile if needed: `decompile_minecraft_version`

### Mapping Version Notes

- **yarn**: Version-specific, must match Minecraft version (works for all versions)
- **mojmap**: Version-specific, must match Minecraft version (works for all versions)
- **intermediary**: Version-specific, stable intermediate format (Fabric's backbone)
- **official**: 
  - **Legacy (≤1.21.11)**: Raw obfuscated (a, b, c), no version metadata
  - **Modern (1.22+ experimental)**: De-obfuscated, human-readable names

### Version Categories

**Obfuscated Era (≤1.21.11):**
- Requires deobfuscation for development
- Official mappings are obfuscated
- Yarn/Mojmap essential for readability
- Standard workflow applies

**De-obfuscated Era (1.22+ experimental snapshots):**
- Official releases are human-readable
- Yarn/Mojmap still recommended for consistency
- Intermediary remains critical for Fabric
- Tools work identically (server auto-detects)

**Transition Period:**
- Some snapshots may be de-obfuscated (opt-in experimental)
- Release versions follow official Mojang timeline
- MCP server handles both formats seamlessly
- No workflow changes required

### Cross-Version Development

**When working across obfuscated/de-obfuscated boundary:**

```
# Use yarn for consistent names across versions
decompile_minecraft_version (version: "1.21.11", mapping: "yarn")
decompile_minecraft_version (version: "1.22-experimental", mapping: "yarn")

# Compare versions safely
compare_versions_detailed (
  fromVersion: "1.21.11",    # Obfuscated
  toVersion: "1.22",          # De-obfuscated
  mapping: "yarn"             # Consistent across both
)
```

**Best Practice:** Always use yarn for Fabric development regardless of target version's obfuscation state.

---

## Critical Reminders

### ALWAYS Remember

1. **Fabric = yarn mappings** (not mojmap, not intermediary for dev) - *consistent across all versions*
2. **Validate before declaring complete** (mixins, access wideners)
3. **Sync docs first** (prevent stale documentation)
4. **Check version compatibility** (especially for porting)
5. **Use appropriate search scope** (indexed vs direct)
6. **Provide validation commands** (so user can verify)
7. **Normalize paths** (tools handle WSL/Windows automatically)
8. **MCP server is future-proof** (handles both obfuscated and de-obfuscated releases automatically)

### NEVER Do

1. Don't suggest mojmap for Fabric development
2. Don't skip mixin validation
3. Don't assume classes exist without checking
4. Don't provide partial validation steps
5. Don't ignore version differences
6. Don't forget to sync documentation
7. Don't mix mapping types in same context
8. Don't worry about obfuscation state - the server handles it

### De-Obfuscated Era Awareness

**When user mentions version 1.22+ or experimental snapshots:**
- Note that these may be de-obfuscated releases
- Recommend yarn anyway for Fabric consistency
- Explain official names are now readable but yarn provides stability
- No workflow changes needed - tools auto-detect format

---

## Example: Complete Mixin Creation Workflow

**User Request:** "Create a mixin to prevent fall damage"

**Response Pattern:**

```
Let me help you create a fall damage prevention mixin for Fabric.

Step 1: Understanding the vanilla implementation
[get_minecraft_source for LivingEntity with fall damage logic]

Step 2: Checking Fabric mixin documentation
[get_fabric_doc for mixins guide]

Step 3: Creating the mixin

[Full mixin code with proper imports and structure]

Step 4: Validation (CRITICAL - run this!)

analyze_mixin (
  source: "[mixin code above]",
  mcVersion: "1.21.11",
  mapping: "yarn"
)

This mixin injects into the fall damage method and cancels it. The @Inject annotation targets the method responsible for applying fall damage, and we use cancellable = true to allow preventing the damage.

Important notes:
- Test in creative world first
- May conflict with other fall damage mods
- Affects all entities, not just players
```

---

## Resource URIs

### Fabric Documentation Resources

**Pattern:** `fabric://docs/{path}`

**Example:**
```
fabric://docs/develop/getting-started.md
fabric://docs/develop/mixins.md
fabric://docs/items/custom-item.md
```

**Access via:**
- `get_fabric_doc` tool
- Direct resource read
- Search results include URI

### Minecraft Source Resources

**Pattern:** `minecraft://source/{version}/{mapping}/{className}`

**Example:**
```
minecraft://source/1.21.1/yarn/net.minecraft.entity.Entity
minecraft://source/1.21.1/mojmap/net.minecraft.world.level.Level
```

**Also available:**
- `minecraft://mappings/{version}/{mapping}`
- `minecraft://registry/{version}/{registryType}`
- `minecraft://versions/list`
- `minecraft://index/{version}/{mapping}`

---

## Final Checklist for Mod Development

Before suggesting a solution is complete, verify:

- [ ] Documentation searched and referenced
- [ ] Target Minecraft version confirmed
- [ ] Correct mapping type used (yarn for Fabric)
- [ ] Source code examined for vanilla implementation
- [ ] Mixin validated with analyze_mixin
- [ ] Access widener validated (if used)
- [ ] Version compatibility checked
- [ ] Dependencies identified
- [ ] Testing instructions provided
- [ ] Potential conflicts noted

---

## Quick Reference Commands

**Initial Setup:**
```bash
sync_fabric_docs
list_minecraft_versions
decompile_minecraft_version (version: "1.21.11", mapping: "yarn")
```

**Development:**
```bash
get_fabric_doc (path: "develop/[topic].md")
get_minecraft_source (version, className, mapping: "yarn")
analyze_mixin (source, mcVersion, mapping: "yarn")
```

**Analysis:**
```bash
analyze_mod_jar (jarPath)
compare_versions (fromVersion, toVersion, mapping: "yarn")
search_minecraft_code (version, query, searchType: "all", mapping: "yarn")
```

**Validation:**
```bash
analyze_mixin (source, mcVersion, mapping: "yarn")
validate_access_widener (content, mcVersion, mapping: "yarn")
```

This skill provides complete coverage of Minecraft Fabric mod development workflows using all available MCP tools.
