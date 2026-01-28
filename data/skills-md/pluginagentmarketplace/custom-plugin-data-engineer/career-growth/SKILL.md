---
name: career-growth
description: Portfolio building, technical interviews, job search strategies, and continuous learning
sasmp_version: "1.3.0"
bonded_agent: 01-data-engineer
bond_type: SUPPORT_BOND
skill_version: "2.0.0"
last_updated: "2025-01"
complexity: foundational
estimated_mastery_hours: 40
prerequisites: []
unlocks: []
---

# Career Growth

Professional development strategies for data engineering career advancement.

## Quick Start

```markdown
# Data Engineer Portfolio Checklist

## Required Projects (Pick 3-5)
- [ ] End-to-end ETL pipeline (Airflow + dbt)
- [ ] Real-time streaming project (Kafka/Spark Streaming)
- [ ] Data warehouse design (Snowflake/BigQuery)
- [ ] ML pipeline with MLOps (MLflow)
- [ ] API for data access (FastAPI)

## Documentation Template
Each project should include:
1. Problem statement
2. Architecture diagram
3. Tech stack justification
4. Challenges & solutions
5. Results/metrics
6. GitHub link with clean code
```

## Core Concepts

### 1. Technical Interview Preparation

```python
# Common coding patterns for data engineering interviews

# 1. SQL Window Functions
"""
Write a query to find the running total of sales by month,
and the percentage change from the previous month.
"""
sql = """
SELECT
    month,
    sales,
    SUM(sales) OVER (ORDER BY month) AS running_total,
    100.0 * (sales - LAG(sales) OVER (ORDER BY month))
        / NULLIF(LAG(sales) OVER (ORDER BY month), 0) AS pct_change
FROM monthly_sales
ORDER BY month;
"""

# 2. Data Processing - Find duplicates
def find_duplicates(data: list[dict], key: str) -> list[dict]:
    """Find duplicate records based on a key."""
    seen = {}
    duplicates = []
    for record in data:
        k = record[key]
        if k in seen:
            duplicates.append(record)
        else:
            seen[k] = record
    return duplicates

# 3. Implement rate limiter
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window = window_seconds
        self.requests = defaultdict(list)

    def is_allowed(self, user_id: str) -> bool:
        now = time.time()
        # Remove old requests
        self.requests[user_id] = [
            t for t in self.requests[user_id]
            if now - t < self.window
        ]
        if len(self.requests[user_id]) < self.max_requests:
            self.requests[user_id].append(now)
            return True
        return False

# 4. Design question: Data pipeline for e-commerce
"""
Requirements:
- Process 1M orders/day
- Real-time dashboard updates
- Historical analytics

Architecture:
1. Ingestion: Kafka for real-time events
2. Processing: Spark Streaming for aggregations
3. Storage: Delta Lake for ACID, Snowflake for analytics
4. Serving: Redis for real-time metrics, API for dashboards
"""
```

### 2. Resume Optimization

```markdown
## Data Engineer Resume Template

### Summary
Data Engineer with X years of experience building scalable data pipelines
processing Y TB/day. Expert in [Spark/Airflow/dbt]. Reduced pipeline
latency by Z% at [Company].

### Experience Format (STAR Method)
**Senior Data Engineer** | Company | 2022-Present
- **Situation**: Legacy ETL system processing 500GB daily with 4-hour latency
- **Task**: Redesign for real-time analytics
- **Action**: Built Spark Streaming pipeline with Delta Lake, implemented
  incremental processing
- **Result**: Reduced latency to 5 minutes, cut infrastructure costs by 40%

### Skills Section
**Languages**: Python, SQL, Scala
**Frameworks**: Spark, Airflow, dbt, Kafka
**Databases**: PostgreSQL, Snowflake, MongoDB, Redis
**Cloud**: AWS (Glue, EMR, S3), GCP (BigQuery, Dataflow)
**Tools**: Docker, Kubernetes, Terraform, Git

### Quantify Everything
- "Built data pipeline" → "Built pipeline processing 2TB/day with 99.9% uptime"
- "Improved performance" → "Reduced query time from 30min to 30sec (60x improvement)"
```

### 3. Interview Questions to Ask

```markdown
## Questions for Data Engineering Interviews

### About the Team
- What does a typical data pipeline look like here?
- How do you handle data quality issues?
- What's the tech stack? Any planned migrations?

### About the Role
- What would success look like in 6 months?
- What's the biggest data challenge the team faces?
- How do data engineers collaborate with data scientists?

### About Engineering Practices
- How do you handle schema changes in production?
- What's your approach to testing data pipelines?
- How do you manage technical debt?

### Red Flags to Watch For
- "We don't have time for testing"
- "One person handles all the data infrastructure"
- "We're still on [very outdated technology]"
- Vague answers about on-call and incident response
```

### 4. Learning Path by Experience Level

```markdown
## Career Progression

### Junior (0-2 years)
Focus Areas:
- SQL proficiency (complex queries, optimization)
- Python for data processing
- One cloud platform deeply (AWS/GCP)
- Git and basic CI/CD
- Understanding ETL patterns

### Mid-Level (2-5 years)
Focus Areas:
- Distributed systems (Spark)
- Data modeling (dimensional, Data Vault)
- Orchestration (Airflow)
- Infrastructure as Code
- Data quality frameworks

### Senior (5+ years)
Focus Areas:
- System design and architecture
- Cost optimization at scale
- Team leadership and mentoring
- Cross-functional collaboration
- Vendor evaluation and selection

### Staff/Principal (8+ years)
Focus Areas:
- Organization-wide data strategy
- Building data platforms
- Technical roadmap ownership
- Industry thought leadership
```

## Resources

### Learning Platforms
- [DataCamp](https://www.datacamp.com/)
- [Coursera Data Engineering](https://www.coursera.org/courses?query=data%20engineering)
- [Zach Wilson's Data Engineering](https://www.youtube.com/@zachphillips)

### Interview Prep
- [LeetCode SQL](https://leetcode.com/problemset/database/)
- [DataLemur](https://datalemur.com/)
- [Interview Query](https://www.interviewquery.com/)

### Community
- [r/dataengineering](https://reddit.com/r/dataengineering)
- [Data Engineering Weekly](https://www.dataengineeringweekly.com/)
- [dbt Community](https://community.getdbt.com/)

### Books
- "Fundamentals of Data Engineering" - Reis & Housley
- "Designing Data-Intensive Applications" - Kleppmann
- "The Data Warehouse Toolkit" - Kimball

## Best Practices

```markdown
# ✅ DO:
- Build public projects on GitHub
- Write technical blog posts
- Contribute to open source
- Network at meetups/conferences
- Keep skills current (follow trends)

# ❌ DON'T:
- Apply without tailoring resume
- Neglect soft skills
- Stop learning after getting hired
- Ignore feedback from interviews
- Burn bridges when leaving jobs
```

---

**Skill Certification Checklist:**
- [ ] Have 3+ portfolio projects on GitHub
- [ ] Can explain system design decisions
- [ ] Can solve SQL problems efficiently
- [ ] Have updated LinkedIn and resume
- [ ] Active in data engineering community
