---
name: discord
description: Use this skill to send a message over Discord to the operator
---

The webhook URL is in `~/.config/discord-agent/webhook-url.txt`

```sh
# Send a message
curl -X POST -F 'content=hello' $(cat ~/.config/discord-agent/webhook-url.txt)

# Send a message with file
curl -X POST -F 'content=hello' -F 'files[0]=@/etc/os-release' $(cat ~/.config/discord-agent/webhook-url.txt)
```
