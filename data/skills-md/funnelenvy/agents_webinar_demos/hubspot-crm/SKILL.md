---
name: hubspot-crm
description: Use when syncing contacts or lists to HubSpot CRM. Automatically uses HUBSPOT_API_TOKEN from environment.
---

# HubSpot CRM Integration

Sync contacts and lists to HubSpot using the REST API.

## Environment Variables

```bash
HUBSPOT_API_TOKEN="pat-na1-..."  # Private App token from HubSpot
```

## Quick Start

```python
import os
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

class HubSpotClient:
    """Simple HubSpot API client."""

    def __init__(self):
        self.token = os.environ.get('HUBSPOT_API_TOKEN')
        if not self.token:
            raise ValueError("HUBSPOT_API_TOKEN environment variable not set")
        self.base_url = "https://api.hubapi.com"

    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        body = json.dumps(data).encode('utf-8') if data else None
        request = Request(url, data=body, headers=headers, method=method)

        with urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
```

## Create Static List

```python
def create_static_list(client, name: str) -> str:
    """Create a static list for contacts. Returns list ID."""
    payload = {
        "name": name,
        "objectTypeId": "0-1",  # REQUIRED: 0-1 = contacts
        "processingType": "MANUAL"
    }

    result = client._request("POST", "/crm/v3/lists", payload)
    # Response is nested: {"list": {"listId": "..."}}
    list_data = result.get("list", result)
    list_id = list_data.get("listId")

    print(f"✅ Created list: {name} (ID: {list_id})")
    return list_id
```

## Search Contact by Email

```python
def search_contact(client, email: str) -> str | None:
    """Find contact by email. Returns contact ID or None."""
    payload = {
        "filterGroups": [{
            "filters": [{
                "propertyName": "email",
                "operator": "EQ",
                "value": email
            }]
        }],
        "properties": ["email"],
        "limit": 1
    }

    result = client._request("POST", "/crm/v3/objects/contacts/search", payload)
    results = result.get("results", [])
    return results[0]["id"] if results else None
```

## Create Contact

```python
def create_contact(client, email: str, firstname: str = None, lastname: str = None) -> str:
    """Create a new contact with email only (vanilla upload).

    Only uses standard HubSpot properties (email, firstname, lastname)
    to avoid errors from missing custom properties in the target account.
    """
    properties = {"email": email}
    if firstname:
        properties["firstname"] = firstname
    if lastname:
        properties["lastname"] = lastname

    result = client._request("POST", "/crm/v3/objects/contacts", {"properties": properties})
    return result["id"]
```

**Important**: Do NOT pass arbitrary CSV columns as properties. HubSpot will reject
any property names that don't exist in the target account. Only use standard fields
(email, firstname, lastname) unless you've confirmed custom properties exist.

## Add Contacts to List

```python
def add_to_list(client, list_id: str, contact_ids: list[str]):
    """Add contacts to a static list. Batches in groups of 100."""
    endpoint = f"/crm/v3/lists/{list_id}/memberships/add"

    batch_size = 100
    total_added = 0

    for i in range(0, len(contact_ids), batch_size):
        batch = contact_ids[i:i + batch_size]
        # IMPORTANT: Payload is a simple array, NOT {"recordIdsToAdd": [...]}
        result = client._request("PUT", endpoint, batch)
        added = len(result.get("recordsIdsAdded", []))
        total_added += added
        print(f"  Added batch: {added} contacts")

    print(f"✅ Added {total_added} total contacts to list")
```

## Full Upload Flow

```python
def upload_users_to_hubspot(emails: list[str], list_name: str) -> str:
    """Upload a list of email addresses to HubSpot."""
    client = HubSpotClient()

    # Create list
    list_id = create_static_list(client, list_name)

    # Find or create contacts
    contact_ids = []
    for email in emails:
        contact_id = search_contact(client, email)
        if not contact_id:
            contact_id = create_contact(client, email)
        contact_ids.append(contact_id)

    # Add to list
    add_to_list(client, list_id, contact_ids)

    print(f"\n✅ Complete!")
    print(f"   List: https://app.hubspot.com/contacts/lists/{list_id}")

    return list_id
```

## Usage Example

```python
# Upload at-risk users from analysis
at_risk_emails = [
    "user_001@demo.reformapp.com",
    "user_002@demo.reformapp.com",
    "user_003@demo.reformapp.com"
]

list_id = upload_users_to_hubspot(
    emails=at_risk_emails,
    list_name="At-Risk Trial Users - Dec 2024"
)
```

## Using the Integration Script

For CSV files, use the provided script:

```bash
.venv/bin/python demos/04-trial-to-paid/scripts/hubspot_integration.py \
  path/to/users.csv \
  "List Name Here"
```

The CSV must have an `email` column.

## API Gotchas

1. **List creation requires `objectTypeId`**: Always include `"objectTypeId": "0-1"` for contacts
2. **Response is nested**: List ID is at `result["list"]["listId"]`, not `result["listId"]`
3. **Add-to-list payload format**: Use simple array `["id1", "id2"]`, NOT `{"recordIdsToAdd": [...]}`
4. **Contact IDs are strings**: Even though they look numeric, treat them as strings
5. **Batch limit**: Add contacts in batches of 100 max

## Error Handling

```python
from urllib.error import HTTPError

try:
    result = client._request("POST", endpoint, payload)
except HTTPError as e:
    error_body = e.read().decode('utf-8')
    print(f"HubSpot API error: {e.code}")
    print(f"  {error_body}")
```

## Getting Your HubSpot Private App Token

1. Go to **Settings** (gear icon) in HubSpot
2. Navigate to **Integrations** > **Private Apps**
3. Click **Create a private app**
4. Give it a name (e.g., "AI Agent Integration")
5. Under **Scopes**, enable:
   - `crm.lists.read`
   - `crm.lists.write`
   - `crm.objects.contacts.read`
   - `crm.objects.contacts.write`
6. Click **Create app** and copy the token
7. Set as `HUBSPOT_API_TOKEN` environment variable
