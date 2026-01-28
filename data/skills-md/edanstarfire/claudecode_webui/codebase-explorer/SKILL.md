---
name: codebase-explorer
description: Identify relevant files, understand architecture patterns, and find code by functionality. Use when you need to understand where specific functionality lives or find files related to a feature area.
---

# Codebase Explorer

## Instructions

### When to Invoke This Skill
- Need to find where specific functionality is implemented
- Understanding codebase structure before making changes
- Locating files related to a feature or bug
- Discovering architectural patterns in the project
- Finding examples of similar functionality
- Understanding dependencies between components

### Exploration Strategies

#### 1. Top-Down Exploration (Start Broad)

**Use when:** You know the general area but not specific files.

**Approach:**
1. Start with project structure overview
2. Identify likely directories
3. Find entry points
4. Trace execution flow

#### 2. Bottom-Up Exploration (Start Specific)

**Use when:** You know specific terms, functions, or classes.

**Approach:**
1. Search for specific strings
2. Find definitions
3. Trace usages
4. Understand context

#### 3. Pattern-Based Exploration

**Use when:** Looking for similar implementations.

**Approach:**
1. Find one example
2. Search for similar patterns
3. Identify conventions
4. Apply understanding

### Tools and Techniques

#### Using Glob to Find Files

**Find by pattern:**
```bash
# All Python files
**/*.py

# All Vue components
frontend/src/components/**/*.vue

# All test files
**/test_*.py
src/tests/**/*.py

# Specific area
src/legion/**/*.py

# Configuration files
**/*.json
**/*.md
```

**Find entry points:**
```bash
# Main entry
main.py
**/main.py

# Server files
**/server.py
**/*_server.py

# Index files
**/index.html
**/index.js
```

#### Using Grep to Search Code

**Find function definitions:**
```bash
# Python functions
def <function_name>

# Python classes
class <ClassName>

# JavaScript/TypeScript functions
function <functionName>
const <functionName> =

# Vue components
export default {
```

**Find usages:**
```bash
# Where is function called?
<function_name>(

# Where is class instantiated?
<ClassName>(

# Where is import used?
from .* import .*<name>
import .* from
```

**Find by functionality:**
```bash
# WebSocket code
websocket
WebSocket

# Database operations
SELECT |INSERT |UPDATE |DELETE

# API endpoints
@app\.route|@router\.(get|post|put|delete)

# Error handling
try:|except |raise |throw
```

**Find configuration:**
```bash
# Environment variables
os\.environ|process\.env

# Configuration files
config|settings|\.env
```

### Exploration Workflows

#### Workflow 1: Finding Feature Implementation

**Goal:** Find where user authentication is implemented.

**Steps:**
1. **Search for keywords:**
   ```bash
   grep -r "auth" --include="*.py"
   grep -r "login" --include="*.py"
   ```

2. **Find files:**
   ```bash
   **/*auth*.py
   **/*login*.py
   ```

3. **Read relevant files:**
   - Look for class/function definitions
   - Identify main entry points
   - Trace dependencies

4. **Find usages:**
   ```bash
   grep "authenticate(" **/*.py
   grep "login(" **/*.py
   ```

5. **Understand flow:**
   - API endpoint → Business logic → Data layer
   - Frontend → API → Backend

#### Workflow 2: Understanding Architecture

**Goal:** Understand how sessions work.

**Steps:**
1. **Find session-related files:**
   ```bash
   **/*session*.py
   ```

2. **Read main files:**
   - Start with core classes (SessionManager, etc.)
   - Understand data structures
   - Identify key methods

3. **Find related components:**
   ```bash
   grep "SessionManager" **/*.py
   grep "session_id" **/*.py
   ```

4. **Trace data flow:**
   - How sessions are created
   - Where session state is stored
   - How sessions are accessed

5. **Map dependencies:**
   - What does session management depend on?
   - What depends on session management?

#### Workflow 3: Finding Similar Implementation

**Goal:** Want to add new API endpoint, find examples.

**Steps:**
1. **Find API endpoint definitions:**
   ```bash
   grep "@app\.route\|@router\.(get|post)" **/*.py
   ```

2. **Read example endpoint:**
   - Understand parameter handling
   - See error handling pattern
   - Note response format

3. **Find related patterns:**
   ```bash
   grep "jsonify\|JSONResponse" **/*.py
   ```

4. **Identify conventions:**
   - Request validation approach
   - Error response format
   - Success response format

#### Workflow 4: Debugging Error Location

**Goal:** Error mentions "WebSocketManager", find where it's defined.

**Steps:**
1. **Find class definition:**
   ```bash
   grep "class WebSocketManager" **/*.py
   ```

2. **Read the class:**
   - Understand responsibilities
   - Note key methods
   - See error handling

3. **Find usages:**
   ```bash
   grep "WebSocketManager(" **/*.py
   ```

4. **Trace error path:**
   - Where is error raised?
   - What triggers it?
   - How to fix?

### Understanding Project Structure

#### Typical Python Backend Structure
```
src/
├── web_server.py          # HTTP server, API endpoints
├── session_coordinator.py  # Orchestration, coordination
├── session_manager.py      # Session lifecycle
├── project_manager.py      # Project management
├── claude_sdk.py          # SDK wrapper
├── message_parser.py      # Message processing
├── data_storage.py        # Persistence
└── tests/                 # Unit tests
    ├── test_*.py
    └── conftest.py
```

#### Typical Frontend Structure
```
frontend/src/
├── components/            # Vue components
│   ├── layout/           # Layout components
│   ├── session/          # Session-related
│   └── messages/         # Message display
├── stores/               # Pinia state management
├── router/               # Vue Router config
├── composables/          # Reusable composition functions
└── utils/                # Helper functions
```

### Reading Code Effectively

#### 1. Start with Entry Points

**Backend:**
- `main.py` - Application entry
- `web_server.py` - API endpoints
- Route handlers - Request processing

**Frontend:**
- `index.html` - HTML entry
- `main.js` - JavaScript entry
- `App.vue` - Root component
- `router/index.js` - Route definitions

#### 2. Follow the Flow

**Request Flow (Backend):**
```
API Endpoint
   ↓
Request Validation
   ↓
Business Logic (Manager/Coordinator)
   ↓
Data Layer (Storage)
   ↓
Response Formation
```

**Component Flow (Frontend):**
```
User Action
   ↓
Component Event Handler
   ↓
Store Action
   ↓
API Call (or Local State Update)
   ↓
Store State Update
   ↓
Reactive UI Update
```

#### 3. Identify Patterns

**Common Patterns to Recognize:**
- Factory pattern (create objects)
- Observer pattern (event handling)
- Repository pattern (data access)
- Coordinator pattern (orchestration)
- Component composition (UI building)

#### 4. Understand Dependencies

**Import Statements Tell Story:**
```python
from .session_manager import SessionManager
from .project_manager import ProjectManager
from .claude_sdk import ClaudeSDK
```
This file coordinates multiple managers.

**Circular Dependencies:**
If A imports B and B imports A, there's likely architectural issue.

### Common Codebase Questions

**"Where is X implemented?"**
→ Search for class/function definition: `grep "def X\|class X"`

**"How is X used?"**
→ Search for usages: `grep "X("`

**"What files handle Y functionality?"**
→ Search for keywords: `grep -r "keyword" --include="*.py"`

**"What are the API endpoints?"**
→ Search for route decorators: `grep "@app\.route\|@router\."`

**"Where is data stored?"**
→ Find storage classes, look for file I/O operations

**"How do frontend and backend communicate?"**
→ Find API calls in frontend, match to endpoints in backend

## Examples

### Example 1: Find session creation logic
```
1. Search for "create_session"
   grep "def create_session" **/*.py

2. Found in: src/session_coordinator.py and src/session_manager.py

3. Read SessionCoordinator.create_session():
   - Calls SessionManager to create session entity
   - Initializes data storage
   - Sets up SDK instance

4. Understand flow:
   API (web_server.py) → SessionCoordinator → SessionManager → DataStorage
```

### Example 2: Find Vue component for session list
```
1. Find session-related components:
   frontend/src/components/session/**/*.vue

2. Look for list-related:
   SessionList.vue, SessionItem.vue

3. Read SessionList.vue:
   - Uses Pinia session store
   - Renders SessionItem for each session
   - Handles selection

4. Check store:
   frontend/src/stores/session.js
   - Sessions stored in Map
   - CRUD operations defined
```

### Example 3: Understand WebSocket message handling
```
1. Find WebSocket code:
   grep "websocket\|WebSocket" **/*.py

2. Found: src/web_server.py has WebSocketManager classes

3. Read WebSocketManager:
   - Manages connections
   - Routes messages
   - Broadcasts updates

4. Find message handlers:
   grep "handle.*message" src/web_server.py

5. Trace message flow:
   WebSocket → Handler → Store/Coordinator → Response
```

### Example 4: Find how permissions work
```
1. Search for permission-related code:
   grep -r "permission" **/*.py

2. Found in:
   - src/session_coordinator.py (permission mode)
   - src/web_server.py (permission callbacks)
   - src/session_manager.py (permission state)

3. Read web_server.py _create_permission_callback():
   - Creates asyncio.Future
   - Sends permission request to frontend
   - Waits for user response
   - Returns decision to SDK

4. Understand flow:
   SDK needs permission → Callback → WebSocket to frontend →
   User decides → WebSocket from frontend → Future resolved →
   SDK receives decision
```
