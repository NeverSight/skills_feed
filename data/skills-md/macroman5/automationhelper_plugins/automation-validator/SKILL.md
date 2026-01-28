---
name: automation-validator
description: Validates automation workflow JSON before deployment for Power Automate, n8n, Make, Zapier and other platforms. Checks syntax, structure, best practices, and potential issues. Analyzes workflow JSON files for platform compliance, missing error handling, performance issues, and security concerns. Use when user wants to validate, review, or check a workflow before deployment/import.
allowed-tools: Read, Grep, Glob
---

# Automation Workflow Validator

Comprehensive pre-deployment validator for automation workflow JSON definitions across multiple platforms.

## Supported Platforms

- **Power Automate** (Microsoft)
- **n8n** (Open-source)
- **Make** (formerly Integromat)
- **Zapier**
- **Other JSON-based workflow platforms**

## Purpose

Validates automation workflows against:
1. **Syntax correctness** - Valid JSON, proper structure
2. **Platform compliance** - Schema, required fields, valid operations (platform-specific)
3. **Best practices** - Error handling, performance, reliability
4. **Security** - Hardcoded credentials, injection risks
5. **Documentation compliance** - Connector/node limits, known constraints

## When This Skill Activates

Triggers on:
- "Validate this workflow JSON"
- "Check this workflow JSON before deployment"
- "Review my workflow JSON for [platform]"
- "Is this flow ready to paste into Power Automate/n8n/Make?"
- "Validate my n8n workflow"
- "Lint this automation"
- "Pre-deployment check"
- **Workflow JSON files** - Any JSON with workflow/flow/automation context (examples: flow.json, workflow.json, scenario.json, automation.json, fixed_flow.json)

## Validation Checklist

### 1. Syntax Validation

**JSON Structure**:
- [ ] Valid JSON syntax (balanced brackets, proper escaping)
- [ ] No trailing commas
- [ ] Proper string escaping for expressions
- [ ] No invalid characters

**Power Automate Schema**:
- [ ] Correct $schema URL
- [ ] Required root elements: definition, schemaVersion
- [ ] Parameters include $connections
- [ ] Valid contentVersion format

**Structure**:
```json
{
  "definition": {
    "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
    "contentVersion": "1.0.0.0",
    "parameters": { /* Required */ },
    "triggers": { /* Required */ },
    "actions": { /* Required */ },
    "outputs": {}
  },
  "schemaVersion": "1.0.0.0"
}
```

### 2. Triggers Validation

**Required Fields**:
- [ ] At least one trigger defined
- [ ] Trigger has "type" field
- [ ] Trigger has "inputs" object
- [ ] Valid trigger types: Request, Recurrence, ApiConnection, etc.

**Common Issues**:
- Missing "kind" in Request triggers
- Invalid recurrence frequency
- Missing required parameters for ApiConnection triggers

**Example Check**:
```json
// GOOD
"triggers": {
  "manual": {
    "type": "Request",
    "kind": "Button",  // Required for manual triggers
    "inputs": {
      "schema": {}
    }
  }
}

// BAD - missing kind
"triggers": {
  "manual": {
    "type": "Request",
    "inputs": {}
  }
}
```

### 3. Actions Validation

**Required Fields**:
- [ ] Each action has "type"
- [ ] Each action has "inputs"
- [ ] Each action has "runAfter" (or is first action)
- [ ] Valid action types

**runAfter Chain**:
- [ ] No orphaned actions (all connected to trigger)
- [ ] No circular dependencies
- [ ] runAfter references exist
- [ ] Proper status values: Succeeded, Failed, Skipped, TimedOut

**GUID Validation**:
- [ ] All GUIDs are valid format (if present)
- [ ] No duplicate GUIDs
- [ ] operationMetadataId unique per action

**Example Check**:
```json
// GOOD
"actions": {
  "Action_1": {
    "type": "Compose",
    "inputs": "test",
    "runAfter": {}  // First action
  },
  "Action_2": {
    "type": "Compose",
    "inputs": "test2",
    "runAfter": {
      "Action_1": ["Succeeded"]  // References existing action
    }
  }
}

// BAD - Action_2 references non-existent action
"actions": {
  "Action_2": {
    "type": "Compose",
    "inputs": "test",
    "runAfter": {
      "NonExistent": ["Succeeded"]
    }
  }
}
```

### 4. Expression Validation

**Common Expression Errors**:
- [ ] All expressions start with @
- [ ] Proper function syntax
- [ ] Valid function names
- [ ] Correct parameter counts
- [ ] Proper string quoting inside expressions

**Check Patterns**:
```javascript
// GOOD
"@body('Get_Item')?['property']"
"@concat('Hello ', variables('Name'))"
"@if(equals(1, 1), 'true', 'false')"

// BAD
"body('Get_Item')['property']"  // Missing @
"@concat(Hello, variables('Name'))"  // Unquoted string
"@if(equals(1, 1) 'true', 'false')"  // Missing comma
```

**Safe Navigation**:
- [ ] Use ?[] for optional properties
- [ ] Null checks for nullable values
- [ ] Default values with coalesce()

### 4.5. Data Structure Validation (NEW!)

**CRITICAL CHECK**: Verify data type consistency throughout flow

**Array Type Consistency**:
- [ ] Check Query/Filter actions for data type indicators
- [ ] Verify `item()` vs `item()?['Property']` usage consistency
- [ ] Validate loop `items()` usage matches source data structure
- [ ] Ensure Select actions output correct structure

**Pattern Detection**:
```javascript
// INCONSISTENT (BUG RISK):
// Filter uses:
"where": "@contains(item(), 'text')"  // ← Array of strings

// But loop uses:
"value": "@items('Loop')?['PropertyName']"  // ← Accessing property on string = ERROR

// CONSISTENT (CORRECT):
// Filter uses:
"where": "@contains(item(), 'text')"  // ← Array of strings

// Loop uses:
"value": "@items('Loop')"  // ← Direct string access = CORRECT
```

**Validation Checks**:
- [ ] All Query actions: Check if `where` uses `item()` or `item()?['Prop']`
- [ ] All Foreach loops: Verify `items()` access matches source type
- [ ] All Select actions: Verify mappings create expected structure
- [ ] Cross-reference: Filter → Loop → SetVariable consistency

**Common Bugs to Detect**:
```json
// BUG PATTERN 1: Property access on primitives
{
  "Filter": {
    "where": "@contains(item(), 'value')"  // String array
  },
  "Loop": {
    "foreach": "@body('Filter')",
    "actions": {
      "BugAction": {
        "value": "@items('Loop')?['Nom']"  // ❌ ERROR: Can't access property on string
      }
    }
  }
}

// BUG PATTERN 2: Empty Select mapping
{
  "Select": {
    "select": {
      "Nom": ""  // ❌ ERROR: Empty mapping creates useless output
    }
  }
}

// BUG PATTERN 3: Inconsistent data access
{
  "Compose1": {
    "inputs": "@item()?['Name']"  // Expects objects
  },
  "Compose2": {
    "inputs": "@item()"  // Treats as primitives
  }
  // ❌ ERROR: Inconsistent - which is it?
}
```

**Validation Actions**:
- ⚠️ **WARNING** if data structure inconsistency detected
- ⚠️ **WARNING** if Select action has empty mappings
- ⚠️ **WARNING** if `item()` usage is inconsistent across actions
- ❌ **ERROR** if property access clearly mismatches source type

### 5. Best Practices Validation

**Error Handling**:
- [ ] Critical actions wrapped in Scope
- [ ] Scope has corresponding error handler
- [ ] Error handler uses "Configure run after"
- [ ] Proper handling of Failed, TimedOut states

**Example**:
```json
"Scope_Main": {
  "type": "Scope",
  "actions": { /* critical actions */ }
},
"Handle_Errors": {
  "type": "Compose",
  "inputs": "Error occurred",
  "runAfter": {
    "Scope_Main": ["Failed", "TimedOut"]
  }
}
```

**Performance**:
- [ ] Apply to each has concurrency configured for API calls
- [ ] Delays present in loops with API calls
- [ ] Filtering at source (not in Apply to each)
- [ ] Do until has timeout and count limits

**Reliability**:
- [ ] Retry policies for transient errors
- [ ] Idempotent operations where possible
- [ ] Proper timeout configuration
- [ ] Variable initialization at flow start

### 6. Security Validation

**Critical Issues**:
- [ ] No hardcoded passwords or API keys
- [ ] No hardcoded connection strings
- [ ] Credentials use secure parameters
- [ ] Sensitive data not logged in plain text

**Check for**:
```json
// BAD - hardcoded credentials
"inputs": {
  "authentication": {
    "password": "MyPassword123",  // SECURITY ISSUE
    "username": "admin@contoso.com"
  }
}

// GOOD - parameterized
"inputs": {
  "authentication": {
    "password": "@parameters('$connections')['connection']['password']",
    "username": "@parameters('$connections')['connection']['username']"
  }
}
```

**Injection Risks**:
- [ ] User input sanitized
- [ ] SQL queries parameterized
- [ ] Dynamic URLs validated
- [ ] File paths validated

### 7. Connector-Specific Validation

**SharePoint**:
- [ ] API calls respect 600/60s limit
- [ ] Delays present in loops
- [ ] List names don't contain periods
- [ ] Attachment size checks (90MB)

**OneDrive**:
- [ ] API calls respect 100/60s limit
- [ ] File size checks (50MB for triggers)
- [ ] Proper delays (3 seconds recommended)

**HTTP**:
- [ ] Timeout configured
- [ ] Retry policy for transient failures
- [ ] Authentication configured
- [ ] URL validation for user input

**Control (Apply to each)**:
- [ ] Concurrency set for API operations
- [ ] Max 5000 items (default)
- [ ] Proper error handling inside loop

**Do Until**:
- [ ] Timeout configured
- [ ] Count limit configured
- [ ] Exit condition will eventually be true

### 8. Documentation Compliance

**Reference PowerAutomateDocs**:
- [ ] Actions use documented parameters
- [ ] Respect documented limitations
- [ ] Follow recommended patterns
- [ ] Match documented examples

**Check against**:
- PowerAutomateDocs/{Connector}/overview.md → Limitations
- PowerAutomateDocs/{Connector}/actions.md → Parameters
- PowerAutomateDocs/BuiltIn/ → Built-in connector patterns

## Validation Output Format

```markdown
# Power Automate Flow Validation Report

## Overall Status: ✅ PASS / ⚠️ WARNINGS / ❌ FAIL

---

## Syntax Validation
**Status**: ✅ Pass

- ✅ Valid JSON syntax
- ✅ Correct Power Automate schema
- ✅ All required root elements present

---

## Structure Validation
**Status**: ✅ Pass

### Triggers
- ✅ 1 trigger defined: "manual"
- ✅ Trigger type valid: Request
- ✅ Required fields present

### Actions
- ✅ 5 actions defined
- ✅ All actions have required fields
- ✅ runAfter chain valid (no orphans)
- ✅ No circular dependencies

---

## Best Practices
**Status**: ⚠️ Warnings

### Error Handling
- ⚠️ **Missing error handling** for "Get_Items" action
  - Recommendation: Wrap in Scope with error handler
  - Impact: Flow fails completely on error

### Performance
- ✅ Apply to each has concurrency configured
- ⚠️ **No delay in API loop**
  - Recommendation: Add 1-second delay after "Get_Items"
  - Impact: Risk of throttling (429 errors)

### Reliability
- ✅ Variables initialized
- ✅ Do until has timeout configured

---

## Security
**Status**: ✅ Pass

- ✅ No hardcoded credentials
- ✅ Using connection parameters
- ✅ No SQL injection risks
- ✅ Sensitive data properly handled

---

## Connector-Specific
**Status**: ⚠️ Warnings

### SharePoint (Get Items)
- ⚠️ **Throttling risk**: 100 iterations with no delays
  - Limit: 600 calls/60 seconds
  - Recommendation: Add 1-second delay or reduce concurrency
  - Reference: PowerAutomateDocs/SharePoint/overview.md

- ✅ Attachment size checks present
- ✅ List names valid (no periods)

---

## Critical Issues: 0
## Warnings: 3
## Passed Checks: 28

---

## Recommendations (Priority Order)

### High Priority
1. **Add error handling for Get_Items**
   ```json
   "Scope_GetItems": {
     "type": "Scope",
     "actions": {
       "Get_Items": { /* existing action */ }
     }
   },
   "Handle_Errors": {
     "runAfter": {
       "Scope_GetItems": ["Failed", "TimedOut"]
     }
   }
   ```

2. **Add delay to prevent throttling**
   ```json
   "Delay": {
     "type": "Wait",
     "inputs": {
       "interval": {
         "count": 1,
         "unit": "Second"
       }
     },
     "runAfter": {
       "Get_Items": ["Succeeded"]
     }
   }
   ```

### Medium Priority
3. **Add timeout to HTTP action**
   - Current: No timeout (default 2 minutes)
   - Recommended: Explicit timeout configuration

---

## Ready for Deployment?

✅ **YES** - Flow is syntactically valid and can be pasted into Power Automate

⚠️ **WITH WARNINGS** - Flow will work but has performance/reliability risks

❌ **NO** - Critical issues must be fixed before deployment

---

## Next Steps

1. Review warnings above
2. Apply high-priority recommendations
3. Test with sample data
4. Monitor first runs for issues
5. Revisit validation after changes

---

## Validation Metadata

- Validated: [timestamp]
- Flow Actions: 5
- Triggers: 1
- Connectors Used: SharePoint, Control
- Total Checks: 31
```

## Validation Levels

### Level 1: Syntax (Blocking)
**Must pass** - Flow won't paste into Power Automate
- Invalid JSON
- Missing required structure
- Invalid schema

### Level 2: Structure (Blocking)
**Must pass** - Flow won't run
- Invalid runAfter chains
- Missing action types
- Invalid expression syntax

### Level 3: Best Practices (Warnings)
**Should fix** - Flow runs but has risks
- Missing error handling
- No throttling mitigation
- Poor performance patterns

### Level 4: Optimization (Suggestions)
**Nice to have** - Improvements
- Better variable naming
- More efficient queries
- Enhanced logging

## Quick Validation Commands

For specific checks without full validation:

### Check Syntax Only
```
"Validate JSON syntax in workflow JSON"
```

### Check Best Practices Only
```
"Review best practices in this flow"
```

### Check Specific Connector
```
"Validate SharePoint usage in workflow JSON"
```

### Security Scan Only
```
"Security scan this Power Automate flow"
```

## Integration with Other Skills

**Before using workflow-builder**:
- Validate requirements are complete
- Check for known limitations

**After using automation-debugger**:
- Validate the fixed workflow JSON
- Ensure all issues resolved
- Verify no new issues introduced

**Before deployment**:
- Always run full validation
- Review warnings
- Document any accepted risks

## Common Validation Failures

### 1. Missing runAfter
```json
// FAIL
"actions": {
  "Action_2": {
    "type": "Compose",
    "inputs": "test"
    // Missing runAfter
  }
}
```
**Fix**: Add `"runAfter": {}` for first action or reference predecessor

### 2. Invalid Expression
```json
// FAIL
"inputs": "@body('Get_Item')['property']"  // Will fail if property missing
```
**Fix**: `"@body('Get_Item')?['property']"` with safe navigation

### 3. No Error Handling
```json
// FAIL
"Get_Items": { /* API call with no error handling */ }
```
**Fix**: Wrap in Scope with error handler

### 4. Throttling Risk
```json
// FAIL
"Apply_to_each": {
  "foreach": "@range(0, 1000)",  // 1000 API calls
  "runtimeConfiguration": {
    "concurrency": {
      "repetitions": 50  // 50 parallel
    }
  }
}
```
**Fix**: Reduce concurrency to 1, add delays

### 5. Missing Timeout
```json
// FAIL
"Do_until": {
  "expression": "@equals(variables('Done'), true)"
  // No limit
}
```
**Fix**: Add `"limit": {"count": 60, "timeout": "PT1H"}`

## Best Practices Enforcement

Enable strict mode for production flows:
- All errors must have handlers
- All loops must have limits
- All API calls must have delays
- All expressions must be safe
- No hardcoded values
- Full documentation compliance

## Examples

**User**: "Validate my workflow JSON before I paste it"

**Skill Response**:
1. Reads workflow JSON file
2. Runs all validation checks
3. Generates detailed report
4. Highlights critical issues
5. Provides fix recommendations
6. Gives deployment readiness status

**User**: "Quick syntax check on my fixed workflow JSON"

**Skill Response**:
1. Reads workflow JSON file
2. Validates JSON syntax
3. Checks platform-specific schema
4. Confirms structure validity
5. Returns pass/fail status

## Supporting Files

See also:
- [Power Automate JSON Format](../../../PowerAutomateDocs/platform-specific format documentation) - Schema requirements
- [Error Patterns](../automation-debugger/ERROR-PATTERNS.md) - Common issues to check for
- [Repository Guide](../../../CLAUDE.md) - Full documentation standards

---

**Version**: 1.1
**Last Updated**: 2025-10-31

## Changelog

### Version 1.1 (2025-10-31)

**Major Improvements**:
- ✅ Added **Section 4.5: Data Structure Validation** (NEW!) - Validates data type consistency
- ✅ Detects **property access on primitives** (critical bug pattern)
- ✅ Validates **Select action mappings** for empty/incorrect values
- ✅ Checks **Filter → Loop → SetVariable consistency**
- ✅ Identifies **`item()` vs `item()?['Property']` mismatches**

**New Validation Checks**:
- Array type consistency validation
- Query/Filter pattern detection (`item()` vs `item()?['Prop']`)
- Foreach loop data access validation
- Select action output structure verification
- Cross-action data flow consistency

**Bug Patterns Now Detected**:
1. Property access on string primitives (`items('Loop')?['Prop']` on string array)
2. Empty Select mappings (`"Nom": ""`)
3. Inconsistent data access patterns across actions

**Impact**:
- Catches critical structural bugs before deployment
- Prevents runtime errors from data type mismatches
- Reduces failed deployments due to data structure issues
- Complements automation-debugger for pre-deployment validation
