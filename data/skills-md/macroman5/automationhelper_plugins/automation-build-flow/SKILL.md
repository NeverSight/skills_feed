---
name: automation-build-flow
description: Workflow builder for Power Automate, n8n, Make, Zapier and other platforms. Generates complete, production-ready workflow JSON from implementation plans or requirements. Uses flow-builder sub-agent to create valid platform-specific JSON with all triggers, actions, error handling, and configurations. Triggers when user has a plan/requirements and wants to generate workflow JSON, or says "build this workflow", "create the flow", "generate JSON". Output ready for import into target platform.
---

# Automation Build Flow

Professional workflow builder that generates complete, production-ready JSON for any automation platform.

## Supported Platforms

- **Power Automate** (Microsoft)
- **n8n** (Open-source)
- **Make** (formerly Integromat)
- **Zapier**
- **Other JSON-based workflow platforms**

## Purpose

This skill generates complete automation workflows by:
1. Taking implementation plan or requirements as input
2. Validating platform compatibility
3. Using flow-builder sub-agent to generate complete JSON
4. Ensuring all best practices are implemented
5. Producing ready-to-import workflow JSON

## When This Skill Activates

Automatically activates when user:
- Has implementation plan: "Build this workflow from the plan"
- Provides requirements: "Create a workflow that does X, Y, Z"
- Requests JSON generation: "Generate the flow JSON"
- Has plan from automation-brainstorm: "Use this plan to build the flow"
- Keywords: "build flow", "create workflow", "generate JSON", "implement this"

**Prerequisites**:
- Platform must be specified (or will ask)
- Requirements must be clear (or will request clarification)

**Does NOT activate when**:
- User needs help planning (use automation-brainstorm)
- User has error to debug (use automation-debugger)
- User wants validation only (use automation-validator)

## Core Workflow

### Phase 1: Input Analysis

1. **Determine Input Type**

   **Type A: Implementation Plan** (from automation-brainstorm)
   - Structured markdown plan
   - Contains all sections (trigger, actions, error handling, etc.)
   - Platform specified
   - Ready to build → Proceed to Phase 2

   **Type B: Direct Requirements** (user provided)
   - User describes what they want
   - May be less structured
   - Needs clarification → Gather requirements

2. **Verify Platform**

   Check if platform specified:
   - In plan: Check "Platform" section
   - In message: Look for platform mention
   - If missing: Ask using AskUserQuestion

   ```
   Use AskUserQuestion tool:

   Question: "Which platform should I generate this workflow for?"
   Header: "Platform"
   Options:
   - Power Automate (Microsoft, generates .json for "Paste code" feature)
   - n8n (Open-source, generates workflow.json for import)
   - Make (Integromat, generates scenario blueprint.json)
   - Zapier (Generates zap JSON for import API)
   - Other (Specify platform and format needed)
   ```

3. **Validate Requirements Completeness**

   Essential elements needed:
   - ✅ Trigger type and configuration
   - ✅ Main actions/steps
   - ✅ Data flow between steps
   - ✅ Error handling requirements
   - ⚠️  Optional: Specific connectors, advanced config

   If missing critical info:
   ```
   Use AskUserQuestion tool to gather missing pieces:

   Example for missing trigger:
   Question: "What should trigger this workflow?"
   Header: "Trigger"
   Options: [Schedule/Event/Webhook/Manual]

   Example for missing actions:
   Question: "What are the main actions this workflow should perform?"
   Header: "Actions"
   MultiSelect: true
   Options: [Based on context]
   ```

### Phase 2: Build Workflow with Sub-Agent

**CRITICAL**: Use Task tool to launch flow-builder sub-agent.

```
Use Task tool with subagent_type="general-purpose" or "Plan"

Prompt: "Generate complete workflow JSON for [PLATFORM] with the following specification:

## Platform
[Power Automate / n8n / Make / Zapier / Other]

## Complete Specification

[IF FROM PLAN: Paste entire implementation plan here]

[IF FROM REQUIREMENTS: Structure requirements as:]

### Trigger
Type: [Schedule/Event/Webhook/Manual]
Configuration:
- [Parameter 1]: [Value]
- [Parameter 2]: [Value]
Platform connector/node: [Specific component]

### Actions/Steps

#### Step 1: [Name]
Purpose: [What it does]
Connector/Node: [Platform-specific component]
Inputs:
- [Input 1]: [Value/Expression]
- [Input 2]: [Value/Expression]
Outputs: [What this step produces]

#### Step 2: [Name]
[Same structure]

[Continue for all steps]

### Conditional Logic
[If applicable, describe conditions and branching]

### Error Handling
Global strategy: [Scope/Try-catch/Error boundary]
Step-specific handling:
- [Step 1]: [On error behavior]
- [Step 2]: [On error behavior]

### Performance Configuration
- API rate limits: [Delays/Throttling needed]
- Batching: [Batch size if applicable]
- Concurrency: [Sequential/Parallel configuration]

### Security
- Authentication: [Method for each connector]
- Sensitive data: [Handling strategy]

### Monitoring
- Logging: [What to log]
- Alerts: [When to alert]

## Requirements for Generated JSON

CRITICAL - The output must be:

1. **Complete and Valid**
   - Syntactically correct JSON for [PLATFORM]
   - All required fields present
   - No placeholders or TODOs
   - Valid IDs/GUIDs as required by platform

2. **Platform-Specific Structure**
   - Follow [PLATFORM] schema exactly
   - Reference: Docs/{Platform}_Documentation/format-specification.md
   - Use correct connector/node names for platform
   - Follow platform naming conventions

3. **Fully Configured**
   - All triggers properly configured
   - All actions have complete inputs
   - Error handlers in place
   - Dependencies/runAfter chains correct
   - Variables initialized if needed

4. **Best Practices Implemented**
   - Error handling as specified
   - Performance optimizations (delays, batching)
   - Security configurations
   - Retry logic for transient errors
   - Idempotency where applicable

5. **Ready for Import**
   - Can be directly imported/pasted into [PLATFORM]
   - No manual editing needed
   - All expressions/formulas valid for platform
   - Connection placeholders where appropriate

## Platform-Specific Requirements

[IF Power Automate]:
- Schema: https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#
- Include $connections parameter
- Use correct operationId for each action
- Proper runAfter chains
- GUID format for operationMetadataId

[IF n8n]:
- nodes array with proper IDs
- connections object linking nodes
- position coordinates for visual layout
- Proper credential references
- Node versions specified

[IF Make]:
- modules array with proper IDs
- Proper connections/routing
- Scenario metadata
- Module configurations

[IF Zapier]:
- steps array
- Proper step types
- Action configurations
- Trigger setup

Return ONLY the complete JSON - no explanations, no markdown code blocks, no additional text.
Just the pure JSON ready for import."
```

**Expected Output from Flow-Builder Agent**:
- Complete, syntactically valid JSON
- Platform-specific format
- All triggers and actions configured
- Error handling implemented
- Performance optimizations applied
- Ready for immediate import

### Phase 3: Validate Generated JSON

Before presenting to user:

1. **Syntax Check**
   - Valid JSON (balanced brackets, proper escaping)
   - No trailing commas
   - Correct structure

2. **Completeness Check**
   - All actions from plan included
   - Trigger properly configured
   - Error handlers present
   - Dependencies/connections valid

3. **Platform Compliance**
   - Follows platform schema
   - Uses valid connector/node names
   - Correct ID/GUID format
   - Platform-specific requirements met

If validation fails → Retry with flow-builder agent with specific corrections needed

### Phase 4: Present Workflow JSON

Format output for user:

```markdown
# Workflow JSON Generated ✅

## Platform
[Platform Name]

## Summary
- **Trigger**: [Trigger type]
- **Actions**: [Count] actions/nodes
- **Error Handling**: [Strategy implemented]
- **Status**: Ready for import

---

## Complete Workflow JSON

**Instructions**: Copy the entire JSON below and import into [PLATFORM]:

[IF Power Automate]: Paste into Power Automate using "Paste code" feature
[IF n8n]: Import via Settings → Import Workflow
[IF Make]: Import via Scenarios → Create new → Import Blueprint
[IF Zapier]: Use Zapier CLI or import API

```json
{
  // Complete workflow JSON here
}
```

---

## What's Included

✅ **Trigger Configuration**
- Type: [Trigger type]
- Configuration: [Key settings]

✅ **Actions/Steps** ([Count] total)
1. [Action 1 name]: [What it does]
2. [Action 2 name]: [What it does]
[Continue for all actions]

✅ **Error Handling**
- Global error handler: [Yes/No]
- Step-level handlers: [Which steps]
- Retry logic: [Where applied]
- Notifications: [Where configured]

✅ **Performance Optimizations**
- API throttling: [Delays/Limits]
- Batching: [If applicable]
- Concurrency: [Configuration]

✅ **Security**
- Authentication: [Methods used]
- Sensitive data: [How handled]

---

## Next Steps

1. **Import into [PLATFORM]**
   - [Platform-specific import instructions]

2. **Configure Connections**
   - [List of connections to configure]
   - [Authentication requirements]

3. **Test the Workflow**
   - Run with sample data
   - Verify error handling
   - Check all actions execute correctly

4. **Validate with automation-validator** (Recommended)
   - Run: "Validate this workflow JSON"
   - Checks for best practices and potential issues

5. **Deploy**
   - Test environment first
   - Monitor initial runs
   - Deploy to production

---

## Configuration Notes

[Any platform-specific notes]:
- After import, configure [connections/credentials]
- Verify [specific settings]
- Adjust [parameters] for your environment

---

## Testing Recommendations

**Test Cases**:
1. Happy path: [Normal execution]
2. Error scenarios: [What to test]
3. Edge cases: [Boundary conditions]

**Validation Points**:
- All actions execute in correct order
- Error handling triggers correctly
- Data transforms as expected
- Performance is acceptable

---

*Generated by automation-build-flow skill. Ready for immediate import into [PLATFORM].*
```

## Output Format Variations by Platform

### Power Automate

```json
{
  "definition": {
    "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
      "$connections": {
        "defaultValue": {},
        "type": "Object"
      }
    },
    "triggers": {
      "trigger_name": {
        "type": "Recurrence",
        "recurrence": {
          "frequency": "Hour",
          "interval": 1
        }
      }
    },
    "actions": {
      "action_1": {
        "type": "ApiConnection",
        "inputs": { /* ... */ },
        "runAfter": {}
      }
    }
  },
  "schemaVersion": "1.0.0.0"
}
```

### n8n

```json
{
  "name": "Workflow Name",
  "nodes": [
    {
      "parameters": { /* ... */ },
      "name": "Node Name",
      "type": "n8n-nodes-base.nodeName",
      "typeVersion": 1,
      "position": [250, 300],
      "id": "uuid"
    }
  ],
  "connections": {
    "Node1": {
      "main": [[{"node": "Node2", "type": "main", "index": 0}]]
    }
  }
}
```

### Make

```json
{
  "name": "Scenario Name",
  "flow": [
    {
      "id": 1,
      "module": "gateway:CustomWebHook",
      "parameters": { /* ... */ }
    }
  ],
  "metadata": {
    "version": 1
  }
}
```

### Zapier

```json
{
  "title": "Zap Name",
  "steps": [
    {
      "type": "trigger",
      "app": "app_name",
      "event": "event_name",
      "params": { /* ... */ }
    }
  ]
}
```

## Best Practices

### 1. Complete Specification to Sub-Agent

```
Provide ALL details to flow-builder:
- Complete plan or requirements
- Platform-specific connector names
- All configurations and parameters
- Error handling requirements
- Performance settings

Don't assume sub-agent knows context!
```

### 2. Validate Before Presenting

```
Always check generated JSON:
✅ Syntax valid
✅ Structure complete
✅ Platform schema compliance
✅ No placeholders/TODOs
✅ All actions present

If issues found → Regenerate with corrections
```

### 3. Clear Import Instructions

```
Provide platform-specific import steps:
- Where to import (exact menu path)
- What to configure after import
- Common issues to watch for
- Validation recommendations
```

### 4. Error Handling Always Included

```
Never skip error handling:
- Global error handler (scope/try-catch)
- Action-level handlers where needed
- Retry logic for transient errors
- Notifications on critical failures
```

### 5. Performance by Default

```
Always include performance optimizations:
- API rate limit respect (delays)
- Batching for high-volume
- Concurrency configuration
- Filtering at source
```

## Integration with Other Skills

### Workflow Progression

```
automation-brainstorm
    ↓
Implementation Plan
    ↓
automation-build-flow (this skill)
    ↓
Complete Workflow JSON
    ↓
automation-validator (recommended)
    ↓
Deploy to Platform
```

### From automation-brainstorm

**Perfect Integration**:
- Receives complete implementation plan
- All sections populated
- Platform specified
- Best practices researched
- Ready to build immediately

**How to Handle**:
1. Extract platform from plan
2. Pass entire plan to flow-builder sub-agent
3. Generate JSON
4. Present to user

### To automation-validator

**Recommended Flow**:
```
After JSON generation:
"Would you like me to validate this workflow before you import it?
I can run automation-validator to check for potential issues."
```

**If user agrees**:
- Save JSON to temp file
- Trigger automation-validator
- Show validation report
- Fix any issues found
- Regenerate if needed

### From Direct Requirements

**If user provides requirements without plan**:
1. Gather essential info (platform, trigger, actions)
2. Use AskUserQuestion for missing pieces
3. Generate JSON from requirements
4. May be simpler than brainstorm output
5. Suggest brainstorm for complex workflows

## Common Scenarios

### Scenario 1: Build from Brainstorm Plan

**User**: "Build the workflow from the plan above"

**Skill**:
1. Identifies plan in conversation history
2. Extracts platform (e.g., "n8n")
3. Passes complete plan to flow-builder sub-agent
4. Receives complete n8n workflow JSON
5. Validates JSON structure
6. Presents to user with import instructions

### Scenario 2: Build from Simple Requirements

**User**: "Create a Power Automate flow that runs daily and emails me a list of new files from OneDrive"

**Skill**:
1. Platform specified → Power Automate ✓
2. Trigger clear → Schedule (daily) ✓
3. Actions clear → Get files, Send email ✓
4. Generates structured spec for flow-builder
5. Receives Power Automate JSON
6. Presents with configuration notes

### Scenario 3: Missing Platform

**User**: "Build a workflow that syncs database to API"

**Skill**:
1. Platform not specified → Ask user
2. User selects "Make"
3. Clarifies: Which database? Which API?
4. Gathers configuration details
5. Generates Make scenario JSON
6. Presents with import instructions

### Scenario 4: Complex Multi-Step

**User**: "Implement the workflow plan for high-volume Salesforce sync"

**Skill**:
1. References plan (contains all details)
2. Platform: n8n (from plan)
3. Passes comprehensive spec to flow-builder:
   - Scheduled trigger (every 5 minutes)
   - Salesforce query with pagination
   - Data transformation nodes
   - Batch processing (100 records)
   - Error handling with retry
   - Notification on failure
4. Receives complex n8n workflow (20+ nodes)
5. Validates all connections
6. Presents with testing recommendations

## Quality Checklist

Before delivering JSON, verify:

- [ ] Platform correctly identified
- [ ] Flow-builder sub-agent used (never hand-code JSON)
- [ ] Generated JSON is syntactically valid
- [ ] All actions from plan/requirements included
- [ ] Trigger properly configured
- [ ] Error handling implemented
- [ ] Performance optimizations applied
- [ ] Platform schema compliance verified
- [ ] No placeholders or TODOs in JSON
- [ ] Import instructions provided
- [ ] Configuration notes included
- [ ] Next steps clearly explained
- [ ] Validation recommended

## Advanced Features

### Iterative Refinement

If user wants changes:
```
"Add email notification when it fails"
→ Regenerate with updated spec
→ Add email action to error handler
→ Present updated JSON
```

### Partial JSON Updates

If user has JSON and wants to modify:
```
"This workflow needs better error handling"
→ Read existing JSON
→ Identify error handling gaps
→ Regenerate with improvements
→ Present updated JSON
```

### Multi-Platform Generation

If user wants same workflow for different platforms:
```
"Generate this for both Power Automate and n8n"
→ Generate for Power Automate
→ Generate for n8n
→ Present both with comparison notes
```

## Troubleshooting

### Sub-Agent Returns Invalid JSON

**Problem**: JSON has syntax errors or missing elements

**Solution**:
1. Validate with JSON parser
2. Identify specific issues
3. Regenerate with detailed corrections:
   ```
   "Previous generation had [SPECIFIC_ISSUE].
   Regenerate with correct [CORRECTION]."
   ```

### Platform Schema Mismatch

**Problem**: JSON doesn't match platform schema

**Solution**:
1. Reference platform format documentation
2. Identify schema violations
3. Provide correct schema example to sub-agent
4. Regenerate with schema compliance focus

### Missing Critical Configuration

**Problem**: Generated JSON missing key settings

**Solution**:
1. Review original spec
2. Identify what's missing
3. Add explicit requirement to sub-agent prompt
4. Regenerate with complete spec

### Ambiguous Requirements

**Problem**: Requirements unclear, can't generate reliably

**Solution**:
1. Don't guess!
2. Use AskUserQuestion to clarify
3. Get specific details
4. Generate only when requirements clear

## Documentation References

Skills should reference:
- `Docs/{Platform}_Documentation/` - Platform docs
- Platform-specific format specifications
- Connector/node documentation
- Best practices guides

---

**This skill is the build engine for automation workflows. Always generates complete, production-ready JSON using flow-builder sub-agent. Never hand-codes workflow JSON.**
