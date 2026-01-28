---
name: automation-quick-fix
description: Fast automation platform error resolver for Power Automate, n8n, Make, Zapier and other platforms. Handles common patterns like 401/403 auth errors, 429 throttling, and data format issues. Provides immediate fixes without deep research for well-known error patterns. Use when error matches common scenarios (status codes 401, 403, 404, 429, timeout, parse JSON failures). For complex or unknown errors, defer to automation-debugger skill. When the user outputs some code/json snippets and ask for a quick fix, this skill will provide immediate solutions.
---

# Automation Quick Fix

Fast-track resolver for common automation workflow error patterns across multiple platforms with immediate, proven solutions.

## Supported Platforms

- **Power Automate** (Microsoft)
- **n8n** (Open-source)
- **Make** (formerly Integromat)
- **Zapier**
- **Other JSON-based workflow platforms**

## Purpose

Provides rapid fixes for frequently encountered automation workflow errors across all platforms:
- Authentication errors (401/403)
- Throttling errors (429)
- Data format issues (JSON parsing, data transformation)
- Timeout errors
- Not found errors (404)
- Basic expression/formula errors

**When to use this skill**: Error matches a well-known pattern
**When to use automation-debugger instead**: Unknown error, complex scenario, or quick fix doesn't resolve

## Activation Triggers

Activates for messages like:
- "Quick fix for 429 error in SharePoint/API/webhook"
- "Fast solution for authentication error in n8n"
- "I'm getting throttled in Make, need immediate fix"
- "Parse JSON is failing in Zapier, quick help"
- "Function expects one parameter but was invoked with 2"
- "Unable to process template language expressions"
- "Fix this expression/filter/query/condition"
- User provides code snippet and asks for "quick fix" or "fix this"
- Status codes: 401, 403, 404, 429 with platform/connector context
- Platform-specific: "n8n node error", "Make scenario failing", "Power Automate action issue"

## ⚠️ IMPORTANT: Data Structure Check (NEW!)

**Before applying any quick fix**, quickly verify data structures in your flow:

### Quick Data Type Check
```javascript
// In filters/queries, check the where clause:

// Array of STRINGS (primitives):
"where": "@contains(item(), 'text')"  // ← item() without property

// Array of OBJECTS:
"where": "@contains(item()?['Name'], 'text')"  // ← item()?['Property']
```

**If your flow has data structure mismatches** (filter uses `item()` but loop uses `items('Loop')?['Property']`), this is NOT a quick fix scenario → use **automation-debugger** instead.

**Quick Fix applies to**: Authentication, throttling, timeouts, parse JSON, NOT structural bugs.

---

## Quick Fix Patterns

### Data Structure Mismatch (Quick Check - NEW!)

**Pattern Recognition**:
- Error: "Cannot evaluate property on undefined/null"
- Loop accessing `items('Loop')?['Property']` but source is array of strings

**Quick Diagnosis**:
```javascript
// Check your filter:
"where": "@contains(item(), 'value')"  // ← This means array of STRINGS!

// But loop tries:
"value": "@items('Loop')?['PropertyName']"  // ← ERROR: Can't access property on string!
```

**Quick Decision**:
- ❌ **NOT a quick fix** → Use **automation-debugger skill**
- This requires analyzing full data flow and structure
- Quick fix = known patterns; structural bugs = deep debugging

---

### Authentication Errors (401/403)

**Pattern Recognition**:
- Status: 401 or 403
- Keywords: "unauthorized", "forbidden", "access denied"

**Immediate Fix**:

```json
{
  "actions": {
    "Scope_With_Auth_Handling": {
      "type": "Scope",
      "actions": {
        "Your_Action": {
          "type": "ApiConnection",
          "inputs": { /* your config */ },
          "authentication": {
            "type": "Raw",
            "value": "@parameters('$connections')['shared_sharepointonline']['connectionId']"
          }
        }
      }
    },
    "Catch_Auth_Error": {
      "type": "Terminate",
      "inputs": {
        "runStatus": "Failed",
        "runError": {
          "code": "AuthenticationFailed",
          "message": "Please re-authenticate the connection in Power Automate"
        }
      },
      "runAfter": {
        "Scope_With_Auth_Handling": ["Failed"]
      }
    }
  }
}
```

**Instructions**:
1. Copy the Scope structure above
2. Replace "Your_Action" with your failing action
3. Update connection name if not SharePoint
4. Save and re-authenticate connection in Power Automate UI

---

### Throttling Errors (429)

**Pattern Recognition**:
- Status: 429
- Keywords: "TooManyRequests", "throttled", "rate limit"

**Immediate Fix - SharePoint/OneDrive**:

```json
{
  "actions": {
    "Apply_to_each_FIXED": {
      "type": "Foreach",
      "foreach": "@body('Get_items')?['value']",
      "runtimeConfiguration": {
        "concurrency": {
          "repetitions": 1
        }
      },
      "actions": {
        "Your_API_Action": {
          "type": "ApiConnection",
          "inputs": { /* your config */ },
          "runAfter": {}
        },
        "Delay_1_Second": {
          "type": "Wait",
          "inputs": {
            "interval": {
              "count": 1,
              "unit": "Second"
            }
          },
          "runAfter": {
            "Your_API_Action": ["Succeeded"]
          }
        }
      }
    }
  }
}
```

**Instructions**:
1. Find your Apply to each loop
2. Add `runtimeConfiguration.concurrency.repetitions: 1`
3. Add Delay action after API calls (1 second for SharePoint, 3 seconds for OneDrive)
4. Save and test

**Quick calculation**:
- SharePoint limit: 600/minute → 1-second delay = 60/minute (safe)
- OneDrive limit: 100/minute → 3-second delay = 20/minute (safe)

---

### Parse JSON Failures

**Pattern Recognition**:
- Error: "InvalidTemplate", "cannot be evaluated"
- Keywords: "Parse JSON", "dynamic content", "schema"

**Immediate Fix**:

```json
{
  "actions": {
    "Parse_JSON_FIXED": {
      "type": "ParseJson",
      "inputs": {
        "content": "@body('HTTP')",
        "schema": {
          "type": "object",
          "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "value": {"type": ["string", "null"]}
          }
        }
      }
    },
    "Safe_Access_Property": {
      "type": "Compose",
      "inputs": "@coalesce(body('Parse_JSON_FIXED')?['value'], 'default')",
      "runAfter": {
        "Parse_JSON_FIXED": ["Succeeded"]
      }
    }
  }
}
```

**Instructions**:
1. Add Parse JSON action with proper schema
2. Use `?['property']` for safe navigation (optional chaining)
3. Use `coalesce()` for default values with null properties
4. Test with sample payload first

**Schema generation tip**:
- Copy sample JSON response
- Use "Generate from sample" in Parse JSON action
- Add `"null"` to type array for optional fields: `{"type": ["string", "null"]}`

---

### Timeout Errors

**Pattern Recognition**:
- Error: "timeout", "timed out"
- Context: Large files, long operations, Do until loops

**Immediate Fix - Do Until**:

```json
{
  "actions": {
    "Do_until_FIXED": {
      "type": "Until",
      "expression": "@equals(variables('Complete'), true)",
      "limit": {
        "count": 60,
        "timeout": "PT1H"
      },
      "actions": {
        "Your_Action": {
          "type": "Compose",
          "inputs": "@variables('Data')"
        },
        "Check_Complete": {
          "type": "SetVariable",
          "inputs": {
            "name": "Complete",
            "value": "@greater(length(variables('Data')), 0)"
          },
          "runAfter": {
            "Your_Action": ["Succeeded"]
          }
        }
      }
    }
  }
}
```

**Instructions**:
1. Always set `limit.count` and `limit.timeout` in Do until
2. Recommended: count=60, timeout="PT1H" (1 hour)
3. Add exit condition that WILL eventually be true
4. Test with smaller iterations first

**Immediate Fix - Large Files**:

```json
{
  "actions": {
    "Check_File_Size_FIXED": {
      "type": "If",
      "expression": {
        "and": [{
          "lessOrEquals": [
            "@triggerBody()?['Size']",
            50000000
          ]
        }]
      },
      "actions": {
        "Process_Normal_File": {
          "type": "ApiConnection",
          "inputs": { /* your file action */ }
        }
      },
      "else": {
        "actions": {
          "Log_Large_File": {
            "type": "Compose",
            "inputs": "File over 50MB - skipping"
          }
        }
      }
    }
  }
}
```

**Instructions**:
1. Add file size check before processing
2. OneDrive: 50MB limit (50000000 bytes)
3. SharePoint attachments: 90MB limit (94371840 bytes)
4. Alternative: Use different API for large files

---

### Not Found Errors (404)

**Pattern Recognition**:
- Status: 404
- Keywords: "not found", "does not exist"

**Immediate Fix**:

```json
{
  "actions": {
    "Try_Get_Item": {
      "type": "Scope",
      "actions": {
        "Get_Item": {
          "type": "ApiConnection",
          "inputs": { /* your get action */ }
        }
      }
    },
    "Handle_Not_Found": {
      "type": "If",
      "expression": {
        "and": [{
          "equals": [
            "@result('Try_Get_Item')[0]['status']",
            "Failed"
          ]
        }]
      },
      "runAfter": {
        "Try_Get_Item": ["Failed", "Succeeded"]
      },
      "actions": {
        "Create_If_Missing": {
          "type": "ApiConnection",
          "inputs": { /* your create action */ }
        }
      },
      "else": {
        "actions": {
          "Use_Existing": {
            "type": "Compose",
            "inputs": "@body('Get_Item')"
          }
        }
      }
    }
  }
}
```

**Instructions**:
1. Wrap Get action in Scope
2. Check result status with `result()` function
3. Create item if not found (or handle alternative)
4. Use dynamic IDs from previous actions (don't hardcode)

---

### Expression Errors

**Pattern Recognition**:
- Error: "Unable to process template language expressions"
- Keywords: "property doesn't exist", "invalid expression"

**Common Quick Fixes**:

**Missing Property**:
```javascript
// BAD
@body('Get_Item')['MissingProperty']

// GOOD
@body('Get_Item')?['MissingProperty']

// BETTER (with default)
@coalesce(body('Get_Item')?['MissingProperty'], 'default_value')
```

**Type Mismatch**:
```javascript
// BAD - concatenating string and number
@concat('Value: ', variables('NumberVariable'))

// GOOD
@concat('Value: ', string(variables('NumberVariable')))
```

**Array Access**:
```javascript
// BAD - array might be empty
@first(body('Get_Items')?['value'])

// GOOD
@if(greater(length(body('Get_Items')?['value']), 0), first(body('Get_Items')?['value']), null)
```

**Null Checks**:
```javascript
// BAD
@variables('NullableVar')

// GOOD
@if(empty(variables('NullableVar')), 'default', variables('NullableVar'))
```

**Function Parenthesis Placement** (NEW!):
```javascript
// BAD - format parameter outside formatDateTime()
toLower(formatDateTime(outputs('Action')?['body/Date'], 'yyyy-MM'))
//                                                     ↑
//                              This closes formatDateTime BEFORE format string!

// ERROR MESSAGE:
// "The template language function 'toLower' expects one parameter:
//  the string to convert to lower casing. The function was invoked with '2' parameters."

// GOOD - format parameter INSIDE formatDateTime()
toLower(formatDateTime(outputs('Action')?['body/Date'], 'yyyy-MM'))
//                                                      ↑
//                          Format string is now INSIDE formatDateTime()
```

**Copy-Paste Fix for Filter Query**:
```javascript
// Original (broken):
@and(
  contains(toLower(item()), 'cnesst'),
  contains(
    toLower(item()),
    toLower(formatDateTime(outputs('Ajouter_une_ligne_à_un_tableau')?['body/Date d''événement CNESST']),'yyyy-MM'))
  )

// Fixed expression (ready to copy-paste into Filter Query action):
@and(
  contains(toLower(item()), 'cnesst'),
  contains(
    toLower(item()),
    toLower(formatDateTime(outputs('Ajouter_une_ligne_à_un_tableau')?['body/Date d''événement CNESST'], 'yyyy-MM'))
  )
)
```

---

## Quick Fix Decision Tree

```
Error Code/Type
│
├── Data Structure Mismatch (item() vs item()?['Prop']) → ❌ Use automation-debugger (NOT quick fix)
│
├── 401/403 → Re-authenticate connection + Add error handling
│
├── 429 → Set concurrency=1 + Add delays
│
├── 404 → Add existence check + Handle not found case
│
├── Timeout → Add limits to Do until OR check file sizes
│
├── Parse JSON → Add schema + Use safe navigation (?[])
│
└── Expression Errors
    ├── "Function expects N parameters but was invoked with M" → Check parenthesis placement
    ├── Missing/null properties → Add ?[] + coalesce()
    ├── Type mismatch → Add string(), int() conversions
    └── Array access → Add length checks + first()/last()
```

## When Quick Fix Isn't Enough

Escalate to automation-debugger skill if:
- Quick fix doesn't resolve the error
- Error doesn't match common patterns
- Multiple interrelated errors
- Complex flow logic involved
- Need deep documentation research
- Unclear root cause

## Output Format

Quick fixes provide:
1. **Pattern identification** (which common error)
2. **Immediate fix** (JSON snippet for actions/nodes)
3. **Copy-paste ready expressions** (for Filter Query, Condition, Variable, etc.) - ALWAYS include the complete @{...} expression ready to copy directly into Power Automate
4. **Instructions** (how to apply)
5. **Validation** (how to test)

**IMPORTANT**: For expression errors (Filter Query, Condition, Variable, Compose, etc.), ALWAYS provide:
- ❌ **Original (broken)**: The full broken expression
- ✅ **Fixed expression**: The complete corrected expression ready to copy-paste

**Example output format**:
```
Quick Fix: Function Parenthesis Placement Error

Pattern: formatDateTime() format parameter placed outside function call

Original (broken):
@and(contains(toLower(item()), 'text'), contains(toLower(item()), toLower(formatDateTime(outputs('Action')?['body/Date']),'yyyy-MM')))

Fixed expression (copy-paste ready):
@and(contains(toLower(item()), 'text'), contains(toLower(item()), toLower(formatDateTime(outputs('Action')?['body/Date'], 'yyyy-MM'))))

What changed: Moved 'yyyy-MM' format string INSIDE formatDateTime() parentheses
```

No need for full debug report structure - focus on speed and copy-paste ready fixes.

## Best Practices

1. **Test first**: Apply quick fix to copy of flow
2. **Verify limits**: Confirm connector-specific constraints
3. **Monitor**: Check flow run history after fix
4. **Escalate if needed**: Use automation-debugger for persistent issues

## Common Connector Limits (Quick Reference)

| Connector | API Limit | Recommended Delay |
|-----------|-----------|-------------------|
| SharePoint | 600/60s | 1 second |
| OneDrive | 100/60s | 3 seconds |
| HTTP | 600/60s | 1 second |
| Apply to each | 50 concurrent | Set to 1 for APIs |

## Examples

**User**: "I'm getting throttled in SharePoint, need quick fix"

**Output**:
```
Quick Fix: SharePoint Throttling (429)

Reduce concurrency and add delays:

[JSON snippet with concurrency + delay]

Apply these changes:
1. Set concurrency to 1
2. Add 1-second delay
3. Save and test

This limits you to 60 API calls/minute (well under 600/minute limit).
```

**User**: "Parse JSON failing with 'property doesn't exist'"

**Output**:
```
Quick Fix: Parse JSON Property Access

Use safe navigation (?[]) and defaults:

[JSON snippet with coalesce()]

Changes needed:
1. Replace ['property'] with ?['property']
2. Add coalesce() for defaults
3. Test with sample data

This handles null/missing properties gracefully.
```

**User**: "Getting error 'toLower expects one parameter but was invoked with 2 parameters' in my Filter Query"

**Output**:
```
Quick Fix: Function Parenthesis Placement Error

Pattern: formatDateTime() format parameter placed outside function call

Original (broken):
@and(
  contains(toLower(item()), 'cnesst'),
  contains(
    toLower(item()),
    toLower(formatDateTime(outputs('Ajouter_une_ligne_à_un_tableau')?['body/Date d''événement CNESST']),'yyyy-MM'))
  )

Fixed expression (copy-paste ready):
@and(
  contains(toLower(item()), 'cnesst'),
  contains(
    toLower(item()),
    toLower(formatDateTime(outputs('Ajouter_une_ligne_à_un_tableau')?['body/Date d''événement CNESST'], 'yyyy-MM'))
  )
)

What changed:
1. Moved 'yyyy-MM' format string INSIDE formatDateTime() parentheses (before the closing parenthesis)
2. The format parameter is now the second parameter of formatDateTime(), not a second parameter to toLower()

How to apply:
1. Open your Filter Query action in Power Automate
2. Delete the current expression
3. Paste the fixed expression above
4. Save and test with your data
```

---

## Integration with Other Skills

- **Quick fix succeeds** → Done!
- **Quick fix fails** → Automatically suggest automation-debugger
- **Unknown error** → Immediately defer to automation-debugger

This skill optimizes for speed on common patterns while maintaining quality through specialized skill delegation when needed.

---

**Version**: 1.2
**Last Updated**: 2025-10-31

## Changelog

### Version 1.2 (2025-10-31)

**Major Enhancements**:
- ✅ Added **Function Parenthesis Placement Error** pattern to Expression Errors
- ✅ Enhanced **Output Format** to emphasize copy-paste ready expressions for all expression types
- ✅ Updated **Activation Triggers** to include expression error patterns
- ✅ Expanded **Decision Tree** with detailed expression error breakdown
- ✅ Added **complete example** showing function parenthesis error fix

**Key Additions**:
- Function parameter placement detection (e.g., `toLower(formatDateTime(...), 'format')` → error)
- Copy-paste ready expression format with ❌ broken / ✅ fixed sections
- Direct support for Filter Query, Condition, Variable, Compose expression fixes
- Clear before/after comparison showing exactly what changed

**New Triggers**:
- "Function expects one parameter but was invoked with 2"
- "Unable to process template language expressions"
- "Fix this expression/filter/query/condition"
- User provides code snippet and asks for "quick fix"

**Output Philosophy**:
- Always provide complete, ready-to-paste expressions
- Show original (broken) and fixed versions side-by-side
- Explain exactly what changed and why
- Include step-by-step application instructions

### Version 1.1 (2025-10-31)

**Minor Improvements**:
- ✅ Added **Data Structure Check section** - Quick validation before applying fixes
- ✅ Added **Data Structure Mismatch pattern** - Recognizes when NOT to quick fix
- ✅ Updated **Decision Tree** - Now includes structural bug detection
- ✅ Clarified escalation to **automation-debugger** for structural issues

**Key Additions**:
- Quick data type check: `item()` vs `item()?['Property']` indicator
- Clear guidance on when quick fix is inappropriate
- Structural bugs (string vs object mismatch) → Use automation-debugger

**Philosophy**:
- Quick fixes are for **known, simple patterns**
- Data structure bugs require **deep analysis** → Not quick fix territory
- Fast triage: Recognize when to escalate immediately
