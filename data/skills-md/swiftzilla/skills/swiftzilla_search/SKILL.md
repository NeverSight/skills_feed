---
name: swiftzilla_search
description: Search Swift technical context using SwiftZilla Deep Insight™. Use this skill when the user asks questions about Swift programming, Apple frameworks (SwiftUI, Combine, etc.), or requires deep technical insights.
license: Proprietary
compatibility: Requires curl, jq
metadata:
  version: "1.0"
  author: SwiftZilla
  website: https://swiftzilla.dev
allowed-tools: Bash(curl:*) Bash(jq:*)
---

# Swift Deep Insight

This skill allows you to retrieve high-precision technical context and deep insights about the Swift programming language and Apple frameworks using the SwiftZilla Deep Insight™ engine.

## Instructions

1.  **Verify System**: Run `./check.sh` to ensure the API key is valid and the server is reachable.
    *   If this fails, STOP and report the error to the user.
2.  **Formulate Query**: Create a specific, technical query based on the user's request.
    *   Good: "async await concurrency model", "SwiftUI View protocol", "Combine Publisher lifecycle"
    *   Bad: "help", "swift", "code"
3.  **Execute Search**: Run the `search.sh` script with the query.
4.  **Process Results**: The script will output formatted text containing relevant technical details. Use this information to answer the user's question, citing specific details where appropriate.

## Usage

### Basic Search

```bash
# Optional: Verify status first
./check.sh

# Perform search
./search.sh "your query here"
```

### Example

User: "How do actors work in Swift?"

Agent Action:
```bash
./search.sh "swift actors concurrency isolation"
```

## Error Handling

The script will return descriptive error messages if:
*   The API key is missing.
*   The SwiftZilla server is unreachable.
*   Authentication fails.
*   No results are found.

Use these error messages to guide the user (e.g., "Please set your SWIFTZILLA_API_KEY to continue.").
