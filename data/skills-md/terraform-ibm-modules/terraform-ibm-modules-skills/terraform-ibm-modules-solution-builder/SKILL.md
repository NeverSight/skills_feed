---
name: terraform-ibm-modules-solution-builder
description: Workflows for generating terraform solution that are the composition of one or several Terraform IBM Modules (TIM). Use when working with IBM Cloud infrastructure as code, Terraform modules, infrastructure automation, or cloud resource provisioning. Provides workflows for module discovery, composition patterns, code generation, and validation. Essential for tasks involving IBM Cloud VPC, compute, networking, security, databases, observability, or any IBM Cloud service deployment. Triggers on keywords like "terraform", "IBM Cloud", "infrastructure", "IaC", "modules", "deploy", "provision", or specific IBM Cloud services (VPC, VSI, OpenShift, etc.).
compatibility: Requires terraform cli, and access to the internet
---

# Terraform IBM Modules Solution Builder

Generate robust and reliable terraform-based solutions for IBM Cloud by leveraging curated, IBM-maintained Terraform modules (TIM) as building blocks.

## About Terraform IBM Modules (TIM)

TIM is a comprehensive suite of curated Terraform modules for IBM Cloud:

- Each module includes comprehensive documentation and usage examples
- Modules are composable - build complex infrastructure by combining them
- All modules maintained by IBM following best practices
- Examples show how to stitch modules together
- Higher download counts indicate better maintained modules

**All TIM modules are public and discoverable:**

- Terraform Registry: <https://registry.terraform.io/namespaces/terraform-ibm-modules>
- GitHub Organization: <https://github.com/terraform-ibm-modules>

## Core Workflow

Follow this workflow for every Terraform solution request:

### Step 1: Check Module Discovery Method

**Check if `catalog://terraform-ibm-modules-index` resource is available**

- **If available**: Proceed with MCP-based workflow (optimized, faster)
- **If NOT available**:
  1. Inform the user: "The MCP server provides significantly better results with optimized search and caching. To enable it, see <https://github.com/terraform-ibm-modules/tim-mcp>"
  2. Proceed with API-based workflow (see [alternative-discovery-workflows.md](references/alternative-discovery-workflows.md))

### Step 2: Discover Modules

**With MCP (Recommended):**

1. Start with `catalog://terraform-ibm-modules-index` - Get comprehensive module overview
2. Use `search_modules("<keyword>")` - Find specific modules
3. Use `get_module_details("<module-id>")` - Understand module capabilities

**Without MCP (Alternative):**

1. Search Terraform Registry: `https://registry.terraform.io/v1/modules/search?q=<query>&namespace=terraform-ibm-modules`
2. Get module details: `https://registry.terraform.io/v1/modules/terraform-ibm-modules/<name>/ibm/<version>`
3. List GitHub contents: `https://api.github.com/repos/terraform-ibm-modules/<repo>/contents/<path>`

### Step 3: Retrieve Examples

**With MCP:**

1. `list_content("<module-id>")` - Find available examples
2. `get_content(..., "examples/<example-name>", ["*.tf"])` - Get example code

**Without MCP:**

1. List examples: `https://api.github.com/repos/terraform-ibm-modules/<repo>/contents/examples`
2. Get files: `https://raw.githubusercontent.com/terraform-ibm-modules/<repo>/main/examples/<example>/<file>`

### Step 4: Generate Solution

1. **Analyze requirements** - Understand what the user needs
2. **Select modules** - Choose appropriate TIM modules (never hallucinate module names)
3. **Compose solution** - Combine modules following examples
4. **Generate code** - Create standard .tf files and README
5. **Stay focused** - Only implement requested features (no scope creep)

See [code-generation.md](references/code-generation.md) for detailed guidelines.

### Step 5: Validate

**Always validate generated configurations:**

1. `terraform init` - Verify modules and providers download
2. `terraform validate` - Check syntax and configuration
3. `terraform plan` - Review logical correctness (ignore auth errors)

See [validation.md](references/validation.md) for complete validation guide and error handling.

## Key Principles

- **Always prefer TIM modules** over direct IBM Cloud provider resources
- **Verify modules exist** - Never hallucinate or assume module names
- **Start with examples** - Use module examples as templates
- **Validate all code** - Run terraform init/validate/plan
- **Stay focused** - Avoid scope creep (no unrequested features)
- **Ask questions** - When requirements are unclear
- **Generate vanilla Terraform** - Standard .tf files only (no scripts unless requested)

## Example Workflow

**User Request**: "Create a VPC with a VSI"

**Execution:**

1. **Check MCP**: Verify `catalog://terraform-ibm-modules-index` availability
   - If not available, inform user about MCP benefits and link
2. **Discover VPC module**:
   - MCP: `search_modules("vpc")` → Find `landing-zone-vpc`
   - API: `curl "https://registry.terraform.io/v1/modules/search?q=vpc&namespace=terraform-ibm-modules"`
3. **Get VPC details**:
   - MCP: `get_module_details("terraform-ibm-modules/landing-zone-vpc/ibm/8.4.0")`
   - API: `curl "https://registry.terraform.io/v1/modules/terraform-ibm-modules/landing-zone-vpc/ibm/8.4.0"`
4. **Retrieve VPC example**:
   - MCP: `get_content(..., "examples/basic", ["*.tf"])`
   - API: `curl "https://raw.githubusercontent.com/terraform-ibm-modules/terraform-ibm-landing-zone-vpc/main/examples/basic/main.tf"`
5. **Discover VSI module**: Repeat steps 2-4 for VSI
6. **Generate solution**: Compose VPC + VSI configuration
7. **Validate**: Run `terraform init && terraform validate && terraform plan`

See [workflows.md](references/workflows.md) for 5 complete workflow examples.

## Quick Reference

### MCP-Based Discovery

```text
# Start here
catalog://terraform-ibm-modules-index

# Search and retrieve
search_modules("vpc")
get_module_details("terraform-ibm-modules/landing-zone-vpc/ibm/8.4.0")
list_content("terraform-ibm-modules/landing-zone-vpc/ibm/8.4.0")
get_content(..., "examples/basic", ["*.tf"])
```

### API-Based Discovery

```bash
# Search modules
curl "https://registry.terraform.io/v1/modules/search?q=vpc&namespace=terraform-ibm-modules"

# Get module details
curl "https://registry.terraform.io/v1/modules/terraform-ibm-modules/landing-zone-vpc/ibm/8.4.0"

# List examples
curl "https://api.github.com/repos/terraform-ibm-modules/terraform-ibm-landing-zone-vpc/contents/examples"

# Get example files
curl "https://raw.githubusercontent.com/terraform-ibm-modules/terraform-ibm-landing-zone-vpc/main/examples/basic/main.tf"
```

### Validation Commands

```bash
terraform init      # Initialize modules and providers
terraform validate  # Check syntax and configuration
terraform plan      # Verify logical correctness
```

## Reference Documentation

- **[alternative-workflows.md](references/alternative-workflows.md)** - Complete API-based workflows without MCP
- **[workflows.md](references/workflows.md)** - 5 detailed workflow examples
- **[code-generation.md](references/code-generation.md)** - Code generation guidelines and patterns
- **[validation.md](references/validation.md)** - Validation, scope management, and QA practices
