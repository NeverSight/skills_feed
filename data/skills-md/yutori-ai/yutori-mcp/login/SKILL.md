---
name: login
description: Log in to Yutori to connect your account
argument-hint: ""
---

# Yutori Login

Tell the user to run this command in a separate terminal window:

```
uvx yutori-mcp login
```

This opens a browser for authentication and saves the API key to `~/.yutori/config.json`. After login, all Yutori tools work automatically.

Do NOT run this command via Bash — the browser and callback server need a real terminal.
