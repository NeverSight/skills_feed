---
name: secret-leak-detector
description: Scans source code, configuration files, and git history for hardcoded credentials, API keys, and tokens. Use when auditing repositories for security leaks or ensuring sensitive data is not committed to version control.
---
# Secret Leak Detector

## Purpose and Intent
The `secret-leak-detector` is designed to safeguard repositories by identifying hardcoded sensitive information such as API keys, database credentials, and authentication tokens before they are committed or after they have been accidentally pushed to history.

## When to Use
- **Pre-commit Checks**: Run this skill before committing changes to ensure no secrets are being introduced.
- **CI/CD Pipelines**: Integrate into automated pipelines to block builds that contain plain-text secrets.
- **Legacy Audits**: Use with `scan_history: true` to perform a deep audit of a project's entire history to find secrets that were deleted but still exist in git logs.

## When NOT to Use
- **Production Logs**: This tool is for source code and config files; it is not optimized for scanning terabytes of runtime logs.
- **Binary Files**: It will not effectively detect secrets inside compiled binaries or encrypted blobs.

## Input and Output Examples

### Input
```yaml
directory_path: "./config"
scan_history: false
```

### Output
```json
{
  "leaks": [
    {
      "file": "config/production.yaml",
      "line": 45,
      "type": "Stripe Secret Key",
      "risk_level": "critical",
      "snippet": "sk_live_**********"
    }
  ]
}
```

## Error Conditions and Edge Cases
- **False Positives**: High-entropy strings in test data or encrypted hashes may be flagged as secrets.
- **Git Repository Required**: If `scan_history` is true, the target directory must be a valid git repository.
- **Permission Denied**: The skill will fail if it lacks read permissions for specific files or the `.git` directory.

## Security and Data-Handling Considerations
- **No Persistence**: This skill does not store the secrets it finds.
- **Masking**: Output snippets are masked to prevent the tool itself from becoming a source of leaks in logs or terminal history.
- **Local Execution**: The skill runs locally and does not phone home or upload code to third-party services.
