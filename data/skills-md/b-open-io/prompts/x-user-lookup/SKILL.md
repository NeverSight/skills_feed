---
name: x-user-lookup
version: 1.0.0
description: Get X/Twitter user profile by username. Use when user asks "who is @username", "get X profile", "lookup Twitter user", "find X account", "user details", "follower count for". Requires X_BEARER_TOKEN.
allowed-tools: Bash(curl:*), Bash(jq:*), Bash(${CLAUDE_PLUGIN_ROOT}:*)
---

# X User Lookup

Get user profile information by username or ID.

## Setup

```bash
export X_BEARER_TOKEN="your-token"  # https://developer.x.com/en/portal/dashboard
```

## Usage

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/lookup.sh <username>
```

## Example

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/lookup.sh kurtwuckertjr
```

## Response Fields

- `id` - User ID
- `name` - Display name
- `username` - Handle (without @)
- `description` - Bio
- `public_metrics` - Followers, following, tweet count
- `verified` - Verification status
- `created_at` - Account creation date

## References

- https://docs.x.com/llms.txt
- https://developer.x.com/en/docs/x-api/users/lookup
