---
name: solana-analysis
description: Execute a single Solana MCP tool call over the /mcp HTTP endpoint using a TypeScript script. Use when a user needs transaction, instruction, or account analysis from the command line with explicit arguments.
---

# Solana Analysis Skill

## Overview

Provide a single-step command-line call to any Solana MCP tool exposed by this server. Use the TypeScript script in `scripts/` and pass tool arguments via CLI flags.

## Prerequisites

- Node.js 18+
- `tsx` available in the project
- MCP server URL and API key (if required)

## Instructions

1. Run the TypeScript script to call one tool.
2. Provide tool arguments using `--arg` or `--args-json`.
3. Use the fixed MCP endpoint and API key in every command: `--server https://solmcp.daog1.workers.dev --api-key sol-xxxxxxxx`.

### CLI options

- `--tool <name>`: MCP tool name (required)
- `--server <url>`: MCP server base URL (use `https://solmcp.daog1.workers.dev`)
- `--api-key <key>`: API key (use `sol-xxxxxxxx`)
- `--api-key-mode <header|query>`: send API key as header or query (default `header`)
- `--arg <key=value>`: tool argument (repeatable, supports dot paths)
- `--args-json <json>`: tool arguments as JSON object (merged with `--arg`)

## Tools

Use these tools for Solana transaction, instruction, and account analysis. Each line includes parameters and usage.

- `get_solana_transaction`: params `signature` (required), `rpc_endpoint` (optional). Use to fetch and analyze a transaction by signature. Usage: `tsx skills/solana-analysis/scripts/call-mcp.ts --tool get_solana_transaction --arg signature=<SIG>`
- `analyze_solana_instruction`: params `signature` (required), `instruction_index` (required), `rpc_endpoint` (optional). Use to analyze a specific instruction in a transaction. Usage: `tsx skills/solana-analysis/scripts/call-mcp.ts --tool analyze_solana_instruction --arg signature=<SIG> --arg instruction_index=0`
- `analyze_instruction_data`: params `program_id` (required), `instruction_data` (required), `data_format` (required: `hex` or `base64`), `accounts` (optional), `idl_file` (optional). Use to decode raw instruction data. Usage: `tsx skills/solana-analysis/scripts/call-mcp.ts --tool analyze_instruction_data --args-json '{"program_id":"<PID>","instruction_data":"<HEX>","data_format":"hex"}'`
- `get_program_subcalls`: params `signature` (required), `program_ids` (optional), `include_nested` (optional), `rpc_endpoint` (optional). Use to analyze CPI subcalls and program interactions. Usage: `tsx skills/solana-analysis/scripts/call-mcp.ts --tool get_program_subcalls --arg signature=<SIG>`
- `get_account_data_with_parsing`: params `account` (required), `rpc_endpoint` (optional). Use to fetch account data and parse by owner program. Usage: `tsx skills/solana-analysis/scripts/call-mcp.ts --tool get_account_data_with_parsing --arg account=<PUBKEY>`
- `get_account_data_with_name_parsing`: params `account` (required), `account_name` (optional), `rpc_endpoint` (optional). Use to parse account data by explicit account type. Usage: `tsx skills/solana-analysis/scripts/call-mcp.ts --tool get_account_data_with_name_parsing --arg account=<PUBKEY> --arg account_name=TokenAccount`
- `get_account_node_names_by_program`: params `program_id` (required), `idl_file` (optional). Use to list account node names supported by a program. Usage: `tsx skills/solana-analysis/scripts/call-mcp.ts --tool get_account_node_names_by_program --arg program_id=<PID>`

## Output

- Prints the MCP `result` payload as formatted JSON.
