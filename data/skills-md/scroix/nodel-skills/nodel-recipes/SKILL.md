---
name: nodel-recipes
description: Write Nodel node recipes (script.py) using Jython 2.5 - define actions, events, parameters, TCP/UDP/HTTP protocols, and device control logic. Use when creating or modifying Nodel scripts.
---

# Nodel Recipe Development

## Critical: Jython 2.5 Syntax

Node scripts execute under Jython 2.5.4. You MUST use Python 2.5-era syntax:

```python
# CORRECT - Python 2.5 syntax
except Exception, e:
    console.error('Error: %s' % e)

# WRONG - Python 3 syntax (will fail)
except Exception as e:
    console.error(f'Error: {e}')
```

See `references/jython-syntax.md` for complete syntax reference.

## Recipe File Structure

A node recipe lives in a folder containing:
- `script.py` - Main recipe logic (required)
- `content/index.xml` - Custom frontend definition (optional)
- `content/css/custom.css` - Custom styles (optional)
- `content/js/custom.js` - Custom JavaScript (optional)

## Core Concepts

### Parameters

Configure node behavior via the web interface:

```python
param_ipAddress = Parameter({'title': 'IP Address', 'schema': {'type': 'string'}})
param_port = Parameter({'title': 'Port', 'schema': {'type': 'integer'}, 'default': 9999})
```

### Local Actions

Commands this node exposes (can be triggered by bindings or REST API):

```python
@local_action({'schema': {'type': 'string', 'enum': ['On', 'Off']}})
def power(arg):
    '''{"group": "Power", "order": 1}'''
    tcp.send('POWER %s\r\n' % arg)
```

Alternative pattern:
- Naming convention also works: `def local_action_PowerOn(arg=None): ...`

### Local Events

State this node emits (can be bound by other nodes):

```python
local_event_Status = LocalEvent({'schema': {'type': 'object'}})

# Emit when state changes
local_event_Status.emit({'power': 'On', 'volume': 50})
```

### Remote Bindings

Connect to other nodes:

```python
# Call actions on other nodes
remote_action_DisplayPower = RemoteAction()
remote_action_DisplayPower.call('On')

# Receive events from other nodes
def remote_event_DisplayStatus(arg):
    console.info('Display status: %s' % arg)
```

## Lifecycle Functions

```python
def main():
    '''Called when node starts. Set up initial state.'''
    console.info('Node starting...')

@after_main
def setup():
    '''Called after main() and parameter loading. Configure connections.'''
    tcp.setDest('%s:%s' % (param_ipAddress, param_port))

@at_cleanup
def cleanup():
    '''Called when node shuts down. Clean up resources.'''
    tcp.close()
```

## Network Protocols

TCP, UDP, and HTTP are available via the toolkit. See `references/toolkit-api.md` for complete documentation with examples.

## Timers

```python
# Repeating timer (poll every 30 seconds)
Timer(poll_status, 30)

# One-time delayed call
call(setup_connection, 5)

# Stoppable timer
status_timer = Timer(check_status, 60, stopped=True)
status_timer.start()
status_timer.stop()
```

## Console Logging

```python
console.log("Light gray - verbose/debug")
console.info("Blue - informational")
console.warn("Orange - warning")
console.error("Red - error")
```

## Common Patterns

### Device Control with Polling

```python
def poll_status():
    tcp.send('STATUS?\r\n')

Timer(poll_status, 30)

def tcp_received(data):
    if 'POWER=' in data:
        local_event_Status.emit({'power': data.split('=')[1]})
```

### Status Monitoring

```python
local_event_Status = LocalEvent({'schema': {'type': 'object', 'properties': {
    'level': {'type': 'integer'},
    'message': {'type': 'string'}
}}})

_lastReceive = 0

def statusCheck():
    diff = (system_clock() - _lastReceive) / 1000.0
    if diff > 90:
        local_event_Status.emit({'level': 2, 'message': 'No response'})
    else:
        local_event_Status.emit({'level': 0, 'message': 'OK'})

Timer(statusCheck, 60)
```

### Dynamic Action Creation

```python
def build_presets():
    for preset in PRESET_NAMES:
        create_local_action('Preset %s' % preset,
            lambda arg, p=preset: activate_preset(p),
            {'group': 'Presets', 'schema': {'type': 'null'}})
```

## Error Handling

```python
@local_action({})
def riskyOperation(arg):
    try:
        result = perform_operation(arg)
        local_event_Success.emit(result)
    except Exception, e:
        console.error('Operation failed: %s' % e)
        local_event_Error.emit(str(e))
```

## Development Philosophy

- **Simplicity First** - Keep code minimal and readable
- **Maintainability > Cleverness** - Prefer explicit over implicit
- **DRY** - Extract common patterns to helper functions
- **Defensive Coding** - Handle network failures gracefully
