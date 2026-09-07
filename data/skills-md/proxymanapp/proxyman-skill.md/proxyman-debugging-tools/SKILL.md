---
name: "proxyman-debugging-tools"
description: "Find and explain current Proxyman debugging tools using official documentation, with GUI, MCP, and CLI workflows where supported. Use for Breakpoint, Map Local or Remote, Scripting, Compose, Repeat, Protobuf, TLS Key Logging, Reverse Proxy, Network Conditions, WebSocket, filters, exports, certificates, and other Proxyman feature guides."
---

# Proxyman Debugging Tools And Documentation

Use official Proxyman documentation to teach or plan a debugging workflow. This skill is documentation-first: it does not assume that a similarly named MCP or CLI action exists.

Use `proxyman-traffic-debugging` when the main task is to operate MCP now. Use `proxyman-app-settings` for a Settings-tab audit or preference change, `proxyman-certificates-recovery` for local root/custom certificate lifecycle or Help-menu Debug Mode/Factory Reset, `proxyman-https-capture` for device/runtime capture configuration, `proxyman-cli` for shell automation, and `proxyman-license-management` for licensing.

## Get The Current Documentation

For every task where current behavior matters:

1. Fetch `https://docs.proxyman.com/llms.txt`.
2. Match the user's feature or symptom to one or more official `.md` entries.
3. Fetch the selected `.md` page directly. Do not reconstruct a page path from memory when the index provides it.
4. Cite the public HTML URL by removing only the final `.md` from the fetched URL.
5. If the page links a prerequisite or troubleshooting page that materially changes the steps, fetch that page too.

Use official Proxyman-owned domains `docs.proxyman.com`, `docs.proxyman.io`, `proxyman.com`, `proxyman.io`, and the live Proxyman MCP server as authorities. A freshly fetched official page may link to an external destination, but treat that destination as authoritative only for its own product or service unless the user asks for third-party guidance.

If internet access is unavailable, say that the latest page could not be verified. You may use the bundled [debugging tool index](references/debugging-tool-index.md) as a navigation fallback, but label it as a snapshot.

## Understand Built-In MCP Documentation

`search_docs`, `answer_setup_question`, `docs://search/{query}`, and the static MCP resources search Proxyman's bundled **setup and troubleshooting** knowledge base. They are version-matched and ideal for capture diagnosis, but they do not represent the full `docs.proxyman.com` catalog.

For a product-wide feature question, fetch the public index even if `search_docs` returns a result. For exact MCP inputs, trust `tools/list`, not the public MCP page or this skill.

## Build The Answer Or Guide

1. Identify the user's goal, target traffic, platform, and whether they want explanation, GUI steps, MCP execution, or CLI automation.
2. Read the current official page and extract prerequisites, supported platforms, limits, and verification behavior.
3. Inspect [debugging tool index](references/debugging-tool-index.md) to map the feature to interfaces.
   - For Breakpoint, Map Local, Map Remote, Scripting, or interaction among those rules, read [request and response modification](references/request-response-modification.md).
   - For Compose or Repeat, Network Conditions, or Reverse Proxy, read [replay and routing workflows](references/replay-and-routing.md).
   - For Protobuf or TLS Key Logging, read [protocol decoding and key logging](references/protocol-decoding-and-key-logging.md).
4. Present only supported routes:
   - **GUI:** menu/screen and ordered user steps from the current page.
   - **MCP:** current tool names, discovery requirement, state read, mutation, and verification.
   - **CLI:** route to `proxyman-cli`; discover installed help before giving exact flags.
5. Include a concrete verification: expected flow, rule inventory, status field, response change, or exported artifact.
6. Include rollback for persistent rules, proxy changes, certificate trust, or capture automation.

If the docs describe a GUI-only feature, say so. Do not invent MCP/CLI parity.

## Guide Shape

Use this compact structure:

```text
Goal
Prerequisites
GUI steps
MCP steps (if exposed)
CLI steps (if exposed)
How to verify
How to undo
Limits / platform notes
Official docs
```

Skip empty interface sections rather than padding the answer.

## Safety

- Start with read-only discovery and traffic inspection.
- Obtain confirmation before changing proxy routing, trust stores, global tool state, external proxy credentials, or other applications.
- Obtain confirmation immediately before deletes, session clearing, certificate uninstall, destructive imports, or irreversible portal actions.
- Keep MCP redaction enabled. Warn that exported original traffic is not sanitized by MCP preview redaction.
- Never paste license keys, TLS session-key logs, tokens, passwords, cookies, or captured secrets into a guide or tool input unless the user explicitly requires it and understands the exposure.
- Do not claim a page is current unless it was fetched during this task.

## Coverage

The reference maps capture/view/filter tools, Repeat/Compose, Breakpoint, Map Local/Remote, Block/Allow List, Scripting, No Caching, External/Reverse/SOCKS proxy, SSL Proxying, certificates, WebSocket, Protobuf/GraphQL, Network Conditions, DNS Spoofing, exports, code generation, diff, OpenAPI, TLS Key Logging, and adjacent GUI tools.

When a current index adds a new debugging page, use it even if it is absent from the snapshot, then state which interfaces the live product exposes.
