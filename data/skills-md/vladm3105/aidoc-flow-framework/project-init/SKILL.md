---
title: "project-init: Initialize projects with AI Dev Flow framework"
name: project-init
description: Initialize projects with AI Dev Flow framework using domain-aware setup
tags:
  - sdd-workflow
  - shared-architecture
custom_fields:
  layer: null
  artifact_type: null
  architecture_approaches: [ai-agent-based, traditional-8layer]
  priority: shared
  development_status: active
  skill_category: utility
  upstream_artifacts: []
  downstream_artifacts: [BRD]
---

# project-init

## Purpose
Provide AI assistants with structured guidance for initializing brand new (greenfield) projects using the AI Dev Flow framework. This skill handles the one-time setup process that must occur BEFORE workflow execution begins.

**⚠️ CRITICAL**: This skill is for NEW PROJECT INITIALIZATION ONLY. For ongoing workflow execution on existing projects, use the `doc-flow` skill instead.

## When to Use This Skill

**Use project-init when:**
- Starting a brand new project from scratch (greenfield)
- No project folders exist yet
- Domain has not been selected
- Project structure needs to be initialized

**Do NOT use project-init when:**
- Project already has docs/ folder structure
- Domain is already configured
- Working on existing project
- → Use `doc-flow` skill instead for workflow execution

## Hand-off to doc-flow

After completing project initialization, AI Assistant **MUST** inform user:

```
✅ Project initialization complete!

Next: Use the `doc-flow` skill to begin workflow execution:
- Create BRD (Business Requirements)
- Create PRD (Product Requirements)
- Follow 15-layer architecture (Layers 0-14) with 11 artifact directories (BRD through TASKS): BRD → PRD → EARS → BDD → ADR → SYS → REQ → [IMPL] → [CTR] → SPEC → TASKS → Code → Tests → Validation
```

---

## Initialization Workflow (8 Steps)

### Step 0: Read Execution Rules

**File**: [AI_ASSISTANT_RULES.md]({project_root}/ai_dev_flow/AI_ASSISTANT_RULES.md)

**Purpose**: Understand core execution rules before starting

**Key Rules**:
1. Domain Selection FIRST
2. Create Folders BEFORE Documents
3. Apply Domain Configuration
4. Run Contract Questionnaire
5. Initialize Index Files
6. Validate Setup
7. Token Optimization
8. Tool-Specific Guidance

**Action**: AI Assistant reads this file to understand all 15 rules

---

### Step 1: Domain Selection (REQUIRED FIRST)

**File**: [DOMAIN_SELECTION_QUESTIONNAIRE.md]({project_root}/ai_dev_flow/DOMAIN_SELECTION_QUESTIONNAIRE.md)

**Purpose**: Determine project domain to load correct configuration

**AI Assistant Action**: Present questionnaire to user

```
═══════════════════════════════════════════════════════════
                 PROJECT DOMAIN SELECTION
═══════════════════════════════════════════════════════════

What is the purpose and focus of this new project?

Select one:

1. Financial Services (DEFAULT)
   - Trading platforms, banking, insurance, portfolio management
   - Regulatory: SEC, FINRA, SOX, Basel III, PCI-DSS

2. Software/SaaS
   - B2B/B2C software services, multi-tenant applications
   - Regulatory: SOC2, GDPR/CCPA, ISO 27001

3. Healthcare
   - EMR, telemedicine, medical devices, patient management
   - Regulatory: HIPAA, FDA, HITECH, 21 CFR Part 11

4. E-commerce
   - Retail, marketplace, subscription services
   - Regulatory: PCI-DSS, GDPR/CCPA, FTC

5. IoT (Internet of Things)
   - Connected devices, sensors, industrial systems
   - Regulatory: FCC, CE, UL/IEC, FDA (medical devices)

6. Other/Generic
   - Internal tools, utilities, custom domain
   - Regulatory: Company policies only

Enter selection (1-6) or press Enter for default (1):
```

**Output**: Domain selected, configuration file determined

**Domain Configuration Mapping**:
| Selection | Domain | Config File |
|-----------|--------|-------------|
| 1 or Enter | Financial Services | FINANCIAL_DOMAIN_CONFIG.md |
| 2 | Software/SaaS | SOFTWARE_DOMAIN_CONFIG.md |
| 3 | Healthcare | DOMAIN_ADAPTATION_GUIDE.md (Healthcare) |
| 4 | E-commerce | DOMAIN_ADAPTATION_GUIDE.md (E-commerce) |
| 5 | IoT | DOMAIN_ADAPTATION_GUIDE.md (IoT) |
| 6 | Other/Generic | GENERIC_DOMAIN_CONFIG.md |

---

### Step 2: Folder Structure Creation (REQUIRED SECOND)

**Rule**: AI Assistant **MUST** create complete directory structure BEFORE creating any documents.

**Why**: Prevents "file not found" errors, ensures proper organization

**IMPORTANT**: Ensure project root directory exists first:

```bash
# Create project root directory if it doesn't exist
mkdir -p {project_root}
cd {project_root}
```

> Replace `{project_root}` with your actual project path (e.g., `/opt/data/my_project`)

**Commands to Execute**:

```bash
# Core 11 artifact directories (BRD through TASKS)
mkdir -p docs/BRD
mkdir -p docs/PRD
mkdir -p docs/EARS
mkdir -p docs/BDD
mkdir -p docs/ADR
mkdir -p docs/SYS
mkdir -p docs/REQ
mkdir -p docs/IMPL
mkdir -p docs/CTR
mkdir -p docs/SPEC
mkdir -p docs/TASKS

# NOTE: REQ and CTR subdirectories are created on-demand by doc-req and doc-ctr skills
# when documents are generated. This ensures folders match actual project needs.

# Scripts directory
mkdir -p scripts

# Work plans directory (for /save-plan command output)
mkdir -p work_plans
```

**Validation**:
```bash
ls -la docs/  # Verify 11 artifact directories created
ls -la work_plans/  # Verify work_plans directory
```

---

### Step 3: Load Domain Configuration

**Files**:
- [FINANCIAL_DOMAIN_CONFIG.md]({project_root}/ai_dev_flow/FINANCIAL_DOMAIN_CONFIG.md) - Default
- [SOFTWARE_DOMAIN_CONFIG.md]({project_root}/ai_dev_flow/SOFTWARE_DOMAIN_CONFIG.md)
- [GENERIC_DOMAIN_CONFIG.md]({project_root}/ai_dev_flow/GENERIC_DOMAIN_CONFIG.md)

**Purpose**: Apply domain-specific terminology and placeholders

**AI Assistant Action**:
1. Read selected domain configuration file
2. Extract placeholder mappings
3. Store terminology for document generation

**Example Mappings**:

**Financial Services**:
```
[RESOURCE_COLLECTION] → Portfolio
[RESOURCE_ITEM] → Position
[USER_ROLE] → Trader / Portfolio Manager
[TRANSACTION] → Trade
[REGULATORY_REQUIREMENT] → SEC Rule 15c3-5
```

**Software/SaaS**:
```
[RESOURCE_COLLECTION] → Workspace
[RESOURCE_ITEM] → Resource
[USER_ROLE] → Account Admin / Member
[TRANSACTION] → API Call
[REGULATORY_REQUIREMENT] → SOC2 Control
```

**Generic**:
```
[RESOURCE_COLLECTION] → Collection
[RESOURCE_ITEM] → Entity
[USER_ROLE] → User
[TRANSACTION] → Action
[REGULATORY_REQUIREMENT] → Company Policy
```

---

### Step 4: Template Copying (Optional)

**Purpose**: Copy framework templates to project (optional step)

**Commands**:
```bash
# Create ai_dev_flow directory for framework templates
mkdir -p ai_dev_flow

# Copy all templates (if framework templates exist)
cp -r {framework_root}/ai_dev_flow/* ai_dev_flow/

# Copy validation scripts
cp {framework_root}/ai_dev_flow/scripts/*.py scripts/
```

**Directory Purpose**:
- `ai_dev_flow/` = Framework templates (BRD-TEMPLATE.md, examples/, etc.)
- `docs/` = Project documentation (BRD-01.md, PRD-01.md, etc.)

**Note**: This step is optional. Templates can also be referenced directly from framework location.

---

### Step 5: Contract Decision (REQUIRED)

**File**: [CONTRACT_DECISION_QUESTIONNAIRE.md]({project_root}/ai_dev_flow/CONTRACT_DECISION_QUESTIONNAIRE.md)

**Purpose**: Determine if CTR (Contracts) layer should be included in workflow

**AI Assistant Action**: Present questionnaire to user

```
═══════════════════════════════════════════════════════════
              CONTRACT DECISION QUESTIONNAIRE
═══════════════════════════════════════════════════════════

Does this project require API contracts or interface definitions?

Select all that apply:

1. ☐ REST/GraphQL APIs (External HTTP endpoints)
2. ☐ Event Schemas (Pub/Sub, message queues, webhooks)
3. ☐ Data Contracts (Shared database schemas, data models between services)
4. ☐ RPC/gRPC Interfaces (Service-to-service communication)
5. ☐ WebSocket APIs (Real-time bidirectional communication)
6. ☐ File Format Specifications (CSV, JSON, XML exchange formats)
7. ☐ None - Internal logic only
8. ☐ Unsure - Need guidance

Enter selections (comma-separated, e.g., "1,2" or single "7"):
```

**Decision Matrix**:
| Selection | Include CTR? | Workflow |
|-----------|--------------|----------|
| 1-6 | **YES** | REQ → IMPL → **CTR** → SPEC → TASKS |
| 7 | **NO** | REQ → IMPL → SPEC → TASKS |
| 8 | Ask follow-up questions | See CONTRACT_DECISION_QUESTIONNAIRE.md |

**Output**: Workflow determined (with or without CTR layer)

---

### Step 6: Index File Initialization + Document Control

**Purpose**: Create index files for each document type

**Document Control Requirements**:
All AI Dev Flow templates include a Document Control section with:
- Project metadata (name, version, date, owner, preparer, status)
- Document Revision History table
- Essential for traceability, change management, and regulatory compliance

**AI Assistant Must Emphasize**:
When creating documents from templates, users must complete the Document Control section with all required fields.

**Commands**:
```bash
# Create index files
touch docs/BRD/BRD-00_index.md
touch docs/prd/PRD-00_index.md
touch docs/ears/EARS-00_index.md
touch docs/BDD/BDD-00_index.md
touch docs/adrs/ADR-00_index.md
touch docs/sys/SYS-00_index.md
touch docs/REQ/REQ-00_index.md
touch docs/IMPL/IMPL-00_index.md
touch docs/CTR/CTR-00_index.md
touch docs/specs/SPEC-00_index.yaml
touch docs/TASKS/TASKS-00_index.md
```

**Index File Purpose**:
- Track all documents of each type
- Provide next available ID
- Document registry with status

---

### Step 7: Validation

**Purpose**: Verify setup complete and correct

**Validation Commands**:
```bash
# Verify directory structure
ls -laR docs/

# Verify index files exist
ls docs/*/index.* || ls docs/*/*_index.*

# Expected: 11 artifact directories (BRD through TASKS) + domain subdirectories
# Expected: 11 index files
```

**Success Criteria**:
- ✅ All 11 artifact directories exist (BRD, PRD, EARS, BDD, ADR, SYS, REQ, IMPL, CTR, SPEC, TASKS)
- ✅ Domain-specific subdirectories exist (risk/, trading/, tenant/, etc.)
- ✅ All index files created
- ✅ All templates include Document Control sections
- ✅ Validation scripts present (if copied)
- ✅ work_plans directory exists (for /save-plan command)

**Error Handling**:
- If folders missing: Re-run Step 2
- If index files missing: Re-run Step 6
- If domain subdirs missing: Check Step 1 domain selection

---

### Step 8: Project Ready - Hand-off to doc-flow

**AI Assistant Confirmation Message**:

```
═══════════════════════════════════════════════════════════
              PROJECT INITIALIZATION COMPLETE
═══════════════════════════════════════════════════════════

✓ Domain: [Financial Services / Software/SaaS / etc.]
✓ Folders: Created (11 artifact directories + domain subdirectories)
✓ Domain Config: Applied ([PLACEHOLDERS] → [domain terms])
✓ Contracts: [Included / Skipped] (CTR layer [active / inactive])
✓ Index Files: Initialized (11 files)
✓ Validation: Passed

Workflow Configuration:
[With CTR]:    REQ → IMPL → CTR → SPEC → TASKS → Code
[Without CTR]: REQ → IMPL → SPEC → TASKS → Code

═══════════════════════════════════════════════════════════
                      NEXT STEPS
═══════════════════════════════════════════════════════════

✅ Project structure ready for development!

Next: Use the `doc-flow` skill to begin workflow execution

Week 1 Tasks (see PROJECT_KICKOFF_TASKS.md):
- Day 1: Create BRD (Business Requirements)
- Day 2: Create PRD + EARS (Product Requirements)
- Day 3: Create BDD + ADR (Tests + Architecture)
- Day 4: Create SYS + REQ (System Specs + Requirements)
- Day 5: Create IMPL + CTR (Implementation Plan + Contracts)
- Day 6: Create SPEC (Technical Specifications)
- Day 7: Create TASKS + Validation

Invoke: doc-flow skill to start Day 1

═══════════════════════════════════════════════════════════
```

---

## Reference Files

All guidance files located in: `{project_root}/ai_dev_flow/`

### Core Guidance Files

1. **[AI_ASSISTANT_RULES.md]({project_root}/ai_dev_flow/AI_ASSISTANT_RULES.md)** - 15 execution rules
2. **[DOMAIN_SELECTION_QUESTIONNAIRE.md]({project_root}/ai_dev_flow/DOMAIN_SELECTION_QUESTIONNAIRE.md)** - Domain selection
3. **[CONTRACT_DECISION_QUESTIONNAIRE.md]({project_root}/ai_dev_flow/CONTRACT_DECISION_QUESTIONNAIRE.md)** - Contract decision
4. **[PROJECT_SETUP_GUIDE.md]({project_root}/ai_dev_flow/PROJECT_SETUP_GUIDE.md)** - Master setup guide
5. **[PROJECT_KICKOFF_TASKS.md]({project_root}/ai_dev_flow/PROJECT_KICKOFF_TASKS.md)** - Week 1 tasks
6. **[TRACEABILITY_SETUP.md]({project_root}/ai_dev_flow/TRACEABILITY_SETUP.md)** - Validation automation
7. **[QUICK_REFERENCE.md]({project_root}/ai_dev_flow/QUICK_REFERENCE.md)** - Quick reference card

### Domain Configuration Files

8. **[FINANCIAL_DOMAIN_CONFIG.md]({project_root}/ai_dev_flow/FINANCIAL_DOMAIN_CONFIG.md)** - Financial Services (DEFAULT)
9. **[SOFTWARE_DOMAIN_CONFIG.md]({project_root}/ai_dev_flow/SOFTWARE_DOMAIN_CONFIG.md)** - Software/SaaS
10. **[GENERIC_DOMAIN_CONFIG.md]({project_root}/ai_dev_flow/GENERIC_DOMAIN_CONFIG.md)** - Generic/Other

---

## Example Usage

### Example 1: Software Application Project

```
User: "Initialize new software application project"

AI Assistant (using project-init skill):

Step 1: Domain Selection
"What is the purpose and focus of this new project?"

User: "2" (Software/SaaS)

AI Assistant:
✓ Domain selected: Software/SaaS
✓ Loading configuration: SOFTWARE_DOMAIN_CONFIG.md
✓ Domain-specific subdirectories: tenant, subscription, billing, workspace

Step 2: Folder Creation
Creating 16-layer architecture (12 artifact directories)...
✓ Created: docs/BRD/
✓ Created: docs/PRD/
✓ Created: docs/EARS/
✓ Created: docs/BDD/
✓ Created: docs/ADR/
✓ Created: docs/SYS/
✓ Created: docs/REQ/
✓ Created: docs/IMPL/
✓ Created: docs/CTR/
✓ Created: docs/SPEC/
✓ Created: docs/TASKS/
✓ Created: docs/REQ/tenant/
✓ Created: docs/REQ/subscription/
✓ Created: docs/REQ/billing/
✓ Created: docs/REQ/workspace/
✓ Created: scripts/
✓ Created: work_plans/

Step 3: Domain Configuration
Applying Software/SaaS terminology:
✓ [RESOURCE_COLLECTION] → Workspace
✓ [RESOURCE_ITEM] → Resource
✓ [USER_ROLE] → Account Admin
✓ [REGULATORY_REQUIREMENT] → SOC2 Control

Step 5: Contract Decision
"Does this project require API contracts?"

User: "1,2" (REST APIs + Event Schemas)

AI Assistant:
✓ Contracts needed
✓ Contract types: REST API (OpenAPI), Event Schemas (AsyncAPI)
✓ Workflow: REQ → IMPL → CTR → SPEC → TASKS

Step 6: Index Files
✓ All 11 index files created

Step 7: Validation
✓ All directories verified
✓ All index files verified

═══════════════════════════════════════════════════════════
              PROJECT INITIALIZATION COMPLETE
═══════════════════════════════════════════════════════════

✓ Domain: Software/SaaS
✓ Folders: Created (11 artifact directories + 4 SaaS subdirectories)
✓ Contracts: Included (CTR layer active)
✓ Workflow: REQ → IMPL → CTR → SPEC → TASKS

Next: Use `doc-flow` skill to begin workflow execution
Start with: BRD-01 (Business Requirements Document)

═══════════════════════════════════════════════════════════
```

---

### Example 2: Software/SaaS Multi-Tenant Platform

```
User: "Set up new SaaS project for team collaboration platform"

AI Assistant (using project-init skill):

Step 1: Domain Selection
User: "2" (Software/SaaS)

AI Assistant:
✓ Domain selected: Software/SaaS
✓ Loading configuration: SOFTWARE_DOMAIN_CONFIG.md
✓ Domain-specific subdirectories: tenant, subscription, billing, workspace

Step 2: Folder Creation
✓ All core directories created
✓ SaaS subdirectories created: tenant/, subscription/, billing/, workspace/
✓ Support directories created: scripts/, work_plans/

Step 3: Domain Configuration
✓ [RESOURCE_COLLECTION] → Workspace
✓ [RESOURCE_ITEM] → Resource
✓ [USER_ROLE] → Account Admin
✓ [TRANSACTION] → API Call
✓ [REGULATORY_REQUIREMENT] → SOC2 Control

Step 5: Contract Decision
User: "1,2" (REST API + Event Schemas)

AI Assistant:
✓ Contracts included
✓ Workflow: REQ → IMPL → CTR → SPEC → TASKS

Project Ready!
Next: Use `doc-flow` skill for BRD-01 creation
```

---

## Troubleshooting

### Issue: Directory Already Exists

**Error**: `mkdir: cannot create directory 'docs': File exists`

**Resolution**:
- Project may already be initialized
- Verify: `ls -la docs/`
- If folders exist, skip to doc-flow skill
- If folders incomplete, delete and re-run project-init

### Issue: Permission Denied

**Error**: `mkdir: cannot create directory: Permission denied`

**Resolution**:
- Check current working directory permissions
- Ensure write access to parent directory
- Use `pwd` to verify location

### Issue: Domain Unclear

**User says**: "I'm not sure which domain to choose"

**AI Assistant Action**:
Run follow-up questions from DOMAIN_SELECTION_QUESTIONNAIRE.md:
1. Does project involve financial transactions? → Financial Services
2. Multi-tenant SaaS application? → Software/SaaS
3. Handle patient health information? → Healthcare
4. Online store or marketplace? → E-commerce
5. Connected devices or sensors? → IoT
6. None of above? → Generic

---

## Tool Optimization Notes

### Claude Code
- File limit: 50K tokens (200KB) standard, 100K max
- Strategy: Single comprehensive files
- No artificial splitting needed

### Gemini CLI
- @ reference limit: 10K tokens (40KB)
- Large files: Use file read tool instead of `@`
- Command: `gemini read FILE.md`

### GitHub Copilot
- Optimal: 10-30KB per file
- Large files: Create companion summaries
- Working set: Max 10 files in Edits mode

---

## Related Skills

**After project-init completes, use:**
- **doc-flow** - Main workflow execution skill
  - Create BRD, PRD, EARS, BDD, ADR, SYS, REQ, IMPL, CTR, SPEC, TASKS
  - Follow 15-layer architecture (Layers 0-14: Strategy layer + 11 artifact directories + 3 execution layers)
  - Generate code from specifications

**Other complementary skills:**
- **mermaid-gen** - Generate Mermaid diagrams
- **charts-flow** - Create architecture diagrams
- **test-automation** - Test suite creation
- **code-review** - Code quality review
- **security-audit** - Security analysis

---

## Quick Reference

**When to use project-init:**
- ✅ Brand new project (no folders exist)
- ✅ Greenfield development
- ✅ Starting from scratch

**When to use doc-flow:**
- ✅ Project already initialized
- ✅ Folders exist (docs/BRD/, docs/PRD/, etc.)
- ✅ Workflow execution (creating BRD, PRD, SPEC, etc.)

**Workflow sequence:**
```
project-init (Day 0) → doc-flow (Day 1+) → other skills (as needed)
```

---

**End of project-init Skill**
