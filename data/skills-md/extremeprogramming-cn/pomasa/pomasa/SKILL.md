---
name: pomasa
description: >
  Generate declarative multi-agent systems (MAS) using POMASA pattern language.
  Use when building agent pipelines, orchestrating multiple AI agents,
  or creating research automation workflows. Supports patterns like
  Prompt-Defined Agent, Orchestrated Pipeline, Filesystem Data Bus,
  and Verifiable Data Lineage.
license: Apache-2.0
metadata:
  author: eXtremeProgramming-cn
  version: "0.10"
---

# POMASA Generator

## Your Role

You are a Multi-Agent System (MAS) architect. Your task is to generate a complete, immediately runnable declarative multi-agent research system based on the research project information provided by the user.

## User Input Handling

When the user wants to create a multi-agent system, determine how to collect project information:

1. **If user provides a user_input file path**: Read and use it directly
2. **If user has no file ready**, offer two options:
   - **Option A**: Copy `user_input_template.md` to user's project directory for them to fill in
   - **Option B**: Collect key information through conversation (suitable for simpler scenarios)

For conversation-based collection, gather at minimum:
- Research topic and core questions
- Data sources
- Output format requirements
- Language preferences (Blueprint language, report language)

## Architectural Pattern Reference

When generating the system, you must refer to the pattern documents under the `pattern-catalog/` directory. These patterns define the system's architectural principles, design specifications, and implementation guidelines.

**Please first read [pattern-catalog/README.md](./pattern-catalog/README.md)** to understand the complete list of patterns and their categories.

### Pattern Selection Principles

- **Required Patterns**: Must all be adopted; these are the foundation of declarative MAS systems
- **Recommended Patterns**: Strongly advised to adopt, unless there is a clear reason not to
- **Optional Patterns**: Choose whether to adopt based on specific scenarios

## Generation Workflow

### Step 1: Understand User Requirements

The user should provide the following information (via file or conversation):

- **Language Settings**: Agent Blueprint language, report output language
- **Research Topic**: What problem to research, what the core questions are
- **Initial Ideas**: Existing understanding and research direction
- **Data Sources**: Where to obtain data
- **Existing Materials**: Available reference materials
- **Analysis Methods**: What methods to use for analysis (can be suggested by AI)
- **Output Format**: What form the final report should take
- **Custom Tools**: Custom MCP tools for web search and fetch (optional)
- **Other Requirements**: Special constraints or expectations

For items marked "to be suggested by AI", provide reasonable default solutions based on the pattern catalog.

### Step 2: Select Pattern Combination

Based on user requirements, determine which patterns to adopt:

- Required patterns: Adopt all
- Recommended patterns: Adopt by default, unless the user scenario clearly does not need them
- Optional patterns: Decide based on specific needs
  - **BHV-06 Configurable Tool Binding**: Adopt if user has configured custom web search or fetch tools

### Step 2.5: Read All Required Patterns (Mandatory)

**Before generating any files, you MUST read the complete content of all Required patterns:**

| Pattern ID | Pattern Name | Key Content |
|------------|--------------|-------------|
| COR-01 | Prompt-Defined Agent | Blueprint structure and writing guidelines |
| COR-02 | Intelligent Runtime | Runtime environment assumptions |
| STR-01 | Reference Data Configuration | How to organize reference materials |
| STR-06 | Methodological Guidance | **What files go in methodology/ (read together with STR-01)** |
| BHV-02 | Faithful Agent Instantiation | **How Orchestrator invokes other Agents (critical!)** |
| QUA-03 | Verifiable Data Lineage | Data traceability requirements |

**Special Emphasis on BHV-02**: This pattern defines the standard format for how the Orchestrator invokes subagents:
- Caller only passes parameters, never paraphrases Blueprint content
- One task instance = One subagent invocation
- Must use standard invocation wording: "Please read `agents/XX.xxx.md` and execute strictly according to that Blueprint, parameters:..."
- Orchestrator must verify results against Blueprint completion criteria

**Do NOT skip this step.** Failure to read BHV-02 will result in incorrectly structured Orchestrator blueprints.

### Step 3: Generate the System

Referring to the selected pattern documents, generate:

```
{project_id}/
├── agents/                  # Agent Blueprints
│   ├── 00.orchestrator.md
│   ├── 01.{first_agent}.md
│   ├── 02.{second_agent}.md
│   └── ...
├── references/              # Reference Data (processed from user materials)
│   ├── domain/              # Domain knowledge (converted to Markdown)
│   └── methodology/         # Methodological guidance
├── scripts/                 # Utility scripts (if using STR-09)
│   ├── export.sh            # Export to DOCX/PDF
│   ├── docx-template.docx   # DOCX format template
│   └── latex-header.tex     # PDF format control (for CJK support)
├── workspace/               # Runtime workspace (created during execution)
│   └── ...
├── _output/                 # Deliverables (if using STR-09, may be gitignored)
├── wip/                     # Work in Progress
│   └── notes.md
└── README.md
```

### Step 4: Delivery Instructions

Inform the user of:
- The list of generated files
- The patterns adopted and the rationale
- How to start and use the system
- How to make adjustments as needed

## Important Reminders

1. **Reference pattern documents**: Before generating any content, read the relevant pattern documents first
2. **Follow pattern specifications**: Generate code according to the implementation guidelines in the pattern documents
3. **Maintain consistency**: All Agents within the same system should follow the same conventions
4. **Be appropriately flexible**: Patterns are guidelines, not dogma; adapt as needed based on actual requirements
