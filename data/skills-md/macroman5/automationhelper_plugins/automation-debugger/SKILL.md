---
name: automation-debugger
description: Expert automation platform error debugger for Power Automate, n8n, Make, Zapier and other workflow platforms. Analyzes JSON flow definitions with error messages, researches official documentation, and generates complete fixed JSON ready for copy-paste. Triggers when user provides error JSON files, workflow JSON with errors, error messages, debug requests, or failing automation content. Returns structured debug report with root cause analysis and working fixed JSON.
---

# Automation Debugger

Expert system for debugging automation workflow errors across multiple platforms and generating production-ready fixes.

## Supported Platforms

- **Power Automate** (Microsoft)
- **n8n** (Open-source automation)
- **Make** (formerly Integromat)
- **Zapier**
- **Other JSON-based workflow platforms**

## Purpose

This skill provides comprehensive debugging for automation workflows by:
1. Analyzing error messages and failing JSON flow definitions
2. Researching official documentation to find root causes (Docs/ directory)
3. Generating complete, valid fixed JSON ready for copy-paste (outputs as fixed_flow.json or similar)
4. Avoiding hallucinations by strictly referencing platform documentation
5. Adapting solutions to platform-specific requirements

## When This Skill Activates

Automatically activates when user provides:
- **Error JSON files** - Any JSON file containing error information (examples: error.json, erreur.json, error_bloc.json, workflow_error.json)
- **Workflow JSON with errors** - Flow/workflow JSON content with error description (any platform)
- **Error messages** - Error messages from workflow runs, logs, or execution history
- **Debug requests** - Explicit requests to "debug", "fix", "analyze", or "troubleshoot" automation errors
- **Status codes** - HTTP status codes (401, 403, 404, 429, 500, etc.) with workflow context
- **Platform-specific errors** - "Power Automate error", "n8n workflow failing", "Make scenario issue", "Zapier zap broken"
- **Failure descriptions** - "My flow keeps failing", "this automation stopped working", "getting errors in workflow"

## Common Pitfalls to AVOID

### ❌ CRITICAL ERROR #1: Assuming Data Structures (Most Common!)

**The Mistake**:
```json
// You see a filter in the error flow
"where": "@contains(toLower(item()), 'keyword')"

// And you ASSUME it's filtering objects, so you fix with:
"value": "@items('Loop')?['PropertyName']"  // ← WRONG IF ARRAY OF STRINGS!
```

**How to Avoid**:
1. **ALWAYS analyze filter syntax first**: `item()` vs `item()?['Prop']`
2. `item()` without property → Array of **primitives** (strings/numbers)
3. `item()?['Property']` → Array of **objects**
4. **Ask user when uncertain** - never guess data structures!
5. Trace data sources back to understand actual types

**Our Real Bug Example**:
```json
// Filter showed it was strings:
"where": "@contains(toLower(item()), 'cnesst')"

// But I incorrectly suggested accessing property:
"value": "@items('LoopCNESST')?['Nom']"  // ← BUG!

// Correct fix was:
"value": "@items('LoopCNESST')"  // ← Just the string!
```

---

### ❌ ERROR #2: Guessing Connector Outputs

**The Mistake**: Assuming SharePoint GetFileItems returns objects with 'Name' property without checking

**How to Avoid**:
1. Search Docs/{Platform}_Documentation/ for output schemas
2. Use WebSearch for official documentation if local docs don't have it
3. Ask user to confirm property names if uncertain
4. Check Select action mappings (they reveal structure)

---

### ❌ ERROR #3: Not Validating Fixes Against Data Flow

**The Mistake**: Creating fixes that work syntactically but fail with actual data types

**How to Avoid**:
1. Complete Phase 0 (Data Structure Analysis) before fixing
2. Trace entire data flow from source to error point
3. Validate item access patterns match data types
4. Test logic against actual data structures

---

## Core Workflow

### Phase 0: Data Structure Analysis (CRITICAL - NEW!)

**NEVER assume data structures without verification**. Before debugging, ALWAYS analyze actual data structures in the failing flow.

1. **Examine the Error Context**
   - Identify which action/variable contains the problematic data
   - Look for variable declarations to understand types
   - Check if error mentions property access on undefined/null

2. **Analyze Filter/Query Operations** (MOST IMPORTANT!)
   - **CRITICAL CHECK**: Look at `where` clauses in Query actions
   - `item()` without property → **Array of primitives (strings/numbers)**
     ```json
     "where": "@contains(toLower(item()), 'keyword')"
     // ↑ This means: Array of strings ["string1", "string2"]
     ```
   - `item()?['PropertyName']` → **Array of objects**
     ```json
     "where": "@contains(item()?['Name'], 'keyword')"
     // ↑ This means: Array of objects [{"Name": "..."}, ...]
     ```

3. **Trace Data Sources**
   - Follow `from` in Query actions back to source
   - Check SharePoint/connector outputs
   - Check Select action mappings (these define output structure!)
   - Verify Compose action inputs
   - Look for Array variable initializations

4. **Validate Item Access Consistency**
   - In loops: Check if `items('LoopName')` or `items('LoopName')?['Property']`
   - In filters: Check if `item()` or `item()?['Property']`
   - **MISMATCH = BUG**: Filter uses `item()` but loop uses `items('Loop')?['Prop']` → ERROR!

5. **Ask User When Uncertain** (Use AskUserQuestion tool)
   - If data structure is ambiguous after analysis
   - If documentation doesn't clarify the structure
   - If multiple valid interpretations exist
   - If error message doesn't make structure clear

   **Example questions**:
   - "I see your filter uses `contains(item(), 'text')`. Is your variable an array of strings like `['text1', 'text2']`, or an array of objects?"
   - "Can you confirm the output structure from [ActionName]? Is it strings or objects with properties?"
   - "The flow accesses `items('Loop')?['Nom']` but the filter suggests strings. Which is correct?"

### Phase 1: Error Analysis

1. **Extract Error Information**
   - Parse the provided JSON (error file, flow snippet, or workflow JSON)
   - Identify the failing action or trigger
   - Classify error type (Authentication/Throttling/Data Format/Timeout/Not Found/Permission)
   - Extract exact error message text

2. **Identify Context**
   - Determine which platform (Power Automate, n8n, Make, Zapier, etc.)
   - Identify connector/node involved (SharePoint, HTTP, Database, etc.)
   - Find the specific action or trigger causing the failure
   - Note any relevant workflow configuration or parameters

### Phase 2: Documentation Research (Multi-Source Strategy - NEW!)

**CRITICAL**: Research thoroughly using multiple sources in order. Never skip or guess!

#### Step 1: Local Documentation Research (Use Task Tool with Explore Agent)

Launch research sub-agent with thorough investigation:

```
Use Task tool with subagent_type="Explore" and thoroughness="very thorough"

Prompt: "Research [PLATFORM] documentation for [ERROR_TYPE] error in [CONNECTOR/NODE_NAME], specifically the [ACTION_NAME] action/node.

Platform: [Power Automate / n8n / Make / Zapier / Other]

Search in Docs/ directory for platform-specific documentation:
1. Platform documentation (Docs/{Platform}_Documentation/)
2. Connector/node overview - find limitations and constraints
3. **Data structure specifications** (output schemas, property names, data types)
4. Action/node documentation - find parameter requirements
5. Common error patterns for this platform

Focus on finding:
- **DATA STRUCTURE DETAILS** (output schemas, property names, array vs object)
- Known limitations causing this error
- Required parameters and their formats (platform-specific)
- API limits or throttling constraints
- Authentication/permission requirements
- Platform-specific quirks or known issues
- Common error scenarios and solutions

Return specific file paths, section names, and exact limitations found."
```

**Expected Output from Research Agent**:
- **Data structure specifications** (schemas, property names, types)
- Specific documentation file paths (Docs/{Platform}_Documentation/)
- Relevant limitations or constraints
- Required parameter formats (platform-specific)
- Known workarounds or solutions
- Platform-specific considerations

#### Step 2: Web Research (Use WebSearch Tool - If Local Docs Insufficient)

**ONLY if local documentation doesn't provide needed information**, use WebSearch:

```
Use WebSearch tool with targeted queries:

Examples:
- "[PLATFORM] [CONNECTOR] output schema"
- "[PLATFORM] [ACTION_NAME] return properties"
- "[ERROR_CODE] [PLATFORM] [CONNECTOR] solution"
- "Microsoft Learn [PLATFORM] [CONNECTOR] documentation"

Search for:
- Official platform documentation (Microsoft Learn, n8n docs, etc.)
- Platform-specific community forums (verified answers only)
- Official API documentation
- Recent Stack Overflow solutions (check dates!)
```

**Validation Requirements**:
- Prefer official documentation over community posts
- Cross-reference multiple sources
- Verify information is current (check publication dates)
- Cite sources in output

#### Step 3: Ask User for Clarification (Use AskUserQuestion Tool)

**If both local docs and web search are unclear or contradictory**, ask the user:

```
Use AskUserQuestion tool with specific targeted questions:

Example:
{
  "questions": [{
    "question": "Your flow uses `contains(item(), 'CNESST')` in the filter. Can you confirm what type of data is in this variable?",
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
- Data structure is ambiguous after documentation search
- Multiple valid interpretations exist for the error
- Documentation contradicts observed flow patterns
- Risk of creating a fix that introduces new bugs

### Phase 3: Solution Design

Based on research findings:

1. **Root Cause Identification**
   - Link error to specific documentation constraint
   - Explain WHY the error occurs (technical reasoning)
   - Reference exact file and section from Docs/{Platform}_Documentation/
   - Consider platform-specific behaviors

2. **Solution Strategy**
   - Design fix addressing root cause
   - Consider connector limitations
   - Include error handling patterns
   - Add retry logic if needed for transient errors
   - Optimize for API limits

3. **Validation**
   - Verify solution against documentation constraints
   - Check for unintended side effects
   - Ensure compliance with Power Automate best practices
   - Validate all parameters and data types

### Phase 4: Fix Generation (Use Task Tool with Flow-Builder Agent)

**CRITICAL**: Use the Task tool to launch a flow-builder agent for JSON generation.

Launch flow-builder sub-agent:

```
Use Task tool with subagent_type="Plan" or "general-purpose"

Prompt: "Generate complete fixed workflow JSON for [PLATFORM] with the following requirements:

Platform: [Power Automate / n8n / Make / Zapier / Other]
Original Error: [ERROR_DETAILS]
Root Cause: [ROOT_CAUSE_FROM_RESEARCH]
Required Fixes: [SPECIFIC_CHANGES_NEEDED]

Create a complete, valid workflow JSON following the platform-specific format in Docs/{Platform}_Documentation/ that:
1. Includes all fixes for the identified error
2. Maintains existing workflow logic that works
3. Adds proper error handling (platform-specific)
4. Includes retry logic if dealing with transient errors
5. Respects API limits with delays if needed
6. Uses valid IDs/GUIDs as required by platform
7. Has correct dependencies/execution order
8. Follows platform-specific syntax and structure
9. Is ready for copy-paste into platform's import/code feature

Return ONLY the complete JSON with no placeholders or TODOs."
```

**Expected Output from Flow-Builder Agent**:
- Complete, syntactically valid JSON (platform-specific format)
- All required structure elements for the platform
- Proper IDs/GUIDs for all operations
- Correct expression/formula syntax
- Complete execution chains/dependencies

### Phase 5: Structured Output

Generate final output using the template from `output-style/template-debug-output.md`:

1. **Error Analysis Section**
   - Error type classification
   - Failing action/trigger identification
   - Original error message
   - Impact description

2. **Root Cause Section**
   - Primary cause explanation
   - Documentation references with specific file paths
   - Technical details of the issue

3. **Solution Section**
   - Recommended fix approach
   - Step-by-step implementation instructions
   - Additional improvements (error handling, performance, reliability)
   - Validation checklist

4. **Fixed JSON Section**
   - Complete, working JSON ready for copy-paste
   - Platform-specific format
   - List of changes applied
   - Configuration notes for after pasting/importing

5. **Alternative Approaches Section** (if applicable)
   - Other viable solutions
   - When to use each alternative
   - Pros/cons comparison

6. **Prevention Section**
   - Best practices to avoid similar errors
   - Monitoring recommendations
   - Regular maintenance tasks

## Output Format

**ALWAYS** follow the XML-structured format from `output-style/template-debug-output.md`:

```xml
<debug_report>
<error_analysis>
[Error classification and details]
</error_analysis>

<root_cause>
[Root cause with documentation references]
</root_cause>

<solution>
[Step-by-step fix instructions]
</solution>

<fixed_json>
[Complete valid JSON ready for copy-paste]
</fixed_json>

<alternative_approaches>
[Other viable solutions if applicable]
</alternative_approaches>

<prevention>
[Best practices and monitoring]
</prevention>
</debug_report>
```

## Critical Requirements

### Documentation-First Approach

**NEVER hallucinate or guess**. Always:
1. Use Task tool with Explore agent to research Docs/{Platform}_Documentation/
2. Reference specific files and sections
3. Quote exact limitations from documentation
4. Verify solutions against documented constraints
5. Adapt to platform-specific requirements and syntax

### Complete JSON Output

**NEVER output partial or placeholder JSON**. Always:
1. Use Task tool with flow-builder agent to generate complete JSON
2. Include all required structure elements (platform-specific)
3. Generate valid IDs/GUIDs as required by platform
4. Ensure syntactic validity (balanced brackets, escaped strings)
5. Validate against platform-specific format documentation
6. Make JSON immediately copy-paste/import ready
7. Follow platform naming conventions and structure

### Quality Assurance

Before delivering output, verify:

**Data Structure Validation** (CRITICAL - New!):
- [ ] Completed Phase 0 (Data Structure Analysis) before creating fix
- [ ] Analyzed all filter/query `where` clauses for data type indicators
- [ ] Verified `item()` vs `item()?['Property']` consistency in fix
- [ ] Checked loop `items()` usage matches actual data structure
- [ ] Traced variable sources to understand actual data types
- [ ] Asked user for clarification if structure was ambiguous
- [ ] No assumptions made about object properties without verification
- [ ] Fix validates against actual data flow (not just syntax)

**Research & Documentation**:
- [ ] Platform identified correctly
- [ ] Research agent consulted Docs/{Platform}_Documentation/
- [ ] Searched web if local docs insufficient (cited sources)
- [ ] Root cause references actual documentation files
- [ ] All claims backed by documentation (local or web)

**Technical Validation**:
- [ ] Flow-builder agent generated complete JSON
- [ ] JSON follows platform-specific format
- [ ] JSON is syntactically valid (no placeholders)
- [ ] All expressions syntactically correct
- [ ] Data type handling matches actual structures (primitives vs objects)
- [ ] Platform-specific syntax and conventions followed

**Output Quality**:
- [ ] All sections of debug report template populated
- [ ] Changes explained clearly with WHY (not just WHAT)
- [ ] Solution is actionable and specific
- [ ] Alternative approaches provided if applicable
- [ ] Prevention tips included to avoid future similar errors

## Error Pattern Knowledge Base

### Common Error Types

1. **Authentication (401/403)**
   - Research: Docs/{Platform}_Documentation/{Connector}/overview.md → Authentication section
   - Check: Permission requirements, connection credentials
   - Fix: Proper authentication configuration, permission grants

2. **Throttling (429)**
   - Research: Docs/{Platform}_Documentation/{Connector}/overview.md → API Limits section
   - Check: Call frequency, batch operations
   - Fix: Add delays, implement exponential backoff, use batch operations

3. **Data Format**
   - Research: Docs/{Platform}_Documentation/BuiltIn/data-operation.md
   - Check: Schema requirements, data types, required fields
   - Fix: Proper Parse JSON schema, type conversions

4. **Timeout**
   - Research: Docs/{Platform}_Documentation/{Connector}/overview.md → Known Limitations
   - Check: File sizes, operation duration, Do until loops
   - Fix: Implement chunking, set proper timeouts, optimize queries

5. **Not Found (404)**
   - Research: Docs/{Platform}_Documentation/{Connector}/actions.md
   - Check: Resource paths, IDs, permissions, resource existence
   - Fix: Validate paths, check permissions, add existence checks

## Sub-Agent Coordination

### Research Agent (Explore)

**Purpose**: Find relevant documentation and constraints

**Input Requirements**:
- Error type
- Connector name
- Action/trigger name

**Expected Output**:
- File paths: `Docs/{Platform}_Documentation/{Connector}/overview.md`
- Specific sections: "Known Limitations", "API Limits", etc.
- Exact constraints: "Max 50MB file size", "600 calls per 60 seconds"

**Invocation**:
```
Task tool, subagent_type="Explore", thoroughness="very thorough"
```

### Flow-Builder Agent

**Purpose**: Generate complete, valid Power Automate JSON

**Input Requirements**:
- Original error details
- Root cause analysis
- Specific fixes needed
- Documentation constraints

**Expected Output**:
- Complete JSON structure
- Valid GUIDs
- Proper runAfter chains
- No placeholders or TODOs

**Invocation**:
```
Task tool, subagent_type="general-purpose" or "Plan"
```

## Examples

### Example 1: Data Structure Bug (Real Case Study - NEW!)

**User Input**: "Fix the DossierPlusRécent variable - the filter works but loop assignment fails"

**Error Flow Snippet**:
```json
{
  "Filtrer_dossier_CNESST": {
    "type": "Query",
    "inputs": {
      "from": "@variables('ListeDesDossier')",
      "where": "@contains(toLower(item()), 'cnesst')"  // ← KEY: item() without property!
    }
  },
  "LoopCNESST": {
    "foreach": "@body('Filtrer_dossier_CNESST')",
    "actions": {
      "DossierPlusRécent_CNESST": {
        "type": "SetVariable",
        "inputs": {
          "name": "DossierPlusRecent",
          "value": "@items('LoopCNESST')?['Nom']"  // ← BUG: Accessing property on string!
        }
      },
      "DEBUG_jour_CNESST": {
        "type": "Compose",
        "inputs": "@int(substring(
          split(items('LoopCNESST')?['Nom'], '.')[0],  // ← BUG: Also accessing Nom
          8, 2))"
      }
    }
  }
}
```

**Debugging Workflow**:

1. **Phase 0 - Data Structure Analysis**:
   - ✅ Examined filter: `"where": "@contains(toLower(item()), 'cnesst')"`
   - ✅ **CRITICAL INSIGHT**: `item()` without property → Array of **strings**!
   - ✅ Not `item()?['Nom']` → So NOT array of objects
   - ✅ **Conclusion**: `ListeDesDossier` = `["CNESST 2025-01-15", "CNESST 2025-02-20"]`

2. **Phase 1 - Error Analysis**:
   - Loop iterates over strings from filter
   - But tries to access: `items('LoopCNESST')?['Nom']`
   - **ERROR**: Can't access property 'Nom' on string primitive!
   - Same bug in DEBUG_jour_CNESST action

3. **Phase 2 - Research** (Skipped - structure analysis sufficient):
   - Data structure analysis revealed the issue
   - No need for documentation research for this bug type

4. **Phase 3 - Solution Design**:
   - Remove `?['Nom']` property access throughout
   - Access string directly: `@items('LoopCNESST')`
   - Update all actions that incorrectly access 'Nom' property

5. **Phase 4 - Generate Fix**:
```json
{
  "DossierPlusRécent_CNESST": {
    "type": "SetVariable",
    "inputs": {
      "name": "DossierPlusRecent",
      "value": "@items('LoopCNESST')"  // ← FIXED: Direct string access
    }
  },
  "DEBUG_jour_CNESST": {
    "type": "Compose",
    "inputs": "@int(substring(
      split(items('LoopCNESST'), '.')[0],  // ← FIXED: Removed ?['Nom']
      8, 2))"
  }
}
```

**Key Lessons**:
- ✅ **ALWAYS check filter syntax first**: `item()` reveals data type
- ✅ `item()` = primitives, `item()?['Prop']` = objects
- ✅ Complete Phase 0 before jumping to solutions
- ✅ Trace data flow from source through transformations
- ❌ **NEVER assume** objects with properties without verification

**Prevention**:
- Use consistent data structures throughout flow
- If you need object properties, use Select action to create them
- Add comments explaining data structure at key points
- Validate filter patterns match loop usage

---

### Example 2: SharePoint Throttling Error

**Input**:
```json
{
  "error": "Status code: 429, TooManyRequests",
  "action": "sharepointonline_getitems",
  "connector": "SharePoint"
}
```

**Workflow**:
1. Classify: Throttling error
2. Research: Launch Explore agent → Docs/{Platform}_Documentation/SharePoint/overview.md
3. Find: "600 API calls per 60 seconds per connection"
4. Design: Add delays between calls, implement paging
5. Build: Launch flow-builder agent → Generate complete JSON with delays
6. Output: Structured debug report with fixed JSON

### Example 2: OneDrive File Size Error

**Input**:
```json
{
  "error": "File not processed",
  "trigger": "onedrive_whenfilecreated",
  "connector": "OneDrive"
}
```

**Workflow**:
1. Classify: File processing error
2. Research: Launch Explore agent → Docs/{Platform}_Documentation/OneDrive/overview.md
3. Find: "Files over 50MB skipped by triggers"
4. Design: Add file size check, alternative large file handling
5. Build: Launch flow-builder agent → Generate JSON with size validation
6. Output: Structured debug report with fixed JSON

## Supporting Files

See also:
- [Output Template](../../../output-style/template-debug-output.md) - Complete output format specification
- [Power Automate JSON Format](../../../Docs/{Platform}_Documentation/power-automate-json-format.md) - Valid JSON structure requirements
- [Repository Guide](../../../CLAUDE.md) - Full repository documentation and patterns

## Best Practices

1. **Always use sub-agents** - Never skip research or flow-builder phases
2. **Reference real documentation** - Every claim must cite Docs/{Platform}_Documentation/
3. **Output complete JSON** - No placeholders, no TODOs, production-ready
4. **Explain changes** - User must understand WHY each fix is needed
5. **Include error handling** - Every fix should have proper error handling
6. **Validate thoroughly** - Check JSON syntax, structure, and compliance
7. **Be specific** - Name exact parameters, values, file paths
8. **Provide alternatives** - Offer multiple approaches when applicable

## Skill Invocation Examples

User messages that trigger this skill:

- "Debug this error.json file"
- "I'm getting a 429 error in my SharePoint flow, here's the JSON: {...}"
- "Fix this Power Automate error: [error message]"
- "My OneDrive trigger isn't working, here's the error JSON"
- "Analyze this flow failure: [JSON content]"
- "Help me fix this authentication error in Power Automate"
- "My workflow is broken, here's the error file"
- "Debug my failing automation, error attached"
- "This n8n workflow keeps erroring out"

---

**Version**: 2.0
**Last Updated**: 2025-10-31
**Platforms**: Power Automate, n8n, Make, Zapier + extensible

## Changelog

### Version 2.0 (2025-10-31)

**Major Improvements**:
- ✅ Added **Phase 0: Data Structure Analysis** (CRITICAL) - Prevents incorrect fixes based on wrong data type assumptions
- ✅ Added **Multi-Source Research Strategy** - Local docs → Web → Ask user (never guess!)
- ✅ Added **Common Pitfalls section** - Highlights critical debugging errors to avoid
- ✅ Added **Real Case Study example** - Data structure bug from actual debugging session
- ✅ Enhanced **Quality Assurance Checklist** - Now includes comprehensive data structure validation
- ✅ Added **AskUserQuestion workflow** - Clarify ambiguous structures before creating fixes
- ✅ Added **WebSearch integration** - Fallback when local docs don't have the answer

**Key Changes**:
- Never assume array structures (strings vs objects) without verification
- Always analyze `item()` vs `item()?['Property']` patterns in filters/queries
- Ask user when uncertain rather than guessing and potentially creating bugs
- Search web for official documentation if local docs are insufficient
- Validate data type consistency throughout flow before generating fixes
- Trace data sources back to understand actual structures

**Lessons Learned from Real Bugs**:
- Mismatched data structure assumptions are the #1 source of incorrect debugging fixes
- Filter syntax is the most reliable indicator: `contains(item(), 'x')` = array of primitives
- Property access on primitives (`items('Loop')?['Prop']` on strings) causes runtime errors
- Always complete Phase 0 before jumping to solutions
- User confirmation beats confident but wrong assumptions
