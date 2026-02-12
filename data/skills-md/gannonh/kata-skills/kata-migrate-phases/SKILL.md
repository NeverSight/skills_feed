---
name: kata-migrate-phases
description: "[DEPRECATED] Use /kata-doctor instead. Migrate phase directories to globally sequential numbering. Triggers include \"migrate phases\", \"fix phase numbers\", \"renumber phases\", \"phase collision\", \"fix phase collisions\", \"fix duplicate phases\", \"phase numbering migration\"."
metadata:
  version: "1.8.0"
  deprecated: true
  replacement: kata-doctor
---
<objective>
**This skill is deprecated.** Phase collision detection and migration is now handled by `/kata-doctor`.

Redirects to `kata-doctor` for backward compatibility with existing trigger phrases.
</objective>

<process>

<step name="deprecation_notice">

Display deprecation notice:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 ⚠ DEPRECATED: /kata-migrate-phases
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase migration is now part of `/kata-doctor`.

Redirecting...
```

</step>

<step name="invoke_doctor">

Invoke the replacement skill:

```
Skill("kata-doctor")
```

</step>

</process>

<success_criteria>
- [ ] Deprecation notice displayed
- [ ] kata-doctor skill invoked
</success_criteria>
