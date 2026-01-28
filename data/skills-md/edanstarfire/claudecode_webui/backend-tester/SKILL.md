---
name: backend-tester
description: Run isolated test environments for backend changes, manage test data, and verify API endpoints. Use when testing Python backend changes without interfering with production instances.
---

# Backend Tester

## Instructions

### When to Invoke This Skill
- Testing changes to Python backend code
- Verifying API endpoint functionality
- Testing session/project management logic
- Debugging SDK integration or message processing
- Testing bug fixes that need verification
- Any backend business logic changes

### Testing Environment

**CRITICAL**: Always use isolated test environment to avoid conflicts with user's production instance.

**Test Configuration:**
- **Port**: 8001 (production uses 8000)
- **Data Directory**: `test_data/` (production uses `data/`)
- **Debug Flags**: `--debug-all` for full logging

### Standard Workflows

#### Automated API Testing (Preferred)

Use for testing API endpoints without UI interaction.

**1. Start Test Server**
```bash
uv run python main.py --debug-all --data-dir test_data --port 8001
```

**2. Run Test Commands**
Use `curl` or Python `requests` to test endpoints:

```bash
# Create project
curl -X POST http://localhost:8001/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Project", "working_directory": "/tmp/test"}'

# Create session
curl -X POST http://localhost:8001/api/sessions \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Session", "project_id": "<project_id>"}'

# Get sessions
curl http://localhost:8001/api/sessions

# Start session
curl -X POST http://localhost:8001/api/sessions/<session_id>/start
```

**3. Verify Responses**
- Check HTTP status codes
- Validate response JSON structure
- Verify expected data returned
- Check error messages for error cases

**4. Stop Server**
```bash
# Press Ctrl+C to stop server
```

**5. Review Logs**
Check `test_data/logs/` for detailed debugging:
- `error.log` - All errors
- `coordinator.log` - Session coordination
- `storage.log` - File operations
- `sdk_debug.log` - SDK integration
- `websocket_debug.log` - WebSocket lifecycle

**6. Clean Up**
```bash
# Remove test data (optional)
rm -rf test_data/
```

#### Manual Testing with UI

Use when user needs to interact with frontend.

**1. Start Test Server in Background**

**Invoke the `process-manager` skill** to safely manage the test server:
- Start server: `uv run python main.py --debug-all --data-dir test_data --port 8001`
- Track process by PID
- Inform user: "Test server running on http://localhost:8001 - please test the changes"

**2. Wait for User Confirmation**
User tests functionality in browser at http://localhost:8001

**3. Stop Test Server**

**Invoke the `process-manager` skill** to safely terminate:
- Stop server by PID (never by name/pattern)
- Verify cleanup
- Confirm port 8001 is free

**CRITICAL**: Always delegate process management to the skill to avoid killing production servers.

### Testing Strategies

#### Testing API Endpoints

**Create Operation:**
```bash
# Test creation
curl -X POST http://localhost:8001/api/<resource> -H "Content-Type: application/json" -d '{...}'

# Verify creation
curl http://localhost:8001/api/<resource>
```

**Read Operation:**
```bash
# Get list
curl http://localhost:8001/api/<resources>

# Get specific item
curl http://localhost:8001/api/<resources>/<id>
```

**Update Operation:**
```bash
# Update item
curl -X PUT http://localhost:8001/api/<resources>/<id> -H "Content-Type: application/json" -d '{...}'

# Verify update
curl http://localhost:8001/api/<resources>/<id>
```

**Delete Operation:**
```bash
# Delete item
curl -X DELETE http://localhost:8001/api/<resources>/<id>

# Verify deletion
curl http://localhost:8001/api/<resources>/<id>
# Should return 404
```

#### Testing Error Cases

Test validation:
```bash
# Missing required field
curl -X POST http://localhost:8001/api/<resource> -H "Content-Type: application/json" -d '{}'
# Should return 400

# Invalid data type
curl -X POST http://localhost:8001/api/<resource> -H "Content-Type: application/json" -d '{"id": "not-a-uuid"}'
# Should return 400

# Non-existent resource
curl http://localhost:8001/api/<resources>/nonexistent-id
# Should return 404
```

#### Testing Session Lifecycle

Complete session workflow:
```bash
# 1. Create project
PROJECT=$(curl -X POST http://localhost:8001/api/projects -H "Content-Type: application/json" -d '{"name":"Test","working_directory":"/tmp"}' | jq -r '.project_id')

# 2. Create session
SESSION=$(curl -X POST http://localhost:8001/api/sessions -H "Content-Type: application/json" -d "{\"project_id\":\"$PROJECT\",\"name\":\"Test Session\"}" | jq -r '.session_id')

# 3. Start session
curl -X POST http://localhost:8001/api/sessions/$SESSION/start

# 4. Send message
curl -X POST http://localhost:8001/api/sessions/$SESSION/messages -H "Content-Type: application/json" -d '{"content":"Hello"}'

# 5. Get messages
curl "http://localhost:8001/api/sessions/$SESSION/messages?limit=50&offset=0"

# 6. Pause session
curl -X POST http://localhost:8001/api/sessions/$SESSION/pause

# 7. Terminate session
curl -X POST http://localhost:8001/api/sessions/$SESSION/terminate

# 8. Clean up
curl -X DELETE http://localhost:8001/api/sessions/$SESSION
curl -X DELETE http://localhost:8001/api/projects/$PROJECT
```

### When to Use Each Approach

**Automated Testing (curl/requests):**
- Testing API logic and responses
- Regression testing after changes
- Testing error handling
- Quick verification of endpoints
- CI/CD integration (future)

**Manual Testing (browser):**
- Testing UI interactions
- WebSocket functionality
- Visual verification
- User flow testing
- Complex multi-step scenarios

**Unit Tests (pytest):**
- Testing individual functions
- Testing business logic
- Testing data models
- Mocking external dependencies

### Test Data Management

**Test Data Location:**
```
test_data/
├── logs/                    # Test run logs
├── projects/                # Test projects
└── sessions/                # Test sessions
```

**Cleaning Up:**
```bash
# Remove all test data
rm -rf test_data/

# Remove just logs
rm -rf test_data/logs/

# Remove specific session
rm -rf test_data/sessions/<session-id>/
```

**Persistent Test Data:**
Sometimes useful to keep test data for debugging:
- Comment out cleanup step
- Rerun tests against same data
- Inspect files directly

## Examples

### Example 1: Test new API endpoint
```
Context: Added new endpoint POST /api/sessions/<id>/reset

Test:
1. Start server: uv run python main.py --debug-all --data-dir test_data --port 8001
2. Create test session
3. Test endpoint: curl -X POST http://localhost:8001/api/sessions/<id>/reset
4. Verify: curl http://localhost:8001/api/sessions/<id>/messages (should be empty)
5. Stop server: Ctrl+C
6. Clean up: rm -rf test_data/
```

### Example 2: Test bug fix with UI
```
Context: Fixed WebSocket reconnection issue

Test:
1. Invoke process-manager skill to start server in background
2. Server runs on port 8001 with test_data/
3. Inform user: "Test at http://localhost:8001"
4. User tests reconnection scenario
5. User confirms: "Works now"
6. Invoke process-manager skill to stop server by PID
7. Verify cleanup successful
```

### Example 3: Automated regression test
```
Context: Need to verify session CRUD operations still work

Test Script:
1. Start server
2. Create project, verify response
3. Create session, verify response
4. Update session name, verify
5. Delete session, verify 404 on next get
6. Delete project, verify 404 on next get
7. Stop server
8. Check logs for errors
9. Clean up test_data/
```
