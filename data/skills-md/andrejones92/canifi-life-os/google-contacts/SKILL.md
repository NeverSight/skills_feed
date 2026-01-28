---
name: google-contacts
description: Enables Claude to create, search, and manage contacts in Google Contacts via Playwright MCP
category: google
---

# Google Contacts Skill

## Overview
Claude can manage your Google Contacts to add new contacts, search for people, organize with labels, and maintain your address book. Integrates with Gmail, Calendar, and other Google services.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/google-contacts/install.sh | bash
```

Or manually:
```bash
cp -r skills/google-contacts ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GOOGLE_EMAIL "your-email@gmail.com"
```

## Privacy & Authentication

**Your credentials, your choice.** Canifi LifeOS respects your privacy.

### Option 1: Manual Browser Login (Recommended)
If you prefer not to share credentials with Claude Code:
1. Complete the [Browser Automation Setup](/setup/automation) using CDP mode
2. Login to the service manually in the Playwright-controlled Chrome window
3. Claude will use your authenticated session without ever seeing your password

### Option 2: Environment Variables
If you're comfortable sharing credentials, you can store them locally:
```bash
canifi-env set SERVICE_EMAIL "your-email"
canifi-env set SERVICE_PASSWORD "your-password"
```

**Note**: Credentials stored in canifi-env are only accessible locally on your machine and are never transmitted.

## Capabilities
- Create new contacts with details
- Search contacts by name, email, or phone
- Edit existing contact information
- Organize contacts with labels
- Merge duplicate contacts
- Import and export contacts
- View contact interaction history
- Add photos to contacts
- Create contact groups
- Share contacts with others
- Sync contacts across devices
- Delete and restore contacts

## Usage Examples

### Example 1: Add Contact
```
User: "Add John Smith to my contacts: phone 555-1234, email john@example.com"
Claude: Creates contact with provided details.
        Confirms: "Added John Smith with phone and email"
```

### Example 2: Find Contact
```
User: "What's Sarah's phone number?"
Claude: Searches contacts for "Sarah", returns phone number.
        Reports: "Sarah Johnson: (555) 987-6543"
```

### Example 3: Organize Contacts
```
User: "Add all my coworkers to a 'Work' label"
Claude: Identifies work contacts, adds to Work label.
        Confirms: "Added 15 contacts to 'Work' label"
```

### Example 4: Update Contact
```
User: "Update Mike's email to mike.new@example.com"
Claude: Finds Mike, updates email address.
        Confirms: "Updated Mike's email address"
```

## Authentication Flow
1. Claude navigates to contacts.google.com via Playwright MCP
2. Authenticates with GOOGLE_EMAIL if needed
3. Handles 2FA if prompted (notifies user via iMessage)
4. Maintains session for subsequent Contacts operations

## Selectors Reference
```javascript
// Create contact button
'[aria-label="Create contact"]'

// Search box
'input[aria-label="Search"]'

// Contact list
'.XXcuqd' // Contact rows

// Contact name
'.oiNmbb'

// Edit button
'[aria-label="Edit"]'

// Name field
'input[aria-label="First name"]'
'input[aria-label="Last name"]'

// Email field
'input[aria-label="Email"]'

// Phone field
'input[aria-label="Phone"]'

// Save button
'[aria-label="Save"]'

// Labels
'[aria-label="Labels"]'

// Delete contact
'[aria-label="Delete"]'

// Merge duplicates
'[aria-label="Merge & fix"]'
```

## Contact Fields
```
First name, Last name
Company, Job title
Email (multiple, with labels: Home, Work, Other)
Phone (multiple, with labels: Mobile, Home, Work)
Address (Street, City, State, Zip, Country)
Birthday
Notes
Website
Relationship (Spouse, Child, etc.)
Custom fields
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Contact Not Found**: Search with variations, ask user to clarify
- **Duplicate Detected**: Notify user, offer to merge
- **Save Failed**: Retry, report any validation errors
- **Import Failed**: Check file format, report specific issues

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Google Contacts:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific search tips or organization strategies
4. Note any sync behavior improvements

## Notes
- Contacts sync across all Google services
- Import formats: CSV, vCard (.vcf)
- Export formats: CSV, vCard
- Duplicate detection available in "Merge & fix"
- Deleted contacts recoverable for 30 days
- Contact photos sync with Google account
- Labels help organize contacts into groups
- "Other contacts" contains auto-saved contacts from email
- Frequent contacts shown in Gmail compose suggestions
