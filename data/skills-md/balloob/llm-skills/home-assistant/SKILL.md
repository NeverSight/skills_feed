---
name: home-assistant
description: Use this if the user wants to connect to Home Assistant or leverage Home Assistant in any shape or form inside their project. Guide users integrating Home Assistant into projects for home automation control or data ingestion. Collects and validates connection credentials (URL and Long-Lived Access Token), provides API reference documentation for Python and Node.js implementations, and helps integrate Home Assistant APIs into user projects.
---

# Home Assistant

## Overview

This skill helps users integrate Home Assistant into their projects, whether to control smart home devices or to ingest sensor data and state information. The skill guides users through connection setup, validates credentials, and provides comprehensive API reference documentation for both Python and Node.js.

## When to Use This Skill

Use this skill when users want to:
- Connect their application to Home Assistant
- Control smart home devices (lights, switches, thermostats, etc.)
- Read sensor data or entity states from Home Assistant
- Automate home control based on custom logic
- Build dashboards or monitoring tools using Home Assistant data
- Integrate Home Assistant into existing Python or Node.js projects

## Connection Setup Workflow

### Step 1: Collect Connection Information

Collect two pieces of information from the user:

1. **Home Assistant URL**: The web address where Home Assistant is accessible
2. **Long-Lived Access Token**: Authentication token for API access

### Step 2: Normalize the URL

If the user provides a URL with a path component (e.g., `http://homeassistant.local:8123/lovelace/dashboard`), normalize it by removing everything after the host and port. The base URL should only include the scheme, host, and port:

- ✓ Correct: `http://homeassistant.local:8123`
- ✗ Incorrect: `http://homeassistant.local:8123/lovelace/dashboard`

### Step 3: Help Users Find Their Token

If users don't know where to find their Long-Lived Access Token, provide these instructions:

1. Log into Home Assistant web interface
2. Click on the user profile (bottom left, user icon or name)
3. Click on the "Security" tab
4. Scroll down to the "Long-Lived Access Tokens" section
5. Click "Create Token"
6. Give the token a name (e.g., "My Project")
7. Copy the generated token (it will only be shown once)

### Step 4: Validate the Connection

Use curl to test the connection and retrieve Home Assistant configuration information.

```bash
curl -X GET \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  <URL>/api/config
```

Example:
```bash
curl -X GET \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  http://homeassistant.local:8123/api/config
```

**Success output:**
```json
{
  "location_name": "Home",
  "latitude": 37.7749,
  "longitude": -122.4194,
  "elevation": 0,
  "unit_system": {
    "length": "km",
    "mass": "g",
    "temperature": "°C",
    "volume": "L"
  },
  "time_zone": "America/Los_Angeles",
  "version": "2024.1.0",
  "config_dir": "/config",
  "allowlist_external_dirs": [],
  "allowlist_external_urls": [],
  "components": ["automation", "light", "switch", ...],
  "config_source": "storage"
}
```

**Key information from the response:**
- `version`: Home Assistant version (e.g., "2024.1.0")
- `location_name`: Name of the Home Assistant instance
- `time_zone`: Configured time zone
- `components`: List of loaded components/integrations

**Failure scenarios:**

Authentication failure (401):
```json
{"message": "Invalid authentication"}
```

Connection failure:
```
curl: (7) Failed to connect to homeassistant.local port 8123: Connection refused
```

If authentication fails, verify:
1. The Long-Lived Access Token is correct
2. The token hasn't been deleted or expired
3. The URL is correct (including http/https and port)

### Step 5: Proceed with Implementation

Once the connection is validated, help the user implement their integration based on their programming language and requirements.

## Core Interaction Patterns

**IMPORTANT**: The following WebSocket API commands form the **core** of how users should interact with Home Assistant. These leverage the automation engine and keep scripts minimal by using native Home Assistant syntax.

### Automation Engine Commands (WebSocket API)

These commands require WebSocket API connection and provide the most powerful and flexible way to interact with Home Assistant:

#### 1. subscribe_trigger - Listen for Specific Events

**Use this when**: You want to be notified when specific conditions occur (state changes, time patterns, webhooks, etc.)

**Command structure**:
```json
{
  "type": "subscribe_trigger",
  "trigger": {
    "platform": "state",
    "entity_id": "binary_sensor.motion_sensor",
    "to": "on"
  },
  "variables": {
    "custom_var": "value"
  }
}
```

**Why use this**: Instead of subscribing to all state changes and filtering, subscribe directly to the triggers you care about. This is more efficient and uses Home Assistant's native trigger syntax.

#### 2. test_condition - Test Conditions Server-Side

**Use this when**: You need to check if a condition is met without implementing the logic in your script

**Command structure**:
```json
{
  "type": "test_condition",
  "condition": {
    "condition": "numeric_state",
    "entity_id": "sensor.temperature",
    "above": 20
  },
  "variables": {
    "custom_var": "value"
  }
}
```

**Why use this**: Offload condition logic to Home Assistant. Your script stays simple while using Home Assistant's powerful condition engine.

#### 3. execute_script - Execute Multiple Actions

**Use this when**: You need to execute a sequence of actions, including `wait_for_trigger`, delays, service calls, and more

**Command structure**:
```json
{
  "type": "execute_script",
  "sequence": [
    {
      "service": "light.turn_on",
      "target": {"entity_id": "light.living_room"}
    },
    {
      "wait_for_trigger": [
        {
          "platform": "state",
          "entity_id": "binary_sensor.motion",
          "to": "off",
          "for": {"minutes": 5}
        }
      ]
    },
    {
      "service": "light.turn_off",
      "target": {"entity_id": "light.living_room"}
    }
  ],
  "variables": {
    "custom_var": "value"
  }
}
```

**Why use this**:
- Execute complex automation logic using native Home Assistant syntax
- Use `wait_for_trigger` to wait for events
- Chain multiple actions together
- Keep your script minimal - all logic is in HA syntax
- **Getting response data**: To get response from service calls, store the result in a response variable and set it as the script result

**Example with response data**:
```json
{
  "type": "execute_script",
  "sequence": [
    {
      "service": "weather.get_forecasts",
      "target": {"entity_id": "weather.home"},
      "response_variable": "weather_data"
    },
    {
      "stop": "Done",
      "response_variable": "weather_data"
    }
  ]
}
```

### Essential Registry Information

To understand Home Assistant's information architecture, also use:

- **config/entity_registry/list**: Learn about entities and their unique IDs
- **config/device_registry/list**: Learn about devices and their entities
- **config/area_registry/list**: Understand how spaces are organized
- **config/floor_registry/list**: Multi-floor layout information

### Current state of the home

If the user is building an application that wants to represent the current state of the home, use:

- **subscribe_entities**: Get real-time updates on all entity states (Home Assistant JS WebSocket has built-in support for this)

## Implementation Guidance

### Python Projects

For Python-based projects, refer to the Python API reference:

- **File**: `references/python_api.md`
- **Usage**: Load this reference when implementing Python integrations
- **Contains**:
  - **Example code**: Python scripts demonstrating common use cases.
- **Key operations**: Automation engine commands, getting states, calling services, subscribing to events, error handling

### Node.js Projects

For Node.js-based projects, refer to the Node.js API reference:

- **File**: `references/node_api.md`
- **Usage**: Load this reference when implementing Node.js integrations
- **Contains**:
  - WebSocket API examples using `home-assistant-js-websocket` library

## Best Practices

1. **Error Handling**: Always implement proper error handling for network failures and authentication issues
2. **Connection Testing**: Validate connections before proceeding with implementation
3. **Real-time Updates**: For monitoring scenarios, use WebSocket APIs instead of polling REST endpoints

## Testing with empty-hass

If users want to test their code without connecting to a real Home Assistant instance, they can use **empty-hass**, a CLI tool that starts an empty Home Assistant instance with pre-configured authentication.

### Quick Start

Run empty-hass using uvx (requires Python with uv installed):

```bash
uvx --from git+https://github.com/balloob/empty-hass empty-hass
```

This will start a Home Assistant instance on `http://localhost:8123` with:
- A pre-onboarded configuration (skips the setup wizard)
- A temporary configuration directory (cleaned up on exit)

Run with `--help` to see available options and login credentials:

```bash
uvx --from git+https://github.com/balloob/empty-hass empty-hass --help
```

This is useful for:
- Testing API integration code before connecting to a production instance
- Development and debugging without affecting real devices
- CI/CD pipelines that need a Home Assistant instance for testing

## Common Integration Patterns

### Data Dashboard
Read sensor states and display them in a custom dashboard or monitoring application.

### Automation Logic
Subscribe to entity state changes and trigger custom actions based on conditions.

### External Triggers
Call Home Assistant services from external events (webhooks, scheduled jobs, user actions).

### Data Export
Retrieve historical data from Home Assistant for analysis or backup purposes.
