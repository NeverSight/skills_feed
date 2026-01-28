---
name: get-contact
description: "Find contact details by name. Searches local contacts/CRM and returns email/phone. Use before scheduling meetings or sending messages when you need contact info."
version: "1.0.0"
author: aviz85
tags:
  - contacts
  - crm
  - utility
usedBy:
  - zoom-meeting
  - whatsapp
  - gmail
---

# Get Contact

Find contact details (email, phone) by name search.

## Sources

Configure your contact sources. Examples:
- **Local JSON** - `~/contacts.json` or your CRM data file
- **Google Contacts** - via People API (future)
- **Any CRM** - adapt the search to your system

## Usage

When you need contact info:

1. Search contacts for name (partial match, case insensitive)
2. If **0 results** → tell user "not found, please provide email/phone"
3. If **1 result** → confirm with user: "Found [name] - [email]. Is this correct?"
4. If **multiple results** → ask user to choose: "Found multiple: 1) Name A 2) Name B"

## IMPORTANT

**Always confirm with user before using contact info.** Common names (יוסי, דוד, John, David) may have multiple people or user may mean someone not in contacts.

## Search Example (JSON)

```bash
# Search by name in contacts file
jq '.contacts[] | select(.name | test("QUERY"; "i")) | {name, email, phone}' ~/contacts.json
```

## Response Format

Return to calling skill:
```json
{
  "found": true,
  "count": 1,
  "contact": {
    "name": "John Smith",
    "email": "john@example.com",
    "phone": "+1234567890"
  }
}
```

Or if multiple:
```json
{
  "found": true,
  "count": 2,
  "contacts": [
    {"name": "John Smith", "email": "john.s@...", "phone": "..."},
    {"name": "John Doe", "email": "john.d@...", "phone": "..."}
  ]
}
```

## Configuration

Create a contacts file or configure your data source path:

```json
// ~/contacts.json
{
  "contacts": [
    {
      "name": "John Smith",
      "email": "john@example.com",
      "phone": "+1234567890"
    }
  ]
}
```

Update the search path in the skill to match your setup.

## Integration

Other skills (zoom-meeting, whatsapp) use this skill to lookup contacts. If this skill isn't available, those skills will ask the user for contact details directly.
