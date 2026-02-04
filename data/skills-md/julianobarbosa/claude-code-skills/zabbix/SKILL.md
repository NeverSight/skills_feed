---
name: zabbix
description: "Zabbix monitoring system automation via API and Python. Use when: (1) Managing hosts, templates, items, triggers, or host groups, (2) Automating monitoring configuration, (3) Sending data via Zabbix trapper/sender, (4) Querying historical data or events, (5) Bulk operations on Zabbix objects, (6) Maintenance window management, (7) User/permission management"
license: MIT
---

# Zabbix Automation Skill

## Overview

This skill provides guidance for automating Zabbix monitoring operations via the API and official Python library `zabbix_utils`.

## Quick Start

### Installation

```bash
pip install zabbix-utils --break-system-packages
```

### Authentication

```python
from zabbix_utils import ZabbixAPI

# Option 1: Username/password
api = ZabbixAPI(url="https://zabbix.example.com")
api.login(user="Admin", password="zabbix")

# Option 2: API token (Zabbix 5.4+, preferred)
api = ZabbixAPI(url="https://zabbix.example.com")
api.login(token="your_api_token")

# Verify connection
print(api.api_version())
```

### Environment Variables Pattern

```python
import os
from zabbix_utils import ZabbixAPI

api = ZabbixAPI(url=os.environ.get("ZABBIX_URL", "http://localhost/zabbix"))
api.login(token=os.environ["ZABBIX_TOKEN"])
```

## Core API Methods

All APIs follow pattern: `api.<object>.<method>()` with methods: `get`, `create`, `update`, `delete`.

### Host Operations

```python
# Get hosts
hosts = api.host.get(output=["hostid", "host", "name"],
                     selectInterfaces=["ip"])

# Create host
api.host.create(
    host="server01",
    groups=[{"groupid": "2"}],  # Linux servers
    interfaces=[{
        "type": 1,  # 1=agent, 2=SNMP, 3=IPMI, 4=JMX
        "main": 1,
        "useip": 1,
        "ip": "192.168.1.100",
        "dns": "",
        "port": "10050"
    }],
    templates=[{"templateid": "10001"}]
)

# Update host
api.host.update(hostid="10084", status=0)  # 0=enabled, 1=disabled

# Delete host
api.host.delete("10084")
```

### Template Operations

```python
# Get templates
templates = api.template.get(output=["templateid", "host", "name"],
                             selectHosts=["hostid", "name"])

# Link template to host
api.host.update(hostid="10084",
                templates=[{"templateid": "10001"}])

# Import template from XML
with open("template.xml") as f:
    api.configuration.import_(
        source=f.read(),
        format="xml",
        rules={
            "templates": {"createMissing": True, "updateExisting": True},
            "items": {"createMissing": True, "updateExisting": True},
            "triggers": {"createMissing": True, "updateExisting": True}
        }
    )
```

### Item Operations

```python
# Get items
items = api.item.get(hostids="10084",
                     output=["itemid", "name", "key_"],
                     search={"key_": "system.cpu"})

# Create item
api.item.create(
    name="CPU Load",
    key_="system.cpu.load[percpu,avg1]",
    hostid="10084",
    type=0,  # 0=Zabbix agent
    value_type=0,  # 0=float, 3=integer, 4=text
    delay="30s",
    interfaceid="1"
)
```

### Trigger Operations

```python
# Get triggers
triggers = api.trigger.get(hostids="10084",
                          output=["triggerid", "description", "priority"],
                          selectFunctions="extend")

# Create trigger
api.trigger.create(
    description="High CPU on {HOST.NAME}",
    expression="last(/server01/system.cpu.load[percpu,avg1])>5",
    priority=3  # 0=not classified, 1=info, 2=warning, 3=average, 4=high, 5=disaster
)
```

### Host Group Operations

```python
# Get groups
groups = api.hostgroup.get(output=["groupid", "name"])

# Create group
api.hostgroup.create(name="Production/Web Servers")

# Add hosts to group
api.hostgroup.massadd(groups=[{"groupid": "5"}],
                      hosts=[{"hostid": "10084"}])
```

### Maintenance Windows

```python
import time

# Create maintenance
api.maintenance.create(
    name="Server Maintenance",
    active_since=int(time.time()),
    active_till=int(time.time()) + 3600,  # 1 hour
    hostids=["10084"],
    timeperiods=[{
        "timeperiod_type": 0,  # One-time
        "period": 3600
    }]
)
```

### Events and Problems

```python
# Get current problems
problems = api.problem.get(output=["eventid", "name", "severity"],
                          recent=True)

# Get events
events = api.event.get(hostids="10084",
                       time_from=int(time.time()) - 86400,
                       output="extend")
```

### History Data

```python
# Get history (value_type must match item's value_type)
# 0=float, 1=character, 2=log, 3=integer, 4=text
history = api.history.get(
    itemids="28269",
    history=0,  # float
    time_from=int(time.time()) - 3600,
    output="extend",
    sortfield="clock",
    sortorder="DESC"
)
```

## Zabbix Sender (Trapper Items)

```python
from zabbix_utils import Sender

sender = Sender(server="zabbix.example.com", port=10051)

# Send single value
response = sender.send_value("hostname", "trap.key", "value123")
print(response)  # {"processed": 1, "failed": 0, "total": 1}

# Send multiple values
from zabbix_utils import ItemValue
values = [
    ItemValue("host1", "key1", "value1"),
    ItemValue("host2", "key2", 42),
]
response = sender.send(values)
```

## Zabbix Getter (Agent Query)

```python
from zabbix_utils import Getter

agent = Getter(host="192.168.1.100", port=10050)
response = agent.get("system.uname")
print(response.value)
```

## Common Patterns

### Bulk Host Creation from CSV

```python
import csv
from zabbix_utils import ZabbixAPI

api = ZabbixAPI(url="https://zabbix.example.com")
api.login(token="your_token")

with open("hosts.csv") as f:
    for row in csv.DictReader(f):
        try:
            api.host.create(
                host=row["hostname"],
                groups=[{"groupid": row["groupid"]}],
                interfaces=[{
                    "type": 1, "main": 1, "useip": 1,
                    "ip": row["ip"], "dns": "", "port": "10050"
                }]
            )
            print(f"Created: {row['hostname']}")
        except Exception as e:
            print(f"Failed {row['hostname']}: {e}")
```

### Find Hosts Without Template

```python
# Get all hosts
all_hosts = api.host.get(output=["hostid", "host"],
                         selectParentTemplates=["templateid"])

# Filter hosts without specific template
template_id = "10001"
hosts_without = [h for h in all_hosts
                 if not any(t["templateid"] == template_id
                           for t in h.get("parentTemplates", []))]
```

### Disable Triggers by Pattern

```python
triggers = api.trigger.get(
    search={"description": "test"},
    output=["triggerid"]
)
for t in triggers:
    api.trigger.update(triggerid=t["triggerid"], status=1)  # 1=disabled
```

## Item Types Reference

| Type | Value | Description |
|------|-------|-------------|
| Zabbix agent | 0 | Active checks |
| Zabbix trapper | 2 | Passive, data pushed via sender |
| Simple check | 3 | ICMP, TCP, etc. |
| Zabbix internal | 5 | Server internal metrics |
| Zabbix agent (active) | 7 | Agent-initiated |
| HTTP agent | 19 | HTTP/REST API monitoring |
| Dependent item | 18 | Derived from master item |
| Script | 21 | Custom scripts |

## Value Types Reference

| Type | Value | Description |
|------|-------|-------------|
| Float | 0 | Numeric (float) |
| Character | 1 | Character string |
| Log | 2 | Log file |
| Unsigned | 3 | Numeric (integer) |
| Text | 4 | Text |

## Trigger Severity Reference

| Severity | Value | Color |
|----------|-------|-------|
| Not classified | 0 | Gray |
| Information | 1 | Light blue |
| Warning | 2 | Yellow |
| Average | 3 | Orange |
| High | 4 | Light red |
| Disaster | 5 | Red |

## Error Handling

```python
from zabbix_utils import ZabbixAPI
from zabbix_utils.exceptions import APIRequestError

try:
    api.host.create(host="duplicate_host", groups=[{"groupid": "2"}])
except APIRequestError as e:
    print(f"API Error: {e.message}")
    print(f"Code: {e.code}")
```

## Debugging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
# Now all API calls will be logged
```

## Scripts Reference

See `scripts/` directory for ready-to-use automation:

- `zabbix-bulk-hosts.py` - Bulk host management from CSV
- `zabbix-maintenance.py` - Create/manage maintenance windows
- `zabbix-export.py` - Export hosts/templates to JSON/XML

## Best Practices

1. **Use API tokens** over username/password when possible
2. **Limit output fields** - Always specify `output=["field1", "field2"]` instead of `output="extend"`
3. **Use search/filter** - Never fetch all objects and filter in Python
4. **Handle pagination** - Large result sets may need `limit` and `offset`
5. **Batch operations** - Use `massadd`, `massupdate` for bulk changes
6. **Error handling** - Always wrap API calls in try/except
7. **Idempotency** - Check if object exists before creating
