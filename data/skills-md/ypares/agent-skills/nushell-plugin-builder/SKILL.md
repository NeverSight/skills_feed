---
name: nushell-plugin-builder
description: Guide for creating Nushell plugins in Rust using nu_plugin and nu_protocol crates. Use when users want to build custom Nushell commands, extend Nushell with new functionality, create data transformations, or integrate external tools/APIs into Nushell. Covers project setup, command implementation, streaming data, custom values, and testing.
---

# Nushell Plugin Builder

## Overview

This skill helps create Nushell plugins in Rust. Plugins are standalone executables that extend Nushell with custom commands, data transformations, and integrations.

## Quick Start

### 1. Create Plugin Project

```bash
cargo new nu_plugin_<name>
cd nu_plugin_<name>
cargo add nu-plugin nu-protocol
```

### 2. Basic Plugin Structure

```rust
use nu_plugin::{EvaluatedCall, MsgPackSerializer, serve_plugin};
use nu_plugin::{EngineInterface, Plugin, PluginCommand, SimplePluginCommand};
use nu_protocol::{LabeledError, Signature, Type, Value};

struct MyPlugin;

impl Plugin for MyPlugin {
    fn version(&self) -> String {
        env!("CARGO_PKG_VERSION").into()
    }

    fn commands(&self) -> Vec<Box<dyn PluginCommand<Plugin = Self>>> {
        vec![Box::new(MyCommand)]
    }
}

struct MyCommand;

impl SimplePluginCommand for MyCommand {
    type Plugin = MyPlugin;

    fn name(&self) -> &str {
        "my-command"
    }

    fn signature(&self) -> Signature {
        Signature::build("my-command")
            .input_output_type(Type::String, Type::Int)
    }

    fn run(
        &self,
        _plugin: &MyPlugin,
        _engine: &EngineInterface,
        call: &EvaluatedCall,
        input: &Value,
    ) -> Result<Value, LabeledError> {
        match input {
            Value::String { val, .. } => {
                Ok(Value::int(val.len() as i64, call.head))
            }
            _ => Err(LabeledError::new("Expected string input")
                .with_label("requires string", call.head))
        }
    }
}

fn main() {
    serve_plugin(&MyPlugin, MsgPackSerializer)
}
```

### 3. Build and Install

```bash
# Build
cargo build --release

# Install to cargo bin
cargo install --path . --locked

# Register with nushell
plugin add ~/.cargo/bin/nu_plugin_<name>  # Add .exe on Windows
plugin use <name>

# Test
"hello" | my-command
```

## Command Types

### SimplePluginCommand
For commands that operate on single values:
- Input: `&Value`
- Output: `Result<Value, LabeledError>`
- Use for: transformations, simple filters, single value operations

### PluginCommand
For commands that handle streams:
- Input: `PipelineData`
- Output: `Result<PipelineData, LabeledError>`
- Use for: streaming transformations, lazy processing, large datasets

See `references/advanced-features.md` for streaming examples.

## Defining Command Signatures

### Input-Output Types
```rust
use nu_protocol::{Signature, Type};

Signature::build("my-command")
    .input_output_type(Type::String, Type::Int)
```

Common types: `String`, `Int`, `Float`, `Bool`, `List(Box<Type>)`, `Record(...)`, `Any`

### Parameters
```rust
Signature::build("my-command")
    // Named flags
    .named("output", SyntaxShape::Filepath, "output file", Some('o'))
    .switch("verbose", "enable verbose output", Some('v'))
    // Positional arguments
    .required("input", SyntaxShape::String, "input value")
    .optional("count", SyntaxShape::Int, "repeat count")
    .rest("files", SyntaxShape::Filepath, "files to process")
```

### Accessing Arguments
```rust
fn run(&self, call: &EvaluatedCall, ...) -> Result<Value, LabeledError> {
    let output: Option<String> = call.get_flag("output")?;
    let verbose: bool = call.has_flag("verbose")?;
    let input: String = call.req(0)?;  // First positional
    let count: Option<i64> = call.opt(1)?;  // Second positional
    let files: Vec<String> = call.rest(2)?;  // Remaining args
}
```

## Error Handling

Always return `LabeledError` with span information:
```rust
Err(LabeledError::new("Error message")
    .with_label("specific issue", call.head))
```

This shows users exactly where the error occurred in their command.

## Serialization

**MsgPackSerializer** (Recommended)
- Binary format, much faster
- Use for production plugins

**JsonSerializer**
- Text-based, human-readable
- Useful for debugging

Choose in `main()`:
```rust
serve_plugin(&MyPlugin, MsgPackSerializer)  // Production
// serve_plugin(&MyPlugin, JsonSerializer)  // Debug
```

## Common Patterns

### String Transformation
```rust
Value::String { val, .. } => {
    Ok(Value::string(val.to_uppercase(), call.head))
}
```

### List Generation
```rust
let items = vec![
    Value::string("a", call.head),
    Value::string("b", call.head),
];
Ok(Value::list(items, call.head))
```

### Record (Table Row)
```rust
use nu_protocol::record;

Ok(Value::record(
    record! {
        "name" => Value::string("example", call.head),
        "size" => Value::int(42, call.head),
    },
    call.head,
))
```

### Table (List of Records)
```rust
let records = vec![
    Value::record(record! { "name" => Value::string("a", span) }, span),
    Value::record(record! { "name" => Value::string("b", span) }, span),
];
Ok(Value::list(records, call.head))
```

See `references/examples.md` for complete working examples including:
- Filtering streams
- HTTP API calls
- File system operations
- Multi-command plugins

## Development Workflow

### Iterative Development
```bash
# Build
cargo build

# Test (debug build)
plugin add target/debug/nu_plugin_<name>
plugin use <name>
"test" | my-command

# After changes, reload
plugin rm <name>
plugin add target/debug/nu_plugin_<name>
plugin use <name>
```

### Automated Testing
```toml
[dev-dependencies]
nu-plugin-test-support = "0.109.1"
```

```rust
#[cfg(test)]
mod tests {
    use nu_plugin_test_support::PluginTest;

    #[test]
    fn test_command() -> Result<(), nu_protocol::ShellError> {
        PluginTest::new("myplugin", MyPlugin.into())?
            .test_examples(&MyCommand)
    }
}
```

See `references/testing-debugging.md` for debugging techniques and troubleshooting.

## Advanced Features

### Streaming Data
For lazy processing of large datasets, use `PipelineData`:
```rust
impl PluginCommand for MyCommand {
    fn run(&self, input: PipelineData, ...) -> Result<PipelineData, LabeledError> {
        let filtered = input.into_iter().filter(|v| /* condition */);
        Ok(PipelineData::ListStream(ListStream::new(filtered, span, None), None))
    }
}
```

### Engine Interaction
```rust
// Get environment variables
let home = engine.get_env_var("HOME")?;

// Set environment variables (before response)
engine.add_env_var("MY_VAR", Value::string("value", span))?;

// Get plugin config from $env.config.plugins.<name>
let config = engine.get_plugin_config()?;

// Get current directory for path resolution
let cwd = engine.get_current_dir()?;
```

### Custom Values
Define custom data types that extend beyond Nushell's built-in types. See `references/advanced-features.md` for complete guide.

## Important Constraints

**Stdio Restrictions**
- Plugins cannot use stdin/stdout (reserved for protocol)
- Check `engine.is_using_stdio()` before attempting stdio access

**Path Handling**
- Always use paths relative to `engine.get_current_dir()`
- Never assume current working directory

**Version Compatibility**
- Match `nu-plugin` and `nu-protocol` versions
- Both should match target Nushell version

## Reference Documentation

- **`references/plugin-protocol.md`** - Protocol details, serialization, lifecycle
- **`references/advanced-features.md`** - Streaming, EngineInterface, custom values
- **`references/examples.md`** - Complete working examples and patterns
- **`references/testing-debugging.md`** - Development workflow, debugging, troubleshooting

## External Resources

- [Official Plugin Guide](https://www.nushell.sh/contributor-book/plugins.html)
- [nu-plugin API Docs](https://docs.rs/nu-plugin/latest/nu_plugin/)
- [Plugin Examples Repository](https://github.com/nushell/plugin-examples)
- [Awesome Nu](https://github.com/nushell/awesome-nu) - Community plugins
- [nushellWith](https://github.com/YPares/nushellWith) - Nix flake for building reproducible Nushell environments with plugins. Includes 100+ pre-packaged plugins from crates.io with binary caching via Garnix. Useful for testing plugins in isolated environments or building standalone Nu scripts.

## Template Script

Use `scripts/init_plugin.py` to scaffold a new plugin with proper structure:
```bash
python3 scripts/init_plugin.py <plugin-name> [--output-dir <path>]
```

This creates a complete working plugin template ready to customize.
