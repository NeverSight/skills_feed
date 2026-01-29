---
name: dify-workflow-skills
description: Build and edit Dify workflow DSL files. Use when creating new Dify workflows from scratch, modifying existing workflows (adding/removing nodes, changing connections), validating workflow structure, or designing LLM-based automation flows with code execution, conditional logic, loops, and error handling.
---

# Dify Workflow DSL Builder

Build, edit, and validate Dify workflow DSL (Domain-Specific Language) files for creating AI-powered automation workflows.

This skill is based on the Dify open-source platform's workflow engine, which powers both Workflow apps and Advanced Chat apps with a React Flow-based visual editor.

## Architecture Overview

Dify workflows use a **queue-based, event-driven architecture** with:

### Backend (Python - Execution Engine)
- **GraphEngine**: Central orchestrator managing workflow execution
- **WorkerPool**: Thread pool for parallel node execution
- **VariablePool**: Centralized variable management across nodes
- **EdgeProcessor**: Handles conditional routing and branch selection
- **Graph Validator**: Ensures workflow integrity before execution

### Frontend (React/TypeScript - Visual Editor)
- **React Flow**: Canvas-based node graph editor
- **Zustand Store**: State management for nodes, edges, and viewport
- **WorkflowContext**: Provides workflow state to component tree
- **BaseNode**: Common wrapper for all node types with handles, headers, and interactions
- **Panel System**: Dynamic configuration panels for each node type
- **Hook Injection Pattern**: Decouples UI from execution logic (draft sync, workflow run)

### Integration Layer
- **workflow**: Core canvas engine (generic React Flow implementation)
- **workflow-app**: Application wrapper (business logic, API integration, lifecycle management)
- **Draft Management**: Auto-save with debouncing and `sendBeacon` for safety
  - Uses debounced sync to prevent excessive API calls
  - Cancels pending syncs on unmount to avoid race conditions
  - Tracks loaded state with `isWorkflowDataLoaded` flag
- **Features System**: Optional features (file upload, speech-to-text, citations) integrated with workflow
- **Trigger Status Management**: Separate store for tracking trigger node enable/disable state
  - Trigger nodes can be enabled or disabled independently
  - Status persists across workflow editor sessions
  - Used for webhook, schedule, and plugin triggers

## Core Capabilities

1. **Create new workflows** - Generate complete workflow YAML files from descriptions
2. **Edit existing workflows** - Add, modify, or remove nodes and connections
3. **Validate workflows** - Check DSL syntax and structure
4. **Design complex flows** - Build workflows with LLM nodes, code execution, branching, loops, and error handling
5. **Error handling strategies** - Implement fail-branch, retry, or default-value error handling

## Quick Reference

**Node Types**: See [references/node_types.md](references/node_types.md) for complete list including:
- **Core Flow**: start, end, answer
- **LLM & AI**: llm, agent, parameter-extractor
- **Logic & Control**: if-else, question-classifier, loop, iteration
- **Data Processing**: code, template-transform, variable-aggregator, assigner, list-operator, document-extractor
- **External Integration**: http-request, tool, knowledge-retrieval, knowledge-index, datasource
- **Advanced**: trigger-webhook, trigger-schedule, trigger-plugin, human-input

**Edge Types and Connections**: See [references/edge_types.md](references/edge_types.md) for:
- Source handle types (source, true/false, success-branch/fail-branch, loop)
- Edge data properties and validation rules
- Common connection patterns

**Node Positioning**: See [references/node_positioning.md](references/node_positioning.md) for:
- Canvas coordinate system and spacing guidelines
- Layout patterns (linear, branching, error handling, iteration)
- Position calculation formulas

**Common Node Properties**: All nodes support these internal properties (prefixed with `_`):
- `_runningStatus`: Current execution status (running, succeeded, failed)
- `_connectedSourceHandleIds`/`_connectedTargetHandleIds`: Connection tracking
- `_isSingleRun`: Single execution mode for debugging
- `_isCandidate`: Phantom node during connection drag
- `_children`: Child nodes for container types (iteration, loop)
- `_iterationLength`/`_iterationIndex`: Iteration state tracking
- `_loopLength`/`_loopIndex`: Loop state tracking
- `_retryIndex`: Current retry attempt
- `_waitingRun`: Queued for execution, human-input

**Workflow Structure**: See [references/workflow_structure.md](references/workflow_structure.md) for complete DSL format

**Edge Types**: See [references/edge_types.md](references/edge_types.md) for connection patterns and handle types

**Node Positioning**: See [references/node_positioning.md](references/node_positioning.md) for layout guidelines

**Templates**: Check [assets/](assets/) for example workflows

## Creating a New Workflow

### Step 1: Understand Requirements

Ask the user:
- What should the workflow do?
- What are the inputs and outputs?
- What processing steps are needed?
- Any conditional logic or error handling?

### Step 2: Design Node Flow

Plan the workflow structure:

1. **Start node** - Define input variables
2. **Processing nodes** - LLM, code, tools, etc.
3. **Control flow** - if-else for branching, loop for iteration
4. **Error handling** - Use fail-branch on code nodes
5. **Output aggregation** - variable-aggregator to merge branches
6. **End node** - Define outputs

### Step 3: Generate Node IDs

Use `scripts/generate_id.py` to create unique node IDs:

```bash
python3 scripts/generate_id.py 5  # Generate 5 unique IDs
```

Or generate in Python/JavaScript:
```python
# Python
import time
node_id = str(int(time.time() * 1000))
```

```javascript
// JavaScript (used in Dify frontend)
const nodeId = `${Date.now()}`
```

**Special ID patterns for container nodes**:
- Iteration/Loop start nodes: `${parentNodeId}start`
- Example: If iteration node ID is `1736668800000`, its start node ID is `1736668800000start`

### Step 4: Build the Workflow

Create the complete YAML structure with:
- Top-level metadata (kind, version, app)
- App section (name, description, icon)
- Workflow section with features and graph
- Nodes array with positions
- Edges array connecting nodes

**Template to use**: Start from `assets/simple_llm_workflow.yml` for basic flows

### Step 5: Validate

Check the workflow structure for common issues:
- All nodes have unique IDs
- All edges reference existing node IDs
- Start and end nodes exist
- Required fields are present
- Variable references use correct syntax: `{{#node_id.field#}}`

## Common Workflow Patterns

### Pattern 1: Simple LLM Flow

Start → LLM → End

**Use case**: Basic question answering, text generation

**Template**: `assets/simple_llm_workflow.yml`

### Pattern 2: Error Handling Flow

Start → Code (with fail-branch) → [Success → Aggregator] / [Fail → LLM Recovery → Retry → Aggregator] → End

**Use case**: Robust data processing with error recovery

**Template**: `assets/error_handling_workflow.yml`

**Key points**:
- Set `error_strategy: fail-branch` on code node
- Fail branch provides `error_message` and `error_type` variables
- Use variable-aggregator to merge success/fail branches
- Reference aggregator output in end node

### Pattern 3: Conditional Routing

Start → If-Else → [True → Handler A] / [False → Handler B] → Aggregator → End

**Use case**: Route requests based on content/type

**Template**: `assets/conditional_workflow.yml`

**Key points**:
- If-else has `true` and `false` sourceHandles
- Use comparison operators: contains, starts_with, is_empty, etc.
- Combine conditions with logical_operator: "and" or "or"

### Pattern 4: Loop Processing

Start → Loop → [Process Items] → Loop End → End

**Use case**: Iterative processing with break conditions

**Key points**:
- Set `loop_count` for maximum iterations
- Define `break_conditions` to exit early
- Loop maintains state across iterations

## Editing Existing Workflows

### Adding a Node

1. Read the existing workflow file
2. Generate a new unique node ID
3. Add node to `workflow.graph.nodes` array with:
   - Unique ID and position
   - Node type and configuration
   - Proper sourcePosition/targetPosition
4. Add edge(s) to `workflow.graph.edges` connecting the new node
5. Update any dependent nodes (e.g., end node outputs)

### Removing a Node

1. Identify the node ID to remove
2. Remove node from `workflow.graph.nodes`
3. Remove all edges referencing that node ID (as source or target)
4. Update downstream nodes that referenced the removed node's outputs

### Modifying Connections

1. Find edge by source and target node IDs
2. Update edge `source`, `target`, `sourceHandle`, or `targetHandle`
3. Update edge `data.sourceType` and `data.targetType` to match actual node types
4. Update edge `id` to follow naming convention: `{source_id}-{handle}-{target_id}-target`

## Variable Reference Syntax

Variables are managed in a centralized **VariablePool** and use the format: `{{#node_id.field_name#}}`

### Variable Types (VarType)

Dify supports these variable types for type-safe data flow:

**Primitive Types**:
- `string`: Text data
- `number`: Floating-point numbers
- `integer`: Whole numbers
- `boolean`: true/false values
- `secret`: Encrypted sensitive data (API keys, passwords)

**Complex Types**:
- `object`: JSON objects
- `file`: Single file reference
- `array`: Generic array
- `array[string]`: Array of strings
- `array[number]`: Array of numbers
- `array[object]`: Array of objects
- `array[boolean]`: Array of booleans
- `array[file]`: Array of files
- `array[any]`: Array of mixed types
- `any`: Any type (use sparingly)

**Special Types**:
- `contexts`: Knowledge retrieval results
- `iterator`: Iteration input variable
- `loop`: Loop input variable

### File Upload Configuration

When using file input types (`file`, `files`, `file-list`), you can configure upload settings:

**Default File Upload Settings**:
```yaml
allowed_file_upload_methods: ['local_file', 'remote_url']
max_length: 5  # Maximum number of files
allowed_file_types: ['image']  # Options: image, document, audio, video, custom
allowed_file_extensions: []  # e.g., ['.pdf', '.docx']
```

**Upload Methods**:
- `local_file`: Direct file upload from local system
- `remote_url`: Upload file from URL

**File Type Categories**:
- `image`: Image files (JPG, PNG, GIF, etc.)
- `document`: Document files (PDF, DOCX, TXT, etc.)
- `audio`: Audio files (MP3, WAV, etc.)
- `video`: Video files (MP4, AVI, etc.)
- `custom`: Custom file types (specify extensions)

### Input Variable Types (InputVarType)

Start nodes use these input types for user-facing variables:

- `text-input`: Single-line text input
- `paragraph`: Multi-line text input
- `select`: Dropdown selection
- `number`: Numeric input
- `checkbox`: Boolean checkbox
- `url`: URL input with validation
- `files`: Multiple file upload
- `file`: Single file upload
- `file-list`: Multiple file list
- `json`: JSON input (object or array)
- `json_object`: JSON object with schema validation
- `contexts`: Knowledge retrieval context
- `iterator`: Iteration variable
- `loop`: Loop variable

### Variable Selector Pattern

The variable pattern regex: `{{#[a-zA-Z0-9_]{1,50}(?:\.[a-zA-Z_][a-zA-Z0-9_]{0,29}){1,10}#}}`

**Selector structure**: `[node_id, variable_name, ...optional_nested_keys]`
- First element: node ID that produced the variable
- Second element: variable name or output field
- Additional elements: nested object keys or array indices (for FileSegment/ObjectSegment)

**ValueSelector**: Array format used in DSL (e.g., `['1732007415808', 'text']`)
- Represented as arrays in YAML: `value_selector: ['node_id', 'field_name']`
- Converted to template syntax in prompts: `{{#node_id.field_name#}}`

### System Variables

Available via `sys` node ID:
- `{{#sys.query#}}` - User query/input
- `{{#sys.files#}}` - Uploaded files
- `{{#sys.conversation_id#}}` - Current conversation ID
- `{{#sys.user_id#}}` - User identifier
- `{{#sys.dialogue_count#}}` - Number of dialogue turns
- `{{#sys.app_id#}}` - Application ID
- `{{#sys.workflow_id#}}` - Workflow ID
- `{{#sys.workflow_run_id#}}` - Current execution ID
- `{{#sys.timestamp#}}` - Current timestamp

### Common Output Fields by Node Type

**LLM Node**:
- `{{#node_id.text#}}` - Generated text response (type: string)
- `{{#node_id.usage#}}` - Token usage information (type: object)
- `{{#node_id.reasoning_content#}}` - Model reasoning (if enabled) (type: string)

**Agent Node**:
- `{{#node_id.usage#}}` - Token usage information (type: object)

**Code Node**:
- `{{#node_id.output_name#}}` - Named outputs defined in node config
- `{{#node_id.error_message#}}` - Error message (fail-branch only) (type: string)
- `{{#node_id.error_type#}}` - Error type (fail-branch only) (type: string)

**Start Node**:
- `{{#node_id.variable_name#}}` - Input variables defined in start node

**If-Else Node**:
- `{{#node_id.condition_result#}}` - Boolean condition result

**Loop Node**:
- `{{#node_id.output#}}` - Loop output array
- `{{#node_id.iteration#}}` - Current iteration number

**HTTP Request Node**:
- `{{#node_id.body#}}` - Response body (type: string)
- `{{#node_id.status_code#}}` - HTTP status code (type: number)
- `{{#node_id.headers#}}` - Response headers (type: object)
- `{{#node_id.files#}}` - Downloaded files if response is file (type: array[file])

**Tool Node**:
- `{{#node_id.text#}}` - Tool output text (type: string)
- `{{#node_id.files#}}` - Tool output files (type: array[file])
- `{{#node_id.json#}}` - Tool output JSON (type: array[object])

**Knowledge Retrieval Node**:
- `{{#node_id.result#}}` - Retrieved knowledge segments (type: array[object])

**Template Transform Node**:
- `{{#node_id.output#}}` - Transformed output (type: string)

**Question Classifier Node**:
- `{{#node_id.class_name#}}` - Classification result (type: string)
- `{{#node_id.usage#}}` - Token usage information (type: object)

**Parameter Extractor Node**:
- `{{#node_id.__is_success#}}` - Extraction success indicator (type: number)
- `{{#node_id.__reason#}}` - Extraction failure reason (type: string)
- `{{#node_id.__usage#}}` - Token usage information (type: object)
- Plus custom extracted parameters defined in node config

**Variable Aggregator**:
- `{{#node_id.output#}}` - Aggregated output from merged branches

**File Object Structure** (when file type is used):
- `name` - File name (type: string)
- `size` - File size in bytes (type: number)
- `type` - File type category (type: string)
- `extension` - File extension (type: string)
- `mime_type` - MIME type (type: string)
- `transfer_method` - Transfer method used (type: string)
- `url` - File URL (type: string)
- `related_id` - Related resource ID (type: string)

**Knowledge Retrieval Result Structure**:
```json
{
  "content": "",
  "title": "",
  "url": "",
  "icon": "",
  "metadata": {
    "dataset_id": "",
    "dataset_name": "",
    "document_id": [],
    "document_name": "",
    "document_data_source_type": "",
    "segment_id": "",
    "segment_position": "",
    "segment_word_count": "",
    "segment_hit_count": "",
    "segment_index_node_hash": "",
    "score": ""
  }
}
```

### Environment and Conversation Variables

**Environment variables** (defined at app level):
- Access via special node ID: `env`
- Example: `{{#env.API_KEY#}}`

**Conversation variables** (session state):
- Access via special node ID: `conversation`
- Example: `{{#conversation.user_context#}}`

### Example Variable Usage

```yaml
# In LLM prompt template
prompt_template:
  - role: system
    text: "You are a helpful assistant."
  - role: user
    text: "Process this input: {{#1732007415808.user_input#}}"

# In code node
variables:
  - ["1732007415808", "user_input"]
  - ["1732007420123", "processed_data"]

# Accessing nested object fields
text: "File name: {{#upload_node.files.name#}}"
text: "API response status: {{#http_node.status_code#}}"
```

## Node Positioning

Position nodes on the canvas for visual clarity:

**Layout Constants** (from Dify frontend):
- `NODE_WIDTH`: 240 pixels
- `X_OFFSET`: 60 pixels (horizontal spacing)
- `NODE_WIDTH_X_OFFSET`: 300 pixels (node width + spacing)
- `Y_OFFSET`: 39 pixels
- `START_INITIAL_POSITION`: { x: 80, y: 282 }
- `NODE_LAYOUT_HORIZONTAL_PADDING`: 60 pixels
- `NODE_LAYOUT_VERTICAL_PADDING`: 60 pixels
- `NODE_LAYOUT_MIN_DISTANCE`: 100 pixels

**Container Node Padding**:
- Iteration/Loop containers:
  - top: 65, right: 16, bottom: 20, left: 16
- Z-index for iteration/loop: 1 (container), 1002 (children)

**Horizontal spacing**: 300-400 pixels between connected nodes
**Vertical spacing**:
- Same level: same y-coordinate
- Branches: offset by 150-200 pixels

**Example positions**:
```yaml
Start: x=80, y=282 # Initial position
LLM: x=380, y=282  # Start + NODE_WIDTH_X_OFFSET
Code: x=680, y=282
End: x=980, y=282
```

For branching:
```yaml
If-else: x=380, y=300
True branch: x=680, y=200
False branch: x=680, y=450
Aggregator: x=980, y=300
```

**Container nodes (Iteration/Loop)**:
- Start node inside container: { x: 24, y: 68 } (relative to container)
- Children nodes have `parentId` set to container ID
- Children have higher z-index (1002) than container (1)

See [references/node_positioning.md](references/node_positioning.md) for detailed layout patterns and formulas.

## Visual Editor Integration

The DSL you create is rendered in the Dify visual workflow editor built with React Flow.

### How DSL Maps to UI

**Nodes** → Visual blocks on canvas with:
- Icon and title (from `type` and `title` fields)
- Connection handles (based on node type and error_strategy)
- Configuration panel (node-specific form in right sidebar)
- Status indicators (running, succeeded, failed)

**Edges** → Bezier curves connecting nodes with:
- Visual styling based on state (hovering, selected, running)
- Labels for branching paths (true/false, classification labels)
- Color coding for success/fail branches

**Viewport** → Canvas view settings:
```yaml
viewport:
  x: 0      # Pan offset X
  y: 0      # Pan offset Y
  zoom: 1.0 # Zoom level (0.1 to 2.0)
```

### Frontend Component Architecture

When your DSL is loaded into the editor:

1. **WorkflowContextProvider** initializes Zustand store with nodes/edges
2. **ReactFlow** renders the canvas with custom node components
3. **BaseNode** wraps each node with common UI (handles, headers)
4. **Panel System** shows configuration forms when node is selected
5. **Hook System** manages draft auto-save and execution

### UI Features Not in DSL

These UI-only properties are managed by the frontend (don't include in DSL):

- `_hovering`, `_connectedNodeIsHovering`: Mouse interaction state
- `_connectedSourceHandleIds`, `_connectedTargetHandleIds`: Computed from edges
- `_runningStatus`, `_singleRunningStatus`: Runtime execution state
- `_isCandidate`: Temporary phantom node during connection drag
- `selected`: Node selection state

**Important**: Only include persistent properties in your DSL (id, type, title, position, configuration). Runtime UI state is computed by the editor.

## Error Handling Strategy

### Error Strategies

Dify supports multiple error handling strategies defined in the node configuration:

**1. fail-branch** (recommended for code/http nodes):
- Creates alternative execution path on error
- Provides `error_message` and `error_type` variables
- Uses `sourceHandle: "fail-branch"` in edge configuration
- Success path uses `sourceHandle: "success-branch"`
- Requires variable-aggregator to merge with success path before continuing to end node
- Allows graceful error recovery and custom error handling logic

**2. default-value**:
- Returns a predefined default value on error
- Continues main execution path without branching
- Simpler but less robust than fail-branch
- Good for non-critical operations where fallback values are acceptable

**3. abort** (default):
- Stops the entire workflow execution on failure
- No additional configuration needed
- Used when errors are unrecoverable

**4. retry**:
- Configurable retry logic with max retries and intervals
- Defined in node's `retry_config` section
- Useful for transient failures (network issues, rate limits)
- **Supported on**: LLM, Tool, HTTP Request, Code nodes only

**Retry Configuration Structure**:
```yaml
retry_config:
  max_retries: 3        # Maximum retry attempts (default: 3)
  retry_interval: 100   # Interval between retries in ms (default: 100)
```

### Implementing Fail-Branch Error Handling

In node configuration:
```yaml
error_strategy: fail-branch
```

In edges array:
```yaml
# Success path
- id: code_node-success-branch-next_node-target
  source: code_node_id
  target: aggregator_id
  sourceHandle: success-branch
  targetHandle: target

# Failure path
- id: code_node-fail-branch-error_handler-target
  source: code_node_id
  target: error_handler_id
  sourceHandle: fail-branch
  targetHandle: target
```

**Available error variables** in fail-branch:
- `{{#node_id.error_message#}}` - Human-readable error description
- `{{#node_id.error_type#}}` - Error type classification

## Validation Checklist

Before finalizing a workflow, verify:

### Structural Validation
- [ ] All node IDs are unique and properly formatted (numeric strings or valid identifiers)
- [ ] Workflow has exactly one root node (start, datasource, or trigger node)
- [ ] Workflow has at least one end node
- [ ] All edges reference valid source and target node IDs that exist in the nodes array
- [ ] No circular dependencies that would create infinite loops (except intentional loop nodes)
- [ ] Root node is correctly identified and accessible

### Edge and Connection Validation
- [ ] All edge IDs are unique
- [ ] Edge `sourceHandle` values match node types:
  - Standard nodes: `"source"` (default)
  - If-else/Question-classifier: `"true"`, `"false"`, or classification label
  - Code/HTTP with error handling: `"success-branch"` or `"fail-branch"`
  - Loop nodes: `"loop"` for continuation
- [ ] Edge `targetHandle` is typically `"target"` for most nodes
- [ ] Edge `data.sourceType` matches the actual source node type
- [ ] Edge `data.targetType` matches the actual target node type
- [ ] Branching paths (from if-else, question-classifier) have edges for all possible outcomes
- [ ] Fail-branch edges exist when `error_strategy: fail-branch` is used

### Variable and Data Flow Validation
- [ ] Variable references use correct syntax: `{{#node_id.field#}}`
- [ ] All referenced variables exist in upstream nodes (nodes that execute before current node)
- [ ] Variable selectors match actual output fields of referenced nodes
- [ ] System variables use correct `sys` prefix: `{{#sys.query#}}`
- [ ] Environment variables use `env` prefix if needed
- [ ] No undefined variable references that would cause runtime errors

### Error Handling Validation
- [ ] Nodes with `error_strategy: fail-branch` have both success and fail edges
- [ ] Branching paths merge at variable-aggregator before reaching end node
- [ ] Variable aggregator receives inputs from all branch paths
- [ ] Default values are provided when using `error_strategy: default-value`
- [ ] Retry configurations are valid (max retries, intervals) if using retry strategy

### Node Configuration Validation
- [ ] Required fields are present for each node type (see node_types.md)
- [ ] Node positions are set for visual layout (x, y coordinates)
- [ ] LLM nodes have valid model configurations (provider, name, mode)
- [ ] Code nodes specify valid language (python3 or javascript)
- [ ] HTTP request nodes have valid URLs and methods
- [ ] Loop nodes have valid `loop_count` and break conditions
- [ ] If-else nodes have properly structured conditions with valid operators

### Workflow Execution Validation
- [ ] No nodes are unreachable (all nodes can be reached from root node)
- [ ] All execution paths eventually lead to an end node or answer node
- [ ] Container nodes (iteration, loop) have proper start/end node pairs
- [ ] Human-input nodes are used appropriately (workflow will pause for input)
- [ ] Trigger nodes (webhook, schedule) are not mixed with standard start nodes

## Node Execution Types

Dify categorizes nodes by their execution behavior. Understanding these types helps design correct workflows:

### EXECUTABLE (Standard Logic Nodes)
Execute logic and produce outputs. Most common node type.
- **Examples**: llm, code, http-request, knowledge-retrieval, template-transform
- **Behavior**: Execute when all input dependencies are satisfied
- **Source Handle**: `"source"` (or `"success-branch"`/`"fail-branch"` with error handling)
- **Outputs**: Defined by node type (see Variable Reference section)

### BRANCH (Conditional Routing Nodes)
Control flow by choosing between multiple paths based on conditions.
- **Examples**: if-else, question-classifier
- **Behavior**: Evaluate conditions and activate one or more output edges
- **Source Handles**:
  - If-else: `"true"`, `"false"`
  - Question-classifier: classification labels (custom)
- **Important**: Unselected paths are marked as "skipped" and don't execute downstream

### CONTAINER (Sub-graph Management)
Manage nested execution contexts with iterations or loops.
- **Examples**: iteration, loop
- **Behavior**: Execute internal sub-graph multiple times
- **Components**:
  - Parent container node
  - Internal start node (iteration-start, loop-start)
  - Internal end node (iteration-end, loop-end)
- **Source Handle**: `"loop"` for iteration/loop continuation
- **State Management**: Maintain loop variables and iteration counts

### RESPONSE (Output Streaming)
Stream outputs to users in real-time.
- **Examples**: answer, end
- **Behavior**: Output results and potentially complete workflow
- **Usage**: Answer nodes can appear mid-workflow; End nodes terminate execution

### ROOT (Entry Points)
Serve as workflow entry points.
- **Examples**: start, datasource, trigger-webhook, trigger-schedule, trigger-plugin
- **Behavior**: First node to execute; no incoming edges
- **Important**: Only ONE root node per workflow
- **Constraint**: Standard start nodes and trigger nodes cannot coexist

### Nodes That Support Output Variables

The following node types can produce output variables that other nodes can reference:
- Start, TriggerWebhook, TriggerPlugin
- LLM, Agent
- KnowledgeRetrieval
- Code
- TemplateTransform
- HttpRequest
- Tool
- VariableAssigner, VariableAggregator
- QuestionClassifier
- ParameterExtractor
- Iteration, Loop
- DocumentExtractor (DocExtractor)
- ListFilter (list-operator)
- DataSource

**Note**: Nodes not in this list (like if-else, end, answer) typically don't produce reusable output variables, though some may have limited internal state.

## Workflow Execution Model

### Execution Flow

1. **Initialization**: GraphEngine enqueues root node into ReadyQueue
2. **Worker Execution**: Worker threads pull nodes from ReadyQueue and execute them
3. **Event Emission**: Workers push events (started, succeeded, failed) to event_queue
4. **Edge Processing**: Dispatcher processes events and identifies downstream nodes
5. **Dependency Resolution**: Downstream nodes added to ReadyQueue when dependencies satisfied
6. **Parallel Execution**: Multiple workers execute independent nodes concurrently
7. **Completion**: Workflow ends when End node executes or execution fails

### Edge States

Edges can be in three states during execution:
- **UNKNOWN**: Initial state, not yet evaluated
- **TAKEN**: Edge is traversed (condition met or path selected)
- **SKIPPED**: Edge is not traversed (condition failed or alternative path chosen)

### Workflow Execution Status

Workflows progress through these states:
- **SCHEDULED**: Queued but not yet started
- **RUNNING**: Currently executing
- **SUCCEEDED**: Completed without errors
- **FAILED**: Terminated due to unhandled error
- **PARTIAL_SUCCEEDED**: Completed with handled errors (via fail-branch or default-value)
- **STOPPED**: Manually stopped or aborted
- **PAUSED**: Waiting for human input (human-input node)

### Node Running Status

Individual nodes track their execution state with these statuses:
- **NOT_START**: Node hasn't started execution yet
- **WAITING**: Node is queued and waiting to execute
- **LISTENING**: Node is listening for events (trigger nodes)
- **RUNNING**: Node is currently executing
- **SUCCEEDED**: Node completed successfully
- **FAILED**: Node failed with unhandled error
- **EXCEPTION**: Node failed but error was handled
- **RETRY**: Node is retrying after failure
- **STOPPED**: Node execution was stopped

**Important UI State Properties** (runtime only, not in DSL):
- `_runningStatus`: Current execution status
- `_singleRunningStatus`: Status when running single node
- `_waitingRun`: Node is queued for execution
- `_retryIndex`: Current retry attempt number
- `_isSingleRun`: Node is in single-run debug mode

### Best Practices for Execution

1. **Parallel vs Sequential**: Independent nodes execute in parallel automatically. Use edges to enforce sequence when needed.
2. **Error Boundaries**: Use fail-branch on critical nodes to prevent workflow abortion
3. **Merge Points**: Always use variable-aggregator to merge branches before convergence
4. **Loop Safety**: Set reasonable `loop_count` limits and clear break conditions
5. **Human Input**: Plan for paused state when using human-input nodes

## Resources

### scripts/
- `generate_id.py` - Generate unique node IDs for workflows
- `validate_workflow.py` - Validate workflow DSL syntax (requires PyYAML)

### references/
- `node_types.md` - Complete reference of all Dify node types with examples
- `workflow_structure.md` - Detailed DSL structure and format specification

### assets/
- `simple_llm_workflow.yml` - Basic start→LLM→end template
- `error_handling_workflow.yml` - Template with fail-branch error handling
- `conditional_workflow.yml` - Template with if-else branching

## Tips for Success

1. **Start simple**: Begin with basic flows, add complexity incrementally
2. **Use templates**: Adapt existing templates rather than starting from scratch
3. **Validate early**: Check structure before adding many nodes
4. **Plan error handling**: Consider what can fail and how to handle it
5. **Name clearly**: Use descriptive node titles for maintainability
6. **Reference docs**: Consult node_types.md for field requirements
7. **Test incrementally**: Build and test workflows step by step
