---
name: drawio-diagram-forge
description: Generate draw.io editable diagrams (.drawio, .drawio.svg) from text, images, or Excel. Orchestrates 3-agent workflow (Analysis → Manifest → SVG generation) with quality gates. Use when creating architecture diagrams, flowcharts, sequence diagrams, or converting existing images to editable format. Supports Azure/AWS cloud icons.
license: CC BY-NC-SA 4.0
metadata:
  author: yamapan (https://github.com/aktsmm)
---

# Draw.io Diagram Forge

Generate **draw.io editable diagrams** using AI-powered orchestrated workflow.

## When to Use

- **General diagram requests** - "Create a diagram", "Draw me a chart", etc.
- Creating architecture diagrams (Azure, AWS, on-premises)
- Converting flowcharts, system diagrams from text descriptions
- Transforming existing images/screenshots into editable draw.io format
- Generating swimlane diagrams, sequence diagrams from Excel/Markdown

## Prerequisites

| Tool                    | Purpose            | Required |
| ----------------------- | ------------------ | -------- |
| **VS Code**             | IDE                | ✅       |
| **Draw.io Integration** | Edit .drawio files | ✅       |
| **GitHub Copilot**      | AI generation      | ✅       |

**Install extension**: [Draw.io Integration](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio)

## Quick Start

### Basic Usage

```
Create a login flow diagram
```

```
Generate an Azure architecture diagram with Hub-Spoke topology
```

```
Convert this Excel file to a flowchart
```

### With Input Files

```
From inputs/requirements.md, create a system architecture diagram
```

```
Recreate this image (inputs/architecture.png) as an editable draw.io file
```

## Output Formats

| Extension      | Description            | When to Use                      |
| -------------- | ---------------------- | -------------------------------- |
| `*.drawio`     | Native draw.io format  | ⭐ **Recommended** - Most stable |
| `*.drawio.svg` | SVG + draw.io metadata | Embedding in Markdown/Web        |
| `*.drawio.png` | PNG + draw.io metadata | Image with edit capability       |

**Output directory**: `outputs/`

## Workflow Overview

```
USER INPUT
    │
    ▼
┌─────────────────────────────────────────────────┐
│           FLOW ORCHESTRATOR                      │
│  ┌─────────────────────────────────────────┐    │
│  │ Internal Modules:                        │    │
│  │ • Analysis (input classification)        │    │
│  │ • Review (quality scoring)               │    │
│  │ • State (context management)             │    │
│  │ • Timeout (watchdog)                     │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
    │
    ├──► MANIFEST GATEWAY (create manifest)
    │
    └──► SVG FORGE (generate diagram + validation)
    │
    ▼
COMPLETED (.drawio file)
```

### Quality Gates

| Score  | Action      | Description                |
| ------ | ----------- | -------------------------- |
| 90-100 | ✅ Proceed  | High quality, continue     |
| 85-89  | ⚠️ Note     | Minor issues noted         |
| 70-84  | 🔄 Fix      | Auto-fix and retry         |
| 50-69  | 📉 Simplify | Reduce complexity          |
| 30-49  | 📦 Partial  | Deliver partial result     |
| 0-29   | ❌ Escalate | Ask user for clarification |

### Iteration Limits

| Limit             | Value | On Exceed                  |
| ----------------- | ----- | -------------------------- |
| Manifest revision | 2     | Force proceed with warning |
| SVG revision      | 2     | Partial success            |
| Total revisions   | 4     | Partial success            |
| Total timeout     | 45min | Checkpoint-based decision  |

## Advanced: Agent Delegation

For complex diagrams, explicitly invoke the orchestrator:

```
@flow-orchestrator Create a detailed microservices architecture from inputs/requirements.md
```

This triggers the full manifest → review → generation → review cycle.

## Cloud Icon Usage

When generating cloud architecture diagrams, follow this **icon selection logic**:

### Step 1: Detect Cloud Provider

Scan input for provider-specific keywords:

| Provider | Keywords                                                                          |
| -------- | --------------------------------------------------------------------------------- |
| Azure    | `Azure`, `Microsoft Cloud`, `App Service`, `Azure AD`, `VNET`, `AKS`, `Key Vault` |
| AWS      | `AWS`, `Amazon`, `EC2`, `Lambda`, `S3`, `RDS`, `VPC`, `EKS`, `DynamoDB`           |
| GCP      | `GCP`, `Google Cloud`, `Cloud Run`, `BigQuery`, `GKE`, `Cloud Functions`          |
| Alibaba  | `Alibaba Cloud`, `Aliyun`, `ECS` (Alibaba context), `OSS`, `MaxCompute`           |
| IBM      | `IBM Cloud`, `IBM Watson`, `IBM OpenShift`                                        |
| Cisco    | `Cisco`, `Meraki`, `ACI`, `Nexus`, `ISE`                                          |

### Step 2: Search for Matching Icon

For each cloud service mentioned:

1. **Search** the appropriate icon library for a matching icon
2. **If found**: Use the provider-specific format (see below)
3. **If not found**: Use a generic shape with the service name as label

### Step 3: Apply Provider-Specific Format

| Provider    | Icon Format                                                   | Library Path                                                                       |
| ----------- | ------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| **Azure**   | `image=img/lib/azure2/{category}/{Icon}.svg`                  | [azure2](https://github.com/jgraph/drawio/tree/dev/src/main/webapp/img/lib/azure2) |
| **AWS**     | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{icon}` | mxgraph.aws4.\*                                                                    |
| **GCP**     | `shape=mxgraph.gcp2.{icon}`                                   | mxgraph.gcp2.\*                                                                    |
| **Alibaba** | `shape=mxgraph.alibabacloud.{icon}`                           | mxgraph.alibabacloud.\*                                                            |
| **IBM**     | `image=img/lib/ibm/{category}/{icon}.svg`                     | [ibm](https://github.com/jgraph/drawio/tree/dev/src/main/webapp/img/lib/ibm)       |
| **Cisco**   | `shape=mxgraph.cisco19.{icon}`                                | mxgraph.cisco19.\*                                                                 |

### Step 4: Fallback for Unknown Services

If no matching icon exists:

```xml
<!-- Generic rectangle with service name -->
<mxCell value="Custom Service" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" />
```

### ⚠️ Critical: Azure Format

```xml
<!-- ❌ WRONG - Will show blue square in VS Code -->
<mxCell style="shape=mxgraph.azure.front_door;..." />

<!-- ✅ CORRECT - Works everywhere -->
<mxCell style="aspect=fixed;image=img/lib/azure2/networking/Front_Doors.svg;..." />
```

**Refer to** [cloud-icons.md](references/cloud-icons.md) for detailed SVG paths and style examples.

## Resources

### References

| File                                                  | Description                      |
| ----------------------------------------------------- | -------------------------------- |
| [mxcell-structure.md](references/mxcell-structure.md) | mxCell XML structure for draw.io |
| [cloud-icons.md](references/cloud-icons.md)           | Azure/AWS icon usage guide       |
| [style-guide.md](references/style-guide.md)           | Node colors, edge styles         |

### Scripts

| File                                             | Description               |
| ------------------------------------------------ | ------------------------- |
| [validate_drawio.py](scripts/validate_drawio.py) | Validate mxCell structure |

## Cloud Icons (Azure/AWS)

To enable cloud icons in generated diagrams:

1. Open generated `.drawio` file in VS Code
2. Click **"+ More Shapes"** (bottom-left)
3. Enable: ✅ **Azure**, ✅ **AWS**
4. Click **Apply**

## Troubleshooting

| Issue             | Cause                 | Solution                  |
| ----------------- | --------------------- | ------------------------- |
| Blank in draw.io  | Missing mxCell        | Check `content` attribute |
| Edges not visible | Invalid source/target | Verify node IDs           |
| Icons missing     | Library not enabled   | Enable Azure/AWS shapes   |

## Technical Details

### How It Works

AI generates **XML/SVG text** that renders as editable diagrams:

```
Natural Language  →  XML/mxGraphModel  →  Rendered Diagram
     ↑                    ↑                      ↑
  Human input        AI generates          SVG rendering
```

### mxCell Completeness Rule

```
Required mxCells >= 2 + nodes + edges
```

- `mxCell id="0"` (root)
- `mxCell id="1"` (default parent)
- One mxCell per node (`vertex="1"`)
- One mxCell per edge (`edge="1"`)
