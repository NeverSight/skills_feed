---
name: schema-creator
description: Creates JSON Schema validation files for skills, agents, hooks, workflows, and data structures. Ensures type safety and input validation across the framework.
version: 2.1.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash, Glob, Grep]
best_practices:
  - Use JSON Schema draft-07 or later
  - Include descriptions for all properties
  - Define required vs optional clearly
  - Add examples in schema
  - Use $ref for reusable definitions
  - Validate schemas before saving
error_handling: graceful
streaming: supported
output_location: .claude/schemas/
---

# Schema Creator Skill

Creates JSON Schema validation files for the Claude Code Enterprise Framework. Schemas enforce type safety, input validation, and structural consistency across skills, agents, hooks, workflows, and custom data structures.

## SYSTEM IMPACT ANALYSIS (CRITICAL - DO NOT SKIP)

**After creating ANY schema, you MUST:**

1. Register in appropriate location (global vs skill-local)
2. Update related validators to use the new schema
3. Add schema reference to CLAUDE.md if globally significant

**Verification:**

```bash
# Verify schema is valid JSON
node -e "JSON.parse(require('fs').readFileSync('.claude/schemas/<schema-name>.json'))"

# Check schema exists
ls .claude/schemas/<schema-name>.json || ls .claude/skills/<skill>/schemas/<schema-name>.json
```

**WHY**: Invalid schemas cause silent validation failures. Unregistered schemas are never used.

---

## Purpose

Schemas provide structured validation for:

1. **Skill Inputs/Outputs** - Validate data passed to and from skills
2. **Agent Definitions** - Validate agent YAML frontmatter and structure
3. **Hook Definitions** - Validate hook configuration and registration
4. **Workflow Definitions** - Validate workflow steps and configuration
5. **Custom Data Structures** - Validate project-specific data formats

## Schema Types

| Type                | Location                                           | Purpose                          |
| ------------------- | -------------------------------------------------- | -------------------------------- |
| Skill Input         | `.claude/skills/{name}/schemas/input.schema.json`  | Validate skill invocation inputs |
| Skill Output        | `.claude/skills/{name}/schemas/output.schema.json` | Validate skill execution outputs |
| Agent Definition    | `.claude/schemas/agent-definition.schema.json`     | Validate agent YAML frontmatter  |
| Skill Definition    | `.claude/schemas/skill-definition.schema.json`     | Validate skill YAML frontmatter  |
| Hook Definition     | `.claude/schemas/hook-definition.schema.json`      | Validate hook configuration      |
| Workflow Definition | `.claude/schemas/workflow-definition.schema.json`  | Validate workflow structure      |
| Custom              | `.claude/schemas/{name}.schema.json`               | Project-specific validation      |

### Reference Schema

**Use `.claude/schemas/agent-definition.schema.json` as the canonical reference schema.**

Before finalizing any schema, compare against reference:

- [ ] Follows JSON Schema draft-07 or later (draft-2020-12 preferred)
- [ ] Has $schema, $id, title, description, type fields
- [ ] Required fields are documented in "required" array
- [ ] All properties have description fields
- [ ] Includes examples where helpful
- [ ] Uses proper patterns (kebab-case names, semver versions)

### CLAUDE.md Registration (MANDATORY)

After creating a schema, update CLAUDE.md if the schema enables new capabilities:

1. **New artifact type schema** - Add to relevant section (Section 3 for agents, Section 8.5 for skills)
2. **Agent/skill/workflow validation schema** - Document in Section 4 (Self-Evolution)
3. **Framework-wide schema** - Add to Existing Schemas Reference table in this skill

**Verification:**

```bash
grep "schema-name" .claude/CLAUDE.md || echo "WARNING: Schema not registered in CLAUDE.md"
```

**BLOCKING**: Schema without documentation may not be discovered by other agents.

## Workflow

### Step 1: Gather Schema Requirements

Before creating a schema, understand:

```
1. WHAT data structure are you validating?
   - Skill input/output
   - Agent/skill/hook/workflow definition
   - Custom data format

2. WHERE should the schema live?
   - Global: .claude/schemas/ (framework-wide)
   - Local: .claude/skills/{skill}/schemas/ (skill-specific)

3. WHAT are the required vs optional fields?
   - Required: Must be present for valid data
   - Optional: Enhance but not required

4. WHAT are the validation rules?
   - Types (string, number, boolean, object, array)
   - Patterns (regex for strings)
   - Ranges (min/max for numbers)
   - Enums (allowed values)
   - Lengths (min/max for strings/arrays)
```

### Step 2: Determine Schema Type and Location

| Creating For       | Schema Location                                     | Example                    |
| ------------------ | --------------------------------------------------- | -------------------------- |
| New skill inputs   | `.claude/skills/{skill}/schemas/input.schema.json`  | `tdd` skill parameters     |
| New skill outputs  | `.claude/skills/{skill}/schemas/output.schema.json` | `tdd` skill results        |
| Global definition  | `.claude/schemas/{name}.schema.json`                | `test-results.schema.json` |
| Reusable component | `.claude/schemas/components/{name}.schema.json`     | `task-status.schema.json`  |

### Step 3: Analyze Data Structure

Examine existing data or specify expected structure:

```javascript
// Example: Analyzing skill output structure
const exampleOutput = {
  success: true,
  result: {
    filesCreated: ['src/test.ts'],
    testsGenerated: 5,
    coverage: 85.2,
  },
  metadata: {
    duration: 1234,
    skill: 'test-generator',
  },
};

// Extract schema from example:
// - success: boolean (required)
// - result: object (optional)
// - metadata: object (optional)
```

### Step 4: Generate JSON Schema

Use the schema template and customize:

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://claude.ai/schemas/{schema-name}",
  "title": "{Schema Title}",
  "description": "{What this schema validates}",
  "type": "object",
  "required": ["field1", "field2"],
  "properties": {
    "field1": {
      "type": "string",
      "description": "Description of field1",
      "minLength": 1,
      "maxLength": 100
    },
    "field2": {
      "type": "number",
      "description": "Description of field2",
      "minimum": 0,
      "maximum": 100
    },
    "optionalField": {
      "type": "boolean",
      "description": "Optional boolean field",
      "default": false
    }
  },
  "additionalProperties": false
}
```

### Step 5: Add Descriptions and Examples

**Every property MUST have a description:**

```json
{
  "properties": {
    "name": {
      "type": "string",
      "description": "The unique identifier for the resource in lowercase-with-hyphens format",
      "pattern": "^[a-z][a-z0-9-]*$",
      "examples": ["my-skill", "test-generator", "code-reviewer"]
    }
  }
}
```

**Add top-level examples:**

```json
{
  "examples": [
    {
      "name": "example-skill",
      "description": "An example skill for demonstration",
      "version": "1.0.0"
    }
  ]
}
```

### Step 6: Create Validation Test

Write a simple test to verify the schema works:

```javascript
// validate-schema-test.cjs
const Ajv = require('ajv');
const schema = require('./.claude/schemas/my-schema.schema.json');

const ajv = new Ajv({ allErrors: true });
const validate = ajv.compile(schema);

// Test valid data
const validData = {
  /* valid example */
};
console.log('Valid:', validate(validData));

// Test invalid data
const invalidData = {
  /* invalid example */
};
console.log('Invalid:', validate(invalidData));
console.log('Errors:', validate.errors);
```

### Step 7: System Impact Analysis (MANDATORY)

**Before marking schema creation complete, verify ALL items:**

```
[ ] Schema file created in correct location
[ ] Schema is valid JSON (parseable)
[ ] Schema has $schema, $id, title, description
[ ] All required fields defined in "required" array
[ ] All properties have descriptions
[ ] Examples included for complex schemas
[ ] Schema registered with validators (if applicable)
[ ] Related documentation updated
```

**Verification Commands:**

```bash
# Validate JSON syntax
node -e "JSON.parse(require('fs').readFileSync('.claude/schemas/{name}.schema.json'))"

# Check required fields
node -e "const s = require('.claude/schemas/{name}.schema.json'); console.log('title:', s.title); console.log('description:', s.description);"

# List all schemas
ls -la .claude/schemas/*.schema.json
```

**BLOCKING**: If any item fails, schema creation is INCOMPLETE. All items must pass.

## System Impact Analysis (MANDATORY)

After creating a schema, complete ALL of the following:

### 1. CLAUDE.md Update

- Add to appropriate section if schema enables new capability
- Section 3 for agent-related schemas
- Section 4.1 for creator ecosystem schemas
- Section 8.5 for skill-related schemas

### 2. Validator Integration

- Check if hooks should validate against new schema
- Update `.claude/hooks/` if schema affects validation
- Add to `schemaMap` in relevant validators

### 3. Related Schemas

- Update related schemas if needed ($ref links)
- Check for circular dependencies
- Ensure $id values are unique

### 4. Documentation

- Update `.claude/docs/` if schema documents new pattern
- Add schema to Existing Schemas Reference table
- Update skill-catalog.md if schema is for a new skill

**Verification Checklist:**

```bash
# Check CLAUDE.md registration
grep "{schema-name}" .claude/CLAUDE.md

# Check for $ref usage in other schemas
grep -r "{schema-name}" .claude/schemas/

# Verify no duplicate $id
grep -h "\$id" .claude/schemas/*.json | sort | uniq -d
```

**BLOCKING**: Schema creation is NOT complete until all impact analysis items are verified.

## Schema Templates

### Basic Input Schema

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://claude.ai/schemas/skill-name-input",
  "title": "Skill Name Input Schema",
  "description": "Input validation schema for skill-name skill",
  "type": "object",
  "required": [],
  "properties": {
    "target": {
      "type": "string",
      "description": "Target file or directory path"
    },
    "options": {
      "type": "object",
      "description": "Optional configuration",
      "properties": {
        "verbose": {
          "type": "boolean",
          "default": false
        }
      }
    }
  },
  "additionalProperties": false
}
```

### Basic Output Schema

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://claude.ai/schemas/skill-name-output",
  "title": "Skill Name Output Schema",
  "description": "Output validation schema for skill-name skill",
  "type": "object",
  "required": ["success"],
  "properties": {
    "success": {
      "type": "boolean",
      "description": "Whether the skill executed successfully"
    },
    "result": {
      "type": "object",
      "description": "The skill execution result",
      "additionalProperties": true
    },
    "error": {
      "type": "string",
      "description": "Error message if execution failed"
    }
  },
  "additionalProperties": false
}
```

### Definition Schema (for agents, skills, hooks)

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://claude.ai/schemas/entity-definition",
  "title": "Entity Definition Schema",
  "description": "Schema for validating entity definition files",
  "type": "object",
  "required": ["name", "description"],
  "properties": {
    "name": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9-]*$",
      "description": "Entity name in lowercase-with-hyphens format"
    },
    "description": {
      "type": "string",
      "minLength": 20,
      "maxLength": 500,
      "description": "Clear description of the entity purpose"
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+(\\.\\d+)?$",
      "default": "1.0.0",
      "description": "Semantic version number"
    }
  },
  "additionalProperties": true,
  "examples": [
    {
      "name": "my-entity",
      "description": "A sample entity for demonstration purposes",
      "version": "1.0.0"
    }
  ]
}
```

## Common JSON Schema Patterns

### String Patterns

```json
{
  "kebab-case": {
    "type": "string",
    "pattern": "^[a-z][a-z0-9-]*$"
  },
  "semver": {
    "type": "string",
    "pattern": "^\\d+\\.\\d+(\\.\\d+)?$"
  },
  "file-path": {
    "type": "string",
    "pattern": "^[\\w./-]+$"
  },
  "email": {
    "type": "string",
    "format": "email"
  },
  "url": {
    "type": "string",
    "format": "uri"
  }
}
```

### Enum Patterns

```json
{
  "model": {
    "type": "string",
    "enum": ["sonnet", "opus", "haiku", "inherit"]
  },
  "priority": {
    "type": "string",
    "enum": ["lowest", "low", "medium", "high", "highest"]
  },
  "status": {
    "type": "string",
    "enum": ["pending", "in_progress", "completed", "failed", "blocked"]
  }
}
```

### Array Patterns

```json
{
  "tools": {
    "type": "array",
    "items": { "type": "string" },
    "minItems": 1,
    "uniqueItems": true,
    "description": "List of available tools"
  },
  "skills": {
    "type": "array",
    "items": { "type": "string", "pattern": "^[a-z][a-z0-9-]*$" },
    "description": "List of skill names"
  }
}
```

### Object Patterns

```json
{
  "config": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "enabled": { "type": "boolean", "default": true },
      "timeout": { "type": "integer", "minimum": 0 }
    }
  },
  "metadata": {
    "type": "object",
    "additionalProperties": true,
    "description": "Arbitrary metadata"
  }
}
```

### Conditional Patterns

```json
{
  "if": {
    "properties": {
      "type": { "const": "mcp" }
    }
  },
  "then": {
    "required": ["server", "command"]
  },
  "else": {
    "required": ["handler"]
  }
}
```

### Using $ref for Reusability

```json
{
  "$defs": {
    "namePattern": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9-]*$",
      "description": "Lowercase with hyphens"
    },
    "toolsList": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 1
    }
  },
  "properties": {
    "name": { "$ref": "#/$defs/namePattern" },
    "tools": { "$ref": "#/$defs/toolsList" }
  }
}
```

## CLI Usage

### Create Schema from Template

```bash
# Create skill input schema
node .claude/skills/schema-creator/scripts/main.cjs \
  --type input \
  --skill my-skill

# Create skill output schema
node .claude/skills/schema-creator/scripts/main.cjs \
  --type output \
  --skill my-skill

# Create global schema
node .claude/skills/schema-creator/scripts/main.cjs \
  --type global \
  --name my-data-format

# Create definition schema
node .claude/skills/schema-creator/scripts/main.cjs \
  --type definition \
  --entity workflow
```

### Validate Schema

```bash
# Validate a schema file
node .claude/skills/schema-creator/scripts/main.cjs \
  --validate .claude/schemas/my-schema.schema.json

# Validate data against schema
node .claude/skills/schema-creator/scripts/main.cjs \
  --validate-data data.json \
  --schema .claude/schemas/my-schema.schema.json
```

### Generate Schema from Example

```bash
# Generate schema from JSON example
node .claude/skills/schema-creator/scripts/main.cjs \
  --from-example example.json \
  --output .claude/schemas/generated.schema.json
```

## Integration with Validators

### Using Ajv for Runtime Validation

```javascript
const Ajv = require('ajv');
const addFormats = require('ajv-formats');

const ajv = new Ajv({ allErrors: true });
addFormats(ajv);

// Load and compile schema
const schema = require('./.claude/schemas/skill-definition.schema.json');
const validate = ajv.compile(schema);

// Validate data
function validateSkillDefinition(data) {
  const valid = validate(data);
  if (!valid) {
    return {
      valid: false,
      errors: validate.errors.map(e => `${e.instancePath} ${e.message}`),
    };
  }
  return { valid: true };
}
```

### Pre-commit Validation Hook

```javascript
// .claude/hooks/schema-validator.js
const fs = require('fs');
const path = require('path');
const Ajv = require('ajv');

const schemaMap = {
  '.claude/agents/': '.claude/schemas/agent-definition.schema.json',
  '.claude/skills/': '.claude/schemas/skill-definition.schema.json',
  '.claude/hooks/': '.claude/schemas/hook-definition.schema.json',
};

function validateFile(filePath) {
  // Find matching schema
  for (const [pattern, schemaPath] of Object.entries(schemaMap)) {
    if (filePath.includes(pattern)) {
      const schema = JSON.parse(fs.readFileSync(schemaPath));
      const ajv = new Ajv();
      const validate = ajv.compile(schema);

      // Parse and validate file
      // ...
    }
  }
}
```

## Workflow Integration

This skill is part of the unified artifact lifecycle. For complete multi-agent orchestration:

**Router Decision:** `.claude/workflows/core/router-decision.md`

- How the Router discovers and invokes this skill's artifacts

**Artifact Lifecycle:** `.claude/workflows/core/skill-lifecycle.md`

- Discovery, creation, update, deprecation phases
- Version management and registry updates
- CLAUDE.md integration requirements

**External Integration:** `.claude/workflows/core/external-integration.md`

- Safe integration of external artifacts
- Security review and validation phases

---

## Cross-Reference: Creator Ecosystem

This skill is part of the **Creator Ecosystem**. Use companion creators for related artifacts:

| Creator              | When to Use                               | Invocation                             |
| -------------------- | ----------------------------------------- | -------------------------------------- |
| **agent-creator**    | Creating agents that use schemas          | `Skill({ skill: 'agent-creator' })`    |
| **skill-creator**    | Creating skills with input/output schemas | `Skill({ skill: 'skill-creator' })`    |
| **hook-creator**     | Creating hooks with validation            | `Skill({ skill: 'hook-creator' })`     |
| **workflow-creator** | Creating workflows with step schemas      | `Skill({ skill: 'workflow-creator' })` |
| **template-creator** | Creating templates with data schemas      | `Skill({ skill: 'template-creator' })` |

### Integration Chain

```text
[SKILL-CREATOR] Creating new skill with validation...
  -> Calls schema-creator for input/output schemas
  -> Schemas created in .claude/skills/{skill}/schemas/

[AGENT-CREATOR] Creating agent with strict validation...
  -> Agent uses agent-definition.schema.json for self-validation
  -> Agent validates inputs using custom schemas

[WORKFLOW-CREATOR] Creating workflow with typed steps...
  -> Each step output validates against schema
  -> Workflow uses workflow-definition.schema.json
```

## Existing Schemas Reference

| Schema                | Location           | Purpose                 |
| --------------------- | ------------------ | ----------------------- |
| `agent-definition`    | `.claude/schemas/` | Agent YAML frontmatter  |
| `skill-definition`    | `.claude/schemas/` | Skill YAML frontmatter  |
| `hook-definition`     | `.claude/schemas/` | Hook configuration      |
| `workflow-definition` | `.claude/schemas/` | Workflow structure      |
| `project-analysis`    | `.claude/schemas/` | Project analyzer output |
| `test-results`        | `.claude/schemas/` | Test execution results  |
| `test_plan`           | `.claude/schemas/` | Test plan structure     |

## File Placement & Standards

### Output Location Rules

This skill outputs to: `.claude/schemas/`

For skill-specific schemas: `.claude/skills/<skill-name>/schemas/`

Schema naming convention:

- Global schemas: `<name>.schema.json`
- Skill input: `input.schema.json`
- Skill output: `output.schema.json`
- Components: `components/<name>.schema.json`

### Mandatory References

- **File Placement**: See `.claude/docs/FILE_PLACEMENT_RULES.md`
- **Developer Workflow**: See `.claude/docs/DEVELOPER_WORKFLOW.md`
- **Artifact Naming**: See `.claude/docs/ARTIFACT_NAMING.md`

### Enforcement

File placement is enforced by `file-placement-guard.cjs` hook.
Invalid placements will be blocked in production mode.

---

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

Check for:

- Previously created schemas
- Known validation issues
- Schema naming conventions

**After completing:**

- New schema created -> Append to `.claude/context/memory/learnings.md`
- Validation issue found -> Append to `.claude/context/memory/issues.md`
- Architecture decision -> Append to `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.

## Iron Laws of Schema Creation

These rules are INVIOLABLE. Breaking them causes validation failures.

```
1. NO SCHEMA WITHOUT $schema FIELD
   - Every schema MUST declare its JSON Schema version
   - Use draft-07 or later: "$schema": "https://json-schema.org/draft-07/schema#"

2. NO SCHEMA WITHOUT title AND description
   - Every schema MUST be self-documenting
   - title: Short name of what it validates
   - description: Detailed explanation of purpose

3. NO PROPERTY WITHOUT description
   - Every property MUST have a description
   - Readers should understand field purpose without external docs

4. NO REQUIRED FIELD WITHOUT DEFINITION
   - If field is in "required" array, it MUST be in "properties"
   - Undefined required fields cause silent validation failures

5. NO ADDITIONALPROPERTIES: true WITHOUT REASON
   - Default to additionalProperties: false for strict validation
   - Only allow additional properties when explicitly needed

6. NO SCHEMA WITHOUT VALIDATION TEST
   - Test schema with valid AND invalid examples
   - Schema that passes everything validates nothing

7. NO CREATION WITHOUT SYSTEM IMPACT ANALYSIS
   - Check if related validators need updating
   - Check if documentation needs updating
   - Check if related schemas need cross-references

8. NO SCHEMA WITHOUT CLAUDE.MD REGISTRATION
   - If schema enables new capabilities, update CLAUDE.md
   - Section 4 (Self-Evolution) for agent/skill/workflow schemas
   - Verify with: grep "schema-name" .claude/CLAUDE.md
```

## Validation Checklist (Run After Every Creation)

```bash
# Verify schema is valid JSON
node -e "JSON.parse(require('fs').readFileSync('.claude/schemas/{name}.schema.json'))"

# Check required fields exist
node -e "const s = require('.claude/schemas/{name}.schema.json'); console.log('Has $schema:', !!s.\$schema); console.log('Has title:', !!s.title); console.log('Has description:', !!s.description);"

# Check all required properties are defined
node -e "const s = require('.claude/schemas/{name}.schema.json'); const r = s.required || []; const p = Object.keys(s.properties || {}); console.log('Missing:', r.filter(x => !p.includes(x)));"

# List all schemas
ls -la .claude/schemas/*.schema.json
```

**Completion Checklist** (all must be checked):

```
[ ] Schema file created with .schema.json extension
[ ] $schema field present (draft-07 or later)
[ ] title and description present
[ ] All properties have descriptions
[ ] required array matches defined properties
[ ] examples included for complex schemas
[ ] Schema validated with test data
[ ] System impact analysis completed
[ ] CLAUDE.md updated if schema enables new capabilities
[ ] Related schemas updated if needed ($ref links)
```

**BLOCKING**: If ANY item fails, schema creation is INCOMPLETE. All items must pass before proceeding.
