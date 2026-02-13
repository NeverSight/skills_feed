---
name: galaxy-automation
description: BioBlend and Planemo expertise for Galaxy workflow automation. Galaxy API usage, workflow invocation, status checking, error handling, batch processing, and dataset management. Essential for any Galaxy automation project.
version: 1.0.0
dependencies: bioblend, planemo
---

# Galaxy Workflow Automation with BioBlend and Planemo

## Purpose

This skill provides expert knowledge for automating Galaxy workflows using **BioBlend** (Python Galaxy API library) and **Planemo** (Galaxy workflow testing and execution tool).

## When to Use This Skill

**Use this skill when:**
- ✅ Automating Galaxy workflow execution via API
- ✅ Building batch processing systems for Galaxy
- ✅ Using BioBlend to interact with Galaxy
- ✅ Testing workflows with Planemo
- ✅ Managing Galaxy histories, datasets, and collections programmatically
- ✅ Polling workflow invocation status
- ✅ Implementing error handling and retry logic for Galaxy operations
- ✅ Creating Galaxy automation pipelines
- ✅ Integrating Galaxy into larger bioinformatics workflows

**This skill is NOT project-specific** - it's useful for ANY Galaxy automation project.

---

## Core BioBlend Concepts

### 1. Galaxy Instance Connection

```python
from bioblend.galaxy import GalaxyInstance

# Connect to Galaxy server
gi = GalaxyInstance(url='https://usegalaxy.org', key='your_api_key')

# Verify connection
print(gi.whoami())
```

**Best practices:**
- Store API keys in environment variables, never in code
- Use HTTPS URLs for production
- Mask API keys in logs: `f"{key[:4]}{'*' * (len(key) - 8)}{key[-4:]}"`

---

### 2. History Management

**Create or find history:**
```python
def get_or_find_history_id(gi, history_name):
    """Get history ID by name, or create if doesn't exist"""
    histories = gi.histories.get_histories(name=history_name)

    if histories:
        return histories[0]['id']
    else:
        history = gi.histories.create_history(name=history_name)
        return history['id']
```

**List histories:**
```python
histories = gi.histories.get_histories()
for hist in histories:
    print(f"{hist['name']}: {hist['id']}")
```

**Get history contents:**
```python
history_id = '...'
contents = gi.histories.show_history(history_id, contents=True)

for item in contents:
    print(f"{item['name']}: {item['state']}")
```

---

### 3. Workflow Invocation

**Get workflow by ID:**
```python
workflow_id = 'a1b2c3d4e5f67890'
workflow = gi.workflows.show_workflow(workflow_id)
print(f"Workflow: {workflow['name']}")
```

**Invoke workflow:**
```python
# Prepare inputs (dataset IDs or dataset collection IDs)
inputs = {
    '0': {'id': dataset_id, 'src': 'hda'},  # hda = history dataset
    '1': {'id': collection_id, 'src': 'hdca'}  # hdca = history dataset collection
}

# Invoke workflow
invocation = gi.workflows.invoke_workflow(
    workflow_id,
    inputs=inputs,
    history_id=history_id,
    import_inputs_to_history=False  # Inputs already in history
)

invocation_id = invocation['id']
print(f"Invocation ID: {invocation_id}")
```

---

### 4. Invocation Status Checking

**Poll invocation status:**
```python
def check_invocation_complete(gi, invocation_id, include_steps=False):
    """
    Check if workflow invocation is complete.

    Returns:
        str: 'ok', 'running', 'failed', 'cancelled', 'error'
    """
    invocation = gi.invocations.show_invocation(
        invocation_id,
        include_workflow_steps=include_steps
    )

    state = invocation['state']

    # Possible states: 'new', 'ready', 'scheduled', 'running',
    #                  'ok', 'failed', 'cancelled', 'error'

    return state
```

**Wait for completion:**
```python
import time

def wait_for_invocation(gi, invocation_id, poll_interval=30, timeout=3600):
    """Wait for invocation to complete"""
    start_time = time.time()

    while True:
        state = check_invocation_complete(gi, invocation_id)

        if state in ['ok', 'failed', 'cancelled', 'error']:
            return state

        if time.time() - start_time > timeout:
            raise TimeoutError(f"Invocation {invocation_id} timed out after {timeout}s")

        time.sleep(poll_interval)
```

**Get invocation details with steps:**
```python
invocation = gi.invocations.show_invocation(
    invocation_id,
    include_workflow_steps=True
)

# Check individual steps
for step_id, step_data in invocation.get('steps', {}).items():
    step_state = step_data['state']
    job_id = step_data.get('job_id')
    print(f"Step {step_id}: {step_state} (job: {job_id})")
```

---

### 5. Error Handling Patterns

**Categorize failures:**
```python
def categorize_failure(gi, invocation_id):
    """Determine if failure is retriable"""
    invocation = gi.invocations.show_invocation(
        invocation_id,
        include_workflow_steps=True
    )

    if invocation['state'] != 'failed':
        return None

    # Check failed steps
    failed_steps = []
    for step_id, step_data in invocation.get('steps', {}).items():
        if step_data['state'] == 'error':
            failed_steps.append({
                'step_id': step_id,
                'job_id': step_data.get('job_id')
            })

    # Analyze job failures
    for step in failed_steps:
        if step['job_id']:
            job = gi.jobs.show_job(step['job_id'])
            stderr = job.get('stderr', '')

            # Check for specific error patterns
            if 'out of memory' in stderr.lower():
                return 'retriable_memory'
            elif 'timeout' in stderr.lower():
                return 'retriable_timeout'
            elif 'network' in stderr.lower():
                return 'retriable_network'

    return 'permanent_failure'
```

---

### 6. Rerun Failed Invocations

**Galaxy rerun API:**
```python
def rerun_failed_invocation(gi, invocation_id, use_cached_job=True,
                           replacement_params=None):
    """
    Rerun a failed invocation using Galaxy's native rerun API.

    Args:
        gi: GalaxyInstance
        invocation_id: Failed invocation ID
        use_cached_job: Reuse successful job results
        replacement_params: Dict of parameter changes

    Returns:
        New invocation ID
    """
    rerun_payload = {
        'use_cached_job': use_cached_job
    }

    if replacement_params:
        rerun_payload['replacement_params'] = replacement_params

    # Call Galaxy rerun API
    response = gi.invocations.rerun_invocation(
        invocation_id,
        **rerun_payload
    )

    new_invocation_id = response['id']
    return new_invocation_id
```

**Detect parameter changes from YAML:**
```python
def build_replacement_params_from_yaml(gi, invocation_id, job_yaml_path):
    """
    Compare YAML parameters with invocation parameters.

    Returns dict of changed parameters for rerun.
    """
    import yaml

    # Read new parameters from YAML
    with open(job_yaml_path, 'r') as f:
        new_params = yaml.safe_load(f)

    # Get original invocation parameters
    invocation = gi.invocations.show_invocation(invocation_id)
    orig_params = invocation.get('inputs', {})

    # Find differences
    replacement_params = {}
    for key, new_value in new_params.items():
        if key in orig_params:
            if orig_params[key] != new_value:
                replacement_params[key] = new_value
        else:
            replacement_params[key] = new_value

    return replacement_params
```

---

### 7. Dataset Operations

**Upload dataset:**
```python
file_path = '/path/to/file.fastq.gz'

dataset = gi.tools.upload_file(
    file_path,
    history_id,
    file_type='fastqsanger.gz'
)

dataset_id = dataset['outputs'][0]['id']
```

**Get dataset details:**
```python
dataset = gi.datasets.show_dataset(dataset_id)
print(f"Name: {dataset['name']}")
print(f"State: {dataset['state']}")  # 'ok', 'queued', 'running', 'error'
print(f"Size: {dataset.get('file_size', 0)} bytes")
```

**Wait for dataset upload:**
```python
def wait_for_dataset(gi, dataset_id, poll_interval=5, timeout=600):
    """Wait for dataset to finish uploading"""
    start_time = time.time()

    while True:
        dataset = gi.datasets.show_dataset(dataset_id)
        state = dataset['state']

        if state == 'ok':
            return True
        elif state == 'error':
            raise RuntimeError(f"Dataset {dataset_id} failed to upload")

        if time.time() - start_time > timeout:
            raise TimeoutError(f"Dataset upload timeout after {timeout}s")

        time.sleep(poll_interval)
```

---

### 8. Collections (Paired, List, List:Paired)

**Create dataset collection:**
```python
# List collection (multiple files)
collection_description = {
    'collection_type': 'list',
    'element_identifiers': [
        {'id': dataset_id1, 'name': 'sample1', 'src': 'hda'},
        {'id': dataset_id2, 'name': 'sample2', 'src': 'hda'},
    ]
}

collection = gi.histories.create_dataset_collection(
    history_id,
    collection_description
)

collection_id = collection['id']
```

**Paired collection (forward/reverse reads):**
```python
collection_description = {
    'collection_type': 'paired',
    'element_identifiers': [
        {'id': forward_dataset_id, 'name': 'forward', 'src': 'hda'},
        {'id': reverse_dataset_id, 'name': 'reverse', 'src': 'hda'},
    ]
}
```

**List:Paired (multiple paired-end samples):**
```python
collection_description = {
    'collection_type': 'list:paired',
    'element_identifiers': [
        {
            'name': 'sample1',
            'collection_type': 'paired',
            'element_identifiers': [
                {'id': sample1_fwd, 'name': 'forward', 'src': 'hda'},
                {'id': sample1_rev, 'name': 'reverse', 'src': 'hda'},
            ]
        },
        {
            'name': 'sample2',
            'collection_type': 'paired',
            'element_identifiers': [
                {'id': sample2_fwd, 'name': 'forward', 'src': 'hda'},
                {'id': sample2_rev, 'name': 'reverse', 'src': 'hda'},
            ]
        }
    ]
}
```

---

## Core Planemo Concepts

### 1. Planemo Command Structure

**Basic syntax:**
```bash
planemo run <workflow_file> <job_yaml> \
    --engine external_galaxy \
    --galaxy_url "https://usegalaxy.org" \
    --galaxy_user_key "your_api_key" \
    --history_name "My Analysis" \
    --test_output_json "invocation.json"
```

**Common options:**
- `--engine external_galaxy`: Use external Galaxy server (not local)
- `--simultaneous_uploads`: Upload all files simultaneously (faster but more resource-intensive)
- `--check_uploads_ok`: Verify uploads completed successfully
- `--test_output_json`: Save invocation details to JSON file

---

### 2. Job YAML Format

**Example job.yml:**
```yaml
# Inputs
input_reads:
  class: File
  path: /path/to/reads.fastq.gz

# Collections
paired_reads:
  class: Collection
  collection_type: paired
  elements:
    - identifier: forward
      class: File
      path: /path/to/forward.fastq.gz
    - identifier: reverse
      class: File
      path: /path/to/reverse.fastq.gz

# Parameters
kmer_size: 21
coverage_threshold: 30
```

---

### 3. Generating Planemo Commands Programmatically

```python
def build_planemo_command(workflow_path, job_yaml, galaxy_url, api_key,
                          history_name, output_json, log_file):
    """
    Build planemo run command.

    Security: Mask API key in display, but use full key in command.
    """
    command = (
        f'planemo run "{workflow_path}" "{job_yaml}" '
        f'--engine external_galaxy '
        f'--galaxy_url "{galaxy_url}" '
        f'--simultaneous_uploads '
        f'--check_uploads_ok '
        f'--galaxy_user_key "{api_key}" '
        f'--history_name "{history_name}" '
        f'--test_output_json "{output_json}" '
        f'> "{log_file}" 2>&1'
    )

    return command
```

**Execute with error handling:**
```python
import os

return_code = os.system(planemo_command)

if return_code != 0:
    # Planemo failed - workflow was NOT launched in Galaxy
    # No invocation ID exists
    print(f"ERROR: Planemo failed with return code {return_code}")
    print(f"Check log: {log_file}")
    # DO NOT mark invocation as failed - it was never created
else:
    # Planemo succeeded - workflow launched
    # Invocation ID is in output JSON
    print(f"SUCCESS: Workflow launched")
```

**CRITICAL:** `os.system()` return codes are shifted by 8 bits:
- Exit code 1 becomes return code 256
- Exit code 2 becomes return code 512
- To get actual exit code: `actual_exit = return_code >> 8`

---

### 4. Parsing Planemo Output

**Extract invocation ID from JSON:**
```python
import json

def extract_invocation_id(output_json_path):
    """Extract invocation ID from planemo test output"""
    with open(output_json_path, 'r') as f:
        data = json.load(f)

    # Planemo output structure
    tests = data.get('tests', [])
    if tests and len(tests) > 0:
        test = tests[0]
        invocation_id = test['data'].get('invocation_id')
        return invocation_id

    return None
```

---

## Common Automation Patterns

### 1. Thread-Safe Galaxy Operations

**Use locks for concurrent API calls:**
```python
import threading

galaxy_lock = threading.Lock()

def thread_safe_invoke_workflow(gi, workflow_id, inputs, history_id):
    """Invoke workflow with thread safety"""
    with galaxy_lock:
        invocation = gi.workflows.invoke_workflow(
            workflow_id,
            inputs=inputs,
            history_id=history_id
        )
        return invocation['id']
```

**Why:** Galaxy API can have issues with concurrent uploads/operations from same API key.

---

### 2. Batch Processing Pattern

```python
def process_samples_batch(gi, workflow_id, samples, max_concurrent=3):
    """
    Process multiple samples with concurrency limit.

    Args:
        gi: GalaxyInstance
        workflow_id: Workflow to run
        samples: List of sample dicts with 'name' and 'files'
        max_concurrent: Max parallel invocations
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed

    def process_one_sample(sample):
        # Create history
        history_id = get_or_find_history_id(gi, sample['name'])

        # Upload files
        dataset_ids = []
        for file_path in sample['files']:
            ds = gi.tools.upload_file(file_path, history_id)
            dataset_ids.append(ds['outputs'][0]['id'])

        # Invoke workflow
        inputs = {'0': {'id': dataset_ids[0], 'src': 'hda'}}
        invocation_id = thread_safe_invoke_workflow(
            gi, workflow_id, inputs, history_id
        )

        # Wait for completion
        state = wait_for_invocation(gi, invocation_id)

        return {
            'sample': sample['name'],
            'invocation_id': invocation_id,
            'state': state
        }

    # Process with limited concurrency
    with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
        futures = {executor.submit(process_one_sample, s): s for s in samples}

        results = []
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(f"Completed: {result['sample']} - {result['state']}")

        return results
```

---

### 3. Resume Capability Pattern

**Track processed samples:**
```python
import json
import os

STATE_FILE = 'processing_state.json'

def load_state():
    """Load processing state"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {'completed': [], 'failed': []}

def save_state(state):
    """Save processing state"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def process_with_resume(samples):
    """Process samples with resume capability"""
    state = load_state()

    for sample in samples:
        sample_name = sample['name']

        # Skip if already completed
        if sample_name in state['completed']:
            print(f"Skipping {sample_name} (already completed)")
            continue

        try:
            # Process sample
            result = process_one_sample(sample)

            if result['state'] == 'ok':
                state['completed'].append(sample_name)
            else:
                state['failed'].append(sample_name)

            save_state(state)

        except Exception as e:
            print(f"Error processing {sample_name}: {e}")
            state['failed'].append(sample_name)
            save_state(state)
```

---

## Security Best Practices

### 1. API Key Management

**Store in environment variables:**
```python
import os

api_key = os.environ.get('GALAXY_API_KEY')
if not api_key:
    raise ValueError("GALAXY_API_KEY environment variable not set")

gi = GalaxyInstance(url, api_key)
```

**Mask in logs:**
```python
def mask_api_key(key):
    """Mask API key for display"""
    if len(key) <= 8:
        return '*' * len(key)
    return f"{key[:4]}{'*' * (len(key) - 8)}{key[-4:]}"

masked_key = mask_api_key(api_key)
print(f"Using API key: {masked_key}")
```

---

### 2. Path Handling

**Always quote paths in shell commands:**
```python
# ✅ Good - handles spaces
command = f'planemo run "{workflow_path}" "{job_yaml}"'

# ❌ Bad - breaks with spaces
command = f'planemo run {workflow_path} {job_yaml}'
```

---

## Debugging

### 1. Galaxy History Inspection

```python
def inspect_history(gi, history_id):
    """Print detailed history information"""
    history = gi.histories.show_history(history_id)
    print(f"History: {history['name']} ({history['id']})")
    print(f"State: {history['state']}")

    contents = gi.histories.show_history(history_id, contents=True)

    for item in contents:
        print(f"  [{item['state']}] {item['name']} (type: {item['history_content_type']})")
```

---

### 2. Invocation Step Analysis

```python
def analyze_failed_invocation(gi, invocation_id):
    """Analyze why invocation failed"""
    invocation = gi.invocations.show_invocation(
        invocation_id,
        include_workflow_steps=True
    )

    print(f"Invocation: {invocation_id}")
    print(f"State: {invocation['state']}")

    for step_id, step_data in invocation.get('steps', {}).items():
        step_state = step_data['state']
        job_id = step_data.get('job_id')

        if step_state == 'error':
            print(f"\nFailed Step {step_id}:")

            if job_id:
                job = gi.jobs.show_job(job_id)
                print(f"  Tool: {job.get('tool_id')}")
                print(f"  Exit code: {job.get('exit_code')}")
                print(f"  Stderr:\n{job.get('stderr', 'N/A')}")
```

---

## Common Pitfalls

1. **Planemo failures vs Galaxy failures**
   - Planemo return code != 0: Workflow was NOT launched, no invocation exists
   - Invocation state = 'failed': Workflow was launched but Galaxy job failed
   - Don't confuse these two failure modes

2. **Concurrent uploads**
   - Too many simultaneous uploads can overwhelm Galaxy
   - Use max_concurrent limits (typically 3-5)
   - Consider `--simultaneous_uploads` vs sequential

3. **Dataset state checking**
   - Don't invoke workflows before uploads complete
   - Always wait for dataset state = 'ok'

4. **History name conflicts**
   - Use unique history names (add timestamps or suffixes)
   - Check for existing histories before creating

5. **Return code interpretation**
   - `os.system()` shifts exit codes (exit 1 → return 256)
   - Use `return_code >> 8` to get actual exit code

6. **Invocation ID recovery**
   - Terminal disconnection loses invocation ID
   - Always save invocation IDs to file immediately
   - Use `--test_output_json` with planemo

---

## Best Practices Summary

1. ✅ Use environment variables for API keys
2. ✅ Mask API keys in logs and output
3. ✅ Quote all file paths in shell commands
4. ✅ Implement thread-safety for concurrent operations
5. ✅ Save state frequently for resume capability
6. ✅ Wait for dataset uploads before invoking workflows
7. ✅ Poll invocation status with reasonable intervals (30-60s)
8. ✅ Distinguish planemo failures from Galaxy failures
9. ✅ Implement proper error handling and retry logic
10. ✅ Use unique history names to avoid conflicts

---

## Related Skills

- **galaxy-tool-wrapping**: For creating Galaxy tool wrappers
- **galaxy-workflow-development**: For creating Galaxy workflows
- **vgp-pipeline**: VGP-specific orchestration (uses this skill as dependency)

---

## Resources

- **BioBlend Documentation**: https://bioblend.readthedocs.io/
- **Planemo Documentation**: https://planemo.readthedocs.io/
- **Galaxy API**: https://docs.galaxyproject.org/en/master/api/
- **Galaxy Training**: https://training.galaxyproject.org/
