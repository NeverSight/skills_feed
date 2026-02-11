---
name: arkts-sta-playground
description: Execute ArkTS-Sta code snippets and files via the Playground HTTP API. Use this for testing ArkTS syntax, learning ArkTS features, verifying code logic, or demonstrating code execution results.
---

# ArkTS-Sta Playground Runner

## Overview

This skill runs ArkTS-Sta code using the ArkTS-Sta Playground HTTP API, providing fast and reliable code execution without browser automation.

## Quick Start

### Basic Usage

Run an ArkTS-Sta file:

```bash
python3 scripts/run_playground.py path/to/code.ets
```

Run code directly as a string:

```bash
python3 scripts/run_playground.py --code "let x: number = 42; console.log(x);"
```

Get JSON output for programmatic parsing:

```bash
python3 scripts/run_playground.py --json --code "console.log('Hello');"
```

## Setup Requirements

Install Python dependencies:

```bash
pip install -r scripts/requirements.txt
```

Required package: `requests>=2.31.0`

## Usage Patterns

### Pattern 1: Quick Code Testing

When testing ArkTS-Sta syntax or verifying code logic:

```bash
python3 scripts/run_playground.py --code "
enum Numbers {
  A = 10,
  B = 2.57,
  C = 0x2B7F,
  D = -1.5,
  E = 12
}
"
```

### Pattern 2: Batch Testing

For testing multiple files:

```bash
for file in test/*.ets; do
    python3 scripts/run_playground.py --json "$file" > "results/$(basename $file .ets).json"
done
```

## How It Works

The script uses the HTTP API endpoint:

1. Sends your ArkTS-Sta code to `https://arkts-play.cn.bz-openlab.ru:10443/compile`
2. Receives compilation results and output
3. Returns formatted results (success status, output, errors)

## API Endpoint

**Base URL:** `https://arkts-play.cn.bz-openlab.ru:10443/compile`

**Method:** POST

**Request:**
```json
{
  "code": "your ArkTS-Sta code here"
}
```

**Response:**
```json
{
  "output": "execution output or empty",
  "error": "error message if compilation failed, null otherwise"
}
```

## Troubleshooting

### Connection issues

If you get connection errors:

1. Check internet connectivity
2. Verify the API endpoint is accessible
3. Check firewall settings

```bash
# Test connectivity
curl -X POST https://arkts-play.cn.bz-openlab.ru:10443/compile \
  -H "Content-Type: application/json" \
  -d '{"code":"let x: number = 42;"}'
```

### Timeout issues

Increase timeout if the API is slow:

```bash
python3 scripts/run_playground.py --timeout 60 path/to/code.ets
```

### SSL certificate errors

If you encounter SSL certificate issues, you may need to:
- Ensure your system's CA certificates are up to date
- Or modify the script to disable SSL verification (not recommended for production)

## Common Use Cases

### Learn ArkTS Syntax

Test and explore ArkTS language features:

```bash
python3 scripts/run_playground.py --code "
// Test union types
let value: string | number = 'hello';
value = 42;
console.log(value);
"
```

### Quick Prototype Verification

Verify code logic before integrating into your project:

```bash
python3 scripts/run_playground.py --code "
function calculateSum(a: number, b: number): number {
    return a + b;
}
console.log('Sum:', calculateSum(10, 20));
"
```

### Debug Code Snippets

Find compilation errors in your code:

```bash
# Run with JSON output for programmatic checking
python3 scripts/run_playground.py --json problem.ets

# Check exit status
if python3 scripts/run_playground.py code.ets; then
    echo "Compilation successful"
else
    echo "Compilation failed"
fi
```

## Script Output

The script returns a JSON structure (with `--json` flag):

```json
{
  "success": true,
  "output": "Execution result here...",
  "error": null,
  "has_error": false
}
```

Fields:
- `success`: Boolean indicating if the API request succeeded
- `output`: Code output or compilation output
- `error`: Error message if compilation failed, `null` otherwise
- `has_error`: Boolean indicating if the code has compilation errors

## Example: Testing Enum with Floating Point

Test if enum with non-integer values causes errors:

```bash
python3 scripts/run_playground.py --code "
enum Numbers {
  A = 10,
  B = 2.57,
  C = 0x2B7F,
  D = -1.5,
  E = 12
}
"
```

Expected result: Should fail with an error about enum values needing to be integers.

## Limitations

- Requires internet access to the API endpoint
- API rate limiting may apply
- Compilation output format depends on the API response

## Tips for Efficient Usage

1. **Use JSON output** for programmatic processing (`--json`)
2. **Batch test** multiple files using shell loops
3. **Check exit codes** in scripts for success/failure
