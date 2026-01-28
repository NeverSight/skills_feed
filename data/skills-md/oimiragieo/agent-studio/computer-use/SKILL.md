---
name: computer-use
description: Claude Computer Use tool integration for desktop automation. Enables Claude to interact with computer environments through screenshots, mouse control, keyboard input, and application automation in sandboxed environments.
version: 1.0
model: opus
invoked_by: both
user_invocable: true
tools: [Read, Write, Bash, WebFetch]
args: '<action> [options]'
best_practices:
  - Always run in sandboxed environment (Docker/VM)
  - Use coordinate scaling for different resolutions
  - Implement human confirmation for meaningful actions
  - Protect against prompt injection in screenshots
  - Limit internet access in automation environment
error_handling: graceful
streaming: supported
safety_level: critical
---

# Computer Use Skill

<identity>
Desktop automation specialist that enables Claude to interact with computer environments through the Anthropic Computer Use tool API, providing screenshot capture, mouse control, keyboard input, and application automation capabilities.
</identity>

<capabilities>
- Configure Computer Use tool with proper display settings
- Execute agent loops for multi-step desktop automation
- Handle coordinate scaling for different screen resolutions
- Implement security best practices for sandboxed execution
- Process screenshots and determine next actions
- Execute mouse actions (click, drag, scroll, move)
- Execute keyboard actions (type, key combinations)
- Wait for UI elements and screen changes
</capabilities>

<instructions>
<execution_process>

### Step 1: Environment Setup

Before using Computer Use, ensure proper sandboxed environment:

1. **Docker Container** (Recommended):

   ```bash
   # Use Anthropic's reference container
   docker run -it --rm \
     -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
     -p 5900:5900 -p 8501:8501 \
     ghcr.io/anthropics/anthropic-quickstarts:computer-use-demo-latest
   ```

2. **Virtual Machine**: Dedicated VM with minimal privileges and isolated network

3. **Never run on host machine** with access to sensitive data or credentials

### Step 2: Tool Configuration

Configure the computer use tool with display settings:

```javascript
const computerTool = {
  type: 'computer_20250124', // or "computer_20251124" for Opus 4.5
  name: 'computer',
  display_width_px: 1024,
  display_height_px: 768,
  display_number: 1,
};
```

**Resolution Guidelines**:

- XGA (1024x768): Default, works well for most tasks
- WXGA (1280x800): Better for wide content
- 1920x1080: Only if needed, may reduce accuracy

### Step 3: Agent Loop Implementation

The core pattern for computer use is an agent loop:

```javascript
async function computerUseAgentLoop(task, maxIterations = 50) {
  const messages = [{ role: 'user', content: task }];

  for (let i = 0; i < maxIterations; i++) {
    // 1. Call Claude with computer tool
    const response = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 4096,
      tools: [computerTool],
      messages,
      betas: ['computer-use-2025-01-24'],
    });

    // 2. Check if task complete
    if (response.stop_reason === 'end_turn') {
      return extractFinalResult(response);
    }

    // 3. Process tool use requests
    const toolResults = [];
    for (const block of response.content) {
      if (block.type === 'tool_use' && block.name === 'computer') {
        const result = await executeComputerAction(block.input);
        toolResults.push({
          type: 'tool_result',
          tool_use_id: block.id,
          content: result,
        });
      }
    }

    // 4. Add assistant response and tool results
    messages.push({ role: 'assistant', content: response.content });
    messages.push({ role: 'user', content: toolResults });
  }

  throw new Error('Max iterations reached');
}
```

### Step 4: Action Execution

Execute computer actions based on Claude's requests:

```javascript
async function executeComputerAction(input) {
  const { action, coordinate, text, scroll_direction, scroll_amount } = input;

  switch (action) {
    case 'screenshot':
      return await captureScreenshot();

    case 'left_click':
      await click(coordinate[0], coordinate[1]);
      return await captureScreenshot();

    case 'type':
      await typeText(text);
      return await captureScreenshot();

    case 'key':
      await pressKey(text);
      return await captureScreenshot();

    case 'mouse_move':
      await moveMouse(coordinate[0], coordinate[1]);
      return await captureScreenshot();

    case 'scroll':
      await scroll(coordinate, scroll_direction, scroll_amount);
      return await captureScreenshot();

    case 'left_click_drag':
      await drag(input.start_coordinate, coordinate);
      return await captureScreenshot();

    case 'wait':
      await sleep(input.duration * 1000);
      return await captureScreenshot();

    default:
      throw new Error(`Unknown action: ${action}`);
  }
}
```

### Step 5: Coordinate Scaling

When display resolution differs from tool configuration:

```javascript
function scaleCoordinates(x, y, fromWidth, fromHeight, toWidth, toHeight) {
  return [Math.round((x * toWidth) / fromWidth), Math.round((y * toHeight) / fromHeight)];
}

// Example: Scale from 1024x768 to actual 1920x1080
const [scaledX, scaledY] = scaleCoordinates(
  500,
  400, // Claude's coordinates
  1024,
  768, // Tool configuration
  1920,
  1080 // Actual display
);
```

</execution_process>

<best_practices>

1. **Sandboxed Execution**: ALWAYS run in Docker container or VM with minimal privileges. Never grant access to sensitive data, authentication credentials, or unrestricted internet.

2. **Human Confirmation**: Implement human-in-the-loop confirmation for meaningful actions like form submissions, file deletions, or external communications.

3. **Prompt Injection Protection**: Be aware that malicious content in screenshots can attempt to manipulate Claude. Validate actions against the original task.

4. **Resolution Consistency**: Keep display resolution consistent throughout a session. XGA (1024x768) provides best balance of accuracy and visibility.

5. **Screenshot After Actions**: Always return a screenshot after each action so Claude can verify the result and determine next steps.

6. **Error Recovery**: Implement graceful error handling. If an action fails, capture screenshot and let Claude decide how to proceed.

7. **Rate Limiting**: Add delays between rapid actions to allow UI to update. Use the `wait` action when needed.

8. **Beta Headers**: Always include the appropriate beta header for your model version.

</best_practices>
</instructions>

<examples>

<code_example>
**Complete Agent Loop Example (Node.js)**

```javascript
const Anthropic = require('@anthropic-ai/sdk');

const anthropic = new Anthropic();

// Tool configuration
const computerTool = {
  type: 'computer_20250124',
  name: 'computer',
  display_width_px: 1024,
  display_height_px: 768,
  display_number: 1,
};

// Main agent loop
async function runComputerUseTask(task) {
  console.log(`Starting task: ${task}`);

  const messages = [{ role: 'user', content: task }];
  let iterations = 0;
  const maxIterations = 50;

  while (iterations < maxIterations) {
    iterations++;
    console.log(`Iteration ${iterations}`);

    const response = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 4096,
      tools: [computerTool],
      messages,
      betas: ['computer-use-2025-01-24'],
    });

    // Check for completion
    if (response.stop_reason === 'end_turn') {
      const textBlocks = response.content.filter(b => b.type === 'text');
      return textBlocks.map(b => b.text).join('\n');
    }

    // Process tool calls
    const toolResults = [];
    for (const block of response.content) {
      if (block.type === 'tool_use' && block.name === 'computer') {
        console.log(`Action: ${block.input.action}`);

        // Execute action and get screenshot
        const screenshot = await executeAction(block.input);

        toolResults.push({
          type: 'tool_result',
          tool_use_id: block.id,
          content: [
            {
              type: 'image',
              source: {
                type: 'base64',
                media_type: 'image/png',
                data: screenshot,
              },
            },
          ],
        });
      }
    }

    messages.push({ role: 'assistant', content: response.content });
    messages.push({ role: 'user', content: toolResults });
  }

  throw new Error('Task did not complete within iteration limit');
}

// Example usage
runComputerUseTask('Open the calculator app and compute 25 * 47')
  .then(result => console.log('Result:', result))
  .catch(err => console.error('Error:', err));
```

</code_example>

<code_example>
**Python Implementation**

```python
import anthropic
import base64
from typing import Any

client = anthropic.Anthropic()

COMPUTER_TOOL = {
    "type": "computer_20250124",
    "name": "computer",
    "display_width_px": 1024,
    "display_height_px": 768,
    "display_number": 1
}

def run_computer_use_task(task: str, max_iterations: int = 50) -> str:
    """Execute a computer use task with agent loop."""
    messages = [{"role": "user", "content": task}]

    for iteration in range(max_iterations):
        print(f"Iteration {iteration + 1}")

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            tools=[COMPUTER_TOOL],
            messages=messages,
            betas=["computer-use-2025-01-24"]
        )

        # Check for completion
        if response.stop_reason == "end_turn":
            text_blocks = [b.text for b in response.content if b.type == "text"]
            return "\n".join(text_blocks)

        # Process tool calls
        tool_results = []
        for block in response.content:
            if block.type == "tool_use" and block.name == "computer":
                print(f"Action: {block.input['action']}")

                # Execute action in your environment
                screenshot_b64 = execute_action(block.input)

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": [{
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": screenshot_b64
                        }
                    }]
                })

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

    raise Exception("Max iterations reached")


def execute_action(action_input: dict[str, Any]) -> str:
    """Execute computer action and return screenshot as base64."""
    action = action_input["action"]

    # Implement using your automation framework
    # (pyautogui, pynput, or container-specific tools)

    if action == "screenshot":
        pass  # Just capture
    elif action == "left_click":
        x, y = action_input["coordinate"]
        # click(x, y)
    elif action == "type":
        text = action_input["text"]
        # type_text(text)
    elif action == "key":
        key = action_input["text"]
        # press_key(key)
    # ... handle other actions

    # Capture and return screenshot
    return capture_screenshot_base64()
```

</code_example>

<usage_example>
**Available Actions Reference**

```javascript
// Basic actions (all versions)
{ "action": "screenshot" }
{ "action": "left_click", "coordinate": [500, 300] }
{ "action": "type", "text": "Hello, world!" }
{ "action": "key", "text": "ctrl+s" }
{ "action": "mouse_move", "coordinate": [500, 300] }

// Enhanced actions (computer_20250124)
{ "action": "scroll", "coordinate": [500, 400], "scroll_direction": "down", "scroll_amount": 3 }
{ "action": "left_click_drag", "start_coordinate": [100, 100], "coordinate": [300, 300] }
{ "action": "right_click", "coordinate": [500, 300] }
{ "action": "middle_click", "coordinate": [500, 300] }
{ "action": "double_click", "coordinate": [500, 300] }
{ "action": "triple_click", "coordinate": [500, 300] }
{ "action": "left_mouse_down", "coordinate": [500, 300] }
{ "action": "left_mouse_up", "coordinate": [500, 300] }
{ "action": "hold_key", "text": "shift", "duration": 1.0 }
{ "action": "wait", "duration": 2.0 }

// Opus 4.5 only (computer_20251124 with enable_zoom: true)
{ "action": "zoom", "coordinate": [500, 300], "zoom_direction": "in", "zoom_amount": 2 }
```

</usage_example>

<usage_example>
**Docker Reference Container**

```bash
# Pull and run the Anthropic reference container
docker pull ghcr.io/anthropics/anthropic-quickstarts:computer-use-demo-latest

# Run with API key
docker run -it --rm \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  -v $(pwd)/output:/home/computeruse/output \
  -p 5900:5900 \
  -p 8501:8501 \
  -p 6080:6080 \
  -p 8080:8080 \
  ghcr.io/anthropics/anthropic-quickstarts:computer-use-demo-latest

# Access points:
# - VNC: localhost:5900 (password: "secret")
# - noVNC web: http://localhost:6080/vnc.html
# - Streamlit UI: http://localhost:8501
# - API: http://localhost:8080
```

</usage_example>

</examples>

## Tool Versions

| Version             | Beta Header               | Model Support | Key Features                                |
| ------------------- | ------------------------- | ------------- | ------------------------------------------- |
| `computer_20250124` | `computer-use-2025-01-24` | Sonnet, Haiku | Enhanced actions (scroll, drag, wait, etc.) |
| `computer_20251124` | `computer-use-2025-11-24` | Opus 4.5 only | Zoom action (requires `enable_zoom: true`)  |

## Security Requirements

### CRITICAL: Sandboxing is Mandatory

Computer Use provides direct control over a computer environment. **NEVER** run without proper sandboxing:

1. **Use dedicated containers/VMs** - Never on host machines with sensitive data
2. **Minimal privileges** - No root access, limited filesystem access
3. **Network isolation** - Restrict or block internet access
4. **No credentials** - Never expose API keys, passwords, or tokens in the environment
5. **Human oversight** - Require confirmation for destructive or external actions

### Prompt Injection Risks

Malicious content displayed on screen can attempt to manipulate Claude:

- Validate that actions align with the original task
- Implement allowlists for permitted applications/websites
- Monitor for suspicious instruction patterns in screenshots

## Error Handling

| Error                   | Cause               | Resolution                               |
| ----------------------- | ------------------- | ---------------------------------------- |
| `invalid_request_error` | Missing beta header | Add `betas: ["computer-use-2025-01-24"]` |
| `tool_use_error`        | Invalid coordinates | Ensure coordinates within display bounds |
| `rate_limit_error`      | Too many requests   | Implement exponential backoff            |
| Action has no effect    | UI not ready        | Add `wait` action before retrying        |
| Wrong element clicked   | Coordinate drift    | Re-capture screenshot and recalculate    |

## Integration with Agents

### Primary Agents

- **developer**: Automated testing, UI verification
- **qa**: End-to-end testing, visual regression
- **devops-troubleshooter**: System debugging, log inspection

### Use Cases

- Automated form filling and data entry
- Application testing and QA automation
- Desktop application interaction
- Browser automation (when headless won't work)
- Legacy system integration
- Visual verification and screenshots

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

Check for:

- Previous computer use configurations
- Known automation patterns
- Environment-specific settings

**After completing:**

- New pattern discovered -> `.claude/context/memory/learnings.md`
- Security concern found -> `.claude/context/memory/issues.md`
- Architecture decision -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.

## Related

- **Anthropic Documentation**: https://docs.anthropic.com/en/docs/build-with-claude/computer-use
- **Reference Implementation**: https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo
- **API Reference**: https://docs.anthropic.com/en/api/computer-use
