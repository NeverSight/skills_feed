---
name: agent-prompts
description: Ready-to-use prompt templates for specialized agents. Use when building n8n workflows, AI integrations, or sales materials. Contains structured prompts for automation-architect, llm-engineer, and sales-automator agents.
---

# Agent Prompts

Ready-to-use prompt templates for specialized Claude Code agents.

## Quick Navigation

| Agent Type | Prompts File | Use Case |
|------------|--------------|----------|
| Workflow Building | `references/workflow-builder.md` | n8n automation workflows |
| AI Integration | `references/ai-workflow.md` | Claude/Gemini AI workflows |
| Sales Materials | `references/sales-proposal.md` | Proposals, emails, pricing |

## How to Use

1. Open the relevant reference file
2. Copy the prompt template
3. Fill in the bracketed placeholders
4. Use with the specified agent

### Example Usage

```
Use the automation-architect agent to:

Build an n8n workflow for ACME Corp:
**Problem:** Manual invoice processing takes 10 hours/week
**Trigger:** Email attachment
**Data sources:** Gmail, QuickBooks
**Output:** Slack notification + QuickBooks entry
```

## Available Prompt Templates

### Workflow Builder (`references/workflow-builder.md`)
- Basic Workflow Prompt
- Lead Capture Workflow
- Data Sync Workflow
- Notification Hub
- Report Generator
- E-commerce Order Workflow
- Customer Support Workflow
- Scheduled Batch Process
- Approval Workflow
- Integration Pattern

### AI Workflow (`references/ai-workflow.md`)
- Basic AI Workflow
- Customer Support AI Agent
- Document Processing AI
- Lead Qualification AI
- Email Response Generator
- Content Summarizer
- Meeting Notes AI
- Multi-Model Fallback Pattern
- AI Agent with Tools
- Data Extraction Prompt Template
- Classification Prompt Template

### Sales Proposal (`references/sales-proposal.md`)
- Full Proposal Generation
- Cold Outreach Email
- Follow-Up Email Sequence
- Objection Response Scripts
- ROI Calculator Content
- Case Study Request
- Discovery Call Prep
- Pricing Page Copy
- Competitor Comparison
- Upsell Email

## Agent Reference

| Agent | Description |
|-------|-------------|
| `automation-architect` | n8n/make.com workflow design |
| `llm-engineer` | AI/RAG systems, prompt engineering |
| `customer-sales-automation:sales-automator` | Cold emails, proposals |
| `code-documentation:docs-architect` | Technical documentation |
| `code-documentation:tutorial-engineer` | Training materials |
