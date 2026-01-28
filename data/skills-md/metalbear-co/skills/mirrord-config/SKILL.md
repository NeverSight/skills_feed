---
name: mirrord-config
description: Helps users generate, edit, and validate mirrord.json configuration files for mirrord (MetalBear). Use when the user wants to connect their local process to a Kubernetes environment, configure features (env/fs/network), or needs feedback on an existing mirrord.json. Always ensures output JSON is valid and schema-conformant.
metadata:
  author: MetalBear
  version: "1.0"
---

# Mirrord Configuration Skill

## Purpose

Generate and validate `mirrord.json` configuration files:
- **Generate** valid configs from natural language descriptions
- **Validate** user-provided configs against schema
- **Fix** invalid configurations with explanations
- **Explain** configuration options and patterns

## Critical First Steps

**Step 1: Load references**
Read BOTH reference files from this skill's `references/` directory:
1. `references/schema.json` - Authoritative JSON Schema
2. `references/configuration.md` - Configuration reference

If using absolute paths, these are located relative to this skill's installation directory. Search for them if needed using patterns like `**/mirrord-config/references/*`.

**Step 2: Install mirrord CLI (if not present)**
```bash
# Check if installed
which mirrord || brew install metalbear-co/mirrord/mirrord || curl -fsSL https://raw.githubusercontent.com/metalbear-co/mirrord/main/scripts/install.sh | bash
```

**Step 3: Validate before presenting**
After generating any config, ALWAYS run:
```bash
mirrord verify-config /path/to/config.json
```
- If validation fails, fix the config and re-validate
- Only present configs that pass validation
- Include validation output in your response

## Request Types

### Generate new config
User describes what they want without providing JSON.
- Extract target (pod/deployment), namespace, features needed
- Create minimal valid config using only schema-defined keys
- Default to minimal configs; mirrord has sensible defaults

### Validate existing config  
User provides JSON to check.
- Parse strictly (catch trailing commas, comments, invalid syntax)
- Validate against schema
- List issues by severity: Errors → Warnings → Suggestions
- Provide corrected version

### Modify existing config
User wants changes to their config.
- Validate first, then apply requested changes
- Ensure modifications maintain schema conformance

## Response Format

### For generation or fixes:
1. Brief summary (1-2 sentences)
2. Valid JSON config in code block
3. Validation output from `mirrord verify-config`:
```json
{
  "type": "Success",
  "warnings": [],
  "compatible_target_types": [...]
}
```
4. Short explanation of key sections (if validation passed)

### For validation:
1. **Errors** (schema violations - will cause failures)
2. **Warnings** (valid but potentially wrong behavior)  
3. **Suggestions** (optional improvements)
4. Corrected JSON config

## Configuration Guidelines

### Common patterns (verify exact keys in schema):

**Target selection:**
- `"target": "pod/name"` or `{"path": "pod/name", "namespace": "staging"}`
- Set `operator` if using operator mode
- Specify `kube_context` if needed

**Features:**
- `"env": true` - Mirror environment variables
- `"env": {"include": "VAR1;VAR2"}` - Selective inclusion
- `"fs": "read"` - Read-only filesystem access
- `"network": true` - Enable network mirroring
- `"network": {"incoming": {"mode": "steal"}}` - Steal incoming traffic

**Network modes:**
- Check schema for valid `incoming.mode` values (e.g., "steal", "mirror", "off")
- Configure HTTP filters, port mapping, localhost handling

**Templating:**
- mirrord uses Tera templates
- Example: `"target": "{{ get_env(name=\"TARGET\", default=\"pod/fallback\") }}"`
- Templates must remain valid JSON

## Validation Rules

**Must enforce:**
- Strict JSON parsing (no comments, no trailing commas)
- All keys must exist in schema
- Correct types (string vs object, enums, etc.)
- Required fields present
- No `additionalProperties` where schema forbids them

**Path notation for errors:**
Use JSON Pointer style: `/feature/network/incoming/mode`

## Common Pitfalls

- User pastes YAML/TOML → Explain JSON required, offer to convert structure
- User requests unsupported key → Say it's not in schema, suggest alternatives
- Overly complex configs → Prefer minimal configs with only requested settings
- Conflicting settings → Identify based on configuration.md semantics

## What to Ask (only if critical)

If request is under-specified, ask for ONE detail:
- Target identity (pod name, namespace)
- Incoming network behavior (steal vs mirror)
- Operator usage (yes/no)
- Specific ports to map/ignore

Otherwise provide safe defaults and note assumptions.

## Automatic Validation Workflow

Every generated or modified config MUST be validated before presentation:

1. Save config to temporary file
2. Run `mirrord verify-config <file>`
3. If validation fails:
   - Parse error messages
   - Fix the config
   - Re-validate until success
4. Present config with validation output

Never skip validation - it catches schema errors we might miss manually.

## Quality Requirements

✓ **Schema-first**: Output must conform to `schema.json`  
✓ **No hallucination**: Only use documented keys  
✓ **Valid JSON**: Always parseable, no comments  
✓ **Actionable feedback**: Clear explanations of what to fix and why  
✓ **Minimal configs**: Don't set unnecessary options

## Example Scenarios

**"Connect to pod api-7c8d9 in staging, steal traffic on port 8080, exclude secret env vars"**
→ Read references, generate minimal config with target, network.incoming, env.exclude

**User provides invalid JSON with trailing comma**
→ Parse error → Fix syntax → Validate against schema → Explain issues → Provide corrected config

**"Is my config valid?" + JSON provided**
→ Check syntax → Validate all keys/types against schema → List violations → Suggest fixes
