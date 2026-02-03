---
name: gcp-error-logs
description: Fetch and analyze error logs from Google Cloud Logging for Cloud Functions. Groups errors by pattern, identifies frequency, and provides root cause insights. Use when debugging GCP errors, investigating Cloud Functions failures, analyzing production issues, or when the user mentions Google Cloud logs, GCP errors, or Cloud Functions issues.
---

# Google Cloud Error Logs Analysis

Fetch and analyze error logs from Google Cloud Logging for Cloud Functions. This skill helps identify error patterns, group similar errors, and provide root cause analysis.

## Trigger Phrases
- "get GCP errors"
- "analyze Cloud Functions logs"
- "check Google Cloud logs"
- "debug Cloud Functions"
- "investigate GCP errors"
- "show error logs from GCP"

## Prerequisites

Verify gcloud CLI is installed and authenticated:

```bash
# Check gcloud is installed
gcloud --version

# Check authentication
gcloud auth list

# If not authenticated
gcloud auth login

# Set default project (optional)
gcloud config set project PROJECT_ID
```

## Workflow: Fetch and Analyze Errors

### Step 1: Fetch Error Logs

Use the fetch script to retrieve error logs from Cloud Logging:

```bash
bash "${SKILL_DIR}/scripts/fetch-errors.sh" --project=PROJECT_ID [OPTIONS]
```

**Required parameter:**
- `--project=PROJECT_ID`: GCP project ID

**Optional parameters:**
- `--function=FUNCTION_NAME`: Specific Cloud Function name
- `--hours=24`: Time range in hours (default: 24)
- `--severity=ERROR`: Log severity level (ERROR, WARNING, CRITICAL)
- `--limit=100`: Maximum number of log entries (default: 100)
- `--output=errors.json`: Output file path (default: /tmp/gcp-errors.json)

**Examples:**

```bash
# Get all errors from last 24 hours
bash scripts/fetch-errors.sh --project=my-project

# Get errors for specific function
bash scripts/fetch-errors.sh --project=my-project --function=processPayment

# Get critical errors from last hour
bash scripts/fetch-errors.sh --project=my-project --hours=1 --severity=CRITICAL

# Get last 500 errors
bash scripts/fetch-errors.sh --project=my-project --limit=500
```

### Step 2: Analyze Error Patterns

Use the analysis script to group and analyze errors:

```bash
python3 "${SKILL_DIR}/scripts/analyze-errors.py" /tmp/gcp-errors.json
```

The analysis script:
- Groups similar errors together
- Calculates error frequency
- Identifies time distribution patterns
- Detects common error types
- Suggests potential root causes

### Step 3: Review Analysis Results

The analysis output includes:

#### Error Summary
- Total error count
- Unique error patterns
- Time range covered
- Most common error types

#### Error Groups
Each group shows:
- Error pattern (normalized message)
- Occurrence count
- First and last seen timestamps
- Affected resources (function names)
- Sample stack trace
- Root cause analysis

#### Time Distribution
- Errors per hour histogram
- Peak error times
- Trend analysis (increasing/decreasing)

## Output Format

Present findings using this template:

```markdown
## GCP Error Analysis Results

**Time Range**: [START] to [END]  
**Total Errors**: [COUNT]  
**Unique Patterns**: [COUNT]  
**Project**: [PROJECT_ID]

### Top Error Patterns

#### 1. [Error Type]
- **Occurrences**: [COUNT] ([PERCENTAGE]%)
- **First Seen**: [TIMESTAMP]
- **Last Seen**: [TIMESTAMP]
- **Affected Functions**: [FUNCTION_NAMES]

**Error Message**:
```
[NORMALIZED_ERROR_MESSAGE]
```

**Root Cause Analysis**:
[ANALYSIS_FROM_COMMON_PATTERNS]

**Recommended Actions**:
- [ACTION_1]
- [ACTION_2]

---

[REPEAT FOR TOP 5-10 ERROR PATTERNS]

### Time Distribution

[ERROR_FREQUENCY_CHART_OR_DESCRIPTION]

### Summary & Recommendations

[OVERALL_ANALYSIS_AND_NEXT_STEPS]
```

## Common Cloud Functions Error Patterns

### Authentication & Authorization

**Error**: `Permission denied` or `403 Forbidden`
- **Cause**: IAM permissions missing
- **Check**: Service account permissions, API enablement
- **Fix**: Grant required roles to service account

**Error**: `Unauthenticated` or `401 Unauthorized`
- **Cause**: Missing or invalid auth token
- **Check**: Token generation, expiration
- **Fix**: Implement proper authentication flow

### Resource Limits

**Error**: `Memory limit exceeded` or `Container killed`
- **Cause**: Function using more memory than allocated
- **Check**: Memory allocation in function config
- **Fix**: Increase memory limit or optimize code

**Error**: `Function execution timeout`
- **Cause**: Function takes longer than timeout setting
- **Check**: Timeout configuration, blocking operations
- **Fix**: Increase timeout or optimize slow operations

**Error**: `Quota exceeded`
- **Cause**: API quota or rate limit reached
- **Check**: API quotas in GCP console
- **Fix**: Request quota increase or implement rate limiting

### Networking

**Error**: `Connection refused` or `ECONNREFUSED`
- **Cause**: Unable to connect to external service
- **Check**: VPC configuration, firewall rules
- **Fix**: Configure VPC connector or check service availability

**Error**: `DNS lookup failed` or `ENOTFOUND`
- **Cause**: Cannot resolve hostname
- **Check**: DNS configuration, hostname spelling
- **Fix**: Verify DNS settings or use IP address

**Error**: `SSL certificate error`
- **Cause**: Invalid or expired SSL certificate
- **Check**: Certificate validity, chain completeness
- **Fix**: Update certificate or disable verification (dev only)

### Code Errors

**Error**: `TypeError`, `ReferenceError`, `SyntaxError`
- **Cause**: JavaScript/Node.js code error
- **Check**: Recent code changes, null checks
- **Fix**: Fix code logic, add error handling

**Error**: `ModuleNotFoundError` or `Cannot find module`
- **Cause**: Missing dependency
- **Check**: package.json dependencies, deployment
- **Fix**: Install dependency and redeploy

**Error**: `Unhandled promise rejection`
- **Cause**: Async error not caught
- **Check**: Try-catch blocks, .catch() handlers
- **Fix**: Add proper error handling

### Cold Start Issues

**Error**: `Function cold start timeout`
- **Cause**: Initialization taking too long
- **Check**: Global scope initialization, dependencies
- **Fix**: Optimize imports, reduce initialization work

### Configuration

**Error**: `Environment variable not set`
- **Cause**: Missing required environment variable
- **Check**: Function configuration
- **Fix**: Set environment variable in deployment

**Error**: `Invalid configuration`
- **Cause**: Malformed config file or settings
- **Check**: YAML/JSON syntax, required fields
- **Fix**: Validate and correct configuration

## Troubleshooting

### Script Fails to Authenticate
```bash
# Reauthenticate
gcloud auth login

# Or use service account
gcloud auth activate-service-account --key-file=KEY_FILE.json
```

### No Logs Found
- Verify project ID is correct
- Check time range (increase --hours)
- Verify function name spelling
- Check if logs exist in GCP Console

### Analysis Script Errors
```bash
# Ensure Python 3 is installed
python3 --version

# The script uses only standard library, no pip install needed
```

### Rate Limiting
If you hit API rate limits:
- Reduce --limit parameter
- Increase time between requests
- Use multiple time ranges instead of one large query

## Advanced Usage

### Custom Filters

Modify the fetch script filter for specific queries:

```bash
# Edit the FILTER variable in scripts/fetch-errors.sh
# Examples:
# - Filter by specific text: textPayload=~"payment failed"
# - Filter by HTTP status: httpRequest.status>=500
# - Filter by user: labels.user_id="12345"
```

### Export for Further Analysis

```bash
# Save to JSON for processing
bash scripts/fetch-errors.sh --project=my-project --output=errors.json

# Convert to CSV (requires jq)
cat errors.json | jq -r '.[] | [.timestamp, .severity, .message] | @csv' > errors.csv
```

### Continuous Monitoring

```bash
# Set up cron job for hourly checks
0 * * * * cd /path/to/skill && bash scripts/fetch-errors.sh --project=my-project --hours=1 --output=/tmp/errors-$(date +\%Y\%m\%d-\%H).json
```

## Additional Resources

For detailed Cloud Logging filter syntax and API reference, see [reference.md](reference.md).

## Quick Reference

| Command | Purpose |
|---------|---------|
| `gcloud auth list` | Check authentication |
| `gcloud projects list` | List available projects |
| `gcloud functions list` | List Cloud Functions |
| `gcloud logging read --help` | View logging command help |
