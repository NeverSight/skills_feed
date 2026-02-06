---
name: hello_world
version: 1.0.0
entrypoint: scripts/main.py
description: A simple skill that greets the user
inputs:
  - type: text
    name: name
    description: Name to greet
outputs:
  - type: text
    name: greeting
    description: Greeting message
tags: [example, simple, greeting]
allow_network: false
---

# Hello World Skill

A minimal example skill that demonstrates the basic structure of an open-skills skill bundle.

## What it does

This skill takes a name as input and returns a friendly greeting message.

## Usage

```json
{
  "name": "Alice"
}
```

Returns:

```json
{
  "greeting": "Hello, Alice! Welcome to open-skills."
}
```

## Files

- `SKILL.md`: Skill metadata and documentation (this file)
- `scripts/main.py`: Main entrypoint with the `run()` function
- `tests/sample_input.json`: Example input for testing
