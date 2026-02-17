---
name: greptimedb-trigger
description: Guide for creating GreptimeDB triggers, by which we can trigger external webhook like Alertmanager. This feature can be used as alternative to Prometheus alerting rule.
---

# GreptimeDB Trigger Guide

Create GreptimeDB trigger definition as an alternative to Prometheus alerting
rule. GreptimeDB trigger maps most concepts from Prometheus alert rules in its
own DDL.

## The workflow

To create Greptime trigger, we should follow these phases:

### Phase 1. Understanding GreptimeDB Trigger

First, we should read greptimedb trigger definitions and how it works from
GreptimeDB's documentation.

There are pages available, use WebFetch to load and understand them:

1. High level information of Trigger
   https://docs.greptime.com/enterprise/trigger/
2. The trigger syntax reference
   https://docs.greptime.com/reference/sql/trigger-syntax/

### Phase 2. Create an initial trigger

Create the trigger based on user provided information.

Note that `CREATE TRIGGER` can also use Greptime TQL to define the rule. The TQL
is Greptime's embedded PromQL in SQL, so using TQL makes migration from
Prometheus alert rules easier.

In most case, the query in trigger should use aggregation and `GROUP BY` for
time-series and time window. This is like using SQL to simulate PromQL
behaviour. If possible, we can use PromQL as TQL to simplify the query.

It can be either existing Prometheus alerting rule yaml, or detailed requirements
described by user.


Return the `CREATE TRIGGER` SQL statement, with some dummy data for the webhook
part if user didn't provide webhook information.

### Phase 3. Configure webhook for trigger

If the user already has a Prometheus Alertmanager setup, use their Alertmanager
information for webhook.

## Reference

### Prometheus Alertmanager

Alertmanager is typically configured in `prometheus.yml` like this

```yaml
...
# Alerting specifies settings related to the Alertmanager
alerting:
  alertmanagers:
    - static_configs:
      - targets:
        # Alertmanager's default port is 9093
        - localhost:9093
```

We can use the target for our webhook destination.

### Step-by-step guide

https://greptime.com/blogs/2025-12-23-trigger-quick-start

### Greptime TQL

https://docs.greptime.com/reference/sql/tql/
