---
name: operation-manual-writer
description: Create standardized business operation manuals, procedures, and documentation following corporate guidelines. Use this skill when the user needs to create or update business documents such as release procedures, work instructions, operation manuals, regulations, or standard operating procedures (SOPs). Triggers include requests like "業務マニュアル作成", "手順書を書いて", "operation manual", "create procedure document", or when standardized business documentation is needed.
---

# Operation Manual Writer

## Overview

This skill creates standardized business operation documentation (manuals, procedures, SOPs, regulations) following corporate documentation guidelines. It ensures consistent structure, clear responsibilities, and practical usability across all business documents.

## When to Use This Skill

Use this skill for creating:
- **Development procedures** (release, testing, environment setup)
- **Operation manuals** (daily reports, weekly reports, application flows, incident response)
- **Administrative procedures** (attendance, expense reimbursement, approval processes)
- **Standard Operating Procedures (SOPs)** for any business process
- **Regulations and policies** requiring standardized format

## Document Types Covered

1. **Release/Deployment Procedures**
2. **Testing Procedures**
3. **Operational Manuals**
4. **Administrative Instructions**
5. **Incident Response Guides**
6. **Policy Documents**
7. **Training Materials**

## Workflow

### 1. Gather Requirements

Ask the user to provide:
- **Purpose**: What is this document for?
- **Target audience**: Who will use this document?
- **Scope**: What processes/activities does it cover?
- **Specific steps**: What are the actual procedures (if known)?
- **Roles**: Who is responsible, who approves, who confirms?

**Example prompt**: "Please tell me: (1) document purpose, (2) target users, (3) process overview, (4) any specific steps"

### 2. Load Guidelines

**CRITICAL**: Before creating any document, read the complete guidelines:

```
references/business-document-guidelines.md
```

These guidelines define:
- Required document sections (7 mandatory headings)
- Writing style and formatting rules
- Responsibility assignment (RACI matrix)
- Version control and approval flow
- Template structure

### 3. Create Document

Follow the standard structure from guidelines:

**Mandatory sections (7 required headings):**
1. **目的 (Purpose)**: Why this document exists
2. **適用範囲 (Scope)**: Who/what it applies to
3. **責任と役割 (Responsibilities and Roles)**: RACI matrix
4. **手順・ルール (Procedures/Rules)**: Step-by-step instructions
5. **例外・注意点 (Exceptions/Cautions)**: Edge cases and important notes
6. **関連ドキュメント (Related Documents)**: References and links
7. **改訂履歴 (Revision History)**: Change log with dates

### 4. Format and Polish

Apply formatting standards:
- Hierarchical numbering (1 → 1.1 → 1.1.1)
- Definitive language (avoid "できれば", "なるべく")
- Date format: YYYY/MM/DD
- Tables and checklists for clarity
- Numbered lists for sequential steps

### 5. Save Document

Save the completed manual to the user's specified location or suggest:

```
operation-manuals/{category}/{document-name}.md
```

## Usage Examples

**Example 1: Release Procedure Manual**

User: "リリース手順書を作成してください"

Agent questions:
- What system/service is being released?
- Who performs the release? (developer, ops team, manager)
- What are the steps? (code freeze, testing, deployment, verification)
- Any approval required?

Agent creates: Structured release manual with all 7 sections

**Example 2: Daily Report Guidelines**

User: "日報の記録ルールを作成して"

Agent questions:
- Who submits daily reports?
- What information should be included?
- Where are reports submitted?
- Any review process?

Agent creates: Daily report policy document with examples

**Example 3: Incident Response Procedure**

User: "インシデント対応手順を整備したい"

Agent questions:
- What types of incidents? (system down, security, data issues)
- Who is on the response team?
- What are the escalation steps?
- Communication protocol?

Agent creates: Incident response manual with clear escalation paths

## Document Quality Standards

Every document must include:
- ✅ Clear purpose statement
- ✅ Defined scope and target audience
- ✅ RACI matrix (Responsible, Accountable, Consulted, Informed)
- ✅ Numbered, sequential procedures
- ✅ Exception handling guidance
- ✅ References to related documents
- ✅ Revision history with initial version

Avoid:
- ❌ Ambiguous language ("maybe", "preferably")
- ❌ Missing responsibility assignments
- ✅ Unnumbered procedures
- ❌ Inconsistent formatting
- ❌ Missing version control


## Resources

### references/

- **business-document-guidelines.md**: Complete guidelines for creating standardized business operation documents, including required sections, formatting rules, and templates. MUST be read before creating any business documentation.
