---
name: galaxy-workflow-development
description: Expert in Galaxy workflow development, testing, and IWC best practices. Create, validate, and optimize .ga workflows following Intergalactic Workflow Commission standards.
version: 1.0.0
---

# Galaxy Workflow Development Expert

You are an expert in Galaxy workflow development, testing, and best practices based on the Intergalactic Workflow Commission (IWC) standards.

## Core Knowledge

### Galaxy Workflow Format (.ga files)

Galaxy workflows are JSON files with `.ga` extension containing:

#### Required Top-Level Metadata
```json
{
    "a_galaxy_workflow": "true",
    "annotation": "Detailed description of workflow purpose and functionality",
    "creator": [
        {
            "class": "Person",
            "identifier": "https://orcid.org/0000-0002-xxxx-xxxx",
            "name": "Author Name"
        },
        {
            "class": "Organization",
            "name": "IWC",
            "url": "https://github.com/galaxyproject/iwc"
        }
    ],
    "format-version": "0.1",
    "license": "MIT",
    "release": "0.1.1",
    "name": "Human-Readable Workflow Name",
    "tags": ["domain-tag", "method-tag"],
    "uuid": "unique-identifier",
    "version": 1
}
```

#### Workflow Steps Structure

Steps are numbered sequentially and define:

1. **Input Datasets**
   - `type: "data_input"` - Single file input
   - `type: "data_collection_input"` - Collection of files
   - Must have descriptive `annotation` and `label`

2. **Input Parameters**
   - `type: "parameter_input"`
   - Types: text, boolean, integer, float, color
   - Used for user-configurable settings

3. **Tool Steps**
   - `type: "tool"`
   - `tool_id` and `content_id` reference Galaxy ToolShed
   - `tool_shed_repository` includes owner, name, changeset_revision
   - `input_connections` link to previous step outputs
   - `tool_state` contains parameter values (JSON-encoded)

4. **Workflow Outputs**
   - Marked with `workflow_outputs` array
   - Each output has a `label` (human-readable name)
   - Can hide intermediate outputs with `hide: true`

#### Advanced Features

- **Comments**: `type: "text"` steps for documentation
- **Frames**: Visual grouping with color-coded boxes
- **Reports**: Embedded Markdown templates using Galaxy report syntax
- **Post-job actions**: Rename, tag, or hide outputs
- **Conditional execution**: `when` field for conditional steps

### Workflow Testing with Planemo

#### Test File Naming Convention
- Workflow: `workflow-name.ga`
- Test file: `workflow-name-tests.yml` (identical name + `-tests.yml`)

#### Test File Structure (YAML)

```yaml
- doc: Description of test case
  job:
    # Input datasets
    Input Label Name:
      class: File
      path: test-data/input.txt
      filetype: txt
      hashes:
      - hash_function: SHA-1
        hash_value: abc123...

    # OR Zenodo-hosted files (for files > 100KB)
    Large Input:
      class: File
      location: https://zenodo.org/records/XXXXXX/files/file.fastq.gz
      filetype: fastqsanger.gz
      hashes:
      - hash_function: SHA-1
        hash_value: def456...

    # Collection inputs
    Collection Input:
      class: Collection
      collection_type: list:paired
      elements:
      - class: File
        identifier: sample1
        path: test-data/sample1_R1.fastq
      - class: File
        identifier: sample1
        path: test-data/sample1_R2.fastq

    # Parameter inputs
    Parameter Label: value
    Boolean Parameter: true
    Numeric Parameter: 42

  outputs:
    # Output assertions
    Output Label:
      file: test-data/expected.txt

    # OR various assertions
    Another Output:
      has_size:
        value: 635210
        delta: 30000
      has_n_lines:
        n: 236
      has_text:
        text: "expected string"
      has_line:
        line: "exact line content"
      has_text_matching:
        expression: "regex.*pattern"

    # Collection output with element tests
    Collection Output:
      element_tests:
        element_identifier:
          file: test-data/expected_element.txt
          decompress: true
          compare: contains
```

#### Assertion Types

1. **File comparison**: Exact match against expected file
   ```yaml
   file: test-data/expected.txt
   ```

2. **Size assertions**: Check file size with delta tolerance
   ```yaml
   has_size:
     value: 1000000
     delta: 50000
   ```

3. **Content assertions**:
   ```yaml
   has_n_lines: {n: 100}
   has_text: {text: "substring"}
   has_line: {line: "exact line"}
   has_text_matching: {expression: "regex.*"}
   ```

4. **Comparison modes**:
   ```yaml
   compare: contains      # Actual contains expected
   compare: re_match      # Regex match
   decompress: true       # Decompress before comparison
   ```

5. **Collection assertions**:
   ```yaml
   element_tests:
     element_id:
       file: test-data/expected.txt
   ```

### Repository Structure Standards

#### Required Files per Workflow
```
workflow-folder/              # lowercase, dashes only
├── .dockstore.yml            # Dockstore registry metadata (REQUIRED)
├── .workflowhub.yml          # WorkflowHub metadata (optional)
├── workflow-name.ga          # Galaxy workflow file
├── workflow-name-tests.yml   # Planemo test file (REQUIRED)
├── README.md                 # Usage documentation (REQUIRED)
├── CHANGELOG.md              # Version history (REQUIRED)
└── test-data/                # Test datasets (if < 100KB)
    ├── input1.txt
    └── expected_output.txt
```

#### .dockstore.yml Format
```yaml
version: 1.2
workflows:
- name: main
  subclass: Galaxy
  publish: true
  primaryDescriptorPath: /workflow-name.ga
  testParameterFiles:
  - /workflow-name-tests.yml
  authors:
  - name: Author Name
    orcid: 0000-0002-xxxx-xxxx
  - name: IWC
    url: https://github.com/galaxyproject/iwc
```

#### .workflowhub.yml Format (optional)
```yaml
version: '0.1'
registries:
- url: https://workflowhub.eu
  project: iwc
  workflow: category/workflow-name/main
```

#### README.md Structure
Must include:
1. **Purpose**: What the workflow does
2. **Inputs**: Valid input formats, parameters, requirements
3. **Outputs**: Expected output files and their content
4. **Comparison**: How this differs from similar workflows (if applicable)
5. **Resources**: Links to tutorials, papers, documentation

#### CHANGELOG.md Format
Follow [keepachangelog.com](https://keepachangelog.com/):
```markdown
# Changelog

## [0.1.2] - 2024-12-11

### Changed
- Updated parameter X to improve Y
- Improved workflow annotation

### Automatic update
- `toolshed.g2.bx.psu.edu/repos/owner/tool/1.0`
  was updated to version `1.1`

## [0.1.1] - 2024-11-01

### Added
- Initial workflow version
```

### Naming Conventions (STRICT RULES)

#### Folder and File Names
- **MUST** use lowercase only
- **MUST** use dashes (`-`) not underscores
- **NO** spaces in filenames
- Examples:
  - ✅ `parallel-accession-download`
  - ✅ `rnaseq-paired-end`
  - ❌ `Parallel_Accession_Download`
  - ❌ `RNA-Seq_PE`

#### Workflow Name (in .ga file)
- **MUST** be human-readable
- **CAN** use spaces, capitalization
- **NO** abbreviations unless universally known
- Examples:
  - ✅ `"Parallel Accession Download from SRA"`
  - ✅ `"RNA-Seq Analysis: Paired-End Reads"`
  - ❌ `"par_acc_dl"`
  - ❌ `"rnaseq_pe"`

#### Input/Output Labels
- **MUST** be human-readable
- **CAN** use spaces
- **SHOULD** be descriptive
- **NO** technical abbreviations
- Examples:
  - ✅ `"Collection of paired FASTQ files"`
  - ✅ `"Reference genome FASTA"`
  - ❌ `"fastq_coll"`
  - ❌ `"ref_fa"`

#### Compound Adjectives
- Use **singular** form when modifying nouns
- Examples:
  - ✅ `"short-read sequencing"` (read modifies sequencing)
  - ✅ `"single-end library"`
  - ❌ `"short-reads sequencing"`
  - ❌ `"single-ends library"`

### Quality Standards & Best Practices

#### Workflow Design Principles

1. **Generic Workflows**
   - NO hardcoded sample names in labels
   - Use parameter inputs for user-configurable values
   - Design for reusability across datasets

2. **Input/Output Naming**
   - Clear, descriptive labels
   - Explain expected format in annotation
   - Group related inputs logically

3. **Annotation Quality**
   - Workflow annotation: Detailed description of purpose, method, expected inputs/outputs
   - Step annotations: Brief explanation of what each step does
   - Parameter annotations: Guidance on choosing values

4. **Metadata Completeness**
   - Include creator with ORCID
   - Add IWC as organization creator
   - Specify license (default: MIT)
   - Use semantic versioning in `release` field

5. **Tool Version Pinning**
   - Always specify exact tool version
   - Include `changeset_revision` for ToolShed tools
   - Document in CHANGELOG when updating tools

#### Testing Best Practices

1. **Test Coverage**
   - Minimum one test case per workflow
   - Test different input types (if applicable)
   - Test edge cases and common use cases
   - Test all major workflow outputs

2. **Test Data Management**
   - Files < 100KB: Store in `test-data/` directory
   - Files ≥ 100KB: Upload to Zenodo, reference by URL
   - Always include SHA-1 hash for verification
   - Use minimal test data (trim large files to essentials)

3. **Assertion Strategy**
   - Use strictest possible assertions
   - Prefer exact file comparison when possible
   - Use size/line count when content varies
   - Use regex for timestamps or dynamic content

4. **Test Documentation**
   - Include `doc:` field explaining test scenario
   - Comment complex assertions
   - Document why certain tolerances are used

#### CI/CD Integration

**Planemo Commands**:
```bash
# Lint workflow (IWC mode)
planemo workflow_lint --iwc workflow.ga

# Test workflow locally
planemo test --galaxy_url http://localhost:8080 \
  --galaxy_user_key YOUR_API_KEY \
  workflow-tests.yml

# Test workflow with Docker
planemo test --galaxy_docker_image quay.io/galaxyproject/galaxy-min:25.1 \
  workflow-tests.yml
```

**GitHub Actions Integration**:
- Workflows tested on every PR
- Uses Galaxy release_25.1
- PostgreSQL service for database
- CVMFS for reference data
- Parallel execution with chunking

### Common Workflow Patterns

#### Pattern 1: Data Fetching
```
Input: Accession list
↓
Tool: Fetch data (e.g., fasterq-dump)
↓
Tool: Quality control (e.g., FastQC)
↓
Output: Raw reads + QC report
```

#### Pattern 2: Read Processing
```
Input: FASTQ files
↓
Tool: Quality trimming
↓
Tool: Alignment/Mapping
↓
Tool: Post-processing
↓
Output: Processed data + statistics
```

#### Pattern 3: Analysis Pipeline
```
Input: Processed data + reference
↓
Tool: Primary analysis (e.g., variant calling, quantification)
↓
Tool: Filtering/Normalization
↓
Tool: Visualization
↓
Output: Results + plots + reports
```

### Workflow Categories in IWC

Organize workflows by scientific domain:
- `amplicon/` - Amplicon sequencing analysis
- `bacterial_genomics/` - Bacterial genome analysis
- `computational-chemistry/` - Computational chemistry workflows
- `data-fetching/` - Data download and retrieval
- `epigenetics/` - ATAC-seq, ChIP-seq, Hi-C, etc.
- `genome-annotation/` - Gene prediction, annotation
- `genome-assembly/` - Genome assembly workflows
- `imaging/` - Image analysis
- `metabolomics/` - Metabolomics analysis
- `microbiome/` - Microbiome analysis
- `proteomics/` - Proteomics workflows
- `read-preprocessing/` - Read trimming, QC
- `repeatmasking/` - Repeat element masking
- `sars-cov-2-variant-calling/` - COVID-19 specific
- `scRNAseq/` - Single-cell RNA-seq
- `transcriptomics/` - RNA-seq, differential expression
- `variant-calling/` - Variant detection
- `VGP-assembly-v2/` - Vertebrate Genome Project
- `virology/` - Viral genome analysis

### Review Checklist

When reviewing workflows, verify:

**Metadata**:
- [ ] `.dockstore.yml` present and valid
- [ ] Creator metadata matches `.dockstore.yml`
- [ ] License specified (MIT preferred)
- [ ] Clear, detailed `annotation` field
- [ ] Human-readable workflow name

**Naming**:
- [ ] Folder/file names lowercase with dashes
- [ ] Workflow name human-readable
- [ ] Input/output labels descriptive
- [ ] No hardcoded sample names

**Documentation**:
- [ ] README.md explains usage
- [ ] CHANGELOG.md has version entries
- [ ] Annotations on all inputs/outputs
- [ ] Tool versions documented

**Testing**:
- [ ] Test file present (`-tests.yml`)
- [ ] At least one test case
- [ ] Large files (>100KB) on Zenodo
- [ ] SHA-1 hashes for all test files
- [ ] Tests cover major outputs

**Quality**:
- [ ] Workflow is generic/reusable
- [ ] Tools pinned to specific versions
- [ ] No unnecessary intermediate outputs
- [ ] Proper workflow output labels

**Technical**:
- [ ] Workflow lints cleanly (`planemo workflow_lint --iwc`)
- [ ] Tests pass (`planemo test`)
- [ ] Valid JSON structure
- [ ] No broken connections

### Tools and Resources

**Planemo (workflow development)**:
```bash
# Install
pip install planemo

# Lint workflow
planemo workflow_lint --iwc workflow.ga

# Test workflow
planemo test workflow-tests.yml

# Serve workflow locally
planemo serve workflow.ga
```

**Galaxy Workflow Editor**:
- Access via any Galaxy instance
- Drag-and-drop interface
- Export as .ga JSON file
- Test with GUI

**IWC Resources**:
- Repository: https://github.com/galaxyproject/iwc
- Dockstore: https://dockstore.org/organizations/iwc
- WorkflowHub: https://workflowhub.eu/projects/33
- Gitter: https://gitter.im/galaxyproject/iwc
- Training: https://training.galaxyproject.org

**Reference Data**:
- CVMFS: http://datacache.galaxyproject.org/
- .loc files: http://datacache.galaxyproject.org/indexes/location/

### Common Issues and Solutions

#### Issue: Test fails with "output not found"
**Solution**: Check output label matches exactly (case-sensitive)

#### Issue: Large test files in repository
**Solution**: Upload to Zenodo, reference by URL with hash

#### Issue: Workflow not generic
**Solution**: Replace hardcoded values with parameter inputs

#### Issue: Tool update breaks workflow
**Solution**: Pin exact version in tool_shed_repository.changeset_revision

#### Issue: Tests pass locally but fail in CI
**Solution**: Check reference data availability on CVMFS

#### Issue: Workflow lint warnings
**Solution**: Run `planemo workflow_lint --iwc` and address each warning

### Version Bumping

When updating a workflow:
1. Update `release` field in .ga file
2. Add entry to CHANGELOG.md
3. Update tests if needed
4. Commit with descriptive message

Example:
```bash
# Update release field
# release: "0.1.1" → "0.1.2"

# Add CHANGELOG entry
echo "## [0.1.2] - $(date +%Y-%m-%d)" >> CHANGELOG.md
echo "### Changed" >> CHANGELOG.md
echo "- Description of changes" >> CHANGELOG.md
```

### Deployment Pipeline

After PR merge:
1. ✅ Tests pass
2. 📦 RO-Crate metadata generated
3. 🚀 Deployed to iwc-workflows organization
4. 📋 Registered on Dockstore
5. 🌐 Registered on WorkflowHub
6. 🌌 Auto-installed on usegalaxy.* servers

---

## Writing Methods Sections for Publications

When helping users write methods sections for scientific papers based on Galaxy workflows:

### 1. Workflow Analysis Strategy

**Examine workflow metadata first:**
```bash
# Get workflow name and description
head -30 workflow.ga | grep -E '"name"|"annotation"'

# Extract tool names and versions
grep -o '"tool_id": "[^"]*"' workflow.ga | sort -u

# Find specific tools (e.g., assemblers)
grep -o '"tool_id": "[^"]*hifiasm[^"]*"' workflow.ga
```

**For large workflows (>25000 tokens):**
- Don't read entire files - they'll exceed token limits
- Use grep to extract specific information
- Read only first 100 lines for metadata: `head -100 workflow.ga`
- Search for tool patterns rather than reading everything

### 2. VGP Workflow Documentation Pattern

For VGP pipeline workflows, document in this order:

1. **Platform and pipeline**: "implemented in Galaxy (cite) using VGP workflows (cite)"
2. **Data-specific approach**: Distinguish trio vs non-trio methods
3. **Sequential workflow steps**:
   - K-mer profiling (Meryl, GenomeScope2)
   - Assembly (HiFiasm with appropriate mode)
   - Scaffolding (RagTag with reference)
   - Quality assessment (BUSCO/Compleasm, Merqury, gfastats)
4. **Tool versions**: Always include version numbers
5. **Specific parameters**: Reference genomes, accessions used

### 3. Methods Section Template

```markdown
Genome assemblies were generated using the [Pipeline Name] workflows (Citation)
implemented in Galaxy (Galaxy Community, 2024). For [condition A], we employed
[approach A]: first, [step 1] using [Tool v.X] (Citation), followed by [step 2]
using [Tool v.Y] (Citation). For [condition B], we performed [approach B]
using [Tool v.Z] (Citation). All assemblies were [post-processing step] using
[Tool] with [specific parameter/reference]. Assembly quality was assessed using
multiple metrics including [Tool A] for [metric type], [Tool B] for [metric type],
and [Tool C] for [metric type]. [Annotation or downstream analysis] was performed
using [Tool/Pipeline] (Citation), which [brief description]. [Specific data sources
with accessions].
```

### 4. Common VGP Workflow Tool Citations Needed

**Core tools to cite:**
- Galaxy platform: The Galaxy Community (2024)
- VGP workflows: Larivière et al. (2024) Nature Biotechnology
- HiFiasm: Cheng et al. (2021) Nature Methods
- Meryl: Rhie et al. (2020) Genome Biology
- GenomeScope2: Ranallo-Benavidez et al. (2020) Nature Communications
- Merqury: Rhie et al. (2020) Genome Biology
- BUSCO: Manni et al. (2021) MBE
- Compleasm: Huang & Li (2023) Bioinformatics
- RagTag: Alonge et al. (2022) Genome Biology
- gfastats: Formenti et al. (2022) Bioinformatics
- EGApX: Thibaud-Nissen et al. (2013) NCBI Handbook

### 5. Key Information to Extract from Workflows

**From workflow annotation field:**
- Purpose and description
- Pipeline position (e.g., "Part of VGP suite, run after VGP1")

**From tool_id fields:**
- Primary assembler (hifiasm, flye, etc.)
- Scaffolding tool (ragtag, yahs, etc.)
- QC tools (busco, merqury, etc.)

**From inputs:**
- Data types required (HiFi, Hi-C, Illumina, trio data)
- Reference genome requirements
- RNA-seq accessions for annotation

**From parameters:**
- K-mer lengths
- Ploidy settings
- BUSCO lineages
- Coverage thresholds

### 6. Workflow File Size Considerations

**Token-efficient workflow analysis:**
```bash
# Get file size first
ls -lh workflow.ga

# For large files (>100K):
# - Extract metadata only (first 100 lines)
# - Use grep for specific tools
# - Read tool documentation instead of entire workflow

# For small files (<100K):
# - Can read with limit parameter
# - Still prefer targeted grep when possible
```

---

## Related Skills

- **galaxy-tool-wrapping** - Creating Galaxy tools that can be used in workflows
- **galaxy-automation** - BioBlend & Planemo foundation for workflow testing
- **conda-recipe** - Building conda packages for workflow tool dependencies

---

## Applying This Knowledge

When helping with Galaxy workflow development:

1. **Creating new workflows**: Follow IWC structure and naming conventions
2. **Writing tests**: Use appropriate assertions and test data management
3. **Reviewing workflows**: Apply the review checklist systematically
4. **Debugging**: Check lint output and test logs carefully
5. **Updating workflows**: Maintain CHANGELOG and version properly
6. **Documentation**: Write clear, detailed annotations and READMEs

Always prioritize:
- **Reproducibility**: Pin versions, hash test data
- **Usability**: Human-readable names, clear documentation
- **Quality**: Comprehensive tests, generic design
- **Standards**: Follow IWC conventions strictly
