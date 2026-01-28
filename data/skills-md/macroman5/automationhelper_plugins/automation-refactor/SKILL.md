---
name: automation-refactor
description: Expert automation workflow refactoring tool for Power Automate, n8n, Make, Zapier and other platforms. Optimizes existing flows by improving performance, reliability, maintainability, and best practices compliance. Triggers when user wants to improve, optimize, refactor, correct values, enhance, or modernize workflows. Analyzes JSON, suggests improvements, outputs refactored flow maintaining original functionality unless changes requested.
---

# Automation Refactor

Expert system for refactoring and optimizing automation workflows across multiple platforms while maintaining functional equivalence and improving code quality.

## Supported Platforms

- **Power Automate** (Microsoft)
- **n8n** (Open-source automation)
- **Make** (formerly Integromat)
- **Zapier**
- **Other JSON-based workflow platforms**

## Purpose

This skill provides comprehensive workflow refactoring by:
1. Analyzing existing workflow JSON for improvement opportunities
2. Applying platform-specific best practices from documentation (Docs/ directory)
3. Optimizing performance, reliability, and maintainability
4. Generating refactored JSON that maintains original functionality
5. Providing detailed report of changes and additional optimization suggestions
6. Ensuring no hallucinations by strictly referencing platform documentation

## Common Pitfalls to AVOID

### ❌ CRITICAL ERROR #1: Assuming Data Structures (Most Common!)

**The Mistake**:
```json
// You see a variable used in a filter
"where": "@contains(item(), 'keyword')"

// And you ASSUME it's an array of objects, so you write:
"value": "@items('Loop')?['PropertyName']"  // ← WRONG!
```

**The Reality**:
```json
// item() without property → Array of STRINGS!
// Correct usage:
"value": "@items('Loop')"  // ← RIGHT!
```

**How to Avoid**:
1. **ALWAYS look at the filter's `where` clause first**
2. `item()` = array of primitives (strings/numbers)
3. `item()?['Prop']` = array of objects
4. **Ask user if unsure** - never guess!

---

### ❌ ERROR #2: Not Researching Documentation

**The Mistake**: Guessing connector outputs, property names, or behaviors

**How to Avoid**:
1. Search local Docs/ directory FIRST
2. Use WebSearch for official docs if not found locally
3. Ask user to confirm if documentation is unclear
4. Reference specific documentation sections in your output

---

### ❌ ERROR #3: Overconfidence Without Validation

**The Mistake**: Providing fixes without verifying against actual data structures

**How to Avoid**:
1. Complete Phase 0 (Data Structure Analysis) BEFORE any changes
2. Use AskUserQuestion tool when ambiguous
3. Test your logic against the actual data flow
4. Verify all `item()` / `items()` usages match data types

---

## When This Skill Activates

Automatically activates when user requests:
- **Optimization keywords**: "optimize", "improve", "enhance", "refactor", "modernize"
- **Correction keywords**: "correct", "fix values", "update parameters", "change configuration"
- **Performance keywords**: "make faster", "reduce API calls", "improve performance"
- **Best practices**: "apply best practices", "follow standards", "clean up"
- **Maintenance**: "simplify", "make more readable", "reduce complexity"
- **Provides flow JSON**: User shares workflow JSON asking for improvements
- **Platform-specific**: "refactor my Power Automate flow", "optimize this n8n workflow", "improve Make scenario"

**Examples of triggering phrases**:
- "Optimize this flow to reduce API calls"
- "Refactor this workflow to follow best practices"
- "Improve the error handling in this flow"
- "Make this automation more reliable"
- "Correct the values in this flow"
- "Enhance this workflow's performance"
- "Simplify this complex flow"
- "Modernize this old workflow"

## Core Workflow

### Phase 0: Data Structure Analysis (CRITICAL)

**NEVER assume data structures without verification**. Before any refactoring, ALWAYS analyze the actual data structures in the flow.

1. **Examine Variable Declarations**
   - Check all variable initializations to understand data types
   - Look for: `"type": "Array"`, `"type": "String"`, `"type": "Object"`
   - Document the structure of each variable

2. **Analyze Filter/Query Operations**
   - **CRITICAL CHECK**: Look at `where` clauses in Query actions
   - If you see `item()` without property access → **Array of primitives (strings/numbers)**
     ```json
     "where": "@contains(toLower(item()), 'keyword')"
     // ↑ This means: Array of strings, NOT array of objects!
     ```
   - If you see `item()?['PropertyName']` → **Array of objects**
     ```json
     "where": "@contains(item()?['Name'], 'keyword')"
     // ↑ This means: Array of objects with 'Name' property
     ```

3. **Trace Data Sources**
   - Follow `from` parameter in Query actions back to source
   - Check SharePoint GetFileItems/GetItems outputs
   - Check Select action mappings (these define output structure)
   - Verify Compose action inputs

4. **Validate Item Access Patterns**
   - In loops: `items('LoopName')` vs `items('LoopName')?['Property']`
   - In filters: `item()` vs `item()?['Property']`
   - **MISMATCH = BUG**: If filter uses `item()` but loop uses `items('Loop')?['Prop']` → ERROR!

5. **Ask User When Uncertain** (Use AskUserQuestion tool)
   - If data structure is ambiguous
   - If documentation doesn't clarify the structure
   - If multiple interpretations are possible

   **Example questions to ask**:
   - "I see your filter uses `contains(item(), 'keyword')`. Does this mean your variable contains an array of strings like `['string1', 'string2']`, or does it contain an array of objects?"
   - "Can you confirm whether the output from [ActionName] is an array of strings or an array of objects with properties?"
   - "I notice a mismatch: the filter treats data as strings but the loop accesses it as objects. Which is correct?"

### Phase 1: Initial Analysis

1. **Extract Flow Information**
   - Parse the provided JSON (flow.json or workflow snippet)
   - Identify platform (Power Automate, n8n, Make, Zapier, etc.)
   - Map all triggers, actions, and dependencies
   - Understand the flow's purpose and logic
   - Note current configuration and parameters

2. **Identify User Requirements**
   - Parse user's refactoring brief/request
   - Determine specific changes requested (if any)
   - Identify optimization goals (performance, reliability, maintainability)
   - Note constraints (must maintain functionality, specific requirements)

3. **Baseline Documentation**
   - Document current flow behavior
   - List all connectors/nodes used
   - Map data flow and transformations
   - Note existing error handling (or lack thereof)

### Phase 2: Comprehensive Analysis (Multi-Source Research)

**CRITICAL**: Always research thoroughly before making changes. Use multiple sources in this order:

#### Step 1: Local Documentation Research (Use Task Tool with Explore Agent)

Launch research sub-agent with thorough investigation:

```
Use Task tool with subagent_type="Explore" and thoroughness="very thorough"

Prompt: "Research [PLATFORM] best practices and optimization guidelines for workflow refactoring, focusing on [CONNECTORS/NODES USED].

Platform: [Power Automate / n8n / Make / Zapier / Other]

Search in Docs/ directory for:
1. Platform best practices documentation (Docs/{Platform}_Documentation/)
2. Connector/node-specific optimization guidelines
3. Data structure specifications (what properties exist, array vs object)
4. Common performance anti-patterns
5. Error handling best practices
6. API rate limit optimization strategies
7. Expression/formula optimization patterns
8. Security best practices

Focus on finding:
- **DATA STRUCTURE DETAILS** (output schemas, property names, data types)
- Performance optimization opportunities
- Reliability improvements (error handling, retry logic)
- Maintainability enhancements (naming, structure, comments)
- Security improvements (credential handling, input validation)
- API efficiency (batching, filtering, pagination)
- Platform-specific recommendations

For each connector/node in the flow, find:
- Output schema/structure (CRITICAL!)
- Recommended configuration patterns
- Known limitations to consider
- Optimization techniques
- Common mistakes to avoid

Return specific file paths, sections, and exact recommendations."
```

**Expected Output from Research Agent**:
- Data structure specifications (schemas, property names)
- Best practices documentation references
- Connector-specific optimization guidelines
- Performance improvement patterns
- Error handling recommendations
- Security considerations
- Platform-specific optimizations

#### Step 2: Web Research (Use WebSearch Tool - If Local Documentation Insufficient)

**ONLY if local documentation doesn't provide needed information**, use WebSearch:

```
Use WebSearch tool with targeted queries:

Examples:
- "Power Automate GetFileItems output schema properties"
- "Power Automate array of strings vs array of objects filter syntax"
- "n8n HTTP Request node output structure"
- "Make iterator data structure format"

Search for:
- Official Microsoft Learn documentation
- Platform-specific forums (Power Users Community)
- Official API documentation
- Verified Stack Overflow answers (check dates!)
```

**Validation Requirements**:
- Prefer official documentation over community posts
- Cross-reference multiple sources
- Verify information is current (check dates)
- Test with user if uncertain

#### Step 3: Ask User for Clarification (Use AskUserQuestion Tool)

**If both local docs and web search are unclear**, ask the user:

```
Use AskUserQuestion tool with specific questions:

Example:
{
  "questions": [{
    "question": "Your flow uses `contains(item(), 'CNESST')`. Can you confirm what type of data is in your variable?",
    "header": "Data Type",
    "options": [
      {
        "label": "Array of strings",
        "description": "Like ['CNESST 2025-01', 'INVALIDITÉ 2025-02']"
      },
      {
        "label": "Array of objects",
        "description": "Like [{'Nom': 'CNESST 2025-01'}, {'Nom': 'INVALIDITÉ 2025-02'}]"
      }
    ],
    "multiSelect": false
  }]
}
```

**When to Ask**:
- Data structure is ambiguous
- Multiple valid interpretations exist
- Documentation contradicts observed patterns
- Risk of introducing bugs with assumptions

### Phase 3: Improvement Identification

Based on research findings, identify opportunities in these categories:

#### 1. Performance Optimizations
- **API call reduction**: Batch operations, filtering at source
- **Concurrency**: Parallel execution where safe
- **Data minimization**: Fetch only needed fields
- **Caching**: Reuse data within flow
- **Loop optimization**: Reduce iterations, early exits

#### 2. Reliability Improvements
- **Error handling**: Add Scopes with Configure run after
- **Retry logic**: Implement exponential backoff for transient failures
- **Timeout handling**: Set appropriate limits
- **Data validation**: Check inputs before processing
- **Idempotency**: Ensure operations can be retried safely

#### 3. Maintainability Enhancements
- **Naming conventions**: Clear, descriptive action names
- **Comments**: Document complex logic
- **Structure**: Organize related actions in Scopes
- **Variables**: Proper initialization and naming
- **Modularity**: Break complex flows into logical sections

#### 4. Security Hardening
- **Credential management**: Use secure connections
- **Input validation**: Sanitize user inputs
- **Data exposure**: Minimize sensitive data in logs
- **Least privilege**: Use minimal required permissions
- **Secret handling**: Never hardcode credentials

#### 5. Best Practices Compliance
- **Platform standards**: Follow official guidelines
- **Connector patterns**: Use recommended approaches
- **Expression optimization**: Simplify complex expressions
- **Resource cleanup**: Ensure proper disposal
- **Monitoring**: Add telemetry for critical operations

### Phase 4: Prioritization & Change Planning

1. **Categorize Improvements**
   - **Critical**: Must fix (security, reliability issues)
   - **High impact**: Significant performance/reliability gains
   - **Medium impact**: Moderate improvements
   - **Low impact**: Nice-to-have enhancements

2. **User Request Alignment**
   - Prioritize changes explicitly requested by user
   - Ensure requested changes are safe and valid
   - Propose alternatives if request conflicts with best practices

3. **Functional Equivalence Check**
   - Verify refactoring maintains original behavior
   - Document any intentional behavior changes
   - Ensure data transformations remain identical
   - Validate output compatibility

4. **Create Change Plan**
   - List all improvements to implement
   - Note improvements identified but not implemented (for suggestions)
   - Explain rationale for each change
   - Reference documentation sources

### Phase 5: Refactored JSON Generation (Use Task Tool with Flow-Builder Agent)

**CRITICAL**: Use the Task tool to launch a flow-builder agent for JSON generation.

Launch flow-builder sub-agent:

```
Use Task tool with subagent_type="general-purpose"

Prompt: "Generate complete refactored workflow JSON for [PLATFORM] with the following requirements:

Platform: [Power Automate / n8n / Make / Zapier / Other]
Original Flow: [ORIGINAL_JSON]
User Requirements: [USER_REFACTORING_REQUEST]
Best Practices Found: [RESEARCH_FINDINGS]
Improvements to Implement: [CHANGE_PLAN]

Create a complete, valid workflow JSON that:
1. Maintains 100% functional equivalence to original (unless user requested changes)
2. Implements all high-priority improvements
3. Adds comprehensive error handling (platform-specific)
4. Optimizes for performance (batching, filtering, concurrency)
5. Follows platform best practices from documentation
6. Includes clear, descriptive action names
7. Adds comments explaining complex logic
8. Uses valid IDs/GUIDs as required by platform
9. Has correct dependencies/execution order
10. Is ready for copy-paste into platform's import/code feature
11. Respects API limits with appropriate delays/batching
12. Includes proper initialization of all variables
13. Validates inputs before processing
14. Implements retry logic for transient failures

Platform-specific requirements:
- Power Automate: Use Scopes for error handling, proper runAfter chains
- n8n: Use Error Trigger nodes, proper node connections
- Make: Use error handlers, proper routing
- Zapier: Use error paths, filters

Return ONLY the complete JSON with no placeholders or TODOs."
```

**Expected Output from Flow-Builder Agent**:
- Complete, syntactically valid JSON (platform-specific format)
- All required structure elements for the platform
- Proper IDs/GUIDs for all operations
- Correct expression/formula syntax
- Complete execution chains/dependencies
- Comprehensive error handling
- Performance optimizations applied

### Phase 6: Validation & Quality Check

Before finalizing output:

1. **Functional Validation**
   - [ ] Original triggers maintained
   - [ ] Original actions preserved (unless change requested)
   - [ ] Data transformations identical
   - [ ] Outputs remain compatible
   - [ ] Error paths handled

2. **Technical Validation**
   - [ ] JSON syntax valid
   - [ ] Platform-specific format correct
   - [ ] All IDs/GUIDs unique
   - [ ] Dependencies properly ordered
   - [ ] Expressions syntactically correct

3. **Optimization Validation**
   - [ ] Performance improvements applied
   - [ ] Error handling comprehensive
   - [ ] Best practices followed
   - [ ] Security considerations addressed
   - [ ] Documentation references accurate

4. **Platform Validation**
   - [ ] Connector limits respected
   - [ ] API patterns correct
   - [ ] Authentication properly configured
   - [ ] Platform-specific features used correctly

### Phase 7: Report Generation

Generate comprehensive refactoring report:

#### Report Structure

```markdown
# Workflow Refactoring Report

## Summary
- **Platform**: [Platform name]
- **Flow Name**: [Flow identifier]
- **Refactoring Goals**: [User's objectives]
- **Changes Applied**: [Number of improvements implemented]
- **Functional Impact**: [Maintained equivalence / Intentional changes]

## Changes Implemented

### Performance Optimizations
- [List of performance improvements with before/after impact]
- Example: "Reduced API calls from 100 to 10 by implementing batch operations"

### Reliability Improvements
- [List of reliability enhancements]
- Example: "Added error handling scope with retry logic for transient failures"

### Maintainability Enhancements
- [List of code quality improvements]
- Example: "Renamed 15 actions for clarity, organized into logical scopes"

### Security Hardening
- [List of security improvements]
- Example: "Replaced hardcoded credentials with secure connection references"

### Best Practices Applied
- [List of platform best practices implemented]
- Example: "Implemented proper variable initialization per Power Automate guidelines"

## Documentation References

[List of specific documentation files and sections consulted]
- Docs/{Platform}_Documentation/{Connector}/overview.md - [Section name]
- Docs/{Platform}_Documentation/best-practices.md - [Section name]

## Additional Optimization Opportunities

### High Priority (Recommended)
- [Improvements identified but not implemented, with rationale]
- Example: "Consider implementing caching for frequently accessed data (requires architectural change)"

### Medium Priority
- [Medium-impact optimizations for future consideration]

### Low Priority
- [Nice-to-have improvements]

## Testing Recommendations

### Functional Testing
1. [Step-by-step testing plan to verify functional equivalence]
2. Test with same inputs as original flow
3. Verify outputs match expected results

### Performance Testing
1. [How to measure performance improvements]
2. Compare run duration with original flow
3. Monitor API call counts

### Error Testing
1. [How to verify error handling works]
2. Test failure scenarios
3. Verify retry logic

## Migration Guide

### Deployment Steps
1. [Step-by-step instructions to deploy refactored flow]
2. Backup original flow
3. Import refactored JSON
4. Update connections if needed
5. Test thoroughly before production

### Rollback Plan
[How to revert if issues arise]

## Next Steps

1. Review changes and approve
2. Test in development environment
3. Deploy to production
4. Monitor for first 24-48 hours
5. Consider additional optimizations listed above

---

**Refactoring Completed**: [Timestamp]
**Documentation Consulted**: [Number of docs referenced]
**Confidence Level**: High (all changes based on official documentation)
```

## Output Format

**ALWAYS** provide two deliverables:

### 1. Refactored JSON File
```json
{
  "comment": "Refactored workflow - [Date] - Implements [key improvements]",
  "definition": {
    // Complete, valid, platform-specific JSON
    // Ready for copy-paste/import
    // No placeholders or TODOs
  }
}
```

### 2. Refactoring Report
- Structured markdown report as detailed above
- Clear explanation of all changes
- Documentation references
- Additional suggestions
- Testing and deployment guidance

## Critical Requirements

### Documentation-First Approach

**NEVER hallucinate or guess**. Always:
1. Use Task tool with Explore agent to research Docs/{Platform}_Documentation/
2. Reference specific files and sections
3. Quote exact best practices from documentation
4. Verify optimizations against documented constraints
5. Adapt to platform-specific requirements

### Functional Equivalence Guarantee

**NEVER change behavior unless explicitly requested**. Always:
1. Maintain exact same triggers
2. Preserve all actions and their logic
3. Keep data transformations identical
4. Ensure outputs remain compatible
5. Document any intentional changes clearly

### Complete JSON Output

**NEVER output partial or placeholder JSON**. Always:
1. Use Task tool with flow-builder agent
2. Include all required structure elements
3. Generate valid IDs/GUIDs
4. Ensure syntactic validity
5. Make JSON immediately ready for import
6. Follow platform-specific format

### Quality Assurance Checklist

Before delivering output, verify:

**Data Structure Validation** (CRITICAL - New!):
- [ ] Analyzed all filter/query `where` clauses for data type indicators
- [ ] Verified `item()` vs `item()?['Property']` consistency throughout flow
- [ ] Checked loop `items()` usage matches source data structure
- [ ] Traced all variable sources to understand actual data types
- [ ] Asked user for clarification if structure was ambiguous
- [ ] No assumptions made about object properties without verification

**Technical Validation**:
- [ ] Platform identified correctly
- [ ] Research agent consulted Docs/{Platform}_Documentation/
- [ ] Searched web if local docs insufficient
- [ ] All improvements reference documentation (local or web)
- [ ] Flow-builder agent generated complete JSON
- [ ] JSON follows platform-specific format
- [ ] JSON syntax valid (no placeholders)
- [ ] All expressions syntactically correct

**Functional Validation**:
- [ ] Functional equivalence maintained (unless changes requested)
- [ ] Data transformations work with actual data types
- [ ] No property access on primitive types (strings, numbers)
- [ ] Array handling matches actual array content type

**Deliverables**:
- [ ] Report includes all required sections
- [ ] Additional optimizations suggested
- [ ] Testing recommendations provided
- [ ] Deployment guidance included
- [ ] Data structure bugs identified and fixed

## Refactoring Patterns

### Pattern 1: API Call Reduction

**Before** (100 API calls):
```json
{
  "Apply_to_each": {
    "foreach": "@body('Get_all_items')?['value']",
    "actions": {
      "Get_user_details": {
        "type": "ApiConnection",
        "inputs": {
          "host": {"connectionName": "shared_office365users"},
          "method": "get",
          "path": "/users/@{items('Apply_to_each')?['Email']}"
        }
      }
    }
  }
}
```

**After** (1 API call with $expand):
```json
{
  "Get_all_items_with_users": {
    "type": "ApiConnection",
    "inputs": {
      "host": {"connectionName": "shared_sharepointonline"},
      "method": "get",
      "path": "/datasets/@{parameters('site')}/tables/@{parameters('list')}/items",
      "queries": {
        "$expand": "Author,Editor",
        "$select": "Id,Title,Author/DisplayName,Author/Email"
      }
    }
  }
}
```

**Impact**: 99% API call reduction, 10x faster execution

---

### Pattern 2: Error Handling Addition

**Before** (no error handling):
```json
{
  "Send_email": {
    "type": "ApiConnection",
    "inputs": {
      "host": {"connectionName": "shared_office365"},
      "method": "post",
      "path": "/Mail"
    }
  }
}
```

**After** (comprehensive error handling):
```json
{
  "Try_Send_Email": {
    "type": "Scope",
    "actions": {
      "Send_email": {
        "type": "ApiConnection",
        "inputs": {
          "host": {"connectionName": "shared_office365"},
          "method": "post",
          "path": "/Mail"
        }
      }
    }
  },
  "Catch_Email_Error": {
    "type": "Scope",
    "runAfter": {
      "Try_Send_Email": ["Failed", "TimedOut"]
    },
    "actions": {
      "Log_Error": {
        "type": "Compose",
        "inputs": {
          "error": "@result('Try_Send_Email')",
          "timestamp": "@utcNow()"
        }
      },
      "Notify_Admin": {
        "type": "ApiConnection",
        "inputs": {
          "host": {"connectionName": "shared_office365"},
          "method": "post",
          "path": "/Mail",
          "body": {
            "To": "admin@company.com",
            "Subject": "Flow Error: Email Send Failed",
            "Body": "@body('Log_Error')"
          }
        }
      }
    }
  }
}
```

**Impact**: Failures tracked, admin notified, debugging simplified

---

### Pattern 3: Performance - Concurrency Optimization

**Before** (sequential, slow):
```json
{
  "Apply_to_each": {
    "foreach": "@body('Get_items')?['value']",
    "actions": {
      "Independent_HTTP_Call": {
        "type": "Http",
        "inputs": {
          "method": "POST",
          "uri": "https://api.example.com/process",
          "body": "@item()"
        }
      }
    }
  }
}
```

**After** (parallel, 5x faster):
```json
{
  "Apply_to_each": {
    "foreach": "@body('Get_items')?['value']",
    "runtimeConfiguration": {
      "concurrency": {
        "repetitions": 10
      }
    },
    "actions": {
      "Independent_HTTP_Call": {
        "type": "Http",
        "inputs": {
          "method": "POST",
          "uri": "https://api.example.com/process",
          "body": "@item()"
        }
      }
    }
  }
}
```

**Impact**: 5x faster for independent operations (use only when operations don't depend on each other)

---

### Pattern 4: Maintainability - Clear Naming

**Before** (cryptic names):
```json
{
  "actions": {
    "Compose": {
      "type": "Compose",
      "inputs": "@body('HTTP')?['data']"
    },
    "Compose_2": {
      "type": "Compose",
      "inputs": "@first(body('Compose'))"
    },
    "HTTP_2": {
      "type": "Http",
      "inputs": {
        "uri": "https://api.example.com/send",
        "body": "@body('Compose_2')"
      }
    }
  }
}
```

**After** (descriptive names):
```json
{
  "actions": {
    "Extract_User_Data_From_API_Response": {
      "type": "Compose",
      "inputs": "@body('Get_Users_From_External_API')?['data']"
    },
    "Get_First_Active_User": {
      "type": "Compose",
      "inputs": "@first(body('Extract_User_Data_From_API_Response'))"
    },
    "Send_Welcome_Email_To_User": {
      "type": "Http",
      "inputs": {
        "uri": "https://api.example.com/send",
        "body": "@body('Get_First_Active_User')"
      }
    }
  }
}
```

**Impact**: Immediately understandable logic, easier maintenance

---

### Pattern 5: Security - Credential Hardening

**Before** (insecure):
```json
{
  "HTTP_Call": {
    "type": "Http",
    "inputs": {
      "uri": "https://api.example.com/data",
      "headers": {
        "Authorization": "Bearer sk-1234567890abcdef"
      }
    }
  }
}
```

**After** (secure):
```json
{
  "Initialize_API_Key": {
    "type": "InitializeVariable",
    "inputs": {
      "variables": [{
        "name": "APIKey",
        "type": "String",
        "value": "@parameters('SecureAPIKey')"
      }]
    }
  },
  "HTTP_Call": {
    "type": "Http",
    "inputs": {
      "uri": "https://api.example.com/data",
      "authentication": {
        "type": "Raw",
        "value": "@concat('Bearer ', variables('APIKey'))"
      }
    },
    "runAfter": {
      "Initialize_API_Key": ["Succeeded"]
    }
  }
}
```

**Impact**: Credentials in secure parameters, not hardcoded in JSON

---

## Platform-Specific Considerations

### Power Automate

**Key Optimizations**:
- Use `$expand` and `$select` in OData queries
- Implement Scopes for error handling
- Set concurrency for independent operations
- Use "Get items" over "List items" (pagination support)
- Filter at source with `$filter` queries

**Best Practices Documentation**: `Docs/PowerAutomateDocs/`

---

### n8n

**Key Optimizations**:
- Use "Split in Batches" node for large datasets
- Implement Error Trigger nodes
- Enable "Always Output Data" for better debugging
- Use "HTTP Request" node with batching
- Leverage "Code" node for complex transformations

**Best Practices Documentation**: `Docs/N8NDocs/`

---

### Make

**Key Optimizations**:
- Use filters to reduce operations
- Implement error handlers on all routes
- Use aggregators for batch operations
- Set appropriate scheduling intervals
- Use routers for conditional logic

---

### Zapier

**Key Optimizations**:
- Use multi-step zaps efficiently
- Implement error paths
- Use filters to reduce task usage
- Leverage built-in apps over webhooks
- Use formatter for data transformation

---

## Sub-Agent Coordination

### Research Agent (Explore)

**Purpose**: Find best practices and optimization guidelines

**Input Requirements**:
- Platform name
- Connectors/nodes used
- Current pain points (if known)

**Expected Output**:
- Documentation file paths
- Specific optimization recommendations
- Limitation warnings
- Security considerations

**Invocation**:
```
Task tool, subagent_type="Explore", thoroughness="very thorough"
```

### Flow-Builder Agent

**Purpose**: Generate complete, optimized workflow JSON

**Input Requirements**:
- Original flow JSON
- User requirements
- Research findings
- Change plan

**Expected Output**:
- Complete JSON structure
- All optimizations applied
- Valid syntax
- No placeholders

**Invocation**:
```
Task tool, subagent_type="general-purpose"
```

## Examples

### Example 1: Data Structure Bug (Real Case Study)

**User**: "Fix the DossierPlusRécent variable assignment - it's filtering on array but accessing wrong property"

**Input Flow**:
```json
{
  "Filtrer_dossier_CNESST": {
    "type": "Query",
    "inputs": {
      "from": "@variables('ListeDesDossier')",
      "where": "@contains(toLower(item()), 'cnesst')"  // ← item() without property!
    }
  },
  "LoopCNESST": {
    "foreach": "@body('Filtrer_dossier_CNESST')",
    "actions": {
      "DossierPlusRécent_CNESST": {
        "type": "SetVariable",
        "inputs": {
          "name": "DossierPlusRecent",
          "value": "@items('LoopCNESST')?['Nom']"  // ← BUG: Accessing 'Nom' property!
        }
      }
    }
  }
}
```

**Analysis Process**:
1. **Phase 0 - Data Structure Analysis**:
   - Check filter: `contains(toLower(item()), 'cnesst')` uses `item()` without property
   - **CONCLUSION**: `ListeDesDossier` is **array of strings**, NOT array of objects!
   - Examples: `["CNESST 2025-01-15", "CNESST 2025-02-20", "INVALIDITÉ 2025-01-10"]`

2. **Identify Bug**:
   - Loop iterates over strings: `["CNESST 2025-01-15", ...]`
   - But tries to access: `items('LoopCNESST')?['Nom']` (treating string as object)
   - **ERROR**: Can't access property on string primitive!

3. **Correct Fix**:
   ```json
   "DossierPlusRécent_CNESST": {
     "type": "SetVariable",
     "inputs": {
       "name": "DossierPlusRecent",
       "value": "@items('LoopCNESST')"  // ← CORRECT: Direct string value
     }
   }
   ```

4. **Also Fix DEBUG Action**:
   ```json
   "DEBUG_jour_CNESST": {
     "type": "Compose",
     "inputs": "@int(substring(substring(
       if(
         contains(split(items('LoopCNESST'), '.')[0], '_'),  // ← Remove ?['Nom']
         last(split(split(items('LoopCNESST'), '.')[0], '_')),
         last(split(split(items('LoopCNESST'), '.')[0], ' '))
       ), 0, 10), 8, 2))"
   }
   ```

**Key Lesson**:
- **ALWAYS check filter syntax first**: `item()` vs `item()?['Prop']` tells you the data structure
- **NEVER assume** objects with properties without verification
- **ASK USER** if ambiguous

**Output**:
- Corrected JSON with proper string handling
- Explanation of the bug and why it occurred
- Prevention tips for future

---

### Example 2: Performance Optimization Request

**User**: "Optimize this Power Automate flow to reduce execution time"

**Input Flow**: Flow with 100 sequential API calls

**Workflow**:
1. Analyze: Identify sequential API calls bottleneck
2. Research: Launch Explore agent → Find batching and concurrency guidelines
3. Plan: Replace sequential calls with batch operation + parallel processing
4. Build: Launch flow-builder agent → Generate optimized JSON
5. Report: Document 90% execution time reduction
6. Suggest: Additional caching opportunities

**Output**:
- Refactored JSON with batch operations
- Report showing before/after metrics
- Additional optimization suggestions

---

### Example 2: Best Practices Application

**User**: "Refactor this flow to follow Power Automate best practices"

**Input Flow**: Working but poorly structured flow

**Workflow**:
1. Analyze: Identify deviations from best practices
2. Research: Launch Explore agent → Find official best practices documentation
3. Plan: Add error handling, improve naming, add comments
4. Build: Launch flow-builder agent → Generate refactored JSON
5. Report: Document all improvements with documentation references
6. Suggest: Consider breaking into child flows for modularity

**Output**:
- Refactored JSON with best practices applied
- Report listing all improvements
- Future enhancement suggestions

---

### Example 3: Error Handling Enhancement

**User**: "Add comprehensive error handling to this workflow"

**Input Flow**: Flow with no error handling

**Workflow**:
1. Analyze: Map all failure points
2. Research: Launch Explore agent → Find error handling patterns
3. Plan: Add Scopes, Configure run after, retry logic
4. Build: Launch flow-builder agent → Generate hardened JSON
5. Report: Document error handling strategy
6. Suggest: Add monitoring and alerting

**Output**:
- Refactored JSON with comprehensive error handling
- Report explaining error handling approach
- Monitoring recommendations

---

## When to Escalate

Use **automation-debugger** instead if:
- Flow has existing errors that need fixing first
- Root cause analysis needed before refactoring
- Complex error patterns require investigation

Use **automation-validator** after refactoring to:
- Validate refactored JSON before deployment
- Ensure no issues introduced
- Get pre-deployment confidence

## Best Practices

1. **Always preserve functionality** unless explicitly requested to change
2. **Document every change** with rationale and documentation reference
3. **Suggest additional improvements** beyond what was implemented
4. **Provide testing guidance** to verify functional equivalence
5. **Include deployment instructions** for smooth rollout
6. **Reference documentation** for every optimization decision
7. **Be transparent** about limitations and trade-offs
8. **Validate thoroughly** before delivering output

## Skill Invocation Examples

User messages that trigger this skill:

- "Optimize this Power Automate flow for better performance"
- "Refactor this workflow to follow best practices"
- "Improve the error handling in this flow.json"
- "Make this automation more reliable"
- "Correct the API call parameters in this flow"
- "Enhance this workflow to reduce execution time"
- "Simplify this complex n8n workflow"
- "Modernize this old Make scenario"
- "Add retry logic to this flow"
- "Reduce the number of API calls in this automation"
- "Make this flow more maintainable"
- "Apply security best practices to this workflow"

---

**Version**: 2.0
**Last Updated**: 2025-10-31
**Platforms**: Power Automate, n8n, Make, Zapier + extensible

## Changelog

### Version 2.0 (2025-10-31)

**Major Improvements**:
- ✅ Added **Phase 0: Data Structure Analysis** (CRITICAL) - Prevents hallucinations about data types
- ✅ Added **Multi-Source Research Strategy** - Local docs → Web → Ask user
- ✅ Added **Common Pitfalls section** - Highlights most frequent errors
- ✅ Added **Real Case Study example** - Data structure bug from actual debugging session
- ✅ Enhanced **Quality Assurance Checklist** - Now includes data structure validation
- ✅ Added **AskUserQuestion workflow** - Clarify ambiguous structures proactively
- ✅ Added **WebSearch integration** - Fallback when local docs insufficient

**Key Changes**:
- Never assume array structures (strings vs objects) without verification
- Always check `item()` vs `item()?['Property']` patterns in filters
- Ask user when uncertain rather than guessing
- Search web for official documentation if local docs don't have answer
- Validate data type consistency throughout flow before making changes

**Lessons Learned**:
- Mismatched data structure assumptions are the #1 source of refactoring bugs
- Filter syntax reveals data types: `contains(item(), 'x')` = array of strings
- Always trace data sources back to understand actual structures
- User confirmation beats confident assumptions
