---
name: zoom-meeting
description: "Schedule Zoom meetings with calendar invites. Use when scheduling client calls, consultations, or any video meeting. Triggers: 'zoom meeting with...', 'schedule call with...', 'consultation with...'"
version: "1.0.0"
author: aviz85
tags:
  - zoom
  - meetings
  - scheduling
  - video-calls
enhancedBy:
  - get-contact: "Auto-lookup contact by name. Without it: ask user for email/phone directly"
  - calendar: "Check conflicts and send invites. Without it: create Zoom only"
  - whatsapp: "Notify contact to check email. Without it: skip notification"
setup: "./SETUP.md"
---

# Zoom Meeting Scheduler

Schedule Zoom meetings and send calendar invites automatically.

## Workflow

When user says "Zoom meeting with [name]":

1. **Find contact** using `get-contact` (or ask user for email)
2. **Check duplicates** - search calendar for existing meeting
3. **Check conflicts** at requested time
4. **Create Zoom meeting** → get join_url + password
5. **Create calendar event** with guest + Zoom link
6. **Send WhatsApp** (optional): "שלחתי לך הזמנה לפגישה במייל"
7. **Confirm** to user with meeting details

## Multiple Contacts

If multiple found, ask user to choose:
```
Found multiple matching "יוסי":
1. יוסי כהן (yossi@...)
2. יוסי לוי (david@...)
Which one?
```

## Setup

**First time?** See [SETUP.md](./SETUP.md) for Zoom app creation and credentials.

**Quick check:** `.env` file needs: `ZOOM_ACCOUNT_ID`, `ZOOM_CLIENT_ID`, `ZOOM_CLIENT_SECRET`

## Calendar Integration

After creating Zoom meeting, create calendar event with `guests` param to auto-send invite.
