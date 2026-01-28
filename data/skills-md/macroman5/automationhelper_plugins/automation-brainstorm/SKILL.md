---
name: automation-brainstorm
description: Interactive workflow design advisor for Power Automate, n8n, Make, Zapier and other platforms. Guides users through planning automation workflows with smart questions about triggers, actions, data flow, and error handling. Uses research sub-agent to find best practices and generates detailed implementation plan. Triggers when user mentions "create workflow", "build flow", "design automation", "need ideas for", or describes workflow requirements without having a complete design.
---

# Automation Brainstorm

Interactive workflow design advisor that helps plan and architect automation workflows through guided conversations.

## Supported Platforms

- **Power Automate** (Microsoft)
- **n8n** (Open-source)
- **Make** (formerly Integromat)
- **Zapier**
- **Other JSON-based workflow platforms**

## Purpose

This skill provides expert guidance for planning automation workflows by:
1. Understanding user requirements through interactive questions
2. Recommending triggers, actions, and data flow patterns
3. Researching platform-specific best practices
4. Identifying potential issues early
5. Generating detailed implementation plan for automation-build-flow

## When This Skill Activates

Automatically activates when user:
- Mentions creating/building a new workflow: "I want to create a flow that..."
- Asks for ideas/advice: "What's the best way to automate..."
- Describes requirements without complete design: "I need to sync data between..."
- Requests planning help: "Help me design a workflow for..."
- Keywords: "create flow", "build automation", "design workflow", "need ideas"

**Does NOT activate when**:
- User has complete plan and wants to build (use automation-build-flow)
- User has error and needs debugging (use automation-debugger)
- User wants to validate existing flow (use automation-validator)

## Core Workflow

### Phase 1: Platform & Context Discovery

**CRITICAL**: Always determine the platform first!

1. **Check if Platform Specified**
   - Look for platform mention in user message
   - Power Automate, n8n, Make, Zapier, etc.

2. **Ask for Platform if Missing**
   ```
   Use AskUserQuestion tool:

   Question: "Which automation platform will you be using for this workflow?"
   Header: "Platform"
   Options:
   - Power Automate (Microsoft cloud platform with Office 365 integration)
   - n8n (Open-source, self-hosted, node-based automation)
   - Make (Visual scenario builder, formerly Integromat)
   - Zapier (SaaS automation platform, easy to use)
   - Other (Specify in custom response)
   ```

3. **Gather Initial Requirements**
   - What problem are they solving?
   - What systems need to connect?
   - What's the expected frequency?
   - Any specific constraints?

### Phase 2: Interactive Design Session

Use AskUserQuestion tool for guided discovery. Ask 2-4 questions per iteration.

#### Question Set 1: Trigger Design

```
Use AskUserQuestion tool:

Question 1: "What should trigger this workflow?"
Header: "Trigger Type"
Options:
- Schedule (Run on a regular schedule - hourly, daily, etc.)
- Event (Triggered by an event - new email, file upload, etc.)
- Webhook (Triggered by HTTP request from external system)
- Manual (Run on demand by user)

Question 2: "How frequently will this workflow run?"
Header: "Frequency"
Options:
- High (Multiple times per minute or real-time)
- Medium (Every few minutes to hourly)
- Low (Daily, weekly, or on-demand)
- Variable (Depends on external events)
```

#### Question Set 2: Data & Actions

```
Use AskUserQuestion tool:

Question 1: "What data sources will you read from?"
Header: "Data Sources"
MultiSelect: true
Options:
- Databases (SQL, NoSQL, cloud databases)
- APIs (REST APIs, webhooks, web services)
- Files (CSV, Excel, JSON, XML, documents)
- Email (Read emails, attachments, process content)
- Other (Cloud storage, messaging systems, etc.)

Question 2: "What actions will the workflow perform?"
Header: "Actions"
MultiSelect: true
Options:
- Transform data (Parse, filter, map, aggregate)
- Create/Update records (Database, CRM, systems)
- Send notifications (Email, Slack, Teams, SMS)
- File operations (Upload, download, convert)
- Other (Custom API calls, complex logic)
```

#### Question Set 3: Error Handling & Requirements

```
Use AskUserQuestion tool:

Question 1: "How critical is this workflow?"
Header: "Criticality"
Options:
- Critical (Must not fail, needs immediate alerts)
- Important (Should retry on failure, log errors)
- Standard (Basic error handling, can fail occasionally)
- Low (Minimal error handling, best effort)

Question 2: "What are your main concerns?"
Header: "Concerns"
MultiSelect: true
Options:
- Performance (Speed, processing large volumes)
- Reliability (Must not lose data, retry logic)
- Security (Handle sensitive data, authentication)
- Monitoring (Need visibility, logging, alerts)
- Cost (API limits, execution costs, efficiency)
```

### Phase 3: Research Best Practices

**CRITICAL**: Use Task tool to launch research sub-agent.

```
Use Task tool with subagent_type="Explore" and thoroughness="very thorough"

Prompt: "Research best practices for [PLATFORM] workflow with the following requirements:

Platform: [Power Automate / n8n / Make / Zapier]
Trigger: [USER_SELECTED_TRIGGER]
Data Sources: [USER_SELECTED_SOURCES]
Actions: [USER_SELECTED_ACTIONS]
Criticality: [USER_SELECTED_CRITICALITY]

Search in Docs/{Platform}_Documentation/ for:
1. Recommended patterns for this trigger type
2. Best practices for the selected data sources
3. Error handling patterns for this criticality level
4. Performance optimization (API limits, batching, etc.)
5. Security best practices for this use case
6. Common pitfalls to avoid

Return:
- Specific connector/node recommendations
- Architectural patterns
- Error handling strategies
- Performance considerations
- Security recommendations
- Example implementations if available"
```

**Expected Research Output**:
- Platform-specific connector/node recommendations
- Best practice patterns from documentation
- Known limitations and workarounds
- Error handling strategies
- Performance optimization tips

### Phase 4: Design Recommendations

Based on user requirements and research findings:

1. **Architecture Overview**
   - Recommended trigger configuration
   - Data flow diagram (textual)
   - Key actions/nodes sequence
   - Branching/conditional logic

2. **Implementation Considerations**
   - API rate limits and throttling
   - Data transformation needs
   - Error handling strategy
   - Retry logic recommendations
   - Monitoring and logging

3. **Platform-Specific Recommendations**
   - Best connectors/nodes for the platform
   - Platform quirks to be aware of
   - Performance optimizations
   - Cost considerations

4. **Potential Issues & Solutions**
   - Common problems for this pattern
   - Preventive measures
   - Fallback strategies

### Phase 5: Generate Implementation Plan

Create detailed, structured plan ready for automation-build-flow skill.

## Implementation Plan Format

```markdown
# Workflow Implementation Plan

## Platform
[Power Automate / n8n / Make / Zapier]

## Overview
[1-2 sentence description of what the workflow does]

## Requirements Summary
- **Trigger**: [Trigger type and configuration]
- **Frequency**: [Expected execution frequency]
- **Data Sources**: [List of sources]
- **Actions**: [List of main actions]
- **Criticality**: [Criticality level]

## Architecture

### 1. Trigger Configuration
**Type**: [Schedule / Event / Webhook / Manual]
**Configuration**:
- Parameter 1: [Value]
- Parameter 2: [Value]

**Platform-Specific**:
- Connector/Node: [Name]
- Special considerations: [Any platform quirks]

### 2. Data Flow

#### Step 1: [Action Name]
**Purpose**: [What this step does]
**Connector/Node**: [Platform-specific component]
**Configuration**:
- Input: [Data source/format]
- Processing: [What happens]
- Output: [Result format]

**Error Handling**:
- On failure: [Retry / Skip / Alert]
- Fallback: [Alternative action if needed]

#### Step 2: [Action Name]
[Same structure as Step 1]

#### Step N: [Action Name]
[Same structure]

### 3. Conditional Logic

**Condition 1**: [Description]
- If true → [Action path]
- If false → [Alternative path]

**Condition 2**: [Description]
[Same structure]

### 4. Error Handling Strategy

**Global Error Handler**:
- Wrap critical sections in: [Scope / Try-Catch / Error boundary]
- On error:
  1. Log error details
  2. [Retry logic if applicable]
  3. Send notification to: [Email / Slack / Teams]

**Action-Specific Error Handling**:
- [Action 1]: [Specific handling]
- [Action 2]: [Specific handling]

### 5. Performance Optimization

**API Rate Limiting**:
- [Connector/API]: [Limit] calls per [time period]
- Mitigation: [Delays / Batching / Throttling strategy]

**Data Processing**:
- Batch size: [Number] items per iteration
- Pagination: [Strategy if needed]
- Filtering: [Filter at source to reduce volume]

**Concurrency**:
- Parallel execution: [Yes/No and configuration]
- Sequential processing: [When and why]

### 6. Security Considerations

**Authentication**:
- [Connector/API]: [Auth method]
- Credential storage: [Secure parameters / Connection references]

**Data Handling**:
- Sensitive data: [Encryption / Masking strategy]
- Logging: [What to log / What to exclude]
- Compliance: [GDPR / HIPAA / Other requirements]

### 7. Monitoring & Logging

**Logging Strategy**:
- Log points: [Where to log]
- Log level: [Info / Warning / Error]
- Log destination: [Platform logs / External system]

**Monitoring**:
- Success metrics: [What indicates success]
- Failure alerts: [When to alert]
- Performance metrics: [Execution time / Volume processed]

## Best Practices Applied

1. **[Platform] Best Practice 1**
   - Applied in: [Step/Action]
   - Benefit: [Why this helps]

2. **[Platform] Best Practice 2**
   - Applied in: [Step/Action]
   - Benefit: [Why this helps]

[Continue for all relevant best practices]

## Known Limitations & Workarounds

1. **Limitation**: [Description]
   - Impact: [How it affects the workflow]
   - Workaround: [Solution implemented]
   - Reference: [Docs/{Platform}_Documentation/file.md]

2. **Limitation**: [Description]
   [Same structure]

## Testing Strategy

**Test Cases**:
1. Happy path: [Normal execution scenario]
2. Error scenarios: [What failures to test]
3. Edge cases: [Boundary conditions]
4. Load testing: [If high volume]

**Validation**:
- Data accuracy: [How to verify]
- Performance: [Acceptable execution time]
- Error handling: [Verify failures handled correctly]

## Deployment Checklist

- [ ] All credentials configured securely
- [ ] Error handling tested
- [ ] Monitoring/alerts set up
- [ ] Documentation created
- [ ] Stakeholders notified
- [ ] Backup/rollback plan ready

## Next Steps

1. Review this plan with stakeholders
2. Use **automation-build-flow** skill to generate workflow JSON
3. Deploy to test environment
4. Execute test cases
5. Monitor initial runs
6. Deploy to production

## References

**Documentation**:
- [Docs/{Platform}_Documentation/[relevant-files].md]

**Best Practices Source**:
- [Specific sections from platform docs]

---

*This plan was generated by automation-brainstorm skill and is ready for automation-build-flow*
```

## Output Delivery

After generating the plan:

1. **Present Complete Plan**
   - Show full structured plan above
   - Highlight key decisions and rationale

2. **Summarize Key Points**
   - Platform and trigger choice
   - Main actions and data flow
   - Critical considerations (performance, security, errors)

3. **Next Steps**
   - Suggest: "Ready to build? Use automation-build-flow with this plan"
   - Or: "Need changes? I can refine any section"

4. **Save Plan** (Optional)
   - Suggest saving plan to file: `workflow_plan_{name}.md`
   - Makes it easy to reference later

## Best Practices

### 1. Always Ask for Platform First
```
If platform not specified → Use AskUserQuestion immediately
Do not proceed with generic advice
Platform determines connectors, patterns, limitations
```

### 2. Iterative Questioning
```
Don't ask all questions at once
2-4 questions per iteration
Adjust questions based on previous answers
Use multiSelect for non-exclusive choices
```

### 3. Research Documentation
```
Always use research sub-agent
Don't rely on general knowledge
Cite specific documentation files
Platform-specific recommendations only
```

### 4. Structured Plan Output
```
Follow the plan format exactly
Include all sections
Be specific (no placeholders or TODOs)
Ready for automation-build-flow consumption
```

### 5. Consider User Experience Level
```
Beginner → More explanation, simpler patterns
Intermediate → Best practices, common patterns
Advanced → Performance optimization, complex patterns
```

## Integration with Other Skills

### Workflow Progression

```
User idea
    ↓
automation-brainstorm (this skill)
    ↓
Implementation Plan
    ↓
automation-build-flow
    ↓
Complete workflow JSON
    ↓
automation-validator
    ↓
Deploy to platform
```

### Skill Handoffs

**To automation-build-flow**:
- Output: Complete implementation plan
- Format: Markdown with all sections
- Contains: All technical details for JSON generation

**To automation-debugger** (if user mentions problems):
- Redirect: "Sounds like you have an error. Let me activate automation-debugger"

**To automation-validator** (if user wants to check existing flow):
- Redirect: "For validation, use automation-validator skill"

## Example Interactions

### Example 1: From Scratch

**User**: "I want to create a workflow that syncs customer data from Salesforce to our database"

**Skill**:
1. Asks: Platform? → User selects "n8n"
2. Asks: Trigger type? → User selects "Schedule"
3. Asks: Frequency? → User selects "Medium (hourly)"
4. Asks: Data sources? → User selects "APIs, Databases"
5. Asks: Criticality? → User selects "Important"
6. Research agent → Finds n8n Salesforce + database best practices
7. Generates plan → Complete implementation plan for n8n
8. Suggests → "Use automation-build-flow to generate the workflow JSON"

### Example 2: Vague Requirements

**User**: "I need something to handle incoming emails"

**Skill**:
1. Asks: Platform? → User selects "Power Automate"
2. Asks: What should happen when email arrives?
3. Asks: Which emails (all, specific sender, subject filter)?
4. Asks: What to do with email content?
5. Asks: Where to save/forward/process?
6. Research agent → Finds Power Automate email handling patterns
7. Generates plan → Detailed implementation plan
8. User reviews and approves

### Example 3: Performance-Critical

**User**: "Build high-volume API sync workflow for Make"

**Skill**:
1. Platform already specified → Make ✓
2. Asks: Trigger type? → User selects "Schedule"
3. Asks: Expected volume? → User: "10,000+ records/hour"
4. Asks: Data sources? → User selects "APIs"
5. Asks: Concerns? → User selects "Performance, Reliability, Cost"
6. Research agent → Finds Make performance best practices, API limits
7. Generates plan → Includes batching, throttling, error recovery
8. Highlights → Performance optimizations, cost considerations

## Quality Checklist

Before delivering plan, verify:

- [ ] Platform specified and confirmed
- [ ] All user requirements captured
- [ ] Research sub-agent consulted documentation
- [ ] Best practices from documentation applied
- [ ] All plan sections complete (no TODOs/placeholders)
- [ ] Platform-specific connectors/nodes recommended
- [ ] Error handling strategy defined
- [ ] Performance considerations addressed
- [ ] Security recommendations included
- [ ] Testing strategy provided
- [ ] Plan is actionable and specific
- [ ] Ready for automation-build-flow skill

## Advanced Features

### Refining the Plan

If user asks for changes:
```
"Can you add email notifications?"
→ Update relevant section
→ Add email action to data flow
→ Update error handling if needed
→ Regenerate updated plan
```

### Multiple Workflows

If requirements suggest multiple workflows:
```
"This should be split into 2 workflows:
1. [Workflow 1 purpose]
2. [Workflow 2 purpose]

Should I create separate plans?"
```

### Comparison Mode

If user unsure about platform:
```
"Would you like me to compare how this would work on:
- n8n vs Power Automate?
- Make vs Zapier?

I can show pros/cons for your use case"
```

## Common Patterns

### High-Volume Data Sync
- Schedule trigger with pagination
- Batching and throttling
- Incremental sync (track last run)
- Robust error handling

### Event-Driven Processing
- Webhook or event trigger
- Immediate processing
- Idempotency (handle duplicates)
- Fast response time

### File Processing
- File upload/creation trigger
- File size validation
- Chunked processing for large files
- Error handling per file

### Multi-System Integration
- Orchestration pattern
- Sequential or parallel execution
- Transaction handling
- Rollback strategy

## Troubleshooting

### User Unsure About Requirements

Guide with examples:
```
"Let me give you examples:
- E-commerce order processing
- Customer onboarding automation
- Report generation and distribution
- Data synchronization between systems

Which is closest to your use case?"
```

### Platform Choice Unclear

Provide guidance:
```
"Platform selection depends on:
- Power Automate: Best if you use Microsoft 365, cloud-native
- n8n: Best if you want self-hosted, open-source, full control
- Make: Best for visual design, many pre-built templates
- Zapier: Best for quick setup, ease of use, SaaS

What's your priority?"
```

## Documentation References

Skills should reference:
- `Docs/{Platform}_Documentation/` - Platform-specific docs
- `output-style/` - Output formatting standards
- Other skills for workflow context

---

**This skill is the starting point for creating new automation workflows. Always generates a complete, actionable plan ready for automation-build-flow skill.**
