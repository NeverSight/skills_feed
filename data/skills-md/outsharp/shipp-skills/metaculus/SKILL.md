---
name: metaculus
description: >
  Metaculus is a forecasting platform where users predict outcomes of real-world
  events. Use this skill to interact with the Metaculus API for browsing questions,
  submitting forecasts, reading community predictions, managing comments, and
  downloading forecast data.

metadata:
  author: Outsharp Inc.
  version: 0.1.0

compatibility:
  requirements:
    - Internet access
    - Any HTTP client (curl, Python requests, fetch, etc.)
    - Python 3.7+ with numpy (for continuous CDF generation/standardization)
  notes:
    - All API requests require authentication via a Token in the Authorization header.
    - Requests and responses are JSON (except data download endpoints which return ZIP files).
    - All timestamps are ISO 8601 / RFC 3339 format (e.g. "2024-10-16T12:56:51.751385Z").
    - The feed is composed of Posts; each Post contains a question, group of questions, conditional pair, or notebook.
    - Question types are binary, multiple_choice, numeric, discrete, and date.
    - Probabilities range from 0.0 to 1.0.
    - Continuous forecasts must be submitted as a 201-point CDF array (or shorter for discrete questions).

allowed-tools:
  - Bash(curl:*)
  - Bash(jq:*)
  - Bash(python*:*)
  - Bash(pip*:*)
  - Bash(npm*:*)
  - Bash(npx*:*)

---

# Metaculus API

[Metaculus](https://www.metaculus.com) is a forecasting platform where users predict outcomes of real-world events. Questions range across science, technology, politics, economics, and more. The platform aggregates individual forecasts into community predictions and scores forecasters on accuracy.

Check this skill and the [official API documentation](https://www.metaculus.com/api/) _FREQUENTLY_ for updates.

> **Feedback:** Contact the Metaculus team at [api-requests@metaculus.com](mailto:api-requests@metaculus.com) with questions, ideas, or feedback.

> **Source code & issues:** [github.com/Metaculus/metaculus](https://github.com/Metaculus/metaculus/issues)

---

## Key Concepts (Glossary)

| Term | Definition |
|---|---|
| **Post** | The primary feed entity. A post wraps a question, group of questions, conditional pair, or notebook. Posts have statuses, authors, projects, and comments. |
| **Question** | A single forecastable item within a post. Types: `binary`, `multiple_choice`, `numeric`, `discrete`, `date`. |
| **Group of Questions** | A post containing multiple related sub-questions displayed together (e.g., "What will GDP be in 2025, 2026, 2027?"). |
| **Conditional** | A post with paired questions: "If [condition], what is P(child)?" — produces question_yes and question_no variants. |
| **Forecast** | A user's prediction on a question. Format depends on question type: probability (binary), CDF (continuous), or distribution (multiple choice). |
| **Community Prediction (CP)** | The aggregated forecast from all users, computed via various aggregation methods. |
| **Aggregation Method** | How individual forecasts are combined: `recency_weighted` (default), `unweighted`, `metaculus_prediction`, `single_aggregation`. |
| **Project** | A container for posts — can be a tournament, category, tag, question series, or site section. |
| **Tournament** | A special project type with prize pools, start/close dates, and leaderboards. |
| **Category** | A topic classification (e.g., "Nuclear Technology & Risks", "Health & Pandemics"). |
| **Resolution** | The actual outcome of a question once known. Values vary by type: `yes`/`no` (binary), a number, a date, or an option name. |
| **Curation Status** | Editorial status of a post: `draft`, `pending`, `rejected`, `approved`. |
| **Scaling** | Defines how a continuous question's range maps to the CDF. Includes `range_min`, `range_max`, `zero_point` (for log scale), and bounds. |
| **CDF** | Cumulative Distribution Function — the format for continuous forecasts. A list of 201 floats (or `inbound_outcome_count + 1` for discrete). |
| **Inbound Outcome Count** | Number of possible outcomes within a question's range (excluding out-of-bounds). Default is 200 for continuous; smaller for discrete. |

---

## Base URL

All endpoints are served from:

```
https://www.metaculus.com
```

All paths below are relative to this base (e.g., `GET /api/posts/` means `GET https://www.metaculus.com/api/posts/`).

---

## Authentication

**All API requests require authentication.** Unauthenticated requests are rejected.

### Getting Your Token

1. Log in to [Metaculus](https://www.metaculus.com).
2. Go to your [Account Settings → API Access](https://www.metaculus.com/accounts/settings/account/#api-access).
3. Copy (or generate) your API token.

### Using the Token

Add the `Authorization` header to every request. The token must be prefixed with the literal string `Token` followed by a space:

```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### Example: curl

```bash
curl -s "https://www.metaculus.com/api/posts/?limit=5&order_by=-published_at" \
  -H "Authorization: Token $METACULUS_API_TOKEN" | jq .
```

### Example: Python

```python
import os, requests

TOKEN = os.environ["METACULUS_API_TOKEN"]
HEADERS = {"Authorization": f"Token {TOKEN}"}
BASE = "https://www.metaculus.com"

resp = requests.get(f"{BASE}/api/posts/", headers=HEADERS, params={"limit": 5})
resp.raise_for_status()
data = resp.json()
```

### Environment Variables

Never hardcode tokens. Store them as environment variables or in a `.env` file:

```
METACULUS_API_TOKEN=your-token-here
```

---

## Rate Limits

Metaculus throttles requests to prevent abuse. If you receive a `429 Too Many Requests` response, implement exponential backoff before retrying.

---

## REST API Endpoints Overview

### Feed (Posts)

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `GET` | `/api/posts/` | Retrieve paginated posts feed with filters | Required |
| `GET` | `/api/posts/{postId}/` | Retrieve a single post with full details | Required |

### Questions & Forecasts

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `POST` | `/api/questions/forecast/` | Submit forecasts for one or more questions | Required |
| `POST` | `/api/questions/withdraw/` | Withdraw active forecasts | Required |

### Comments

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `GET` | `/api/comments/` | Retrieve comments (filter by post or author) | Required |
| `POST` | `/api/comments/create/` | Create a new comment on a post | Required |

### Utilities & Data

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `GET` | `/api/posts/{postId}/download-data/` | Download question data as a ZIP of CSVs | Required |
| `GET` | `/api/projects/{projectId}/download-data/` | Download full project data as a ZIP of CSVs | Required (admin/whitelisted) |

---

## Data Model

### Post → Question Hierarchy

A **Post** is the top-level entity in the feed. Each post contains exactly one of:

- `question` — a single question (binary, numeric, date, multiple choice, or discrete)
- `group_of_questions` — multiple related sub-questions
- `conditional` — a conditional pair (condition + child, producing question_yes and question_no)
- A notebook (no question content)

The other fields will be `null`. For example, a post with a single binary question will have `question` populated and `conditional`/`group_of_questions` set to `null`.

### Post

| Field | Type | Description |
|---|---|---|
| `id` | integer | Unique post ID |
| `title` | string | Full title |
| `short_title` | string | URL-friendly short title |
| `slug` | string | URL slug |
| `author_id` | integer | Author's user ID |
| `author_username` | string | Author's username |
| `projects` | object | Associated projects (see below) |
| `created_at` | datetime | When the post was created |
| `published_at` | datetime? | When the post was published |
| `open_time` | datetime? | When the question opened for forecasting |
| `edited_at` | datetime | Last edit timestamp |
| `curation_status` | string | `draft`, `pending`, `rejected`, or `approved` |
| `comment_count` | integer | Number of comments |
| `status` | string | `open`, `upcoming`, `closed`, `resolved`, `draft`, `pending`, `rejected` |
| `nr_forecasters` | integer | Number of unique forecasters |
| `question` | Question? | Single question (if applicable) |
| `conditional` | Conditional? | Conditional pair (if applicable) |
| `group_of_questions` | GroupOfQuestions? | Question group (if applicable) |
| `user_permission` | string | `forecaster` or `viewer` |
| `vote` | object | `{ score: int, user_vote: string? }` |
| `forecasts_count` | integer | Total number of forecasts |

### Post Projects Object

| Field | Type | Description |
|---|---|---|
| `site_main` | Project[] | Site-level project associations |
| `tournament` | Project[] | Tournaments this post belongs to |
| `category` | Category[] | Categories |
| `tag` | Tag[] | Tags |
| `question_series` | Project[] | Question series |
| `default_project` | Project | The post's primary/default project |

### Project

| Field | Type | Description |
|---|---|---|
| `id` | integer | Project ID |
| `type` | string | `site_main`, `tournament`, etc. |
| `name` | string | Display name |
| `slug` | string? | URL slug |
| `prize_pool` | string | Prize pool amount (e.g., "0.00") |
| `start_date` | datetime? | Start date |
| `close_date` | datetime? | Close date |
| `is_ongoing` | boolean? | Whether the project is ongoing |
| `default_permission` | string | Default user permission (e.g., "forecaster") |
| `visibility` | string | `normal`, `not_in_main_feed`, `unlisted` |

### Question

| Field | Type | Description |
|---|---|---|
| `id` | integer | Unique question ID (**used in forecast submissions, not the post ID**) |
| `title` | string | Question title |
| `description` | string | Full description (may be omitted unless `include_descriptions=true`) |
| `type` | string | `binary`, `multiple_choice`, `numeric`, `discrete`, `date` |
| `status` | string | `upcoming`, `open`, `closed`, `resolved` |
| `resolution` | string? | Resolution value (null if unresolved) |
| `resolution_criteria` | string | How the question will be resolved |
| `fine_print` | string | Additional resolution details |
| `created_at` | datetime | Creation timestamp |
| `open_time` | datetime | When forecasting opens |
| `scheduled_close_time` | datetime | When forecasting is scheduled to close |
| `actual_close_time` | datetime | When forecasting actually closed |
| `scheduled_resolve_time` | datetime | When resolution is scheduled |
| `actual_resolve_time` | datetime? | When it was actually resolved |
| `options` | string[] | Current options (multiple choice only) |
| `all_options_ever` | string[] | All options that have ever existed (multiple choice only) |
| `open_upper_bound` | boolean | Whether the upper bound is open |
| `open_lower_bound` | boolean | Whether the lower bound is open |
| `inbound_outcome_count` | integer? | Number of discrete outcomes in range (default 200 for continuous) |
| `unit` | string | Display unit (e.g., "$", "°C") |
| `label` | string? | Label for sub-questions |
| `scaling` | QuestionScaling | Range and scaling parameters |
| `aggregations` | object | Community prediction aggregations (see below) |

### QuestionScaling

| Field | Type | Description |
|---|---|---|
| `range_min` | float? | Lower boundary of the input range |
| `range_max` | float? | Upper boundary of the input range |
| `zero_point` | float? | Log-scale zero point (null = linear scaling) |
| `open_upper_bound` | boolean? | Whether upper bound is open |
| `open_lower_bound` | boolean? | Whether lower bound is open |
| `inbound_outcome_count` | integer? | Number of outcomes within range |
| `continuous_range` | string[]? | Real-value locations where the CDF is evaluated |

### Aggregations

Each question includes an `aggregations` object with up to four methods:

- `recency_weighted` — Default; weights recent forecasts more heavily
- `unweighted` — Equal weight for all forecasts
- `metaculus_prediction` — Metaculus's proprietary prediction
- `single_aggregation` — Beta; admin-only

Each method contains:

| Field | Type | Description |
|---|---|---|
| `history` | object[] | Time series of aggregated forecasts |
| `latest` | object? | Most recent aggregated forecast |
| `score_data` | object? | Scoring information |

Each history/latest entry contains:

| Field | Type | Description |
|---|---|---|
| `start_time` | datetime | When this aggregation period started |
| `end_time` | datetime? | When this aggregation period ended |
| `forecast_values` | float[] | The aggregated forecast (probability for binary, CDF for continuous) |
| `forecaster_count` | integer | Number of contributing forecasters |
| `centers` | float[] | Median/center values |
| `interval_lower_bounds` | float[] | Lower confidence bounds |
| `interval_upper_bounds` | float[] | Upper confidence bounds |
| `means` | float? | Mean values |

### Conditional

| Field | Type | Description |
|---|---|---|
| `id` | integer | Conditional ID |
| `condition` | Question | The condition question |
| `condition_child` | Question | The child question |
| `question_yes` | Question | "If condition = Yes" variant |
| `question_no` | Question | "If condition = No" variant |

### GroupOfQuestions

| Field | Type | Description |
|---|---|---|
| `id` | integer | Group ID |
| `description` | string | Group description |
| `resolution_criteria` | string | Resolution criteria |
| `fine_print` | string | Additional details |
| `group_variable` | string | The variable that differs across sub-questions |
| `graph_type` | string | `multiple_choice_graph` or `fan_graph` |
| `questions` | Question[] | The sub-questions |

### Comment

| Field | Type | Description |
|---|---|---|
| `id` | integer | Comment ID |
| `author` | object | `{ id, username, is_bot, is_staff }` |
| `parent_id` | integer? | Parent comment ID (for replies) |
| `root_id` | integer? | Root comment ID in thread |
| `created_at` | datetime | Creation timestamp |
| `text` | string | Comment content |
| `on_post` | integer | Post ID the comment belongs to |
| `included_forecast` | boolean | Whether the user's last forecast is included |
| `is_private` | boolean | Whether the comment is private |
| `vote_score` | integer | Total vote score |
| `user_vote` | integer | Current user's vote (-1, 0, 1) |

---

## Endpoints: Detailed Reference

### GET /api/posts/ — Retrieve Posts Feed

Returns a paginated list of posts with extensive filtering and sorting.

**Query Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `limit` | integer | Page size (default varies) |
| `offset` | integer | Pagination offset |
| `tournaments` | string[] | Filter by tournament slugs (e.g., `metaculus-cup`, `aibq3`) |
| `statuses` | string[] | Filter by status: `upcoming`, `closed`, `resolved`, `open` |
| `forecast_type` | string[] | Filter by type: `binary`, `multiple_choice`, `numeric`, `discrete`, `date`, `conditional`, `group_of_questions`, `notebook` |
| `categories` | string[] | Filter by category slugs (e.g., `nuclear`, `health-pandemics`) |
| `forecaster_id` | integer | Posts where this user has forecasted |
| `not_forecaster_id` | integer | Posts where this user has NOT forecasted |
| `for_main_feed` | boolean | Filter for main feed suitability |
| `with_cp` | boolean | Include community predictions (default: `false`). For groups, returns CP for top 3 sub-questions only. |
| `include_cp_history` | boolean | Include full CP history per aggregation method (default: `false`) |
| `include_descriptions` | boolean | Include `description`, `fine_print`, `resolution_criteria` fields |
| `order_by` | string | Sort field. Prefix with `-` for descending. Options below. |
| `open_time__gt` | datetime | Open time greater than (also supports `__gte`, `__lt`, `__lte`) |
| `published_at__gt` | datetime | Published time greater than (also supports `__gte`, `__lt`, `__lte`) |
| `scheduled_resolve_time__gt` | datetime | Scheduled resolve time greater than (also supports `__gte`, `__lt`, `__lte`) |

**`order_by` options:**

| Value | Description |
|---|---|
| `published_at` | Publication time |
| `open_time` | When forecasting opened |
| `vote_score` | Community vote score |
| `comment_count` | Number of comments |
| `forecasts_count` | Number of forecasts |
| `scheduled_close_time` | Scheduled close time |
| `scheduled_resolve_time` | Scheduled resolution time |
| `user_last_forecasts_date` | When the user last forecasted |
| `unread_comment_count` | Unread comments |
| `weekly_movement` | Weekly probability movement |
| `divergence` | Divergence metric |
| `hotness` | Composite trending score (decays after 3.5 days) |
| `score` | User forecasting performance (**requires** `forecaster_id`) |

**Response:**

```json
{
  "next": "https://www.metaculus.com/api/posts/?limit=20&offset=20",
  "previous": null,
  "results": [ /* array of Post objects */ ]
}
```

**Example: Fetch open binary questions, newest first:**

```bash
curl -s "https://www.metaculus.com/api/posts/?statuses=open&forecast_type=binary&order_by=-published_at&limit=10&with_cp=true" \
  -H "Authorization: Token $METACULUS_API_TOKEN" | jq '.results[] | {id, title, status}'
```

**Example: Fetch questions from a tournament:**

```bash
curl -s "https://www.metaculus.com/api/posts/?tournaments=metaculus-cup&with_cp=true&limit=20" \
  -H "Authorization: Token $METACULUS_API_TOKEN" | jq .
```

**Example: Fetch questions you haven't forecasted on yet:**

```bash
# Replace YOUR_USER_ID with your actual Metaculus user ID
curl -s "https://www.metaculus.com/api/posts/?not_forecaster_id=YOUR_USER_ID&statuses=open&limit=10" \
  -H "Authorization: Token $METACULUS_API_TOKEN" | jq .
```

---

### GET /api/posts/{postId}/ — Retrieve Post Details

Returns full details for a single post, including all sub-questions and aggregations.

**Path Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `postId` | integer | The post ID |

**Example:**

```bash
curl -s "https://www.metaculus.com/api/posts/12345/" \
  -H "Authorization: Token $METACULUS_API_TOKEN" | jq .
```

---

### POST /api/questions/forecast/ — Submit Forecasts

Submit one or more forecasts. The request body is a **JSON array** of forecast objects.

> **Important:** The `question` field takes the **question ID**, not the post ID. Get the question ID from `post.question.id`, `post.group_of_questions.questions[].id`, or `post.conditional.question_yes.id` / `post.conditional.question_no.id`.

#### Binary Forecast

```json
[
  {
    "question": 12345,
    "probability_yes": 0.63
  }
]
```

| Field | Type | Required | Description |
|---|---|---|---|
| `question` | integer | Yes | Question ID |
| `probability_yes` | float | Yes | Probability between 0 and 1 |
| `end_time` | datetime | No | Auto-withdraw timestamp |

#### Multiple Choice Forecast

```json
[
  {
    "question": 12345,
    "probability_yes_per_category": {
      "Futurama": 0.5,
      "Paperclipalypse": 0.3,
      "Singularia": 0.2
    }
  }
]
```

| Field | Type | Required | Description |
|---|---|---|---|
| `question` | integer | Yes | Question ID |
| `probability_yes_per_category` | object | Yes | Map of option name → probability. **Must sum to 1.0.** |
| `end_time` | datetime | No | Auto-withdraw timestamp |

#### Continuous Forecast (Numeric / Date / Discrete)

```json
[
  {
    "question": 12345,
    "continuous_cdf": [0.0, 0.00005, 0.00010, "... 201 values total ...", 1.0]
  }
]
```

| Field | Type | Required | Description |
|---|---|---|---|
| `question` | integer | Yes | Question ID |
| `continuous_cdf` | float[] | Yes | CDF array (see CDF generation section below) |
| `distribution_input` | object | No | Slider values for frontend display |
| `end_time` | datetime | No | Auto-withdraw timestamp |

#### Conditional Forecast

Submit forecasts for both the "if Yes" and "if No" questions:

```json
[
  { "question": 111, "probability_yes": 0.499 },
  { "question": 222, "probability_yes": 0.501 }
]
```

Where `111` is `conditional.question_yes.id` and `222` is `conditional.question_no.id`.

#### Group Forecast

Submit forecasts for multiple sub-questions in a single request:

```json
[
  { "question": 1, "probability_yes": 0.11 },
  { "question": 2, "probability_yes": 0.22 },
  { "question": 3, "probability_yes": 0.33 }
]
```

**Example: Submit a binary forecast with curl:**

```bash
curl -s -X POST "https://www.metaculus.com/api/questions/forecast/" \
  -H "Authorization: Token $METACULUS_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '[{"question": 12345, "probability_yes": 0.75}]'
```

**Responses:**

| Status | Description |
|---|---|
| `201` | Forecasts submitted successfully |
| `400` | Invalid request format |

---

### POST /api/questions/withdraw/ — Withdraw Forecasts

Withdraw active forecasts. The request body is a JSON array of withdrawal objects.

```json
[
  { "question": 12345 },
  { "question": 12346 }
]
```

**Example:**

```bash
curl -s -X POST "https://www.metaculus.com/api/questions/withdraw/" \
  -H "Authorization: Token $METACULUS_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '[{"question": 12345}]'
```

---

### GET /api/comments/ — Retrieve Comments

Fetch comments with filters. **Either `post` or `author` is required.**

**Query Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `post` | integer | One of post/author | Post ID to filter by |
| `author` | integer | One of post/author | Author user ID to filter by |
| `limit` | integer | No | Number of comments to retrieve |
| `offset` | integer | No | Pagination offset |
| `is_private` | boolean | No | Filter private vs public (default: `false`) |
| `use_root_comments_pagination` | boolean | No | If `true`, pagination applies to root comments only; all child comments are included |
| `sort` | string | No | `created_at` (ascending) or `-created_at` (descending) |
| `focus_comment_id` | integer | No | Place this comment at the top of results |

**Response:**

```json
{
  "total_count": 42,
  "count": 15,
  "next": "https://www.metaculus.com/api/comments/?post=123&limit=10&offset=10",
  "previous": null,
  "results": [ /* array of Comment objects */ ]
}
```

- `total_count` — Total root + child comments
- `count` — Total root comments only

**Example:**

```bash
curl -s "https://www.metaculus.com/api/comments/?post=12345&sort=-created_at&limit=20" \
  -H "Authorization: Token $METACULUS_API_TOKEN" | jq .
```

---

### POST /api/comments/create/ — Create a Comment

**Request Body:**

| Field | Type | Required | Description |
|---|---|---|---|
| `on_post` | integer | Yes | Post ID to comment on |
| `text` | string | Yes | Comment content |
| `included_forecast` | boolean | Yes | Include the user's last forecast |
| `is_private` | boolean | Yes | Whether the comment is private |
| `parent` | integer | No | Parent comment ID (for replies) |

**Example:**

```bash
curl -s -X POST "https://www.metaculus.com/api/comments/create/" \
  -H "Authorization: Token $METACULUS_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "on_post": 12345,
    "text": "I updated my forecast based on the latest data.",
    "included_forecast": false,
    "is_private": false
  }'
```

**Responses:**

| Status | Description |
|---|---|
| `201` | Comment created successfully (returns Comment object) |
| `400` | Invalid request format |

---

### GET /api/posts/{postId}/download-data/ — Download Question Data

Downloads forecast data as a ZIP file containing CSVs.

**Path Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `postId` | integer | Post ID (the number after `/questions/` in the URL) |

**Query Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `sub_question` | integer | No | Sub-question ID for group/conditional questions |
| `aggregation_methods` | string[] | No | Methods to include: `recency_weighted`, `unweighted`, `metaculus_prediction`, `single_aggregation`. Default: `recency_weighted` only |
| `include_bots` | boolean | No | Include bot forecasts in aggregation recalculation |
| `user_ids` | string[] | No | Specific user IDs (whitelisted users only). Requires `aggregation_methods`. |
| `minimize` | boolean | No | Default: `true`. If `false`, includes all data points (may produce large files) |
| `include_comments` | boolean | No | Default: `false`. If `true`, adds `comment_data.csv` |
| `include_scores` | boolean | No | Default: `false`. If `true`, adds `score_data.csv` |

**ZIP Contents:**

| File | Description |
|---|---|
| `question_data.csv` | Question metadata, scaling, resolution |
| `forecast_data.csv` | Individual and aggregated forecasts |
| `comment_data.csv` | Comments (if `include_comments=true`) |
| `score_data.csv` | Scores (if `include_scores=true`) |

**Example:**

```bash
curl -s "https://www.metaculus.com/api/posts/12345/download-data/?include_comments=true" \
  -H "Authorization: Token $METACULUS_API_TOKEN" \
  -o question_data.zip
```

---

### GET /api/projects/{projectId}/download-data/ — Download Project Data

Downloads data for an entire project as a ZIP. **Only available to site admins and whitelisted users.**

**Path Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `projectId` | integer | Project ID |

**Query Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `include_comments` | boolean | No | Include comments CSV |
| `include_scores` | boolean | No | Include scores CSV |

---

## Generating Continuous CDFs

Continuous, numeric, date, and discrete questions require forecasts as a CDF (Cumulative Distribution Function). This section explains how to generate valid CDFs.

### CDF Rules

1. **Length:** The CDF must have exactly `inbound_outcome_count + 1` values. For most continuous questions, this is **201** values. For discrete questions, it depends on the question.

2. **Bounds:**
   - If `open_lower_bound == false` (closed): first value **must be 0.0**
   - If `open_lower_bound == true` (open): first value **must be ≥ 0.001** (at least 0.1% mass below lower bound)
   - If `open_upper_bound == false` (closed): last value **must be 1.0**
   - If `open_upper_bound == true` (open): last value **must be ≤ 0.999** (at least 0.1% mass above upper bound)

3. **Monotonicity:** The CDF must be strictly increasing by at least `0.01 / inbound_outcome_count` per step (i.e., `0.00005` per step for the standard 200).

4. **Maximum step:** No two adjacent values may differ by more than `0.2 * (200 / inbound_outcome_count)`.

### Understanding Scaling

The CDF values correspond to evenly spaced points across the **internal** [0, 1] range. To map real-world values to CDF positions:

- **Linear scaling** (`zero_point` is `null`): `internal = (value - range_min) / (range_max - range_min)`
- **Logarithmic scaling** (`zero_point` is set): requires log transformation (see function below)
- **Date questions**: convert ISO dates to unix timestamps first, then apply scaling

### Python: Nominal Value to CDF Location

```python
import datetime
import numpy as np

def nominal_location_to_cdf_location(
    nominal_location: str | float,
    question_data: dict,
) -> float:
    """Takes a location in nominal format (e.g. 123, "123",
    or datetime in iso format) and scales it to metaculus's
    "internal representation" range [0,1] incorporating question scaling"""
    if question_data["type"] == "date":
        scaled_location = datetime.datetime.fromisoformat(
            nominal_location
        ).timestamp()
    else:
        scaled_location = float(nominal_location)
    scaling = question_data["scaling"]
    range_min = scaling.get("range_min")
    range_max = scaling.get("range_max")
    zero_point = scaling.get("zero_point")
    if zero_point is not None:
        # logarithmically scaled question
        deriv_ratio = (range_max - zero_point) / (range_min - zero_point)
        unscaled_location = (
            np.log(
                (scaled_location - range_min) * (deriv_ratio - 1)
                + (range_max - range_min)
            )
            - np.log(range_max - range_min)
        ) / np.log(deriv_ratio)
    else:
        # linearly scaled question
        unscaled_location = (scaled_location - range_min) / (
            range_max - range_min
        )
    return unscaled_location
```

### Python: Generate CDF from Percentiles

```python
def generate_continuous_cdf(
    percentiles: dict,
    question_data: dict,
    below_lower_bound: float = None,
    above_upper_bound: float = None,
) -> list[float]:
    """
    Takes a set of percentiles and returns a corresponding CDF with
    inbound_outcome_count + 1 values (typically 201).

    percentiles: dict mapping percentile keys to nominal values
      Keys must end in a number interpretable as a float in (0, 100).
      Values are in the question's real-world scale.
      Example:
        {
          "percentile_05": 25,
          "percentile_25": 500,
          "percentile_50": 650,
          "percentile_75": 700,
          "percentile_95": 990,
        }

    below_lower_bound: probability mass below range_min (for open lower bound)
    above_upper_bound: probability mass above range_max (for open upper bound)
    """
    percentile_locations = []
    if below_lower_bound is not None:
        percentile_locations.append((0.0, below_lower_bound))
    if above_upper_bound is not None:
        percentile_locations.append((1.0, 1 - above_upper_bound))
    for percentile, nominal_location in percentiles.items():
        height = float(str(percentile).split("_")[-1]) / 100
        location = nominal_location_to_cdf_location(
            nominal_location, question_data
        )
        percentile_locations.append((location, height))
    percentile_locations.sort()
    first_point, last_point = percentile_locations[0], percentile_locations[-1]
    if (first_point[0] > 0.0) or (last_point[0] < 1.0):
        raise ValueError(
            "Percentiles must encompass bounds of the question"
        )

    def get_cdf_at(location):
        previous = percentile_locations[0]
        for i in range(1, len(percentile_locations)):
            current = percentile_locations[i]
            if previous[0] <= location <= current[0]:
                return previous[1] + (current[1] - previous[1]) * (
                    location - previous[0]
                ) / (current[0] - previous[0])
            previous = current

    n_points = (question_data.get("inbound_outcome_count") or 200) + 1
    continuous_cdf = [get_cdf_at(i / (n_points - 1)) for i in range(n_points)]
    return continuous_cdf
```

### Python: Standardize CDF for Submission

This function ensures your CDF satisfies all validation rules. It adds a small linear component to guarantee monotonicity and respects bound constraints.

```python
def standardize_cdf(cdf, question_data: dict):
    """
    Standardize a CDF for submission:
    - No mass outside closed bounds
    - Minimum mass outside open bounds
    - Strictly increasing by at least the minimum step
    - Caps maximum step size
    """
    lower_open = question_data["open_lower_bound"]
    upper_open = question_data["open_upper_bound"]
    inbound_outcome_count = question_data.get("inbound_outcome_count") or 200
    default_inbound_outcome_count = 200

    cdf = np.asarray(cdf, dtype=float)
    if not cdf.size:
        return []

    scale_lower_to = 0 if lower_open else cdf[0]
    scale_upper_to = 1.0 if upper_open else cdf[-1]
    rescaled_inbound_mass = scale_upper_to - scale_lower_to

    def standardize(F: float, location: float) -> float:
        rescaled_F = (F - scale_lower_to) / rescaled_inbound_mass
        if lower_open and upper_open:
            return 0.988 * rescaled_F + 0.01 * location + 0.001
        elif lower_open:
            return 0.989 * rescaled_F + 0.01 * location + 0.001
        elif upper_open:
            return 0.989 * rescaled_F + 0.01 * location
        return 0.99 * rescaled_F + 0.01 * location

    for i, value in enumerate(cdf):
        cdf[i] = standardize(value, i / (len(cdf) - 1))

    pmf = np.diff(cdf, prepend=0, append=1)
    cap = 0.2 * (default_inbound_outcome_count / inbound_outcome_count)

    def cap_pmf(scale: float) -> np.ndarray:
        return np.concatenate(
            [pmf[:1], np.minimum(cap, scale * pmf[1:-1]), pmf[-1:]]
        )

    def capped_sum(scale: float) -> float:
        return float(cap_pmf(scale).sum())

    lo = hi = scale = 1.0
    while capped_sum(hi) < 1.0:
        hi *= 1.2
    for _ in range(100):
        scale = 0.5 * (lo + hi)
        s = capped_sum(scale)
        if s < 1.0:
            lo = scale
        else:
            hi = scale
        if s == 1.0 or (hi - lo) < 2e-5:
            break

    pmf = cap_pmf(scale)
    pmf[1:-1] *= (cdf[-1] - cdf[0]) / pmf[1:-1].sum()
    cdf = np.cumsum(pmf)[:-1]
    cdf = np.round(cdf, 10)
    return cdf.tolist()
```

### End-to-End Example: Submit a Continuous Forecast

```python
import os, requests, numpy as np

TOKEN = os.environ["METACULUS_API_TOKEN"]
HEADERS = {"Authorization": f"Token {TOKEN}"}
BASE = "https://www.metaculus.com"

# 1. Fetch the question
post_id = 12345
resp = requests.get(f"{BASE}/api/posts/{post_id}/", headers=HEADERS)
resp.raise_for_status()
post = resp.json()
question = post["question"]

# 2. Define your percentile beliefs (in real-world units)
percentiles = {
    "percentile_05": 25,
    "percentile_25": 40,
    "percentile_50": 55,
    "percentile_75": 70,
    "percentile_95": 90,
}

# 3. Generate and standardize the CDF
raw_cdf = generate_continuous_cdf(
    percentiles,
    question,
    below_lower_bound=0.01,
    above_upper_bound=0.01,
)
final_cdf = standardize_cdf(raw_cdf, question)

# 4. Submit
resp = requests.post(
    f"{BASE}/api/questions/forecast/",
    headers={**HEADERS, "Content-Type": "application/json"},
    json=[{"question": question["id"], "continuous_cdf": final_cdf}],
)
resp.raise_for_status()
print("Forecast submitted!")
```

---

## Common Patterns

### Browse the Feed

```bash
# Newest open questions
curl -s "https://www.metaculus.com/api/posts/?statuses=open&order_by=-published_at&limit=10&with_cp=true" \
  -H "Authorization: Token $METACULUS_API_TOKEN" | jq '.results[] | {id, title, status}'
```

### Get Community Prediction for a Post

```bash
curl -s "https://www.metaculus.com/api/posts/12345/" \
  -H "Authorization: Token $METACULUS_API_TOKEN" \
  | jq '.question.aggregations.recency_weighted.latest'
```

### Find Trending Questions

```bash
curl -s "https://www.metaculus.com/api/posts/?order_by=-hotness&statuses=open&limit=10&with_cp=true" \
  -H "Authorization: Token $METACULUS_API_TOKEN" | jq '.results[] | {id, title}'
```

### Find Questions by Category

```bash
curl -s "https://www.metaculus.com/api/posts/?categories=nuclear&statuses=open&with_cp=true&limit=10" \
  -H "Authorization: Token $METACULUS_API_TOKEN" | jq '.results[] | {id, title}'
```

### Find Questions in a Tournament

```bash
curl -s "https://www.metaculus.com/api/posts/?tournaments=aibq3&with_cp=true&limit=50" \
  -H "Authorization: Token $METACULUS_API_TOKEN" | jq '.results[] | {id, title, status}'
```

### Submit a Binary Forecast

```bash
curl -s -X POST "https://www.metaculus.com/api/questions/forecast/" \
  -H "Authorization: Token $METACULUS_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '[{"question": 12345, "probability_yes": 0.75}]'
```

### Submit a Multiple Choice Forecast

```bash
curl -s -X POST "https://www.metaculus.com/api/questions/forecast/" \
  -H "Authorization: Token $METACULUS_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '[{
    "question": 12345,
    "probability_yes_per_category": {
      "Option A": 0.4,
      "Option B": 0.35,
      "Option C": 0.25
    }
  }]'
```

### Withdraw a Forecast

```bash
curl -s -X POST "https://www.metaculus.com/api/questions/withdraw/" \
  -H "Authorization: Token $METACULUS_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '[{"question": 12345}]'
```

### Read Comments on a Post

```bash
curl -s "https://www.metaculus.com/api/comments/?post=12345&sort=-created_at&limit=20" \
  -H "Authorization: Token $METACULUS_API_TOKEN" | jq '.results[] | {author: .author.username, text: .text}'
```

### Post a Comment

```bash
curl -s -X POST "https://www.metaculus.com/api/comments/create/" \
  -H "Authorization: Token $METACULUS_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "on_post": 12345,
    "text": "My analysis suggests a higher probability because...",
    "included_forecast": true,
    "is_private": false
  }'
```

### Reply to a Comment

```bash
curl -s -X POST "https://www.metaculus.com/api/comments/create/" \
  -H "Authorization: Token $METACULUS_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "on_post": 12345,
    "parent": 67890,
    "text": "Good point — I updated my forecast accordingly.",
    "included_forecast": false,
    "is_private": false
  }'
```

### Python: Paginate Through All Open Questions

```python
import os, requests

TOKEN = os.environ["METACULUS_API_TOKEN"]
HEADERS = {"Authorization": f"Token {TOKEN}"}
BASE = "https://www.metaculus.com"

all_posts = []
offset = 0
limit = 100

while True:
    resp = requests.get(
        f"{BASE}/api/posts/",
        headers=HEADERS,
        params={
            "statuses": "open",
            "limit": limit,
            "offset": offset,
            "with_cp": True,
        },
    )
    resp.raise_for_status()
    data = resp.json()
    results = data["results"]
    all_posts.extend(results)
    if data["next"] is None:
        break
    offset += limit

print(f"Fetched {len(all_posts)} open posts")
```

### Python: Find Questions with Large Movement

```python
import os, requests

TOKEN = os.environ["METACULUS_API_TOKEN"]
HEADERS = {"Authorization": f"Token {TOKEN}"}
BASE = "https://www.metaculus.com"

resp = requests.get(
    f"{BASE}/api/posts/",
    headers=HEADERS,
    params={
        "statuses": "open",
        "order_by": "-weekly_movement",
        "forecast_type": "binary",
        "with_cp": True,
        "limit": 10,
    },
)
resp.raise_for_status()
for post in resp.json()["results"]:
    q = post.get("question")
    if q and q.get("aggregations"):
        latest = q["aggregations"].get("recency_weighted", {}).get("latest")
        if latest:
            prob = latest.get("centers", [None])[0]
            print(f"[{post['id']}] {post['title']} — CP: {prob}")
```

---

## Question Type Quick Reference

| Type | Forecast Format | Key Fields |
|---|---|---|
| `binary` | `probability_yes: float` (0–1) | — |
| `multiple_choice` | `probability_yes_per_category: {option: float}` (sum = 1.0) | `options`, `all_options_ever` |
| `numeric` | `continuous_cdf: float[]` (201 values) | `scaling`, `open_lower_bound`, `open_upper_bound`, `unit` |
| `date` | `continuous_cdf: float[]` (201 values) | `scaling` (range_min/max are unix timestamps) |
| `discrete` | `continuous_cdf: float[]` (`inbound_outcome_count + 1` values) | `inbound_outcome_count`, `scaling` |

---

## Post Status Lifecycle

```
draft → pending → approved → open → closed → resolved
                → rejected
```

| Status | Description |
|---|---|
| `draft` | Author is still editing |
| `pending` | Submitted for curation review |
| `rejected` | Rejected by curators |
| `open` | Approved and accepting forecasts |
| `upcoming` | Approved but not yet open for forecasting |
| `closed` | No longer accepting forecasts; awaiting resolution |
| `resolved` | Final outcome determined |

---

## Error Handling

| Status Code | Meaning | Action |
|---|---|---|
| `200` | Success | — |
| `201` | Created | — |
| `400` | Bad request | Check request format, CDF validity, required fields |
| `401` | Unauthorized | Check your `Authorization: Token ...` header |
| `403` | Forbidden | You don't have permission (e.g., project data download) |
| `404` | Not found | Check the post/question/project ID |
| `429` | Rate limited | Implement exponential backoff and retry |
| `500` | Server error | Retry after a delay; if persistent, contact Metaculus |

---

## Usage Tips

- **Always pass `with_cp=true`** when listing posts if you need community predictions — aggregations are empty by default.
- **Use `include_cp_history=true`** only when you need historical CP data — it increases response size significantly.
- **Use `include_descriptions=true`** only when needed — descriptions can be large.
- **Question ID ≠ Post ID** — Forecasts use the `question.id`, not the `post.id`. Always fetch the post first to get the question ID.
- **For group posts**, `with_cp=true` on the list endpoint only returns CP for the top 3 sub-questions. Use the detail endpoint (`/api/posts/{postId}/`) for all sub-questions.
- **CDF generation is the trickiest part** — use the provided Python functions or adapt them. Always run `standardize_cdf()` before submitting.
- **Combine filters** for targeted queries — e.g., `statuses=open&forecast_type=binary&categories=nuclear` narrows results efficiently.
- **Paginate responsibly** — use `limit` and `offset`. Don't fetch all posts at once.
- **The `order_by=score` sort requires `forecaster_id`** — it ranks questions by a specific user's performance.
- **Date questions use unix timestamps** in `scaling.range_min` and `scaling.range_max` — convert ISO dates to timestamps before mapping to CDF locations.
- **Respect rate limits** — implement backoff when you receive 429 responses.

---

## Resources

| Resource | URL |
|---|---|
| Metaculus Platform | [metaculus.com](https://www.metaculus.com) |
| API Documentation | [metaculus.com/api](https://www.metaculus.com/api/) |
| Account Settings (API Token) | [metaculus.com/accounts/settings](https://www.metaculus.com/accounts/settings/account/#api-access) |
| GitHub Issues | [github.com/Metaculus/metaculus](https://github.com/Metaculus/metaculus/issues) |
| Contact | [api-requests@metaculus.com](mailto:api-requests@metaculus.com) |