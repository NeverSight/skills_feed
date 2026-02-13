---
name: managing-environments
description: Best practices for managing development environments including Python venv and conda. Always check environment status before installations and confirm with user before proceeding.
version: 1.1.0
---

# Managing Development Environments

Guidelines for working with Python virtual environments (venv) and conda environments. This skill ensures safe, organized package installations by always checking and confirming the active environment before proceeding.

## When to Use This Skill

Activate this skill whenever:
- Installing Python packages or tools
- User requests to install dependencies
- Setting up a new Python project
- Debugging import or package issues
- Working with any Python development

## Core Principles

1. **Always check environment status** before any installation
2. **Always confirm with user** which environment to use
3. **Never install without environment confirmation**
4. **Warn if no environment is active**
5. **Help user choose appropriate environment type**

---

## Environment Detection Workflow

### Step 1: Check Environment Status

**Before ANY installation command**, run these checks:

```bash
# Check for active venv
echo "Python executable: $(which python)"
echo "Virtual environment: $VIRTUAL_ENV"

# Check for conda environment
echo "Conda environment: $CONDA_DEFAULT_ENV"
conda info --envs 2>/dev/null || echo "Conda not available"
```

### Step 2: Interpret Results

**Scenario A: venv is active**
```
Python executable: /path/to/project/.venv/bin/python
Virtual environment: /path/to/project/.venv
Conda environment:
```
→ Python venv is active

**Scenario B: conda environment is active**
```
Python executable: /path/to/miniconda3/envs/myenv/bin/python
Virtual environment:
Conda environment: myenv
```
→ Conda environment is active

**Scenario C: No environment (system Python)**
```
Python executable: /usr/bin/python
Virtual environment:
Conda environment:
```
→ ⚠️ No environment active! Warn user.

**Scenario D: Both detected (rare)**
```
Virtual environment: /path/to/.venv
Conda environment: base
```
→ Both active, prioritize what `which python` shows, but confirm with user

### Step 3: Confirm with User

**Always ask before proceeding:**

```
I've detected the following environment:
- Environment type: [venv/conda/none]
- Location: [path]
- Python version: [version]

Is this the environment you want me to use for installing [package/tool]?
```

**Wait for user confirmation before proceeding.**

---

## Installation Patterns by Environment Type

### For Python venv

```bash
# Activate (if needed)
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows

# Install packages
pip install package-name

# Install with specific version
pip install package-name==1.2.3

# Install from requirements
pip install -r requirements.txt

# Install development dependencies
pip install -e ".[dev]"
```

### For Conda Environment

```bash
# Activate (if needed)
conda activate environment-name

# Install from conda-forge (preferred for scientific packages)
conda install -c conda-forge package-name

# Install with pip (if not available in conda)
pip install package-name

# Install from environment file
conda env update -f environment.yml

# Install specific version
conda install package-name=1.2.3
```

### Critical: Channel Priority for Conda

For bioinformatics/scientific packages:
1. Try `conda-forge` first: `conda install -c conda-forge package`
2. Try `bioconda` for bio tools: `conda install -c bioconda package`
3. Fall back to pip only if not available: `pip install package`

**Why:** Conda manages binary dependencies better than pip for scientific packages.

### Handling Conda TOS Acceptance Errors

If conda installation fails with:
```
CondaToSNonInteractiveError: Terms of Service have not been accepted
```

**Solution**: Use pip instead (installed packages work identically):
```bash
/path/to/envs/ENV_NAME/bin/pip install PACKAGE_NAME
```

**Example** - Installing JupyterLab:
```bash
# This fails with TOS error
conda install -n curation_paper -c conda-forge jupyterlab -y

# Use pip instead
/Users/delphine/miniconda3/envs/curation_paper/bin/pip install jupyterlab
```

Packages installed via pip integrate seamlessly with conda environments.

---

## No Environment Active - Warning & Planning

If no environment is detected, **DO NOT PROCEED with installation**. Instead:

### Step 1: Warn User

```
⚠️ WARNING: No Python environment detected!

You're currently using system Python:
- Location: [path to python]
- Version: [version]

Installing packages to system Python can:
- Cause conflicts with system packages
- Require sudo/admin privileges
- Make projects difficult to reproduce
- Break system tools that depend on specific versions

I recommend creating a virtual environment first.
```

### Step 2: Help Choose Environment Type

Ask user about their project needs:

**Decision Tree:**

```
Question: What type of project are you working on?

A. Pure Python project (web dev, scripting, etc.)
   → Recommend: Python venv
   → Fast, lightweight, standard Python tool

B. Data science / Scientific computing
   → Ask: Do you need non-Python dependencies? (R, C libraries, etc.)

   B1. Yes (or using packages like numpy, scipy, pandas, etc.)
       → Recommend: Conda
       → Better binary dependency management

   B2. No, only Python packages
       → Recommend: Python venv
       → Simpler and faster

C. Bioinformatics / Genomics
   → Recommend: Conda (with bioconda channel)
   → Most tools available via bioconda
   → Manages complex dependencies well

D. Galaxy tool development
   → Recommend: Conda
   → Galaxy uses conda for tool dependencies
   → Direct compatibility
```

### Step 3: Offer to Create Environment

**For venv:**
```bash
# Create venv
python -m venv .venv

# Activate
source .venv/bin/activate  # Linux/Mac

# Verify
which python
```

**For conda:**
```bash
# Create conda environment
conda create -n project-name python=3.11

# Activate
conda activate project-name

# Verify
conda info --envs
which python
```

---

## Common Scenarios

### Scenario 1: User Asks to Install Package

**❌ Bad (without checking):**
```
pip install pandas
```

**✅ Good (with environment check):**
```
1. Check environment status
2. Show user what environment is active
3. Ask: "Is this the environment you want to use?"
4. Wait for confirmation
5. Then: pip install pandas (or conda install as appropriate)
```

### Scenario 2: Multiple Packages Needed

**User:** "Install pandas, numpy, and matplotlib"

**Response:**
```
Let me first check your environment...

[run environment detection]

I've detected: [environment details]

I need to install:
- pandas
- numpy
- matplotlib

Is this the correct environment? Should I use [pip/conda install -c conda-forge]?
```

### Scenario 3: User in Wrong Environment

**User:** "Install scikit-learn" (but they're in a different project's venv)

**Response:**
```
⚠️ I've detected you're in a virtual environment at:
/path/to/other-project/.venv

But we're working in directory:
/path/to/current-project

This might be the wrong environment. Options:
1. Deactivate and create/activate the correct environment for this project
2. Continue with current environment (if this is intentional)
3. Cancel installation

Which would you prefer?
```

### Scenario 4: Conda Base Environment

**Detection:** User is in conda base environment

**Response:**
```
⚠️ You're currently in the conda 'base' environment.

It's generally better practice to create a separate environment for each project
to avoid dependency conflicts.

Options:
1. Create a new conda environment for this project
2. Continue with base environment (not recommended)

Would you like me to create a project-specific environment?
```

---

## Environment Selection Guidelines

### Use Python venv When:
- ✅ Pure Python project
- ✅ Simple dependencies (all available on PyPI)
- ✅ Standard web development (Django, Flask, FastAPI)
- ✅ No compiled extensions or C libraries
- ✅ Want fastest environment creation
- ✅ Working with Python 3.3+

**Advantages:**
- Lightweight and fast
- Built into Python (no extra installation)
- Simple and standard
- Works on all platforms

**Disadvantages:**
- Harder to manage non-Python dependencies
- Binary packages may need system libraries
- Version conflicts harder to resolve

### Use Conda Environment When:
- ✅ Data science / machine learning
- ✅ Scientific computing (numpy, scipy, pandas)
- ✅ Bioinformatics / genomics
- ✅ Need specific Python versions
- ✅ Cross-language dependencies (R, C++, etc.)
- ✅ Galaxy tool development
- ✅ Complex binary dependencies

**Advantages:**
- Manages binary dependencies
- Cross-language support
- Better for scientific packages
- Can manage Python version
- Excellent for reproducibility

**Disadvantages:**
- Slower than venv
- Larger disk space usage
- Requires conda installation
- More complex

---

## Best Practices

### 1. One Environment Per Project

**Good:**
```
project-a/
├── .venv/          # project-a's environment
├── requirements.txt
└── src/

project-b/
├── .venv/          # project-b's environment
├── requirements.txt
└── src/
```

**Bad:**
```
# Using same environment for multiple projects
# → Version conflicts inevitable
```

### 2. Document Environment Setup

Always create environment specification files:

**For venv:**
```bash
# Create requirements.txt
pip freeze > requirements.txt

# Or for development
pip freeze > requirements-dev.txt
```

**For conda:**
```bash
# Create environment.yml
conda env export > environment.yml

# Or minimal version
conda env export --from-history > environment.yml
```

### 3. Add Environment to .gitignore

```gitignore
# Python venv
.venv/
venv/
env/

# Conda
.conda/
```

### 4. Include Python Version

**For venv (in README):**
```
Python 3.11+ required
```

**For conda (in environment.yml):**
```yaml
name: myproject
dependencies:
  - python=3.11
  - pandas
  - numpy
```

---

## Resumable Data Fetch Scripts

### Pattern for Long-Running Data Retrieval

When building scripts that fetch data from external sources (APIs, S3, etc.), implement these patterns for robustness:

```python
def fetch_with_caching(item_id, output_dir):
    """Fetch data with local caching to support resume."""
    output_file = output_dir / f"{item_id}_data.txt"

    # Skip if already downloaded
    if output_file.exists():
        with open(output_file, 'r') as f:
            content = f.read()
        return True, "cached", content

    # Fetch logic here...
    # Save to file on success

    return success, status, content

def main():
    # Load existing results to skip completed work
    existing_csv = base_dir / 'results.csv'
    if existing_csv.exists():
        df_existing = pd.read_csv(existing_csv)
        existing_ids = set(df_existing['id'].tolist())
        df_to_process = df_to_process[~df_to_process['id'].isin(existing_ids)]
        print(f"Skipping {len(existing_ids)} items with existing data")

    # Process remaining items
    for item in df_to_process:
        success, status, data = fetch_with_caching(item, output_dir)
        # Process and accumulate results...

    # Merge with existing results
    if existing_csv.exists():
        df_existing = pd.read_csv(existing_csv)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new

    # Save combined results
    df_combined.to_csv(output_csv, index=False)
```

### Key Features

1. **File-level caching**: Save each fetch result immediately
2. **Resume capability**: Skip already-processed items automatically
3. **Incremental results**: Merge new results with existing data
4. **Interruption-safe**: Can be stopped and restarted without data loss

### Progress Tracking

```python
try:
    from tqdm import tqdm
    iterator = tqdm(items, total=len(items), desc="Processing")
except ImportError:
    print("(Install tqdm for progress bar: pip install tqdm)")
    iterator = items
```

### Rate Limiting

```python
import time

for item in items:
    result = fetch_data(item)
    if result.success:
        time.sleep(0.2)  # Be respectful to external services
```

This pattern makes scripts production-ready and user-friendly for long-running operations.

---

## Troubleshooting

### Issue 1: "pip: command not found" in venv

**Problem:** venv created but pip not available

**Solution:**
```bash
python -m ensurepip
python -m pip install --upgrade pip
```

### Issue 2: Conda environment activation fails

**Problem:** `conda activate` doesn't work

**Solution:**
```bash
# Initialize conda for shell
conda init bash  # or zsh, fish, etc.

# Restart shell or source
source ~/.bashrc
```

### Issue 3: Wrong Python version in environment

**For venv:**
```bash
# Specify Python version when creating
python3.11 -m venv .venv
```

**For conda:**
```bash
# Specify version explicitly
conda create -n myenv python=3.11
```

### Issue 4: Package conflicts

**For venv:**
```bash
# Start fresh
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**For conda:**
```bash
# Try updating resolver
conda update -n base conda
conda install -c conda-forge mamba  # Faster solver
mamba install package-name
```

---

## Quick Reference

### Environment Detection Commands

```bash
# Check what's active
which python
echo $VIRTUAL_ENV
echo $CONDA_DEFAULT_ENV

# Python version
python --version

# Installed packages
pip list          # for pip
conda list        # for conda

# Environment location
pip show package-name  # shows where package is installed
```

### Activation Commands

```bash
# venv
source .venv/bin/activate                    # Linux/Mac
.venv\Scripts\activate                       # Windows

# conda
conda activate environment-name

# Deactivation
deactivate                                   # venv
conda deactivate                             # conda
```

---

## Examples

### Example 1: Safe Installation Flow

**User:** "Install requests"

**Claude:**
```
Let me check your environment first...

[Checks environment]

I see you're in a Python venv at: /home/user/project/.venv
Python version: 3.11.5

Is this the correct environment for installing requests?
```

**User:** "Yes"

**Claude:**
```bash
pip install requests
```

### Example 2: No Environment Warning

**User:** "Install scikit-learn"

**Claude:**
```
⚠️ WARNING: No virtual environment detected!

You're using system Python at: /usr/bin/python3
Installing to system Python is not recommended.

This is a data science package. I suggest creating a conda environment:

conda create -n ml-project python=3.11
conda activate ml-project
conda install -c conda-forge scikit-learn

Would you like me to help set this up?
```

### Example 3: Environment Type Suggestion

**User:** "I need to install biopython, numpy, and pandas"

**Claude:**
```
I notice you need scientific and bioinformatics packages.

Currently: No environment active

I recommend creating a conda environment because:
- Better binary dependency management for numpy/pandas
- Bioconda channel has biopython
- Manages versions more reliably

Suggested setup:
conda create -n bio-project python=3.11
conda activate bio-project
conda install -c conda-forge pandas numpy
conda install -c bioconda biopython

Would you like to proceed with this?
```

---

## Summary

**Always remember:**

1. ✅ **Check environment before any installation**
2. ✅ **Show user what environment is active**
3. ✅ **Confirm with user before proceeding**
4. ⚠️ **Warn if no environment is active**
5. 💡 **Help choose appropriate environment type**
6. 📝 **Document environment setup for reproducibility**

**Never:**
- ❌ Install without checking environment
- ❌ Assume user wants to use system Python
- ❌ Install without user confirmation
- ❌ Skip warning about base conda environment

This skill ensures clean, reproducible, conflict-free Python environments across all projects.
