---
name: greenhouse-harvest
description: Interface with the Greenhouse Harvest API v3 to query recruitment and hiring data conversationally. Use when the user needs to retrieve or analyze information from their Greenhouse ATS including candidate applications, interview schedules, pipeline metrics, job postings, recruiter performance, or other talent acquisition data. Supports queries like "How many candidates applied this week?", "What status is Jane Smith in?", "How many interviews are booked tomorrow?", "What's the passthrough rate from phone screen to onsite?", and similar conversational requests for recruitment analytics.
---

# Greenhouse Harvest API Integration

## Overview

Query and analyze recruitment data from the Greenhouse Harvest API v3 conversationally. Handle requests for candidate counts, application statuses, interview schedules, pipeline conversions, and other talent acquisition metrics.

## Setup

### Install Dependencies

First, install the required Python packages:

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install requests
```

### Authentication Setup

The Greenhouse Harvest API v3 uses OAuth authentication with client credentials. Set the following environment variables:

```bash
export GREENHOUSE_CLIENT_ID="your-client-id"
export GREENHOUSE_CLIENT_SECRET="your-client-secret"
export GREENHOUSE_USER_ID="your-user-id"  # Optional - defaults to service account
```

**Getting OAuth credentials:**
1. Go to Greenhouse: Configure → Dev Center → API Credential Management
2. Create a new credential and select "Harvest V3 (OAuth)"
3. Copy the Client ID and Client Secret
4. Optionally specify a User ID for the 'sub' parameter (or omit to use auto-generated service account)

## Quick Start

Use the provided Python client for all API interactions:

```python
from greenhouse_client import GreenhouseClient

client = GreenhouseClient()

# List all open jobs
jobs = client.get('/v3/jobs', params={'status': 'open'})

# Get applications for a specific job
applications = client.get_all('/v3/applications', params={'job_id': 12345})

# Get scheduled interviews for this week
interviews = client.get_all('/v3/scheduled_interviews', params={
    'starts_after': '2024-01-15T00:00:00Z',
    'starts_before': '2024-01-22T00:00:00Z'
})
```

The client handles:
- OAuth authentication via environment variables
- Automatic token generation and refresh
- Automatic pagination with `get_all()`
- Rate limiting with exponential backoff
- Error handling and retries

## Common Query Workflows

### Candidate Counting

**User request:** "How many candidates have applied for software engineer this week?"

**Steps:**
1. Find the job by searching job names
2. Calculate the date range (e.g., last 7 days)
3. Query applications filtered by `job_id` and `created_after`
4. Count results

**See:** `references/common_queries.md` → "Candidate Counting Queries" for complete examples

### Candidate Status Lookup

**User request:** "What status is Jane Smith in?"

**Steps:**
1. Search candidates by name (fetch all or filter by `updated_after`)
2. Get their application IDs
3. Fetch each application to get current stage and job

**Note:** Greenhouse lacks direct name search; filter locally or use date ranges to limit scope.

**See:** `references/common_queries.md` → "Candidate Status Lookup" for optimization strategies

### Interview Metrics

**User request:** "How many interviews are booked this week?"

**Steps:**
1. Calculate date range
2. Query `/v3/scheduled_interviews` with `starts_after` and `starts_before`
3. Count and optionally group by day, interviewer, or interview type

**See:** `references/common_queries.md` → "Interview Counting Queries" for examples

### Pipeline Conversion Analysis

**User request:** "What is the passthrough rate from application review to phone screen for the product designer role?"

**Steps:**
1. Find the job by name
2. Get job stages to identify stage IDs and priorities
3. Fetch applications for the job (optionally filter by date range)
4. Count applications that reached each stage based on current_stage priority
5. Calculate conversion rate

**Note:** Greenhouse tracks current stage, not full history. For more accurate data, use scorecards as a proxy for stage completion.

**See:** `references/common_queries.md` → "Pipeline Conversion Analysis" for detailed approaches

### Other Common Queries

The skill supports many other query types:

- **Time-to-hire analysis:** Average days from application to hire
- **Source effectiveness:** Which sources bring the most candidates
- **Recruiter performance:** Candidates sourced by specific recruiters
- **Scorecard analysis:** Average interview ratings

**See:** `references/common_queries.md` for complete patterns and code examples

## When to Use Which Reference

### references/api_endpoints.md

**Use when:** You need to understand what endpoints are available or what parameters/filters they support.

**Contents:**
- All major endpoints organized by category
- Query parameters and filters
- Response structures
- Common response fields
- Pagination and rate limiting details

**Examples:**
- "What filters can I use on the applications endpoint?"
- "How do I search for interviews by date?"
- "What fields are returned in a candidate object?"

### references/schema.md

**Use when:** You need detailed field definitions or relationships between data models.

**Contents:**
- Complete schema for Candidate, Application, Job, Interview, Scorecard, User objects
- Field types and descriptions
- Relationships between objects (via ID references)
- Enum values (application statuses, recommendation levels, etc.)
- Handling null values and timestamps

**Examples:**
- "What does the current_stage field contain?"
- "What are the possible values for application status?"
- "How are candidates linked to applications?"

### references/common_queries.md

**Use when:** You're handling a conversational query and need a complete workflow pattern.

**Contents:**
- Complete code examples for common query types
- Step-by-step workflows
- Performance optimization tips
- Pitfalls and how to avoid them
- Date filtering strategies
- Data aggregation patterns

**Examples:**
- "How do I count candidates for a specific role?"
- "How do I calculate pipeline conversion rates?"
- "How do I handle name searches efficiently?"

## Best Practices

### 1. Filter Data to Reduce Volume

Some endpoints support query filters, while others require client-side filtering:

```python
from datetime import datetime, timedelta

# Endpoints that support date filters (candidates, jobs, etc.)
one_week_ago = (datetime.now() - timedelta(days=7)).isoformat()
candidates = client.get_all('/v3/candidates', params={'created_after': one_week_ago})

# Applications endpoint does NOT support filters - fetch all and filter client-side
all_apps = client.get_all('/v3/applications')
recent_apps = [app for app in all_apps
               if datetime.fromisoformat(app['created_at'].replace('Z', '+00:00')) > datetime.now() - timedelta(days=7)]
```

### 2. Use get_all() for Automatic Pagination

The Greenhouse API uses cursor-based pagination via Link headers. The client handles this automatically:

```python
# Automatically fetches all pages using cursor pagination
all_jobs = client.get_all('/v3/jobs')

# Limit pages for safety during testing
recent = client.get_all('/v3/candidates', max_pages=5)
```

**Note:** The `page` parameter is not supported by the API. Use `get_all()` for pagination or manually follow Link headers.

### 3. Cache Reference Data

Jobs, users, departments, and offices change infrequently. Cache them:

```python
# Fetch once
jobs_cache = {job['id']: job for job in client.get_all('/v3/jobs')}

# Reuse
job_name = jobs_cache[application['job_id']]['name']
```

### 4. Handle Missing Data

Always check for null/missing fields:

```python
stage_name = app['current_stage']['name'] if app.get('current_stage') else 'Unknown'
```

### 5. Consider Time Zones

All Greenhouse timestamps are UTC. Convert for user-facing reports if needed.

## Data Model Relationships

Understanding how objects relate:

```
Candidate
    ├─ has many Applications
    │      ├─ belongs to Job
    │      ├─ has current_stage (Job Stage)
    │      └─ has many Scorecards
    └─ has Recruiter (User)

Job
    ├─ has many Stages
    ├─ belongs to Department
    ├─ belongs to Office
    └─ has Hiring Team (Users)

Scheduled Interview
    ├─ belongs to Application
    ├─ has many Interviewers (Users)
    └─ uses Interview Kit

Scorecard
    ├─ belongs to Application
    ├─ belongs to Interviewer (User)
    └─ has ratings and questions
```

## Troubleshooting

### OAuth Credentials Not Found

```
ValueError: OAuth credentials not provided. Set GREENHOUSE_CLIENT_ID and GREENHOUSE_CLIENT_SECRET environment variables
```

**Solution:** Set the required environment variables:
```bash
export GREENHOUSE_CLIENT_ID="your-client-id"
export GREENHOUSE_CLIENT_SECRET="your-client-secret"
export GREENHOUSE_USER_ID="your-user-id"  # Optional
```

### Authentication Failed

If you receive 401 errors, verify:
- Your Client ID and Client Secret are correct
- Your OAuth credentials have not been rotated (old secrets expire after 1 week)
- Your credentials have the necessary API permissions

### Rate Limiting

The client handles rate limiting automatically with retries and exponential backoff. If you consistently hit limits:
- Use more specific date filters
- Cache reference data
- Use `max_pages` parameter when testing

### Slow Queries

For large organizations, fetching all candidates/applications can be slow:
- Always use `created_after` or `updated_after` filters
- Cache frequently accessed data (jobs, users)
- Use `max_pages` to limit data volume during development

### Missing Stage History

Greenhouse only tracks current stage, not full progression history:
- Use scorecards to infer which stages were completed
- Use the activity feed for detailed progression tracking
- Consider tracking stage changes in your own system for historical analysis

## Resources

### scripts/greenhouse_client.py

Python API client with authentication, pagination, error handling, and rate limiting.

**Import and use:**
```python
from greenhouse_client import GreenhouseClient
client = GreenhouseClient()
```

### references/api_endpoints.md

Comprehensive endpoint documentation organized by resource type.

### references/schema.md

Detailed data models and field definitions for all major objects.

### references/common_queries.md

Complete workflow patterns and code examples for conversational queries.
