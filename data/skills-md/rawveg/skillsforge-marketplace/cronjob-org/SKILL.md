---
name: cronjob-org
description: Cron-Job.org Documentation
---

# Cronjob-Org Skill

Comprehensive assistance with the Cron-Job.org REST API for programmatically managing scheduled HTTP jobs. This skill provides guidance on creating, updating, deleting, and monitoring cron jobs through the official API.

## When to Use This Skill

This skill should be triggered when:
- **Creating automated HTTP requests** on a schedule using Cron-Job.org
- **Managing cron jobs programmatically** through the REST API
- **Implementing job monitoring** and execution history tracking
- **Setting up notifications** for job failures or successes
- **Working with API authentication** and rate limits
- **Debugging cron job executions** or analyzing performance metrics
- **Building integrations** that require scheduled HTTP calls
- **Configuring job schedules** using timezone-aware cron expressions

## Key Concepts

### API Authentication
- **API Keys**: Generated in the Cron-Job.org Console under Settings
- **Bearer Token**: API keys are sent via the `Authorization` header
- **IP Restrictions**: Optional IP allowlisting for enhanced security
- **Rate Limits**: 100 requests/day (default), 5,000 requests/day (sustaining members)

### Job Object
A Job represents a scheduled HTTP request with:
- **URL**: The endpoint to call
- **Schedule**: Cron expression with timezone support
- **Settings**: Timeout, HTTP method, headers, authentication
- **State**: Enabled/disabled, execution status, history

### Execution History
Each job execution creates a HistoryItem containing:
- **Timing**: Actual vs planned execution time, jitter, duration
- **Response**: HTTP status code, headers, body (if saveResponses enabled)
- **Performance**: DNS lookup, connection, SSL handshake, transfer times

### Rate Limits
Different endpoints have different rate limits:
- **Job List/Details**: 5 requests/second
- **Job Creation**: 1 request/second, 5 requests/minute
- **History**: 5 requests/second

## Quick Reference

### 1. Authentication Setup

```bash
# Set your API key as a bearer token in the Authorization header
Authorization: Bearer YOUR_API_KEY_HERE
```

**Notes:**
- API keys are generated in the Console → Settings
- Treat API keys as secrets (like passwords)
- Enable IP restrictions whenever possible for security

### 2. List All Jobs (curl)

```bash
curl -X GET https://api.cron-job.org/jobs \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**
```json
{
  "jobs": [
    {
      "jobId": 12345,
      "enabled": true,
      "title": "Daily Backup",
      "url": "https://example.com/backup",
      "lastStatus": 200,
      "lastExecution": 1699920000,
      "nextExecution": 1700006400
    }
  ],
  "jobsPartialError": false
}
```

**Rate Limit:** 5 requests/second

### 3. Create a New Job (Python)

```python
import requests

API_KEY = "your_api_key_here"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

job_data = {
    "job": {
        "url": "https://example.com/api/health-check",
        "enabled": True,
        "title": "Health Check",
        "saveResponses": True,
        "schedule": {
            "timezone": "America/New_York",
            "hours": [-1],          # Every hour
            "mdays": [-1],          # Every day of month
            "minutes": [0],         # At minute 0
            "months": [-1],         # Every month
            "wdays": [-1]           # Every day of week
        }
    }
}

response = requests.post(
    "https://api.cron-job.org/jobs",
    headers=headers,
    json=job_data
)

print(f"Created job ID: {response.json()['jobId']}")
```

**Rate Limit:** 1 request/second, 5 requests/minute

### 4. Update an Existing Job

```python
import requests

API_KEY = "your_api_key_here"
JOB_ID = 12345

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Only include fields you want to change
update_data = {
    "job": {
        "enabled": False,  # Disable the job
        "title": "Updated Title"
    }
}

response = requests.patch(
    f"https://api.cron-job.org/jobs/{JOB_ID}",
    headers=headers,
    json=update_data
)

print("Job updated successfully" if response.status_code == 200 else "Update failed")
```

**Rate Limit:** 5 requests/second

### 5. Job with HTTP Authentication

```json
{
  "job": {
    "url": "https://api.example.com/protected",
    "enabled": true,
    "title": "Protected Endpoint",
    "auth": {
      "enable": true,
      "user": "api_user",
      "password": "secret_password"
    }
  }
}
```

**Notes:**
- Uses HTTP Basic Authentication
- Credentials are stored securely by Cron-Job.org

### 6. Job with Custom Headers

```json
{
  "job": {
    "url": "https://api.example.com/webhook",
    "enabled": true,
    "title": "Webhook with Headers",
    "extendedData": {
      "headers": {
        "X-API-Key": "your-api-key",
        "Content-Type": "application/json",
        "User-Agent": "MyCronJob/1.0"
      },
      "body": "{\"event\": \"scheduled_check\"}"
    },
    "requestMethod": 1  // 0=GET, 1=POST, 2=PUT, 3=PATCH, 4=DELETE, etc.
  }
}
```

### 7. Job with Failure Notifications

```json
{
  "job": {
    "url": "https://example.com/critical-task",
    "enabled": true,
    "title": "Critical Task",
    "notifications": {
      "onFailure": true,
      "onSuccess": false,
      "onDisable": true
    }
  }
}
```

**Notification Options:**
- `onFailure`: Notify after job fails (set `onFailureMinutes` for threshold)
- `onSuccess`: Notify when job succeeds after previous failure
- `onDisable`: Notify when job is automatically disabled

### 8. Get Job Execution History

```python
import requests

API_KEY = "your_api_key_here"
JOB_ID = 12345

headers = {"Authorization": f"Bearer {API_KEY}"}

response = requests.get(
    f"https://api.cron-job.org/jobs/{JOB_ID}/history",
    headers=headers
)

data = response.json()
print(f"Last {len(data['history'])} executions:")
for item in data['history']:
    print(f"  {item['date']}: Status {item['httpStatus']} ({item['duration']}ms)")

print(f"\nNext executions: {data['predictions']}")
```

**Rate Limit:** 5 requests/second

### 9. Schedule Examples

**Every day at 2:30 AM EST:**
```json
{
  "schedule": {
    "timezone": "America/New_York",
    "hours": [2],
    "mdays": [-1],
    "minutes": [30],
    "months": [-1],
    "wdays": [-1]
  }
}
```

**Every Monday and Friday at 9 AM UTC:**
```json
{
  "schedule": {
    "timezone": "UTC",
    "hours": [9],
    "mdays": [-1],
    "minutes": [0],
    "months": [-1],
    "wdays": [1, 5]  // 0=Sunday, 1=Monday, ..., 6=Saturday
  }
}
```

**Every 15 minutes:**
```json
{
  "schedule": {
    "timezone": "UTC",
    "hours": [-1],
    "mdays": [-1],
    "minutes": [0, 15, 30, 45],
    "months": [-1],
    "wdays": [-1]
  }
}
```

### 10. Delete a Job

```python
import requests

API_KEY = "your_api_key_here"
JOB_ID = 12345

headers = {"Authorization": f"Bearer {API_KEY}"}

response = requests.delete(
    f"https://api.cron-job.org/jobs/{JOB_ID}",
    headers=headers
)

print("Job deleted" if response.status_code == 200 else "Delete failed")
```

**Rate Limit:** 5 requests/second

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **api.md** - Complete REST API reference including:
  - Authentication and security
  - Rate limits and quotas
  - All API endpoints (jobs, history)
  - Request/response formats
  - Object schemas (Job, DetailedJob, JobSchedule, HistoryItem, etc.)
  - HTTP status codes and error handling
  - Timing statistics and performance metrics

Use the reference file for:
- Detailed object schema documentation
- Complete list of request/response fields
- Advanced configuration options
- Troubleshooting API errors

## Working with This Skill

### For Beginners
1. Start by **reading the API authentication section** in `references/api.md`
2. Generate an API key in the Cron-Job.org Console
3. Use the **Quick Reference examples** above to:
   - List your existing jobs
   - Create a simple job with a basic schedule
   - View execution history
4. Test with curl or Python before building integrations

### For Intermediate Users
Focus on:
- **Custom headers and authentication** for API integrations
- **Notification settings** for failure alerting
- **Schedule optimization** using timezone-aware cron expressions
- **Execution history analysis** for monitoring job performance
- **Rate limit management** for high-volume applications

### For Advanced Users
Explore:
- **Batch job management** with proper rate limit handling
- **Performance optimization** using timing statistics from HistoryItem
- **Error handling strategies** based on HTTP status codes
- **IP allowlisting** for production security
- **Sustaining membership** for higher API quotas (5,000 requests/day)

### Navigation Tips
- Use `references/api.md` for complete endpoint documentation
- Check HTTP status codes section for error troubleshooting
- Review object schemas for all available configuration fields
- Reference the schedule examples for common cron patterns

## Common Patterns

### Pattern 1: Health Check Monitoring
Create a job that pings your service every 5 minutes and notifies on failure:

```python
job = {
    "url": "https://myapp.com/health",
    "enabled": True,
    "title": "App Health Check",
    "saveResponses": False,
    "schedule": {
        "timezone": "UTC",
        "hours": [-1],
        "mdays": [-1],
        "minutes": [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55],
        "months": [-1],
        "wdays": [-1]
    },
    "notifications": {
        "onFailure": True,
        "onSuccess": True,
        "onDisable": True
    }
}
```

### Pattern 2: Daily Data Sync
Trigger a webhook at 3 AM daily with custom headers:

```python
job = {
    "url": "https://api.myapp.com/sync",
    "enabled": True,
    "title": "Daily Data Sync",
    "requestMethod": 1,  # POST
    "extendedData": {
        "headers": {
            "X-Sync-Token": "secret",
            "Content-Type": "application/json"
        },
        "body": '{"action": "daily_sync"}'
    },
    "schedule": {
        "timezone": "America/Los_Angeles",
        "hours": [3],
        "mdays": [-1],
        "minutes": [0],
        "months": [-1],
        "wdays": [-1]
    }
}
```

### Pattern 3: Weekday Business Hours Job
Run a job every weekday at 9 AM and 5 PM:

```python
job = {
    "url": "https://example.com/business-task",
    "enabled": True,
    "title": "Business Hours Task",
    "schedule": {
        "timezone": "America/New_York",
        "hours": [9, 17],
        "mdays": [-1],
        "minutes": [0],
        "months": [-1],
        "wdays": [1, 2, 3, 4, 5]  # Monday-Friday
    }
}
```

## HTTP Status Codes

| Code | Description |
|------|-------------|
| 200  | OK - Request succeeded |
| 400  | Bad Request - Invalid request or input data |
| 401  | Unauthorized - Invalid API key |
| 403  | Forbidden - API key cannot be used from this origin |
| 404  | Not Found - Resource doesn't exist |
| 409  | Conflict - Resource already exists |
| 429  | Too Many Requests - Quota or rate limit exceeded |
| 500  | Internal Server Error |

## Important Limits

- **Daily Quota**: 100 requests/day (default), 5,000 requests/day (sustaining members)
- **Job Creation**: 1 request/second, 5 requests/minute
- **Other Endpoints**: 5 requests/second
- **Job Timeout**: Configurable per job (default system timeout applies)
- **Response Storage**: Enable `saveResponses` to store headers/body in history

## Security Best Practices

1. **Protect API Keys**: Treat them like passwords, never commit to version control
2. **Enable IP Restrictions**: Limit API access to specific IP addresses
3. **Use HTTPS**: All API communication is HTTPS-only
4. **Rotate Keys**: Periodically regenerate API keys
5. **Monitor Usage**: Track API request counts to avoid quota exhaustion

## Resources

### Official Documentation
- REST API Docs: https://docs.cron-job.org/rest-api.html
- Console: https://console.cron-job.org/

### Supported Timezones
See the official documentation for a complete list of supported timezone values (e.g., "UTC", "America/New_York", "Europe/London").

### Example Use Cases
- **API Health Checks**: Monitor service availability
- **Data Synchronization**: Trigger scheduled data imports/exports
- **Report Generation**: Generate and send periodic reports
- **Cache Warming**: Pre-load caches before peak traffic
- **Webhook Delivery**: Send scheduled webhook notifications
- **Backup Triggers**: Initiate automated backup processes

## Troubleshooting

### 401 Unauthorized
- Verify API key is correct
- Check Authorization header format: `Authorization: Bearer YOUR_KEY`
- Ensure API key hasn't been revoked

### 403 Forbidden
- Check if IP restrictions are enabled
- Verify your IP address is allowlisted

### 429 Too Many Requests
- Review rate limits for specific endpoint
- Implement exponential backoff
- Consider sustaining membership for higher limits

### Job Not Executing
- Verify job is enabled
- Check schedule configuration
- Review `nextExecution` timestamp
- Check if job has been auto-disabled due to failures

### Missing Response Data in History
- Ensure `saveResponses` is set to `true`
- Use the detailed history item endpoint for headers/body

## Notes

- All timestamps are Unix timestamps in seconds
- Schedule uses arrays where `[-1]` means "all values" (every hour, every day, etc.)
- Job execution times may have jitter (scheduling delay) - check `HistoryItem.jitter`
- Failed jobs may be automatically disabled based on notification settings
- Execution history is limited; use the API to retrieve recent items

## Updating

This skill was generated from official Cron-Job.org documentation. For the latest API changes:
1. Visit https://docs.cron-job.org/rest-api.html
2. Check for new endpoints or schema changes
3. Update your integration code accordingly
