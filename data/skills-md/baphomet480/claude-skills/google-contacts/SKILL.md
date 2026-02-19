---
name: google-contacts
description: Full CRUD Google Contacts interactions — search, list, get, create, update, and delete contacts.
---

# Google Contacts Skill

Full CRUD Contacts management for AI agents. Search, list, get, create, update, and delete contacts.

## Features

- **Search**: Find contacts by name, email, or phone.
- **List**: Paginated listing of all contacts (sorted by last name).
- **Get**: Fetch a single contact by resource name with full details.
- **Create**: Add contacts with name, email, phone, organization, title, and notes.
- **Update**: Patch existing contacts (etag-based conflict detection).
- **Delete**: Remove contacts.

## Prerequisites

1.  **Google Cloud Project** with **Google People API** enabled.
2.  **OAuth 2.0 Credentials** — either `gcloud` ADC or `credentials.json`.

## Setup

### ⚡ Quick Setup (Recommended)

Set up Gmail, Calendar, and Contacts all at once:

```bash
uv run ~/.agents/skills/gmail/scripts/setup_workspace.py
```

### Manual Setup

1.  **Using gcloud ADC**:

    ```bash
    gcloud auth application-default login \
      --scopes https://www.googleapis.com/auth/contacts,https://www.googleapis.com/auth/cloud-platform
    ```

    Then verify:

    ```bash
    uv run skills/google-contacts/scripts/contacts.py verify
    ```

2.  **Alternative (credentials.json)**:
    - Place `credentials.json` in `~/.contacts_credentials/`.
    - Run `uv run skills/google-contacts/scripts/contacts.py setup`

## Usage

### Search Contacts

```bash
# Find Han Solo
uv run skills/google-contacts/scripts/contacts.py search --query "Han Solo"

# Find by email
uv run skills/google-contacts/scripts/contacts.py search --query "falcon.net" --limit 5
```

### List All Contacts

```bash
# First page
uv run skills/google-contacts/scripts/contacts.py list --limit 50

# Subsequent pages (use nextPageToken from previous result)
uv run skills/google-contacts/scripts/contacts.py list --page-token "NEXT_PAGE_TOKEN"
```

### Get a Single Contact

```bash
uv run skills/google-contacts/scripts/contacts.py get --id "people/c12345"
```

### Create a Contact

```bash
uv run skills/google-contacts/scripts/contacts.py create \
  --first "Lando" \
  --last "Calrissian" \
  --email "lando@cloudcity.com" \
  --phone "555-0123" \
  --org "Cloud City Administration" \
  --title "Baron Administrator" \
  --notes "Old gambling buddy"
```

### Update a Contact

Only provided fields change. The script auto-fetches the current `etag` for conflict detection:

```bash
uv run skills/google-contacts/scripts/contacts.py update \
  --id "people/c12345" \
  --phone "555-9999" \
  --title "General"
```

### Delete a Contact

```bash
uv run skills/google-contacts/scripts/contacts.py delete --id "people/c12345"
```

## JSON Output

**Contact:**

```json
{
  "resourceName": "people/c12345",
  "name": "Han Solo",
  "givenName": "Han",
  "familyName": "Solo",
  "emails": [{ "value": "captain@falcon.net", "type": "work" }],
  "phones": [{ "value": "555-0987", "type": "mobile" }],
  "organizations": [{ "name": "Rebel Alliance", "title": "General" }],
  "addresses": [{ "formatted": "Millennium Falcon", "type": "home" }],
  "biography": "Shot first.",
  "urls": [],
  "birthday": null
}
```

**List Result (paginated):**

```json
{
  "contacts": [ ... ],
  "totalItems": 142,
  "nextPageToken": "NEXT_PAGE_TOKEN"
}
```
